import csv
from pathlib import Path

from atlas.config import COUNTRY_UNIVERSE, NON_SOVEREIGN, PILLARS

CODING_DIR = Path(__file__).resolve().parents[1] / "data" / "coding"


def test_country_universe_csv_matches_config():
    rows = list(csv.DictReader((CODING_DIR / "country_universe.csv").open(encoding="utf-8")))
    assert {r["iso3"] for r in rows} == set(COUNTRY_UNIVERSE)
    non_sovereign_rows = {r["iso3"] for r in rows if r["soberania"] == "no_soberano"}
    assert non_sovereign_rows == NON_SOVEREIGN
    for row in rows:
        if row["iso3"] in NON_SOVEREIGN:
            assert row["incluir_en_indice_numerico"] == "false"
        else:
            assert row["incluir_en_indice_numerico"] == "true"


def test_rubric_has_anchor_for_every_pillar_indicator():
    text = (CODING_DIR / "rubric.md").read_text(encoding="utf-8")
    for pillar_spec in PILLARS.values():
        assert pillar_spec["label"] in text, pillar_spec["label"]
    # 8 pillars x 3 indicators x 5 levels = 120 anchor rows in level tables
    anchor_rows = [
        line
        for line in text.splitlines()
        if line.startswith("| ") and line.split("|")[1].strip() in {"0", "1", "2", "3", "4"}
    ]
    assert len(anchor_rows) == 8 * 3 * 5


def test_pldi_coding_csv_header_matches_schema():
    header = (CODING_DIR / "pldi_coding.csv").read_text(encoding="utf-8").splitlines()[0]
    expected = {
        "iso3",
        "pillar",
        "indicator",
        "score",
        "evidence_record_ids",
        "evidence_note",
        "coder",
        "coded_at",
        "confidence",
        "insufficient_evidence",
    }
    assert set(header.split(",")) == expected
