"""Codifica pldi_coding.csv a partir de los registros verificados de P4.

Este es el "coder" documentado que el plan permite en la sección 6
("an LLM coder under the identical rubric with sources attached is
acceptable if documented"): cada puntuación se deriva de una regla
determinista y explícita sobre el número de registros verificados que
cumplen un filtro por pilar/indicador — no es una lectura cualitativa
fina de cada ancla de `rubric.md`, y se documenta como tal.

Regla de conteo (idéntica para todos los indicadores con evidencia
disponible, ver metodologia.qmd P5 para la justificación):
    0 registros -> 0
    1 registro  -> 1
    2-3         -> 2
    4-6         -> 3
    7+          -> 4

Pilares sin ninguna fuente todavía (Publicaciones, Academia,
Herramientas, Ciudadanía) se codifican `score=0, insufficient_evidence=True`
en los 23 países: no es un "0 tras búsqueda documentada" (ancla real de
nivel 0), es ausencia de intake, y por eso se excluyen del índice
agregado en P7 en vez de contar como un cero real.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pandas as pd

from atlas.config import COUNTRY_UNIVERSE, DATA_CODING, DATA_PROCESSED, PILLARS
from atlas.schemas import PldiCoding

RECORDS_DIR = DATA_PROCESSED / "records"
CODER = "claude-sonnet-5 (P5 automated rule-based coder, ver metodologia.qmd)"

PILLARS_WITHOUT_SOURCE = {"publicaciones", "academia", "herramientas", "ciudadania"}


def _count_to_score(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n <= 3:
        return 2
    if n <= 6:
        return 3
    return 4


def _load(pillar: str) -> pd.DataFrame:
    path = RECORDS_DIR / f"{pillar}.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _filtered_ids(df: pd.DataFrame, iso3: str, mask: pd.Series) -> list[str]:
    subset = df[(df["iso3"] == iso3) & mask]
    return subset["record_id"].tolist()


def build_leyes_indicators(iso3: str, leyes: pd.DataFrame) -> dict[str, list[str]]:
    if leyes.empty:
        return {"a": [], "b": [], "c": []}
    sector_ambitos = {
        "Derecho Sanitario",
        "Derechos Sanitarios",
        "Derechos de Consumidor",
        "Procedimiento Administrativo",
        "Derechos Judiciales",
        "Justicia y Derechos Lingüísticos",
    }
    a = _filtered_ids(leyes, iso3, leyes["ambito"] == "Lenguaje Claro")
    b = _filtered_ids(leyes, iso3, leyes["ambito"].isin(sector_ambitos))
    c = _filtered_ids(leyes, iso3, leyes["tipo"].isin(["norma_privada", "convenio"]))
    return {"a": a, "b": b, "c": c}


def build_instituciones_indicators(iso3: str, inst: pd.DataFrame) -> dict[str, list[str]]:
    if inst.empty:
        return {"a": [], "b": [], "c": []}
    a = _filtered_ids(inst, iso3, inst["tipo"].isin(["ministerio", "gobierno", "instituto"]))
    b = _filtered_ids(inst, iso3, inst["tipo"].isin(["red", "comision"]))
    c = _filtered_ids(inst, iso3, inst["tipo"] == "poder_judicial")
    return {"a": a, "b": b, "c": c}


def build_proyectos_indicators(iso3: str, proy: pd.DataFrame) -> dict[str, list[str]]:
    if proy.empty:
        return {"a": [], "b": [], "c": []}
    admin_mask = proy["area"].fillna("").str.contains("admin", case=False)
    a = _filtered_ids(proy, iso3, admin_mask)
    b = _filtered_ids(proy, iso3, pd.Series(True, index=proy.index))
    return {"a": a, "b": b, "c": []}  # c: sin evaluación/monitoreo extraído todavía


def build_formacion_indicators(
    iso3: str, cursos: pd.DataFrame, encuentros: pd.DataFrame, inst: pd.DataFrame
) -> dict[str, list[str]]:
    a = _filtered_ids(cursos, iso3, pd.Series(True, index=cursos.index)) if not cursos.empty else []
    b = (
        _filtered_ids(encuentros, iso3, pd.Series(True, index=encuentros.index))
        if not encuentros.empty
        else []
    )
    c = _filtered_ids(inst, iso3, inst["tipo"] == "asociacion") if not inst.empty else []
    return {"a": a, "b": b, "c": c}


def code_all() -> pd.DataFrame:
    leyes = _load("leyes")
    inst = _load("instituciones")
    proy = _load("proyectos")
    cursos = _load("cursos")
    encuentros = _load("encuentros")

    now = datetime.now(UTC)
    rows: list[PldiCoding] = []

    for iso3 in COUNTRY_UNIVERSE:
        indicators_by_pillar = {
            "leyes": build_leyes_indicators(iso3, leyes),
            "instituciones": build_instituciones_indicators(iso3, inst),
            "proyectos": build_proyectos_indicators(iso3, proy),
            "formacion": build_formacion_indicators(iso3, cursos, encuentros, inst),
        }
        for pillar in PILLARS:
            if pillar in PILLARS_WITHOUT_SOURCE:
                for indicator in ("a", "b", "c"):
                    rows.append(
                        PldiCoding(
                            iso3=iso3,
                            pillar=pillar,
                            indicator=indicator,
                            score=0,
                            coder=CODER,
                            coded_at=now,
                            confidence="baja",
                            insufficient_evidence=True,
                            evidence_note=(
                                "Sin documento fuente en Drive todavía (P2); "
                                "no es un cero tras búsqueda documentada."
                            ),
                        )
                    )
                continue

            evidence = indicators_by_pillar[pillar]
            for indicator in ("a", "b", "c"):
                ids = evidence[indicator]
                score = _count_to_score(len(ids))
                rows.append(
                    PldiCoding(
                        iso3=iso3,
                        pillar=pillar,
                        indicator=indicator,
                        score=score,
                        evidence_record_ids=ids,
                        coder=CODER,
                        coded_at=now,
                        confidence="baja",
                        insufficient_evidence=(score == 0),
                        evidence_note=(
                            None
                            if ids
                            else "Sin registros verificados para este indicador."
                        ),
                    )
                )
    return pd.DataFrame([r.model_dump(mode="json") for r in rows])


def main() -> None:
    df = code_all()
    out_path = DATA_CODING / "pldi_coding.csv"
    df.to_csv(out_path, index=False)
    print(f"Escrito {out_path}: {len(df)} filas ({df['iso3'].nunique()} países x 8 pilares x 3)")


if __name__ == "__main__":
    main()
