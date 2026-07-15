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

- **P0 Scaffold:** hecho.
- **P1 Decisiones + rubric:** hecho — `rubric.md` (120 anclas) y
  `country_universe.csv`.
- **P2 Drive intake:** parcial. `data/interim/drive_manifest.parquet` y
  `data/raw/*.txt` están poblados (12 archivos) a partir de una captura
  interactiva con el conector de Drive de la sesión, no de un rerun del
  `drive_sync.py` credencializado (que existe pero no se ha podido
  ejecutar sin una service account). Ver `atlas/metodologia.qmd` para el
  detalle — el criterio de aceptación formal de P2 (idempotencia
  verificada) sigue pendiente.
- **P3 Extracción:** hecho para los 5 pilares con fuente disponible
  (Leyes, Proyectos, Cursos, Instituciones, Encuentros) vía parsers
  deterministas por regex (`src/atlas/intake/extract.py`), no LLM — ver
  `atlas/metodologia.qmd`. 1024 registros candidatos en
  `data/interim/records/`, todos con `fuente_file_id` + `cita` verbatim.
- **P4 Revisión:** control de calidad **automatizado**, no revisión
  humana (no hay una persona disponible en este entorno) —
  `src/atlas/intake/review.py`. 1023/1024 candidatos promovidos a
  `data/processed/records/` con una columna `confianza` marcando los
  campos derivados por heurística.
- **P5 Codificación:** `src/atlas/build/score.py` codifica 552 filas
  (23 países × 8 pilares × 3 indicadores) con una regla de conteo
  determinista y documentada, no una lectura fina de cada ancla.
- **P6 Fiabilidad:** **NO completado.** Requiere un segundo codificador
  independiente; no se ha fabricado uno ni un Krippendorff's α falso —
  ver `data/coding/adjudication.md`.
- **P7 Semáforo + índice:** hecho — `data/processed/pldi.parquet`,
  `semaforo.html`, sensibilidad drop-one-pillar. Hallazgo importante:
  Brasil y Haití tienen 0% de cobertura pese a estar en el universo.
- **P8 Atlas:** sitio Quarto generado (`atlas/_quarto.yml`, 8 capítulos,
  23 fichas, 4 anexos), pero **el render no se ha podido verificar**
  (Quarto CLI no instalado en este entorno). Sin mapas geoespaciales
  (fuera de alcance de esta sesión).
- **P9 Study B / P10 Release:** ver `atlas/metodologia.qmd` — ambos
  gateados por el P6 pendiente; no ejecutados. `LICENSE-CODE`/
  `LICENSE-DATA` ya cubren la parte de licencia de P10.
