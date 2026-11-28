HERO = 'How to actually build a voice agent: the realtime APIs from the labs, the open-source frameworks that handle audio, turn-taking and interruptions for you, connecting to a phone line, tool calls mid-conversation, handing over to a human, and writing prompts for the ear rather than the eye.'
CAV = 'Read from public repositories on 28 Nov 2026: OpenAI’s realtime agents, realtime console and Twilio demos; Google’s Live API web console; Pipecat; LiveKit Agents. API details on vendor doc sites could not be opened from our sandbox, so method names are kept general and code is shortened and not executed. The worked example is made up.'

sec('options', 'Three ways to start',
tbl(['Route', 'You get', 'You handle', 'Good for'], [
['A lab’s realtime API directly', 'Speech-to-speech model, tools, a session over WebSocket or WebRTC', 'Audio plumbing, telephony, turn and interruption edge cases', 'Prototypes; teams committed to one lab'],
['An open-source framework', 'Pipelines, transports, turn detection, interruptions, many model plugins', 'Hosting and scaling', 'Most production builds'],
['A hosted voice-agent platform', 'Everything, including phone numbers and dashboards ⚠️', 'Less control, per-minute fees', 'Fast launches, small teams']]) + MAP)

sec('realtime', 'Realtime APIs from the labs',
pts(('OpenAI.', ['The Realtime API reached general availability with gpt-realtime in August 2025 (our lab-updates data). OpenAI’s realtime console is a reference app for inspecting events; its realtime agents demo uses the Agents SDK for two patterns: “Chat-Supervisor” and “Sequential Handoff”, where “specialized agents (powered by realtime api) transfer the user between them”.']),
('Google.', ['The Live API web console is “a react-based starter app for using the Live API over a websocket”, with streaming audio playback and recording; its demos include “proactive audio” and tool use such as Google Search grounding.']),
('Others.', ['xAI (Grok Voice), Microsoft (MAI-Voice), Mistral (Voxtral and a voice agent SDK) shipped voice models in 2025–26 ⚠️ (secondary sources in our data). Anthropic’s Claude apps have voice conversations; we did not find a speech-to-speech developer API in the docs we could open ⚠️.'])))

sec('frameworks', 'Open-source frameworks',
tbl(['', 'Pipecat', 'LiveKit Agents'], [
['What it is', 'Python framework for real-time voice and multimodal agents', '“Realtime, programmable participants that run on servers”'],
['Transports', 'WebSockets, WebRTC and more', 'LiveKit’s WebRTC server; SIP telephony stack'],
['Models', 'Pluggable STT, LLM, TTS and realtime services', '“Mix and match the right STT, LLM, TTS, and Realtime API”'],
['Turn-taking', 'Smart Turn (from the Pipecat ecosystem)', 'Semantic turn detection model'],
['Structure', 'Pipecat Flows for structured conversations; multi-agent hand-offs and fan-out', 'Job dispatch; MCP tools; built-in tests with judges'],
['Licence', 'Open source', 'Open source, self-hostable']]) +
CODE('A cascade pipeline (Pipecat-style, shortened)', '''pipeline = Pipeline([
    transport.input(),          # caller audio in
    stt,                        # streaming speech-to-text
    context_aggregator.user(),  # add the caller's turn to the conversation
    llm,                        # language model with tools
    tts,                        # streaming text-to-speech
    transport.output(),         # audio back to the caller
    context_aggregator.assistant()])''', 'shape of a Pipecat pipeline, shortened, not executed'))

sec('phone', 'Connecting a phone line',
pts(('The Twilio + OpenAI demo, step by step.', ['A call reaches a Twilio number; Twilio asks your webhook for TwiML instructions; the TwiML tells Twilio to open “a bi-directional stream” to your WebSocket server; the server forwards audio between the call and the Realtime API and sends transcripts to a web page.'])) +
CODE('TwiML from the demo', '''<Response>
  <Say>Connected</Say>
  <Connect>
    <Stream url="{{WS_URL}}" />
  </Connect>
  <Say>Disconnected</Say>
</Response>''', 'from the openai-realtime-twilio-demo README') +
pts(('Other routes.', ['SIP trunks into LiveKit or another media server; phone numbers from a voice-agent platform ⚠️. Phone audio is narrowband and compressed; test your speech-to-text on real calls.'])))

