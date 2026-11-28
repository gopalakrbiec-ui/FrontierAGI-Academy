# Cost of one call minute, voice agent vs a human agent. Standard library only.
# All prices are example assumptions in US dollars, not any vendor's list price.
AGENT = {"speech-to-text": 0.006, "LLM tokens": 0.010, "text-to-speech": 0.015,
         "telephony": 0.010, "platform / hosting": 0.010}
HUMAN_HOURLY = 18.0          # fully loaded cost per agent hour (example)
OCCUPANCY = 0.75             # share of paid time spent on calls
CALL_MIN, CALLS = 6, 50_000  # average call length, calls per month
CONTAIN = 0.6                # share of calls the voice agent finishes without a human

agent_min = sum(AGENT.values())
human_min = HUMAN_HOURLY / 60 / OCCUPANCY
for k, v in AGENT.items():
    print(f"{k:20} ${v:.3f}/min")
print(f"{'voice agent total':20} ${agent_min:.3f}/min")
print(f"{'human agent':20} ${human_min:.3f}/min")
all_human = CALLS * CALL_MIN * human_min
mixed = CALLS * CALL_MIN * agent_min + CALLS * (1 - CONTAIN) * CALL_MIN * human_min
print(f"monthly, all human: ${all_human:,.0f}; agent first, {CONTAIN:.0%} contained: ${mixed:,.0f} ({mixed / all_human:.0%})")
