#!/usr/bin/env python3
"""Controles racionales de lectores. No es un generador TPK ni una prueba de CH."""
from fractions import Fraction
from itertools import product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_prefix(value, depth):
    """Primera cadena de intervalos cerrados en la carta ternaria de control."""
    require(Fraction(0) <= value <= Fraction(1), "dominio unitario")
    numerator, denominator = 0, 1
    digits = []
    for _ in range(depth):
        chosen = None
        for digit in range(3):
            q, den = 3 * numerator + digit, 3 * denominator
            if Fraction(q, den) <= value <= Fraction(q + 1, den):
                chosen = (q, den, digit)
                break
        require(chosen is not None, "cobertura de sucesores")
        numerator, denominator, digit = chosen
        digits.append(digit)
    return tuple(digits), numerator, denominator


def ceil_fraction(value):
    return -((-value.numerator) // value.denominator)


def evaluation_with_constant_tail(prefix, tail_digit):
    """Evaluación exacta de una cinta eventualmente constante de control."""
    value = sum((Fraction(d, 3 ** (i + 1)) for i, d in enumerate(prefix)), Fraction())
    return value + Fraction(tail_digit, 2 * 3 ** len(prefix))


def normalization_control():
    values = {Fraction(k, d) for d in range(1, 26) for k in range(d + 1)}
    tests = 0
    for value in sorted(values):
        previous = ()
        for depth in range(1, 7):
            digits, q, den = canonical_prefix(value, depth)
            require(digits[:-1] == previous, "compatibilidad de restricciones")
            expected = max(0, min(den - 1, ceil_fraction(value * den) - 1))
            require(q == expected, "fórmula cerrada con extremos")
            require(Fraction(q, den) <= value <= Fraction(q + 1, den), "contención")
            previous = digits
            tests += 1
    return {"rational_values": len(values), "depths": 6, "checks": tests, "passed": True}


def same_value_different_histories_control():
    histories = [((1,), 0), ((0,), 2)]
    values = [evaluation_with_constant_tail(*h) for h in histories]
    require(histories[0] != histories[1], "historias distintas")
    require(values[0] == values[1] == Fraction(1, 3), "igualdad exacta de valores")
    for depth in range(1, 9):
        a = canonical_prefix(values[0], depth)[0]
        b = canonical_prefix(values[1], depth)[0]
        require(a == b == (0,) + (2,) * (depth - 1), "misma normalización")
    require(len(set(histories)) == 2, "memorias no identificadas por normalizar")
    return {"distinct_histories": 2, "same_value": "1/3",
            "normalization_depths": 8, "passed": True}


def one_prefix_many_values_control():
    prefix_depth, tail_depth = 3, 5
    total = 0
    for q in range(3 ** prefix_depth):
        values = []
        for bits in product((0, 1), repeat=tail_depth):
            value = Fraction(q, 3 ** prefix_depth) + Fraction(1, 3 ** (prefix_depth + 1))
            value += sum((Fraction(2 * bit, 3 ** (prefix_depth + 1 + k))
                          for k, bit in enumerate(bits, start=1)), Fraction())
            _, selected_q, _ = canonical_prefix(value, prefix_depth)
            require(selected_q == q, "misma etiqueta de prefijo")
            values.append((bits, value))
            total += 1
        require(len({value for _, value in values}) == 2 ** tail_depth,
                "inyectividad de la familia finita")
        for i, (bits, value) in enumerate(values):
            for other_bits, other_value in values[i + 1:]:
                k = next(j for j, (a, b) in enumerate(zip(bits, other_bits), start=1) if a != b)
                require(abs(value - other_value) >= Fraction(1, 3 ** (prefix_depth + 1 + k)),
                        "cota por primer trit distinto")
    return {"prefixes": 3 ** prefix_depth, "values_per_prefix": 2 ** tail_depth,
            "total_values": total,
            "infinite_claim": "PROVED_IN_NOTE_R5_NOT_BY_THIS_FINITE_TEST",
            "passed": True}


def main():
    result = {
        "result": "PASS_CONTROLES_LECTORES_RANGO_GENEALOGICO",
        "checks": [normalization_control(), same_value_different_histories_control(),
                   one_prefix_many_values_control()],
        "scope": "RATIONAL_TERNARY_PUBLICATION_CONTROLS_NOT_TPK_CENSUS",
        "full_tpk_generator_executed": False,
        "all_three_global_rank_conditions_proved": False,
        "ambient_ch_proved": False,
        "ordinal_or_constructibility_membership_decided": False,
        "generated_constants_recomputed": False,
        "external_constant_targets": False,
        "pdfs_modified": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
