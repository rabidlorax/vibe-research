#!/usr/bin/env python3
"""Bolometric luminosity of TOI-1227 from the bolometric flux and Galactic
position printed in Mann et al. 2022 (arXiv:2110.09531v2, stellar table),
compared with the luminosity printed in the same table.

Usage: python src/toi1227_luminosity.py   (no input, no network)
"""
import math

F_BOL = 7.87e-11                     # erg cm^-2 s^-1, as printed
X, Y, Z = 51.34, -85.22, -16.95      # pc, as printed
L_PRINTED = 2.51e-3                  # L_sun, as printed
R, TEFF = 0.56, 3072.0               # R_sun, K, as printed
PC_CM, L_SUN = 3.0856775814913673e18, 3.828e33   # IAU 2015 nominal L_sun, erg/s

d = math.sqrt(X * X + Y * Y + Z * Z)
L = 4 * math.pi * (d * PC_CM) ** 2 * F_BOL / L_SUN
L_sb = R**2 * (TEFF / 5772.0) ** 4
print(f"distance {d:.1f} pc")
print(f"L from F_bol and distance: {L:.4f} L_sun")
print(f"L from R and Teff:         {L_sb:.4f} L_sun")
print(f"L printed:                 {L_PRINTED:.5f} L_sun (ratio to F_bol value {L_PRINTED / L:.3f})")
