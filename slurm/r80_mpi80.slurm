#!/bin/bash
#SBATCH --job-name=wg_r80_mpi80
#SBATCH --partition=2650
#SBATCH --time=01:00:00
#SBATCH --nodes=4
#SBATCH --ntasks=80
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --output=logs/wg_r80_mpi80_%j.out
#SBATCH --error=logs/wg_r80_mpi80_%j.err

set -euo pipefail
mkdir -p logs results
module purge
module load Mamba/25.9.1-0
eval "$(mamba shell hook --shell bash)"
mamba activate photonics_mpi
export OMP_NUM_THREADS=1

echo "Bare SOI waveguide r80 MPI x80"
echo "Job ID: $SLURM_JOB_ID"
echo "Nodes: $SLURM_NNODES"
echo "Node list: $SLURM_NODELIST"
echo "Total MPI ranks: $SLURM_NTASKS"
echo "Start time: $(date)"

mpiexec -n "$SLURM_NTASKS" python src/waveguide_validation_mpi.py --resolution 80

rc=$?
echo "Simulation exit code: $rc"
echo "End time: $(date)"
exit "$rc"
