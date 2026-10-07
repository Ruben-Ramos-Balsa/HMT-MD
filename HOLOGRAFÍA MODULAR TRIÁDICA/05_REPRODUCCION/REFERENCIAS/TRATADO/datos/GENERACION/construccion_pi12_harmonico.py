#!/usr/bin/env python3
"""Construcción exacta del tramo armónico de Pi_12^{+-}.

La entrada es la terna transversal congelada (b3,b4,Q), con

    b3_m = K_m - K_{m+3},
    b4_m = K_m - K_{m+4},
    Q    = sum_m K_m.

La función ``pi12_harmonico`` reconstruye K desde esa terna y obtiene el
vector firmado U_12 sin recibir alpha ni constantes físicas. La procedencia
upstream de la terna no se demuestra en este programa; se verifica su
equivalencia exacta con la transformada H4.
"""

from __future__ import annotations

from fractions import Fraction
import json
import random
from typing import Iterable, Sequence


B3_CANONICO = (-495, -116, -684, 108, 601, -90,
               -173, -88, 313, 560, -397, 461)
B4_CANONICO = (-425, -281, -481, 671, -255, 30,
               475, -543, 680, 251, 6, -128)
Q_CANONICO = 6263
U12_ESPERADO = (2378, 1406, 2479, -452, 998, -551,
                -668, -204, -371, -322, -28, -997)
U_APP_COMPRIMIDO = (903, 850, 850, 252, 109, 252,
                    903, 850, 850, 252, 109, 252)


def diferencia(x: Sequence[int], paso: int) -> tuple[int, ...]:
    """D_p x = (x_m-x_{m+p})_m, con índices módulo 12."""
    n = len(x)
    return tuple(x[m] - x[(m + paso) % n] for m in range(n))


def suma_ciclos(x: Sequence[int], paso: int) -> tuple[int, ...]:
    """Suma sobre las gcd(12,paso) órbitas del desplazamiento dado."""
    from math import gcd

    return tuple(sum(x[r::gcd(len(x), paso)])
                 for r in range(gcd(len(x), paso)))


def validar_ledger(b3: Sequence[int], b4: Sequence[int], q: int) -> None:
    if len(b3) != 12 or len(b4) != 12:
        raise ValueError("b3 y b4 deben tener longitud 12")
    if suma_ciclos(b3, 3) != (0, 0, 0):
        raise ValueError("b3 no es una 3-diferencia cerrada")
    if suma_ciclos(b4, 4) != (0, 0, 0, 0):
        raise ValueError("b4 no es una 4-diferencia cerrada")
    if diferencia(b3, 4) != diferencia(b4, 3):
        raise ValueError("fallo de compatibilidad D4 b3 = D3 b4")

    br = tuple(sum(b4[r::3]) for r in range(3))
    numeradores = (q + 2 * br[0] + br[1],
                   q - br[0] + br[1],
                   q - br[0] - 2 * br[1])
    if any(v % 3 for v in numeradores):
        raise ValueError("Q y b4 no producen sectores DC enteros")


def pi12_harmonico(
    b3: Sequence[int], b4: Sequence[int], q: int
) -> tuple[int, ...]:
    """Mapa directo (b3,b4,Q) -> U_12 firmado.

    Para cada clase r módulo 3, b3 entrega los tres modos no constantes de
    Hadamard. Las sumas de b4 por clases módulo 3 y Q entregan los tres modos
    constantes. El orden de fase queda anclado por m=0 y la orientación
    positiva m -> m+1.
    """
    validar_ledger(b3, b4, q)

    br = tuple(sum(b4[r::3]) for r in range(3))
    a = (
        (q + 2 * br[0] + br[1]) // 3,
        (q - br[0] + br[1]) // 3,
        (q - br[0] - 2 * br[1]) // 3,
    )

    u = [0] * 12
    for r in range(3):
        d0, d1, d2, d3 = (b3[r + 3 * j] for j in range(4))
        modos = (a[r], d1 - d3, d0 + d2, d0 - d2)
        for j, valor in enumerate(modos):
            u[r + 3 * j] = valor
    return tuple(u)


