from atlas.config import COUNTRY_UNIVERSE
from atlas.intake.extract import (
    extract_cursos,
    extract_encuentros,
    extract_instituciones,
    extract_leyes,
    extract_proyectos,
    normalize_country,
)


def test_normalize_country_accepts_known_aliases():
    assert normalize_country("México") == "MEX"
    assert normalize_country("Mexico") == "MEX"
    assert normalize_country("España") == "ESP"


def test_normalize_country_rejects_out_of_universe():
    assert normalize_country("Alemania") is None
    assert normalize_country("País no especificado") is None
    assert normalize_country("Luxemburgo") is None


def test_extract_leyes_every_record_has_valid_iso3_and_short_cita():
    records, _dropped = extract_leyes("1_Rx7rBU85IK38HJJqXBV14xLfTwcA9kN")
    assert len(records) > 0
    for r in records:
        assert r.iso3 in COUNTRY_UNIVERSE
        assert len(r.cita.split()) <= 25
        assert r.fuente_file_id == "1_Rx7rBU85IK38HJJqXBV14xLfTwcA9kN"


def test_extract_proyectos_finds_known_project():
    records, _dropped = extract_proyectos("1ssEsITh2TCm7qI7OLK79BNTeX26m39Y6")
    names = {r.nombre for r in records}
    assert "CLAPPI" in names


def test_extract_cursos_produces_records():
    records, _dropped = extract_cursos("1VyM75p_CXQNX4vr2RI0lTHXOAdiaqgYb")
    assert len(records) > 10


def test_extract_instituciones_drops_out_of_universe_countries():
    records, dropped = extract_instituciones("13FSED3pQflH87uQOCVKr1YYgIfoRBMGV")
    assert all(r.iso3 in COUNTRY_UNIVERSE for r in records)
    dropped_countries = {d.reason for d in dropped}
    assert any("Alemania" in reason for reason in dropped_countries)


def test_extract_encuentros_produces_records():
    records, _dropped = extract_encuentros("1EJr162UfAYDGIhDcsg6EC-YNR3Yo2bCy")
    assert len(records) > 10
