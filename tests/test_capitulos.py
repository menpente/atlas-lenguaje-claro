from atlas.build.capitulos import build_all


def test_build_all_generates_eight_chapters():
    written = build_all()
    assert len(written) == 8


def test_chapters_without_source_say_so_explicitly():
    written = build_all()
    academia = [p for p in written if "academia" in p][0]
    content = open(academia, encoding="utf-8").read()
    assert "Sin fuente documental todavía" in content


def test_leyes_chapter_has_a_sourced_case_study():
    written = build_all()
    leyes = [p for p in written if "leyes" in p][0]
    content = open(leyes, encoding="utf-8").read()
    assert "## Caso:" in content
    assert "Fuente: `" in content
