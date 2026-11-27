# Generates assets/diagrams/sf-series/*.svg for the "Inside the Software Factory" series
#   python3 scripts/diagrams_software_factory_series.py
# Numbers come from the sources named under each chart; diagrams marked illustrative are our drawing.
import os, subprocess
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagrams_adlc.py')).read().split('# 1 timeline')[0]
exec(_src)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'assets', 'diagrams', 'sf-series') + '/'
os.makedirs(OUT, exist_ok=True)
def save(n, s): open(OUT + n, 'w').write(s + '</svg>')
ST = [('Intake', '#2563eb'), ('Plan', '#7c3aed'), ('Parallel build', '#0d9488'), ('Gates', '#d97706'), ('Human gate', '#be123c'), ('Ship & measure', '#15803d')]

# 1. the six stations
W, H = 1200, 430; s = head(W, H, 'A software factory: six stations', 'The system around the coding agents. Each station has a job, an artefact it hands on and a typical failure (our framing)') + ANIM
SUB = [['tickets · bugs · alerts', 'hand-off: a request'], ['split · size · spec', 'hand-off: a task + tests'], ['many agents at once', 'hand-off: a branch'], ['lint · tests · evals · scans', 'hand-off: a passing PR'], ['review · approve', 'hand-off: a merge'], ['deploy · watch · learn', 'hand-off: new tickets']]
for i, (t, c) in enumerate(ST):
    x = 24 + i * 194
    s += f'<g class="fd" style="animation-delay:{i*.18}s">' + box(x, 110, 170, 96, f'{i+1}. {t}', SUB[i], c) + '</g>'
    if i < 5: s += arr(x + 170, 158, x + 194, 158)
FAIL = ['vague tickets', 'tasks too big', 'agents collide', 'weak tests pass bugs', 'reviews rubber-stamp', 'nobody measures escapes']
for i, f in enumerate(FAIL): s += note(24 + i * 194 + 85, 230, 'fails when:', '#b91c1c', 11.5, 'middle', True) + note(24 + i * 194 + 85, 246, f, '#b91c1c', 11.5, 'middle')
s += f'<path class="dr" d="M1110,250 C1110,360 90,360 90,250" fill="none" stroke="#15803d" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#a)"/>'
s += note(600, 378, 'Feedback loop: production results and escaped defects become the next tickets', '#15803d', 13, 'middle', True)
s += note(24, 414, 'Our framing of the stations, after vendor descriptions (Factory.ai, Warp, TrueFoundry) and Stripe’s published Minions design.', '#64748b', 11.5)
save('1-stations.svg', s)

# 2. what the numbers count
rows = [('Agent-started PRs (GitHub, Sep 2026)', 40, '#2563eb', 'of all PRs started with an agent draft'),
        ('AI-written merged lines (LinearB elite)', 45, '#7c3aed', 'top 10% of 253 orgs'),
        ('PRs with AI help (LinearB elite)', 54, '#0d9488', 'top 10% of orgs'),
        ('PRs by autonomous agents (LinearB elite)', 4.9, '#be123c', 'under 5%'),
        ('Google: new code AI-generated (claim)', 75, '#64748b', '⚠️ CEO statement, Apr 2026'),
        ('Microsoft: code in repos by AI (claim)', 25, '#94a3b8', '⚠️ 20–30%, 2025 statement')]
hbars('2-what-counts.svg', 'Six “AI share of code” numbers that measure different things', 'Same question, different denominators: PRs started, lines merged, PRs assisted, PRs fully autonomous, company claims', rows, 100,
      src='Sources: GitHub Octoverse 2026; LinearB 2026 AI benchmarks (2.7M PRs, Feb–May 2026); company statements via press ⚠️. Bars are not comparable with each other.', W=1200)

