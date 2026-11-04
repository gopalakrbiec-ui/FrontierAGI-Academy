"""cluster_plan.py — how many GPUs for Maestro-2, and for how long?

Days = FLOPs / (GPUs x peak x MFU x goodput x 86,400). Bigger clusters finish
sooner but lose some efficiency (MFU) and more time to failures (goodput).
Peak is the H100's dense BF16 figure; goodput is 1 minus the time lost per day in failure_rate.py;
MFU and prices are SCENARIO
assumptions.
"""
FLOPS, PEAK, PRICE = 9.6e24 * 1.10, 989e12, 2.40   # B2 plus 10% headroom

def main():
    print(f"target {FLOPS:.2e} FLOPs (option B2 + 10% headroom)\n")
    print(f"{'GPUs':>6} {'MFU':>5} {'goodput':>8} {'days':>6} {'GPU-hours':>10} {'cost $M':>8}")
    for g, mfu, gp in ((2048, 0.42, 0.94), (4096, 0.40, 0.91), (8192, 0.37, 0.86)):
        days = FLOPS / (g * PEAK * mfu * gp * 86400); gh = g * days * 24
        print(f"{g:6} {mfu:5.0%} {gp:8.0%} {days:6.0f} {gh / 1e6:9.2f}M {gh * PRICE / 1e6:8.1f}")

if __name__ == "__main__":
    main()
