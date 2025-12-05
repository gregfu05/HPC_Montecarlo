PYTHON ?= python3
CONFIG ?= src/config.yaml
OUTDIR ?= results

.PHONY: install test run mpi strong weak clean

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install numpy pyyaml mpi4py

test:
	$(PYTHON) -m pytest -q src/tests

run:
	$(PYTHON) -m src.main --config $(CONFIG) --outdir $(OUTDIR)

mpi:
	mpirun -np 4 $(PYTHON) -m src.main --config $(CONFIG) --outdir $(OUTDIR)

strong:
	SCALING_MODE=strong $(PYTHON) -m src.main --config $(CONFIG) --outdir $(OUTDIR)

weak:
	SCALING_MODE=weak $(PYTHON) -m src.main --config $(CONFIG) --outdir $(OUTDIR)

clean:
	rm -rf __pycache__ src/__pycache__ src/tests/__pycache__ results/csv results/logs results/plots results/profiling
