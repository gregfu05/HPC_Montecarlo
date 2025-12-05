#!/bin/bash
#SBATCH --job-name=mc-gpu
#SBATCH --nodes=2
#SBATCH --gpus-per-node=2
#SBATCH --time=00:20:00
#SBATCH --partition=gpu
#SBATCH --output=results/logs/gpu_%j.out

# Placeholder GPU submission; the core simulation is CPU-only but can be profiled on GPU nodes.
module load gcc/11.4.0 openmpi/4.1.5 cuda/12.2

CONFIG=${CONFIG:-src/config.yaml}
OUTDIR=${OUTDIR:-results}

mpirun python3 -m src.main --config "${CONFIG}" --outdir "${OUTDIR}"
