#!/usr/bin/env python3
"""Verify the Meep/MPI software environment used by this repository."""

import sys
import meep as mp
import numpy as np
import scipy
import matplotlib
import mpi4py

if mp.am_master():
    print(f"Python: {sys.version.split()[0]}")
    print(f"Meep: {mp.__version__}")
    print(f"MPI-enabled Meep: {mp.with_mpi()}")
    print(f"Meep processors visible: {mp.count_processors()}")
    print(f"NumPy: {np.__version__}")
    print(f"SciPy: {scipy.__version__}")
    print(f"Matplotlib: {matplotlib.__version__}")
    print(f"mpi4py: {mpi4py.__version__}")

if not mp.with_mpi():
    raise RuntimeError("Meep is not MPI-enabled. Install the MPI-enabled PyMeep build.")
