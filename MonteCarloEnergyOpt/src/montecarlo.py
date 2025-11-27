"""Monte Carlo Metropolis and simulated annealing implementation."""

from __future__ import annotations

import logging
import math
import os
import time
from dataclasses import dataclass
from typing import List

import numpy as np

from . import energy, utils


@dataclass
class SimulationConfig:
    """Configuration for a Monte Carlo run."""

    steps: int = 1000
    step_size: float = 0.1
    temperature_start: float = 1.0
    temperature_min: float = 0.01
    anneal_rate: float = 0.995
    seed: int | None = None
    log_interval: int = 100
    save_interval: int = 0
    outdir: str = "results"
    xyz_path: str | None = None
    bond_pairs: List[List[int]] | None = None
    bond_k: float = 50.0
    bond_r0: float = 1.0

    @classmethod
    def from_dict(cls, cfg: dict) -> "SimulationConfig":
        """Construct from a dictionary with defaults."""
        sim = cfg.get("simulate", {})
        molecule_cfg = cfg.get("molecule", {})
        return cls(
            steps=int(sim.get("steps", cls.steps)),
            step_size=float(sim.get("step_size", cls.step_size)),
            temperature_start=float(sim.get("temperature", {}).get("start", cls.temperature_start)),
            temperature_min=float(sim.get("temperature", {}).get("min", cls.temperature_min)),
            anneal_rate=float(sim.get("temperature", {}).get("anneal_rate", cls.anneal_rate)),
            seed=sim.get("seed", cls.seed),
            log_interval=int(sim.get("log_interval", cls.log_interval)),
            save_interval=int(sim.get("save_interval", cls.save_interval)),
            outdir=str(sim.get("outdir", cls.outdir)),
            xyz_path=molecule_cfg.get("xyz"),
            bond_pairs=molecule_cfg.get("bond_pairs"),
            bond_k=float(molecule_cfg.get("bond_k", cls.bond_k)),
            bond_r0=float(molecule_cfg.get("bond_r0", cls.bond_r0)),
        )


@dataclass
class RunResult:
    energies: List[float]
    accepted: int
    attempted: int
    best_energy: float
    best_positions: np.ndarray
    runtime: float


class MonteCarloSimulator:
    """Perform Metropolis Monte Carlo with simulated annealing on a molecule."""

    def __init__(
        self,
        molecule: energy.Molecule,
        config: SimulationConfig,
        rng: np.random.Generator,
        logger: logging.Logger | None = None,
    ) -> None:
        self.molecule = molecule
        energy.validate_molecule(self.molecule)
        self.config = config
        self.rng = rng
        self.logger = logger or logging.getLogger(__name__)

    def _temperature(self, step: int) -> float:
        """Exponential decay temperature schedule."""
        t = self.config.temperature_start * (self.config.anneal_rate ** step)
        return max(t, self.config.temperature_min)

    def run(self) -> RunResult:
        """Execute Monte Carlo simulation and return results."""
        start_time = time.time()
        current_energy = energy.total_energy_neighbor(self.molecule)
        energies = [current_energy]
        best_energy = current_energy
        best_positions = self.molecule.positions.copy()
        accepted = 0
        attempted = 0

        for step in range(1, self.config.steps + 1):
            attempted += 1
            temp = self._temperature(step)
            atom_index = int(self.rng.integers(0, len(self.molecule.atoms)))
            displacement = self.rng.normal(loc=0.0, scale=self.config.step_size, size=3)
            new_pos = self.molecule.atoms[atom_index].position + displacement
            delta_e = energy.delta_energy_for_atom_move(self.molecule, atom_index, new_pos)

            accept = False
            if delta_e <= 0:
                accept = True
            else:
                prob = math.exp(-delta_e / max(temp, 1e-12))
                if self.rng.random() < prob:
                    accept = True

            if accept:
                self.molecule.update_atom_position(atom_index, new_pos)
                current_energy += delta_e
                accepted += 1
                if current_energy < best_energy:
                    best_energy = current_energy
                    best_positions = self.molecule.positions.copy()

            energies.append(current_energy)

            if step % max(1, self.config.log_interval) == 0:
                self.logger.info(
                    "step=%d temp=%.5f energy=%.6f best=%.6f accepted=%d/%d",
                    step,
                    temp,
                    current_energy,
                    best_energy,
                    accepted,
                    attempted,
                )

        runtime = time.time() - start_time
        self.logger.info(
            "Completed %d steps in %.3f s | acceptance=%.3f best_energy=%.6f",
            self.config.steps,
            runtime,
            accepted / attempted if attempted else 0.0,
            best_energy,
        )
        return RunResult(
            energies=energies,
            accepted=accepted,
            attempted=attempted,
            best_energy=best_energy,
            best_positions=best_positions,
            runtime=runtime,
        )


def build_chain_molecule(n_atoms: int, bond_length: float, bond_k: float) -> energy.Molecule:
    """Construct a simple linear chain molecule."""
    atoms = [energy.Atom(atom_id=i, position=np.array([i * bond_length, 0.0, 0.0])) for i in range(n_atoms)]
    bonds = [energy.Bond(atom_i=i, atom_j=i + 1, k=bond_k, r0=bond_length) for i in range(n_atoms - 1)]
    return energy.Molecule(atoms, bonds)


def molecule_from_config(cfg: SimulationConfig) -> energy.Molecule:
    """Create molecule from configuration."""
    if cfg.xyz_path:
        if not os.path.exists(cfg.xyz_path):
            raise FileNotFoundError(f"XYZ file not found: {cfg.xyz_path}")
        positions = utils.read_xyz(cfg.xyz_path)
        atoms = [energy.Atom(atom_id=i, position=pos) for i, pos in enumerate(positions)]
    else:
        atoms = [
            energy.Atom(atom_id=i, position=np.array([i * cfg.bond_r0, 0.0, 0.0]))
            for i in range(4)
        ]
    if cfg.bond_pairs:
        bonds = [energy.Bond(atom_i=i, atom_j=j, k=cfg.bond_k, r0=cfg.bond_r0) for i, j in cfg.bond_pairs]
    else:
        bonds = [energy.Bond(atom_i=i, atom_j=i + 1, k=cfg.bond_k, r0=cfg.bond_r0) for i in range(len(atoms) - 1)]
    return energy.Molecule(atoms, bonds)


def log_scaling_result(
    outdir: str,
    rank: int,
    size: int,
    num_atoms: int,
    steps: int,
    runtime: float,
    mode: str,
) -> None:
    """Append scaling metrics to CSV."""
    import csv
    import os

    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, f"scaling_{mode}.csv")
    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["rank", "size", "num_atoms", "steps", "runtime_s", "mode"])
        writer.writerow([rank, size, num_atoms, steps, f"{runtime:.6f}", mode])
