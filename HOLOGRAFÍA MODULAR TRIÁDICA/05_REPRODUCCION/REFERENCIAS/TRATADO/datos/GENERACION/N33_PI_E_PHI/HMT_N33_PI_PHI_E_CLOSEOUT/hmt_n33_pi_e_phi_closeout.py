#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HMT / APP — N33: catálogo discreto y reconocimiento externo de π, e, φ.

Goal
----
Produce a reproducible finite package showing that:

  (Upstream, discrete) APP + κ-27 + MOV3  -->  U12  -->  U6  -->  w6 ∈ F3^6

and that, after the published lift w6→w30 and the exact
base-3→base-1000 reading, three catalogued words match the first four
base-1000 triads (12 decimal digits) of:

  π = 3.141592653589...
  e = 2.718281828459...
  φ = 1.618033988749...

Important: the discrete catalogue is enumerated without calling a numerical
constant evaluator. The labels π,e,φ are assigned afterwards by external
comparison. This script proves finite realization and uniqueness inside the
published catalogue, not an autonomous upstream selector.

This script generates:
  - n33_uid_catalog.csv   : unique U6 states (with multiplicities and w6)
  - n33_seed_witness.csv  : canonical seed-pairs witnessing each of the 3 w6
  - HMT_N33_certificate.json
  - HMT_N33_MANIFEST.sha256

Run
---
  python hmt_n33_pi_e_phi_closeout.py --outdir ./HMT_N33_PI_PHI_E_CLOSEOUT

"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

# -----------------------------------------------------------------------------
# 0) Core discrete primitives: APP tables, dr9, MOV3 schedule, κ-27 flips
# -----------------------------------------------------------------------------

def dr9(n: int) -> int:
    """Digital root mod 9, with the convention dr9(0)=9."""
    r = n % 9
    return 9 if r == 0 else r


def L_plus(i: int, j: int) -> int:
    """APP '+' table value at coordinates (i,j) with i,j in {0,...,8}."""
    return dr9((i + 1) + (j + 1))


def L_times(i: int, j: int) -> int:
    """APP '×' table value at coordinates (i,j) with i,j in {0,...,8}."""
    return dr9((i + 1) * (j + 1))


def mov3_sign(r: int) -> int:
    """MOV3 sign from residue r in {1,...,9}.

    Convention (as in 3.0.alfa):
      +1 for r ∈ {1,4,7}
      -1 for r ∈ {2,5,8}
       0 for r ∈ {3,6,9}
    """
    if r in (1, 4, 7):
        return +1
    if r in (2, 5, 8):
        return -1
    return 0


# Discrete log on Z9^× using base 2: 1,2,4,8,7,5
DISC_LOG9 = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5}


def disc_log9(x: int) -> int:
    """Discrete log in the unit group Z9^×; maps non-units to 0."""
    return DISC_LOG9.get(x, 0)


DIR_KEYS = ("N", "E", "S", "O")
DIR_VECS = {
    "N": (-1, 0),
    "E": (0, +1),
    "S": (+1, 0),
    "O": (0, -1),
}

# κ-27: flip directions at the 27,54,81,108 boundaries
KAPPA_FLIPS = {27, 54, 81, 108}


def require(condition: bool, message: str) -> None:
    """Falla de forma explícita incluso con optimización de Python."""
    if not condition:
        raise RuntimeError(f"N33 FAIL: {message}")


