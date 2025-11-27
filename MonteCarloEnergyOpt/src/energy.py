"""Energy calculations for Monte Carlo molecular optimization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np


@dataclass(frozen=True)
class Atom:
    """Simple atom representation with an integer id and 3D position."""

    atom_id: int
    position: np.ndarray

    def copy_with_position(self, position: np.ndarray) -> "Atom":
        """Return a new Atom with updated position."""
        return Atom(atom_id=self.atom_id, position=np.asarray(position, dtype=float))


@dataclass(frozen=True)
class Bond:
    """Harmonic bond between two atoms."""

    atom_i: int
    atom_j: int
    k: float
    r0: float


class Molecule:
    """Molecule composed of atoms and bonds with neighbor list cache."""

    def __init__(self, atoms: List[Atom], bonds: List[Bond]) -> None:
        self.atoms: List[Atom] = atoms
        self.bonds: List[Bond] = bonds
        self._neighbor_bonds: Dict[int, List[Bond]] = self._build_neighbor_list(bonds)

    @property
    def positions(self) -> np.ndarray:
        """Return positions stacked as (n_atoms, 3) array."""
        return np.vstack([atom.position for atom in self.atoms])

    def update_atom_position(self, atom_index: int, new_position: np.ndarray) -> None:
        """Update atom position in place."""
        self.atoms[atom_index] = self.atoms[atom_index].copy_with_position(new_position)

    def copy(self) -> "Molecule":
        """Deep copy atoms and bonds."""
        atoms_copy = [atom.copy_with_position(atom.position.copy()) for atom in self.atoms]
        bonds_copy = list(self.bonds)
        return Molecule(atoms_copy, bonds_copy)

    def neighbor_bonds(self, atom_index: int) -> List[Bond]:
        """Return bonds connected to the given atom index."""
        return self._neighbor_bonds.get(atom_index, [])

    @staticmethod
    def _build_neighbor_list(bonds: Iterable[Bond]) -> Dict[int, List[Bond]]:
        neighbor_map: Dict[int, List[Bond]] = {}
        for bond in bonds:
            neighbor_map.setdefault(bond.atom_i, []).append(bond)
            neighbor_map.setdefault(bond.atom_j, []).append(bond)
        return neighbor_map


def _bond_energy_vectorized(pos_i: np.ndarray, pos_j: np.ndarray, k: float, r0: float) -> float:
    """Compute harmonic bond energy."""
    delta = pos_i - pos_j
    distance = np.linalg.norm(delta)
    return 0.5 * k * (distance - r0) ** 2


def total_energy_bruteforce(molecule: Molecule) -> float:
    """Compute total energy by iterating over all bonds."""
    energy = 0.0
    positions = molecule.positions
    for bond in molecule.bonds:
        energy += _bond_energy_vectorized(
            positions[bond.atom_i], positions[bond.atom_j], bond.k, bond.r0
        )
    return float(energy)


def total_energy_neighbor(molecule: Molecule) -> float:
    """
    Compute total energy using neighbor list adjacency.

    Bonds are iterated once; neighbor list is primarily useful for local updates.
    """
    # Using set to avoid double counting.
    energy = 0.0
    positions = molecule.positions
    seen: set[Tuple[int, int]] = set()
    for atom_idx, bonds in molecule._neighbor_bonds.items():
        for bond in bonds:
            key = tuple(sorted((bond.atom_i, bond.atom_j)))
            if key in seen:
                continue
            seen.add(key)
            energy += _bond_energy_vectorized(
                positions[bond.atom_i], positions[bond.atom_j], bond.k, bond.r0
            )
    return float(energy)


def delta_energy_for_atom_move(
    molecule: Molecule, atom_index: int, new_position: np.ndarray
) -> float:
    """
    Compute energy difference for moving a single atom to a new position.

    Only bonds adjacent to the atom are considered to avoid full recomputation.
    """
    old_pos = molecule.atoms[atom_index].position
    delta_e = 0.0
    for bond in molecule.neighbor_bonds(atom_index):
        other_index = bond.atom_j if bond.atom_i == atom_index else bond.atom_i
        other_pos = molecule.atoms[other_index].position
        old_energy = _bond_energy_vectorized(old_pos, other_pos, bond.k, bond.r0)
        new_energy = _bond_energy_vectorized(new_position, other_pos, bond.k, bond.r0)
        delta_e += new_energy - old_energy
    return float(delta_e)


def validate_molecule(molecule: Molecule) -> None:
    """Validate molecule consistency."""
    n_atoms = len(molecule.atoms)
    for bond in molecule.bonds:
        if bond.atom_i >= n_atoms or bond.atom_j >= n_atoms:
            raise ValueError(f"Bond references out-of-range atom: {bond}")
        if bond.atom_i == bond.atom_j:
            raise ValueError(f"Bond cannot connect atom to itself: {bond}")
    for atom in molecule.atoms:
        if atom.position.shape != (3,):
            raise ValueError(f"Atom position must be shape (3,), got {atom.position.shape}")
