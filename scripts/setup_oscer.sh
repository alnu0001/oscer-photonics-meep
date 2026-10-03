#!/usr/bin/env bash
set -euo pipefail
module purge
module load Mamba/25.9.1-0
eval "$(mamba shell hook --shell bash)"

if mamba env list | awk '{print $1}' | grep -qx photonics_mpi; then
  echo "Environment photonics_mpi already exists."
else
  mamba env create -f environment.yml
fi

mamba activate photonics_mpi
python scripts/verify_environment.py
echo
echo "Environment ready. For a parallel verification run:"
echo "  mpiexec -n 4 python scripts/verify_environment.py"
