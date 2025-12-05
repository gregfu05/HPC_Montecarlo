#!/bin/bash
#SBATCH --job-name=mc-mpi
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:20:00
#SBATCH --partition=standard
#SBATCH --output=results/logs/mpi_%j.out

module load gcc/11.4.0 openmpi/4.1.5

export OMPI_MCA_btl_vader_single_copy_mechanism=none
export PYTHONWARNINGS="ignore"

CONFIG=${CONFIG:-src/config.yaml}
OUTDIR=${OUTDIR:-results}

mpirun python3 -m src.main --config "${CONFIG}" --outdir "${OUTDIR}"
