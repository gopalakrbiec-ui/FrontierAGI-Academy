import re
R = '/home/user/Claude_Project_3_LLM/'
src = open(R + 'pages/computer-use-loop.html').read()
head = src[:src.index('<style>')].replace('Computer Use, Step by Step', 'A Voice Call, Millisecond by Millisecond')
head = re.sub(r'<!-- SEO:START.*?SEO:END -->\n?', '', head, flags=re.S)
nav = src[src.index('</style>') + len('</style>'):src.index('<main')]
CSS = '''<style>
.vc{max-width:1180px;margin:0 auto;padding:18px 16px 30px}
.vc-hero{background:linear-gradient(135deg,#0f172a,#be123c 45%,#0d9488);color:#fff;border-radius:16px;padding:22px}.vc-hero h1{margin:0 0 6px;font-size:1.7rem}.vc-hero p{margin:0;color:#fff1f2;line-height:1.55}
.vc-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:12px 0}.vc-bar button,.vc-bar label{border:1px solid #cbd5e1;background:#fff;border-radius:999px;padding:6px 12px;font-weight:700;cursor:pointer;font-size:.85rem}.vc-bar label{display:inline-flex;gap:6px;align-items:center}.vc-bar button.on{background:#0f172a;color:#fff}
.vc-card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:12px;margin:10px 0}
#vcSvg{display:block;width:100%;height:auto;font-family:Arial,Helvetica,sans-serif}
.vc-kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.vc-kpi div{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;font-size:.8rem;color:#475569}.vc-kpi b{display:block;font-size:1.15rem;color:#0f172a}
.vc-say{font-size:1rem;line-height:1.6;min-height:3.2em}.vc-say b{color:#be123c}
.vc-more{margin-top:14px;color:#334155;font-size:.88rem;line-height:1.6}
body.vc-embed .navbar,body.vc-embed .nav-panel-wrap,body.vc-embed .nav-backdrop,body.vc-embed .vc-hero,body.vc-embed .vc-more,body.vc-embed .to-top{display:none!important}body.vc-embed main{padding-top:0!important}
@media (max-width:760px){.vc-kpi{grid-template-columns:repeat(2,1fr)}}
</style>'''
BODY = '''<main style="padding-top: 94px;">
<div class="vc">
  <div class="vc-hero"><h1>A Voice Call, Millisecond by Millisecond</h1><p class="intro">One turn of a support call: the caller says “it arrived broken, I want a refund”. The waterfall shows every stage until they hear the agent’s first word. Switch the architecture and the line, turn on smarter turn detection, slow down the order-lookup tool, or let the caller interrupt, and watch the delay change against an 800 ms target.</p></div>
  <div class="vc-bar"><b style="font-size:.85rem">Build:</b><button data-a="cascade" class="on">Cascade (STT → LLM → TTS)</button><button data-a="s2s">Speech-to-speech</button>
  <b style="font-size:.85rem">Line:</b><button data-n="web" class="on">Browser</button><button data-n="phone">Phone</button></div>
  <div class="vc-bar"><label><input type="checkbox" id="oTurn"> Smart turn detection</label><label><input type="checkbox" id="oNear"> Nearer, faster model</label><label><input type="checkbox" id="oTool"> Slow tool call (1.8 s)</label><label><input type="checkbox" id="oFill"> Say a filler first</label><label><input type="checkbox" id="oBarge"> Caller interrupts</label><button id="vcPlay">▶ Play the turn</button></div>
  <div class="vc-kpi"><div>First audio at ear<b id="kF">—</b></div><div>Target 800 ms<b id="kT">—</b></div><div>Silence the caller hears<b id="kS">—</b></div><div>Answer with order details<b id="kA">—</b></div></div>
  <div class="vc-card"><svg id="vcSvg" viewBox="0 0 900 360" role="img" aria-label="Latency waterfall for one voice turn"></svg></div>
  <div class="vc-card vc-say" id="vcSay"></div>
  <div class="vc-more"><p>A teaching model: stage timings are our illustrative assumptions (the same ones as <code>latency_budget.py</code> in Part 2), not vendor measurements. Read the series: <a href="../blog/voice-agents-map.html">Part 1</a> · <a href="../blog/voice-agents-latency.html">latency budget</a> · <a href="../blog/voice-agents-building.html">building one</a> · <a href="../blog/voice-agents-production.html">production</a>.</p><p>Disclosure: Claude, made by Anthropic, helps write this site; the series covers voice products from OpenAI, Google, Microsoft, xAI, Mistral and open-source projects.</p></div>
</div>
</main>
<script src="../app.js"></script>
<script>
(function(){
var embed=/[?&]embed=1/.test(location.search);if(embed)document.body.classList.add('vc-embed');
var g=function(i){return document.getElementById(i)},A='cascade',N='web',run=0;
var COL={turn:'#d97706',stt:'#2563eb',llm:'#7c3aed',tts:'#0d9488',s2s:'#be123c',net:'#475569',tool:'#0f172a',fill:'#15803d'};
function stages(){var t=g('oTurn').checked,near=g('oNear').checked,S=[];
 S.push(['End-of-turn wait',t?250:500,'turn']);
 if(A==='cascade'){S.push(['Speech-to-text final',150,'stt']);S.push(['LLM first token',near?300:450,'llm']);S.push(['First sentence ready',150,'llm']);S.push(['Text-to-speech first audio',200,'tts']);}
 else S.push(['Model first audio',near?300:450,'s2s']);
 S.push([N==='phone'?'Phone line and codec':'Browser network',N==='phone'?250:60,'net']);return S;}
function calc(){var S=stages(),t=0,rows=[];S.forEach(function(s){rows.push([s[0],t,s[1],s[2]]);t+=s[1];});var first=t,answer=t,silence=t,say='';
 var tool=g('oTool').checked,fill=g('oFill').checked;
 if(tool){var ts=first-(N==='phone'?250:60)-(A==='cascade'?350:0);rows.push(['Order lookup tool',ts,1800,'tool']);answer=ts+1800+(A==='cascade'?500:300)+(N==='phone'?250:60);
  if(fill){rows.push(['Filler: “Let me check that order…”',first,1500,'fill']);silence=first;}else{silence=answer;first=answer;}}
 return {rows:rows,first:first,answer:answer,silence:silence};}
function draw(k){var c=calc(),max=Math.max(2000,c.answer+300),X=function(v){return 230+v/max*640},s='';
 for(var v=0;v<=max;v+=500)s+='<line x1="'+X(v)+'" y1="30" x2="'+X(v)+'" y2="'+(40+c.rows.length*38)+'" stroke="#e2e8f0"/><text x="'+X(v)+'" y="22" text-anchor="middle" font-size="11" fill="#64748b">'+v+' ms</text>';
 s+='<line x1="'+X(800)+'" y1="28" x2="'+X(800)+'" y2="'+(44+c.rows.length*38)+'" stroke="#15803d" stroke-width="2" stroke-dasharray="5 4"/><text x="'+(X(800)+4)+'" y="'+(56+c.rows.length*38)+'" font-size="11" fill="#15803d" font-weight="700">800 ms target</text>';
 c.rows.forEach(function(r,i){var y=40+i*38,show=k===undefined||i<k;s+='<text x="10" y="'+(y+18)+'" font-size="12.5" font-weight="700" fill="#0f172a">'+r[0]+'</text>';
  if(show)s+='<rect x="'+X(r[1])+'" y="'+(y+4)+'" width="'+Math.max(3,X(r[1]+r[2])-X(r[1]))+'" height="22" rx="5" fill="'+COL[r[3]]+'"/><text x="'+(X(r[1]+r[2])+4)+'" y="'+(y+20)+'" font-size="11.5" fill="#334155">'+r[2]+' ms</text>';});
 if(g('oBarge').checked&&(k===undefined||k>=c.rows.length)){var by=40+c.rows.length*38;s+='<text x="10" y="'+(by+40)+'" font-size="12.5" font-weight="700" fill="#be123c">Caller interrupts → stop audio within ~200 ms, keep only what was heard</text>';}
 g('vcSvg').setAttribute('viewBox','0 0 900 '+(90+c.rows.length*38+(g('oBarge').checked?30:0)));g('vcSvg').innerHTML=s;
 var ok=c.first<=800;g('kF').textContent=c.first.toLocaleString()+' ms';g('kT').textContent=ok?'✅ met':'❌ missed by '+(c.first-800)+' ms';g('kS').textContent=c.silence.toLocaleString()+' ms';g('kA').textContent=c.answer.toLocaleString()+' ms';
 var tool=g('oTool').checked,fill=g('oFill').checked;
 g('vcSay').innerHTML='<b>Caller:</b> “It arrived broken, I want a refund.”<br><b>Agent</b> (after '+c.first+' ms): '+(tool?(fill?'“Let me check that order for you…” … then at '+c.answer+' ms: “I see order 4729 for $240. Because it is over $100, I’ll connect you to a colleague to approve it.”':'(silence until '+c.answer+' ms) “I see order 4729 for $240…”'):'“I’m sorry about that. Can you tell me your order number?”')+(g('oBarge').checked?'<br><b>Caller</b> (interrupting): “It’s 4-7-2-9.” → the agent stops talking and listens.':'');}
function play(){var me=++run,n=calc().rows.length,k=0;(function nx(){if(me!==run)return;draw(k);if(k++<n)setTimeout(nx,matchMedia('(prefers-reduced-motion: reduce)').matches?20:450);})();}
document.querySelectorAll('[data-a]').forEach(function(b){b.onclick=function(){A=b.dataset.a;document.querySelectorAll('[data-a]').forEach(function(x){x.classList.toggle('on',x===b)});draw();};});
document.querySelectorAll('[data-n]').forEach(function(b){b.onclick=function(){N=b.dataset.n;document.querySelectorAll('[data-n]').forEach(function(x){x.classList.toggle('on',x===b)});draw();};});
['oTurn','oNear','oTool','oFill','oBarge'].forEach(function(i){g(i).onchange=function(){run++;draw();};});g('vcPlay').onclick=play;draw();
function tell(){if(embed&&parent!==window)parent.postMessage({vcHeight:Math.ceil(document.querySelector('.vc').getBoundingClientRect().bottom+8)},'*');}
addEventListener('resize',tell);setTimeout(tell,400);document.addEventListener('click',function(){setTimeout(tell,60);});
})();
</script>
</body>
</html>
'''
open(R + 'pages/voice-call-latency.html', 'w').write(head + CSS + nav + BODY)
