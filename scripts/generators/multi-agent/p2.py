HERO = 'The two patterns most teams end up choosing between: a supervisor that calls specialists as tools and writes the answer itself, or hand-offs where a specialist takes over the conversation. This part compares them in detail, shows how the OpenAI Agents SDK, LangGraph, CrewAI and Claude’s sub-agents implement them, covers what context to pass between agents, and ends with a design checklist.'
CAV = 'Framework behaviour is quoted from the OpenAI Agents SDK docs (orchestration and handoffs pages), the LangGraph Supervisor and Swarm READMEs, CrewAI’s README and Anthropic’s posts, read on 28 Nov 2026. Code snippets are shortened from those sources and were not executed. The refund example is made up.'
OAI = 'https://github.com/openai/openai-agents-python/blob/main/docs/multi_agent.md'

sec('two', 'The two patterns side by side',
fig('3-tools-vs-handoffs.svg', 'Left: manager calls two specialists and answers the user. Right: triage hands off to refund agent, which hands off to policy agent', 'Our drawing of the two patterns in the OpenAI SDK docs.') +
tbl(['', 'Agents as tools (supervisor)', 'Hand-offs (swarm)'], [
['Who talks to the user', 'The manager, always', 'Whichever agent is active'],
['Who writes the final answer', 'The manager', 'The last specialist'],
['Control', 'Returns to the manager after each call', 'Moves to the specialist'],
['Guardrails', 'Can be enforced “in one place” (OpenAI docs)', 'Each agent needs its own'],
['Context', 'Manager’s window grows with every result', 'Each specialist sees what the hand-off passes'],
['Best when', 'One agent should own the result and combine specialists', 'The specialist should respond directly and keep prompts focused']]) + MAP)

sec('openai', 'OpenAI Agents SDK',
pts(('Its own guidance.', ['“Use agents as tools when a specialist should help with a bounded subtask but should not take over the user-facing conversation. Use handoffs when routing itself is part of the workflow and you want the chosen specialist to own the remainder of the current turn.”']),
('Combine them.', ['“A triage agent might hand off to a specialist, and that specialist can still call other agents as tools for narrow subtasks.”'])) +
CODE('Both patterns (Python, shortened)', '''refund = Agent(name="Refund agent", instructions="Handle refunds up to $100; ask a human above that.")
policy = Agent(name="Policy agent", instructions="Answer questions about the refund policy.")

# agents as tools: the manager stays in charge
manager = Agent(name="Support manager",
                tools=[refund.as_tool(tool_name="refund", tool_description="Process a refund"),
                       policy.as_tool(tool_name="policy", tool_description="Look up policy")])

# hand-offs: triage passes control
triage = Agent(name="Triage", handoffs=[refund, policy])''') +
pts(('Tips from the same docs.', ['“Invest in good prompts”, “monitor your app and iterate”, “have specialized agents that excel in one task”, and “invest in evals”.'])))

sec('langgraph', 'LangGraph: supervisor and swarm',
pts(('Supervisor.', ['The langgraph-supervisor library creates a supervisor “to orchestrate multiple specialized agents” with a “tool-based agent handoff mechanism”. Its README now says: “We now recommend using the supervisor pattern directly via tools rather than this library for most use cases. The tool-calling approach gives you more control over context engineering.”']),
('Swarm.', ['langgraph-swarm: “agents dynamically hand off control to one another based on their specializations”, and the system remembers which agent was last active so the next user message goes to it.']),
('Why the shift to tools.', ['Our reading: calling specialists as tools makes it explicit what text goes in and out of each agent, which is the main thing teams need to control (see <a href="context-eng-map.html">context engineering</a>).'])))

sec('crewai', 'CrewAI: crews, processes and flows',
pts(('Crews.', ['Agents with roles, goals and tasks working together; a hierarchical process adds a manager that delegates and checks ⚠️ (process details from our earlier teardown).']),
('Flows.', ['CrewAI’s README: “precise, event-driven control through Flows”, which “combine precise workflow control, single LLM calls, and native support for Crews.” That is the workflow-around-agents mix Anthropic recommends.']),
('More.', ['Our <a href="agentic-crewai.html">CrewAI teardown</a>.'])))

