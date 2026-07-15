import pandas as pd

from atlas.intake.review import qa_pillar


def test_qa_drops_blank_defining_field():
    df = pd.DataFrame(
        [
            {"iso3": "ESP", "fuente_file_id": "x", "cita": "algo", "nombre": "  "},
            {"iso3": "ESP", "fuente_file_id": "x", "cita": "algo", "nombre": "Proyecto real"},
        ]
    )
    kept, dropped = qa_pillar("proyectos", df)
    assert len(kept) == 1
    assert len(dropped) == 1
    assert kept.iloc[0]["nombre"] == "Proyecto real"


def test_qa_drops_duplicates():
    df = pd.DataFrame(
        [
            {"iso3": "ESP", "fuente_file_id": "x", "cita": "algo", "nombre": "Curso A"},
            {"iso3": "ESP", "fuente_file_id": "x", "cita": "otra cita", "nombre": "Curso A"},
        ]
    )
    kept, dropped = qa_pillar("cursos", df)
    assert len(kept) == 1
    assert dropped[0].reason.startswith("duplicado")


def test_qa_flags_low_confidence_institucion_tipo_otro():
    df = pd.DataFrame(
        [{"iso3": "ESP", "fuente_file_id": "x", "cita": "algo", "nombre": "X", "tipo": "otro"}]
    )
    kept, _dropped = qa_pillar("instituciones", df)
    assert kept.iloc[0]["confianza"] == "baja"
