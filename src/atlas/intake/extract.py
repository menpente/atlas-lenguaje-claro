"""Extrae registros candidatos de los textos cacheados en data/raw/.

No usa un modelo de lenguaje: los documentos fuente actuales (capítulos
del manuscrito panhispánico) siguen una plantilla de frase muy regular
por pilar, así que la extracción determinista por regex es más fiable
y más barata que una pasada LLM, y elimina el riesgo de invención propio
de una extracción generativa. Si en el futuro entran fuentes con prosa
libre (PDFs de leyes originales, por ejemplo), esas sí necesitarán una
pasada LLM con el texto adjunto — este módulo no lo hace todavía.

Todo registro producido aquí es un CANDIDATO (`verified` sin fijar) y
debe pasar por `review.py` antes de entrar en data/processed/records/.
"""

from __future__ import annotations

import csv
import io
import re
import unicodedata
from dataclasses import dataclass

import pandas as pd
from pydantic import ValidationError

from atlas.config import COUNTRY_UNIVERSE, DATA_INTERIM, DATA_RAW
from atlas.schemas import (
    CursoRecord,
    EncuentroRecord,
    InstitucionRecord,
    LeyRecord,
    ProyectoRecord,
    TipoLey,
)

MANIFEST_PATH = DATA_INTERIM / "drive_manifest.parquet"
RECORDS_DIR = DATA_INTERIM / "records"
MAX_CITA_WORDS = 25

# Alias de nombre de país -> iso3. Cualquier país no listado aquí (p.ej.
# Alemania, Luxemburgo, Unión Europea, "País no especificado") se
# considera fuera del universo del Atlas y se descarta, no se fuerza.
_ALIASES = {
    "mexico": "MEX",
    "eeuu": "USA",
    "ee.uu.": "USA",
    "estados unidos": "USA",
}


def _strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


_NAME_TO_ISO3 = {_strip_accents(name).lower(): iso3 for iso3, name in COUNTRY_UNIVERSE.items()}
_NAME_TO_ISO3.update(_ALIASES)


def normalize_country(raw_name: str) -> str | None:
    key = _strip_accents(raw_name).strip().lower().rstrip(".")
    return _NAME_TO_ISO3.get(key)


def _truncate_cita(text: str, max_words: int = MAX_CITA_WORDS) -> str:
    words = text.split()
    return " ".join(words[:max_words])


@dataclass
class DroppedRecord:
    pillar: str
    reason: str
    raw_snippet: str


def _read_raw(file_id: str) -> str:
    return (DATA_RAW / f"{file_id}.txt").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Leyes: se extraen de la hoja de cálculo (tiene URLs y citas reales), no del
# capítulo narrativo, que no cita fuentes verificables (ver metodologia.qmd).
# ---------------------------------------------------------------------------

_TIPO_MAP = {
    "ley ordinaria": TipoLey.ley,
    "ley general": TipoLey.ley,
    "ley orgánica": TipoLey.ley,
    "ley orgánica derecho de defensa": TipoLey.ley,
    "ley autonómica": TipoLey.ley,
    "ley federal": TipoLey.ley,
    "ley local": TipoLey.ley,
    "ley provincial": TipoLey.ley,
    "ley nacional": TipoLey.ley,
    "ley estatuaria": TipoLey.ley,
    "decreto": TipoLey.decreto,
    "real decreto": TipoLey.decreto,
    "decreto-ley": TipoLey.decreto,
    "decreto con fuerza de ley": TipoLey.decreto,
    "decreto ley": TipoLey.decreto,
    "resolución": TipoLey.resolucion,
    "orden presidencial": TipoLey.orden,
    "orden ministerial": TipoLey.orden,
    "circular": TipoLey.circular,
    "directiva": TipoLey.directiva,
    "convenio": TipoLey.convenio,
    "carta de derechos": TipoLey.carta_derechos,
    "proyecto de ley ordinaria": TipoLey.proyecto_ley,
    "iniciativa de proyecto de ley": TipoLey.proyecto_ley,
}

_NOT_YET_BINDING = {TipoLey.proyecto_ley}


