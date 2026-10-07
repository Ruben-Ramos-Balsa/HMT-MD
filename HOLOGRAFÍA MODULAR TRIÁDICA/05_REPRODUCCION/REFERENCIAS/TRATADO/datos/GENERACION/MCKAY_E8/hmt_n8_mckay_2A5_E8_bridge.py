#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HMT — Documento técnico N8 (compañero computacional)

Correspondencia de McKay para el grupo icosaédrico binario 2A5 ≅ SL(2,5):
reconstrucción computacional del diagrama afín \tilde{E}_8, extracción de datos
estructurales (marcas/dimensiones, Cartan, Coxeter, espectro), y verificación
recursiva de la serie de Hilbert de invariantes.

───────────────────────────────────────────────────────────────────────────────
0. Filosofía de este archivo (alineada con el protocolo HMT)
───────────────────────────────────────────────────────────────────────────────

Este script NO se apoya en un "banco externo" (CODATA, ajustes experimentales, etc.).
El objetivo es puramente algebraico-espectral:

    • fijar un objeto rígido (el diagrama afín \tilde{E}_8),
    • derivar de él invariantes verificables por cálculo,
    • y producir un paquete exportable que pueda auditarse de manera autónoma.

La conexión con HMT (APP/TPK, diccionario modular-triádico, etc.) se entiende
como una fase posterior de comparación estructural: una vez construido el sello
\tilde{E}_8 de manera no ambigua, se contrasta si aparece (o no) dentro de la
dinámica discreta APP/TPK por invariantes duros (espectro, null root, series de
Hilbert, etc.).

Referencias clásicas (para contexto, no como dependencia computacional):
    - Klein (1884), Du Val (1934), McKay (1980), Slodowy (1980), Kostant (1984),
      Bourbaki (Lie).

───────────────────────────────────────────────────────────────────────────────
1. Qué se calcula exactamente (lista explícita de "observables" del N8)
───────────────────────────────────────────────────────────────────────────────

(1) Matriz de adyacencia A_aff de \tilde{E}_8 en un etiquetado concreto (9 nodos).
(2) Matriz tipo Cartan afín C_aff = 2I - A_aff.
(3) Null root / vector de marcas d en el núcleo de C_aff:
        C_aff d = 0,
    y su interpretación como vector de dimensiones de irreps.
(4) Chequeo de orden (teoría de rep. finitas):
        sum_i d_i^2 = |Γ|,
    con |Γ| = 120 para 2A5 (grupo icosaédrico binario).
(5) Reglas de descomposición McKay:
        V ⊗ ρ_i = ⊕_{j ~ i} ρ_j,
    donde V es la representación fundamental (dimensión 2) adyacente a la trivial.
(6) Serie de Hilbert de invariantes a_n = dim (Sym^n V)^Γ.
    Se obtiene por recursión (McKay + Clebsch–Gordan SU(2)):
        m_{n+1} = A_aff m_n - m_{n-1},
    y se verifica que:
        Σ a_n t^n = (1 - t^60)/((1 - t^12)(1 - t^20)(1 - t^30)).
(7) Extracción del tipo finito E8 (eliminando el nodo afín):
        A_fin = A_aff[1:,1:],   C_fin = 2I - A_fin,
    determinante, espectro, número de Coxeter h=30 y exponente-coseno.

Todo lo anterior se imprime de forma legible y se deja estructurado como funciones.

───────────────────────────────────────────────────────────────────────────────
2. Dependencias
───────────────────────────────────────────────────────────────────────────────

Solo bibliotecas estándar + (numpy, sympy). Si networkx está disponible se utiliza
solo para isomorfismo opcional; no es necesario.

