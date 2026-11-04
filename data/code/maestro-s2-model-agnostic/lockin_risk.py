"""lockin_risk.py — what if the external provider changes the terms?

Stress-test the routed plan: the frontier API raises prices 2x, deprecates the
model (quality drops while re-tuning), or is cut off. Gross margin per task is
compared with a plan that keeps a fallback route warm. All numbers SCENARIO.
"""
PRICE, BASE_COST, EXT_SHARE, EXT_COST = 0.28, 0.087, 0.15, 0.25   # platform price/task; routed cost (router.py); share on API

def margin(cost): return (PRICE - cost) / PRICE

def main():
    print(f"{'shock':36} {'cost/task':>9} {'margin':>7}")
    for name, extra in (("none", 0), ("API price x2", EXT_SHARE * EXT_COST), ("API cut off, fallback to Maestro-2", EXT_SHARE * (0.10 - EXT_COST))):
        c = BASE_COST + extra; print(f"{name:36} {c:9.3f} {margin(c):7.1%}")
    print("\ncut-off also costs quality on new-language tasks (63% -> 48% merge) until Maestro-3")

if __name__ == "__main__":
    main()
