# Reproducibility protocol

## Goal
A researcher with access to the OU OSCER cluster should be able to rebuild the `photonics_mpi` environment, verify MPI-enabled Meep, execute the supplied SLURM jobs, and recover the reference SOI waveguide transmission values within a stated numerical tolerance.

## Environment levels
1. `environment.yml` - portable reconstruction specification.
2. `environment-oscer-exact.yml` - full resolved Conda environment exported from OSCER.
3. `environment-oscer-explicit.txt` - exact package URLs/builds from the validated environment.
4. `package-list.txt` - human-readable package inventory.
5. `software-stack.txt` - Python, Meep, MPI, Mamba, host, kernel, and loaded-module provenance.

Files 2-5 must be generated on OSCER from the actual validated environment by running `scripts/export_exact_environment.sh`.

## Reference numerical result
The r120 reference case uses:
- resolution: 120 pixels/um
- 8 nodes
- 160 MPI ranks total
- 20 ranks per node
- 1 OpenMP thread per MPI rank
- 60,005 timesteps
- termination time: 250.02083333333334 Meep time units
- transmission: 1.00003722
- transmission percentage: 100.003722%
- input backward ratio: 1.49296142e-07
- output backward ratio: 1.53197790e-07
- field-decay ratio: approximately 1.4978980551e-14

Exact wall-clock runtime is not required to match because cluster load, communication, node allocation, and scheduler conditions vary.

## Mesh-independence criterion
The study used a practical mesh-independence criterion of less than 0.01% relative change between the two finest transmission values, together with a small deviation from the known analytical limit `T = 1`.

The r100-to-r120 transmission change is approximately 0.001291%.
