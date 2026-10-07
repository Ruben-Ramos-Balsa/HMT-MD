#!/usr/bin/env python3
"""Independent finite CAR and weighted-fibre tests for the torsion coupling.

The Clifford matrices and normal-order prescription come from VIII/33.
Numerical geometry/measure values are diagnostic fixtures, not HMT outputs.
"""
import importlib.util
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location("finite_matrix_helpers", Path(__file__).with_name("verificar_acoplamiento_finito.py"))
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)
zero, eye, diag = lib.zero, lib.eye, lib.diag
adj, mul, add, scale = lib.adj, lib.mul, lib.add, lib.scale
kron, direct, norm, comm = lib.kron, lib.direct, lib.norm, lib.comm


def dg(m):
    n = len(m)
    a = zero(2**n)
    for state in range(2**n):
        for j in range(n):
            if not state & (1 << j):
                continue
            middle = state ^ (1 << j)
            sign1 = (-1)**bin(state & ((1 << j) - 1)).count("1")
            for i in range(n):
                if m[i][j] and not middle & (1 << i):
                    sign2 = (-1)**bin(middle & ((1 << i) - 1)).count("1")
                    a[middle | (1 << i)][state] += sign1 * sign2 * m[i][j]
    return a


def normal_quartic(ms):
    q = zero(2**len(ms[0]))
    for sign, m in zip((-1, -1, -1, 1), ms):
        b = dg(m)
        q = add(q, add(mul(b, b), dg(mul(m, m)), -1), sign)
    return q


def main():
    checks = []

    def yes(name, condition, residual=None):
        checks.append({"name": name, "passed": bool(condition), "residual": residual})
        if not condition:
            raise AssertionError(name)

    def eq(name, a, b):
        r = lib.residual(a, b)
        yes(name, r < 1e-12, r)

    def ne(name, a, b):
        r = lib.residual(a, b)
        yes(name, r > 1e-6, r)

    j, r, z = [[0, -1], [1, 0]], [[0, 1], [1, 0]], [[1, 0], [0, -1]]
    gs = [kron(j, eye(2)), kron(r, eye(2)), kron(z, r), kron(z, z)]
    adirac = scale(gs[0], -1j)
    triplets = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
    ms = [mul(mul(mul(adirac, gs[a]), gs[b]), gs[c]) for a, b, c in triplets]
    explicit = [scale(kron(j, r), 1j), scale(kron(j, z), 1j), scale(kron(eye(2), j), 1j), scale(kron(z, j), 1j)]
    gamma5 = scale(mul(mul(mul(gs[0], gs[1]), gs[2]), gs[3]), 1j)
    pl, pr = scale(add(eye(4), gamma5, -1), .5), scale(add(eye(4), gamma5), .5)
    charge = add(pl, scale(pr, 4))
    for k, (m, expected) in enumerate(zip(ms, explicit)):
        eq(f"current_{k}_from_Clifford", m, expected)
        eq(f"current_{k}_Hermitian", m, adj(m))
        eq(f"current_{k}_square_identity", mul(m, m), eye(4))
        eq(f"current_{k}_commutes_chirality", comm(m, gamma5), zero(4))

    q = normal_quartic(ms)
    eq("quartic_Hermitian", q, adj(q))
    number = dg(eye(4))
    eq("quartic_preserves_number", comm(q, number), zero(16))
    eq("quartic_chiral_gauge_invariant", comm(q, dg(charge)), zero(16))
    for n, value in ((0, 0), (1, 0), (3, 4), (4, 8)):
        indices = [k for k in range(16) if bin(k).count("1") == n]
        restricted = [[q[i][j] for j in indices] for i in indices]
        eq(f"occupation_{n}_restriction", restricted, scale(eye(len(indices)), value))
    indices = [3, 5, 6, 9, 10, 12]
    expected = [[0,0,0,0,0,-4],[0,2,0,0,6,0],[0,0,2,-6,0,0],[0,0,-6,2,0,0],[0,6,0,0,2,0],[-4,0,0,0,0,0]]
    eq("two_occupation_matrix", [[q[i][j] for j in indices] for i in indices], expected)
    raw = zero(16)
    for sign, m in zip((-1, -1, -1, 1), ms):
        raw = add(raw, mul(dg(m), dg(m)), sign)
    eq("normal_order_contraction_plus_2N", q, add(raw, scale(number, 2)))
    ne("negative_omit_normal_order", raw, q)

    # Two copies of the spinor share one total current. This checks the
    # cross terms and invariance under mixing the two copy coordinates.
    total_m = [kron(m, eye(2)) for m in ms]
    qa = normal_quartic([kron(m, diag([1, 0])) for m in ms])
    qb = normal_quartic([kron(m, diag([0, 1])) for m in ms])
    qt = normal_quartic(total_m)
    ne("negative_discard_cross_species_current", qt, add(qa, qb))
    eq("total_current_internal_mixing_invariant", comm(qt, dg(kron(eye(4), r))), zero(256))

    # Dynamical two-volume geometry: the clock exchanges configurations;
    # the coefficient of the quartic changes with inverse volume.
    ht = direct(scale(q, -3/20), scale(q, -3/40))
    clock = kron(r, eye(16))
    eq("geometry_torsion_Hermitian", ht, adj(ht))
    ne("torsion_exchanges_with_geometric_clock", comm(clock, ht), zero(32))
    eq("coupled_clock_torsion_Hermitian", add(clock, ht), adj(add(clock, ht)))

    # Correct Hilbert adjoint between Gibbs fibres: A^* W A=W0.
    a = diag([1, 1, math.sqrt(2), math.sqrt(2/3)])
    ai = diag([1, 1, 1/math.sqrt(2), 1/math.sqrt(2/3)])
    w = diag([.5, .5, .25, .75])
    w0 = scale(eye(4), .5)
    eq("density_transport_unitary_between_measures", mul(mul(adj(a), w), a), w0)
    hc = mul(mul(a, kron(r, eye(2))), ai)
    eq("transported_clock_weighted_selfadjoint", mul(adj(hc), w), mul(w, hc))
    ne("negative_use_Euclidean_adjoint_between_measures", hc, adj(hc))

    print(json.dumps({
        "status": "PASS_TORSION_TOTAL_CURRENT_FINITE_FOCK",
        "checks_passed": len(checks),
        "scope": "Finite normal-ordered total spin current, geometry-dependent coefficient and weighted Hilbert adjoints; not all PCH constraints.",
        "checks": checks,
    }, indent=2))


if __name__ == "__main__":
    main()
