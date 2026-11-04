"""metrics.py — vanity metrics vs value metrics.

Two quarters of product data. Sessions and tokens went up; the metrics tied to
customer value tell a different story. Data are SCENARIO numbers.
"""
Q = {"Q1": dict(sessions=410_000, tokens_b=38.0, tasks=2_100_000, merged=1_090_000, reverted=41_000, hours_saved=520_000),
     "Q2": dict(sessions=655_000, tokens_b=71.0, tasks=2_900_000, merged=1_310_000, reverted=88_000, hours_saved=560_000)}

def main():
    a, b = Q["Q1"], Q["Q2"]
    for k in ("sessions", "tokens_b"): print(f"vanity  {k:12} {a[k]:>12,} -> {b[k]:>12,}  ({b[k] / a[k] - 1:+.0%})")
    acc = lambda q: q["merged"] / q["tasks"]; kept = lambda q: (q["merged"] - q["reverted"]) / q["merged"]
    print(f"value   merge rate   {acc(a):12.1%} -> {acc(b):12.1%}")
    print(f"value   kept 30 days {kept(a):12.1%} -> {kept(b):12.1%}")
    print(f"value   hours saved  {a['hours_saved']:>12,} -> {b['hours_saved']:>12,}  ({b['hours_saved'] / a['hours_saved'] - 1:+.0%})")
    print(f"\nhours saved per 1k sessions: {a['hours_saved'] / a['sessions'] * 1000:.0f} -> {b['hours_saved'] / b['sessions'] * 1000:.0f}")

if __name__ == "__main__":
    main()