sec('claude', 'Claude’s sub-agents',
pts(('In Claude Code and the Claude Agent SDK.', ['A main agent can start sub-agents for focused work; each has its own context window and returns a summary. That is the agents-as-tools pattern used mainly for context isolation.']),
('In the research system.', ['A lead agent plans, starts 3–5 sub-agents in parallel and synthesises their results; sub-agents return condensed findings. Anthropic notes the lead agent currently runs sub-agents “synchronously, waiting for each set of subagents to complete before proceeding”, which “simplifies coordination, but creates bottlenecks”.']),
('No hand-offs to the user.', ['Sub-agents report back to the main agent rather than taking over the conversation (our reading of the documented behaviour).'])))

sec('context', 'What to pass between agents',
tbl(['Pass this', 'Why', 'Avoid'], [
['The goal and constraints, in the user’s words', 'Specialists otherwise solve a different problem', 'A one-word task like “refund”'],
['What has already been tried', 'Prevents repeated work', 'Full raw history'],
['Exact IDs and data needed (order ID, amount)', 'Specialists need facts, not chat', 'Pasting whole records'],
['What to return and in what shape', 'Manager can combine results', '“Tell me what you find”'],
['Limits: budget, time, tools allowed', 'Keeps sub-work bounded', 'Unlimited delegation']]) +
pts(('Anthropic’s lesson on delegation.', ['Early on, lead agents gave vague instructions such as “research the semiconductor shortage”, and sub-agents duplicated work. Each sub-agent needs “an objective, an output format, guidance on the tools and sources to use, and clear task boundaries” (research system post).'])))

sec('example', 'Worked example: the refund desk (made up)',
tbl(['Turn', 'Supervisor design', 'Hand-off design'], [
['1', 'Manager reads the request, calls <code>policy</code>: “is a broken item eligible?”', 'Triage hands off to Refund agent'],
['2', 'Manager calls <code>refund</code> with order ID and $240', 'Refund agent checks the order; amount over $100'],
['3', 'Refund tool returns “needs human approval”', 'Refund agent hands off to Policy agent to explain escalation'],
['4', 'Manager writes one reply and files the approval request', 'Policy agent replies; may not know the order details unless passed'],
['Result', 'One voice, one owner, more tokens in the manager', 'Focused prompts, but context can drop between hand-offs']]))

sec('mistakes', 'Common mistakes',
pts('Hand-offs without passing the goal and key facts: the next agent starts from scratch.', 'Ping-pong: two agents keep handing control back and forth. Add a hop limit.', 'A supervisor that forwards every token of every worker result into its own window. Ask workers for summaries in a fixed shape.', 'Too many specialists with overlapping jobs: the router or supervisor cannot choose well (same problem as overlapping tools).', 'No owner for the final answer in a swarm: nobody checks the whole.'))

sec('checklist', 'Design checklist',
tbl(['#', 'Check'], [
['1', 'One sentence for each agent’s job; no overlaps'],
['2', 'Decide who talks to the user and who owns the final answer'],
['3', 'Hand-off and delegation messages carry goal, constraints, facts and return format'],
['4', 'Hop or depth limits; a time and token budget per task'],
['5', 'Guardrails at the boundary that matters (manager, or every agent in a swarm)'],
['6', 'Traces show each agent’s input and output'],
['7', 'Evals on the whole task, not just each agent']]))

sec('sources', 'Sources',
pts(A(OAI, 'OpenAI Agents SDK: agent orchestration'), A('https://github.com/openai/openai-agents-python/blob/main/docs/handoffs.md', 'OpenAI Agents SDK: handoffs'), A('https://github.com/langchain-ai/langgraph-supervisor-py', 'LangGraph Supervisor'), A('https://github.com/langchain-ai/langgraph-swarm-py', 'LangGraph Swarm'), A('https://github.com/crewAIInc/crewAI', 'CrewAI'), A('https://www.anthropic.com/engineering/multi-agent-research-system', 'Anthropic: multi-agent research system')))
JS = ''
