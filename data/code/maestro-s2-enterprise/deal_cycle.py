"""deal_cycle.py — why enterprise revenue arrives late.

A funnel of enterprise opportunities moves through pilot, security review,
procurement and rollout. Each stage has a conversion rate and a duration.
Rates, durations and contract sizes are SCENARIO assumptions.
"""
STAGES = [("first meeting -> pilot", 0.40, 4), ("pilot -> security review", 0.65, 8), ("security review -> procurement", 0.70, 10), ("procurement -> signed", 0.80, 8)]

def main():
    n, weeks = 100.0, 0
    for name, r, w in STAGES:
        n *= r; weeks += w; print(f"{name:32} {r:4.0%}  {w:2} wk   {n:5.1f} of 100 left, week {weeks}")
    acv = 420_000
    print(f"\n{n:.1f} signed per 100 opportunities after {weeks} weeks; ${n * acv / 1e6:.1f}M ACV at ${acv / 1e3:.0f}k each")
    print(f"security review alone takes {STAGES[2][2]} of {weeks} weeks and loses {1 - STAGES[2][1]:.0%} of deals")

if __name__ == "__main__":
    main()
