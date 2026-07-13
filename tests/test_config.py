from atlas.config import COUNTRY_UNIVERSE, NON_SOVEREIGN, PILLARS


def test_country_universe_size():
    assert len(COUNTRY_UNIVERSE) == 23


def test_non_sovereign_subset_of_universe():
    assert NON_SOVEREIGN <= set(COUNTRY_UNIVERSE)


def test_pillars_have_three_indicators():
    assert len(PILLARS) == 8
    for pillar, spec in PILLARS.items():
        assert set(spec["indicators"]) == {"a", "b", "c"}, pillar
