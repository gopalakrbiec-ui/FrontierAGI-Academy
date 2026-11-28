HERO = 'A voice agent has to answer in under a second, know when the caller has finished, cope with being interrupted, and say everything out loud with no screen to fall back on. This opening part explains what makes voice different from chat, the two ways to build a voice agent, the stack and the companies in it, where voice agents are used, and how we got from “press 1” menus to realtime models.'
CAV = 'Built from public repositories read on 28 Nov 2026 (Pipecat, LiveKit Agents, Smart Turn, OpenAI’s realtime agents, console and Twilio demos, Google’s Live API web console) and dated launches in our lab-updates data, some of which come from secondary sources ⚠️. Vendor documentation sites for OpenAI, Google, ElevenLabs and Deepgram could not be opened from our sandbox. Latency and cost figures in this series are our illustrative models unless a source is named.'

sec('different', 'Why voice is harder than chat',
tbl(['Problem', 'In chat', 'In voice'], [
['Speed', 'A few seconds is fine; text streams in', 'More than about a second of silence feels broken'],
['Turn-taking', 'The user presses send', 'The agent must guess when the caller has finished'],
['Interruptions', 'Rare', 'Callers talk over the agent; it must stop at once'],
['Output', 'Lists, links, tables', 'Only speech: short sentences, numbers read back'],
['Input quality', 'Typed text', 'Accents, noise, phone codecs, crosstalk'],
['Identity', 'Logged-in user', 'Anyone can call; voices can be faked']]) +
pts(('The one-line version (our reading).', ['A voice agent is a chat agent with a hard real-time deadline and a much narrower output channel.'])) + MAP)

sec('arch', 'Two ways to build one',
fig('1-architectures.svg', 'Cascade: caller audio, speech-to-text, LLM, text-to-speech, caller hears. Speech-to-speech: caller audio, realtime model, caller hears', 'Both supported by Pipecat and LiveKit Agents.') +
tbl(['', 'Cascade (STT → LLM → TTS)', 'Speech-to-speech (realtime model)'], [
['How', 'Three models in a pipeline, each streaming', 'One model takes audio in and gives audio out'],
['Latency', 'More hops, each adds delay', 'Fewer hops; usually faster (our reading)'],
['Control', 'You see the transcript and the reply text; swap any part', 'Less visibility in between'],
['Voice quality', 'Pick any TTS voice', 'Keeps tone and emotion from the input ⚠️'],
['Tools', 'Any LLM with tools', 'Realtime models support tools; the OpenAI demo pairs one with a text “supervisor” for harder tool work'],
['Examples', 'Pipecat or LiveKit with STT, LLM and TTS plugins', 'OpenAI gpt-realtime, Gemini Live, Grok Voice ⚠️']]) +
pts(('Hybrid.', ['OpenAI’s realtime agents demo shows a “chat-supervisor” pattern: a realtime model talks to the user and handles simple turns, while “a more intelligent, text-based supervisor model” handles tool calls and harder answers.'])))

sec('stack', 'The stack',
fig('4-stack.svg', 'Six layers: telephony, orchestration framework, speech-to-speech models, speech-to-text, language model, text-to-speech, with example products', 'Our grouping.') +
pts(('Telephony and transport.', ['Phone calls arrive over the public phone network (PSTN) or SIP; browsers and apps use WebRTC or WebSockets. Twilio’s demo with OpenAI opens “a bi-directional stream” from the call to a backend that forwards audio to the model.']),
('Orchestration.', ['Pipecat calls itself “an open-source Python framework for building real-time voice and multimodal conversational agents”; LiveKit Agents builds “realtime, programmable participants that run on servers”, with telephony, semantic turn detection, MCP support and a built-in test framework.']),
('Models.', ['Speech-to-text, a language model and text-to-speech in a cascade, or one realtime speech-to-speech model.'])))

sec('turns', 'The hardest small problem: whose turn is it?',
fig('3-turns.svg', 'Left: silence timer interrupts a caller who paused. Right: turn model waits until the sentence is finished', 'From the Smart Turn README’s description.') +
pts(('Silence is not enough.', ['Smart Turn’s README: most voice agents use voice activity detection (VAD), which “can’t take into account the actual linguistic or acoustic content of the speech”. People pause mid-sentence; a silence timer either cuts them off or waits too long.']),
('Turn models.', ['Smart Turn v3.2 is an open, audio-native model in 23 languages including Hindi and Bengali, running “in as little as 10ms on some CPUs”. LiveKit uses “a transformer model to detect when a user is done with their turn”.'])))

