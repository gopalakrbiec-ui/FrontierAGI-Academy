HERO = 'Multi-agent systems fail in their own ways: agents misunderstand their roles, drop information between each other, stop too early or never stop. This part covers what research and practitioners report about those failures, why errors compound along chains, what multi-agent costs in tokens, and how to observe, test and ship these systems safely.'
CAV = 'Failure categories come from the MAST project (“Why Do Multi-Agent Systems Fail?”, Cemri et al., 2025): we read its repository but could not open the paper, so category details are marked ⚠️. Cost figures and production lessons are as reported in Anthropic’s multi-agent research system post (read 28 Nov 2026). The compounding script is a toy model with stated assumptions.'
MAR = 'https://www.anthropic.com/engineering/multi-agent-research-system'

sec('mast', 'What goes wrong: the MAST taxonomy',
pts(('The study.', ['The MAST repository describes “the first comprehensive study of MAS challenges” and a dataset of over 1,000 annotated multi-agent traces.']),
('Three groups of failure ⚠️.', ['<b>Specification and system design</b>: agents ignore their role or the task constraints, repeat steps, lose conversation history, do not know when the task is done.', '<b>Inter-agent misalignment</b>: agents withhold information, ignore other agents’ input, derail the conversation, reset the discussion.', '<b>Task verification and termination</b>: stopping too early, no or weak verification, wrong verification.', 'Group names and members are from our memory of the paper, not re-checked.']),
('Our reading.', ['Most failures are about communication and checking, not about any single agent being weak. Better models help less than clearer roles and real verification.'])) + MAP)

sec('compound', 'Errors compound',
RUN('multi-agent-failures-cost', 'compounding.py') +
fig('6-compounding.svg', 'Lines showing chain success falling with the number of hand-offs, with and without a checker', 'From the script output.') +
pts(('Reading the output.', ['At 95% success per hand-off, a 10-step chain succeeds only 60% of the time; at 90%, 35%.', 'A checker that catches 80% of failed steps and retries once lifts the 10-step chain to about 89% and 75%.', 'Token cost scales the other way: at Anthropic’s reported ratios, a task that costs 3,000 tokens as a chat costs ~45,000 as a multi-agent system.']),
('Lesson.', ['Fewer hand-offs and verification at each boundary matter more than adding agents.'])))

sec('anthropic', 'Lessons from running one in production',
tbl(['Lesson (Anthropic post)', 'What it means for you'], [
['Agents are stateful and errors compound; minor issues can derail long runs', 'Build resumption from checkpoints, not restarts from scratch'],
['Small changes to the lead agent “can unpredictably change how subagents behave”', 'Test the whole system after any prompt change'],
['Debugging needs full tracing of decisions and interactions', 'Trace every agent’s input, output and tool calls'],
['Deploying updates mid-run is risky; they used “rainbow deployments”', 'Roll out new versions gradually; keep old ones for running tasks'],
['Synchronous sub-agents create bottlenecks', 'Accept it for simplicity, or design asynchronous coordination carefully']]))

sec('observe', 'Observability for multi-agent systems',
pts(('Trace the whole tree.', ['One trace per task, with a span per agent and per tool call, so you can see who asked whom for what. OpenTelemetry’s GenAI conventions and MCP’s trace propagation help (see <a href="adlc-operations-observability.html">ADLC operations</a>).']),
('Watch these metrics.', ['Hand-offs per task, hop depth, repeated work (two agents fetching the same thing), tokens per agent, time waiting on sub-agents, and how often the final check fails.']),
('Look at transcripts.', ['Anthropic stresses manual review alongside automated evals, because emergent behaviour shows up in conversations between agents, not in single outputs.'])))

sec('test', 'How to test them',
tbl(['Level', 'What to test', 'How'], [
['Each agent', 'Does it do its narrow job?', 'Unit evals with fixed inputs'],
['Each boundary', 'Does the hand-off carry goal, facts and format?', 'Contract tests on delegation messages'],
['Whole task', 'Does the system succeed end to end?', 'Task eval set, several runs per task'],
['Failure injection', 'What if one agent is wrong, slow or silent?', 'Replace an agent with a faulty stub'],
['Cost and time', 'Within budget?', 'Track tokens and wall time per task']]) +
pts(('Start small.', ['Anthropic reports starting evals with about 20 queries representing real usage, because early changes have large effects (“you can spot changes with just a few test cases”).'])))

sec('safety', 'Safety and permissions',
pts('Give each agent only the tools its job needs; do not let every agent touch money or production systems.', 'Put human approval on irreversible actions at the boundary where they happen, not only at the top.', 'Treat messages from other agents as untrusted input: an agent that read a malicious web page can pass injected instructions on (see <a href="computer-use-safety.html">computer-use safety</a>).', 'Across companies, use authenticated protocols such as <a href="agent-protocols-a2a.html">A2A</a> rather than shared prompts.'))

sec('cost', 'When the cost is worth it',
tbl(['Signal', 'Multi-agent likely worth it', 'Probably not'], [
['Task value', 'High (research, due diligence, migrations)', 'Low (FAQ answers)'],
['Parallel parts', 'Many independent parts', 'Tightly coupled steps'],
['Context', 'Exceeds one window', 'Fits comfortably'],
['Tools', 'Many complex tools', 'A few simple ones'],
['Latency budget', 'Minutes acceptable', 'Seconds required']]) +
'<p>Built on Anthropic’s stated fit conditions; the table layout and thresholds are our reading.</p>')

sec('migrate', 'Moving from one agent to several, safely',
tbl(['Step', 'Do'], [
['1', 'Measure the single-agent baseline on your eval set: success, cost, time'],
['2', 'Find the bottleneck: context overflow, slow serial work, or mixed skills'],
['3', 'Pick the smallest pattern that addresses it (sub-agents for context, sectioning for speed, router for mixed skills)'],
['4', 'Add tracing and a whole-task eval before going live'],
['5', 'Roll out to a slice of traffic; compare with the baseline'],
['6', 'Keep the single-agent path as a fallback until the new one wins clearly']]))

sec('checklist', 'Final checklist for the series',
tbl(['Area', 'Check'], [
['Need', 'A single good agent was tried first and its limit is clear'],
['Pattern', 'The simplest pattern that fixes that limit'],
['Roles', 'One sentence per agent, no overlaps, one owner of the answer'],
['Boundaries', 'Hand-offs carry goal, constraints, facts and return format; hop limits'],
['Checks', 'Verification at boundaries; a final whole-task check'],
['Cost', 'Token and time budget per task; measured against the baseline'],
['Operations', 'Full tracing, gradual rollout, failure injection tests']]))

sec('sources', 'Sources',
pts(A('https://github.com/multi-agent-systems-failure-taxonomy/MAST', 'MAST: Why Do Multi-Agent Systems Fail? (repository and dataset)') + ' ⚠️', A(MAR, 'Anthropic: How we built our multi-agent research system'), A('https://www.anthropic.com/engineering/building-effective-agents', 'Anthropic: Building effective agents'), 'Script: <code>data/code/multi-agent-failures-cost/compounding.py</code>'))
JS = ''
