# Generates assets/diagrams/context-eng/*.svg for the "Context Engineering" series
#   python3 scripts/diagrams_context_engineering.py
# Facts: Anthropic "Effective context engineering for AI agents", Agent Skills and multi-agent research posts,
# Claude docs (prompt caching, context editing, compaction, context windows), LangChain context_engineering repo.
# The budget chart runs data/code/context-eng-long-tasks/budget_sim.py (illustrative toy model). Layouts are ours.
import os, subprocess, sys
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagrams_adlc.py')).read().split('# 1 timeline')[0]
exec(_src)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'assets', 'diagrams', 'context-eng') + '/'
os.makedirs(OUT, exist_ok=True)
def save(n, s): open(OUT + n, 'w').write(s + '</svg>')
C = {'sys': '#475569', 'tools': '#2563eb', 'mem': '#7c3aed', 'rag': '#0d9488', 'res': '#d97706', 'hist': '#be123c', 'free': '#e2e8f0'}

# 1 anatomy of a context window
W, H = 1200, 430; s = head(W, H, 'What fills an agent’s context window', 'One illustrative mid-task snapshot; shares vary a lot by agent (our example)') + ANIM
P = [('System prompt', 4, 'sys'), ('Tool definitions', 8, 'tools'), ('Project file + memory', 4, 'mem'), ('Retrieved documents', 10, 'rag'), ('Tool results', 34, 'res'), ('Conversation + reasoning', 18, 'hist'), ('Free space', 22, 'free')]
x = 40
for i, (t, p, k) in enumerate(P):
    w = 1120 * p / 100
    s += f'<rect class="gr" style="animation-delay:{i*.12}s" x="{x:.0f}" y="110" width="{w-3:.0f}" height="90" rx="8" fill="{C[k]}"/>'
    s += note(x + w / 2, 160, f'{p}%', '#fff' if k != 'free' else '#475569', 15, 'middle', True)
    s += note(x + w / 2, 230 + (i % 2) * 26, t, C[k] if k != 'free' else '#64748b', 13, 'middle', True)
    x += w
s += note(40, 316, 'Stable (cacheable): system prompt, tools, project file', '#334155', 13.5, bold=True) + note(40, 338, 'Grows every turn: tool results and conversation, usually the biggest and least useful part', '#334155', 13.5)
s += note(40, 370, 'Anthropic: “find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome.”', '#7c3aed', 13, bold=True)
s += note(24, H - 14, 'Shares are illustrative, not measured. Source for the principle: Anthropic, “Effective context engineering for AI agents”.', '#64748b', 11.5)
save('1-anatomy.svg', s)

# 2 four strategies
W, H = 1200, 340; s = head(W, H, 'Four things you can do with context', 'The write / select / compress / isolate framing used in LangChain’s context engineering repo, with examples from Anthropic’s docs') + ANIM
ST = [('Write', 'save it outside the window', ['notes files, to-do lists', 'memory tool', 'scratchpads'], C['mem']), ('Select', 'pull in only what is needed', ['just-in-time retrieval', 'grep / glob over files', 'skills loaded on demand'], C['rag']),
      ('Compress', 'keep the gist, drop the bulk', ['compaction (summaries)', 'tool result clearing', 'trimming old turns'], C['res']), ('Isolate', 'give work its own window', ['sub-agents', 'sandboxes holding big data', 'separate state fields'], C['tools'])]
for i, (t, sub, L, c) in enumerate(ST):
    x = 30 + i * 290; s += f'<g class="fd" style="animation-delay:{i*.15}s">' + box(x, 90, 260, 190, t, [sub, ''] + ['• ' + l for l in L], c, fs=20) + '</g>'
s += note(24, H - 14, 'Sources: github.com/langchain-ai/context_engineering (notebooks 1–4); Anthropic engineering blog and Claude docs.', '#64748b', 11.5)
save('2-strategies.svg', s)

# 3 budget simulation (from the script)
r = subprocess.run([sys.executable, '-S', os.path.join(ROOT, 'data', 'code', 'context-eng-long-tasks', 'budget_sim.py')], capture_output=True, text=True).stdout.splitlines()
rows = []
for ln in r[1:5]:
    name = ln[:20].strip(); parts = ln[20:].split()
    rows.append((name, int(parts[0].replace(',', '')), int(parts[1].replace(',', ''))))
