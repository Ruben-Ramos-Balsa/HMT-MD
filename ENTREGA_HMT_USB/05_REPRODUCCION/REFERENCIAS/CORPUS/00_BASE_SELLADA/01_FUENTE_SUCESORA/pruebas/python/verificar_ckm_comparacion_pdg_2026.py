#!/usr/bin/env python3
"""Verifica la tabla CKM externa sin convertirla en entrada del generador."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HMT = ROOT / "datos/HMT_CKM_angular_torsional_values_v14.json"
HMT_CERT = ROOT / "certificados/CERTIFICADO_MD_CORE.json"
EXTERNAL = ROOT / "datos/ckm_comparacion_pdg_2026.json"
TEX = ROOT / "manuscrito/sections/md/08_ckm_cp.tex"

EXPECTED_EXTERNAL_SOURCE = {
    "institution": "Particle Data Group",
    "title": "CKM Quark-Mixing Matrix",
    "revision": "March 2026",
    "file_version": "2026-06-01",
    "url": "https://pdg.lbl.gov/2026/reviews/rpp2026-rev-ckm-matrix.pdf",
    "pdf_bytes": 512111,
    "pdf_sha256": "c6b23ae8572345c3ab739e233ea47a25e879f8534c9021a10e9ca1bd3bb8d433",
    "location": "paragraph preceding and equation (12.28), page 13 of the review",
}
EXPECTED_EXTERNAL_PARAMETERS = {
    "sin_theta12": {"central": "0.22517", "minus": "0.00068", "plus": "0.00068"},
    "sin_theta23": {"central": "0.04189", "minus": "0.00069", "plus": "0.00081"},
    "sin_theta13": {"central": "0.003763", "minus": "0.000083", "plus": "0.000088"},
    "delta_rad": {"central": "1.154", "minus": "0.025", "plus": "0.025"},
    "J": {"central": "0.0000316", "minus": "0.0000011", "plus": "0.0000013"},
}
EXPECTED_HMT_PARAMETERS = {
    "theta12_deg": "13.003313589509013",
    "theta23_deg": "2.3980561573315993",
    "theta13_deg": "0.21397738224350707",
    "delta_deg": "65.67617312355422",
    "J": "0.000031189723326632974",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL_CKM_COMPARACION_PDG_2026: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def signed_residual(value: float, central: float, minus: float, plus: float) -> float:
    sigma = minus if value < central else plus
    return (value - central) / sigma


def main() -> None:
    for path in (HMT, HMT_CERT, EXTERNAL, TEX):
        require(path.is_file(), f"falta {path.relative_to(ROOT)}")

    hmt = json.loads(HMT.read_text(encoding="utf-8"))
    hmt_cert = json.loads(HMT_CERT.read_text(encoding="utf-8"))
    external = json.loads(EXTERNAL.read_text(encoding="utf-8"))
    require(
        external.get("schema") == "HMT_MD_CKM_EXTERNAL_COMPARISON_V1",
        "schema externo incorrecto",
    )
    require(
        external["interpretive_limits"]["used_as_generator_input"] is False,
        "la fuente externa no puede ser entrada del generador",
    )
    require(
        external["interpretive_limits"]["covariance_packaged"] is False,
        "no debe fingirse una covarianza no empaquetada",
    )
    for key, expected in EXPECTED_EXTERNAL_SOURCE.items():
        require(
            external["external_source"].get(key) == expected,
            f"procedencia externa alterada: {key}",
        )
    require(
        external["external_parameters"] == EXPECTED_EXTERNAL_PARAMETERS,
        "parámetros oficiales PDG alterados",
    )
    require(
        external["hmt_certified_parameters"] == EXPECTED_HMT_PARAMETERS,
        "parámetros HMT certificados alterados",
    )
    require(
        external["hmt_source"].get("numeric_note")
        == (
            "Its J field is the inherited binary64 projection; the decimal value "
            "in hmt_certified_parameters and CERTIFICADO_MD_CORE.json is "
            "authoritative for publication."
        ),
        "falta documentar la proyección binary64 heredada de J",
    )
    require(
        hmt_cert.get("J") == "3.1189723326632974e-05",
        "el certificado nuclear no conserva J con la precisión publicada",
    )
    require(
        math.isclose(
            float(hmt["J"]),
            float(EXPECTED_HMT_PARAMETERS["J"]),
            rel_tol=0.0,
            abs_tol=2e-18,
        ),
        "la proyección binary64 heredada de J no aproxima el valor certificado",
    )

    parameters = external["external_parameters"]
    certified = external["hmt_certified_parameters"]
    hmt_values = {
        "theta12_deg": float(certified["theta12_deg"]),
        "theta23_deg": float(certified["theta23_deg"]),
        "theta13_deg": float(certified["theta13_deg"]),
        "delta_deg": float(certified["delta_deg"]),
        "J": float(certified["J"]),
    }
    for source_key, certified_key in (
        ("theta12_deg", "theta12_deg"),
        ("theta23_deg", "theta23_deg"),
        ("theta13_deg", "theta13_deg"),
        ("delta_CKM_deg", "delta_deg"),
    ):
        require(
            math.isclose(
                float(hmt[source_key]),
                float(certified[certified_key]),
                rel_tol=0.0,
                abs_tol=5e-15,
            ),
            f"fuente HMT incompatible: {source_key}",
        )

    conversions: dict[str, dict[str, float]] = {}
    for key in ("12", "23", "13"):
        item = parameters[f"sin_theta{key}"]
        central = math.degrees(math.asin(float(item["central"])))
        lower = central - math.degrees(
            math.asin(float(item["central"]) - float(item["minus"]))
        )
        upper = math.degrees(
            math.asin(float(item["central"]) + float(item["plus"]))
        ) - central
        value = hmt_values[f"theta{key}_deg"]
        conversions[f"theta{key}_deg"] = {
            "hmt": value,
            "external_central": central,
            "external_minus": lower,
            "external_plus": upper,
            "signed_residual": signed_residual(value, central, lower, upper),
        }

    delta = parameters["delta_rad"]
    delta_central = math.degrees(float(delta["central"]))
    delta_minus = math.degrees(float(delta["minus"]))
    delta_plus = math.degrees(float(delta["plus"]))
    conversions["delta_deg"] = {
        "hmt": hmt_values["delta_deg"],
        "external_central": delta_central,
        "external_minus": delta_minus,
        "external_plus": delta_plus,
        "signed_residual": signed_residual(
            hmt_values["delta_deg"], delta_central, delta_minus, delta_plus
        ),
    }

    j_item = parameters["J"]
    conversions["J"] = {
        "hmt": hmt_values["J"],
        "external_central": float(j_item["central"]),
        "external_minus": float(j_item["minus"]),
        "external_plus": float(j_item["plus"]),
        "signed_residual": signed_residual(
            hmt_values["J"],
            float(j_item["central"]),
            float(j_item["minus"]),
            float(j_item["plus"]),
        ),
    }

    expected_rounded = {
        "theta12_deg": -0.24,
        "theta23_deg": -0.07,
        "theta13_deg": -0.34,
        "delta_deg": -0.31,
        "J": -0.37,
    }
    for key, expected in expected_rounded.items():
        observed = round(conversions[key]["signed_residual"], 2)
        require(observed == expected, f"residuo {key}: {observed} != {expected}")

    source = TEX.read_text(encoding="utf-8")
    required_tokens = (
        r"\label{tab:comparacion-angular-ckm-pdg-2026}",
        r"\textsc{reconocimiento externo}",
        r"\chi^2",
        "covarianza",
        "PDGCKM2026",
    )
    table_numeric_tokens = (
        r"\(13.00331359\)",
        r"\(13.01287\pm0.03999\)",
        r"\(-0.24\)",
        r"\(2.39805616\)",
        r"\(2.40082^{+0.04645}_{-0.03957}\)",
        r"\(-0.07\)",
        r"\(0.21397738\)",
        r"\(0.215605^{+0.005042}_{-0.004756}\)",
        r"\(-0.34\)",
        r"\(65.67617312\)",
        r"\(66.1193\pm1.4324\)",
        r"\(-0.31\)",
        r"\(3.11897233\)",
        r"\(3.16^{+0.13}_{-0.11}\)",
        r"\(-0.37\)",
    )
    missing = [token for token in required_tokens if token not in source]
    missing.extend(token for token in table_numeric_tokens if token not in source)
    require(not missing, "tabla LaTeX incompleta: " + ", ".join(missing))

    payload = {
        "schema": "HMT_MD_CKM_EXTERNAL_COMPARISON_CERT_V1",
        "status": "PASS_CKM_COMPARACION_PDG_2026",
        "proof_status": "RECONOCIMIENTO_EXTERNO",
        "comparison_is_generator_input": False,
        "covariance_packaged": False,
        "marginal_residuals": conversions,
        "external_pdf_sha256": external["external_source"]["pdf_sha256"],
        "legacy_binary64_J": hmt["J"],
        "certified_decimal_J": EXPECTED_HMT_PARAMETERS["J"],
        "hmt_data_sha256": sha256(HMT),
        "hmt_certificate_sha256": sha256(HMT_CERT),
        "external_data_sha256": sha256(EXTERNAL),
        "latex_sha256": sha256(TEX),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
