import numpy as np

from src import montecarlo
from src import utils


def test_metropolis_reproducibility_zero_move():
    cfg = montecarlo.SimulationConfig(steps=5, step_size=0.0, temperature_start=1.0, temperature_min=1.0, anneal_rate=1.0, seed=123)
    mol = montecarlo.build_chain_molecule(n_atoms=3, bond_length=1.0, bond_k=10.0)
    rng = utils.create_rng(cfg.seed, rank=0)
    sim = montecarlo.MonteCarloSimulator(mol, cfg, rng)
    result = sim.run()
    # With zero displacement, energy remains constant and all proposals accepted.
    assert all(np.isclose(e, result.energies[0]) for e in result.energies)
    assert result.accepted == result.attempted


def test_annealing_schedule_monotonic():
    cfg = montecarlo.SimulationConfig(steps=3, temperature_start=2.0, temperature_min=0.5, anneal_rate=0.5)
    mol = montecarlo.build_chain_molecule(n_atoms=2, bond_length=1.0, bond_k=5.0)
    rng = utils.create_rng(cfg.seed, rank=0)
    sim = montecarlo.MonteCarloSimulator(mol, cfg, rng)
    temps = [sim._temperature(i) for i in range(5)]
    assert all(temps[i] >= temps[i + 1] for i in range(len(temps) - 1))
    assert temps[-1] >= cfg.temperature_min
