sec('dashboard', 'An example dashboard',
tbl(['Metric', 'Example', 'Good direction'], [
['Calls per day', '6,200', '—'],
['Containment', '58%', 'Up, with CSAT stable'],
['Task success (checked)', '81%', 'Up'],
['Latency p95 at ear', '1.4 s', 'Down'],
['Transfers: “asked for a person”', '14%', 'Down over time'],
['Repeat calls within 7 days', '9%', 'Down'],
['Cost per handled call', '$0.31', 'Down']]) +
'<p>Values are made up to show the layout.</p>')

sec('rollout', 'Rolling out safely',
tbl(['Stage', 'What', 'Exit when'], [
['Internal', 'Staff call the agent', 'No serious failures in 200 calls'],
['After hours', 'Agent takes calls when no humans are on', 'Containment and CSAT acceptable'],
['Overflow', 'Agent takes calls when queues are long', 'No rise in repeat calls'],
['Front door', 'Agent answers first, humans one step away', 'Stable for a month']]) +
'<p>Our suggested sequence; adapt it to your risk and regulations.</p>')

sec('people', 'What happens to the people',
pts('Human agents handle harder, more emotional calls; training and support for them matter more, not less.', 'New roles appear: conversation designers, call reviewers, voice QA, prompt and policy owners.', 'See our articles on <a href="ai-economy-jobs-evidence.html">AI and jobs</a> and <a href="tech-jobs-offshoring-ai.html">offshoring and AI</a>, which covers contact centres in India and the Philippines.'))

sec('future', 'Where this is heading (our prediction)',
pts('Speech-to-speech becomes the default for talking; text models stay behind it for tools and reasoning.', 'Turn-taking gets close to human speed with audio-native turn models.', 'Indian-language voice agents grow fast as open models cover more languages and code-mixing.', 'Rules on disclosure and AI calls tighten, and voice authentication alone falls out of use.'))
