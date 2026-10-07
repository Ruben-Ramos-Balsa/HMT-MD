#!/usr/bin/env python3
"""Verifica estructura, tipado, huellas y reproducción del anexo PDG 2026."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


EXPECTED_SNAPSHOT_SHA256 = (
    "40dc2587d9ae912d26fafb6b41f300f341d2a1f4bd620ff5b5f03827c39453fe"
)
EXPECTED_PARTICLES = 1170
EXPECTED_GROUPS = 438
EXPECTED_OBSERVABLES = 855
EXPECTED_MASS = 471
EXPECTED_WIDTH = 384
EXPECTED_ROWS = EXPECTED_PARTICLES + EXPECTED_OBSERVABLES


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_static(output_dir: Path) -> dict[str, int]:
    csv_path = output_dir / "catalogo_externo_pdg_2026.csv"
    json_path = output_dir / "catalogo_externo_pdg_2026.json"
    sources_path = output_dir / "fuentes_metrologicas_2026.json"
    manifest_path = output_dir / "MANIFEST_SHA256.json"
    for path in (csv_path, json_path, sources_path, manifest_path):
        require(path.is_file(), f"artefacto ausente: {path}")

    manifest = load_json(manifest_path)
    require(
        manifest["snapshot"]["sha256"] == EXPECTED_SNAPSHOT_SHA256,
        "huella del snapshot incorrecta en el manifiesto",
    )
    for filename, metadata in manifest["artifacts"].items():
        path = output_dir / filename
        require(sha256_file(path) == metadata["sha256"], f"SHA incorrecto: {filename}")
        require(path.stat().st_size == metadata["bytes"], f"bytes incorrectos: {filename}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    catalogue = load_json(json_path)
    require(rows == catalogue["rows"], "CSV y JSON no contienen las mismas filas")
    require(len(rows) == EXPECTED_ROWS, f"censo total inesperado: {len(rows)}")

    output_ids = [row["output_id"] for row in rows]
    require(len(output_ids) == len(set(output_ids)), "output_id duplicado")
    identities = [row for row in rows if row["record_kind"] == "PARTICLE_IDENTITY"]
    observables = [
        row for row in rows if row["record_kind"] == "SUMMARY_TABLE_OBSERVABLE"
    ]
    require(len(identities) == EXPECTED_PARTICLES, "censo de identidades incorrecto")
    require(len(observables) == EXPECTED_OBSERVABLES, "censo de observables incorrecto")

    group_ids = {row["particle_group_pdgid"] for row in identities}
    require(len(group_ids) == EXPECTED_GROUPS, "censo de grupos PDG incorrecto")
    mass_rows = [row for row in observables if row["observable_kind"] == "MASS"]
    width_rows = [row for row in observables if row["observable_kind"] == "WIDTH"]
    require(len(mass_rows) == EXPECTED_MASS, f"censo de masas incorrecto: {len(mass_rows)}")
    require(
        len(width_rows) == EXPECTED_WIDTH,
        f"censo de anchuras incorrecto: {len(width_rows)}",
    )

    property_keys = [
        (row["particle_group_pdgid"], row["property_pdgid"])
        for row in observables
    ]
    require(
        len(property_keys) == len(set(property_keys)),
        "observable de grupo duplicado",
    )
    property_data_ids = [row["property_data_id"] for row in observables]
    require(
        len(property_data_ids) == len(set(property_data_ids)),
        "pdgdata.id duplicado",
    )
    identity_ids = {row["output_id"] for row in identities}
    for row in observables:
        links = set(row["particle_output_ids"].split(" | "))
        require(links, f"observable sin identidades: {row['output_id']}")
        require(links <= identity_ids, f"enlace de identidad inválido: {row['output_id']}")
        require(row["statute"] == "RECONOCIMIENTO_EXTERNO", "estatuto externo alterado")
        require(row["covariance"] == "UNAVAILABLE", "covarianza inventada")
        require(
            row["scheme"] == "UNAVAILABLE_IN_SNAPSHOT",
            "esquema inferido sin soporte",
        )
        require(row["scale"] == "UNAVAILABLE_IN_SNAPSHOT", "escala inferida sin soporte")
        require(row["source_license"] == "CC BY 4.0", "licencia PDG alterada")
        require(row["value_type"], "value_type omitido")
        require(row["display_power_of_ten"], "potencia de presentación omitida")
        require(
            row["snapshot_sha256"] == EXPECTED_SNAPSHOT_SHA256,
            "huella PDG alterada en una fila",
        )

    allowed_coverage = {"ACTIVE", "HISTORICAL", "ABSENT"}
    allowed_modes = {
        "TARGET_RESIDUAL_CALIBRATED",
        "EXTERNAL_ONLY",
    }
    for row in rows:
        require(row["coverage_state"] in allowed_coverage, "coverage_state inválido")
        require(row["construction_mode"] in allowed_modes, "construction_mode inválido")
        if row["record_kind"] == "PARTICLE_IDENTITY":
            require(
                row["coverage_state"] == "ABSENT",
                "una masa calibrada fue promovida a realización de identidad física",
            )
        if row["coverage_state"] == "ACTIVE":
            require(
                row["construction_mode"] == "TARGET_RESIDUAL_CALIBRATED",
                "ACTIVE promovido a salida prospectiva",
            )
            require(row["causal_direction"] == "INVERSE", "ACTIVE sin dirección inversa")
        if row["coverage_state"] == "ABSENT":
            require(
                row["hmt_mapping_status"] == "PHYSICAL_INTERFACE_OPEN",
                "ABSENT sin interfaz abierta",
            )
        if row["observable_kind"] == "WIDTH":
            require(row["coverage_state"] == "ABSENT", "anchura promovida a cobertura HMT")
        if row["particle_group_pdgid"] in {"S001", "S002", "S036"}:
            require(
                row["observable_kind"] != "MASS",
                "masa de neutrino no contenida en pdgparticle fue inventada",
            )

    sources = load_json(sources_path)
    source_index = {entry["source_id"]: entry for entry in sources["sources"]}
    require("PDG_2026_SUMMARY_TABLES" in source_index, "fuente PDG ausente")
    require("BIPM_SI_BROCHURE_9ED_V4_01_2026" in source_index, "fuente BIPM ausente")
    require("CODATA_2022_NIST" in source_index, "fuente CODATA 2022 ausente")
    require(
        "CODATA_2018_NIST_HISTORICAL" in source_index,
        "fuente CODATA 2018 ausente",
    )
    for source_id in (
        "BIPM_SI_BROCHURE_9ED_V4_01_2026",
        "CODATA_2022_NIST",
        "CODATA_2018_NIST_HISTORICAL",
    ):
        require(
            source_index[source_id]["used_as_generator_input"] is False,
            f"{source_id} usado indebidamente como selector",
        )

    return {
        "particles": len(identities),
        "groups": len(group_ids),
        "observables": len(observables),
        "mass": len(mass_rows),
        "width": len(width_rows),
        "rows": len(rows),
        "active": sum(row["coverage_state"] == "ACTIVE" for row in rows),
        "historical": sum(row["coverage_state"] == "HISTORICAL" for row in rows),
        "absent": sum(row["coverage_state"] == "ABSENT" for row in rows),
    }


def check_reproduction(root: Path, output_dir: Path, snapshot: Path) -> None:
    require(snapshot.is_file(), f"snapshot ausente para reproducción: {snapshot}")
    require(sha256_file(snapshot) == EXPECTED_SNAPSHOT_SHA256, "snapshot con SHA incorrecto")
    generator = root / "pruebas" / "python" / "generar_catalogo_externo_pdg_2026.py"
    with tempfile.TemporaryDirectory(prefix="hmt-pdg-2026-") as temporary:
        regenerated = Path(temporary)
        command = [
            sys.executable,
            "-I",
            "-B",
            "-S",
            str(generator),
            "--snapshot",
            str(snapshot),
            "--output-dir",
            str(regenerated),
        ]
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            text=True,
            capture_output=True,
        )
        require(
            completed.returncode == 0,
            f"regeneración falló: {completed.stdout}\n{completed.stderr}",
        )
        for filename in (
            "catalogo_externo_pdg_2026.csv",
            "catalogo_externo_pdg_2026.json",
            "fuentes_metrologicas_2026.json",
            "MANIFEST_SHA256.json",
        ):
            require(
                (regenerated / filename).read_bytes() == (output_dir / filename).read_bytes(),
                f"reproducción no byte-idéntica: {filename}",
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("/tmp/pdg-2026.0.sqlite"),
    )
    parser.add_argument(
        "--sin-regenerar",
        action="store_true",
        help="verifica sólo los artefactos empaquetados y sus huellas",
    )
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    output_dir = root / "datos" / "catalogo_externo_pdg_2026"
    counts = check_static(output_dir)
    if not arguments.sin_regenerar:
        check_reproduction(root, output_dir, arguments.snapshot.resolve())

    print(
        "PASS_CATALOGO_EXTERNO_PDG_2026 "
        + " ".join(f"{key}={value}" for key, value in counts.items())
        + f" reproduced={str(not arguments.sin_regenerar).lower()}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"FAIL_CATALOGO_EXTERNO_PDG_2026: {error}", file=sys.stderr)
        raise SystemExit(1)
