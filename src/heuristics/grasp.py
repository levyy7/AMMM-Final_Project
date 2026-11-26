import sys
import random
import time
from instance import Instance
from greedy import construct, write_solution
from local_search import local_search, total

def grasp(inst, alpha, max_iters, time_limit, seed=None):
    random.seed(seed)
    best = None
    best_energy = float("inf")
    start = time.time()
    for it in range(max_iters):
        if time.time() - start > time_limit:
            break
        sol = construct(inst, alpha)              
        if sol is None:
            continue
        sol = local_search(inst, sol)             
        e, _ = total(inst, sol)
        if e < best_energy:                        
            best = sol
            best_energy = e
    return best

if __name__ == "__main__":
    inst = Instance(sys.argv[1])
    alpha = float(sys.argv[3])
    iters = int(sys.argv[4])
    sol = grasp(inst, alpha, iters, time_limit=60, seed=1)
    if sol is None:
        print("No solution found.")
    else:
        write_solution(sys.argv[2], sol)
        print("GRASP:", sol, total(inst, sol))