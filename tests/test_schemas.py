from datetime import datetime

import pytest
from pydantic import ValidationError

from atlas.schemas import LeyRecord, PldiCoding, TipoLey


def test_ley_record_requires_provenance():
    record = LeyRecord(
        iso3="ESP",
        fuente_file_id="abc123",
        cita="Ley 39/2015 obliga a la administracion a usar lenguaje claro",
        tipo=TipoLey.ley,
        titulo="Ley 39/2015",
        ambito="administracion",
        vinculante=True,
    )
    assert record.iso3 == "ESP"


def test_ley_record_rejects_unknown_country():
    with pytest.raises(ValidationError):
        LeyRecord(
            iso3="XYZ",
            fuente_file_id="abc123",
            cita="cita de prueba",
            tipo=TipoLey.ley,
            titulo="Ley ficticia",
            ambito="administracion",
            vinculante=True,
        )


def test_ley_record_rejects_long_cita():
    with pytest.raises(ValidationError):
        LeyRecord(
            iso3="ESP",
            fuente_file_id="abc123",
            cita=" ".join(["palabra"] * 26),
            tipo=TipoLey.ley,
            titulo="Ley ficticia",
            ambito="administracion",
            vinculante=True,
        )


def test_pldi_coding_zero_score_needs_no_evidence():
    coding = PldiCoding(
        iso3="HTI",
        pillar="leyes",
        indicator="a",
        score=0,
        coder="rdlf",
        coded_at=datetime.now(),
    )
    assert coding.score == 0


def test_pldi_coding_nonzero_score_requires_evidence_or_flag():
    with pytest.raises(ValidationError):
        PldiCoding(
            iso3="HTI",
            pillar="leyes",
            indicator="a",
            score=2,
            coder="rdlf",
            coded_at=datetime.now(),
        )

    # marcar insufficient_evidence explicitamente si no hay registros
    coding = PldiCoding(
        iso3="HTI",
        pillar="leyes",
        indicator="a",
        score=2,
        coder="rdlf",
        coded_at=datetime.now(),
        insufficient_evidence=True,
    )
    assert coding.insufficient_evidence
