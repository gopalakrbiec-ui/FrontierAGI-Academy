"""triage.py — model, harness or context? Triage before you train.

400 failed customer tasks from the last quarter were labelled by the layer that
would fix them (the model + harness + context frame). Fixes to context and
harness are cheap and fast; only "model" failures justify a new pre-training
run. Counts, fix rates and costs are SCENARIO numbers from the story.
"""
FAILS = [  # (cause, layer, count, share a fix would recover)
    ("missing repo conventions in context", "context", 92, 0.80),
    ("stale or wrong skill retrieved", "context", 56, 0.70),
    ("tool-call loop / bad retry policy", "harness", 71, 0.75),
    ("plan too long, no checkpoints", "harness", 41, 0.60),
    ("multi-file reasoning over 4h tasks", "model", 63, 0.55),
    ("unfamiliar languages (Rust, Kotlin)", "model", 47, 0.65),
    ("long-context recall past 128k", "model", 30, 0.60)]
COST = {"context": ("2 weeks", 0.05), "harness": ("6 weeks", 0.3), "model": ("9 months", 22.0)}  # time, $M

def main():
    tot = sum(f[2] for f in FAILS)
    for layer in ("context", "harness", "model"):
        rows = [f for f in FAILS if f[1] == layer]; n = sum(r[2] for r in rows); rec = sum(r[2] * r[3] for r in rows)
        print(f"{layer:8} {n:4} failures ({n / tot:4.0%})  fix recovers {rec:5.1f} tasks  in {COST[layer][0]:9} for ${COST[layer][1]:5.2f}M")
    cheap = sum(f[2] * f[3] for f in FAILS if f[1] != "model"); model = sum(f[2] * f[3] for f in FAILS if f[1] == "model")
    print(f"\nfix context + harness first: {cheap:.0f} of {tot} failures ({cheap / tot:.0%})")
    print(f"only a new model fixes:      {model:.0f} of {tot} ({model / tot:.0%}) -> train Maestro-2 only for these")

if __name__ == "__main__":
    main()
