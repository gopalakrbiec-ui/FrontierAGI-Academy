"""mini_claude_code.py — a toy harness in the style of Claude Code (illustrative).

One general agent loop + configuration: an instructions file loaded every session,
built-in tools, permission rules, a post-edit hook and a subagent with its own
context. The "model" is a scripted stub so the run is repeatable; a real harness
calls an LLM API at the marked line. Standard library only.
"""
REPO = {"dates.py": "def parse(s):\n    d, m, y = s.split('/')\n    return (int(y), int(m), int(d))\n",
        "test_dates.py": "from dates import parse\nassert parse('2026-11-07') == (2026, 11, 7)\n"}
MEMORY = "Run tests with: python test_dates.py\nKeep diffs minimal."          # CLAUDE.md
PERMS = {"read": "allow", "search": "allow", "edit": "ask", "bash": "allow:tests"}
APPROVE = {"edit"}                                                         # the human says yes to edits

def run_tests():
    try:
        ns = {}; exec(REPO["dates.py"], ns)
        y = ns["parse"]("2026-11-07"); return "PASS" if y == (2026, 11, 7) else f"FAIL got {y}"
    except Exception as e:
        return f"FAIL {type(e).__name__}: {e}"

def tool(name, arg):
    rule = PERMS.get(name, "deny")
    if rule == "ask" and name not in APPROVE: return "denied by user"
    if name == "read": return REPO[arg]
    if name == "search": return [f for f, t in REPO.items() if arg in t]
    if name == "bash": return run_tests()
    if name == "edit":
        REPO[arg[0]] = arg[1]; return "edited " + arg[0] + " | hook: formatted"   # PostToolUse-style hook
    return "unknown tool"

def subagent(task):                     # own context: only the summary returns to the main loop
    hits = tool("search", "parse")
    return f"subagent summary: '{task}' -> parse() lives in {hits[0]}, test expects ISO dates"

SCRIPT = [("subagent", "find the failing test and the code it covers"), ("bash", None),
          ("edit", ("dates.py", "def parse(s):\n    y, m, d = s.split('-')\n    return (int(y), int(m), int(d))\n")),
          ("bash", None), ("done", "fixed parse() for ISO dates; tests pass; PR ready")]

def model(turn, context):               # <- a real harness calls the LLM here
    return SCRIPT[turn]

def main():
    context = ["system: " + MEMORY.splitlines()[0], "user: the date test fails, fix it and open a PR"]
    for turn in range(10):
        act, arg = model(turn, context)
        if act == "done": print(f"turn {turn + 1}: DONE  {arg}"); break
        out = subagent(arg) if act == "subagent" else tool(act, arg)
        context.append(f"{act} -> {out}")
        print(f"turn {turn + 1}: {act:8} [{PERMS.get(act, 'allow')}] -> {str(out).splitlines()[0]}")
    print(f"context lines: {len(context)} (the subagent's search stayed out of the main context)")

if __name__ == "__main__":
    main()
