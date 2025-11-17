import csv
import glob
import json
import os

import matplotlib.pyplot as plt


def main():
    files = glob.glob("results/sim_rank*_size*_seed*.json")
    summary = []
    for path in files:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        parts = os.path.basename(path).split("_")
        rank = parts[2][4:]
        summary.append({
            "rank": rank,
            "seed": data["seed"],
            "time_s": data["time_s"],
            "final_energy": data["energies"][-1][1],
        })

    keys = ["rank", "seed", "time_s", "final_energy"]
    with open("results/summary_all.csv", "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=keys)
        writer.writeheader()
        for row in summary:
            writer.writerow(row)

    plt.figure()
    plt.plot([s["rank"] for s in summary], [s["time_s"] for s in summary], marker="o")
    plt.xlabel("Rank")
    plt.ylabel("Time (s)")
    plt.title("Time per rank")
    plt.savefig("results/time_vs_rank.png")
    plt.close()


if __name__ == "__main__":
    main()
