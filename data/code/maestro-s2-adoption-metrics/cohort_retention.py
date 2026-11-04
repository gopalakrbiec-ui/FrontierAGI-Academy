"""cohort_retention.py — net revenue retention by customer cohort.

Monthly recurring revenue ($k) per cohort at month 0, 6 and 12 after signing.
Net revenue retention (NRR) = revenue a cohort pays now / what it paid at
start, including expansion and churn. Data are SCENARIO numbers.
"""
COH = {"PR-bot cohort (month 14)": (300, 318, 345), "Platform early (month 30)": (520, 690, 860), "Enterprise (month 38)": (900, 1150, None)}

def main():
    for n, (m0, m6, m12) in COH.items():
        line = f"{n:28} start ${m0}k  m6 {m6 / m0:5.0%}"
        if m12: line += f"  m12 {m12 / m0:5.0%}"
        print(line)
    print("\nNRR above 100% means existing customers grow faster than any churn: the platform cohort is the business")

if __name__ == "__main__":
    main()
