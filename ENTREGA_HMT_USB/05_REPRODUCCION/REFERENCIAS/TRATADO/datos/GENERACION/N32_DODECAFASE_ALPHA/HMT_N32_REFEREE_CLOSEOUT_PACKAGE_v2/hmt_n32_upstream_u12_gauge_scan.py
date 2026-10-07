#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hmt_n32_upstream_u12_gauge_scan.py

N32 addendum: exhaustive U6 catalogue from APP/TPK, explicit gauge scan, and
an internal-filter report. The historical filename says upstream_U12, but
this program produces U6 data (and at most the periodic U12cat=U6||U6); it
does not produce the signed dodecaphase witness U12sgn.

This script is designed to be:
  - deterministic
  - self-contained (stdlib only)
  - alpha-free (does not use the fine-structure constant)

Outputs (written next to this script unless overridden by --outdir):
  - n32_u6_seed_table.csv              (104,976 rows: seed -> uid)
  - n32_uid_representative_seed.csv    (468 rows: uid -> lexicographically smallest seed)
  - n32_uid_u6_catalog.csv             (468 rows: uid -> U6, U6 mod 3)
  - n32_variant_scan.json              (variant summaries and constraint pass/fail)
  - HMT_N32_UPSTREAM_U12_CERTIFICATE.json (legacy filename; scope stated inside)

The finite catalogue engine used here matches the "U-seed table" engine
(which appears in the internal material as a 104,976-seed exhaustive scan).

"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
import os
from typing import Dict, Iterable, List, Sequence, Tuple


L = 9
PLUS_SLOTS = {1, 4, 7}
TIMES_SLOTS = {2, 5, 8}
TORSION_SLOTS = {3, 6, 9}
# For U6 (6 events * 9 ticks) we flip at the kappa-27 boundaries inside 54 ticks.
FLIPS_U6 = {27, 54}

# Cardinal steps in (row=i, col=j) coordinates.
DIRS: Dict[str, Tuple[int, int]] = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "O": (0, -1),  # Oeste
}
DIR_KEYS = ("N", "E", "S", "O")


def require(condition: bool, message: str) -> None:
    """Falla de forma explícita incluso con optimización de Python."""
    if not condition:
        raise RuntimeError(f"N32 SCAN FAIL: {message}")


def csv_data_rows(path: str) -> int:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def droot9(n: int) -> int:
    """Digital root modulo 9 with range {1,...,9}."""
    r = n % 9
    return 9 if r == 0 else r


def build_plus9() -> List[List[int]]:
    return [[droot9((i + 1) + (j + 1)) for j in range(L)] for i in range(L)]


def build_times9() -> List[List[int]]:
    return [[droot9((i + 1) * (j + 1)) for j in range(L)] for i in range(L)]


PLUS9 = build_plus9()
TIMES9 = build_times9()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def log9_map_discrete(generator: int) -> Dict[int, int]:
    """Discrete-log map on the unit group (Z/9Z)^× with generator g.

    Units are {1,2,4,5,7,8}. Non-units (multiples of 3) are mapped to 0.

    Returns a dict on digits 1..9 with values in {0,...,5}.

    Note: This is *not* a logarithm on the full semigroup; it's a log on units and
    a "root-kill" (0) on 3,6,9.
    """
    if generator not in (2, 5):
        raise ValueError("generator must be 2 or 5 for (Z/9Z)^×")

    # Build exponent table on the 6-cycle.
    exp_of: Dict[int, int] = {}
    x = 1
    for k in range(6):
        exp_of[x] = k
        x = (x * generator) % 9

    out: Dict[int, int] = {}
    for d in range(1, 10):
        if d % 3 == 0:
            out[d] = 0
        else:
            out[d] = exp_of[d]
    return out


def log9_map_3adic_valuation() -> Dict[int, int]:
    """3-adic valuation v3(d) for digits 1..9.

    1,2,4,5,7,8 -> 0
    3,6 -> 1
    9 -> 2

    (This variant is included in H as a "reasonable" alternative twist; it is *not*
    the canonical choice in the upstream material.)
    """
    out: Dict[int, int] = {}
    for d in range(1, 10):
        n = 0
        x = d
        while x % 3 == 0:
            x //= 3
            n += 1
        out[d] = n
    return out


def log9_map_identity() -> Dict[int, int]:
    """Identity map: d -> d. (Alternative, not canonical.)"""
    return {d: d for d in range(1, 10)}


