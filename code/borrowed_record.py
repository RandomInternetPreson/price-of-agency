"""
borrowed_record.py -- the believed sage: a record earned where the answer is easy, spent where it is hard.

Chapter 11's town (nine boats, a good day needs five on the fish, famine = three bad days running in ninety). Days are
PLAIN (share 1-h) or HARD (share h). A reader is right with probability p_e on a plain day and p_h on a hard one.
One voice in the harbor -- call him the sage -- is right with probability q_e on a plain day and q_h on a hard one.

(1) THE RECORD. A fisher who keeps one tally per voice (right / wrong, all days together) sees the sage right
    a = (1-h) q_e + h q_h of days and himself right p = (1-h) p_e + h p_h. He follows the sage against his own reading
    exactly when a > p (Theorem 21's inequality).
(2) THE TOWN. Reading town: bad-day probability (1-h) B(p_e) + h B(p_h), B(p) = P(fewer than five of nine readers right).
    Following town: (1-h)(1-q_e) + h (1-q_h).
(3) WHERE THE RECORD WAS EARNED. On plain days the readers' majority is already right 1 - B(p_e) of the time: the sage adds
    nothing there. On hard days he is worse than the majority whenever q_h < 1 - B(p_h) -- and worse than every single
    reader whenever q_h < p_h.
(4) THE SPLIT TALLY. A fisher who keeps TWO tallies per voice -- plain days and hard days -- follows the sage on plain days
    and reads on hard ones. The ruler does not abolish the sage; it puts him where he is right.
(5) HOW LONG STANDING LASTS. Let a hard day's outcome be recorded against the voice that called it with probability v
    (in a fishery v = 1; where outcomes are slow, confounded or kept by the sage, v is small). A reputation for never
    being wrong lasts until the first recorded miss: 1 / (h v (1 - q_h)) days on average. A reputation held at odds
    O : 1 that he is as good on hard days as his believers think (q_b) lasts ln(O) / (h v KL(q_h || q_b)) days.
Everything exact. Writes code/results/borrowed_record.md
"""
import os
from math import comb, log
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); N, M, DAYS = 9, 5, 90


def run3(p):
    v = np.zeros(4); v[0] = 1
    for _ in range(DAYS):
        n = np.zeros(4); n[0] = (1 - p) * v[:3].sum(); n[1] = p * v[0]; n[2] = p * v[1]; n[3] = v[3] + p * v[2]; v = n
    return v[3]


def B(p, k=0, q=None):
    """P(fewer than M of the fleet on the fish): N-k readers at p; k followers all right w.p. q."""
    r = [comb(N - k, j) * p ** j * (1 - p) ** (N - k - j) for j in range(N - k + 1)]
    if k == 0: return sum(r[:M])
    return q * sum(r[j] for j in range(len(r)) if j + k < M) + (1 - q) * sum(r[:M])


def case(h, pe, ph, qe, qh):
    a = (1 - h) * qe + h * qh; p = (1 - h) * pe + h * ph
    read = (1 - h) * B(pe) + h * B(ph); follow = (1 - h) * (1 - qe) + h * (1 - qh)
    split = (1 - h) * (1 - qe) + h * B(ph) if qe > 1 - B(pe) else read          # follow on plain days only (if he beats the majority there), read on hard
    dose = [(1 - h) * B(pe, k, qe) + h * B(ph, k, qh) for k in range(N + 1)]
    return dict(a=a, p=p, read=read, follow=follow, split=split, dose=dose)


def kl(q, qb):
    return q * log(q / qb) + (1 - q) * log((1 - q) / (1 - qb))