def extract_leyes(file_id: str) -> tuple[list[LeyRecord], list[DroppedRecord]]:
    raw = _read_raw(file_id)
    lines = raw.splitlines()
    header_line = lines[0].split(" ", 1)[1] if lines[0].startswith("Hoja1 ") else lines[0]
    reader = csv.DictReader(io.StringIO("\n".join([header_line, *lines[1:]])))

    records: list[LeyRecord] = []
    dropped: list[DroppedRecord] = []
    for row in reader:
        pais = (row.get("país") or "").strip()
        iso3 = normalize_country(pais) if pais else None
        if iso3 is None:
            dropped.append(DroppedRecord("leyes", f"país fuera de universo: {pais!r}", str(row)))
            continue

        titulo = (row.get("nombre_ley") or "").strip()
        if not titulo:
            dropped.append(DroppedRecord("leyes", "sin nombre_ley", str(row)))
            continue

        tipo_raw = (row.get("tipo") or "").strip().lower()
        tipo = _TIPO_MAP.get(tipo_raw)
        if tipo is None:
            dropped.append(DroppedRecord("leyes", f"tipo no mapeado: {tipo_raw!r}", str(row)))
            continue

        fecha = (row.get("fecha") or "").strip()
        anio = int(fecha[:4]) if fecha[:4].isdigit() else None

        cita_source = row.get("Observaciones") or titulo
        try:
            record = LeyRecord(
                iso3=iso3,
                fuente_file_id=file_id,
                cita=_truncate_cita(cita_source),
                tipo=tipo,
                titulo=titulo,
                anio=anio,
                ambito=(row.get("área") or "sin clasificar").strip(),
                url_oficial=(row.get("URL") or None),
                vinculante=tipo not in _NOT_YET_BINDING,
            )
        except ValidationError as exc:
            dropped.append(DroppedRecord("leyes", str(exc), str(row)))
            continue
        records.append(record)
    return records, dropped


# ---------------------------------------------------------------------------
# Proyectos
# ---------------------------------------------------------------------------

_PROYECTO_RE = re.compile(
    r"El proyecto «(?P<titulo>.+?)» fue desarrollado en (?P<resto1>.*?)\. "
    r"Tuvo lugar en (?P<pais_resto>.*?)\. "
    r"(?:El área principal de aplicación fue (?P<area>.*?)\. )?"
    r"Este proyecto representa un avance concreto",
    re.DOTALL,
)


def extract_proyectos(file_id: str) -> tuple[list[ProyectoRecord], list[DroppedRecord]]:
    raw = _read_raw(file_id)
    records: list[ProyectoRecord] = []
    dropped: list[DroppedRecord] = []

    for match in _PROYECTO_RE.finditer(raw):
        resto1 = match.group("resto1").strip()
        if " por " in resto1:
            anio, entidad = resto1.split(" por ", 1)
        else:
            anio, entidad = resto1, "no especificada"
        anio = anio.strip() or None
        entidad = entidad.strip() or "no especificada"

        pais_resto = match.group("pais_resto").strip()
        if " en modalidad " in pais_resto:
            pais, modalidad = pais_resto.split(" en modalidad ", 1)
        else:
            pais, modalidad = pais_resto, None

        iso3 = normalize_country(pais)
        if iso3 is None:
            dropped.append(
                DroppedRecord(
                    "proyectos", f"país fuera de universo: {pais!r}", match.group(0)[:200]
                )
            )
            continue

        try:
            record = ProyectoRecord(
                iso3=iso3,
                fuente_file_id=file_id,
                cita=_truncate_cita(match.group(0)),
                nombre=match.group("titulo").strip(),
                anio=anio,
                entidad=entidad,
                area=(match.group("area") or "").strip() or None,
                modalidad=(modalidad or "").strip() or None,
            )
        except ValidationError as exc:
            dropped.append(DroppedRecord("proyectos", str(exc), match.group(0)[:200]))
            continue
        records.append(record)
    return records, dropped


# ---------------------------------------------------------------------------
# Cursos
# ---------------------------------------------------------------------------

