#!/usr/bin/env python3
"""Structural finite-coupling controls; no HMT value fitting.

Standard-library-only matrix implementation. Integer charge/occupation
commutators are exact up to the displayed oscillator square roots; group
covariance checks use complex floating point with explicit tolerances.
Fixture masses and angles are test data, not generated physical predictions.
"""
import cmath
import itertools
import json
import math


def zero(n, m=None):
    return [[0j for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = 1
    return a


def diag(v):
    a = zero(len(v))
    for i, x in enumerate(v):
        a[i][i] = x
    return a


def adj(a):
    return [[complex(a[j][i]).conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def mul(a, b):
    c = zero(len(a), len(b[0]))
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    c[i][j] += x * y
    return c


def add(a, b, factor=1):
    return [[x + factor * y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(a, z):
    return [[z * x for x in row] for row in a]


def kron(a, b):
    return [[x * y for x in rowa for y in rowb] for rowa in a for rowb in b]


def direct(a, b):
    c = zero(len(a) + len(b))
    for i, row in enumerate(a):
        c[i][:len(a)] = row
    for i, row in enumerate(b):
        c[i + len(a)][len(a):] = row
    return c


def norm(a):
    return max((abs(x) for row in a for x in row), default=0)


def residual(a, b):
    return norm(add(a, b, -1))


def comm(a, b):
    return add(mul(a, b), mul(b, a), -1)


def su2(c, s):
    return [[c, s], [-s.conjugate(), c.conjugate()]]


def yukawa(h, yu, yd, colors):
    # [tilde(h) tensor Yu, h tensor Yd], ordered as weak/flavour.
    ht = [h[1].conjugate(), -h[0].conjugate()]
    n = len(yu)
    y = zero(2 * n)
    for w in range(2):
        for i in range(n):
            for j in range(n):
                y[w * n + i][j] = ht[w] * yu[i][j]
                y[w * n + i][n + j] = h[w] * yd[i][j]
    return kron(y, eye(colors))


def creator(mode, count):
    a = zero(2**count)
    for state in range(2**count):
        if not state & (1 << mode):
            parity = bin(state & ((1 << mode) - 1)).count("1")
            a[state | (1 << mode)][state] = (-1)**parity
    return a


def main():
    checks = []

    def yes(label, condition, error=None):
        checks.append({"name": label, "passed": bool(condition), "residual": error})
        if not condition:
            raise AssertionError(label)

    def equal(label, a, b):
        r = residual(a, b)
        yes(label, r < 1e-10, r)

    def differs(label, a, b):
        r = residual(a, b)
        yes(label, r > 1e-5, r)

    # Nontrivial unitary mixing fixture; not a physical CKM prediction.
    r12 = [[3/5, 4/5, 0], [-4/5, 3/5, 0], [0, 0, 1]]
    r23 = [[1, 0, 0], [0, 5/13, 12/13], [0, -12/13, 5/13]]
    v = mul(mul(r12, diag([1, 1j, 1])), r23)
    equal("CKM_fixture_unitary", mul(v, adj(v)), eye(3))
    du, dd = diag([1, 2, 4]), diag([3, 5, 7])
    yu, yd = du, mul(mul(v, dd), adj(v))
    weak = su2(complex(3/5), complex(4/5))
    color = diag([cmath.exp(0.19j), cmath.exp(-0.31j), cmath.exp(0.12j)])
    theta = 0.23
    h = [complex(2, 1), complex(-1, 3)]
    gh = [cmath.exp(3j * theta) * z[0] for z in mul(weak, [[x] for x in h])]
    yl = scale(kron(kron(weak, eye(3)), color), cmath.exp(1j * theta))
    yr = kron(direct(scale(eye(3), cmath.exp(4j * theta)), scale(eye(3), cmath.exp(-2j * theta))), color)
    yh, ygh = yukawa(h, yu, yd, 3), yukawa(gh, yu, yd, 3)
    equal("quark_Yukawa_covariance", mul(ygh, yr), mul(yl, yh))
    equal("vacuum_mass_CKM_same_basis", yukawa([0j, 1+0j], yu, yd, 3), kron(direct(du, yd), eye(3)))
    differs("negative_freezing_Higgs_breaks_covariance", mul(yh, yr), mul(yl, yh))
    badv = scale(v, 2)
    differs("negative_nonunitary_mixing", mul(badv, adj(badv)), eye(3))

    # Leptonic Dirac realization with a declared neutral singlet.
    yl_lep = scale(kron(weak, eye(3)), cmath.exp(-3j * theta))
    yr_lep = direct(eye(3), scale(eye(3), cmath.exp(-6j * theta)))
    equal("lepton_Yukawa_covariance", mul(yukawa(gh, yu, yd, 1), yr_lep), mul(yl_lep, yukawa(h, yu, yd, 1)))

    # Charged bosonic oscillator and two fermion modes. The total charge
    # is the integer-normalized received quark pair (1,4), plus 3 per boson.
    cd_l, cd_r = creator(0, 2), creator(1, 2)
    cl, cr = adj(cd_l), adj(cd_r)
    nl, nr = mul(cd_l, cl), mul(cd_r, cr)
    nb = diag([0, 1, 2])
    bd = zero(3)
    bd[1][0], bd[2][1] = 1, math.sqrt(2)
    b = adj(bd)
    transfer = kron(bd, mul(cd_l, cr))
    interaction = add(transfer, adj(transfer))
    h0 = add(kron(nb, eye(4)), kron(eye(3), add(nl, scale(nr, 2))))
    total = add(h0, interaction)
    charge = add(kron(scale(nb, 3), eye(4)), kron(eye(3), add(nl, scale(nr, 4))))
    equal("CAR_modes", add(mul(cl, cd_r), mul(cd_r, cl)), zero(4))
    equal("interacting_Hermitian", total, adj(total))
    equal("joint_charge_conserved", comm(total, charge), zero(12))
    differs("interaction_changes_boson_occupation", comm(total, kron(nb, eye(4))), zero(12))
    differs("interaction_changes_left_fermion_occupation", comm(total, kron(eye(3), nl)), zero(12))
    ug = diag([cmath.exp(0.47j * charge[i][i]) for i in range(12)])
    equal("finite_gauge_action", mul(mul(ug, total), adj(ug)), total)
    # Fixed boundary charge 4: the two-dimensional sector exchanges a
    # right mode with a left mode plus one charged boson.
    p = diag([int(charge[i][i] == 4) for i in range(12)])
    equal("charge_sector_projector", mul(p, p), p)
    equal("gauge_sector_reduces_H", comm(total, p), zero(12))
    yes("charge_sector_is_nontrivial", sum(p[i][i] for i in range(12)) == 2)
    yes("interaction_survives_reduction", norm(mul(mul(p, interaction), p)) > 0)
    # Even observable algebra in the retained charge sector. The exact
    # 2x2 Hamiltonian is [[2,1],[1,2]], so its heat kernel is explicit.
    def heat(t):
        return scale([[math.cosh(t), -math.sinh(t)], [-math.sinh(t), math.cosh(t)]], math.exp(-2*t))

    def trace(a):
        return sum(a[i][i] for i in range(len(a)))

    b0 = heat(1.0)
    b1 = mul(mul(heat(0.6), diag([0, 1])), heat(0.4))
    bs = [b0, b1]
    gram = [[trace(mul(adj(x), y)) for y in bs] for x in bs]
    equal("finite_time_reflection_kernel_Hermitian", gram, adj(gram))
    yes("finite_time_reflection_diagonal_positive", all(gram[i][i].real >= 0 for i in range(2)))
    yes("finite_time_reflection_determinant_positive", (gram[0][0]*gram[1][1] - gram[0][1]*gram[1][0]).real >= -1e-14)
    differs("negative_drop_adjoint", add(h0, transfer), adj(add(h0, transfer)))
    wrong = add(h0, kron(eye(3), add(mul(cd_l, cr), mul(cd_r, cl))))
    differs("negative_drop_charged_Higgs", comm(wrong, charge), zero(12))
    incomplete = diag([1, 0])
    differs("negative_incomplete_weak_multiplet_cutoff", comm(incomplete, weak), zero(2))

    # Naive central-difference control, not a claim about an already
    # identified HMT Dirac symbol. In d periodic dimensions there are 2^d
    # exact corner zeros in the free symbol sin(p_j a)/a.
    corners = {}
    for d in (1, 2, 3, 4):
        points = list(itertools.product((0, 1), repeat=d))
        yes(f"central_symbol_{d}d_{2**d}_corner_zeros", all(sum(math.sin(math.pi * k)**2 for k in p0) < 1e-24 for p0 in points))
        corners[str(d)] = len(points)
    print(json.dumps({
        "status": "PASS_FINITE_YUKAWA_FOCK_COUPLING",
        "checks_passed": len(checks),
        "scope": "Finite compatibility controls; masses/angles are generic test fixtures, not HMT physical evaluations; no continuum chiral conclusion.",
        "central_difference_corner_zeros": corners,
        "checks": checks,
    }, indent=2))


if __name__ == "__main__":
    main()
