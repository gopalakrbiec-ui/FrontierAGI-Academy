"""eval_m2.py — the sealed evaluation: is Maestro-2 worth what it cost?

Two sets were written down before the run (Part 14): the 83 model-only failures
from Part 10 and 400 held-out customer tasks. Each task is run with Maestro-1
and Maestro-2 under the same harness and context. The held-out gain gets a
95% paired-bootstrap interval. Per-task outcomes are SCENARIO data generated
from a fixed seed; the method is the one used in Season 1, Part 12.
"""
import random
random.seed(11)
P1, P2 = 0.62, 0.69            # scenario pass rates on held-out tasks
held = [(random.random() < P1, None) for _ in range(400)]
held = [(a, a or random.random() < (P2 - P1) / (1 - P1)) for a, _ in held]   # M2 keeps M1's wins, adds some
for i in random.sample(range(400), 9):                                         # ...and loses a few (regressions)
    held[i] = (held[i][0], False)
fixed = sum(1 for _ in range(83) if random.random() < 0.55)                    # of the 83 model-only failures

def boot(pairs, n=2000):
    d = []
    for _ in range(n):
        s = [random.choice(pairs) for _ in pairs]
        d.append(sum(b - a for a, b in s) / len(s))
    d.sort(); return d[int(0.025 * n)], d[int(0.975 * n)]

def main():
    a = sum(x for x, _ in held); b = sum(y for _, y in held); reg = sum(1 for x, y in held if x and not y)
    lo, hi = boot([(int(x), int(y)) for x, y in held])
    print(f"model-only failures fixed: {fixed} of 83 ({fixed / 83:.0%})")
    print(f"held-out tasks: Maestro-1 {a}/400 ({a / 4:.1f}%)  Maestro-2 {b}/400 ({b / 4:.1f}%)")
    print(f"gain {100 * (b - a) / 400:+.1f} points, 95% CI [{100 * lo:+.1f}, {100 * hi:+.1f}]; regressions: {reg} tasks")
    print("verdict:", "SHIP behind the gate" if lo > 0 else "do not ship")

if __name__ == "__main__":
    main()
