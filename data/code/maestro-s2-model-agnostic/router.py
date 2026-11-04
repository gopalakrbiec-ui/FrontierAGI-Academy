"""router.py — model-agnostic or not?

Each task type can go to Maestro-2 (own model), an external frontier API, or a
small open model. Quality (merge rate) and cost per task are SCENARIO numbers;
external prices are placeholders, not any vendor's list price. The router picks,
per task type, the cheapest option within 2 points of the best quality.
"""
OPT = {"Maestro-2": {}, "frontier API": {}, "small open": {}}
TASKS = [  # type, share of volume, {option: (merge rate, $ per task)}
    ("repo-specific fixes", 0.45, {"Maestro-2": (0.61, 0.08), "frontier API": (0.55, 0.22), "small open": (0.38, 0.02)}),
    ("dependency upgrades", 0.20, {"Maestro-2": (0.72, 0.06), "frontier API": (0.73, 0.18), "small open": (0.66, 0.02)}),
    ("new-language code", 0.15, {"Maestro-2": (0.48, 0.10), "frontier API": (0.63, 0.25), "small open": (0.30, 0.03)}),
    ("docs and tests", 0.20, {"Maestro-2": (0.80, 0.05), "frontier API": (0.81, 0.15), "small open": (0.79, 0.01)})]

def main():
    q = c = 0; share = {k: 0 for k in OPT}
    for t, w, o in TASKS:
        best = max(v[0] for v in o.values())
        pick = min((k for k, v in o.items() if v[0] >= best - 0.02), key=lambda k: o[k][1])
        q += w * o[pick][0]; c += w * o[pick][1]; share[pick] += w
        print(f"{t:22} -> {pick:12} merge {o[pick][0]:.0%}  ${o[pick][1]:.2f}")
    m2q = sum(w * o['Maestro-2'][0] for _, w, o in TASKS); m2c = sum(w * o['Maestro-2'][1] for _, w, o in TASKS)
    print(f"\nrouted:      merge {q:.1%}  ${c:.3f}/task  volume " + ", ".join(f"{k} {v:.0%}" for k, v in share.items()))
    print(f"Maestro-2 only: merge {m2q:.1%}  ${m2c:.3f}/task")

if __name__ == "__main__":
    main()
