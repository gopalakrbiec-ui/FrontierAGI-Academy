"""series_a.py — three Series A term sheets compared on dilution and runway.

Cap table after the seed and every offer are the story's SCENARIO numbers.
Post-money valuation = pre-money + new money; the option-pool top-up is
taken from the pre-money (the usual 'pool shuffle'), so founders pay for it.
"""
CAP = {"Gopala": 0.66, "seed investors": 0.25, "option pool": 0.09}   # after the seed (scenario)
CASH_M = 7.4                                                          # month 22: cash before the round
# name, new money $M, pre-money $M, pool target after the round
OFFERS = [("A: big fund", 60, 240, 0.12), ("B: strategic", 45, 255, 0.10), ("C: small, fast", 30, 150, 0.10)]
BURN = {22: 0.42, 26: 1.10, 30: 3.40, 36: 1.95}                       # $M/month: team growth (hiring_plan.py), Maestro-2 run months 30-35 (scenario)
REV0, GROWTH = 0.137, 0.08                                            # $M/month at month 22, growth (assumption)

def round_table(new, pre, pool):
    post = pre + new
    inv = new / post
    shuffle = max(0, pool - CAP["option pool"] * (1 - inv))   # extra pool, carved from pre-money holders
    old = 1 - inv - pool
    scale = old / (CAP["Gopala"] + CAP["seed investors"])
    return post, inv, CAP["Gopala"] * scale, CAP["seed investors"] * scale, pool, shuffle

def runway(new):
    """Month when cash falls below 9 months of burn: the latest safe start for the next raise."""
    cash, rev, m, low = CASH_M + new, REV0, 22, CASH_M + new
    while m < 72:
        b = [v for k, v in BURN.items() if m >= k][-1]
        if cash < 9 * (b - rev): return f"low ${low:4.1f}M  raise again by month {m}"
        cash -= max(0, b - rev); rev *= 1 + GROWTH; m += 1; low = min(low, cash)
        if rev >= b: return f"low ${low:4.1f}M  break-even at month {m}"
    return "beyond month 72"

def main():
    print(f"{'offer':16} {'post $M':>7} {'new inv':>7} {'Gopala':>7} {'seed':>6} {'pool':>5}  runway")
    for name, new, pre, pool in OFFERS:
        post, inv, g, s, p, sh = round_table(new, pre, pool)
        print(f"{name:16} {post:7.0f} {inv:7.1%} {g:7.1%} {s:6.1%} {p:5.0%}  {runway(new)}")
    print("pool shuffle in offer A costs Gopala "
          f"{(CAP['Gopala'] * (1 - 60 / 300) - round_table(60, 240, 0.12)[2]) * 100:.1f} points")

if __name__ == "__main__":
    main()