def check_log9_constraints(logmap: Dict[int, int], *, generator: int | None = None) -> Dict[str, bool]:
    """Internal constraints for the twist map ("neighbor 3-adic")."""
    # C_root: multiples of 3 map to 0.
    c_root = (logmap[3] == 0 and logmap[6] == 0 and logmap[9] == 0)

    # C_unit_hom: on units, map is a homomorphism into Z/6Z (mod 6).
    units = [1, 2, 4, 5, 7, 8]
    ok = True
    for a in units:
        for b in units:
            ab = (a * b) % 9
            if ab == 0:
                ok = False
                break
            # discrete log property holds mod 6
            if (logmap[ab] - (logmap[a] + logmap[b])) % 6 != 0:
                ok = False
                break
        if not ok:
            break

    # C_gen_min: optional, choose smallest primitive generator (2).
    # If a generator is supplied, check that logmap(generator)=1.
    c_gen = True
    if generator is not None:
        c_gen = (logmap[generator] % 6 == 1)

    return {
        "C_root_kill": c_root,
        "C_unit_hom_mod6": ok,
        "C_generator_maps_to_1": c_gen,
    }


def simulate_plus_S(seedP: Tuple[int, int], hP0: Tuple[int, int]) -> List[int]:
    """Compute S-event sums for 6 events (U6) for a given PLUS seed."""
    p = [seedP[0], seedP[1]]
    h = [hP0[0], hP0[1]]
    t_global = 0
    out: List[int] = []
    for _event in range(6):
        S = 0
        for _k in range(9):
            t_global += 1
            r = ((t_global - 1) % 9) + 1
            if r in PLUS_SLOTS:
                i, j = p
                S += PLUS9[i][j]
                p[0] = (p[0] + h[0]) % 9
                p[1] = (p[1] + h[1]) % 9
            if t_global in FLIPS_U6:
                h[0] = (-h[0]) % 9
                h[1] = (-h[1]) % 9
        out.append(S)
    return out


def simulate_times_digits(seedT: Tuple[int, int], hT0: Tuple[int, int]) -> List[List[int]]:
    """Collect TIMES-layer digits encountered in the 3 TIMES slots per event (6 events)."""
    p = [seedT[0], seedT[1]]
    h = [hT0[0], hT0[1]]
    t_global = 0
    out: List[List[int]] = []
    for _event in range(6):
        digs: List[int] = []
        for _k in range(9):
            t_global += 1
            r = ((t_global - 1) % 9) + 1
            if r in TIMES_SLOTS:
                i, j = p
                digs.append(TIMES9[i][j])
                p[0] = (p[0] + h[0]) % 9
                p[1] = (p[1] + h[1]) % 9
            if t_global in FLIPS_U6:
                h[0] = (-h[0]) % 9
                h[1] = (-h[1]) % 9
        # should be 3 digits per event
        out.append(digs)
    return out


def triad_from_SE(S: int, E: int, T: int = 3) -> int:
    """Base-1000 triad from (S,E,T) event sums."""
    d1 = S % 10
    d2 = (S + E) % 10
    d3 = (3 * S + 5 * E + 7 * T) % 10
    return 100 * d1 + 10 * d2 + d3


@dataclasses.dataclass(frozen=True)
class Variant:
    name: str
    logmap: Dict[int, int]
    generator_for_constraint: int | None = None


def build_seed_lists() -> Tuple[List[Tuple[int, int, str]], List[Tuple[int, int, str]]]:
    plus_seeds: List[Tuple[int, int, str]] = []
    times_seeds: List[Tuple[int, int, str]] = []
    for i in range(9):
        for j in range(9):
            for h in DIR_KEYS:
                plus_seeds.append((i, j, h))
                times_seeds.append((i, j, h))
    return plus_seeds, times_seeds


