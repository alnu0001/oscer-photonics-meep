# Third-party software and licenses

The BSD 3-Clause License in this repository applies to original repository materials authored for this project, including the environment specifications, helper scripts, SLURM workflows, documentation, and project simulation scripts unless a file states otherwise.

This repository does **not** relicense third-party software. The environment specification installs third-party packages from their respective distribution channels, and each dependency remains governed by its own license.

Important examples include:
- Meep / PyMeep - GNU General Public License (GPL), as distributed by the Meep project.
- MPB (MIT Photonic Bands) - its upstream project license.
- Python - Python Software Foundation license.
- NumPy, SciPy, Matplotlib, mpi4py, MPICH, Mamba/Conda and other dependencies - their respective upstream licenses.

No Meep source tree or Meep binary distribution is vendored in this repository. Users obtain dependencies through the documented Mamba/Conda environment creation process.
