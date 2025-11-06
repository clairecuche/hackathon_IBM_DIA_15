"""Energy mix utilities.

Provide a small function to map a user's country to a representative energy
mix (fractions summing to 1). This is intentionally simple and extensible.
"""
from typing import Dict


_COUNTRY_ENERGY_MIX = {
    "france": {"nuclear": 0.6, "renewables": 0.3, "gas": 0.06, "grid": 0.04},
    "germany": {"coal": 0.25, "renewables": 0.5, "gas": 0.15, "nuclear": 0.0, "grid": 0.1},
    "uk": {"renewables": 0.4, "gas": 0.35, "nuclear": 0.15, "grid": 0.1},
    "united kingdom": {"renewables": 0.4, "gas": 0.35, "nuclear": 0.15, "grid": 0.1},
    "united states": {"gas": 0.4, "coal": 0.2, "renewables": 0.25, "nuclear": 0.1, "grid": 0.05},
    "usa": {"gas": 0.4, "coal": 0.2, "renewables": 0.25, "nuclear": 0.1, "grid": 0.05},
    "india": {"coal": 0.6, "renewables": 0.25, "gas": 0.1, "grid": 0.05},
    "china": {"coal": 0.6, "renewables": 0.25, "nuclear": 0.08, "grid": 0.07},
}


def get_energy_mix_for_country(country: str) -> Dict[str, float]:
    """Return an energy mix dict for the given country name or code.

    The lookup is case-insensitive and falls back to a simple global mix if
    the country is unknown.
    """
    if not country:
        return {"grid": 1.0}
    key = country.strip().lower()
    mix = _COUNTRY_ENERGY_MIX.get(key)
    if mix:
        return mix

    # try a loose match for common abbreviations
    short = key.replace(" ", "")
    for k in _COUNTRY_ENERGY_MIX:
        if k.replace(" ", "") == short:
            return _COUNTRY_ENERGY_MIX[k]

    # fallback global mix (approx)
    return {"renewables": 0.3, "gas": 0.3, "coal": 0.2, "nuclear": 0.1, "grid": 0.1}