def main():
    h, pe, ph, qe, qh = 0.3, 0.90, 0.55, 1.0, 0.50
    c = case(h, pe, ph, qe, qh)
    L = ["# The borrowed record (2026-11-12) — a voice that is right where the answer is easy and wrong where it is hard", "",
         f"Printed town: {int(100*h)}% of days are hard. Readers: right {int(100*pe)}% of plain days, {int(100*ph)}% of hard days. "
         f"The sage: right on every plain day, {int(100*qh)}% of hard days — worse than any single reader exactly when the day is hard.", "",
         "| | right, all days (the record) | right on plain days | right on hard days |", "|---|---|---|---|",
         f"| one reader | {100*c['p']:.1f}% | {100*pe:.0f}% | {100*ph:.0f}% |",
         f"| the readers' majority | {100*(1-c['read']):.1f}% | {100*(1-B(pe)):.2f}% | {100*(1-B(ph)):.1f}% |",
         f"| the sage | {100*c['a']:.1f}% | {100*qe:.0f}% | {100*qh:.0f}% |", "",
         f"One tally per voice: the sage's record ({100*c['a']:.1f}%) beats every reader's ({100*c['p']:.1f}%), so every fisher follows him — correctly, on the tally he keeps.", "",
         "| arrangement | bad days | famine (three running in ninety) |", "|---|---|---|",
         f"| everyone reads | {100*c['read']:.1f}% | {100*run3(c['read']):.1f}% |",
         f"| everyone follows the sage | {100*c['follow']:.1f}% | {100*run3(c['follow']):.1f}% |",
         f"| two tallies: follow him on plain days, read on hard ones | {100*c['split']:.1f}% | {100*run3(c['split']):.1f}% |", "",
         "Followers by number (one tally): famine " + ", ".join(f"{k}: {100*run3(c['dose'][k]):.1f}%" for k in range(N + 1)) + ".", "",
         f"Where the record was earned: on plain days the majority was already right {100*(1-B(pe)):.2f}% of the time. Everything the sage is right about, the town already knew. "
         f"Every day on which following him differs from reading is a hard day, and on those he is right {100*qh:.0f}% of the time against the majority's {100*(1-B(ph)):.1f}%.", "",
         "## How long the standing lasts", "",
         "A hard day's outcome is recorded against the voice that called it with probability v.", "",
         "| share of hard-day outcomes recorded (v) | believed never wrong: days to the first recorded miss | believed right 95% on hard days, at odds 99 to 1: days until the odds turn |", "|---|---|---|"]
    for v in (1.0, 0.3, 0.1, 0.03, 0.01):
        d1 = 1 / (h * v * (1 - qh)); d2 = log(99) / (h * v * kl(qh, 0.95))
        L.append(f"| {v:g} | {d1:,.0f} ({d1/90:.1f} seasons) | {d2:,.0f} ({d2/90:.1f} seasons) |")
    L += ["", "Standing lasts in inverse proportion to how much of the hard part is recorded. Record all of it and the borrowed record is gone inside a month; record one hard day in a hundred and it outlasts seven seasons of famine at "
          f"{100*run3(c['follow']):.0f}% each.", "",
          "## How wide the condition is", "",
          "Grid: hard-day share h ∈ {0.1 … 0.5}; readers p_e ∈ {0.8, 0.9, 0.95}, p_h ∈ {0.4 … 0.65}; sage right on every plain day, q_h ∈ {0.25 … 0.6}.", ""]
    tot = win = worse_single = both = 0
    for hh in (0.1, 0.2, 0.3, 0.4, 0.5):
        for a_ in (0.8, 0.9, 0.95):
            for b_ in (0.4, 0.45, 0.5, 0.55, 0.6, 0.65):
                for q_ in (0.25, 0.3, 0.4, 0.5, 0.6):
                    cc = case(hh, a_, b_, 1.0, q_); tot += 1
                    followed = cc['a'] > cc['p']; hurts = cc['follow'] > cc['read']
                    win += followed and hurts; worse_single += followed and q_ < b_; both += followed and hurts and q_ < b_
    L += [f"- the sage's single tally beats every reader's AND following him raises the town's bad days: {win} of {tot} worlds;",
          f"- his single tally beats every reader's while he is worse than each single reader on hard days: {worse_single} of {tot};",
          f"- both at once: {both} of {tot}.", "",
          "## The gate beside him (Chapter 5's terms)",
          f"A neighbor who cannot tell a plain day from a hard one needs knowledge better than the sage's RECORD ({100*c['a']:.0f}%) before acting on it is rational — "
          f"not better than his accuracy on the days that decide anything ({100*qh:.0f}%). The gate is set by the record, and the record was set by the easy days."]
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    open(os.path.join(HERE, 'results', 'borrowed_record.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