# 3. history timeline
W, H = 1200, 330; s = head(W, H, 'From “software factory” to agent factories', 'The idea is 55+ years old; the workers changed') + ANIM
s += '<line x1="40" y1="200" x2="1160" y2="200" stroke="#cbd5e1" stroke-width="4"/>'
EV = [(60, '1969', 'Hitachi software works', 'Japan’s first “factory” for code', '#64748b', 1), (170, '1975–77', 'SDC, Toshiba Fuchu', 'standard tools + reuse', '#64748b', 0),
      (290, '2001', 'Agile Manifesto', 'small teams, short cycles', '#475569', 1), (390, '2009', 'DevOps', 'pipelines + automation', '#475569', 0),
      (510, '2021', 'Copilot preview', 'AI autocompletes code', '#2563eb', 1), (620, 'Feb 2025', 'Claude Code', 'agent works a whole repo', '#7c3aed', 0),
      (730, 'Oct 2025', 'Parallel agents in IDEs', 'worktrees, remote runners ⚠️', '#0d9488', 1), (840, 'Feb 2026', 'Stripe Minions', '1,000+ agent PRs a week', '#d97706', 0),
      (950, 'Jun–Aug 2026', 'Factory platforms', 'Factory.ai 2.0, Warp ⚠️', '#be123c', 1), (1070, 'Sep 2026', '40% of GitHub PRs', 'start with an agent', '#15803d', 0)]
for i, (x, y, t, sub, c, up) in enumerate(EV):
    x = 110 + (x - 60) * 0.98; yy = 110 if up else 246
    s += f'<g class="fd" style="animation-delay:{i*.15}s"><circle cx="{x}" cy="200" r="8" fill="{c}"/><line x1="{x}" y1="{200-8 if up else 208}" x2="{x}" y2="{yy+50 if up else yy-16}" stroke="{c}" stroke-width="1.4"/>'
    s += note(x, yy + 4, y, c, 13, 'middle', True) + note(x, yy + 22, t, '#0f172a', 12.5, 'middle', True) + note(x, yy + 40, sub, '#475569', 11.5, 'middle') + '</g>'
s += note(24, 318, 'Sources: Cusumano, “Japan’s Software Factories” (1991); Stripe engineering blog; GitHub Octoverse 2026; vendor announcements ⚠️.', '#64748b', 11.5)
save('3-history.svg', s)

# 4. a minion run
W, H = 1200, 470; s = head(W, H, 'One Stripe minion run, start to pull request', 'From Stripe’s Minions posts (Feb 2026). Rectangles = deterministic code; dashed = agent loop') + ANIM
N = [(24, 90, 'Slack, CLI, web or ticket', ['engineer or a flaky-test ticket'], '#2563eb', 0), (264, 90, 'Devbox ready in ~10 s', ['pre-warmed EC2, QA env, no prod'], '#475569', 0),
     (504, 90, 'Hydrate context', ['MCP tools on links in the thread', 'scoped rule files'], '#7c3aed', 0), (744, 90, 'Implement task', ['agent loop (forked goose)'], '#0d9488', 1),
     (984, 90, 'Run linters', ['deterministic node, loop locally'], '#d97706', 0), (984, 250, 'Push → CI round 1', ['selected tests of 3M+', 'auto-apply autofixes'], '#d97706', 0),
     (744, 250, 'Fix CI failures', ['agent loop, one more try'], '#0d9488', 1), (504, 250, 'Push → CI round 2', ['then stop: max two rounds'], '#d97706', 0),
     (264, 250, 'Pull request', ['Stripe PR template'], '#15803d', 0), (24, 250, 'Human review', ['engineer reviews, asks a peer', 'or sends new instructions'], '#be123c', 0)]
for i, (x, y, t, sub, c, ag) in enumerate(N):
    s += f'<g class="fd" style="animation-delay:{i*.12}s">' + box(x, y, 200, 96, t, sub, c, dash=bool(ag)) + '</g>'
for a, b in [(0, 1), (1, 2), (2, 3), (3, 4)]: s += arr(N[a][0] + 200, 138, N[b][0], 138)
s += arr(1084, 186, 1084, 250)
for a, b in [(5, 6), (6, 7), (7, 8), (8, 9)]: s += arr(N[a][0], 298, N[b][0] + 200, 298)
s += box(24, 380, 560, 60, 'Toolshed: central MCP server, ~500 tools', ['minions get a small curated subset; security controls block destructive calls'], '#7c3aed')
s += box(616, 380, 560, 60, 'Result: 1,300+ merged PRs a week', ['fully minion-written, every one human-reviewed (Stripe, Part 2)'], '#15803d')
save('4-minion-run.svg', s)

