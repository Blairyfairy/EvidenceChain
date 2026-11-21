"""Educational, non-operational RF link calculations (no targeting optimization)."""
import math

def fspl_db(frequency_mhz: float, distance_km: float) -> float:
    if frequency_mhz <= 0 or distance_km <= 0:
        raise ValueError('frequency and distance must be positive')
    return 32.44 + 20 * math.log10(frequency_mhz) + 20 * math.log10(distance_km)

def wavelength_m(frequency_mhz: float) -> float:
    if frequency_mhz <= 0:
        raise ValueError('frequency must be positive')
    return 299.792458 / frequency_mhz

def photon_energy_ev(frequency_mhz: float) -> float:
    if frequency_mhz <= 0:
        raise ValueError('frequency must be positive')
    return 4.135667696e-15 * frequency_mhz * 1e6
