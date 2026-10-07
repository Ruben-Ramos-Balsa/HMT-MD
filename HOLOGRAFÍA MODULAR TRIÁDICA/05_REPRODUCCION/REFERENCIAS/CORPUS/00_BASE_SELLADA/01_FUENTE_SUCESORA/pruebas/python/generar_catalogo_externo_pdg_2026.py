#!/usr/bin/env python3
"""Genera el anexo externo PDG 2026 sin convertirlo en entrada de HMT--MD.

El programa usa exclusivamente la biblioteca estándar.  Produce una fila de
identidad por cada entrada de ``pdgparticle`` y una sola fila por propiedad de
masa o anchura de las Summary Tables 2026.  Las propiedades se enlazan con
todas las identidades de carga/antipartícula de su grupo PDG, pero no se
duplican para cada una de ellas.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "HMT_MD_EXTERNAL_CATALOG_1.0"
EXPECTED_SNAPSHOT_SHA256 = (
    "40dc2587d9ae912d26fafb6b41f300f341d2a1f4bd620ff5b5f03827c39453fe"
)
PDG_EDITION = "2026"
PDG_SUMMARY_TABLES_CUTOFF = "2026-01-15"
ACCESS_DATE = "2026-07-26"

# La tabla calibrada activa contiene diez especies y usa el electrón como
# escala posterior.  Sólo la propiedad canónica en MeV/GeV recibe cobertura
# ACTIVE; representaciones alternativas (por ejemplo, masa en u) siguen siendo
# comparaciones externas.
ACTIVE_MASS_PROPERTIES = {
    "S003M": "escala electrónica calibrada y electrón central (5,5)",
    "S004M": "tabla calibrada de diez especies: mu",
    "S008M": "tabla calibrada de diez especies: pi cargado",
    "S009M": "tabla calibrada de diez especies: pi neutro",
    "S010M": "tabla calibrada de diez especies: K cargado",
    "S011M": "tabla calibrada de diez especies: K neutro",
    "S016M": "tabla calibrada de diez especies: protón",
    "S017M": "tabla calibrada de diez especies: neutrón",
    "S035M": "tabla calibrada de diez especies: tau",
    "S043M": "tabla calibrada de diez especies: W",
    "S044M": "tabla calibrada de diez especies: Z",
}

# Estas filas existen en el decodificador inverso de doce especies, pero no son
# salidas prospectivas.  Se conservan como HISTORICAL para impedir su promoción
# accidental.
HISTORICAL_INVERSE_MASS_PROPERTIES = {
    "Q001M": "decodificador inverso de doce especies: quark d",
    "Q002M": "decodificador inverso de doce especies: quark u",
    "Q003M": "decodificador inverso de doce especies: quark s",
    "Q004M": "decodificador inverso de doce especies: quark c",
    "Q005M": "decodificador inverso de doce especies: quark b",
    "Q007TP": "decodificador inverso de doce especies: quark t",
    "S126M": "decodificador inverso de doce especies: Higgs",
}

CSV_FIELDS = [
    "schema_version",
    "output_id",
    "record_kind",
    "particle_group_pdgid",
    "particle_output_ids",
    "particle_names",
    "particle_entry_id",
    "object_name",
    "cc_type",
    "mcid",
    "charge_e",
    "quantum_i",
    "quantum_g",
    "quantum_j",
    "quantum_p",
    "quantum_c",
    "property_data_id",
    "property_pdgid",
    "observable_kind",
    "observable_description",
    "domain",
    "codomain",
    "statute",
    "causal_direction",
    "construction_mode",
    "coverage_state",
    "hmt_mapping_status",
    "hmt_mapping",
    "value",
    "value_text",
    "display_value",
    "display_power_of_ten",
    "display_in_percent",
    "value_type",
    "limit_type",
    "confidence_level",
    "uncertainty_positive",
    "uncertainty_negative",
    "uncertainty_kind",
    "covariance",
    "scale_factor",
    "unit",
    "scheme",
    "scale",
    "metrology_note",
    "pdg_comment",
    "source",
    "source_url",
    "source_edition",
    "source_cutoff",
    "source_license",
    "snapshot_sha256",
    "source_accessed_at",
    "falsifier",
]


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_number(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return format(value, ".17g")
    return str(value)


def clean(value: Any) -> str:
    return "" if value is None else str(value)


def pipe_join(values: Iterable[str]) -> str:
    return " | ".join(str(value) for value in values)


def source_columns(snapshot_sha256: str) -> dict[str, str]:
    return {
        "source": "Particle Data Group (PDG)",
        "source_url": "https://pdg.lbl.gov/api",
        "source_edition": PDG_EDITION,
        "source_cutoff": PDG_SUMMARY_TABLES_CUTOFF,
        "source_license": "CC BY 4.0",
        "snapshot_sha256": snapshot_sha256,
        "source_accessed_at": ACCESS_DATE,
    }


def hmt_mapping(property_pdgid: str = "", group_pdgid: str = "") -> dict[str, str]:
    if property_pdgid in ACTIVE_MASS_PROPERTIES:
        return {
            "causal_direction": "INVERSE",
            "construction_mode": "TARGET_RESIDUAL_CALIBRATED",
            "coverage_state": "ACTIVE",
            "hmt_mapping_status": "RECONSTRUCCION_CALIBRADA",
            "hmt_mapping": ACTIVE_MASS_PROPERTIES[property_pdgid],
        }
    if property_pdgid in HISTORICAL_INVERSE_MASS_PROPERTIES:
        return {
            "causal_direction": "INVERSE",
            "construction_mode": "TARGET_RESIDUAL_CALIBRATED",
            "coverage_state": "HISTORICAL",
            "hmt_mapping_status": "RECONSTRUCCION_CALIBRADA",
            "hmt_mapping": HISTORICAL_INVERSE_MASS_PROPERTIES[property_pdgid],
        }

    return {
        "causal_direction": "NONE",
        "construction_mode": "EXTERNAL_ONLY",
        "coverage_state": "ABSENT",
        "hmt_mapping_status": "PHYSICAL_INTERFACE_OPEN",
        "hmt_mapping": (
            "sin realización HMT--MD sellada para este registro; una reconstrucción "
            "de masa no construye la identidad física ni la representación"
        ),
    }


def uncertainty_fields(row: sqlite3.Row) -> dict[str, str]:
    limit_type = clean(row["limit_type"])
    error_positive = row["error_positive"]
    error_negative = row["error_negative"]
    if limit_type:
        return {
            "uncertainty_positive": "NOT_APPLICABLE",
            "uncertainty_negative": "NOT_APPLICABLE",
            "uncertainty_kind": "NOT_APPLICABLE_LIMIT",
            "covariance": "UNAVAILABLE",
        }
    if error_positive is None and error_negative is None:
        return {
            "uncertainty_positive": "UNAVAILABLE",
            "uncertainty_negative": "UNAVAILABLE",
            "uncertainty_kind": "UNAVAILABLE",
            "covariance": "UNAVAILABLE",
        }
    positive = text_number(error_positive)
    negative = text_number(error_negative)
    kind = "SYMMETRIC" if positive == negative else "ASYMMETRIC"
    return {
        "uncertainty_positive": positive or "UNAVAILABLE",
        "uncertainty_negative": negative or "UNAVAILABLE",
        "uncertainty_kind": kind,
        "covariance": "UNAVAILABLE",
    }


def load_snapshot(snapshot: Path) -> tuple[dict[str, str], list[sqlite3.Row], list[sqlite3.Row]]:
    connection = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        info = {
            row["name"]: row["value"]
            for row in connection.execute("SELECT name, value FROM pdginfo ORDER BY name")
        }
        particles = list(
            connection.execute(
                """
                SELECT id, pdgid, name, cc_type, mcid, charge,
                       quantum_i, quantum_g, quantum_j, quantum_p, quantum_c
                FROM pdgparticle
                ORDER BY id
                """
            )
        )
        properties = list(
            connection.execute(
                """
                WITH RECURSIVE
                particle_roots(id, pdgid) AS (
                    SELECT DISTINCT p.pdgid_id, p.pdgid
                    FROM pdgparticle AS p
                ),
                descendants(id, pdgid, parent_id, parent_pdgid,
                            description, data_type, node_sort,
                            root_pdgid, depth) AS (
                    SELECT n.id, n.pdgid, n.parent_id, n.parent_pdgid,
                           n.description, n.data_type, n.sort,
                           r.pdgid, 0
                    FROM pdgid AS n
                    JOIN particle_roots AS r ON r.id = n.id
                    UNION ALL
                    SELECT c.id, c.pdgid, c.parent_id, c.parent_pdgid,
                           c.description, c.data_type, c.sort,
                           d.root_pdgid, d.depth + 1
                    FROM pdgid AS c
                    JOIN descendants AS d ON c.parent_id = d.id
                )
                SELECT d.id AS data_id, d.pdgid AS property_pdgid,
                       d.edition, d.value_type, d.in_summary_table,
                       d.confidence_level, d.limit_type, d.comment,
                       d.value, d.value_text, d.error_positive,
                       d.error_negative, d.scale_factor, d.unit_text,
                       d.display_value_text, d.display_power_of_ten,
                       d.display_in_percent, d.sort AS data_sort,
                       n.description AS observable_description,
                       n.data_type AS observable_kind,
                       n.root_pdgid, n.depth, n.node_sort
                FROM pdgdata AS d
                JOIN descendants AS n ON n.id = d.pdgid_id
                WHERE n.data_type IN ('M', 'G')
                  AND d.edition = ?
                  AND d.in_summary_table = 1
                ORDER BY n.root_pdgid, n.node_sort, d.sort, d.id
                """,
                (PDG_EDITION,),
            )
        )
    finally:
        connection.close()
    return info, particles, properties


def build_rows(
    snapshot_sha256: str,
    particles: list[sqlite3.Row],
    properties: list[sqlite3.Row],
) -> tuple[list[dict[str, str]], dict[str, list[str]], dict[str, list[str]]]:
    group_names: dict[str, list[str]] = defaultdict(list)
    group_output_ids: dict[str, list[str]] = defaultdict(list)
    rows: list[dict[str, str]] = []
    source = source_columns(snapshot_sha256)

    for particle in particles:
        output_id = f"PDG2026:particle:{particle['id']:06d}"
        group = particle["pdgid"]
        group_names[group].append(clean(particle["name"]))
        group_output_ids[group].append(output_id)
        mapping = hmt_mapping(group_pdgid=group)
        row = {field: "" for field in CSV_FIELDS}
        row.update(source)
        row.update(mapping)
        row.update(
            {
                "schema_version": SCHEMA_VERSION,
                "output_id": output_id,
                "record_kind": "PARTICLE_IDENTITY",
                "particle_group_pdgid": group,
                "particle_output_ids": output_id,
                "particle_names": clean(particle["name"]),
                "particle_entry_id": text_number(particle["id"]),
                "object_name": clean(particle["name"]),
                "cc_type": clean(particle["cc_type"]),
                "mcid": text_number(particle["mcid"]),
                "charge_e": text_number(particle["charge"]),
                "quantum_i": clean(particle["quantum_i"]),
                "quantum_g": clean(particle["quantum_g"]),
                "quantum_j": clean(particle["quantum_j"]),
                "quantum_p": clean(particle["quantum_p"]),
                "quantum_c": clean(particle["quantum_c"]),
                "observable_kind": "IDENTITY",
                "observable_description": "entrada individual de pdgparticle",
                "domain": "pdgparticle(snapshot=PDG_2026)",
                "codomain": "EXTERNAL_PARTICLE_IDENTITY_RECORD",
                "statute": "RECONOCIMIENTO_EXTERNO",
                "value": "NOT_APPLICABLE",
                "value_text": "NOT_APPLICABLE",
                "display_value": "NOT_APPLICABLE",
                "display_power_of_ten": "NOT_APPLICABLE",
                "display_in_percent": "NOT_APPLICABLE",
                "value_type": "NOT_APPLICABLE",
                "limit_type": "NOT_APPLICABLE",
                "confidence_level": "NOT_APPLICABLE",
                "uncertainty_positive": "NOT_APPLICABLE",
                "uncertainty_negative": "NOT_APPLICABLE",
                "uncertainty_kind": "NOT_APPLICABLE",
                "covariance": "NOT_APPLICABLE",
                "scale_factor": "NOT_APPLICABLE",
                "unit": "NOT_APPLICABLE",
                "scheme": "NOT_APPLICABLE",
                "scale": "NOT_APPLICABLE",
                "metrology_note": (
                    "registro de identidad; no constituye un observable ni una predicción"
                ),
                "pdg_comment": "NOT_APPLICABLE",
                "falsifier": (
                    "falla si la fila no reproduce exactamente la identidad, carga o "
                    "números cuánticos almacenados en pdgparticle"
                ),
            }
        )
        rows.append(row)

    for prop in properties:
        group = prop["root_pdgid"]
        property_pdgid = prop["property_pdgid"]
        output_id = (
            f"PDG2026:observable:{group}:{property_pdgid}:{prop['data_id']:06d}"
        )
        mapping = hmt_mapping(property_pdgid=property_pdgid, group_pdgid=group)
        uncertainty = uncertainty_fields(prop)
        is_mass = prop["observable_kind"] == "M"
        observable_kind = "MASS" if is_mass else "WIDTH"
        codomain = (
            "EXTERNAL_MASS_VALUE_OR_LIMIT_WITH_UNIT"
            if is_mass
            else "EXTERNAL_WIDTH_VALUE_OR_LIMIT_WITH_UNIT"
        )
        metrology_note = (
            "El snapshot no estructura el esquema ni la escala de renormalización; "
            "para masas de quark y convenciones de polo debe consultarse la ficha PDG."
        )
        if not group.startswith("Q"):
            metrology_note = (
                "La convención de masa, polo o anchura no se infiere: se conserva "
                "la descripción PDG y se marca esquema/escala como no disponibles."
            )
        row = {field: "" for field in CSV_FIELDS}
        row.update(source)
        row.update(mapping)
        row.update(uncertainty)
        row.update(
            {
                "schema_version": SCHEMA_VERSION,
                "output_id": output_id,
                "record_kind": "SUMMARY_TABLE_OBSERVABLE",
                "particle_group_pdgid": group,
                "particle_output_ids": pipe_join(group_output_ids[group]),
                "particle_names": pipe_join(group_names[group]),
                "object_name": clean(prop["observable_description"]),
                "property_pdgid": property_pdgid,
                "property_data_id": text_number(prop["data_id"]),
                "observable_kind": observable_kind,
                "observable_description": clean(prop["observable_description"]),
                "domain": f"pdgdata[{property_pdgid}](PDG_2026_SUMMARY_TABLES)",
                "codomain": codomain,
                "statute": "RECONOCIMIENTO_EXTERNO",
                "value": text_number(prop["value"]) or "UNAVAILABLE",
                "value_text": clean(prop["value_text"]) or "UNAVAILABLE",
                "display_value": clean(prop["display_value_text"]) or "UNAVAILABLE",
                "display_power_of_ten": text_number(prop["display_power_of_ten"]),
                "display_in_percent": text_number(prop["display_in_percent"]),
                "value_type": clean(prop["value_type"]) or "UNAVAILABLE",
                "limit_type": clean(prop["limit_type"]) or "NONE",
                "confidence_level": (
                    text_number(prop["confidence_level"]) or "UNAVAILABLE"
                ),
                "unit": clean(prop["unit_text"]) or "DIMENSIONLESS_OR_UNSPECIFIED",
                "scale_factor": text_number(prop["scale_factor"]) or "UNAVAILABLE",
                "scheme": "UNAVAILABLE_IN_SNAPSHOT",
                "scale": "UNAVAILABLE_IN_SNAPSHOT",
                "metrology_note": metrology_note,
                "pdg_comment": clean(prop["comment"]) or "UNAVAILABLE",
                "falsifier": (
                    "falla si el valor, límite, unidad, incertidumbre, propietario PDG "
                    "o estatuto HMT difiere del snapshot y de las listas de cobertura "
                    "declaradas"
                ),
            }
        )
        rows.append(row)

    return rows, group_names, group_output_ids


def sources_document(snapshot_sha256: str, pdg_info: dict[str, str]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": ACCESS_DATE,
        "sources": [
            {
                "source_id": "PDG_2026_SUMMARY_TABLES",
                "institution": "Particle Data Group",
                "edition": PDG_EDITION,
                "summary_tables_cutoff": PDG_SUMMARY_TABLES_CUTOFF,
                "snapshot_release_timestamp": pdg_info.get(
                    "data_release_timestamp", "UNAVAILABLE"
                ),
                "citation": pdg_info.get("citation", "UNAVAILABLE"),
                "url": "https://pdg.lbl.gov/api",
                "snapshot_about": pdg_info.get("about", "UNAVAILABLE"),
                "license": pdg_info.get("license", "UNAVAILABLE"),
                "snapshot_filename": "pdg-2026.0.sqlite",
                "snapshot_sha256": snapshot_sha256,
                "accessed_at": ACCESS_DATE,
                "role": "EXTERNAL_COMPARISON_INPUT_ONLY",
                "used_as_generator_input": True,
            },
            {
                "source_id": "BIPM_SI_BROCHURE_9ED_V4_01_2026",
                "institution": "Bureau International des Poids et Mesures",
                "edition": "9th edition, version 4.01, June 2026",
                "doi": "10.59161/AUEZ1291",
                "url": "https://doi.org/10.59161/AUEZ1291",
                "license": "UNAVAILABLE_IN_LOCAL_AUTHORITY",
                "accessed_at": ACCESS_DATE,
                "role": "METROLOGICAL_AUTHORITY_ONLY_NOT_GENERATOR_INPUT",
                "used_as_generator_input": False,
            },
            {
                "source_id": "CODATA_2022_NIST",
                "institution": "CODATA / NIST",
                "edition": "2022 recommended values",
                "url": "https://physics.nist.gov/cuu/Constants/",
                "license": "UNAVAILABLE_IN_LOCAL_AUTHORITY",
                "accessed_at": ACCESS_DATE,
                "role": "CURRENT_EXTERNAL_RECOGNITION_ONLY_NOT_GENERATOR_INPUT",
                "used_as_generator_input": False,
            },
            {
                "source_id": "CODATA_2018_NIST_HISTORICAL",
                "institution": "CODATA / NIST",
                "edition": "2018 recommended values",
                "url": "https://physics.nist.gov/cuu/Constants/archive2018.html",
                "license": "UNAVAILABLE_IN_LOCAL_AUTHORITY",
                "accessed_at": ACCESS_DATE,
                "role": "HISTORICAL_RECOGNITION_ONLY_NOT_GENERATOR_INPUT",
                "used_as_generator_input": False,
            },
        ],
        "independence_clause": (
            "BIPM y CODATA tipan unidades y comparaciones; no seleccionan firmas, "
            "rutas, torres ni realizaciones HMT--MD."
        ),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=CSV_FIELDS,
            extrasaction="raise",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("/tmp/pdg-2026.0.sqlite"),
        help="snapshot SQLite oficial de PDG 2026",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=(
            Path(__file__).resolve().parents[2]
            / "datos"
            / "catalogo_externo_pdg_2026"
        ),
    )
    arguments = parser.parse_args()

    snapshot = arguments.snapshot.resolve()
    if not snapshot.is_file():
        fail(f"snapshot ausente: {snapshot}")
    snapshot_sha256 = sha256_file(snapshot)
    if snapshot_sha256 != EXPECTED_SNAPSHOT_SHA256:
        fail(
            "huella del snapshot inesperada: "
            f"{snapshot_sha256} != {EXPECTED_SNAPSHOT_SHA256}"
        )

    pdg_info, particles, properties = load_snapshot(snapshot)
    if pdg_info.get("edition") != PDG_EDITION:
        fail(f"edición PDG inesperada: {pdg_info.get('edition')!r}")
    if pdg_info.get("license") != "CC BY 4.0":
        fail(f"licencia PDG inesperada: {pdg_info.get('license')!r}")
    if len(particles) != 1170:
        fail(f"censo pdgparticle inesperado: {len(particles)}")
    if len(properties) != 855:
        fail(f"censo masa/anchura Summary Tables inesperado: {len(properties)}")

    rows, group_names, _ = build_rows(snapshot_sha256, particles, properties)
    output_dir = arguments.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "catalogo_externo_pdg_2026.csv"
    json_path = output_dir / "catalogo_externo_pdg_2026.json"
    sources_path = output_dir / "fuentes_metrologicas_2026.json"
    manifest_path = output_dir / "MANIFEST_SHA256.json"

    identity_count = sum(row["record_kind"] == "PARTICLE_IDENTITY" for row in rows)
    observable_count = sum(
        row["record_kind"] == "SUMMARY_TABLE_OBSERVABLE" for row in rows
    )
    mass_count = sum(row["observable_kind"] == "MASS" for row in rows)
    width_count = sum(row["observable_kind"] == "WIDTH" for row in rows)
    active_count = sum(row["coverage_state"] == "ACTIVE" for row in rows)
    historical_count = sum(row["coverage_state"] == "HISTORICAL" for row in rows)
    absent_count = sum(row["coverage_state"] == "ABSENT" for row in rows)

    catalogue = {
        "schema_version": SCHEMA_VERSION,
        "edition": PDG_EDITION,
        "generated_at": ACCESS_DATE,
        "snapshot_sha256": snapshot_sha256,
        "deduplication_rule": (
            "cada entrada de pdgparticle tiene una fila de identidad; cada propiedad "
            "M/G se publica una sola vez por grupo PDG y enlaza todas sus identidades"
        ),
        "counts": {
            "particle_entries": identity_count,
            "particle_groups": len(group_names),
            "summary_observables": observable_count,
            "mass_observables": mass_count,
            "width_observables": width_count,
            "rows_total": len(rows),
            "coverage_active_rows": active_count,
            "coverage_historical_rows": historical_count,
            "coverage_absent_rows": absent_count,
        },
        "rows": rows,
    }
    sources = sources_document(snapshot_sha256, pdg_info)
    write_csv(csv_path, rows)
    write_json(json_path, catalogue)
    write_json(sources_path, sources)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "snapshot": {
            "filename": snapshot.name,
            "sha256": snapshot_sha256,
            "packaged": False,
            "retrieval": "official PDG API snapshot; see fuentes_metrologicas_2026.json",
        },
        "artifacts": {
            csv_path.name: {
                "sha256": sha256_file(csv_path),
                "bytes": csv_path.stat().st_size,
            },
            json_path.name: {
                "sha256": sha256_file(json_path),
                "bytes": json_path.stat().st_size,
            },
            sources_path.name: {
                "sha256": sha256_file(sources_path),
                "bytes": sources_path.stat().st_size,
            },
        },
        "counts": catalogue["counts"],
    }
    write_json(manifest_path, manifest)

    print(
        "PASS_GENERACION_CATALOGO_EXTERNO_PDG_2026 "
        f"particles={identity_count} groups={len(group_names)} "
        f"observables={observable_count} mass={mass_count} width={width_count} "
        f"rows={len(rows)} active={active_count} historical={historical_count} "
        f"absent={absent_count}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"FAIL_GENERACION_CATALOGO_EXTERNO_PDG_2026: {error}", file=sys.stderr)
        raise SystemExit(1)
