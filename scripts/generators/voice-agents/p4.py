HERO = 'Running voice agents for real: how to test them with simulated callers, accents and noise; which numbers to watch; what a call minute costs against a human agent, with a runnable calculator; consent, disclosure and voice-cloning risks; and what changes for India’s many languages.'
CAV = 'The cost script uses example prices, not any vendor’s list price. Legal points are general and not legal advice; rules differ by country and change, and we could not check every regulator’s site from our sandbox ⚠️. Language-support details come from project READMEs (Smart Turn, IndicF5) read on 28 Nov 2026.'

sec('test', 'Testing voice agents',
tbl(['Level', 'How', 'Catches'], [
['Text-only', 'Run the agent’s logic on transcripts', 'Wrong answers, policy mistakes, tool errors'],
['Simulated callers', 'An LLM plays the caller, converted to speech, through the full pipeline', 'Turn-taking, interruptions, latency, misheard words'],
['Accent and noise sets', 'Recordings with accents, background noise, phone codecs', 'Speech-to-text failures'],
['Real phone lines', 'Calls through the actual telephony path', 'Codec and network problems'],
['Human review', 'Listen to a sample of real calls weekly', 'Tone, awkwardness, things metrics miss']]) +
pts(('Framework help.', ['LiveKit Agents has a “builtin test framework” to “write tests and use judges”. Pipecat has a real-time debugger (Whisker).'])) + MAP)

sec('metrics', 'What to measure',
tbl(['Metric', 'Meaning', 'Watch for'], [
['Containment', 'Share of calls finished without a human', 'High containment with low satisfaction = callers giving up'],
['Task success', 'Did the caller get what they needed?', 'Measure by checking outcomes, not by the agent’s claim'],
['Latency p95', 'Slow turns at the caller’s ear', 'Spikes at busy hours'],
['Transfers and reasons', 'Why calls went to humans', 'A single step causing most transfers'],
['Interruptions per call', 'Barge-ins and talk-overs', 'Agent too slow or too wordy'],
['Repeat callers', 'Same person calling again within days', 'Hidden failure'],
['CSAT / survey', 'Caller satisfaction', 'Low response rates bias it']]))

sec('cost', 'What a call minute costs',
RUN('voice-agents-production', 'cost_per_minute.py') +
fig('5-cost.svg', 'Bars for voice agent cost parts, total and human agent cost per minute', 'From the script output (example prices).') +
pts(('Reading the output.', ['With these example prices the agent costs about $0.05 a minute against about $0.40 for a human at $18 an hour and 75% occupancy.', 'Because 40% of calls still reach a human, total cost falls to about half, not to an eighth: containment, not the per-minute price, decides the saving.']),
('What the toy model leaves out.', ['Building and maintaining the agent, telephony contracts, quality review, and the cost of bad experiences when the agent fails.'])))

sec('consent', 'Consent, disclosure and the law',
pts(('Tell callers it is an AI.', ['Say so in the greeting. The EU AI Act requires that people be informed when they interact with an AI system (Article 50 transparency duties, applying from August 2026 ⚠️; see our <a href="adlc-release-rollout.html">release article</a>).']),
('Recording and transcripts.', ['Many places require consent or notice before recording; transcripts may be personal data under privacy laws such as GDPR and India’s DPDP Act ⚠️.']),
('Outbound AI calls.', ['In the US, the FCC ruled in 2024 that AI-generated voices in robocalls fall under the TCPA’s consent rules ⚠️ (from memory; check current rules).']),
('Our reading.', ['Treat disclosure, consent and data minimisation as part of the design, not a legal afterthought.'])))

sec('clone', 'Voice cloning and fraud',
pts('Realistic synthetic voices make impersonation easy: callers pretending to be customers, and fake “bank” calls to customers.', 'Do not use voice alone to authenticate callers; add knowledge factors, one-time codes or app confirmation.', 'Use only voices you have rights to; get consent from any person whose voice is cloned.', 'Log and watch for unusual patterns (many calls about one account, scripted-sounding callers).'))

sec('india', 'India: languages, scale and payments',
pts(('Languages.', ['Most callers in India switch between languages, often within one sentence (code-mixing). Check every component: Smart Turn lists Hindi and Bengali among its 23 languages; AI4Bharat’s IndicF5 is an open text-to-speech model for 11 Indian languages (Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu), trained on 1,417 hours of speech (its README).']),
('Government platform.', ['Bhashini, India’s national language translation mission, offers speech and translation services ⚠️ (not opened from our sandbox).']),
('Costs.', ['Lower human-agent costs in India change the maths: at a lower hourly rate, containment must be higher for the agent to pay off. Re-run the cost script with local numbers.']),
('Payments.', ['A voice agent can start a UPI payment, but the payer confirms in their UPI app; see <a href="agent-protocols-payments.html">agent payments</a>.'])))

sec('ops', 'Running it day to day',
tbl(['Task', 'How often'], [
['Listen to a sample of calls', 'Weekly'],
['Review transfer reasons and top failures', 'Weekly'],
['Re-run the test set after any prompt, model or voice change', 'Every change'],
['Check latency p95 by hour and region', 'Daily dashboard'],
['Update knowledge and policies the agent quotes', 'When they change'],
['Review consent and disclosure wording', 'Quarterly, or when laws change']]))

sec('checklist', 'Production checklist',
pts('Disclose AI at the start; follow recording and consent rules.', 'Never authenticate by voice alone.', 'Test with simulated callers, accents, noise and real phone lines.', 'Track containment together with satisfaction and repeat calls.', 'Warm transfer with a summary; humans available.', 'Budget by containment, not just per-minute price.', 'Weekly call review, and re-test after every change.'))

sec('sources', 'Sources',
pts(A('https://github.com/livekit/agents', 'LiveKit Agents (test framework)'), A('https://github.com/pipecat-ai/pipecat', 'Pipecat (Whisker debugger)'), A('https://github.com/pipecat-ai/smart-turn', 'Smart Turn (languages)'), A('https://github.com/ai4bharat/IndicF5', 'AI4Bharat IndicF5'), 'Script: <code>data/code/voice-agents-production/cost_per_minute.py</code>'))
JS = ''
