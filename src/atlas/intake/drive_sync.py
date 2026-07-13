"""Sincroniza el manifiesto de Drive y cachea el texto de cada archivo.

Requiere credenciales de service account en la variable de entorno
GOOGLE_APPLICATION_CREDENTIALS, con acceso de lectura a la carpeta del
Atlas. No se ha ejecutado en este entorno (sin credenciales disponibles);
el manifiesto actual (`data/interim/drive_manifest.parquet`) se generó con
`build_manifest_snapshot.py` a partir de una captura manual vía el
conector interactivo de Drive de la sesión — ver metodologia.qmd, P2.

Idempotencia: una fila por `file_id`; se cachea por `file_id` +
`modified_at`, así que reejecutar sobre un Drive sin cambios no descarga
nada de nuevo ni duplica filas del manifiesto.
"""

from __future__ import annotations

import io

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from atlas.config import DATA_INTERIM, DATA_RAW, DRIVE_ATLAS_FOLDER_ID

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

GOOGLE_DOC_EXPORT_MIME = "text/plain"
FOLDER_MIME = "application/vnd.google-apps.folder"

_TEXT_EXPORTABLE_MIMES = {
    "application/vnd.google-apps.document",
    "application/vnd.google-apps.spreadsheet",
    "application/vnd.google-apps.presentation",
}


def _get_service():
    credentials = service_account.Credentials.from_service_account_file(
        _credentials_path(), scopes=SCOPES
    )
    return build("drive", "v3", credentials=credentials)


def _credentials_path() -> str:
    import os

    path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not path:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS no está configurada; "
            "drive_sync.py requiere una service account con acceso a la carpeta del Atlas"
        )
    return path


def list_folder_tree(service, folder_id: str, folder_name: str = "_root") -> list[dict]:
    """Lista recursivamente archivos y subcarpetas bajo `folder_id`."""
    entries: list[dict] = []
    query = f"'{folder_id}' in parents and trashed = false"
    page_token = None
    while True:
        response = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, webViewLink)",
                pageToken=page_token,
            )
            .execute()
        )
        for item in response.get("files", []):
            if item["mimeType"] == FOLDER_MIME:
                entries.extend(list_folder_tree(service, item["id"], item["name"]))
            else:
                entries.append(
                    {
                        "file_id": item["id"],
                        "name": item["name"],
                        "mime": item["mimeType"],
                        "folder": folder_name,
                        "modified_at": item["modifiedTime"],
                        "web_link": item.get("webViewLink", ""),
                    }
                )
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return entries


def _cached_modified_at(file_id: str) -> str | None:
    cache_meta = DATA_RAW / f"{file_id}.modified_at"
    return cache_meta.read_text().strip() if cache_meta.exists() else None


def cache_text(service, file_id: str, mime: str, modified_at: str) -> None:
    """Descarga y cachea el texto de un archivo por file_id, si cambió."""
    if _cached_modified_at(file_id) == modified_at:
        return

    if mime in _TEXT_EXPORTABLE_MIMES:
        data = service.files().export(fileId=file_id, mimeType=GOOGLE_DOC_EXPORT_MIME).execute()
        text = data.decode("utf-8") if isinstance(data, bytes) else data
    else:
        buf = io.BytesIO()
        request = service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        text = _extract_text(buf.getvalue(), mime)

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    (DATA_RAW / f"{file_id}.txt").write_text(text, encoding="utf-8")
    (DATA_RAW / f"{file_id}.modified_at").write_text(modified_at, encoding="utf-8")


def _extract_text(content: bytes, mime: str) -> str:
    if mime == "application/pdf":
        import pdfplumber

        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n\n".join(page.extract_text() or "" for page in pdf.pages)
    if mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        import docx

        document = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in document.paragraphs)
    raise ValueError(f"No sé extraer texto de mime={mime!r}; añadir soporte antes de usar")


def sync(folder_id: str = DRIVE_ATLAS_FOLDER_ID) -> pd.DataFrame:
    service = _get_service()
    entries = list_folder_tree(service, folder_id)
    df = pd.DataFrame(entries).drop_duplicates(subset="file_id", keep="last")
    df["modified_at"] = pd.to_datetime(df["modified_at"], format="ISO8601", utc=True)

    for row in df.itertuples():
        cache_text(service, row.file_id, row.mime, str(row.modified_at))

    DATA_INTERIM.mkdir(parents=True, exist_ok=True)
    df.to_parquet(DATA_INTERIM / "drive_manifest.parquet", index=False)
    return df


def main() -> None:
    df = sync()
    print(f"Manifiesto actualizado: {len(df)} archivos")


if __name__ == "__main__":
    main()