def partes_signadas(u: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Descomposición canónica u=u^+-u^- con soportes disjuntos."""
    positivo = tuple(max(v, 0) for v in u)
    negativo = tuple(max(-v, 0) for v in u)
    return positivo, negativo


def reconstruir_potencial(
    b3: Sequence[int], b4: Sequence[int], q: int
) -> tuple[int, ...]:
    """Reconstruye el potencial sólo para verificar la equivalencia H4.

    Se integra el grafo de Cayley de Z/12 generado por 3 y 4. La conectividad
    (gcd(3,4)=1) deja una sola constante; Q la fija.
    """
    validar_ledger(b3, b4, q)
    valores: list[int | None] = [None] * 12
    valores[0] = 0
    pendientes = [0]
    while pendientes:
        m = pendientes.pop()
        assert valores[m] is not None
        for paso, borde in ((3, b3), (4, b4)):
            vecino = (m + paso) % 12
            candidato = valores[m] - borde[m]
            if valores[vecino] is None:
                valores[vecino] = candidato
                pendientes.append(vecino)
            elif valores[vecino] != candidato:
                raise ValueError("el ledger no integra a un potencial")

    base = tuple(int(v) for v in valores if v is not None)
    if len(base) != 12:
        raise ValueError("el grafo de integración no resultó conexo")
    desplazamiento = Fraction(q - sum(base), 12)
    if desplazamiento.denominator != 1:
        raise ValueError("Q no fija un potencial entero")
    return tuple(v + desplazamiento.numerator for v in base)


def hadamard_mod3(k: Sequence[int]) -> tuple[int, ...]:
    """H4 sobre las tres órbitas m=r+3j, reintercalado en orden natural."""
    u = [0] * 12
    for r in range(3):
        x0, x1, x2, x3 = (k[r + 3 * j] for j in range(4))
        modos = (
            x0 + x1 + x2 + x3,
            x0 + x1 - x2 - x3,
            x0 - x1 + x2 - x3,
            x0 - x1 - x2 + x3,
        )
        for j, valor in enumerate(modos):
            u[r + 3 * j] = valor
    return tuple(u)


def rango_racional(matriz: Iterable[Iterable[int]]) -> int:
    a = [[Fraction(v) for v in fila] for fila in matriz]
    if not a:
        return 0
    filas, columnas = len(a), len(a[0])
    pivote_fila = 0
    for columna in range(columnas):
        pivote = next((i for i in range(pivote_fila, filas)
                       if a[i][columna]), None)
        if pivote is None:
            continue
        a[pivote_fila], a[pivote] = a[pivote], a[pivote_fila]
        factor = a[pivote_fila][columna]
        a[pivote_fila] = [v / factor for v in a[pivote_fila]]
        for i in range(filas):
            if i == pivote_fila or not a[i][columna]:
                continue
            factor = a[i][columna]
            a[i] = [a[i][j] - factor * a[pivote_fila][j]
                    for j in range(columnas)]
        pivote_fila += 1
        if pivote_fila == filas:
            break
    return pivote_fila


def matriz_diferencia(paso: int) -> list[list[int]]:
    matriz = []
    for m in range(12):
        fila = [0] * 12
        fila[m] = 1
        fila[(m + paso) % 12] -= 1
        matriz.append(fila)
    return matriz


def tiene_periodo(x: Sequence[int], periodo: int) -> bool:
    return all(x[m] == x[(m + periodo) % len(x)] for m in range(len(x)))


def auditoria() -> dict[str, object]:
    u = pi12_harmonico(B3_CANONICO, B4_CANONICO, Q_CANONICO)
    k = reconstruir_potencial(B3_CANONICO, B4_CANONICO, Q_CANONICO)
    u_mas, u_menos = partes_signadas(u)

    assert u == U12_ESPERADO
    assert hadamard_mod3(k) == u
    assert diferencia(k, 3) == B3_CANONICO
    assert diferencia(k, 4) == B4_CANONICO
    assert sum(k) == Q_CANONICO
    assert all(a == 0 or b == 0 for a, b in zip(u_mas, u_menos))
    assert tuple(a - b for a, b in zip(u_mas, u_menos)) == u

    # Identidad universal: la fórmula directa coincide con H4 para potenciales
    # enteros arbitrarios, no sólo para el ejemplo canónico.
    rng = random.Random(12034)
    pruebas_aleatorias = 250
    for _ in range(pruebas_aleatorias):
        testigo = tuple(rng.randint(-5000, 5000) for _ in range(12))
        directo = pi12_harmonico(
            diferencia(testigo, 3), diferencia(testigo, 4), sum(testigo)
        )
        assert directo == hadamard_mod3(testigo)

    d3 = matriz_diferencia(3)
    d4 = matriz_diferencia(4)
    suma = [[1] * 12]
    rangos = {
        "D3": rango_racional(d3),
        "D4": rango_racional(d4),
        "D3_D4": rango_racional(d3 + d4),
        "D3_Q": rango_racional(d3 + suma),
        "D4_Q": rango_racional(d4 + suma),
        "D3_D4_Q": rango_racional(d3 + d4 + suma),
    }
    assert rangos == {
        "D3": 9,
        "D4": 8,
        "D3_D4": 11,
        "D3_Q": 10,
        "D4_Q": 9,
        "D3_D4_Q": 12,
    }

    app_periodo_6 = tiene_periodo(U_APP_COMPRIMIDO, 6)
    firmado_periodo_6 = tiene_periodo(u, 6)
    assert app_periodo_6 and not firmado_periodo_6

    return {
        "status": "PASS",
        "operator": (
            "H_12 o R_(D3,D4,Q): (b^(90), b^(120), Q) -> K -> U_12 signed; "
            "E_90/120 itself is K -> (b^(90), b^(120), Q)"
        ),
        "phase_convention": "m=0 origin; positive orientation m->m+1",
        "b90": list(B3_CANONICO),
        "b120": list(B4_CANONICO),
        "Q": Q_CANONICO,
        "sector_sums_A": [u[0], u[1], u[2]],
        "U12_signed": list(u),
        "U12_plus": list(u_mas),
        "U12_minus": list(u_menos),
        "K_reconstructed_intermediate": list(k),
        "rank_ablation": rangos,
        "random_integer_identity_tests": pruebas_aleatorias,
        "period6_no_go": {
            "U_APP_has_period_6": app_periodo_6,
            "U12_signed_has_period_6": firmado_periodo_6,
            "conclusion": (
                "No shift-equivariant map can obtain the signed target from "
                "the compressed APP word alone."
            ),
        },
        "E_90_120_on_frozen_transverse_data": "CLOSED_AS_(D3K,D4K,sumK)",
        "upstream_provenance": (
            "NEWSO routes 108/243 and rotor D108 are regenerated conditionally "
            "on their published target words by certificados/NEWSO/"
            "verificar_newso_ct108.py; the signed U12 "
            "payload and K are frozen and hash-certified in N32."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(auditoria(), ensure_ascii=False, indent=2))
