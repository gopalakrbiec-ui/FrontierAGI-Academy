#!/usr/bin/env python3
"""Add an "Each layer over time" timeline under the rings on the lab platform pages.

    python3 scripts/ring_timelines.py      # rewrites the <!-- RINGTL --> block in each rings page

Items come from data/lab-updates.json. Which ring an item belongs to is decided by the keyword
rules below (our grouping; company, funding and safety items are left out). Run build.py afterwards.
"""
import html
import json
import re

PAGES = {
    'anthropic': dict(page='pages/claude-platform-rings.html', anchor='<div class="cr-how">', start='2023-01',
        layers=[('Layer 0 · Model', '#1c1917', r'^claude( \d|$| \(first)|opus|sonnet|haiku|fable|mythos|^claude 3 family'),
                ('Layer 1 · Messages API', '#6b4c9a', r'context window|contextual retrieval|google cloud'),
                ('Layer 2 · Tool-use loop', '#2f6b45', r'computer use'),
                ('Layer 3 · Agent harness', '#2b5a9e', r'model context|mcp|agent skills|claude code(?! for| review| security)|bun'),
                ('Layer 4 · Products', '#b4532a', r'claude\.ai|claude pro|projects|artifacts|claude for|design|tag$|duet|science$|claude ship|labs|code review|code security|code for team')],
        skip=r'series|invest|constitution|safety|scaling|asl-3|espionage|distillation|watermark|directive|golden gate|hardware standard|institute|academy|ipo|s-1|usage limits|redeployed|novel enzyme'),
    'openai': dict(page='pages/openai-platform-rings.html', anchor='<div class="cr-more">', start='2021-10',
        layers=[('Layer 0 · Models', '#0b3d2e', r'^gpt|^o\d|instructgpt|dall|whisper|sora( preview| video| 2)|images 2|gpt-oss'),
                ('Layer 1 · Developer platform', '#10a37f', r'api|devday|ultrafast|price cut'),
                ('Layer 2 · Tools', '#2f6b45', r'plugins|image generation|realtime'),
                ('Layer 3 · Agent stack', '#2b5a9e', r'agents sdk|agentkit|codex|operator|deep research|commerce'),
                ('Layer 4 · Products', '#b4532a', r'chatgpt|gpt store|atlas|sora app|wallet|dots|pulse|group chats')],
        skip=r'board|stargate|hallucinate|safety tests'),
    'google': dict(page='pages/google-platform-rings.html', anchor='<div class="cr-more">', start='2021-11',
        layers=[('Layer 0 · Models', '#0b2a5b', r'gemini|gemma|palm|imagen|veo|nano banana|genie|gopher|chinchilla'),
                ('Layer 1 · Developer platform', '#4285f4', r'generally available|embeddinggemma'),
                ('Layer 2 · Tools', '#0f9d58', r'xx-no-match'),
                ('Layer 3 · Agent stack', '#1f2937', r'cli|jules|antigravity|astra'),
                ('Layer 4 · Products', '#b4532a', r'bard|flow|alpha|gold|icpc|robotics')],
        skip=r'deepmind formed|institute|gato'),
}
PRIO = {'anthropic': [3, 4, 2, 1, 0], 'openai': [3, 2, 1, 4, 0], 'google': [3, 1, 4, 0, 2]}  # check specific layers first

CSS = ('.rtl{margin-top:22px;background:#fff;border:1px solid #e7e5e4;border-radius:14px;padding:18px 20px}.rtl h2{margin:0 0 4px;font-size:1.35rem}'
       '.rtl>p{margin:0 0 12px;color:#57534e;line-height:1.5}.rtl-row{margin:14px 0 4px}.rtl-row h3{margin:0 0 4px;font-size:1rem;color:var(--c)}'
       '.rtl-row h3 small{color:#78716c;font-weight:600}.rtl-tr{position:relative;height:34px;border-bottom:2px solid #e7e5e4;margin:0 8px}'
       '.rtl-y{position:absolute;bottom:-20px;font-size:.72rem;color:#a8a29e;transform:translateX(-50%)}.rtl-y:before{content:"";position:absolute;left:50%;top:-14px;height:8px;border-left:1px solid #d6d3d1}'
       '.rtl-d{position:absolute;bottom:-7px;width:12px;height:12px;margin-left:-6px;border-radius:50%;background:var(--c);border:2px solid #fff;box-shadow:0 0 0 1px var(--c);cursor:pointer;padding:0;animation:rtlIn .5s both}'
       '.rtl-d.f{width:16px;height:16px;margin-left:-8px;bottom:-9px}.rtl-d:hover,.rtl-d.on{transform:scale(1.4)}'
       '@keyframes rtlIn{from{opacity:0;transform:translateY(-14px)}}@media (prefers-reduced-motion:reduce){.rtl-d{animation:none}}'
       '.rtl-ch{display:flex;gap:6px;overflow-x:auto;padding:26px 2px 6px}.rtl-ch button{flex:0 0 auto;border:1px solid #e7e5e4;border-left:3px solid var(--c);background:#fafaf9;border-radius:8px;padding:4px 8px;font-size:.78rem;cursor:pointer;text-align:left}'
       '.rtl-ch button b{display:block;color:#78716c;font-size:.7rem}.rtl-ch button.on{background:#fff7ed}'
       '.rtl-info{margin-top:12px;border-left:4px solid #f59e0b;background:#fffbeb;border-radius:8px;padding:10px 12px;line-height:1.5;min-height:2em}'
       'body.cr-embed .rtl{display:none}')


