sec('template', 'A system prompt template',
CODE('System prompt skeleton (our template)', '''<role>You are the refund assistant for Acme's support team.</role>

<goal>Resolve refund requests correctly and quickly. A correct "no" is better than a wrong "yes".</goal>

<policy>
- Refund up to $100 when the order record shows the item was damaged or not delivered.
- Above $100, prepare the case and ask a human to approve. Why: larger refunds are often disputed.
- Never promise a refund before the tool confirms it.
</policy>

<tools>
- get_customer: first, to confirm who you are talking to.
- search_orders: find the order; ask for the order number if several match.
- issue_refund: only after the checks above.
</tools>

<output>One short reply to the customer, then a one-line internal note.</output>

<examples>(3 short, different cases)</examples>''') +
pts(('Why this shape.', ['Rules come with reasons, so the model can handle cases nobody listed; tools come with when-to-use guidance; examples are few and different. Anthropic’s advice is to start minimal like this and add only what testing shows is missing.'])))

sec('mcp', 'MCP servers and context',
pts(('Every connected server adds tool definitions.', ['MCP makes it easy to connect many servers; each one brings its tools into the window. Connecting “everything” is the fastest way to a bloated tool set.']),
('What helps.', ['Connect per task or per sub-agent; use a gateway or tool search to expose only what is needed; ask server authors for compact results. MCP’s 2026-07-28 revision adds caching hints and asks servers to list tools in a deterministic order, which also helps prompt caching (our <a href="agent-protocols-mcp.html">MCP article</a>).']),
('Disclosure.', ['MCP was introduced by Anthropic.'])))

sec('agentic', 'Agentic search in practice',
tbl(['Data', 'Good tools to give the agent', 'Why'], [
['A codebase', 'glob, grep, read file with line ranges', 'Fresh every time; no index to go stale'],
['A large database', 'Read-only SQL with row limits', 'The agent fetches counts and samples, not tables'],
['Logs', 'Search by time and service; head/tail', 'Avoids loading gigabytes'],
['Company documents', 'Search returning titles and snippets, then read one', 'Agent chooses what to open'],
['The web', 'Search plus fetch of readable text', 'Pages trimmed before they reach the model']]) +
pts(('A pattern worth copying.', ['Return a small preview plus a handle (file path, query ID, URL). The agent decides whether to load more. This is Anthropic’s “lightweight identifiers” idea made concrete.'])))

sec('mistakes2', 'Mistakes we see in real setups',
tbl(['Mistake', 'Effect', 'Fix'], [
['Project file copied from another repo', 'Wrong commands, wasted tokens every call', 'Write it from scratch; keep it short'],
['One tool per API endpoint', 'Dozens of near-duplicates', 'Design tools around tasks'],
['Returning JSON with every field', 'Thousands of tokens per call', 'Select fields; summarise lists'],
['Examples that all look alike', 'Model overfits one pattern', 'Pick examples that differ in what matters'],
['Retrieval on by default for every turn', 'Irrelevant chunks every time', 'Let the agent decide when to search']]))

sec('compare', 'How other stacks describe the same ideas',
tbl(['Source', 'Their words', 'Same as'], [
['LangChain notebooks', 'Write, select, compress, isolate', 'Parts 2 and 3 of this series'],
['Anthropic', 'Smallest set of high-signal tokens; just-in-time; compaction; notes; sub-agents', 'The whole series'],
['OpenAI sample apps', 'Models that write code to act, returning “only the text or screenshots it needs”', 'Trimmed tool results (see our <a href="computer-use-labs.html">computer-use labs</a> article)'],
['Coding-agent project files', 'CLAUDE.md, AGENTS.md, GEMINI.md ⚠️', 'Up-front context']]))
