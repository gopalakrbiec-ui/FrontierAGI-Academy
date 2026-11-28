sec('why', 'Why teams reach for multiple agents',
pts(('Context limits.', ['One agent reading four websites, a database and a codebase fills its window. Giving each source its own agent keeps every window clean; the main agent sees only summaries. This is the most solid reason, and it is really a context engineering decision (see <a href="context-eng-long-tasks.html">long tasks</a>).']),
('Speed.', ['Independent parts can run at the same time. Anthropic’s research system cut research time by up to 90% on complex queries this way.']),
('Specialisation.', ['A focused prompt with a few tools usually beats one prompt that tries to do everything. OpenAI’s docs: “Have specialized agents that excel in one task, rather than having a general purpose agent that is expected to be good at anything.”']),
('Checks.', ['A second agent that reviews or votes catches mistakes the first one makes.']),
('Weak reasons (our reading).', ['Because it looks like a team chart; because a framework makes it easy; because “agents” sounds more impressive than “a function call”.'])))

sec('anti', 'Anti-patterns to avoid',
tbl(['Anti-pattern', 'What happens', 'Instead'], [
['An agent per job title (“CEO agent”, “CTO agent”)', 'Role-play without real division of work; long chats, little output', 'Split by information or tools, not by titles'],
['Agents that all read everything', 'Same context copied many times; cost explodes', 'Give each agent only what its job needs'],
['No owner of the final answer', 'Contradictory outputs, nobody checks the whole', 'One supervisor or a final verifier'],
['Unlimited delegation', 'Agents spawn agents; costs and time run away', 'Depth and budget limits'],
['Free-form group chat for a fixed process', 'Unpredictable order, hard to test', 'A chain or router in code']]))

sec('signals', 'Signals that you need to split (and signals you don’t)',
tbl(['You see this', 'Likely fix'], [
['The agent forgets early instructions late in long tasks', 'Context techniques first; then sub-agents'],
['Answers are good but slow because the agent works serially', 'Sectioning or parallel sub-agents'],
['One prompt has grown to cover five different jobs', 'Router or supervisor with specialists'],
['Quality varies and a human reviewer would catch the errors', 'Evaluator–optimizer'],
['Errors come from wrong facts, not wrong steps', 'Better retrieval, not more agents'],
['The agent picks the wrong tool', 'Fewer, clearer tools, not more agents']]))

sec('protocols', 'Inside one system vs across companies',
pts('Everything in this series is about agents inside one system, usually one codebase and one framework. When the other agent belongs to another team or company, the same patterns apply, but the connection becomes a protocol: <a href="agent-protocols-a2a.html">A2A</a> for tasks between agents, <a href="agent-protocols-mcp.html">MCP</a> for tools.', 'The design questions do not change: who owns the answer, what is passed across, how failures are detected, and who pays for the tokens.'))
