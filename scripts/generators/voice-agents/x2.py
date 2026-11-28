sec('compare', 'Phone line vs browser vs app',
tbl(['Channel', 'Extra delay (our example)', 'Audio quality', 'Notes'], [
['Browser (WebRTC)', '~60 ms', 'Wideband', 'Echo cancellation built in'],
['Mobile app (WebRTC)', '~60–150 ms', 'Wideband', 'Mobile networks vary'],
['Phone line (PSTN)', '~250 ms', 'Narrowband, compressed', 'Hardest for speech-to-text'],
['SIP from a contact centre', 'Varies', 'Depends on codec', 'Often adds more hops']]) +
'<p>Delays are illustrative; measure your own path.</p>')

sec('trace', 'One turn, traced (illustrative)',
tbl(['Time (ms)', 'Event'], [
['0', 'Caller stops speaking: “…and I want a refund.”'],
['250', 'Turn model: finished'],
['300', 'Final transcript ready'],
['600', 'Model’s first token: “I can help with that.”'],
['700', 'First sentence sent to text-to-speech'],
['850', 'First audio chunk generated'],
['1,100', 'Caller hears “I can…” (phone-line overhead included)'],
['1,150', 'Meanwhile, the order-lookup tool starts']]))

sec('budgeting', 'Setting a latency budget for your team',
pts('Pick a target at the caller’s ear (for example 800 ms p50, 1,500 ms p95; our suggestion).', 'Split it by stage and give each component owner a number.', 'Fail a release if p95 grows beyond the budget on the test set (see <a href="adlc-release-rollout.html">staged rollouts</a>).', 'Re-check after every model or vendor change; a “better” model can be slower.'))

sec('tradeoffs', 'Speed vs quality trade-offs',
tbl(['Faster choice', 'What you may lose'], [
['Smaller, faster model', 'Reasoning on hard questions (use a supervisor model for those)'],
['Shorter end-of-turn wait', 'More cut-offs; mitigated by a turn model'],
['Speaking before the full answer is ready', 'Occasional need to correct course mid-reply'],
['Skipping a tool call', 'Accuracy; answers from memory may be wrong'],
['Lower-quality voice', 'Naturalness and trust']]))
