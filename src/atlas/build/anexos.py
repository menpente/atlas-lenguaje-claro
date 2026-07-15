"""Genera atlas/anexos/*.qmd a partir de data/processed/. No editar a mano."""

from __future__ import annotations

import pandas as pd

from atlas.config import COUNTRY_UNIVERSE, DATA_PROCESSED, REPO_ROOT

ANEXOS_DIR = REPO_ROOT / "atlas" / "anexos"

_SOURCE_DOCS = [
    ("Índice del Atlas", "1vlsdKknauVH9KegOnu9bvm7V5vw7HmxIFCjSAYwTQog"),
    ("00 Atlas_Lenguaje_Claro_Indice_Explicado.docx", "1e6nPBjCuNEFiNx1r2QDP7fewBnHPPKfj"),
    ("01 Atlas_Lenguaje_Claro_Cap1_Proyectos_Refinado.docx", "1ssEsITh2TCm7qI7OLK79BNTeX26m39Y6"),
    ("02 Atlas_Lenguaje_Claro_Cap2_Encuentros_Refinado.docx", "1EJr162UfAYDGIhDcsg6EC-YNR3Yo2bCy"),
    ("03 Atlas_Lenguaje_Claro_Cap3_Cursos.docx", "1VyM75p_CXQNX4vr2RI0lTHXOAdiaqgYb"),
    ("04 Atlas_Lenguaje_Claro_Cap4_Leyes.docx", "1M9C7wDLrk1OpDGkXvzX3KLlXaVN6RoQ-"),
    ("05 Atlas_Lenguaje_Claro_Cap5_Instituciones.docx", "13FSED3pQflH87uQOCVKr1YYgIfoRBMGV"),
    ("Leyes españolas.xlsx", "1_Rx7rBU85IK38HJJqXBV14xLfTwcA9kN"),
    ("Índice Atlas.xlsx", "1Nop9qlgbgdVt1wPMhD9vb8mM61H82uEG"),
    ("Ejemplo país COLOMBIA.docx", "15phBIZo0jS6e8Ve09wPFbUSrMy5W0qsf"),
]


def _load(pillar: str) -> pd.DataFrame:
    path = DATA_PROCESSED / "records" / f"{pillar}.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def build_bibliografia() -> str:
    lines = [
        "# Bibliografía {.unnumbered}",
        "",
        "Fuentes documentales usadas para el intake (P2) y la extracción (P3). "
        "Cada una tiene un `file_id` de Google Drive trazable en todos los "
        "registros de `data/processed/records/`.",
        "",
    ]
    for name, file_id in _SOURCE_DOCS:
        lines.append(f"- **{name}** (`{file_id}`)")
    return "\n".join(lines) + "\n"


def build_listado_leyes() -> str:
    leyes = _load("leyes")
    lines = ["# Listado de leyes {.unnumbered}", ""]
    if leyes.empty:
        lines.append("Sin leyes verificadas todavía.")
        return "\n".join(lines) + "\n"

    lines.append("| País | Título | Tipo | Año | Vinculante | URL |")
    lines.append("|---|---|---|---|---|---|")
    for _, row in leyes.sort_values(["iso3", "anio"]).iterrows():
        nombre_pais = COUNTRY_UNIVERSE.get(row["iso3"], row["iso3"])
        anio = "" if pd.isna(row["anio"]) else int(row["anio"])
        url = "" if pd.isna(row["url_oficial"]) else f"[enlace]({row['url_oficial']})"
        lines.append(
            f"| {nombre_pais} | {row['titulo']} | {row['tipo']} | {anio} | "
            f"{row['vinculante']} | {url} |"
        )
    return "\n".join(lines) + "\n"


def build_listado_instituciones() -> str:
    inst = _load("instituciones")
    lines = ["# Listado de instituciones {.unnumbered}", ""]
    if inst.empty:
        lines.append("Sin instituciones verificadas todavía.")
        return "\n".join(lines) + "\n"

    lines.append("| País | Institución | Tipo |")
    lines.append("|---|---|---|")
    for _, row in inst.sort_values(["iso3", "nombre"]).iterrows():
        nombre_pais = COUNTRY_UNIVERSE.get(row["iso3"], row["iso3"])
        lines.append(f"| {nombre_pais} | {row['nombre']} | {row['tipo']} |")
    return "\n".join(lines) + "\n"


def build_quien_es_quien() -> str:
    inst = _load("instituciones")
    lines = [
        "# Quién es quién {.unnumbered}",
        "",
        "**Limitación conocida:** este anexo agrupa organizaciones por tipo, no "
        "personas. Existe una base de contactos individuales "
        "(`COPIA BD DBeaver.xlsx`, ~280 personas) pero solo se cacheó "
        "parcialmente en P2 (excede el límite de una lectura interactiva) y no "
        "se ha usado como fuente en P3 — ver `metodologia.qmd`. Un verdadero "
        "\"quién es quién\" de personas requiere primero recuperar ese archivo "
        "completo con credenciales de service account.",
        "",
    ]
    if inst.empty:
        lines.append("Sin organizaciones verificadas todavía.")
        return "\n".join(lines) + "\n"

    for tipo, group in inst.groupby("tipo"):
        lines.append(f"## {tipo.replace('_', ' ').title()}")
        lines.append("")
        for _, row in group.sort_values("nombre").iterrows():
            nombre_pais = COUNTRY_UNIVERSE.get(row["iso3"], row["iso3"])
            lines.append(f"- {row['nombre']} ({nombre_pais})")
        lines.append("")
    return "\n".join(lines) + "\n"


def build_all() -> list[str]:
    ANEXOS_DIR.mkdir(parents=True, exist_ok=True)
    builders = {
        "bibliografia.qmd": build_bibliografia,
        "listado_leyes.qmd": build_listado_leyes,
        "listado_instituciones.qmd": build_listado_instituciones,
        "quien_es_quien.qmd": build_quien_es_quien,
    }
    written = []
    for filename, builder in builders.items():
        path = ANEXOS_DIR / filename
        path.write_text(builder(), encoding="utf-8")
        written.append(str(path))
    return written


def main() -> None:
    written = build_all()
    print(f"Generados {len(written)} anexos en {ANEXOS_DIR}")


if __name__ == "__main__":
    main()
