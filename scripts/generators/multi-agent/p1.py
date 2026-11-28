HERO = 'Two agents are not always better than one. This opening part lays out the eight common ways to arrange agents (chains, routers, parallel voting, evaluator loops, supervisors, hand-offs, debate and hierarchies), what each is for, which frameworks support it, and the first question to ask: should this be multi-agent at all?'
CAV = 'Pattern definitions come from Anthropic’s “Building effective agents” and multi-agent research posts, the OpenAI Agents SDK orchestration docs, and the READMEs of LangGraph Supervisor, LangGraph Swarm, CrewAI and AutoGen, read on 28 Nov 2026. Research results (multi-agent debate, the MAST failure study) are cited from their repositories; we could not open the papers themselves from our sandbox, so their details are marked ⚠️.'
BEA = 'https://www.anthropic.com/engineering/building-effective-agents'
MAR = 'https://www.anthropic.com/engineering/multi-agent-research-system'
OAI = 'https://github.com/openai/openai-agents-python/blob/main/docs/multi_agent.md'

sec('first', 'First question: do you need more than one agent?',
pts(('Start simple.', ['Anthropic: “we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all.” For many applications “optimizing single LLM calls with retrieval and in-context examples is usually enough.”']),
('What multi-agent costs.', ['In Anthropic’s data, agents use about 4× the tokens of chat and multi-agent systems about 15×. Every extra agent adds calls, waiting and places to fail.']),
('When it pays.', ['Anthropic found multi-agent systems “excel at valuable tasks that involve heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools.”']),
('When it does not.', ['Domains “that require all agents to share the same context or involve many dependencies between agents are not a good fit”; “most coding tasks involve fewer truly parallelizable tasks than research.”'])) + MAP)

sec('two', 'Workflows and agents: who decides',
fig('2-spectrum.svg', 'A line from code-decides patterns on the left to model-decides patterns on the right', 'Placement is our reading.') +
pts(('Two kinds of system.', ['Anthropic: “Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage.”', 'OpenAI’s SDK docs make the same split: “Orchestrating via LLM” versus “Orchestrating via code”, adding that code orchestration “makes tasks more deterministic and predictable, in terms of speed, cost and performance.”']),
('Mix them.', ['Real systems combine both: code decides the big steps, an agent decides inside a step. OpenAI: “You can mix and match these patterns.”'])))

sec('catalogue', 'The eight patterns',
fig('1-catalogue.svg', 'Eight small diagrams: chain, router, parallel, evaluator-optimizer, supervisor, hand-offs, debate, hierarchy', 'Names follow Anthropic, OpenAI and LangGraph documentation.') +
tbl(['Pattern', 'How it works', 'Use when', 'Main risk'], [
['Chain', 'Each step processes the previous output; code gates between steps', 'The task splits into fixed steps', 'Errors compound along the chain'],
['Router', 'Classify the input, send it to one specialist', 'Distinct categories handled differently', 'Misrouting'],
['Parallel / vote', 'Split into independent parts, or run the same task several times', 'Speed, or more confidence', 'Cost; correlated mistakes'],
['Evaluator–optimizer', 'One generates, another critiques, loop', 'Clear criteria and feedback helps', 'Endless loops; judge blind spots'],
['Supervisor (agents as tools)', 'A manager calls specialists and writes the answer', 'One agent should own the result', 'Manager bottleneck; context bloat'],
['Hand-offs / swarm', 'Control passes to whichever agent fits', 'Specialists should talk to the user directly', 'Lost context; ping-pong'],
['Debate', 'Agents argue over rounds; a judge or vote decides', 'Factual or reasoning checks', 'Cost; agreeing on a wrong answer'],
['Hierarchy', 'Supervisors of supervisors', 'Very large tasks with sub-teams', 'Telephone effect; latency']]))

sec('workflows', 'The workflow patterns, from Anthropic’s guide',
pts(('Prompt chaining.', ['Each call “processes the output of the previous one”, with “programmatic checks” as gates. Ideal when the task “can be easily and cleanly decomposed into fixed subtasks.”']),
('Routing.', ['“Classifies an input and directs it to a specialized followup task.” Example: support queries split into general, refund and technical, or easy questions to a small model and hard ones to a large one.']),
('Parallelization.', ['Two forms: “sectioning” (independent subtasks in parallel) and “voting” (“running the same task multiple times to get diverse outputs”).']),
('Orchestrator-workers.', ['“A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results.” Unlike parallelization, “subtasks aren’t pre-defined”.']),
('Evaluator-optimizer.', ['“One LLM call generates a response while another provides evaluation and feedback in a loop.” Good fit when human feedback would demonstrably improve the output and an LLM can give that feedback.'])))

sec('agents', 'The agent patterns',
pts(('Supervisor / agents as tools.', ['OpenAI SDK: “A manager agent keeps control of the conversation and calls specialist agents through <code>Agent.as_tool()</code>.” LangGraph’s supervisor library builds “hierarchical multi-agent systems”, and now recommends doing this “directly via tools” for more control over context.']),
('Hand-offs / swarm.', ['OpenAI SDK: “A triage agent routes the conversation to a specialist, and that specialist becomes the active agent.” LangGraph Swarm: agents “dynamically hand off control to one another based on their specializations.”']),
('Debate.', ['Du et al. (2023) proposed multiple model instances proposing and debating answers over several rounds to improve factuality and reasoning ⚠️ (paper not opened; code repo read).']),
('Group chat and crews.', ['AutoGen popularised conversational group chats of agents; it is now archived, with Microsoft Agent Framework as its successor. CrewAI organises agents into Crews, with Flows for event-driven control.'])))