col = {'none': '#be123c', 'clear tool results': '#d97706', 'compaction': '#7c3aed', 'sub-agents': '#2563eb'}
hbars('3-budget.svg', 'Input tokens over a 40-turn toy run', 'Total input tokens the lead agent reads, by strategy (our toy model; sub-agents’ own tokens not counted)',
      [(n, round(t / 1e6, 2), col[n], f'peak {p:,}') for n, t, p in rows], max(t for _, t, _ in rows) / 1e6 * 1.3, unit='M', W=1100,
      src='Source: data/code/context-eng-long-tasks/budget_sim.py (assumptions in the script). Anthropic reports multi-agent systems use ~15× the tokens of chat.')

# 4 progressive disclosure (skills)
W, H = 1200, 380; s = head(W, H, 'Progressive disclosure: how skills stay cheap', 'Three levels, from Anthropic’s Agent Skills post') + ANIM
LV = [('Level 1: name + description', 'pre-loaded for every installed skill', 'a line or two each', '#0d9488'), ('Level 2: SKILL.md body', 'read only when the skill looks relevant', 'instructions', '#2563eb'), ('Level 3: extra files and scripts', 'opened or run only if needed', 'references, code', '#7c3aed')]
for i, (t, a, b, c) in enumerate(LV):
    y = 80 + i * 92; w = 1120 - i * 220
    s += f'<g class="fd" style="animation-delay:{i*.2}s"><rect x="{40+i*110}" y="{y}" width="{w}" height="74" rx="12" fill="{c}14" stroke="{c}" stroke-width="1.8"/>' + note(64 + i * 110, y + 30, t, c, 16, bold=True) + note(64 + i * 110, y + 54, a + ' · ' + b, '#334155', 13) + '</g>'
s += note(24, H - 14, 'Same idea for tools: Claude’s tool search tool lets an agent defer tool definitions until needed (Claude docs, context windows).', '#64748b', 11.5)
save('4-disclosure.svg', s)

# 5 cache ordering
W, H = 1200, 400; s = head(W, H, 'Order the context so the cache can hit', 'Caches match on an exact prefix: anything that changes must come after the stable part (Claude prompt caching docs)') + ANIM
s += note(40, 100, 'Breaks the cache every turn', '#be123c', 15, bold=True) + note(40, 250, 'Caches well', '#15803d', 15, bold=True)
BAD = [('Timestamp', '#be123c', 160), ('System prompt', C['sys'], 220), ('Tools', C['tools'], 200), ('History…', C['hist'], 360)]
GOOD = [('Tools', C['tools'], 200), ('System prompt', C['sys'], 220), ('Project file', C['mem'], 170), ('◆ breakpoint', '#15803d', 130), ('History…', C['hist'], 190), ('Timestamp + new message', '#be123c', 210)]
for row, y in ((BAD, 115), (GOOD, 265)):
    x = 40
    for t, c, w in row:
        s += f'<rect x="{x}" y="{y}" width="{w-6}" height="60" rx="8" fill="{c}1f" stroke="{c}" stroke-width="1.6"/>' + note(x + (w - 6) / 2, y + 36, t, '#0f172a', 13.5, 'middle', True); x += w
s += note(24, H - 14, 'Docs: up to 4 cache breakpoints; 5-minute or 1-hour lifetimes; place the breakpoint at the end of the static prefix, not on the varying block.', '#64748b', 11.5)
save('5-cache-order.svg', s)

# 6 three long-task techniques
W, H = 1200, 320; s = head(W, H, 'Three techniques for long tasks', 'Anthropic’s guidance on which to use when') + ANIM
T3 = [('Compaction', 'summarise and restart the window', 'tasks with lots of back-and-forth', 'can drop a detail that matters later', C['res']),
      ('Structured notes', 'agent writes NOTES.md / to-dos, reads them back', 'iterative work with clear milestones', 'notes drift if never pruned', C['mem']),
      ('Sub-agents', 'clean windows, return 1,000–2,000-token summaries', 'research with parallel directions', 'many more tokens in total', C['tools'])]
for i, (t, how, best, risk, c) in enumerate(T3):
    x = 30 + i * 390; s += f'<g class="fd" style="animation-delay:{i*.2}s">' + box(x, 90, 360, 180, t, ['', how, '', 'best for: ' + best, '', 'risk: ' + risk], c, fs=19) + '</g>'
s += note(24, H - 14, 'Source: Anthropic, “Effective context engineering for AI agents” (compaction, structured note-taking, sub-agent architectures). Risks are our reading.', '#64748b', 11.5)
save('6-long-tasks.svg', s)
print('wrote', OUT)
