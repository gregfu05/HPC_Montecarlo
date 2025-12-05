HPC Monte Carlo Molecular Optimization
======================================

This project implements a Metropolis Monte Carlo + simulated annealing workflow for a simple bonded molecule model. It is designed for embarrassingly parallel HPC execution (MPI ranks run independent trajectories with unique seeds) and includes neighbor-list optimization for local energy updates, Slurm scripts, and reproducibility artifacts.

Quickstart (CPU)
----------------
- Create environment: `python3 -m venv .venv && source .venv/bin/activate && pip install -r <(cat env/environment.yml | yq '.dependencies[]' -)` or `conda env create -f env/environment.yml`.
- Run single-rank simulation: `python -m src.main --config src/config.yaml --outdir results`.
- View outputs in `results/csv/` (energies, XYZ) and logs in `results/logs/`.

HPC / MPI Usage
---------------
- Build Apptainer image: `apptainer build env/project.sif env/project.def`.
- Launch MPI job: `sbatch slurm/submit_mpi.sbatch` (uses `python -m src.main` under `mpirun`).
- For quick manual MPI: `mpirun -np 4 python -m src.main --config src/config.yaml --outdir results`.
- GPU sbatch is provided as a placeholder (`slurm/submit_gpu.sbatch`) for environments where CUDA nodes are required by policy.

Configuration
-------------
- YAML config lives in `src/config.yaml`.
- Key fields:
  - `molecule.xyz`: path to XYZ coordinates.
  - `molecule.bond_pairs`: list of bonded atom index pairs.
  - `molecule.bond_k` / `molecule.bond_r0`: harmonic bond parameters.
  - `simulate.steps`, `simulate.step_size`, `simulate.temperature.start/min/anneal_rate`, `simulate.seed`, `simulate.outdir`.
- CLI overrides: `--steps`, `--seed`, `--outdir`.

Algorithm Notes
---------------
- Harmonic bond energy: `0.5 * k * (|ri-rj| - r0)^2`.
- Neighbor list caches bond adjacency for O(nbonds per atom) local `ΔE` updates.
- Metropolis acceptance with simulated annealing temperature schedule (`T = max(Tmin, T0 * anneal_rate^step)`).
- Each MPI rank runs an independent trajectory; best energy across ranks is gathered on rank 0.

Testing
-------
- Run unit tests: `pytest -q src/tests`.
- Tests cover energy correctness, neighbor list parity, deterministic Metropolis behavior, and annealing schedule monotonicity.

Reproducibility & Results
-------------------------
- Seeds are deterministic and offset by MPI rank.
- Scaling metrics append to `results/csv/scaling_<mode>.csv`.
- Exact reproduction commands are documented in `reproduce.md`; system details in `SYSTEM.md`.
