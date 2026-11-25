#!/usr/bin/env python3
"""Pull recent posts from chosen X (Twitter) accounts and keep the likely announcements as TIPS for review.

    python3 scripts/fetch_x_tips.py                 # needs X_BEARER_TOKEN (app-only token, paid X API tier)
    python3 scripts/fetch_x_tips.py --days 3
    python3 scripts/fetch_x_tips.py --selftest      # offline check, no network, no token

Accounts come from data/x-watchlist.json ("accounts": handles without @). If X_USER_TOKEN (a user OAuth 2.0
token with tweet.read users.read) and X_USER_ID are set, the script instead reads that user's own
"Following" timeline (GET /2/users/:id/timelines/reverse_chronological), i.e. posts from everyone they follow.

Output: data/x-tips.json. TIPS ONLY: the site never renders this file. Each tip is checked against the
primary source (lab blog, paper, filing) and, if it holds up, added to data/lab-updates.json /
model-releases.json / benchmarks.json / ai-investments.json with that source, by a person or the weekly
review session. Only post id, author, date, link, matched keywords and a short snippet are stored.
Needs network access to api.x.com (not reachable from the authoring sandbox; runs in GitHub Actions).
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WATCH = ROOT / "data" / "x-watchlist.json"
OUT = ROOT / "data" / "x-tips.json"
API = "https://api.x.com/2"
SNIP = 200
# (pattern, weight, label). Case-insensitive on post text.
TERMS = [
    (r"\bintroduc(ing|es|ed)\b", 3, "introducing"), (r"\blaunch(ing|es|ed)?\b", 3, "launch"), (r"\breleas(e|ing|ed)\b", 2, "release"),
    (r"\bnow available\b|\bgenerally available\b|\bin preview\b", 3, "availability"), (r"\bopen[- ]?(source|weights?)\b", 2, "open weights"),
    (r"\bmodel\b", 1, "model"), (r"\bbenchmark|\bstate[- ]of[- ]the[- ]art\b|\bsota\b|\bscore[sd]?\b", 2, "benchmark"),
    (r"\bAPI\b|\bpricing\b|\bprice\b", 1, "api/pricing"), (r"\braise[sd]?\b|\bfunding\b|\bseries [a-h]\b|\bvaluation\b|\bIPO\b", 3, "funding"),
    (r"\bGPUs?\b|\bTPUs?\b|\bchip\b|\bdata ?cent(er|re)\b|\bgigawatt\b|\bGW\b", 2, "compute"), (r"\bpaper\b|\barxiv\b|\bresearch\b", 1, "research"),
    (r"\bsystem card\b|\bsafety\b|\bpolicy\b", 1, "safety/policy"),
]


def score(text):
    s, hits = 0, []
    for pat, w, lab in TERMS:
        if re.search(pat, text, re.I):
            s += w
            hits.append(lab)
    return s, hits


def known_sources():
    urls = set()
    for f in ["lab-updates.json", "model-releases.json", "benchmarks.json", "ai-investments.json", "stack-innovations.json"]:
        try:
            urls |= set(re.findall(r"https?://[^\"\s]+", (ROOT / "data" / f).read_text()))
        except OSError:
            pass
    return {u.rstrip("/").lower() for u in urls}


def get(path, params, token):
    url = API + path + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token, "User-Agent": "FrontierAGI-Academy tips"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get("x-rate-limit-reset", "0") or 0) - int(time.time())
                time.sleep(min(max(wait, 15), 900))
                continue
            if e.code in (401, 403):
                sys.exit(f"X API refused the request ({e.code}). Check the token and that your API tier can read posts.")
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    return {}


def to_tip(p, users, known):
    text = p.get("text", "")
    s, hits = score(text)
    links = [u.get("expanded_url", "") for u in (p.get("entities", {}) or {}).get("urls", [])]
    links = [l for l in links if l and "x.com/" not in l and "twitter.com/" not in l]
    author = users.get(p.get("author_id"), p.get("author_id", ""))
    return {
        "id": p["id"], "author": author, "date": p.get("created_at", "")[:10],
        "url": f"https://x.com/{author}/status/{p['id']}", "links": links[:3],
        "snippet": re.sub(r"\s+", " ", text)[:SNIP], "score": s, "why": hits,
        "maybe_known": any(l.rstrip("/").lower() in known for l in links),
        "likes": (p.get("public_metrics") or {}).get("like_count"),
    }


def fetch(days, token):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    fields = {"tweet.fields": "created_at,public_metrics,entities,author_id", "max_results": 100, "start_time": since}
    posts, users = [], {}
    uid, utok = os.environ.get("X_USER_ID"), os.environ.get("X_USER_TOKEN")
    if uid and utok:
        res = get(f"/users/{uid}/timelines/reverse_chronological", dict(fields, expansions="author_id", **{"user.fields": "username"}), utok)
        posts = res.get("data", [])
        users = {u["id"]: u["username"] for u in (res.get("includes", {}) or {}).get("users", [])}
        mode = "following timeline"
    else:
        handles = json.loads(WATCH.read_text())["accounts"]
        for i in range(0, len(handles), 100):
            res = get("/users/by", {"usernames": ",".join(handles[i:i + 100])}, token)
            for u in res.get("data", []):
                users[u["id"]] = u["username"]
            for e in res.get("errors", []):
                print("not found:", e.get("value"), file=sys.stderr)
        for u_id in users:
            res = get(f"/users/{u_id}/tweets", dict(fields, exclude="retweets,replies"), token)
            for p in res.get("data", []):
                p.setdefault("author_id", u_id)
                posts.append(p)
            time.sleep(1)
        mode = "watchlist"
    return posts, users, mode


def write(tips, mode, days):
    tips = sorted([t for t in tips if t["score"] >= 3], key=lambda t: (-t["score"], t["date"]))[:200]
    OUT.write_text(json.dumps({
        "about": "Tips only, never shown on the site. Check each against its primary source before adding it to the data files.",
        "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "mode": mode, "days": days, "count": len(tips), "items": tips,
    }, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(tips)} tips written to {OUT.relative_to(ROOT)} ({mode})")


def selftest():
    users = {"1": "OpenAI"}
    p = {"id": "99", "author_id": "1", "created_at": "2026-11-20T10:00:00.000Z", "text": "Introducing our new model, now available in the API.",
         "entities": {"urls": [{"expanded_url": "https://openai.com/index/x/"}, {"expanded_url": "https://x.com/a/status/1"}]}, "public_metrics": {"like_count": 5}}
    t = to_tip(p, users, {"https://openai.com/index/x"})
    assert t["score"] >= 8 and "introducing" in t["why"] and t["links"] == ["https://openai.com/index/x/"], t
    assert t["maybe_known"] and t["url"] == "https://x.com/OpenAI/status/99" and t["date"] == "2026-11-20"
    assert score("Happy holidays everyone")[0] == 0
    json.loads(WATCH.read_text())["accounts"]
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    token = os.environ.get("X_BEARER_TOKEN", "")
    if not token and not os.environ.get("X_USER_TOKEN"):
        print("No X_BEARER_TOKEN or X_USER_TOKEN set; nothing fetched.")
        return
    posts, users, mode = fetch(a.days, token)
    known = known_sources()
    write([to_tip(p, users, known) for p in posts], mode, a.days)


if __name__ == "__main__":
    main()
