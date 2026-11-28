sec('patterns', 'Caching patterns for agents',
tbl(['Pattern', 'Breakpoints', 'When'], [
['Static prefix only', 'One, after tools + system prompt + project file', 'Short chats, many users with the same setup'],
['Prefix + growing history', 'One after the prefix, one moving with the latest turn', 'Agent loops: each turn reads the last turn’s cache'],
['Per-tenant context', 'Shared prefix, then one per customer', 'SaaS agents with per-customer documents'],
['Long gaps between turns', 'Use the 1-hour lifetime', 'Agents that wait for tools, humans or approvals']]) +
pts(('Watch the interaction with clearing and compaction.', ['Clearing old tool results or compacting changes earlier parts of the history, so the cached prefix after that point is lost. Claude’s docs mention managing thinking-block clearing alongside prompt caching for this reason. Clear in batches (the <code>clear_at_least</code> setting) rather than a little every turn (our reading).'])))

sec('dashboard', 'An example dashboard',
tbl(['Metric', 'Example value', 'Healthy direction'], [
['Task success on the eval set', '82%', 'Flat or up after a context change'],
['Median input tokens per task', '410k', 'Down'],
['Cache read share of input', '74%', 'Up'],
['Median cost per task', '$0.38', 'Down'],
['Compactions per task', '1.2', 'Stable'],
['Goal-loss incidents after compaction', '2 per 100 tasks', 'Down']]) +
'<p>Values are made up to show the layout. Put cost and success on the same screen so nobody optimises one without the other.</p>')

sec('experiment', 'A worked experiment (illustrative)',
tbl(['Change', 'Success (100 tasks × 3 runs)', 'Cost per task', 'Decision'], [
['Baseline', '78%', '$1.10', '—'],
['Trim tool results to needed fields', '79%', '$0.71', 'Keep'],
['Stable prefix first + caching', '79%', '$0.24', 'Keep'],
['Aggressive compaction at 30%', '71%', '$0.19', 'Reject: success fell'],
['Compaction at 60% + notes file', '80%', '$0.22', 'Keep']]) +
pts(('The lesson.', ['Cheaper is not always better; the aggressive compaction run saved money and lost tasks. These numbers are made up to show the method, not results.'])))

sec('providers', 'Other providers and self-hosting',
pts('OpenAI and Google also offer prompt or context caching with their own rules and prices ⚠️ (we could not open their docs from our sandbox; check minimum lengths, lifetimes and whether caching is automatic).', 'Self-hosted serving engines such as vLLM and SGLang reuse shared prefixes across requests ⚠️; the same rule applies: stable content first.', 'Gateways can add a semantic cache for whole answers, which is different: it skips the model call entirely for similar questions (see our <a href="../pages/llm-gateway.html">LLM gateway map</a>).'))
