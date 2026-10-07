#!/usr/bin/env python3
"""Certificado adversarial de la lectura dodecafásica enriquecida."""

from __future__ import annotations

import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path

from operador_lectura_dodecafasica import (
    EstadoTPKEnriquecido,
    ObservablesTransversales,
    accion_inducida_en_modos,
    agregar_observables_transversales,
    diferencia,
    desplazar,
    invertir_lectura_armonica,
    lectura_armonica,
    lectura_transversal,
    olvidar_hoja_por_suma,
    reconstruir_registro_transversal,
    reflejar,
    separar_signos,
)


ROOT = Path(__file__).resolve().parent
K_CAN = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
U_CAN = (2378, 1406, 2479, -452, 998, -551,
         -668, -204, -371, -322, -28, -997)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(matrix: list[list[int]]) -> int:
    a = [[Fraction(x) for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        p = a[pivot_row][col]
        a[pivot_row] = [x / p for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col]:
                q = a[r][col]
                a[r] = [a[r][c] - q * a[pivot_row][c] for c in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def difference_matrix(step: int) -> list[list[int]]:
    out = [[0] * 12 for _ in range(12)]
    for i in range(12):
        out[i][i] = 1
        out[i][(i + step) % 12] -= 1
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    require(lectura_armonica(K_CAN) == U_CAN, "falló la evaluación canónica")
    require(invertir_lectura_armonica(U_CAN) == K_CAN, "falló la inversa canónica")

    b3, b4, q = lectura_transversal(K_CAN)
    require(q == 6263, "modo total incorrecto")
    require(b3 == (-495, -116, -684, 108, 601, -90,
                   -173, -88, 313, 560, -397, 461), "D3 incorrecto")
    require(b4 == (-425, -281, -481, 671, -255, 30,
                   475, -543, 680, 251, 6, -128), "D4 incorrecto")
    observables_can = ObservablesTransversales(b3, b4, q)
    require(reconstruir_registro_transversal(observables_can) == K_CAN,
            "la agregación transversal no reconstruyó K")
    require(agregar_observables_transversales(observables_can) == (K_CAN, U_CAN),
            "la agregación transversal no reconstruyó K y U12")

    positive, negative = separar_signos(U_CAN)
    require(all(not (a and b) for a, b in zip(positive, negative)),
            "los soportes positivo y negativo no son disjuntos")
    require(tuple(a - b for a, b in zip(positive, negative)) == U_CAN,
            "la separación firmada no recompone el vector")

    rng = random.Random(20260722)
    for test in range(600):
        k = tuple(rng.randrange(-2000, 2001) for _ in range(12))
        u = lectura_armonica(k)
        require(invertir_lectura_armonica(u) == k, f"roundtrip fallido {test}")
        tb3, tb4, tq = lectura_transversal(k)
        require(
            reconstruir_registro_transversal(ObservablesTransversales(tb3, tb4, tq)) == k,
            f"reconstrucción transversal fallida {test}",
        )
        for r in (0, 1, 3, 4, 6, 11):
            transported = accion_inducida_en_modos(u, rotacion=r)
            require(transported == lectura_armonica(desplazar(k, r)),
                    f"covariancia rotacional fallida {test}:{r}")
        transported_reflection = accion_inducida_en_modos(u, reflexion=True)
        require(transported_reflection == lectura_armonica(reflejar(k)),
                f"covariancia por reflexión fallida {test}")

    d3 = difference_matrix(3)
    d4 = difference_matrix(4)
    stacked = d3 + d4
    with_total = stacked + [[1] * 12]
    ranks = {
        "D3": rank(d3),
        "D4": rank(d4),
        "D3_D4": rank(stacked),
        "D3_D4_Q": rank(with_total),
    }
    require(ranks == {"D3": 9, "D4": 8, "D3_D4": 11, "D3_D4_Q": 12},
            "rangos inesperados")

    # Una sola coordenada transversal alterada ya no pertenece a la imagen
    # conjunta y debe ser rechazada por las ecuaciones redundantes.
    b3_bad = list(b3)
    b3_bad[0] += 1
    incompatible_rejected = False
    try:
        reconstruir_registro_transversal(ObservablesTransversales(tuple(b3_bad), b4, q))
    except ValueError:
        incompatible_rejected = True
    require(incompatible_rejected, "una perturbación incompatible no fue rechazada")

    # Las diferencias sin carga dejan libre la constante. Se exhiben dos
    # potenciales distintos con las mismas cocadenas transversales.
    constant_shift = tuple(x + 7 for x in K_CAN)
    require(diferencia(constant_shift, 3) == b3 and diferencia(constant_shift, 4) == b4,
            "el control de ablación del modo total está mal construido")
    require(sum(constant_shift) != q, "el desplazamiento constante no cambió la carga")

    # Ablación de hoja: k y k+d tienen la misma suma de posiciones opuestas.
    delta = (1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0)
    k2 = tuple(a + b for a, b in zip(K_CAN, delta))
    require(olvidar_hoja_por_suma(K_CAN) == olvidar_hoja_por_suma(k2),
            "la ablación propuesta no identificó el par")
    require(lectura_armonica(K_CAN) != lectura_armonica(k2),
            "la ablación de hoja no perdió información")

    # Ablación de orientación: el registro y su reflejo pertenecen a una misma
    # clase no orientada, pero sus contrastes orientados son diferentes.
    require(K_CAN != reflejar(K_CAN), "el control de orientación es degenerado")
    require(lectura_armonica(K_CAN) != lectura_armonica(reflejar(K_CAN)),
            "la orientación no cambia los contrastes")

    # Dos estados con la misma sombra visible y distinto registro prueban que
    # no existe lectura desde la proyección visible sin añadir una sección.
    visible = (903, 850, 850, 252, 109, 252) * 2
    state1 = EstadoTPKEnriquecido(visible, 1, 1, K_CAN)
    state2 = EstadoTPKEnriquecido(visible, 1, 1, k2)
    require(state1.visible == state2.visible, "control visible mal construido")
    require(lectura_armonica(state1.registro) != lectura_armonica(state2.registro),
            "los registros distintos no fueron separados")

    cert = {
        "schema": "HMT.lectura-dodecafasica-enriquecida.v1",
        "status": "PASS",
        "domain": "estado TPK enriquecido con registro orientado de doce eventos",
        "canonical": {
            "K": K_CAN,
            "U12_signed": U_CAN,
            "D3K": b3,
            "D4K": b4,
            "Q": q,
            "positive": positive,
            "negative": negative,
        },
        "generic_tests": 600,
        "ranks": ranks,
        "ablations": {
            "forget_total_mode_Q": "one-dimensional constant ambiguity",
            "perturb_redundant_transverse_equation": "rejected as incompatible",
            "forget_opposite_sheet": "noninjective",
            "forget_orientation": "noninjective for oriented contrasts",
            "visible_periodic_projection_only": "does not determine the ledger",
        },
        "logical_result": (
            "The aggregation (D3K,D4K,Q) -> K -> signed U12 is fully defined, "
            "exact and compatibility-checking. No inverse from a period-six visible "
            "projection is asserted or required."
        ),
        "sources_sha256": {
            "operador_lectura_dodecafasica.py": sha(ROOT / "operador_lectura_dodecafasica.py"),
            "verificar_lectura_dodecafasica.py": sha(Path(__file__).resolve()),
        },
    }
    (ROOT / "CERTIFICADO_LECTURA_DODECAFASICA.json").write_text(
        json.dumps(cert, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PASS — lectura dodecafásica enriquecida, inversa, covariancia y ablaciones")


if __name__ == "__main__":
    main()
