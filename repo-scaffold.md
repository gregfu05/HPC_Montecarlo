1️⃣ Repo Scaffold — “HPC Monte Carlo Molecular Optimization”
Repo Layout
MonteCarloEnergyOpt/
│
├── src/                     # Main simulation code
│   ├── __init__.py
│   ├── montecarlo.py        # Core Monte Carlo & simulated annealing routines
│   ├── energy.py            # Energy calculation, bond potential, neighbor lists
│   ├── utils.py             # Helper functions (random seeds, logging)
│   ├── main.py              # CLI entry point for running simulations
│   ├── config.yaml          # Simulation parameters (num_atoms, steps, temp schedule)
│   └── tests/               # Unit tests for correctness
│       ├── test_energy.py
│       └── test_montecarlo.py
│
├── env/                     # Environment and container
│   ├── project.def          # Apptainer recipe
│   ├── environment.yml      # Conda environment (optional)
│   └── modules.txt          # Exact module versions used on Magic Castle cluster
│
├── slurm/                   # Slurm scripts
│   ├── run.sh               # Wrapper for Apptainer or env execution
│   ├── submit_mpi.sbatch    # CPU-based MPI strong scaling runs
│   ├── submit_gpu.sbatch    # Multi-GPU PyTorch/DDP or CUDA-enabled simulation
│   └── helpers/             # Optional helper scripts (e.g., job arrays)
│
├── data/                    # Tiny sample data + download scripts
│   ├── sample_molecule.xyz  # Minimal molecule for testing
│   ├── fetch_full_dataset.sh # Script to download larger molecule sets if public
│   └── README.md            # Explain data sources and formats
│
├── results/                 # All outputs from runs
│   ├── logs/                # Slurm logs and stdout
│   ├── csv/                 # Simulation outputs per run
│   ├── plots/               # PNG/SVG scaling, efficiency, energy vs iteration
│   └── profiling/           # perf, Nsight, LIKWID, or PAPI logs
│
├── docs/                    # Papers, proposals, slides, and general docs
│   ├── paper.pdf            # 4–6 page HPC paper
│   ├── eurohpc_proposal.pdf # 6–8 page EuroHPC proposal
│   ├── slides.pdf           # 5-slide pitch
│   └── README.md            # Project overview and instructions
│
├── reproduce.md             # Exact commands to reproduce results, including seeds, modules, flags
├── SYSTEM.md                # Node types, CPU/GPU used, module list, driver/runtime versions
├── Makefile / setup.py      # Build & install scripts if needed
├── LICENSE
└── README.md                # Top-level description, quick start, and repo structure




Key Notes for Assignment Compliance
Nodes & Parallelism


Minimum: 2 CPU nodes for MPI, 2 GPU nodes for GPU experiments.


Optional strong scaling up to 4–8 nodes.


Weak scaling: increase molecule size with nodes to keep workload per rank constant.


Reproducibility


Fix random seeds.


Record module versions in modules.txt or container in project.def.


Provide exact compile/runtime commands in reproduce.md.


Profiling & Performance


Logs in results/profiling/.


Plot strong & weak scaling in results/plots/.


Record CPU/GPU utilization, I/O, and communication time.


Optimization Step


Implement neighbor lists (energy.py) for reduced computation cost.


Optionally overlap communication & computation when aggregating results (montecarlo.py).


Slurm Execution


run.sh for Apptainer wrapper.


submit_mpi.sbatch for multi-node CPU runs.


submit_gpu.sbatch for multi-GPU runs with DDP or CUDA.


Data Handling


Keep only tiny sample in repo.


Script larger datasets download.


Include README explaining formats & sources.


Deliverables


docs/ contains final paper, proposal, slides.


results/ contains CSV, plots, logs.


SYSTEM.md + reproduce.md ensures reproducibility.

