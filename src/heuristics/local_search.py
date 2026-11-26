import sys
from instance import Instance
from greedy import construct, write_solution

def total(inst, blocks):
    e = sum(inst.energy(a, b) for (a, b) in blocks)
    p = sum(inst.profit(a, b) for (a, b) in blocks)
    return e, p

def best_in_gap(inst, lo, hi, base_profit):
    best = None
    for length in range(inst.L, inst.U + 1):
        for a in range(lo, hi - length + 2):
            b = a + length - 1
            if base_profit + inst.profit(a, b) >= inst.T:
                e = inst.energy(a, b)
                if best is None or e < best[0]:
                    best = (e, a, b)
    return best

def local_search(inst, blocks):
    blocks = sorted(blocks)
    energy, profit = total(inst, blocks)
    improved = True
    while improved:
        improved = False
        best_energy = energy
        best_blocks = None
        K = len(blocks)

        for i in range(K):
            for j in (i, i + 1):          
                if j >= K:
                    continue
                removed = blocks[i:j + 1]
                kept = blocks[:i] + blocks[j + 1:]
                e_rem, p_rem = total(inst, removed)
                e_kept = energy - e_rem
                p_kept = profit - p_rem

                lo = blocks[i - 1][1] + 2 if i > 0 else 1
                hi = blocks[j + 1][0] - 2 if j + 1 < K else inst.N

                if p_kept >= inst.T and e_kept < best_energy:
                    best_energy = e_kept
                    best_blocks = kept

                cand = best_in_gap(inst, lo, hi, p_kept)
                if cand is not None and e_kept + cand[0] < best_energy:
                    best_energy = e_kept + cand[0]
                    best_blocks = sorted(kept + [(cand[1], cand[2])])

        if best_blocks is not None:        
            blocks = best_blocks
            energy, profit = total(inst, blocks)
            improved = True                
    return blocks

if __name__ == "__main__":
    inst = Instance(sys.argv[1])
    sol = construct(inst)
    if sol is None:
        print("No solution found.")
    else:
        print("greedy:", sol, total(inst, sol))
        sol = local_search(inst, sol)
        write_solution(sys.argv[2], sol)
        print("LS:", sol, total(inst, sol))