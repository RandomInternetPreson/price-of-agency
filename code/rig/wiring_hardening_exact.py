"""
wiring_hardening_exact.py -- Ch 15 §2 "the wiring theorem, hardened": exact floors
(no sampling) for a continuum of wirings between gated and additive, plus random
wirings, across worlds, policies, habit-space sizes and coin sizes. CPU only,
multiprocessing; minutes on a many-core Xeon.

The dichotomy as printed (T11, T11', Door-2 note): gated floors saturate strictly
below the sage at every h; additive floors rise to the seed-unknown value d0 at
h = 3. Two named wirings do not make a theorem. This sweep asks what the floor is a
function OF, by varying the only thing the two wirings differ in -- how far the
fresh bits reach across the quantile axis:
  span:d   cell(S,U) = (S + U*d) mod M,  d in {1, 2, 4, ..., m_S}   (d=1 contiguous
           window = gated-like; d = m_S = additive at full resolution)
  random:k random bijection of cells (k = 1..K)
and reporting, per configuration, (d0, delta_inf, sage, wall) and the summary
statistic REACH = (d * (m_U - 1) + 1) / M, the fraction of the quantile axis a
habit's fresh bits can reach.

Output: results_exact/wiring_hardening.csv and wiring_hardening_SUMMARY.md with
  (a) the floor vs reach curve per (n, s, policy, m_S, h)   -- is it monotone? a step?
  (b) random wirings' floors vs the additive floor           -- are generic wirings additive-like?
  (c) the dichotomy check: every gated-like (d=1) floor < sage?  every additive floor at
      h >= 3 within 1e-3 of d0?  (a single counterexample is a refutation and is printed first)
  (d) the sandwich check per config: wall <= floor <= sage (T9')
Usage: python wiring_hardening_exact.py [--workers N] [--quick]
"""
import argparse, csv, itertools, os, sys, time
from multiprocessing import Pool
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import and_world as aw


def one(job):
    n, s, pname, m_S, h, wiring = job
    w = aw.World(n, s)
    pol = w.policy(pname)
    aim, dA_E, wall = w.stats(pol)
    m_U = 2 ** h
    G = aw.action_table(pol, aw.quantile_map(wiring, m_S, m_U), m_S, m_U)
    L_F, L = aw.lik_tables(G, w)
    d0, dinf = aw.exact_floors(L, w)
    # the finite quantile grid REALIZES a slightly different policy than pol; the T9' wall must be
    # computed for the realized one (pol_real = P(A|F,E) with S,U marginalized), else the check
    # fails spuriously at small reach where the window sits inside one quantile bin.
    wall_ideal = wall
    _, _, wall = w.stats(L_F.mean(0))
    M = m_S * m_U
    if wiring.startswith('span:'):
        d = int(wiring.split(':')[1]); reach = (d * (m_U - 1) + 1) / M
    elif wiring == 'gated':
        reach = m_U / M
    elif wiring in ('additive', 'additive:c'):
        reach = 1.0
    else:
        reach = float('nan')
    return dict(n=n, s=s, policy=pname, m_S=m_S, h=h, wiring=wiring, reach=reach, sage=w.sage, wall=wall, wall_ideal=wall_ideal,
                aim=aim, d0=d0, dinf=dinf, inverted=dinf < w.sage - 1e-9,
                otp_equal=abs(dinf - d0) < 1e-3,
                # T9' lower wall binds every seed-known floor (U unknown is still part of R);
                # the sage upper wall binds only the fully-surveilled floor, i.e. h = 0 (U trivial).
                sandwich_ok=(wall - 1e-9 <= dinf) and (h > 0 or dinf <= w.sage + 1e-9),
                # printed-additive one-time-pad law: L[S] is S-independent iff m_S | m_U, i.e. h >= log2 m_S
                otp_predicted=(m_U % m_S == 0))


