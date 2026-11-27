"""
living_town_skill.py -- stress objective #6: the acting -> reading conjecture, made a model and swept.

The living town (living_town_S1.py): N = 9 fishers, 4 grounds, a hub right w.p. q, each fisher chooses
daily between following the hub and acting on his own reading (EMA of payoffs, softmax, exploration);
finite fish split among boats on the fish ground (the crowding penalty that de-herds the town).
THE ONE NEW INGREDIENT: a fisher's reading accuracy is a SKILL that decays with disuse and recovers with use:
    p_i <- p_i - lam * (p_i - 1/nG)   on a day he follows the hub      (calibration decays toward chance)
    p_i <- p_i + mu  * (p_max - p_i)  on a day he acts on his reading  (one's own mistakes recalibrate)
Question: starting from an established broadcast town (everyone follows), is there a point of no return --
a decay rate past which the town can no longer de-herd because by the time crowding makes reading pay,
nobody can read? Sweeps lam, mu, hub accuracy q, yield Y (crowding strength), and the initial skill.
Outputs, per configuration: long-run hub fraction, mean skill, majority-hit rate, famine proxy, and whether
the town converted (hub fraction < 0.5 at the end). GPU (torch) vectorized over runs; CPU fallback.
Usage: python living_town_skill.py --runs 2000 --days 600 --shard 0 --nshards 6 ; --smoke ; then summarize_living_town_skill.py
"""
import os, sys, time, argparse, itertools, csv
import numpy as np
try:
    import torch
except ImportError:
    torch = None

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'results_living2')
N, nG = 9, 4
# Y = boatloads of fish on the fish ground (each boat can land one boatload): Y = 1 is the strongest crowding
# (catch 1/k, the first run's payoff, where the old Y axis was normalized away and so was vacuous), Y = 9 is the
# glass sea (no crowding at N = 9).
GRID = dict(lam=[0.0, 0.002, 0.005, 0.01, 0.02, 0.05], mu=[0.005, 0.02, 0.05], q=[0.8, 0.9],
            Y=[1.0, 3.0, 5.0, 9.0], p0=[0.7], p_max=[0.7])
alpha, temp, eps = 0.15, 0.15, 0.05


def simulate(cfg, R, days, dev, gen):
    lam, mu, q, Y, p0, p_max = (cfg[k] for k in ['lam', 'mu', 'q', 'Y', 'p0', 'p_max'])
    U = lambda *shape: torch.rand(*shape, device=dev, generator=gen)
    init = [1.0, 0.2] if cfg.get('init', 'hub') == 'hub' else [0.2, 1.0]   # [hub, self]: broadcast town, or a town of readers
    ema = torch.tensor(init, device=dev).repeat(R, N, 1)
    p = torch.full((R, N), p0, device=dev)
    hub_frac = torch.zeros(days, device=dev); maj = torch.zeros(days, device=dev); skill = torch.zeros(days, device=dev)
    for d in range(days):
        F = torch.randint(0, nG, (R,), device=dev, generator=gen)
        hub_call = torch.where(U(R) < q, F, torch.randint(0, nG, (R,), device=dev, generator=gen))
        own_call = torch.where(U(R, N) < p, F[:, None], torch.randint(0, nG, (R, N), device=dev, generator=gen))
        prob_self = torch.softmax(ema / temp, dim=2)[:, :, 1]
        choose_self = U(R, N) < prob_self
        explore = U(R, N) < eps
        choose_self = torch.where(explore, U(R, N) < 0.5, choose_self)
        pick = torch.where(choose_self, own_call, hub_call[:, None])
        on = pick == F[:, None]
        k = on.sum(1, keepdim=True).clamp(min=1)
        pay = torch.where(on, (Y / k).clamp(max=1.0), torch.zeros_like(p)) * 3.0     # per-boat catch = min(1, Y/k) boatloads
        idx = choose_self.long()
        upd = (1 - alpha) * torch.gather(ema, 2, idx[..., None]).squeeze(-1) + alpha * pay
        ema.scatter_(2, idx[..., None], upd[..., None])
        # skill dynamics
        p = torch.where(choose_self, p + mu * (p_max - p), p - lam * (p - 1.0 / nG))
        hub_frac[d] = (~choose_self).float().mean(); maj[d] = (on.sum(1) >= 5).float().mean(); skill[d] = p.mean()
    last = slice(days - 60, days)
    return dict(hub_frac_end=float(hub_frac[last].mean()), hub_frac_d100=float(hub_frac[90:110].mean()),
                skill_end=float(skill[last].mean()), maj_end=float(maj[last].mean()), maj_early=float(maj[:30].mean()),
                converted=float((hub_frac[last].mean() < 0.5).float()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', type=int, default=2000); ap.add_argument('--days', type=int, default=600)
    ap.add_argument('--shard', type=int, default=0); ap.add_argument('--nshards', type=int, default=1)
    ap.add_argument('--smoke', action='store_true'); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    if torch is None:
        raise SystemExit('torch required')
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    gen = torch.Generator(device=dev); gen.manual_seed(a.seed + 1000 * a.shard)
    os.makedirs(OUT, exist_ok=True)
    keys = list(GRID); configs = [dict(zip(keys, v)) for v in itertools.product(*GRID.values())]
    if a.smoke:
        configs = [c for c in configs if c['mu'] == 0.02 and c['q'] == 0.8 and c['Y'] == 1.0 and c['p0'] == 0.7]
        a.runs, a.days = 300, 300
    mine = configs[a.shard::a.nshards]
    path = os.path.join(OUT, f'living_skill_{a.shard:02d}.csv'); done = set()
    if os.path.exists(path):
        for row in csv.DictReader(open(path, encoding='utf-8')):
            done.add(tuple(float(row[k]) for k in keys))
    print(f"{dev}: {len(mine)} configs, {len(done)} done, runs={a.runs} days={a.days}", flush=True)
    newfile = not os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f); t0 = time.time()
        outkeys = ['hub_frac_end', 'hub_frac_d100', 'skill_end', 'maj_end', 'maj_early', 'converted']
        if newfile:
            w.writerow(keys + outkeys)
        for i, cfg in enumerate(mine):
            if tuple(float(cfg[k]) for k in keys) in done:
                continue
            r = simulate(cfg, a.runs, a.days, dev, gen)
            w.writerow([cfg[k] for k in keys] + [f"{r[k]:.4f}" for k in outkeys]); f.flush()
            if a.smoke or (i + 1) % 10 == 0:
                print(f"  {i+1}/{len(mine)} {cfg} -> hub_end {r['hub_frac_end']:.3f} skill_end {r['skill_end']:.3f} maj_end {r['maj_end']:.3f} [{time.time()-t0:.0f}s]", flush=True)
    print('done.', flush=True)


if __name__ == '__main__':
    main()
