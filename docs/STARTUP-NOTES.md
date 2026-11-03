# Startup notes

Owner's notes (one section per conversation) for the Maestro series (especially Season 2, Phases 8–9: the product, agents as customers, competing at the frontier). Each section is the owner's summary of a conversation. They are summaries, not a verified transcript, so quote them as the owner's notes, not as Rauch's exact words, unless a primary source is found and cited.

Added 3 Nov 2026.

## Takeaways from a conversation with Guillermo Rauch

| Theme | Rauch's argument | Why it matters |
|---|---|---|
| Ride the incoming wave | Startups beat incumbents by building for the next platform shift, not by copying legacy systems. | Incumbents are strongest on the old wave. The new wave resets the playing field, which is where a small company can win. |
| Agents as a new customer class | AI coding agents now choose and use tools. They favour API-driven, modular stacks like Next.js and headless backends. | Developer experience now has two audiences, humans and agents. Products that are easy for agents to read, call and deploy get adopted faster. |
| Trust as the moat | In a post-AGI world, capability becomes cheap and trust becomes scarce. Trust is the result of quality, reliability and design, not something you can chase directly. | When anyone can generate software, buyers choose whoever they believe won't break things. That belief can't be faked; it comes from a track record. |
| Engineering for verification | Humans should define goals and allocate capital, while automated evals and checks keep agent output high-quality and secure. | The bottleneck moves from writing code to proving it's correct, so evals and verification loops become core engineering work. |
| Personal operating philosophy | Lessons from his house fire and from raising six kids, his "sub-agents": teach them to think and build fundamentals. | In an AI-heavy world, judgment and foundational skills matter more, because they're what let you direct and check AI work. |

**The common thread:** as AI makes building easier, value shifts to three things:
1. choosing the right direction, the next wave;
2. making your product easy for agents to use;
3. proving quality through verification, which over time compounds into trust.

## Takeaways from a conversation with Jon Noronha (Gamma)

Added 3 Nov 2026. Owner's summary, not a verified transcript; Gamma's architecture figures (about 20 models, 200 API calls per deck) are as reported in the conversation and should be marked ⚠️ unless a primary source is cited.

| Theme | Noronha's argument | Why it matters |
|---|---|---|
| The agent harness is the product | The model is a commodity. The tools around it, for acting, self-inspecting and interacting with users, are where value and defensibility live. | Two products on the same LLM can differ enormously. The moat is in the orchestration, not the model. |
| Gamma's architecture | One deck takes about 20 models and 200 API calls: a cloud sandbox, context gathering, drafting, then repeated visual QA passes. | Quality output comes from a pipeline, not a single prompt. Multi-step generate-check-fix loops are the norm. |
| Find your edge in taste-heavy domains | Build where human judgment and subjective quality matter, such as personal gaming, physical services and niche professional tools. | When "correct" is fuzzy, generic AI fails and taste becomes the differentiator, which incumbents and model labs struggle to copy. |
| Avoiding "AI smell" | Generic-feeling output is the core risk. Gamma counters it with constant experimentation and by letting users steer the creative process. | Benchmarks don't capture taste. Human-in-the-loop control and rapid iteration matter more than eval scores here. |
| The marketing engineer | A new role that uses agents to run high-frequency, data-driven experiments at scale. | Marketing shifts from intuition and campaigns to continuous experimentation, so one person can test what used to take a team. |
| Underhyped: image models | Image AI is undervalued for specific uses like home decor visualisation and professional design workflows. | The opportunity is in vertical, workflow-specific applications rather than general image generation. |

**The common thread:** the model is the engine, but the harness, meaning the tools, QA loops and taste built around it, is the product. Value goes to whoever designs the best system around the model for a domain where quality is subjective.

## Rauch and Noronha together

- Both stress verification loops.
- **Rauch** frames them as automated checks for correctness and security.
- **Noronha** adds taste-driven QA for subjective quality.
- Together: an agent product needs both kinds of check, one asking **"is it right?"** and one asking **"is it good?"**

## Where these show up in the Maestro series

- **Trust as the moat, and engineering for verification:** already the spine of the story: the fixed human gate, the evaluation harness and the gate record (Season 1, Parts 11–12; Season 2, Parts 3–4).
- **Agents as a new customer class:** use in Season 2, Phase 8 ("From PR bot to agent platform", "The harness as product"): Maestro's APIs, docs and tools should be easy for other agents to call.
- **Ride the incoming wave:** use in Season 2, Phase 9 ("When a frontier lab ships your product", "Market shifts").
- **The harness is the product (Noronha):** the core of Season 2, Part 16 ("The harness as product") and Part 17 ("Model-agnostic or not?"): if the model is a commodity, Maestro's moat is the harness, gate and skill library. Gamma's generate-check-fix pipeline is a reference case (⚠️ figures as reported).
- **"Is it right?" and "is it good?":** Maestro's gate checks correctness today; Phase 8 should add taste/quality checks (reviewer acceptance, style and maintainability of changes) and user steering, and show both in the product.
- **The marketing engineer:** a candidate role in the go-to-market team (Season 2, Part 2 follow-up and Phase 9 distribution).
- **Taste-heavy domains and vertical image models:** inputs for Phase 6's "Hunting the next moat" (candidate directions) and Phase 9's market-shift scenarios.
- **Judgment and fundamentals:** use in the team and culture threads (hiring, onboarding, what Gopala keeps doing himself).
