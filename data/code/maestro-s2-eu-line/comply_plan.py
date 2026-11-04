"""comply_plan.py — what crossing the line costs.

Obligations for providers of general-purpose models with systemic risk come
from AI Act Articles 52-55 (notify the Commission, documentation, evaluations
including adversarial testing, risk mitigation, serious-incident reporting,
cybersecurity). Owners, weeks and costs are SCENARIO estimates.
"""
OB = [("notify the Commission (Art. 52)", "CEO + counsel", 1, 0.02),
      ("update technical docs + downstream info (Art. 53)", "research + docs", 6, 0.15),
      ("update copyright policy + data summary (Art. 53)", "data lead + counsel", 4, 0.10),
      ("evaluations incl. adversarial testing (Art. 55)", "safety team + external red team", 10, 0.90),
      ("systemic-risk assessment + mitigation (Art. 55)", "safety lead", 8, 0.35),
      ("serious-incident reporting process (Art. 55)", "ops + safety", 3, 0.08),
      ("cybersecurity for weights and infra (Art. 55)", "security", 12, 0.60)]

def main():
    for name, who, wk, c in OB: print(f"{name:52} {who:32} {wk:3} wk  ${c:4.2f}M")
    tot = sum(o[3] for o in OB); crit = max(o[2] for o in OB)
    print(f"\ntotal ${tot:.2f}M; longest item {crit} weeks (runs in parallel with the ~12-week training run)")
    print(f"share of the Maestro-2 compute bill (~$19.5M on 4,096 GPUs): {tot / 19.5:.0%}")

if __name__ == "__main__":
    main()
