import sys
from instance import Instance

INF = float("inf")

def compatible(a, b, blocks):
    for (x, y) in blocks:
        if a <= y + 1 and x <= b + 1:
            return False
    return True

def cost(inst, a, b, need):
    p = inst.profit(a, b)
    if p == 0:
        return INF
    return inst.energy(a, b) / min(p, need)

def evaluate_candidate(inst, cands, blocks, need):
    result = []
    for (a, b) in cands:
        if compatible(a, b, blocks):
            q = cost(inst, a, b, need)
            if q < INF:
                result.append((q, a, b))
    return result

def free_profit(inst, blocks):
    free = [True] * (inst.N + 1)
    for (x, y) in blocks:
        for i in range(max(x - 1, 1), min(y + 1, inst.N) + 1):
            free[i] = False

    total = 0
    run_len = 0
    run_sum = 0
    for i in range(1, inst.N + 1):
        if free[i]:
            run_len += 1
            run_sum += inst.P[i - 1]
        else:
            if run_len >= inst.L:
                total += run_sum
            run_len = 0
            run_sum = 0
    if run_len >= inst.L:          
        total += run_sum
    return total

def construct(inst):
    cands = inst.candidates()
    blocks = []
    profit = 0
    while profit < inst.T:
        need = inst.T - profit
        evaluated = sorted(evaluate_candidate(inst, cands, blocks, need))
        chosen = None
        for (q, a, b) in evaluated:
            if profit + inst.profit(a, b) + free_profit(inst, blocks + [(a, b)]) >= inst.T:
                chosen = (q, a, b)
                break
        if chosen is None:
            return None
        q, a, b = chosen
        blocks.append((a, b))
        profit += inst.profit(a, b)
        print(f"Selected block: ({a}, {b}) need {need} cost {q:.4f}")
    return sorted(blocks)

def write_solution(path, blocks):
    with open(path, "w") as f:
        for (a, b) in blocks:
            f.write(f"{a} {b}\n")

if __name__ == "__main__":
    inst = Instance(sys.argv[1])
    sol = construct(inst)
    if sol is None:
        print("No solution found.")
    else:
        write_solution(sys.argv[2], sol)
        e = sum(inst.energy(a, b) for (a, b) in sol)
        p = sum(inst.profit(a, b) for (a, b) in sol)
        print(sol, "energy:", e, "profit:", p, "T:", inst.T)
