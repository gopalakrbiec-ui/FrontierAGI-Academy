"""hiring_plan.py — the first 36 hires after the Series A, in order.

Fully loaded cost = salary + equity value is NOT included; this is cash:
salary, benefits, payroll tax, laptop and tools (our assumption: 1.3 x base).
Base salaries are SCENARIO bands for a remote-first company hiring globally,
not market data. Each row: month the person starts, team, role, base $k/yr.
"""
LOAD = 1.3
PLAN = [
    (22, "research", "research lead (post-training & RL)", 330), (22, "infra", "head of infrastructure", 300),
    (23, "product", "head of product engineering", 280), (23, "gtm", "founding account executive", 190),
    (23, "safety", "safety & evaluation lead", 280), (24, "research", "research engineer: environments", 250),
    (24, "research", "research engineer: data", 250), (24, "infra", "ML infrastructure engineer", 240),
    (24, "product", "product engineer: agents", 220), (24, "ops", "finance & people operations", 170),
    (25, "research", "research scientist: RSI levels", 300), (25, "product", "product designer", 190),
    (25, "gtm", "solutions engineer", 200), (25, "safety", "red-team engineer", 240),
    (26, "infra", "site reliability engineer", 220), (26, "research", "research engineer: evals", 240),
    (26, "product", "product engineer: integrations", 210), (26, "gtm", "customer success lead", 170),
    (27, "research", "research scientist: pre-training", 310), (27, "infra", "kernel & performance engineer", 280),
    (27, "product", "product manager: platform", 220), (28, "gtm", "account executive", 180),
    (28, "research", "research engineer: synthetic data", 240), (28, "safety", "security engineer", 240),
    (29, "infra", "ML infrastructure engineer", 240), (29, "product", "product engineer: harness", 220),
    (30, "research", "research engineer: training", 250), (30, "gtm", "solutions engineer", 200),
    (30, "ops", "legal & compliance counsel", 260), (31, "research", "research scientist: agents", 300),
    (31, "product", "product engineer: enterprise", 210), (32, "infra", "site reliability engineer", 220),
    (32, "gtm", "head of sales", 260), (33, "research", "research engineer: RL", 250),
    (33, "safety", "evaluation engineer", 230), (34, "product", "developer relations", 190),
]

def main():
    teams = sorted({p[1] for p in PLAN})
    print("month  headcount  people $M/month  " + "  ".join(f"{t:>8}" for t in teams))
    for m in (22, 24, 26, 28, 30, 32, 34):
        on = [p for p in PLAN if p[0] <= m]
        cost = sum(p[3] for p in on) * LOAD / 12 / 1000 + 0.025   # + Gopala and the two Season 1 hires (scenario)
        print(f"{m:5}  {len(on) + 3:9}  {cost:15.2f}  " + "  ".join(f"{sum(1 for p in on if p[1] == t):8}" for t in teams))
    first5 = [p[2] for p in PLAN[:5]]
    print("first five:", "; ".join(first5))
    print(f"research share of hires: {sum(1 for p in PLAN if p[1] == 'research') / len(PLAN):.0%}")

if __name__ == "__main__":
    main()
