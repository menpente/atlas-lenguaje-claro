"""Construye data/interim/drive_manifest.parquet a partir de un snapshot fijo.

Este snapshot se capturo a mano el 2026-07-13 usando el conector de Drive
interactivo de la sesion (no credenciales de service account), enumerando
la carpeta `1rRJA1bVXezmB4i_uzVy0bp2eFHJL31t8` y sus 7 subcarpetas. No es
idempotente frente a Drive real: es una foto fija, no un rerun. Cuando
existan credenciales de service account, `drive_sync.py` debe sustituir
este script generando el mismo esquema de salida.
"""

import pandas as pd

from atlas.config import DATA_INTERIM

SNAPSHOT_CAPTURED_AT = "2026-07-13T22:15:00Z"

# file_id, name, mime, folder, modified_at, web_link
_ENTRIES = [
    (
        "1vlsdKknauVH9KegOnu9bvm7V5vw7HmxIFCjSAYwTQog",
        "Índice del Atlas",
        "application/vnd.google-apps.document",
        "_root",
        "2025-11-18T19:39:39.700Z",
        "https://docs.google.com/document/d/1vlsdKknauVH9KegOnu9bvm7V5vw7HmxIFCjSAYwTQog/edit",
    ),
    (
        "1nRWn8rBwBtyiOSdMZwssUZ_Fgm2Th6I_",
        "COPIA BD DBeaver.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "_root",
        "2026-03-02T18:35:43.085Z",
        "https://drive.google.com/file/d/1nRWn8rBwBtyiOSdMZwssUZ_Fgm2Th6I_/view",
    ),
    (
        "1Nop9qlgbgdVt1wPMhD9vb8mM61H82uEG",
        "Índice Atlas.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "_root",
        "2026-01-19T10:00:34.107Z",
        "https://drive.google.com/file/d/1Nop9qlgbgdVt1wPMhD9vb8mM61H82uEG/view",
    ),
    (
        "15phBIZo0jS6e8Ve09wPFbUSrMy5W0qsf",
        "Ejemplo país COLOMBIA.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "_root",
        "2025-11-19T11:18:46Z",
        "https://drive.google.com/file/d/15phBIZo0jS6e8Ve09wPFbUSrMy5W0qsf/view",
    ),
    (
        "1lxOQGhErfncAbIXZgf49hmQjSyiR0QbL",
        "TT Atlas_Panhispanico_Lenguaje_Claro_COMPLETO_Saltos.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "_root",
        "2025-09-12T10:38:20Z",
        "https://drive.google.com/file/d/1lxOQGhErfncAbIXZgf49hmQjSyiR0QbL/view",
    ),
    (
        "1e6nPBjCuNEFiNx1r2QDP7fewBnHPPKfj",
        "00 Atlas_Lenguaje_Claro_Indice_Explicado.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "_root",
        "2025-09-12T10:36:26Z",
        "https://drive.google.com/file/d/1e6nPBjCuNEFiNx1r2QDP7fewBnHPPKfj/view",
    ),
    (
        "1ssEsITh2TCm7qI7OLK79BNTeX26m39Y6",
        "01 Atlas_Lenguaje_Claro_Cap1_Proyectos_Refinado.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "1. Proyectos",
        "2025-09-12T10:26:54Z",
        "https://drive.google.com/file/d/1ssEsITh2TCm7qI7OLK79BNTeX26m39Y6/view",
    ),
    (
        "1EJr162UfAYDGIhDcsg6EC-YNR3Yo2bCy",
        "02 Atlas_Lenguaje_Claro_Cap2_Encuentros_Refinado.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "2. Encuentros",
        "2025-09-12T10:28:39Z",
        "https://drive.google.com/file/d/1EJr162UfAYDGIhDcsg6EC-YNR3Yo2bCy/view",
    ),
    (
        "1VyM75p_CXQNX4vr2RI0lTHXOAdiaqgYb",
        "03 Atlas_Lenguaje_Claro_Cap3_Cursos.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "3. Cursos",
        "2025-09-12T10:29:47Z",
        "https://drive.google.com/file/d/1VyM75p_CXQNX4vr2RI0lTHXOAdiaqgYb/view",
    ),
    (
        "1_Rx7rBU85IK38HJJqXBV14xLfTwcA9kN",
        "Leyes españolas.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "4. Leyes",
        "2025-12-09T19:28:49Z",
        "https://drive.google.com/file/d/1_Rx7rBU85IK38HJJqXBV14xLfTwcA9kN/view",
    ),
    (
        "1M9C7wDLrk1OpDGkXvzX3KLlXaVN6RoQ-",
        "04 Atlas_Lenguaje_Claro_Cap4_Leyes.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "4. Leyes",
        "2025-09-12T10:30:40Z",
        "https://drive.google.com/file/d/1M9C7wDLrk1OpDGkXvzX3KLlXaVN6RoQ-/view",
    ),
    (
        "13FSED3pQflH87uQOCVKr1YYgIfoRBMGV",
        "05 Atlas_Lenguaje_Claro_Cap5_Instituciones.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "5. Instituciones",
        "2025-09-12T10:31:35Z",
        "https://drive.google.com/file/d/13FSED3pQflH87uQOCVKr1YYgIfoRBMGV/view",
    ),
]

# Carpetas vacias detectadas en el audit — sin archivos, se registran igual
# para que el mapeo pilar<->carpeta quede documentado desde P2.
_EMPTY_FOLDERS = ["6. Estudios académicos", "7. Conclusiones"]


def build() -> pd.DataFrame:
    df = pd.DataFrame(
        _ENTRIES,
        columns=["file_id", "name", "mime", "folder", "modified_at", "web_link"],
    )
    df["modified_at"] = pd.to_datetime(df["modified_at"], format="ISO8601", utc=True)
    df["snapshot_captured_at"] = pd.to_datetime(SNAPSHOT_CAPTURED_AT)
    return df


def main() -> None:
    df = build()
    DATA_INTERIM.mkdir(parents=True, exist_ok=True)
    out_path = DATA_INTERIM / "drive_manifest.parquet"
    df.to_parquet(out_path, index=False)
    print(f"Escrito {out_path} ({len(df)} archivos; carpetas vacías: {_EMPTY_FOLDERS})")


if __name__ == "__main__":
    main()
