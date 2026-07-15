"""Genera atlas/paises/{iso3}.qmd — nunca se edita a mano (ver plan, sección 6).

Solo incluye datos derivados de `data/processed/`. No se rellenan
población, PIB ni idiomas: esos campos no se han recolectado todavía
(ver `Ejemplo país COLOMBIA.docx` en Drive, que los deja en blanco) y
"no disponible" es preferible a inventarlos.
"""

from __future__ import annotations

import pandas as pd
from jinja2 import Template

from atlas.config import COUNTRY_UNIVERSE, DATA_PROCESSED, PILLARS, REPO_ROOT

PAISES_DIR = REPO_ROOT / "atlas" / "paises"

TEMPLATE = Template(
    trim_blocks=True,
    lstrip_blocks=True,
    source="""# {{ nombre }} {{ancla}}

## Datos básicos

Población, idiomas oficiales y cooficiales, variantes del español: **no disponible
todavía** — no se ha recolectado esta información en el intake (ver
`data/coding/country_universe.csv`).

## Semáforo de implantación

| Pilar | Puntuación media | Estado |
|---|---|---|
{% for pillar, label, score, estado in filas_semaforo -%}
| {{ label }} | {{ score }} | {{ estado }} |
{% endfor %}

**Índice**: {{ indice }} · **Cobertura de evidencia**: {{ cobertura }}% de los 24
indicadores tienen al menos un registro verificado.

## Instrumentos clave

{% if leyes.empty %}
Sin leyes verificadas todavía para este país.
{% else %}
{% for _, row in leyes.iterrows() -%}
{% set anio_txt = ", " ~ (row.anio | int) if row.anio and row.anio == row.anio else "" %}
{% set url_txt = " — [" ~ row.url_oficial ~ "](" ~ row.url_oficial ~ ")" if row.url_oficial and row.url_oficial == row.url_oficial else "" %}
- **{{ row.titulo }}** ({{ row.tipo }}{{ anio_txt }}){{ url_txt }}
{% endfor %}
{% endif %}

{% if not instituciones.empty %}
### Instituciones registradas

{% for _, row in instituciones.iterrows() -%}
- {{ row.nombre }} ({{ row.tipo }})
{% endfor %}
{% endif %}

## Nota metodológica

Ficha generada automáticamente desde `data/processed/` el {{ fecha }}. No editar a
mano — cualquier corrección debe hacerse en los registros de origen
(`data/processed/records/`) y regenerar con `make index`.
"""
)


def _semaforo_row(score: float | None) -> str:
    if score is None or pd.isna(score):
        return "sin datos"
    if score >= 3:
        return "verde"
    if score >= 2:
        return "ámbar"
    return "rojo"


def render_ficha(
    iso3: str, nombre: str, pldi_row: pd.Series, records: dict[str, pd.DataFrame]
) -> str:
    filas_semaforo = []
    for pillar, spec in PILLARS.items():
        score = pldi_row.get(pillar)
        score_display = "sin datos" if score is None or pd.isna(score) else f"{score:.1f}"
        filas_semaforo.append((pillar, spec["label"], score_display, _semaforo_row(score)))

    indice = "sin datos" if pd.isna(pldi_row.get("indice")) else f"{pldi_row['indice']:.1f}/100"
    cobertura = f"{pldi_row.get('cobertura', 0) * 100:.0f}"

    leyes = records.get("leyes", pd.DataFrame())
    leyes = leyes[leyes["iso3"] == iso3] if not leyes.empty else leyes
    instituciones = records.get("instituciones", pd.DataFrame())
    instituciones = (
        instituciones[instituciones["iso3"] == iso3] if not instituciones.empty else instituciones
    )

    return TEMPLATE.render(
        nombre=nombre,
        ancla=f"{{#sec-{iso3.lower()}}}",
        filas_semaforo=filas_semaforo,
        indice=indice,
        cobertura=cobertura,
        leyes=leyes,
        instituciones=instituciones,
        fecha="2026-07-13",
    )


def build_all() -> list[str]:
    pldi = pd.read_parquet(DATA_PROCESSED / "pldi.parquet").set_index("iso3")
    records = {
        pillar: pd.read_csv(DATA_PROCESSED / "records" / f"{pillar}.csv")
        for pillar in ("leyes", "instituciones", "proyectos", "cursos", "encuentros")
        if (DATA_PROCESSED / "records" / f"{pillar}.csv").exists()
    }

    PAISES_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for iso3, nombre in COUNTRY_UNIVERSE.items():
        content = render_ficha(iso3, nombre, pldi.loc[iso3], records)
        path = PAISES_DIR / f"{iso3.lower()}.qmd"
        path.write_text(content, encoding="utf-8")
        written.append(str(path))
    return written


def main() -> None:
    written = build_all()
    print(f"Generadas {len(written)} fichas de país en {PAISES_DIR}")


if __name__ == "__main__":
    main()
