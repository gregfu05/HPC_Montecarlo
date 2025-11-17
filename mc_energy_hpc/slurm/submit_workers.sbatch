#!/bin/bash
#SBATCH -J mc-mpi
#SBATCH -A <account>
#SBATCH -N 2
#SBATCH --ntasks-per-node=16
#SBATCH -t 00:30:00
#SBATCH -o results/mc_%j.out

module purge
source env/load_modules.sh
export OMP_NUM_THREADS=1

srun --mpi=pmix python src/run_sim.py --n_atoms 100 --steps 50000 --seed 42 --out results
