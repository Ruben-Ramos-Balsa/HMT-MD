#!/usr/bin/env python3
"""Auditoría de los tres usos documentados de «dos vías» en HMT.

1. Reconstrucción exacta del sello K por Hadamard y por (D3,D4,Q).
2. Evaluación exacta del acarreo dados K y las tres palabras de entrada.
3. Control analítico E21/22 por inversión de la ecuación de vacancias.

La tercera pieza verifica la raíz del kernel fijado; no pretende derivar aquí
los coeficientes de ese kernel. Sólo usa la biblioteca estándar de Python.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path


K_EXPECTED = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
U = (2378, 1406, 2479, -452, 998, -551, -668, -204, -371, -322, -28, -997)
D3 = (-495, -116, -684, 108, 601, -90, -173, -88, 313, 560, -397, 461)
D4 = (-425, -281, -481, 671, -255, 30, 475, -543, 680, 251, 6, -128)
Q = 6263

PI_TRIADS = (141, 592, 653, 589, 793, 238, 462, 643, 383, 279, 502, 884)
E_TRIADS = (718, 281, 828, 459, 45, 235, 360, 287, 471, 352, 662, 497)
PHI_TRIADS = (618, 33, 988, 749, 894, 848, 204, 586, 834, 365, 638, 117)
ALPHA_TRIADS = (7, 297, 352, 569, 283, 800, 997, 285, 105, 472, 380, 663)

H4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"HMT ALPHA FAIL: {message}")


def mat_vec(matrix, vector):
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def k_from_hadamard():
    blocks = (U[0::3], U[1::3], U[2::3])
    k_blocks = []
    for block in blocks:
        transformed = mat_vec(H4, block)
        require(all(value % 4 == 0 for value in transformed),
                "la inversa Hadamard no es entera")
        k_blocks.append(tuple(value // 4 for value in transformed))
    return tuple(k_blocks[r][j] for j in range(4) for r in range(3))


def k_from_differences():
    values: list[int | None] = [None] * 12
    values[0] = 0
    pending = [0]
    while pending:
        m = pending.pop()
        require(values[m] is not None, "potencial transversal indefinido")
        for step, border in ((3, D3), (4, D4)):
            nxt = (m + step) % 12
            candidate = values[m] - border[m]
            if values[nxt] is None:
                values[nxt] = candidate
                pending.append(nxt)
            else:
                require(values[nxt] == candidate,
                        "inconsistencia en la integración D3/D4")
    base = tuple(int(value) for value in values if value is not None)
    shift = Fraction(Q - sum(base), 12)
    require(shift.denominator == 1, "Q no fija una traslación entera")
    return tuple(value + shift.numerator for value in base)


def alpha_by_carry(k):
    digits = [0] * 12
    carries = [0] * 13
    for m in range(11, -1, -1):
        raw = PI_TRIADS[m] + E_TRIADS[m] - PHI_TRIADS[m] - k[m] + carries[m + 1]
        digits[m] = raw % 1000
        carries[m] = (raw - digits[m]) // 1000
    return tuple(digits), tuple(carries)


def pi_chudnovsky(precision: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision + 30
        constant = Decimal(426880) * Decimal(10005).sqrt()
        m, ell, x, kk = 1, 13591409, 1, 6
        series = Decimal(ell)
        for n in range(1, precision // 14 + 5):
            m = (m * (kk**3 - 16 * kk)) // (n**3)
            ell += 545140134
            x *= -262537412640768000
            series += Decimal(m * ell) / Decimal(x)
            kk += 12
        return +(constant / series)


def vacancy_root():
    with localcontext() as ctx:
        ctx.prec = 90
        one = Decimal(1)
        pi = pi_chudnovsky(85)
        epsilon = (Decimal(10) / Decimal(9)).ln() / Decimal(10).ln()

        def polynomial(x):
            return (
                2 * pi * x
                - Decimal(7) * x**2 / 4
                + x**3 / (2 * pi)
                + x**4 / 20
                - Decimal(2) * x**5 / 21
                - x**6 / 46
            )

        def derivative(x):
            return (
                2 * pi
                - Decimal(7) * x / 2
                + Decimal(3) * x**2 / (2 * pi)
                + x**3 / 5
                - Decimal(10) * x**4 / 21
                - Decimal(6) * x**5 / 46
            )

        root = epsilon / (2 * pi)
        for _ in range(20):
            root -= (polynomial(root) - epsilon) / derivative(root)
        residual = polynomial(root) - epsilon
        alpha_text = "0." + "".join(f"{value:03d}" for value in ALPHA_TRIADS)
        alpha_hmt = Decimal(alpha_text)
        hmt_residual = polynomial(alpha_hmt) - epsilon
        return {
            "epsilon_vac": str(+epsilon),
            "positive_small_root": str(+root),
            "root_inverse": str(+(one / root)),
            "newton_residual": str(+residual),
            "alpha_hmt": alpha_text,
            "alpha_hmt_inverse": str(+(one / alpha_hmt)),
            "kernel_residual_at_alpha_hmt": str(+hmt_residual),
            "inverse_difference": str(+(one / root - one / alpha_hmt)),
        }


def main():
    k_h = k_from_hadamard()
    k_e = k_from_differences()
    require(k_h == k_e == K_EXPECTED,
            "las reconstrucciones del sello no coinciden")
    digits, carries = alpha_by_carry(k_h)
    require(digits == ALPHA_TRIADS, "el acarreo condicionado no coincide")

    high_face = tuple(i + 1 for i, value in enumerate(k_h) if value >= 729)
    he = {1, 3, 4, 6, 9, 10}
    ppi = {2, 4, 5, 6, 7, 8, 9, 10, 11}
    require(high_face == tuple(sorted(he & ppi)) == (4, 6, 9, 10),
            "falla la doble descripción de B_K")
    h_alpha = tuple(sorted(set(high_face) | {5, 7}))
    require(h_alpha == (4, 5, 6, 7, 9, 10),
            "falla la extensión a H_alpha")

    result = {
        "schema": "HMT.alpha_dos_vias.audit.v1",
        "status": "PASS",
        "exact_seal_reconstructions": {
            "Hadamard_inverse": list(k_h),
            "D3_D4_Q_integration": list(k_e),
        },
        "exact_alpha_carry": {
            "triads": list(digits),
            "decimal": "0." + "".join(f"{value:03d}" for value in digits),
            "carries": list(carries),
        },
        "double_structural_face": {
            "high_crown_of_K": list(high_face),
            "H_e_intersection_P_pi": list(sorted(he & ppi)),
            "negative_Witt_hexad": list(h_alpha),
        },
        "vacancy_kernel_check": vacancy_root(),
        "logical_scope": {
            "exact_conditioned_numeric_map": (
                "right-to-left dodecaphase carry with frozen K, "
                "pi/e/phi triads and c13=0"
            ),
            "exact_independent_controls": [
                "K from Hadamard versus K from D3,D4,Q",
                "B_K from high crown versus H_e intersection P_pi",
            ],
            "conditional_numeric_control": (
                "E21/22 root after its six-term vacancy kernel is fixed; "
                "this script does not derive the kernel coefficients"
            ),
        },
    }
    output = Path(__file__).with_name("verificacion_alpha_dos_vias.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