sec('frameworks', 'Which frameworks support which pattern',
tbl(['Pattern', 'OpenAI Agents SDK', 'LangGraph', 'CrewAI', 'Claude Agent SDK / Claude Code', 'Google ADK'], [
['Chain', 'Code', 'Graph edges', 'Sequential process, Flows', 'Code', 'Sequential agent ⚠️'],
['Router', 'Structured output + code', 'Conditional edges', 'Flows', 'Code', 'Yes ⚠️'],
['Parallel', '<code>asyncio.gather</code>', 'Parallel branches', 'Async tasks ⚠️', 'Parallel sub-agents', 'Parallel agent ⚠️'],
['Evaluator loop', 'While loop (docs)', 'Cycles', 'Flows', 'Code', 'Loop agent ⚠️'],
['Supervisor', '<code>Agent.as_tool()</code>', 'Supervisor via tools', 'Hierarchical process', 'Sub-agents (Task tool)', 'Agents as tools ⚠️'],
['Hand-offs', 'Handoffs', 'Swarm library', '—', '—', 'Transfers ⚠️']]) +
'<p>⚠️ cells come from our earlier framework teardowns and were not re-checked today. See <a href="agentic-frameworks-compared.html">agent frameworks compared</a>.</p>')

sec('choose', 'A quick chooser',
tbl(['If…', 'Start with'], [
['The steps are known in advance', 'Chain'],
['Inputs fall into clear types', 'Router'],
['Parts are independent, or you need a second opinion', 'Parallel / vote'],
['Quality improves with critique and you can state the criteria', 'Evaluator–optimizer'],
['One agent should own the answer but needs specialists', 'Supervisor'],
['Specialists should take over the conversation', 'Hand-offs'],
['The work is huge and naturally splits into teams', 'Hierarchy (rarely needed)'],
['None of the above clearly applies', 'One good agent with good tools']]))

sec('example', 'One task, four designs (illustrative)',
'<p>Task: “Compare our refund policy with three competitors and draft an update.” Call counts and timings are our rough estimates.</p>' +
tbl(['Design', 'Model calls', 'Wall time', 'Notes'], [
['One agent', '~25', 'Long, sequential', 'Simple; context fills with four websites'],
['Chain (research → compare → draft → check)', '~28', 'Long', 'Easy to test each step'],
['Supervisor + 3 parallel researchers', '~40', 'Shorter', 'Clean windows per competitor; more tokens'],
['Hand-offs between researcher, analyst, writer', '~35', 'Long', 'Risk of losing the user’s constraints between agents']]) +
pts(('Our reading.', ['The supervisor with parallel researchers fits this task best: the parts are independent and each needs its own reading. The chain is a close second if predictability matters more than speed.'])))

sec('history', 'A short history',
tbl(['When', 'What'], [
['2023', 'Research systems explore role-play and multi-agent collaboration (CAMEL, ChatDev, MetaGPT, AutoGen) ⚠️ (dates from memory); multi-agent debate paper.'],
['Dec 2024', 'Anthropic’s “Building effective agents” names the workflow patterns and urges simplicity.'],
['Mar 2025', 'OpenAI Agents SDK with handoffs and agents-as-tools (our lab-updates data); MAST failure taxonomy paper ⚠️.'],
['2025', 'LangGraph supervisor and swarm libraries; Anthropic publishes its multi-agent research system; A2A launched for cross-company agents.'],
['2026', 'AutoGen archived in favour of Microsoft Agent Framework; frameworks converge on supervisor-via-tools and hand-offs; harnesses ship sub-agents by default.']]))

sec('glossary', 'Glossary',
tbl(['Term', 'Meaning'], [
['Orchestration', 'Deciding which agent runs, in what order, and what comes next'],
['Supervisor / orchestrator', 'An agent that plans and delegates to workers'],
['Worker / specialist', 'An agent with a narrow job and tools'],
['Hand-off', 'Passing control of the conversation to another agent'],
['Agents as tools', 'Calling another agent like a function and getting its result back'],
['Swarm', 'Agents passing control among themselves without a central manager'],
['Sectioning / voting', 'Parallel split of a task / parallel repeats of the same task'],
['Evaluator', 'An agent or model that scores and critiques another’s output']]))

sec('sources', 'Sources',
pts(A(BEA, 'Anthropic: Building effective agents'), A(MAR, 'Anthropic: How we built our multi-agent research system'), A(OAI, 'OpenAI Agents SDK: agent orchestration'), A('https://github.com/langchain-ai/langgraph-supervisor-py', 'LangGraph Supervisor'), A('https://github.com/langchain-ai/langgraph-swarm-py', 'LangGraph Swarm'), A('https://github.com/crewAIInc/crewAI', 'CrewAI'), A('https://github.com/microsoft/autogen', 'AutoGen (archived)'), A('https://github.com/composable-models/llm_multiagent_debate', 'Multi-agent debate (code)') + ' ⚠️', A('https://github.com/multi-agent-systems-failure-taxonomy/MAST', 'MAST failure taxonomy (code and data)') + ' ⚠️'))
JS = ''
