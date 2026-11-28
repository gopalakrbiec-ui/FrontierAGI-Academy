# Time from the caller finishing a sentence to hearing the agent start replying. Standard library only.
# Every number is an illustrative assumption in milliseconds, not a vendor measurement; change them to your own.
STAGES = {
    "cascade": [("end-of-turn wait", 500), ("speech-to-text final", 150), ("LLM first token", 450),
                ("first sentence ready", 150), ("text-to-speech first audio", 200)],
    "speech-to-speech": [("end-of-turn wait", 500), ("model first audio", 450)],
}
NETWORK = {"browser (WebRTC)": 60, "phone line (PSTN)": 250}   # extra round-trip and codec delay
TUNE = {"end-of-turn wait": 250, "LLM first token": 300, "model first audio": 300}  # smart turn model + nearer region

for arch, stages in STAGES.items():
    for net, extra in NETWORK.items():
        base = sum(ms for _, ms in stages) + extra
        tuned = sum(TUNE.get(name, ms) for name, ms in stages) + extra
        print(f"{arch:16} {net:18} {base:>5} ms   tuned {tuned:>5} ms")
print("tuned = semantic turn detection (500->250 ms) and a nearer, faster model (450->300 ms)")
