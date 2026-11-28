sec('example', 'A worked example: one refund ticket, two windows',
'<p>The same support agent handles the same ticket (“refund my $240 order, it arrived broken”) with two context designs. Token counts are our rough estimates, not measurements.</p>' +
tbl(['Part of the window', 'Unengineered agent', 'Engineered agent'], [
['System prompt', '4,000 tokens: 60 refund rules for edge cases', '900 tokens: the policy with reasons, three examples'],
['Tools', '48 tools from five MCP servers, ~14,000 tokens', '6 tools for support, ~1,500 tokens; others found by tool search'],
['Customer data', 'Full CRM record and 200 past tickets, ~25,000 tokens', '<code>get_customer</code> returns the 10 fields needed, ~400 tokens'],
['Order history', 'Whole order export pasted in', '<code>search_orders</code> returns the one order and a count'],
['Policy documents', 'All 40 pages retrieved up front', 'Refund section fetched when the agent asks'],
['After 12 turns', '~70,000 tokens, earlier tool output still raw', '~9,000 tokens, old results cleared'],
['Outcome risk', 'Picks the wrong of three similar tools; misses the $100 approval rule buried on page 31', 'Policy in view; approval rule in the system prompt']]) +
pts(('What changed.', ['Nothing about the model. Every difference is a choice about what to put in the window. This is why teams often get bigger gains from context work than from switching models (our reading).'])))

sec('roles', 'Who does context engineering in a team',
tbl(['Role', 'Owns', 'Typical change'], [
['Agent / AI engineer', 'Prompts, tools, retrieval, compaction settings', 'Trim tool results; add a skill'],
['Platform team', 'Gateways, caching, MCP servers, shared memory', 'Turn on caching; defer tool definitions'],
['Domain expert', 'The content of policies, examples and project files', 'Rewrite rules as principles with reasons'],
['Eval owner', 'Task sets and metrics', 'Prove a context change did not break success'],
['Forward deployed engineer', 'Customer-specific context: their data, tools and rules', 'Map the customer’s systems into a few clean tools (see <a href="fde-engagement.html">inside an FDE engagement</a>)']]))

sec('glossary', 'Glossary',
tbl(['Term', 'Meaning'], [
['Context window', 'The maximum number of tokens a model can take in one call'],
['Context rot', 'Accuracy and recall falling as the window fills'],
['Attention budget', 'Anthropic’s phrase for the limited focus a model can spread across tokens'],
['Just-in-time context', 'Loading data with tools when needed instead of up front'],
['Progressive disclosure', 'Showing a short summary first and details only when relevant'],
['Compaction', 'Summarising history and continuing in a fresh window'],
['Tool result clearing', 'Replacing old tool outputs with short stubs'],
['Sub-agent', 'A helper agent with its own window that returns a summary'],
['Prompt caching', 'Reusing a processed prompt prefix at a lower price'],
['KV cache', 'Per-token attention data a model keeps while processing a context']]))

sec('faq', 'Questions people ask',
pts(('“With a 1M-token window, can I just put everything in?”', ['You can, and for one-off analysis of a long document it may be fine. For agents that loop, you pay for every token on every call and quality drops as the window fills.']),
('“Is this just RAG?”', ['No. RAG is one way to select context. Context engineering also covers instructions, tools, history, memory, isolation and cost.']),
('“Will better models make this unnecessary?”', ['Anthropic expects less human curation as models improve, but also that long interactions will stay hard: “the challenge of maintaining coherence across extended interactions will remain central.”']),
('“Where do I start?”', ['Measure what fills your window today, trim tool results, then add caching. Those three usually pay off first (our reading).'])))
