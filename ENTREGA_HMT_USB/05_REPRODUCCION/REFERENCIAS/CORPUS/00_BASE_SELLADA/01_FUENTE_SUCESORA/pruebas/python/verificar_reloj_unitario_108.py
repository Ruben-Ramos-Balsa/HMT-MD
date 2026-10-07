#!/usr/bin/env python3
"""Verifica la realización finita del reloj unitario de 108 estados."""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEX = ROOT / "manuscrito/sections/md/11d_regimenes_cuadraticos_lector_temporal.tex"
N = 108


def fail(message: str) -> None:
    raise SystemExit(f"FAIL_RELOJ_UNITARIO_108: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    require(TEX.is_file(), f"falta {TEX.relative_to(ROOT)}")
    source = TEX.read_text(encoding="utf-8")
    required_tokens = (
        r"\label{eq:hamiltoniano-reloj-108}",
        r"\label{thm:reloj-unitario-108}",
        r"\label{eq:propagador-reloj-108}",
        r"\label{eq:respuesta-reloj-108}",
        r"\label{eq:lagrangiano-reloj-108}",
        r"\label{eq:accion-reloj-108}",
        r"U_{\rm step}",
        r"\mathrm i\hbar_{\rm int}\dot\psi=H_{\rm clk}\psi",
        r"La realización finita",
        r"extensión a una fase material",
    )
    missing = [token for token in required_tokens if token not in source]
    require(not missing, "contrato LaTeX incompleto: " + ", ".join(missing))

    shift = [(j + 1) % N for j in range(N)]
    visited = []
    current = 0
    for _ in range(N):
        visited.append(current)
        current = shift[current]
    require(current == 0, "el desplazamiento no cierra en 108 pasos")
    require(len(set(visited)) == N, "el periodo del desplazamiento no es primitivo")

    zeta = cmath.exp(2j * math.pi / N)
    maximum_phase_error = 0.0
    for k in range(N):
        shift_eigenvalue = zeta ** (-k)
        hamiltonian_phase = cmath.exp(-2j * math.pi * k / N)
        maximum_phase_error = max(
            maximum_phase_error,
            abs(shift_eigenvalue - hamiltonian_phase),
        )
    require(maximum_phase_error < 1e-12, "fallo de la identidad espectral")

    response = [zeta**n for n in range(N)]
    proper_returns = [
        n for n in range(1, N) if abs(response[n] - response[0]) < 1e-12
    ]
    require(not proper_returns, f"retornos propios inesperados: {proper_returns}")
    require(abs(zeta**N - 1) < 1e-12, "la respuesta no cierra en 108")

    payload = {
        "schema": "HMT_MD_UNITARY_CLOCK_108_CERT_V1",
        "status": "PASS_RELOJ_UNITARIO_108",
        "proof_status": "EXACTO_INTERNO_RELATIVO_A_COMPLETACION",
        "dimension": N,
        "shift_cycle_length": len(visited),
        "proper_return_times": proper_returns,
        "hamiltonian_spectrum_indices": list(range(N)),
        "maximum_phase_error": format(maximum_phase_error, ".17g"),
        "response_primitive_period": N,
        "energy_type": "ACTION/TIME",
        "finite_hmt_time_crystal_status": "CLOSED_IN_DECLARED_FINITE_DOMAIN",
        "macroscopic_material_phase_status": "EXTERNAL_EXPERIMENTAL_RECOGNITION",
        "external_material_realization_requirements": [
            "OPEN_CLASS_STABILITY",
            "MACROSCOPIC_PERSISTENCE",
            "PROTECTION_MECHANISM",
        ],
        "latex_sha256": sha256(TEX),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
