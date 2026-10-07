#!/usr/bin/env python3
"""Verifica la matriz atómica de la adenda física HMT--MD.

Sólo usa la biblioteca estándar, no escribe archivos y conserva todas las
puertas bajo ``python -O``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


EXPECTED_WITNESS = {
    "main": (
        Path(
            "testigos_integracion/"
            "adenda_realizaciones_fisicas_hmt_md_2026-07-26/"
            "manuscrito/main.tex"
        ),
        "b1cb67ac8afdaf46066ad7f6628fda1da2f3e914e3797644226c05a0317b46cf",
    ),
    "instruction": (
        Path(
            "testigos_integracion/"
            "adenda_realizaciones_fisicas_hmt_md_2026-07-26/"
            "INSTRUCCION_DE_INTEGRACION.md"
        ),
        "2c1e5d942d5ad8f869ceed48bd28e6b4d703da342f5f0a97b844824cb6c93491",
    ),
    "pdf": (
        Path(
            "testigos_integracion/"
            "adenda_realizaciones_fisicas_hmt_md_2026-07-26/pdf/"
            "EXTENSIONES_NULAS_CLAUSURA_MATERIAL_TEMPERATURA_Y_"
            "GRAVITACION_HMT_MD_2026-07-26.pdf"
        ),
        "e8dc2378c49401b546f0e86d67e34c0e81cabff061f5faf002107dd8bf67bf32",
    ),
}

CANONICAL_STATUTES = {
    "EXACTO_INTERNO",
    "RELATIVO_A_PRIMITIVAS",
    "RECONSTRUCCION_CALIBRADA",
    "RECONOCIMIENTO_EXTERNO",
    "INTERFAZ_FISICA",
    "PROGRAMA_ABIERTO",
}

LATEX_LABEL_PREFIXES = {
    "chap",
    "sec",
    "thm",
    "prop",
    "def",
    "crit",
    "cor",
    "tab",
    "fig",
    "prin",
    "macro",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def block_sha(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    require(1 <= start <= end <= len(lines), f"rango inválido: {path}:{start}-{end}")
    text = "\n".join(lines[start - 1 : end]) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    matrix_path = root / "datos/matriz_cobertura_atomica_adenda_37pp.json"
    csv_path = root / "datos/matriz_cobertura_atomica_adenda_37pp.csv"
    markdown_path = root / "auditoria/MATRIZ_COBERTURA_ATOMICA_ADENDA_37PP.md"
    certificate_path = (
        root / "certificados/matriz_cobertura_atomica_adenda_37pp.json"
    )

    for path in (matrix_path, csv_path, markdown_path, certificate_path):
        require(path.is_file(), f"artefacto ausente: {path}")

    for name, (relative_path, expected_sha) in EXPECTED_WITNESS.items():
        path = root / relative_path
        require(path.is_file(), f"testigo ausente: {name}")
        require(
            sha256_path(path) == expected_sha,
            f"huella del testigo alterada: {name}",
        )

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    require(
        matrix.get("schema") == "HMT_MD_ATOMIC_COVERAGE_MATRIX_V2",
        "schema de matriz incorrecto",
    )
    require(matrix.get("witness_is_read_only") is True, "testigo no marcado solo lectura")
    require(
        matrix.get("all_locators_are_relative_to_delivery_root") is True,
        "la matriz no declara localizadores portables",
    )
    rows = matrix.get("rows")
    require(isinstance(rows, list), "rows no es una lista")
    require(len(rows) >= 80, "granularidad insuficiente: menos de 80 filas")
    require(matrix.get("row_count") == len(rows), "row_count incoherente")

    required_fields = {
        "id",
        "origin",
        "primary_residence",
        "destination",
        "proof_status",
        "formula_and_all_hypotheses",
        "proof_or_certificate",
        "negative_control_or_falsifier",
        "incorporation_status",
    }
    ids: set[str] = set()
    source_ranges: dict[str, set[int]] = {}
    source_paths: dict[str, Path] = {}

    for row in rows:
        require(isinstance(row, dict), "fila no es objeto")
        require(required_fields <= set(row), f"campos ausentes en {row.get('id')}")
        row_id = row["id"]
        require(isinstance(row_id, str) and row_id, "id vacío")
        require(row_id not in ids, f"id duplicado: {row_id}")
        ids.add(row_id)

        origin = row["origin"]
        destination = row["destination"]
        residence = row["primary_residence"]
        for obj, name in (
            (origin, "origin"),
            (destination, "destination"),
            (residence, "primary_residence"),
        ):
            require(isinstance(obj, dict), f"{name} no es objeto en {row_id}")

        source_rel = Path(origin["relative_path"])
        dest_rel = Path(destination["relative_path"])
        require(
            not source_rel.is_absolute() and ".." not in source_rel.parts,
            f"origen no portable en {row_id}",
        )
        require(
            not dest_rel.is_absolute() and ".." not in dest_rel.parts,
            f"destino no portable en {row_id}",
        )
        source_path = root / source_rel
        dest_path = root / dest_rel
        require(source_path.is_file(), f"origen ausente en {row_id}")
        require(dest_path.is_file(), f"destino ausente en {row_id}")
        start = int(origin["line_start"])
        end = int(origin["line_end"])
        dstart = int(destination["line_start"])
        dend = int(destination["line_end"])
        require(
            origin["exact_locator"] == f"{source_rel.as_posix()}:{start}-{end}",
            f"localizador de origen incoherente en {row_id}",
        )
        require(
            destination["exact_locator"]
            == f"{dest_rel.as_posix()}:{dstart}-{dend}",
            f"localizador de destino incoherente en {row_id}",
        )
        require(
            origin["sha256_block"] == block_sha(source_path, start, end),
            f"bloque de origen alterado en {row_id}",
        )
        require(
            destination["sha256_block"] == block_sha(dest_path, dstart, dend),
            f"bloque de destino alterado en {row_id}",
        )
        require(
            residence["stable_label"] == destination["stable_label"],
            f"etiqueta de residencia y destino diverge en {row_id}",
        )
        require(
            residence["relative_file"] == dest_rel.as_posix(),
            f"ruta relativa incorrecta en {row_id}",
        )

        label = destination["stable_label"]
        require(isinstance(label, str) and ":" in label, f"etiqueta inestable en {row_id}")
        prefix = label.split(":", 1)[0]
        if prefix in LATEX_LABEL_PREFIXES:
            dest_text = dest_path.read_text(encoding="utf-8")
            require(
                f"\\label{{{label}}}" in dest_text,
                f"etiqueta LaTeX ausente en {row_id}: {label}",
            )

        statutes = row["proof_status"]
        require(isinstance(statutes, list) and statutes, f"estatuto vacío en {row_id}")
        require(
            set(statutes) <= CANONICAL_STATUTES,
            f"estatuto no canónico en {row_id}",
        )
        for field in (
            "formula_and_all_hypotheses",
            "proof_or_certificate",
            "negative_control_or_falsifier",
            "incorporation_status",
        ):
            value = row[field]
            require(isinstance(value, str) and value.strip(), f"{field} vacío en {row_id}")

        artifact = origin["artifact"]
        source_paths.setdefault(artifact, source_path)
        require(
            source_paths[artifact] == source_path,
            f"dos rutas para el artefacto {artifact}",
        )
        source_ranges.setdefault(artifact, set()).update(range(start, end + 1))

    coverage = matrix.get("source_coverage")
    require(isinstance(coverage, dict), "source_coverage ausente")
    for artifact, source_path in source_paths.items():
        lines = source_path.read_text(encoding="utf-8").splitlines()
        covered = set(source_ranges[artifact])
        blank = {
            number
            for number, line in enumerate(lines, start=1)
            if not line.strip()
        }
        covered.update(blank)
        missing = sorted(set(range(1, len(lines) + 1)) - covered)
        require(not missing, f"líneas sin cobertura en {artifact}: {missing[:10]}")
        item = coverage.get(artifact)
        require(isinstance(item, dict), f"reporte ausente para {artifact}")
        require(item.get("missing_lines") == [], f"reporte con huecos en {artifact}")
        require(
            item.get("coverage_percent") == 100.0,
            f"cobertura distinta de 100% en {artifact}",
        )
        require(
            item.get("sha256") == sha256_path(source_path),
            f"huella de fuente incoherente en {artifact}",
        )

    require(
        certificate.get("status")
        == "PASS_MATRIZ_COBERTURA_ATOMICA_ADENDA_37PP",
        "certificado sin estado PASS",
    )
    require(certificate.get("row_count") == len(rows), "certificado con conteo distinto")
    artifacts = certificate.get("artifacts")
    require(isinstance(artifacts, dict), "manifest de artefactos ausente")
    for path in (matrix_path, csv_path, markdown_path):
        relative = str(path.relative_to(root))
        require(
            artifacts.get(relative) == sha256_path(path),
            f"huella incoherente en certificado: {relative}",
        )

    own_text = Path(__file__).read_text(encoding="utf-8")
    banned_token = "a" + "ssert("
    require(banned_token not in own_text, "el verificador contiene assert")

    print(
        "PASS_MATRIZ_COBERTURA_ATOMICA_ADENDA_37PP "
        f"rows={len(rows)} sources={len(source_paths)} "
        "coverage=100.00000000 witness=immutable"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
