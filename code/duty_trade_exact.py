"""
duty_trade_exact.py -- a wall still standing, taken down: THE UNCERTAINTY ONE PARTY SHEDS LANDS ON NOBODY IN PARTICULAR.

Chapter 11's town. Each day k of the nine boats are ON CALL: their day belongs to someone else's schedule. An on-call
boat reads worse that day (accuracy 1/4 + (p - 1/4)(1 - d)), and skill moves as in the town that stops reading (S3):
    a day spent reading:  p <- p + mu (p_max - p)          a day on call:  p <- p - lam (p - 1/4).
Two ways to decide who is on call:
    LOT      k boats drawn fresh each day -- every boat is on call k/9 of its days;
    TRADE    the same k boats every day, paid by the others to take it.
Long-run skill (the mean of the linear dynamics): p* = [(1-f) mu p_max + f lam / 4] / [(1-f) mu + f lam], f = share of days on call.
Scored two ways: the fleet's MEAN catch (what the parties to the trade can divide between them -- a trade that raises it can
compensate every seller) and the town's FAMINE (three bad days running in ninety; a good day needs five boats on the fish).
Writes code/results/duty_trade_exact.md
"""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); N, M, DAYS = 9, 5, 90


def run3(p):
    v = np.zeros(4); v[0] = 1
    for _ in range(DAYS):
        n = np.zeros(4); n[0] = (1 - p) * v[:3].sum(); n[1] = p * v[0]; n[2] = p * v[1]; n[3] = v[3] + p * v[2]; v = n
    return v[3]


def badday(ps):
    d = np.array([1.0])
    for p in ps: d = np.convolve(d, [1 - p, p])
    return d[:M].sum()


def pstar(f, lam, mu, pmax):
    return ((1 - f) * mu * pmax + f * lam / 4) / ((1 - f) * mu + f * lam)


def on(p, d):
    return 0.25 + (p - 0.25) * (1 - d)


def arrangements(k, d, lam, mu, pmax):
    f = k / N; pl = pstar(f, lam, mu, pmax)
    lot = [on(pl, d)] * k + [pl] * (N - k)
    trade = [on(0.25 if lam > 0 else pmax, d)] * k + [pmax] * (N - k)
    return lot, trade, pl


def main():
    mu = 0.02
    L = ["# Who is on call (2026-11-10) — the same burden, drawn by lot or sold", "",
         "Nine boats; k on call each day; skill fades on call (rate λ) and returns with reading (rate μ = 0.02); d = how much of an on-call day's reading is lost. "
         "Long-run skill at the mean of the dynamics; famine and mean catch exact given those accuracies.", "",
         "## p_max = 0.7", "",
         "| k on call | d | λ/μ | LOT: every boat's skill | mean catch | famine | TRADE: sellers' / buyers' skill | mean catch | famine | trade raises mean catch | trade raises famine |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    tally = {'both_up': 0, 'catch_up_famine_down': 0, 'catch_down_famine_up': 0, 'catch_down_famine_down': 0}; rows = 0
    for pmax in (0.7, 0.8):
        for k in (1, 2, 3, 4):
            for d in (0.5, 1.0):
                for ratio in (0.25, 1.0, 4.0):
                    lam = ratio * mu; lot, trade, pl = arrangements(k, d, lam, mu, pmax)
                    ml, mt = sum(lot) / N, sum(trade) / N; fl, ft = run3(badday(lot)), run3(badday(trade)); rows += 1
                    key = ('both_up' if (mt > ml and ft > fl) else 'catch_up_famine_down' if (mt > ml) else 'catch_down_famine_up' if ft > fl else 'catch_down_famine_down')
                    tally[key] += 1
                    if pmax == 0.7:
                        L.append(f"| {k} | {d} | {ratio} | {pl:.3f} | {ml:.3f} | {100*fl:.1f}% | 0.250 / {pmax:.3f} | {mt:.3f} | {100*ft:.1f}% | {'yes' if mt > ml else 'no'} | {'YES' if ft > fl else 'no'} |")
    L += ["", f"## Across all {rows} cases (p_max 0.7 and 0.8; k 1–4; d 0.5, 1; λ/μ 0.25, 1, 4)", "",
          f"- trade raises the mean catch AND raises famine (every party can be made whole and the town starves more often): **{tally['both_up']}**",
          f"- trade raises the mean catch and lowers famine (specialization pays the town too): **{tally['catch_up_famine_down']}**",
          f"- trade lowers the mean catch and raises famine (no compensated trade is possible; lot is better on both): **{tally['catch_down_famine_up']}**",
          f"- trade lowers the mean catch and lowers famine: **{tally['catch_down_famine_down']}**", "",
          "## The rule the numbers follow",
          "Total skill kept by the fleet: by lot, 9 (1−f) μ Δ / ((1−f) μ + f λ) above chance; by trade, 9 (1−f) Δ (Δ = p_max − 1/4, f = k/9). "
          "So the lot keeps more skill than the trade exactly when skill fades more slowly than it returns (λ < μ), and less when it fades faster — "
          "and on top of that, by lot an on-call boat still brings whatever its skill is worth that day (d < 1), where a boat that is always on call brings chance."]
    # the buyer's own ledger
    L += ["", "## The buyer's own ledger (always the same sign)",
          "A boat that buys its way off the rota reads every day: its own accuracy goes from the lot's mix to p_max in every case above. "
          "The trade is therefore always wanted by the buyer; whether the sellers can be made whole is the mean-catch column; whether the town is better off is the famine column. "
          "The three need not agree."]
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    open(os.path.join(HERE, 'results', 'duty_trade_exact.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
