# HPC notes and scaling observations

## Successful reference configuration
The final r120 calculation completed using 160 MPI ranks across 8 OSCER nodes with 20 ranks per node and one OpenMP thread per rank.

SLURM accounting for the successful r120 job reported approximately 1:39:07 elapsed time. Meep reported 5920.7057 seconds of run time.

## Important scaling observation
A trial r120 allocation using 280 MPI ranks across 14 nodes did not reach normal FDTD timestep output after more than one hour and was canceled. The same physical r120 model subsequently ran successfully using 160 MPI ranks across 8 nodes.

This demonstrates that increasing MPI rank count does not necessarily reduce time-to-solution. Communication, synchronization, eigenmode-source initialization, and domain-decomposition overhead can dominate when the problem is over-parallelized.

For this reference problem, `r120_mpi160.slurm` is the validated high-resolution configuration.

## Grid-rounding warning
At r120, Meep reports that the grid volume is not an integer number of pixels and rounds the vertical cell dimension to 3.21667 um. This is expected for the nominal 3.220 um requested vertical extent at 120 pixels/um.
