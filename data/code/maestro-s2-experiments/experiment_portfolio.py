"""experiment_portfolio.py — pick this quarter's experiments under a fixed
compute budget, by expected value per GPU-hour (a 0/1 knapsack).

Every experiment is the story's SCENARIO proposal: p = chance it gives a
usable result, value = what a usable result is worth to the roadmap (0-10),
cost = GPU-hours (thousands). Budget: 120k GPU-hours of research compute.
"""
from itertools import combinations

EXPS = [  # id, track, p, value, cost (k GPU-h)
    ("X1", "L4 skill retrieval v2", 0.6, 8, 30),
    ("X2", "L4 skill pruning", 0.7, 5, 10),
    ("X3", "L3 failure curriculum", 0.4, 7, 25),
    ("X4", "L2 harness search", 0.5, 6, 20),
    ("X5", "L1 eval sampling", 0.9, 2, 5),
    ("X6", "L5 sandbox: self-edited search", 0.15, 9, 40),
    ("X7", "env generator (Part 8)", 0.5, 8, 35),
    ("X8", "long-context skills", 0.3, 6, 45),
]
BUDGET = 120

def main():
    best, bv = (), 0.0
    for k in range(1, len(EXPS) + 1):
        for c in combinations(EXPS, k):
            cost = sum(e[4] for e in c)
            ev = sum(e[2] * e[3] for e in c)
            if cost <= BUDGET and ev > bv:
                best, bv = c, ev
    print(f"{'id':3} {'experiment':30} {'EV':>5} {'k GPU-h':>8} {'EV/k':>6}")
    for e in sorted(EXPS, key=lambda e: -e[2] * e[3] / e[4]):
        mark = "*" if e in best else " "
        print(f"{e[0]:3} {e[1]:30} {e[2] * e[3]:5.2f} {e[4]:8} {e[2] * e[3] / e[4]:6.3f} {mark}")
    print(f"chosen (*): {', '.join(e[0] for e in best)}  cost {sum(e[4] for e in best)}k of {BUDGET}k  EV {bv:.2f}")

if __name__ == "__main__":
    main()
