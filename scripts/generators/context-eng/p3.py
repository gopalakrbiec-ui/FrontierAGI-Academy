HERO = 'A coding migration, a research report or a day-long operations task produces far more tokens than any window holds. This part covers the techniques that keep long tasks coherent: clearing old tool results, compaction, structured notes and memory, and sub-agents with their own windows. It includes a runnable simulation, the API settings that implement each technique, how the main harnesses do it, and how each one fails.'
CAV = 'Techniques and quotes come from Anthropic’s “Effective context engineering for AI agents” and multi-agent research posts and from Claude’s context editing and compaction docs (read 28 Nov 2026); compaction and context editing are marked beta in those docs. The simulation is a toy model with stated assumptions, not a benchmark. Harness behaviour for non-Anthropic tools comes from our earlier teardowns and is marked ⚠️ where we could not re-check it.'
ACE = 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents'

sec('problem', 'Why long tasks break',
pts(('The window fills.', ['Anthropic: long-horizon tasks are those where “the token count exceeds the LLM’s context window”, such as “large codebase migrations or comprehensive research projects”.']),
('Bigger windows are not the answer.', ['“For the foreseeable future, context windows of all sizes will be subject to context pollution and information relevance concerns.”']),
('Three named fixes.', ['Anthropic lists “compaction, structured note-taking, and multi-agent architectures”, plus tool result clearing as the lightest form of compaction.'])) +
fig('6-long-tasks.svg', 'Three techniques with what they are best for and their risks', 'Risks are our reading.') + MAP)

sec('sim', 'A simulation you can run',
'<p>A toy agent runs 40 turns. Each turn adds 300 tokens of model text and a 2,500-token tool result on top of a 6,000-token fixed prefix. The script compares doing nothing with three strategies.</p>' +
RUN('context-eng-long-tasks', 'budget_sim.py') +
fig('3-budget.svg', 'Bar chart of total input tokens by strategy', 'Drawn from the script output.') +
pts(('Reading the output.', ['Doing nothing overflows a 100,000-token window at turn 34 and reads 2.5 million tokens in total.', 'Clearing old tool results cuts total input to about a third and keeps the window under 27,000 tokens.', 'Compaction halves the total but lets the window grow to ~59,000 before each reset.', 'Sub-agents look cheapest for the lead agent, but the script does not count the sub-agents’ own tokens; Anthropic reports multi-agent systems use about 15× the tokens of chat.']),
('Caveat.', ['Real tasks differ: results vary in size, some must be kept, and summaries cost a model call. Use the script’s shape, not its numbers.'])))

sec('clearing', 'Tool result clearing: the lightest touch',
pts(('Idea.', ['Once a tool result has been used deep in the history, the agent rarely needs the raw text again. Replace it with a short stub.']),
('In the Claude API.', ['Context editing (beta header <code>context-management-2025-06-27</code>) offers <code>clear_tool_uses_20250919</code>: clear when input passes a trigger, keep the last N tool uses, clear at least some tokens, and exclude tools such as web search.'])) +
CODE('Context editing settings (Python)', '''context_management={"edits": [{
    "type": "clear_tool_uses_20250919",
    "trigger": {"type": "input_tokens", "value": 30000},   # start clearing above this
    "keep": {"type": "tool_uses", "value": 3},              # keep the last 3 results
    "clear_at_least": {"type": "input_tokens", "value": 5000},
    "exclude_tools": ["web_search"]}]}''', 'shortened from the Claude docs, not executed') +
pts(('Also: thinking clearing.', ['<code>clear_thinking_20251015</code> manages earlier thinking blocks, trading reasoning continuity for space.'])))

sec('compaction', 'Compaction: summarise and continue',
pts(('What it does.', ['Claude’s docs: compaction “replaces the older turns of a conversation with a summary that Claude writes on the server”. Options: compaction on demand (you decide when), at a token threshold (the API decides), or your own summariser.']),
('What to keep.', ['Anthropic’s Claude Code keeps “architectural decisions, unresolved bugs, and implementation details” and drops “redundant tool outputs or messages”, then continues with the summary plus “the five most recently accessed files”.']),
('How to tune it.', ['“Start by maximizing recall to ensure your compaction prompt captures every relevant piece of information from the trace, then iterate to improve precision.”']),
('The risk.', ['“Overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later.”']))+
tbl(['Keep in a summary', 'Drop'], [
['Goal, constraints and the user’s latest decisions', 'Raw command output already acted on'],
['Decisions made and why', 'Exploration that led nowhere (keep one line saying so)'],
['Open bugs, failing tests, next steps', 'Repeated file contents'],
['Names of files, IDs and links to reload', 'Polite back-and-forth']]))

