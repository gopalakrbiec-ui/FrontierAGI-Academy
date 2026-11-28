sec('prompt', 'A compaction prompt you can start from',
CODE('Compaction prompt (our template)', '''Summarise this agent session so a fresh copy of you can continue with no other context.
Keep, in this order:
1. The user's goal and constraints, in their words.
2. Decisions made and the reason for each.
3. What was tried and failed, and why (one line each).
4. Current state: files changed, tests passing or failing, open bugs.
5. The next three steps.
6. Exact names: files, IDs, URLs, commands that matter.
Drop raw tool output, repeated file contents and small talk.
Prefer keeping a detail you are unsure about over dropping it.''') +
pts(('Why it is written this way.', ['It follows Anthropic’s advice to tune for recall first: the last line tells the summariser to err on the side of keeping. Test it on real traces and check what the agent forgets after a reset.'])))

sec('trace', 'One long task, step by step (illustrative)',
tbl(['Step', 'Window', 'What happens'], [
['Turn 1', '8k', 'System prompt, tools, project file; task: migrate 40 files to a new API'],
['Turns 2–12', '8k → 45k', 'Agent greps, reads files, edits, runs tests; results pile up'],
['Turn 13', '45k → 22k', 'Clearing removes raw results older than the last 3'],
['Turns 14–30', '22k → 70k', 'More edits; the agent keeps NOTES.md: 25 of 40 done, two tricky cases'],
['Turn 31', '70k → 12k', 'Compaction: summary + NOTES.md + the five recent files'],
['Turns 32–40', '12k → 40k', 'Finishes the remaining files; reads NOTES.md to recall the tricky cases'],
['Turn 41', '—', 'A sub-agent reviews all 40 diffs in its own window and returns a 1,500-token report']]) +
pts(('Our reading.', ['The three techniques work best together: clearing is cheap and frequent, compaction is occasional, notes carry what must survive both, and a sub-agent handles a wide review.'])))

sec('budget2', 'Setting the triggers',
tbl(['Setting', 'Starting point (our reading)', 'Why'], [
['Tool result clearing trigger', '25–35% of the window', 'Cheap; keeps the working window small'],
['Results kept after clearing', '3–5 most recent', 'Enough for the current step'],
['Compaction trigger', '50–70% of the window', 'Leaves room for the summary call and the answer'],
['Notes rewrite', 'At each milestone or before compaction', 'Notes are what survives'],
['Sub-agent summary size', '1,000–2,000 tokens', 'Anthropic’s reported range']]) +
'<p>Tune these on your own eval set; the right numbers depend on how large your tool results are and how much the task depends on early details.</p>')

sec('multisession', 'Across sessions and days',
pts(('The window resets every session.', ['Anything the agent must know tomorrow has to be written somewhere: a notes file in the repo, a memory tool, a ticket comment.']),
('Patterns.', ['Session handoff note at the end of each session; a project file updated when conventions change; a memory store for user preferences.']),
('Watch for staleness.', ['Old notes can mislead more than no notes. Date them, and prune at milestones.']),
('This site does it too.', ['Our own builds rely on CLAUDE.md as the memory between sessions; it is long, so the agent searches it rather than reading it all.'])))
