#!/usr/bin/env python3
"""Controles finitos exactos de la sección 13 de VI, sin datos físicos.

No sustituye las pruebas generales del manuscrito. CAR: 1..7 modos;
Coxeter: las ocho ternas de paridad; censos: hasta 6 modos/7 partículas;
corte bosónico: N=0..32. Todos los controles usan enteros exactos.
"""

import sys

if sys.flags.optimize:
    sys.stderr.write("RECHAZADO_OPTIMIZACION: ejecutar sin -O ni -OO.\n")
    sys.exit(2)

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path


class VerificationFailure(RuntimeError):
    """Un control explícito falla; no depende de la instrucción assert."""


COUNTS = Counter()


def check(condition, group, detail):
    if not condition:
        raise VerificationFailure("{}: {}".format(group, detail))
    COUNTS[group] += 1


def fermion_op(mask, j, creation):
    if mask < 0 or j < 0:
        raise ValueError("La ocupación y el índice deben ser no negativos.")
    present = bool(mask & (1 << j))
    if present == creation:
        return None
    preceding = bin(mask & ((1 << j) - 1)).count("1")
    sign = -1 if preceding % 2 else 1
    return mask ^ (1 << j), sign


def compose(mask, first_j, first_creation, second_j, second_creation):
    first = fermion_op(mask, first_j, first_creation)
    if first is None:
        return {}
    second = fermion_op(first[0], second_j, second_creation)
    if second is None:
        return {}
    return {second[0]: first[1] * second[1]}


def sparse_add(left, right):
    result = dict(left)
    for target, coefficient in right.items():
        result[target] = result.get(target, 0) + coefficient
    return {target: coefficient for target, coefficient in result.items()
            if coefficient}


def graded_swap(state, i):
    terms, sign = state
    first, second = terms[i], terms[i + 1]
    result = list(terms)
    result[i], result[i + 1] = second, first
    return tuple(result), sign * (-1 if first[1] * second[1] else 1)


def boson_ladder(m, N, creation):
    """Devuelve (ocupación final, cuadrado del coeficiente), o cero.

    Las amplitudes normalizadas son raíces de enteros. En un recorrido
    de ida y vuelta se multiplican raíces iguales, por lo que se conserva
    exactamente el entero correspondiente sin evaluación de sqrt.
    """
    if N < 0 or m < 0 or m > N:
        raise ValueError("Se requiere N >= 0 y 0 <= m <= N.")
    if creation:
        return None if m == N else (m + 1, m + 1)
    return None if m == 0 else (m - 1, m)


def boson_round_trip(m, N, creation_first):
    first = boson_ladder(m, N, creation_first)
    if first is None:
        return 0
    second = boson_ladder(first[0], N, not creation_first)
    if second is None or second[0] != m or first[1] != second[1]:
        raise VerificationFailure("El retorno bosónico no conserva su coeficiente.")
    return first[1]