# 5. workflows vs agents vs blueprints
W, H = 1200, 360; s = head(W, H, 'Workflow, agent, blueprint', 'Stripe’s “blueprint”: a workflow in code whose nodes are either plain code or an agent loop') + ANIM
s += band(24, 80, 360, 250, 'WORKFLOW: FIXED GRAPH', '#475569') + band(420, 80, 360, 250, 'AGENT: LOOP WITH TOOLS', '#0d9488') + band(816, 80, 360, 250, 'BLUEPRINT: BOTH', '#d97706')
for i, t in enumerate(['Step A', 'Step B', 'Step C']): s += box(64 + i * 104, 170, 88, 50, t, c='#475569', fs=13)
s += arr(152, 195, 168, 195) + arr(256, 195, 272, 195)
s += box(520, 140, 160, 56, 'Model decides', c='#0d9488', dash=True) + box(520, 236, 160, 56, 'Call a tool', c='#0d9488')
s += f'<path d="M680,168 C740,168 740,264 680,264" fill="none" stroke="#0d9488" stroke-width="1.7" marker-end="url(#a)"/><path d="M520,264 C460,264 460,168 520,168" fill="none" stroke="#0d9488" stroke-width="1.7" marker-end="url(#a)"/>'
B = [(836, 'Implement', 1), (936, 'Lint', 0), (1036, 'Fix CI', 1)]
for x, t, ag in B: s += box(x, 170, 84, 50, t, c='#0d9488' if ag else '#d97706', dash=bool(ag), fs=13)
s += arr(920, 195, 936, 195) + arr(1020, 195, 1036, 195)
s += note(200, 300, 'predictable, cannot handle surprises', '#475569', 12, 'middle') + note(600, 318, 'flexible, may skip required steps', '#0d9488', 12, 'middle') + note(996, 300, 'guaranteed steps + flexible ones', '#b45309', 12, 'middle', True)
save('5-blueprint.svg', s)

# 6. isolation ladder
W, H = 1200, 380; s = head(W, H, 'Where parallel agents run: the isolation ladder', 'Each rung buys more isolation and more agents at once, for more setup (our reading)') + ANIM
R = [('Same folder', 'one agent at a time', 'agents overwrite each other', '#94a3b8'), ('Git worktrees', 'a checkout per agent, one machine', 'ports, databases, caches collide', '#2563eb'),
     ('Containers', 'own filesystem + services per agent', 'heavier, slower to start', '#7c3aed'), ('Cloud dev boxes', 'pre-warmed VMs (Stripe: ~10 s)', 'needs platform investment', '#0d9488')]
for i, (t, a, b, c) in enumerate(R):
    x = 40 + i * 285; y = 260 - i * 50
    s += f'<g class="fd" style="animation-delay:{i*.2}s">' + box(x, y, 250, 92, t, [a, 'limit: ' + b], c) + '</g>'
    if i < 3: s += arr(x + 250, y + 46, x + 285, y - 4)
s += note(40, 368, 'Isolation also bounds damage: Stripe’s devboxes run in a QA environment with no production data and no open internet, so agents run without permission prompts.', '#475569', 12)
save('6-isolation.svg', s)

# 7. review bottleneck (illustrative model, same as the article calculator)
W, H = 1200, 420; s = head(W, H, 'The review bottleneck (illustrative)', 'Agents add PRs; one reviewer handles a fixed number a day. Past that line the queue grows every day') + ANIM
x0, y0, pw, ph = 90, 360, 1040, 260
s += f'<line x1="{x0}" y1="{y0}" x2="{x0+pw}" y2="{y0}" stroke="#334155"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-ph}" stroke="#334155"/>'
pts = []; pts2 = []
for a in range(0, 21):
    made = a * 3.0; merged = min(made, 24.0)
    X = x0 + a / 20 * pw; pts.append(f'{X:.0f},{y0 - made/60*ph:.0f}'); pts2.append(f'{X:.0f},{y0 - merged/60*ph:.0f}')
