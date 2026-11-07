"""mini_codex.py — a toy harness in the style of Codex (illustrative).

Delegation and isolation: each task gets its own copy of the repository (standing
in for a cloud container), reads AGENTS.md, works under an approval mode, and
hands back a diff for review. Several tasks run independently. The "model" is a
scripted stub; standard library only.
"""
import copy, difflib
REPO = {"AGENTS.md": "test: python test_dates.py\nconvention: minimal diffs\n",
        "dates.py": "def parse(s):\n    d, m, y = s.split('/')\n    return (int(y), int(m), int(d))\n",
        "README.md": "Date utils\n"}
MODES = {"read-only": set(), "auto": {"edit", "test"}, "full": {"edit", "test", "network"}}
PLANS = {"fix-date-test": [("test", None), ("edit", ("dates.py", "    d, m, y = s.split('/')\n", "    y, m, d = s.split('-')\n")), ("test", None)],
         "update-readme": [("edit", ("README.md", "Date utils\n", "Date utils (ISO 8601 input)\n"))],
         "fetch-deps": [("network", "pip download requests")]}

def run_task(name, mode):
    box = copy.deepcopy(REPO)                       # isolated container per task
    log = [f"read AGENTS.md: {box['AGENTS.md'].splitlines()[0]}"]
    for act, arg in PLANS[name]:
        if act not in MODES[mode]: log.append(f"{act}: blocked by '{mode}' mode"); continue
        if act == "edit": f, old, new = arg; box[f] = box[f].replace(old, new); log.append(f"edit {f}")
        elif act == "test": ok = "y, m, d" in box["dates.py"]; log.append("test: " + ("pass" if ok else "fail"))
    diff = [l for f in REPO for l in difflib.unified_diff(REPO[f].splitlines(), box[f].splitlines(), f"a/{f}", f"b/{f}", lineterm="", n=0)]
    return log, diff

def main():
    for name, mode in (("fix-date-test", "auto"), ("update-readme", "auto"), ("fetch-deps", "auto")):
        log, diff = run_task(name, mode)
        print(f"task {name} [{mode}]: " + "; ".join(log))
        print("  diff for review: " + (" | ".join(l for l in diff if l[:1] in "+-" and l[:3] not in ("+++", "---")) or "(no changes)"))
    print(f"original repo untouched: {'d, m, y' in REPO['dates.py']}")

if __name__ == "__main__":
    main()
