#!/usr/bin/env python3
"""Control focal de transductores APP y retornos decimales.

Procedencia: 10_producto_nativo.tex (producto, C07, B05) y c44_body.tex
(358--420) del tratado activo. No comprueba resultados analíticos de RH.
No se usa multiplicación entera para generar el resultado de Horner;
la aritmética entera se emplea después como comparación independiente.
"""

import hashlib
import json
from pathlib import Path


COUNTS = {"app_add": 0, "app_mul": 0}
MAX_CARRY = {"add": 0, "digit_mul": 0}


def app_add(i, j):
    assert 1 <= i <= 9 and 1 <= j <= 9
    COUNTS["app_add"] += 1
    q, r0 = divmod(i + j - 1, 9)
    return r0 + 1, q


def app_mul(i, j):
    assert 1 <= i <= 9 and 1 <= j <= 9
    COUNTS["app_mul"] += 1
    q, r0 = divmod(i * j - 1, 9)
    return r0 + 1, q


def encode(n):
    assert n >= 0
    digits = []
    while n:
        n, remainder = divmod(n - 1, 9)
        digits.append(remainder + 1)
    return tuple(digits)


def evaluate(word):
    return sum(d * 9**j for j, d in enumerate(word))


def add_words(u, v):
    result, carry = [], 0
    for j in range(max(len(u), len(v))):
        local = [w[j] for w in (u, v) if j < len(w)]
        if len(local) == 2:
            residue, quotient = app_add(*local)
        else:
            residue, quotient = local[0], 0
        if carry:
            residue, extra = app_add(residue, carry)
            quotient += extra
        result.append(residue)
        carry = quotient
        MAX_CARRY["add"] = max(MAX_CARRY["add"], carry)
        assert carry <= 2
    if carry:
        result.append(carry)
    return tuple(result)


def digit_multiply(d, u):
    assert 1 <= d <= 9
    result, carry = [], 0
    for digit in u:
        residue, quotient = app_mul(digit, d)
        if carry:
            residue, extra = app_add(residue, carry)
            quotient += extra
        result.append(residue)
        carry = quotient
        MAX_CARRY["digit_mul"] = max(MAX_CARRY["digit_mul"], carry)
        assert carry <= 9
    if carry:
        result.append(carry)
    return tuple(result)


def native_product(u, v):
    acc = ()
    for digit in reversed(v):
        acc = add_words(digit_multiply(9, acc), digit_multiply(digit, u))
    return acc


def decimal_return(n):
    assert n >= 2
    residue, count = 1, 0
    while True:
        residue = (10 * residue) % n
        count += 1
        if residue == 1:
            return count
        assert count <= n


def main():
    # Includes 25 x 25 positive inputs as requested, expanded to 225 x 225.
    inputs = range(225)
    for a in inputs:
        assert evaluate(encode(a)) == a
        for b in inputs:
            u, v = encode(a), encode(b)
            assert add_words(u, v) == encode(a + b)
            result = native_product(u, v)
            assert result == encode(a * b), (a, b, result)
            assert native_product(v, u) == result
    # Long forms exercise repeated propagation beyond the short grid.
    long_words = [(9,) * n for n in range(1, 10)]
    for word in long_words:
        for d in range(1, 10):
            assert evaluate(digit_multiply(d, word)) == d * evaluate(word)
    orders = {str(n): decimal_return(n) for n in (7, 13, 77, 91, 143)}
    assert set(orders.values()) == {6}
    quotients = {n: (10**order - 1) // int(n) for n, order in orders.items()}
    assert all(q % 9 == 0 for q in quotients.values())
    source = Path(__file__).resolve().parents[1] / "sections/primos_retornos.tex"
    print(json.dumps({
        "status": "PASS_CONTROL_FOCAL_PRIMOS_RETORNOS",
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "grid_inputs": [0, 224],
        "ordered_input_pairs": 225**2,
        "operations_checked": ["bijection", "native_addition", "digit_product", "Horner_product", "commutativity"],
        "long_digit_product_cases": 81,
        "local_calls": COUNTS,
        "maximum_observed_carry": MAX_CARRY,
        "decimal_orders": orders,
        "repetition_quotients": quotients,
        "scope": "Finite executable checks; the manuscript contains the general proofs. No RH or global TPK-history assertion.",
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
