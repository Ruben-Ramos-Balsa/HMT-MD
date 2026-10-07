#!/usr/bin/env python3
"""Entrada autónoma y fail-closed del paquete universitario HMT--MD.

Solo usa la biblioteca estándar, solo lee la raíz candidata y no compila.
El modo ordinario exige cierre material total; ``--check-staging`` acredita
únicamente que la fotografía bloqueada es íntegra y no ha sido promovida.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import posixpath
import re
import sys
import tempfile
import types
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_START = ROOT / "START_HERE_HMT_MD.json"
START_SCHEMA = "hmt-autonomous-root-entry-v1"
CONTRACT_SCHEMA = "hmt-proof-carrier-admission-v2"
GRAPH_SCHEMA = "hmt-complete-inventory-graph-v1"
LOCAL_INPUT_SCHEMA = "hmt-local-input-manifest-v2"
ENTRYPOINT_SCHEMA = "hmt-three-successor-entrypoints-v2"
STAGING = "STAGING_NO_PROMOTION"
FINAL = "FINAL_READY"
MATERIALIZED = "MATERIALIZED_EXACT_SHA256"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_SYSTEM_INPUT_ROOTS = ("/usr/local/texlive", "/Library/TeX")
FATAL_LOG_PATTERNS = (
    "Emergency stop",
    "Fatal error occurred",
    "No pages of output",
    "==> Fatal error",
)
BUILD_STATE_SUFFIXES = {
    ".aux", ".bbl", ".bcf", ".blg", ".lof", ".lot", ".nav", ".out",
    ".snm", ".toc",
}

EXPECTED_METRICS = {
    "scientific_nodes": 14175,
    "scientific_materialized_nodes": 14175,
    "active_nodes": 496,
    "api_chunk_nodes": 1539,
    "claim_nodes": 46,
    "full_registry_claim_nodes": 117,
    "full_registry_evidence_nodes": 188,
    "full_registry_causal_edges": 249,
    "material_owner_nodes": 49,
    "view_nodes": 20,
    "eval_nodes": 40,
    "scientific_transition_index_entries": 137,
    "active_toc_entries": 3019,
    "active_fls_local_inputs": 496,
}

EXPECTED_OUTPUT_BUNDLES = {"INTEGRAL", "SINTESIS_ACADEMICA", "CADENA_COMPACTA"}
EXPECTED_RECEIPT_IDS = {
    "EVIDENCE_MANIFEST",
    "MARKER_MANIFEST",
    "ADDITIVE_DELTA_MANIFEST",
    "TERMINAL_INDEX",
    "GENERATED_CONSTANTS",
    "GENEALOGY_UNIQUE",
    "EXT_TPK_AUTONOMOUS",
    "R_HMT_PRECEDENCE_FULL",
    "JOINT_CONTINUUM",
    "MASS_LAW",
    "PHYSICS_OWNERS",
    "DOMAIN_BINDINGS",
    "RUNTIME_ISOLATION",
    "LOCAL_INPUT_MANIFEST",
    "THREE_ENTRYPOINT_MANIFEST",
    "ADMISSION_V2",
}

REQUIRED_HUMAN_PHRASES = (
    "generación coinductiva correlacionada, de profundidad arbitraria, de π, φ, e y α por la dinámica APP–TRIT–TPK, con retorno de fase, avance de memoria y conservación genealógica",
    "46 centinelas tipados",
    "117 claims registrados",
    "14.175 objetos científicos",
)
FORBIDDEN_HUMAN_TERMS = ("cuadrirrelación", "cuatrirrelación")
PREDECESSOR_PDF_HASHES = {
    "dba375044bf3511bd30a885d1d86c8f589498fed94bfb19f00400b605ddc0835",
    "37b3328765b73072aaee13d10028d5334f082aba2ddc26de853c90d9035401b4",
    "aceb2f6c3b22b80590fe7ff6d9a087a1280ace78ec721945f2a7434bf452eb93",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_hex64(value: object) -> bool:
    return isinstance(value, str) and bool(HEX64.fullmatch(value))


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_NOT_OBJECT:{path}")
    return value


def local_path(root: Path, raw: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(raw, str) or not raw:
        errors.append(f"{label}_PATH_UNSET")
        return None
    relative = Path(raw)
    if relative.is_absolute() or ".." in relative.parts:
        errors.append(f"{label}_PATH_UNSAFE:{raw}")
        return None
    path = (root / relative).resolve(strict=False)
    try:
        path.relative_to(root.resolve(strict=True))
    except ValueError:
        errors.append(f"{label}_PATH_OUTSIDE_ROOT:{raw}")
        return None
    return path


def check_exact_file(
    root: Path,
    record: dict[str, Any],
    label: str,
    errors: list[str],
    blockers: list[str],
    blocker_id: str,
) -> Path | None:
    path = local_path(root, record.get("candidate_relative_path"), label, errors)
    expected = record.get("sha256")
    if path is None:
        blockers.append(blocker_id)
        return None
    if not path.is_file():
        blockers.append(blocker_id)
        return None
    if not is_hex64(expected):
        blockers.append(blocker_id)
        return path
    actual = sha256(path)
    if actual != expected:
        errors.append(f"{label}_HASH_MISMATCH:{actual}!={expected}")
        blockers.append(blocker_id)
        return None
    return path.resolve(strict=True)


def import_module(path: Path, name: str) -> Any:
    # El verificador debe seguir siendo de sólo lectura incluso sin ``-B``:
    # cargar por importlib crearía __pycache__ dentro del propio paquete y
    # violaría la clausura que se comprueba a continuación.
    module = types.ModuleType(name)
    module.__file__ = str(path)
    source = path.read_text(encoding="utf-8")
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


def canonical_digest(rows: list[str]) -> str:
    payload = ("\n".join(sorted(rows)) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def normalize_fls_record(raw: str, pwd: str) -> str:
    value = raw.strip()
    if not value or "\x00" in value:
        raise ValueError("FLS_RECORD_EMPTY_OR_NUL")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    if not posixpath.isabs(value):
        value = posixpath.join(pwd, value)
    normalized = posixpath.normpath(value)
    if not posixpath.isabs(normalized):
        raise ValueError(f"FLS_RECORD_NOT_ABSOLUTE_AFTER_PWD:{raw}")
    return normalized


def parse_fls_portable(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
    pwd_rows = [posixpath.normpath(row[4:].strip()) for row in lines if row.startswith("PWD ")]
    if len(set(pwd_rows)) != 1 or not pwd_rows or not posixpath.isabs(pwd_rows[0]):
        raise ValueError(f"FLS_PWD_INVALID:{pwd_rows!r}")
    pwd = pwd_rows[0]

    def records(kind: str) -> list[str]:
        prefix = kind + " "
        return sorted({
            normalize_fls_record(row[len(prefix):], pwd)
            for row in lines if row.startswith(prefix)
        })

    return {"pwd": pwd, "inputs": records("INPUT"), "outputs": records("OUTPUT")}


def is_system_fls_input(path: str) -> bool:
    return any(path == root or path.startswith(root + "/") for root in EXPECTED_SYSTEM_INPUT_ROOTS)


def runtime_cache_extras(root: Path) -> list[str]:
    """Enumera cachés ejecutables ajenos al contenido fuente del paquete."""
    result: set[str] = set()
    for current_raw, directories, filenames in os.walk(root, followlinks=False):
        current = Path(current_raw)
        for directory in list(directories):
            if directory == "__pycache__":
                path = current / directory
                result.add(path.relative_to(root).as_posix())
                # El directorio completo queda prohibido; no es necesario
                # recorrer ni enumerar cada bytecode de su interior.
                directories.remove(directory)
        for filename in filenames:
            if filename.endswith(".pyc"):
                path = current / filename
                result.add(path.relative_to(root).as_posix())
    return sorted(result)


def symlink_extras(root: Path) -> list[str]:
    """Impide que la autonomía dependa de enlaces presentes sólo en el host."""
    result: set[str] = set()
    for current_raw, directories, filenames in os.walk(root, followlinks=False):
        current = Path(current_raw)
        for name in list(directories):
            path = current / name
            if path.is_symlink():
                result.add(path.relative_to(root).as_posix())
                directories.remove(name)
        for name in filenames:
            path = current / name
            if path.is_symlink():
                result.add(path.relative_to(root).as_posix())
    return sorted(result)


def check_unsymlinked_exact_file(
    root: Path,
    record: dict[str, Any],
    label: str,
    errors: list[str],
) -> Path | None:
    raw = record.get("candidate_relative_path")
    expected = record.get("sha256")
    if not isinstance(raw, str) or not raw:
        errors.append(f"{label}_PATH_UNSET")
        return None
    relative = Path(raw)
    if relative.is_absolute() or ".." in relative.parts or relative == Path("."):
        errors.append(f"{label}_PATH_UNSAFE:{raw}")
        return None
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            errors.append(f"{label}_SYMLINK_FORBIDDEN:{raw}")
            return None
    if not cursor.is_file():
        errors.append(f"{label}_FILE_MISSING:{raw}")
        return None
    try:
        cursor.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError):
        errors.append(f"{label}_PATH_OUTSIDE_ROOT:{raw}")
        return None
    if not is_hex64(expected):
        errors.append(f"{label}_HASH_UNSET")
        return None
    actual = sha256(cursor)
    if actual != expected:
        errors.append(f"{label}_HASH_MISMATCH:{actual}!={expected}")
        return None
    return cursor


def validate_pdf_file(path: Path, label: str, errors: list[str]) -> None:
    size = path.stat().st_size
    if size < 1024:
        errors.append(f"{label}_PDF_TOO_SMALL:{size}")
        return
    with path.open("rb") as stream:
        header = stream.read(8)
        stream.seek(max(0, size - 4096))
        tail = stream.read()
    if not header.startswith(b"%PDF-") or b"%%EOF" not in tail:
        errors.append(f"{label}_PDF_STRUCTURE_INVALID")


def validate_log_file(
    path: Path,
    recorded_pdf_path: str,
    label: str,
    errors: list[str],
) -> None:
    body = path.read_text(encoding="utf-8", errors="replace")
    for pattern in FATAL_LOG_PATTERNS:
        if pattern in body:
            errors.append(f"{label}_LOG_FATAL:{pattern}")
    if re.search(r"(?m)^! (?:LaTeX Error|Package .* Error|Undefined control sequence)", body):
        errors.append(f"{label}_LOG_TEX_ERROR")
    if "Output written on" not in body:
        errors.append(f"{label}_LOG_OUTPUT_DECLARATION_MISSING")
    recorded_name = posixpath.basename(recorded_pdf_path)
    recorded_stem = Path(recorded_name).stem
    if recorded_name not in body and recorded_stem not in body:
        errors.append(f"{label}_LOG_RECORDED_PDF_UNIDENTIFIED")


def rows_by_id(
    rows: object,
    key: str,
    expected: set[str],
    label: str,
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        errors.append(f"{label}_NOT_LIST")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            errors.append(f"{label}_ROW_NOT_OBJECT")
            continue
        identity = row.get(key)
        if not isinstance(identity, str) or not identity or identity in result:
            errors.append(f"{label}_ID_MISSING_OR_DUPLICATE:{identity!r}")
            continue
        result[identity] = row
    if set(result) != expected or len(rows) != len(expected):
        errors.append(
            f"{label}_ID_SET_INVALID:missing={sorted(expected-set(result))}:"
            f"extra={sorted(set(result)-expected)}"
        )
    return result


def validate_successor_closure(
    start: dict[str, Any],
    contract: dict[str, Any],
    root: Path,
    receipt_payloads: dict[str, dict[str, Any]],
    receipt_paths: dict[str, Path],
    bundle_files: dict[str, dict[str, Path]],
    errors: list[str],
    blockers: list[str],
) -> None:
    local_manifest = receipt_payloads.get("LOCAL_INPUT_MANIFEST", {})
    entry_manifest = receipt_payloads.get("THREE_ENTRYPOINT_MANIFEST", {})
    attempted_final = any(
        value == FINAL for value in (
            start.get("status"), contract.get("status"),
            local_manifest.get("status"), entry_manifest.get("status"),
        )
    )
    if not attempted_final:
        return

    before = len(errors)
    closure_blockers = {
        "RECEIPT:LOCAL_INPUT_MANIFEST",
        "RECEIPT:THREE_ENTRYPOINT_MANIFEST",
        *("OUTPUT_BUNDLE:" + bundle_id for bundle_id in EXPECTED_OUTPUT_BUNDLES),
    }
    cache_extras = runtime_cache_extras(root)
    if cache_extras:
        sample = ",".join(cache_extras[:8])
        errors.append(
            f"CLOSURE_RUNTIME_CACHE_FORBIDDEN:count={len(cache_extras)}:sample={sample}"
        )
    links = symlink_extras(root)
    if links:
        sample = ",".join(links[:8])
        errors.append(
            f"CLOSURE_SYMLINK_EXTRA_FORBIDDEN:count={len(links)}:sample={sample}"
        )
    if local_manifest.get("schema_version") != LOCAL_INPUT_SCHEMA:
        errors.append(f"CLOSURE_LOCAL_INPUT_SCHEMA:{local_manifest.get('schema_version')}")
    if entry_manifest.get("schema_version") != ENTRYPOINT_SCHEMA:
        errors.append(f"CLOSURE_ENTRYPOINT_SCHEMA:{entry_manifest.get('schema_version')}")
    for label, payload in (("LOCAL_INPUT", local_manifest), ("ENTRYPOINT", entry_manifest)):
        if payload.get("status") != FINAL or payload.get("promotion_allowed") is not True:
            errors.append(f"CLOSURE_{label}_NOT_FINAL")
        if payload.get("blocking_obligations") != []:
            errors.append(f"CLOSURE_{label}_BLOCKERS_NOT_EMPTY")
    if local_manifest.get("system_input_roots") != list(EXPECTED_SYSTEM_INPUT_ROOTS):
        errors.append("CLOSURE_SYSTEM_INPUT_ROOTS_INVALID")
    if local_manifest.get("semantic_allowlist_permitted") is not False:
        errors.append("CLOSURE_SEMANTIC_ALLOWLIST_PERMITTED")
    if local_manifest.get("inventory_driven") is not True:
        errors.append("CLOSURE_NOT_INVENTORY_DRIVEN")

    # Los dos manifiestos deben estar ligados también desde el contrato, no
    # sólo desde la lista de recibos de START_HERE.
    for receipt_id, contract_key in (
        ("LOCAL_INPUT_MANIFEST", "candidate_local_input_manifest"),
        ("THREE_ENTRYPOINT_MANIFEST", "candidate_entrypoint_manifest"),
    ):
        path = receipt_paths.get(receipt_id)
        record = contract.get(contract_key, {})
        if path is None or not isinstance(record, dict):
            errors.append(f"CLOSURE_{receipt_id}_CONTRACT_RECORD_MISSING")
            continue
        relative = path.relative_to(root).as_posix()
        if record.get("candidate_relative_path") != relative or record.get("sha256") != sha256(path):
            errors.append(f"CLOSURE_{receipt_id}_CONTRACT_BINDING_MISMATCH")
    local_record = contract.get("candidate_local_input_manifest", {})
    if not isinstance(local_record, dict) or local_record.get("semantic_allowlist_permitted") is not False:
        errors.append("CLOSURE_CONTRACT_SEMANTIC_ALLOWLIST_INVALID")

    start_bundles = rows_by_id(
        start.get("output_bundles"), "bundle_id", EXPECTED_OUTPUT_BUNDLES,
        "CLOSURE_START_BUNDLES", errors,
    )
    contract_bundles = rows_by_id(
        contract.get("required_publication_bundles"), "bundle_id",
        EXPECTED_OUTPUT_BUNDLES, "CLOSURE_CONTRACT_BUNDLES", errors,
    )
    local_bundles = rows_by_id(
        local_manifest.get("bundles"), "bundle_id", EXPECTED_OUTPUT_BUNDLES,
        "CLOSURE_LOCAL_BUNDLES", errors,
    )
    entry_bundles = rows_by_id(
        entry_manifest.get("bundles"), "bundle_id", EXPECTED_OUTPUT_BUNDLES,
        "CLOSURE_ENTRY_BUNDLES", errors,
    )

    input_rows = local_manifest.get("inputs")
    if not isinstance(input_rows, list):
        errors.append("CLOSURE_INPUT_ROWS_NOT_LIST")
        input_rows = []
    inputs_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    candidates_by_bundle: dict[str, set[str]] = {
        bundle_id: set() for bundle_id in EXPECTED_OUTPUT_BUNDLES
    }
    for index, row in enumerate(input_rows):
        label = f"CLOSURE_INPUT_{index}"
        if not isinstance(row, dict):
            errors.append(f"{label}_NOT_OBJECT")
            continue
        bundle_id = row.get("bundle_id")
        recorded = row.get("fls_recorded_path")
        original_recorded = row.get("source_fls_recorded_path_provenance_only")
        if bundle_id not in EXPECTED_OUTPUT_BUNDLES or not isinstance(recorded, str):
            errors.append(f"{label}_IDENTITY_INVALID")
            continue
        try:
            canonical_recorded = normalize_fls_record(recorded, "/")
        except ValueError as exc:
            errors.append(f"{label}_RECORDED_PATH_INVALID:{exc}")
            continue
        if canonical_recorded != recorded or is_system_fls_input(recorded):
            errors.append(f"{label}_RECORDED_PATH_NONCANONICAL_OR_SYSTEM")
        if not isinstance(original_recorded, str) or not original_recorded:
            errors.append(f"{label}_ORIGINAL_FLS_RECORD_MISSING")
        key = (bundle_id, recorded)
        if key in inputs_by_key:
            errors.append(f"{label}_DUPLICATE_RECORDED_PATH")
            continue
        inputs_by_key[key] = row
        candidate_relative = row.get("candidate_relative_path")
        if not isinstance(candidate_relative, str):
            errors.append(f"{label}_CANDIDATE_PATH_INVALID")
            continue
        if candidate_relative in candidates_by_bundle[bundle_id]:
            errors.append(f"{label}_DUPLICATE_CANDIDATE_PATH")
        candidates_by_bundle[bundle_id].add(candidate_relative)
        if Path(candidate_relative).name != posixpath.basename(recorded):
            errors.append(f"{label}_BASENAME_MISMATCH")
        role = row.get("role")
        expected_role = (
            "BUILD_STATE_INPUT" if Path(recorded).suffix.lower() in BUILD_STATE_SUFFIXES
            else "SOURCE_OR_ASSET"
        )
        if role != expected_role:
            errors.append(f"{label}_ROLE_INVALID:{role}!={expected_role}")
        check_unsymlinked_exact_file(root, row, label, errors)

    output_rows = local_manifest.get("outputs")
    if not isinstance(output_rows, list):
        errors.append("CLOSURE_OUTPUT_ROWS_NOT_LIST")
        output_rows = []
    outputs_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for index, row in enumerate(output_rows):
        label = f"CLOSURE_OUTPUT_{index}"
        if not isinstance(row, dict):
            errors.append(f"{label}_NOT_OBJECT")
            continue
        bundle_id = row.get("bundle_id")
        kind = str(row.get("kind", "")).lower()
        recorded = row.get("fls_recorded_path")
        original_recorded = row.get("source_fls_recorded_path_provenance_only")
        if bundle_id not in EXPECTED_OUTPUT_BUNDLES or kind not in {"pdf", "log"} or not isinstance(recorded, str):
            errors.append(f"{label}_IDENTITY_INVALID")
            continue
        if not isinstance(original_recorded, str) or not original_recorded:
            errors.append(f"{label}_ORIGINAL_FLS_RECORD_MISSING")
        try:
            canonical_recorded = normalize_fls_record(recorded, "/")
        except ValueError as exc:
            errors.append(f"{label}_RECORDED_PATH_INVALID:{exc}")
            continue
        if canonical_recorded != recorded or Path(recorded).suffix.lower() != "." + kind:
            errors.append(f"{label}_RECORDED_PATH_OR_SUFFIX_INVALID")
        key = (bundle_id, kind)
        if key in outputs_by_key:
            errors.append(f"{label}_DUPLICATE_KIND")
            continue
        outputs_by_key[key] = row

    total_expected = 0
    for bundle_id in sorted(EXPECTED_OUTPUT_BUNDLES):
        files = bundle_files.get(bundle_id, {})
        start_row = start_bundles.get(bundle_id, {})
        contract_row = contract_bundles.get(bundle_id, {})
        local_row = local_bundles.get(bundle_id, {})
        entry_row = entry_bundles.get(bundle_id, {})
        if set(files) != {"pdf", "fls", "log"}:
            errors.append(f"CLOSURE_{bundle_id}_FILES_INCOMPLETE")
            continue
        if start_row.get("status") != MATERIALIZED or contract_row.get("status") != MATERIALIZED:
            errors.append(f"CLOSURE_{bundle_id}_STATUS_NOT_MATERIALIZED")
        start_artifacts = start_row.get("artifacts", {})
        contract_artifacts = contract_row.get("artifacts", {})
        if not isinstance(start_artifacts, dict) or not isinstance(contract_artifacts, dict):
            errors.append(f"CLOSURE_{bundle_id}_ARTIFACTS_INVALID")
            continue
        for kind in ("pdf", "fls", "log"):
            if start_artifacts.get(kind) != contract_artifacts.get(kind):
                errors.append(f"CLOSURE_{bundle_id}_{kind.upper()}_START_CONTRACT_MISMATCH")
        stems = {path.stem for path in files.values()}
        if len(stems) != 1:
            errors.append(f"CLOSURE_{bundle_id}_LOCAL_TRIPLE_STEM_MISMATCH")
        fls_record = start_artifacts.get("fls", {})
        if not isinstance(fls_record, dict):
            errors.append(f"CLOSURE_{bundle_id}_FLS_RECORD_INVALID")
            continue
        fls_relative = fls_record.get("candidate_relative_path")
        fls_hash = fls_record.get("sha256")
        if (
            local_row.get("fls_relative_path") != fls_relative
            or local_row.get("fls_sha256") != fls_hash
            or entry_row.get("fls_relative_path") != fls_relative
            or entry_row.get("fls_sha256") != fls_hash
            or sha256(files["fls"]) != fls_hash
        ):
            errors.append(f"CLOSURE_{bundle_id}_FLS_BINDING_MISMATCH")
        portable_relative = local_row.get("portable_fls_relative_path")
        portable_hash = local_row.get("portable_fls_sha256")
        if (
            entry_row.get("portable_fls_relative_path") != portable_relative
            or entry_row.get("portable_fls_sha256") != portable_hash
            or portable_relative == fls_relative
        ):
            errors.append(f"CLOSURE_{bundle_id}_PORTABLE_FLS_BINDING_MISMATCH")
        portable_path = check_unsymlinked_exact_file(
            root,
            {
                "candidate_relative_path": portable_relative,
                "sha256": portable_hash,
            },
            f"CLOSURE_{bundle_id}_PORTABLE_FLS",
            errors,
        )
        if portable_path is None:
            continue
        try:
            original_fls_data = parse_fls_portable(files["fls"])
            fls_data = parse_fls_portable(portable_path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"CLOSURE_{bundle_id}_FLS_INVALID:{exc}")
            continue
        original_non_system_inputs = {
            path for path in original_fls_data["inputs"]
            if not is_system_fls_input(path)
        }
        manifest_original_inputs = {
            row.get("source_fls_recorded_path_provenance_only")
            for row in input_rows
            if isinstance(row, dict) and row.get("bundle_id") == bundle_id
        }
        if manifest_original_inputs != original_non_system_inputs:
            errors.append(
                f"CLOSURE_{bundle_id}_ORIGINAL_FLS_INPUT_MAP_MISMATCH:"
                f"missing={len(original_non_system_inputs-manifest_original_inputs)}:"
                f"extra={len(manifest_original_inputs-original_non_system_inputs)}"
            )
        original_output_records = {
            row.get("source_fls_recorded_path_provenance_only")
            for row in output_rows
            if isinstance(row, dict) and row.get("bundle_id") == bundle_id
        }
        expected_original_outputs = {
            path for path in original_fls_data["outputs"]
            if Path(path).suffix.lower() in {".pdf", ".log"}
        }
        if original_output_records != expected_original_outputs:
            errors.append(
                f"CLOSURE_{bundle_id}_ORIGINAL_FLS_OUTPUT_MAP_MISMATCH"
            )
        all_inputs = fls_data["inputs"]
        system_inputs = [path for path in all_inputs if is_system_fls_input(path)]
        non_system_inputs = [path for path in all_inputs if not is_system_fls_input(path)]
        total_expected += len(non_system_inputs)
        manifest_keys = {
            recorded for (row_bundle, recorded) in inputs_by_key if row_bundle == bundle_id
        }
        if manifest_keys != set(non_system_inputs):
            errors.append(
                f"CLOSURE_{bundle_id}_INPUT_SET_MISMATCH:"
                f"missing={len(set(non_system_inputs)-manifest_keys)}:"
                f"extra={len(manifest_keys-set(non_system_inputs))}"
            )
        content_rows = [
            f"{path}\t{inputs_by_key[(bundle_id, path)].get('sha256', '')}"
            for path in non_system_inputs if (bundle_id, path) in inputs_by_key
        ]
        expected_summary = {
            "pwd_provenance_only": fls_data["pwd"],
            "source_pwd_provenance_only": original_fls_data["pwd"],
            "all_input_count": len(all_inputs),
            "all_input_path_digest": canonical_digest(all_inputs),
            "system_input_count": len(system_inputs),
            "system_input_path_digest": canonical_digest(system_inputs),
            "non_system_input_count": len(non_system_inputs),
            "non_system_path_digest": canonical_digest(non_system_inputs),
            "non_system_path_content_digest": canonical_digest(content_rows),
            "output_count": len(fls_data["outputs"]),
            "output_path_digest": canonical_digest(fls_data["outputs"]),
        }
        for key, expected in expected_summary.items():
            if local_row.get(key) != expected:
                errors.append(f"CLOSURE_{bundle_id}_{key.upper()}_MISMATCH")

        entry_relative = entry_row.get("entrypoint_relative_path")
        entry_hash = entry_row.get("entrypoint_sha256")
        recorded_entrypoint = entry_row.get("fls_recorded_entrypoint")
        if (
            entry_row.get("status") != MATERIALIZED
            or contract_row.get("entrypoint_relative_path") != entry_relative
            or contract_row.get("entrypoint_sha256") != entry_hash
            or not isinstance(recorded_entrypoint, str)
        ):
            errors.append(f"CLOSURE_{bundle_id}_ENTRYPOINT_BINDING_INVALID")
        else:
            mapped = inputs_by_key.get((bundle_id, recorded_entrypoint))
            if (
                recorded_entrypoint not in non_system_inputs
                or mapped is None
                or mapped.get("candidate_relative_path") != entry_relative
                or mapped.get("sha256") != entry_hash
                or Path(entry_relative).name != posixpath.basename(recorded_entrypoint)
            ):
                errors.append(f"CLOSURE_{bundle_id}_ENTRYPOINT_NOT_EXACT_FLS_INPUT")
            if isinstance(entry_relative, str):
                check_unsymlinked_exact_file(
                    root,
                    {"candidate_relative_path": entry_relative, "sha256": entry_hash},
                    f"CLOSURE_{bundle_id}_ENTRYPOINT",
                    errors,
                )

        for kind in ("pdf", "log"):
            row = outputs_by_key.get((bundle_id, kind))
            artifact = start_artifacts.get(kind, {})
            recorded_candidates = [
                path for path in fls_data["outputs"] if Path(path).suffix.lower() == "." + kind
            ]
            if row is None or len(recorded_candidates) != 1:
                errors.append(f"CLOSURE_{bundle_id}_{kind.upper()}_FLS_OUTPUT_COUNT_INVALID")
                continue
            recorded = row.get("fls_recorded_path")
            if recorded != recorded_candidates[0]:
                errors.append(f"CLOSURE_{bundle_id}_{kind.upper()}_RECORDED_OUTPUT_MISMATCH")
            if not isinstance(artifact, dict) or (
                row.get("candidate_relative_path") != artifact.get("candidate_relative_path")
                or row.get("sha256") != artifact.get("sha256")
                or sha256(files[kind]) != artifact.get("sha256")
            ):
                errors.append(f"CLOSURE_{bundle_id}_{kind.upper()}_LOCAL_OUTPUT_BINDING_MISMATCH")
        # El log original declara el nombre/ruta de la salida de compilación
        # original. El mapa FLS portátil liga esa salida por SHA a un destino
        # local que puede tener otro nombre; no debe exigirse que el log
        # histórico haya anticipado ese renombrado posterior.
        pdf_output = outputs_by_key.get((bundle_id, "pdf"), {}).get(
            "source_fls_recorded_path_provenance_only", ""
        )
        validate_pdf_file(files["pdf"], f"CLOSURE_{bundle_id}", errors)
        validate_log_file(files["log"], str(pdf_output), f"CLOSURE_{bundle_id}", errors)

    if len(input_rows) != total_expected or local_manifest.get("total_non_system_input_count") != total_expected:
        errors.append(
            f"CLOSURE_TOTAL_INPUT_COUNT_MISMATCH:{len(input_rows)}:"
            f"{local_manifest.get('total_non_system_input_count')}!={total_expected}"
        )
    if len(output_rows) != 2 * len(EXPECTED_OUTPUT_BUNDLES):
        errors.append(f"CLOSURE_OUTPUT_ROW_COUNT_INVALID:{len(output_rows)}")
    if len(errors) != before:
        blockers.extend(sorted(closure_blockers))


def run_successor_closure_redteams() -> list[dict[str, Any]]:
    """Ejercita la clausura con un paquete mínimo íntegramente temporal."""
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="hmt-three-closure-") as temp_name:
        root = Path(temp_name)
        bundle_files: dict[str, dict[str, Path]] = {}
        start_bundles: list[dict[str, Any]] = []
        contract_bundles: list[dict[str, Any]] = []
        local_bundles: list[dict[str, Any]] = []
        entry_bundles: list[dict[str, Any]] = []
        input_rows: list[dict[str, Any]] = []
        output_rows: list[dict[str, Any]] = []

        for bundle_id in sorted(EXPECTED_OUTPUT_BUNDLES):
            stem = "main_" + bundle_id.casefold()
            source_dir = root / "sources" / bundle_id
            output_dir = root / "outputs" / bundle_id
            source_dir.mkdir(parents=True)
            output_dir.mkdir(parents=True)
            entrypoint = source_dir / (stem + ".tex")
            toc = source_dir / (stem + ".toc")
            pdf = output_dir / (stem + ".pdf")
            log = output_dir / (stem + ".log")
            fls = output_dir / (stem + ".fls")
            entrypoint.write_text("synthetic entrypoint\n", encoding="utf-8")
            toc.write_text("synthetic build state\n", encoding="utf-8")
            pdf.write_bytes(b"%PDF-1.5\n" + b"0" * 1100 + b"\n%%EOF\n")
            recorded_root = f"/synthetic-build/{bundle_id}"
            recorded_entry = recorded_root + "/" + entrypoint.name
            recorded_toc = recorded_root + "/" + toc.name
            recorded_pdf = recorded_root + "/" + pdf.name
            recorded_log = recorded_root + "/" + log.name
            log.write_text(
                f'Output written on "{recorded_pdf}" (1 page).\n', encoding="utf-8"
            )
            fls.write_text(
                "\n".join((
                    "PWD " + recorded_root,
                    "INPUT /usr/local/texlive/synthetic/system.sty",
                    "INPUT " + entrypoint.name,
                    "INPUT " + toc.name,
                    "OUTPUT " + recorded_log,
                    "OUTPUT " + recorded_pdf,
                )) + "\n",
                encoding="utf-8",
            )
            portable_fls = output_dir / (stem + ".portable.fls")
            portable_entry = str(entrypoint.resolve(strict=True))
            portable_toc = str(toc.resolve(strict=True))
            portable_pdf = str(pdf.resolve(strict=True))
            portable_log = str(log.resolve(strict=True))
            portable_fls.write_text(
                "\n".join((
                    "PWD " + str(root.resolve(strict=True)),
                    "INPUT /usr/local/texlive/synthetic/system.sty",
                    "INPUT " + portable_entry,
                    "INPUT " + portable_toc,
                    "OUTPUT " + portable_log,
                    "OUTPUT " + portable_pdf,
                )) + "\n",
                encoding="utf-8",
            )
            bundle_files[bundle_id] = {"pdf": pdf, "fls": fls, "log": log}
            artifacts = {
                kind: {
                    "candidate_relative_path": path.relative_to(root).as_posix(),
                    "sha256": sha256(path),
                }
                for kind, path in bundle_files[bundle_id].items()
            }
            start_bundles.append({
                "bundle_id": bundle_id,
                "status": MATERIALIZED,
                "artifacts": copy.deepcopy(artifacts),
            })
            contract_bundles.append({
                "bundle_id": bundle_id,
                "status": MATERIALIZED,
                "entrypoint_relative_path": entrypoint.relative_to(root).as_posix(),
                "entrypoint_sha256": sha256(entrypoint),
                "artifacts": copy.deepcopy(artifacts),
            })
            fls_data = parse_fls_portable(portable_fls)
            system_inputs = [path for path in fls_data["inputs"] if is_system_fls_input(path)]
            non_system_inputs = [path for path in fls_data["inputs"] if not is_system_fls_input(path)]
            candidate_by_recorded = {
                portable_entry: entrypoint,
                portable_toc: toc,
            }
            original_by_recorded = {
                portable_entry: recorded_entry,
                portable_toc: recorded_toc,
            }
            bundle_input_rows = []
            for recorded in non_system_inputs:
                candidate = candidate_by_recorded[recorded]
                bundle_input_rows.append({
                    "bundle_id": bundle_id,
                    "fls_recorded_path": recorded,
                    "source_fls_recorded_path_provenance_only": (
                        original_by_recorded[recorded]
                    ),
                    "candidate_relative_path": candidate.relative_to(root).as_posix(),
                    "sha256": sha256(candidate),
                    "role": (
                        "BUILD_STATE_INPUT"
                        if candidate.suffix.lower() in BUILD_STATE_SUFFIXES
                        else "SOURCE_OR_ASSET"
                    ),
                })
            input_rows.extend(bundle_input_rows)
            content_rows = [
                f"{row['fls_recorded_path']}\t{row['sha256']}"
                for row in bundle_input_rows
            ]
            local_bundles.append({
                "bundle_id": bundle_id,
                "fls_relative_path": artifacts["fls"]["candidate_relative_path"],
                "fls_sha256": artifacts["fls"]["sha256"],
                "portable_fls_relative_path": portable_fls.relative_to(root).as_posix(),
                "portable_fls_sha256": sha256(portable_fls),
                "pwd_provenance_only": fls_data["pwd"],
                "source_pwd_provenance_only": recorded_root,
                "all_input_count": len(fls_data["inputs"]),
                "all_input_path_digest": canonical_digest(fls_data["inputs"]),
                "system_input_count": len(system_inputs),
                "system_input_path_digest": canonical_digest(system_inputs),
                "non_system_input_count": len(non_system_inputs),
                "non_system_path_digest": canonical_digest(non_system_inputs),
                "non_system_path_content_digest": canonical_digest(content_rows),
                "output_count": len(fls_data["outputs"]),
                "output_path_digest": canonical_digest(fls_data["outputs"]),
            })
            entry_bundles.append({
                "bundle_id": bundle_id,
                "status": MATERIALIZED,
                "entrypoint_relative_path": entrypoint.relative_to(root).as_posix(),
                "entrypoint_sha256": sha256(entrypoint),
                "fls_recorded_entrypoint": portable_entry,
                "source_fls_recorded_entrypoint_provenance_only": recorded_entry,
                "fls_relative_path": artifacts["fls"]["candidate_relative_path"],
                "fls_sha256": artifacts["fls"]["sha256"],
                "portable_fls_relative_path": portable_fls.relative_to(root).as_posix(),
                "portable_fls_sha256": sha256(portable_fls),
            })
            for kind, recorded, original_record in (
                ("pdf", portable_pdf, recorded_pdf),
                ("log", portable_log, recorded_log),
            ):
                output_rows.append({
                    "bundle_id": bundle_id,
                    "kind": kind,
                    "fls_recorded_path": recorded,
                    "source_fls_recorded_path_provenance_only": original_record,
                    "candidate_relative_path": artifacts[kind]["candidate_relative_path"],
                    "sha256": artifacts[kind]["sha256"],
                })

        local_manifest = {
            "schema_version": LOCAL_INPUT_SCHEMA,
            "status": FINAL,
            "promotion_allowed": True,
            "blocking_obligations": [],
            "system_input_roots": list(EXPECTED_SYSTEM_INPUT_ROOTS),
            "semantic_allowlist_permitted": False,
            "inventory_driven": True,
            "total_non_system_input_count": len(input_rows),
            "bundles": local_bundles,
            "inputs": input_rows,
            "outputs": output_rows,
        }
        entry_manifest = {
            "schema_version": ENTRYPOINT_SCHEMA,
            "status": FINAL,
            "promotion_allowed": True,
            "blocking_obligations": [],
            "bundles": entry_bundles,
        }
        receipt_dir = root / "receipts"
        receipt_dir.mkdir()
        local_path = receipt_dir / "local.json"
        entry_path = receipt_dir / "entry.json"
        local_path.write_text(json.dumps(local_manifest), encoding="utf-8")
        entry_path.write_text(json.dumps(entry_manifest), encoding="utf-8")
        contract = {
            "status": FINAL,
            "candidate_local_input_manifest": {
                "candidate_relative_path": local_path.relative_to(root).as_posix(),
                "sha256": sha256(local_path),
                "semantic_allowlist_permitted": False,
            },
            "candidate_entrypoint_manifest": {
                "candidate_relative_path": entry_path.relative_to(root).as_posix(),
                "sha256": sha256(entry_path),
            },
            "required_publication_bundles": contract_bundles,
        }
        start = {"status": FINAL, "output_bundles": start_bundles}
        baseline_payloads = {
            "LOCAL_INPUT_MANIFEST": local_manifest,
            "THREE_ENTRYPOINT_MANIFEST": entry_manifest,
        }
        receipt_paths = {
            "LOCAL_INPUT_MANIFEST": local_path,
            "THREE_ENTRYPOINT_MANIFEST": entry_path,
        }

        def exercise(name: str, mutate: Any, expected: str | None) -> None:
            payloads = copy.deepcopy(baseline_payloads)
            mutate(payloads)
            errors: list[str] = []
            blockers: list[str] = []
            validate_successor_closure(
                start, contract, root, payloads, receipt_paths,
                bundle_files, errors, blockers,
            )
            passed = not errors if expected is None else any(expected in error for error in errors)
            rows.append({"name": name, "passed": passed, "errors": errors})

        exercise("closure_positive", lambda value: None, None)
        cache_dir = root / "runtime-cache-redteam" / "__pycache__"
        cache_dir.mkdir(parents=True)
        (cache_dir / "forbidden.pyc").write_bytes(b"synthetic-bytecode")
        exercise(
            "closure_runtime_cache_forbidden",
            lambda value: None,
            "RUNTIME_CACHE_FORBIDDEN",
        )
        (cache_dir / "forbidden.pyc").unlink()
        cache_dir.rmdir()
        cache_dir.parent.rmdir()
        external_target = root.parent / (root.name + "-external-target")
        external_target.write_text("external\n", encoding="utf-8")
        package_symlink = root / "external-runtime-symlink"
        package_symlink.symlink_to(external_target)
        exercise(
            "closure_package_symlink_forbidden",
            lambda value: None,
            "SYMLINK_EXTRA_FORBIDDEN",
        )
        package_symlink.unlink()
        external_target.unlink()
        exercise(
            "closure_empty_input_manifest",
            lambda value: value["LOCAL_INPUT_MANIFEST"].__setitem__("inputs", []),
            "INPUT_SET_MISMATCH",
        )
        exercise(
            "closure_input_removed",
            lambda value: value["LOCAL_INPUT_MANIFEST"]["inputs"].pop(),
            "INPUT_SET_MISMATCH",
        )
        exercise(
            "closure_input_hash_changed",
            lambda value: value["LOCAL_INPUT_MANIFEST"]["inputs"][0].__setitem__("sha256", "0" * 64),
            "HASH_MISMATCH",
        )
        exercise(
            "closure_input_path_escape",
            lambda value: value["LOCAL_INPUT_MANIFEST"]["inputs"][0].__setitem__("candidate_relative_path", "../escape.tex"),
            "PATH_UNSAFE",
        )

        first = baseline_payloads["LOCAL_INPUT_MANIFEST"]["inputs"][0]
        symlink_dir = root / "symlink" / str(first["bundle_id"])
        symlink_dir.mkdir(parents=True)
        symlink = symlink_dir / Path(str(first["candidate_relative_path"])).name
        symlink.symlink_to(root / str(first["candidate_relative_path"]))
        exercise(
            "closure_input_symlink",
            lambda value: value["LOCAL_INPUT_MANIFEST"]["inputs"][0].__setitem__(
                "candidate_relative_path", symlink.relative_to(root).as_posix()
            ),
            "SYMLINK_FORBIDDEN",
        )
        exercise(
            "closure_entrypoint_basename_changed",
            lambda value: value["THREE_ENTRYPOINT_MANIFEST"]["bundles"][0].__setitem__(
                "fls_recorded_entrypoint",
                next(
                    row["fls_recorded_path"]
                    for row in value["LOCAL_INPUT_MANIFEST"]["inputs"]
                    if row["bundle_id"] == value["THREE_ENTRYPOINT_MANIFEST"]["bundles"][0]["bundle_id"]
                    and row["role"] == "BUILD_STATE_INPUT"
                ),
            ),
            "ENTRYPOINT_NOT_EXACT_FLS_INPUT",
        )
        exercise(
            "closure_output_hash_changed",
            lambda value: value["LOCAL_INPUT_MANIFEST"]["outputs"][0].__setitem__("sha256", "f" * 64),
            "LOCAL_OUTPUT_BINDING_MISMATCH",
        )
        exercise(
            "closure_build_state_input_removed",
            lambda value: value["LOCAL_INPUT_MANIFEST"].__setitem__(
                "inputs",
                [row for row in value["LOCAL_INPUT_MANIFEST"]["inputs"] if row["role"] != "BUILD_STATE_INPUT"],
            ),
            "INPUT_SET_MISMATCH",
        )
    return rows


def audit_start(start: dict[str, Any], root: Path) -> dict[str, Any]:
    root = root.resolve(strict=True)
    errors: list[str] = []
    blockers: list[str] = []
    if start.get("schema_version") != START_SCHEMA:
        errors.append(f"START_SCHEMA:{start.get('schema_version')}")
    if start.get("external_runtime_dependencies") != []:
        errors.append("START_EXTERNAL_RUNTIME_DEPENDENCIES_NOT_EMPTY")
    if start.get("network_required") is not False:
        errors.append("START_NETWORK_REQUIREMENT_NOT_FALSE")
    if start.get("compilation_permitted") is not False:
        errors.append("START_COMPILATION_PERMISSION_NOT_FALSE")

    contract_path = local_path(root, start.get("contract_relative_path"), "CONTRACT", errors)
    if contract_path is None or not contract_path.is_file():
        errors.append("START_CONTRACT_MISSING")
        contract: dict[str, Any] = {}
    else:
        contract = load_json(contract_path)
        if contract.get("schema_version") != CONTRACT_SCHEMA:
            errors.append(f"START_CONTRACT_SCHEMA:{contract.get('schema_version')}")

    readme_record = start.get("human_readme", {})
    readme_path = check_exact_file(
        root, readme_record, "README", errors, blockers, "HUMAN_README"
    ) if isinstance(readme_record, dict) else None
    if readme_path is not None:
        body = readme_path.read_text(encoding="utf-8")
        normalized_body = " ".join(body.split())
        for phrase in REQUIRED_HUMAN_PHRASES:
            if phrase not in normalized_body:
                errors.append("README_REQUIRED_CAUSAL_PHRASE_MISSING:" + phrase)
        for term in FORBIDDEN_HUMAN_TERMS:
            if term.casefold() in body.casefold():
                errors.append("README_FORBIDDEN_HUMAN_TERM_PRESENT:" + term)

    generation = start.get("coinductive_generation_policy", {})
    if generation.get("arbitrary_depth") is not True:
        errors.append("START_COINDUCTIVE_ARBITRARY_DEPTH_FALSE")
    if generation.get("finite_runs_are_witnesses_only") is not True:
        errors.append("START_FINITE_RUNS_PROMOTED_TO_SCOPE")
    if generation.get("phase_return_advances_memory") is not True:
        errors.append("START_PHASE_RETURN_MEMORY_ADVANCE_FALSE")
    if generation.get("distinguished_publications_not_scope_limit") != [
        "pi", "phi", "e", "alpha"
    ]:
        errors.append("START_DISTINGUISHED_PUBLICATIONS_SCOPE_INVALID")
    if generation.get("open_family_of_constants_and_realizations") is not True:
        errors.append("START_OPEN_PUBLICATION_FAMILY_FALSE")

    # Grafo completo local. La ruta y las huellas deben coincidir tanto con
    # START_HERE como con el contrato v2.
    graph_record = start.get("complete_inventory_graph", {})
    if not isinstance(graph_record, dict):
        errors.append("START_GRAPH_RECORD_INVALID")
        graph_record = {}
    graph_manifest_path = check_exact_file(
        root,
        {
            "candidate_relative_path": graph_record.get("manifest_relative_path"),
            "sha256": graph_record.get("manifest_sha256"),
        },
        "GRAPH_MANIFEST",
        errors,
        blockers,
        "COMPLETE_INVENTORY_GRAPH_FINAL",
    )
    graph_gate_path = check_exact_file(
        root,
        {
            "candidate_relative_path": graph_record.get("verifier_relative_path"),
            "sha256": graph_record.get("verifier_sha256"),
        },
        "GRAPH_VERIFIER",
        errors,
        blockers,
        "COMPLETE_INVENTORY_GRAPH_FINAL",
    )
    contract_graph = contract.get("candidate_complete_inventory_graph", {})
    expected_contract_graph = {
        "candidate_relative_path": graph_record.get("manifest_relative_path"),
        "sha256": graph_record.get("manifest_sha256"),
        "verifier_relative_path": graph_record.get("verifier_relative_path"),
        "verifier_sha256": graph_record.get("verifier_sha256"),
    }
    if not isinstance(contract_graph, dict) or any(
        contract_graph.get(key) != value for key, value in expected_contract_graph.items()
    ):
        errors.append("START_GRAPH_CONTRACT_BINDING_MISMATCH")

    graph_result: dict[str, Any] = {}
    if graph_manifest_path is not None and graph_gate_path is not None and contract:
        try:
            graph_manifest = load_json(graph_manifest_path)
            if graph_manifest.get("schema_version") != GRAPH_SCHEMA:
                errors.append(f"START_GRAPH_SCHEMA:{graph_manifest.get('schema_version')}")
            graph_gate = import_module(graph_gate_path, "hmt_root_complete_graph_gate")
            graph_result = graph_gate.validate_manifest(contract, graph_manifest, root)
        except Exception as exc:
            errors.append(f"START_GRAPH_EXECUTION_FAILED:{exc}")
        else:
            if not graph_result.get("structural_ok"):
                errors.extend(
                    "START_GRAPH:" + str(error)
                    for error in graph_result.get("errors", [])
                )
            if not graph_result.get("final_ready"):
                blockers.append("COMPLETE_INVENTORY_GRAPH_FINAL")
            metrics = graph_result.get("metrics", {})
            if any(metrics.get(key) != value for key, value in EXPECTED_METRICS.items()):
                errors.append("START_GRAPH_REQUIRED_METRICS_MISMATCH")
    if start.get("required_graph_metrics") != EXPECTED_METRICS:
        errors.append("START_REQUIRED_GRAPH_METRICS_WEAKENED")

    # Generador documental ya presente y portador Ext_TPK independiente.
    generators = start.get("generators", {})
    if not isinstance(generators, dict):
        errors.append("START_GENERATORS_NOT_OBJECT")
        generators = {}
    document_generator = generators.get("document_composition", {})
    if not isinstance(document_generator, dict):
        errors.append("START_DOCUMENT_GENERATOR_INVALID")
    else:
        check_exact_file(
            root, document_generator, "DOCUMENT_GENERATOR", errors, blockers,
            "DOCUMENT_COMPOSITION_GENERATOR",
        )
    ext_generator = generators.get("autonomous_ext_tpk", {})
    if not isinstance(ext_generator, dict):
        errors.append("START_EXT_GENERATOR_INVALID")
    else:
        ext_path = check_exact_file(
            root, ext_generator, "EXT_GENERATOR", errors, blockers,
            "EXT_TPK_AUTONOMOUS_GENERATOR",
        )
        if ext_generator.get("status") == "PASS" and ext_path is None:
            errors.append("START_EXT_GENERATOR_PREMATURE_PASS")
        if ext_generator.get("status") != "PASS":
            blockers.append("EXT_TPK_AUTONOMOUS_GENERATOR")

    # Doce familias de manifiestos/recibos. Un JSON STAGING sigue siendo un
    # artefacto legítimo de diagnóstico, pero no satisface el cierre exigido.
    receipt_rows = start.get("required_receipts", [])
    if not isinstance(receipt_rows, list):
        errors.append("START_RECEIPTS_NOT_LIST")
        receipt_rows = []
    receipt_ids = {
        row.get("receipt_id") for row in receipt_rows if isinstance(row, dict)
    }
    if receipt_ids != EXPECTED_RECEIPT_IDS or len(receipt_rows) != len(EXPECTED_RECEIPT_IDS):
        errors.append(
            "START_RECEIPT_IDS_INCOMPLETE:"
            f"missing={sorted(EXPECTED_RECEIPT_IDS-receipt_ids)}:"
            f"extra={sorted(receipt_ids-EXPECTED_RECEIPT_IDS)}"
        )
    receipt_payloads: dict[str, dict[str, Any]] = {}
    receipt_paths: dict[str, Path] = {}
    for row in receipt_rows:
        if not isinstance(row, dict):
            continue
        receipt_id = str(row.get("receipt_id", ""))
        blocker_id = "RECEIPT:" + receipt_id
        path = check_exact_file(root, row, blocker_id, errors, blockers, blocker_id)
        if path is None:
            continue
        if path.suffix.lower() != ".json":
            errors.append(f"{blocker_id}_NOT_JSON")
            blockers.append(blocker_id)
            continue
        try:
            payload = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{blocker_id}_INVALID_JSON:{exc}")
            blockers.append(blocker_id)
            continue
        receipt_payloads[receipt_id] = payload
        receipt_paths[receipt_id] = path
        expected_status = row.get("required_status")
        status_pointer = str(row.get("status_field", "status"))
        if payload.get(status_pointer) != expected_status:
            blockers.append(blocker_id)
        for flag in row.get("required_true_flags", []):
            if payload.get(flag) is not True:
                blockers.append(blocker_id)
        if receipt_id == "TERMINAL_INDEX":
            receipts = payload.get("receipts", [])
            if not isinstance(receipts, list) or len(receipts) != 5:
                errors.append("TERMINAL_INDEX_RECEIPT_COUNT_INVALID")
                blockers.append(blocker_id)
                continue
            seen = set()
            for terminal in receipts:
                result_id = terminal.get("result")
                if isinstance(result_id, str):
                    seen.add(result_id)
                relative = Path(str(terminal.get("file", "")))
                if relative.is_absolute() or ".." in relative.parts:
                    errors.append(f"TERMINAL_RECEIPT_PATH_UNSAFE:{result_id}")
                    blockers.append(blocker_id)
                    continue
                receipt_path = (path.parent / relative).resolve(strict=False)
                if not receipt_path.is_file():
                    errors.append(f"TERMINAL_RECEIPT_MISSING:{result_id}")
                    blockers.append(blocker_id)
                    continue
                expected_hash = terminal.get("sha256")
                if not is_hex64(expected_hash) or sha256(receipt_path) != expected_hash:
                    errors.append(f"TERMINAL_RECEIPT_HASH_MISMATCH:{result_id}")
                    blockers.append(blocker_id)
                    continue
                receipt = load_json(receipt_path)
                if receipt.get("status") != expected_status:
                    blockers.append(blocker_id)
                for flag in row.get("required_true_flags", []):
                    if receipt.get(flag) is not True:
                        blockers.append(blocker_id)
            if seen != {"RH", "NS", "YM", "Hodge", "BSD"}:
                errors.append("TERMINAL_INDEX_RESULT_SET_INVALID")
                blockers.append(blocker_id)

    # Tres y solo tres ternas PDF/FLS/log dentro de la raíz.
    bundles = start.get("output_bundles", [])
    if not isinstance(bundles, list):
        errors.append("START_OUTPUT_BUNDLES_NOT_LIST")
        bundles = []
    bundle_ids = {row.get("bundle_id") for row in bundles if isinstance(row, dict)}
    if bundle_ids != EXPECTED_OUTPUT_BUNDLES or len(bundles) != 3:
        errors.append(
            "START_OUTPUT_BUNDLE_IDS_INCOMPLETE:"
            f"missing={sorted(EXPECTED_OUTPUT_BUNDLES-bundle_ids)}:"
            f"extra={sorted(bundle_ids-EXPECTED_OUTPUT_BUNDLES)}"
        )
    bundle_files: dict[str, dict[str, Path]] = {}
    for bundle in bundles:
        if not isinstance(bundle, dict):
            continue
        bundle_id = str(bundle.get("bundle_id", ""))
        bundle_blocker = "OUTPUT_BUNDLE:" + bundle_id
        artifacts = bundle.get("artifacts", {})
        if not isinstance(artifacts, dict) or set(artifacts) != {"pdf", "fls", "log"}:
            errors.append(f"{bundle_blocker}_ARTIFACT_SET_INVALID")
            blockers.append(bundle_blocker)
            continue
        complete = True
        verified: dict[str, Path] = {}
        for kind in ("pdf", "fls", "log"):
            record = artifacts.get(kind, {})
            if not isinstance(record, dict):
                errors.append(f"{bundle_blocker}_{kind.upper()}_RECORD_INVALID")
                complete = False
                continue
            path = check_exact_file(
                root, record, f"{bundle_blocker}_{kind.upper()}", errors,
                blockers, bundle_blocker,
            )
            complete = complete and path is not None
            if path is not None:
                verified[kind] = path
            if record.get("sha256") in PREDECESSOR_PDF_HASHES:
                errors.append(f"PREDECESSOR_HASH_USED_AS_SUCCESSOR:{bundle_id}:{kind}")
                complete = False
        if not complete:
            blockers.append(bundle_blocker)
        bundle_files[bundle_id] = verified

    # En cuanto cualquier componente intenta declararse final, las ternas,
    # sus entrypoints y todos los INPUT no sistémicos de sus FLS se validan
    # como una única clausura material. Un manifiesto vacío nunca autoriza la
    # promoción aunque tenga estado y huella formalmente correctos.
    validate_successor_closure(
        start, contract, root, receipt_payloads, receipt_paths,
        bundle_files, errors, blockers,
    )

    for pending in contract.get("pending_admission_groups", []):
        if isinstance(pending, str) and pending:
            blockers.append("CONTRACT_PENDING:" + pending)
    if contract.get("status") != FINAL:
        blockers.append("CONTRACT_FINAL_READY")

    blockers = sorted(set(blockers))
    declared = start.get("declared_blocker_ids", [])
    if not isinstance(declared, list) or sorted(set(declared)) != blockers or len(declared) != len(set(declared)):
        errors.append(
            "START_DECLARED_BLOCKERS_MISMATCH:"
            f"missing={sorted(set(blockers)-set(declared if isinstance(declared, list) else []))}:"
            f"extra={sorted(set(declared if isinstance(declared, list) else [])-set(blockers))}"
        )

    if blockers:
        if start.get("status") != STAGING:
            errors.append(f"START_PREMATURE_STATUS:{start.get('status')}")
        if start.get("promotion_allowed") is not False:
            errors.append("START_PREMATURE_PROMOTION")
    else:
        if start.get("status") != FINAL:
            errors.append(f"START_NOT_FINAL:{start.get('status')}")
        if start.get("promotion_allowed") is not True:
            errors.append("START_FINAL_PROMOTION_FALSE")

    integrity_ok = not errors
    final_ready = integrity_ok and not blockers and start.get("status") == FINAL
    return {
        "schema_version": "hmt-autonomous-root-entry-audit-v1",
        "status": (
            "PASS_START_HERE_HMT_MD_FINAL_READY"
            if final_ready else
            "PASS_START_HERE_HMT_MD_STAGING_LOCKED"
            if integrity_ok else
            "FAIL_START_HERE_HMT_MD_INTEGRITY"
        ),
        "integrity_ok": integrity_ok,
        "final_ready": final_ready,
        "promotion_allowed": final_ready,
        "errors": errors,
        "blockers": blockers,
        "graph_status": graph_result.get("status"),
        "graph_metrics": graph_result.get("metrics", {}),
    }


def run_self_test(start: dict[str, Any], root: Path) -> tuple[bool, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    baseline = audit_start(start, root)
    baseline_is_final = baseline["integrity_ok"] and baseline["final_ready"]
    rows.append({
        "name": "positive_final_ready" if baseline_is_final else "positive_staging_lock",
        "passed": baseline["integrity_ok"],
        "errors": baseline["errors"],
    })
    attacks: list[tuple[str, Any, str]] = [
        (
            "scientific_count_weakened",
            lambda value: value["required_graph_metrics"].__setitem__("scientific_nodes", 14174),
            "START_REQUIRED_GRAPH_METRICS_WEAKENED",
        ),
        (
            "graph_hash_changed",
            lambda value: value["complete_inventory_graph"].__setitem__("manifest_sha256", "0" * 64),
            "GRAPH_MANIFEST_HASH_MISMATCH",
        ),
        (
            "output_bundle_removed",
            lambda value: value["output_bundles"].pop(),
            "START_OUTPUT_BUNDLE_IDS_INCOMPLETE",
        ),
        (
            "receipt_family_removed",
            lambda value: value["required_receipts"].pop(),
            "START_RECEIPT_IDS_INCOMPLETE",
        ),
    ]
    if baseline_is_final:
        # Tras el sellado, los ataques de staging deben alterar realmente el
        # estado FINAL. Volver a escribir PASS/FINAL o quitar un blocker ya
        # ausente no constituye un red-team y producía falsos negativos.
        attacks.extend([
            (
                "ext_generator_hash_changed",
                lambda value: value["generators"]["autonomous_ext_tpk"].__setitem__(
                    "sha256", "0" * 64
                ),
                "EXT_GENERATOR_HASH_MISMATCH",
            ),
            (
                "terminal_receipt_hash_changed",
                lambda value: next(
                    row for row in value["required_receipts"]
                    if row.get("receipt_id") == "TERMINAL_INDEX"
                ).__setitem__("sha256", "0" * 64),
                "RECEIPT:TERMINAL_INDEX_HASH_MISMATCH",
            ),
            (
                "final_status_demoted",
                lambda value: (
                    value.__setitem__("status", STAGING),
                    value.__setitem__("promotion_allowed", False),
                ),
                "START_NOT_FINAL",
            ),
        ])
    else:
        attacks.extend([
            (
                "ext_stub_promoted",
                lambda value: value["generators"]["autonomous_ext_tpk"].__setitem__(
                    "status", "PASS"
                ),
                "START_EXT_GENERATOR_PREMATURE_PASS",
            ),
            (
                "terminal_blocker_hidden",
                lambda value: value.__setitem__(
                    "declared_blocker_ids",
                    [
                        item for item in value["declared_blocker_ids"]
                        if item != "RECEIPT:TERMINAL_INDEX"
                    ],
                ),
                "START_DECLARED_BLOCKERS_MISMATCH",
            ),
            (
                "premature_final_ready",
                lambda value: (
                    value.__setitem__("status", FINAL),
                    value.__setitem__("promotion_allowed", True),
                ),
                "START_PREMATURE_STATUS",
            ),
        ])
    for name, mutate, expected in attacks:
        attacked = copy.deepcopy(start)
        mutate(attacked)
        result = audit_start(attacked, root)
        rows.append({
            "name": name,
            "passed": not result["integrity_ok"] and any(
                expected in error for error in result["errors"]
            ),
            "errors": result["errors"],
        })
    rows.extend(run_successor_closure_redteams())
    return all(row["passed"] for row in rows), rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=Path, default=DEFAULT_START)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check-staging", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    start = load_json(args.start)
    if args.self_test:
        passed, rows = run_self_test(start, args.root)
        for row in rows:
            print(("PASS" if row["passed"] else "FAIL") + "_START_REDTEAM_" + row["name"].upper())
            if not row["passed"]:
                for error in row["errors"]:
                    print(error)
        if not passed:
            print("FAIL_START_HERE_HMT_MD_SELF_TEST")
            return 1
        print(
            f"PASS_START_HERE_HMT_MD_SELF_TEST tests={len(rows)} "
            "state_aware=staging_or_final"
        )
        return 0

    result = audit_start(start, args.root)
    print(result["status"])
    print(
        "START_GRAPH_COUNTS "
        f"scientific={result['graph_metrics'].get('scientific_nodes')} "
        f"active={result['graph_metrics'].get('active_nodes')} "
        f"api_chunks={result['graph_metrics'].get('api_chunk_nodes')} "
        f"sentinels={result['graph_metrics'].get('claim_nodes')} "
        f"formal_claims={result['graph_metrics'].get('full_registry_claim_nodes')} "
        f"evidence={result['graph_metrics'].get('full_registry_evidence_nodes')} "
        f"causal_edges={result['graph_metrics'].get('full_registry_causal_edges')} "
        f"owners={result['graph_metrics'].get('material_owner_nodes')} "
        f"views={result['graph_metrics'].get('view_nodes')} "
        f"evals={result['graph_metrics'].get('eval_nodes')}"
    )
    for error in result["errors"]:
        print(error)
    if args.check_staging:
        return 0 if result["integrity_ok"] and not result["final_ready"] else 1
    if not result["final_ready"]:
        print(f"FAIL_START_HERE_HMT_MD_STAGING_BLOCKED blockers={len(result['blockers'])}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL_START_HERE_HMT_MD:{exc}", file=sys.stderr)
        raise SystemExit(1)
