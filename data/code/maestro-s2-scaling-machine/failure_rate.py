"""failure_rate.py — interruptions scale with GPU count.

Rate from Meta's Llama 3 report: 419 unexpected interruptions in a 54-day
snapshot on 16,384 H100 GPUs. Checkpoint interval from Young's approximation,
interval = sqrt(2 x checkpoint cost x mean time between failures).
Checkpoint and restart times are SCENARIO assumptions.
"""
import math
RATE = 419 / (16384 * 54)            # interruptions per GPU-day (Llama 3 snapshot)
CKPT_MIN, RESTART_MIN = 2.0, 15.0    # minutes to save a checkpoint; to detect, replace and restart

def main():
    print(f"rate: {RATE:.2e} interruptions per GPU-day\n")
    print(f"{'GPUs':>6} {'per day':>8} {'MTBF h':>7} {'ckpt every':>10} {'lost/day':>9}")
    for g in (2048, 4096, 8192, 16384):
        per_day = RATE * g; mtbf = 24 * 60 / per_day; iv = math.sqrt(2 * CKPT_MIN * mtbf)
        lost = per_day * (RESTART_MIN + iv / 2) + (24 * 60 / iv) * CKPT_MIN   # minutes per day
        print(f"{g:6} {per_day:8.1f} {mtbf / 60:7.1f} {iv:8.0f} m {lost / 1440:9.1%}")

if __name__ == "__main__":
    main()
