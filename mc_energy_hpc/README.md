# Monte Carlo Energy HPC

End-to-end Monte Carlo energy simulation workflow ready for MPI clusters and reproducibility. The repo bundles simulation code, Slurm launchers, environment descriptors, and aggregation helpers.

## Quick start

```bash
conda env create -f env/environment.yml
conda activate mc-hpc
python -m mpi4py.run -n 2 src/run_sim.py --n_atoms 30 --steps 5000
```

Collect multiple JSON outputs in `results/` and run `python src/aggregate_results.py` to build `summary_all.csv` plus a `time_vs_rank.png` chart.

Use `run.sh python src/run_sim.py ...` to automatically pick the module stack or Apptainer image.
