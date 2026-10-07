#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N32 -- Descomposición icosaédrica del borde SU-12 y escalera APP dimensional.

Este script realiza dos cálculos independientes pero conectados dentro de HMT 3.0:

(A) Cálculo de la representación de A5 sobre 12 puntos (vértices de icosaedro / cosets A5/C5),
    construcción de proyectores centrales P_1, P_3, P_3', P_4, P_5 y proyección de vectores HMT
    de 12 triadas: K_R12, alpha, pi, e, phi y semillas w6 dobladas.

(B) Cálculo de la APP dimensional: para B_d={1,...,9}^d y C_d={0,...,9}^d se calculan
    active bulk, decimal corona, lectores dr9 aditivo/productivo, y las fórmulas cerradas
    S_+(d)=45*9^(d-1), S_x(d)=9^(d+1)-9(d+3)6^(d-1). En d=3 se recupera
    1000=729+271, S_+(3)=3645, y 196884=54*(3645+1).

El propósito metodológico es separar:
 - lo que es teorema de representación finita;
 - lo que es proyección calculada de vectores HMT;
 - lo que es estructura dimensional del cubo de triadas;
 - y lo que aún no es derivación infinita de dígitos (requiere un mapa dinámico de transición).

No usa datos metrológicos externos ni constantes físicas salvo los vectores HMT ya congelados como objetos
para proyectar. La parte APP dimensional es enteramente aritmética.
"""
from __future__ import annotations
import itertools
import json
import math
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

OUT = Path('/mnt/data')

# -----------------------------------------------------------------------------
# Utilidades de permutaciones: A5 como permutaciones pares de {0,1,2,3,4}
# -----------------------------------------------------------------------------
Perm = Tuple[int, ...]

def compose(p: Perm, q: Perm) -> Perm:
    """Composición p∘q: aplica q y después p."""
    return tuple(p[i] for i in q)

def inverse(p: Perm) -> Perm:
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return tuple(r)

def parity(p: Perm) -> int:
    invs = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                invs += 1
    return invs % 2

def cycle_type(p: Perm) -> Tuple[int, ...]:
    seen = [False] * len(p)
    ty = []
    for i in range(len(p)):
        if not seen[i]:
            j = i
            L = 0
            while not seen[j]:
                seen[j] = True
                L += 1
                j = p[j]
            if L > 1:
                ty.append(L)
    return tuple(sorted(ty, reverse=True)) or (1,)

A5: List[Perm] = [p for p in itertools.permutations(range(5)) if parity(p) == 0]
assert len(A5) == 60
ID: Perm = tuple(range(5))

# Clases de conjugación en A5
unassigned = set(A5)
classes = []
while unassigned:
    g = next(iter(unassigned))
    cls = set(compose(compose(h, g), inverse(h)) for h in A5)
    classes.append(cls)
    unassigned -= cls

# Etiquetado: tomamos g5=(0 1 2 3 4) para distinguir 5A y 5B.
g5: Perm = (1, 2, 3, 4, 0)
g5sq = compose(g5, g5)
cls_idx: Dict[Perm, int] = {}
for idx, cls in enumerate(classes):
    for g in cls:
        cls_idx[g] = idx
class_of_g5 = cls_idx[g5]
class_of_g5sq = cls_idx[g5sq]

# Identificamos clases por etiquetas estándar para el orden de salida 1A,5A,5B,3A,2A.
label_by_class = {}
for idx, cls in enumerate(classes):
    ty = cycle_type(next(iter(cls)))
    if ty == (1,):
        label_by_class[idx] = '1A'
    elif ty == (3,):
        label_by_class[idx] = '3A'
    elif ty == (2, 2):
        label_by_class[idx] = '2A'
    elif ty == (5,):
        if idx == class_of_g5:
            label_by_class[idx] = '5A'
        elif idx == class_of_g5sq:
            label_by_class[idx] = '5B'
        else:
            label_by_class[idx] = '5?'
    else:
        label_by_class[idx] = str(ty)

# Subgrupo C5 generado por g5. Acción de A5 sobre cosets izquierdos A5/C5: 12 puntos.
H = set()
cur = ID
for _ in range(5):
    H.add(cur)
    cur = compose(g5, cur)
assert len(H) == 5
remaining = set(A5)
cosets: List[set] = []
while remaining:
    rep = next(iter(remaining))
    cos = set(compose(rep, h) for h in H)
    cosets.append(cos)
    remaining -= cos
assert len(cosets) == 12
coset_index: Dict[Perm, int] = {}
for idx, cos in enumerate(cosets):
    for x in cos:
        coset_index[x] = idx

def rep_matrix(g: Perm) -> np.ndarray:
    P = np.zeros((12, 12), dtype=float)
    for i, cos in enumerate(cosets):
        x = next(iter(cos))
        y = compose(g, x)
        j = coset_index[y]
        P[j, i] = 1.0
    return P

# Tabla de caracteres de A5. Orden de clases: 1A, 5A, 5B, 3A, 2A.
phi = (1 + math.sqrt(5.0)) / 2.0

def char_val(rep: str, g: Perm) -> float:
    label = label_by_class[cls_idx[g]]
    if rep == '1':
        return 1.0
    if rep == '3':
        return {'1A': 3.0, '5A': phi, '5B': 1 - phi, '3A': 0.0, '2A': -1.0}[label]
    if rep == "3'":
        return {'1A': 3.0, '5A': 1 - phi, '5B': phi, '3A': 0.0, '2A': -1.0}[label]
    if rep == '4':
        return {'1A': 4.0, '5A': -1.0, '5B': -1.0, '3A': 1.0, '2A': 0.0}[label]
    if rep == '5':
        return {'1A': 5.0, '5A': 0.0, '5B': 0.0, '3A': -1.0, '2A': 1.0}[label]
    raise ValueError(rep)

dim_irrep = {'1': 1, '3': 3, "3'": 3, '4': 4, '5': 5}
projectors: Dict[str, np.ndarray] = {}
for rep, d in dim_irrep.items():
    P = np.zeros((12, 12), dtype=float)
    for g in A5:
        P += char_val(rep, inverse(g)) * rep_matrix(g)
    P *= d / 60.0
    projectors[rep] = P

projector_checks = {}
for rep, P in projectors.items():
    projector_checks[rep] = {
        'trace': float(np.trace(P)),
        'rank': int(np.linalg.matrix_rank(P, tol=1e-8)),
        'idempotence_error': float(np.linalg.norm(P @ P - P)),
    }
projector_checks['sum_identity_error'] = float(np.linalg.norm(sum(projectors.values()) - np.eye(12)))
max_orth = 0.0
for a, b in itertools.combinations(projectors, 2):
    max_orth = max(max_orth, float(np.linalg.norm(projectors[a] @ projectors[b])))
projector_checks['max_orthogonality_error'] = max_orth

# Carácter de la representación de 12 puntos por clases.
char12_by_label = {}
for idx, cls in enumerate(classes):
    label = label_by_class[idx]
    vals = [int(round(np.trace(rep_matrix(g)))) for g in cls]
    char12_by_label[label] = vals[0]

# -----------------------------------------------------------------------------
# Vectores HMT de 12 componentes y proyecciones por isotypic components.
# -----------------------------------------------------------------------------
vectors: Dict[str, List[int]] = {
    'K_R12': [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601],
    'alpha_12triads': [7, 297, 352, 569, 283, 800, 997, 285, 105, 472, 380, 663],
    'pi_12triads': [141, 592, 653, 589, 793, 238, 462, 643, 383, 279, 502, 884],
    'e_12triads': [718, 281, 828, 459, 45, 235, 360, 287, 471, 352, 662, 497],
    'phi_12triads': [618, 33, 988, 749, 894, 848, 204, 586, 834, 365, 638, 117],
    'w6_pi_doubled': [0, 1, 0, 2, 1, 1, 0, 1, 0, 2, 1, 1],
    'w6_e_doubled': [2, 0, 1, 1, 0, 1, 2, 0, 1, 1, 0, 1],
    'w6_phi_doubled': [1, 2, 1, 2, 0, 0, 1, 2, 1, 2, 0, 0],
}

def projection_stats(vec: List[int]) -> Dict[str, Dict[str, float]]:
    v = np.array(vec, dtype=float)
    vc = v - np.mean(v)
    total_raw = float(np.dot(v, v))
    total_center = float(np.dot(vc, vc))
    out = {}
    for rep, P in projectors.items():
        comp = P @ v
        compc = P @ vc
        n2 = float(np.dot(comp, comp))
        n2c = float(np.dot(compc, compc))
        out[rep] = {
            'raw_norm2': n2,
            'raw_fraction': n2 / total_raw if total_raw else 0.0,
            'centered_norm2': n2c,
            'centered_fraction': n2c / total_center if total_center > 1e-12 else 0.0,
        }
    return out

vector_stats = {name: projection_stats(vec) for name, vec in vectors.items()}

# Convenience: sorted centered fractions for narrative.
vector_centered_summary = {}
for name, st in vector_stats.items():
    vector_centered_summary[name] = {rep: st[rep]['centered_fraction'] for rep in ['1', '3', "3'", '4', '5']}

# -----------------------------------------------------------------------------
# APP dimensional: closed formulas and tables.
# -----------------------------------------------------------------------------
def dr9_residue(r: int) -> int:
    return 9 if r % 9 == 0 else r % 9

def S_plus_dim(d: int) -> int:
    # Uniform digital-root distribution over active residues 1..9.
    return 45 * (9 ** (d - 1))

def S_times_dim(d: int) -> int:
    # Derived from multiplicative distribution modulo 9 over active digits 1..9.
    return 9 ** (d + 1) - 9 * (d + 3) * (6 ** (d - 1))

def delta_dim(d: int) -> int:
    return S_times_dim(d) - S_plus_dim(d)

def corona_count(d: int) -> int:
    return 10 ** d - 9 ** d

def active_count(d: int) -> int:
    return 9 ** d

app_dim_table = []
for d in [1, 2, 3, 6, 9, 12, 18, 24, 30, 36]:
    app_dim_table.append({
        'd': d,
        'active_9d': active_count(d),
        'full_10d': 10 ** d,
        'corona': corona_count(d),
        'active_fraction': active_count(d) / (10 ** d),
        'S_plus': S_plus_dim(d),
        'S_times': S_times_dim(d),
        'Delta': delta_dim(d),
    })

moonshine_anchor = {
    'Delta_2D': delta_dim(2),
    'S_plus_3D': S_plus_dim(3),
    'computed_196884': delta_dim(2) * (S_plus_dim(3) + 1),
}
assert moonshine_anchor['computed_196884'] == 196884

# Corona stratification for d=3: exactly k zero coordinates.
corona_strata_d3 = {
    'exactly_one_zero': 3 * 1 * 9 ** 2,
    'exactly_two_zeros': 3 * 1 * 1 * 9,
    'exactly_three_zeros': 1,
}
assert sum(corona_strata_d3.values()) == 271

# -----------------------------------------------------------------------------
# Checks / JSON / TeX output
# -----------------------------------------------------------------------------
results = {
    'A5': {
        'order': len(A5),
        'class_sizes': {label_by_class[i]: len(cls) for i, cls in enumerate(classes)},
        'char12_by_class': char12_by_label,
        'phi': phi,
        'projector_checks': projector_checks,
    },
    'vectors': vectors,
    'vector_stats': vector_stats,
    'vector_centered_summary': vector_centered_summary,
    'APP_dimensional': {
        'table': app_dim_table,
        'formulas': {
            'S_plus_d': '45*9^(d-1)',
            'S_times_d': '9^(d+1)-9*(d+3)*6^(d-1)',
            'Delta_d': 'S_times_d-S_plus_d',
            'active': '9^d',
            'corona': '10^d-9^d',
        },
        'moonshine_anchor': moonshine_anchor,
        'corona_strata_d3': corona_strata_d3,
    },
}

json_path = OUT / 'hmt_n32_results.json'
json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')

# Hash important arrays for reproducibility.
def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()
manifest = {
    'K_R12_sha256': sha256_text(','.join(map(str, vectors['K_R12']))),
    'alpha_12triads_sha256': sha256_text(','.join(map(str, vectors['alpha_12triads']))),
    'pi_e_phi_sha256': sha256_text('|'.join(','.join(map(str, vectors[k])) for k in ['pi_12triads','e_12triads','phi_12triads'])),
    'A5_class_sizes': results['A5']['class_sizes'],
}
(OUT / 'hmt_n32_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

# Create a LaTeX results snippet.
def pct(x: float) -> str:
    return f"{100*x:.2f}"

lines = []
lines.append(r"\section*{Resultados computacionales insertados}")
lines.append(r"\subsection*{A5 y proyectores}")
lines.append(r"El grupo $A_5$ construido tiene orden $60$. La acción sobre $A_5/C_5$ tiene $12$ puntos.")
lines.append(r"El carácter de la representación de permutación sobre las clases $1A,5A,5B,3A,2A$ es:")
lines.append(r"\[")
lines.append(r"\chi_{12}=(12,2,2,0,0)."); lines.append(r"\]")
lines.append(r"Los rangos computados de los proyectores centrales son:")
lines.append(r"\[")
lines.append(r"\operatorname{rank}(P_1,P_3,P_{3'},P_4,P_5)=(1,3,3,0,5).")
lines.append(r"\]")
lines.append(r"El error máximo de idempotencia de los proyectores es $" + f"{max(v['idempotence_error'] for k,v in projector_checks.items() if isinstance(v, dict)):.3e}" + r"$ y el error de suma $\sum P_\rho=I$ es $" + f"{projector_checks['sum_identity_error']:.3e}" + r"$.")

lines.append(r"\subsection*{Energía isotypic de vectores HMT (centrados)}")
lines.append(r"Las fracciones siguientes se calculan después de sustraer la media, para eliminar el modo trivial $P_1$.")
lines.append(r"\begin{center}\begin{tabular}{lrrrr}")
lines.append(r"\toprule")
lines.append(r"Vector & $P_3$ & $P_{3'}$ & $P_5$ & $P_4$\\")
lines.append(r"\midrule")
for name in ['K_R12','alpha_12triads','pi_12triads','e_12triads','phi_12triads','w6_pi_doubled','w6_e_doubled','w6_phi_doubled']:
    st=vector_stats[name]
    safe = name.replace('_', r'\_')
    p3 = pct(st['3']['centered_fraction'])
    p3p = pct(st["3'"]['centered_fraction'])
    p5 = pct(st['5']['centered_fraction'])
    p4 = pct(st['4']['centered_fraction'])
    lines.append(f"{safe} & {p3}\\% & {p3p}\\% & {p5}\\% & {p4}\\%\\\\")
lines.append(r"\bottomrule")
lines.append(r"\end{tabular}\end{center}")

lines.append(r"\subsection*{APP dimensional}")
lines.append(r"Para $B_d=\{1,\ldots,9\}^d$ y $C_d=\{0,\ldots,9\}^d$ se obtiene:")
lines.append(r"\[")
lines.append(r"|B_d|=9^d,\qquad |C_d\setminus B_d|=10^d-9^d.")
lines.append(r"\]")
lines.append(r"Además:")
lines.append(r"\[")
lines.append(r"S_{+,d}=45\,9^{d-1},\qquad S_{\times,d}=9^{d+1}-9(d+3)6^{d-1}.")
lines.append(r"\]")
lines.append(r"En particular, para $d=3$:")
lines.append(r"\[")
lines.append(r"9^3=729,\qquad 10^3-9^3=271,\qquad S_{+,3}=3645.")
lines.append(r"\]")
lines.append(r"Y se recupera el ancla moonshine:")
lines.append(r"\[")
lines.append(r"196884=\Delta_{2D}(S_{+,3}+1)=54(3645+1).")
lines.append(r"\]")
lines.append(r"\begin{center}\begin{tabular}{rrrrr}")
lines.append(r"\toprule")
lines.append(r"$d$ & $9^d$ & $10^d-9^d$ & $S_{+,d}$ & $\Delta_d$\\")
lines.append(r"\midrule")
for row in app_dim_table[:7]:
    lines.append(f"{row['d']} & {row['active_9d']} & {row['corona']} & {row['S_plus']} & {row['Delta']}\\\\")
lines.append(r"\bottomrule")
lines.append(r"\end{tabular}\end{center}")

tex_results_path = OUT / 'hmt_n32_results.tex'
tex_results_path.write_text('\n'.join(lines), encoding='utf-8')

print("N32 results generated")
print("Projector ranks:", {rep: projector_checks[rep]['rank'] for rep in ['1','3',"3'",'4','5']})
print("A5 char12:", char12_by_label)
print("alpha centered fractions:", vector_centered_summary['alpha_12triads'])
print("moonshine anchor:", moonshine_anchor)
print("manifest:", manifest)