s += f'<polyline class="dr" points="{" ".join(pts)}" fill="none" stroke="#2563eb" stroke-width="3"/><polyline class="dr" points="{" ".join(pts2)}" fill="none" stroke="#15803d" stroke-width="3"/>'
s += f'<rect x="{x0+8/20*pw}" y="{y0-ph}" width="{pw-8/20*pw}" height="{ph}" fill="#fee2e2" opacity=".5"/>'
s += note(x0 + 14/20*pw, y0 - ph + 22, 'queue grows here', '#b91c1c', 13, 'middle', True)
s += note(x0 + pw, y0 + 22, 'agents per team →', '#334155', 12, 'end') + note(x0 - 8, y0 - ph - 6, 'PRs a day', '#334155', 12)
s += note(x0 + pw - 10, y0 - 60/60*ph + 30, 'PRs produced', '#2563eb', 13, 'end', True) + note(x0 + pw - 10, y0 - 24/60*ph - 8, 'PRs merged (4 reviewers × 6 a day)', '#15803d', 13, 'end', True)
s += note(24, 404, 'Illustrative: 3 PRs per agent per day, 4 reviewers handling 6 each. Change the inputs in the calculator in this article.', '#64748b', 11.5)
save('7-bottleneck.svg', s)

# 8. gates stack
W, H = 1200, 440; s = head(W, H, 'The gates: what each one catches', 'Cheap, fast checks first; slow, expensive checks last (“shift feedback left”)') + ANIM
G = [('Pre-push lint + format', 'seconds', 'style, obvious errors', '#2563eb'), ('Type check + build', 'seconds–minutes', 'broken interfaces', '#7c3aed'),
     ('Selected tests + autofixes', 'minutes', 'regressions in touched code', '#0d9488'), ('Security + dependency scans', 'minutes', 'secrets, known vulnerabilities', '#d97706'),
     ('Evals for AI features', 'minutes–hours', 'quality drops in model behaviour', '#c2410c'), ('Cost + scope limits', 'per run', 'runaway tokens, oversized diffs', '#475569'),
     ('Human review', 'hours', 'wrong intent, risky design, taste', '#be123c')]
for i, (t, sp, c_, col) in enumerate(G):
    y = 76 + i * 50; w = 1150 - i * 70
    s += f'<g class="fd" style="animation-delay:{i*.12}s"><rect x="{(1200-w)/2}" y="{y}" width="{w}" height="42" rx="8" fill="{col}18" stroke="{col}"/>'
    s += note(600, y + 18, t, '#0f172a', 14, 'middle', True) + note(600, y + 35, f'{sp} · catches: {c_}', '#334155', 12, 'middle') + '</g>'
s += note(24, 428, 'Our reading of common practice; Stripe runs lint on every push in under a second, at most two CI rounds, then human review.', '#64748b', 11.5)
save('8-gates.svg', s)

# 9. LinearB yield
W, H = 1200, 400; s = head(W, H, 'Agent PRs land less often than other PRs', 'LinearB “PR yield rate”: share of opened PRs that merge, by organisation tier (2026 benchmarks)') + ANIM
T = [('Elite (top 10%)', 90, 79), ('Good (top 30%)', 86, 58), ('Fair (top 60%)', 81, 37)]
for i, (t, a, g) in enumerate(T):
    y = 100 + i * 90
    s += note(24, y + 30, t, '#0f172a', 14, bold=True)
    s += f'<rect class="gr" x="240" y="{y}" width="{a*8}" height="26" rx="6" fill="#64748b"/>' + note(250 + a * 8, y + 19, f'{a}% all PRs', '#0f172a', 13, bold=True)
    s += f'<rect class="gr" style="animation-delay:.3s" x="240" y="{y+32}" width="{g*8}" height="26" rx="6" fill="#be123c"/>' + note(250 + g * 8, y + 51, f'{g}% agentic PRs', '#be123c', 13, bold=True)
s += note(24, 384, 'Source: LinearB 2026 AI benchmarks, 2.7M PRs, 83,000 developers, 253 organisations, Feb–May 2026 (vendor first-party data) ⚠️.', '#64748b', 11.5)
save('9-yield.svg', s)

