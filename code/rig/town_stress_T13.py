"""
town_stress_T13.py -- stress objective #4: the fishing town (Theorem 13) under lying masters, remembering
seas, persistent reader errors and shared blindness. Monte Carlo on GPU (torch) with CPU fallback.

Town (fishing_town_T13.py): n = 4 grounds, N = 9 boats, 90-day season, a good day is >= 5 boats on the
fish ground, famine = 3 consecutive bad days. Readers are right w.p. p (= 0.7 at the book's constants);
the master w.p. q; k boats follow the master, N - k read for themselves.
Extensions, each a parameter:
  rho_G     the fish ground persists day to day w.p. rho_G (else fresh uniform draw)      -- remembering sea
  rho_err   a reader who was wrong yesterday is wrong again today w.p. rho_err (else fresh) -- bad weeks
  c         w.p. c the day is 'blind': every reader sees the same false ground            -- shared blindness (T14)
  rho_h     the master's error persists w.p. rho_h                                          -- a master in a slump
  lie       on a day the master knows the ground, w.p. lie he announces a wrong one       -- strategic misdirection
Output: famine probability per configuration and follower dose k = 0..9, in results_town/town_stress_<shard>.csv.
Usage:  python town_stress_T13.py --seasons 20000 --shard 0 --nshards 6      (one process per GPU via CUDA_VISIBLE_DEVICES)
        python town_stress_T13.py --smoke
Summarize: python summarize_town_stress.py
"""
import os, sys, time, argparse, itertools, csv
import numpy as np
try:
    import torch
except ImportError:
    torch = None

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'results_town')
nG, N, DAYS, ST = 4, 9, 90, 3
GRID = dict(q=[0.7, 0.8, 0.9, 0.99], p=[0.7], rho_G=[0.0, 0.5, 0.9], rho_err=[0.0, 0.5, 0.9],
            c=[0.0, 0.1, 0.3], rho_h=[0.0, 0.5, 0.9], lie=[0.0, 0.1, 0.3])


def season_famine(cfg, k, S, dev, gen):
    """Famine probability over S simulated seasons for k master-followers. Vectorized over seasons."""
    q, p, rho_G, rho_err, c, rho_h, lie = (cfg[x] for x in ['q', 'p', 'rho_G', 'rho_err', 'c', 'rho_h', 'lie'])
    nread = N - k
    U = lambda *shape: torch.rand(*shape, device=dev, generator=gen)
    G = torch.randint(0, nG, (S,), device=dev, generator=gen)
    wrong_r = U(S, nread) < (1 - p)                 # yesterday's reader error flags (start fresh)
    wrong_h = U(S) < (1 - q)
    streak = torch.zeros(S, dtype=torch.int8, device=dev); famine = torch.zeros(S, dtype=torch.bool, device=dev)
    for d in range(DAYS):
        G = torch.where(U(S) < rho_G, G, torch.randint(0, nG, (S,), device=dev, generator=gen))
        # readers: persistent error or fresh draw
        fresh_wrong = U(S, nread) < (1 - p)
        wrong_r = torch.where(U(S, nread) < rho_err, wrong_r, fresh_wrong)
        blind = U(S) < c
        false_common = (G + torch.randint(1, nG, (S,), device=dev, generator=gen)) % nG   # a shared wrong ground
        false_own = (G[:, None] + torch.randint(1, nG, (S, nread), device=dev, generator=gen)) % nG
        reader_pick = torch.where(wrong_r, false_own, G[:, None])
        reader_pick = torch.where(blind[:, None], false_common[:, None], reader_pick)
        on_readers = (reader_pick == G[:, None]).sum(1)
        # master: persistent error or fresh; a lie sends followers wrong on a day he knows
        fresh_wrong_h = U(S) < (1 - q)
        wrong_h = torch.where(U(S) < rho_h, wrong_h, fresh_wrong_h)
        lies = (~wrong_h) & (U(S) < lie)
        master_right = (~wrong_h) & (~lies)
        on = on_readers + torch.where(master_right, torch.full_like(on_readers, k), torch.zeros_like(on_readers))
        bad = on < 5
        streak = torch.where(bad, streak + 1, torch.zeros_like(streak))
        famine |= streak >= ST
    return float(famine.float().mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seasons', type=int, default=20000); ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--nshards', type=int, default=1); ap.add_argument('--smoke', action='store_true'); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    if torch is None:
        raise SystemExit('torch required (pip install torch)')
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    gen = torch.Generator(device=dev); gen.manual_seed(a.seed + 1000 * a.shard)
    os.makedirs(OUT, exist_ok=True)
    keys = list(GRID); configs = [dict(zip(keys, vals)) for vals in itertools.product(*GRID.values())]
    if a.smoke:
        configs = [c for c in configs if c['rho_G'] == 0 and c['rho_err'] == 0 and c['c'] == 0 and c['rho_h'] == 0 and c['lie'] == 0]
        a.seasons = 20000
    mine = configs[a.shard::a.nshards]
    path = os.path.join(OUT, f'town_stress_{a.shard:02d}.csv')
    done = set()
    if os.path.exists(path):
        for row in csv.DictReader(open(path, encoding='utf-8')):
            done.add(tuple(float(row[k]) for k in keys))
    print(f"{dev}: {len(mine)} configs in this shard, {len(done)} done, {a.seasons} seasons each", flush=True)
    newfile = not os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if newfile:
            w.writerow(keys + [f'famine_k{k}' for k in range(N + 1)])
        t0 = time.time()
        for i, cfg in enumerate(mine):
            if tuple(float(cfg[k]) for k in keys) in done:
                continue
            fam = [season_famine(cfg, k, a.seasons, dev, gen) for k in range(N + 1)]
            w.writerow([cfg[k] for k in keys] + [f"{x:.5f}" for x in fam]); f.flush()
            if a.smoke or (i + 1) % 20 == 0:
                print(f"  {i+1}/{len(mine)}  {cfg}  famine k=0 {fam[0]:.4f}  k=1 {fam[1]:.4f}  k=9 {fam[9]:.4f}  [{time.time()-t0:.0f}s]", flush=True)
    print('done.', flush=True)


if __name__ == '__main__':
    main()
