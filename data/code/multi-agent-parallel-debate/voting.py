# Voting with several agents: how much does majority vote help? Standard library only.
# Each agent answers a yes/no check correctly with probability p. "Correlated" means agents
# share a mistake some of the time (same model, same prompt), modelled as a shared draw with probability rho.
import random
random.seed(7)
TRIALS = 20_000

def vote(n, p, rho):
    right = 0
    for _ in range(TRIALS):
        shared = random.random() < rho              # everyone copies one common answer
        common = random.random() < p
        votes = [common if shared else (random.random() < p) for _ in range(n)]
        right += sum(votes) > n / 2
    return right / TRIALS

print(f"{'agents':>6} {'independent':>12} {'correlated (rho=0.5)':>22}")
for n in (1, 3, 5, 9):
    print(f"{n:>6} {vote(n, 0.70, 0):>12.1%} {vote(n, 0.70, 0.5):>22.1%}")
print("one agent at p=0.70; calls cost n times as much")
