# Generates assets/diagrams/multi-agent/*.svg for the "Multi-Agent Orchestration Patterns" series
#   python3 scripts/diagrams_multi_agent.py
# Pattern names follow Anthropic's "Building effective agents" and the OpenAI Agents SDK / LangGraph docs;
# charts 5 and 6 run the scripts in data/code/ (illustrative toy models). Layouts are ours.
import os, subprocess, sys
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagrams_adlc.py')).read().split('# 1 timeline')[0]
exec(_src)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'assets', 'diagrams', 'multi-agent') + '/'
os.makedirs(OUT, exist_ok=True)
def save(n, s): open(OUT + n, 'w').write(s + '</svg>')
def run(rel): return subprocess.run([sys.executable, '-S', os.path.join(ROOT, 'data', 'code', rel)], capture_output=True, text=True).stdout.splitlines()
def node(x, y, t, c, w=110): return box(x - w / 2, y - 22, w, 44, t, None, c, fs=12.5)

# 1 the pattern catalogue (8 mini topologies)
W, H = 1200, 700; s = head(W, H, 'Eight ways to arrange agents', 'From fixed workflows (left) to agents that decide who works next (right); names from Anthropic, OpenAI and LangGraph docs') + ANIM
cells = [(0, 0, 'Chain', '#475569'), (1, 0, 'Router', '#2563eb'), (2, 0, 'Parallel / vote', '#0d9488'), (3, 0, 'Evaluator–optimizer', '#d97706'),
         (0, 1, 'Supervisor (agents as tools)', '#7c3aed'), (1, 1, 'Hand-offs / swarm', '#be123c'), (2, 1, 'Debate', '#0891b2'), (3, 1, 'Hierarchy', '#15803d')]
for i, (cx, cy, t, c) in enumerate(cells):
    x0, y0 = 30 + cx * 290, 76 + cy * 310
    s += f'<g class="fd" style="animation-delay:{i*.1}s"><rect x="{x0}" y="{y0}" width="270" height="290" rx="14" fill="{c}0d" stroke="{c}" stroke-width="1.6"/>' + note(x0 + 135, y0 + 28, t, c, 15, 'middle', True)
    X = lambda dx: x0 + dx; Y = lambda dy: y0 + dy
    if t == 'Chain':
        for k in range(3): s += node(X(135), Y(80 + k * 70), f'Agent {k+1}', c) + (arr(X(135), Y(102 + k * 70), X(135), Y(128 + k * 70)) if k < 2 else '')
        s += note(X(135), Y(275), 'fixed steps, gates between', '#334155', 12, 'middle')
    elif t == 'Router':
        s += node(X(135), Y(80), 'Router', c)
        for k, dx in enumerate((50, 135, 220)): s += arr(X(135), Y(102), X(dx), Y(178)) + node(X(dx), Y(200), ['Billing', 'Tech', 'Refund'][k], c, 78)
        s += note(X(135), Y(275), 'classify once, send to one', '#334155', 12, 'middle')
    elif t == 'Parallel / vote':
        for k, dx in enumerate((50, 135, 220)): s += node(X(dx), Y(90), f'A{k+1}', c, 70) + arr(X(dx), Y(112), X(135), Y(178))
        s += node(X(135), Y(200), 'Aggregate', c)
        s += note(X(135), Y(275), 'same or split task, combine', '#334155', 12, 'middle')
    elif t == 'Evaluator–optimizer':
        s += node(X(135), Y(90), 'Generator', c) + node(X(135), Y(200), 'Evaluator', c)
        s += arr(X(115), Y(112), X(115), Y(178)) + arr(X(155), Y(178), X(155), Y(112), None, c, True) + note(X(200), Y(150), 'feedback', c, 12, 'middle')
        s += note(X(135), Y(275), 'loop until it passes', '#334155', 12, 'middle')
    elif t == 'Supervisor (agents as tools)':
        s += node(X(135), Y(80), 'Supervisor', c)
        for k, dx in enumerate((50, 135, 220)): s += arr(X(135), Y(102), X(dx), Y(178), None, c, False, True) + node(X(dx), Y(200), f'Worker {k+1}', c, 78)
        s += note(X(135), Y(275), 'supervisor keeps control, owns answer', '#334155', 12, 'middle')
    elif t == 'Hand-offs / swarm':
        pts_ = [(70, 100), (200, 100), (135, 200)]
        for k, (dx, dy) in enumerate(pts_): s += node(X(dx), Y(dy), ['Triage', 'Billing', 'Refund'][k], c, 86)
        s += arr(X(113), Y(100), X(157), Y(100)) + arr(X(200), Y(122), X(150), Y(178)) + arr(X(120), Y(178), X(75), Y(122), None, c, True)
        s += note(X(135), Y(275), 'control passes to whoever is active', '#334155', 12, 'middle')
    elif t == 'Debate':
        s += node(X(70), Y(90), 'Agent A', c, 90) + node(X(200), Y(90), 'Agent B', c, 90) + node(X(135), Y(200), 'Judge / vote', c)
        s += arr(X(115), Y(84), X(155), Y(84), None, c, False, True) + arr(X(70), Y(112), X(120), Y(178)) + arr(X(200), Y(112), X(150), Y(178))
        s += note(X(135), Y(275), 'argue over rounds, then decide', '#334155', 12, 'middle')
    else:
        s += node(X(135), Y(70), 'Top', c) + node(X(70), Y(150), 'Lead 1', c, 86) + node(X(200), Y(150), 'Lead 2', c, 86)
        s += arr(X(125), Y(92), X(80), Y(128)) + arr(X(145), Y(92), X(190), Y(128))
        for k, dx in enumerate((40, 100, 170, 230)): s += node(X(dx), Y(225), 'W', c, 44) + arr(X(70 if k < 2 else 200), Y(172), X(dx), Y(203))
        s += note(X(135), Y(275), 'supervisors of supervisors', '#334155', 12, 'middle')
    s += '</g>'
