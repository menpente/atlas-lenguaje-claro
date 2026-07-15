from atlas.build.anexos import build_all


def test_build_all_generates_four_anexos():
    written = build_all()
    assert len(written) == 4


def test_quien_es_quien_flags_the_dbeaver_limitation():
    written = build_all()
    path = [p for p in written if "quien_es_quien" in p][0]
    content = open(path, encoding="utf-8").read()
    assert "DBeaver" in content
    assert "parcialmente" in content
