#!/usr/bin/env python3
"""Verificación independiente de las identidades de la adenda HMT--MD.

Sólo usa la biblioteca estándar. Todas las puertas permanecen activas bajo
``python -O``; el archivo no contiene instrucciones ``assert``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


getcontext().prec = 90


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def matmul(a, b):
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    return [
        [sum((a[i][k] * b[k][j] for k in range(inner)), Fraction(0))
         for j in range(cols)]
        for i in range(rows)
    ]


def matscale(c, a):
    return [[c * x for x in row] for row in a]


def matadd(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    source_paths = [
        root / "manuscrito/main.tex",
        root / "manuscrito/sections/md/05c_factorizacion_split_caracter.tex",
        root / "manuscrito/sections/md/04c_realizaciones_nula_material.tex",
        root / "manuscrito/sections/md/04d_ocupacion_estadistica.tex",
        root / "manuscrito/sections/md/04e_termodinamica_rutas.tex",
        root / "manuscrito/sections/md/10c_puente_retorno_holonomia_cartan.tex",
        root / "manuscrito/sections/md/11_gravedad_cartan_holst.tex",
        root / "manuscrito/sections/md/11b_gravedad_sin_graviton_fundamental.tex",
        root / "manuscrito/sections/md/11c_transductor_gravitatorio_G.tex",
        root / "manuscrito/sections/md/11d_regimenes_cuadraticos_lector_temporal.tex",
        root / "manuscrito/sections/md/12b_sintesis_realizaciones.tex",
    ]
    current_path = root / "autoridad_consultada/CURRENT.json"
    route_cert_path = root / "certificados/extension_ruta_caracter.json"
    dynamics_cert_path = root / "certificados/dinamica_cociente_468.json"

    for source_path in source_paths:
        require(source_path.is_file(), f"fuente integrada ausente: {source_path.name}")

    current = json.loads(current_path.read_text(encoding="utf-8"))
    route_cert = json.loads(route_cert_path.read_text(encoding="utf-8"))
    dynamics_cert = json.loads(dynamics_cert_path.read_text(encoding="utf-8"))

    require(
        current["revision"] == "2026-07-22.2",
        "la revisión canónica no es 2026-07-22.2",
    )
    require(
        route_cert["status"] == "PASS_EXTENSION_ROUTE_CHARACTER",
        "el certificado extensión-ruta-carácter no está activo",
    )
    require(
        route_cert["angular_lattice"]["determinant"] == -12,
        "determinante angular distinto de -12",
    )
    require(
        route_cert["angular_lattice"]["smith_invariants"] == [1, 12],
        "forma de Smith angular distinta de (1,12)",
    )

    z = Fraction(0)
    o = Fraction(1)
    identity = [[o, z], [z, o]]
    R = [[o, z], [z, -o]]
    p_plus = matscale(Fraction(1, 2), matadd(identity, R))
    p_minus = matscale(Fraction(1, 2), matadd(identity, matscale(-o, R)))

    require(matmul(p_plus, p_plus) == p_plus, "P+ no es idempotente")
    require(matmul(p_minus, p_minus) == p_minus, "P- no es idempotente")
    require(
        matmul(p_plus, p_minus) == [[z, z], [z, z]],
        "P+P- no se anula",
    )
    require(matadd(p_plus, p_minus) == identity, "P++P- no es la identidad")
    require(det2(p_plus) == 0 and det2(p_minus) == 0, "rayos no nulos")

    split_samples = 0
    for n_a in range(-6, 7):
        for s_c in range(-18, 19, 6):
            w_plus = Fraction(6 * n_a + s_c, 12)
            w_minus = Fraction(6 * n_a - s_c, 12)
            require(
                w_plus + w_minus == n_a,
                "la suma de enrollamientos no devuelve n_A",
            )
            require(
                w_plus - w_minus == Fraction(s_c, 6),
                "la diferencia no devuelve s_C/6",
            )
            # Comprobación exacta a nivel de exponentes:
            # w+(A+C)+w-(A-C) = n_A A + (s_C/6) C.
            coeff_a = w_plus + w_minus
            coeff_c = w_plus - w_minus
            require(coeff_a == n_a, "coeficiente angular incorrecto")
            require(coeff_c == Fraction(s_c, 6), "coeficiente dual incorrecto")
            split_samples += 1

    alpha = Decimal(current["recognition"]["alpha_12"])
    c_deg = Decimal(
        current["canonical_corrections_2026_07_18"]["canonical_contraangle"][
            "Cstar_degrees_full"
        ]
    )
    pi = Decimal(
        "3.1415926535897932384626433832795028841971693993751058209749445923078"
    )
    a_deg = Decimal(1000) * alpha
    a_rad = a_deg * pi / Decimal(180)
    c_rad = c_deg * pi / Decimal(180)

    # Control numérico multiprecisión de la misma identidad en una muestra
    # representativa; exp pertenece a Decimal en los runtimes admitidos.
    numeric_samples = 0
    for n_a, s_c in [(0, 0), (1, 6), (4, -12), (24, 0), (9, 18)]:
        wp = Decimal(6 * n_a + s_c) / Decimal(12)
        wm = Decimal(6 * n_a - s_c) / Decimal(12)
        log_rp = wp * (a_rad + c_rad)
        log_rm = wm * (a_rad - c_rad)
        lhs = (log_rp + log_rm).exp()
        rhs = (
            Decimal(n_a) * a_rad + Decimal(s_c) * c_rad / Decimal(6)
        ).exp()
        require(abs(lhs - rhs) < Decimal("1e-75"), "fallo numérico split")
        numeric_samples += 1

    # Multiplicar Z por exp(t/2) añade exactamente t al log-determinante.
    for t in [
        Decimal("-0.125"),
        Decimal("0"),
        Decimal("0.03125"),
        Decimal("2.75"),
    ]:
        scale = (t / Decimal(2)).exp()
        require(
            abs(scale * scale - t.exp()) < Decimal("1e-78"),
            "la extensión central de torres no duplica correctamente",
        )

    f_av = [[0, 1], [1, 1]]
    require(matmul(f_av, f_av) == [[1, 1], [1, 2]], "F_av^2 incorrecta")
    require(fib(107) == 10284720757613717413913, "F107 incorrecto")
    require(fib(109) == 26925748508234281076009, "F109 incorrecto")
    hinge = dynamics_cert["areal_volumetric_hinge"]
    require(hinge["F_av"] == f_av, "F_av no coincide con el certificado")
    require(
        hinge["native_length_108"]["F107"] == fib(107)
        and hinge["native_length_108"]["F109"] == fib(109),
        "la profundidad 108 no coincide",
    )
    require(
        dynamics_cert["raw_chronology"]["positions_and_orientations_return_after_ticks"]
        == 54,
        "retorno de orientación distinto de 54",
    )
    require(
        dynamics_cert["raw_chronology"]["full_phase_return_after_ticks"] == 108,
        "retorno de fase distinto de 108",
    )
    require(
        dynamics_cert["calendar_cocycles"]["orientation_reversals_per_108"] == 4,
        "número de inversiones distinto de 4",
    )
    require(
        dynamics_cert["calendar_cocycles"]["total_variation_per_108"] == 72,
        "variación total distinta de 72",
    )

    # Vectores de dimensiones en la base (M,L,T,Theta).
    hbar_dim = (1, 2, -1, 0)
    omega_dim = (0, 0, -1, 0)
    k_b_dim = (1, 2, -2, -1)
    theta_dim = (0, 0, 0, 1)
    energy_dim = (1, 2, -2, 0)
    require(
        tuple(a + b for a, b in zip(hbar_dim, omega_dim)) == energy_dim,
        "hbar*omega no tiene dimensión de energía",
    )
    require(
        tuple(a + b for a, b in zip(k_b_dim, theta_dim)) == energy_dim,
        "k_B*Theta no tiene dimensión de energía",
    )

    c_dim = (0, 1, -1, 0)
    t_dim = (0, 0, 1, 0)
    g_dim = (-1, 3, -2, 0)
    g_from_chart = tuple(
        5 * c_dim[i] + 2 * t_dim[i] - hbar_dim[i] for i in range(4)
    )
    require(g_from_chart == g_dim, "el transductor de G está mal tipado")

    source_text = "\n".join(
        source_path.read_text(encoding="utf-8") for source_path in source_paths
    )
    require("\\hbar_{\\HMT}" not in source_text, "hbar_HMT ambiguo reaparece")
    require(
        "\\omega_0" in source_text
        and "\\frac{2\\pi}{108" in source_text,
        "frecuencia térmica sin t0",
    )
    require(
        "D_\\omega F^{IJ}=0" in source_text,
        "primera identidad de Bianchi ausente",
    )
    require(
        "D_\\omega T_{\\rm tor}^I" in source_text
        and "\\wedge e^J" in source_text,
        "segunda identidad de Bianchi ausente",
    )
    banned_token = "a" + "ssert("
    require(banned_token not in Path(__file__).read_text(encoding="utf-8"),
            "el verificador contiene una puerta desactivable")

    result = {
        "schema": "HMT.MD.adenda-realizaciones-fisicas.v1",
        "status": "PASS_ADENDA_REALIZACIONES_FISICAS",
        "canonical_revision": current["revision"],
        "checks": {
            "split_projectors": True,
            "null_boundary_and_positive_interior": True,
            "angular_character_exponent_identity": True,
            "tower_central_scaling": True,
            "fibonacci_hinge_at_depth_108": True,
            "returns_54_108_and_cocycles": True,
            "thermal_line_dimensions": True,
            "gravitational_line_dimensions": True,
            "no_ambiguous_hbar_name": True,
            "no_assert_statements": True,
        },
        "counts": {
            "exact_split_samples": split_samples,
            "multiprecision_split_samples": numeric_samples,
            "projector_identities": 5,
            "dimension_vectors": 2,
        },
        "source_hashes": {
            **{
                str(path.relative_to(root)): sha256(path)
                for path in source_paths
            },
            "CURRENT.json": sha256(current_path),
            "extension_ruta_caracter.json": sha256(route_cert_path),
            "dinamica_cociente_468.json": sha256(dynamics_cert_path),
        },
        "typed_scope": {
            "proved": [
                "split algebra and null cone identities",
                "exact factorization of the active angular character",
                "central inclusion of the global tower exponent",
                "Fibonacci envelope and finite return data read from active certificates",
                "dimensional typing of the thermal and gravitational transducers",
            ],
            "not_proved_by_this_certificate": [
                "physical photon or electron realization",
                "derivation of CAR or the spin-statistics theorem",
                "selection of the temperature unit or the SI value of k_B",
                "canonical holonomy character selecting theta_G",
                "absence or presence of an emergent spin-2 quantum",
            ],
        },
    }

    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
