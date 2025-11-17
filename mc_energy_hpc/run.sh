#!/usr/bin/env bash
set -euo pipefail
if [[ -f env/project.sif ]]; then
  apptainer exec --nv --bind "$PWD":"$PWD" --pwd "$PWD" env/project.sif "$@"
else
  source env/load_modules.sh
  "$@"
fi
