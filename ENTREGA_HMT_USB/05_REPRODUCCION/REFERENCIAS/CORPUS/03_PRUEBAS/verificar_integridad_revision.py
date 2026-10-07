#!/usr/bin/env python3
"""Verifica ausencia y alteración de archivos declarados en una revisión.

Alcance estricto: integridad binaria y portabilidad de rutas. Un PASS de este
programa no prueba teoremas, causalidad matemática ni suficiencia académica.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "HMT_MD_REVISION_INTEGRITY_MANIFEST_V1"
SCOPE = "PRESERVATION_AND_FILE_INTEGRITY_ONLY"
ARTIFACT_CLASS = "REVISION_DE_TRABAJO"
PUBLICATION_STATUS = "NOT_FINAL_READY"
MATHEMATICAL_CLAIMS_STATUS = "NOT_VERIFIED_BY_THIS_CHECK"
COMPUTATIONAL_REGRESSION_SCOPE = "ONLY_EXPLICIT_EXECUTION_RECEIPTS_MAY_BE_LISTED_AND_HASHED"
SEALED_STATE = "SEALED_INTEGRITY_SNAPSHOT_OF_REVISION_WORK"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ManifestError(RuntimeError):
    """Manifiesto inválido, ambiguo o no confinado."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"No se puede leer el manifiesto: {exc}") from exc


def _relative_path(value: object, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ManifestError(f"{field} debe ser una ruta relativa no vacía")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ManifestError(f"{field} no está confinado: {value!r}")
    return path


def _contains_symlink(root: Path, relative: Path) -> bool:
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return True
    return False


def verify_manifest(manifest_path: Path) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    data = _load_json(manifest_path)
    if not isinstance(data, dict):
        raise ManifestError("La raíz JSON debe ser un objeto")
    if data.get("schema") != SCHEMA:
        raise ManifestError(f"schema debe ser {SCHEMA}")
    if data.get("scope") != SCOPE:
        raise ManifestError(f"scope debe ser {SCOPE}")
    if data.get("artifact_class") != ARTIFACT_CLASS:
        raise ManifestError(f"artifact_class debe ser {ARTIFACT_CLASS}")
    if data.get("publication_status") != PUBLICATION_STATUS:
        raise ManifestError(f"publication_status debe ser {PUBLICATION_STATUS}")
    if data.get("mathematical_universal_claims") != MATHEMATICAL_CLAIMS_STATUS:
        raise ManifestError(
            f"mathematical_universal_claims debe ser {MATHEMATICAL_CLAIMS_STATUS}"
        )
    if data.get("computational_regression") != COMPUTATIONAL_REGRESSION_SCOPE:
        raise ManifestError(
            f"computational_regression debe ser {COMPUTATIONAL_REGRESSION_SCOPE}"
        )
    if data.get("hash_algorithm") != "sha256":
        raise ManifestError("hash_algorithm debe ser sha256")

    root_relative = _relative_path(data.get("root"), "root")
    root = (manifest_path.parent / root_relative).resolve(strict=False)
    if not root.is_dir():
        raise ManifestError("La raíz declarada no existe o no es directorio")
    seal_state = data.get("seal_state")
    compilation_complete = data.get("compilation_complete")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ManifestError("entries debe ser una lista")

    # La plantilla no puede producir accidentalmente un PASS durante la compilación.
    if seal_state != SEALED_STATE or compilation_complete is not True:
        return {
            "schema": "HMT_MD_REVISION_INTEGRITY_RECEIPT_V1",
            "scope": SCOPE,
            "artifact_class": ARTIFACT_CLASS,
            "publication_status": PUBLICATION_STATUS,
            "mathematical_universal_claims": MATHEMATICAL_CLAIMS_STATUS,
            "computational_regression": COMPUTATIONAL_REGRESSION_SCOPE,
            "status": "HOLD_NOT_SEALED",
            "paths_are_relative_to_declared_root": True,
            "checked": 0,
            "missing": [],
            "altered": [],
            "message": "La plantilla sigue abierta; genere las huellas sólo después de terminar la compilación.",
        }
    if not entries:
        raise ManifestError("Un manifiesto sellado no puede tener entries vacío")

    seen: set[str] = set()
    missing: list[str] = []
    altered: list[dict[str, object]] = []
    invalid: list[dict[str, str]] = []
    checked = 0
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ManifestError(f"entries[{index}] debe ser un objeto")
        relative = _relative_path(entry.get("path"), f"entries[{index}].path")
        portable = relative.as_posix()
        if portable in seen:
            raise ManifestError(f"Ruta duplicada en entries: {portable}")
        seen.add(portable)
        expected_hash = entry.get("sha256")
        expected_size = entry.get("size")
        if not isinstance(expected_hash, str) or not SHA256_RE.fullmatch(expected_hash):
            raise ManifestError(f"entries[{index}].sha256 no es SHA-256 hexadecimal")
        if isinstance(expected_size, bool) or not isinstance(expected_size, int) or expected_size < 0:
            raise ManifestError(f"entries[{index}].size debe ser entero no negativo")
        if _contains_symlink(root, relative):
            invalid.append({"path": portable, "error": "symlink_not_allowed"})
            continue
        candidate = (root / relative).resolve(strict=False)
        try:
            candidate.relative_to(root)
        except ValueError:
            invalid.append({"path": portable, "error": "resolved_path_outside_root"})
            continue
        if not candidate.is_file():
            missing.append(portable)
            continue
        actual_size = candidate.stat().st_size
        actual_hash = sha256_file(candidate)
        checked += 1
        if actual_size != expected_size or actual_hash != expected_hash:
            altered.append(
                {
                    "path": portable,
                    "expected_size": expected_size,
                    "actual_size": actual_size,
                    "expected_sha256": expected_hash,
                    "actual_sha256": actual_hash,
                }
            )

    ok = not missing and not altered and not invalid and checked == len(entries)
    return {
        "schema": "HMT_MD_REVISION_INTEGRITY_RECEIPT_V1",
        "scope": SCOPE,
        "artifact_class": ARTIFACT_CLASS,
        "publication_status": PUBLICATION_STATUS,
        "mathematical_universal_claims": MATHEMATICAL_CLAIMS_STATUS,
        "computational_regression": COMPUTATIONAL_REGRESSION_SCOPE,
        "status": "PASS_FILE_INTEGRITY" if ok else "FAIL_FILE_INTEGRITY",
        "paths_are_relative_to_declared_root": True,
        "manifest_sha256": sha256_file(manifest_path),
        "declared": len(entries),
        "checked": checked,
        "missing": sorted(missing),
        "altered": sorted(altered, key=lambda item: str(item["path"])),
        "invalid": sorted(invalid, key=lambda item: item["path"]),
        "claims_not_made": [
            "No demuestra teoremas ni hipótesis.",
            "No certifica causalidad HMT--MD.",
            "No sustituye puertas científicas ni revisión académica.",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "MANIFIESTO_INTEGRIDAD_REVISION_PLANTILLA.json",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = verify_manifest(args.manifest)
    except ManifestError as exc:
        print(f"FAIL_MANIFEST_INTEGRIDAD: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == "PASS_FILE_INTEGRITY":
        return 0
    if result["status"] == "HOLD_NOT_SEALED":
        return 3
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
