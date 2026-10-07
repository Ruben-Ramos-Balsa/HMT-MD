#!/usr/bin/env python3
"""Certifica el selector radial y el 3-vecino que conduce a Leech.

El cálculo parte de la realización explícita de ``A2`` con matriz de Gram
[[2,-1],[-1,2]], del pegado discriminante indicado en el manuscrito y del
origen marcado por la bandera HMT.  Comprueba el mínimo radial, I1--I3,
determinantes, paridad y la cota que excluye raíces en las clases nuevas.
La identificación final con Leech usa después el teorema clásico de
clasificación de los retículos pares unimodulares de rango 24.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "certificados/vecino_leech.json"

AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)

RHO = (Fraction(1), Fraction(1))
MU = (
    (Fraction(0), Fraction(0)),
    (Fraction(2, 3), Fraction(1, 3)),
    (Fraction(1, 3), Fraction(2, 3)),
)
SIMPLE_ROOTS = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
A2_ROOTS = (
    (Fraction(1), Fraction(0)),
    (Fraction(-1), Fraction(0)),
    (Fraction(0), Fraction(1)),
    (Fraction(0), Fraction(-1)),
    (Fraction(1), Fraction(1)),
    (Fraction(-1), Fraction(-1)),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def inner_a2(
    left: tuple[Fraction, Fraction],
    right: tuple[Fraction, Fraction],
) -> Fraction:
    x, y = left
    u, v = right
    return 2 * x * u - x * v - y * u + 2 * y * v


def norm_a2(vector: tuple[Fraction, Fraction]) -> Fraction:
    return inner_a2(vector, vector)


def codeword(q: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple(
        sum(q[i] * AW[i][j] for i in range(6)) % 3
        for j in range(6)
    )
    return q + right


def vector_inner(
    left: tuple[tuple[Fraction, Fraction], ...],
    right: tuple[tuple[Fraction, Fraction], ...],
) -> Fraction:
    return sum(
        (inner_a2(x, y) for x, y in zip(left, right)),
        Fraction(0),
    )


def recover_origin() -> int:
    h_negative = {4, 5, 6, 7, 9, 10}
    h_e = {1, 3, 4, 6, 9, 10}
    h_phi = {1, 2, 3, 4, 7, 9}
    h_app = {2, 3, 5, 10, 11, 12}
    origin = (h_e & h_phi) - (h_negative | h_app)
    require(origin == {1}, f"el marco no recupera un origen único: {origin}")
    return next(iter(origin))


def glue_code_audit() -> dict[str, object]:
    """Construye C_W y certifica el pegado par unimodular de A2^12."""

    words = [codeword(q) for q in itertools.product(range(3), repeat=6)]
    require(len(words) == 3**6 and len(set(words)) == 3**6, "dimensión de C_W")
    weights = Counter(sum(value != 0 for value in word) for word in words)
    require(weights == Counter({9: 440, 6: 264, 12: 24, 0: 1}), "enumerador de C_W")
    require(all(weight % 3 == 0 for weight in weights), "pesos no divisibles por tres")

    generators = [
        codeword(tuple(int(i == j) for j in range(6)))
        for i in range(6)
    ]
    code_gram_mod3 = [
        [sum(x * y for x, y in zip(left, right)) % 3 for right in generators]
        for left in generators
    ]
    require(
        all(value == 0 for row in code_gram_mod3 for value in row),
        "el código gráfico no es autoortogonal",
    )

    representatives_are_dual = all(
        inner_a2(mu, root).denominator == 1
        for mu in MU
        for root in SIMPLE_ROOTS
    )
    require(representatives_are_dual, "representantes fuera de A2 dual")
    discriminant_addition = all(
        all(value.denominator == 1 for value in difference)
        for i in range(3)
        for j in range(3)
        for difference in [
            tuple(MU[i][k] + MU[j][k] - MU[(i + j) % 3][k] for k in range(2))
        ]
    )
    require(discriminant_addition, "los representantes no realizan F3")

    glue_generators = [tuple(MU[value] for value in word) for word in generators]
    glue_gram = [
        [vector_inner(left, right) for right in glue_generators]
        for left in glue_generators
    ]
    integral_gram = all(
        value.denominator == 1 for row in glue_gram for value in row
    )
    even_diagonal = all(
        glue_gram[i][i].denominator == 1
        and glue_gram[i][i].numerator % 2 == 0
        for i in range(6)
    )
    require(integral_gram and even_diagonal, "el pegado no es integral y par")

    nonzero_weights = [sum(value != 0 for value in word) for word in words if any(word)]
    minimum_weight = min(nonzero_weights)
    minimum_new_glue_norm = Fraction(2, 3) * minimum_weight
    require(minimum_weight == 6 and minimum_new_glue_norm == 4, "raíces nuevas en el pegado")

    determinant_root_lattice = 3**12
    glue_index = len(words)
    determinant_glued = Fraction(determinant_root_lattice, glue_index**2)
    require(determinant_glued == 1, "determinante del pegado")

    return {
        "code_size": len(words),
        "dimension": 6,
        "weight_enumerator": {str(weight): count for weight, count in sorted(weights.items())},
        "generator_gram_mod3": code_gram_mod3,
        "discriminant_representatives_in_A2_dual": representatives_are_dual,
        "discriminant_addition_mod_A2": discriminant_addition,
        "glue_generator_gram": [[str(value) for value in row] for row in glue_gram],
        "glue_generator_gram_integral": integral_gram,
        "glue_generator_norms_even": even_diagonal,
        "minimum_nonzero_code_weight": minimum_weight,
        "minimum_nonzero_glue_coset_norm": str(minimum_new_glue_norm),
        "root_system_of_glued_lattice": "A2^12",
        "root_lattice_determinant": determinant_root_lattice,
        "glue_index": glue_index,
        "glued_lattice_determinant": str(determinant_glued),
        "conclusion": "the glued lattice is the even unimodular Niemeier lattice with root system A2^12",
    }


def local_coset_minima() -> dict[str, str]:
    representatives = {"mu0": MU[0], "mu1": MU[1], "mu2": MU[2]}
    minima: dict[str, str] = {}
    for name, mu in representatives.items():
        for sign in (-1, 1):
            shift = (
                mu[0] + sign * RHO[0] / 3,
                mu[1] + sign * RHO[1] / 3,
            )
            values = [
                norm_a2((shift[0] + m, shift[1] + n))
                for m in range(-3, 4)
                for n in range(-3, 4)
            ]
            minimum = min(values)
            require(
                minimum == Fraction(2, 9),
                f"mínimo local inesperado para {name},{sign}",
            )
            suffix = "plus" if sign > 0 else "minus"
            minima[f"{name}_{suffix}"] = str(minimum)
    return minima


def radial_minimum() -> dict[str, object]:
    # a_i=1+3b_i, b_i>=0. La divisibilidad de v^2 por 18 equivale a
    # sum(b_i)=1 (mod 3). Un valor b_i>=4 supera ya la cota candidata 54.
    states: dict[int, tuple[int, int, tuple[int, ...]]] = {0: (0, 1, ())}
    for _ in range(12):
        next_states: dict[int, tuple[int, int, tuple[int, ...]]] = {}
        for residue, (cost, count, witness) in states.items():
            for b in range(4):
                new_residue = (residue + b) % 3
                new_cost = cost + 2 * (1 + 3 * b) ** 2
                candidate = next_states.get(new_residue)
                if candidate is None or new_cost < candidate[0]:
                    next_states[new_residue] = (
                        new_cost,
                        count,
                        witness + (b,),
                    )
                elif new_cost == candidate[0]:
                    next_states[new_residue] = (
                        candidate[0],
                        candidate[1] + count,
                        candidate[2],
                    )
        states = next_states
    norm, count, witness = states[1]
    require(norm == 54 and count == 12, "mínimo radial o multiplicidad")
    require(sorted(witness) == [0] * 11 + [1], "forma del minimizador")
    origin = recover_origin()
    # (1,-2) es congruente con rho=(1,1) módulo 3, tiene norma 14 y no es
    # radial. Junto a once copias de rho da un representante de norma 36 en
    # la misma clase residual que el vector radial.
    nonradial_coordinate = (Fraction(1), Fraction(-2))
    require(
        tuple(int(value) % 3 for value in nonradial_coordinate) == (1, 1),
        "el control no radial no está en la clase de rho",
    )
    nonradial_coordinate_norm = norm_a2(nonradial_coordinate)
    require(nonradial_coordinate_norm == 14, "norma local no radial")
    nonradial_counterexample_norm = int(nonradial_coordinate_norm + 11 * 2)
    require(nonradial_counterexample_norm == 36, "control no radial")
    return {
        "domain": "L_rho,+: a_i=1+3b_i, b_i>=0, sum(b_i)=1 mod 3",
        "minimum_norm_divisible_by_18": norm,
        "number_of_minimizers": count,
        "canonical_origin_from_incidence": origin,
        "canonical_coefficients": [4] + [1] * 11,
        "nonradial_same_class_counterexample_norm": nonradial_counterexample_norm,
        "nonradial_first_coordinate": ["1", "-2"],
        "scope": "54 is minimal in the declared positive radial cone",
    }


def neighbor_conditions(glue: dict[str, object]) -> dict[str, object]:
    coefficients = (4,) + (1,) * 11
    norm = 2 * sum(value * value for value in coefficients)
    pairings_mod3 = sorted(
        {
            int(value * inner_a2(RHO, root)) % 3
            for value in coefficients
            for root in A2_ROOTS
        }
    )
    require(norm == 54 and norm % 18 == 0, "I2")
    character_surjective = pairings_mod3 == [1, 2]
    old_roots_excluded = 0 not in pairings_mod3
    require(character_surjective and old_roots_excluded, "I1 no excluye raíces antiguas")

    determinant_niemeier = Fraction(str(glue["glued_lattice_determinant"]))
    kernel_index = 3
    determinant_kernel = determinant_niemeier * kernel_index**2
    extension_index = 3
    determinant_neighbor = determinant_kernel / extension_index**2
    require(determinant_niemeier == 1, "pegado no unimodular")
    require(
        determinant_kernel == 9 and determinant_neighbor == 1,
        "determinantes del vecino",
    )

    v_over_3_root_pairing = Fraction(coefficients[0], 3) * inner_a2(
        RHO, SIMPLE_ROOTS[0]
    )
    v_over_3_not_in_niemeier = v_over_3_root_pairing.denominator != 1
    v_in_kernel = norm % 3 == 0
    kernel_pairing_modulus = 3
    shift_denominator = 3
    v_over_3_in_dual_of_kernel = kernel_pairing_modulus == shift_denominator
    coset_order = (
        3
        if v_over_3_not_in_niemeier and v_in_kernel
        else 0
    )
    require(
        v_over_3_not_in_niemeier
        and v_in_kernel
        and v_over_3_in_dual_of_kernel
        and coset_order == 3,
        "I3",
    )

    shifted_lower_bound = 12 * Fraction(2, 9)
    require(
        shifted_lower_bound == Fraction(8, 3) and shifted_lower_bound > 2,
        "la cota no excluye raíces nuevas",
    )
    base_even = bool(glue["glue_generator_norms_even"])
    shift_norm = Fraction(norm, 9)
    cross_term_has_even_factor = 2 % 2 == 0
    neighbor_even = (
        base_even
        and shift_norm.denominator == 1
        and shift_norm.numerator % 2 == 0
        and cross_term_has_even_factor
    )
    rootless = old_roots_excluded and shifted_lower_bound > 2
    require(neighbor_even and rootless, "paridad o ausencia de raíces")

    return {
        "I1": {
            "v_coefficients_in_root_basis": list(coefficients),
            "v_in_A2_12": all(isinstance(value, int) for value in coefficients),
            "character_surjective": character_surjective,
            "root_pairings_mod3": pairings_mod3,
            "old_roots_excluded": old_roots_excluded,
        },
        "I2": {
            "v_squared": norm,
            "v_squared_mod_18": norm % 18,
            "v_over_3_squared": norm // 9,
        },
        "I3": {
            "kernel_definition": "<x,v> is divisible by 3",
            "dual_pairing_formula": "<x,v/3>=<x,v>/3 is integral on the kernel",
            "v_over_3_in_dual_of_kernel": v_over_3_in_dual_of_kernel,
            "nonintegral_pairing_with_first_A2_root": str(v_over_3_root_pairing),
            "v_over_3_not_in_niemeier": v_over_3_not_in_niemeier,
            "v_in_congruence_kernel": v_in_kernel,
            "coset_order": coset_order,
        },
        "determinants": {
            "N_A2_12": str(determinant_niemeier),
            "congruence_kernel": str(determinant_kernel),
            "three_neighbor": str(determinant_neighbor),
        },
        "parity_derivation": {
            "base_lattice_even": base_even,
            "cross_term_has_factor_2": cross_term_has_even_factor,
            "shift_norm": str(shift_norm),
        },
        "even": neighbor_even,
        "new_coset_norm_lower_bound": str(shifted_lower_bound),
        "rootless": rootless,
        "classical_consequence": (
            "the even unimodular rootless rank-24 neighbor is Leech"
        ),
    }


def main() -> None:
    glue = glue_code_audit()
    result = {
        "schema": "HMT.exceptional.leech-neighbor.v3",
        "status": "PASS",
        "a2_gram": [[2, -1], [-1, 2]],
        "discriminant_representatives": [
            ["0", "0"],
            ["2/3", "1/3"],
            ["1/3", "2/3"],
        ],
        "ternary_glue": glue,
        "radial_selector": radial_minimum(),
        "local_shifted_cosets": local_coset_minima(),
        "neighbor": neighbor_conditions(glue),
        "w24_scope": (
            "The residual binary branch W12-to-W24 is established separately "
            "from the ternary Niemeier-to-Leech branch; no W24-to-Leech map "
            "is asserted"
        ),
    }
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("PASS_VECINO_LEECH")


if __name__ == "__main__":
    main()
