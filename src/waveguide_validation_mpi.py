#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import csv
from pathlib import Path
import meep as mp

LAMBDA0 = 1.550
WG_WIDTH = 0.450
WG_HEIGHT = 0.220
N_SI = 3.476
N_SIO2 = 1.44
UNDERCLAD = 1.000
AIR_ABOVE = 1.000
TRANSVERSE_SPAN = 2.000
VALIDATION_LENGTH = 5.000
DPML = 0.50


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--resolution",
        type=int,
        default=40,
        help="FDTD resolution in pixels/um",
    )
    args = parser.parse_args()
    resolution = args.resolution

    fcen = 1.0 / LAMBDA0
    fwidth = 0.10 * fcen

    source_x = -3.00
    input_monitor_x = -2.50
    output_monitor_x = +2.50
    x_nonpml = 7.00

    sx = x_nonpml + 2 * DPML
    sy = TRANSVERSE_SPAN + 2 * DPML
    z_nonpml = UNDERCLAD + WG_HEIGHT + AIR_ABOVE
    sz = z_nonpml + 2 * DPML
    cell = mp.Vector3(sx, sy, sz)

    silicon = mp.Medium(index=N_SI)
    sio2 = mp.Medium(index=N_SIO2)

    oxide_height_with_pml = UNDERCLAD + DPML
    oxide_center_z = -(
        WG_HEIGHT / 2
        + oxide_height_with_pml / 2
    )

    geometry = [
        mp.Block(
            material=sio2,
            center=mp.Vector3(0, 0, oxide_center_z),
            size=mp.Vector3(mp.inf, mp.inf, oxide_height_with_pml),
        ),
        mp.Block(
            material=silicon,
            center=mp.Vector3(0, 0, 0),
            size=mp.Vector3(mp.inf, WG_WIDTH, WG_HEIGHT),
        ),
    ]

    source = mp.EigenModeSource(
        src=mp.GaussianSource(frequency=fcen, fwidth=fwidth),
        center=mp.Vector3(source_x, 0, 0),
        size=mp.Vector3(0, TRANSVERSE_SPAN, z_nonpml),
        direction=mp.X,
        eig_band=1,
        eig_kpoint=mp.Vector3(1, 0, 0),
        eig_match_freq=True,
        eig_parity=mp.NO_PARITY,
    )

    sim = mp.Simulation(
        cell_size=cell,
        boundary_layers=[mp.PML(DPML)],
        geometry=geometry,
        sources=[source],
        default_material=mp.air,
        resolution=resolution,
    )

    monitor_size = mp.Vector3(0, TRANSVERSE_SPAN, z_nonpml)

    input_monitor = sim.add_mode_monitor(
        fcen,
        0,
        1,
        mp.ModeRegion(
            center=mp.Vector3(input_monitor_x, 0, 0),
            size=monitor_size,
        ),
    )

    output_monitor = sim.add_mode_monitor(
        fcen,
        0,
        1,
        mp.ModeRegion(
            center=mp.Vector3(output_monitor_x, 0, 0),
            size=monitor_size,
        ),
    )

    if mp.am_master():
        print("\n==============================================")
        print("BARE SOI WAVEGUIDE VALIDATION")
        print("==============================================\n")
        print(f"Resolution        = {resolution} pixels/um")
        print(f"Wavelength        = {LAMBDA0} um")
        print(f"Si width          = {WG_WIDTH} um")
        print(f"Si height         = {WG_HEIGHT} um")
        print(f"Propagation test  = {VALIDATION_LENGTH} um")
        print(f"n(Si)             = {N_SI}")
        print(f"n(SiO2)           = {N_SIO2}\n")

    sim.run(
        until_after_sources=mp.stop_when_fields_decayed(
            50,
            mp.Ey,
            mp.Vector3(output_monitor_x, 0, 0),
            1e-9,
        )
    )

    input_coeff = sim.get_eigenmode_coefficients(
        input_monitor,
        [1],
        eig_parity=mp.NO_PARITY,
    )
    output_coeff = sim.get_eigenmode_coefficients(
        output_monitor,
        [1],
        eig_parity=mp.NO_PARITY,
    )

    a_input_forward = input_coeff.alpha[0, 0, 0]
    a_input_backward = input_coeff.alpha[0, 0, 1]
    a_output_forward = output_coeff.alpha[0, 0, 0]
    a_output_backward = output_coeff.alpha[0, 0, 1]

    p_input_forward = abs(a_input_forward) ** 2
    p_input_backward = abs(a_input_backward) ** 2
    p_output_forward = abs(a_output_forward) ** 2
    p_output_backward = abs(a_output_backward) ** 2

    transmission = p_output_forward / p_input_forward
    transmission_percent = 100.0 * transmission
    transmission_yield_percent = transmission_percent
    backward_input_ratio = p_input_backward / p_input_forward
    backward_output_ratio = p_output_backward / p_input_forward
    meets_99p5_requirement = transmission >= 0.995

    if mp.am_master():
        print("\n==============================================")
        print("RESULT")
        print("==============================================\n")
        print(f"Forward TE0 input power  = {p_input_forward:.12e}")
        print(f"Forward TE0 output power = {p_output_forward:.12e}\n")
        print(f"Transmission T           = {transmission:.8f}")
        print(f"Transmission             = {transmission_percent:.6f} %")
        print(f"Transmission yield       = {transmission_yield_percent:.6f} %\n")
        print(f"Input backward ratio     = {backward_input_ratio:.8e}")
        print(f"Output backward ratio    = {backward_output_ratio:.8e}\n")
        print("Acceptance requirement   = 99.500000 %")
        print(f"Numerical criterion met  = {meets_99p5_requirement}")
        print("\n==============================================")

        output_directory = Path("results")
        output_directory.mkdir(exist_ok=True)
        output_file = output_directory / (
            f"waveguide_r{resolution}_mpi{mp.count_processors()}.csv"
        )

        with output_file.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "resolution_px_per_um",
                "wavelength_um",
                "waveguide_width_um",
                "waveguide_height_um",
                "validation_length_um",
                "transmission",
                "transmission_percent",
                "transmission_yield_percent",
                "input_backward_ratio",
                "output_backward_ratio",
                "meets_99p5_percent_requirement",
                "mpi_ranks",
            ])
            writer.writerow([
                resolution,
                LAMBDA0,
                WG_WIDTH,
                WG_HEIGHT,
                VALIDATION_LENGTH,
                transmission,
                transmission_percent,
                transmission_yield_percent,
                backward_input_ratio,
                backward_output_ratio,
                meets_99p5_requirement,
                mp.count_processors(),
            ])

        print(f"\nSaved result to: {output_file}")


if __name__ == "__main__":
    main()
