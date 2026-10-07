#!/usr/bin/env python3
"""Control exacto de la normalización modular del corredor HMT--Moonshine.

El programa verifica por aritmética entera la expansión inicial de
    j = E4^3 / Delta
y de J_Mon = j - 744, junto con las descomposiciones enteras impresas en el
manuscrito. No sustituye los teoremas de clasificación de retículas ni la
construcción FLM: éstos prueban las flechas estructurales; este certificado
controla la bisagra de normalización y el ``+1`` graduado.
"""

from __future__ import annotations

import ast
import math
import pathlib
import sys


MAX_DEGREE = 6


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def multiply(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (MAX_DEGREE + 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i + j <= MAX_DEGREE:
                result[i + j] += a * b
    return result


def sigma3(n: int) -> int:
    return sum(d**3 for d in range(1, n + 1) if n % d == 0)


def main() -> int:
    tree = ast.parse(pathlib.Path(__file__).read_text(encoding="utf-8"))
    require(
        not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        "assert detectado",
    )

    e4 = [1] + [240 * sigma3(n) for n in range(1, MAX_DEGREE + 1)]
    e4_cubed = multiply(multiply(e4, e4), e4)

    # Delta(q)=q*prod_{n>=1}(1-q^n)^24. Se calcula D=Delta/q.
    delta_over_q = [1] + [0] * MAX_DEGREE
    for n in range(1, MAX_DEGREE + 1):
        factor = [0] * (MAX_DEGREE + 1)
        for k in range(0, 25):
            if n * k <= MAX_DEGREE:
                factor[n * k] = math.comb(24, k) * ((-1) ** k)
        delta_over_q = multiply(delta_over_q, factor)

    inverse_delta_over_q = [0] * (MAX_DEGREE + 1)
    inverse_delta_over_q[0] = 1
    for n in range(1, MAX_DEGREE + 1):
        inverse_delta_over_q[n] = -sum(
            delta_over_q[k] * inverse_delta_over_q[n - k]
            for k in range(1, n + 1)
        )

    shifted_j = multiply(e4_cubed, inverse_delta_over_q)
    # shifted_j[n] es el coeficiente de q^(n-1) en j.
    expected_j = {
        -1: 1,
        0: 744,
        1: 196884,
        2: 21493760,
        3: 864299970,
    }
    for exponent, expected in expected_j.items():
        require(
            shifted_j[exponent + 1] == expected,
            f"coeficiente incorrecto de j en q^{exponent}",
        )

    j_mon = dict(expected_j)
    j_mon[0] -= 744
    require(j_mon[-1] == 1, "la línea de vacío no tiene multiplicidad uno")
    require(j_mon[0] == 0, "J_Mon conserva término constante")
    require(j_mon[1] == 196884, "dimensión de grado dos incorrecta")
    require(196884 == 1 + 196883, "descomposición Monster incorrecta")
    require(196884 == 196560 + 324, "descomposición Leech incorrecta")
    require(196884 == 54 * (5 * 729 + 1), "descomposición HMT incorrecta")

    print(
        "PASS_CORREDOR_VOA_MOONSHINE "
        "j_coefficients=1,744,196884,21493760,864299970 "
        "J_constant=0 vacuum_dimension=1 grade2=196884 "
        "monster_split=1+196883 leech_split=196560+324 "
        "hmt_split=54*(5*729+1)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
