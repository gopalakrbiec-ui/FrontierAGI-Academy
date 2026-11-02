"""gate_roster.py — assign two reviewers to each gate review without conflicts.

As the team grows, the gate (Part 11) needs more reviewers than Gopala.
Rules: a reviewer may not have authored the update or manage its author,
and at least one reviewer per review comes from the safety team.
Updates and reviewers are the story's SCENARIO; the assignment is greedy
and balances load, then reports any review it could not staff.
"""
REVIEWERS = {"safety lead": ("safety", None), "red-team eng": ("safety", "safety lead"),
             "eval eng": ("safety", "safety lead"), "research lead": ("research", None),
             "infra head": ("infra", None), "Gopala": ("exec", None)}
MANAGES = {"research lead": {"env eng", "data eng", "rl eng"}, "safety lead": {"red-team eng", "eval eng"}}
UPDATES = [("u-41", "env eng"), ("u-42", "rl eng"), ("u-43", "data eng"), ("u-44", "red-team eng"),
           ("u-45", "research lead"), ("u-46", "env eng"), ("u-47", "rl eng"), ("u-48", "eval eng")]

def ok(rev, author):
    return rev != author and author not in MANAGES.get(rev, set())

def main():
    load = {r: 0 for r in REVIEWERS}
    for uid, author in UPDATES:
        safety = sorted((r for r, (t, _) in REVIEWERS.items() if t == "safety" and ok(r, author)), key=lambda r: load[r])
        if not safety:
            print(f"{uid} by {author:13}: CANNOT STAFF (no eligible safety reviewer) -> escalate"); continue
        first = safety[0]
        rest = sorted((r for r in REVIEWERS if r != first and ok(r, author)), key=lambda r: (load[r], r == "Gopala"))
        second = rest[0]
        load[first] += 1; load[second] += 1
        print(f"{uid} by {author:13}: {first} + {second}")
    print("load:", ", ".join(f"{r} {n}" for r, n in load.items()))

if __name__ == "__main__":
    main()
