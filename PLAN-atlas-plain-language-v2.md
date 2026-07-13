# Atlas del Lenguaje Claro — Execution Plan (v2)

**Owner:** Rubén de la Fuente (DelaFuente.AI)
**Supersedes:** `PLAN-atlas-plain-language.md` (v1, global/OECD framing — now split out as Study B)
**Purpose:** hand to Claude Code as the project spec. Work phase by phase. Stop at each acceptance gate.

---

## 0. Reality check

An Atlas project **already exists**: a Drive folder with an *Índice del Atlas* document and seven thematic subfolders. This plan is written **against that index**, not against a greenfield design.

Two consequences:

1. **The Atlas is Ibero-American and editorial**, not global and statistical. Universe ≈ 22 countries; deliverable is a book-shaped atlas with thematic maps, case studies and one-page country fact sheets.
2. **The correlation-with-development-indicators idea does not survive N=22 in a single region.** It is therefore **split out as Study B**, a separate global analysis with its own universe. Do not contaminate the Atlas with fragile models.

---

## 1. Two deliverables, deliberately separated

| | **Study A — El Atlas** | **Study B — Correlation study** |
|---|---|---|
| Universe | 22 Ibero-American countries + EEUU (per the existing índice) | Global, ~60 countries (v1 universe: OECD + PLAIN/Clarity + Ibero-America + any country with a statute) |
| Output | Editorial atlas: thematic maps, case studies, country fact sheets, **semáforo de implantación** | Paper/notebook: PLDI vs development indicators, residuals, typology |
| Stats | Descriptive only. No models. | Spearman + FDR, OLS with region FE, cluster typology |
| Audience | Ibero-American plain-language community | Research / policy |
| Repo | `atlas-lenguaje-claro/` | `pldi-correlates/` (separate repo, imports the coding schema) |

