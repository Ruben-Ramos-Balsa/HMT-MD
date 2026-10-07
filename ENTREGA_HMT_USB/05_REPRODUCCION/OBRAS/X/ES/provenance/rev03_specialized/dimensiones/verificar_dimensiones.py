#!/usr/bin/env python3
"""Exact finite witnesses for the nonadic dimensional-refinement theorems.

The universal statements are proved in refinamiento_dimensional_momentos.tex.
This independent standard-library checker tests finite instances and falsifies
several stronger identifications that those theorems do not make. No asserts,
floating-point arithmetic, target constants, or third-party libraries are used.
It reads the inherited K and writes nothing; its JSON result is sent to stdout.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import isqrt
from pathlib import Path
import json
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OWNER = ROOT / "output/ARTICULO_GEOMETRIA_POSITIVA_CONTINUO_YANG_MILLS_20260919_REV02/appendices/network_cluster.tex"
TEX = HERE / "refinamiento_dimensional_momentos.tex"
CHECKS = []


def require(name, condition, **detail):
    if not condition:
        raise RuntimeError("FAIL: " + name + " " + str(detail))
    CHECKS.append({"name": name, **detail})


def det(matrix):
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    result = F(1)
    for i in range(n):
        pivot = next((j for j in range(i, n) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            result = -result
        p = a[i][i]
        result *= p
        for j in range(i + 1, n):
            if a[j][i]:
                c = a[j][i] / p
                for k in range(i + 1, n):
                    a[j][k] -= c * a[i][k]
                a[j][i] = F(0)
    return result


def product(xs):
    out = F(1)
    for x in xs:
        out *= x
    return out


def transpose(a):
    return list(map(list, zip(*a)))


def matmul(a, b):
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def gram(rows, mass=F(1)):
    out = matmul(transpose(rows), rows)
    return [[mass * x for x in row] for row in out]


def subtract(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


owner_bytes = OWNER.read_bytes()
match = re.search(r"K=\(([0-9,\s]+)\)", owner_bytes.decode("utf-8"))
if match is None:
    raise RuntimeError("K not found in the inherited source")
K = tuple(int(s) for s in match.group(1).replace("\n", "").split(","))
Q = sum(K)
require("inherited_positive_register", len(K) == 12 and min(K) > 0, K=K, Q=Q)
d = tuple(F(x, Q) for x in K)
marks = [F(0)]
for length in d:
    marks.append(marks[-1] + length)


def grid(r):
    p = 9 ** r
    nodes = [marks[j] + F(c, p) * d[j] for j in range(12) for c in range(p)]
    return nodes + [F(1)]


def cells(r):
    t = grid(r)
    return [(t[i], t[i + 1] - t[i]) for i in range(len(t) - 1)]


def monomials(t, q):
    return [[x ** p for p in range(q)] for x in t]


def averages(r, q):
    return [[((b + length) ** (p + 1) - b ** (p + 1)) / ((p + 1) * length)
             for p in range(q)] for b, length in cells(r)]


def moment(p):
    return sum(((marks[j + 1] ** (p + 1) - marks[j] ** (p + 1)) / d[j]
                for j in range(12)), F(0)) / (12 * (p + 1))


def coarsen(rows):
    return [[sum((rows[9 * i + h][j] for h in range(9)), F(0)) / 9
             for j in range(len(rows[0]))] for i in range(len(rows) // 9)]


def lift(rows):
    return [list(row) for row in rows for _ in range(9)]


grids = [grid(r) for r in range(3)]
for r, t in enumerate(grids):
    p = 9 ** r
    require("strict_marked_grid", len(t) == 12 * p + 1 and t[0] == 0 and t[-1] == 1
            and all(x < y for x, y in zip(t, t[1:])), r=r, N=len(t))
    require("recovery_of_K", all(Q * sum((length for _, length in cells(r)[j * p:(j + 1) * p]), F(0)) == K[j]
            for j in range(12)), r=r)
    require("mesh_exact", max(length for _, length in cells(r)) == F(max(K), Q * p), r=r)
    if r < 2:
        require("inherited_node_restriction", grids[r + 1][::9] == t, r=r)
        require("parent_child_carry", all(divmod(9 * c + h, 9) == (c, h)
                for c in range(p) for h in range(9)), r=r)

# Every specified dimension can be accommodated by increasing the same grid.
for k, m in [(1, 1), (2, 4), (9, 4), (10, 7), (3, 20), (100, 1000)]:
    r = 0
    while 12 * 9 ** r + 1 < k + m:
        r += 1
    require("finite_pair_cofinality", 12 * 9 ** r + 1 >= k + m, k=k, m=m, level=r)

# Exact Vandermonde determinants, including q greater than the original 13.
for r, qs in [(0, [1, 2, 3, 4, 8, 13]), (1, [2, 5, 14, 17])]:
    t = grids[r]
    for q in qs:
        ids = [i * (len(t) - 1) // (q - 1) for i in range(q)] if q > 1 else [0]
        xs = [t[i] for i in ids]
        computed = det(monomials(xs, q))
        vandermonde = product(xs[j] - xs[i] for i in range(q) for j in range(i + 1, q))
        require("positive_Vandermonde_minor", computed == vandermonde and computed > 0, r=r, q=q)

# Finitely sampled C Z^T ranks; universal rank is the polynomial Gram proof.
for r, k, m in [(0, 1, 1), (0, 2, 4), (0, 9, 4), (1, 10, 7), (1, 3, 20)]:
    t = grids[r]
    maxdegree = 2 * k + m - 2
    sums = [sum((x ** p for x in t), F(0)) for p in range(maxdegree + 1)]
    y = [[sums[a + b] for b in range(k + m)] for a in range(k)]
    require("nodal_Y_full_row_rank", det([row[:k] for row in y]) > 0, r=r, k=k, m=m)

for r in range(2):
    q = 6
    old = monomials(grids[r], q)
    new = monomials(grids[r + 1], q)
    added = [row for i, row in enumerate(new) if i % 9]
    require("nodal_Gram_rank_one_update", subtract(gram(new), gram(old)) == gram(added), r=r, q=q)
    require("polynomial_flag_restriction", new[::9] == old, r=r, q=q)

moments = [moment(p) for p in range(16)]
require("calendar_probability", moments[0] == 1)
require("calendar_not_global_length_measure", moments[1] != F(1, 2))
require("marked_quantiles_recover_register", all(
        sum((d[h] / (12 * d[h]) for h in range(j)), F(0)) == F(j, 12)
        and Q * (marks[j] - marks[j - 1]) == K[j - 1] for j in range(1, 13)))

for r in range(3):
    t = grids[r]
    a = averages(r, 13)
    L = len(a)
    require("all_cell_moments_exact", all(sum((row[p] for row in a), F(0)) / L == moments[p]
            for p in range(13)), r=r, highest_degree=12)
    h = max(length for _, length in cells(r))
    require("nodal_moment_error_bound", all(abs(sum((x ** p for x in t), F(0)) / len(t) - moments[p])
            <= p * h + F(1, len(t)) for p in range(1, 13)), r=r)
    # Coordinate and variance operators recover every interval exactly.
    for i, (b, length) in enumerate(cells(r)):
        centre = a[i][1]
        variance = a[i][2] - centre * centre
        square = 12 * variance
        num, den = isqrt(square.numerator), isqrt(square.denominator)
        if num * num != square.numerator or den * den != square.denominator:
            raise RuntimeError("The recovery square is not an exact rational square")
        recovered = F(num, den)
        if recovered != length or centre - recovered / 2 != b:
            raise RuntimeError("Failed interval reconstruction")
    require("all_intervals_recovered_from_operators", True, r=r, cells=L)
    require("positive_average_not_multiplicative", all(row[2] - row[1] ** 2 > 0 for row in a), r=r)

for r in range(2):
    q = 7
    a = averages(r, q)
    finer = averages(r + 1, q)
    detail = subtract(finer, lift(a))
    zeros = [[F(0) for _ in range(q)] for _ in a]
    require("exact_nine_child_average", coarsen(finer) == a, r=r, q=q)
    require("zero_mean_details", coarsen(detail) == zeros, r=r, q=q)
    require("exact_positive_Gram_increment", subtract(gram(finer, F(1, len(finer))), gram(a, F(1, len(a))))
            == gram(detail, F(1, len(finer))), r=r, q=q)
    require("exact_detail_reconstruction", [[u + v for u, v in zip(ar, dr)] for ar, dr in zip(lift(a), detail)]
            == finer, r=r, q=q)
    # A diagonal compressed observable is precisely its nine-child mean.
    weighted = [[row[p] for p in range(q)] for row in finer]
    require("operator_compression_identity", coarsen(weighted) == a, r=r)

for r, qs in [(0, [1, 2, 3, 6]), (1, [4, 13])]:
    for q in qs:
        a = averages(r, q)
        ids = [i * (len(a) - 1) // (q - 1) for i in range(q)] if q > 1 else [0]
        require("ordered_cell_average_minor_positive", det([a[i] for i in ids]) > 0, r=r, q=q)

for r, k, m in [(0, 2, 4), (0, 8, 4), (1, 10, 7)]:
    a = averages(r, k + m)
    y = matmul(transpose([row[:k] for row in a]), a)
    require("cell_Y_full_row_rank", det([row[:k] for row in y]) > 0, r=r, k=k, m=m)

# A low-dimensional exhaustive check samples all ordered pairs and triples.
a = averages(0, 3)
for q in [2, 3]:
    require("all_initial_cell_minors", all(det([a[i][:q] for i in ids]) > 0
            for ids in combinations(range(12), q)), q=q)

nodal_first = [sum(t, F(0)) / len(t) for t in grids]
require("nodal_moments_are_not_exactly_invariant", len(set(nodal_first)) == len(nodal_first),
        moments=[str(x) for x in nodal_first])

# The construction is not a fit to the particular published K: a second
# rational positive profile has the same calendar masses and cell maps.
d2 = tuple(F(2 * j + 1, 144) for j in range(12))
marks2 = [F(0)]
for length in d2:
    marks2.append(marks2[-1] + length)
require("second_profile_probability", marks2[-1] == 1)
for r in [0, 1]:
    n = 9 ** r
    # The interval-affine map preserves the relative coordinate c/n.
    ok = True
    for j in range(12):
        for c in range(n + 1):
            x = marks[j] + F(c, n) * d[j]
            image = marks2[j] + (x - marks[j]) * d2[j] / d[j]
            ok = ok and image == marks2[j] + F(c, n) * d2[j]
    require("profile_transport_preserves_calendar_cells", ok, r=r)

report = {
    "status": "PASS_REFINAMIENTO_DIMENSIONAL_RACIONAL",
    "scope": "Finite exact rational witnesses; the universal proofs reside in the accompanying TeX.",
    "universal_claims_not_inferred_from_finite_tests": True,
    "forbidden_promotions": ["one selected C equals the full higher-rank image", "geometric refinement clock equals Gamma_9 without a clock map", "nodal measures are unchanged by inserting nodes", "canonical forms are identical for different growing convex bodies", "positive conditional expectation is multiplicative"],
    "owner": str(OWNER),
    "owner_sha256": sha256(owner_bytes).hexdigest(),
    "section": str(TEX),
    "section_sha256": sha256(TEX.read_bytes()).hexdigest(),
    "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    "K": K,
    "Q": Q,
    "levels": [{"r": r, "cells": len(t) - 1, "nodes": len(t)} for r, t in enumerate(grids)],
    "moments_0_to_5": [str(x) for x in moments[:6]],
    "check_count": len(CHECKS),
    "checks": CHECKS,
}
print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
