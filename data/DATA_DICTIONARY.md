# Diccionario de datos

Todo número o afirmación del Atlas debe ser trazable a un archivo de esta carpeta. Este documento describe qué contiene cada uno.

## `raw/` (inmutable, versionado salvo un archivo)

Caché de texto extraído de Drive, un `.txt` por `file_id`. Se versiona para que `extract.py` y sus tests sean reproducibles en un checkout limpio (CI incluido). Se excluye únicamente la hoja de contactos (`1nRWn8rBwBtyiOSdMZwssUZ_Fgm2Th6I_.txt`) porque contiene datos de contacto de personas físicas (ver `atlas/metodologia.qmd`, nota de privacidad). Regenerar con `make intake` (requiere `GOOGLE_APPLICATION_CREDENTIALS`) o ver `src/atlas/intake/build_manifest_snapshot.py` para la captura de referencia del 2026-07-13.

## `interim/`

- **`drive_manifest.parquet`**: `file_id, name, mime, folder, modified_at, web_link, snapshot_captured_at` — un archivo de Drive por fila.
- **`records/{pillar}.csv`**: registros **candidatos** de P3, sin verificar (`verified` sin fijar). Columnas comunes: `iso3, fuente_file_id, cita, verified` + campos específicos del pilar (ver `src/atlas/schemas.py`).
- **`records/_dropped.csv`**: `pillar, reason, raw_snippet` — filas descartadas en la extracción (país fuera de universo, tipo no mapeado, etc.), con motivo.

## `processed/`

- **`records/{pillar}.csv`**: registros que pasaron el control de calidad de P4 (`record_id, ..., confianza, verified="ok"`). `confianza="baja"` marca campos derivados por heurística (ver `atlas/metodologia.qmd`, P4). **Esto no es una revisión humana** — ver la misma nota.
- **`records/_qa_dropped.csv`**: `pillar, reason, nombre_o_titulo, iso3` — filas descartadas en el control de calidad (duplicados, campos vacíos).
- **`pldi.parquet`**: `iso3, nombre, {pilar}..., indice, cobertura` — una fila por país. `{pilar}` es la media de sus 3 indicadores (NaN si ninguno tiene evidencia). `indice` = media de pilares / 4 × 100 (NaN si cobertura = 0). `cobertura` = fracción de los 24 indicadores con evidencia real (no `insufficient_evidence`).
- **`semaforo.html`**: tabla país × pilar coloreada (verde/ámbar/rojo/sin-datos), generada por `src/atlas/viz/semaforo.py`.
- **`sensitivity_drop_one_pillar.csv`**: `pilar_omitido, spearman_rho, n_paises_comparados` — sensibilidad del ranking del índice a omitir cada pilar.

## `coding/`

- **`country_universe.csv`**: `iso3, nombre, soberania, incluir_en_indice_numerico, notas` — las 23 entidades del universo y por qué Puerto Rico está excluido del índice numérico.
- **`rubric.md`**: ancla observable por indicador × nivel (0-4), para los 8 pilares.
- **`pldi_coding.csv`**: `iso3, pillar, indicator, score, evidence_record_ids, evidence_note, coder, coded_at, confidence, insufficient_evidence` — 552 filas (23 × 8 × 3). `evidence_record_ids` apunta a `record_id` de `processed/records/`. `coder` identifica explícitamente si quien codificó fue un modelo o una persona.
- **`adjudication.md`**: por qué la fiabilidad (P6) no se ha verificado — no es un formato de datos, es la explicación de una fase pendiente.

## Esquemas completos

Ver `src/atlas/schemas.py` (pydantic) para la definición exacta de cada tipo de registro y sus validaciones (país en universo, cita ≤25 palabras, score con evidencia o `insufficient_evidence`).
