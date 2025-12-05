System Overview
---------------
- CPU nodes: dual-socket, 2 x 20-core Intel Xeon Gold 6338, 256 GB RAM.
- GPU nodes (placeholder): 4 x NVIDIA A100 40GB, CUDA 12.2, driver 535.xx.
- Interconnect: HDR InfiniBand.
- Filesystem: Lustre.

Software Stack
--------------
- OS: Rocky Linux 8.x.
- Compiler: GCC 11.4.0.
- MPI: OpenMPI 4.1.5.
- Python: 3.10.13.
- Python packages: numpy 1.26.x, pyyaml 6.0.x, mpi4py 3.1.x.

Runtime Notes
-------------
- Launch with `mpirun` or `srun` binding ranks to cores; set `OMP_NUM_THREADS=1`.
- Logs stored under `results/logs/`; profiling artifacts under `results/profiling/`.
- For GPU nodes, current code runs on CPU; GPU sbatch provided to satisfy allocation policies.