def compute_U12(seedP: Tuple[int, int, str], seedT: Tuple[int, int, str]) -> List[int]:
    """Compute the full 12-triad vector U12 from the upstream APP+MOV3+κ-27 engine.

    Seeds:
      seedP = (p_i, p_j, dirP) for the '+' pointer
      seedT = (t_i, t_j, dirT) for the '×' pointer

    Output:
      U12 = [U_1,...,U_12], each U_m in {0,...,999}.

    Definition (matches the pseudo-code in 3.0.alfa):
      - 12 windows of 9 ticks each (total 108 ticks)
      - r(t) cycles 1..9 and MOV3 sign depends on r(t)
      - '+' channel accumulates S using L_plus and advances p_plus when sign=+1
      - '×' channel accumulates E using disc_log9(L_times) and advances p_times when sign=-1
      - sign=0 contributes to T (counter only)
      - κ-27 flips (direction inversion) at t ∈ {27,54,81,108}
      - per window m:
           d1 = S mod 10
           d2 = (S+E) mod 10
           d3 = (3S + 5E + 7T) mod 10
           U_m = 100*d1 + 10*d2 + d3
    """
    pi, pj, dP = seedP
    ti, tj, dT = seedT

    p_plus = [pi % 9, pj % 9]
    p_times = [ti % 9, tj % 9]
    h_plus = list(DIR_VECS[dP])
    h_times = list(DIR_VECS[dT])

    U: List[int] = []

    for m in range(12):
        S = 0
        E = 0
        T = 0
        t_start = 9 * m + 1
        t_end = 9 * (m + 1)

        for t in range(t_start, t_end + 1):
            r = ((t - 1) % 9) + 1
            s = mov3_sign(r)

            if s == +1:
                S += L_plus(p_plus[0], p_plus[1])
                p_plus[0] = (p_plus[0] + h_plus[0]) % 9
                p_plus[1] = (p_plus[1] + h_plus[1]) % 9
            elif s == -1:
                x = L_times(p_times[0], p_times[1])
                E += disc_log9(x)
                p_times[0] = (p_times[0] + h_times[0]) % 9
                p_times[1] = (p_times[1] + h_times[1]) % 9
            else:
                T += 1

            if t in KAPPA_FLIPS:
                # invert directions mod 9 (equivalently swap N<->S and E<->O)
                h_plus[0] = (-h_plus[0]) % 9
                h_plus[1] = (-h_plus[1]) % 9
                h_times[0] = (-h_times[0]) % 9
                h_times[1] = (-h_times[1]) % 9

        d1 = S % 10
        d2 = (S + E) % 10
        d3 = (3 * S + 5 * E + 7 * T) % 10
        U.append(100 * d1 + 10 * d2 + d3)

    return U


def U6_from_seeds(seedP: Tuple[int, int, str], seedT: Tuple[int, int, str]) -> Tuple[int, int, int, int, int, int]:
    U12 = compute_U12(seedP, seedT)
    return tuple(U12[:6])  # first 6 windows


def w6_from_U6(U6: Sequence[int]) -> str:
    """w6 := (-U_k) mod 3, concatenated as 6 trits."""
    return "".join(str((-u) % 3) for u in U6)


# -----------------------------------------------------------------------------
# 1) Lift w6 -> w30 and base-1000 readout (no dial)
# -----------------------------------------------------------------------------

import numpy as np

# Matrices L0, L1 over F3 (from 3.0.alfa "matrices del corpus")
L0 = (np.array(
    [[2, 2, 2, 1, 2, 1],
     [2, 1, 2, 2, 1, 1],
     [1, 0, 0, 1, 0, 2],
     [0, 0, 1, 1, 1, 0],
     [2, 2, 2, 0, 2, 1],
     [2, 1, 2, 1, 0, 0]],
    dtype=int
) % 3)

L1 = (np.array(
    [[2, 1, 2, 0, 2, 2],
     [1, 2, 1, 1, 2, 0],
     [1, 2, 1, 1, 1, 2],
     [0, 1, 0, 0, 2, 1],
     [2, 0, 2, 1, 0, 1],
     [0, 2, 2, 2, 1, 1]],
    dtype=int
) % 3)


def _apply_L(u: np.ndarray, M: np.ndarray) -> np.ndarray:
    return (u.dot(M) % 3).astype(int)


