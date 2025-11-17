# Reproducibility

- Python version: 3.11.x
- Conda env: `env/environment.yml`
- Cluster modules: `env/load_modules.sh`
- Git hash: `$(git rev-parse --short HEAD)`
- Commands:
  - `python -m mpi4py.run -n 4 src/run_sim.py --n_atoms 30 --steps 5000`
  - `sbatch slurm/submit_workers.sbatch`
- Seeds: `base seed + rank*10007`
