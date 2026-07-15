import pandas as pd

from atlas.viz.semaforo import (
    country_index,
    coverage,
    drop_one_pillar_sensitivity,
    load_coding,
    pillar_scores,
    render_semaforo_html,
)


def test_pillar_scores_treats_insufficient_evidence_as_nan():
    df = load_coding()
    pillars = pillar_scores(df)
    # Brasil and Haití have zero real evidence anywhere -> every pillar NaN.
    assert pillars.loc["BRA"].isna().all()
    assert pillars.loc["HTI"].isna().all()


def test_country_index_is_nan_when_no_coverage():
    df = load_coding()
    pillars = pillar_scores(df)
    idx = country_index(pillars)
    assert pd.isna(idx["BRA"])


def test_coverage_between_zero_and_one():
    df = load_coding()
    cov = coverage(df)
    assert cov.between(0, 1).all()
    assert cov["BRA"] == 0


def test_drop_one_pillar_sensitivity_runs_for_all_pillars():
    df = load_coding()
    pillars = pillar_scores(df)
    sens = drop_one_pillar_sensitivity(pillars)
    assert len(sens) == 8
    assert sens["spearman_rho"].dropna().between(-1, 1).all()


def test_semaforo_html_never_uses_color_alone():
    df = load_coding()
    pillars = pillar_scores(df)
    html = render_semaforo_html(pillars)
    assert "sin datos" in html
    assert 'class="visually-hidden"' in html
