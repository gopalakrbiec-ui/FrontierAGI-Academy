"""boundary_check.py — check proposed experiments against the safety
boundary for their RSI level before they are allowed to run.

Policy (the story's; modelled on the gate in Season 1, Part 11):
  L1-L2  normal cluster; results reach the product only through the gate
  L3     + a safety reviewer signs the task-generation rules
  L4     + changes to product skills need two gate approvals
  L5     + isolated sandbox, no network, no write access to its own evaluator,
           a kill switch tested this week, and never touches the product
Experiments are SCENARIO proposals from the research tracks.
"""
RULES = {
    1: [],
    2: [],
    3: ["reviewer"],
    4: ["reviewer", "two_approvals"],
    5: ["reviewer", "sandbox", "no_network", "evaluator_readonly", "kill_switch", "no_product"],
}
PROPOSALS = [
    ("E-101", 1, "auto-tune eval sampling", set()),
    ("E-102", 2, "search over agent harness prompts", set()),
    ("E-103", 3, "generate tasks from customer failures", {"reviewer"}),
    ("E-104", 4, "promote 40 new skills to product", {"reviewer"}),
    ("E-105", 5, "let the loop edit its own reward checker", {"reviewer", "sandbox", "no_network", "kill_switch", "no_product"}),
    ("E-106", 5, "agent proposes new research directions", {"reviewer", "sandbox", "no_network", "evaluator_readonly", "kill_switch", "no_product"}),
]

def main():
    ok = 0
    for eid, lvl, what, has in PROPOSALS:
        missing = [r for r in RULES[lvl] if r not in has]
        ok += not missing
        print(f"{eid} L{lvl} {what:42} {'RUN' if not missing else 'BLOCKED: missing ' + ', '.join(missing)}")
    print(f"{ok} of {len(PROPOSALS)} may run")

if __name__ == "__main__":
    main()