sec('uses', 'Where voice agents are used',
tbl(['Use', 'What the agent does', 'Why voice'], [
['Customer support lines', 'Answers, looks up orders, transfers to humans', 'Customers still phone'],
['Appointments and bookings', 'Checks slots, books, sends confirmation', 'High volume, simple structure'],
['Healthcare intake ⚠️', 'Collects symptoms and details before a visit', 'Staff shortages; strict rules apply'],
['Outbound reminders', 'Calls to confirm or reschedule', 'Cheap at scale; consent rules apply'],
['Assistants in apps and devices', 'Hands-free questions and tasks', 'Driving, cooking, accessibility'],
['Language practice and tutoring', 'Conversation partner', 'Speaking needs speech']]) +
'<p>Adoption figures from vendors are usually company-reported; we do not cite them here.</p>')

sec('history', 'From phone menus to realtime models',
fig('7-timeline.svg', 'Timeline from IVR menus to realtime models and 2026 voice launches', 'Dated launches from our lab-updates data.') +
tbl(['Era', 'What changed'], [
['1990s–2000s', 'IVR menus and keyword recognition: “press or say 1” ⚠️'],
['2011–2016', 'Phone assistants (Siri and others) bring speech recognition to everyone ⚠️'],
['Sep 2022', 'OpenAI releases Whisper, a widely used open speech-to-text model'],
['Oct 2024', 'OpenAI’s Realtime API (DevDay 2024): speech-to-speech for developers'],
['Aug 2025', 'gpt-realtime and the Realtime API reach general availability; Microsoft’s MAI-Voice-1'],
['Oct 2026', 'Grok Voice 3.0, GPT-Live-1.1 in ChatGPT Voice, Mistral’s Voxtral 3 with a voice agent SDK ⚠️ (secondary sources)']]))

sec('choose', 'Which approach to start with',
tbl(['If…', 'Start with'], [
['You need the lowest latency and natural tone', 'A speech-to-speech realtime model'],
['You need full control, audits or a specific voice', 'A cascade'],
['Complex tool use and policies matter most', 'Cascade, or the chat-supervisor hybrid'],
['You need phone calls', 'A framework with telephony (LiveKit, Pipecat with Twilio or SIP)'],
['Many languages, including Indian ones', 'Check language support per component; see Part 4'],
['You just want to try it', 'A provider demo (OpenAI realtime console, Gemini Live web console)']]))

sec('mistakes', 'Five common mistakes',
pts('Reusing a chat prompt: long paragraphs and bullet lists sound terrible when read aloud.', 'A fixed silence timeout for turn-taking: callers get cut off mid-sentence.', 'Ignoring the phone line: codecs and network add hundreds of milliseconds and reduce audio quality.', 'No plan for interruptions: the agent keeps talking after the caller says “no, wait”.', 'No hand-over to a human: the caller is stuck in a loop with a machine.'))

sec('glossary', 'Glossary',
tbl(['Term', 'Meaning'], [
['STT / ASR', 'Speech-to-text / automatic speech recognition'],
['TTS', 'Text-to-speech'],
['Speech-to-speech / realtime model', 'One model that listens and speaks'],
['VAD', 'Voice activity detection: speech or silence?'],
['Turn detection', 'Deciding when the caller has finished'],
['Barge-in', 'The caller interrupting the agent'],
['PSTN / SIP', 'The public phone network / the protocol that connects calls to software'],
['WebRTC', 'Real-time audio and video between browsers and servers'],
['Containment', 'Share of calls finished without a human']]))

sec('sources', 'Sources',
pts(A('https://github.com/pipecat-ai/pipecat', 'Pipecat'), A('https://github.com/livekit/agents', 'LiveKit Agents'), A('https://github.com/pipecat-ai/smart-turn', 'Smart Turn'), A('https://github.com/openai/openai-realtime-agents', 'OpenAI realtime agents demo'), A('https://github.com/openai/openai-realtime-twilio-demo', 'OpenAI Realtime API with Twilio'), A('https://github.com/google-gemini/live-api-web-console', 'Google Live API web console'), 'Launch dates: <a href="../pages/lab-updates.html">Frontier Lab Updates</a>'))
JS = ''
