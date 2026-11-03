"""moat_futures.py — score five candidate moats under three market futures,
then pick the one that holds up best (minimum regret), not the one that wins
the single most likely future.

Scores (0-10) and future probabilities are the story's SCENARIO estimates.
Futures: A = frontier labs ship strong coding agents fast;
         B = open models catch up and prices collapse;
         C = regulation makes change-by-change evidence mandatory.
"""
MOATS = {
    "verified environments at scale": (8, 7, 8),
    "customer skill library (today)": (6, 5, 8),
    "automated harness design": (5, 7, 4),
    "self-improving tool use": (7, 4, 5),
    "long-horizon agents": (4, 3, 5),
}
P = (0.45, 0.30, 0.25)

def main():
    best = [max(v[i] for v in MOATS.values()) for i in range(3)]
    print(f"{'moat':32} {'A':>3} {'B':>3} {'C':>3} {'expected':>9} {'worst regret':>13}")
    rows = []
    for m, v in MOATS.items():
        ev = sum(p * s for p, s in zip(P, v))
        regret = max(b - s for b, s in zip(best, v))
        rows.append((regret, -ev, m, v, ev))
    for regret, _, m, v, ev in sorted(rows):
        print(f"{m:32} {v[0]:3} {v[1]:3} {v[2]:3} {ev:9.2f} {regret:13}")
    pick = sorted(rows)[0]
    print(f"robust pick: {pick[2]} (worst regret {pick[0]}, expected {pick[4]:.2f})")

if __name__ == "__main__":
    main()
