"""
town_stress2.py -- the two town stresses still owed after town_stress_T13.py (stress objective #4b):
  mem    fishers who CONSULT YESTERDAY'S SEA. Yesterday's fish ground is public at day's end. A Bayesian fisher
         whose reading disagrees with yesterday's ground follows yesterday iff
             a (1-acc)/3 > b acc,   a = rho_G + (1-rho_G)/4,  b = (1-rho_G)/4
         (for 70% readers: iff the sea persists with rho_G > 0.6). Readers and master each apply the rule at their
         own accuracy. Where the rule fires, every reader goes to the same ground: the remembered sea is a public
         signal, and the town is one head with the sea's accuracy.
  Yc     a master who fishes for himself and MISDIRECTS WHEN IT PAYS: he announces a wrong ground whenever his
         following k exceeds Yc boats (the point where followers would crowd his own catch). Yc = 0 means honest.
Other axes as before: master accuracy q, sea memory rho_G, reader-error persistence rho_err.
Town: 4 grounds, 9 boats, 90 days, good day = at least 5 boats on the fish, famine = 3 bad days running.
Usage: python town_stress2.py --seasons 20000     (GPU if available; ~144 configs x 10 doses)  ;  --smoke
Output: results_town2/town_stress2.csv ; summarize with summarize_town_stress2.py
"""
import os, time, argparse, itertools, csv
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'results_town2')
nG, N, DAYS, ST, P_READ = 4, 9, 90, 3, 0.7
GRID = dict(q=[0.8, 0.9, 0.99], rho_G=[0.0, 0.5, 0.7, 0.9], mem=[0, 1], Yc=[0, 2, 4], rho_err=[0.0, 0.5])


def follows_yesterday(acc, rho_G):
    a = rho_G + (1 - rho_G) / nG; b = (1 - rho_G) / nG
    return a * (1 - acc) / (nG - 1) > b * acc


def season_famine(cfg, k, S, dev, gen):
    q, rho_G, mem, Yc, rho_err = cfg['q'], cfg['rho_G'], int(cfg['mem']), int(cfg['Yc']), cfg['rho_err']
    nread = N - k
    U = lambda *shape: torch.rand(*shape, device=dev, generator=gen)
    RI = lambda lo, hi, shape: torch.randint(lo, hi, shape, device=dev, generator=gen)
    Gprev = RI(0, nG, (S,))
    wrong_r = U(S, max(nread, 1)) < (1 - P_READ)
    streak = torch.zeros(S, dtype=torch.int8, device=dev); famine = torch.zeros(S, dtype=torch.bool, device=dev)
    r_mem = bool(mem) and follows_yesterday(P_READ, rho_G); m_mem = bool(mem) and follows_yesterday(q, rho_G)
    liar = Yc > 0 and k > Yc
    for d in range(DAYS):
        G = torch.where(U(S) < rho_G, Gprev, RI(0, nG, (S,)))
        if nread > 0:
            fresh = U(S, nread) < (1 - P_READ)
            wrong_r = torch.where(U(S, nread) < rho_err, wrong_r, fresh)
            own = torch.where(wrong_r, (G[:, None] + RI(1, nG, (S, nread))) % nG, G[:, None])
            pick = Gprev[:, None].expand(S, nread) if r_mem else own
            on_readers = (pick == G[:, None]).sum(1)
        else:
            on_readers = torch.zeros(S, dtype=torch.long, device=dev)
        m_wrong = U(S) < (1 - q)
        call = torch.where(m_wrong, (G + RI(1, nG, (S,))) % nG, G)
        if m_mem:
            call = Gprev
        announce = (call + RI(1, nG, (S,))) % nG if liar else call
        on = on_readers + (announce == G).long() * k
        bad = on < 5
        streak = torch.where(bad, streak + 1, torch.zeros_like(streak))
        famine |= streak >= ST
        Gprev = G
    return float(famine.float().mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seasons', type=int, default=20000); ap.add_argument('--smoke', action='store_true'); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    gen = torch.Generator(device=dev); gen.manual_seed(a.seed)
    os.makedirs(OUT, exist_ok=True)
    keys = list(GRID); configs = [dict(zip(keys, v)) for v in itertools.product(*GRID.values())]
    if a.smoke:
        configs = [c for c in configs if c['q'] == 0.8 and c['rho_err'] == 0.0 and c['rho_G'] in (0.0, 0.9) and c['Yc'] in (0, 2)]
        a.seasons = 4000
    path = os.path.join(OUT, 'town_stress2.csv'); done = set()
    if os.path.exists(path):
        for row in csv.DictReader(open(path, encoding='utf-8')):
            done.add(tuple(float(row[k]) for k in keys))
    print(f"{dev}: {len(configs)} configs, {len(done)} done, {a.seasons} seasons each", flush=True)
    newfile = not os.path.exists(path); t0 = time.time()
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if newfile:
            w.writerow(keys + [f'famine_k{k}' for k in range(N + 1)])
        for i, cfg in enumerate(configs):
            if tuple(float(cfg[k]) for k in keys) in done:
                continue
            fam = [season_famine(cfg, k, a.seasons, dev, gen) for k in range(N + 1)]
            w.writerow([cfg[k] for k in keys] + [f"{x:.5f}" for x in fam]); f.flush()
            if a.smoke or (i + 1) % 12 == 0:
                print(f"  {i+1}/{len(configs)} {cfg} k0 {fam[0]:.3f} k1 {fam[1]:.3f} k5 {fam[5]:.3f} k9 {fam[9]:.3f} [{time.time()-t0:.0f}s]", flush=True)
    print('done.', flush=True)


if __name__ == '__main__':
    main()
