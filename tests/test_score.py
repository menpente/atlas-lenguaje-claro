import pandas as pd

from atlas.build.score import _count_to_score, code_all
from atlas.config import COUNTRY_UNIVERSE, PILLARS


def test_count_to_score_boundaries():
    assert _count_to_score(0) == 0
    assert _count_to_score(1) == 1
    assert _count_to_score(3) == 2
    assert _count_to_score(6) == 3
    assert _count_to_score(7) == 4
    assert _count_to_score(100) == 4


def test_code_all_covers_full_universe():
    df = code_all()
    assert len(df) == len(COUNTRY_UNIVERSE) * len(PILLARS) * 3
    assert set(df["iso3"]) == set(COUNTRY_UNIVERSE)
    assert set(df["pillar"]) == set(PILLARS)


def test_code_all_scores_in_range_and_evidence_consistent():
    df = code_all()
    assert df["score"].between(0, 4).all()
    nonzero = df[df["score"] > 0]
    for _, row in nonzero.iterrows():
        has_evidence = isinstance(row["evidence_record_ids"], list) and len(
            row["evidence_record_ids"]
        ) > 0
        assert has_evidence or row["insufficient_evidence"]


def test_pillars_without_source_are_flagged_insufficient():
    df = code_all()
    no_source = df[df["pillar"].isin(["publicaciones", "academia", "herramientas", "ciudadania"])]
    assert (no_source["score"] == 0).all()
    assert no_source["insufficient_evidence"].all()


def test_pldi_coding_csv_round_trips():
    from atlas.config import DATA_CODING

    on_disk = pd.read_csv(DATA_CODING / "pldi_coding.csv")
    assert len(on_disk) == 552
