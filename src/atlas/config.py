"""Universo de paises, registro de pilares y rutas del proyecto.

Decisiones del propietario (2026-07-13), ver metodologia.qmd:
- Universo: union de las dos listas encontradas en Drive (22 paises del
  indice + Puerto Rico), marco Iberoamericano (Brasil como miembro pleno).
- Pilares 7-8 (Herramientas, Ciudadania) aceptados como nueva contribucion.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_INTERIM = REPO_ROOT / "data" / "interim"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
DATA_CODING = REPO_ROOT / "data" / "coding"

DRIVE_ATLAS_FOLDER_ID = "1rRJA1bVXezmB4i_uzVy0bp2eFHJL31t8"

# iso3 -> nombre en espanol. Puerto Rico usa el codigo ISO 3166-1 PRI
# (entidad no soberana, territorio de EEUU) y se trata como caso especial
# en el semaforo/indice, no como pais con instituciones nacionales propias.
COUNTRY_UNIVERSE: dict[str, str] = {
    "ARG": "Argentina",
    "BOL": "Bolivia",
    "BRA": "Brasil",
    "CHL": "Chile",
    "COL": "Colombia",
    "CRI": "Costa Rica",
    "CUB": "Cuba",
    "ECU": "Ecuador",
    "SLV": "El Salvador",
    "ESP": "España",
    "USA": "Estados Unidos",
    "GTM": "Guatemala",
    "HTI": "Haití",
    "HND": "Honduras",
    "MEX": "México",
    "NIC": "Nicaragua",
    "PAN": "Panamá",
    "PRY": "Paraguay",
    "PER": "Perú",
    "PRI": "Puerto Rico",
    "DOM": "República Dominicana",
    "URY": "Uruguay",
    "VEN": "Venezuela",
}

# Entidades no soberanas: se excluyen de comparaciones de "leyes nacionales"
# vinculantes pero se incluyen en fichas, mapas y anexos.
NON_SOVEREIGN = {"PRI"}

# Pilar -> (carpeta Drive relacionada o None, indicadores a/b/c)
PILLARS: dict[str, dict] = {
    "leyes": {
        "label": "Leyes",
        "drive_folder": "4. Leyes",
        "indicators": {
            "a": "Estatuto vinculante de lenguaje claro",
            "b": (
                "Deber incorporado en ley sectorial (justicia, consumo, salud, "
                "procedimiento administrativo)"
            ),
            "c": "Normas privadas/sectoriales + mecanismo de cumplimiento",
        },
    },
    "instituciones": {
        "label": "Instituciones",
        "drive_folder": "5. Instituciones",
        "indicators": {
            "a": "Unidad/oficina publica dedicada",
            "b": "Red o comision nacional",
            "c": "Penetracion en poder judicial / redaccion legislativa",
        },
    },
    "proyectos": {
        "label": "Proyectos",
        "drive_folder": "1. Proyectos",
        "indicators": {
            "a": "Programa o plan de gobierno",
            "b": "Proyectos sectoriales sostenidos",
            "c": "Evidencia de evaluacion/monitoreo",
        },
    },
    "publicaciones": {
        "label": "Publicaciones",
        "drive_folder": None,
        "indicators": {
            "a": "Guia(s) de estilo nacional(es) oficial(es)",
            "b": "Adopcion de ISO 24495-1:2023 o norma equivalente",
            "c": "Requisito de testeo con usuarios",
        },
    },
    "formacion": {
        "label": "Formación",
        "drive_folder": "3. Cursos + 2. Encuentros",
        "indicators": {
            "a": "Cursos / certificacion",
            "b": "Congresos o encuentros recurrentes",
            "c": "Asociacion profesional",
        },
    },
    "academia": {
        "label": "Academia",
        "drive_folder": "6. Estudios académicos",
        "indicators": {
            "a": "Grupos de investigacion / catedras",
            "b": "Publicaciones y tesis",
            "c": "Redes academicas",
        },
    },
    "herramientas": {
        "label": "Herramientas",
        "drive_folder": None,
        "indicators": {
            "a": "Metricas de legibilidad validadas para el idioma nacional",
            "b": "Corpus/datasets de simplificacion",
            "c": "Herramienta publica desplegada (incl. basada en LLM)",
        },
    },
    "ciudadania": {
        "label": "Ciudadanía",
        "drive_folder": None,
        "indicators": {
            "a": "Resultados de comprension medidos",
            "b": "Deberes de lectura facil / accesibilidad cognitiva",
            "c": "Incidencia de sociedad civil",
        },
    },
}

SCALE_ANCHORS = {
    0: "sin evidencia tras busqueda documentada",
    1: "aislado / simbolico / puntual",
    2: "existe pero no vinculante, parcial o subnacional",
    3: "nacional, institucionalizado, vinculante o casi",
    4: "nacional, vinculante, dotado de recursos y evaluado",
}
