import argparse
import time
from instance import Instance
from greedy import construct, write_solution
from local_search import local_search, total
from grasp import grasp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--algo", choices=["greedy", "ls", "grasp"], required=True)
    parser.add_argument("--alpha", type=float, default=0.3)
    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--time", type=float, default=60)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    inst = Instance(args.input)
    start = time.time()
    if args.algo == "greedy":
        sol = construct(inst)
    elif args.algo == "ls":
        sol = construct(inst)
        if sol is not None:
            sol = local_search(inst, sol)
    else:
        sol = grasp(inst, args.alpha, args.iters, args.time, args.seed)
    elapsed = time.time() - start

    if sol is None:
        print(f"{args.algo}: no solution  time={elapsed:.3f}s")
    else:
        write_solution(args.output, sol)
        e, p = total(inst, sol)
        print(f"{args.algo}: energy={e} profit={p} time={elapsed:.3f}s")