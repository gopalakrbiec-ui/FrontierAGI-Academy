#!/usr/bin/env python3
"""Build a lab's interactive evolution timeline from data/lab-updates.json.

    python3 scripts/lab_evolution.py anthropic   # refreshes pages/claude-evolution.html
    python3 scripts/lab_evolution.py openai      # writes   pages/openai-evolution.html

The finished Claude page (pages/claude-evolution.html) is the template: this script swaps in the lab's
items, title, intro, phases, colours and postMessage key. Lanes, phases and the keyword rules that sort
items into lanes are our grouping (the pages say so). Run scripts/build.py afterwards.
"""
import json
import re
import sys

LABS = {
    'anthropic': dict(
        out='pages/claude-evolution.html', key='ceHeight', start='2022-03-01', y0='2022',
        title='How Claude Evolved, 2023–2026', grad='linear-gradient(135deg,#1c1917,#6b4c9a 50%,#b4532a)',
        intro='From one chat model in March 2023 to model families, a developer platform, an agent harness and products for coding, science, design and whole industries. Every Anthropic announcement this site tracks, laid out in seven lanes. Press play to watch it grow, hide lanes, or tap any dot.',
        rules=[('co', r'series|invest|ipo|s-1|partnership|acquires|compute deal|institute|frontier academy|usage limits'),
               ('safe', r'constitution|safety|scaling policy|asl-3|espionage|distillation|watermark|directive|golden gate|hardware standard'),
               ('app', r'^claude 2 and claude\.ai'), ('model', r'^claude 3\.5 sonnet and artifacts'),
               ('agent', r'claude code|skills|computer use|ship|agent'),
               ('plat', r'mcp|model context|context window|contextual retrieval|100k'),
               ('ind', r'for (financial|life|healthcare|creative|teachers)|science|novel enzyme'),
               ('app', r'claude\.ai|pro$|projects|design|tag|duet|labs')],
        phases=[['2023-03', '2024-03', 'A model you talk to', 'Claude, Claude 2 and claude.ai, Pro, the constitution and the Responsible Scaling Policy.'],
                ['2024-03', '2025-02', 'Tiers, a workspace and hands', 'Opus / Sonnet / Haiku tiers, Artifacts and Projects, computer use, MCP.'],
                ['2025-02', '2026-01', 'An agent that does work', 'Claude Code, Claude 4, Agent Skills, the first industry products.'],
                ['2026-01', '2026-12', 'A portfolio', 'Healthcare, Design, Science, Slack and Ship; new Fable and Mythos lines; the IPO.']],
        see='<a href="claude-platform-rings.html">The Claude Platform in Rings</a>',
        disclose='Disclosure: Claude, made by Anthropic, helps write this site, so this is Anthropic’s own history drawn with Claude’s help.'),
    'openai': dict(
        out='pages/openai-evolution.html', key='oaeHeight', start='2021-09-01', y0='2021',
        title='How OpenAI Evolved, 2021–2026', grad='linear-gradient(135deg,#0b3d2e,#10a37f 55%,#111827)',
        intro='From a GPT-3 API with a waitlist to ChatGPT, a developer platform, reasoning models, coding and computer-use agents, a browser and a wallet. Every OpenAI announcement this site tracks, laid out in seven lanes. Press play to watch it grow, hide lanes, or tap any dot.',
        rules=[('co', r'board removes|altman'),
               ('safe', r'hallucinate|safety tests'),
               ('agent', r'codex|operator|deep research|agent'),
               ('plat', r'api|devday|apps sdk'),
               ('ind', r'health'),
               ('app', r'chatgpt|gpt store|sora app|atlas|wallet|pro adds')],
        phases=[['2021-10', '2022-11', 'An API for researchers', 'The GPT-3 API opens without a waitlist; InstructGPT, DALL·E 2, Whisper.'],
                ['2022-11', '2024-05', 'ChatGPT and a platform', 'ChatGPT, GPT-4, plugins, the Assistants API, GPTs and the GPT Store.'],
                ['2024-05', '2025-08', 'Reasoning and agents', 'GPT-4o, the o-series, Operator, deep research, the Agents SDK and Codex.'],
                ['2025-08', '2026-12', 'A portfolio', 'GPT-5 and GPT-6 families, open weights, the Atlas browser, Sora app, Health and Wallet.']],
        see='<a href="openai-platform-rings.html">The OpenAI Platform in Rings</a>',
        disclose='Disclosure: Claude, made by Anthropic (an OpenAI competitor), helps write this site.'),
}
COLS = ['#e7e5e4', '#ede9fe', '#dbeafe', '#ffedd5']


def lane(title, rules):
    t = title.lower()
    for ln, rx in rules:
        if re.search(rx, t):
            return ln
    return 'model'


def sub(pattern, repl, s, flags=re.S):
    out, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    assert n == 1, pattern
    return out


def build(lab):
    C = LABS[lab]
    d = json.load(open('data/lab-updates.json'))
    items = sorted([x for x in d['items'] if x['lab'] == lab], key=lambda x: x['date'])
    rows = [[x['date'], x['title'], lane(x['title'], C['rules']), x.get('summary', ''), x.get('source', ''),
             1 if x.get('flagship') else 0] for x in items]
    s = open('pages/claude-evolution.html').read()
    s = sub(r'<title>.*?</title>', '<title>%s — FrontierAGI Academy</title>' % C['title'], s)
    s = re.sub(r'<!-- SEO:START -->.*?<!-- SEO:END -->\n?', '', s, count=1, flags=re.S)
    s = sub(r'\.ce-hero\{background:[^;]*;', '.ce-hero{background:%s;' % C['grad'], s)
    s = sub(r'<div class="ce-hero"><h1>.*?</h1><p class="intro">.*?</p></div>',
            '<div class="ce-hero"><h1>%s</h1><p class="intro">%s</p></div>' % (C['title'], C['intro']), s)
    s = sub(r'aria-label="Timeline of [^"]*"', 'aria-label="Timeline of %s releases by lane"' % C['title'].split(' Evolved')[0].replace('How ', ''), s)
    s = sub(r'Disclosure: [^<]*</p><p>See also <a [^<]*</a>\.',
            C['disclose'] + '</p><p>See also ' + C['see'] + '.', s)
    s = sub(r'var R=\[.*?\];\n', 'var R=' + json.dumps(rows, ensure_ascii=False) + ';\n', s)
    ph = [p + [COLS[i]] for i, p in enumerate(C['phases'])]
    s = sub(r'var PH=\[.*?\];', 'var PH=' + json.dumps(ph, ensure_ascii=False) + ';', s)
    s = sub(r"var T0=mo\('[0-9-]+'\)", "var T0=mo('%s')" % C['start'], s)
    extra = ",'2022-01'" if C['start'] < '2022' else ''
    s = re.sub(r"\['20\d\d-\d\d',('2022-01',)?'2023-01'", "['%s'%s,'2023-01'" % (C['start'][:7], extra), s, count=1)
    s = re.sub(r"m==='20\d\d-\d\d'\?'20\d\d'", "m==='%s'?'%s'" % (C['start'][:7], C['y0']), s, count=1)
    s = s.replace('ceHeight', C['key'])
    open(C['out'], 'w').write(s)
    counts = {}
    for r in rows:
        counts[r[2]] = counts.get(r[2], 0) + 1
    print(C['out'], len(rows), counts)


if __name__ == '__main__':
    for lab in sys.argv[1:] or ['anthropic']:
        build(lab)