_CURSO_RE = re.compile(
    r"(?P<pais>[^:\n]{2,60}): El curso «(?P<nombre>.+?)» fue organizado por (?P<entidad>.*?)\. "
    r"(?:Tuvo como responsable a .*?\. )?"
    r"(?:Entre los formadores destacó .*?\. )?"
    r"(?:Se impartió en (?P<fecha_modalidad>.*?)\. )?"
    r"(?:Su área de referencia fue .*?\. )?"
    r"(?:Se desarrolló en la región de .*?\. )?"
    r"Esta formación contribuyó a la difusión y profesionalización",
    re.DOTALL,
)


def extract_cursos(file_id: str) -> tuple[list[CursoRecord], list[DroppedRecord]]:
    raw = _read_raw(file_id)
    records: list[CursoRecord] = []
    dropped: list[DroppedRecord] = []

    for match in _CURSO_RE.finditer(raw):
        pais = match.group("pais").strip()
        iso3 = normalize_country(pais)
        if iso3 is None:
            dropped.append(
                DroppedRecord("cursos", f"país fuera de universo: {pais!r}", match.group(0)[:200])
            )
            continue

        try:
            record = CursoRecord(
                iso3=iso3,
                fuente_file_id=file_id,
                cita=_truncate_cita(match.group(0)),
                nombre=match.group("nombre").strip(),
                entidad=match.group("entidad").strip(),
            )
        except ValidationError as exc:
            dropped.append(DroppedRecord("cursos", str(exc), match.group(0)[:200]))
            continue
        records.append(record)
    return records, dropped


# ---------------------------------------------------------------------------
# Instituciones
# ---------------------------------------------------------------------------

_INSTITUCION_RE = re.compile(
    r"(?P<pais>[^:\n]{2,60}): La institución «(?P<nombre>.+?)» se encuentra en (?P<ciudad>.*?)\. "
    r"(?:Su teléfono de contacto es .*?\. )?"
    r"(?:Se puede contactar a través del correo .*?\.\.? )?"
    r"Forma parte del entramado institucional",
    re.DOTALL,
)

_TIPO_INSTITUCION_KEYWORDS = [
    ("ministerio", "ministerio"),
    ("universidad", "universidad"),
    ("facultad", "universidad"),
    ("gobierno", "gobierno"),
    ("poder judicial", "poder_judicial"),
    ("juzgado", "poder_judicial"),
    ("tribunal", "poder_judicial"),
    ("red ", "red"),
    ("asociación", "asociacion"),
    ("colegio", "asociacion"),
    ("comisión", "comision"),
    ("instituto", "instituto"),
    ("fundación", "fundacion"),
]


def _infer_tipo_institucion(nombre: str) -> str:
    lowered = _strip_accents(nombre).lower()
    for keyword, tipo in _TIPO_INSTITUCION_KEYWORDS:
        if _strip_accents(keyword) in lowered:
            return tipo
    return "otro"


def extract_instituciones(file_id: str) -> tuple[list[InstitucionRecord], list[DroppedRecord]]:
    raw = _read_raw(file_id)
    records: list[InstitucionRecord] = []
    dropped: list[DroppedRecord] = []

    for match in _INSTITUCION_RE.finditer(raw):
        pais = match.group("pais").strip()
        iso3 = normalize_country(pais)
        if iso3 is None:
            dropped.append(
                DroppedRecord(
                    "instituciones", f"país fuera de universo: {pais!r}", match.group(0)[:200]
                )
            )
            continue

        nombre = match.group("nombre").strip()
        try:
            record = InstitucionRecord(
                iso3=iso3,
                fuente_file_id=file_id,
                cita=_truncate_cita(match.group(0)),
                nombre=nombre,
                tipo=_infer_tipo_institucion(nombre),
            )
        except ValidationError as exc:
            dropped.append(DroppedRecord("instituciones", str(exc), match.group(0)[:200]))
            continue
        records.append(record)
    return records, dropped


# ---------------------------------------------------------------------------
# Encuentros
# ---------------------------------------------------------------------------

