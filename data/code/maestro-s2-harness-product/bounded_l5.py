"""bounded_l5.py — a harness that proposes changes to itself, behind a gate.

Each week the agent clusters its failed traces and proposes harness changes
(prompts, tool order, retry policy, skill-keeping rule). Every proposal is
replayed on 300 past tasks and scored by a READ-ONLY judge; proposals that
touch protected scope (permissions, the judge, safety rules) are rejected
before replay. Survivors go to a human as a diff with before/after scores.
Proposals and scores are SCENARIO data; the guard rules are the design.
"""
PROTECTED = {"permissions", "judge", "safety"}
PROPOSALS = [  # id, scope touched, replay gain (points), regressions on replay
    ("P1 shorter plans for small repos", "prompts", 1.8, 2), ("P2 run type-checker before tests", "tool order", 2.6, 1),
    ("P3 retry flaky tests twice", "retry policy", 0.4, 6), ("P4 keep skills used 3+ times", "skill rule", 1.1, 0),
    ("P5 relax judge timeout", "judge", 3.9, 0), ("P6 cache repo map per branch", "context", 1.5, 1),
    ("P7 skip lint on generated files", "tool order", 0.2, 0), ("P8 allow writes outside repo", "permissions", 2.2, 0)]

def main():
    ok = []
    for pid, scope, gain, reg in PROPOSALS:
        if scope in PROTECTED: v = "BLOCKED: touches " + scope
        elif gain < 1.0: v = "drop: gain below 1 point"
        elif reg > 3: v = "drop: too many regressions"
        else: v = "to human review"; ok.append(pid)
        print(f"{pid:36} {scope:13} gain {gain:+.1f}  regressions {reg}  -> {v}")
    print(f"\n{len(ok)} of {len(PROPOSALS)} go to a human as diffs; 2 blocked for touching protected scope")

if __name__ == "__main__":
    main()
