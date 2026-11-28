# Generates assets/diagrams/agent-protocols/*.svg for the "Agent Protocols" series
#   python3 scripts/diagrams_agent_protocols.py
# Facts come from the protocol specs read on 28 Nov 2026 (MCP 2026-07-28, A2A 1.0, AP2 v0.2, ACP 2026-04-17, x402); layouts are ours.
import os
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagrams_adlc.py')).read().split('# 1 timeline')[0]
exec(_src)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'diagrams', 'agent-protocols') + '/'
os.makedirs(OUT, exist_ok=True)
def save(n, s): open(OUT + n, 'w').write(s + '</svg>')
C = {'mcp': '#2563eb', 'a2a': '#0d9488', 'com': '#d97706', 'pay': '#be123c', 'id': '#7c3aed', 'g': '#475569'}

# 1 the protocol stack
W, H = 1200, 560; s = head(W, H, 'The agent protocol stack, late 2026', 'Which protocol carries which conversation (our grouping of the published specs)') + ANIM
L = [('Payments', 'prove the user allowed this payment; move the money', 'AP2 (mandates) · x402 (HTTP 402 payments) · card networks’ agent tokens ⚠️', C['pay']),
     ('Commerce', 'browse, build a cart, check out with a merchant', 'ACP (OpenAI + Stripe) · UCP (Google and partners)', C['com']),
     ('Agent ↔ agent', 'hand a task to another team’s or company’s agent', 'A2A (Linux Foundation, from Google)', C['a2a']),
     ('Agent ↔ tools and data', 'call tools, read resources, use prompts', 'MCP (Agentic AI Foundation, from Anthropic)', C['mcp']),
     ('Identity and auth (under all of them)', 'who is calling, on whose behalf, with what rights', 'OAuth 2.1 / OpenID Connect, signed requests, verifiable credentials', C['id'])]
for i, (t, job, ex, c) in enumerate(L):
    y = 80 + i * 92
    s += f'<g class="fd" style="animation-delay:{i*.15}s"><rect x="24" y="{y}" width="1152" height="80" rx="12" fill="{c}12" stroke="{c}" stroke-width="1.6"/>'
    s += note(44, y + 30, t, c, 17, bold=True) + note(44, y + 54, job, '#334155', 13) + note(1156, y + 44, ex, '#0f172a', 13.5, 'end', True) + '</g>'
s += note(24, H - 14, 'Each layer can run without the ones above it. AP2 runs as an extension of A2A and UCP; ACP added MCP support in 2026-04-17.', '#64748b', 11.5)
save('1-stack.svg', s)

# 2 timeline
W, H = 1200, 420; s = head(W, H, 'Two years of agent protocols', 'Release dates from each project’s own changelog or announcement; ⚠️ = date from secondary reporting') + ANIM
EV = [('2024-11', 'MCP launched', 'Anthropic', C['mcp'], 1), ('2025-03', 'MCP 2025-03-26', 'OAuth 2.1, Streamable HTTP', C['mcp'], -1), ('2025-04', 'A2A announced ⚠️', 'Google', C['a2a'], 1),
      ('2025-06', 'A2A to Linux Fdn ⚠️', 'MCP 2025-06-18: elicitation', C['a2a'], -1), ('2025-09', 'AP2 + ACP', 'Google · OpenAI and Stripe', C['pay'], 1), ('2025-11', 'MCP 2025-11-25', 'tasks (experimental)', C['mcp'], -1),
      ('2025-12', 'MCP to AAIF', 'Agentic AI Foundation', C['mcp'], 1), ('2026-01', 'UCP ⚠️', 'Google and partners', C['com'], -1), ('2026-03', 'A2A 1.0', 'stable spec', C['a2a'], 1),
      ('2026-04', 'ACP 2026-04-17', 'cart, feeds, MCP', C['com'], -1), ('2026-07', 'MCP 2026-07-28', 'stateless core', C['mcp'], 1)]
s += '<line x1="50" y1="220" x2="1160" y2="220" stroke="#334155" stroke-width="3"/>'
for i, (d, t, sub, c, up) in enumerate(EV):
    x = 80 + i * 104; ty = 130 if up > 0 else 300
    s += f'<g class="fd" style="animation-delay:{i*.12}s"><circle cx="{x}" cy="220" r="8" fill="{c}"/><line x1="{x}" y1="{220-up*8}" x2="{x}" y2="{ty+(18 if up>0 else -34)}" stroke="{c}" stroke-dasharray="3 3"/>'
    s += note(x, ty - 14 if up > 0 else ty, d, c, 12.5, 'middle', True) + note(x, ty + 4 if up > 0 else ty + 18, t, '#0f172a', 12.5, 'middle', True) + note(x, ty + 20 if up > 0 else ty + 34, sub, '#475569', 11, 'middle') + '</g>'
