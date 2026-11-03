#!/usr/bin/env python3
"""
Regenerates the generated parts of README.md:
  STATS   – counts line (articles, series, maps)
  MAPS    – every interactive map with a screenshot (data/readme-maps.json),
            then a compact strip of series hub pages
  SERIES  – one section per article series, grouped by the homepage section it
            sits in and in homepage card order (blog/series.json + index.html);
            the two newest series are expanded, the rest are collapsed
Run by scripts/build.py (and `--check` by build.py --check).
Screenshots live in assets/readme/ and are made by scripts/readme_shots.js.
"""

import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent.parent
README = ROOT / "README.md"
BASE = "https://gopalakrbiec-ui.github.io/FrontierAGI-Academy"


def cell(t):
    return unescape(re.sub(r"<[^>]+>", "", str(t))).replace("|", "\\|").replace("\n", " ").strip()


def load():
    posts = json.loads((ROOT / "blog/index.json").read_text(encoding="utf-8"))["posts"]
    series = json.loads((ROOT / "blog/series.json").read_text(encoding="utf-8"))["series"]
    maps = json.loads((ROOT / "data/readme-maps.json").read_text(encoding="utf-8"))
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    return posts, series, maps, home


def sections_of(home, series):
    """Homepage section (eyebrow) and description for each spotlight id, by position."""
    eyebrows = [(m.start(), cell(m.group(1))) for m in re.finditer(r'class="eyebrow">(.*?)</div>', home)]
    out = {}
    for s in series:
        i = home.find(f'id="{s["id"]}"')
        sec = "More series"
        for pos, label in eyebrows:
            if pos < i:
                sec = label
        d = re.search(r'class="home-(?:series|rsi|lineage)-desc"[^>]*>(.*?)</div>', home[i:i + 4000], re.S)
        out[s["id"]] = (sec, cell(d.group(1)) if d else "")
    return out


def maps_block(maps):
    lines = []
    total = 0
    for group, items in maps["groups"]:
        lines.append(f"### {group}\n")
        lines.append("<table>")
        for k in range(0, len(items), 2):
            lines.append("<tr>")
            for m in items[k:k + 2]:
                total += 1
                url = f"{BASE}/pages/{m['page']}.html"
                tag = " 🎞️" if m.get("gif") else ""
                data = f"<br><sub>Data: <code>{m['data']}</code></sub>" if m["data"] != "in-page" else ""
                lines.append(f'<td width="50%" valign="top"><a href="{url}"><img src="assets/readme/{m["shot"]}" alt="{m["name"]}" width="100%"></a><br><b><a href="{url}">{m["name"]}</a></b>{tag}<br>{m["line"]}{data}</td>')
            if len(items[k:k + 2]) == 1:
                lines.append('<td width="50%"></td>')
            lines.append("</tr>")
        lines.append("</table>\n")
    lines.append("### 🧭 Series hubs: each series at a glance\n")
    lines.append("<table>")
    hubs = maps["hubs"]
    for k in range(0, len(hubs), 3):
        lines.append("<tr>")
        for h in hubs[k:k + 3]:
            url = f"{BASE}/pages/{h['page']}.html"
            lines.append(f'<td width="33%" align="center"><a href="{url}"><img src="assets/readme/{h["shot"]}" alt="{h["name"]}" width="100%"></a><br><a href="{url}"><b>{h["name"]}</b></a></td>')
        lines.append("</tr>")
    lines.append("</table>")
    return "\n".join(lines), total


def series_block(posts, series, maps, home):
    bys = {p["slug"]: p for p in posts}
    sec = sections_of(home, series)
    newest = sorted(series, key=lambda s: max((bys[x]["date"] for x in s["slugs"] if x in bys), default=""), reverse=True)
    open_ids = {s["id"] for s in newest[:2]}
    out, cur, seen = [], None, set()
    for s in series:
        label, desc = sec[s["id"]]
        if label != cur:
            cur = label
            out.append(f"\n### {label}\n")
        rows = [bys[x] for x in s["slugs"] if x in bys]
        seen.update(x["slug"] for x in rows)
        hub = maps["hub_of"].get(s["id"])
        out.append(f"#### {s['icon']} {cell(s['title'])}\n")
        meta = f"{len(rows)} articles"
        if hub:
            meta += f" · 🧭 [Hub page]({BASE}/pages/{hub}.html)"
        out.append((desc + "  \n" if desc else "") + f"<sub>{meta}</sub>\n")
        table = ["| # | Article | Read |", "|---|---|---|"]
        for n, p in enumerate(rows, 1):
            table.append(f"| {n} | {p.get('emoji', '📝')} [{cell(p['title'])}]({BASE}/blog/{p['slug']}.html) | {p.get('readTime', '')} |")
        t = "\n".join(table)
        if s["id"] in open_ids:
            out.append(f"🆕 *Newest series, shown in full.*\n\n{t}\n")
        else:
            out.append(f"<details><summary>Show all {len(rows)} articles</summary>\n\n{t}\n\n</details>\n")
    rest = [p for p in posts if p["slug"] not in seen]
    if rest:
        out.append("\n### 📝 More articles (not in a series)\n")
        table = ["| Article | Date |", "|---|---|"] + [f"| {p.get('emoji', '📝')} [{cell(p['title'])}]({BASE}/blog/{p['slug']}.html) | {p.get('date', '')} |" for p in rest]
        out.append(f"<details><summary>Show {len(rest)} more articles</summary>\n\n" + "\n".join(table) + "\n\n</details>\n")
    return "\n".join(out)


def replace(content, name, body):
    a, b = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    pat = re.compile(re.escape(a) + r".*?" + re.escape(b), re.S)
    if not pat.search(content):
        raise SystemExit(f"ERROR: {name} markers not found in README.md")
    return pat.sub(lambda _: f"{a}\n{body}\n{b}", content)


def update_readme(check=False):
    posts, series, maps, home = load()
    content = README.read_text(encoding="utf-8")
    mb, nmaps = maps_block(maps)
    stats = f"**{len(posts)} articles** · **{len(series)} series** · **{nmaps} interactive maps** + **{len(maps['hubs'])} series hubs** · newest post {max(p['date'] for p in posts)}"
    updated = replace(content, "STATS", stats)
    updated = replace(updated, "MAPS", mb)
    updated = replace(updated, "SERIES", series_block(posts, series, maps, home))
    if check:
        return 0 if updated == content else 1
    README.write_text(updated, encoding="utf-8")
    print(f"README updated — {len(posts)} post(s) written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(update_readme(check="--check" in sys.argv))
