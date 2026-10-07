#!/usr/bin/env python3
"""Verifica el delta atómico Bell/CHSH/EPR."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_sha(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    require(1 <= start <= end <= len(lines), "rango Bell inválido")
    return hashlib.sha256(
        ("\n".join(lines[start - 1 : end]) + "\n").encode("utf-8")
    ).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    matrix_path = root / "datos/matriz_control_bell_chsh_epr.json"
    csv_path = root / "datos/matriz_control_bell_chsh_epr.csv"
    md_path = root / "auditoria/ANEXO_CONTROL_BELL_CHSH_EPR.md"
    cert_path = root / "certificados/matriz_control_bell_chsh_epr.json"
    source_cert_path = root / "certificados/localidad_bell_hmt.json"
    provenance_path = root / "datos/bell_hmt/procedencia_bell_hmt.json"
    tex_path = root / "manuscrito/sections/md/04f_localidad_bell_proyeccion.tex"

    for path in (
        matrix_path, csv_path, md_path, cert_path, source_cert_path,
        provenance_path, tex_path,
    ):
        require(path.is_file(), f"artefacto ausente: {path}")

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    source_cert = json.loads(source_cert_path.read_text(encoding="utf-8"))
    require(
        matrix.get("schema") == "HMT_MD_BELL_ATOMIC_CONTROL_MATRIX_V2",
        "schema Bell incorrecto",
    )
    require(matrix.get("separate_from_adenda_37pp") is True, "delta no separado")
    require(
        matrix.get("all_locators_are_relative_to_delivery_root") is True,
        "localizadores Bell no declarados portables",
    )
    rows = matrix.get("rows")
    require(isinstance(rows, list) and len(rows) == 16, "conteo Bell incorrecto")
    require(matrix.get("row_count") == 16, "row_count Bell incoherente")

    ids: set[str] = set()
    required = {
        "id", "source_provenance", "primary_residence", "destination",
        "proof_status", "formula_and_all_hypotheses", "proof_or_certificate",
        "negative_control_or_falsifier", "incorporation_status",
    }
    for item in rows:
        require(required <= set(item), f"campos Bell ausentes en {item.get('id')}")
        identifier = item["id"]
        require(identifier not in ids, f"id Bell duplicado: {identifier}")
        ids.add(identifier)
        require(item["source_provenance"], f"procedencia vacía en {identifier}")
        residence = item["primary_residence"]
        require(
            residence["file"]
            == "manuscrito/sections/md/04f_localidad_bell_proyeccion.tex",
            f"residencia Bell incorrecta en {identifier}",
        )
        destination = item["destination"]
        start = int(destination["line_start"])
        end = int(destination["line_end"])
        require(
            destination["exact_locator"]
            == (
                "manuscrito/sections/md/04f_localidad_bell_proyeccion.tex:"
                f"{start}-{end}"
            ),
            f"localizador Bell incoherente en {identifier}",
        )
        require(
            destination["sha256_block"] == block_sha(tex_path, start, end),
            f"bloque Bell alterado en {identifier}",
        )
        label = residence["stable_label"]
        prefix = label.split(":", 1)[0]
        if prefix in {"chap", "sec", "eq", "thm", "cor", "crit"}:
            require(
                f"\\label{{{label}}}" in tex_path.read_text(encoding="utf-8"),
                f"etiqueta Bell ausente: {label}",
            )
        require(
            set(item["proof_status"])
            <= {
                "EXACTO_INTERNO", "RELATIVO_A_PRIMITIVAS",
                "INTERFAZ_FISICA", "PROGRAMA_ABIERTO",
            },
            f"estatuto Bell no canónico en {identifier}",
        )
        for field in (
            "formula_and_all_hypotheses",
            "proof_or_certificate",
            "negative_control_or_falsifier",
            "incorporation_status",
        ):
            require(bool(str(item[field]).strip()), f"{field} vacío en {identifier}")

    require(
        source_cert.get("status") == "PASS_LOCALIDAD_BELL_HMT",
        "certificado Bell base no pasa",
    )
    require(source_cert.get("deterministic_strategies") == 16, "censo Bell distinto")
    require(source_cert.get("chsh_values") == [-2, 2], "valores CHSH distintos")
    require(source_cert.get("chsh_violations") == 0, "violaciones CHSH locales")
    require(source_cert.get("signaling_violations") == 0, "señalización local")
    require(
        source_cert.get("latex_sha256") == sha256(tex_path),
        "el certificado Bell base no corresponde al LaTeX activo",
    )
    require(
        source_cert.get("provenance_sha256") == sha256(provenance_path),
        "el certificado Bell base no corresponde a la procedencia activa",
    )
    require(
        cert.get("status") == "PASS_MATRIZ_CONTROL_BELL_CHSH_EPR",
        "certificado de matriz Bell no pasa",
    )
    require(cert.get("row_count") == len(rows), "conteo en certificado Bell distinto")
    for path in (matrix_path, csv_path, md_path):
        relative = str(path.relative_to(root))
        require(
            cert["artifacts"].get(relative) == sha256(path),
            f"huella Bell incoherente: {relative}",
        )

    own_text = Path(__file__).read_text(encoding="utf-8")
    banned_token = "a" + "ssert("
    require(banned_token not in own_text, "el verificador Bell contiene assert")
    print(
        "PASS_MATRIZ_CONTROL_BELL_CHSH_EPR "
        "rows=16 strategies=16 chsh_values=-2,2 violations=0 signaling=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
