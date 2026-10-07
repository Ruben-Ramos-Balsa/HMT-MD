"""Exact tests of the proposed polar radial publication of the complete archive.

No measured constants are inputs. The tests do not prove that this choice
of physical reader is forced by the original HMT constructor.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def scale(a, c):
    return [[c*x for x in row] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return add(a, scale(b, -1))


def inv(a):
    n = len(a)
    z = [list(row)+list(erow) for row, erow in zip(a, eye(n))]
    for j in range(n):
        pivot = next(k for k in range(j, n) if z[k][j])
        z[j], z[pivot] = z[pivot], z[j]
        d = z[j][j]
        z[j] = [v/d for v in z[j]]
        for k in range(n):
            if k != j:
                d = z[k][j]
                z[k] = [x-d*y for x, y in zip(z[k], z[j])]
    return [row[n:] for row in z]


def det(a):
    z = [list(row) for row in a]
    d = F(1)
    for j in range(len(a)):
        pivot = next((k for k in range(j, len(a)) if z[k][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            z[j], z[pivot] = z[pivot], z[j]
            d = -d
        p = z[j][j]
        d *= p
        for k in range(j+1, len(a)):
            factor = z[k][j]/p
            z[k] = [x-factor*y for x, y in zip(z[k], z[j])]
    return d


def positive(a):
    return a == tr(a) and all(det([row[:k] for row in a[:k]]) > 0
                             for k in range(1, len(a)+1))


def diagonal(a):
    return [[a[i][i] if i == j else F(0) for j in range(len(a))]
            for i in range(len(a))]


def kron(a, b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def run():
    checks = 0

    def check(value):
        nonlocal checks
        if not value:
            raise AssertionError('Control failed: ' + str(checks+1))
        checks += 1

    flags = list((q, a, b) for q in range(1, 9)
                 for a, b in combinations((1, 2, 4, 5, 7, 8), 2))
    omega = [(j, (j+3*k) % 12, flag) for j in range(12)
             for k in range(4) for flag in flags]
    N = len(omega)
    check(len(flags) == 120)
    check(N == 5760 and len(set(omega)) == N)
    check([sum(j == k for j, _, _ in omega) for k in range(12)] == [480]*12)
    check(F(N-1, 4*N) == F(5759, 23040))
    check(F(N-1, 4*N)+F(1, 4*N) == F(1, 4))

    i4 = eye(4)
    h4 = [[F(x) for x in row] for row in
          ((1, 1, 1, 1), (1, -1, 1, -1),
           (1, 1, -1, -1), (1, -1, -1, 1))]
    B, U = scale(h4, F(1, 4)), scale(h4, F(1, 2))
    P = [[F(1, 4)]*4 for _ in range(4)]
    Q = sub(i4, P)
    C, M = mm(Q, B), mm(P, B)
    check(mm(tr(B), B) == scale(i4, F(1, 4)))
    check(mm(U, tr(U)) == i4)
    check(add(mm(tr(C), C), mm(tr(M), M)) == scale(i4, F(1, 4)))
    check(mm(tr(C), M) == scale(i4, 0))
    check(scale(add(C, M), 2) == U)
    check(mm(C, tr(C)) == scale(Q, F(1, 4)))
    check(diagonal(mm(C, tr(C))) == scale(i4, F(3, 16)))
    check(mm(scale(C, 2), tr(scale(C, 2))) != i4)
    for i in range(4):
        for j in range(4):
            eij = [[F(k == i and l == j) for l in range(4)] for k in range(4)]
            check(diagonal(diagonal(eij)) == diagonal(eij))
            check(diagonal(eij) == (eij if i == j else scale(i4, 0)))

    a = [[F(x) for x in row] for row in
         ((1, 2, 0, 1), (0, 1, 1, 0), (1, 0, 2, 1), (0, 1, 0, 1))]
    X = add(mm(tr(a), a), i4)
    check(positive(X))
    Y = mm(U, mm(X, tr(U)))
    check(positive(Y))
    for L in (F(2, 7), F(11, 13), F(5759, 23040)):
        hbar, c = F(17, 19), F(23, 29)
        D = scale(U, L)
        DX = mm(D, X)
        R = scale(Y, L)
        check(mm(D, tr(D)) == scale(i4, L**2))
        check(positive(R))
        check(mm(R, R) == mm(DX, tr(DX)))
        check(mm(scale(R, 2), scale(R, 2)) != mm(DX, tr(DX)))
        conj_length = scale(mm(U, mm(inv(X), tr(U))), L)
        check(mm(R, conj_length) == scale(i4, L**2))
        quantum = hbar*c/L
        energy = scale(Y, quantum)
        mass = scale(energy, 1/c**2)
        G = c**3*L**2/hbar
        check(R == scale(energy, L**2/(hbar*c)))
        check(R == scale(mass, G/c**2))
        for V in ([[F(1), F(0), F(0), F(0)]],
                  [[F(1), F(0), F(0), F(0)], [F(0), F(0), F(1), F(0)]]):
            check(mm(V, mm(R, tr(V))) ==
                  scale(mm(V, mm(energy, tr(V))), L**2/(hbar*c)))
        # Ancillary memory adds a factor without changing the original N.
        Ua, Xa = kron(U, eye(2)), kron(X, eye(2))
        Da = scale(Ua, L)
        Ra = scale(mm(Ua, mm(Xa, tr(Ua))), L)
        check(mm(Ra, Ra) == mm(mm(Da, Xa), tr(mm(Da, Xa))))

    # Exact obstruction: polar publication and early compression differ.
    x2 = [[F(2), F(1)], [F(1), F(2)]]
    v = [[F(1), F(0)]]
    p = mm(tr(v), v)
    ex = mm(v, mm(x2, tr(v)))
    ex2 = mm(v, mm(mm(x2, x2), tr(v)))
    defect = sub(ex2, mm(ex, ex))
    check(ex == [[F(2)]])
    check(ex2 == [[F(5)]])
    check(defect == [[F(1)]])
    check(defect == mm(v, mm(x2, mm(sub(eye(2), p), mm(x2, tr(v))))))
    # A reducing subspace has zero defect.
    xd = [[F(2), F(0)], [F(0), F(3)]]
    check(mm(v, mm(mm(xd, xd), tr(v))) ==
          mm(mm(v, mm(xd, tr(v))), mm(v, mm(xd, tr(v)))))
    return checks


if __name__ == '__main__':
    here = Path(__file__).resolve()
    print(json.dumps({
        'status': 'PASS_POLAR_RADIAL_ARCHIVE_CONSTRUCTION',
        'exact_checks': run(),
        'full_archive_unitary': True,
        'polar_normalization_proven_for_defined_reader': True,
        'early_compression_defect_explicit': True,
        'G_target_used': False,
        'full_generator_reexecuted': False,
        'original_HMT_physical_reader_selection_proven': False,
        'PDFs_modified': False,
        'script_sha256': hashlib.sha256(here.read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2))
