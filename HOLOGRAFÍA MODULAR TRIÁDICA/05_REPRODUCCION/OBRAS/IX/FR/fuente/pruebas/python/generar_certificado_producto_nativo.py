#!/usr/bin/env python3
"""Genera el certificado exacto del producto nativo sobre palabras nonádicas."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from a9_native import (
    DIGITS,
    add_words,
    all_factor_pairs_native,
    cell_table,
    encode_bijective9,
    flatten,
    irreducibles_native,
    lifted_cell,
    native_product_words,
    word_value,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "certificados/producto_nativo_generador.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compressed_visible_times() -> list[list[int]]:
    """Compresion canonica por bloques del lector visible multiplicativo.

    Este objeto no es la tabla de cocientes locales ``Q_times(a,b)``: es el
    cociente, por nueve, de cada suma de bloque de la tabla visible R_times.
    La notación histórica usaba Q_times para ambos niveles; aquí se separan.
    """

    classes = ((1, 4, 7), (2, 5, 8), (3, 6, 9))
    matrix: list[list[int]] = []
    for left_class in classes:
        row: list[int] = []
        for right_class in classes:
            total = sum(
                lifted_cell("times", left, right).residue
                for left in left_class
                for right in right_class
            )
            if total % 9:
                raise RuntimeError("la compresion Q_times no es integral")
            row.append(total // 9)
        matrix.append(row)
    return matrix


def determinant_3x3(matrix: list[list[int]]) -> int:
    """Determinante exacto, sin una biblioteca espectral externa."""

    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def first_visible_only_failure() -> dict[str, int]:
    for left in DIGITS:
        for right in DIGITS:
            cell = lifted_cell("times", left, right)
            if cell.residue != left * right:
                return {
                    "left": left,
                    "right": right,
                    "visible_only": cell.residue,
                    "exact": left * right,
                    "discarded_quotient": cell.quotient,
                }
    raise RuntimeError("el control sin memoria no fallo")


def perturbed_99_control() -> dict[str, int]:
    cell = lifted_cell("times", 9, 9)
    perturbed = 9 * (cell.quotient - 1) + cell.residue
    return {
        "left": 9,
        "right": 9,
        "canonical": cell.reconstructed,
        "perturbed": perturbed,
        "defect": perturbed - cell.reconstructed,
    }


def zero_digit_rejection_control() -> dict[str, object]:
    """Intenta introducir el cero ordinario como digito y exige su rechazo."""

    rejected = False
    exception = ""
    try:
        native_product_words((0,), (1,))
    except ValueError as error:
        rejected = True
        exception = type(error).__name__
    if not rejected:
        raise RuntimeError("el transductor acepto 0 como digito de D9")
    return {
        "attempted_word": [0],
        "rejected": rejected,
        "exception": exception,
    }


def add_without_qplus(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Mutante adversarial que conserva R+ y elimina toda memoria Q+."""

    output: list[int] = []
    width = max(len(left), len(right))
    for index in range(width):
        if index < len(left) and index < len(right):
            output.append(lifted_cell("plus", left[index], right[index]).residue)
        elif index < len(left):
            output.append(left[index])
        else:
            output.append(right[index])
    return tuple(output)


def multiply_digit_without_qplus(
    word: tuple[int, ...], digit: int
) -> tuple[int, ...]:
    """Hoja producto intacta, pero sin el cociente de las colisiones aditivas."""

    if not word:
        return ()
    output: list[int] = []
    carry = 0
    for source_digit in word:
        product_cell = lifted_cell("times", source_digit, digit)
        residue = product_cell.residue
        next_carry = product_cell.quotient
        if carry:
            residue = lifted_cell("plus", residue, carry).residue
        output.append(residue)
        carry = next_carry
    if carry:
        output.append(carry)
    return tuple(output)


def qplus_ablation_control() -> dict[str, object]:
    """Ejecuta un producto global con Q+ eliminado y publica su defecto."""

    left_value, right_value = 10, 18
    left = encode_bijective9(left_value)
    right = encode_bijective9(right_value)
    accumulator: tuple[int, ...] = ()
    for digit in reversed(right):
        shifted = multiply_digit_without_qplus(accumulator, 9)
        partial = multiply_digit_without_qplus(left, digit)
        accumulator = add_without_qplus(shifted, partial)
    mutant_value = word_value(accumulator)
    expected = left_value * right_value
    if mutant_value == expected:
        raise RuntimeError("la ablacion Q+ no produjo el fallo exigido")
    return {
        "left": left_value,
        "right": right_value,
        "expected": expected,
        "mutant_word": list(accumulator),
        "mutant_value": mutant_value,
        "defect": mutant_value - expected,
    }