"""

from __future__ import annotations

import math
import itertools
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import sympy as sp


# ------------------------------------------------------------------------------
# Utilidades de formato (para impresión clara)
# ------------------------------------------------------------------------------

def format_matrix_int(M: np.ndarray) -> str:
    """Devuelve una representación en texto de una matriz entera."""
    rows = []
    for r in M:
        rows.append("[" + " ".join(f"{int(x):2d}" for x in r) + "]")
    return "\n".join(rows)


def format_vector_int(v: np.ndarray) -> str:
    """Imprime un vector entero como lista compacta."""
    return "[" + ", ".join(str(int(x)) for x in v) + "]"


# ------------------------------------------------------------------------------
# 3. Datos estructurales: grafo afín \tilde{E}_8 (adyacencia)
# ------------------------------------------------------------------------------

@dataclass(frozen=True)
class AffineE8:
    """Contenedor de la realización (etiquetada) de \tilde{E}_8 usada en N8."""
    A_aff: np.ndarray            # 9x9 adjacency (integer)
    C_aff: np.ndarray            # 9x9 Cartan-like matrix 2I - A
    dims: np.ndarray             # length-9 mark vector (positive integer)
    edges: List[Tuple[int, int]] # list of undirected edges (i<j)


def build_affine_E8() -> AffineE8:
    """
    Construye una realización explícita del diagrama afín \tilde{E}_8.

    Etiquetado (coincide con el LaTeX):
        Nodos: 0..8
        - Nodo 0: representación trivial ρ_0 (dimensión 1).
        - Nodo 1: representación fundamental V = ρ_1 (dimensión 2), adyacente a 0.
        - El resto sigue una cadena con una rama en el nodo 5.

    Aristas:
        0-1-2-3-4-5-6-7 y 5-8
    """
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
    n = 9
    A = np.zeros((n, n), dtype=int)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1

    C = 2 * np.eye(n, dtype=int) - A

    # Nullspace (exacto, racional) y reescalado a vector entero mínimo positivo
    ns = sp.Matrix(C).nullspace()
    if len(ns) != 1:
        raise RuntimeError(f"Se esperaba núcleo 1D para C_aff; obtenido dim={len(ns)}")

    v = ns[0]
    # v es racional; hallamos un múltiplo entero mínimo positivo
    lcm_den = sp.ilcm(*[sp.denom(x) for x in v])
    d = np.array([int(lcm_den * x) for x in v], dtype=int)

    # Normalizamos para que gcd(d)=1 y d_0=1
    g = int(sp.gcd_list(list(d)))
    d = d // g
    if d[0] != 1:
        # reescala por d[0] si fuese necesario (en esta realización debe dar 1)
        g0 = d[0]
        d = d // g0

    if np.any(d <= 0):
        raise RuntimeError("El vector de marcas no resultó estrictamente positivo.")

    return AffineE8(A_aff=A, C_aff=C, dims=d, edges=edges)


# ------------------------------------------------------------------------------
# 4. Verificaciones duras: null root, suma de cuadrados, equilibrio local
# ------------------------------------------------------------------------------

def check_null_root(data: AffineE8) -> None:
    """Verifica C_aff d = 0 exactamente."""
    C = sp.Matrix(data.C_aff)
    d = sp.Matrix(list(map(int, data.dims)))
    res = C * d
    if any(int(x) != 0 for x in res):
        raise AssertionError(f"Fallo: C_aff d != 0. Residuo: {list(res)}")


def check_sum_of_squares_order(data: AffineE8, group_order: int = 120) -> None:
    """
    Chequeo de teoría de rep. finitas:
        |Γ| = Σ_i (dim ρ_i)^2

    Para Γ = 2A5 (icosaédrico binario) el orden es 120.
    """
    s = int(np.sum(data.dims.astype(int) ** 2))
    if s != group_order:
        raise AssertionError(f"Fallo: sum(d_i^2)={s} != {group_order}")


def check_dimension_balance(data: AffineE8) -> None:
    """
    En grafos de McKay simplemente-lazo se cumple:
        2 d_i = Σ_{j~i} d_j

    Esto es un chequeo local que garantiza compatibilidad de dimensiones en
    cada regla V ⊗ ρ_i = ⊕_{j~i} ρ_j.
    """
    A = data.A_aff
    d = data.dims
    for i in range(A.shape[0]):
        neighbor_sum = int(np.dot(A[i], d))
        if neighbor_sum != 2 * int(d[i]):
            raise AssertionError(
                f"Fallo balance en nodo {i}: sum vecinos={neighbor_sum}, 2d_i={2*d[i]}"
            )


# ------------------------------------------------------------------------------
# 5. Reglas McKay explícitas (tabla de descomposición)
# ------------------------------------------------------------------------------

def mckay_decomposition_table(data: AffineE8) -> Dict[int, List[int]]:
    """Devuelve, para cada i, la lista de j tales que ρ_j aparece en V⊗ρ_i."""
    A = data.A_aff
    neighbors = {i: [j for j in range(A.shape[0]) if A[i, j] == 1] for i in range(A.shape[0])}
    return neighbors


# ------------------------------------------------------------------------------
# 6. Recursión SU(2) → serie de Hilbert de invariantes
# ------------------------------------------------------------------------------

def sym_power_multiplicities(data: AffineE8, nmax: int) -> List[np.ndarray]:
    """
    Calcula multiplicidades de irreps en Sym^n(V) restringida a Γ, usando:

        V ⊗ Sym^n(V) ≅ Sym^{n+1}(V) ⊕ Sym^{n-1}(V)  (identidad SU(2))
    que, al restringir a Γ y expandir en irreps, se traduce en:

        A_aff m_n = m_{n+1} + m_{n-1}
        => m_{n+1} = A_aff m_n - m_{n-1}

    Condiciones iniciales:
        m_0 = (1,0,...,0)  (representación trivial)
        m_1 = (0,1,0,...,0) (la fundamental V corresponde al nodo 1)

    Resultado:
        m_n es un vector en Z_{\ge 0}^{9}.

    Nota: Este cálculo NO usa la tabla de caracteres; se apoya únicamente en:
        - la estructura del grafo McKay (A_aff),
        - la identidad de Clebsch–Gordan (SU(2)),
        - y el hecho de que V corresponde al nodo 1.
    """
    A = data.A_aff
    n_nodes = A.shape[0]
    m: List[np.ndarray] = [np.zeros(n_nodes, dtype=int) for _ in range(nmax + 1)]
    m[0][0] = 1
    if nmax >= 1:
        m[1][1] = 1

    for n in range(1, nmax):
        m[n + 1] = A.dot(m[n]) - m[n - 1]
        if np.any(m[n + 1] < 0):
            raise AssertionError(f"Multiplicidad negativa en n={n+1}: {m[n+1]}")

    return m


def hilbert_series_closed_form_coeffs(nmax: int) -> List[int]:
    """
    Coeficientes de la serie cerrada esperada para Γ = 2A5:

        H(t) = (1 - t^60)/((1 - t^12)(1 - t^20)(1 - t^30))

    Devuelve [a_0, ..., a_{nmax}].
    """
    t = sp.Symbol("t")
    H = (1 - t**60) / ((1 - t**12) * (1 - t**20) * (1 - t**30))
    series = sp.series(H, t, 0, nmax + 1).removeO()
    return [int(sp.expand(series).coeff(t, k)) for k in range(nmax + 1)]


# ------------------------------------------------------------------------------
# 7. Extracción del tipo finito E8 y espectro cosenoidal
# ------------------------------------------------------------------------------

@dataclass(frozen=True)
class FiniteE8:
    A_fin: np.ndarray  # 8x8 adjacency
    C_fin: np.ndarray  # 8x8 Cartan matrix
    det: int
    eigenvalues_adj: np.ndarray


def build_finite_E8_from_affine(data: AffineE8) -> FiniteE8:
    """Elimina el nodo afín (0) para obtener el diagrama finito E8."""
    A_fin = data.A_aff[1:, 1:]
    C_fin = 2 * np.eye(8, dtype=int) - A_fin
    det = int(sp.Matrix(C_fin).det())
    eig = np.linalg.eigvalsh(A_fin.astype(float))
    return FiniteE8(A_fin=A_fin, C_fin=C_fin, det=det, eigenvalues_adj=eig)


def expected_E8_exponents() -> List[int]:
    """Exponentes clásicos de E8."""
    return [1, 7, 11, 13, 17, 19, 23, 29]


def expected_E8_cauchy_eigs(h: int = 30) -> np.ndarray:
    """
    Autovalores esperados de la matriz de adyacencia de E8 (simplemente-lazo):

        λ_m = 2 cos(π m / h),  m exponente,  h=30.
    """
    exps = expected_E8_exponents()
    vals = np.array([2 * math.cos(math.pi * m / h) for m in exps], dtype=float)
    return np.sort(vals)


# ------------------------------------------------------------------------------
# 8. (Opcional) Generación explícita del sistema de raíces E8 (240 raíces)
# ------------------------------------------------------------------------------

def e8_root_system() -> List[Tuple[float, ...]]:
    """
    Genera el sistema de raíces de E8 en R^8 (240 raíces), con la realización
    estándar de la retícula E8:

        E8 = {x in Z^8 : sum x_i even} ∪ {x in Z^8 + (1/2,...,1/2) : sum x_i even}.

    Las raíces son los vectores de norma cuadrada 2 en esa retícula.
    """
    roots: List[Tuple[float, ...]] = []

    # Tipo 1: (±1, ±1, 0,...,0) con dos posiciones no nulas.
    for i, j in itertools.combinations(range(8), 2):
        for si in (+1, -1):
            for sj in (+1, -1):
                v = [0.0] * 8
                v[i] = float(si)
                v[j] = float(sj)
                roots.append(tuple(v))

    # Tipo 2: (±1/2,...,±1/2) con número par de signos negativos.
    for signs in itertools.product((+1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(tuple(0.5 * float(s) for s in signs))

    # Elimina duplicados (aunque no debería haber) conservando orden
    roots = list(dict.fromkeys(roots))
    return roots


# ------------------------------------------------------------------------------
# 9. Ejecución principal: imprime un informe
# ------------------------------------------------------------------------------

def main() -> None:
    print("═══════════════════════════════════════════════════════════════════════")
    print("N8 — McKay(2A5) → Ẽ8 : informe de cálculo (HMT)")
    print("═══════════════════════════════════════════════════════════════════════\n")

    data = build_affine_E8()

    print("1) Grafo afín Ẽ8 (adyacencia A_aff) en el etiquetado fijado:")
    print(format_matrix_int(data.A_aff))
    print()

    print("2) Matriz tipo Cartan afín C_aff = 2I - A_aff:")
    print(format_matrix_int(data.C_aff))
    print()

    print("3) Null root / vector de marcas (interpretación: dimensiones irreps):")
    print("d =", format_vector_int(data.dims))
    print("   suma de cuadrados Σ d_i^2 =", int(np.sum(data.dims**2)))
    print()

    # Verificaciones duras
    check_null_root(data)
    check_sum_of_squares_order(data, group_order=120)
    check_dimension_balance(data)
    print("✓ Verificaciones: C_aff d = 0, Σ d_i^2 = 120, y balance local 2d_i = Σ vecinos d_j.\n")

    # Reglas McKay
    print("4) Reglas McKay explícitas: V ⊗ ρ_i = ⊕_{j~i} ρ_j (V=ρ_1).")
    neigh = mckay_decomposition_table(data)
    for i in range(9):
        rhs = " ⊕ ".join(f"ρ_{j}" for j in neigh[i])
        print(f"   V ⊗ ρ_{i}  ≅  {rhs}")
    print()

    # Serie de Hilbert por recursión
    nmax = 60
    print(f"5) Serie de invariantes a_n = dim(Sym^n V)^Γ para 0≤n≤{nmax}")
    mults = sym_power_multiplicities(data, nmax=nmax)
    a_rec = [int(m[0]) for m in mults]
    a_closed = hilbert_series_closed_form_coeffs(nmax=nmax)

    ok = (a_rec == a_closed)
    print("   Comparación recursión vs forma cerrada:",
          "COINCIDE exactamente." if ok else "NO coincide (revisar).")
    if not ok:
        # imprime primeras discrepancias
        for k, (u, v) in enumerate(zip(a_rec, a_closed)):
            if u != v:
                print(f"   Discrepancia en n={k}: rec={u}, cerrada={v}")
                break
    else:
        # imprime una tabla parcial (no inundar salida)
        print("   Tabla (n : a_n) en grados donde a_n>0 hasta 60:")
        for n, an in enumerate(a_rec):
            if an > 0:
                print(f"     n={n:2d} : a_n={an}")
    print()

    print("   Forma cerrada verificada:")
    print("     H(t) = (1 - t^60)/((1 - t^12)(1 - t^20)(1 - t^30))")
    print("   (Grados 12,20,30 y relación 60: sello Klein/icosaedro ↔ E8.)\n")

    # Extrae E8 finito
    fin = build_finite_E8_from_affine(data)
    print("6) Tipo finito E8: A_fin (8x8) y Cartan C_fin = 2I - A_fin.")
    print("A_fin:")
    print(format_matrix_int(fin.A_fin))
    print("\nC_fin:")
    print(format_matrix_int(fin.C_fin))
    print(f"\n   det(C_fin) = {fin.det}  (unimodularidad).")
    print()

    # Espectro cosenoidal
    eig = np.sort(fin.eigenvalues_adj)
    eig_expected = expected_E8_cauchy_eigs(h=30)
    print("7) Espectro de A_fin (numérico):")
    print("   eig(A_fin) =", np.array2string(eig, precision=12, separator=", "))
    print("\n   Autovalores esperados 2 cos(pi m/30), m en exponentes E8:")
    print("   expected  =", np.array2string(eig_expected, precision=12, separator=", "))
    print("\n   Error máximo |eig - expected| =", float(np.max(np.abs(eig - eig_expected))))
    print()

    # Raíces E8 (opcional)
    roots = e8_root_system()
    print("8) Sistema de raíces E8 (realización estándar en R^8):")
    print("   número de raíces generadas =", len(roots), "(se espera 240).")
    if len(roots) != 240:
        raise AssertionError("Fallo: el recuento de raíces de E8 no es 240.")
    print("✓ Recuento 240 confirmado.\n")

    print("═══════════════════════════════════════════════════════════════════════")
    print("Fin del informe N8.")
    print("═══════════════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