def jobs(quick):
    ns = [4, 6]; ss = [0.3, 0.5, 0.7]; pols = ['lam', 'hand']
    mSs = [8, 64, 1024] if not quick else [8, 64]
    hs = [0, 1, 2, 3, 4] if not quick else [1, 2, 3]
    K = 8 if not quick else 3
    out = []
    for n, s, p, m_S, h in itertools.product(ns, ss, pols, mSs, hs):
        wirings = ['gated', 'additive', 'additive:c']
        d = 1
        while d <= m_S:
            wirings.append(f'span:{d}'); d *= 2
        wirings += [f'random:{k}' for k in range(1, K + 1)]
        out += [(n, s, p, m_S, h, wname) for wname in wirings]
    # the one-time-pad law needs h up to log2 m_S (key as long as the habit): additive only, h <= 7
    for n, s, p, m_S in itertools.product(ns, ss, pols, mSs):
        for h in range(max(hs) + 1, min(int(np.log2(m_S)) + 1, 7) + 1):
            out.append((n, s, p, m_S, h, 'additive'))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--out', default=os.path.join(HERE, 'results_exact'))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    J = jobs(args.quick)
    print(f"{len(J)} exact configurations on {args.workers} workers")
    t0 = time.time()
    with Pool(args.workers) as pool:
        rows = pool.map(one, J, chunksize=4)
    print(f"done in {time.time() - t0:.0f}s")
    csvp = os.path.join(args.out, 'wiring_hardening.csv')
    with open(csvp, 'w', newline='', encoding='utf-8') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)

    md = ["# Wiring theorem, hardened — exact floors\n",
          f"{len(rows)} configurations; n ∈ {{4,6}}, s ∈ {{0.3,0.5,0.7}}, policies lam/hand, m_S ∈ {sorted({r['m_S'] for r in rows})}, "
          f"h ∈ {sorted({r['h'] for r in rows})}. All exact enumeration (no sampling). Model-world quantities only.\n"]
    # (c) refutation hunt first
    bad_g = [r for r in rows if r['wiring'] in ('gated', 'span:1') and r['h'] >= 1 and not r['inverted']]
    bad_a = [r for r in rows if r['wiring'] == 'additive' and r['h'] >= 3 and not r['otp_equal']]
    # exact law: predicted-equal configs must match d0 to machine precision; predicted-unequal must not be exactly equal
    law_bad = [r for r in rows if r['wiring'] == 'additive' and r['otp_predicted'] and abs(r['dinf'] - r['d0']) > 1e-9]
    law_extra = [r for r in rows if r['wiring'] == 'additive' and not r['otp_predicted'] and abs(r['dinf'] - r['d0']) < 1e-12]
    bad_s = [r for r in rows if not r['sandwich_ok']]
    md.append("## Refutation hunt\n")
    md.append(f"- gated-like (gated, span:1) floors NOT below the sage at h ≥ 1: **{len(bad_g)}** of "
              f"{sum(1 for r in rows if r['wiring'] in ('gated', 'span:1') and r['h'] >= 1)}")
    for r in bad_g[:20]:
        md.append(f"  - n={r['n']} s={r['s']} {r['policy']} m_S={r['m_S']} h={r['h']} {r['wiring']}: floor {r['dinf']:.4f} vs sage {r['sage']:.4f}")
    md.append(f"- additive (printed formula) at h ≥ 3 NOT within 1e-3 of seed-unknown d0: **{len(bad_a)}** of "
              f"{sum(1 for r in rows if r['wiring'] == 'additive' and r['h'] >= 3)}")
    for r in bad_a[:20]:
        md.append(f"  - n={r['n']} s={r['s']} {r['policy']} m_S={r['m_S']} h={r['h']}: floor {r['dinf']:.4f} vs d0 {r['d0']:.4f}")
    md.append(f"- one-time-pad LAW, sufficiency (m_S | m_U, i.e. h ≥ log2 m_S for the printed additive formula ⇒ EXACT equality; "
              f"proof: the quantile set {{(S+0.5)/m_S + (U+0.5)/m_U mod 1}} is then the same grid for every S) violated: "
              f"**{len(law_bad)}** of {sum(1 for r in rows if r['wiring'] == 'additive' and r['otp_predicted'])} predicted-equal configs. "
              f"Necessity is generic, not exact: {len(law_extra)} configs reach equality early by saturation at d0 = 1 "
              f"(of {sum(1 for r in rows if r['wiring'] == 'additive' and not r['otp_predicted'])}).")
    md.append("  Gap d0 − floor by h (printed additive, mean over n, s, policy): " + "; ".join(
        f"m_S={m_S}: " + ", ".join(f"h={h}: {np.mean([r['d0'] - r['dinf'] for r in rows if r['wiring'] == 'additive' and r['m_S'] == m_S and r['h'] == h]):.4f}"
                                   for h in sorted({r['h'] for r in rows if r['wiring'] == 'additive' and r['m_S'] == m_S}))
        for m_S in sorted({r['m_S'] for r in rows})))
    for r in (law_bad + law_extra)[:12]:
        md.append(f"  - n={r['n']} s={r['s']} {r['policy']} m_S={r['m_S']} h={r['h']}: floor {r['dinf']:.6f} d0 {r['d0']:.6f} predicted equal={r['otp_predicted']}")
    md.append("- gated inversion MARGIN min over h ≥ 1 and m_S of (sage − floor), per (n, s, policy) — negative = inversion fails:")
    marg = {}
    for r in rows:
        if r['wiring'] == 'gated' and r['h'] >= 1:
            k = (r['n'], r['s'], r['policy']); marg[k] = min(marg.get(k, 9), r['sage'] - r['dinf'])
    md.append("  | n | s | policy | min margin | wall/sage |\n  |---|---|---|---|---|")
    for k in sorted(marg):
        r0 = next(r for r in rows if (r['n'], r['s'], r['policy']) == k and r['wiring'] == 'gated' and r['h'] == 1 and r['m_S'] == 8)
        md.append(f"  | {k[0]} | {k[1]} | {k[2]} | {marg[k]:+.3f} | {r0['wall'] / r0['sage']:.2f} |")
    md.append(f"- T9′ lower wall (wall ≤ every seed-known floor) or h=0 sage wall violated: **{len(bad_s)}** of {len(rows)}\n")
    # (a) floor vs reach
    md.append("## Floor vs reach (span family), n=4 s=0.5 hand policy, h=3\n")
    md.append("| m_S | " + " | ".join(f"d={d}" for d in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]) + " | additive (printed) | d0 | sage |")
    md.append("|---|" + "---|" * 14)
    for m_S in sorted({r['m_S'] for r in rows}):
        sel = {r['wiring']: r for r in rows if (r['n'], r['s'], r['policy'], r['m_S'], r['h']) == (4, 0.5, 'hand', m_S, 3)}
        cells = [f"{sel[f'span:{d}']['dinf']:.3f}" if f'span:{d}' in sel else '' for d in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]]
        md.append(f"| {m_S} | " + " | ".join(cells) + f" | {sel['additive']['dinf']:.3f} | {sel['additive']['d0']:.3f} | {sel['additive']['sage']:.3f} |")
    # monotonicity in reach across all configs
    viol = 0; tot = 0
    for key, grp in itertools.groupby(sorted([r for r in rows if r['wiring'].startswith('span:')],
                                             key=lambda r: (r['n'], r['s'], r['policy'], r['m_S'], r['h'], r['reach'])),
                                      key=lambda r: (r['n'], r['s'], r['policy'], r['m_S'], r['h'])):
        fl = [r['dinf'] for r in grp]
        tot += 1; viol += any(fl[i + 1] < fl[i] - 1e-9 for i in range(len(fl) - 1))
    md.append(f"\nFloor non-decreasing in reach: holds in {tot - viol}/{tot} (n,s,policy,m_S,h) groups "
              "(violations listed in the CSV by filtering span rows).\n")
    # reach law: same reach => same floor across m_S?
    byreach = {}
    for r in rows:
        if r['wiring'].startswith('span:'):
            byreach.setdefault((r['n'], r['s'], r['policy'], r['h'], round(r['reach'], 6)), []).append(r['dinf'])
    spread = [max(v) - min(v) for v in byreach.values() if len(v) > 1]
    if spread:
        md.append(f"REACH LAW check: across habit-space sizes m_S, configurations with the same (n, s, policy, h, reach) have floors "
                  f"differing by at most {max(spread):.4f} ({len(spread)} comparable groups). If this is ~0 the floor is a function of "
                  "reach alone for the span family -- the dichotomy is the two ends of one curve, parameterized by how far the "
                  "fresh bits travel across the habit's choice space.\n")
    # (b) random wirings
    md.append("## Random wirings vs the two named ones (mean over random seeds)\n")
    md.append("| n | s | policy | m_S | h | gated | random (mean ± sd) | additive:c | additive (printed) | d0 | sage |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for key in sorted({(r['n'], r['s'], r['policy'], r['m_S'], r['h']) for r in rows}):
        if key[1] != 0.5 or key[4] == 0 or key[4] > 4:
            continue
        sel = [r for r in rows if (r['n'], r['s'], r['policy'], r['m_S'], r['h']) == key]
        by = {r['wiring']: r for r in sel}
        rnd = [r['dinf'] for r in sel if r['wiring'].startswith('random')]
        md.append(f"| {key[0]} | {key[1]} | {key[2]} | {key[3]} | {key[4]} | {by['gated']['dinf']:.3f} | "
                  f"{np.mean(rnd):.3f} ± {np.std(rnd):.3f} | {by['additive:c']['dinf']:.3f} | {by['additive']['dinf']:.3f} | "
                  f"{by['additive']['d0']:.3f} | {by['additive']['sage']:.3f} |")
    md.append("\nReading: if random wirings sit at the additive:c value, generic wirings are additive-like and the gated "
              "wiring is the special (measure-small) structure — the dichotomy becomes 'gated is the exception'. "
              "If they sit between, the floor is a continuous function of reach and the dichotomy is the two ends of a curve.\n")
    p = os.path.join(args.out, 'wiring_hardening_SUMMARY.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(md)); print('\n'.join(md)); print('wrote', csvp, p)


if __name__ == "__main__":
    main()
