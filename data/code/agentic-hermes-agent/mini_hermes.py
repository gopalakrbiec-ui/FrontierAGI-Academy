"""mini_hermes.py — a toy harness in the style of Hermes Agent (illustrative).

A gateway receives chat messages; the agent searches past sessions (SQLite FTS5,
falling back to a simple scan if FTS5 is missing), reuses a skill it wrote last
time, and writes or updates skills after a task. The "model" is a scripted stub;
standard library only.
"""
import sqlite3
db = sqlite3.connect(":memory:")
try:
    db.execute("CREATE VIRTUAL TABLE sessions USING fts5(text)"); FTS = True
except sqlite3.OperationalError:
    db.execute("CREATE TABLE sessions(text)"); FTS = False
SKILLS = {}

def search(q):
    if FTS: return [r[0] for r in db.execute("SELECT text FROM sessions WHERE sessions MATCH ?", (q,))]
    return [r[0] for r in db.execute("SELECT text FROM sessions") if q in r[0]]

def handle(platform, msg):
    hits = search("date")
    skill = SKILLS.get("fix-date-tests")
    steps = skill["steps"] if skill else ["run tests", "inspect parse()", "try formats", "fix", "re-run"]
    db.execute("INSERT INTO sessions VALUES (?)", (f"{platform}: {msg} -> fixed date parsing",))
    if skill: skill["uses"] += 1
    else: SKILLS["fix-date-tests"] = {"steps": ["run tests with TZ=UTC", "check split format", "fix", "re-run"], "uses": 1}
    return f"[{platform}] recalled {len(hits)} past session(s), {'reused skill' if skill else 'no skill yet'}, {len(steps)} steps"

def main():
    print(handle("slack", "date test failing, please fix"))
    print(handle("telegram", "the date test broke again"))
    print(f"skills: {[(k, v['uses']) for k, v in SKILLS.items()]}  session search: {'fts5' if FTS else 'scan'}")

if __name__ == "__main__":
    main()
