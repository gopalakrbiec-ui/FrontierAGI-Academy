# Prompt caching on a 40-turn agent run, three ways. Standard library only.
# Multipliers from Anthropic's prompt caching docs: 5-minute cache write = 1.25x base input price,
# cache read = 0.1x (the standard multiplier; some newer models are lower). Price is an example: $3 per million input tokens.
PRICE, WRITE, READ = 3.0, 1.25, 0.10
PREFIX, STEP, TURNS = 6_000, 2_800, 40          # stable prefix; tokens each turn adds (illustrative)

def cost(layout):
    usd, cached = 0.0, 0
    for t in range(TURNS):
        ctx = PREFIX + t * STEP
        if layout == "no caching":
            usd += ctx * PRICE / 1e6
            continue
        if layout == "timestamp at the top":       # a changing first block breaks every prefix match
            usd += ctx * WRITE * PRICE / 1e6
            continue
        new = ctx - cached                          # stable prefix first, breakpoint at the end
        usd += (cached * READ + new * WRITE) * PRICE / 1e6
        cached = ctx
    return usd

base = cost("no caching")
for layout in ["no caching", "timestamp at the top", "stable prefix first"]:
    c = cost(layout)
    print(f"{layout:22} ${c:6.2f}  ({c / base:.0%} of no caching)")
