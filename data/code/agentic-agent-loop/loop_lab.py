"""loop_lab.py — one agent loop, five "dial settings" in the style of five harnesses (illustrative).

The same task (a failing date test -> fix -> open a PR) runs through one loop whose dials
are set the way each harness documents its behaviour: planning, approvals, sub-loops,
compaction, and whether it writes something reusable after the task. The "model" is a
scripted stub, so the run is repeatable; token counts are our rough model (4 chars/token).
Standard library only.
"""
PROFILES = {   # plan, approve edits?, subagent explore?, compact at (tokens), learn after task?, async?
    "Claude Code":  dict(plan="todo list", ask_edit=True,  sub=True,  compact=1200, learn="memory note", run="interactive"),
    "Codex":        dict(plan="plan step", ask_edit=False, sub=False, compact=1200, learn=None,          run="sandboxed"),
    "Gemini/Jules": dict(plan="plan approval", ask_edit=False, sub=False, compact=9000, learn=None,       run="async VM"),
    "Deep Agents":  dict(plan="write_todos", ask_edit=True, sub=True,  compact=1200, learn=None,          run="in your app"),
    "Hermes Agent": dict(plan="todo list", ask_edit=False, sub=True,  compact=1200, learn="new skill",   run="interactive"),
}
BIG_LOG = "x" * 6000                      # a noisy test log: observation handling matters

def tok(lines): return sum(len(l) for l in lines) // 4

def run(name, p, truncate=True, known=False):
    ctx = ["system: repo rules", "user: date test fails; fix it and open a PR"]
    turns = calls = approvals = compactions = 0
    steps = [("plan", p["plan"])]
    if not known:
        steps += [("explore", "subagent summary: parse() in dates.py")] if p["sub"] else [("search", "dates.py"), ("read", "dates.py, test_dates.py")]
    steps += [("bash", "FAIL ValueError\n" + BIG_LOG), ("edit", "dates.py"), ("bash", "PASS"), ("git", "PR opened")]
    for act, out in steps:
        turns += 1; calls += 1
        if act == "edit" and p["ask_edit"]: approvals += 1
        if act == "plan" and p["plan"] == "plan approval": approvals += 1
        if truncate and act == "bash" and len(out) > 2000: out = out[:200] + " ...[truncated, full log saved to file]"
        ctx.append(f"{act}: {out}")
        if tok(ctx) > p["compact"]: ctx = ctx[:2] + ["summary of earlier turns"] + ctx[-1:]; compactions += 1
    learned = p["learn"] or "-"
    return turns, calls, approvals, compactions, tok(ctx), learned

print(f"{'harness':13} {'turns':>5} {'calls':>5} {'asks':>4} {'compact':>7} {'ctx tok':>7}  after task")
for name, p in PROFILES.items():
    t, c, a, k, x, l = run(name, p)
    print(f"{name:13} {t:5} {c:5} {a:4} {k:7} {x:7}  {l}")
print()
t, c, a, k, x, l = run("Claude Code", PROFILES["Claude Code"], truncate=False)
print(f"without truncating the test log: ctx {x} tokens after {k} compaction(s)")
for name in ("Claude Code", "Hermes Agent"):
    t2 = run(name, PROFILES[name], known=True)[0]
    print(f"{name}: rerun of a similar task with what it kept: {t2} turns instead of {run(name, PROFILES[name])[0]}")
print("same task, same model stub: the dials change approvals, context and what is kept afterwards")
