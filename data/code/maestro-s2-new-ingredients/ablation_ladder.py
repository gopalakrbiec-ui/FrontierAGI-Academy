"""ablation_ladder.py — which new ingredients earn a place in Maestro-2?

Each candidate is trained at two small scales (1B and 3B active) with three
seeds each, against a baseline. An ingredient is kept only if the mean gain is
more than twice its standard error at BOTH scales (small effects that vanish
with scale are the classic trap). Measured gains (points on the held-out task
suite) are SCENARIO numbers; the ideas are real (see the article's sources).
"""
import statistics as st
RUNS = {  # ingredient: {scale: [gain per seed]}
    "multi-token prediction": {"1B": [0.6, 0.9, 0.7], "3B": [0.8, 1.0, 0.9]},
    "aux-loss-free load balancing": {"1B": [0.3, 0.5, 0.4], "3B": [0.4, 0.6, 0.5]},
    "FP8 training (matched loss)": {"1B": [0.0, 0.1, -0.1], "3B": [0.1, 0.0, 0.0]},
    "environment data in mid-training": {"1B": [1.1, 0.7, 1.4], "3B": [1.5, 1.2, 1.8]},
    "+10% code in the mixture": {"1B": [0.9, 0.2, 1.3], "3B": [0.1, -0.4, 0.5]},
    "new 200k tokenizer": {"1B": [0.5, -0.6, 0.9], "3B": [0.3, -0.2, 0.2]},
    "wider attention heads": {"1B": [0.4, 0.3, 0.5], "3B": [-0.1, 0.0, 0.1]}}

NONINF = {"FP8 training (matched loss)"}   # judged on "no worse" (mean > -0.2): its prize is speed

def main():
    keep = []
    for name, sc in RUNS.items():
        cells, ok = [], True
        for s in ("1B", "3B"):
            m, se = st.mean(sc[s]), st.stdev(sc[s]) / len(sc[s]) ** 0.5
            ok &= (m > -0.2) if name in NONINF else (m > 2 * se); cells.append(f"{s} {m:+.2f}±{se:.2f}")
        verdict = ("KEEP (speed)" if name in NONINF else "KEEP") if ok else "drop"
        if ok: keep.append(name)
        print(f"{name:34} {'   '.join(cells)}   {verdict}")
    print(f"\nkept {len(keep)} of {len(RUNS)}: {', '.join(keep)}")
    print("FP8 passes a no-worse test, not a gain test: its prize is speed (see fp8_budget.py)")

if __name__ == "__main__":
    main()
