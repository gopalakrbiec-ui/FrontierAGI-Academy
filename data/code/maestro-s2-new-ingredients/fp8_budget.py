"""fp8_budget.py — what FP8 training buys Maestro-2.

H100 peak dense throughput doubles from BF16 (989 TFLOP/s) to FP8 (1,979).
Real end-to-end gains are far smaller: not every operation runs in FP8, and
communication and memory traffic do not speed up. The achieved speed-ups are
SCENARIO assumptions bracketing what public reports describe.
"""
FLOPS, PEAK, MFU, PRICE, GPUS = 1.06e25, 989e12, 0.40, 2.40, 4096

def main():
    base = FLOPS / (PEAK * MFU * 0.91) / 3600
    print(f"{'precision':26} {'GPU-hours':>10} {'days on 4,096':>14} {'cost $M':>8}")
    for name, sp in (("BF16 (baseline)", 1.0), ("FP8, cautious (x1.25)", 1.25), ("FP8, planned (x1.35)", 1.35), ("FP8, ideal peak (x2.0)", 2.0)):
        gh = base / sp
        print(f"{name:26} {gh / 1e6:9.2f}M {gh / GPUS / 24:14.0f} {gh * PRICE / 1e6:8.1f}")
    print(f"\nplanned saving: {(base - base / 1.35) * PRICE / 1e6:.1f} $M and {(base - base / 1.35) / GPUS / 24:.0f} days")

if __name__ == "__main__":
    main()
