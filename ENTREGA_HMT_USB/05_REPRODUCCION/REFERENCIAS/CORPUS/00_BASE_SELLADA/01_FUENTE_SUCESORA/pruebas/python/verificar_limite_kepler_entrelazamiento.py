#!/usr/bin/env python3
"""Puerta finita del límite central, holonomía y entropía bicapa."""

from __future__ import annotations

import cmath
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KEPLER = ROOT / "manuscrito/sections/md/11f_limite_central_kepler_sommerfeld.tex"
LAYERS = ROOT / "manuscrito/sections/md/04c_realizaciones_nula_material.tex"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL_LIMITE_KEPLER_ENTRELAZAMIENTO: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def gauss_test() -> tuple[Fraction, Fraction]:
    vertices = tuple(range(6))
    undirected_edges = ((0, 1), (0, 3), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5))
    values = {
        edge: Fraction((17 * edge[0] + 11 * edge[1] + 3) % 13 - 6, 7)
        for edge in undirected_edges
    }

    def field(x: int, y: int) -> Fraction:
        if (x, y) in values:
            return values[(x, y)]
        if (y, x) in values:
            return -values[(y, x)]
        return Fraction(0)

    subset = {0, 1, 3}
    divergence_sum = sum(
        (sum((field(x, y) for y in vertices), Fraction(0)) for x in subset),
        Fraction(0),
    )
    boundary_flux = sum(
        (
            field(x, y)
            for x in subset
            for y in vertices
            if y not in subset
        ),
        Fraction(0),
    )
    return divergence_sum, boundary_flux


def shell_count(radius: int) -> int:
    points = range(-radius, radius + 1)
    cube = {(x, y, z) for x in points for y in points for z in points}
    directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    return sum(
        (x + dx, y + dy, z + dz) not in cube
        for x, y, z in cube
        for dx, dy, dz in directions
    )


