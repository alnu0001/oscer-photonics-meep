# OSCER command sequence

This file documents the reproducibility command sequence used for the validated Meep workflow.

## Connect and clone
```bash
ssh USERNAME@sooner.oscer.ou.edu
git clone https://github.com/alnu0001/oscer-photonics-meep.git
cd oscer-photonics-meep
```

## Load Mamba and activate
```bash
module purge
module load Mamba/25.9.1-0
eval "$(mamba shell hook --shell bash)"
mamba activate photonics_mpi
```

For a fresh installation:
```bash
bash scripts/setup_oscer.sh
```

## Verify Meep and MPI
```bash
python scripts/verify_environment.py
mpiexec -n 4 python scripts/verify_environment.py
```

Useful direct checks:
```bash
python --version
which python
which mpiexec
mpiexec --version
mamba --version
python -c "import meep as mp; print(mp.__version__); print('MPI:', mp.with_mpi()); print('Processors:', mp.count_processors())"
```

## Check Python syntax
```bash
python -m py_compile src/waveguide_validation_mpi.py
```

## Submit reference jobs
```bash
sbatch slurm/r40_mpi20.slurm
sbatch slurm/r60_mpi80.slurm
sbatch slurm/r80_mpi80.slurm
sbatch slurm/r100_mpi160.slurm
sbatch slurm/r120_mpi160.slurm
```

## Monitor a job
Replace `JOBID` and `LOGFILE` with the actual values.
```bash
squeue -j JOBID
squeue -j JOBID -o "%.18i %.2t %.10M %.4D %R"
tail -n 80 logs/LOGFILE.out
grep "on time step" logs/LOGFILE.out | tail -n 15
tail -F logs/LOGFILE.out | grep --line-buffered "on time step"
stat -c 'Last write: %y   Size: %s bytes' logs/LOGFILE.out
tail -n 30 logs/LOGFILE.err
```

Stop only the live viewer with `Ctrl+C`. This does not cancel the SLURM job.

## After completion
```bash
sacct -j JOBID --format=JobID,JobName,State,ExitCode,Elapsed,AllocNodes,AllocCPUS
```

## Cancel a job
```bash
scancel JOBID
```

## Export exact environment provenance
```bash
bash scripts/export_exact_environment.sh
```

Commit the generated exact environment files for archival releases.
