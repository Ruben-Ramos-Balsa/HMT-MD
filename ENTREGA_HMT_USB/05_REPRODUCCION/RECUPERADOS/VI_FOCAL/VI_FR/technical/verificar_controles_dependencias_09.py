#!/usr/bin/env python3
"""Controles finitos exactos de la sección 09 del Artículo VI.

Biblioteca estándar. No produce el libro canónico E108, no calcula todos
los lectores del corpus y no identifica metrológicamente una constante.
Los checks son explícitos: también se ejecutan bajo python -O.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import gcd
from pathlib import Path
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, column))
             for column in zip(*b)] for row in a]


def matvec(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def rank(rows) -> int:
    matrix = [[F(v) for v in row] for row in rows]
    pivot = 0
    for column in range(len(matrix[0])):
        found = next((r for r in range(pivot, len(matrix))
                      if matrix[r][column]), None)
        if found is None:
            continue
        matrix[pivot], matrix[found] = matrix[found], matrix[pivot]
        scale = matrix[pivot][column]
        matrix[pivot] = [v / scale for v in matrix[pivot]]
        for r in range(len(matrix)):
            if r != pivot:
                scale = matrix[r][column]
                matrix[r] = [x - scale * y
                             for x, y in zip(matrix[r], matrix[pivot])]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def difference_vector(i: int, j: int, size: int = 9):
    return [int(k == i) - int(k == j) for k in range(size)]


def cubic_incidence():
    def rho9(n):
        return 1 + (n - 1) % 9

    incidence = [[0] * 9 for _ in range(9)]
    for i, j, k in itertools.product(range(1, 10), repeat=3):
        incidence[rho9(i + j + k) - 1][rho9(i * j * k) - 1] += 1
    n0 = [[int(v) for v in row] for row in (
        "011011014", "101101104", "102012003",
        "011011014", "101101104", "002102013",
        "011011014", "101101104", "012002103")]
    expected = [[9 * v for v in row] for row in n0]
    require(incidence == expected, "incidencia APP3 distinta de 9N0")
    row_sizes = list(map(sum, incidence))
    column_sizes = [sum(column) for column in zip(*incidence)]
    require(row_sizes == [81] * 9, "fibras aditivas")
    require(column_sizes == [36, 36, 108, 36, 36, 108, 36, 36, 297],
            "fibras multiplicativas")
    m = [[sum(F(incidence[a][b] * incidence[c][b], 81 * column_sizes[b])
              for b in range(9)) for c in range(9)] for a in range(9)]
    eigenpairs = [
        (F(1), [1] * 9),
        (F(1, 4), [1, -1, 0] * 3),
        (F(7, 132), [1, 1, -2] * 3),
        (F(1, 18), difference_vector(2, 5)),
        (F(1, 18), difference_vector(2, 8)),
        (F(0), difference_vector(0, 3)),
        (F(0), difference_vector(0, 6)),
        (F(0), difference_vector(1, 4)),
        (F(0), difference_vector(1, 7)),
    ]
    for value, vector in eigenpairs:
        require(matvec(m, vector) == [value * entry for entry in vector],
                f"autovector incorrecto para {value}")
    require(rank([vector for _, vector in eigenpairs]) == 9,
            "los nueve autovectores no son independientes")
    squared_norm = max(value * (1 - value) for value, _ in eigenpairs)
    require(squared_norm == F(3, 16), "norma cuadrada del conmutador")
    # Este bloque extremal es racional después de normalizar el conmutador.
    s, j = [[1, 0], [0, -1]], [[0, 1], [-1, 0]]
    identity = [[1, 0], [0, 1]]
    require(multiply(s, s) == identity, "S2")
    require(multiply(j, j) == [[-1, 0], [0, -1]], "J2")
    require(multiply(s, j) == [[-v for v in row] for row in multiply(j, s)],
            "anticonmutacion SJ")
    return {
        "domain_size": 9 ** 3, "N": incidence,
        "additive_fiber_sizes": row_sizes,
        "multiplicative_fiber_sizes": column_sizes,
        "eigenvalue_multiplicities": dict(Counter(str(v) for v, _ in eigenpairs)),
        "eigenbasis_rank": 9, "commutator_norm_squared": str(squared_norm),
        "commutator_norm": "sqrt(3)/4",
        "scope": "Norma deducida mediante el lema de dos proyectores demostrado en09; no diagonalización flotante de729x729.",
    }


def record_inverse():
    # Coordenadas publicadas: entradas de esta comprobación posterior.
    # No se afirma que este programa las produzca desde el estado TPK.
    b = [-495, -116, -684, 108, 601, -90, -173, -88, 313, 560, -397, 461]
    c = [-425, -281, -481, 671, -255, 30, 475, -543, 680, 251, 6, -128]
    q = 6263
    expected = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
    w = [c[i] - b[(i + 1) % 12] for i in range(12)]
    require(sum(w) == 0, "suma de diferencias consecutivas")
    require(all(b[i] == sum(w[(i + j) % 12] for j in range(3))
                for i in range(12)), "condicion de imagen D3")
    prefix = [sum(w[:i]) for i in range(12)]
    require((q + sum(prefix)) % 12 == 0, "congruencia integral de Q")
    k = [(q + sum(prefix)) // 12 - p for p in prefix]
    require(k == expected, "inversa del registro publicado")
    require([k[i] - k[(i + 3) % 12] for i in range(12)] == b, "D3K")
    require([k[i] - k[(i + 4) % 12] for i in range(12)] == c, "D4K")
    require(sum(k) == q, "QK")
    h4 = [[1, 1, 1, 1], [1, 1, -1, -1],
          [1, -1, 1, -1], [1, -1, -1, 1]]
    require(multiply(h4, h4) == [[4 * int(i == j) for j in range(4)]
                               for i in range(4)], "H4 cuadrado")
    orbit_sums = [sum(c[r + 3 * j] for j in range(4)) for r in range(3)]
    require((q + 2 * orbit_sums[0] + orbit_sums[1]) % 3 == 0,
            "integralidad PiH")
    a0 = (q + 2 * orbit_sums[0] + orbit_sums[1]) // 3
    a = [a0, a0 - orbit_sums[0], a0 - orbit_sums[0] - orbit_sums[1]]
    u = [0] * 12
    for r in range(3):
        d = [b[r + 3 * j] for j in range(4)]
        block = [a[r], d[1] - d[3], d[0] + d[2], d[0] - d[2]]
        require(block == matvec(h4, [k[r + 3 * j] for j in range(4)]),
                "PiH no coincide con H12K")
        inverse = matvec(h4, block)
        require(inverse == [4 * k[r + 3 * j] for j in range(4)],
                "inversa Hadamard")
        for j in range(4):
            u[r + 3 * j] = block[j]
    require(u == [2378, 1406, 2479, -452, 998, -551,
                  -668, -204, -371, -322, -28, -997], "registro firmado")
    return {"input_kind": "coordenadas terminales publicadas", "K": k, "U": u,
            "Q": q, "inverse_image_conditions": True,
            "PiH_and_Hadamard_agree": True, "E108_produced": False}


def electronic_readers():
    row, column, horizontal, vertical = 5, 5, 1, 1
    word, trajectory = [], []
    for tick in range(1, 109):
        regime = (tick - 1) % 3
        before = [row, column, horizontal, vertical]
        if regime == 0:
            value = row + column
            column = 1 + ((column - 1 + horizontal) % 9)
        elif regime == 1:
            value = row * column
            row = 1 + ((row - 1 + vertical) % 9)
        else:
            value = 9
        digit = (1 + (value - 1) % 9) % 3
        word.append(digit)
        if tick in (27, 54, 81):
            horizontal, vertical = -horizontal, -vertical
        trajectory.append({"tick": tick, "before": before, "digit": digit,
                           "after": [row, column, horizontal, vertical]})
    text = "".join(map(str, word))
    require(text == ("100000220" * 3 + "120200000" * 3) * 2,
            "la recurrencia central no produce (a3b3)2")
    require(word[:54] == word[54:], "semirretorno de la publicacion")
    disagreements = {k: sum(word[t] != word[(t + k) % 108] for t in range(108))
                     for k in (1, 3, 4, 27, 36)}
    require(disagreements == {1: 54, 3: 56, 4: 68, 27: 48, 36: 32},
            "desacuerdos ciclicos")
    require(all(v % 2 == 0 for v in disagreements.values()), "paridad Dk")
    kd = [disagreements[27] + disagreements[36], disagreements[1],
          (disagreements[4] - disagreements[3]) // 2]
    tau = [1] * 3 + [-1] * 3 + [1] * 3 + [-1] * 3
    c = [sum(tau[r] * tau[(r + k) % 12] for r in range(12)) for k in range(12)]
    a = {length: sum(sum(tau[(r + j) % 12] for j in range(length)) ** 2
                     for r in range(12)) for length in range(1, 13)}
    for length in range(1, 13):
        require(a[length] == length * c[0] +
                2 * sum((length - k) * c[k] for k in range(1, length)),
                f"expansion de A_{length}")
    require(c[:4] == [12, 4, -4, -12], "correlaciones de tau")
    require([a[3], a[4]] == [44, 32], "A3,A4")
    require(3 * 4 + 4 * (-3) == 0 and gcd(4, 3) == 1,
            "cancelacion diagonal primitiva")
    omega = 4 * a[3] - 3 * a[4]
    require(omega == -2 * c[1] - 4 * c[2] - 6 * c[3] == 80, "Omega")
    p6 = sum(tau[r] * tau[r + 6] for r in range(6))
    ko = [omega, len(word) // 2, p6]
    require(kd == ko == [80, 54, 6], "igualdad KD=KOmega en el centro")
    return {"trajectory_rule": "recurrencia central especificada en09",
            "word_108": text, "trajectory": trajectory,
            "Dk": disagreements, "tau": tau, "C0_to_C3": c[:4],
            "A3": a[3], "A4": a[4], "P6": p6, "KD": kd, "KOmega": ko,
            "scope": "Trayectoria central; no igualdad de ambos lectores en todo el atlas ni productor E108."}


def action_decade():
    lower_numerator = 1618 * 7297 ** 16
    upper_numerator = 1619 * 7298 ** 16
    require(lower_numerator > 10 ** 65, "cota inferior de la decada")
    require(upper_numerator < 10 ** 66, "cota superior de la decada")
    return {"input_enclosures": {"phi": ["1618/1000", "1619/1000"],
                                  "alpha": ["7297/1000000", "7298/1000000"]},
            "denominator": str(10 ** 99),
            "lower_numerator": str(lower_numerator),
            "upper_numerator": str(upper_numerator),
            "consequence": "10^-34 < phi*alpha^16 < 10^-33",
            "scope": "Propagacion exacta de estos encierros; este control no produce por si mismo sus entradas ni la mantisa completa."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / "sections/09_dependencias_anteriores.tex"
    receipt = args.receipt or root / "technical/RECIBO_CONTROLES_DEPENDENCIAS_09.json"
    report = {"schema": "HMT.VI.controles_finitos.09.v1",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "python_optimization": sys.flags.optimize,
              "checks_use_assert": False, "script_sha256": sha256(Path(__file__)),
              "scope": "Controles exactos finitos, no puerta canonica ni autonomia global.",
              "E108_produced": False, "global_autonomy_certified": False,
              "compiled_pdf": False}
    try:
        require(source.is_file(), "no se encuentra la seccion09")
        report["source"] = {"path": str(source.relative_to(root)), "sha256": sha256(source)}
        report["controls"] = {"APP3_prefactor": cubic_incidence(),
                              "terminal_record_inverse": record_inverse(),
                              "electronic_readers": electronic_readers(),
                              "action_decade": action_decade()}
        report["status"] = "PASS_CONTROLES_FINITOS_DEPENDENCIAS_09"
        code = 0
    except Exception as exc:
        report["status"] = "FAIL_CONTROLES_FINITOS_DEPENDENCIAS_09"
        report["error"] = f"{type(exc).__name__}: {exc}"
        code = 1
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "receipt": str(receipt),
                      "error": report.get("error")}, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