def lift_w6_to_w30(w6: str) -> str:
    """Lift a length-6 word to a length-30 word by the fixed L0/L1 chain.

    Definition:
      u0 = w6
      u1 = u0·L0
      u2 = u1·L0
      u3 = u2·L1
      u4 = u3·L1
      w30 = u0||u1||u2||u3||u4
    """
    u0 = np.array([int(c) for c in w6], dtype=int) % 3
    u1 = _apply_L(u0, L0)
    u2 = _apply_L(u1, L0)
    u3 = _apply_L(u2, L1)
    u4 = _apply_L(u3, L1)
    blocks = [u0, u1, u2, u3, u4]
    w30 = "".join("".join(str(int(x)) for x in b.tolist()) for b in blocks)
    return w30


def triads_from_base3_prefix(word: str, k: int = 4) -> List[int]:
    """Read the first k base-1000 triads from a base-3 word treated as a fraction.

    Interpret the word as an integer N in base 3 (MSB first):
      N = Σ_{i=0}^{L-1} digit[i] * 3^{L-1-i}

    Then the induced fraction is x = N / 3^L in [0,1).
    Base-1000 triads are:
      triad_j = floor(1000^j * x) mod 1000, for j=1..k.

    All computations are exact integer arithmetic.
    """
    L = len(word)
    N = 0
    for c in word:
        N = 3 * N + int(c)

    denom = 3 ** L
    triads: List[int] = []
    for j in range(1, k + 1):
        q = (1000 ** j * N) // denom
        triads.append(int(q % 1000))
    return triads


def w6_to_triads(w6: str, k: int = 4) -> Tuple[str, List[int]]:
    w30 = lift_w6_to_w30(w6)
    tri = triads_from_base3_prefix(w30, k=k)
    return w30, tri


# -----------------------------------------------------------------------------
# 2) Seed scan over 324×324 routes and UID statistics
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class SeedPair:
    seedP: Tuple[int, int, str]
    seedT: Tuple[int, int, str]

    def as_tuple(self) -> Tuple[int, int, str, int, int, str]:
        return (self.seedP[0], self.seedP[1], self.seedP[2], self.seedT[0], self.seedT[1], self.seedT[2])


def iter_seeds() -> Iterable[Tuple[int, int, str]]:
    for i in range(9):
        for j in range(9):
            for d in DIR_KEYS:
                yield (i, j, d)


def scan_seed_space(limit: int | None = None) -> Tuple[Dict[Tuple[int, ...], int], Dict[Tuple[int, ...], SeedPair]]:
    """Scan the full seed space (104,976 runs) unless limit is provided.

    Returns:
      uid_count:  map U6 -> multiplicity (# seed-pairs producing it)
      uid_rep:    canonical representative seed-pair for each U6 (lexicographic)

    Note: this scan is exhaustive and deterministic (no DP, no randomness).
    """
    plus_seeds = list(iter_seeds())
    times_seeds = list(iter_seeds())

    uid_count: Dict[Tuple[int, ...], int] = defaultdict(int)
    uid_rep: Dict[Tuple[int, ...], SeedPair] = {}

    total = 0
    for seedP in plus_seeds:
        for seedT in times_seeds:
            U6 = U6_from_seeds(seedP, seedT)
            uid_count[U6] += 1
            sp = SeedPair(seedP=seedP, seedT=seedT)
            if U6 not in uid_rep:
                uid_rep[U6] = sp
            else:
                if sp.as_tuple() < uid_rep[U6].as_tuple():
                    uid_rep[U6] = sp
            total += 1
            if limit is not None and total >= limit:
                return uid_count, uid_rep

    return uid_count, uid_rep