The **semáforo** is the bridge: the same rubric feeds both. Code the 22 first (they're the ones with collaborators and sources); extend the coding to the wider universe only in Study B.

---

## 2. Open decisions — RESOLVED by owner on 2026-07-13

1. **Country list.** Two conflicting lists existed in Drive itself: the *Índice del Atlas* Google Doc (21 named + EEUU, includes Haití, no Puerto Rico) vs. *Índice Atlas.xlsx* (includes Puerto Rico + Estados Unidos, no Haití). **Decision: union of both — 23 entities**, with Puerto Rico treated as a non-sovereign special case. See `src/atlas/config.py::COUNTRY_UNIVERSE`.
2. **Brasil and Haití.** **Decision: Ibero-American frame, Brasil as full member.** Chapter texts should say "Iberoamericano", not "hispanohablante".
3. **Two proposed new chapters** (Herramientas, Ciudadanía). **Decision: accepted as pillars 7-8.**
4. **Licence.** **Decision: CC-BY 4.0 for text/data (`LICENSE-DATA`), MIT for code (`LICENSE-CODE`).**

Additional finding from the Drive audit (not anticipated by v1 of this plan): the folders are **not empty**. Chapter drafts already exist for Leyes and Instituciones, plus a near-complete manuscript (`TT Atlas_Panhispanico_Lenguaje_Claro_COMPLETO_Saltos.docx`) with real project records, and a contacts database. P2/P3 should mine these drafts as primary sources, not assume a blank intake. A `7. Conclusiones` folder exists but is empty; there is no dedicated `Publicaciones` folder.

---

## 3. Pillars — aligned to the existing índice

The chapters *are* the pillars. Do not invent a parallel taxonomy.

| Pillar | Drive folder | Indicators (each 0–4) |
|---|---|---|
| **1. Leyes** | `4. Leyes` | (a) binding plain-language statute; (b) duty embedded in sectoral law (justicia, consumo, salud, procedimiento administrativo); (c) private/sectoral norms + any enforcement mechanism |
| **2. Instituciones** | `5. Instituciones` | (a) dedicated public unit/office; (b) national network or comisión; (c) penetración into judiciary / legislative drafting |
| **3. Proyectos** | `1. Proyectos` | (a) government-wide programme or plan; (b) sustained sectoral projects; (c) evidence of evaluation/monitoring |
| **4. Publicaciones** | (guías y manuales) | (a) official national style guide(s); (b) ISO 24495-1:2023 adoption or equivalent norm; (c) testing-with-users requirement |
| **5. Formación** | `3. Cursos` + `2. Encuentros` | (a) courses / certification; (b) recurring congresses or encuentros; (c) professional association |
| **6. Academia** | `6. Estudios académicos` | (a) research groups / chairs; (b) publications & theses; (c) academic networks |
| **7. Herramientas** *(accepted)* | — | (a) readability metrics validated for the national language(s); (b) corpora/datasets; (c) deployed public tooling |
| **8. Ciudadanía** *(accepted)* | — | (a) measured comprehension outcomes; (b) lectura fácil / cognitive accessibility duties; (c) civil-society advocacy |

Scale anchors (identical across all indicators — write them out per-indicator in `rubric.md`):

```
0 = sin evidencia tras búsqueda documentada
1 = aislado / simbólico / puntual
2 = existe pero no vinculante, parcial o subnacional
3 = nacional, institucionalizado, vinculante o casi
4 = nacional, vinculante, dotado de recursos y evaluado
```

**Semáforo** = pillar-level colour (rojo 0–1 / ámbar 2 / verde 3–4). **Índice** = mean of pillars, 0–100. With N=23, the semáforo is the headline; the numeric index is a supporting view, not a league table.

---

## 4. The collection pipeline

The Drive subfolders are the intake, and — per the audit above — already contain drafted chapter text and a near-complete manuscript to mine, not just raw sources.

**`src/atlas/intake/drive_sync.py`**
- Authenticate to Drive; walk folder `1rRJA1bVXezmB4i_uzVy0bp2eFHJL31t8` recursively.
- For every file: record `file_id, name, mime, folder (→ pillar), modified_at, web_link` into `data/interim/drive_manifest.parquet`.
- Download/export text: Google Docs → text; PDFs → `pdfplumber` (fallback OCR); DOCX → `python-docx`. Cache by `file_id` + `modified_at` so re-runs are cheap.
- **Idempotent.** Re-running must not duplicate rows.

**`src/atlas/intake/extract.py`**
- For each document, extract candidate **records** into a typed table, one row per *thing*, not per file:
  - `leyes.csv`: `iso3, tipo{ley|decreto|reglamento|norma_privada}, titulo, año, ambito, url_oficial, vinculante{sí|no}, fuente_file_id`
  - `instituciones.csv`: `iso3, nombre, tipo, año_creación, url, fuente_file_id`
  - `proyectos.csv`, `encuentros.csv`, `cursos.csv`, `estudios.csv`, `publicaciones.csv` — same pattern.
- Use an LLM extraction pass **with the source text attached**, emitting strict JSON validated against a `pydantic` schema. **Every record must carry `fuente_file_id` + a verbatim `cita` (≤25 words) locating the claim in the source.** Records without provenance are dropped, not guessed.
- Output `data/interim/records/*.csv` for **human review**. These are *candidates*, not truth.

**`src/atlas/intake/review.py`**
- Emit a review sheet per pillar (CSV or a small Streamlit app) where a human sets `verified ∈ {ok, fix, drop}` and edits fields.
- Only `verified == ok` rows flow into `data/processed/records/`.

**Acceptance (P2):** re-running `make intake` on an unchanged Drive produces a byte-identical manifest and zero new candidate records.

---

## 5. Scoring (`data/coding/`)

- `rubric.md` — observable anchors for every indicator × level. Written **before** any scoring.
- `pldi_coding.csv` — `iso3, pillar, indicator, score, evidence_record_ids, evidence_note, coder, coded_at, confidence`.
- Scores must be **justified by verified records** from §4 (`evidence_record_ids` points into `data/processed/records/`). A score with no records must be 0, or explicitly marked `insufficient_evidence` and excluded.
- **Reliability:** double-code a random 20% (Rubén + a second coder; an LLM coder under the identical rubric with sources attached is acceptable if documented). Compute **Krippendorff's α (ordinal)**. Target ≥ 0.67. Below that: revise rubric, recode. Do not proceed.
- Adjudication log in `data/coding/adjudication.md`.

---

## 6. Atlas outputs

**Per chapter (7–8 chapters):**
- Thematic map of the Ibero-American region (choropleth or dot map of records — e.g. all *leyes*, all *encuentros*).
- Short, direct prose in the Cervantes register: concise, factual, image-led.
- **One case study per chapter** (per the índice).
- Table of records for that pillar, with links.

**Per country (23 fact sheets, 1 page):**
- Generated from a Jinja template by `src/atlas/build/fichas.py` — **never hand-edited**.
- Basic data: population, official + co-official languages, language contact situation, Spanish variant notes (the índice explicitly wants variants and lenguas cooficiales/en contacto).
- Semáforo across the pillars (radar or 8-cell colour strip).
- Key instruments: laws, institutions, guides — with links.
- 150–250 words of narrative.

**Cross-cutting:**
- The **mapa de calor / semáforo de implantación** — the flagship figure.
- **Anexos** (already in the índice): bibliografía, listado de leyes, listado de instituciones, quién es quién. These are **generated from `data/processed/records/`**, not maintained by hand. That's the single biggest labour saving in the project.

**Format:** Quarto site + PDF book. **Write in Spanish.** Structure for a later `en/` mirror; don't retrofit.

Colour: colour-blind-safe semáforo (do not use raw red/green — use a ColorBrewer diverging ramp that survives deuteranopia). "Sin datos" must be visually distinct from "cero".

---

## 7. Study B — the correlation study (separate repo)

Only start after the Atlas coding is stable.

- Extend the rubric coding to the **~60-country global universe** (v1 universe rule).
- Correlates, joined by ISO3: HDI; log GDP per capita PPP (World Bank `NY.GDP.PCAP.PP.KD`); WGI Government Effectiveness; **OECD PIAAC** adult literacy proficiency (limited coverage — expect ~30 countries); UN DESA EGDI + Online Services Index; WJP Rule of Law (open-government factor, check licence); OGP membership + years; RTI Rating; CPI; education spending % GDP.
- **Spearman** ρ with bootstrap 95% CIs (10k), **Benjamini–Hochberg FDR** correction. Report ρ, CI, N, q.
- OLS `PLDI ~ log(GDPpc) + region FE`, robust SEs. Expect region FE to absorb much of the variance — say so.
- **Residuals are the finding:** countries with far more plain-language infrastructure than income predicts. Publish `residuals.csv` and a chapter on it.
- Typology: clustering on pillar scores, k by silhouette; name the clusters ("statute-led", "profession-led", "administration-led", "nascent").
- **No causal language anywhere.** Add `tests/test_no_causal_claims.py` that greps `.qmd`/`.md` for a banned list (`causa`, `provoca`, `impulsa`, `impacto de X en Y`, `leads to`, `drives`) and fails the build.

---

## 8. Repository layout

```
atlas-lenguaje-claro/
├── README.md
├── pyproject.toml            # uv; ruff; pytest
├── Makefile                  # make intake | make records | make index | make site
├── data/
│   ├── raw/                  # immutable Drive exports, cached by file_id
│   ├── interim/
│   │   ├── drive_manifest.parquet
│   │   └── records/          # LLM-extracted CANDIDATES (unverified)
│   ├── processed/
│   │   ├── records/          # human-verified records — the asset
│   │   └── pldi.parquet
│   └── coding/
│       ├── rubric.md
│       ├── country_universe.csv
│       ├── pldi_coding.csv
│       └── adjudication.md
├── src/atlas/
│   ├── config.py             # universe, pillar registry, Drive folder id, paths
│   ├── intake/                # drive_sync.py, extract.py, review.py
│   ├── build/                 # index.py, fichas.py, anexos.py
│   ├── viz/                   # semaforo.py, mapas.py
│   └── schemas.py             # pydantic + pandera
├── tests/
└── atlas/                    # Quarto (es/)
    ├── _quarto.yml
    ├── index.qmd
    ├── metodologia.qmd       # write EARLY, not last
    ├── capitulos/01-leyes.qmd … 08-ciudadania.qmd
    ├── paises/{iso3}.qmd     # generated
    └── anexos/               # generated
```

---

## 9. Phases

| Phase | Deliverable | Definition of done |
|---|---|---|
| **P0** Scaffold | repo, uv env, Makefile, CI (ruff+pytest), schemas | `make test` passes on empty project |
| **P1** Decisions + rubric | §2 answered by owner; `country_universe.csv`; `rubric.md` | Observable anchor for every indicator × 5 levels |
| **P2** Drive intake | `drive_sync.py`, manifest, cached exports | Idempotent: unchanged Drive → identical manifest |
| **P3** Extraction | candidate records per pillar | Every record has `fuente_file_id` + verbatim `cita`; schema-valid; zero records without provenance |
| **P4** Human review | `data/processed/records/` | 100% of candidates triaged ok/fix/drop |
| **P5** Coding | `pldi_coding.csv` | Every score links to verified record ids, or is 0 / `insufficient_evidence` |
| **P6** Reliability | 20% double-coded, α | α ≥ 0.67 ordinal, or rubric revised + recoded |
| **P7** Semáforo + índice | `pldi.parquet`, semáforo figure | Sensitivity: drop-one-pillar rank correlation reported |
| **P8** Atlas | Quarto site + PDF, 22 fichas, anexos generated | Builds from clean clone with only `data/coding/*` + Drive as input |
| **P9** Study B | separate repo, correlations + residuals + typology | FDR-corrected, bootstrap CIs, causal-language test passes |
| **P10** Release | Zenodo DOI, licence, `CITATION.cff`, data dictionary | Every number in the atlas traceable to a source file |

---

## 10. Instructions to Claude Code

- Work **one phase at a time**. At the end of each, report: what was built, which acceptance criteria are met, and every judgement call made.
- **Never fabricate a law, an institution, a URL, a date or a score.** If not found, write `not_found` and log the search terms tried. One invented *Boletín Oficial* citation would discredit the whole atlas — and this project's entire premise is that public institutions should be trustworthy and legible.
- LLM extraction is a **candidate generator**, never an authority. Nothing enters `data/processed/` without human verification.
- `data/raw/` is immutable. All transformation happens in code.
- Prefer boring, inspectable code: pure functions, tidy frames, parquet, no clever abstractions.
- Log every methodological decision into `metodologia.qmd` **as you make it**.
- Do not resolve §2 yourself. Ask.
