"""Genera atlas/capitulos/0X-*.qmd a partir de data/processed/. No editar a mano.

Las introducciones de Leyes/Instituciones/Proyectos/Cursos/Encuentros son las
del manuscrito original en Drive (fuente citada). Publicaciones/Academia/
Herramientas/Ciudadanía no tienen manuscrito todavía — su párrafo lo dice
explícitamente en vez de inventar contenido editorial.
"""

from __future__ import annotations

import pandas as pd

from atlas.config import COUNTRY_UNIVERSE, DATA_PROCESSED, PILLARS, REPO_ROOT

CAPITULOS_DIR = REPO_ROOT / "atlas" / "capitulos"

_INTROS = {
    "leyes": (
        "El reconocimiento legal del derecho a un lenguaje claro constituye un paso "
        "fundamental para su consolidación como política pública. Las leyes "
        "recopiladas en este capítulo muestran cómo distintos países iberoamericanos "
        "han comenzado a integrar el lenguaje claro en sus marcos normativos, desde "
        "la sanidad y la justicia hasta la transparencia administrativa."
    ),
    "instituciones": (
        "Las instituciones desempeñan un papel clave en la promoción y consolidación "
        "del lenguaje claro. Este capítulo reúne a academias, organismos públicos, "
        "universidades y entidades que, en distintos países, han impulsado proyectos, "
        "políticas y prácticas para garantizar el derecho a comprender."
    ),
    "proyectos": (
        "Los proyectos constituyen el motor práctico del lenguaje claro. Son las "
        "experiencias piloto, las guías, los libros y los recursos que buscan "
        "transformar la comunicación en distintos ámbitos sociales, jurídicos y "
        "administrativos."
    ),
    "publicaciones": (
        "**Sin fuente documental todavía.** No existe una carpeta dedicada a guías y "
        "manuales en el Drive del proyecto (ver metodologia.qmd, P2). Este capítulo "
        "se generará cuando exista una fuente que extraer."
    ),
    "formacion": (
        "La formación es clave para profesionalizar el lenguaje claro y extenderlo a "
        "sectores estratégicos como la administración pública, la justicia y los "
        "medios de comunicación. Los cursos recogidos muestran la diversidad de "
        "enfoques, instituciones y países que han apostado por enseñar a comunicar "
        "con claridad. Los encuentros — congresos, jornadas, seminarios — son "
        "espacios donde se comparten experiencias y se discuten retos y soluciones."
    ),
    "academia": (
        "**Sin fuente documental todavía.** La carpeta '6. Estudios académicos' del "
        "Drive del proyecto está vacía (ver metodologia.qmd, P2). Este capítulo se "
        "generará cuando exista una fuente que extraer."
    ),
    "herramientas": (
        "**Pilar de nueva creación (decisión del propietario, P1), sin fuente "
        "documental todavía.** Cubrirá métricas de legibilidad, corpus de "
        "simplificación y herramientas públicas desplegadas para los idiomas del "
        "universo del Atlas."
    ),
    "ciudadania": (
        "**Pilar de nueva creación (decisión del propietario, P1), sin fuente "
        "documental todavía.** Cubrirá estudios de comprensión lectora, deberes de "
        "lectura fácil y accesibilidad cognitiva, e incidencia de sociedad civil."
    ),
}

_RECORD_SOURCES = {
    "leyes": ["leyes"],
    "instituciones": ["instituciones"],
    "proyectos": ["proyectos"],
    "formacion": ["cursos", "encuentros"],
}

_CHAPTER_ORDER = [
    "leyes",
    "instituciones",
    "proyectos",
    "publicaciones",
    "formacion",
    "academia",
    "herramientas",
    "ciudadania",
]

def _load(pillar: str) -> pd.DataFrame:
    path = DATA_PROCESSED / "records" / f"{pillar}.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def _records_for(pillar: str) -> pd.DataFrame:
    sources = _RECORD_SOURCES.get(pillar, [])
    frames = [_load(s) for s in sources]
    frames = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def _country_counts_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "Sin registros verificados todavía para este pilar.\n"
    counts = df["iso3"].value_counts()
    lines = ["| País | Nº de registros |", "|---|---|"]
    for iso3, n in counts.items():
        nombre = COUNTRY_UNIVERSE.get(iso3, iso3)
        lines.append(f"| {nombre} | {n} |")
    return "\n".join(lines) + "\n"


def _case_study(pillar: str, df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    field = next((f for f in ("titulo", "nombre") if f in df.columns), None)
    row = df.sort_values(["iso3", field]).iloc[0]
    nombre_pais = COUNTRY_UNIVERSE.get(row["iso3"], row["iso3"])
    titulo = row[field]
    return (
        f"\n## Caso: {titulo} ({nombre_pais})\n\n"
        f"> {row['cita']}\n\n"
        f"Fuente: `{row['fuente_file_id']}` (registro `{row.get('record_id', 'sin id')}`).\n"
    )


def render_chapter(pillar: str, number: int) -> str:
    label = PILLARS[pillar]["label"]
    df = _records_for(pillar)
    return (
        f"# {number:02d}. {label}\n\n"
        f"{_INTROS[pillar]}\n\n"
        f"## Registros por país\n\n"
        f"{_country_counts_table(df)}"
        f"{_case_study(pillar, df)}"
    )


def build_all() -> list[str]:
    CAPITULOS_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for i, pillar in enumerate(_CHAPTER_ORDER, start=1):
        content = render_chapter(pillar, i)
        path = CAPITULOS_DIR / f"{i:02d}-{pillar}.qmd"
        path.write_text(content, encoding="utf-8")
        written.append(str(path))
    return written


def main() -> None:
    written = build_all()
    print(f"Generados {len(written)} capítulos en {CAPITULOS_DIR}")


if __name__ == "__main__":
    main()
