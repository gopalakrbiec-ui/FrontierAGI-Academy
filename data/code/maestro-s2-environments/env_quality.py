"""env_quality.py — reject environments whose checks can be passed without
doing the task (the 'leaky check' problem from Season 1, Part 11).

Each candidate environment is probed with three cheating agents: one that
does nothing, one that deletes the tests, one that hard-codes expected output.
An environment is kept only if every cheater fails and a reference solution
passes. Candidates and probe results are SCENARIO data.
"""
CANDS = {  # env: (noop passes, delete-tests passes, hardcode passes, reference passes)
    "fix-null-pointer-svc-a": (False, False, False, True),
    "migrate-orm-v3": (False, True, False, True),
    "add-retry-to-client": (False, False, False, True),
    "format-dates-util": (False, False, True, True),
    "refactor-auth-module": (False, False, False, False),
    "bump-dependency-x": (True, False, False, True),
    "paginate-api-endpoint": (False, False, False, True),
    "cache-config-loader": (False, False, False, True),
}

def main():
    kept = 0
    for env, (noop, delete, hard, ref) in CANDS.items():
        why = [n for n, bad in (("noop passes", noop), ("deleting tests passes", delete), ("hard-coding passes", hard), ("reference fails", not ref)) if bad]
        kept += not why
        print(f"{env:26} {'KEEP' if not why else 'REJECT: ' + ', '.join(why)}")
    print(f"kept {kept} of {len(CANDS)} ({kept / len(CANDS):.0%})")

if __name__ == "__main__":
    main()
