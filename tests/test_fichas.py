from atlas.build.fichas import build_all


def test_build_all_generates_23_fichas():
    written = build_all()
    assert len(written) == 23


def test_ficha_never_fabricates_population():
    written = build_all()
    esp = [p for p in written if p.endswith("esp.qmd")][0]
    content = open(esp, encoding="utf-8").read()
    assert "no disponible" in content


def test_ficha_has_no_broken_bracket_url():
    written = build_all()
    esp = [p for p in written if p.endswith("esp.qmd")][0]
    content = open(esp, encoding="utf-8").read()
    assert "[url truncado]" not in content
