import argparse
import json
import os

from mpi4py import MPI

from simulation import MonteCarloSim


def parse_args():
    parser = argparse.ArgumentParser(description="Run Monte Carlo energy simulations with MPI")
    parser.add_argument("--n_atoms", type=int, default=30)
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--temp", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--record", type=int, default=1000)
    parser.add_argument("--out", type=str, default="results")
    return parser.parse_args()


def main():
    args = parse_args()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    sim = MonteCarloSim(n_atoms=args.n_atoms, temp=args.temp, seed=args.seed + rank * 10007, max_steps=args.steps)
    res = sim.run(record_every=args.record)

    os.makedirs(args.out, exist_ok=True)
    fname = f"{args.out}/sim_rank{rank}_size{size}_seed{args.seed + rank * 10007}.json"
    with open(fname, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)

    summary = {
        "rank": rank,
        "seed": args.seed + rank * 10007,
        "time_s": res["time_s"],
        "final_energy": res["energies"][-1][1],
    }
    summaries = comm.gather(summary, root=0)
    if rank == 0:
        import csv

        keys = ["rank", "seed", "time_s", "final_energy"]
        with open(f"{args.out}/summary_size{size}_seed{args.seed}.csv", "w", newline="", encoding="utf-8") as cf:
            writer = csv.DictWriter(cf, fieldnames=keys)
            writer.writeheader()
            for entry in summaries:
                writer.writerow(entry)
        print("Wrote CSV summary")


if __name__ == "__main__":
    main()
