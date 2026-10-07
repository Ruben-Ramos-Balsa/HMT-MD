#!/usr/bin/env python3
"""
Deterministic APP+TPK artifacts:
- CT108 canonical routes on the 9×9 torus for N/E/S/O (positions + digit d_t).
- w6 seeds (π,e,φ), candado A (6×6 over F3), w18 generation, and base-1000 triad reader with carry.

Outputs:
- TPK_K27_routes_CT108_NEWSO.csv
- hmt_pi_e_phi_w6_w18_triads.csv
"""

from __future__ import annotations
import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple

# -----------------------------
# Helpers (APP on Z9)
# -----------------------------
def dr9(n: int) -> int:
    r = n % 9
    return 9 if r == 0 else r

def d_plus(r: int, c: int) -> int:
    """Digital-root addition on 1..9 coordinates."""
    return dr9(r + c)

def d_mul(r: int, c: int) -> int:
    """Digital-root multiplication on 1..9 coordinates."""
    return dr9(r * c)

def mov3_digit(d: int) -> int:
    """Return trit in {-1,0,+1} from digit d∈{1..9}."""
    if d in (1, 4, 7):
        return +1
    if d in (2, 5, 8):
        return -1
    return 0

# -----------------------------
# CT-27 / K-27 transport
# -----------------------------
def ct27_residue(tick: int) -> int:
    """Residue ρ(t) ∈ {1..9}, periodic with 9."""
    return 1 + (tick - 1) % 9

def ct27_sector(tick: int) -> int:
    """Sector s(t)=mov3(ρ(t)) ∈ {-1,0,+1}."""
    return mov3_digit(ct27_residue(tick))

def wrap_1_9(x: int) -> int:
    """Wrap integer to 1..9."""
    return ((x - 1) % 9) + 1

@dataclass
class RouteState:
    r: int
    c: int
    # direction increments in (dr,dc) with components in {-1,0,1}
    dr: int
    dc: int

START_CELLS = {
    "N": (1, 1),
    "E": (1, 4),
    "S": (4, 1),
    "O": (4, 4),
}
HEADINGS = {
    "N": (0, +1),
    "E": (+1, 0),
    "S": (0, -1),
    "O": (-1, 0),
}

def tpk_combined_step(state: RouteState, tick: int, flip_every_27: bool = True) -> Tuple[RouteState, int]:
    """
    Combined TPK transport used in the canonical CT108 routes:
    - sector +1 (areal): d = dr9(r+c), then move along (dr,dc) horizontally/vertically as defined by route heading.
    - sector -1 (volumetric): d = dr9(r*c), then move (same heading).
    - sector 0 (torsion): d = 9, no move.
    - At tick 27,54,81,108 we flip heading (optional).
    """
    s = ct27_sector(tick)
    r, c, dr, dc = state.r, state.c, state.dr, state.dc

    # Compute digit at current cell
    if s == +1:
        d = d_plus(r, c)
    elif s == -1:
        d = d_mul(r, c)
    else:
        d = 9

    # Move (except torsion)
    if s != 0:
        r = wrap_1_9(r + dr)
        c = wrap_1_9(c + dc)

    # Flip heading at multiples of 27 (K-27 boundary)
    if flip_every_27 and tick % 27 == 0:
        dr, dc = -dr, -dc

    return RouteState(r=r, c=c, dr=dr, dc=dc), d

def generate_routes_csv(path: str, steps: int = 108) -> None:
    rows: List[Dict[str, object]] = []
    for route in ("N", "E", "S", "O"):
        r0, c0 = START_CELLS[route]
        dr, dc = HEADINGS[route]
        st = RouteState(r=r0, c=c0, dr=dr, dc=dc)

        for t in range(1, steps + 1):
            # record BEFORE update (so digit matches current cell)
            event_m = 1 + (t - 1) // 9
            rho = ct27_residue(t)
            s = ct27_sector(t)
            rows.append({
                "route": route,
                "tick": t,
                "event_m": event_m,
                "residue_rho": rho,
                "sector_s": s,
                "pos_r": st.r,
                "pos_c": st.c,
                "digit_d": (d_plus(st.r, st.c) if s == +1 else (d_mul(st.r, st.c) if s == -1 else 9)),
            })
            st, _ = tpk_combined_step(st, t)

    # write
    fieldnames = ["route","tick","event_m","residue_rho","sector_s","pos_r","pos_c","digit_d"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

# -----------------------------
# Candado A over F3 and carry-lector base-1000
# -----------------------------
A_F3 = [
    [2,2,2,1,2,1],
    [2,1,2,2,1,1],
    [1,0,0,1,0,2],
    [0,0,1,1,1,0],
    [2,2,2,0,2,1],
    [2,1,2,1,0,0],
]

SEEDS = {
    "pi":  "010211",
    "e":   "201101",
    "phi": "121200",
}

def rowvec_mul_mod3(u: List[int], M: List[List[int]]) -> List[int]:
    out = []
    for j in range(6):
        s = 0
        for k in range(6):
            s += u[k] * M[k][j]
        out.append(s % 3)
    return out

def gen_w18(seed6: str) -> str:
    u = [int(c) for c in seed6]
    blocks = []
    for _ in range(3):
        blocks.append("".join(str(x) for x in u))
        u = rowvec_mul_mod3(u, A_F3)
    return "".join(blocks)

def triads_from_word(word: str, k: int) -> List[int]:
    # long-division reader: N/D in base 1000, returns k triads
    N = int(word, 3)
    D = 3 ** len(word)
    triads = []
    for _ in range(k):
        N *= 1000
        triads.append(int(N // D))
        N = N % D
    return triads

def write_pi_e_phi_csv(path: str) -> None:
    rows = []
    for name, w6 in SEEDS.items():
        w18 = gen_w18(w6)
        t6 = triads_from_word(w6, 1)[0]
        t18 = triads_from_word(w18, 2)
        rows.append({
            "const": name,
            "w6": w6,
            "triad_from_6digits": f"{t6:03d}",
            "w18": w18,
            "triads_from_18digits": f"{t18[0]:03d} {t18[1]:03d}",
        })
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

if __name__ == "__main__":
    generate_routes_csv("TPK_K27_routes_CT108_NEWSO.csv", steps=108)
    write_pi_e_phi_csv("hmt_pi_e_phi_w6_w18_triads.csv")
    print("Wrote: TPK_K27_routes_CT108_NEWSO.csv")
    print("Wrote: hmt_pi_e_phi_w6_w18_triads.csv")
