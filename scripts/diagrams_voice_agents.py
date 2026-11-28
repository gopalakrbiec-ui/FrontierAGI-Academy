# Generates assets/diagrams/voice-agents/*.svg for the "Voice and Real-Time Agents" series
#   python3 scripts/diagrams_voice_agents.py
# Facts: Pipecat, LiveKit Agents, OpenAI realtime samples, Gemini Live console and Smart Turn READMEs,
# dated launches from data/lab-updates.json. Charts 2 and 5 run the scripts in data/code/ (illustrative toy models).
import os, subprocess, sys
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagrams_adlc.py')).read().split('# 1 timeline')[0]
exec(_src)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'assets', 'diagrams', 'voice-agents') + '/'
os.makedirs(OUT, exist_ok=True)
def save(n, s): open(OUT + n, 'w').write(s + '</svg>')
def run(rel): return subprocess.run([sys.executable, '-S', os.path.join(ROOT, 'data', 'code', rel)], capture_output=True, text=True).stdout.splitlines()
C = {'stt': '#2563eb', 'llm': '#7c3aed', 'tts': '#0d9488', 's2s': '#be123c', 'net': '#475569', 'turn': '#d97706'}

# 1 two architectures
W, H = 1200, 440; s = head(W, H, 'Two ways to build a voice agent', 'A cascade of three models, or one speech-to-speech model (both supported by Pipecat and LiveKit Agents)') + ANIM
s += band(24, 76, 1152, 160, 'CASCADE', C['stt']) + band(24, 256, 1152, 150, 'SPEECH-TO-SPEECH (REALTIME MODEL)', C['s2s'])
for i, (t, sub, c) in enumerate([('Caller audio', 'mic / phone', C['net']), ('Speech-to-text', 'streaming transcript', C['stt']), ('LLM', 'text in, text out, tools', C['llm']), ('Text-to-speech', 'streams audio back', C['tts']), ('Caller hears', 'speaker', C['net'])]):
    x = 50 + i * 228; s += f'<g class="fd" style="animation-delay:{i*.12}s">' + box(x, 112, 190, 80, t, [sub], c) + '</g>' + (arr(x + 190, 152, x + 228, 152) if i < 4 else '')
for i, (t, sub, c, x, w) in enumerate([('Caller audio', 'mic / phone', C['net'], 50, 190), ('Realtime model', 'audio in → audio out, tools', C['s2s'], 390, 420), ('Caller hears', 'speaker', C['net'], 962, 190)]):
    s += box(x, 290, w, 80, t, [sub], c)
s += arr(240, 330, 388, 330) + arr(812, 330, 960, 330)
s += note(24, H - 12, 'Cascade: pick each model, see the text, easier to control. Speech-to-speech: fewer hops, keeps tone of voice, less visible in between (our summary).', '#64748b', 11.5)
save('1-architectures.svg', s)

# 2 latency waterfall from script
r = run('voice-agents-latency/latency_budget.py')[:4]
W, H = 1100, 360; s = head(W, H, 'From “caller stops talking” to “agent starts talking”', 'Toy latency budget in milliseconds (latency_budget.py); grey = after tuning') + ANIM
for i, ln in enumerate(r):
    a = ln.split(); base = int(a[-5]); tuned = int(a[-2]); lab = ln[:35].strip().replace('  ', ' ')
    y = 86 + i * 62; X = lambda v: 330 + v / 2000 * 700
    s += note(24, y + 22, lab, '#0f172a', 13, bold=True)
    s += f'<rect class="gr" style="animation-delay:{i*.15}s" x="330" y="{y+4}" width="{X(base)-330:.0f}" height="24" rx="5" fill="{C["s2s"] if "speech-to" in lab else C["llm"]}"/>' + note(X(base) + 6, y + 22, f'{base} ms', '#0f172a', 12.5, bold=True)
    s += f'<rect x="330" y="{y+32}" width="{X(tuned)-330:.0f}" height="12" rx="4" fill="#94a3b8"/>' + note(X(tuned) + 6, y + 43, f'tuned {tuned}', '#475569', 11.5)
s += f'<line x1="{330+800/2000*700:.0f}" y1="76" x2="{330+800/2000*700:.0f}" y2="{H-40}" stroke="#15803d" stroke-dasharray="5 4"/>' + note(330 + 800 / 2000 * 700 + 4, 74, '800 ms', '#15803d', 12, bold=True)
s += note(24, H - 12, 'Humans usually leave gaps of a few hundred ms between turns (conversation research ⚠️); 800 ms is a common practical target (our reading).', '#64748b', 11.5)
save('2-latency.svg', s)

# 3 turn detection
W, H = 1200, 360; s = head(W, H, 'When has the caller finished?', 'Silence alone (VAD) vs a turn-detection model that also listens to words and tone (Smart Turn, LiveKit turn detector)') + ANIM
s += band(24, 76, 560, 250, 'SILENCE TIMER (VAD ONLY)', C['turn']) + band(616, 76, 560, 250, 'SEMANTIC / AUDIO TURN MODEL', '#15803d')
for i, t in enumerate(['“My order number is…”', '(pause to find it)', 'Agent jumps in ✗', 'Caller talks over it']): s += box(50, 110 + i * 52, 510, 42, t, None, C['turn'] if i != 2 else '#be123c', fs=13)
for i, t in enumerate(['“My order number is…”', '(pause: sentence not finished)', 'Model waits ✓', '“…4-7-2-9.” → reply']): s += box(642, 110 + i * 52, 510, 42, t, None, '#15803d', fs=13)
s += note(24, H - 12, 'Smart Turn v3.2: 23 languages, ~10 ms on some CPUs, under 100 ms on most cloud instances, runs only during silences (its README).', '#64748b', 11.5)
save('3-turns.svg', s)

