sec('design', 'Designing a conversation, not a menu',
pts(('Old IVR thinking.', ['A tree of options: “for billing say billing”. Callers hate it because they must fit the system.']),
('Voice agent thinking.', ['Let the caller say what they want in their own words, then confirm and act. The agent asks only for what it is missing.']),
('Keep structure where it helps.', ['Verification, payments and legal disclosures still follow a fixed order. Pipecat Flows and similar tools exist for exactly these “predefined or dynamic conversation paths with state management”.']),
('Our rule of thumb.', ['Free conversation for understanding the request; fixed steps for anything that moves money or changes an account.'])))

sec('modality', 'Voice plus a screen',
pts('Many “voice” agents are multimodal: the caller talks, and a link, form or summary appears on their phone or in an app.', 'Send by text or app what is hard to say: links, long numbers, lists of options, receipts.', 'Google’s Live API demos render charts and lists in the web page while the conversation continues; LiveKit and Pipecat both support video and data alongside audio.', 'Design rule (our reading): speak the decision, show the details.'))

sec('who', 'Who builds voice agents',
tbl(['Kind of company', 'What they sell', 'Examples'], [
['Model labs', 'Realtime speech models and APIs', 'OpenAI, Google, xAI, Microsoft, Mistral'],
['Speech specialists', 'Speech-to-text and text-to-speech', 'ElevenLabs, Deepgram, open models ⚠️'],
['Infrastructure', 'Real-time media, telephony', 'LiveKit, Twilio, Daily (Pipecat’s creators) ⚠️'],
['Voice-agent platforms', 'Hosted agents with numbers and dashboards', 'Several start-ups ⚠️'],
['Contact-centre vendors', 'Agents inside existing call-centre software', 'Large CCaaS providers ⚠️']]) +
'<p>⚠️ marks company roles we describe from general knowledge and could not check on their sites today.</p>')

sec('faq', 'Questions people ask',
pts(('“Will callers know it is an AI?”', ['They should, because you tell them. Hiding it damages trust and may break the law where disclosure is required.']),
('“Is speech-to-speech always better?”', ['It is usually faster and sounds more natural, but a cascade gives more control and visibility. Many production systems still use cascades or hybrids.']),
('“Can it handle angry callers?”', ['It can stay calm and transfer quickly; it should not try to “win” the conversation. Detect strong emotion and hand over.'])))