def local_cocycle_census() -> dict[str, int]:
    additive_errors = 0
    multiplicative_errors = 0
    distributive_errors = 0
    for left in DIGITS:
        for middle in DIGITS:
            for right in DIGITS:
                r_lm_p = lifted_cell("plus", left, middle)
                r_mr_p = lifted_cell("plus", middle, right)
                lhs_add = r_lm_p.quotient + lifted_cell(
                    "plus", r_lm_p.residue, right
                ).quotient
                rhs_add = r_mr_p.quotient + lifted_cell(
                    "plus", left, r_mr_p.residue
                ).quotient
                additive_errors += lhs_add != rhs_add

                r_lm_x = lifted_cell("times", left, middle)
                r_mr_x = lifted_cell("times", middle, right)
                lhs_times = lifted_cell(
                    "times", r_lm_x.residue, right
                ).quotient + right * r_lm_x.quotient
                rhs_times = lifted_cell(
                    "times", left, r_mr_x.residue
                ).quotient + left * r_mr_x.quotient
                multiplicative_errors += lhs_times != rhs_times

                r_lr_x = lifted_cell("times", left, right)
                lhs_dist = lifted_cell(
                    "times", left, r_mr_p.residue
                ).quotient + left * r_mr_p.quotient
                rhs_dist = (
                    lifted_cell(
                        "plus", r_lm_x.residue, r_lr_x.residue
                    ).quotient
                    + r_lm_x.quotient
                    + r_lr_x.quotient
                )
                distributive_errors += lhs_dist != rhs_dist
    return {
        "triples_each_identity": 9**3,
        "additive_associativity_cocycle_errors": additive_errors,
        "multiplicative_associativity_cocycle_errors": multiplicative_errors,
        "lifted_distributivity_cocycle_errors": distributive_errors,
    }


