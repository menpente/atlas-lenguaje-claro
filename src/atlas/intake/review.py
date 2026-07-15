"""Aplica un paso de control de calidad automatizado sobre los candidatos
de P3 y promueve lo que pasa a data/processed/records/.

IMPORTANTE — esto NO es la revisión humana que describe el plan (sección
4: "a human sets verified ∈ {ok, fix, drop}"). No hay una persona
distinta del extractor disponible en este entorno para hacerlo. Lo que
este módulo hace es un control heurístico y determinista: descarta
duplicados, campos definitorios vacíos y artefactos de plantilla, y deja
todo lo demás marcado `verified="ok"` con una columna `confianza` que
señala los campos derivados por heurística (`tipo` de institución no
reconocido, `vinculante` de leyes) para que una revisión humana futura
sepa por dónde empezar. Ver metodologia.qmd, sección P4, para la
justificación completa y la limitación que esto implica.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import pandas as pd

from atlas.config import DATA_INTERIM, DATA_PROCESSED

INTERIM_RECORDS = DATA_INTERIM / "records"
PROCESSED_RECORDS = DATA_PROCESSED / "records"

_DEFINING_FIELD = {
    "leyes": "titulo",
    "proyectos": "nombre",
    "cursos": "nombre",
    "instituciones": "nombre",
    "encuentros": "nombre",
}

_ONLY_PUNCT_RE = re.compile(r"^[\W_]*$", re.UNICODE)


@dataclass
class QaDrop:
    pillar: str
    reason: str
    nombre_o_titulo: str
    iso3: str


def _is_blank_or_punct(value) -> bool:
    if value is None or (isinstance(value, float)) or not str(value).strip():
        return True
    return bool(_ONLY_PUNCT_RE.match(str(value).strip()))


def qa_pillar(pillar: str, df: pd.DataFrame) -> tuple[pd.DataFrame, list[QaDrop]]:
    field = _DEFINING_FIELD[pillar]
    dropped: list[QaDrop] = []
    seen: set[tuple[str, str, str]] = set()
    keep_mask = []
    confidence = []

    for row in df.itertuples():
        value = getattr(row, field)
        iso3 = row.iso3
        fuente = row.fuente_file_id
        dedupe_key = (iso3, str(value).strip().lower(), fuente)

        if _is_blank_or_punct(value):
            dropped.append(
                QaDrop(pillar, "campo definitorio vacío o sin contenido", str(value), iso3)
            )
            keep_mask.append(False)
            confidence.append(None)
            continue
        if _is_blank_or_punct(getattr(row, "cita", None)):
            dropped.append(QaDrop(pillar, "cita vacía", str(value), iso3))
            keep_mask.append(False)
            confidence.append(None)
            continue
        if dedupe_key in seen:
            dropped.append(QaDrop(pillar, "duplicado (mismo país+nombre+fuente)", str(value), iso3))
            keep_mask.append(False)
            confidence.append(None)
            continue
        seen.add(dedupe_key)
        keep_mask.append(True)

        # Campos derivados por heurística en P3, no leídos directamente de una
        # afirmación explícita del texto fuente: se marcan de baja confianza
        # para que una revisión humana los priorice.
        if pillar == "instituciones" and getattr(row, "tipo", None) == "otro":
            confidence.append("baja")
        elif pillar == "leyes":
            confidence.append("baja")  # vinculante siempre es heurístico, ver metodologia.qmd
        else:
            confidence.append("alta")

    kept = df[keep_mask].copy()
    kept["confianza"] = [c for c, keep in zip(confidence, keep_mask, strict=True) if keep]
    kept["verified"] = "ok"
    kept.insert(0, "record_id", [f"{pillar}_{i:04d}" for i in range(len(kept))])
    return kept, dropped


def run_all() -> dict[str, int]:
    PROCESSED_RECORDS.mkdir(parents=True, exist_ok=True)
    all_dropped: list[QaDrop] = []
    counts: dict[str, int] = {}

    for pillar in _DEFINING_FIELD:
        src_path = INTERIM_RECORDS / f"{pillar}.csv"
        if not src_path.exists():
            continue
        df = pd.read_csv(src_path)
        kept, dropped = qa_pillar(pillar, df)
        all_dropped.extend(dropped)
        counts[pillar] = len(kept)
        kept.to_csv(PROCESSED_RECORDS / f"{pillar}.csv", index=False)

    dropped_df = pd.DataFrame(
        [
            {
                "pillar": d.pillar,
                "reason": d.reason,
                "nombre_o_titulo": d.nombre_o_titulo,
                "iso3": d.iso3,
            }
            for d in all_dropped
        ]
    )
    dropped_df.to_csv(PROCESSED_RECORDS / "_qa_dropped.csv", index=False)
    counts["_qa_dropped"] = len(all_dropped)
    return counts


def main() -> None:
    counts = run_all()
    for pillar, n in counts.items():
        print(f"{pillar}: {n}")


if __name__ == "__main__":
    main()
