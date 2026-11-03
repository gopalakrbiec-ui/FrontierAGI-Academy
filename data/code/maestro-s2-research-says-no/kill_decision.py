"""kill_decision.py — the long-horizon agents direction against the kill
criteria written before it started (month 27). SCENARIO results, month 33.

A direction is killed if ANY pre-registered criterion fails at its checkpoint.
"""
CRITERIA = [  # name, target, observed, higher is better
    ("held-out tasks solved, 4h+ horizon (%)", 25, 11, True),
    ("gain over the L4 skill library baseline (pts)", 3.0, 0.4, True),
    ("cost per solved task vs product ($)", 2.0, 6.8, False),
    ("customers who would pay in interviews (of 12)", 4, 5, True),
]

def main():
    fails = 0
    for name, target, obs, up in CRITERIA:
        ok = obs >= target if up else obs <= target
        fails += not ok
        print(f"{name:48} target {target:>5}  observed {obs:>5}  {'pass' if ok else 'FAIL'}")
    print("decision:", "KILL the direction" if fails else "continue", f"({fails} of {len(CRITERIA)} criteria failed)")

if __name__ == "__main__":
    main()
