"""investor_metrics.py — the numbers a Series A investor asks for, from the
story's month-18 customer table (SCENARIO data, not a real company).

Monthly recurring revenue (MRR) per customer at month 6 of their contract
and now; serving cost from Part 15's $1.17 per million tokens.
"""
# name, MRR $k 12 months ago (0 = not a customer yet), MRR $k now, tokens (billions) per month
CUSTOMERS = [
    ("partner-A", 9.0, 14.5, 2.0), ("partner-B", 8.0, 12.0, 1.7), ("partner-C", 6.0, 10.0, 1.4),
    ("pilot-D", 4.0, 3.0, 0.4),   ("E", 0, 16.0, 2.2), ("F", 0, 14.0, 1.9),
    ("G", 0, 14.0, 1.9), ("H", 0, 13.5, 1.8), ("I", 0, 13.0, 1.8),
]
PRICE_PER_M_TOKENS_COST = 1.17      # $ serving cost per million tokens (Part 15)
OTHER_COGS_K = 21.0                 # $k/month: support, integrations, eval runs for customers (scenario)
BURN_K = 352.0                      # $k/month net burn at month 18 (Part 18)
NET_NEW_ARR_K = 12 * (110 - 46)     # ARR added over the last 12 months, $k (scenario)

def main():
    mrr = sum(c[2] for c in CUSTOMERS)
    tokens_cost = sum(c[3] for c in CUSTOMERS) * 1000 * PRICE_PER_M_TOKENS_COST / 1000
    gm = 1 - (tokens_cost + OTHER_COGS_K) / mrr
    old = [c for c in CUSTOMERS if c[1] > 0]
    nrr = sum(c[2] for c in old) / sum(c[1] for c in old)
    top3 = sum(sorted((c[2] for c in CUSTOMERS), reverse=True)[:3]) / mrr
    print(f"MRR now            ${mrr:6.1f}k   ARR ${mrr * 12 / 1000:.2f}M")
    print(f"serving cost       ${tokens_cost:6.1f}k/month for {sum(c[3] for c in CUSTOMERS):.1f}B tokens")
    print(f"gross margin       {gm:6.1%}")
    print(f"net revenue retention (12-month cohort of {len(old)}): {nrr:.0%}")
    print(f"top-3 customer share  {top3:.0%}")
    print(f"burn multiple      {BURN_K * 12 / NET_NEW_ARR_K:.1f}x  (net burn / net new ARR)")

if __name__ == "__main__":
    main()