def verify():
    for d in range(1, 8):
        for mask in range(1 << d):
            for i in range(d):
                for j in range(d):
                    for left_creation, right_creation in product((False, True), repeat=2):
                        left = compose(mask, j, right_creation, i, left_creation)
                        right = compose(mask, i, left_creation, j, right_creation)
                        expected = ({mask: 1}
                                    if i == j and left_creation != right_creation else {})
                        check(sparse_add(left, right) == expected, "CAR",
                              (d, mask, i, j, left_creation, right_creation))
                number = compose(mask, i, False, i, True)
                expected_number = {mask: 1} if mask & (1 << i) else {}
                check(number == expected_number, "numero_fermionico", (d, mask, i))
                coefficient = number.get(mask, 0)
                check(coefficient * coefficient == coefficient,
                      "Pauli_idempotencia", (d, mask, i))
                check(compose(mask, i, True, i, True) == {},
                      "Pauli_doble_creacion", (d, mask, i))

    for parity in product((0, 1), repeat=3):
        state = (tuple(enumerate(parity)), 1)
        check(graded_swap(graded_swap(state, 0), 0) == state,
              "Coxeter", (parity, "s0_cuadrado"))
        left = graded_swap(graded_swap(graded_swap(state, 0), 1), 0)
        right = graded_swap(graded_swap(graded_swap(state, 1), 0), 1)
        check(left == right, "Coxeter", (parity, "trenza"))

    for d in range(1, 7):
        for n in range(8):
            exterior = sum(1 for _ in combinations(range(d), n))
            symmetric = sum(1 for _ in combinations_with_replacement(range(d), n))
            check(exterior == (comb(d, n) if n <= d else 0),
                  "censos", (d, n, "exterior"))
            check(symmetric == comb(d + n - 1, n),
                  "censos", (d, n, "simetrico"))

    for N in range(33):
        diagonal = []
        for m in range(N + 1):
            result = (boson_round_trip(m, N, True)
                      - boson_round_trip(m, N, False))
            expected = 1 - ((N + 1) if m == N else 0)
            check(result == expected, "frontera_bosonica", (N, m))
            diagonal.append(result)
        check(sum(diagonal) == 0, "traza_conmutador_finito", N)
        check(diagonal[-1] != 1, "negativo_CCR_sin_frontera", N)

    # Quitar los signos de inserción produciría 2|{0,1}> en vez de cero.
    signed = sparse_add(compose(0, 0, True, 1, True),
                        compose(0, 1, True, 0, True))
    unsigned = {3: 2}
    check(signed == {} and unsigned != signed,
          "negativo_omision_signo_exterior", "dos modos vacíos")
    # En dos modos ocupados N0+N1 tiene autovalor 2, cuyo cuadrado es 4.
    total = sum(compose(3, j, False, j, True).get(3, 0) for j in (0, 1))
    check(total == 2 and total * total != total,
          "negativo_numero_degenerado_no_proyector", "N0+N1")

    for args in ((-1, 0, True), (0, -1, False)):
        try:
            fermion_op(*args)
        except ValueError:
            check(True, "dominios_rechazados", args)
        else:
            check(False, "dominios_rechazados", args)
    for args in ((-1, 2, False), (3, 2, True), (0, -1, True)):
        try:
            boson_ladder(*args)
        except ValueError:
            check(True, "dominios_rechazados", args)
        else:
            check(False, "dominios_rechazados", args)

    script = Path(__file__).resolve()
    optimized = subprocess.run(
        [sys.executable, "-O", "-I", "-S", str(script), "--guard-probe"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    check(optimized.returncode == 2
          and "RECHAZADO_OPTIMIZACION" in optimized.stderr
          and "PASS" not in optimized.stdout,
          "negativo_Python_O", optimized.returncode)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--guard-probe", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.guard_probe:
        return 0
    script = Path(__file__).resolve()
    section = script.parent.parent / "sections" / "13_fock_pauli_composicion.tex"
    receipt_path = args.receipt or script.with_name("RECIBO_FOCK_PAULI.json")
    receipt = {
        "schema": "hmt_vi_fock_pauli_controles_finitos_v1",
        "scope": "Realizaciones finitas exactas de la sección 13; no certificación física.",
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "command": [sys.executable, "-I", "-S", str(script),
                    "--receipt", str(receipt_path.resolve())],
        "sources": {str(script): digest(script), str(section): digest(section)},
        "bounds": {"modos_CAR": [1, 7], "ternas_paridad": 8,
                   "modos_censos": [1, 6], "particulas_censos": [0, 7],
                   "corte_bosonico_N": [0, 32]},
        "arithmetic": "Entera exacta; productos de raíces mediante sus cuadrados iguales.",
        "not_certified": ["límite dinámico", "localidad relativista",
                          "identificación física de etiquetas", "prueba general por muestreo"],
    }
    try:
        verify()
    except (VerificationFailure, ValueError) as error:
        receipt["result"] = "FAIL_FINITE_FOCK_PAULI"
        receipt["error"] = str(error)
        code = 1
    else:
        receipt["result"] = "PASS_FINITE_FOCK_PAULI_NOT_PHYSICAL_CERTIFICATION"
        code = 0
    receipt["checks"] = dict(sorted(COUNTS.items()))
    receipt["total_checks"] = sum(COUNTS.values())
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    print(json.dumps({"result": receipt["result"], "checks": receipt["checks"],
                      "total_checks": receipt["total_checks"],
                      "receipt": str(receipt_path.resolve())}, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