save('1-catalogue.svg', s)

# 2 control spectrum
W, H = 1200, 300; s = head(W, H, 'Who decides what happens next?', 'Anthropic separates workflows (code decides) from agents (the model decides); OpenAI’s SDK docs call these orchestrating via code vs via LLM') + ANIM
s += '<defs><linearGradient id="gq"><stop offset="0" stop-color="#475569"/><stop offset="1" stop-color="#be123c"/></linearGradient></defs><rect x="60" y="120" width="1080" height="18" rx="9" fill="url(#gq)"/>'
for i, (t, x) in enumerate([('Chain', 90), ('Router', 230), ('Parallel / vote', 380), ('Evaluator loop', 540), ('Supervisor', 700), ('Hierarchy', 850), ('Hand-offs / swarm', 990), ('Open group chat', 1120)]):
    s += f'<g class="fd" style="animation-delay:{i*.1}s"><circle cx="{x}" cy="129" r="10" fill="#fff" stroke="#0f172a" stroke-width="2"/>' + note(x, 100 if i % 2 else 170, t, '#0f172a', 13, 'middle', True) + '</g>'
s += note(60, 230, 'Code decides: predictable, cheap, easy to test', '#475569', 14, bold=True) + note(1140, 230, 'Model decides: flexible, costly, harder to test', '#be123c', 14, 'end', True)
s += note(24, H - 14, 'Placement on the line is our reading.', '#64748b', 11.5)
save('2-spectrum.svg', s)

# 3 supervisor vs handoff message flow
W, H = 1200, 430; s = head(W, H, 'Agents as tools vs hand-offs', 'The two patterns the OpenAI Agents SDK docs name as most common; LangGraph’s supervisor and swarm libraries follow the same split') + ANIM
s += band(24, 76, 560, 320, 'AGENTS AS TOOLS (SUPERVISOR)', '#7c3aed') + band(616, 76, 560, 320, 'HAND-OFFS (SWARM)', '#be123c')
s += node(150, 140, 'User', '#0f172a', 90) + node(300, 140, 'Manager', '#7c3aed') + node(200, 290, 'Refund spec.', '#7c3aed', 120) + node(420, 290, 'Policy spec.', '#7c3aed', 120)
s += arr(195, 140, 245, 140, None, '#334155', False, True) + arr(285, 162, 215, 268, 'call', '#7c3aed', False, True) + arr(315, 162, 405, 268, 'call', '#7c3aed', False, True)
s += note(300, 360, 'Manager talks to the user and writes the final answer', '#334155', 12.5, 'middle', True)
s += node(740, 140, 'User', '#0f172a', 90) + node(890, 140, 'Triage', '#be123c') + node(1060, 140, 'Refund agent', '#be123c', 120) + node(1060, 290, 'Policy agent', '#be123c', 120)
s += arr(785, 140, 835, 140) + arr(945, 140, 1000, 140, 'hand off', '#be123c') + arr(1060, 162, 1060, 268, 'hand off', '#be123c') + f'<path d="M1000,290 C850,290 760,240 745,163" fill="none" stroke="#be123c" stroke-width="1.7" stroke-dasharray="5 4" marker-end="url(#a)"/>'
s += note(900, 360, 'Whoever is active talks to the user directly', '#334155', 12.5, 'middle', True)
save('3-tools-vs-handoffs.svg', s)

