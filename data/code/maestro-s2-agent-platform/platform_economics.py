"""platform_economics.py — from a PR bot to an agent platform.

Three ways to sell the same model: the PR bot (fixed tasks inside GitHub), a
platform where customers build their own agents on Maestro's harness, and an
API for other companies' agents (agents as customers, from the owner's notes on
Rauch). Volumes, prices and costs per task are SCENARIO assumptions.
"""
LINES = [  # name, tasks per month, price per task $, serving + tools cost per task $, support per month $
    ("PR bot (today)", 900_000, 0.40, 0.09, 120_000),
    ("Agent platform", 2_600_000, 0.28, 0.08, 380_000),
    ("API for other agents", 6_000_000, 0.06, 0.035, 60_000)]

def main():
    tr, tg = 0, 0
    for n, t, p, c, s in LINES:
        rev = t * p; gm = rev - t * c - s; tr += rev; tg += gm
        print(f"{n:22} revenue ${rev / 1e3:7.0f}k/month  gross margin ${gm / 1e3:6.0f}k ({gm / rev:4.0%})")
    print(f"\ntotal ${tr / 1e6:.2f}M/month, blended margin {tg / tr:.0%}; annualised revenue ${12 * tr / 1e6:.1f}M")

if __name__ == "__main__":
    main()
