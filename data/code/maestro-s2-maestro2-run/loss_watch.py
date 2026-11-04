"""loss_watch.py — spotting a loss spike before it becomes a divergence.

A synthetic loss curve (falling, with noise) has three injected spikes. The
watcher compares each step with a rolling mean and standard deviation of the
last 50 steps: z > 4 once = skip that batch; z > 4 three steps in a row =
roll back to the last checkpoint and lower the learning rate. The curve is
SYNTHETIC; the rules mirror common practice.
"""
import math, random, statistics as st
random.seed(3)
SPIKES = {1200: [1.2], 2600: [0.9, 1.1, 1.3, 1.2], 4100: [0.7]}

def curve(n=5000):
    out, i = [], 0
    while i < n:
        base = 1.85 + 2.2 * math.exp(-i / 900) + random.gauss(0, 0.02)
        if i in SPIKES:
            for s in SPIKES[i]: out.append(base + s); i += 1
            continue
        out.append(base); i += 1
    return out

def main():
    ys, hot = curve(), 0
    for i in range(50, len(ys)):
        w = ys[i - 50:i]; z = (ys[i] - st.mean(w)) / (st.stdev(w) + 1e-9)
        hot = hot + 1 if z > 4 else 0
        if hot == 1: print(f"step {i}: z={z:5.1f}  skip batch")
        if hot == 3: print(f"step {i}: z={z:5.1f}  3 in a row -> ROLL BACK to last checkpoint, lower LR 20%")
    print(f"\nfinal loss {st.mean(ys[-50:]):.3f}; spikes handled without a restart from scratch")

if __name__ == "__main__":
    main()
