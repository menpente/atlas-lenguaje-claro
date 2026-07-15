from pathlib import Path

import pandas as pd

from atlas.config import DATA_RAW
from atlas.intake.build_manifest_snapshot import build

MANIFEST_PATH = Path(__file__).resolve().parents[1] / "data" / "interim" / "drive_manifest.parquet"


def test_manifest_snapshot_has_no_duplicate_file_ids():
    df = build()
    assert df["file_id"].is_unique


def test_manifest_snapshot_covers_leyes_and_instituciones_folders():
    df = build()
    folders = set(df["folder"])
    assert "4. Leyes" in folders
    assert "5. Instituciones" in folders


# Contacts spreadsheet (COPIA BD DBeaver.xlsx): deliberately excluded from
# git (real people's phone numbers/emails) and from every extractor.
_NO_CACHE_EXPECTED = {"1nRWn8rBwBtyiOSdMZwssUZ_Fgm2Th6I_"}


def test_every_manifest_file_has_a_raw_cache():
    df = build()
    for file_id in df["file_id"]:
        if file_id in _NO_CACHE_EXPECTED:
            continue
        assert (DATA_RAW / f"{file_id}.txt").exists(), file_id


def test_committed_manifest_matches_snapshot_builder():
    if not MANIFEST_PATH.exists():
        return
    on_disk = pd.read_parquet(MANIFEST_PATH)
    rebuilt = build()
    assert set(on_disk["file_id"]) == set(rebuilt["file_id"])
