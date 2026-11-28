import re
R = '/home/user/Claude_Project_3_LLM/'
src = open(R + 'pages/computer-use-loop.html').read()
head = src[:src.index('<style>')].replace('Computer Use, Step by Step', 'The Context Window, Live')
head = re.sub(r'<!-- SEO:START.*?SEO:END -->\n?', '', head, flags=re.S)
nav = src[src.index('</style>') + len('</style>'):src.index('<main')]
CSS = '''<style>
.cw{max-width:1180px;margin:0 auto;padding:18px 16px 30px}
.cw-hero{background:linear-gradient(135deg,#0f172a,#0d9488 50%,#d97706);color:#fff;border-radius:16px;padding:22px}.cw-hero h1{margin:0 0 6px;font-size:1.7rem}.cw-hero p{margin:0;color:#f0fdfa;line-height:1.55}
.cw-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:12px 0}.cw-bar button,.cw-bar label{border:1px solid #cbd5e1;background:#fff;border-radius:999px;padding:6px 12px;font-weight:700;cursor:pointer;font-size:.85rem}.cw-bar label{display:inline-flex;gap:6px;align-items:center}
.cw-bar label.on{border-color:#0d9488;background:#f0fdfa}
.cw-card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:12px;margin:10px 0}
.cw-win{display:flex;height:54px;border-radius:10px;overflow:hidden;border:2px solid #0f172a;background:#f1f5f9;position:relative}
.cw-win div{height:100%;transition:width .35s ease;display:flex;align-items:center;justify-content:center;color:#fff;font-size:.72rem;font-weight:800;white-space:nowrap;overflow:hidden}
.cw-over{border-color:#dc2626!important;box-shadow:0 0 0 3px #fecaca}
.cw-leg{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px;font-size:.8rem;color:#334155}.cw-leg span{display:inline-flex;align-items:center;gap:5px}.cw-leg i{width:12px;height:12px;border-radius:3px;display:inline-block}
.cw-kpi{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}.cw-kpi div{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;font-size:.8rem;color:#475569}.cw-kpi b{display:block;font-size:1.15rem;color:#0f172a}
#cwChart{width:100%;height:auto;display:block}
.cw-cap{font-weight:700;color:#0f766e;min-height:1.4em;margin:6px 0}
.cw-more{margin-top:14px;color:#334155;font-size:.88rem;line-height:1.6}
body.cw-embed .navbar,body.cw-embed .nav-panel-wrap,body.cw-embed .nav-backdrop,body.cw-embed .cw-hero,body.cw-embed .cw-more,body.cw-embed .to-top{display:none!important}body.cw-embed main{padding-top:0!important}
@media (max-width:760px){.cw-kpi{grid-template-columns:repeat(2,1fr)}}
@media (prefers-reduced-motion:reduce){.cw-win div{transition:none}}
</style>'''
BODY = '''<main style="padding-top: 94px;">
<div class="cw">
  <div class="cw-hero"><h1>The Context Window, Live</h1><p class="intro">One agent task, 40 turns, one context window. Press play and watch the window fill with tool results and history until it overflows. Then switch on the fixes one at a time (lean tools and skills, tool result clearing, compaction, sub-agents, prompt caching) and see what each does to the window, the total tokens and the bill.</p></div>
  <div class="cw-bar"><button id="cwPlay">▶ Play 40 turns</button><button id="cwReset">↺ Reset</button>
   <label><input type="checkbox" id="oLean"> Lean tools + skills</label><label><input type="checkbox" id="oClear"> Clear old tool results</label><label><input type="checkbox" id="oComp"> Compaction</label><label><input type="checkbox" id="oSub"> Sub-agents</label><label><input type="checkbox" id="oCache"> Prompt caching</label>
   <label>Window <select id="oWin"><option value="100000">100k</option><option value="200000">200k</option><option value="1000000">1M</option></select></label></div>
  <div class="cw-card"><div class="cw-cap" id="cwCap">Turn 0 of 40</div><div class="cw-win" id="cwWin"></div><div class="cw-leg" id="cwLeg"></div></div>
  <div class="cw-kpi"><div>Window now<b id="kNow">0</b></div><div>Peak window<b id="kPeak">0</b></div><div>Input tokens so far<b id="kTot">0</b></div><div>Cost so far<b id="kCost">$0</b></div><div>Events<b id="kEv">—</b></div></div>
  <div class="cw-card"><svg id="cwChart" viewBox="0 0 900 260" role="img" aria-label="Window size per turn"></svg></div>
  <div class="cw-more"><p>A toy model, not a benchmark. Assumptions: system prompt 1,500 tokens, tools 12,000 (lean: 2,500 with deferred definitions and skill metadata), project file 3,000; each turn adds 300 tokens of model text and a 2,500-token tool result; clearing keeps the last 3 results; compaction at 60% of the window leaves a 2,000-token summary; sub-agents take every 10th block of work and return 1,500 tokens (their own tokens are not counted; Anthropic reports multi-agent systems use about 15× the tokens of chat); price example $3 per million input tokens, caching with 1.25× writes and 0.1× reads as in Claude’s docs. Read the series: <a href="../blog/context-eng-map.html">Part 1</a> · <a href="../blog/context-eng-what-goes-in.html">what goes in</a> · <a href="../blog/context-eng-long-tasks.html">long tasks</a> · <a href="../blog/context-eng-caching-evals.html">caching and measuring</a>.</p><p>Disclosure: Claude, made by Anthropic, helps write this site, and many of the techniques shown come from Anthropic’s posts and docs.</p></div>
</div>
</main>
<script src="../app.js"></script>
<script>
(function(){
var embed=/[?&]embed=1/.test(location.search);if(embed)document.body.classList.add('cw-embed');
var g=function(i){return document.getElementById(i)},T=40,timer=null,turn=0;
var SEG=[['sys','System prompt','#475569'],['tools','Tools + skills','#2563eb'],['file','Project file','#7c3aed'],['sum','Summaries','#0d9488'],['res','Tool results','#d97706'],['hist','Conversation','#be123c']];
g('cwLeg').innerHTML=SEG.map(function(s){return '<span><i style="background:'+s[2]+'"></i>'+s[1]+'</span>'}).join('')+'<span><i style="background:#f1f5f9;border:1px solid #94a3b8"></i>Free space</span>';
function opts(){return {lean:g('oLean').checked,clear:g('oClear').checked,comp:g('oComp').checked,sub:g('oSub').checked,cache:g('oCache').checked,W:+g('oWin').value}}
function simulate(o){var hist=[],sums=0,out=[],tot=0,cost=0,cached=0,ev=[];
 var pre={sys:1500,tools:o.lean?2500:12000,file:3000};var P=pre.sys+pre.tools+pre.file;
 for(var t=1;t<=T;t++){hist.push([300,2500]);
  if(o.clear)for(var i=0;i<hist.length-3;i++)hist[i][1]=Math.min(hist[i][1],40);
  if(o.sub&&t%10==0){hist=hist.slice(0,-10);sums+=1500;ev.push('turn '+t+': sub-agent summary');}
  var r=0,h=0;hist.forEach(function(x){h+=x[0];r+=x[1]});var ctx=P+sums+r+h;
  if(o.comp&&ctx>0.6*o.W){hist=[];sums=2000;ev.push('turn '+t+': compaction');r=0;h=0;ctx=P+sums;cached=0;}
  tot+=ctx;
  if(o.cache){var nw=Math.max(0,ctx-cached);cost+=(Math.min(cached,ctx)*0.1+nw*1.25)*3/1e6;cached=ctx;if(o.clear)cached=P;}else cost+=ctx*3/1e6;
  out.push({t:t,ctx:ctx,parts:{sys:pre.sys,tools:pre.tools,file:pre.file,sum:sums,res:r,hist:h},tot:tot,cost:cost,ev:ev.slice()});}
 return out;}
var RUN=simulate(opts()),BASE=simulate({lean:0,clear:0,comp:0,sub:0,cache:0,W:+g('oWin').value});
function fmt(n){return n>=1e6?(n/1e6).toFixed(2)+'M':n>=1e3?Math.round(n/1e3)+'k':String(n)}
function draw(k){var o=opts(),W=o.W,s=k?RUN[k-1]:null,win=g('cwWin');
 if(!s){win.innerHTML='';win.classList.remove('cw-over');g('cwCap').textContent='Turn 0 of 40: press play';['kNow','kPeak','kTot'].forEach(function(i){g(i).textContent='0'});g('kCost').textContent='$0';g('kEv').textContent='—';chart(0);return;}
 var over=s.ctx>W;win.classList.toggle('cw-over',over);
 win.innerHTML=SEG.map(function(x){var v=s.parts[x[0]],w=Math.min(100,v/W*100);return w>0?'<div style="width:'+w+'%;background:'+x[2]+'" title="'+x[1]+': '+v.toLocaleString()+' tokens">'+(w>6?x[1]:'')+'</div>':''}).join('');
 var peak=0;for(var i=0;i<k;i++)peak=Math.max(peak,RUN[i].ctx);
 g('kNow').textContent=fmt(s.ctx);g('kPeak').textContent=fmt(peak);g('kTot').textContent=fmt(s.tot);g('kCost').textContent='$'+s.cost.toFixed(2);g('kEv').textContent=s.ev.length?s.ev.length+' ('+s.ev[s.ev.length-1]+')':'none';
 g('cwCap').textContent='Turn '+k+' of 40 · '+(over?'⚠️ overflowed the '+fmt(W)+' window: the agent would fail or lose text here':Math.round(s.ctx/W*100)+'% of the '+fmt(W)+' window used');chart(k);}
function chart(k){var o=opts(),W=o.W,maxV=Math.max(W*1.05,Math.max.apply(null,BASE.map(function(x){return x.ctx}))),X=function(t){return 50+(t-1)/(T-1)*820},Y=function(v){return 220-v/maxV*190};
 var s='<line x1="50" y1="220" x2="870" y2="220" stroke="#94a3b8"/><line x1="50" y1="'+Y(W)+'" x2="870" y2="'+Y(W)+'" stroke="#dc2626" stroke-dasharray="6 4"/><text x="866" y="'+(Y(W)-6)+'" text-anchor="end" font-size="12" fill="#dc2626">window limit '+fmt(W)+'</text>';
 s+='<polyline fill="none" stroke="#cbd5e1" stroke-width="2.5" points="'+BASE.map(function(x){return X(x.t)+','+Y(x.ctx)}).join(' ')+'"/><text x="54" y="'+(Y(BASE[T-1].ctx)<40?40:30)+'" font-size="12" fill="#94a3b8">grey: no fixes</text>';
 if(k)s+='<polyline fill="none" stroke="#0d9488" stroke-width="3" points="'+RUN.slice(0,k).map(function(x){return X(x.t)+','+Y(x.ctx)}).join(' ')+'"/><circle cx="'+X(k)+'" cy="'+Y(RUN[k-1].ctx)+'" r="5" fill="#0d9488"/>';
 for(var t=1;t<=T;t+=5)s+='<text x="'+X(t)+'" y="240" text-anchor="middle" font-size="11" fill="#64748b">'+t+'</text>';
 s+='<text x="460" y="256" text-anchor="middle" font-size="11" fill="#64748b">turn</text><text x="8" y="20" font-size="11" fill="#64748b">tokens in window</text>';
 g('cwChart').innerHTML=s;}
function recalc(){RUN=simulate(opts());BASE=simulate({lean:0,clear:0,comp:0,sub:0,cache:0,W:+g('oWin').value});document.querySelectorAll('.cw-bar label').forEach(function(l){var c=l.querySelector('input');if(c)l.classList.toggle('on',c.checked)});draw(turn);}
['oLean','oClear','oComp','oSub','oCache','oWin'].forEach(function(i){g(i).addEventListener('change',recalc)});
g('cwPlay').onclick=function(){clearInterval(timer);if(turn>=T)turn=0;var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;if(rm){turn=T;draw(turn);return;}timer=setInterval(function(){turn++;draw(turn);if(turn>=T)clearInterval(timer);},220);};
g('cwReset').onclick=function(){clearInterval(timer);turn=0;draw(0);};
draw(0);
function tell(){if(embed&&parent!==window)parent.postMessage({cwHeight:Math.ceil(document.querySelector('.cw').getBoundingClientRect().bottom+8)},'*');}
addEventListener('resize',tell);setTimeout(tell,400);document.addEventListener('click',function(){setTimeout(tell,60);});
})();
</script>
</body>
</html>
'''
open(R + 'pages/context-window-live.html', 'w').write(head + CSS + nav + BODY)