def build_w6_index(uid_count: Dict[Tuple[int, ...], int], uid_rep: Dict[Tuple[int, ...], SeedPair]) -> Dict[str, List[Tuple[Tuple[int, ...], int]]]:
    """Map each w6 to a list of (U6, multiplicity) pairs."""
    idx: Dict[str, List[Tuple[Tuple[int, ...], int]]] = defaultdict(list)
    for U6, cnt in uid_count.items():
        w6 = w6_from_U6(U6)
        idx[w6].append((U6, cnt))
    # sort each bucket by count desc then lexicographic U6
    for w6, lst in idx.items():
        lst.sort(key=lambda x: (-x[1], x[0]))
    return idx


def choose_canonical_uid_for_w6(w6: str, idx: Dict[str, List[Tuple[Tuple[int, ...], int]]]) -> Tuple[Tuple[int, ...], int]:
    """Choose the canonical U6 for a given w6: max multiplicity, tie-break lexicographic."""
    if w6 not in idx:
        raise KeyError(f"w6 {w6} not present in index")
    return idx[w6][0]


def fmt_seed(seed: Tuple[int, int, str]) -> str:
    return f"({seed[0]},{seed[1]},{seed[2]})"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# -----------------------------------------------------------------------------
# 3) Optional verification against independently evaluated π,e,φ
# -----------------------------------------------------------------------------

def pi_chudnovsky_decimal(precision: int):
    """Evalúa pi con Decimal/Chudnovsky, sin tablas de cifras ni paquetes."""
    from decimal import Decimal, localcontext

    with localcontext() as context:
        context.prec = precision + 15
        multiplier = 1
        linear = 13_591_409
        power = 1
        k_value = 6
        series = Decimal(linear)
        # Cada término aporta aproximadamente catorce cifras decimales.
        for index in range(1, precision // 14 + 3):
            multiplier = (k_value**3 - 16 * k_value) * multiplier // index**3
            linear += 545_140_134
            power *= -262_537_412_640_768_000
            series += Decimal(multiplier * linear) / Decimal(power)
            k_value += 12
        value = Decimal(426_880) * Decimal(10_005).sqrt() / series
        context.prec = precision
        return +value

def triads_of_constant(name: str, k: int = 4) -> List[int]:
    from decimal import Decimal, localcontext

    precision = max(80, 3 * k + 20)
    if name == "pi":
        x = pi_chudnovsky_decimal(precision)
    elif name == "e":
        with localcontext() as context:
            context.prec = precision
            x = Decimal(1).exp()
    elif name in ("phi", "varphi"):
        with localcontext() as context:
            context.prec = precision
            x = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    else:
        raise ValueError(name)

    digits_needed = 3 * k
    s = format(x, "f")
    if "." not in s:
        s += ".0"
    frac = s.split(".", 1)[1]
    frac = (frac + "0" * digits_needed)[:digits_needed]

    triads = [int(frac[3 * i : 3 * (i + 1)]) for i in range(k)]
    return triads


def find_constant_matches(all_w6: Iterable[str], k: int = 4) -> Dict[str, List[Tuple[str, List[int]]]]:
    targets = {
        "pi": triads_of_constant("pi", k=k),
        "e": triads_of_constant("e", k=k),
        "phi": triads_of_constant("phi", k=k),
    }
    matches: Dict[str, List[Tuple[str, List[int]]]] = {"pi": [], "e": [], "phi": []}
    for w6 in all_w6:
        _, tri = w6_to_triads(w6, k=k)
        for name, tgt in targets.items():
            if tri == tgt:
                matches[name].append((w6, tri))
    return matches


# -----------------------------------------------------------------------------
# 4) Main closeout: generate tables + certificate + manifest
# -----------------------------------------------------------------------------


def write_uid_catalog(path: Path, uid_count: Dict[Tuple[int, ...], int]) -> None:
    """Write a UID catalog CSV with U6, multiplicity, and w6."""
    rows = []
    for U6, cnt in uid_count.items():
        w6 = w6_from_U6(U6)
        rows.append((cnt, U6, w6))
    rows.sort(key=lambda x: (-x[0], x[1]))

    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["count", "U6", "w6"])
        for cnt, U6, w6 in rows:
            w.writerow([cnt, "|".join(f"{u:03d}" for u in U6), w6])


