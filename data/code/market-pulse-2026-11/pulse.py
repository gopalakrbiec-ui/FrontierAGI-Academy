"""pulse.py — AI Market Pulse, monthly issue: counts the month from the site's own data.

Reads data/lab-updates.json, data/model-releases.json, data/ai-investments.json and
data/predictions-2027.json. Prints this month's lab announcements by lab, releases by
modality and open share, the latest reported funding quarter, and predictions due.
Change MONTH to produce the next issue. Standard library only.
"""
import json, os
MONTH = "2026-11"
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
lu = json.load(open(os.path.join(D, "lab-updates.json")))["items"]
mr = json.load(open(os.path.join(D, "model-releases.json")))["items"]
iv = json.load(open(os.path.join(D, "ai-investments.json")))
pr = json.load(open(os.path.join(D, "predictions-2027.json")))["items"]
LATER = ['anthropic-20261118-ipo-priced', 'anthropic-20261123-claude-ship', 'microsoft-20261117-mai-code-2', 'openai-20250121-the-stargate-project', 'openai-20250819-chatgpt-go', 'openai-20250925-chatgpt-pulse', 'openai-20250929-instant-checkout-and-the-agentic-commerc', 'openai-20251120-group-chats-in-chatgpt', 'openai-20260426-sora-app-discontinued', 'openai-20260929-agents-api-with-computer-use-decisions', 'openai-20260929-chatgpt-space-and-private-intelligence', 'openai-20260929-dots-always-on-agents-in-chatgpt', 'openai-20260929-ultrafast-tier-and-pro-500', 'openai-20261113-chatgpt-wallet']  # items added to the data after this article was published (backfills); excluded so the output matches the page
lu = [x for x in lu if x.get("id") not in LATER]
mr = [x for x in mr if x.get("id") not in LATER]
CUTOFF = "2026-11-17"  # last data date before this issue was published (18 Nov); later items belong to the next issue
items = [x for x in lu if str(x["date"]).startswith(MONTH) and str(x["date"]) <= CUTOFF]
by = {}
for x in items: by[x["lab"]] = by.get(x["lab"], 0) + 1
print(f"{MONTH}: {len(items)} lab announcements, {sum(1 for x in items if x.get('flagship'))} flagship")
print("  by lab: " + ", ".join(f"{k} {v}" for k, v in sorted(by.items(), key=lambda kv: -kv[1])))
rel = [x for x in mr if str(x["date"]).startswith(MONTH) and str(x["date"]) <= CUTOFF]
mods = {}
for x in rel:
    for m in x["mod"]: mods[m] = mods.get(m, 0) + 1
print(f"  model releases: {len(rel)} ({', '.join(f'{k} {v}' for k, v in sorted(mods.items(), key=lambda kv: -kv[1]))}); open-weight {sum(1 for x in rel if x.get('open') in (1, 2))}")
q = iv["quarters"][-1]
print(f"latest funding quarter reported: {q['q']} ${q['total']}B ({q['by']})")
due = [p for p in pr if p["check"] <= MONTH]
print(f"predictions due by {MONTH}: {len(due)} of {len(pr)}; next check {min(p['check'] for p in pr)}")
