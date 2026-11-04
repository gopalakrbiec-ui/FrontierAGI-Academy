"""eu_line.py — will Maestro-2 cross the EU AI Act compute line?

The AI Act presumes a general-purpose model has systemic-risk capabilities when
its cumulative training compute exceeds 10^25 FLOPs (Article 51(2)). Which later
stages count, and how exactly, should be checked against the Commission's
guidelines with counsel. The ledger entries are SCENARIO estimates.
"""
LINE = 1e25
LEDGER = [("pre-training, option B2", 9.60e24), ("long-context mid-training", 0.30e24),
          ("RL post-training (environments)", 0.45e24), ("skill fine-tunes (per customer)", 0.02e24)]

def main():
    tot = 0
    for name, f in LEDGER:
        tot += f; print(f"{name:34} {f:9.2e}   running total {tot:9.2e}  ({tot / LINE:5.1%} of line)")
    print(f"\ntotal {tot:.2e} FLOPs: {'ABOVE' if tot > LINE else 'below'} the 1e25 presumption by {abs(tot - LINE) / LINE:.1%}")
    need = (tot - LINE) / (6 * 32e9)
    print(f"to stay under, cut pre-training by {need / 1e12:.1f}T tokens (from 50T) or drop the RL stage")

if __name__ == "__main__":
    main()
