import re
R = '/home/user/Claude_Project_3_LLM/'
src = open(R + 'pages/computer-use-loop.html').read()
head = src[:src.index('<style>')].replace('Computer Use, Step by Step', 'Multi-Agent Patterns, Side by Side')
head = re.sub(r'<!-- SEO:START.*?SEO:END -->\n?', '', head, flags=re.S)
nav = src[src.index('</style>') + len('</style>'):src.index('<main')]
CSS = '''<style>
.ma{max-width:1180px;margin:0 auto;padding:18px 16px 30px}
.ma-hero{background:linear-gradient(135deg,#0f172a,#7c3aed 45%,#be123c);color:#fff;border-radius:16px;padding:22px}.ma-hero h1{margin:0 0 6px;font-size:1.7rem}.ma-hero p{margin:0;color:#f5f3ff;line-height:1.55}
.ma-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0}.ma-tabs button{border:2px solid var(--c);background:#fff;color:var(--c);border-radius:999px;padding:5px 12px;font-weight:800;cursor:pointer;font-size:.83rem}.ma-tabs button.on{background:var(--c);color:#fff}
.ma-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0}.ma-bar button,.ma-bar label{border:1px solid #cbd5e1;background:#fff;border-radius:999px;padding:6px 12px;font-weight:700;cursor:pointer;font-size:.85rem}.ma-bar label{display:inline-flex;gap:6px;align-items:center}
.ma-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:12px}
.ma-wrap{background:#fff;border:1px solid #e2e8f0;border-radius:14px}#maSvg{display:block;width:100%;height:auto;font-family:Arial,Helvetica,sans-serif}
.ma-side{display:grid;gap:10px;align-content:start}
.ma-kpi{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.ma-kpi div{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;font-size:.8rem;color:#475569}.ma-kpi b{display:block;font-size:1.15rem;color:#0f172a}
.ma-card{background:#fff;border:1px solid #e2e8f0;border-left:5px solid var(--c,#7c3aed);border-radius:12px;padding:12px;font-size:.9rem;line-height:1.5}.ma-card h3{margin:0 0 4px;font-size:1rem}
.ma-log{white-space:pre-wrap;font:12px/1.5 ui-monospace,Menlo,monospace;background:#0f172a;color:#e2e8f0;border-radius:10px;padding:10px;min-height:120px;max-height:200px;overflow:auto}
.ma-cmp{width:100%;border-collapse:collapse;font-size:.84rem;margin-top:12px}.ma-cmp th,.ma-cmp td{border-bottom:1px solid #e2e8f0;padding:6px;text-align:left}.ma-cmp tr.on{background:#f5f3ff;font-weight:700}
.ma-more{margin-top:14px;color:#334155;font-size:.88rem;line-height:1.6}
.ma-n rect{transition:filter .2s}.ma-n.hot rect{filter:drop-shadow(0 0 6px var(--c))}.ma-n.bad rect{stroke:#dc2626!important;stroke-width:3}
body.ma-embed .navbar,body.ma-embed .nav-panel-wrap,body.ma-embed .nav-backdrop,body.ma-embed .ma-hero,body.ma-embed .ma-more,body.ma-embed .to-top{display:none!important}body.ma-embed main{padding-top:0!important}
@media (max-width:860px){.ma-grid{grid-template-columns:1fr}}
</style>'''
BODY = '''<main style="padding-top: 94px;">
<div class="ma">
  <div class="ma-hero"><h1>Multi-Agent Patterns, Side by Side</h1><p class="intro">The same task, “compare our refund policy with three competitors and draft an update”, run through seven ways of arranging agents. Pick a pattern and press run: messages move between agents, and the counters show model calls, waiting time and tokens. Then make one agent get it wrong and see which patterns catch it.</p></div>
  <div class="ma-tabs" id="maTabs"></div>
  <div class="ma-bar"><button id="maRun">▶ Run the task</button><label><input type="checkbox" id="maBad"> One agent gets a fact wrong</label></div>
  <div class="ma-grid"><div class="ma-wrap"><svg id="maSvg" viewBox="0 0 640 420" role="img" aria-label="Agents and messages for the selected pattern"></svg></div>
  <div class="ma-side"><div class="ma-kpi"><div>Model calls<b id="kC">0</b></div><div>Waiting time (steps)<b id="kT">0</b></div><div>Tokens (rough)<b id="kK">0</b></div><div>Wrong fact reached the answer?<b id="kE">—</b></div></div>
  <div class="ma-card" id="maCard"></div><div class="ma-log" id="maLog"></div></div></div>
  <table class="ma-cmp" id="maCmp"></table>
  <div class="ma-more"><p>A teaching simulation: call counts, step times and tokens are our illustrative estimates for this one task, not measurements. Patterns follow Anthropic’s “Building effective agents”, the OpenAI Agents SDK orchestration docs and LangGraph’s supervisor and swarm libraries. Read the series: <a href="../blog/multi-agent-map.html">Part 1</a> · <a href="../blog/multi-agent-supervisor-handoff.html">supervisors and hand-offs</a> · <a href="../blog/multi-agent-parallel-debate.html">parallel, voting, debate</a> · <a href="../blog/multi-agent-failures-cost.html">failures and cost</a>.</p><p>Disclosure: Claude, made by Anthropic, helps write this site; the series cites Anthropic, OpenAI (a competitor), LangChain, CrewAI and Microsoft (an Anthropic investor).</p></div>
</div>
</main>
<script src="../app.js"></script>
<script>
(function(){
var embed=/[?&]embed=1/.test(location.search);if(embed)document.body.classList.add('ma-embed');
var g=function(i){return document.getElementById(i)},svg=g('maSvg'),run=0;
// node: [id,label,x,y]; steps: [from,to,label,parallelGroup]; catch: does the pattern catch a wrong fact?
var P={
single:{n:'One agent',c:'#475569',nodes:[['u','User',90,210],['a','Agent',330,210],['w','Web + docs',560,210]],steps:[['u','a','task'],['a','w','search A'],['w','a','page A'],['a','w','search B'],['w','a','page B'],['a','w','search C'],['w','a','page C'],['a','a','compare + draft'],['a','u','draft']],calls:25,time:9,tok:90,bad:'a',catch:0,text:'One agent does everything in one window. Simple and cheap to build, but the window fills with three competitors’ pages and the work runs one step after another.'},
chain:{n:'Chain',c:'#334155',nodes:[['u','User',60,210],['r','Researcher',190,110],['m','Comparer',330,210],['d','Drafter',470,110],['k','Checker',590,210]],steps:[['u','r','task'],['r','m','findings'],['m','d','comparison'],['d','k','draft'],['k','u','checked draft']],calls:28,time:5,tok:85,bad:'r',catch:1,text:'Fixed steps in code with a gate at the end. Easy to test each step; the checker can catch a wrong fact, but every step waits for the previous one.'},
router:{n:'Router',c:'#2563eb',nodes:[['u','User',80,210],['ro','Router',240,210],['p','Policy agent',450,110],['b','Billing agent',450,310]],steps:[['u','ro','task'],['ro','p','route: policy'],['p','p','research + draft'],['p','u','draft']],calls:24,time:4,tok:80,bad:'p',catch:0,text:'Classifies once and sends the whole job to one specialist. Great for mixed traffic; for this single research task it adds little.'},
supervisor:{n:'Supervisor + parallel workers',c:'#7c3aed',nodes:[['u','User',70,210],['s','Supervisor',230,210],['w1','Worker A',430,90],['w2','Worker B',430,210],['w3','Worker C',430,330],['k','Synthesis',200,360]],steps:[['u','s','task'],['s','w1','brief A',1],['s','w2','brief B',1],['s','w3','brief C',1],['w1','s','summary A',2],['w2','s','summary B',2],['w3','s','summary C',2],['s','k','combine + check'],['k','u','draft']],calls:40,time:5,tok:160,bad:'w2',catch:1,text:'The supervisor writes three briefs, workers research in parallel in clean windows and return short summaries; the supervisor owns the answer and can cross-check sources. Faster here, but more tokens in total.'},
handoff:{n:'Hand-offs',c:'#be123c',nodes:[['u','User',80,210],['t','Triage',240,110],['r','Researcher',420,110],['a','Analyst',420,310],['w','Writer',240,310]],steps:[['u','t','task'],['t','r','hand off'],['r','a','hand off'],['a','w','hand off'],['w','u','draft']],calls:35,time:5,tok:120,bad:'r',catch:0,text:'Control passes along; whoever is active talks to the user. Focused prompts, but if the researcher hands on a wrong fact, nobody downstream is set up to check it, and the user’s constraints can get lost between hops.'},
evaluator:{n:'Evaluator loop',c:'#d97706',nodes:[['u','User',80,210],['g','Writer',300,120],['e','Critic',300,300],['w','Web + docs',540,120]],steps:[['u','g','task'],['g','w','research'],['w','g','pages'],['g','e','draft 1'],['e','g','feedback: cite sources'],['g','e','draft 2'],['e','u','passes']],calls:32,time:7,tok:110,bad:'g',catch:1,text:'A critic reviews against explicit criteria and sends feedback until the draft passes. Good for quality; with a sourcing rule in its criteria it catches the unsupported fact.'},
debate:{n:'Debate',c:'#0891b2',nodes:[['u','User',80,210],['a','Agent A',300,100],['b','Agent B',300,320],['j','Judge',520,210]],steps:[['u','a','task',1],['u','b','task',1],['a','b','round 1',2],['b','a','rebuttal',2],['a','b','round 2',3],['b','a','agree?',3],['a','j','final A',4],['b','j','final B',4],['j','u','decision']],calls:44,time:6,tok:170,bad:'a',catch:1,text:'Two agents argue over rounds and a judge decides. Can catch a reasoning or factual error when the other agent challenges it; costs the most here.'}};
var ORD=['single','chain','router','supervisor','handoff','evaluator','debate'],cur='supervisor';
g('maTabs').innerHTML=ORD.map(function(k){return '<button data-k="'+k+'" style="--c:'+P[k].c+'">'+P[k].n+'</button>'}).join('');
g('maCmp').innerHTML='<tr><th>Pattern</th><th>Model calls</th><th>Waiting (steps)</th><th>Tokens (rough, k)</th><th>Catches a wrong fact?</th></tr>'+ORD.map(function(k){var p=P[k];return '<tr data-k="'+k+'"><td>'+p.n+'</td><td>'+p.calls+'</td><td>'+p.time+'</td><td>'+p.tok+'</td><td>'+(p.catch?'✅ likely':'❌ unlikely')+'</td></tr>'}).join('');
function pos(p,id){for(var i=0;i<p.nodes.length;i++)if(p.nodes[i][0]===id)return p.nodes[i];}
function draw(){var p=P[cur],s='<defs><marker id="mh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/></marker></defs>';
 p.steps.forEach(function(st){if(st[0]===st[1])return;var a=pos(p,st[0]),b=pos(p,st[1]),dx=b[2]-a[2],dy=b[3]-a[3],L=Math.hypot(dx,dy)||1,ex=Math.min(Math.abs((b[1].length*7.5+30)/2/(dx/L||1e-9)),Math.abs(24/(dy/L||1e-9))),sx=Math.min(Math.abs((a[1].length*7.5+30)/2/(dx/L||1e-9)),Math.abs(24/(dy/L||1e-9)));s+='<line x1="'+(a[2]+dx/L*sx)+'" y1="'+(a[3]+dy/L*sx)+'" x2="'+(b[2]-dx/L*(ex+3))+'" y2="'+(b[3]-dy/L*(ex+3))+'" stroke="#94a3b8" stroke-width="2" marker-end="url(#mh)"/>';});
 p.nodes.forEach(function(n){var w=n[1].length*7.5+30;s+='<g class="ma-n" id="n-'+n[0]+'" style="--c:'+p.c+'"><rect x="'+(n[2]-w/2)+'" y="'+(n[3]-22)+'" width="'+w+'" height="44" rx="10" fill="'+(n[0]==='u'?'#f1f5f9':p.c+'18')+'" stroke="'+(n[0]==='u'?'#475569':p.c)+'" stroke-width="2"/><text x="'+n[2]+'" y="'+(n[3]+5)+'" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">'+n[1]+'</text></g>';});
 s+='<g id="dots"></g>';svg.innerHTML=s;
 document.querySelectorAll('.ma-tabs button').forEach(function(b){b.classList.toggle('on',b.dataset.k===cur)});
 document.querySelectorAll('#maCmp tr').forEach(function(r){r.classList.toggle('on',r.dataset.k===cur)});
 var cd=g('maCard');cd.style.setProperty('--c',p.c);cd.innerHTML='<h3>'+p.n+'</h3>'+p.text;
 g('kC').textContent='0';g('kT').textContent='0';g('kK').textContent='0';g('kE').textContent='—';g('maLog').textContent='Press ▶ Run the task.';}
function play(){var me=++run,p=P[cur],bad=g('maBad').checked,log=g('maLog'),dots=document.getElementById('dots');log.textContent='';draw();log.textContent='';
 var groups=[],i=0;while(i<p.steps.length){var grp=p.steps[i][3];if(grp){var gs=[];while(i<p.steps.length&&p.steps[i][3]===grp)gs.push(p.steps[i++]);groups.push(gs);}else groups.push([p.steps[i++]]);}
 var k=0,t=0,calls=0;(function nx(){if(me!==run)return;if(k>=groups.length){g('kC').textContent=p.calls;g('kK').textContent=p.tok+'k';g('kE').textContent=bad?(p.catch?'No: caught':'Yes ⚠️'):'—';log.textContent+=(bad?(p.catch?'✓ the wrong fact was caught before the answer.\\n':'⚠️ the wrong fact reached the user.\\n'):'✓ done.\\n');return;}
  var grp=groups[k++];t++;g('kT').textContent=t;
  grp.forEach(function(st){calls+=Math.round(p.calls/p.steps.length);g('kC').textContent=calls;var a=pos(p,st[0]),b=pos(p,st[1]),isBad=bad&&st[0]===p.bad&&st[1]!==st[0];
   log.textContent+=(grp.length>1?'∥ ':'')+a[1]+' → '+b[1]+': '+st[2]+(isBad?'  (contains a wrong fact)':'')+'\\n';log.scrollTop=1e5;
   var nb=document.getElementById('n-'+st[1]);if(nb){nb.classList.add('hot');setTimeout(function(){nb.classList.remove('hot')},700);}
   if(isBad){var na=document.getElementById('n-'+st[0]);if(na)na.classList.add('bad');}
   if(st[0]!==st[1]){var c=document.createElementNS('http://www.w3.org/2000/svg','circle');c.setAttribute('r',7);c.setAttribute('fill',isBad?'#dc2626':p.c);dots.appendChild(c);var t0=performance.now();(function mv(now){var f=Math.min(1,(now-t0)/650);c.setAttribute('cx',a[2]+(b[2]-a[2])*f);c.setAttribute('cy',a[3]+(b[3]-a[3])*f);if(f<1)requestAnimationFrame(mv);else c.remove();})(t0);}});
  setTimeout(nx,matchMedia('(prefers-reduced-motion: reduce)').matches?50:800);})();}
document.querySelectorAll('.ma-tabs button').forEach(function(b){b.onclick=function(){cur=b.dataset.k;run++;draw();};});
document.querySelectorAll('#maCmp tr[data-k]').forEach(function(r){r.style.cursor='pointer';r.onclick=function(){cur=r.dataset.k;run++;draw();};});
g('maRun').onclick=play;g('maBad').onchange=function(){run++;draw();};draw();
function tell(){if(embed&&parent!==window)parent.postMessage({maHeight:Math.ceil(document.querySelector('.ma').getBoundingClientRect().bottom+8)},'*');}
addEventListener('resize',tell);setTimeout(tell,400);document.addEventListener('click',function(){setTimeout(tell,60);});
})();
</script>
</body>
</html>
'''
open(R + 'pages/multi-agent-patterns.html', 'w').write(head + CSS + nav + BODY)
