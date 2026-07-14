"""Esquemas pydantic para el manifiesto de Drive, los registros candidatos
extraidos por LLM y la codificacion PLDI.

Regla de oro (ver plan, seccion 10): un registro sin `fuente_file_id` y
`cita` verbatim no es un registro valido. Nunca se inventa una fecha, una
URL o una cita.
"""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from atlas.config import COUNTRY_UNIVERSE, PILLARS


def _validate_iso3(v: str) -> str:
    if v not in COUNTRY_UNIVERSE:
        raise ValueError(f"iso3 '{v}' no esta en COUNTRY_UNIVERSE")
    return v


class DriveManifestEntry(BaseModel):
    file_id: str
    name: str
    mime: str
    folder: str
    modified_at: datetime
    web_link: str


class RecordBase(BaseModel):
    """Campos de procedencia obligatorios para cualquier registro candidato."""

    iso3: str
    fuente_file_id: str
    cita: str = Field(..., description="Cita verbatim (<=25 palabras) que localiza la afirmacion")
    verified: Literal["ok", "fix", "drop"] | None = None

    @field_validator("iso3")
    @classmethod
    def check_iso3(cls, v: str) -> str:
        return _validate_iso3(v)

    @field_validator("cita")
    @classmethod
    def check_cita_length(cls, v: str) -> str:
        if len(v.split()) > 25:
            raise ValueError("cita debe tener 25 palabras o menos")
        return v


class TipoLey(StrEnum):
    """Ampliado en P3: el 4-valor original no cubría las categorías reales
    encontradas en las fuentes (resoluciones, órdenes, circulares, directivas
    de la UE, convenios, cartas de derechos, proyectos de ley aún no vigentes).
    """

    ley = "ley"
    decreto = "decreto"
    reglamento = "reglamento"
    resolucion = "resolucion"
    orden = "orden"
    circular = "circular"
    directiva = "directiva"
    convenio = "convenio"
    carta_derechos = "carta_derechos"
    proyecto_ley = "proyecto_ley"
    norma_privada = "norma_privada"


class LeyRecord(RecordBase):
    tipo: TipoLey
    titulo: str
    anio: int | None = None
    ambito: str
    url_oficial: str | None = None
    vinculante: bool


class InstitucionRecord(RecordBase):
    nombre: str
    tipo: str
    anio_creacion: int | None = None
    url: str | None = None


class ProyectoRecord(RecordBase):
    nombre: str
    anio: str | None = None
    entidad: str
    area: str | None = None
    modalidad: str | None = None


class EncuentroRecord(RecordBase):
    nombre: str
    anio: str | None = None
    entidad: str
    modalidad: str | None = None


class CursoRecord(RecordBase):
    nombre: str
    entidad: str
    nivel: str | None = None
    url: str | None = None


class EstudioRecord(RecordBase):
    tipo: Literal["grupo_investigacion", "publicacion", "tesis", "congreso", "red"]
    titulo: str
    entidad: str | None = None
    anio: int | None = None
    url: str | None = None


class PublicacionRecord(RecordBase):
    titulo: str
    entidad: str
    tipo: Literal["guia_estilo", "norma_iso", "manual"] = "guia_estilo"
    url: str | None = None


class HerramientaRecord(RecordBase):
    nombre: str
    tipo: Literal["metrica_legibilidad", "corpus", "herramienta_publica"]
    entidad: str | None = None
    url: str | None = None


class CiudadaniaRecord(RecordBase):
    tipo: Literal["estudio_comprension", "deber_lectura_facil", "incidencia_sociedad_civil"]
    titulo: str
    entidad: str | None = None
    url: str | None = None


class PldiCoding(BaseModel):
    iso3: str
    pillar: str
    indicator: Literal["a", "b", "c"]
    score: int = Field(ge=0, le=4)
    evidence_record_ids: list[str] = Field(default_factory=list)
    evidence_note: str | None = None
    coder: str
    coded_at: datetime
    confidence: Literal["alta", "media", "baja"] | None = None
    insufficient_evidence: bool = False

    @field_validator("iso3")
    @classmethod
    def check_iso3(cls, v: str) -> str:
        return _validate_iso3(v)

    @field_validator("pillar")
    @classmethod
    def check_pillar(cls, v: str) -> str:
        if v not in PILLARS:
            raise ValueError(f"pillar '{v}' no esta en PILLARS")
        return v

    @model_validator(mode="after")
    def check_score_has_evidence(self) -> "PldiCoding":
        # Seccion 5 del plan: una puntuacion > 0 debe estar respaldada por
        # registros verificados, o quedar marcada insufficient_evidence.
        if self.score > 0 and not self.evidence_record_ids and not self.insufficient_evidence:
            raise ValueError(
                "score > 0 requiere evidence_record_ids, o marcar insufficient_evidence=True"
            )
        return self
