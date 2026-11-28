HERO = 'Every agent decision is made from whatever sits in its context window at that moment. Context engineering is the work of choosing those tokens: what goes in, what stays out, what gets summarised and what gets handed to someone else. This opening part explains the idea, why bigger windows did not make it go away, what fills a window, the four strategies, and where the subject came from.'
CAV = 'Built from Anthropic’s engineering posts (“Effective context engineering for AI agents”, the Agent Skills post, the multi-agent research system post), Claude’s docs on context windows, prompt caching, context editing and compaction, and LangChain’s context_engineering repository, all read on 28 Nov 2026. We could not open OpenAI’s or Google’s doc sites from our sandbox, so their approaches are described only where we have their sample repos or launch posts. Window shares in the anatomy chart are illustrative.'
ACE = 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents'

sec('what', 'What context engineering is',
pts(('Context is every token the model sees.', ['Anthropic’s definition: context is “the set of tokens included when sampling from a large-language model”, and the engineering problem is “optimizing the utility of those tokens against the inherent constraints of LLMs”.', 'That means the system prompt, tool definitions, project files, retrieved documents, tool results, earlier messages and the model’s own reasoning, not just the instructions you typed.']),
('From prompt engineering to context engineering.', ['Prompt engineering is about writing good instructions once. Anthropic calls context engineering “the natural progression of prompt engineering”: an agent runs in a loop, produces new information every turn, and that information “must be cyclically refined”.', 'In their words, “the curation phase happens each time we decide what to pass to the model”. It is a runtime job, not a one-off writing job.']),
('One-line version.', ['LangChain’s repo quotes Andrej Karpathy: context engineering is the “delicate art and science of filling the context window with just the right information for the next step.”'])) + MAP)

sec('why', 'Why bigger windows did not solve it',
pts(('Context rot.', ['Claude’s context window docs: “As token count grows, accuracy and recall degrade, a phenomenon known as context rot.” Anthropic’s post says the effect “emerges across all models”, gentler in some than others.']),
('An attention budget.', ['Every token can attend to every other, so n tokens make n² pairs; models also saw fewer long sequences in training. Anthropic’s summary: “a performance gradient rather than a hard cliff”, with less precise retrieval and long-range reasoning as the window fills.']),
('Cost and speed.', ['Every token in the window is paid for on every call and adds latency. An agent that re-reads a 100,000-token history forty times pays for four million tokens.']),
('Our reading.', ['Million-token windows are useful, but they raise the ceiling rather than remove the need to choose. The engineering question changes from “will it fit?” to “will it help?”'])))

sec('anatomy', 'What fills a window',
fig('1-anatomy.svg', 'Stacked bar showing system prompt, tool definitions, project file, retrieved documents, tool results, conversation and free space', 'Illustrative mid-task snapshot.') +
tbl(['Part', 'What it is', 'Changes?', 'Typical problem'], [
['System prompt', 'Role, rules, output format', 'Rarely', 'Too vague or a wall of if-then rules'],
['Tool definitions', 'Names, descriptions, input schemas of every tool', 'Rarely', 'Dozens of overlapping tools'],
['Project file / memory', 'CLAUDE.md, AGENTS.md, saved notes', 'Sometimes', 'Stale or bloated instructions'],
['Retrieved documents', 'Search results, files read, RAG chunks', 'Per step', 'Irrelevant chunks crowd out relevant ones'],
['Tool results', 'Command output, API responses, page text', 'Every step', 'Huge raw outputs kept long after use'],
['Conversation and reasoning', 'User turns, model replies, thinking', 'Every step', 'Grows without limit'],
['Free space', 'Room left for the answer and next steps', '—', 'Runs out mid-task']]) +
pts(('Where the waste is.', ['In most agent traces we have looked at, tool results and history are the biggest and the least reused. Anthropic’s post calls clearing old tool results “one of the safest lightest touch forms of compaction”.'])))

sec('principle', 'The guiding principle',
box('Anthropic’s rule', '<p style="margin:6px 0">“Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome.”</p>', 'wr-box sf-quote') +
pts(('Smallest is not shortest.', ['The same post: “minimal does not necessarily mean short; you still need to give the agent sufficient information up front.”']),
('Start minimal, add on failure.', ['“Start by testing a minimal prompt with the best model available… and then add clear instructions and examples to improve performance based on failure modes found during initial testing.”']),
('Do the simplest thing that works.', ['Anthropic expects that “agentic design will trend towards letting intelligent models act intelligently, with progressively less human curation.”'])))

sec('four', 'Four strategies: write, select, compress, isolate',
fig('2-strategies.svg', 'Four boxes: write, select, compress, isolate, with examples', 'The framing used in LangChain’s context engineering notebooks.') +
tbl(['Strategy', 'Question it answers', 'Examples', 'Covered in'], [
['Write', 'What should live outside the window?', 'Notes files, to-do lists, memory tools', '<a href="context-eng-long-tasks.html">Part 3</a>'],
['Select', 'What should come in, and when?', 'Just-in-time retrieval, grep and glob, skills loaded on demand, tool search', '<a href="context-eng-what-goes-in.html">Part 2</a>'],
['Compress', 'How do we keep the gist and drop the bulk?', 'Compaction, tool result clearing, trimming', '<a href="context-eng-long-tasks.html">Part 3</a>'],
['Isolate', 'What deserves its own window?', 'Sub-agents, sandboxes holding large data', '<a href="context-eng-long-tasks.html">Part 3</a>']]) +
pts(('Plus one that is about money.', ['Order the context so the stable part can be cached, which cuts the cost of everything above. That is <a href="context-eng-caching-evals.html">Part 4</a>.'])))

