HERO = 'The cheapest token is the one you never send. This part goes through each part of the context you control before the agent starts: the system prompt and its “right altitude”, project files like CLAUDE.md and AGENTS.md, tool sets and tool descriptions, examples, retrieval versus agentic search, and skills and tool search that load detail only when needed. It ends with a budget calculator.'
CAV = 'Guidance is quoted from Anthropic’s “Effective context engineering for AI agents” and Agent Skills posts and Claude’s context window docs (read 28 Nov 2026). The calculator is our own simple model with example inputs; token counts for real prompts depend on the tokenizer.'
ACE = 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents'

sec('prompt', 'System prompts at the right altitude',
pts(('Two ways to get it wrong.', ['Anthropic describes a “Goldilocks zone” between “hardcoding complex, brittle logic” (long if-then rule lists) and “vague, high-level guidance that fails to give the LLM concrete signals” or “falsely assumes shared context”.']),
('What the right altitude looks like.', ['“Specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics.”']),
('Structure helps people more than models now.', ['Sections such as background, instructions, tool guidance and output description, marked with XML tags or Markdown headers, though “the exact formatting of prompts is likely becoming less important as models become more capable.”'])) +
tbl(['Too low (brittle)', 'Right altitude', 'Too high (vague)'], [
['“If the refund is $99.99 or less and the customer tier is gold or silver and…”', '“Refund up to $100 when the order record supports it; above that, ask a human. Explain the decision in one sentence.”', '“Be helpful with refunds.”'],
['Breaks on the first case nobody listed', 'Covers new cases with a clear rule and a reason', 'Model guesses the policy']]) + MAP)

sec('files', 'Project files: CLAUDE.md, AGENTS.md and friends',
pts(('What they are.', ['Plain Markdown files the harness loads at the start of every session: build commands, conventions, warnings. Claude Code reads CLAUDE.md; AGENTS.md is an open format read by several coding agents ⚠️ (its list of supporting tools changes often).']),
('Why they work.', ['They are the “up front” half of the hybrid Anthropic describes: always loaded, so they must earn their place.']),
('Keep them lean.', ['Every line is paid for on every call. Put rarely needed detail in separate files the agent can open when needed, or in a skill.']),
('Real example.', ['This site’s own CLAUDE.md is long because it is the only memory between sessions; we keep it as a reference and rely on the agent to search it, which is the same trade-off.'])))

sec('tools', 'Tools: fewer, clearer, cheaper',
pts(('The contract.', ['Anthropic: tools “define the contract between agents and their information/action space”; they should be “self-contained, robust to error, and extremely clear with respect to their intended use”.']),
('The failure they see most.', ['“Bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use.” Their test: if a human engineer cannot say which tool fits, the agent will not do better.']),
('Token-efficient results.', ['Return what the agent needs, not the whole API response: filtered fields, a count plus the first rows, a link to the full file.'])) +
tbl(['Bad tool', 'Better tool'], [
['<code>get_all_orders()</code> returns 5,000 rows', '<code>search_orders(customer, since, limit=20)</code> returns matches and a total'],
['Three overlapping tools: <code>find_user</code>, <code>lookup_customer</code>, <code>get_account</code>', 'One <code>get_customer(id or email)</code>'],
['Raw HTML of a page', 'Readable text or the accessibility tree, trimmed'],
['Error: “500”', 'Error that says what went wrong and what to try next']]))

sec('search', 'Too many tools: deferred definitions',
pts(('The problem.', ['Each tool definition sits in every call. Agents connected to many MCP servers can carry tens of thousands of tokens of tool definitions before doing anything.']),
('The fix.', ['Load tool definitions only when needed. Claude’s docs point to the tool search tool to “defer tool definitions”; other harnesses filter tools per task or per sub-agent ⚠️ (details vary).']),
('Rule of thumb (our reading).', ['If an agent has more tools than you could explain from memory, give it a search tool or split it into specialists.'])))

sec('examples', 'Examples: a few good ones',
pts(('Still recommended.', ['Anthropic calls few-shot examples “a well known best practice that we continue to strongly advise.”']),
('But not a rule dump.', ['Teams often “stuff a laundry list of edge cases into a prompt”. Instead, curate “a set of diverse, canonical examples”: “for an LLM, examples are the ‘pictures’ worth a thousand words.”']),
('Practical tip (our reading).', ['Three to five examples that differ in the ways that matter beat twenty that look alike. Refresh them from real failures.'])))

