#!/usr/bin/env python3
"""Resuelve las capas materiales vivas de HMT--MD.

La autoridad de partida no es una revisión nominal. Se compone de:

1. el último artefacto HMT--MD global, sellado y verificado, cualquiera que
   sea su raíz documental;
2. la última edición integral verificada, que conserva la cobertura del
   tratado completo.

Ambas capas se resuelven por estados y manifiestos materiales. Las revisiones
REV.1/REV.3/REV.4 y demás predecesoras sólo pueden reaparecer como testigos de
procedencia, nunca como ``fallback``.

Los ámbitos con una publicación especializada posterior se añaden como capas
tipadas. No sustituyen ni la autoridad global ni la edición integral. La capa
de masas se deriva del certificado final de la monografía activa y conserva el
paquete rector sellado como testigo de no regresión.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HMT2_ROOT = Path("/Users/ruben/Documents/HMT2")
SEARCH_ROOTS = (
    HMT2_ROOT,
    Path("/Users/ruben/Documents/New project"),
    Path("/Users/ruben/Documents/excelencia academica"),
)
SNAPSHOT = HMT2_ROOT / "CONTINUIDAD_EDITORIAL" / "ULTIMA_AUTORIDAD_HMT_MD.json"
OLD_AUTHORITY_TOKENS = ("REV_1", "REV1", "REV_3", "REV3", "REV_4", "REV4")
ARCHIVE_ROOT_PREFIXES = (
    "CORPUS_DIGITAL_RECTOR_HMT_MD_",
    "PAQUETE_PROBATORIO_COMUN_AUTONOMO_HMT_MD_",
    "PAQUETE_DEMOSTRATIVO_AUTONOMO_HMT_MD_",
    "PAQUETE_DEMOSTRATIVO_HMT_MD_AISLADO_",
    # Distribuciones francesas autocontenidas: copias de procedencia, no autoridades.
    "EDITION_FR_HMT_",
)


def is_archival_copy(path: Path) -> bool:
    """Impide que una recopilación autocontenida compita con su autoridad viva."""
    return any(
        any(part.startswith(prefix) for prefix in ARCHIVE_ROOT_PREFIXES)
        for part in path.parts
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def absolute(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def inside(root: Path, path: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (FileNotFoundError, ValueError):
        return False
    return True


def parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def time_text(value: dt.datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def score(time: dt.datetime | None, primary: Path, secondary: Path) -> tuple[int, int, int]:
    """Devuelve siempre enteros; evita comparar datetime, str, float e int."""
    epoch_ns = int(time.timestamp() * 1_000_000_000) if time is not None else 0
    return (epoch_ns, primary.stat().st_mtime_ns, secondary.stat().st_mtime_ns)


SHA_LINE = re.compile(r"^([0-9a-f]{64})  (.+)$")


def verify_sha_manifest(root: Path, manifest: Path) -> set[str] | None:
    if not manifest.is_file() or not inside(root, manifest):
        return None
    members: set[str] = set()
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        if not raw:
            continue
        match = SHA_LINE.fullmatch(raw)
        if match is None:
            return None
        expected, relative = match.groups()
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            return None
        member = root / rel
        if not member.is_file() or not inside(root, member) or sha256(member) != expected:
            return None
        members.add(relative)
    return members


@dataclass(frozen=True)
class IntegralCandidate:
    root: Path
    source_main: Path
    state: Path
    status_file: Path
    material_status: str
    pdf: Path
    pdf_sha256: str
    pages: int
    receipt: Path
    manuscript_manifest: Path
    delivery_manifest: Path
    qa: Path
    build_time: dt.datetime | None


@dataclass(frozen=True)
class SealedCandidate:
    root: Path
    source_main: Path
    manifest: Path
    manifest_status: str
    artifact_id: str
    title: str
    pdf: Path
    pdf_sha256: str
    pages: int
    receipt: Path
    manuscript_manifest: Path | None
    build_time: dt.datetime | None


@dataclass(frozen=True)
class MassSpecializedCandidate:
    root: Path
    certificate: Path
    status: str
    title: str
    pdf: Path
    pdf_sha256: str
    pages: int
    source: Path
    source_sha256: str
    preservation_receipt: Path
    scientific_receipt: Path
    result_matrix: Path
    proof_matrix: Path
    approved_canvas: Path
    join_certificate: Path
    qa: Path
    build_time: dt.datetime | None


@dataclass(frozen=True)
class MassNonRegressionWitness:
    root: Path
    descriptor: Path
    status: str
    package_id: str
    result: Path
    contract: Path
    matrix: Path
    certificate: Path
    sha256sums: Path
    gate: Path


def integral_state_paths() -> list[Path]:
    return sorted(
        path
        for path in HMT2_ROOT.glob("**/gestion/ESTADO_EDICION_*.json")
        if not is_archival_copy(path)
    )


def parse_integral(path: Path) -> IntegralCandidate | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if path.parent.name != "gestion":
        return None
    root = path.parent.parent
    artifact_id = payload.get("artifact_id")
    if not isinstance(artifact_id, str) or not artifact_id.startswith(
        "EL-CIERRE-HOLOGRAFICO-INFINITO"
    ):
        return None
    material_status = payload.get("status")
    if material_status not in {
        "COMPILED_AND_VERIFIED",
        "FINAL_PDF_AND_PACKAGES_BUILT_AND_VERIFIED",
        "FINAL_PDF_BUILT_QA_PASSED_AND_PACKAGED",
    }:
        return None
    pdf_spec = payload.get("pdf")
    if not isinstance(pdf_spec, dict):
        return None
    pdf_value = pdf_spec.get("path")
    expected = pdf_spec.get("sha256")
    pages = pdf_spec.get("pages")
    expected_bytes = pdf_spec.get("bytes")
    if not isinstance(pdf_value, str) or not isinstance(expected, str) or not isinstance(pages, int):
        return None
    pdf = absolute(root, pdf_value)
    if (
        not pdf.is_file()
        or pdf.read_bytes()[:5] != b"%PDF-"
        or sha256(pdf) != expected
        or (isinstance(expected_bytes, int) and pdf.stat().st_size != expected_bytes)
    ):
        return None
    # El entrypoint pertenece al estado material de cada edición. Las
    # autoridades históricas que no declaraban ``source`` conservan como
    # fallback ``manuscrito/main.tex``; una edición sucesora puede publicar un
    # entrypoint distinto sin falsear su procedencia compilada.
    source_spec = payload.get("source")
    source_value = "manuscrito/main.tex"
    source_expected: str | None = None
    if isinstance(source_spec, dict):
        declared_source = source_spec.get("path")
        declared_source_sha = source_spec.get("sha256")
        if declared_source is not None and not isinstance(declared_source, str):
            return None
        if declared_source_sha is not None and not isinstance(declared_source_sha, str):
            return None
        if isinstance(declared_source, str):
            source_value = declared_source
        if isinstance(declared_source_sha, str):
            source_expected = declared_source_sha
    source_main = absolute(root, source_value)
    if (
        not source_main.is_file()
        or not inside(root, source_main)
        or (source_expected is not None and sha256(source_main) != source_expected)
    ):
        return None
    source_entrypoint = source_main.relative_to(root).as_posix()

    precompile = payload.get("precompile")
    if not isinstance(precompile, dict) or not isinstance(precompile.get("receipt_path"), str):
        return None
    receipt = absolute(root, precompile["receipt_path"])
    receipt_sha = precompile.get("receipt_sha256")
    if not receipt.is_file() or not isinstance(receipt_sha, str) or sha256(receipt) != receipt_sha:
        return None
    try:
        receipt_payload = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if receipt_payload.get("status") != "PASS_HMT_MD_PRECOMPILE":
        return None
    # Las ediciones recientes declaran el manifiesto del manuscrito dentro del
    # propio recibo y pueden emplear nomenclatura pública en castellano.  La
    # ruta declarada y su huella son la autoridad; el glob histórico queda
    # únicamente como compatibilidad con expedientes anteriores.
    manuscript_manifest: Path | None = None
    ledgers = receipt_payload.get("editorial_ledgers")
    if isinstance(ledgers, dict):
        manuscript_spec = ledgers.get("manuscript_manifest")
        if isinstance(manuscript_spec, dict):
            manifest_value = manuscript_spec.get("path")
            manifest_sha = manuscript_spec.get("sha256")
            if isinstance(manifest_value, str) and isinstance(manifest_sha, str):
                declared_manifest = Path(manifest_value)
                if (
                    declared_manifest.is_file()
                    and inside(root, declared_manifest)
                    and sha256(declared_manifest) == manifest_sha
                ):
                    manuscript_manifest = declared_manifest
    if manuscript_manifest is None:
        manuscript_manifests = sorted(receipt.parent.glob("manuscript_manifest*.json"))
        if len(manuscript_manifests) != 1:
            return None
        manuscript_manifest = manuscript_manifests[0]

    status_file: Path | None = None
    qa: Path | None = None
    for candidate in sorted(root.glob("STATUS*.json")):
        try:
            status_payload = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        publication = status_payload.get("publication")
        visual_qa = status_payload.get("visual_qa")
        pre = status_payload.get("precompile")
        if not isinstance(publication, dict) or not isinstance(visual_qa, dict) or not isinstance(pre, dict):
            continue
        if (
            status_payload.get("title") != "El cierre holográfico del infinito"
            or publication.get("sha256") != expected
            or publication.get("pages") != pages
            or status_payload.get("entrypoint") != source_entrypoint
            or status_payload.get("entrypoint_sha256") != sha256(source_main)
            or pre.get("status") != "PASS_HMT_MD_PRECOMPILE"
            or pre.get("receipt_sha256") != receipt_sha
            or not str(visual_qa.get("status", "")).startswith("PASS")
        ):
            continue
        qa_value = visual_qa.get("report")
        qa_sha = visual_qa.get("report_sha256")
        if not isinstance(qa_value, str) or not isinstance(qa_sha, str):
            continue
        qa_candidate = absolute(root, qa_value)
        if not qa_candidate.is_file() or sha256(qa_candidate) != qa_sha:
            continue
        status_file, qa = candidate, qa_candidate
        break
    if status_file is None or qa is None:
        # Las ediciones integrales reforzadas publican su estado material en
        # ``gestion/ESTADO_EDICION_*.json`` y no duplican necesariamente ese
        # mismo contenido en un ``STATUS*.json`` de raíz. En ese esquema el
        # propio estado es el descriptor de autoridad. El informe visual se
        # acepta sólo si está dentro de la edición y declara la huella exacta
        # del PDF; más abajo el manifiesto de entrega deberá sellarlo también.
        qa_candidates = sorted(root.glob("qa/QA*.md")) + sorted(
            root.glob("gestion/QA*.md")
        )
        for qa_candidate in qa_candidates:
            try:
                qa_text = qa_candidate.read_text(encoding="utf-8")
            except OSError:
                continue
            if inside(root, qa_candidate) and expected in qa_text:
                status_file, qa = path, qa_candidate
                break
    if status_file is None or qa is None:
        return None

    required = {
        str(pdf.relative_to(root)),
        str(path.relative_to(root)),
        str(receipt.relative_to(root)),
        str(qa.relative_to(root)),
    }
    delivery_manifest: Path | None = None
    for candidate in sorted(root.glob("gestion/MANIFIESTO_ENTREGA*.sha256")):
        members = verify_sha_manifest(root, candidate)
        if members is not None and required <= members:
            delivery_manifest = candidate
            break
    if delivery_manifest is None:
        return None
    return IntegralCandidate(
        root=root,
        source_main=source_main,
        state=path,
        status_file=status_file,
        material_status=str(material_status),
        pdf=pdf,
        pdf_sha256=expected,
        pages=pages,
        receipt=receipt,
        manuscript_manifest=manuscript_manifest,
        delivery_manifest=delivery_manifest,
        qa=qa,
        build_time=parse_time(receipt_payload.get("timestamp_utc")),
    )


def sealed_manifest_paths() -> list[Path]:
    paths: set[Path] = set()
    for root in SEARCH_ROOTS:
        paths.update(root.glob("**/gestion/MANIFIESTO_ARTEFACTO_FINAL.json"))
    return sorted(path for path in paths if not is_archival_copy(path))


def parse_sealed(path: Path) -> SealedCandidate | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if payload.get("schema_version") != "hmt-final-artifact-manifest-v1":
        return None
    manifest_status = payload.get("status")
    artifact_id = payload.get("artifact_id")
    title = payload.get("title")
    if (
        not isinstance(manifest_status, str)
        or not manifest_status.startswith("SEALED_")
        or not isinstance(artifact_id, str)
        or not isinstance(title, str)
    ):
        return None
    root = path.parent.parent
    pdf_spec = payload.get("pdf")
    precompile = payload.get("precompile")
    if not isinstance(pdf_spec, dict) or not isinstance(precompile, dict):
        return None
    pdf_value = pdf_spec.get("path")
    expected = pdf_spec.get("sha256")
    pages = pdf_spec.get("pages")
    expected_bytes = pdf_spec.get("bytes")
    if not isinstance(pdf_value, str) or not isinstance(expected, str) or not isinstance(pages, int):
        return None
    pdf = absolute(root, pdf_value)
    if (
        not pdf.is_file()
        or pdf.read_bytes()[:5] != b"%PDF-"
        or sha256(pdf) != expected
        or (isinstance(expected_bytes, int) and pdf.stat().st_size != expected_bytes)
    ):
        return None
    receipt_value = precompile.get("receipt_path")
    receipt_sha = precompile.get("receipt_sha256")
    if not isinstance(receipt_value, str) or not isinstance(receipt_sha, str):
        return None
    receipt = absolute(root, receipt_value)
    if not receipt.is_file() or sha256(receipt) != receipt_sha:
        return None
    try:
        receipt_payload = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if receipt_payload.get("status") != "PASS_HMT_MD_PRECOMPILE":
        return None
    artifact = receipt_payload.get("artifact")
    receipt_artifact_id = artifact.get("id") if isinstance(artifact, dict) else None
    declared_receipt_artifact_id = precompile.get("receipt_artifact_id")
    if not isinstance(artifact, dict) or (
        receipt_artifact_id != artifact_id
        and declared_receipt_artifact_id != receipt_artifact_id
    ):
        return None
    source_value = artifact.get("entrypoint")
    if not isinstance(source_value, str):
        return None
    source_main = Path(source_value)
    if not source_main.is_file() or not inside(root, source_main):
        return None

    # El manifiesto final sella cada entrada declarada; cualquier deriva invalida
    # el candidato, incluida la del PDF o del recibo.
    sealed_inputs = payload.get("sealed_inputs")
    if not isinstance(sealed_inputs, list) or not sealed_inputs:
        return None
    for entry in sealed_inputs:
        if not isinstance(entry, dict):
            return None
        value, declared = entry.get("path"), entry.get("sha256")
        if not isinstance(value, str) or not isinstance(declared, str):
            return None
        member = absolute(root, value)
        if not member.is_file() or not inside(root, member) or sha256(member) != declared:
            return None

    manuscript_manifest: Path | None = None
    ledgers = receipt_payload.get("editorial_ledgers")
    if isinstance(ledgers, dict):
        manuscript = ledgers.get("manuscript_manifest")
        if isinstance(manuscript, dict) and isinstance(manuscript.get("path"), str):
            candidate = Path(manuscript["path"])
            declared = manuscript.get("sha256")
            if candidate.is_file() and isinstance(declared, str) and sha256(candidate) == declared:
                manuscript_manifest = candidate
    created = parse_time(payload.get("created_at")) or parse_time(receipt_payload.get("timestamp_utc"))
    return SealedCandidate(
        root=root,
        source_main=source_main,
        manifest=path,
        manifest_status=manifest_status,
        artifact_id=artifact_id,
        title=title,
        pdf=pdf,
        pdf_sha256=expected,
        pages=pages,
        receipt=receipt,
        manuscript_manifest=manuscript_manifest,
        build_time=created,
    )


def mass_delivery_certificate_paths() -> list[Path]:
    paths: set[Path] = set()
    for root in SEARCH_ROOTS:
        paths.update(root.glob("**/gestion/CERTIFICADO_ENTREGA_PDF_REV*.json"))
    return sorted(path for path in paths if not is_archival_copy(path))


def parse_mass_specialized(path: Path) -> MassSpecializedCandidate | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        payload.get("schema") != "HMT_MD_MASS_MONOGRAPH_FINAL_DELIVERY_V1"
        or payload.get("status") != "PASS_ENTREGA_PDF_MASAS_REV2"
        or path.parent.name != "gestion"
    ):
        return None
    root = path.parent.parent
    if not inside(root, path):
        return None

    artifact = payload.get("artifact")
    preservation = payload.get("preservation")
    scientific = payload.get("scientific_preflight")
    domain = payload.get("mass_domain")
    layout = payload.get("layout_qa")
    if not all(isinstance(item, dict) for item in (artifact, preservation, scientific, domain, layout)):
        return None

    title = artifact.get("title")
    pdf_value, pdf_sha, pages = artifact.get("pdf"), artifact.get("sha256"), artifact.get("physical_pages")
    source_value, source_sha = artifact.get("source"), artifact.get("source_sha256")
    if not all(isinstance(item, str) for item in (title, pdf_value, pdf_sha, source_value, source_sha)):
        return None
    if not isinstance(pages, int):
        return None
    pdf, source = Path(pdf_value), Path(source_value)
    if (
        not pdf.is_file()
        or not source.is_file()
        or not inside(root, pdf)
        or not inside(root, source)
        or pdf.read_bytes()[:5] != b"%PDF-"
        or sha256(pdf) != pdf_sha
        or sha256(source) != source_sha
    ):
        return None

    def bound(relative: Any, declared: Any) -> Path | None:
        if not isinstance(relative, str) or not isinstance(declared, str):
            return None
        candidate = absolute(root, relative)
        if not candidate.is_file() or not inside(root, candidate) or sha256(candidate) != declared:
            return None
        return candidate

    preservation_receipt = bound(preservation.get("receipt"), preservation.get("receipt_sha256"))
    scientific_receipt = bound(scientific.get("receipt"), scientific.get("receipt_sha256"))
    join_certificate = bound(domain.get("join_certificate"), domain.get("join_certificate_sha256"))
    qa = bound(layout.get("report"), layout.get("report_sha256"))
    result_matrix = root / "gestion" / "MATRIZ_RESULTADOS_RECTORES.tsv"
    proof_matrix = root / "gestion" / "MATRIZ_RECTORA_PUENTE_FISICO.json"
    approved_canvas = root / "gestion" / "LIENZO_APROBADO_PUENTE_FISICO.json"
    if (
        preservation_receipt is None
        or scientific_receipt is None
        or join_certificate is None
        or qa is None
        or not result_matrix.is_file()
        or not proof_matrix.is_file()
        or not approved_canvas.is_file()
        or not inside(root, result_matrix)
        or not inside(root, proof_matrix)
        or not inside(root, approved_canvas)
        or sha256(result_matrix) != scientific.get("matrix_sha256")
        or scientific.get("status") != "PASS_HMT_MD_PRECOMPILE"
        or scientific.get("results") != 61
        or scientific.get("five_continuum_constructions")
        != "PASS_NO_DISGREGACION_CINCO_CONSTRUCCIONES_CONTINUO"
        or layout.get("status") != "PASS_MAQUETACION_PDF_MASAS_REV2"
        or preservation.get("route_cards") != 324
        or preservation.get("mass_inventory_rows") != 471
        or preservation.get("width_inventory_rows") != 384
        or preservation.get("reconstruction") != "BYTE_IDENTICAL"
        or domain.get("cells") != 81
        or domain.get("route_families") != 56
        or domain.get("multisections") != 13
        or domain.get("oriented_routes") != 324
    ):
        return None

    try:
        scientific_payload = json.loads(scientific_receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    ledgers = scientific_payload.get("editorial_ledgers")
    if not isinstance(ledgers, dict):
        return None
    proof_spec, canvas_spec = ledgers.get("matrix"), ledgers.get("canvas")
    if not isinstance(proof_spec, dict) or not isinstance(canvas_spec, dict):
        return None
    if (
        Path(str(proof_spec.get("path", ""))).resolve() != proof_matrix.resolve()
        or proof_spec.get("sha256") != sha256(proof_matrix)
        or Path(str(canvas_spec.get("path", ""))).resolve() != approved_canvas.resolve()
        or canvas_spec.get("sha256") != sha256(approved_canvas)
        or ledgers.get("results") != 61
    ):
        return None

    return MassSpecializedCandidate(
        root=root,
        certificate=path,
        status=str(payload["status"]),
        title=str(title),
        pdf=pdf,
        pdf_sha256=str(pdf_sha),
        pages=pages,
        source=source,
        source_sha256=str(source_sha),
        preservation_receipt=preservation_receipt,
        scientific_receipt=scientific_receipt,
        result_matrix=result_matrix,
        proof_matrix=proof_matrix,
        approved_canvas=approved_canvas,
        join_certificate=join_certificate,
        qa=qa,
        build_time=parse_time(payload.get("timestamp")),
    )


def mass_witness_descriptor_paths() -> list[Path]:
    paths: set[Path] = set()
    for root in SEARCH_ROOTS:
        paths.update(root.glob("**/CURRENT.json"))
    return sorted(path for path in paths if not is_archival_copy(path))


def parse_mass_witness(path: Path) -> MassNonRegressionWitness | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        payload.get("schema") != "HMTMD.mass_law_focal_authority.v1"
        or payload.get("status") != "SEALED_FOCAL_AUTHORITY"
        or not isinstance(payload.get("package_id"), str)
    ):
        return None
    root = path.parent
    # A self-contained dossier may legitimately carry a byte-identical copy of
    # the focal mass-law package.  Such a copy is evidence, not a second living
    # authority.  The canonical package publishes its stable ``package_id`` as
    # the directory name; copied descriptors under generic ``masas`` or
    # evidence directories must therefore be excluded from authority counting.
    if root.name != payload["package_id"]:
        return None
    required = {
        "result": root / "RESULTADO_RECTOR.md",
        "contract": root / "CONTRATO_NO_REGRESION.md",
        "matrix": root / "MATRIZ_RECTORA.tsv",
        "certificate": root / "certificados" / "paquete_rector.json",
        "sha256sums": root / "SHA256SUMS",
        "gate": root / "pruebas" / "verificar_paquete_rector.py",
    }
    if not inside(root, path) or any(not inside(root, member) for member in required.values()):
        return None
    return MassNonRegressionWitness(
        root=root,
        descriptor=path,
        status=str(payload["status"]),
        package_id=str(payload["package_id"]),
        result=required["result"],
        contract=required["contract"],
        matrix=required["matrix"],
        certificate=required["certificate"],
        sha256sums=required["sha256sums"],
        gate=required["gate"],
    )


def resolve_integral() -> IntegralCandidate:
    candidates = [candidate for path in integral_state_paths() if (candidate := parse_integral(path))]
    if not candidates:
        raise SystemExit("FAIL_ULTIMA_AUTORIDAD_HMT_MD no_verified_integral_candidate")
    return max(candidates, key=lambda item: score(item.build_time, item.pdf, item.state))


def resolve_sealed() -> SealedCandidate:
    candidates = [candidate for path in sealed_manifest_paths() if (candidate := parse_sealed(path))]
    if not candidates:
        raise SystemExit("FAIL_ULTIMA_AUTORIDAD_HMT_MD no_verified_global_sealed_candidate")
    return max(candidates, key=lambda item: score(item.build_time, item.pdf, item.manifest))


def resolve_mass_specialized() -> MassSpecializedCandidate:
    candidates = [
        candidate
        for path in mass_delivery_certificate_paths()
        if (candidate := parse_mass_specialized(path))
    ]
    if not candidates:
        raise SystemExit("FAIL_ULTIMA_AUTORIDAD_HMT_MD no_verified_mass_specialized_candidate")
    return max(candidates, key=lambda item: score(item.build_time, item.pdf, item.certificate))


def resolve_mass_witness() -> MassNonRegressionWitness:
    candidates = [
        candidate
        for path in mass_witness_descriptor_paths()
        if (candidate := parse_mass_witness(path))
    ]
    if len(candidates) != 1:
        raise SystemExit(
            "FAIL_ULTIMA_AUTORIDAD_HMT_MD expected_one_mass_non_regression_witness"
        )
    return candidates[0]


def integral_payload(candidate: IntegralCandidate) -> dict[str, Any]:
    return {
        "role": "LATEST_INTEGRAL_EDITION",
        "authority_root": str(candidate.root),
        "source_main": str(candidate.source_main),
        "source_main_sha256": sha256(candidate.source_main),
        "state": str(candidate.state),
        "state_sha256": sha256(candidate.state),
        "authority_status": str(candidate.status_file),
        "authority_status_sha256": sha256(candidate.status_file),
        "material_status": candidate.material_status,
        "pdf": str(candidate.pdf),
        "pdf_sha256": candidate.pdf_sha256,
        "pdf_pages": candidate.pages,
        "pdf_mtime_ns": candidate.pdf.stat().st_mtime_ns,
        "build_time_utc": time_text(candidate.build_time),
        "precompile_receipt": str(candidate.receipt),
        "precompile_receipt_sha256": sha256(candidate.receipt),
        "manuscript_manifest": str(candidate.manuscript_manifest),
        "manuscript_manifest_sha256": sha256(candidate.manuscript_manifest),
        "delivery_manifest": str(candidate.delivery_manifest),
        "delivery_manifest_sha256": sha256(candidate.delivery_manifest),
        "qa": str(candidate.qa),
        "qa_sha256": sha256(candidate.qa),
        "publication_ready": True,
    }


def sealed_payload(candidate: SealedCandidate) -> dict[str, Any]:
    return {
        "role": "LATEST_GLOBAL_SEALED_ARTIFACT",
        "artifact_id": candidate.artifact_id,
        "title": candidate.title,
        "authority_root": str(candidate.root),
        "source_main": str(candidate.source_main),
        "source_main_sha256": sha256(candidate.source_main),
        "artifact_manifest": str(candidate.manifest),
        "artifact_manifest_sha256": sha256(candidate.manifest),
        "material_status": candidate.manifest_status,
        "pdf": str(candidate.pdf),
        "pdf_sha256": candidate.pdf_sha256,
        "pdf_pages": candidate.pages,
        "pdf_mtime_ns": candidate.pdf.stat().st_mtime_ns,
        "build_time_utc": time_text(candidate.build_time),
        "precompile_receipt": str(candidate.receipt),
        "precompile_receipt_sha256": sha256(candidate.receipt),
        "manuscript_manifest": str(candidate.manuscript_manifest) if candidate.manuscript_manifest else None,
        "manuscript_manifest_sha256": sha256(candidate.manuscript_manifest) if candidate.manuscript_manifest else None,
        "publication_ready": True,
    }


def mass_specialized_payload(
    candidate: MassSpecializedCandidate,
    witness: MassNonRegressionWitness,
) -> dict[str, Any]:
    return {
        "role": "LATEST_SPECIALIZED_MASS_LAW_ARTIFACT",
        "scope": "MASS_LAW_ONLY",
        "artifact_id": "TEORIA-HOLOGRAFICA-INTEGRAL-MASA-HMT-MD-REV2-20260820",
        "relationship_to_integral": "POSTERIOR_SPECIALIZED_DELTA_DOES_NOT_REPLACE_INTEGRAL",
        "publication_ready": True,
        "authority_root": str(candidate.root),
        "active_artifact": {
            "title": candidate.title,
            "status": candidate.status,
            "delivery_certificate": str(candidate.certificate),
            "delivery_certificate_sha256": sha256(candidate.certificate),
            "pdf": str(candidate.pdf),
            "pdf_sha256": candidate.pdf_sha256,
            "pdf_pages": candidate.pages,
            "pdf_bytes": candidate.pdf.stat().st_size,
            "source": str(candidate.source),
            "source_sha256": candidate.source_sha256,
            "preservation_receipt": str(candidate.preservation_receipt),
            "preservation_receipt_sha256": sha256(candidate.preservation_receipt),
            "scientific_receipt": str(candidate.scientific_receipt),
            "scientific_receipt_sha256": sha256(candidate.scientific_receipt),
            "result_matrix": str(candidate.result_matrix),
            "result_matrix_sha256": sha256(candidate.result_matrix),
            "proof_matrix": str(candidate.proof_matrix),
            "proof_matrix_sha256": sha256(candidate.proof_matrix),
            "approved_canvas": str(candidate.approved_canvas),
            "approved_canvas_sha256": sha256(candidate.approved_canvas),
            "join_certificate": str(candidate.join_certificate),
            "join_certificate_sha256": sha256(candidate.join_certificate),
            "qa": str(candidate.qa),
            "qa_sha256": sha256(candidate.qa),
            "build_time_utc": time_text(candidate.build_time),
        },
        "non_regression_witness": {
            "role": "SEALED_NON_REGRESSION_WITNESS_ONLY",
            "package_id": witness.package_id,
            "status": witness.status,
            "authority_root": str(witness.root),
            "descriptor": str(witness.descriptor),
            "descriptor_sha256": sha256(witness.descriptor),
            "result": str(witness.result),
            "result_sha256": sha256(witness.result),
            "contract": str(witness.contract),
            "contract_sha256": sha256(witness.contract),
            "matrix": str(witness.matrix),
            "matrix_sha256": sha256(witness.matrix),
            "certificate": str(witness.certificate),
            "certificate_sha256": sha256(witness.certificate),
            "sha256sums": str(witness.sha256sums),
            "sha256sums_sha256": sha256(witness.sha256sums),
            "gate": str(witness.gate),
            "gate_sha256": sha256(witness.gate),
        },
    }


def resolve_payload() -> dict[str, Any]:
    global_sealed = sealed_payload(resolve_sealed())
    integral = integral_payload(resolve_integral())
    mass_law = mass_specialized_payload(resolve_mass_specialized(), resolve_mass_witness())
    for layer in (global_sealed, integral):
        locator = "\n".join(str(layer.get(key, "")) for key in ("authority_root", "pdf", "source_main"))
        if any(token in locator.upper() for token in OLD_AUTHORITY_TOKENS):
            raise SystemExit("FAIL_ULTIMA_AUTORIDAD_HMT_MD historical_revision_selected")
    return {
        "schema": "hmt-md-latest-material-authority-v3",
        "selection_rule": "LATEST_GLOBAL_SEALED_ARTIFACT_PLUS_LATEST_VERIFIED_INTEGRAL_EDITION",
        "consultation_order": [
            "global_latest_sealed_artifact",
            "latest_integral_edition",
            "latest_specialized_artifacts.mass_law_when_in_scope",
        ],
        "global_latest_sealed_artifact": global_sealed,
        "latest_integral_edition": integral,
        "latest_specialized_artifacts": {
            "mass_law": mass_law,
        },
        "authority_policy": (
            "START_FROM_THE_LATEST_GLOBAL_SEALED_ARTIFACT_AND_RETAIN_THE_LATEST_"
            "INTEGRAL_EDITION_FOR_COMPLETE_COVERAGE"
        ),
        "historical_revisions_role": "COMPARATIVE_AND_PROVENANCE_WITNESSES_ONLY",
        "historical_revisions_forbidden_as_authority_or_fallback": [
            "REV.1",
            "REV.3",
            "REV.4",
        ],
        "specialized_artifacts_policy": (
            "POSTERIOR_SPECIALIZED_DELTAS_ARE_MANDATORY_WHEN_IN_SCOPE_AND_DO_NOT_"
            "REPLACE_GLOBAL_OR_INTEGRAL_AUTHORITY"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="actualiza atómicamente el snapshot")
    parser.add_argument("--check", action="store_true", help="coteja sin escribir el snapshot")
    args = parser.parse_args()

    payload = resolve_payload()
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        temporary = SNAPSHOT.with_suffix(".json.tmp")
        temporary.write_text(rendered, encoding="utf-8")
        os.replace(temporary, SNAPSHOT)
    if args.check:
        if not SNAPSHOT.is_file() or SNAPSHOT.read_text(encoding="utf-8") != rendered:
            raise SystemExit("FAIL_ULTIMA_AUTORIDAD_HMT_MD snapshot_stale")

    print("PASS_ULTIMA_AUTORIDAD_HMT_MD")
    for label, layer in (
        ("GLOBAL", payload["global_latest_sealed_artifact"]),
        ("INTEGRAL", payload["latest_integral_edition"]),
    ):
        print(f"{label}_ROOT={layer['authority_root']}")
        print(f"{label}_SOURCE={layer['source_main']}")
        print(f"{label}_STATUS={layer['material_status']}")
        print(f"{label}_PDF={layer['pdf']}")
        print(f"{label}_PDF_SHA256={layer['pdf_sha256']}")
        print(f"{label}_PDF_PAGES={layer['pdf_pages']}")
        print(f"{label}_MANIFEST={layer.get('artifact_manifest') or layer.get('delivery_manifest')}")
        print(f"{label}_PRECOMPILE_RECEIPT={layer['precompile_receipt']}")
    mass_law = payload["latest_specialized_artifacts"]["mass_law"]
    print(f"SPECIALIZED_MASS_LAW_ROOT={mass_law['authority_root']}")
    print(f"SPECIALIZED_MASS_LAW_PDF={mass_law['active_artifact']['pdf']}")
    print(f"SPECIALIZED_MASS_LAW_PDF_SHA256={mass_law['active_artifact']['pdf_sha256']}")
    print("SPECIALIZED_MASS_LAW_READY=true")
    print("MODE=LATEST_GLOBAL_AND_INTEGRAL_AUTHORITY_FIRST")


if __name__ == "__main__":
    main()
