#!/bin/bash
#SBATCH -J ddp-test
#SBATCH -N 2
#SBATCH --ntasks-per-node=2
#SBATCH --gres=gpu:2
#SBATCH -t 00:20:00

module purge
module load cuda/12.2
module load python/3.11.4

srun python -m torch.distributed.run --nproc_per_node=2 src/train_ddp.py