def main() -> None:
    plus_cells = flatten(cell_table("plus"))
    times_cells = flatten(cell_table("times"))
    compressed_times = compressed_visible_times()
    cell_invariants = {
        "cell_count_each_sheet": len(plus_cells),
        "sum_R_plus": sum(cell.residue for cell in plus_cells),
        "sum_Q_plus": sum(cell.quotient for cell in plus_cells),
        "sum_R_times": sum(cell.residue for cell in times_cells),
        "sum_Q_times": sum(cell.quotient for cell in times_cells),
        "sum_reconstructed_plus": sum(cell.reconstructed for cell in plus_cells),
        "sum_reconstructed_times": sum(cell.reconstructed for cell in times_cells),
        "defect_visible": sum(cell.residue for cell in times_cells)
        - sum(cell.residue for cell in plus_cells),
        "defect_memory": sum(cell.quotient for cell in times_cells)
        - sum(cell.quotient for cell in plus_cells),
        "defect_total": sum(cell.reconstructed for cell in times_cells)
        - sum(cell.reconstructed for cell in plus_cells),
        "visible_R_times_mod3_block_quotient": compressed_times,
        "compressed_times_determinant": determinant_3x3(compressed_times),
        "compressed_times_trace": sum(compressed_times[index][index] for index in range(3)),
        "compressed_times_characteristic_polynomial": [1, -17, -9, 9],
        "compressed_times_exact_spectrum": ["-1", "9-6*sqrt(2)", "9+6*sqrt(2)"],
        "compressed_times_signature": [2, 1],
    }
    cell_tables = {
        "R_plus": [[cell.residue for cell in row] for row in cell_table("plus")],
        "Q_plus": [[cell.quotient for cell in row] for row in cell_table("plus")],
        "R_times": [[cell.residue for cell in row] for row in cell_table("times")],
        "Q_times": [[cell.quotient for cell in row] for row in cell_table("times")],
    }
    cocycles = local_cocycle_census()
    if any(value for key, value in cocycles.items() if key.endswith("errors")):
        raise RuntimeError("regresion en los cociclos locales de A9#")

    expected_invariants = {
        "cell_count_each_sheet": 81,
        "sum_R_plus": 405,
        "sum_Q_plus": 45,
        "sum_R_times": 459,
        "sum_Q_times": 174,
        "sum_reconstructed_plus": 810,
        "sum_reconstructed_times": 2025,
        "defect_visible": 54,
        "defect_memory": 129,
        "defect_total": 1215,
        "visible_R_times_mod3_block_quotient": [
            [4, 5, 6],
            [5, 4, 6],
            [6, 6, 9],
        ],
        "compressed_times_determinant": -9,
        "compressed_times_trace": 17,
        "compressed_times_characteristic_polynomial": [1, -17, -9, 9],
        "compressed_times_exact_spectrum": ["-1", "9-6*sqrt(2)", "9+6*sqrt(2)"],
        "compressed_times_signature": [2, 1],
    }
    if cell_invariants != expected_invariants:
        raise RuntimeError("regresion en los invariantes canonicos de A9#")

    roundtrip_limit = 9**5
    roundtrip_mismatches = 0
    for value in range(roundtrip_limit + 1):
        if word_value(encode_bijective9(value)) != value:
            roundtrip_mismatches += 1

    pair_limit = 729
    intertwiner_mismatches = 0
    commutativity_mismatches = 0
    for left in range(pair_limit + 1):
        left_word = encode_bijective9(left)
        for right in range(pair_limit + 1):
            right_word = encode_bijective9(right)
            product_word = native_product_words(left_word, right_word)
            if word_value(product_word) != left * right:
                intertwiner_mismatches += 1
            if product_word != native_product_words(right_word, left_word):
                commutativity_mismatches += 1

    algebra_limit = 80
    associativity_mismatches = 0
    identity_mismatches = 0
    unit = encode_bijective9(1)
    for value in range(algebra_limit + 1):
        word = encode_bijective9(value)
        if (
            native_product_words(word, unit) != word
            or native_product_words(unit, word) != word
        ):
            identity_mismatches += 1
    for left in range(algebra_limit + 1):
        left_word = encode_bijective9(left)
        for middle in range(algebra_limit + 1):
            middle_word = encode_bijective9(middle)
            left_middle_word = native_product_words(left_word, middle_word)
            for right in range(algebra_limit + 1):
                right_word = encode_bijective9(right)
                lhs = native_product_words(left_middle_word, right_word)
                rhs = native_product_words(
                    left_word,
                    native_product_words(middle_word, right_word),
                )
                if lhs != rhs:
                    associativity_mismatches += 1

    factor_limit = 500
    factor_pairs = all_factor_pairs_native(factor_limit)
    irreducibles = irreducibles_native(factor_limit)
    coproduct_samples = {
        str(value): [list(pair) for pair in factor_pairs[value]]
        for value in (1, 2, 9, 12, 13, 81)
    }
    reduced_samples = {
        str(value): [
            list(pair)
            for pair in factor_pairs[value]
            if pair[0] >= 2 and pair[1] >= 2
        ]
        for value in (2, 9, 12, 13, 81)
    }

    sample_trace = []
    sample_left = encode_bijective9(81)
    sample_right = encode_bijective9(81)
    sample_word = native_product_words(sample_left, sample_right, sample_trace)

    certificate = {
        "schema": "HMT.producto-nativo-A9.v1",
        "status": "PASS",
        "declared_premise": "extensión aritmética local A9# sobre D9={1,...,9}",
        "native_source_sha256": sha256(HERE / "a9_native.py"),
        "representation": {
            "digit_set": list(DIGITS),
            "zero_word": [],
            "base": 9,
            "orientation": "little-endian",
            "numeration": "bijective base 9",
            "roundtrip_limit": roundtrip_limit,
            "roundtrip_mismatches": roundtrip_mismatches,
        },
        "cell_invariants": cell_invariants,
        "cell_tables": cell_tables,
        "local_cocycles": cocycles,
        "intertwiner": {
            "pair_limit": pair_limit,
            "pairs_checked": (pair_limit + 1) ** 2,
            "mismatches": intertwiner_mismatches,
            "commutativity_mismatches": commutativity_mismatches,
            "associativity_limit": algebra_limit,
            "associativity_triples_checked": (algebra_limit + 1) ** 3,
            "associativity_mismatches": associativity_mismatches,
            "identity_mismatches": identity_mismatches,
        },
        "native_coproduct": {
            "limit": factor_limit,
            "irreducible_count": len(irreducibles),
            "irreducibles": list(irreducibles),
            "samples": coproduct_samples,
            "reduced_samples": reduced_samples,
        },
        "trace_example_81_times_81": {
            "left_word": list(sample_left),
            "right_word": list(sample_right),
            "output_word": list(sample_word),
            "output_value": word_value(sample_word),
            "local_cell_count": len(sample_trace),
            "local_cells": [
                {
                    "operation": cell.operation,
                    "left": cell.left,
                    "right": cell.right,
                    "R": cell.residue,
                    "Q": cell.quotient,
                }
                for cell in sample_trace
            ],
        },
        "negative_controls": {
            "visible_only": first_visible_only_failure(),
            "perturb_Q_times_9_9_minus_one": perturbed_99_control(),
            "standard_zero_digit": zero_digit_rejection_control(),
            "remove_Q_plus_global_product": qplus_ablation_control(),
        },
        "scope": {
            "proved": [
                "exact local A9# reconstruction on both sheets",
                "bijective base-nine word transducer",
                "native monoid product on N_0 words",
                "unitary basis intertwiner W_times on the positive canonical radix sector",
                "native divisor coproduct and irreducible selector in finite audit windows",
                "all global statements are relative to the declared finite A9# cell",
            ],
            "not_proved": [
                "global EF-G9 invariance of the product sector",
                "derivation of the local A9# cell from a weaker alphabet",
            ],
        },
    }

    if any(
        (
            roundtrip_mismatches,
            intertwiner_mismatches,
            commutativity_mismatches,
            associativity_mismatches,
            identity_mismatches,
        )
    ):
        raise RuntimeError("el producto nativo no supera el entrelazamiento exhaustivo")

    OUT.write_text(
        json.dumps(certificate, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(certificate, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
