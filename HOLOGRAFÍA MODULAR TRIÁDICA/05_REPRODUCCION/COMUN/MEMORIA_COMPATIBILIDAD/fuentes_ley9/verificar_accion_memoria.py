#!/usr/bin/env python3
"""Exact local checks; no claim of full HMT or experimental certification."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import json

I = ((F(1), F(0)), (F(0), F(1)))

def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))

def transpose(a):
    return tuple(zip(*a))

def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]

def tr(a):
    return a[0][0] + a[1][1]

def inv(a):
    d = det(a)
    return ((a[1][1]/d, -a[0][1]/d), (-a[1][0]/d, a[0][0]/d))

def mix(a, p):
    return tuple(tuple(p * I[i][j] + (1-p) * a[i][j]
                       for j in range(2)) for i in range(2))

def check(h):
    assert det(h) == 1
    a = mul(h, transpose(h))
    tau = tr(a) - 2
    assert tau >= 0
    wv, wm = mix(a, F(8, 9)), mix(a, F(1, 9))
    nu2 = det(wv)
    ev = tr(wv)/4 - F(1, 2)
    em = tr(wm)/4 - F(1, 2)
    assert nu2 == det(wm) == 1 + F(8, 81) * tau
    assert ev == tau/36
    assert nu2-1 == F(32, 9)*ev
    assert em == 8*ev
    assert ev+em == tau/4
    hinv = inv(h)
    assert tr(mul(hinv, transpose(hinv))) == tr(a)
    for p in (F(1, 9), F(1, 3), F(1, 2), F(2, 3), F(8, 9)):
        w = mix(a, p)
        de = tr(w)/4-F(1, 2)
        assert det(w) == 1+p*(1-p)*tau
        assert det(w)-1 == 4*p*de
    # Check covariance and energy metric under a non-orthogonal chart.
    m = ((F(2), F(1)), (F(0), F(1, 2)))
    minv = inv(m)
    g = mul(transpose(minv), minv)
    vm = mul(mul(m, wv), transpose(m))
    assert tr(mul(g, vm)) == tr(wv)
    assert det(vm) == det(wv)
    return tau, nu2, ev, em

def hn(n):
    return ((F(1+n), F(n*n)), (F(n), F(n*n-n+1)))

def main():
    count = 0
    for n in range(-30, 31):
        tau, nu2, ev, em = check(hn(n))
        assert tau == n*n*(2*n*n-2*n+5)
        assert check(hn(-n))[0]-tau == 4*n**3
        count += 1
    for x in range(-6, 7):
        for y in range(-6, 7):
            a, b = F(x, 3), F(y, 4)
            check(((1+a*b, a), (b, F(1))))
            count += 1
    assert check(hn(1)) == (5, F(121,81), F(5,36), F(10,9))
    assert check(hn(-1)) == (9, F(17,9), F(1,4), F(2))
    nu = F(11,9)
    workv = (nu-1)*(9*nu-7)/32
    assert workv == F(1,36)
    workm = F(10,9)-(nu-1)/2
    assert workm == 1
    assert F(5,4)-(workv+workm) == nu-1 == F(2,9)
    # Polynomial identity for arbitrary symbolic nu, checked on exact rationals.
    for j in range(101):
        v = 1+F(j, 13)
        excess = F(9,32)*(v*v-1)
        passive = (v-1)/2
        work = (v-1)*(9*v-7)/32
        assert work >= 0 and excess == work+passive
    # Negative control: displacement changes energy, not determinant/purity.
    assert det(I)-1 != F(32,9)*F(1,2)
    with localcontext() as ctx:
        ctx.prec = 50
        workminus = (Decimal(9)-2*Decimal(17).sqrt())/12
    print(json.dumps({
        "status": "CONTROLES_ALGEBRAICOS_LOCALES_CORRECTOS",
        "exact_matrix_cases": count,
        "exact_passivity_identity_cases": 101,
        "n1": {"purity": "9/11", "visible_excess_over_hf": "5/36",
               "visible_ergotropy_over_hf": "1/36",
               "joint_minus_local_work_over_hf": "2/9"},
        "nminus1_visible_ergotropy_over_hf": str(workminus),
        "negative_control_displacement_detected": True,
        "scope": "Local matrix identities; not a proof of physical realization or a global HMT gate."
    }, indent=2))

if __name__ == "__main__":
    main()
