"""run_sim.py — 4,096 GPUs, one long run, simulated day by day.

Interruptions arrive at the Llama 3 rate (419 in 54 days on 16,384 GPUs).
Each costs a restart plus, on average, half a checkpoint interval of lost work.
Seeded random numbers make the output repeatable. Restart time and the planned
step budget are SCENARIO assumptions; this is a simulation, not a real run.
"""
import random
random.seed(7)
GPUS, RATE, CKPT_MIN, RESTART_MIN, IV = 4096, 419 / (16384 * 54), 2.0, 15.0, 54
NEED_HOURS = 56.0 * 24        # productive hours needed (FP8 plan: ~56 days of pure compute)

def main():
    done, day, intr, lost = 0.0, 0, 0, 0.0
    while done < NEED_HOURS:
        day += 1; k = sum(1 for _ in range(GPUS) if random.random() < RATE)
        l = (k * (RESTART_MIN + IV / 2) + (1440 / IV) * CKPT_MIN) / 60
        intr += k; lost += l; done += 24 - l
        if day % 10 == 0: print(f"day {day:3}: {intr:4} interruptions so far, {done / NEED_HOURS:5.1%} of the run done")
    print(f"\nfinished on day {day}: {intr} interruptions, {lost:.0f} hours lost, goodput {(day * 24 - lost) / (day * 24):.1%}")

if __name__ == "__main__":
    main()
