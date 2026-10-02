# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Atlas Iberoamericano del Lenguaje Claro (Study A): a Python pipeline that turns Google Drive source documents into verified records, scores 23 countries × 8 pillars × 3 indicators into a plain-language index (PLDI), and generates a Quarto site. Prose, docs and data are in Spanish. `PLAN-atlas-plain-language-v2.md` is the phased plan (P0–P10); the status table at the end of `atlas/metodologia.qmd` is the authoritative record of what is done.

## Commands

Uses `uv` (Python ≥ 3.11). CI (`.github/workflows/ci.yml`) runs lint then tests.

```
make install                       # uv sync --extra dev
make lint                          # uv run ruff check src tests
make test                          # uv run pytest
uv run pytest tests/test_score.py::test_name   # single test
make records                       # extract.py then review.py
make index                         # score.py then semaforo.py
make generate                      # fichas, anexos, capitulos -> .qmd files
make site                          # generate + `quarto render` (Quarto CLI not installed in the original env; render never verified)
make intake                        # drive_sync.py; needs GOOGLE_APPLICATION_CREDENTIALS
```

Ruff: line length 100, rules E,F,I,UP,B. `src/atlas/build/fichas.py` is exempt from E501 (embedded Jinja template).

## Architecture

Data flows strictly through `data/` stages; each stage is a module run with `python -m atlas.<pkg>.<mod>`:

1. **intake** (`src/atlas/intake/`): `drive_sync` caches Drive text into `data/raw/<file_id>.txt` and writes `data/interim/drive_manifest.parquet`. `extract` parses raw text with deterministic regex parsers (no LLM) into candidate records `data/interim/records/<pillar>.csv`, each carrying `fuente_file_id` + verbatim `cita`; dropped rows go to `_dropped.csv` with a reason. `review` is an *automated* QA pass (not human review) that promotes candidates to `data/processed/records/`, adding a `confianza` column for heuristic-derived fields.
2. **build/score** (`build/score.py`): applies a fixed counting rule (0→0, 1→1, 2–3→2, 4–6→3, 7+→4) to processed records and writes `data/coding/pldi_coding.csv` (552 rows). Pillars with no source are `score=0, insufficient_evidence=True`, which is not the same as a documented "searched, found nothing" zero. `rubric.md` holds the 120 anchors, but the code does not read them per-anchor.
3. **index/viz**: `data/processed/pldi.parquet` (pillar = mean of 3 indicators, index = mean of pillars / 4 × 100, NaN when coverage is 0), `semaforo.html`, and the drop-one-pillar sensitivity CSV.
4. **site** (`build/fichas|anexos|capitulos`, then `atlas/` Quarto project): Jinja templates generate the `.qmd` pages under `atlas/paises/`, `atlas/anexos/`, `atlas/capitulos/` from the processed data.

Shared definitions live in `src/atlas/config.py` (`COUNTRY_UNIVERSE`, path constants derived from `REPO_ROOT`) and `src/atlas/schemas.py` (pydantic models per pillar, ISO3 validation, `PldiCoding`). Puerto Rico (PRI) is a non-sovereign special case excluded from the numeric index (`country_universe.csv`).

## Things that are easy to get wrong

- **Honesty constraints are deliberate.** P6 inter-coder reliability is NOT done (see `data/coding/adjudication.md`); no fake second coder or Krippendorff's α, no Zenodo DOI, and P4 is automated QA rather than human verification. Do not paper over these in docs or code.
- **Index results to preserve in docs:** Brazil and Haiti have 0% coverage despite being in the universe.
- **`data/raw/` IS committed** (so extraction tests work in CI), except the contacts spreadsheet `data/raw/1nRWn8rBwBtyiOSdMZwssUZ_Fgm2Th6I_.txt`, which holds personal phone numbers/emails and is gitignored.
- The committed raw cache and manifest came from an interactive Drive-connector capture, not a credentialed `drive_sync.py` run, so idempotence of intake is unverified.
- Everything in `data/processed/` and the generated `.qmd` pages is derived; regenerate via make targets rather than hand-editing.
- Licenses: MIT for code (`LICENSE-CODE`), CC-BY 4.0 for text/data (`LICENSE-DATA`). Study B (PLDI vs. development indicators) lives in a separate repo.