_ENCUENTRO_RE = re.compile(
    r"(?P<pais>[^:\n]{2,60}): La ponencia «(?P<titulo>.+?)» se presentó en (?P<evento_fecha>.*?)\. "
    r"Fue impartida por (?P<ponentes_entidad>.*?)\. "
    r"(?:Se desarrolló en modalidad (?P<modalidad>.*?)\. )?"
    r"(?:El área principal abordada fue .*?\. )?"
    r"Este encuentro contribuyó al avance de la reflexión colectiva",
    re.DOTALL,
)


def extract_encuentros(file_id: str) -> tuple[list[EncuentroRecord], list[DroppedRecord]]:
    raw = _read_raw(file_id)
    records: list[EncuentroRecord] = []
    dropped: list[DroppedRecord] = []

    for match in _ENCUENTRO_RE.finditer(raw):
        pais = match.group("pais").strip()
        iso3 = normalize_country(pais)
        if iso3 is None:
            dropped.append(
                DroppedRecord(
                    "encuentros", f"país fuera de universo: {pais!r}", match.group(0)[:200]
                )
            )
            continue

        ponentes_entidad = match.group("ponentes_entidad").strip()
        if ", en representación de " in ponentes_entidad:
            _, entidad = ponentes_entidad.rsplit(", en representación de ", 1)
        else:
            entidad = "no especificada"

        evento_fecha = match.group("evento_fecha").strip()
        anio_match = re.search(r"(\d{4})", evento_fecha)
        anio = anio_match.group(1) if anio_match else None

        try:
            record = EncuentroRecord(
                iso3=iso3,
                fuente_file_id=file_id,
                cita=_truncate_cita(match.group(0)),
                nombre=match.group("titulo").strip(),
                anio=anio,
                entidad=entidad.strip() or "no especificada",
                modalidad=(match.group("modalidad") or "").strip() or None,
            )
        except ValidationError as exc:
            dropped.append(DroppedRecord("encuentros", str(exc), match.group(0)[:200]))
            continue
        records.append(record)
    return records, dropped


# ---------------------------------------------------------------------------
# Orquestación
# ---------------------------------------------------------------------------

# file_id de cada fuente, resuelto contra el manifiesto de P2.
_SOURCE_FILE_IDS = {
    "leyes": "1_Rx7rBU85IK38HJJqXBV14xLfTwcA9kN",  # Leyes españolas.xlsx
    "proyectos": "1ssEsITh2TCm7qI7OLK79BNTeX26m39Y6",
    "cursos": "1VyM75p_CXQNX4vr2RI0lTHXOAdiaqgYb",
    "instituciones": "13FSED3pQflH87uQOCVKr1YYgIfoRBMGV",
    "encuentros": "1EJr162UfAYDGIhDcsg6EC-YNR3Yo2bCy",
}

_EXTRACTORS = {
    "leyes": extract_leyes,
    "proyectos": extract_proyectos,
    "cursos": extract_cursos,
    "instituciones": extract_instituciones,
    "encuentros": extract_encuentros,
}


def run_all() -> dict[str, int]:
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    all_dropped: list[DroppedRecord] = []
    counts: dict[str, int] = {}

    for pillar, extractor in _EXTRACTORS.items():
        file_id = _SOURCE_FILE_IDS[pillar]
        records, dropped = extractor(file_id)
        all_dropped.extend(dropped)
        counts[pillar] = len(records)

        rows = [r.model_dump(mode="json") for r in records]
        pd.DataFrame(rows).to_csv(RECORDS_DIR / f"{pillar}.csv", index=False)

    dropped_df = pd.DataFrame(
        [
            {"pillar": d.pillar, "reason": d.reason, "raw_snippet": d.raw_snippet}
            for d in all_dropped
        ]
    )
    dropped_df.to_csv(RECORDS_DIR / "_dropped.csv", index=False)
    counts["_dropped"] = len(all_dropped)
    return counts


def main() -> None:
    counts = run_all()
    for pillar, n in counts.items():
        print(f"{pillar}: {n}")


if __name__ == "__main__":
    main()
