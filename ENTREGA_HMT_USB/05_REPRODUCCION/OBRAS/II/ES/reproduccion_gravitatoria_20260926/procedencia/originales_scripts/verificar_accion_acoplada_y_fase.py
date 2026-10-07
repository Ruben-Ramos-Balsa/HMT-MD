#!/usr/bin/env python3
"""Exact tests of the coupled TPK energy reduction, not a physical G fit.

The rational matrices below are test realizations of VII30b's typed theorem.
They are not claimed to be a new selector of a native gravitational state.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


checks = []


def check(name, actual, expected):
    if actual != expected:
        raise AssertionError((name, actual, expected))
    checks.append(name)


def zero(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return list(map(list, zip(*a)))


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(s, a):
    return [[s*x for x in r] for r in a]


def mul(a, b):
    return [[sum(x*y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def inverse(a):
    n = len(a)
    b = [list(r)+eye(n)[i] for i, r in enumerate(a)]
    for i in range(n):
        k = next(k for k in range(i, n) if b[k][i])
        b[k], b[i] = b[i], b[k]
        q = b[i][i]
        b[i] = [v/q for v in b[i]]
        for k in range(n):
            if k != i:
                q = b[k][i]
                b[k] = [v-q*w for v, w in zip(b[k], b[i])]
    return [r[n:] for r in b]


def block(a, row, col, n=2, m=2):
    return [r[col:col+m] for r in a[row:row+n]]


def put(a, b, row, col):
    for i, r in enumerate(b):
        for j, v in enumerate(r):
            a[row+i][col+j] = v


def hcat(xs):
    return [sum((list(a[i]) for a in xs), []) for i in range(len(xs[0]))]


def vcat(xs):
    return sum(([list(r) for r in a] for a in xs), [])


def dot(a, b):
    return mul(transpose(a), b)[0][0]


def congruence(a, w):
    return mul(mul(a, w), transpose(a))


def tails(us):
    tail = eye(len(us[0]))
    bs = [None]*len(us)
    for j in reversed(range(len(us))):
        bs[j] = tail
        tail = mul(tail, us[j])
    return tail, bs


def solve(us, w, a, b):
    u, bs = tails(us)
    B = hcat(bs)
    C = inverse(w)
    R = congruence(B, C)
    z = add(b, scale(-1, mul(u, a)))
    y = mul(inverse(R), z)
    r = mul(mul(C, transpose(B)), y)
    fs = [a]
    d = len(a)
    for j, v in enumerate(us):
        fs.append(add(mul(v, fs[-1]), block(r, j*d, 0, d, 1)))
    return dict(u=u, bs=bs, B=B, C=C, R=R, z=z, y=y, r=r,
                q=mul(w, r), fs=fs, energy=dot(r, mul(w, r)))


def run():
    d, n = 2, 3
    I = eye(d)
    us = [[[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]],
          [[F(1), F(0)], [F(0), F(-1)]],
          [[F(5, 13), F(-12, 13)], [F(12, 13), F(5, 13)]]]
    for j, u in enumerate(us):
        check(f'unitary_{j}', congruence(u, I), I)
    check('noncommuting_transport', mul(us[0], us[1]) != mul(us[1], us[0]), True)

    lower = eye(d*n)
    for i in range(1, d*n):
        lower[i][i-1] = F(i, 3)
    lower[4][0] = F(2, 7)
    w = add(mul(transpose(lower), lower), eye(d*n))
    a, b = [[F(1)], [F(-2)]], [[F(3)], [F(1)]]
    s = solve(us, w, a, b)
    check('coupled_positive_factorization',
          add(w, scale(-1, mul(transpose(lower), lower))), eye(d*n))
    check('nonzero_cross_incidence', block(w, 0, 2) != zero(2, 2), True)
    check('constraint', mul(s['B'], s['r']), s['z'])
    check('endpoint_reconstruction', s['fs'][-1], b)
    check('multiplier', s['q'], mul(transpose(s['B']), s['y']))
    check('effective_energy', s['energy'], dot(s['z'], s['y']))

    seed = [[F(i+1)] for i in range(d*n)]
    k = add(seed, scale(-1, mul(mul(mul(s['C'], transpose(s['B'])),
                                   inverse(s['R'])), mul(s['B'], seed))))
    check('kernel_perturbation', mul(s['B'], k), zero(d, 1))
    check('minimum_orthogonality', dot(k, s['q']), F(0))
    rk = add(s['r'], k)
    check('minimum_Pythagoras', dot(rk, mul(w, rk)),
          s['energy']+dot(k, mul(w, k)))
    check('strict_minimum_test', dot(k, mul(w, k)) > 0, True)

    # Coarsen first two incidences into a block, without dropping correlations.
    mid = zero(4, 6)
    put(mid, us[1], 0, 0)
    put(mid, I, 0, 2)
    put(mid, I, 2, 4)
    Rmid = congruence(mid, s['C'])
    last = hcat([us[2], I])
    check('coupled_reduction_by_stages', congruence(last, Rmid), s['R'])
    diagonal_only = add(congruence(us[2], block(Rmid, 0, 0)), block(Rmid, 2, 2))
    cross = add(mul(us[2], block(Rmid, 0, 2)),
                mul(block(Rmid, 2, 0), transpose(us[2])))
    check('cross_terms_explicit', add(diagonal_only, cross), s['R'])
    check('cross_terms_matter', diagonal_only != s['R'], True)
    coarse = solve([mul(us[1], us[0]), us[2]], inverse(Rmid), a, b)
    check('coupled_coarse_action', coarse['energy'], s['energy'])

    # Global reversal includes every off-diagonal block by congruence.
    J = zero(d*n, d*n)
    for j, u in enumerate(us):
        put(J, scale(-1, inverse(u)), (n-1-j)*d, j*d)
    Ji = inverse(J)
    wrev = congruence(transpose(Ji), w)
    rev = solve([inverse(u) for u in reversed(us)], wrev, b, a)
    check('reversal_residual', rev['r'], mul(J, s['r']))
    check('reversal_action', rev['energy'], s['energy'])
    check('reversal_compliance', rev['R'], congruence(inverse(s['u']), s['R']))

    # All real connection coordinates, not just a radial or scalar variation.
    for j in range(n):
        for row in range(d):
            for col in range(d):
                A = zero(d, d)
                A[row][col] = F(1)
                K = mul(mul(s['bs'][j], A), inverse(s['bs'][j]))
                du = mul(K, s['u'])
                dB = hcat([mul(K, t) if i < j else zero(d, d)
                           for i, t in enumerate(s['bs'])])
                dR0 = mul(mul(dB, s['C']), transpose(s['B']))
                dR = add(dR0, transpose(dR0))
                dz = scale(-1, mul(du, a))
                effective = 2*dot(s['y'], dz)-dot(s['y'], mul(dR, s['y']))
                qj = block(s['q'], j*d, 0, d, 1)
                direct = -2*dot(qj, mul(A, mul(us[j], s['fs'][j])))
                check(f'connection_{j}_{row}_{col}', effective, direct)

    for i in range(d*n):
        for j in range(i, d*n):
            dw = zero(d*n, d*n)
            dw[i][j] = dw[j][i] = F(1)
            dC = scale(-1, mul(mul(s['C'], dw), s['C']))
            dR = congruence(s['B'], dC)
            check(f'weight_{i}_{j}', -dot(s['y'], mul(dR, s['y'])),
                  dot(s['r'], mul(dw, s['r'])))

    # Clock-fixed quadratic generator recovers all coupled weights exactly.
    D = eye(d*n)
    for j in range(1, n):
        put(D, scale(-1, us[j]), j*d, (j-1)*d)
    A = mul(mul(transpose(D), w), D)
    Di = inverse(D)
    check('generator_to_weight', mul(mul(transpose(Di), A), Di), w)
    # Realification of -i H/hbar yields an exact first-jet phase test.
    hbar = F(7, 5)  # Test unit, not a generated or measured constant.
    phase_first_jet = zero(2*d*n, 2*d*n)
    put(phase_first_jet, scale(1/hbar, A), 0, d*n)
    put(phase_first_jet, scale(-1/hbar, A), d*n, 0)
    recovered = scale(hbar, block(phase_first_jet, 0, d*n, d*n, d*n))
    check('phase_first_jet_to_generator', recovered, A)
    check('doubling_cost_changes_full_phase_first_jet', scale(2, recovered) != A, True)

    # Schur elimination of vertex variables agrees with endpoint compliance.
    Hbb = block(A, 4, 4)
    Hii = block(A, 0, 0, 4, 4)
    Hbi = block(A, 4, 0, 2, 4)
    schur = add(Hbb, scale(-1, mul(mul(Hbi, inverse(Hii)), transpose(Hbi))))
    check('generator_schur_equals_compliance_inverse', schur, inverse(s['R']))

    # Dynamic elimination carries the temporal coefficient too.
    omega = F(1, 7)
    lam = hbar*omega
    resolvent = inverse(add(A, scale(-lam, eye(6))))
    Kii = add(Hii, scale(-lam, eye(4)))
    Keff = add(add(Hbb, scale(-lam, eye(2))),
               scale(-1, mul(mul(Hbi, inverse(Kii)), transpose(Hbi))))
    check('dynamic_compressed_resolvent', block(resolvent, 4, 4), inverse(Keff))
    Z = add(eye(2), mul(mul(Hbi, mul(inverse(Hii), inverse(Hii))), transpose(Hbi)))
    check('dynamic_memory_correction_nonzero', Z != eye(2), True)
    # Positivity: Z-I = (Hii^-1 Hib)* (Hii^-1 Hib).
    lift = mul(inverse(Hii), transpose(Hbi))
    check('dynamic_memory_positive_gram', add(Z, scale(-1, eye(2))),
          mul(transpose(lift), lift))

    # A canonical coordinate change transports the reciprocal by the dual
    # congruence. The identity holds for every invertible T, including Z^1/2.
    T = [[F(2), F(1)], [F(1), F(1)]]
    Ti = inverse(T)
    L, Q = F(3), F(5)
    Rb, Hb, Lambda = scale(L, schur), scale(Q, schur), scale(L, inverse(schur))
    Rc = congruence(transpose(Ti), Rb)
    Hc = congruence(transpose(Ti), Hb)
    Lc = congruence(T, Lambda)
    check('canonical_radial_energy_proportionality', Rc, scale(L/Q, Hc))
    check('canonical_dual_reciprocity', mul(Rc, Lc), scale(L*L, eye(2)))
    check('noncommuting_canonical_test', mul(T, schur) != mul(schur, T), True)
    wrong = congruence(transpose(Ti), Lambda)
    check('same_congruence_is_not_dual', mul(Rc, wrong) != scale(L*L, eye(2)), True)

    return {
        'status': 'PASS_ACCION_ACOPLADA_VARIACION_Y_FASE_CONDICIONADA',
        'checks_count': len(checks), 'checks': checks,
        'matrix_domain': 'Finite paths; full positive coupled W; invertible transports',
        'normalization_theorem': 'A fixed lifted full generator fixes its quadratic form and Schur response',
        'native_gravitational_W_selected': False,
        'native_phase_quadratic_identification_evaluated': False,
        'G_calibrated': False, 'PDF_or_Lean_changed': False,
        'test_realization': {'incidences': n, 'fiber_dimension': d,
                             'W_positive_by': 'L^T L + I',
                             'physical_selector': False},
        'boundary_compliance': [[str(x) for x in r] for r in s['R']],
        'memory_temporal_coefficient': [[str(x) for x in r] for r in Z],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'status': result['status'], 'checks_count': result['checks_count']},
                     ensure_ascii=False))
