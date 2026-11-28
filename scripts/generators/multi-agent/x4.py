sec('incidents', 'What failures look like in practice (illustrative)',
tbl(['Story', 'Root cause', 'Fix'], [
['Two researcher agents spent the budget searching the same sources', 'Vague briefs, no division of sources', 'Briefs with explicit boundaries'],
['A refund was processed twice', 'Two agents both believed they owned the refund step', 'One owner per action; idempotency keys (see our <a href="agentic-runtimes-compared.html">runtimes crash test</a>)'],
['The final report contradicted itself', 'Supervisor pasted worker outputs without reconciling them', 'A synthesis step with a consistency check'],
['A task “finished” with half the files unchanged', 'Termination decided by an agent that never checked', 'Verification against the task list before done'],
['An injected instruction spread through the team', 'Worker read a malicious page and passed text on as instructions', 'Treat agent messages as data; tool permissions per agent']]) +
'<p>Made-up but typical stories, matched to the MAST-style categories above.</p>')

sec('dashboard', 'An example dashboard',
tbl(['Metric', 'Example', 'Good direction'], [
['Task success (whole system)', '84%', 'Up'],
['Hand-offs per task (median)', '4', 'Stable or down'],
['Duplicate work rate', '6%', 'Down'],
['Tokens per task, by agent', 'Lead 30k, workers 120k', 'Down without success falling'],
['Final-check failures', '9%', 'Down'],
['Wall time (p90)', '6 min', 'Within budget']]) +
'<p>Values are made up to show the layout.</p>')

sec('future', 'Where this is heading (our prediction)',
pts('Fewer, stronger agents: as single agents handle longer contexts and tool sets, many multi-agent designs collapse back into one agent with sub-agents for isolation.', 'Supervisor-via-tools becomes the default; free-form group chat stays in research and demos.', 'Asynchronous coordination improves: agents that can steer each other mid-task rather than waiting (Anthropic names this as a current limit).', 'Cross-company multi-agent work grows through protocols (A2A) with clearer contracts and billing.'))

sec('glossary2', 'Glossary of failure terms',
tbl(['Term', 'Meaning'], [
['Compounding error', 'Small per-step failure rates multiplying along a chain'],
['Ping-pong', 'Agents handing control back and forth without progress'],
['Premature termination', 'Stopping before the task is actually done'],
['Telephone effect', 'Information degrading as it is passed through several agents'],
['Failure injection', 'Deliberately making one agent fail to test the system'],
['Rainbow deployment', 'Running old and new versions side by side while shifting traffic gradually']]))
