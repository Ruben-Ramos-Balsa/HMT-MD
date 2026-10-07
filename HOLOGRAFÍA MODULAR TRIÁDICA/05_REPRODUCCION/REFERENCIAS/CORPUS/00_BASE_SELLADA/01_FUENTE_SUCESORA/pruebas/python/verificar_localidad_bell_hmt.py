#!/usr/bin/env python3
"""Puerta finita para CHSH local y el tipado Bell/HMT del manuscrito."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEX = ROOT / "manuscrito/sections/md/04f_localidad_bell_proyeccion.tex"
PROVENANCE = ROOT / "datos/bell_hmt/procedencia_bell_hmt.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL_LOCALIDAD_BELL_HMT: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    for path in (TEX, PROVENANCE):
        if not path.is_file():
            fail(f"falta {path.relative_to(ROOT)}")

    source = TEX.read_text(encoding="utf-8")
    required = (
        r"\label{eq:factorizacion-bell-local}",
        r"\label{eq:funcional-chsh}",
        r"\label{thm:cota-chsh-local}",
        r"\label{eq:cota-chsh-dos}",
        r"\label{eq:no-senalizacion-bell}",
        r"\label{thm:no-promocion-bell-por-proyeccion}",
        r"\label{eq:cambio-base-informacion-bell}",
        r"\label{eq:programa-bell-hmt}",
        r"\label{crit:bell-localidad-no-localidad}",
        r"v=(1,1)",
        r"p\geq\kappa/H",
        r"\cref{def:escala-termica-triadica}",
        r"interfaz HMT aún",
        r"ausente.",
    )
    missing = [token for token in required if token not in source]
    if missing:
        fail("contrato LaTeX incompleto: " + ", ".join(missing))

    strategies = []
    violations = []
    signaling_violations = []
    for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4):
        correlations = {
            "E00": a0 * b0,
            "E01": a0 * b1,
            "E10": a1 * b0,
            "E11": a1 * b1,
        }
        value = (
            correlations["E00"]
            + correlations["E01"]
            + correlations["E10"]
            - correlations["E11"]
        )
        row = {
            "A0": a0,
            "A1": a1,
            "B0": b0,
            "B1": b1,
            "S_CHSH": value,
        }
        strategies.append(row)
        if abs(value) > 2:
            violations.append(row)

        responses_a = (a0, a1)
        responses_b = (b0, b1)
        marginals_a = {
            (a, b): responses_a[a] for a in (0, 1) for b in (0, 1)
        }
        marginals_b = {
            (a, b): responses_b[b] for a in (0, 1) for b in (0, 1)
        }
        no_signal_a = all(
            marginals_a[(a, 0)] == marginals_a[(a, 1)] for a in (0, 1)
        )
        no_signal_b = all(
            marginals_b[(0, b)] == marginals_b[(1, b)] for b in (0, 1)
        )
        if not (no_signal_a and no_signal_b):
            signaling_violations.append(row)

    if len(strategies) != 16:
        fail(f"censo determinista inesperado: {len(strategies)}")
    if violations:
        fail(f"violaciones CHSH locales: {len(violations)}")
    if signaling_violations:
        fail(f"violaciones de no señalización: {len(signaling_violations)}")

    values = sorted({row["S_CHSH"] for row in strategies})
    if values != [-2, 2]:
        fail(f"espectro CHSH inesperado: {values}")

    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    if provenance.get("schema") != "HMT_MD_BELL_PROVENANCE_V1":
        fail("schema de procedencia incorrecto")
    sources = provenance.get("sources", [])
    if len(sources) != 6:
        fail("procedencia arqueológica incompleta")
    required_hashes = {
        "26164a15800721a8f0fc6859ecc47329e8c771517fc81f0a74fece8c4a9f2657",
        "5444aeea0d5a7ad6ce8bac2a50af1044682adc71746beeedc55ff918102af0c2",
        "bb13634c978bfb62189d47347bfb0fc1e6bdcf82d32008cacdc934d349b77553",
    }
    observed_hashes = {item.get("sha256") for item in sources}
    if not required_hashes <= observed_hashes:
        fail("faltan autoridades o refutaciones históricas vinculantes")

    payload = {
        "status": "PASS_LOCALIDAD_BELL_HMT",
        "proof_status": "FORMALIZACION_NUEVA_CERTIFICADO_NUEVO",
        "deterministic_strategies": len(strategies),
        "chsh_values": values,
        "max_abs_chsh": max(abs(row["S_CHSH"]) for row in strategies),
        "chsh_violations": len(violations),
        "signaling_violations": len(signaling_violations),
        "hypotheses": [
            "LOCAL_FACTORIZATION",
            "MEASUREMENT_INDEPENDENCE",
            "NORMALIZATION",
            "NO_CONTEXTUAL_POSTSELECTION",
        ],
        "hmt_physical_realization": "PROGRAMA_ABIERTO",
        "latex_sha256": sha256(TEX),
        "provenance_sha256": sha256(PROVENANCE),
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
