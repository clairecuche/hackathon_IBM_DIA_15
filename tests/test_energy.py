from backend import energy


def test_known_country():
    mix = energy.get_energy_mix_for_country("France")
    assert isinstance(mix, dict)
    # France mapping contains 'nuclear' in our sample data
    assert "nuclear" in mix


def test_unknown_country_fallback():
    mix = energy.get_energy_mix_for_country("Narnia")
    # fallback returns a dict with approximate keys
    assert isinstance(mix, dict)
    assert sum(mix.values()) > 0