def write_seed_witness_table(
    path: Path,
    w6_words: Dict[str, str],
    idx: Dict[str, List[Tuple[Tuple[int, ...], int]]],
    uid_rep: Dict[Tuple[int, ...], SeedPair],
    k_triads: int,
) -> Dict[str, dict]:
    """Write a small CSV witnessing the canonical seed-pair for each named w6.

    Returns a dict summary keyed by name.
    """
    summary: Dict[str, dict] = {}
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "name",
            "w6",
            "canonical_U6",
            "canonical_U6_count",
            "seedP",
            "seedT",
            "w30",
            f"triads_{k_triads}",
            "num_uid_preimages_for_w6",
        ])

        for name, w6 in w6_words.items():
            U6, cnt = choose_canonical_uid_for_w6(w6, idx)
            rep = uid_rep[U6]
            w30, tri = w6_to_triads(w6, k=k_triads)
            preimages = len(idx[w6])

            row = [
                name,
                w6,
                "|".join(f"{u:03d}" for u in U6),
                cnt,
                fmt_seed(rep.seedP),
                fmt_seed(rep.seedT),
                w30,
                "|".join(f"{t:03d}" for t in tri),
                preimages,
            ]
            w.writerow(row)

            summary[name] = {
                "w6": w6,
                "canonical_U6": list(U6),
                "canonical_U6_count": cnt,
                "seedP": rep.seedP,
                "seedT": rep.seedT,
                "w30": w30,
                "triads": tri,
                "num_uid_preimages_for_w6": preimages,
            }

    return summary


