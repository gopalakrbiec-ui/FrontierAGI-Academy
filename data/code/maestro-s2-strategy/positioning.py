"""positioning.py — how four kinds of option score on what buyers said matters.

Weights come from the story's 31 SCENARIO customer interviews (share of
buyers who ranked the criterion in their top three, normalised). Scores
(1-5) are Gopala's own judgement of each archetype, not measurements of
any real company. The sensitivity test asks: how far must one weight move
before Maestro stops winning?
"""
CRIT = ["works on our private code", "evidence each change is safe", "raw model capability",
        "price per task", "fits our tools today", "vendor will exist in 3 years"]
W = [0.24, 0.20, 0.16, 0.14, 0.14, 0.12]
OPTS = {
    "Maestro (specialist)":        [5, 5, 3, 4, 3, 2],
    "frontier-lab coding agent":   [3, 3, 5, 3, 4, 5],
    "open model + DIY harness":    [4, 2, 3, 5, 2, 3],
    "dev-tool incumbent add-on":   [2, 3, 3, 3, 5, 5],
}

def score(w):
    return {k: sum(a * b for a, b in zip(w, v)) for k, v in OPTS.items()}

def main():
    s = score(W)
    for k, v in sorted(s.items(), key=lambda x: -x[1]):
        print(f"{k:28} {v:.2f}")
    print("sensitivity: weight increase (others shrink in proportion) that makes Maestro lose")
    for i, c in enumerate(CRIT):
        for step in range(1, 101):
            w = [x * (1 - step / 100) for x in W]
            w[i] = W[i] + (1 - W[i]) * step / 100
            w = [x / sum(w) for x in w]
            r = score(w)
            best = max(r, key=r.get)
            if best != "Maestro (specialist)":
                print(f"  {c:30} {W[i]:.2f} -> {w[i]:.2f}  {best} wins"); break
        else:
            print(f"  {c:30} never")

if __name__ == "__main__":
    main()
