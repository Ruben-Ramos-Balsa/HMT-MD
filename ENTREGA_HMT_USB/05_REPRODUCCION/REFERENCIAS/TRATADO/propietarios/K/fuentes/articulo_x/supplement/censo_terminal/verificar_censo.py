#!/usr/bin/env python3
"""Exact terminal census from already-published HMT output cylinders.

Only the Python standard library is used. The historical N38 encoder and
its ACT-derived profile are not imported or executed. The declared reader
profile is an explicit premise, not an output proved universal by counting.
All validation remains active under -O. This program writes only stdout.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUTS = (HERE.parent / "alpha_completa" / "certificados"
           / "ley_nueve_puertas_2026-07-30" / "salidas")
CHANNELS = ("pi", "e", "phi")
P_LENGTH, R_LENGTH, L_LENGTH, TRIADS = 30, 1050, 1080, 171
PROFILE = {
    "dots_mod3": (2, 2, 0),
    "norms_mod3": (0, 0, 0),
    "row_weights_integer": (3, 3, 3),
    "hamming_integer": (2, 5, 3),
    "rank_mod3": 3,
    "column_weights_integer": (1, 1, 2, 2, 3, 0),
    "column_sums_mod3": (1, 2, 2, 1, 2, 0),
    "orientation_mod3": (1, 1, 2),
}
CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def digits(n, length, base=3):
    out = [0] * length
    for i in range(length - 1, -1, -1):
        n, out[i] = divmod(n, base)
    require(n == 0, "Digit length overflow")
    return tuple(out)


def stable_floor(numerator, denominator, multiplier):
    """Image floor of the complete half-open interval [n/d,(n+1)/d)."""
    lo = numerator * multiplier // denominator
    hi = ((numerator + 1) * multiplier - 1) // denominator
    require(lo == hi, "Published cylinder does not certify a stable floor")
    return lo


def intersecting_cylinders(t, q, d, base, space):
    """R with [ (base+R)/d,(base+R+1)/d ) meeting [t/q,(t+1)/q)."""
    lo = max(0, t * d // q - base)
    hi = min(space - 1, ((t + 1) * d - 1) // q - base)
    return lo, hi


def catalog(name):
    path = OUTPUTS / (name + "_1000_decimales.txt")
    raw = path.read_bytes()
    integer, fraction = raw.decode("ascii").strip().split(".")
    require(integer.isdigit() and fraction.isdigit(), "Nondecimal output")
    require(len(fraction) == 1000, "Expected exactly 1000 fractional digits")
    n, den = int(fraction), 10 ** len(fraction)
    p = stable_floor(n, den, 3 ** P_LENGTH)
    t = stable_floor(n, den, 1000 ** TRIADS)
    d, q, space = 3 ** L_LENGTH, 1000 ** TRIADS, 3 ** R_LENGTH
    base = p * space
    lo, hi = intersecting_cylinders(t, q, d, base, space)
    require(lo <= hi, "Empty terminal catalog")
    require(0 < lo <= hi < space - 1, "Unexpected clipping at prefix boundary")
    require(hi - lo + 1 < 729, "Six-trit reduction is not injective")
    rows = [digits((lo + i) % 729, 6) for i in range(hi - lo + 1)]
    for value in (lo, hi):
        require((base + value) * q < (t + 1) * d,
                "Right decimal boundary does not intersect")
        require((base + value + 1) * q > t * d,
                "Left decimal boundary does not intersect")
    require((base + lo) * q <= t * d, "Previous cell not excluded")
    require((base + hi + 1) * q >= (t + 1) * d, "Next cell not excluded")
    # This subsequent readout does not participate in the catalog or filters.
    observed_word = stable_floor(n, den, d)
    observed_tail = observed_word - base
    require(lo <= observed_tail <= hi, "Observed output lies outside its catalog")
    record = {
        "output_path_relative_to_supplement": str(path.relative_to(HERE.parent)),
        "output_sha256": hashlib.sha256(raw).hexdigest(),
        "fractional_digits": len(fraction),
        "prefix_integer_P": p,
        "prefix_trits": "".join(map(str, digits(p, P_LENGTH))),
        "triad_integer_T": str(t),
        "R_lo": str(lo), "R_hi": str(hi), "count": len(rows),
        "first_boundary_integer_mod729": lo % 729,
        "last_boundary_integer_mod729": hi % 729,
        "catalog_boundary_words": ["".join(map(str, row)) for row in rows],
        "subsequent_output_comparison": {
            "rank_one_based": observed_tail - lo + 1,
            "boundary": "".join(map(str, digits(observed_word % 729, 6))),
        },
    }
    return rows, record


def dot(a, b):
    return sum(x * y for x, y in zip(a, b)) % 3


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def weight(a):
    return sum(x != 0 for x in a)


def bit_count(mask):
    # Also supports Python versions preceding int.bit_count().
    return bin(mask).count("1")


def rank_mod3(rows):
    m = [list(row) for row in rows]
    rank = 0
    for column in range(6):
        pivot = next((i for i in range(rank, len(m)) if m[i][column] % 3), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        inverse = m[rank][column] % 3
        m[rank] = [(inverse * v) % 3 for v in m[rank]]
        for i in range(len(m)):
            if i != rank:
                factor = m[i][column]
                m[i] = [(v - factor * w) % 3 for v, w in zip(m[i], m[rank])]
        rank += 1
        if rank == len(m):
            break
    return rank


def pair_masks(left, right, expected_dot, expected_hamming):
    dots, distances = [], []
    for a in left:
        dmask, hmask = 0, 0
        for j, b in enumerate(right):
            if dot(a, b) == expected_dot:
                dmask |= 1 << j
            if hamming(a, b) == expected_hamming:
                hmask |= 1 << j
        dots.append(dmask)
        distances.append(hmask)
    return dots, distances


def census(catalogs):
    pi, e, phi = (catalogs[name] for name in CHANNELS)
    p = PROFILE
    dp, hp = pair_masks(pi, phi, p["dots_mod3"][1], p["hamming_integer"][1])
    de, he = pair_masks(e, phi, p["dots_mod3"][2], p["hamming_integer"][2])
    nphi = sum(1 << k for k, row in enumerate(phi) if dot(row, row) == p["norms_mod3"][2])
    wphi = sum(1 << k for k, row in enumerate(phi) if weight(row) == p["row_weights_integer"][2])
    counts = {"all": len(pi) * len(e) * len(phi), "dots": 0,
              "dots_norms": 0, "dots_norms_weights": 0, "full_local": 0}
    contributions = []
    triples = []
    for i, a in enumerate(pi):
        local = [0, 0, 0, 0]
        for j, b in enumerate(e):
            if dot(a, b) != p["dots_mod3"][0]:
                continue
            mask = dp[i] & de[j]
            local[0] += bit_count(mask)
            if (dot(a, a), dot(b, b)) != p["norms_mod3"][:2]:
                continue
            mask &= nphi
            local[1] += bit_count(mask)
            if (weight(a), weight(b)) != p["row_weights_integer"][:2]:
                continue
            mask &= wphi
            local[2] += bit_count(mask)
            if hamming(a, b) != p["hamming_integer"][0]:
                continue
            mask &= hp[i] & he[j]
            local[3] += bit_count(mask)
            while mask:
                bit = mask & -mask
                k = bit.bit_length() - 1
                triples.append((i, j, k))
                mask ^= bit
        contributions.append(local)
    keys = ("dots", "dots_norms", "dots_norms_weights", "full_local")
    for position, key in enumerate(keys):
        counts[key] = sum(row[position] for row in contributions)
    require(counts["full_local"] == len(triples), "Mask/enumeration disagreement")
    rank_survivors, weight_survivors, column_survivors, selected = [], [], [], []
    for i, j, k in triples:
        rows = (pi[i], e[j], phi[k])
        # Independent scalar checks on every candidate emitted by the masks.
        require(tuple(dot(rows[u], rows[v]) for u, v in ((0, 1), (0, 2), (1, 2))) == p["dots_mod3"], "Dot mask error")
        require(tuple(dot(row, row) for row in rows) == p["norms_mod3"], "Norm mask error")
        require(tuple(weight(row) for row in rows) == p["row_weights_integer"], "Weight mask error")
        require(tuple(hamming(rows[u], rows[v]) for u, v in ((0, 1), (0, 2), (1, 2))) == p["hamming_integer"], "Hamming mask error")
        item = {"ranks": [i + 1, j + 1, k + 1],
                "matrix": [list(row) for row in rows],
                "row_sums_mod3": [sum(row) % 3 for row in rows]}
        if rank_mod3(rows) != p["rank_mod3"]:
            continue
        rank_survivors.append(item)
        columns = tuple(zip(*rows))
        if tuple(weight(col) for col in columns) != p["column_weights_integer"]:
            continue
        weight_survivors.append(item)
        if tuple(sum(col) % 3 for col in columns) != p["column_sums_mod3"]:
            continue
        column_survivors.append(item)
        sigma = p["orientation_mod3"]
        if any(item["row_sums_mod3"] == [(t * s) % 3 for s in sigma] for t in range(3)):
            selected.append(item)
    counts.update(rank=len(rank_survivors), rank_column_weights=len(weight_survivors),
                  rank_column_weights_sums=len(column_survivors), oriented=len(selected))
    return {"counts": counts, "contributions_by_pi_rank": contributions,
            "full_local_rank_triples": [[i + 1, j + 1, k + 1] for i, j, k in triples],
            "column_survivors": column_survivors, "selected": selected}


def small_endpoint_tests():
    cases = 0
    for d in range(1, 12):
        for q in range(1, 12):
            for t in range(q):
                lo, hi = intersecting_cylinders(t, q, d, 0, d)
                by_formula = list(range(lo, hi + 1))
                by_overlap = [n for n in range(d)
                              if n * q < (t + 1) * d and (n + 1) * q > t * d]
                require(by_formula == by_overlap, "Semi-open endpoint convention failed")
                cases += 1
    return cases


def main():
    require(P_LENGTH + R_LENGTH == L_LENGTH, "Length mismatch")
    require(1000 ** TRIADS <= 3 ** L_LENGTH < 1000 ** (TRIADS + 1), "Capacity mismatch")
    endpoint_cases = small_endpoint_tests()
    catalogs, records = {}, {}
    for name in CHANNELS:
        catalogs[name], records[name] = catalog(name)
    result = census(catalogs)
    expected = {"all": 7567952, "dots": 275794, "dots_norms": 6235,
                "dots_norms_weights": 3127, "full_local": 331,
                "rank_column_weights_sums": 2, "oriented": 1}
    for key, value in expected.items():
        require(result["counts"][key] == value, "Census mismatch: " + key)
    require([records[n]["count"] for n in CHANNELS] == [196, 197, 196], "Catalog counts changed")
    require([records[n]["first_boundary_integer_mod729"] for n in CHANNELS] == [67, 584, 117], "Catalog starts changed")
    require(result["selected"][0]["ranks"] == [records[n]["subsequent_output_comparison"]["rank_one_based"] for n in CHANNELS], "Selection differs from subsequent output readout")
    payload = {
        "schema": "HMT.terminal_census.output_cylinders.explicit_reader.v1",
        "scope": "Exact finite census with declared output cylinders and reader profile; no claim of universal profile derivation.",
        "inputs": "Previously published HMT output cylinders; no N38/x0/ACT input, no alpha values.",
        "parameters": {"prefix_trits": P_LENGTH, "tail_trits": R_LENGTH,
                       "total_trits": L_LENGTH, "decimal_triads": TRIADS},
        "declared_profile": PROFILE, "catalogs": records, **result,
        "small_endpoint_test_cases": endpoint_cases, "exact_checks": CHECKS,
        "result": "EXACT_FINITE_CENSUS_REPRODUCED_WITH_EXPLICIT_PREMISES",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
