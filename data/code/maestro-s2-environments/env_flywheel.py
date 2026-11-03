"""env_flywheel.py — environments as a compounding asset.

Each month the team builds new environments; a share fails the quality check
(leaky or trivial checks) and is discarded; kept environments lose 2% a month
to drift (APIs change, tasks go stale). The model's gain on held-out tasks
grows with the square root of good environments (diminishing returns).
Build rates, pass rates and the gain constant are SCENARIO assumptions.
"""
def run(build_per_month, pass_rate, months=12, decay=0.02, k=0.12):
    good, out = 0.0, []
    for m in range(1, months + 1):
        good = good * (1 - decay) + build_per_month * pass_rate
        out.append((m, good, k * good ** 0.5))
    return out

def main():
    for label, b, q in (("plan: 250/month, 70% pass", 250, 0.70), ("rushed: 400/month, 35% pass", 400, 0.35), ("slow: 120/month, 85% pass", 120, 0.85)):
        r = run(b, q)
        print(f"{label:30} month 6: {r[5][1]:6.0f} envs, +{r[5][2]:.1f} pts   month 12: {r[11][1]:6.0f} envs, +{r[11][2]:.1f} pts")

if __name__ == "__main__":
    main()
