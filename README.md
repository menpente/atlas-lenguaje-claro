# Atlas Iberoamericano del Lenguaje Claro

Pipeline de intake, codificacion y build editorial para el Atlas del
Lenguaje Claro (Estudio A). El Estudio B (correlacion global PLDI vs.
indicadores de desarrollo) vive en un repositorio aparte.

Ver `PLAN-atlas-plain-language-v2.md` (en esta carpeta) para el plan de
ejecucion completo por fases (P0-P10).

## Universo y decisiones del propietario (2026-07-13)

- **Universo:** 23 entidades — union de las dos listas encontradas en
  Drive (indice + Puerto Rico como caso especial no soberano). Ver
  `src/atlas/config.py::COUNTRY_UNIVERSE`.
- **Marco:** Iberoamericano (Brasil como miembro pleno del indice, no solo
  hispanohablante).
- **Pilares:** 8 — los 6 ya redactados en el manuscrito existente
  (Proyectos, Encuentros, Cursos, Leyes, Instituciones, Estudios
  academicos) mas dos nuevos aceptados como contribucion original del
  proyecto: Herramientas y Ciudadania.
- **Licencia:** CC-BY 4.0 para texto/datos (`LICENSE-DATA`), MIT para
  codigo (`LICENSE-CODE`).

## Estructura

```
data/
  raw/          # exports inmutables de Drive, cacheados por file_id
  interim/      # manifiesto + registros candidatos (sin verificar)
  processed/    # registros verificados por humanos — el activo real
  coding/       # rubric.md, country_universe.csv, pldi_coding.csv
src/atlas/      # config, esquemas pydantic, intake/build/viz
tests/
atlas/          # sitio Quarto (es/)
```

## Desarrollo

```
make install   # uv sync
make test      # ruff + pytest
```

## Estado

- **P0 Scaffold:** hecho — repo, uv, Makefile, CI, esquemas.
- **P1 Decisiones + rubric:** decisiones resueltas (arriba); `rubric.md`
  y `country_universe.csv` pendientes.
- P2 en adelante: ver plan.
