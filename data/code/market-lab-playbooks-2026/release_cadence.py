"""release_cadence.py — how each frontier lab spent 2026, from the site's own data.

Reads data/lab-updates.json (Frontier Lab Updates) and counts, per lab, the 2026 items
by type (model, product, API, pricing, research, company) and flagship releases.
Standard library only.
"""
import json, os
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab-updates.json")))
LATER = ['anthropic-20261118-ipo-priced', 'anthropic-20261123-claude-ship', 'microsoft-20261117-mai-code-2', 'openai-20250121-the-stargate-project', 'openai-20250819-chatgpt-go', 'openai-20250925-chatgpt-pulse', 'openai-20250929-instant-checkout-and-the-agentic-commerc', 'openai-20251120-group-chats-in-chatgpt', 'openai-20260426-sora-app-discontinued', 'openai-20260929-agents-api-with-computer-use-decisions', 'openai-20260929-chatgpt-space-and-private-intelligence', 'openai-20260929-dots-always-on-agents-in-chatgpt', 'openai-20260929-ultrafast-tier-and-pro-500', 'openai-20261113-chatgpt-wallet']  # items added to the data after this article was published (backfills); excluded so the output matches the page
d["items"] = [x for x in d["items"] if x.get("id") not in LATER]
T = [t[0] for t in d["types"]]
by = {}
CUTOFF = "2026-11-17"  # last data date before this brief was published (18 Nov); later items are left out
for x in d["items"]:
    if not str(x["date"]).startswith("2026") or str(x["date"]) > CUTOFF: continue
    r = by.setdefault(x["lab"], {t: 0 for t in T}); r[x["type"]] += 1; r["flag"] = r.get("flag", 0) + (1 if x.get("flagship") else 0)
print(f"{'lab':10} {'total':>5} " + " ".join(f"{t[:7]:>7}" for t in T) + " flagship")
for lab, r in sorted(by.items(), key=lambda kv: -sum(kv[1][t] for t in T)):
    tot = sum(r[t] for t in T)
    print(f"{lab:10} {tot:5d} " + " ".join(f"{r[t]:7d}" for t in T) + f" {r.get('flag', 0):8d}")
tot = sum(sum(r[t] for t in T) for r in by.values()); prod = sum(r["product"] for r in by.values())
print(f"2026 items: {tot}; products/features {prod / tot:.0%}. Coverage is uneven by lab (see article), so compare patterns, not totals")
