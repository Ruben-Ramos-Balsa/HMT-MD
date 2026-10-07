#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HMT (extracto operativo): dos piezas que a menudo se mezclan

1) Motor de rutas κ27/TPK (NEWSO) sobre el toro 9×9
   - Ruta = (i_t, j_t, h_t)
   - Dígito local d(i,j)=1+(i mod 3)+3*(j mod 3)  (1..9)
   - Rotación de heading por MOV3(d):
        MOV3(d)=+1 -> rotar izquierda
        MOV3(d)=-1 -> rotar derecha
        MOV3(d)= 0 -> mantener
     y después avanzar 1 celda en la nueva dirección.
   - Estados de arranque (según el corpus):  
        N: (0,0,E), E: (0,3,S), S: (3,0,N), O: (3,3,O)

2) Lector de acarreos 729+271 (base-3 → base-1000) + Candado A (F3)
   - Dado un seed w6 ∈ F3^6, genera:
        w12 = w6·A
        w18 = w6 || w12 || (w12·A)
   - Triada 1: d1 = floor(1000 * N6 / 3^6)
   - Triadas (d1,d2) correctas: usar N18:
        M2 = floor(1000^2 * N18 / 3^18)
        (d1,d2) = (floor(M2/1000) mod 1000, M2 mod 1000)

Nota:
- Este script NO “inyecta” decimales de π/e/φ; sólo verifica el lector
  (carry) una vez dados los seeds w6 del corpus.
- En el corpus, “aquí los acarreos importan”: con N6 solo, e y φ salen
  con d1-1; con N18 sale el +1 automáticamente.

Salida:
- Imprime resultados del carry-lector para π, e, φ.
- Exporta rutas κ27/TPK (NEWSO) a CSV (108 ticks) y un ejemplo de selección NAL-κ27.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import csv

# ----------------------------
# Helpers: mov3 y base-3
# ----------------------------
def mov3_trit_from_digit(d: int) -> int:
    """MOV3: {1,4,7}->{+1}, {2,5,8}->{-1}, {3,6,9}->{0}."""
    if d in (1, 4, 7):
        return +1
    if d in (2, 5, 8):
        return -1
    if d in (3, 6, 9):
        return 0
    raise ValueError(d)

def trit_to_ternary_digit(t: int) -> int:
    """Map: +1→1, 0→0, -1→2."""
    return {+1: 1, 0: 0, -1: 2}[t]

def base3_to_int(s: str) -> int:
    n = 0
    for ch in s:
        d = ord(ch) - 48
        if d not in (0, 1, 2):
            raise ValueError("Non ternary digit")
        n = 3*n + d
    return n