sec('retrieval', 'Retrieval, agentic search, or both',
tbl(['Approach', 'How', 'Good for', 'Weak at'], [
['Pre-retrieval (RAG)', 'Embed documents; fetch top chunks before the model runs', 'Fast answers over stable documents', 'Wrong chunks, stale index, no follow-up'],
['Agentic search', 'Agent calls search, grep, glob, SQL as needed', 'Codebases, changing data, multi-step questions', 'Slower, more calls, needs good tools'],
['Hybrid', 'Some context up front, the rest on demand', 'Most real agents', 'More moving parts']]) +
pts(('Signals for free.', ['Anthropic notes that file names, folder hierarchies and timestamps are themselves context: “a file named test_utils.py in a tests folder implies a different purpose than a file with the same name located in src/core_logic/”.']),
('See also.', ['Our <a href="../pages/rag-compare.html">RAG vs agentic RAG vs graph RAG</a> map.'])))

sec('skills', 'Skills: progressive disclosure',
fig('4-disclosure.svg', 'Three nested levels: name and description, SKILL.md body, extra files', 'From Anthropic’s Agent Skills post.') +
pts(('How it works.', ['A skill is “a directory containing a SKILL.md file” with “organized folders of instructions, scripts, and resources”. At startup the agent “pre-loads the name and description of every installed skill into its system prompt”: the first level of progressive disclosure.']),
('Only when relevant.', ['The SKILL.md body is read when the skill looks relevant to the task; extra files and scripts are opened or run only if needed.']),
('Why it matters.', ['You can install many skills while paying only a line or two each until one is used. Agent Skills were donated to the Agentic AI Foundation in October 2026 (our lab-updates data).'])))

sec('budget', 'Try it: a context budget',
'<div class="sf-c" id="cb">'
'<label>System prompt (tokens) <input type="range" id="cbP" min="200" max="8000" step="100" value="1500"><output id="cbPo"></output></label>'
'<label>Number of tools <input type="range" id="cbT" min="0" max="120" value="40"><output id="cbTo"></output></label>'
'<label>Tokens per tool definition <input type="range" id="cbD" min="50" max="800" step="10" value="250"><output id="cbDo"></output></label>'
'<label>Project file (tokens) <input type="range" id="cbF" min="0" max="15000" step="250" value="3000"><output id="cbFo"></output></label>'
'<label>Installed skills <input type="range" id="cbS" min="0" max="80" value="20"><output id="cbSo"></output></label>'
'<label><input type="checkbox" id="cbX"> Defer tool definitions (load ~5 per task)</label>'
'<label>Window size <select id="cbW"><option value="200000">200k</option><option value="1000000">1M</option></select></label>'
'<div class="sf-o" id="cbO"></div></div>' +
'<p>Our simple model: skill metadata at about 80 tokens each, deferred tools load five definitions plus a ~400-token search tool. Example inputs, not measurements.</p>')

sec('checklist', 'Before the agent starts: a checklist',
tbl(['#', 'Check'], [
['1', 'System prompt states goal, rules with reasons, and output; no rule lists for edge cases'],
['2', 'Project file under a size you would read yourself; detail moved to files or skills'],
['3', 'Every tool has one clear job; no two tools you could confuse'],
['4', 'Tool results trimmed to what the next step needs'],
['5', 'More than ~20 tools? Defer or split (our rule of thumb)'],
['6', '3–5 diverse, canonical examples instead of an edge-case list'],
['7', 'Retrieval or search decided per data type, not by default'],
['8', 'Stable parts first, so they can be cached (Part 4)']]))

sec('sources', 'Sources',
pts(A(ACE, 'Anthropic: Effective context engineering for AI agents'), A('https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills', 'Anthropic: Agent Skills'), A('https://platform.claude.com/docs/en/build-with-claude/context-windows', 'Claude docs: context windows (tool search, context awareness)'), A('https://github.com/langchain-ai/context_engineering', 'LangChain: context_engineering')))

JS = '''<script>
(function(){var g=function(i){return document.getElementById(i)},I=['cbP','cbT','cbD','cbF','cbS','cbX','cbW'];
function r(){var P=+g('cbP').value,T=+g('cbT').value,D=+g('cbD').value,F=+g('cbF').value,S=+g('cbS').value,X=g('cbX').checked,W=+g('cbW').value;
g('cbPo').textContent=P.toLocaleString();g('cbTo').textContent=T;g('cbDo').textContent=D;g('cbFo').textContent=F.toLocaleString();g('cbSo').textContent=S;
var tools=X?Math.min(T,5)*D+400:T*D,skills=S*80,tot=P+tools+F+skills,pct=tot/W*100;
g('cbO').innerHTML='<b class="big">'+tot.toLocaleString()+' tokens</b> before the agent reads a single file ('+pct.toFixed(1)+'% of a '+(W/1000)+'k window)<br>System prompt '+P.toLocaleString()+' · tools '+tools.toLocaleString()+(X?' (deferred)':'')+' · project file '+F.toLocaleString()+' · skill metadata '+skills.toLocaleString()+'<br>Over a 40-call task the model reads this prefix 40 times: '+(tot*40).toLocaleString()+' tokens. Cache it (Part 4) and keep it lean.';}
I.forEach(function(i){g(i).addEventListener('input',r);g(i).addEventListener('change',r)});r();})();
</script>'''
