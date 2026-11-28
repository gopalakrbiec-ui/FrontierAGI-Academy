import html, re, sys, subprocess
R = '/home/user/Claude_Project_3_LLM/'
S = '/tmp/claude-0/-home-user-Claude-Project-3-LLM/b946cee3-962e-52f7-8e92-b1e88a2e2e94/scratchpad/ce/'
E = html.escape
PARTS = [
 ('context-eng-map', 'Context Engineering, Explained: What Goes in an Agent’s Window', '🪟'),
 ('context-eng-what-goes-in', 'What Goes In and What Stays Out: Prompts, Tools, Retrieval and Skills', '🧺'),
 ('context-eng-long-tasks', 'Long Tasks Without Losing the Plot: Compaction, Notes and Sub-Agents', '🧵'),
 ('context-eng-caching-evals', 'Context Costs Money: Caching, Ordering and Measuring What Works', '💸'),
]
n = int(sys.argv[1]); slug, title, emoji = PARTS[n - 1]
T = open(R + 'blog/computer-use-labs.html').read()
head = T[:T.index('<!-- NAV:END -->') + len('<!-- NAV:END -->')]
head = re.sub(r'<title>.*?</title>', '<title>' + E(title) + ' — FrontierAGI Academy</title>', head, 1)
head = re.sub(r'<!-- SEO:START -->.*?<!-- SEO:END -->\n?', '', head, 1, flags=re.S)
tail_css = T[T.index('</main>') + 7:T.index('<script src="../app.js')]
tail_css = tail_css.replace('linear-gradient(135deg,#0f172a,#7c3aed 50%,#d97706)', 'linear-gradient(135deg,#0f172a,#0d9488 50%,#d97706)')

def fig(f, alt, cap): return f'<figure class="bp-fig"><a href="../assets/diagrams/context-eng/{f}" target="_blank" rel="noopener"><img src="../assets/diagrams/context-eng/{f}" alt="{E(alt)}" loading="lazy"></a><figcaption>{cap} <span class="bp-zoom">Tap to open full size.</span></figcaption></figure>'
def pts(*items):
    s = '<ul class="mo-pts">'
    for it in items:
        if isinstance(it, tuple): s += '<li>' + it[0] + '<ul>' + ''.join('<li>' + x + '</li>' for x in it[1]) + '</ul></li>'
        else: s += '<li>' + it + '</li>'
    return s + '</ul>'
def tbl(hd, rows): return '<div class="wr-scroll"><table class="as-cmp"><tr>' + ''.join('<th>' + h + '</th>' for h in hd) + '</tr>' + ''.join('<tr>' + ''.join('<td>' + c + '</td>' for c in r) + '</tr>' for r in rows) + '</table></div>'
def box(label, body, kind='wr-box'): return f'<div class="{kind}"><b class="l">{label}</b>{body}</div>'
def A(u, t): return f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
def CODE(h, t, note='example, not executed'): return f'<div class="mo-code"><div class="h"><span>{h}</span><span>{note}</span></div><pre>{E(t)}</pre></div>'
def RUN(slug_, f):
    p = R + f'data/code/{slug_}/{f}'
    src = open(p).read(); out = subprocess.run(['python3', '-I', p], capture_output=True, text=True).stdout
    return f'<div class="mo-code"><div class="h"><span>$ python3 {f}</span><span>data/code/{slug_}/{f}</span></div><pre>{E(src)}</pre></div><div class="mo-out">$ python3 {f}\n{E(out)}</div>'
SEC = []
def sec(i, t, body): SEC.append((i, t, body))
MAP = '<p class="sf-map"><b>🗺️ Explore it:</b> <a href="../pages/context-window-live.html">The Context Window, Live</a> fills a window step by step during one agent task and lets you switch on compaction, result clearing, sub-agents, skills and caching to see what each saves.</p>'
def SER(here):
    rows = ''.join(('<li class="here">' if i + 1 == here else '<li>') + f'<span>{p[2]} Part {i+1}</span> ' + (f'<b>{E(p[1])}</b> (you are here)' if i + 1 == here else f'<a href="{p[0]}.html">{E(p[1])}</a>') + '</li>' for i, p in enumerate(PARTS))
    return f'<div class="wr-box sf-ser"><b class="l">🪟 Context Engineering · 4 parts</b><ol>{rows}</ol><p>Map: <a href="../pages/context-window-live.html">The Context Window, Live</a>. Related on this site: <a href="adlc-code-context.html">ADLC Part 5: code becomes context</a>, <a href="agent-memory-state.html">agent memory and state</a>, <a href="../pages/agent-memory.html">How AI Agents Remember</a>, <a href="agentic-claude-code.html">Claude Code, taken apart</a>.</p></div>'
DISC = '<b>Disclosure:</b> Claude, made by Anthropic, helps write this site. Many examples here come from Anthropic’s own posts and docs, because they publish the most detail on this topic; we mark where other labs and frameworks differ.'
exec(open(S + f'p{n}.py').read())
import os
if os.path.exists(S + f'x{n}.py'): exec(open(S + f'x{n}.py').read())
SEC.sort(key=lambda x: {'checklist': 1, 'next': 1, 'sources': 2}.get(x[0], 0))
nav = '<div class="wr-section-nav">' + ''.join(f'<a href="#{i}">{E(t)}</a>' for i, t, _ in SEC) + '</div>'
body = ''.join(f'<h2 id="{i}" class="wr-sec">{k+1}. {E(t)}</h2>\n{b}\n' for k, (i, t, b) in enumerate(SEC))
words = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<pre>.*?</pre>', '', body, flags=re.S)).split())
main = f'''
<main style="padding-top: 94px;">
  <div class="blog-post-wrap">
    <div class="blog-breadcrumb"><a href="../index.html">Home</a><span>›</span><a href="../pages/blog.html">Blog</a><span>›</span><span>Context Engineering</span></div>
    <div class="wr-hero cs-hero as-hero sf-hero">
      <span class="wr-badge">Context Engineering · Part {n} of 4</span>
      <h1>{E(title)}</h1>
      <p>{HERO}</p>
    </div>
    <div class="blog-meta-row">
      <div class="blog-author-chip"><div class="blog-author-avatar">FL</div><div><div class="blog-author-name">FrontierAGI Team</div><div class="blog-post-date">November 28, 2026 · {max(1, round(words/230))} min read</div></div></div>
    </div>
    <div class="wr-box wr-caveat"><b class="l">⚠️ How to read this (as of 28 Nov 2026)</b>{CAV} Figures marked ⚠️ come from vendors, press or secondary reports; “our reading” marks judgement; simulations and calculators are our own simple models with example inputs. {DISC}</div>
    {nav}
{body}
{SER(n)}
</main>{tail_css}<script src="../app.js"></script>
{JS}
</body>
</html>
'''
open(R + 'blog/' + slug + '.html', 'w').write(head + main)
print(slug, 'words', words)
