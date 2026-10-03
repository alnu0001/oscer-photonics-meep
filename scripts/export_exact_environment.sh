#!/usr/bin/env bash
set -euo pipefail

module purge
module load Mamba/25.9.1-0
eval "$(mamba shell hook --shell bash)"
mamba activate photonics_mpi

conda env export > environment-oscer-exact.yml
conda list --explicit > environment-oscer-explicit.txt
conda list > package-list.txt

{
  echo "Captured: $(date --iso-8601=seconds)"
  echo "Host: $(hostname)"
  echo "Kernel: $(uname -a)"
  echo "Python: $(python --version 2>&1)"
  echo "Python path: $(which python)"
  echo "Mamba: $(mamba --version 2>&1)"
  echo "MPI launcher: $(which mpiexec)"
  echo "MPI version:"
  mpiexec --version 2>&1 | head -n 5
  echo "Meep:"
  python - <<'PY'
import meep as mp
print(mp.__version__)
print("MPI enabled:", mp.with_mpi())
print("Processors visible in this invocation:", mp.count_processors())
PY
  echo "Loaded modules:"
  module list 2>&1
} > software-stack.txt

echo "Wrote environment-oscer-exact.yml"
echo "Wrote environment-oscer-explicit.txt"
echo "Wrote package-list.txt"
echo "Wrote software-stack.txt"
