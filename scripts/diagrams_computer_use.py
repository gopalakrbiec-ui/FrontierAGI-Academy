# Generates assets/diagrams/computer-use/*.svg for the "Computer-Use and Browser Agents" series
#   python3 scripts/diagrams_computer_use.py
# Facts: Anthropic computer/browser use tool docs, OpenAI CUA sample app, Gemini computer-use-preview,
# OSWorld / WebArena READMEs, data/benchmarks.json and data/lab-updates.json (read 28 Nov 2026). Layouts are ours.
import os, json
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagrams_adlc.py')).read().split('# 1 timeline')[0]
exec(_src)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'assets', 'diagrams', 'computer-use') + '/'
os.makedirs(OUT, exist_ok=True)
def save(n, s): open(OUT + n, 'w').write(s + '</svg>')
B = '#2563eb'; T = '#0d9488'; O = '#d97706'; R = '#be123c'; P = '#7c3aed'; G = '#475569'

# 1 the loop
W, H = 1200, 420; s = head(W, H, 'The computer-use loop', 'Every computer-use agent repeats the same four steps until the task is done or it stops') + ANIM
ST = [('Look', ['screenshot, page tree', 'or code output'], B), ('Decide', ['model picks the', 'next action(s)'], P), ('Act', ['click, type, scroll,', 'navigate, run code'], O), ('Check', ['did it work?', 'new screenshot'], T)]
for i, (t, sub, c) in enumerate(ST):
    x = 40 + i * 290; s += f'<g class="fd" style="animation-delay:{i*.2}s">' + box(x, 110, 240, 110, t, sub, c, fs=18) + '</g>'
    if i < 3: s += arr(x + 240, 165, x + 290, 165)
s += '<path d="M1040,222 C1040,330 160,330 160,222" fill="none" stroke="#334155" stroke-width="1.8" stroke-dasharray="7 5" marker-end="url(#a)"/>'
s += note(600, 318, 'repeat: often 10–100+ steps for one task', '#334155', 13.5, 'middle', True)
s += box(380, 340, 440, 46, 'Stop: done, stuck, or a human must confirm', None, R, fs=13.5)
save('1-loop.svg', s)

# 2 three ways to see
W, H = 1200, 470; s = head(W, H, 'Three ways an agent “sees” software', 'Pixels work everywhere; structure and code are cheaper and more reliable where they exist (our comparison)') + ANIM
C3 = [('Pixels (screenshots)', B, ['screenshot → x,y click', 'any app, any OS', 'costly images each step', 'fragile on tiny text', 'e.g. Claude computer use,', 'Gemini computer use']),
      ('Structure (accessibility tree / DOM)', T, ['read elements by role and name', 'web pages and some apps', 'cheap text, exact targets', 'misses canvas and visuals', 'e.g. Playwright MCP, Claude', 'browser use (also screenshots)']),
      ('Code (scripted actions)', O, ['model writes Playwright / Python', 'loops over many fields at once', 'fewest model calls', 'needs a runtime and sandbox', 'e.g. OpenAI CUA sample app,', 'browser-use library'])]
for i, (t, c, L) in enumerate(C3):
    x = 30 + i * 390; s += f'<g class="fd" style="animation-delay:{i*.2}s"><rect x="{x}" y="80" width="360" height="350" rx="14" fill="{c}10" stroke="{c}" stroke-width="1.8"/>' + note(x + 180, 112, t, c, 16, 'middle', True)
    for k, l in enumerate(L): s += note(x + 24, 156 + k * 42, ('• ' if k < 4 else '') + l, '#0f172a' if k < 4 else '#475569', 14 if k < 4 else 12.5, bold=(k < 4 and False))
    s += '</g>'
save('2-three-ways.svg', s)

# 3 timeline
W, H = 1200, 420; s = head(W, H, 'Two years of computer-use agents', 'Launch dates from the labs’ own announcements (data/lab-updates.json); benchmarks from their READMEs') + ANIM
EV = [('2023-07', 'WebArena', 'web benchmark', G, 1), ('2024-04', 'OSWorld', 'desktop benchmark', G, -1), ('2024-10', 'Claude computer use', '14.9% OSWorld', '#b4532a', 1), ('2025-01', 'Operator', 'OpenAI CUA', '#10a37f', -1),
      ('2025-07', 'ChatGPT agent', 'Operator merged', '#10a37f', 1), ('2025-07', 'OSWorld-Verified', 'fixed tasks', G, -1), ('2025-10', 'ChatGPT Atlas', 'agent browser', '#10a37f', 1), ('2025-11', 'Antigravity', 'Google', B, -1),
      ('2026-08', 'Claude toolsets', 'computer + browser', '#b4532a', 1), ('2026-09', 'Agents API', 'OpenAI computer use', '#10a37f', -1), ('2026-10', 'OSWorld-2.1', 'leaders 80–89%', G, 1)]
