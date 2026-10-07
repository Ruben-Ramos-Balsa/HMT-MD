#!/usr/bin/env python3
"""Exact rational checks for recovered nonadic memory and K reconstruction.

All operations are finite. They supplement the proofs in the source owners;
they do not identify the arithmetic Cayley, a finite permutation and the
K-directed diagonal flow as one operator. No optional modules or assert.
"""
from fractions import Fraction as F
import json

COUNT = 0


def check(label, actual, expected):
    global COUNT
    if actual != expected:
        raise ArithmeticError(f"{label}: {actual!r} != {expected!r}")
    COUNT += 1


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, c):
    return [[c*x for x in row] for row in a]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def apply(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def power(a, n):
    out = identity(len(a))
    for _ in range(n):
        out = mul(out, a)
    return out


def shift(n, j):
    return [[F(col == (row+j) % n) for col in range(n)]
            for row in range(n)]


def compression(c):
    return scale(add(scale(identity(len(c)), F(8)), c), F(1, 9))


def defect_gram(c, metric=None):
    metric = identity(len(c)) if metric is None else metric
    e = add(identity(len(c)), scale(c, F(-1)))
    return scale(mul(mul(transpose(e), metric), e), F(8, 81))


def nonadic_balance(c):
    n = len(c)
    eye = identity(n)
    t = compression(c)
    lhs = add(mul(transpose(t), t), defect_gram(c))
    rhs = scale(add(scale(eye, F(8)), mul(transpose(c), c)), F(1, 9))
    check('general nonadic balance', lhs, rhs)


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        leading = a[r][j]
        a[r] = [x/leading for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                coeff = a[i][j]
                a[i] = [x-coeff*y for x, y in zip(a[i], a[r])]
        r += 1
    return r


I = identity(12)
S3, S4 = shift(12, 3), shift(12, 4)
T3, T4 = compression(S3), compression(S4)
check('S3 order four', power(S3, 4), I)
check('S4 order three', power(S4, 3), I)
check('S3 not order three', power(S3, 3) == I, False)
check('S3 and S4 commute', mul(S3, S4), mul(S4, S3))
T3inv = scale(add(add(scale(I, F(512)), scale(S3, F(-64))),
                 add(scale(power(S3, 2), F(8)), scale(power(S3, 3), F(-1)))),
              F(1, 455))
check('exact inverse T3', mul(T3, T3inv), I)
nonadic_balance(S3)
nonadic_balance(S4)
pfix4 = scale(add(add(I, S4), power(S4, 2)), F(1, 3))
check('S4 fixed sector has dimension four', rank(pfix4), 4)
check('S4 compression contracts only complement by 19/27',
      mul(transpose(T4), T4),
      add(pfix4, scale(add(I, scale(pfix4, F(-1))), F(19, 27))))

# Inputs are the documented normalized memory records, not K itself.
# z0=m0/sqrt(8), z1=m1/sqrt(8).
Z0_NUM = [495, 116, 684, -108, -601, 90, 173, 88, -313, -560, 397, -461]
Z1_NUM = [2729, 2503, 3818, -5843, 2583, -920, -4051, 4338,
          -5312, -1583, 233, 1505]
z0, z1 = [F(x, 9) for x in Z0_NUM], [F(x, 81) for x in Z1_NUM]
b = [-9*x for x in z0]
c = [-9*x for x in apply(T3inv, z1)]
w = [c[i]-b[(i+1) % 12] for i in range(12)]
check('closed difference cycle', sum(w), 0)
B = [sum(w[:i]) for i in range(12)]
q = F(6263)
k = [(q+sum(B))/12-x for x in B]
EXPECTED_K = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
check('K reconstructed from two memories and charge', k, EXPECTED_K)
check('charge preserved', sum(k), q)
check('positive full register', min(k) > 0, True)
check('memory0 reconstructed', apply(scale(add(S3, scale(I, -1)), F(1, 9)), k), z0)
check('memory1 reconstructed', apply(mul(scale(add(S4, scale(I, -1)), F(1, 9)), T3), k), z1)
check('first difference recovered', w, [k[i]-k[(i+1) % 12] for i in range(12)])
check('centered reconstruction independent of q',
      [sum(B)/12-x for x in B], [x-q/12 for x in k])

memory0 = scale(add(S3, scale(I, F(-1))), F(1, 9))
memory1 = mul(scale(add(S4, scale(I, F(-1))), F(1, 9)), T3)
check('joint memory rank eleven', rank(memory0+memory1), 11)
check('uniform vector in kernel', apply(memory0+memory1, [F(1)]*12), [F(0)]*24)
gram = scale(add(mul(transpose(memory0), memory0),
                 mul(transpose(memory1), memory1)), F(8))
terminal = mul(T4, T3)
check('joint conservation', add(gram, mul(transpose(terminal), terminal)), I)
check('exact terminal trace', sum(mul(transpose(terminal), terminal)[i][i]
                                 for i in range(12)), F(16900, 2187))

# Exact counterexample: det(g)=1 does not make g Euclidean unitary.
g = [[F(2), F(0)], [F(0), F(1, 2)]]
ginv = [[F(1, 2), F(0)], [F(0), F(2)]]
nonadic_balance(g)
tg = compression(g)
check('visible expansion on first coordinate', tg[0][0], F(10, 9))
check('Euclidean conserved unit fails',
      add(mul(transpose(tg), tg), defect_gram(g)) == identity(2), False)

# Same compression transported as an operator between metric charts.
c0 = shift(2, 1)
cs = mul(mul(g, c0), ginv)
gs = mul(transpose(ginv), ginv)
ts = compression(cs)
check('transported metric unitarity', mul(mul(transpose(cs), gs), cs), gs)
check('transported compression naturality', mul(ts, g), mul(g, compression(c0)))
check('transported metric conservation',
      add(mul(mul(transpose(ts), gs), ts), defect_gram(cs, gs)), gs)
check('fixed chart commutation fails', mul(g, c0) == mul(c0, g), False)

# The two-component isometry gives a trace-preserving operator channel.
# Writing D=sqrt(8)(I-C)/9 eliminates the radical from D X D*.
x = [[F(2), F(1, 3)], [F(1, 3), F(1)]]
t0 = compression(c0)
e0 = add(identity(2), scale(c0, F(-1)))
channel = add(mul(mul(t0, x), transpose(t0)),
              scale(mul(mul(e0, x), transpose(e0)), F(8, 81)))
check('two-component channel', channel,
      scale(add(scale(x, F(8)), mul(mul(c0, x), transpose(c0))), F(1, 9)))
check('channel trace preserved', channel[0][0]+channel[1][1], x[0][0]+x[1][1])

print(json.dumps({'result': 'PASS_NONADIC_K_EXACT', 'checks': COUNT,
                  'arithmetic': 'Fraction', 'K': EXPECTED_K,
                  'scope': 'memory reconstruction, finite norm identities, transported-metric witness'},
                 ensure_ascii=False))
