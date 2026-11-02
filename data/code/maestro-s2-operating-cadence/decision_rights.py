"""decision_rights.py — check the company's decision table for the usual faults.

Roles per decision use RAPID-style letters (Bain & Company): R recommend,
A agree (veto), P perform, I input, D decide. The table is the story's
SCENARIO; the checks are the point:
  1. exactly one D per decision;
  2. nobody holds both R and D on a gate decision (no self-approval);
  3. the CEO is not the sole D on gate decisions (the gate stays independent);
  4. every decision has someone who performs it.
"""
T = {
    "ship a model update (gate)":    {"research lead": "R", "safety lead": "D", "gate reviewer 2": "A", "CEO": "I", "infra head": "P"},
    "start a training run > $1M":    {"research lead": "R", "CEO": "D", "board": "A", "infra head": "P", "finance": "I"},
    "hire a team lead":              {"CEO": "D", "team leads": "I", "people ops": "P"},
    "price change":                  {"head of sales": "R", "CEO": "D", "finance": "I", "product head": "I"},
    "new customer data agreement":   {"head of sales": "R", "counsel": "A", "CEO": "D", "security": "P"},
    "release to a new customer tier":{"product head": "R", "safety lead": "A", "CEO": "D", "infra head": "P"},
    "change the gate's thresholds":  {"safety lead": "R", "CEO": "D", "board": "A", "research lead": "I"},
    "pause the self-improvement loop": {"safety lead": "D", "on-call engineer": "P", "CEO": "I"},
}

def check(table):
    issues = []
    for dec, roles in table.items():
        ds = [p for p, r in roles.items() if "D" in r]
        if len(ds) != 1: issues.append(f"{dec}: {len(ds)} deciders")
        if "P" not in "".join(roles.values()): issues.append(f"{dec}: nobody performs it")
        if "gate" in dec or "loop" in dec:
            if any("R" in r and "D" in r for r in roles.values()): issues.append(f"{dec}: self-approval")
            if ds == ["CEO"] and "A" not in "".join(roles.values()): issues.append(f"{dec}: CEO alone decides a gate matter")
    return issues

def main():
    print(f"{len(T)} decisions checked")
    for i in check(T) or ["no faults"]:
        print(" ", i)
    bad = dict(T); bad["ship a model update (gate)"] = {"research lead": "RD", "CEO": "I", "infra head": "P"}
    bad["change the gate's thresholds"] = {"CEO": "RD", "infra head": "P"}
    print("a tempting shortcut (research lead ships its own updates, CEO tunes the gate):")
    for i in check(bad):
        print(" ", i)

if __name__ == "__main__":
    main()
