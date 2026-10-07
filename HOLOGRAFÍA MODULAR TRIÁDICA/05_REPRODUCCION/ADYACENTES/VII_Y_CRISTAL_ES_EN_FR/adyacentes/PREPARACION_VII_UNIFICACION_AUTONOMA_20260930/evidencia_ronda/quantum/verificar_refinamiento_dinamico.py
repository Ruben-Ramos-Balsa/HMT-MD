#!/usr/bin/env python3
"""Exact nonadic energy/norm checks plus floating resolvent regressions.

Tests are synthetic, not input constants or a proof of four-force unification.
The infinite-level proof is in REFINAMIENTO_DINAMICO_NONADICO.md.
"""
from fractions import Fraction as F
import json
import math


def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    out = zero(len(a), len(b[0]))
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] += x*y
    return out


def forms(n):
    l, m = zero(n+1), zero(n+1)
    for j in range(n):
        for a, b, v in ((0, 0, n), (1, 1, n), (0, 1, -n), (1, 0, -n)):
            l[j+a][j+b] += v
        for a, b, v in ((0, 0, F(1, 3*n)), (1, 1, F(1, 3*n)),
                        (0, 1, F(1, 6*n)), (1, 0, F(1, 6*n))):
            m[j+a][j+b] += v
    return l, m


def inclusion(n, factor=9):
    j = zero(factor*n+1, n+1)
    for r in range(factor*n):
        cell, rem = divmod(r, factor)
        j[r][cell] = 1-F(rem, factor)
        j[r][cell+1] = F(rem, factor)
    j[-1][-1] = 1
    return j


def harmonic(n):
    return [[1-F(j, n), F(j, n)] for j in range(n+1)]


def tridiagonal(diag, off, rhs):
    d, b = list(diag), list(rhs)
    for j in range(1, len(d)):
        r = off[j-1]/d[j-1]
        d[j] -= r*off[j-1]
        b[j] -= r*b[j-1]
    x = [0.0]*len(d)
    x[-1] = b[-1]/d[-1]
    for j in range(len(d)-2, -1, -1):
        x[j] = (b[j]-off[j]*x[j+1])/d[j]
    return x


def schur(n, kappa):
    k2 = kappa*kappa
    endpoint = n+k2/(3*n)
    off = -n+k2/(6*n)
    diag = [2*n+2*k2/(3*n)]*(n-1)
    rhs = [0.0]*(n-1)
    rhs[0] = -off
    solution = tridiagonal(diag, [off]*(n-2), rhs)
    return endpoint+off*solution[0], off*solution[-1]


def kernel(n, kappa):
    eta = 2*math.asinh(kappa/(2*n*math.sqrt(1-kappa*kappa/(6*n*n))))
    prefactor = kappa*math.sqrt(1+kappa*kappa/(12*n*n))
    return prefactor/math.tanh(n*eta), -prefactor/math.sinh(n*eta)


def main():
    checks = []
    def check(name, value):
        if not value:
            raise AssertionError(name)
        checks.append(name)

    z = [[F(1, 3), F(1, 6)], [F(1, 6), F(1, 3)]]
    k0 = [[F(1), F(-1)], [F(-1), F(1)]]
    for n in (1, 3, 9):
        l, m = forms(n)
        lf, mf = forms(9*n)
        j = inclusion(n)
        check(f'energy_inclusion_{n}', mul(transpose(j), mul(lf, j)) == l)
        check(f'norm_inclusion_{n}', mul(transpose(j), mul(mf, j)) == m)
        a = harmonic(n)
        check(f'boundary_energy_{n}', mul(transpose(a), mul(l, a)) == k0)
        check(f'boundary_norm_{n}', mul(transpose(a), mul(m, a)) == z)
        # Nontrivial unitary sign gauge: all identities conjugate together.
        signs = [(-1)**j for j in range(n+1)]
        mg = [[signs[i]*m[i][j]*signs[j] for j in range(n+1)] for i in range(n+1)]
        ag = [[signs[i]*x for x in a[i]] for i in range(n+1)]
        check(f'unitary_frame_norm_{n}', mul(transpose(ag), mul(mg, ag)) == z)

    for n in (3, 9, 27):
        a = harmonic(n)
        raw = mul(transpose(a), a)
        check(f'raw_norm_diag_{n}', raw[0][0] == F((n+1)*(2*n+1), 6*n))
        check(f'raw_norm_off_{n}', raw[0][1] == F(n*n-1, 6*n))
        trap = [[F(0), F(0)], [F(0), F(0)]]
        for j, row in enumerate(a):
            weight = F(1, 2*n) if j in (0, n) else F(1, n)
            for p in range(2):
                for q in range(2):
                    trap[p][q] += weight*row[p]*row[q]
        check(f'trapezoid_diag_{n}', trap[0][0] == F(1, 3)+F(1, 6*n*n))
        check(f'trapezoid_off_{n}', trap[0][1] == F(1, 6)-F(1, 6*n*n))
        check(f'negative_raw_is_not_temporal_norm_{n}', raw != z)
        for kappa in (.3, 1., 2.):
            got, expected = schur(n, kappa), kernel(n, kappa)
            check(f'resolvent_formula_{n}_{kappa}', max(abs(x-y) for x,y in zip(got, expected)) < 2e-11)

    errors = {}
    for kappa in (.3, 1., 2.):
        limit = (kappa/math.tanh(kappa), -kappa/math.sinh(kappa))
        seq = []
        for n in (9, 81, 729, 6561):
            seq.append(max(abs(x-y) for x,y in zip(kernel(n, kappa), limit)))
        check(f'resolvent_converges_{kappa}', all(b<a for a,b in zip(seq,seq[1:])) and seq[-1] < 1e-7)
        errors[str(kappa)] = seq
    print(json.dumps({'result': 'PASS_REFINAMIENTO_DINAMICO_NONADICO',
                      'checks': len(checks), 'exact_checks': 30,
                      'floating_checks': 12,
                      'four_interaction_complete_closure': False,
                      'domain': 'declared unitary route realization; exact norm and Galerkin limit in accompanying proof',
                      'convergence_errors': errors}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