# 4 the stack
W, H = 1200, 470; s = head(W, H, 'The voice agent stack', 'Layers and example products; names from public repos and our lab-updates data, not an endorsement') + ANIM
L = [('Telephony and transport', 'PSTN / SIP, WebRTC, WebSockets', 'Twilio, LiveKit SIP, browser WebRTC', C['net']),
     ('Orchestration framework', 'pipelines, turn-taking, interruptions', 'Pipecat, LiveKit Agents, OpenAI Agents SDK', '#0f172a'),
     ('Speech-to-speech models', 'audio in and out', 'OpenAI gpt-realtime, Gemini Live, Grok Voice ⚠️', C['s2s']),
     ('Speech-to-text', 'streaming transcription', 'Whisper-family, Deepgram ⚠️, Voxtral', C['stt']),
     ('Language model', 'reasoning, tools', 'any chat model', C['llm']),
     ('Text-to-speech', 'natural voices, streaming', 'ElevenLabs ⚠️, MAI-Voice, open models', C['tts'])]
for i, (t, job, ex, c) in enumerate(L):
    y = 76 + i * 64; s += f'<g class="fd" style="animation-delay:{i*.12}s"><rect x="24" y="{y}" width="1152" height="54" rx="10" fill="{c}12" stroke="{c}" stroke-width="1.6"/>' + note(44, y + 24, t, c, 15, bold=True) + note(44, y + 44, job, '#334155', 12.5) + note(1156, y + 34, ex, '#0f172a', 13, 'end', True) + '</g>'
save('4-stack.svg', s)

# 5 cost per minute from script
r = run('voice-agents-production/cost_per_minute.py')
rows = [(ln[:20].strip(), float(ln.split('$')[1].split('/')[0])) for ln in r if '/min' in ln]
col = {'voice agent total': '#be123c', 'human agent': '#475569'}
hbars('5-cost.svg', 'Cost per call minute (example prices)', 'Voice agent parts vs a human agent at $18/hour, 75% occupancy (cost_per_minute.py)', [(n, v, col.get(n, '#0d9488'), f'${v:.3f}') for n, v in rows], max(v for _, v in rows) * 1.25, unit='', W=1100,
      src='Assumptions in data/code/voice-agents-production/cost_per_minute.py; not vendor prices. ' + r[-1])

# 6 a call with tools and hand-over
W, H = 1200, 400; s = head(W, H, 'One support call, start to finish', 'Our worked example: refund for a broken order') + ANIM
ST = [('Greet + disclose AI', C['net']), ('Verify caller', C['turn']), ('Listen: broken item', C['stt']), ('“Let me check that…”', C['tts']), ('Tool: look up order', C['llm']), ('$240 > $100 limit', '#be123c'), ('Warm transfer to human', '#15803d')]
for i, (t, c) in enumerate(ST):
    x = 24 + i * 166; s += f'<g class="fd" style="animation-delay:{i*.15}s">' + box(x, 120, 150, 90, t, None, c, fs=13) + '</g>' + (arr(x + 150, 165, x + 166, 165) if i < 6 else '')
s += note(24, 260, 'Filler speech covers the tool call; the transfer passes a summary so the caller does not repeat themselves.', '#334155', 13.5, bold=True)
s += note(24, 284, 'OpenAI’s realtime agents demo shows the same idea: a fast realtime agent talks while a stronger text model handles tools (“chat-supervisor”).', '#334155', 13)
s += note(24, H - 12, 'Illustrative flow.', '#64748b', 11.5)
save('6-call.svg', s)

# 7 timeline
W, H = 1200, 400; s = head(W, H, 'From phone menus to realtime models', 'Dated launches from data/lab-updates.json; earlier milestones are general history ⚠️') + ANIM
EV = [('1990s', 'IVR menus', '“press 1 for…”', '#64748b', 1), ('2011', 'Siri', 'voice assistants', '#64748b', -1), ('2022-09', 'Whisper', 'open speech-to-text', '#10a37f', 1), ('2024-10', 'Realtime API', 'OpenAI DevDay', '#10a37f', -1),
      ('2025-08', 'gpt-realtime GA', 'OpenAI', '#10a37f', 1), ('2025-08', 'MAI-Voice-1', 'Microsoft', '#2563eb', -1), ('2026-10', 'Grok Voice 3.0', 'xAI', '#0f172a', 1), ('2026-10', 'GPT-Live-1.1', 'ChatGPT Voice', '#10a37f', -1), ('2026-10', 'Voxtral 3', 'Mistral + voice SDK', '#d97706', 1)]
s += '<line x1="50" y1="210" x2="1160" y2="210" stroke="#334155" stroke-width="3"/>'
for i, (d, t, sub, c, up) in enumerate(EV):
    x = 90 + i * 128; ty = 120 if up > 0 else 290
    s += f'<g class="fd" style="animation-delay:{i*.1}s"><circle cx="{x}" cy="210" r="8" fill="{c}"/><line x1="{x}" y1="{210-up*8}" x2="{x}" y2="{ty+(18 if up>0 else -34)}" stroke="{c}" stroke-dasharray="3 3"/>' + note(x, ty - 14 if up > 0 else ty, d, c, 12.5, 'middle', True) + note(x, ty + 4 if up > 0 else ty + 18, t, '#0f172a', 12.5, 'middle', True) + note(x, ty + 20 if up > 0 else ty + 34, sub, '#475569', 11, 'middle') + '</g>'
s += note(24, H - 12, 'Some 2026 entries come from secondary sources in our lab-updates data ⚠️.', '#64748b', 11.5)
save('7-timeline.svg', s)
print('wrote', OUT)