# 4 research system
W, H = 1200, 400; s = head(W, H, 'Case study: Anthropic’s multi-agent research system', 'Numbers as reported by Anthropic in its 2025 engineering post') + ANIM
s += node(140, 200, 'User question', '#0f172a', 150) + node(380, 200, 'Lead agent (plans)', '#7c3aed', 180)
for k in range(4): s += node(650, 110 + k * 60, f'Sub-agent {k+1} · searches', '#0d9488', 200) + arr(470, 200, 548, 110 + k * 60)
s += node(930, 200, 'Lead synthesises', '#7c3aed', 180) + node(1120, 200, 'Citations', '#d97706', 110)
for k in range(4): s += arr(752, 110 + k * 60, 838, 200)
s += arr(216, 200, 288, 200) + arr(1022, 200, 1063, 200)
s += note(40, 352, '+90.2% vs single-agent Opus 4 on its internal research eval · 3–5 sub-agents in parallel, each using 3+ tools in parallel · research time cut by up to 90%', '#334155', 12.5, bold=True)
s += note(40, 374, 'Cost: multi-agent systems used ~15× the tokens of chat. Not a good fit for most coding tasks, per the same post.', '#be123c', 12.5)
save('4-research-system.svg', s)

# 5 voting chart from script
r = run('multi-agent-parallel-debate/voting.py')[1:5]
rows = []
for ln in r:
    a = ln.split(); rows.append((int(a[0]), float(a[1].rstrip('%')), float(a[2].rstrip('%'))))
W, H = 1100, 380; s = head(W, H, 'Voting helps less when agents make the same mistakes', 'Majority-vote accuracy, one agent 70% right (toy model from voting.py)') + ANIM
for i, (n, ind, cor) in enumerate(rows):
    y = 90 + i * 66
    s += note(24, y + 30, f'{n} agent' + ('s' if n > 1 else ''), '#0f172a', 14, bold=True)
    s += f'<rect class="gr" style="animation-delay:{i*.15}s" x="180" y="{y+6}" width="{(ind-50)*14:.0f}" height="22" rx="5" fill="#0d9488"/>' + note(186 + (ind - 50) * 14, y + 23, f'{ind:.1f}% independent', '#0f172a', 12.5, bold=True)
    s += f'<rect class="gr" style="animation-delay:{i*.15+.1}s" x="180" y="{y+32}" width="{(cor-50)*14:.0f}" height="22" rx="5" fill="#d97706"/>' + note(186 + (cor - 50) * 14, y + 49, f'{cor:.1f}% correlated', '#0f172a', 12.5, bold=True)
s += note(24, H - 14, 'Source: data/code/multi-agent-parallel-debate/voting.py. Bars start at 50%. Correlated = half the time all agents share one answer.', '#64748b', 11.5)
save('5-voting.svg', s)

# 6 compounding chart from script
r = run('multi-agent-failures-cost/compounding.py')[1:6]
W, H = 1100, 400; s = head(W, H, 'Errors compound along a chain of agents', 'Chance the whole chain succeeds, by number of hand-offs (toy model from compounding.py)') + ANIM
X = lambda k: 120 + (k - 1) / 19 * 780; Y = lambda v: 330 - v / 100 * 250
for v in (25, 50, 75, 100): s += f'<line x1="120" y1="{Y(v)}" x2="900" y2="{Y(v)}" stroke="#e2e8f0"/>' + note(110, Y(v) + 4, f'{v}%', '#64748b', 11, 'end')
series = [(1, '#2563eb', 's=0.95'), (2, '#0d9488', 's=0.95 + checker'), (3, '#be123c', 's=0.90'), (4, '#d97706', 's=0.90 + checker')]
data = [[float(x.rstrip('%')) for x in ln.split()[1:]] for ln in r]; ks = [int(ln.split()[0]) for ln in r]
for j, c, lab in series:
    s += '<polyline class="dr" fill="none" stroke="%s" stroke-width="3" points="%s"/>' % (c, ' '.join(f'{X(k):.0f},{Y(d[j-1]):.0f}' for k, d in zip(ks, data)))
    s += note(X(20) + 8, Y(data[-1][j - 1]) + 4, lab, c, 12, bold=True)
for k in ks: s += note(X(k), 350, str(k), '#64748b', 11.5, 'middle')
s += note(570, 372, 'hand-offs in the chain', '#64748b', 11.5, 'middle')
s += note(24, H - 6, 'Checker = catches 80% of failed steps and retries once (assumption). Source: data/code/multi-agent-failures-cost/compounding.py.', '#64748b', 11.5)
save('6-compounding.svg', s)
print('wrote', OUT)
