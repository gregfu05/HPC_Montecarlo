import numpy as np

from src import energy


def test_total_energy_matches_neighbor():
    atoms = [
        energy.Atom(atom_id=0, position=np.array([0.0, 0.0, 0.0])),
        energy.Atom(atom_id=1, position=np.array([1.0, 0.0, 0.0])),
        energy.Atom(atom_id=2, position=np.array([2.0, 0.0, 0.0])),
    ]
    bonds = [
        energy.Bond(atom_i=0, atom_j=1, k=10.0, r0=1.0),
        energy.Bond(atom_i=1, atom_j=2, k=10.0, r0=1.0),
    ]
    mol = energy.Molecule(atoms, bonds)
    brute = energy.total_energy_bruteforce(mol)
    neighbor = energy.total_energy_neighbor(mol)
    assert np.isclose(brute, neighbor)


def test_delta_energy_local_update():
    atoms = [
        energy.Atom(atom_id=0, position=np.array([0.0, 0.0, 0.0])),
        energy.Atom(atom_id=1, position=np.array([1.0, 0.0, 0.0])),
    ]
    bonds = [energy.Bond(atom_i=0, atom_j=1, k=20.0, r0=1.0)]
    mol = energy.Molecule(atoms, bonds)
    new_pos = np.array([1.1, 0.0, 0.0])
    delta = energy.delta_energy_for_atom_move(mol, 0, new_pos)
    mol.update_atom_position(0, new_pos)
    full = energy.total_energy_bruteforce(mol)
    # Starting energy is zero; delta should equal full energy after move.
    assert np.isclose(delta, full, atol=1e-8)
