#!/usr/bin/env python3
"""Add the "Each wave over time" block to pages/agentic-framework.html (<!-- WAVETL --> markers).

Milestones are well-known public dates; the last two waves are our prediction, so they show
"signals so far" instead. Run build.py afterwards.
"""
import html, json, re

W = [
    ('AI & machine learning', '#64748b', '1950 onwards', [
        ('1950', 'Turing asks “Can machines think?”', 'Alan Turing’s paper “Computing Machinery and Intelligence” proposes the imitation game.'),
        ('1956', 'Dartmouth workshop names “artificial intelligence”', 'The summer workshop proposed by McCarthy, Minsky, Rochester and Shannon.'),
        ('1958', 'The perceptron', 'Frank Rosenblatt’s learning machine, the ancestor of today’s neural networks.'),
        ('1986', 'Backpropagation popularised', 'Rumelhart, Hinton and Williams show how to train multi-layer networks.'),
        ('1997', 'Deep Blue beats Kasparov', 'IBM’s chess computer wins a match against the world champion.'),
        ('2001', 'Random forests', 'Leo Breiman’s ensemble method, a workhorse of classical machine learning.')]),
    ('Deep learning', '#2563eb', '2006 onwards', [
        ('2006', 'Deep belief nets', 'Hinton, Osindero and Teh show deep networks can be trained layer by layer.'),
        ('2012', 'AlexNet wins ImageNet', 'A GPU-trained convolutional network cuts the image-recognition error sharply.'),
        ('2014', 'GANs', 'Goodfellow et al. introduce generative adversarial networks.'),
        ('2015', 'ResNet', 'Residual connections make networks with 100+ layers trainable.'),
        ('2016', 'AlphaGo beats Lee Sedol', 'DeepMind’s system wins at Go, 4 games to 1.'),
        ('2017', 'The Transformer', '“Attention Is All You Need” introduces the architecture behind today’s LLMs.')]),
    ('Generative AI', '#7c3aed', '2018 onwards', [
        ('2018', 'GPT-1 and BERT', 'Pre-train on lots of text, then adapt: the recipe for language models.'),
        ('2020', 'GPT-3', 'A 175B-parameter model shows few-shot learning from the prompt alone.'),
        ('2021', 'DALL·E', 'Images generated from text descriptions.'),
        ('2022', 'Stable Diffusion', 'An open-weight image model anyone can run.'),
        ('2022-11', 'ChatGPT', 'A chat interface brings LLMs to the public.'),
        ('2023-03', 'GPT-4 and Claude', 'Stronger multimodal and chat models reach developers and users.')]),
    ('AI agents', '#0d9488', '2022 onwards', [
        ('2022-10', 'ReAct', 'A paper showing models can interleave reasoning with actions such as search.'),
        ('2023-03', 'ChatGPT plugins and Auto-GPT', 'Models start calling tools; open-source autonomous loops go viral.'),
        ('2023-06', 'Function calling in the API', 'Structured tool calls become a standard API feature.'),
        ('2024-10', 'Computer use', 'Anthropic lets Claude operate a desktop through screenshots, mouse and keyboard.'),
        ('2025-01', 'Operator', 'OpenAI’s browser-using agent.')]),
    ('Agentic AI', '#ea580c', '2024 onwards', [
        ('2024-11', 'Model Context Protocol', 'An open protocol (introduced by Anthropic) for connecting agents to tools and data.'),
        ('2025-02', 'Claude Code', 'An agentic coding tool that works across a whole repository.'),
        ('2025-03', 'OpenAI Agents SDK', 'A framework for multi-agent workflows with handoffs and guardrails.'),
        ('2025-04', 'Agent2Agent (A2A)', 'Google’s protocol for agents talking to other agents.'),
        ('2025-05', 'Codex cloud agent', 'Coding tasks run in parallel in cloud sandboxes.'),
        ('2025-12', 'Agentic AI Foundation', 'MCP moves to a neutral foundation.')]),
    ('Next wave? (our prediction)', '#7c3aed', 'signals so far · our guess: late 2020s', [
        ('2025-09', 'Agentic Commerce Protocol', 'Agents that can pay: checkout inside ChatGPT. A signal for agent economies.'),
        ('2025-10', 'Agent Skills', 'Packaged know-how agents load on demand. A signal for agents learning on the job.'),
        ('2026-09', 'Always-on agents (Dots)', 'Agents that keep running in the background for a person. A signal for agent organisations.')]),
    ('AGI? (our prediction)', '#be185d', 'signals so far · no date', [
        ('2024-12', 'o3 on ARC-AGI-1', 'A reasoning model scores highly on a test built to resist memorisation.'),
        ('2025-03', 'METR time horizons', 'METR measures the length of tasks agents can finish, doubling roughly every seven months.'),
        ('2025-07', 'IMO gold-level maths', 'OpenAI and Google DeepMind models reach gold-medal level on Olympiad problems.')]),
]
CSS = ('.wtl{margin-top:22px;background:#fff;border:1px solid #e7e5e4;border-radius:14px;padding:18px 20px}.wtl h2{margin:0 0 4px;font-size:1.35rem}.wtl>p{margin:0 0 8px;color:#57534e;line-height:1.5}'
       '.wtl-row{margin:14px 0 0}.wtl-row h3{margin:0;font-size:1rem;color:var(--c)}.wtl-row h3 small{color:#78716c;font-weight:600}'
       '.wtl-ch{display:flex;gap:0;overflow-x:auto;padding:8px 2px 6px;align-items:stretch}.wtl-ch button{flex:0 0 auto;position:relative;border:1px solid #e7e5e4;border-top:3px solid var(--c);background:#fafaf9;border-radius:8px;padding:6px 9px;font-size:.8rem;cursor:pointer;text-align:left;max-width:200px;margin-right:18px;animation:wtlIn .5s both}'
       '.wtl-ch button:not(:last-child):after{content:"→";position:absolute;right:-15px;top:40%;color:var(--c);font-weight:700}'
       '.wtl-ch button b{display:block;color:var(--c);font-size:.75rem}.wtl-ch button.on{background:#fff7ed}.wtl-row.p button{border-style:dashed;border-top-style:dashed}'
       '@keyframes wtlIn{from{opacity:0;transform:translateX(-10px)}}@media (prefers-reduced-motion:reduce){.wtl-ch button{animation:none}}'
       '.wtl-info{margin-top:12px;border-left:4px solid #f59e0b;background:#fffbeb;border-radius:8px;padding:10px 12px;line-height:1.5}body.af-embed .wtl{display:none}')

