# Bare SOI waveguide reference model

## Device
- Structure: straight silicon-on-insulator (SOI) strip waveguide
- Propagation direction: +x
- Operating wavelength: 1550 nm = 1.550 um
- Silicon core width: 450 nm = 0.450 um
- Silicon core height: 220 nm = 0.220 um
- Silicon refractive index: n_Si = 3.476
- Silicon relative permittivity: epsilon_Si = 12.0826
- Silicon dioxide refractive index: n_SiO2 = 1.44
- Silicon dioxide relative permittivity: epsilon_SiO2 = 2.0736
- Air refractive index: n_air = 1.00
- Physical SiO2 undercladding: 1.000 um
- Air above core: 1.000 um
- Non-PML transverse span: 2.000 um
- PML thickness: 0.500 um

## Source and monitors
- Source x position: -3.000 um
- Input monitor x position: -2.500 um
- Output monitor x position: +2.500 um
- Exact monitor separation: 5.000 um
- Source: Meep `EigenModeSource`
- Mode: fundamental TE-like eigenmode, band 1
- Eigenmode k-point: (1, 0, 0)
- `eig_match_freq = True`
- `eig_parity = NO_PARITY`
- Center frequency: 1 / 1.55 = 0.645161 1/um
- Gaussian source bandwidth: 0.10 times center frequency

## Computational domain
Nominal dimensions including PML:
- Lx = 8.000 um
- Ly = 3.000 um
- Lz = 3.220 um

At r120, Meep realizes Lz as 3.21667 um because the requested cell size is rounded to the spatial grid.

## Measurement
Forward modal transmission:
`T = P_TE0,out / P_TE0,in`

with `P proportional to |alpha|^2` from Meep eigenmode coefficients.

For the uniform, lossless reference section, the analytical expectation is `T = 1`.

The time-domain simulation uses `stop_when_fields_decayed` with an electric-field decay threshold of `1e-9` evaluated at the output-monitor location.
