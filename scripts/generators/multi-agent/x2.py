sec('brief', 'A delegation brief template',
CODE('Brief from a supervisor to a worker (our template)', '''GOAL: Find whether competitor A refunds damaged items without a return, and since when.
WHY: We are updating our refund policy; the user wants to match or beat competitors.
ALREADY KNOWN: Competitor A's policy page (link) says "30-day returns"; no mention of damage.
SOURCES: Competitor A's help centre and terms; news only if dated 2025 or later.
DO NOT: Contact anyone; use more than 15 searches; summarise other competitors.
RETURN: JSON {answer: yes/no/unclear, quote, url, date_checked, confidence 0-1}.
STOP WHEN: You have a quote from an official page, or after 15 searches.''') +
pts(('Why each line.', ['It follows Anthropic’s list (“an objective, an output format, guidance on the tools and sources to use, and clear task boundaries”) and adds why the task matters and when to stop, which prevents both duplicated and endless work.'])))

sec('state', 'Shared state: messages, blackboards and files',
tbl(['Approach', 'How', 'Good for', 'Watch for'], [
['Messages only', 'Agents pass text to each other', 'Small systems', 'Information lost between hops'],
['Shared state object', 'A typed state every agent reads and updates (LangGraph style)', 'Workflows with known fields', 'Agents overwriting each other'],
['Files or a scratchpad', 'Agents write notes and artefacts to shared files', 'Long tasks, code, research', 'Stale or conflicting notes'],
['A task system', 'Tasks with status, owner and results (like A2A tasks)', 'Long-running or cross-team work', 'More infrastructure']]) +
pts(('Our reading.', ['Prefer explicit, typed hand-off messages plus a shared store for large artefacts. Agents should pass references (file path, task ID), not copies of big documents.'])))

sec('loops', 'Stopping rules',
tbl(['Risk', 'Rule'], [
['Hand-off ping-pong', 'Max hops per user turn (e.g. 3); repeat hand-off to the same agent ends the turn'],
['Delegation explosion', 'Max depth (e.g. 2) and max workers per task'],
['Evaluator never satisfied', 'Max rounds (e.g. 3), then return the best draft with the critique'],
['Runaway cost', 'Token budget per task; stop and report when 80% is used'],
['Silent worker', 'Timeout per worker; continue without it and say so']]) +
'<p>The numbers are starting points, not recommendations from any vendor; tune them on your eval set.</p>')

sec('compare2', 'Same feature, different names',
tbl(['Idea', 'OpenAI Agents SDK', 'LangGraph', 'CrewAI', 'Claude'], [
['Call a specialist and get a result back', 'Agents as tools', 'Supervisor via tools', 'Hierarchical manager delegates ⚠️', 'Sub-agents'],
['Pass the conversation to a specialist', 'Handoffs', 'Swarm', '—', '—'],
['Fixed multi-step process', 'Code orchestration', 'Graph', 'Flows / sequential process', 'Code around the SDK'],
['Cross-company agent', 'A2A ⚠️', 'A2A ⚠️', 'A2A ⚠️', 'A2A / MCP']]))