sec('toolsmid', 'Tool calls mid-conversation',
pts('Keep tools few and fast; voice magnifies latency (see <a href="voice-agents-latency.html">Part 2</a>).', 'Say what you are doing before a slow tool, not after.', 'Confirm before actions that change things: “I’ll refund $80 to your card ending 4412. Shall I go ahead?”', 'Read numbers back in groups (“four seven, two nine”), and spell names when it matters.', 'Never read out full card numbers or secrets; use the last few digits.'))

sec('handover', 'Handing over to a human',
pts(('Warm transfer.', ['Pass a short summary (who, what, what was tried) to the human and, ideally, play it to them before connecting, so the caller does not repeat everything.']),
('When to transfer (our reading).', ['The caller asks for a person; the agent fails twice at the same step; the request is above a limit; strong emotion or a safety issue; low confidence in the transcript.']),
('Patterns.', ['The OpenAI demo’s sequential hand-off shows agent-to-agent transfer; the same idea with a human queue at the end is the usual production design (see <a href="multi-agent-supervisor-handoff.html">supervisors and hand-offs</a>).'])))

sec('prompt', 'Writing for the ear',
CODE('Voice system prompt excerpt (our template)', '''You are speaking on a phone call. Everything you write is read aloud.
- Use short sentences. One question at a time.
- No lists, markdown, emojis or URLs. Say "I'll text you the link" instead.
- Read numbers in small groups. Confirm amounts and dates before acting.
- If you didn't catch something, ask once, then offer to transfer.
- Start with: "Hi, this is Acme's automated assistant." Never claim to be human.''') +
pts(('Why.', ['Chat habits (bullet lists, long paragraphs, “here are five options”) are hard to follow by ear. Spoken interfaces need fewer choices per turn (our reading).'])))

sec('example', 'Worked example: the refund line (made up)',
fig('6-call.svg', 'Seven steps from greeting to warm transfer', 'Illustrative flow.') +
tbl(['Step', 'Agent says or does'], [
['Greet', '“Hi, this is Acme’s automated assistant. How can I help?”'],
['Verify', 'Asks for the order number and postcode; reads them back'],
['Listen', 'Caller: “It arrived broken, I want my money back.”'],
['Filler', '“Let me check that order for you.” (tool call runs)'],
['Decide', 'Order is $240, above the $100 limit for automatic refunds'],
['Transfer', '“I’ll connect you to a colleague who can approve this. I’ve passed on the details.”'],
['Summary to human', '“Order 4729, $240, item broken on arrival, caller verified, wants a refund.”']]))

sec('checklist', 'Build checklist',
pts('Choose cascade, speech-to-speech or hybrid on purpose (Part 1).', 'Use a framework unless you have a reason not to.', 'Turn detection, streaming and barge-in working before anything else.', 'Few, fast tools; confirm before acting.', 'Voice-specific prompt; AI disclosure in the greeting.', 'Warm transfer to a human with a summary.', 'Test on real phone lines with real accents (Part 4).'))

sec('sources', 'Sources',
pts(A('https://github.com/openai/openai-realtime-agents', 'OpenAI realtime agents demo'), A('https://github.com/openai/openai-realtime-console', 'OpenAI realtime console'), A('https://github.com/openai/openai-realtime-twilio-demo', 'OpenAI Realtime API with Twilio'), A('https://github.com/google-gemini/live-api-web-console', 'Google Live API web console'), A('https://github.com/pipecat-ai/pipecat', 'Pipecat'), A('https://github.com/livekit/agents', 'LiveKit Agents')))
JS = ''
