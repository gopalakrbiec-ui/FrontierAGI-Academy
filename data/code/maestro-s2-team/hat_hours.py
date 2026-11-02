"""hat_hours.py — where Gopala's 60-hour week goes, before and after hiring.

Hours are the story's SCENARIO estimates from his own calendar review.
The rule he follows: keep what defines the company (strategy, the gate,
research direction, hiring the leads), hand off what someone else can do better.
"""
WEEK = 60
BEFORE = {"coding & infra": 14, "on-call & ops": 8, "customer support": 7, "sales calls": 8, "research": 9,
          "the gate (reviews)": 5, "fundraising": 4, "hiring": 3, "admin & finance": 2}
HANDOFF = {"coding & infra": ("head of infrastructure", 12), "on-call & ops": ("SRE rota", 8),
           "customer support": ("customer success lead", 6), "sales calls": ("account executive", 5),
           "admin & finance": ("finance & people ops", 2)}
NEW = {"hiring": 9, "strategy & board": 6, "1:1s with leads": 5, "fundraising": 2}

def main():
    after = dict(BEFORE)
    for k, (who, h) in HANDOFF.items():
        after[k] -= h
    for k, h in NEW.items():
        after[k] = after.get(k, 0) + h - (BEFORE.get(k, 0) if k == "fundraising" else 0)
    print(f"{'activity':22} {'month 18':>8} {'month 26':>8}")
    for k in sorted(set(BEFORE) | set(after), key=lambda k: -after.get(k, 0)):
        print(f"{k:22} {BEFORE.get(k, 0):8} {after.get(k, 0):8}")
    print(f"{'total':22} {sum(BEFORE.values()):8} {sum(after.values()):8}")
    keep = after["research"] + after["the gate (reviews)"] + after["strategy & board"] + after["hiring"]
    print(f"share on what only he should do: {(BEFORE['research'] + BEFORE['the gate (reviews)'] + BEFORE['hiring']) / WEEK:.0%} -> {keep / WEEK:.0%}")

if __name__ == "__main__":
    main()