sec('notes', 'Structured notes and memory',
pts(('Agent-written notes.', ['“The agent regularly writes notes persisted to memory outside of the context window. These notes get pulled back into the context window at later times.” A to-do list or NOTES.md is enough.']),
('A memory tool.', ['Anthropic released a file-based memory tool (beta) with Sonnet 4.5 to “store and consult information outside the context window”, so agents can keep project state across sessions.']),
('A good notes file (our template).', ['Goal · done so far · decisions · open questions · next three steps · files that matter. Rewritten, not appended, at each milestone.']),
('See also.', ['Our <a href="../pages/agent-memory.html">agent memory map</a> and <a href="agent-memory-state.html">memory and state</a> article cover longer-term memory stores.'])))

sec('subagents', 'Sub-agents: isolation, at a price',
pts(('Why.', ['Each sub-agent “might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens).” The lead agent keeps a clean window for synthesis.']),
('Evidence.', ['Anthropic’s multi-agent research system (Opus 4 lead, Sonnet 4 sub-agents) beat single-agent Opus 4 by 90.2% on its internal research eval; token usage alone explained 80% of performance variance on BrowseComp.']),
('Cost.', ['“Agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats.” Worth it only when the task’s value pays for it.']),
('Our reading.', ['Use sub-agents for wide, parallel exploration (search, research, reading many files); keep tightly coupled work, such as editing one module, in one agent.'])))

sec('choose', 'Which technique when',
tbl(['Situation', 'Start with', 'Add'], [
['Many large tool results, short task', 'Tool result clearing', '—'],
['Long conversation with a user', 'Compaction', 'Notes for decisions'],
['Multi-hour coding task with milestones', 'Notes / to-do list', 'Compaction, clearing'],
['Broad research across many sources', 'Sub-agents', 'Notes for the lead agent'],
['Work spanning days or sessions', 'Memory tool or notes file', 'Compaction within each session']]) +
'<p>Anthropic’s own summary: compaction for “extensive back-and-forth”, note-taking for “iterative development with clear milestones”, multi-agent for “complex research and analysis where parallel exploration pays dividends”.</p>')

sec('harness', 'How harnesses handle it',
tbl(['Harness', 'Compaction', 'Sub-agents', 'Notes / memory'], [
['Claude Code', 'Automatic and on demand; keeps recent files', 'Yes, with their own windows', 'CLAUDE.md, to-do list'],
['Codex', 'Yes ⚠️', 'Yes ⚠️', 'AGENTS.md ⚠️'],
['Gemini CLI', 'Yes ⚠️', 'Limited ⚠️', 'GEMINI.md ⚠️'],
['Deep Agents (LangChain)', 'Summarisation middleware ⚠️', 'Yes', 'Virtual file system for notes']]) +
'<p>Non-Anthropic rows come from our <a href="agentic-agent-loop.html">agent loop comparison</a> and harness teardowns and were not re-checked today ⚠️.</p>')

sec('fail', 'How long-context agents fail',
tbl(['Failure', 'Sign', 'Fix'], [
['Goal drift', 'Agent solves a different problem after a compaction', 'Put the goal and constraints at the top of every summary and notes file'],
['Lost detail', 'A rejected approach gets tried again', 'Record “tried X, failed because Y” in notes'],
['Summary of a summary', 'Quality falls after several compactions', 'Rebuild from notes plus key files instead of re-summarising'],
['Sub-agent telephone', 'Lead agent acts on a wrong sub-agent summary', 'Ask sub-agents for sources and confidence; spot-check'],
['Runaway cost', 'Tokens grow faster than progress', 'Budget per task; stop and ask a human'],
['Context rot without overflow', 'Quality drops long before the window is full', 'Clear and compact by quality signals, not just size']]))

sec('checklist', 'Long-task checklist',
pts('Set a clearing or compaction trigger well below the window size.', 'Keep a notes file the agent rewrites at milestones.', 'Write the compaction prompt for recall first, then precision; test it on real traces.', 'Use sub-agents for breadth, not for every step.', 'Track tokens, cost and success per task, before and after each change (Part 4).'))

sec('sources', 'Sources',
pts(A(ACE, 'Anthropic: Effective context engineering for AI agents'), A('https://platform.claude.com/docs/en/build-with-claude/context-editing', 'Claude docs: context editing'), A('https://platform.claude.com/docs/en/build-with-claude/compaction', 'Claude docs: compaction'), A('https://www.anthropic.com/engineering/multi-agent-research-system', 'Anthropic: multi-agent research system'), A('https://github.com/langchain-ai/context_engineering', 'LangChain: context_engineering (compress and isolate notebooks)')))
JS = ''
