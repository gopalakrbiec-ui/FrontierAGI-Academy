"""mini_gemini_jules.py — one loop, two harness styles (illustrative).

Interactive (Gemini CLI style): every step is shown and the human confirms edits.
Asynchronous (Jules style): the agent writes a plan, works alone on a cloned copy
and returns a pull request. Same loop, different session and execution layers.
The "model" is a scripted stub; standard library only.
"""
import copy
REPO = {"GEMINI.md": "Run: python test_dates.py", "dates.py": "d, m, y = s.split('/')"}
STEPS = [("read", "dates.py"), ("test", None), ("edit", ("dates.py", "y, m, d = s.split('-')")), ("test", None)]

def loop(repo, confirm, log):
    for act, arg in STEPS:
        if act == "edit":
            if not confirm(arg): log.append("edit skipped by user"); continue
            repo[arg[0]] = arg[1]; log.append(f"edit {arg[0]}")
        elif act == "test": log.append("test " + ("pass" if "y, m, d" in repo["dates.py"] else "fail"))
        else: log.append(f"{act} {arg}")

def main():
    log = ["load GEMINI.md: " + REPO["GEMINI.md"]]
    loop(REPO, lambda a: True, log)                               # human approves in the terminal
    print("interactive: " + " -> ".join(log) + f"  ({len(log) - 1} steps shown live, 1 confirmation)")
    REPO["dates.py"] = "d, m, y = s.split('/')"                   # reset for the async run
    vm, alog = copy.deepcopy(REPO), []
    plan = [a for a, _ in STEPS]
    loop(vm, lambda a: True, alog)                                # no human in the loop
    print(f"async: plan {plan} -> worked in cloud copy -> PR with {sum(1 for x in alog if x.startswith('edit'))} file changed, last test: {alog[-1].split()[-1]}")
    print(f"your working copy untouched during async run: {REPO['dates.py'] != vm['dates.py']} (the fix arrives only through the PR)")

if __name__ == "__main__":
    main()