def triads_from_w18(w18: str) -> tuple[int, int]:
    if len(w18) != 18:
        raise ValueError("Need 18 ternary digits")
    N18 = base3_to_int(w18)
    M2  = (1000**2 * N18) // (3**18)
    d1  = (M2 // 1000) % 1000
    d2  =  M2 % 1000
    return d1, d2

def d1_from_w6(w6: str) -> int:
    N6 = base3_to_int(w6)
    return (1000 * N6) // (3**6)

# ----------------------------
# Candado A (F3) y evolución
# ----------------------------
A = [
    [2,2,2,1,2,1],
    [2,1,2,2,1,1],
    [1,0,0,1,0,2],
    [0,0,1,1,1,0],
    [2,2,2,0,2,1],
    [2,1,2,1,0,0],
]

def matmul_row_vec_mod3(u6: list[int]) -> list[int]:
    out = []
    for j in range(6):
        s = 0
        for i in range(6):
            s += u6[i] * A[i][j]
        out.append(s % 3)
    return out

def w18_from_w6(w6: str) -> str:
    u0 = [int(c) for c in w6]
    u1 = matmul_row_vec_mod3(u0)
    u2 = matmul_row_vec_mod3(u1)
    return "".join(map(str,u0+u1+u2))

# ----------------------------
# κ27/TPK rotor (rutas NEWSO)
# ----------------------------
# Direcciones: 0=N,1=E,2=S,3=O
DIRS = {0: (-1, 0), 1: (0, +1), 2: (+1, 0), 3: (0, -1)}
def rot_left(h: int) -> int:
    # Izquierda (N->O, E->N, S->E, O->S) en orden (N,E,S,O)
    return (h - 1) % 4
def rot_right(h: int) -> int:
    return (h + 1) % 4

def digit_field(i: int, j: int) -> int:
    """d(i,j)=1+(i mod3)+3*(j mod3) en {1..9}."""
    return 1 + (i % 3) + 3 * (j % 3)

def tau_leaf(i: int, j: int) -> int:
    r = (i + j) % 3
    if r == 1:
        return +1
    if r == 2:
        return -1
    return 0

@dataclass(frozen=True)
class RotorState:
    i: int
    j: int
    h: int

STARTS = {
    "N": RotorState(0, 0, 1),  # E
    "E": RotorState(0, 3, 2),  # S
    "S": RotorState(3, 0, 0),  # N
    "O": RotorState(3, 3, 3),  # O
}

def rotor_trace(route: str, steps: int = 108) -> list[dict]:
    st = STARTS[route]
    i, j, h = st.i, st.j, st.h
    rows = []
    for t in range(1, steps + 1):
        d = digit_field(i, j)
        mv = mov3_trit_from_digit(d)
        rows.append({
            "route": route,
            "tick": t,
            "i": i,
            "j": j,
            "h": h,
            "digit": d,
            "mov3_digit": mv,
            "tau": tau_leaf(i, j),
        })
        # rotate
        if mv == +1:
            h = rot_left(h)
        elif mv == -1:
            h = rot_right(h)
        # move
        di, dj = DIRS[h]
        i = (i + di) % 9
        j = (j + dj) % 9
    return rows

def export_rotor_routes_csv(out_csv: Path, steps: int = 108) -> None:
    fields = ["route","tick","i","j","h","digit","mov3_digit","tau"]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in "NESO":
            for row in rotor_trace(r, steps=steps):
                w.writerow(row)

# ----------------------------
# NAL-κ27 (ejemplo de selección de puertas)
# ----------------------------
def nal_kappa27_indices(digits_by_route: dict[str, list[int]]) -> list[int]:
    """
    Implementación operativa basada en el texto:
    ciclo de 27 ticks, selecciona 9 índices:
      J1: >=3 rutas en {3,6,9} y alguna en 9
      si |J1|<6: añade >=3 rutas en {3,6}
      si |J|<9: añade {5,23}
      si aún falta: completa con los menores restantes (para tener 9 fijos/ciclo)
    Devuelve índices globales (1..108).
    """
    J = []
    for cyc in range(4):
        base = 27 * cyc
        cand = []
        for j in range(1, 28):
            idx = base + j
            digs = [digits_by_route[r][idx-1] for r in "NESO"]
            u = sum(1 for d in digs if d in (3,6,9))
            has9 = any(d == 9 for d in digs)
            v = sum(1 for d in digs if d in (3,6))
            cand.append((j,u,has9,v))
        Jcyc = [j for (j,u,has9,v) in cand if u >= 3 and has9]
        if len(Jcyc) < 6:
            for (j,u,has9,v) in cand:
                if j not in Jcyc and v >= 3:
                    Jcyc.append(j)
        if len(Jcyc) < 9:
            for extra in (5, 23):
                if extra not in Jcyc:
                    Jcyc.append(extra)
        if len(Jcyc) < 9:
            for (j,u,has9,v) in cand:
                if j not in Jcyc:
                    Jcyc.append(j)
                    if len(Jcyc) >= 9:
                        break
        Jcyc = sorted(Jcyc)[:9]
        J.extend([base + j for j in Jcyc])
    return sorted(J)

def main():
    # --- Parte 1: Carry-lector cerrado (DP-9ENE-rotor) ---
    seeds = {
        "pi":  "010211",
        "e":   "201101",
        "phi": "121200",
    }
    print("\n=== Carry‑lector 729+271 + Candado A (F3) ===\n")
    for name, w6 in seeds.items():
        w18 = w18_from_w6(w6)
        d1_naive = d1_from_w6(w6)
        d1, d2 = triads_from_w18(w18)
        print(f"[{name}]")
        print(f"  w6   = {w6}")
        print(f"  w18  = {w18}")
        print(f"  d1 (solo N6)  = {d1_naive}")
        print(f"  triadas N18   = ({d1},{d2})  ->  {d1}.{d2:03d}")
        print("")

    # --- Parte 2: rutas κ27/TPK y export ---
    out_csv = Path("/mnt/data/K27_TPK_rotor_routes_NEWSO_108.csv")
    export_rotor_routes_csv(out_csv, steps=108)
    print(f"Rutas κ27/TPK exportadas a: {out_csv}")

    # Ejemplo NAL-κ27 sobre el campo de dígitos d(i,j)
    digits_by_route = {}
    for r in "NESO":
        tr = rotor_trace(r, steps=108)
        digits_by_route[r] = [row["digit"] for row in tr]
    J = nal_kappa27_indices(digits_by_route)
    print("\n=== Ejemplo NAL‑κ27 (puertas) sobre las 4 rutas ===")
    print(f"Total puertas en 108 ticks: {len(J)}")
    print("Primeras 18 puertas (índices 1‑based):", J[:18])
    print("Puertas por ciclo de 27 ticks:")
    for cyc in range(4):
        cycJ = [j for j in J if 27*cyc < j <= 27*(cyc+1)]
        print(f"  ciclo {cyc}: {cycJ}")

    # Muestra breve de los primeros 20 ticks de cada ruta
    print("\n=== Primeros 20 ticks por ruta (i,j,h,digit,MOV3) ===")
    for r in "NESO":
        tr = rotor_trace(r, steps=20)
        print(f"\nRuta {r}:")
        for row in tr:
            print(f"  t={row['tick']:3d}  (i,j)=({row['i']:d},{row['j']:d})  h={row['h']}  d={row['digit']}  mov3={row['mov3_digit']}")

if __name__ == "__main__":
    main()