def scan_u6_for_variant(variant: Variant, *, write_tables: bool, outdir: str) -> Dict[str, object]:
    """Scan all 104,976 seeds for a given variant.

    Returns a summary dict and optionally writes tables.
    """
    plus_seeds, times_seeds = build_seed_lists()

    # Precompute S-vectors for each plus-seed.
    S_by_plus: Dict[Tuple[int, int, str], List[int]] = {}
    for iP, jP, hP in plus_seeds:
        S_by_plus[(iP, jP, hP)] = simulate_plus_S((iP, jP), DIRS[hP])

    # Precompute TIMES digits (not yet mapped) for each times-seed.
    digs_by_times: Dict[Tuple[int, int, str], List[List[int]]] = {}
    for iT, jT, hT in times_seeds:
        digs_by_times[(iT, jT, hT)] = simulate_times_digits((iT, jT), DIRS[hT])

    # Precompute E-vectors for this variant.
    E_by_times: Dict[Tuple[int, int, str], List[int]] = {}
    lm = variant.logmap
    for seedT, digs_events in digs_by_times.items():
        E_by_times[seedT] = [sum(lm[d] for d in digs) for digs in digs_events]

    # Scan all pairs.
    U6_to_count: Dict[Tuple[int, int, int, int, int, int], int] = {}
    seed_to_u6: Dict[Tuple[int, int, str, int, int, str], Tuple[int, int, int, int, int, int]] = {}

    for iP, jP, hP in plus_seeds:
        S_vec = S_by_plus[(iP, jP, hP)]
        for iT, jT, hT in times_seeds:
            E_vec = E_by_times[(iT, jT, hT)]
            U6 = tuple(triad_from_SE(S_vec[m], E_vec[m], 3) for m in range(6))
            U6_to_count[U6] = U6_to_count.get(U6, 0) + 1
            if write_tables:
                seed_to_u6[(iP, jP, hP, iT, jT, hT)] = U6

    uniq_u6 = len(U6_to_count)
    # Assign uids by sorting U6.
    U6_sorted = sorted(U6_to_count.keys())
    uid_of = {U6: idx for idx, U6 in enumerate(U6_sorted)}

    # Representative seeds (lexicographically smallest) per uid.
    reps: Dict[int, Tuple[int, int, str, int, int, str]] = {uid: None for uid in range(uniq_u6)}  # type: ignore

    if write_tables:
        # Write seed -> uid table.
        seed_path = os.path.join(outdir, "n32_u6_seed_table.csv")
        with open(seed_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["iP", "jP", "hP", "iT", "jT", "hT", "uid"])
            for seed, U6 in seed_to_u6.items():
                iP, jP, hP, iT, jT, hT = seed
                uid = uid_of[U6]
                w.writerow([iP, jP, hP, iT, jT, hT, uid])
                if reps[uid] is None or seed < reps[uid]:
                    reps[uid] = seed

        # Write representative table.
        rep_path = os.path.join(outdir, "n32_uid_representative_seed.csv")
        with open(rep_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["uid", "iP", "jP", "hP", "iT", "jT", "hT"])
            for uid in range(uniq_u6):
                seed = reps[uid]
                require(seed is not None, f"uid {uid} sin semilla representante")
                iP, jP, hP, iT, jT, hT = seed
                w.writerow([uid, iP, jP, hP, iT, jT, hT])

        # Write uid -> U6 catalog.
        cat_path = os.path.join(outdir, "n32_uid_u6_catalog.csv")
        with open(cat_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["uid", "U6", "U6_mod3"])
            for uid, U6 in enumerate(U6_sorted):
                mod3 = tuple((-u) % 3 for u in U6)
                w.writerow([uid, "|".join(f"{x:03d}" for x in U6), "".join(str(x) for x in mod3)])

    # Fiber-size stats
    counts = list(U6_to_count.values())
    counts.sort()
    summary_counts = {
        "min": counts[0],
        "max": counts[-1],
        "unique_fiber_sizes": len(set(counts)),
    }

    return {
        "variant": variant.name,
        "unique_U6": uniq_u6,
        "seed_count": 104_976,
        "fiber_stats": summary_counts,
        "log_constraints": check_log9_constraints(variant.logmap, generator=variant.generator_for_constraint),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=".", help="Output directory")
    ap.add_argument("--fast", action="store_true", help="Skip writing the 104,976-row seed table")
    args = ap.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    # Define a small, explicit H of reasonable twist variants.
    variants: List[Variant] = [
        Variant(
            name="LOG9_discrete_log_gen2_canonical",
            logmap=log9_map_discrete(2),
            generator_for_constraint=2,
        ),
        Variant(
            name="LOG9_discrete_log_gen5_alt",
            logmap=log9_map_discrete(5),
            generator_for_constraint=5,
        ),
        Variant(
            name="LOG9_3adic_valuation_alt",
            logmap=log9_map_3adic_valuation(),
        ),
        Variant(
            name="LOG9_identity_alt",
            logmap=log9_map_identity(),
        ),
    ]

    scan_summaries: List[Dict[str, object]] = []

    # Run canonical variant with full tables (unless --fast).
    write_tables = not args.fast
    canonical_summary = scan_u6_for_variant(variants[0], write_tables=write_tables, outdir=outdir)
    scan_summaries.append(canonical_summary)

    # Run other variants without writing huge tables.
    for v in variants[1:]:
        scan_summaries.append(scan_u6_for_variant(v, write_tables=False, outdir=outdir))

    # Gate matemático: fija cardinalidades, fibras y restricciones del calibre.
    observed = [
        (
            summary["variant"],
            summary["seed_count"],
            summary["unique_U6"],
            summary["fiber_stats"],
            summary["log_constraints"],
        )
        for summary in scan_summaries
    ]
    expected = [
        (
            "LOG9_discrete_log_gen2_canonical", 104_976, 468,
            {"min": 144, "max": 1944, "unique_fiber_sizes": 3},
            {"C_root_kill": True, "C_unit_hom_mod6": True,
             "C_generator_maps_to_1": True},
        ),
        (
            "LOG9_discrete_log_gen5_alt", 104_976, 468,
            {"min": 144, "max": 1944, "unique_fiber_sizes": 3},
            {"C_root_kill": True, "C_unit_hom_mod6": True,
             "C_generator_maps_to_1": True},
        ),
        (
            "LOG9_3adic_valuation_alt", 104_976, 144,
            {"min": 432, "max": 1296, "unique_fiber_sizes": 4},
            {"C_root_kill": False, "C_unit_hom_mod6": True,
             "C_generator_maps_to_1": True},
        ),
        (
            "LOG9_identity_alt", 104_976, 684,
            {"min": 72, "max": 1296, "unique_fiber_sizes": 4},
            {"C_root_kill": False, "C_unit_hom_mod6": False,
             "C_generator_maps_to_1": True},
        ),
    ]
    require(observed == expected, "resumen de variantes distinto del rector")

    if write_tables:
        table_rows = {
            "n32_u6_seed_table.csv": 104_976,
            "n32_uid_representative_seed.csv": 468,
            "n32_uid_u6_catalog.csv": 468,
        }
        for filename, row_count in table_rows.items():
            path = os.path.join(outdir, filename)
            require(os.path.isfile(path), f"no se produjo {filename}")
            require(csv_data_rows(path) == row_count,
                    f"{filename} no contiene {row_count} filas de datos")

    variant_path = os.path.join(outdir, "n32_variant_scan.json")
    with open(variant_path, "w", encoding="utf-8") as f:
        json.dump({"variants": scan_summaries}, f, indent=2, sort_keys=True)

    # Build a certificate with hashes.
    cert = {
        "script": os.path.basename(__file__),
        "logical_scope": (
            "Exhaustive U6 catalogue and gauge scan only. "
            "It does not extract the frozen signed U12 witness."
        ),
        "legacy_filename_notice": (
            "UPSTREAM_U12 refers historically to periodic U12cat=U6||U6, "
            "not to U12sgn."
        ),
        "outdir": os.path.relpath(outdir, start=os.getcwd()),
        "outdir_path_kind": "relative_to_execution_directory",
        "produced": {
            "n32_variant_scan.json": sha256_file(variant_path),
        },
        "canonical": {
            "variant": variants[0].name,
            "summary": canonical_summary,
        },
    }

    if write_tables:
        for fn in ["n32_u6_seed_table.csv", "n32_uid_representative_seed.csv", "n32_uid_u6_catalog.csv"]:
            p = os.path.join(outdir, fn)
            if os.path.exists(p):
                cert["produced"][fn] = sha256_file(p)

    cert_path = os.path.join(outdir, "HMT_N32_UPSTREAM_U12_CERTIFICATE.json")
    with open(cert_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, sort_keys=True)

    print("Wrote:", variant_path)
    if write_tables:
        print("Wrote:", os.path.join(outdir, "n32_u6_seed_table.csv"))
        print("Wrote:", os.path.join(outdir, "n32_uid_representative_seed.csv"))
        print("Wrote:", os.path.join(outdir, "n32_uid_u6_catalog.csv"))
    print("Wrote:", cert_path)
    print("PASS — catálogo U6 N32, calibres y cardinalidades verificados")


if __name__ == "__main__":
    main()