s += '<line x1="50" y1="220" x2="1160" y2="220" stroke="#334155" stroke-width="3"/>'
for i, (d, t, sub, c, up) in enumerate(EV):
    x = 80 + i * 104; ty = 130 if up > 0 else 300
    s += f'<g class="fd" style="animation-delay:{i*.1}s"><circle cx="{x}" cy="220" r="8" fill="{c}"/><line x1="{x}" y1="{220-up*8}" x2="{x}" y2="{ty+(18 if up>0 else -34)}" stroke="{c}" stroke-dasharray="3 3"/>'
    s += note(x, ty - 14 if up > 0 else ty, d, c, 12.5, 'middle', True) + note(x, ty + 4 if up > 0 else ty + 18, t, '#0f172a', 12.5, 'middle', True) + note(x, ty + 20 if up > 0 else ty + 34, sub, '#475569', 11, 'middle') + '</g>'
s += note(24, H - 14, 'Claude toolsets = computer_toolset_20260801 / browser_toolset_20260801 (version dates). WebArena and OSWorld dates are their papers’ (⚠️ from memory).', '#64748b', 11.5)
save('3-timeline.svg', s)

# 4 benchmark bars (OSWorld-2.1 offline subset)
bm = json.load(open(os.path.join(ROOT, 'data', 'benchmarks.json')))
names = {m['id']: m.get('name', m['id']) for m in json.load(open(os.path.join(ROOT, 'data', 'model-releases.json')))['items']}
rows = sorted([x for x in bm['scores'] if x['b'] == 'osworld-2-1'], key=lambda x: -x['v'])
col = lambda m: '#b4532a' if m.startswith('anthropic') else ('#10a37f' if m.startswith('openai') else B)
hbars('4-osworld.svg', 'OSWorld-2.1 (offline subset), late 2026', 'Share of desktop tasks completed; ⚠️ = secondary source', [((names.get(x['m'], x['m'])[:34]) + (' ⚠️' if x.get('sec') else ''), x['v'], col(x['m']), '') for x in rows], 100, W=1100,
      src='Source: data/benchmarks.json (Google’s Gemini 4 Carbon evals table, 28 Oct 2026; Fable 5.2 via a secondary report). Lab-run numbers; harnesses differ.')

# 5 lab tools compared
W, H = 1200, 470; s = head(W, H, 'How the three big labs ship computer use', 'From each lab’s own docs or sample repo (read 28 Nov 2026); our summary') + ANIM
LB = [('Anthropic', '#b4532a', ['computer toolset: 17 actions', 'browser toolset: 27 (+4 optional)', 'you run the VM or browser', 'injection classifiers on screenshots', 'Claude in Chrome (product)']),
      ('OpenAI', '#10a37f', ['model writes code to act', 'Playwright or PyAutoGUI runtime', 'ComputerToolset in the SDK', 'Agents API with computer use', 'ChatGPT agent, Atlas (products)']),
      ('Google', B, ['Gemini computer use model', 'Playwright or Browserbase env', 'browser-first sample agent', 'Vertex AI or Gemini API', 'Mariner, Antigravity (products)'])]
for i, (t, c, L) in enumerate(LB):
    x = 30 + i * 390; s += f'<g class="fd" style="animation-delay:{i*.2}s"><rect x="{x}" y="80" width="360" height="350" rx="14" fill="{c}10" stroke="{c}" stroke-width="1.8"/>' + note(x + 180, 114, t, c, 18, 'middle', True)
    for k, l in enumerate(L): s += note(x + 26, 164 + k * 50, '• ' + l, '#0f172a', 14)
    s += '</g>'
save('5-labs.svg', s)

# 6 defence layers
W, H = 1200, 500; s = head(W, H, 'Defences for an agent that clicks', 'Layered: no single layer stops prompt injection (our checklist, based on the labs’ safety guidance)') + ANIM
DL = [('Isolated VM or browser profile', 'no personal logins, minimal rights', B), ('Domain allow-list', 'only the sites the task needs', T), ('Injection screening', 'classifiers on screenshots and pages', P),
      ('Human confirmation', 'payments, sending, deleting, accepting terms', O), ('Step, time and cost limits', 'stop runaway loops', R), ('Recording and review', 'screenshots + actions kept for audit', G)]
for i, (t, sub, c) in enumerate(DL):
    y = 76 + i * 68; s += f'<g class="fd" style="animation-delay:{i*.12}s"><rect x="{60+i*30}" y="{y}" width="{1080-i*60}" height="56" rx="10" fill="{c}12" stroke="{c}" stroke-width="1.6"/>' + note(84 + i * 30, y + 25, t, c, 15, bold=True) + note(84 + i * 30, y + 45, sub, '#334155', 12.5) + '</g>'
save('6-defences.svg', s)
print('wrote', OUT)