sec('jit', 'Just in time instead of all up front',
pts(('The shift.', ['Many apps embed documents and retrieve chunks before the model runs. Anthropic sees teams adding “just in time” strategies: the agent keeps “lightweight identifiers (file paths, stored queries, web links, etc.)” and loads data with tools when it needs it.']),
('Claude Code as the example.', ['Its CLAUDE.md files are “dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time”. It can query large databases and use <code>head</code> and <code>tail</code> “without ever loading the full data objects into context”.']),
('The trade-off.', ['Exploring at runtime is slower than retrieving pre-computed data, and an agent without good tools and heuristics “can waste context by misusing tools, chasing dead-ends”. Anthropic suggests hybrids for less dynamic content such as legal or finance work.'])))

sec('long', 'Long tasks: three techniques',
fig('6-long-tasks.svg', 'Three boxes: compaction, structured notes, sub-agents', 'Anthropic’s guidance; risks are our reading.') +
pts(('Compaction.', ['Summarise a full window and continue in a fresh one. Claude Code keeps “architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs”, plus the five most recently accessed files.']),
('Structured notes.', ['The agent writes a to-do list or NOTES.md and reads it back after a reset; Anthropic’s Pokémon-playing Claude kept “precise tallies across thousands of game steps”.']),
('Sub-agents.', ['Each explores in a clean window and returns “a condensed, distilled summary of its work (often 1,000-2,000 tokens)”.']),
('More in Part 3.', ['With a runnable simulation comparing all three on the same toy task.'])))

sec('history', 'Where the term came from',
tbl(['When', 'What'], [
['2022–2023', 'Prompt engineering is the main craft: few-shot examples, chain-of-thought, system prompts; RAG becomes the standard way to add knowledge.'],
['2024', 'Tool use and early agents; context windows reach hundreds of thousands, then a million tokens; long-context benchmarks show recall dropping with length.'],
['Mid-2025', '“Context engineering” spreads as a name among agent builders; LangChain publishes its write/select/compress/isolate notebooks ⚠️ (exact date not checked).'],
['Sep 2025', 'Anthropic publishes “Effective context engineering for AI agents” and launches context editing (tool result clearing) and a memory tool with Sonnet 4.5.'],
['Oct 2025', 'Anthropic introduces Agent Skills with progressive disclosure.'],
['By late 2026', 'Server-side compaction (beta) in the Claude API, thinking-block clearing, tool search; harnesses everywhere ship compaction and sub-agents by default (see our <a href="agentic-agent-loop.html">agent loop</a> comparison).']]))

sec('vs', 'How it relates to things you already know',
tbl(['Term', 'Relationship to context engineering'], [
['Prompt engineering', 'A subset: writing the instructions part of the context well'],
['RAG', 'One way to select context; agentic search is another'],
['Agent memory', 'The write side: what is saved outside the window and how it comes back (our <a href="../pages/agent-memory.html">memory map</a>)'],
['Tool design', 'Tools decide how much each result costs in tokens'],
['Multi-agent systems', 'Often justified as context isolation more than as division of labour'],
['Prompt caching', 'The cost side: same context, far cheaper when ordered well']]))

sec('mistakes', 'Five common mistakes',
pts('Treating the window as free storage: pasting whole files, logs or web pages “just in case”.', 'Giving the agent every tool you have: Anthropic warns that “if a human engineer can’t definitively say which tool should be used in a given situation, an AI agent can’t be expected to do better.”', 'Keeping raw tool output forever after it has been used.', 'Putting changing data (timestamps, user IDs) at the top of the prompt, which breaks prompt caching.', 'Changing context without measuring: a smaller window is only better if the task success rate holds.'))

sec('next', 'What the rest of the series covers',
tbl(['Part', 'Focus', 'Interactive'], [
['<a href="context-eng-what-goes-in.html">2</a>', 'System prompts, project files, tools, examples, retrieval, skills, tool search', 'Context budget calculator'],
['<a href="context-eng-long-tasks.html">3</a>', 'Compaction, result clearing, notes, memory, sub-agents, harness comparison', 'Runnable budget simulation'],
['<a href="context-eng-caching-evals.html">4</a>', 'Prompt caching, ordering, KV cache, measuring changes, checklist', 'Runnable caching cost script']]))

sec('sources', 'Sources',
pts(A(ACE, 'Anthropic: Effective context engineering for AI agents'), A('https://platform.claude.com/docs/en/build-with-claude/context-windows', 'Claude docs: context windows'), A('https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills', 'Anthropic: Agent Skills'), A('https://www.anthropic.com/engineering/multi-agent-research-system', 'Anthropic: How we built our multi-agent research system'), A('https://github.com/langchain-ai/context_engineering', 'LangChain: context_engineering notebooks')))
JS = ''