def mo(d):
    y, m = int(d[:4]), int(d[5:7])
    return y * 12 + m - 1


def build(lab):
    C = PAGES[lab]
    items = sorted([x for x in json.load(open('data/lab-updates.json'))['items'] if x['lab'] == lab], key=lambda x: x['date'])
    rows = [[] for _ in C['layers']]
    for x in items:
        t = x['title'].lower()
        if re.search(C['skip'], t):
            continue
        for i in PRIO[lab]:
            if re.search(C['layers'][i][2], t):
                rows[i].append(x)
                break
    t0, t1 = mo(C['start'] + '-01'), mo('2026-12-01')
    pos = lambda d: round((mo(d if len(d) > 7 else d + '-01') - t0) / (t1 - t0) * 100, 2)
    out = ['<!-- RINGTL:START -->', '<style>' + CSS + '</style>', '<div class="rtl" id="rtl"><h2>Each layer over time</h2>',
           '<p>When each ring gained its pieces, from the announcements this site tracks (Frontier Lab Updates). Big dots are flagship releases. Tap a dot or a chip for the summary and source. Which ring an announcement belongs to is our grouping; company, funding and safety news are left out (they are on the full timeline).</p>']
    years = range(int(C['start'][:4]) + (1 if C['start'][5:] != '01' else 0), 2027)
    k = 0
    for i, (name, col, _) in enumerate(C['layers']):
        out.append('<div class="rtl-row" style="--c:%s"><h3>%s <small>· %d</small></h3><div class="rtl-tr">' % (col, name, len(rows[i])))
        out += ['<span class="rtl-y" style="left:%s%%">%d</span>' % (pos('%d-01' % y), y) for y in years]
        for j, x in enumerate(rows[i]):
            out.append('<button class="rtl-d%s" style="left:%s%%;animation-delay:%.2fs" data-k="%d" title="%s · %s" aria-label="%s"></button>' % (
                ' f' if x.get('flagship') else '', pos(x['date']), j * .06, k + j, x['date'], html.escape(x['title']), html.escape(x['title'])))
        out.append('</div><div class="rtl-ch">')
        for j, x in enumerate(rows[i]):
            out.append('<button data-k="%d"><b>%s</b>%s</button>' % (k + j, x['date'], html.escape(x['title'])))
        out.append('</div></div>')
        k += len(rows[i])
    data = [[x['date'], x['title'], x.get('summary', ''), x.get('source', '')] for r in rows for x in r]
    out.append('<div class="rtl-info" id="rtlInfo">Tap any dot or chip.</div></div>')
    out.append('<script>(function(){var D=' + json.dumps(data, ensure_ascii=False) + ',box=document.getElementById("rtl"),inf=document.getElementById("rtlInfo");'
               'box.addEventListener("click",function(e){var b=e.target.closest("[data-k]");if(!b)return;var k=b.getAttribute("data-k"),x=D[k];'
               'box.querySelectorAll(".on").forEach(function(o){o.classList.remove("on")});box.querySelectorAll(\'[data-k="\'+k+\'"]\').forEach(function(o){o.classList.add("on")});'
               'inf.innerHTML="<b>"+x[0]+" · "+x[1]+"</b><br>"+x[2]+(x[3]?\' <a hr\'+\'ef="\'+x[3]+\'" target="_blank" rel="noopener">Source →</a>\':"")});})();</script>')
    out.append('<!-- RINGTL:END -->')
    blk = '\n'.join(out) + '\n'
    s = open(C['page']).read()
    if '<!-- RINGTL:START -->' in s:
        s = re.sub(r'<!-- RINGTL:START -->.*?<!-- RINGTL:END -->\n', lambda m: blk, s, flags=re.S)
    else:
        assert s.count(C['anchor']) == 1
        s = s.replace(C['anchor'], blk + C['anchor'])
    open(C['page'], 'w').write(s)
    print(C['page'], [len(r) for r in rows])


if __name__ == '__main__':
    for lab in PAGES:
        build(lab)
