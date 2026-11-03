"""sunk_cost.py — why the $1.9M already spent should not decide anything.

Compares the expected value of continuing six more months against stopping
and moving the team to the environments track. Probabilities and values are
the story's SCENARIO estimates; the money already spent appears in neither
option, because it is gone either way.
"""
SPENT = 1.9          # $M already spent (sunk)
CONT_COST = 2.4      # $M for six more months
P_SUCCESS = 0.12     # chance the direction recovers, given month-33 evidence
WIN_VALUE = 12.0     # $M value if it does
ENV_VALUE = 3.1      # $M expected value of moving the same people to environments

def main():
    cont = P_SUCCESS * WIN_VALUE - CONT_COST
    print(f"already spent (ignored): ${SPENT}M")
    print(f"continue: {P_SUCCESS:.0%} x ${WIN_VALUE}M - ${CONT_COST}M = ${cont:+.2f}M")
    print(f"stop and redeploy: ${ENV_VALUE:+.2f}M")
    print(f"break-even chance of success to justify continuing: {(CONT_COST + ENV_VALUE) / WIN_VALUE:.0%}")

if __name__ == "__main__":
    main()
