Reproducibility Guide
---------------------

Environment
-----------
- Load modules (Magic Castle example):
  - `module load gcc/11.4.0 openmpi/4.1.5 python/3.10.13`
  - `pip install --user numpy==1.26.4 pyyaml==6.0.1 mpi4py==3.1.5`
- Optional container: `apptainer build env/project.sif env/project.def`

Single-Rank Run
---------------
```bash
python -m src.main --config src/config.yaml --outdir results
```

MPI Strong Scaling (2 nodes, 4 ranks/node)
------------------------------------------
```bash
sbatch slurm/submit_mpi.sbatch
# or
mpirun -np 8 python -m src.main --config src/config.yaml --outdir results
```

Weak Scaling Example
--------------------
```bash
export SCALING_MODE=weak
mpirun -np 4 python -m src.main --config src/config.yaml --outdir results
```

Reproduce Tests
---------------
```bash
pytest -q src/tests
```

Outputs
-------
- Energies per iteration: `results/csv/energies_rank*.csv`
- Best structures: `results/csv/best_rank*.xyz`
- Logs: `results/logs/`
- Scaling summaries: `results/csv/scaling_<mode>.csv`
