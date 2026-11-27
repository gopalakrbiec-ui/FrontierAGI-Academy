# Generates assets/diagrams/fde/*.svg for "The Forward Deployed Engineer" series from data/fde-postings.json
#   python3 scripts/diagrams_fde.py
import os, json, collections, statistics
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagrams_adlc.py')).read().split('# 1 timeline')[0]
exec(_src)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'assets', 'diagrams', 'fde') + '/'
os.makedirs(OUT, exist_ok=True)
def save(n, s): open(OUT + n, 'w').write(s + '</svg>')
D = json.load(open(os.path.join(ROOT, 'data', 'fde-postings.json')))
P = D['postings']; SNAP = D['snapshot']
SRC = f'Source: our snapshot of {len(P)} forward deployed postings on 10 companies’ own job boards, {SNAP} (data/fde-postings.json).'
COL = {'Databricks': '#dc2626', 'Palantir': '#111827', 'OpenAI': '#10a37f', 'Cursor': '#475569', 'Scale AI': '#7c3aed', 'Cohere': '#d97706', 'Anthropic': '#b4532a', 'ElevenLabs': '#0891b2', 'Harvey': '#1d4ed8', 'Ramp': '#65a30d'}

# 1 who is hiring
C = collections.Counter(p['company'] for p in P).most_common()
hbars('1-companies.svg', 'Who is hiring forward deployed engineers', 'Open roles with “forward deployed” in the title, by company',
      [(c, n, COL.get(c, '#64748b'), '') for c, n in C], max(n for _, n in C), unit='', W=1100, src=SRC)

# 2 pay ranges (US, core + senior)
W, H = 1100, 140 + 9 * 46; s = head(W, H, 'Posted US pay ranges for forward deployed engineers', 'Median of posted base-salary ranges per company, individual-contributor roles; equity not included') + ANIM
rows = []
for c, _ in C:
    U = [p['usd'] for p in P if p['company'] == c and p['usd'] and p['level'] in ('core', 'senior')]
    if U: rows.append((c, statistics.median(u[0] for u in U), statistics.median(u[1] for u in U), len(U)))
rows.sort(key=lambda r: r[2])
x0, x1, lo, hi = 260, 1040, 100000, 450000
X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
for v in range(100000, 450001, 50000):
    s += f'<line x1="{X(v):.0f}" y1="92" x2="{X(v):.0f}" y2="{H-34}" stroke="#e2e8f0"/>' + note(X(v), 88, f'${v//1000}k', '#64748b', 11, 'middle')
for i, (c, a, b, n) in enumerate(rows):
    y = 108 + i * 46
    s += note(24, y + 18, f'{c} ({n})', '#0f172a', 13.5, bold=True)
    s += f'<rect class="gr" style="animation-delay:{i*.1}s" x="{X(a):.0f}" y="{y+4}" width="{X(b)-X(a):.0f}" height="20" rx="10" fill="{COL.get(c,"#64748b")}"/>'
    s += note(X(b) + 8, y + 19, f'${a/1000:.0f}k–${b/1000:.0f}k', '#0f172a', 12.5, bold=True)
s += note(24, H - 16, SRC + ' (n) = postings with a US range.', '#64748b', 11)
save('2-pay.svg', s)

# 3 skills
U = {}
for p in P: U.setdefault((p['company'], p['title']), p)
U = list(U.values()); n = len(U)
SK = [('travel', 'Travel'), ('customer', 'Working with customers'), ('python', 'Python'), ('ts', 'TypeScript / JavaScript'), ('agents', 'Agents'), ('evals', 'Evals'), ('llm', 'LLMs / generative AI'), ('clearance', 'Security clearance'), ('rag', 'RAG / retrieval'), ('mcp', 'MCP')]
hbars('3-skills.svg', 'What forward deployed postings ask for', f'Share of {n} distinct postings (company + title) whose text mentions each', [(lab, round(sum(p[k] for p in U) / n * 100), '#0d9488' if k in ('travel', 'customer') else '#2563eb', '') for k, lab in SK], 100, W=1100, src=SRC)

# 4 regions + travel
R = collections.Counter(p['region'] for p in P).most_common()
hbars('4-regions.svg', 'Where the roles are', 'Open forward deployed roles by region', [(r, k, '#7c3aed' if r != 'India' else '#d97706', '') for r, k in R], R[0][1], unit='', W=1100, src=SRC)
T = collections.Counter(p['travel_pct'] for p in P if p['travel_pct'])
hbars('5-travel.svg', 'How much travel', f'Postings that state a travel share ({sum(T.values())} of {len(P)})', [(f'Up to {k}%', v, '#be123c', '') for k, v in sorted(T.items())], max(T.values()), unit='', W=1100, src=SRC)

# 6 levels
L = collections.Counter(p['level'] for p in P)
order = ['intern', 'new grad', 'core', 'senior', 'manager']
hbars('6-levels.svg', 'Entry points into the role', 'Open roles by level, read from job titles (our grouping)', [(k.capitalize(), L[k], '#15803d' if k in ('intern', 'new grad') else '#475569', '') for k in order], max(L.values()), unit='', W=1100, src=SRC)

# 7 engagement
W, H = 1200, 400; s = head(W, H, 'An FDE engagement, in five phases', 'Our synthesis of posting texts and public descriptions; lengths vary from weeks to months') + ANIM
PH = [('Discover', ['sit with users', 'find the real problem', 'agree a success metric'], '#2563eb'), ('Prototype', ['build on real data fast', 'demo to users', 'cut scope'], '#7c3aed'),
      ('Productionise', ['security, evals, monitoring', 'fit the customer’s systems', 'handle edge cases'], '#0d9488'), ('Prove & expand', ['measure against the metric', 'win the next use case'], '#d97706'),
      ('Hand over', ['train the customer team', 'feed lessons to product', 'move to next customer'], '#be123c')]
for i, (t, sub, c) in enumerate(PH):
    x = 24 + i * 234
    s += f'<g class="fd" style="animation-delay:{i*.2}s">' + box(x, 100, 210, 130, t, sub, c) + '</g>'
    if i < 4: s += arr(x + 210, 165, x + 234, 165)
s += f'<path class="dr" d="M1110,232 C1110,330 130,330 130,232" fill="none" stroke="#15803d" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#a)"/>'
s += note(600, 348, 'What they learn in the field goes back into the product (the “margin for moat” bet)', '#15803d', 13, 'middle', True)
save('7-engagement.svg', s)

# 8 paths into the role
W, H = 1200, 420; s = head(W, H, 'Paths into forward deployed engineering', 'Where FDEs come from, and the gap each path has to close (our reading of posting requirements)') + ANIM
SRCS = [('Software engineer', 'customer skills, travel, scoping', '#2563eb'), ('Solutions / sales engineer', 'production-grade building', '#7c3aed'), ('Consultant', 'shipping code yourself', '#d97706'),
        ('Data / ML engineer', 'full-stack apps, customer work', '#0d9488'), ('Founder', 'working inside a big customer', '#be123c'), ('New graduate', 'Palantir / Databricks programmes', '#15803d')]
for i, (t, gap, c) in enumerate(SRCS):
    y = 76 + i * 56
    s += box(24, y, 380, 48, t, ['gap: ' + gap], c, fs=13) + arr(404, y + 24, 760, 210, None, c)
s += box(760, 160, 320, 100, 'Forward deployed engineer', ['median 6 years asked', '79% mention customers'], '#0f172a')
save('8-paths.svg', s)
print('wrote diagrams to', OUT)
