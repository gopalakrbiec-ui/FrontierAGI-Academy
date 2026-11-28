HERO = 'Context is also a bill. An agent re-reads its whole window on every call, so the same tokens are paid for again and again. This part covers prompt caching and why the order of the context decides whether it works, what the KV cache underneath is doing, and how to measure whether a context change actually helped. It ends with a checklist for the whole series.'
CAV = 'Caching rules and multipliers come from Claude’s prompt caching docs (read 28 Nov 2026): 5-minute cache writes cost 1.25× the base input price, 1-hour writes 2×, cache reads 0.1× on most models (lower on some newer ones). Other providers cache differently and we could not open their docs from our sandbox ⚠️. The cost script uses an example price and assumes every turn arrives within the cache lifetime.'

sec('why', 'Why context costs so much',
pts(('Re-reading.', ['Each call sends the full context. A 40-turn task with a growing window reads the early tokens forty times.']),
('Size × calls.', ['Total cost grows roughly with the square of the number of turns when history is kept, which is why the techniques in <a href="context-eng-long-tasks.html">Part 3</a> matter for money as well as quality.']),
('Latency too.', ['Longer prompts take longer to process before the first output token; caching reduces that as well (Claude docs: “cut costs and latency”).'])) + MAP)

sec('caching', 'Prompt caching in one minute',
pts(('What it is.', ['The provider stores the processed prefix of your prompt. If the next request starts with exactly the same prefix, it reads it from the cache at a fraction of the price.']),
('Claude’s rules (docs).', ['Mark the end of the reusable prefix with <code>cache_control</code>, or use automatic caching.', 'Up to 4 breakpoints, for parts that change at different rates (tools rarely, project context daily).', 'Lifetimes of 5 minutes or 1 hour; writes cost 1.25× or 2× base input, reads 0.1× on most models.', 'A minimum cacheable length (512 to over 1,000 tokens depending on model) and a 20-block lookback window.']),
('The key condition.', ['It matches on the exact prefix. Change one token near the start and everything after it is new.'])))

sec('order', 'Order matters: stable first',
fig('5-cache-order.svg', 'Two rows: timestamp first breaks the cache; tools, system prompt and project file first with a breakpoint caches well', 'Based on Claude’s prompt caching docs.') +
pts(('The docs’ advice.', ['For changing content such as “timestamps, per-request context, the incoming message”, “place the breakpoint at the end of the static prefix, not on the varying block.”']),
('A good order (our reading).', ['Tools → system prompt → project file and stable examples → [breakpoint] → retrieved documents → conversation history → the newest message and anything with a date or ID.']),
('Common cache breakers.', ['A timestamp or request ID in the system prompt; tools listed in a different order each call (MCP’s 2026-07-28 revision now asks servers to list tools in a deterministic order for this reason, see our <a href="agent-protocols-mcp.html">MCP article</a>); per-user text near the top; editing earlier messages.'])))

sec('script', 'The cost difference, measured on a toy run',
RUN('context-eng-caching-evals', 'cache_cost.py') +
pts(('Reading the output.', ['Same 40-turn task, three layouts. Putting a changing timestamp at the top is worse than no caching (every call pays the write premium and never reads). Putting the stable prefix first cuts the bill to about 15%.']),
('Assumptions.', ['$3 per million input tokens (example), standard 0.1× reads, every turn within the 5-minute lifetime, output tokens not counted. With long gaps between turns, the 1-hour cache or a fresh write changes the picture.'])))

sec('kv', 'Under the hood: the KV cache',
pts(('What the model stores.', ['For every token in the context, each attention layer keeps key and value vectors: the KV cache. Prompt caching across requests is, roughly, keeping that work so it does not have to be recomputed ⚠️ (providers do not publish exact implementations).']),
('Why it limits windows.', ['KV cache memory grows with context length, layers and heads, which is why long contexts are expensive to serve. Our <a href="transformer-upgrades.html">transformer upgrades</a> article has a KV-cache calculator, and <a href="../pages/llm-api-journey.html">What happens when you call an LLM API</a> shows prefill and decode.']),
('What that means for you.', ['Shorter, stable prefixes are cheaper for the provider to keep, which is why caching is priced the way it is.'])))

sec('measure', 'Measuring whether a context change helped',
pts(('Measure outcomes, not tokens alone.', ['A smaller window that fails more tasks is a loss. Track task success, tokens per task, cost per task, latency and the number of steps together.']),
('A simple protocol (our reading).', ['Fix an eval set of 30–100 real tasks (see <a href="adlc-requirements-evals.html">ADLC Part 3</a>).', 'Run the current context setup and the change on the same tasks, several times each, since agents are not deterministic.', 'Compare success with a confidence interval (our <a href="adlc-test-evaluation.html">Wilson-interval calculator</a>), then cost and steps.', 'Keep the change only if success holds and cost falls, or success rises at an acceptable cost.']),
('Useful signals in traces.', ['Tokens per turn over time; how often the agent re-reads the same file; compaction count; cache read share; “lost” goals after compaction.'])))

sec('table', 'What each technique costs and saves',
tbl(['Technique', 'Saves', 'Costs', 'Risk'], [
['Lean system prompt and project file', 'Every call', 'Writing effort', 'Missing guidance'],
['Fewer, clearer tools; deferred definitions', 'Every call', 'Tool redesign; a search step', 'Agent misses a tool'],
['Trimmed tool results', 'Every later call', 'Tool changes', 'Dropping needed fields'],
['Tool result clearing', 'Long tasks', 'Re-fetching when needed', 'Low'],
['Compaction', 'Long tasks', 'A summary call', 'Lost detail'],
['Notes and memory', 'Long and multi-session tasks', 'Write and read steps', 'Stale notes'],
['Sub-agents', 'Lead agent’s window', 'Many more total tokens', 'Bad summaries'],
['Prompt caching', 'The re-read prefix (85% on our toy run)', 'Write premium', 'Broken by ordering']]))

sec('india', 'A note on cost-sensitive markets',
pts('For teams paying in rupees or serving price-sensitive users, caching and lean context are often the difference between a viable product and not. Our <a href="frontier-lab-startup-playbook.html">start-up playbook</a> has serving and agent cost calculators to put these savings into a budget.', 'Open-weight models served yourself (vLLM, SGLang) support prefix caching as well ⚠️ (check your server’s docs); the same ordering rules apply.'))

sec('checklist', 'The whole series as one checklist',
tbl(['Stage', 'Check'], [
['Before the agent starts', 'Right-altitude system prompt; lean project file; few clear tools; canonical examples'],
['During each step', 'Just-in-time retrieval; trimmed tool results; skills and tools loaded on demand'],
['Long tasks', 'Clearing trigger; compaction tuned for recall; notes file; sub-agents for breadth'],
['Cost', 'Stable prefix first; cache breakpoints; no timestamps at the top'],
['Quality', 'Eval set; repeated runs; success, cost and steps compared before shipping']]))

sec('sources', 'Sources',
pts(A('https://platform.claude.com/docs/en/build-with-claude/prompt-caching', 'Claude docs: prompt caching'), A('https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents', 'Anthropic: Effective context engineering for AI agents'), A('https://platform.claude.com/docs/en/build-with-claude/context-windows', 'Claude docs: context windows'), 'Script: <code>data/code/context-eng-caching-evals/cache_cost.py</code>'))
JS = ''
