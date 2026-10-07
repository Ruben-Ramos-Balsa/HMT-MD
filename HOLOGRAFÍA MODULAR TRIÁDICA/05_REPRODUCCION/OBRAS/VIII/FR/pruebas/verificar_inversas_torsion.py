#!/usr/bin/env python3
"""Control racional focal de dos inversas algebraicas en dimensión cuatro.

Sólo biblioteca estándar. No lee manuscritos, paquetes ni rutas personales;
no usa red y no escribe archivos. --json emite un recibo estructurado en stdout.
Los controles usan comparaciones explícitas: conservan su efecto con python -O.

Alcance: inversa de T -> T^I wedge e^J - e^I wedge T^J e inversa
de K -> T, sobre las 24 bases racionales respectivas. No comprueba el
extractor de una corriente material ni determina su acoplamiento físico.
"""

import argparse
import json
import sys
from fractions import Fraction
from itertools import combinations


DIMENSION = 4
PASS = "PASS_INVERSIONES_ALGEBRAICAS_TORSION"
FAIL = "FAIL_INVERSIONES_ALGEBRAICAS_TORSION"


class CheckFailure(Exception):
    """Una identidad difiere en un elemento de base especificado."""


def clean(form):
    return {mask: value for mask, value in form.items() if value}


def add(left, right, coefficient=Fraction(1)):
    result = dict(left)
    for mask, value in right.items():
        result[mask] = result.get(mask, Fraction(0)) + coefficient * value
    return clean(result)


def wedge(left, right):
    """Producto exterior; máscaras binarias representan multiíndices ordenados."""
    result = {}
    for x, value in left.items():
        for y, other in right.items():
            if x & y:
                continue
            inversions = sum(
                1
                for i in range(DIMENSION)
                for j in range(DIMENSION)
                if (x >> i) & 1 and (y >> j) & 1 and i > j
            )
            mask = x | y
            result[mask] = (
                result.get(mask, Fraction(0))
                + (-1) ** inversions * value * other
            )
    return clean(result)


def interior(index, form):
    """Contracción con E_index, dual de la cotetrada e^index."""
    result = {}
    for mask, value in form.items():
        if (mask >> index) & 1:
            earlier = bin(mask & ((1 << index) - 1)).count("1")
            result[mask ^ (1 << index)] = (-1) ** earlier * value
    return clean(result)


def torsion_map(torsion, cotetrad):
    return [
        [
            add(
                wedge(torsion[i], cotetrad[j]),
                wedge(cotetrad[i], torsion[j]),
                Fraction(-1),
            )
            for j in range(DIMENSION)
        ]
        for i in range(DIMENSION)
    ]


def inverse_torsion_map(y, cotetrad):
    """B^I=sum_J i_EJ Y^IJ, b=1/4 sum_I i_EI B^I, T^I=B^I-e^I wedge b."""
    b_vector = []
    for i in range(DIMENSION):
        component = {}
        for j in range(DIMENSION):
            component = add(component, interior(j, y[i][j]))
        b_vector.append(component)
    trace = {}
    for i in range(DIMENSION):
        trace = add(trace, interior(i, b_vector[i]), Fraction(1, 4))
    return [
        add(b_vector[i], wedge(cotetrad[i], trace), Fraction(-1))
        for i in range(DIMENSION)
    ]


def check_torsion_inverse():
    cotetrad = [{1 << j: Fraction(1)} for j in range(DIMENSION)]
    checked = 0
    for i in range(DIMENSION):
        for a, b in combinations(range(DIMENSION), 2):
            torsion = [{} for unused in range(DIMENSION)]
            torsion[i] = {(1 << a) | (1 << b): Fraction(1)}
            restored = inverse_torsion_map(torsion_map(torsion, cotetrad), cotetrad)
            if restored != torsion:
                raise CheckFailure(
                    "Inversa de torsión: base (I,a,b)=%r; esperado=%r; obtenido=%r"
                    % ((i, a, b), torsion, restored)
                )
            checked += 1
    if checked != 24:
        raise CheckFailure("Cardinal de bases de torsión distinto de 24")
    return checked