def main() -> None:
    for path in (KEPLER, LAYERS):
        require(path.is_file(), f"falta {path.relative_to(ROOT)}")

    kepler_source = KEPLER.read_text(encoding="utf-8")
    layers_source = LAYERS.read_text(encoding="utf-8")
    required_kepler = (
        r"\label{thm:gauss-grafo-hmt-md}",
        r"\label{eq:inverso-area-cascaron}",
        r"\label{eq:lagrangiano-hamiltoniano-kepler}",
        r"\label{prop:conica-kepleriana-hmt-md}",
        r"\label{eq:cubierta-levi-civita}",
        r"\label{thm:periodo-orientado-banda-orbital}",
        r"\label{eq:cierre-fase-holonomia-sommerfeld}",
        r"\label{prop:desplazamiento-sommerfeld-holonomia}",
        r"\label{crit:limite-kepler-sommerfeld}",
        "índices de Maslov",
        r"R\in\mathbb Z_{\geq0}",
        r"A_{\rm ell}=\pi ab",
        r"[\mathcal K]=\mathsf E\,\mathsf L",
    )
    required_layers = (
        r"\label{eq:estado-entrelazado-ida-retorno}",
        r"\label{prop:entropia-entrelazamiento-ida-retorno}",
        r"\label{eq:entropia-ida-retorno}",
        "interfaz física",
        "caso determinista",
        r"0\log0:=0",
        r"\textsc{demostrada con estructura de partida explícita}",
    )
    missing = [token for token in required_kepler if token not in kepler_source]
    missing.extend(token for token in required_layers if token not in layers_source)
    require(not missing, "contrato LaTeX incompleto: " + ", ".join(missing))

    divergence_sum, boundary_flux = gauss_test()
    require(divergence_sum == boundary_flux, "falla Gauss en el grafo testigo")

    shell_counts = {radius: shell_count(radius) for radius in range(5)}
    expected_shell_counts = {
        radius: 6 * (2 * radius + 1) ** 2 for radius in range(5)
    }
    require(shell_counts == expected_shell_counts, "falla el censo del cascarón")

    coupling = 7.0
    reduced_mass = 3.0
    angular_momentum = 2.0
    scale = coupling / (reduced_mass * angular_momentum**2)
    eccentricity = 0.41
    phase = 0.37
    maximum_binet_residual = 0.0
    for sample in range(721):
        angle = 2 * math.pi * sample / 720
        u = scale * (1 + eccentricity * math.cos(angle - phase))
        u_second = -scale * eccentricity * math.cos(angle - phase)
        maximum_binet_residual = max(
            maximum_binet_residual,
            abs(u_second + u - scale),
        )
    require(maximum_binet_residual < 1e-14, "falla la cónica de Binet")

    semimajor_axis = 5.0
    orbital_eccentricity = 0.37
    semiminor_axis = semimajor_axis * math.sqrt(1 - orbital_eccentricity**2)
    semilatus_rectum = semimajor_axis * (1 - orbital_eccentricity**2)
    specific_angular_momentum = math.sqrt(
        coupling * semilatus_rectum / reduced_mass
    )
    period_from_area = (
        2 * math.pi * semimajor_axis * semiminor_axis
        / specific_angular_momentum
    )
    period_squared_expected = (
        4 * math.pi**2 * reduced_mass * semimajor_axis**3 / coupling
    )
    kepler_third_law_relative_error = abs(
        period_from_area**2 - period_squared_expected
    ) / period_squared_expected
    require(
        kepler_third_law_relative_error < 2e-15,
        "falla la tercera ley de Kepler",
    )

    holonomy_phase_errors = []
    for integer in range(-3, 4):
        for epsilon, offset in ((1, 0.0), (-1, 0.5)):
            action_over_hbar = 2 * math.pi * (integer + offset)
            closure = epsilon * cmath.exp(1j * action_over_hbar)
            holonomy_phase_errors.append(abs(closure - 1))
    require(max(holonomy_phase_errors) < 1e-14, "falla el cierre de holonomía")

    probabilities = (0.5, 0.3, 0.2)
    entropy = -sum(p * math.log(p) for p in probabilities)
    require(entropy > 0, "la entropía no es positiva")
    deterministic_entropy = -sum(
        p * math.log(p) for p in (1.0, 0.0, 0.0) if p > 0
    )
    require(deterministic_entropy == 0.0, "falla el control separable")
    deterministic_entropy = 0.0

    amplitudes = [
        [
            math.sqrt(probabilities[i]) if i == j else 0.0
            for j in range(len(probabilities))
        ]
        for i in range(len(probabilities))
    ]
    rho_advanced = [
        [
            sum(amplitudes[i][k] * amplitudes[j][k] for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]
    rho_retarded = [
        [
            sum(amplitudes[k][i] * amplitudes[k][j] for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]
    expected_reduced = [
        [probabilities[i] if i == j else 0.0 for j in range(3)]
        for i in range(3)
    ]
    reduced_error = max(
        abs(observed[i][j] - expected_reduced[i][j])
        for observed in (rho_advanced, rho_retarded)
        for i in range(3)
        for j in range(3)
    )
    require(reduced_error < 1e-15, "fallan las matrices reducidas")
    schmidt_rank = sum(p > 0 for p in probabilities)
    deterministic_schmidt_rank = sum(p > 0 for p in (1.0, 0.0, 0.0))
    require(schmidt_rank == 3, "rango de Schmidt no determinista incorrecto")
    require(
        deterministic_schmidt_rank == 1,
        "el control determinista no tiene rango de Schmidt uno",
    )

    payload = {
        "schema": "HMT_MD_KEPLER_ENTANGLEMENT_CERT_V1",
        "status": "PASS_LIMITE_KEPLER_ENTRELAZAMIENTO",
        "gauss_graph": {
            "divergence_sum": str(divergence_sum),
            "boundary_flux": str(boundary_flux),
            "equal": True,
        },
        "shell_counts": shell_counts,
        "binet_maximum_residual": format(maximum_binet_residual, ".17g"),
        "kepler_third_law_relative_error": format(
            kepler_third_law_relative_error, ".17g"
        ),
        "holonomy_maximum_phase_error": format(max(holonomy_phase_errors), ".17g"),
        "entanglement_entropy_test": format(entropy, ".17g"),
        "deterministic_entropy": format(deterministic_entropy, ".1f"),
        "reduced_density_maximum_error": format(reduced_error, ".17g"),
        "schmidt_rank_test": schmidt_rank,
        "deterministic_schmidt_rank": deterministic_schmidt_rank,
        "proof_status": {
            "graph_gauss": "EXACTO_INTERNO",
            "inverse_area": "RELATIVO_A_ISOTROPIA",
            "kepler_dynamics": "INTERFAZ_FISICA",
            "mobius_holonomy": "EXACTO_INTERNO",
            "sommerfeld_shift": "RELATIVO_A_FASE_SEMICLASICA",
            "formal_bilayer_entropy": "RELATIVO_A_PRIMITIVAS",
            "physical_entanglement": "INTERFAZ_FISICA",
        },
        "kepler_latex_sha256": sha256(KEPLER),
        "layers_latex_sha256": sha256(LAYERS),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
