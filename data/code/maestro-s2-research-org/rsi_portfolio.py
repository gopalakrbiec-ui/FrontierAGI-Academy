"""rsi_portfolio.py — split 10 researchers and the research compute across
five tracks, one per RSI level (L1-L5), under fixed safety rules.

Every number is the story's SCENARIO estimate, not a measurement:
  value  = expected moat value if the track succeeds (0-10, team judgement)
  p      = chance of a usable result within 12 months
  risk   = how much harm a failure could do outside a sandbox (0-10)
Rules (from the boundary policy in this part):
  * L5 runs only in an isolated sandbox and gets at most 10% of compute;
  * every track at L3 or above has a safety reviewer attached;
  * a track needs at least one researcher to exist.
The allocator tries every split of researchers and keeps the one with the
best risk-adjusted value: sum(value * p * people^0.6) - 0.15 * sum(risk * share).
"""
from itertools import product

TRACKS = [  # level, name, value, p, risk
    (1, "L1 eval & training automation", 3, 0.9, 1),
    (2, "L2 harness and strategy search", 6, 0.6, 2),
    (3, "L3 curriculum from failures", 7, 0.5, 4),
    (4, "L4 skill library (the product)", 9, 0.7, 5),
    (5, "L5 meta-improvement (sandbox)", 8, 0.15, 9),
]
PEOPLE, L5_COMPUTE_CAP = 10, 0.10

def score(split):
    total = sum(split)
    if total != PEOPLE or min(split) < 1:
        return None
    share = [s / total for s in split]
    if share[4] > L5_COMPUTE_CAP + 1e-9:        # compute follows people in this model
        return None
    gain = sum(v * p * s ** 0.6 for (_, _, v, p, _), s in zip(TRACKS, split))
    harm = 0.15 * sum(r * sh * 10 for (_, _, _, _, r), sh in zip(TRACKS, share))
    return gain - harm

def main():
    best = max((s for s in product(range(1, 7), repeat=5) if score(s) is not None), key=score)
    print(f"{'track':34} {'people':>6} {'compute':>8}  reviewer")
    for (lvl, name, *_), n in zip(TRACKS, best):
        print(f"{name:34} {n:6} {n / PEOPLE:8.0%}  {'safety' if lvl >= 3 else '-'}")
    print(f"risk-adjusted value {score(best):.2f}")
    even = (2, 2, 2, 2, 2)
    print(f"even split (2 each) is not allowed: L5 would get {2 / PEOPLE:.0%} of compute" if score(even) is None else f"even split value {score(even):.2f}")
    heavy = (1, 1, 2, 5, 1)
    print(f"all-in on the product (1,1,2,5,1) value {score(heavy):.2f}")

if __name__ == "__main__":
    main()