s += note(24, H - 14, 'Sources: MCP spec changelogs; A2A CHANGELOG (1.0.0 on 12 Mar 2026); AP2 docs (16 Sep 2025); ACP changelog (2025-09-29 first release).', '#64748b', 11.5)
save('2-timeline.svg', s)

# 3 MCP: old vs new request
W, H = 1200, 470; s = head(W, H, 'MCP becomes stateless (revision 2026-07-28)', 'Before: a session opened with a handshake. After: every request carries its own version and capabilities') + ANIM
s += band(24, 76, 560, 360, 'UP TO 2025-11-25', '#64748b') + band(616, 76, 560, 360, 'FROM 2026-07-28', C['mcp'])
OLD = ['initialize  →  capabilities agreed', 'notifications/initialized', 'Mcp-Session-Id header on every call', 'tools/list (could differ per session)', 'tools/call …', 'server → client: sampling / elicitation']
NEW = ['(optional) server/discover', 'tools/call with _meta: version + capabilities', 'no session id; any server replica can answer', 'tools/list same for everyone, cacheable (ttlMs)', 'needs input? result “input_required”', 'client retries with inputResponses']
for i, t in enumerate(OLD): s += f'<g class="fd" style="animation-delay:{i*.1}s">' + box(48, 108 + i * 52, 512, 42, t, None, '#64748b', fs=13) + '</g>'
for i, t in enumerate(NEW): s += f'<g class="fd" style="animation-delay:{.6+i*.1}s">' + box(640, 108 + i * 52, 512, 42, t, None, C['mcp'], fs=13) + '</g>'
s += note(24, H - 14, 'Source: MCP specification 2026-07-28, “Key Changes” (SEP-2567, SEP-2575, SEP-2322). Why it matters: plain load balancers and caches now work.', '#64748b', 11.5)
save('3-mcp-stateless.svg', s)

# 4 A2A task lifecycle
W, H = 1200, 450; s = head(W, H, 'An A2A task’s life', 'States from the A2A 1.0 specification; arrows are the usual paths') + ANIM
N = {'sub': (40, 180, 'submitted'), 'work': (260, 180, 'working'), 'inp': (500, 80, 'input-required'), 'auth': (500, 290, 'auth-required'), 'done': (800, 60, 'completed'),
     'fail': (800, 150, 'failed'), 'can': (800, 240, 'canceled'), 'rej': (800, 330, 'rejected')}
for k, (x, y, t) in N.items():
    c = C['a2a'] if k in ('sub', 'work') else ('#d97706' if k in ('inp', 'auth') else ('#15803d' if k == 'done' else '#be123c'))
    s += box(x, y, 180 if k not in ('inp', 'auth') else 200, 50, t, None, c, fs=14)
s += arr(220, 205, 258, 205) + arr(440, 195, 498, 110) + arr(498, 120, 442, 200, None, '#d97706', True) + arr(440, 218, 498, 310) + arr(498, 300, 442, 222, None, '#d97706', True)
for y in (85, 175, 265, 355): s += arr(440, 205, 798, y, None, '#94a3b8')
s += '<path d="M130,232 C130,400 600,400 796,362" fill="none" stroke="#94a3b8" stroke-width="1.7" stroke-dasharray="5 4" marker-end="url(#a)"/>' + note(420, 392, 'refused at the start', '#64748b', 11.5, 'middle')
s += note(1000, 90, 'terminal', '#15803d', 13, bold=True) + note(1000, 110, 'no more messages', '#475569', 12) + note(1000, 270, 'terminal', '#be123c', 13, bold=True) + note(1000, 290, 'start a new task', '#475569', 12)
s += note(620, 150, 'interrupted: the client sends', '#b45309', 12, 'middle') + note(620, 166, 'more input or credentials', '#b45309', 12, 'middle')
s += note(24, H - 14, 'Source: A2A specification 1.0 (TASK_STATE_*). Updates arrive by polling, a stream (SSE / gRPC) or push notifications to a webhook.', '#64748b', 11.5)
save('4-a2a-task.svg', s)

# 5 MCP vs A2A
W, H = 1200, 430; s = head(W, H, 'MCP is vertical, A2A is horizontal', 'The A2A project’s own framing: MCP gives one agent depth; A2A gives a system reach') + ANIM
s += box(470, 60, 260, 70, 'Support agent', ['your company'], C['a2a'])
for i, t in enumerate(['CRM tool', 'Refund API', 'Policy docs', 'Ticket system']):
    x = 70 + i * 140; s += box(x, 300, 124, 50, t, None, C['mcp'], fs=13) + arr(600, 132, x + 62, 298, 'MCP' if i == 0 else None, C['mcp'])
for i, t in enumerate(['Carrier’s shipping agent', 'Bank’s fraud agent']):
    y = 180 + i * 110; s += box(880, y, 280, 60, t, ['another company, opaque'], C['a2a'], dash=True) + arr(732, 100, 878, y + 30, 'A2A' if i == 0 else None, C['a2a'])
