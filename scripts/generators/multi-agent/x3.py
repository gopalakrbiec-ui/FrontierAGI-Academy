sec('mixture', 'Mixing models: cheap workers, strong judge',
pts(('The common shape.', ['Many small, cheap workers do the wide work; one stronger model plans, judges or synthesises. Anthropic’s research system used Opus 4 as the lead and Sonnet 4 as sub-agents.']),
('Why it works (our reading).', ['Most tokens are spent reading and searching, which smaller models do well; judgement and synthesis happen once, where the strong model matters most.']),
('Routing again.', ['Anthropic’s routing example sends easy questions to a small model and hard ones to a larger one. The same idea applies inside a multi-agent system: decide per sub-task which model to use (see our <a href="../pages/llm-gateway.html">LLM gateway</a> map for model routing).'])))

sec('guardrail', 'Parallel guardrails, a closer look',
pts(('The pattern.', ['One agent answers; another, in parallel, checks the request (or the draft) for policy problems. If the checker objects, the answer is held.']),
('Why parallel.', ['The user waits only for the slower of the two, not both in sequence; and, per Anthropic, a separate call does the check better than one call doing both jobs.']),
('Design tips (our reading).', ['Give the checker a narrow rubric and a cheap model; log every hold; review holds weekly to fix false positives.'])) +
CODE('Answer and check in parallel (Python, shortened, not executed)', '''answer, verdict = await asyncio.gather(
    run(assistant, user_message),
    run(policy_checker, user_message))
if verdict.blocked:
    return "I can't help with that request."
return answer'''))

sec('research', 'Designing a research team of agents',
tbl(['Decision', 'Choice that worked for Anthropic', 'Our note'], [
['How many sub-agents', 'Scale to the query: one for simple facts, more for broad comparisons', 'Put the scaling rules in the lead agent’s prompt'],
['What each gets', 'Objective, output format, tools and sources, boundaries', 'See the brief template in Part 2'],
['How they search', 'Start wide, then narrow', 'Short broad queries first'],
['How results return', 'Condensed findings to the lead', 'Fixed format makes synthesis easier'],
['Citations', 'A separate step attributes claims to sources', 'Do not trust sub-agent summaries without sources']]))

sec('faq', 'Questions people ask',
pts(('“Is a multi-agent system just an ensemble?”', ['Voting is an ensemble. Sectioning, supervisors and hand-offs are division of labour. They solve different problems.']),
('“Should every agent use a different model?”', ['Only when it helps: diverse models make votes more independent; a cheaper model for wide work saves money. Otherwise one model with different prompts is simpler.']),
('“How many agents is too many?”', ['When you cannot say in one sentence what each does, or when the hand-offs per task keep rising without better results (our reading).'])))
