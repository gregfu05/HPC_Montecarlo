"""CLI entry point for Monte Carlo molecular optimization."""

from __future__ import annotations

import argparse
import csv
import logging
import os
from typing import Any, Dict

from . import montecarlo, utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monte Carlo molecular energy optimization.")
    parser.add_argument("--config", type=str, default="src/config.yaml", help="Path to YAML config.")
    parser.add_argument("--outdir", type=str, default=None, help="Override output directory.")
    parser.add_argument("--steps", type=int, default=None, help="Override number of Monte Carlo steps.")
    parser.add_argument("--seed", type=int, default=None, help="Override RNG seed.")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level.")
    return parser.parse_args()


def _apply_cli_overrides(cfg: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    cfg = cfg.copy()
    cfg.setdefault("simulate", {})
    cfg.setdefault("molecule", {})
    if args.steps is not None:
        cfg["simulate"]["steps"] = args.steps
    if args.seed is not None:
        cfg["simulate"]["seed"] = args.seed
    if args.outdir is not None:
        cfg["simulate"]["outdir"] = args.outdir
    return cfg


def save_energy_csv(path: str, energies: list[float]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "energy"])
        for idx, e in enumerate(energies):
            writer.writerow([idx, f"{e:.8f}"])


def main() -> None:
    args = parse_args()
    cfg_raw = utils.load_config(args.config)
    cfg = _apply_cli_overrides(cfg_raw, args)
    env_scaling = os.getenv("SCALING_MODE")
    if env_scaling:
        cfg.setdefault("scaling", {})
        cfg["scaling"]["mode"] = env_scaling
    sim_cfg = montecarlo.SimulationConfig.from_dict(cfg)

    comm, rank, size = utils.detect_mpi()
    rng = utils.create_rng(sim_cfg.seed, rank=rank)
    log_file = os.path.join(sim_cfg.outdir, "logs", f"run_rank{rank}.log")
    level = getattr(logging, args.log_level.upper(), logging.INFO)
    logger = utils.setup_logger("montecarlo", log_file=log_file, level=level)

    molecule = montecarlo.molecule_from_config(sim_cfg)
    simulator = montecarlo.MonteCarloSimulator(molecule, sim_cfg, rng, logger)
    result = simulator.run()

    csv_path = os.path.join(sim_cfg.outdir, "csv", f"energies_rank{rank}.csv")
    save_energy_csv(csv_path, result.energies)
    best_xyz = os.path.join(sim_cfg.outdir, "csv", f"best_rank{rank}.xyz")
    utils.write_xyz(best_xyz, result.best_positions)

    # Gather best results across ranks.
    summary = {"rank": rank, "best_energy": result.best_energy, "runtime": result.runtime}
    gathered = comm.gather(summary, root=0)
    if rank == 0:
        best_global = min(gathered, key=lambda x: x["best_energy"])
        logger.info(
            "Global best energy %.6f from rank %d (runtime %.3f s)",
            best_global["best_energy"],
            best_global["rank"],
            best_global["runtime"],
        )
        montecarlo.log_scaling_result(
            outdir=os.path.join(sim_cfg.outdir, "csv"),
            rank=best_global["rank"],
            size=size,
            num_atoms=len(molecule.atoms),
            steps=sim_cfg.steps,
            runtime=best_global["runtime"],
            mode="strong" if cfg.get("scaling", {}).get("mode", "strong") == "strong" else "weak",
        )

    # Broadcast best energy for reproducibility metadata.
    best_energy = comm.bcast(result.best_energy, root=0)
    if rank == 0:
        logger.info("Broadcasted best energy %.6f to all ranks", best_energy)


if __name__ == "__main__":
    main()
