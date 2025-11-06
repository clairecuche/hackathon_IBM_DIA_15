DEFAULT_PUE = 1.05  # midpoint (1.0 – 1.1)

# Electricity emission factors by country (kgCO2e/kWh)
# - generation: emissions from electricity production (including the energy mix)
# - t_and_d: network losses (Transmission & Distribution)
EMISSION_FACTORS = {
    "Australia": {"generation": 0.58023, "t_and_d": 0.03495},
    "France": {"generation": 0.04704, "t_and_d": 0.00420},
    "China": {"generation": 0.66307, "t_and_d": 0.04652},
    "Japan": {"generation": 0.43984, "t_and_d": 0.02163},
    "United States": {"generation": 0.35507, "t_and_d": 0.01811},
    "Brazil": {"generation": 0.06398, "t_and_d": 0.01276},
    "Ireland": {"generation": 0.26292, "t_and_d": 0.02091},
}

def _country_factor(country: str) -> float:
    """
    Computes the electricity emission factor (kgCO2e/kWh) for a given country.
    """
    if country not in EMISSION_FACTORS:
        raise KeyError(f"Unknown country: {country}. Not yet included in our country catalog.")

    f = EMISSION_FACTORS[country]
    required_keys = ["generation", "t_and_d"]
  
    # Basic checks
    for k in required_keys:
        if f.get(k) is None:
            raise ValueError(
                f"The field '{k}' is not defined for {country}. "
                "Please complete EMISSION_FACTORS with values in kgCO2e/kWh."
            )

        return f["generation"] + f["t_and_d"]


def compute_co2e_kg(
    energy_consumption_llm_total_kwh: float,
    country: str,
    pue: float = DEFAULT_PUE,
) -> float:
    """
    Converts the energy (kWh) of an LLM inference request into kgCO2e.

    Parameters
    ----------
    energy_consumption_llm_total_kwh : float
        Energy per request *already in kWh* (e.g., the column `energy_consumption_llm_total`).
    country : str
        Key of the country in EMISSION_FACTORS (e.g., "Australia", "France", ...).
    pue : float
        PUE (Power Usage Effectiveness) to apply (default = 1.05).

    Returns
    -------
    kgCO2e : float
        The resulting carbon emissions in kilograms of CO2 equivalent.
    """
    if energy_consumption_llm_total_kwh < 0:
        raise ValueError("Energy cannot be negative.")
    if not (0.8 <= pue <= 2.0):
        raise ValueError("PUE outside reasonable range (0.8–2.0).")

    ef = _country_factor(country)  # kgCO2e/kWh
    energy_with_pue = energy_consumption_llm_total_kwh * pue
    kg_co2e = energy_with_pue * ef
    return kg_co2e

def forest_area_acres(co2e_kg, duration_seconds, sequestration_rate_per_acre=1000):
    """
    Estimate acres of forest required to offset CO₂e emissions.

    Parameters:
        co2e_kg (float): total emissions in kilograms of CO₂e
        duration_seconds (float): duration of emissions in seconds
        sequestration_rate_per_acre (float): CO₂ absorbed per acre per year (kg CO₂/acre/year)
                                             default = 1000 kg CO₂/year/acre

    Returns:
        float: acres of forest required
    """
    SECONDS_PER_YEAR = 31_536_000
    years = duration_seconds / SECONDS_PER_YEAR
    return co2e_kg / (sequestration_rate_per_acre * years)

def co2e_to_google_searches(co2e_kg, co2_per_search=0.00123):
    """
    Convert CO₂e (in kg) to equivalent number of Google searches.
    Default emission per search = 1.23 g CO₂e (Everyone.Eco)
    """
    return co2e_kg / co2_per_search