out = ['<!-- WAVETL:START -->', '<style>' + CSS + '</style>', '<div class="wtl" id="wtl"><h2>Each wave over time</h2>',
       '<p>A few landmark moments for each circle, oldest first. Dates are public release or publication dates; the picks are ours. The last two waves have not happened, so they show signals we read as early hints: our reading, not a forecast with dates.</p>']
D, k = [], 0
for name, col, sub, ms in W:
    out.append('<div class="wtl-row%s" style="--c:%s"><h3>%s <small>· %s</small></h3><div class="wtl-ch">' % (' p' if '?' in name else '', col, name, sub))
    for j, (d, t, info) in enumerate(ms):
        out.append('<button data-k="%d" style="animation-delay:%.2fs"><b>%s</b>%s</button>' % (k, j * .08, d, html.escape(t)))
        D.append([d, t, info]); k += 1
    out.append('</div></div>')
out.append('<div class="wtl-info" id="wtlInfo">Tap a moment for a one-line explanation.</div></div>')
out.append('<script>(function(){var D=' + json.dumps(D, ensure_ascii=False) + ',b=document.getElementById("wtl"),i=document.getElementById("wtlInfo");'
           'b.addEventListener("click",function(e){var x=e.target.closest("[data-k]");if(!x)return;b.querySelectorAll(".on").forEach(function(o){o.classList.remove("on")});x.classList.add("on");'
           'var d=D[x.getAttribute("data-k")];i.innerHTML="<b>"+d[0]+" · "+d[1]+"</b><br>"+d[2]});})();</script>')
out.append('<!-- WAVETL:END -->')
blk = '\n'.join(out) + '\n'
p = 'pages/agentic-framework.html'
s = open(p).read()
if '<!-- WAVETL:START -->' in s:
    s = re.sub(r'<!-- WAVETL:START -->.*?<!-- WAVETL:END -->\n', lambda m: blk, s, flags=re.S)
else:
    a = '  <div class="af-more">'
    assert s.count(a) == 1
    s = s.replace(a, blk + a)
open(p, 'w').write(s)
print(k, 'milestones')
