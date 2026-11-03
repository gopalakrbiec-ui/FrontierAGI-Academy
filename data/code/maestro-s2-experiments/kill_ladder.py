"""kill_ladder.py — run experiments up an evidence ladder and stop early.

Rungs (Season 1, Part 2's method at team scale): toy (2%) -> small (10%) ->
medium (30%) -> full (100%) of the experiment's compute. Each rung has a
pre-registered bar; an experiment that misses a bar is killed there.
Results are SCENARIO numbers: the measured gain (points) at each rung.
The chosen five ran; X5 joined after X7 was killed and freed compute.
"""
RUNGS = [("toy", 0.02, 0.5), ("small", 0.10, 1.0), ("medium", 0.30, 1.5), ("full", 1.00, 2.0)]
RESULTS = {  # experiment: (k GPU-h if run to full, gains at each rung)
    "X1": (30, [1.1, 1.6, 2.2, 2.6]), "X2": (10, [0.8, 1.2, 1.4, 1.5]),
    "X3": (25, [0.9, 0.6, None, None]), "X4": (20, [0.7, 1.3, 1.9, 2.3]),
    "X5": (5, [0.6, 1.1, 1.6, 2.1]), "X7": (35, [0.3, None, None, None]),
}

def main():
    spent = full = 0.0
    for x, (cost, gains) in RESULTS.items():
        full += cost
        for (name, frac, bar), g in zip(RUNGS, gains):
            spent += cost * frac
            if g is None or g < bar:
                print(f"{x}: killed at {name:6} (gain {g if g is not None else 0:.1f} < bar {bar}) after {cost * frac:5.1f}k GPU-h")
                break
        else:
            print(f"{x}: passed all rungs, {cost}k GPU-h")
    print(f"compute used {spent:.1f}k of {full:.0f}k if everything ran to full ({1 - spent / full:.0%} saved)")

if __name__ == "__main__":
    main()
