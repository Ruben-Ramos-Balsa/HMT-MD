#!/usr/bin/env python3
"""Finite exact witnesses for cocycle/curvature; no global-closure claim."""
from itertools import product

checks = 0


def check(a, b):
    global checks
    assert a == b, (a, b)
    checks += 1


def turns(word, previous=1):
    total = 0
    for direction in word:
        total += direction != previous
        previous = direction
    return total


for word in product((-1, 1), repeat=6):
    for cut in range(7):
        first, second = word[:cut], word[cut:]
        check(turns(word), turns(first) + turns(second, first[-1] if first else 1))
loop = (1, -1, -1, 1)
check(sum(loop), 0)
check(loop[-1], 1)
check(turns(loop), 2)
assert all(1 <= 5 + sum(loop[:j]) <= 9 for j in range(5))
checks += 1


def heis(x, y):
    a, b, t = x
    c, d, s = y
    return ((a+c) % 9, (b+d) % 9, (t+s+b*c) % 9)


def inv(x):
    a, b, t = x
    return (-a % 9, -b % 9, (-t+a*b) % 9)


for a, b, c, d in product(range(9), repeat=4):
    u, v = (a, b, 0), (c, d, 0)
    commutator = heis(heis(heis(u, v), inv(u)), inv(v))
    check(commutator, (0, 0, (b*c-a*d) % 9))
    for r in range(9):
        # X^a Z^b |r> = omega^(br) |r+a>.
        # AB=omega^k BA gives AB-BA=(omega^k-1)BA, not k times I.
        exponent_ab = d*r + b*(r+c)
        exponent_ba = b*r + d*(r+a)
        check((exponent_ab-exponent_ba) % 9, (b*c-a*d) % 9)
    for e, f in ((1, 0), (0, 1), (2, 3)):
        w = (e, f, 0)
        check(heis(heis(u, v), w), heis(u, heis(v, w)))
for a, b, c in product(range(9), repeat=3):
    check((a+b)//9 + ((a+b)%9+c)//9,
          (b+c)//9 + (a+(b+c)%9)//9)

# Exact memory witness on the bilateral basis: Gamma |n> = |n+1>.
for n in range(-100, 101):
    check((n+1)**2-n**2, 2*n+1)


def mat(rows):
    return tuple(tuple(row) for row in rows)


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def mul(a, b):
    return mat([[sum(a[i][k]*b[k][j] for k in range(len(b)))
                 for j in range(len(b[0]))] for i in range(len(a))])


def transpose(a):
    return mat(zip(*a))


def subtract(a, b):
    return mat([[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)])


def permutation(order):
    return mat([[int(order[j] == i) for j in range(len(order))]
                for i in range(len(order))])


# A coupled finite matrix stands for the sum of all declared terms;
# transport uses the entire matrix, not its diagonal or a chosen sector.
hx = mat([[5, 1, 2, 0], [1, 7, 3, 1], [2, 3, 11, 4], [0, 1, 4, 13]])
ue, uf = permutation((2, 0, 3, 1)), permutation((1, 3, 0, 2))
hy = mul(mul(ue, hx), transpose(ue))
hz = mul(mul(uf, hy), transpose(uf))
ufe = mul(uf, ue)
check(mul(hy, ue), mul(ue, hx))
check(mul(hz, ufe), mul(ufe, hx))
px, py, pz = eye(4), eye(4), eye(4)
for degree in range(10):
    # These are every Taylor coefficient through this degree in exp(-itH).
    check(mul(py, ue), mul(ue, px))
    check(mul(pz, ufe), mul(ufe, px))
    px, py, pz = mul(px, hx), mul(py, hy), mul(pz, hz)

# Keeping H frozen under a non-symmetry gives precisely a nonzero R_e.
assert subtract(mul(hx, ue), mul(ue, hx)) != mat([[0]*4 for _ in range(4)])
checks += 1
s1, s3 = mat([[0, 1], [1, 0]]), mat([[1, 0], [0, -1]])
check(subtract(mul(s1, s3), mul(s3, s1)), mat([[0, -2], [2, 0]]))
print(f"PASS_FOCAL_COCICLO_ACCION_CURVATURA exact_checks={checks}")