# 10. DORA amplifier
W, H = 1200, 360; s = head(W, H, 'AI is an amplifier (DORA 2025)', 'The same agents make a strong delivery system faster and a weak one more unstable') + ANIM
s += box(40, 120, 220, 100, 'More AI-written code', ['more changes, faster'], '#2563eb')
s += arr(260, 150, 420, 110, 'strong tests, small changes', '#15803d') + arr(260, 190, 420, 250, 'weak tests, big changes', '#be123c', m='r')
s += box(420, 70, 330, 80, 'Higher throughput, stable', ['changes ship faster, incidents flat'], '#15803d')
s += box(420, 210, 330, 80, 'Higher throughput, less stable', ['more rollbacks and incidents'], '#be123c')
s += box(800, 120, 360, 110, 'DORA 2025 findings', ['~5,000 respondents · 90% use AI at work', 'AI now raises throughput', 'instability still rises with AI use'], '#475569')
s += note(24, 344, 'Source: DORA, State of AI-assisted Software Development 2025 (dora.dev). The diagram is our illustration of its “amplifier” finding.', '#64748b', 11.5)
save('10-amplifier.svg', s)

# 11. this site's factory, with counts from this checkout
n = subprocess.run(['git', 'log', '--oneline'], cwd=ROOT, capture_output=True, text=True).stdout.count('\n')
W, H = 1200, 420; s = head(W, H, 'This site as a one-worker software factory', 'The same six stations, as they run for FrontierAGI Academy') + ANIM
SS = [('Intake', ['owner’s chat requests', 'weekly data routine'], '#2563eb'), ('Plan', ['outline, sources, files to touch'], '#7c3aed'), ('Build', ['one agent (Claude) writes', 'pages, scripts, data'], '#0d9488'),
      ('Gates', ['build.py --check: links, data,', 'stale files · Playwright 1400/390', '· CI re-runs article code'], '#d97706'), ('Human gate', ['owner reviews the live page', 'and asks for changes'], '#be123c'), ('Ship & measure', ['push → GitHub Pages', 'feedback becomes the next request'], '#15803d')]
for i, (t, sub, c) in enumerate(SS):
    x = 24 + i * 194
    s += f'<g class="fd" style="animation-delay:{i*.15}s">' + box(x, 100, 170, 120, t, sub, c) + '</g>'
    if i < 5: s += arr(x + 170, 160, x + 194, 160)
s += f'<path class="dr" d="M1110,222 C1110,320 90,320 90,222" fill="none" stroke="#15803d" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#a)"/>'
s += note(600, 340, f'{n} commits are visible in this repository checkout (shallow history from 26 Oct 2026)', '#0f172a', 13, 'middle', True)
s += note(600, 362, 'Missing next to a full factory: parallel workers, automatic intake, production metrics', '#b91c1c', 12.5, 'middle')
save('11-our-factory.svg', s)

# 12. road to autonomous software
W, H = 1200, 380; s = head(W, H, 'From factory to autonomous software: what has to be solved', 'Our prediction of the order; dates are guesses') + ANIM
RD = [('Today', 'agents write, people approve every merge', '#15803d'), ('Next', 'agents also review low-risk changes; people approve by risk tier', '#2563eb'),
      ('Then', 'agents deploy behind canaries and roll back on their own', '#7c3aed'), ('Later', 'agents run on-call for their own services; people set goals and limits', '#be123c')]
for i, (t, d, c) in enumerate(RD):
    x = 30 + i * 290
    ww = d.split(); L = ['']
    for w_ in ww:
        if len(L[-1]) + len(w_) > 36: L.append('')
        L[-1] = (L[-1] + ' ' + w_).strip()
    s += f'<g class="fd" style="animation-delay:{i*.2}s">' + box(x, 90, 260, 100, t, L, c) + '</g>'
    if i < 3: s += arr(x + 260, 140, x + 290, 140)
NEED = ['Agent identity and accountability', 'Prompt-injection-proof tools', 'Long-run reliability', 'Checking work people cannot check']
for i, t in enumerate(NEED): s += box(30 + i * 290, 240, 260, 56, t, c='#475569', dash=True, fs=12)
s += note(600, 330, 'Needed before each step can be trusted (dashed = open problems)', '#475569', 13, 'middle', True)
save('12-road.svg', s)
print('wrote', len([f for f in os.listdir(OUT) if f.endswith('.svg')]), 'diagrams to', OUT)
