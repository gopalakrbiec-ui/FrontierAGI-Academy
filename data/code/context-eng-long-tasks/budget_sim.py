# A toy agent run: 40 tool-using turns, four context strategies. Standard library only.
# Numbers are illustrative assumptions (not measurements): fixed prefix 6,000 tokens
# (system prompt + tool definitions), each turn adds 300 tokens of model text and a 2,500-token tool result.
PREFIX, TEXT, RESULT, TURNS, WINDOW = 6_000, 300, 2_500, 40, 100_000

def run(strategy):
    history, total_in, peak, summaries = [], 0, 0, 0
    for t in range(TURNS):
        history.append([TEXT, RESULT])
        if strategy == "clear tool results":          # keep only the last 3 raw results
            for h in history[:-3]:
                h[1] = 40                              # a short "[result cleared]" stub
        ctx = PREFIX + sum(a + b for a, b in history)
        if strategy == "compaction" and ctx > 0.6 * WINDOW:
            history = [[2_000, 0]]                     # summary replaces history
            summaries += 1
            ctx = PREFIX + 2_000
        if strategy == "sub-agents" and t % 10 == 9:   # every 10 turns a sub-agent's work
            history = history[:-10] + [[1_500, 0]]     # comes back as a 1,500-token summary
            ctx = PREFIX + sum(a + b for a, b in history)
        total_in += ctx
        peak = max(peak, ctx)
    return total_in, peak, summaries

base = run("none")[0]
print(f"{'strategy':20} {'input tokens':>13} {'peak window':>12} {'vs none':>8}")
for s in ["none", "clear tool results", "compaction", "sub-agents"]:
    tot, peak, n = run(s)
    note = f"  ({n} compactions)" if n else ""
    print(f"{s:20} {tot:>13,} {peak:>12,} {tot / base:>7.0%}{note}")
print(f"'none' overflows a {WINDOW:,}-token window at turn {next(t for t in range(1, TURNS + 1) if PREFIX + t * (TEXT + RESULT) > WINDOW)}")
