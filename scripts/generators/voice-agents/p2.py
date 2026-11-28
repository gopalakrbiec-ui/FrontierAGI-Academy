HERO = 'In conversation people answer each other within a few hundred milliseconds. A voice agent has to come close, while waiting to be sure the caller has finished, transcribing, thinking, maybe calling a tool and speaking. This part breaks that time into stages, shows where it goes on a phone line versus a browser, and goes through the techniques that win back the most milliseconds, with a runnable latency budget.'
CAV = 'Stage timings are our illustrative assumptions, set out in a runnable script; real numbers depend on the vendor, model, region and network. Conversation-gap research is cited from memory and marked ⚠️ (we could not open the papers from our sandbox). Smart Turn and framework details come from their READMEs read on 28 Nov 2026.'

sec('target', 'The target: how fast do people answer?',
pts(('Human turn-taking.', ['Studies across many languages find people usually start replying within a few hundred milliseconds of the other person stopping, often around 200 ms ⚠️ (Stivers et al., 2009; from memory).']),
('What that means for agents (our reading).', ['Matching humans is not realistic for most systems today; around 800 ms from end of speech to first audio feels responsive; beyond about 1.5 seconds callers start repeating themselves or asking “hello?”.']),
('Measure the right thing.', ['The number that matters is “caller stops speaking → caller hears the first syllable”, measured at the caller’s ear, not a model’s time-to-first-token.'])) + MAP)

sec('stages', 'Where the time goes',
tbl(['Stage', 'What happens', 'Our example (ms)'], [
['End-of-turn wait', 'Deciding the caller has finished', '500 (silence timer) / 250 (turn model)'],
['Speech-to-text final', 'Finalising the last words', '150'],
['LLM first token', 'Prompt processing + first output', '450 / 300 with a nearer, faster model'],
['First sentence ready', 'Enough text to start speaking', '150'],
['Text-to-speech first audio', 'First audio chunk generated', '200'],
['Network and codec', 'Browser ~60, phone line ~250', '60–250']]) +
RUN('voice-agents-latency', 'latency_budget.py') +
fig('2-latency.svg', 'Bars for four combinations with and without tuning, against an 800 ms line', 'From the script output.') +
pts(('Reading the output.', ['A cascade over the phone takes 1.7 seconds in our example; tuning turn detection and the model brings it to 1.3.', 'A speech-to-speech model in the browser drops to about 0.6 seconds once tuned; on a phone line, 0.8.', 'The biggest single lever in this model is the end-of-turn wait, not the language model.'])))

sec('turn', 'Win back time: smarter turn detection',
pts(('Why it is the biggest lever.', ['A silence timer must be long enough not to cut people off mid-sentence, so it wastes time on every turn. A turn model can respond sooner when the sentence is clearly finished and wait longer when it is not.']),
('Options.', ['Smart Turn (open, 23 languages, audio-native, “under 100ms on most cloud instances”, run only during silence alongside a VAD such as Silero); LiveKit’s transformer turn detector; turn handling built into realtime models ⚠️.'])))

sec('stream', 'Win back time: stream everything',
pts('Transcribe while the caller speaks, not after.', 'Send text to TTS sentence by sentence as the model produces it; start speaking at the first sentence.', 'Play audio as soon as the first chunk arrives.', 'Keep the system prompt short and cache it (see <a href="context-eng-caching-evals.html">prompt caching</a>): prompt processing is part of the first-token time.'))

sec('filler', 'Win back time: say something while you think',
pts(('Fillers and acknowledgements.', ['“Let me check that for you” while a tool runs. OpenAI’s realtime agents demo shows the realtime agent replying at once and deferring to the supervisor for the tool call, with about two seconds between the end of “give me a moment to check on that” and the answer.']),
('Use sparingly (our reading).', ['Fillers on every turn sound robotic. Use them only when a tool or slow step is coming.'])))

sec('place', 'Win back time: put things close together',
pts('Run the agent in a region near the callers and the phone provider’s media servers.', 'Avoid extra hops: telephony → your server → model → back. Some platforms host the model and media together ⚠️.', 'Prefer WebRTC over WebSockets for browser audio where you can; it is built for real-time media (our reading).', 'Phone calls add codec and network delay you cannot remove; budget for it.'))

sec('interrupt', 'Interruptions (barge-in)',
pts(('What must happen.', ['When the caller starts speaking, stop playback within a fraction of a second, stop generating, and keep track of how much of the reply was actually heard.']),
('Why the last part matters.', ['If the agent said “your refund of $240 will…” and was cut off, its history must not claim it told the caller the full sentence (our reading of a common bug).']),
('False interruptions.', ['Coughs, “mm-hm”, background voices. Turn models and echo cancellation reduce these; some agents treat short backchannels as “keep going” ⚠️.'])))

sec('tools', 'Tools within the budget',
tbl(['Tool latency', 'Strategy'], [
['Under ~300 ms', 'Just call it'],
['0.3–2 s', 'Short filler, then answer'],
['2–10 s', 'Say what is happening, maybe offer to wait or call back'],
['Longer', 'Hand off to a background task and follow up by SMS, email or callback']]) +
'<p>Thresholds are our rule of thumb. Pre-fetch likely data (the caller’s account, recent orders) as soon as the call starts and the number is known.</p>')

sec('measure', 'Measuring latency properly',
pts('Log timestamps for every stage: end of caller speech, final transcript, first token, first audio sent, first audio played.', 'Report p50 and p95, not averages: one 4-second pause per call is what callers remember.', 'Test on real phone lines, not only in the browser.', 'Track latency together with interruptions and “hello?” turns, which are symptoms of slowness.'))

sec('checklist', 'Latency checklist',
tbl(['#', 'Check'], [
['1', 'End-of-turn detection by a turn model, not just a silence timer'],
['2', 'Every stage streams; TTS starts at the first sentence'],
['3', 'Short, cached system prompt; a fast model for the talking'],
['4', 'Fillers only before slow steps'],
['5', 'Region and hops minimised; phone overhead budgeted'],
['6', 'Barge-in stops audio fast and records what was heard'],
['7', 'p95 latency measured at the caller’s ear']]))

sec('sources', 'Sources',
pts(A('https://github.com/pipecat-ai/smart-turn', 'Smart Turn'), A('https://github.com/livekit/agents', 'LiveKit Agents (semantic turn detection)'), A('https://github.com/openai/openai-realtime-agents', 'OpenAI realtime agents demo (chat-supervisor timing)'), 'Stivers et al. (2009), “Universals and cultural variation in turn-taking in conversation”, PNAS ⚠️', 'Script: <code>data/code/voice-agents-latency/latency_budget.py</code>'))
JS = ''
