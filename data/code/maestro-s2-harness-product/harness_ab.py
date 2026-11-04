"""harness_ab.py — the harness is the product.

The same model (Maestro-2) runs 500 replayed customer tasks under four
harnesses. "Right" = tests pass. "Good" = a reviewer would merge it as written
(style, size, maintainability): the owner's notes on Noronha ("is it right?"
and "is it good?"). Every attempt also costs a reviewer's time ($1.50 at
about a minute and a half). Rates and costs are SCENARIO numbers.
"""
H = [  # name, right, good given right, cost per task $
    ("single shot", 0.58, 0.55, 0.05),
    ("plan + execute", 0.66, 0.60, 0.08),
    ("generate-check-fix", 0.74, 0.62, 0.11),
    ("generate-check-fix + taste review", 0.73, 0.81, 0.13)]

REVIEW = 1.50   # $ of reviewer time per attempt, merged or not

def main():
    for n, r, g, c in H:
        merged = r * g
        print(f"{n:36} right {r:4.0%}  good|right {g:4.0%}  merged {merged:4.0%}  model ${c:.2f}  all-in ${(c + REVIEW) / merged:.2f} per merged change")
    best = min(H, key=lambda h: (h[3] + REVIEW) / (h[1] * h[2]))
    print(f"\ncheapest per merged change, counting reviewer time: {best[0]}")

if __name__ == "__main__":
    main()
