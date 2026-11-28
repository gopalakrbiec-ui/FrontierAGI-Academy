HERO = 'Several agents can work on one task at once: splitting it into independent parts, answering the same question several times and voting, critiquing each other’s work, or arguing until they agree. This part explains when each helps, why voting helps less than the maths suggests, includes a runnable simulation, and walks through Anthropic’s multi-agent research system as a case study.'
CAV = 'Pattern definitions are quoted from Anthropic’s “Building effective agents”; the case study numbers are as reported in Anthropic’s multi-agent research system post (read 28 Nov 2026). The debate paper (Du et al., 2023) could not be opened from our sandbox; we describe it from its code repository ⚠️. The voting script is a toy model with stated assumptions.'
BEA = 'https://www.anthropic.com/engineering/building-effective-agents'
MAR = 'https://www.anthropic.com/engineering/multi-agent-research-system'

sec('kinds', 'Four ways to put several agents on one task',
tbl(['Kind', 'What runs in parallel', 'How results combine', 'Good for'], [
['Sectioning', 'Different parts of the task', 'Join, merge or synthesise', 'Speed; separate concerns (e.g. answer + guardrail)'],
['Voting', 'The same task, several times', 'Majority, threshold, best-of-n', 'Confidence on checks and classifications'],
['Evaluator–optimizer', 'A generator and a critic, in turns', 'Loop until the critic passes it', 'Writing, translation, search depth'],
['Debate', 'Several agents proposing and rebutting', 'Converge, or a judge decides', 'Factual and reasoning questions']]) + MAP)

sec('sectioning', 'Sectioning: split the work',
pts(('Anthropic’s examples.', ['Guardrails where “one model instance processes user queries while another screens them for inappropriate content”, which “tends to perform better than having the same LLM call handle both”; evals where each call scores a different aspect.']),
('Why it works.', ['“LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect.”']),
('Where it breaks.', ['When parts are not really independent: two parallel agents editing the same file, or researchers who each need the others’ findings.'])))

sec('voting', 'Voting: ask more than once',
pts(('Anthropic’s examples.', ['Reviewing code for vulnerabilities with several prompts; judging whether content is inappropriate with “different vote thresholds to balance false positives and negatives.”'])) +
RUN('multi-agent-parallel-debate', 'voting.py') +
fig('5-voting.svg', 'Bars of majority-vote accuracy for 1, 3, 5 and 9 agents, independent vs correlated', 'From the script output.') +
pts(('Reading the output.', ['With independent mistakes, nine 70%-accurate agents reach 90% by majority vote.', 'When half the time they share one answer (same model, same prompt), nine agents only reach about 80%, for nine times the cost.']),
('What makes votes independent.', ['Different prompts, different models, different tools or evidence. Same-model, same-prompt voting mostly repeats the same mistake (our reading, consistent with the simulation).'])))

sec('evaluator', 'Evaluator–optimizer: generate, critique, repeat',
pts(('When it fits.', ['Anthropic: when “LLM responses can be demonstrably improved when a human articulates their feedback” and “the LLM can provide such feedback”. Examples: literary translation; complex search where the evaluator decides if more searching is needed.']),
('Make the critic useful.', ['Give it the criteria, examples of good and bad, and permission to say “pass”. Cap the number of rounds.']),
('Watch for.', ['A critic that always finds something (endless loops); a critic with the same blind spots as the writer; scores that drift. Our <a href="eval-llm-judges.html">LLM judges</a> article covers judge reliability.'])) +
CODE('Evaluator loop (pseudocode)', '''draft = writer(task)
for round in range(3):                 # hard cap
    verdict = critic(task, draft, criteria)
    if verdict.passed:
        break
    draft = writer(task, draft, verdict.feedback)
return draft, verdict'''))

sec('debate', 'Debate: argue, then decide',
pts(('The idea.', ['Du et al. (2023) proposed having “multiple language model instances propose and debate their individual responses and reasoning processes over multiple rounds to arrive at a common final answer” ⚠️ (wording from memory of the abstract; the repo covers arithmetic, grade-school maths, biographies and MMLU tasks).']),
('When it helps (our reading).', ['Questions with a checkable answer where models can catch each other’s reasoning errors.']),
('Limits.', ['Many rounds multiply cost; agents can converge on a confident wrong answer; a single strong model with a verifier is often cheaper.'])))

sec('case', 'Case study: Anthropic’s research system',
fig('4-research-system.svg', 'Lead agent plans, four sub-agents search in parallel, lead synthesises, citations added', 'Numbers as reported by Anthropic.') +
pts(('Architecture.', ['A lead agent plans and spins up sub-agents that search in parallel; it synthesises their findings; a citation step attributes claims.']),
('Results reported.', ['The multi-agent system with an Opus 4 lead and Sonnet 4 sub-agents “outperformed single-agent Claude Opus 4 by 90.2%” on its internal research eval.', 'Parallelism (3–5 sub-agents, each using 3+ tools in parallel) “cut research time by up to 90% for complex queries”.', 'Token usage explained 80% of performance variance on BrowseComp.']),
('Lessons they report.', ['Prompting for “good heuristics rather than rigid rules”; scaling effort to query complexity; careful delegation instructions; “small changes to the lead agent can unpredictably change how subagents behave.”']),
('What it does not show.', ['That multi-agent helps every task. The same post says coding tasks have fewer parallel parts and costs are about 15× chat.'])))

sec('choose', 'Which to use',
tbl(['Goal', 'Use', 'Cheaper alternative to try first'], [
['Faster answers on wide tasks', 'Sectioning', 'One agent with parallel tool calls'],
['More reliable yes/no checks', 'Voting with diverse prompts or models', 'One stronger model + a rule check'],
['Better quality on open-ended output', 'Evaluator–optimizer', 'A better prompt with examples'],
['Fewer reasoning mistakes', 'Debate or verifier', 'A verifier that checks the answer']]))

sec('cost', 'What it costs',
tbl(['Pattern', 'Calls per task (n agents, r rounds)', 'Wall time'], [
['Sectioning', 'n + 1', '≈ slowest part + combine'],
['Voting', 'n', '≈ one call (parallel)'],
['Evaluator–optimizer', '2r', 'r rounds in sequence'],
['Debate', 'n × r + judge', 'r rounds in sequence']]) +
'<p>Formulas are our simple counts; real systems add tool calls inside each agent.</p>')

sec('checklist', 'Checklist',
pts('Are the parallel parts really independent?', 'Are the voters really different (prompts, models, evidence)?', 'Does the critic have explicit criteria and a round cap?', 'Is there a cheaper single-agent baseline to beat?', 'Is the extra cost worth the gain on your eval set?'))

sec('sources', 'Sources',
pts(A(BEA, 'Anthropic: Building effective agents'), A(MAR, 'Anthropic: How we built our multi-agent research system'), A('https://github.com/composable-models/llm_multiagent_debate', 'Du et al.: multi-agent debate (code)') + ' ⚠️', 'Script: <code>data/code/multi-agent-parallel-debate/voting.py</code>'))
JS = ''
