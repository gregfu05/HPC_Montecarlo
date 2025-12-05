#!/usr/bin/env bash
# Wrapper to execute simulation within Apptainer or system environment.
set -euo pipefail

IMAGE="${IMAGE:-env/project.sif}"
CONFIG="${CONFIG:-src/config.yaml}"
OUTDIR="${OUTDIR:-results}"

if [[ -f "${IMAGE}" ]]; then
    echo "Running with Apptainer image ${IMAGE}"
    apptainer exec "${IMAGE}" python3 -m src.main --config "${CONFIG}" --outdir "${OUTDIR}" "$@"
else
    echo "Apptainer image not found; running with host Python."
    python3 -m src.main --config "${CONFIG}" --outdir "${OUTDIR}" "$@"
fi
