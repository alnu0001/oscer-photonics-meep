# OSCER Photonics Meep

**Reproducible Meep FDTD computational-photonics environment for OU OSCER with MPI-enabled HPC workflows and a validated SOI waveguide benchmark.**

This repository open-sources the software environment, Python simulation code, SLURM job scripts, reproducibility commands, reference results, and validation procedure used to run three-dimensional Meep simulations on the University of Oklahoma OSCER high-performance computing cluster.

The repository is designed so that another researcher with OSCER access can rebuild the `photonics_mpi` environment, verify MPI-enabled Meep, reproduce the reference bare silicon-on-insulator (SOI) waveguide calculation, and compare the result against the numerical benchmark.

## What is being open-sourced

This project contains:

- the `photonics_mpi` Mamba/Conda environment specification;
- Python 3.11 + Meep 1.34.0 MPI-enabled simulation workflow;
- MPI (Message Passing Interface) verification tools;
- SLURM (Simple Linux Utility for Resource Management) job scripts for OSCER;
- the bare SOI waveguide Meep model;
- mesh-convergence benchmark data from 40 to 120 pixels/um;
- commands used to create, verify, run, monitor, and archive the workflow;
- scripts for exporting the exact installed package set from OSCER.

The environment itself is the reusable research-software product. The bare SOI waveguide is the first validated reference implementation.

## Reference software stack

Validated on the OU OSCER Sooner cluster with:

- OSCER module: `Mamba/25.9.1-0`
- environment name: `photonics_mpi`
- Python: 3.11
- Meep / PyMeep: 1.34.0
- MPI-enabled PyMeep build using MPICH
- `mpi4py`
- NumPy
- SciPy
- Matplotlib
- SLURM scheduler

The portable environment definition is in `environment.yml`. For archival reproducibility, generate the exact resolved package list from the validated OSCER environment using `scripts/export_exact_environment.sh` and commit the generated files.

## Reference physical model

The benchmark is a uniform, lossless SOI strip waveguide:

| Parameter | Value |
|---|---:|
| Operating wavelength | 1550 nm = 1.550 um |
| Silicon core width | 450 nm = 0.450 um |
| Silicon core height | 220 nm = 0.220 um |
| Silicon refractive index | 3.476 |
| Silicon relative permittivity | 12.0826 |
| SiO2 refractive index | 1.44 |
| SiO2 relative permittivity | 2.0736 |
| Air refractive index | 1.00 |
| Physical SiO2 undercladding | 1.000 um |
| Air above core | 1.000 um |
| PML thickness | 0.500 um |
| Non-PML transverse span | 2.000 um |
| Source position | x = -3.000 um |
| Input mode monitor | x = -2.500 um |
| Output mode monitor | x = +2.500 um |
| Monitor separation | 5.000 um |
| Excitation | fundamental TE-like eigenmode, band 1 |
| Propagation direction | +x |
| Gaussian bandwidth | 0.10 fc |
| Field-decay threshold | 1e-9 |
| Baseline material loss/nonlinearity | none |
| Analytical transmission | T = 1 |

The silicon core is continuous along x so that the 5 um validation section contains no artificial input or output facets.

## Transmission definition

The forward fundamental-mode transmission is

`T = P_TE0,out / P_TE0,in`

where modal powers are obtained from Meep eigenmode decomposition. For the uniform, lossless reference waveguide, the analytical limit is `T = 1`.

## Mesh-convergence benchmark

| Resolution (pixels/um) | Grid spacing (nm) | Transmission T | Absolute error | Error from ideal (%) |
|---:|---:|---:|---:|---:|
| 40 | 25.00 | 1.00038747 | 3.8747e-4 | 0.038747 |
| 60 | 16.67 | 1.00023423 | 2.3423e-4 | 0.023423 |
| 80 | 12.50 | 1.00005872 | 5.8720e-5 | 0.005872 |
| 100 | 10.00 | 1.00005013 | 5.0130e-5 | 0.005013 |
| 120 | 8.33 | 1.00003722 | 3.7220e-5 | 0.003722 |

The r100-to-r120 transmission change is approximately 0.001291%, below the 0.01% practical mesh-independence criterion used in the study.

The successful r120 reference run used 160 MPI ranks across 8 OSCER nodes, completed 60,005 FDTD timesteps to `t = 250.0208333`, produced a field-decay ratio of approximately `1.50e-14`, and returned `T = 1.00003722`.

## Quick start on OSCER

```bash
ssh USERNAME@sooner.oscer.ou.edu
git clone https://github.com/alnu0001/oscer-photonics-meep.git
cd oscer-photonics-meep
bash scripts/setup_oscer.sh
```

Verify the environment:

```bash
mamba activate photonics_mpi
python scripts/verify_environment.py
mpiexec -n 4 python scripts/verify_environment.py
```

Run the validated r120 calculation:

```bash
sbatch slurm/r120_mpi160.slurm
```

Monitor it using the commands in `docs/OSCER_COMMANDS.md`.

## Exact environment capture

After rebuilding or validating the environment on OSCER, run:

```bash
bash scripts/export_exact_environment.sh
```

This generates:

- `environment-oscer-exact.yml`
- `environment-oscer-explicit.txt`
- `package-list.txt`
- `software-stack.txt`

Commit these files for an archival release. They should come from the actual validated OSCER environment rather than being guessed or manually fabricated.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── THIRD_PARTY.md
├── CITATION.cff
├── CONTRIBUTING.md
├── environment.yml
├── src/
│   └── waveguide_validation_mpi.py
├── slurm/
│   ├── r40_mpi20.slurm
│   ├── r60_mpi80.slurm
│   ├── r80_mpi80.slurm
│   ├── r100_mpi160.slurm
│   └── r120_mpi160.slurm
├── scripts/
│   ├── setup_oscer.sh
│   ├── verify_environment.py
│   └── export_exact_environment.sh
├── results/
│   ├── mesh_convergence_summary.csv
│   ├── hpc_run_metadata.csv
│   └── reference_r120_result.txt
└── docs/
    ├── OSCER_COMMANDS.md
    ├── MODEL_PARAMETERS.md
    ├── REPRODUCIBILITY.md
    └── HPC_NOTES.md
```

## License

Original repository materials are licensed under the **BSD 3-Clause "New" or "Revised" License**. Third-party software installed by the environment retains its own license. See `LICENSE` and `THIRD_PARTY.md`.

Copyright (c) 2026 Ahmed Al-Nusairi.
