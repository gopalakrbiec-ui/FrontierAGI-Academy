"""security_review.py — what enterprise security teams ask, and the gaps.

Items common in enterprise security questionnaires for AI vendors, with the
status at month 42 and weeks to close each gap. Status and weeks are SCENARIO.
"""
ITEMS = [("SOC 2 Type II report", "in progress", 16), ("SSO / SCIM", "done", 0), ("audit logs of every agent action", "done", 0),
         ("data residency (EU region)", "gap", 10), ("no training on customer code by default", "done", 0), ("customer-managed keys", "gap", 8),
         ("model card + EU AI Act status", "done", 0), ("agent permission scopes per repo", "done", 0), ("pen-test report (last 12 months)", "gap", 6),
         ("incident response SLA", "done", 0)]

def main():
    for n, s, w in ITEMS: print(f"{n:42} {s:12} {('+' + str(w) + ' wk') if w else ''}")
    gaps = [i for i in ITEMS if i[1] != "done"]
    print(f"\n{len(ITEMS) - len(gaps)} of {len(ITEMS)} ready; {len(gaps)} open; longest {max(g[2] for g in gaps)} weeks (run in parallel)")

if __name__ == "__main__":
    main()