def check_contorsion_inverse():
    """Índices internos bajos: K_IJK=-K_JIK; T_IJK=K_IKJ-K_IJK."""
    checked = 0
    for a, b in combinations(range(DIMENSION), 2):
        for c in range(DIMENSION):
            k = {(a, b, c): Fraction(1), (b, a, c): Fraction(-1)}
            torsion = {
                (i, j, l): k.get((i, l, j), Fraction(0))
                - k.get((i, j, l), Fraction(0))
                for i in range(DIMENSION)
                for j in range(DIMENSION)
                for l in range(DIMENSION)
            }
            for i in range(DIMENSION):
                for j in range(DIMENSION):
                    for l in range(DIMENSION):
                        restored = (
                            torsion[l, i, j]
                            - torsion[i, j, l]
                            - torsion[j, l, i]
                        ) / 2
                        if restored != k.get((i, j, l), Fraction(0)):
                            raise CheckFailure(
                                "Inversa de contorsión: base=%r; componente=%r"
                                % ((a, b, c), (i, j, l))
                            )
            checked += 1
    if checked != 24:
        raise CheckFailure("Cardinal de bases de contorsión distinto de 24")
    return checked


def build_receipt():
    receipt = {
        "schema": "hmt.vii.inversas_torsion.focal.v1",
        "status": FAIL,
        "dimension": DIMENSION,
        "arithmetic": "fractions.Fraction; operaciones racionales exactas",
        "scope": "Composición inversa tras aplicación directa en 24 bases de cada dominio",
        "torsion": {
            "domain": "Lambda^2(T*M) tensor E; dimensión 24",
            "codomain": "Lambda^3(T*M) tensor Lambda^2(E); dimensión 24",
            "direct": "Y^IJ=T^I wedge e^J-e^I wedge T^J",
            "inverse": "B^I=sum_J i_EJ Y^IJ; b=(1/4)sum_I i_EI B^I; T^I=B^I-e^I wedge b",
            "source_label": "vii:eq:torsion-explicita",
            "basis_checks": 0,
        },
        "contorsion": {
            "domain": "K_IJK=-K_JIK; dimensión 24",
            "codomain": "T_IJK=-T_IKJ; dimensión 24",
            "direct": "T_IJK=K_IKJ-K_IJK",
            "inverse": "K_IJK=(T_KIJ-T_IJK-T_JKI)/2",
            "source_label": "vii:eq:contorsion-componentes",
            "basis_checks": 0,
        },
        "interpretation": (
            "La linealidad y la igualdad de dimensiones extienden las identidades "
            "comprobadas en las bases a ambos espacios completos. El control usa "
            "una cotetrada y su marco dual; la no degeneración es una hipótesis."
        ),
        "not_certified": [
            "Extracción o identificación de una corriente material desde el estado HMT",
            "Acción fermiónica concreta, contracción física o amplitud torsional",
            "Derivación global de HMT, verificación de todo el manuscrito o compilación PDF",
        ],
        "external_inputs": [],
        "network_access": False,
        "data_files_read_or_written": [],
    }
    try:
        receipt["torsion"]["basis_checks"] = check_torsion_inverse()
        receipt["contorsion"]["basis_checks"] = check_contorsion_inverse()
        receipt["status"] = PASS
    except CheckFailure as error:
        receipt["failure"] = str(error)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emitir recibo JSON en stdout")
    args = parser.parse_args()
    receipt = build_receipt()
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(receipt["status"])
        print("Bases de torsión: %s/24" % receipt["torsion"]["basis_checks"])
        print("Bases de contorsión: %s/24" % receipt["contorsion"]["basis_checks"])
        print("Alcance: inversas algebraicas; no extracción de corriente material.")
        if "failure" in receipt:
            print(receipt["failure"], file=sys.stderr)
    return 0 if receipt["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
