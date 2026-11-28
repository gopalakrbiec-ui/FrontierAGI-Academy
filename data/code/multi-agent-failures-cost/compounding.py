# Why long chains of agents fail more often, and what a checker buys. Standard library only.
# Each hand-off succeeds with probability s. A verifier catches a failed step with probability c
# and the step is retried once (illustrative assumptions, not measurements).
def chain(steps, s, c=0.0):
    p_step = s + (1 - s) * c * s               # fail, get caught, retry succeeds
    return p_step ** steps

print(f"{'steps':>5} {'s=0.95':>8} {'s=0.95 + checker':>18} {'s=0.90':>8} {'s=0.90 + checker':>18}")
for k in (1, 3, 5, 10, 20):
    print(f"{k:>5} {chain(k, .95):>8.1%} {chain(k, .95, .8):>18.1%} {chain(k, .90):>8.1%} {chain(k, .90, .8):>18.1%}")

# Token cost: Anthropic reports agents use ~4x and multi-agent systems ~15x the tokens of a chat.
chat = 3_000
for name, mult in [("chat", 1), ("single agent", 4), ("multi-agent", 15)]:
    print(f"{name:>13}: ~{chat * mult:>6,} tokens per task (if a chat uses {chat:,})")
