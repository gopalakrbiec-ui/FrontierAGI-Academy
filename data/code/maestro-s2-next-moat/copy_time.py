"""copy_time.py — how long would a well-funded rival need to copy each moat?

months = build_months / (1 + rival_speedup) + data_months, where data_months
is the time to collect what cannot be bought (customer tasks, gate history).
All inputs are the story's SCENARIO estimates; the rival is assumed to have
3x Maestro's engineers (speedup 2).
"""
MOATS = {  # build months for Maestro, months of data that cannot be bought
    "verified environments at scale": (18, 12),
    "customer skill library (today)": (12, 18),
    "automated harness design": (9, 0),
    "self-improving tool use": (12, 3),
    "long-horizon agents": (15, 0),
}
SPEEDUP = 2

def main():
    for m, (build, data) in sorted(MOATS.items(), key=lambda kv: -(kv[1][0] / (1 + SPEEDUP) + kv[1][1])):
        months = build / (1 + SPEEDUP) + data
        print(f"{m:32} {months:5.1f} months  {'durable' if months >= 12 else 'copyable'}")

if __name__ == "__main__":
    main()
