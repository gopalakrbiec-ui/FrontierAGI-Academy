"""market_size.py — bottom-up market sizing, the way investors check it.

Every input is OUR ASSUMPTION for the story (labelled on the page), not a
market statistic: we count teams Gopala can actually reach, not 'all developers'.
"""
SEGMENTS = [  # segment, companies, engineering teams each, share that fit (private code, regulated), $k per team per year
    ("regulated mid-size (finance, health)", 6000, 8, 0.30, 36),
    ("large enterprise", 1500, 60, 0.15, 30),
    ("software scale-ups", 12000, 4, 0.20, 24),
]
REACH_3Y = 0.04      # share of the fitting market a 40-person company can win in three years (assumption)

def main():
    tot = 0
    for name, n, teams, fit, price in SEGMENTS:
        v = n * teams * fit * price / 1000
        tot += v
        print(f"{name:38} {n * teams * fit:9,.0f} teams  ${v:7,.0f}M/yr")
    print(f"{'serviceable market':38} {'':15}  ${tot:7,.0f}M/yr")
    print(f"3-year target at {REACH_3Y:.0%} of it:            ${tot * REACH_3Y:7,.1f}M ARR")

if __name__ == "__main__":
    main()