s += note(24, H - 14, 'Our example. Tools are called with arguments; remote agents are given tasks and may ask questions back, stream progress or take days.', '#64748b', 11.5)
save('5-mcp-vs-a2a.svg', s)

# 6 AP2 mandates
W, H = 1200, 470; s = head(W, H, 'AP2: proving the user said yes', 'Signed “mandates” travel with the purchase (AP2 v0.2); who sees what') + ANIM
R = [('User', 'on a trusted surface', 40, '#0f172a'), ('Shopping agent', 'builds cart', 280, C['a2a']), ('Merchant', 'checkout', 520, C['com']), ('Credential provider', 'wallet / issuer', 760, C['pay']), ('Payment processor', 'merchant’s PSP', 1000, '#475569')]
for t, sub, x, c in R: s += box(x, 80, 170, 60, t, [sub], c, fs=13.5)
s += arr(125, 142, 365, 210, 'signs open mandates', '#7c3aed', lx=230, ly=196)
s += box(250, 214, 260, 64, 'Open mandates', ['limits: budget, items, merchant, expiry'], '#7c3aed', fs=13)
s += arr(380, 280, 600, 330, None, '#7c3aed') + box(470, 330, 300, 64, 'Closed checkout mandate', ['exact cart → merchant'], C['com'], fs=13) + arr(620, 330, 605, 142, None, C['com'])
s += arr(510, 262, 860, 330, None, '#7c3aed') + box(800, 330, 300, 64, 'Closed payment mandate', ['exact amount → provider, network, PSP'], C['pay'], fs=13) + arr(950, 330, 845, 142, None, C['pay']) + arr(950, 330, 1085, 142, None, C['pay'])
s += note(24, H - 30, 'Human present: the user signs the closed mandates. Human not present: the agent signs them, inside the limits of the user-signed open mandates.', '#334155', 12.5, bold=True)
s += note(24, H - 12, 'Source: AP2 specification v0.2 (roles, mandates, modes). Standardisation continues in FIDO Alliance working groups.', '#64748b', 11.5)
save('6-ap2.svg', s)

# 7 x402 flow
W, H = 1200, 400; s = head(W, H, 'x402: paying for an API call with HTTP 402', 'The x402 README’s flow, shortened') + ANIM
X = [(60, 'Agent (client)', C['a2a']), (520, 'Resource server', C['com']), (960, 'Facilitator', C['pay'])]
for x, t, c in X: s += box(x, 70, 200, 50, t, None, c) + f'<line x1="{x+100}" y1="122" x2="{x+100}" y2="372" stroke="{c}" stroke-dasharray="4 4"/>'
M = [(160, 620, 'GET /data'), (620, 160, '402 + PAYMENT-REQUIRED'), (160, 620, 'retry + PAYMENT-SIGNATURE'), (620, 1060, '/verify, then /settle'), (1060, 620, 'settled'), (620, 160, '200 OK + data + PAYMENT-RESPONSE')]
for i, (a, b, t) in enumerate(M):
    y = 150 + i * 38; s += f'<g class="fd" style="animation-delay:{i*.15}s">' + arr(a, y, b, y, t, '#334155', lx=(a + b) / 2, ly=y - 5) + '</g>'
s += note(24, H - 10, 'Source: x402 README (x402 Foundation; started at Coinbase). Built for machine-to-machine payments, mainly stablecoins today.', '#64748b', 11.5)
save('7-x402.svg', s)

# 8 one purchase across the stack
W, H = 1200, 520; s = head(W, H, 'One agent purchase, every protocol', 'Our worked example: “reorder printer ink under $60”') + ANIM
ST = [('1', 'Read past orders and preferences', 'MCP', C['mcp']), ('2', 'Ask the office-supplies merchant’s agent for stock', 'A2A', C['a2a']), ('3', 'Create and update a checkout session', 'ACP or UCP', C['com']),
      ('4', 'Attach the user’s signed mandate (≤ $60, ink only)', 'AP2', C['pay']), ('5', 'Pay through card rails or stablecoin', 'PSP or x402', C['pay']), ('6', 'Order webhook → tell the user', 'ACP / UCP', C['com'])]
for i, (n, t, p, c) in enumerate(ST):
    y = 80 + i * 70
    s += f'<g class="fd" style="animation-delay:{i*.15}s"><circle cx="50" cy="{y+24}" r="18" fill="{c}"/>' + note(50, y + 29, n, '#fff', 15, 'middle', True) + box(84, y, 760, 48, t, None, c, fs=14) + box(870, y, 300, 48, p, None, c, fill='#ffffff', fs=14) + '</g>'
s += note(24, H - 14, 'Illustrative. Real deployments often use only one or two of these; see Part 4 for who supports what.', '#64748b', 11.5)
save('8-purchase.svg', s)
print('wrote', OUT)
