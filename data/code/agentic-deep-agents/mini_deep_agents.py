"""mini_deep_agents.py — a toy harness in the style of Deep Agents (illustrative).

A harness as a library: a to-do planner, sub-agents with isolated context, and a
filesystem used as working memory so large tool outputs do not flood the context.
The "model" is a scripted stub; standard library only.
"""
FS = {}                                     # pluggable filesystem backend (here: a dict)
LIMIT = 200                                 # characters of tool output allowed into context

def tool_run_tests():
    return "collected 812 tests\n" + "." * 811 + "F\nFAILED test_dates.py::test_iso - ValueError: not enough values"

def offload(name, text):
    if len(text) <= LIMIT: return text
    FS[name] = text; return f"[{len(text)} chars saved to /{name}; last line: {text.splitlines()[-1]}]"

def subagent(question):
    ctx = [question, offload("tests.log", tool_run_tests())]      # its own, throwaway context
    FS["findings.md"] = "parse() splits on '/', test passes ISO '2026-11-07'"
    return "see /findings.md", len(ctx)

def main():
    todos = ["reproduce failure", "find cause", "fix parse()", "re-run tests"]
    ctx = ["user: fix the failing date test"]
    print("plan: " + " | ".join(f"[ ] {t}" for t in todos))
    note, n = subagent("why does test_dates fail?")
    ctx.append("subagent: " + note); todos[0] = todos[1] = None
    FS["dates.py"] = "y, m, d = s.split('-')"; ctx.append("edit dates.py")
    log2 = "collected 812 tests\n" + "." * 812 + "\n812 passed"
    ctx.append(offload("tests2.log", log2))
    print("plan: " + " | ".join("[x] " + t for t in ["reproduce failure", "find cause", "fix parse()", "re-run tests"]))
    print(f"main context: {len(ctx)} messages, {sum(len(c) for c in ctx)} chars; files: {sorted(FS)}")
    print(f"without offloading, the two test logs would add {len(tool_run_tests()) + len(log2)} chars to the context")

if __name__ == "__main__":
    main()