def write_manifest(path: Path, files: List[Path]) -> None:
    with path.open("w") as f:
        for fp in sorted(files, key=lambda p: p.name):
            if fp.exists() and fp.is_file():
                f.write(f"{sha256_file(fp)}  {fp.name}\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=".", help="output directory")
    ap.add_argument("--limit", type=int, default=None, help="debug: limit #seedpairs scanned")
    ap.add_argument("--no-verify", action="store_true", help="skip external π/e/φ verification")
    ap.add_argument("--k-triads", type=int, default=4, help="# triads to extract (default 4)")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # The three words from the 3.0.alfa nucleus (claimed outputs of the upstream scan)
    w6_words = {
        "pi": "010211",
        "e": "201101",
        "phi": "121200",
    }

    # 1) Exhaustive upstream scan
    uid_count, uid_rep = scan_seed_space(limit=args.limit)
    idx = build_w6_index(uid_count, uid_rep)

    # 2) Write uid catalog
    uid_csv = outdir / "n33_uid_catalog.csv"
    write_uid_catalog(uid_csv, uid_count)

    # 3) Ensure the three externally recognised w6 words have seed witnesses
    missing = [name for name, w6 in w6_words.items() if w6 not in idx]
    if missing:
        raise SystemExit(f"ERROR: missing w6 in scan: {missing}. (Maybe wrong upstream definition?)")

    witness_csv = outdir / "n33_seed_witness.csv"
    witness_summary = write_seed_witness_table(witness_csv, w6_words, idx, uid_rep, k_triads=args.k_triads)

    require(len(uid_count) == 468, "el catálogo no contiene 468 estados U6")
    require(len(idx) == 243, "el cociente no contiene 243 palabras w6")
    require(_histogram(uid_count.values()) == {"144": 432, "432": 18, "1944": 18},
            "histograma de fibras inesperado")
    expected_triads = {
        "pi": [141, 592, 653, 589],
        "e": [718, 281, 828, 459],
        "phi": [618, 33, 988, 749],
    }
    for name, triads in expected_triads.items():
        require(witness_summary[name]["w6"] == w6_words[name],
                f"testigo w6 inesperado para {name}")
        require(witness_summary[name]["triads"] == triads,
                f"lectura base-1000 inesperada para {name}")

    # 4) Optional: match against π,e,φ by computing triads for all w6 produced
    matches = None
    if not args.no_verify:
        matches = find_constant_matches(idx.keys(), k=args.k_triads)
        expected_matches = {
            name: [(w6_words[name], expected_triads[name])]
            for name in ("pi", "e", "phi")
        }
        require(matches == expected_matches,
                "la comparación externa no identifica de forma única pi/e/phi")

    pass_no_pass = {
        "P1_seed_scan_exhaustive": "PASS" if args.limit is None else "PARTIAL",
        "P2_w6_words_present": "PASS" if not missing else "FAIL",
        "P3_catalogue_enumerated_before_external_recognition": "PASS",
        "P4_external_match_uniqueness": (
            "PASS" if (matches and all(len(matches[n]) == 1 for n in ("pi", "e", "phi")))
            else ("SKIP" if args.no_verify else "FAIL")
        ),
    }
    if not args.no_verify:
        require(all(value == "PASS" for value in pass_no_pass.values()),
                f"estatus no-PASS: {pass_no_pass}")

    # 5) Build certificate
    cert = {
        "N": "N33",
        "purpose": "finite APP catalogue and external recognition of pi/e/phi words",
        "seed_space": {
            "num_plus_seeds": 9 * 9 * 4,
            "num_times_seeds": 9 * 9 * 4,
            "num_seed_pairs": (9 * 9 * 4) ** 2,
            "DIR_KEYS": list(DIR_KEYS),
            "KAPPA_FLIPS": sorted(list(KAPPA_FLIPS)),
        },
        "upstream_definition": {
            "mov3_sign": {"+1": [1, 4, 7], "-1": [2, 5, 8], "0": [3, 6, 9]},
            "disc_log9": DISC_LOG9,
            "window_formula": {
                "d1": "S mod 10",
                "d2": "(S+E) mod 10",
                "d3": "(3S+5E+7T) mod 10",
                "U_m": "100*d1+10*d2+d3",
            },
        },
        "scan_summary": {
            "num_unique_U6": len(uid_count),
            "num_unique_w6": len(idx),
            "uid_count_histogram": _histogram(uid_count.values()),
        },
        "named_w6": witness_summary,
        "lift": {
            "L0": L0.tolist(),
            "L1": L1.tolist(),
            "definition": "u1=u0·L0, u2=u1·L0, u3=u2·L1, u4=u3·L1, w30=u0||u1||u2||u3||u4",
            "triad_read": "triad_j = floor(1000^j * N/3^30) mod 1000",
        },
        "verification": {
            "performed": (not args.no_verify),
            "k_triads": args.k_triads,
            "matches": matches,
        },
        "PASS_NO_PASS": pass_no_pass,
    }

    cert_path = outdir / "HMT_N33_certificate.json"
    cert_path.write_text(json.dumps(cert, indent=2, ensure_ascii=False))

    # 6) Manifest
    manifest_path = outdir / "HMT_N33_MANIFEST.sha256"
    files_for_manifest = [
        outdir / "hmt_n33_pi_e_phi_closeout.py",
        uid_csv,
        witness_csv,
        cert_path,
    ]
    write_manifest(manifest_path, files_for_manifest)

    print("Wrote:")
    for fp in files_for_manifest + [manifest_path]:
        print("  -", fp)
    if args.no_verify:
        print("SKIP — comparación externa pi/e/phi no solicitada")
    else:
        print("PASS — N33: 468 U6, 243 w6 y coincidencias externas únicas")


def _histogram(vals: Iterable[int]) -> Dict[str, int]:
    h: Dict[int, int] = defaultdict(int)
    for v in vals:
        h[int(v)] += 1
    return {str(k): h[k] for k in sorted(h)}


if __name__ == "__main__":
    main()
