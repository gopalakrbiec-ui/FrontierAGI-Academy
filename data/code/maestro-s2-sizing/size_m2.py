"""size_m2.py — sizing Maestro-2 under a compute budget.

Training compute uses the standard estimate FLOPs ~= 6 x N x D (N = parameters
active per token, D = training tokens). Loss is predicted with the Chinchilla
fit of Hoffmann et al. (2022): L = E + A/N^a + B/D^b. Applying a dense-model
fit to a mixture-of-experts model by using ACTIVE parameters is a rough
approximation, used here only to rank options. Prices, MFU and the candidate
shapes and the two penalty weights are SCENARIO assumptions. Maestro-1's row
counts the final run only.
"""
E, A, B, a, b = 1.69, 406.4, 410.7, 0.34, 0.28   # Hoffmann et al. 2022, fit 3
PEAK, MFU, PRICE = 989e12, 0.40, 2.40            # H100 dense BF16 FLOP/s; our MFU; $/GPU-hour

def loss(n, d): return E + A / n ** a + B / d ** b

def main():
    cands = [("Maestro-1 (today)", 11.7e9, 10e12), ("B1: 24B active, 60T", 24e9, 60e12),
             ("B2: 32B active, 50T", 32e9, 50e12), ("B3: 40B active, 48T", 40e9, 48e12),
             ("B4: 70B active, 25T", 70e9, 25e12)]
    print(f"{'option':22} {'FLOPs':>9} {'tok/param':>9} {'GPU-hours':>10} {'cost $M':>8} {'pred. loss':>10}")
    for name, n, d in cands:
        f = 6 * n * d; gh = f / (PEAK * MFU) / 3600
        print(f"{name:22} {f:9.2e} {d / n:9.0f} {gh / 1e6:9.2f}M {gh * PRICE / 1e6:8.1f} {loss(n, d):10.3f}")
    # score = predicted loss + training-cost penalty + serving-cost penalty (active params drive serving cost)
    print(f"\n{'option':22} {'loss':>6} {'+train':>7} {'+serve':>7} {'score':>7}")
    sc = []
    for name, n, d in cands[1:]:
        tr, sv = 0.002 * 6 * n * d / 1e24, 0.0006 * n / 1e9
        sc.append((loss(n, d) + tr + sv, name)); print(f"{name:22} {loss(n, d):6.3f} {tr:7.4f} {sv:7.4f} {sc[-1][0]:7.4f}")
    print(f"\nchosen (lowest score): {min(sc)[1]}")

if __name__ == "__main__":
    main()
