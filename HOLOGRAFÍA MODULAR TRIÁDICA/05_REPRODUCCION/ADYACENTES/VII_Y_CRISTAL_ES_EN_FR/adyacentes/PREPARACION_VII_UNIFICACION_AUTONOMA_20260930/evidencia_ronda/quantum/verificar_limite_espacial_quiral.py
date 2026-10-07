#!/usr/bin/env python3
"""Controles focales; sólo stdlib, sin reescribir fuentes o certificados.

Los fixtures matriciales prueban la implementación de identidades generales.
No generan constantes físicas ni sustituyen la genealogía de los propietarios.
Las pruebas de límite infinito se encuentran en la nota compañera.
"""

import json
import math


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def adj(a):
    return [[a[i][j].conjugate() for i in range(len(a))]
            for j in range(len(a[0]))]


def add(a, b, sign=1):
    return [[a[i][j] + sign * b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def scale(a, c):
    return [[c * x for x in row] for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def diag(v):
    return [[v[i] if i == j else 0 for j in range(len(v))]
            for i in range(len(v))]


def direct(a, b):
    return ([r + [0] * len(b) for r in a]
            + [[0] * len(a) + r for r in b])


def kron(a, b):
    return [[a[i][j] * b[k][ell]
             for j in range(len(a[0])) for ell in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def comm(a, b):
    return add(mul(a, b), mul(b, a), -1)


def zero(a):
    return all(x == 0 for row in a for x in row)


def creator(n, k):
    d = 2 ** n
    result = [[0] * d for _ in range(d)]
    for mask in range(d):
        if not mask & (1 << k):
            sign = (-1) ** bin(mask & ((1 << k) - 1)).count("1")
            result[mask | (1 << k)][mask] = sign
    return result


checks = []


def check(name, condition, kind="exact"):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "kind": kind, "pass": True})


# Isometric graded inclusion; both coarse chirality labels survive.
j = [[1, 0], [0, 0], [0, 1], [0, 0]]
js = adj(j)
chi = diag([1, 1, -1, -1])
chi0 = diag([1, -1])
check("isometry", mul(js, j) == eye(2))
check("chirality_intertwines", mul(chi, j) == mul(j, chi0))
check("chirality_is_involution", mul(chi, chi) == eye(4))

# Clifford realization received from VIII/33; exact nontrivial spin transport.
j2 = [[0, 1], [-1, 0]]
r2 = [[0, 1], [1, 0]]
z2 = diag([1, -1])
gammas = [kron(j2, eye(2)), kron(r2, eye(2)),
          kron(z2, r2), kron(z2, z2)]
g5 = scale(mul(mul(mul(gammas[0], gammas[1]), gammas[2]), gammas[3]), 1j)
check("source_gamma5_hermitian", adj(g5) == g5)
check("source_gamma5_involution", mul(g5, g5) == eye(4))
for k, g in enumerate(gammas):
    check("source_gamma5_anticommutes_%d" % k, zero(add(mul(g5, g), mul(g, g5))))
t = mul(gammas[1], gammas[2])
check("spin_transport_unitary", mul(adj(t), t) == eye(4))
check("spin_transport_even", zero(comm(t, g5)))
dt = [scale(t, -1)[i] + eye(4)[i] for i in range(4)]
chiv = direct(g5, g5)
check("edge_chirality_square", mul(dt, chiv) == mul(g5, dt))
w = add(scale(eye(4), 2), g5)
response = mul(mul(adj(dt), w), dt)
check("response_DstarWD_is_even", zero(comm(response, chiv)))

# Strong intertwining preserves products AND their residuals.
a = diag([2, 7, 3, 11])
b = [[0, 0, 1, 0], [0, 0, 0, 2],
     [1, 0, 0, 0], [0, 2, 0, 0]]
a0 = mul(mul(js, a), j)
b0 = mul(mul(js, b), j)
check("A_strong_intertwiner", mul(a, j) == mul(j, a0))
check("B_strong_intertwiner", mul(b, j) == mul(j, b0))
check("even_A", zero(comm(chi, a)))
check("odd_B", zero(add(mul(chi, b), mul(b, chi))))
check("ordered_product", mul(mul(a, b), j) == mul(j, mul(a0, b0)))
check("commutator_transport", mul(comm(a, b), j) == mul(j, comm(a0, b0)))
check("nonzero_residual_is_not_erased", not zero(comm(a0, b0)))

# Reuse the proved compression identity from MEMORIA_DOMINIO_Y_ALGEBRA.md.
# This new fixture adds the preserved chirality, not a new general theorem.
x = [[0, 1], [1, 0]]
y = [[0, -1j], [1j, 0]]
af = direct(x, x)
bf = direct(y, y)
aa = mul(mul(js, af), j)
bb = mul(mul(js, bf), j)
q = add(eye(4), mul(j, js), -1)
xa = mul(mul(q, af), j)
xb = mul(mul(q, bf), j)
lhs = add(mul(mul(js, comm(af, bf)), j), comm(aa, bb), -1)
rhs = add(mul(adj(xa), xb), mul(adj(xb), xa), -1)
check("compression_defect_identity", lhs == rhs)
check("compressed_operators_zero", zero(aa) and zero(bb))
check("compressed_commutator_nonzero", lhs == scale(eye(2), 2j))
check("defect_even_despite_chirality", zero(comm(chi, af)) and zero(comm(chi, bf)))
check("discarding_detail_is_detected", lhs != comm(aa, bb))

# Exterior Fock inclusion for two received modes into three; no new state law.
jf = [[int(i == k) for k in range(4)] for i in range(8)]
check("Fock_isometry", mul(adj(jf), jf) == eye(4))
for k in range(2):
    c2, c3 = creator(2, k), creator(3, k)
    check("creator_naturality_%d" % k, mul(c3, jf) == mul(jf, c2))
    check("annihilator_naturality_%d" % k, mul(adj(c3), jf) == mul(jf, adj(c2)))
for k in range(3):
    for ell in range(3):
        ck, cl = creator(3, k), creator(3, ell)
        anti = add(mul(adj(ck), cl), mul(cl, adj(ck)))
        check("CAR_%d_%d" % (k, ell), anti == scale(eye(8), int(k == ell)))

# Numerical samples of the analytic bound in the note, NOT its proof.
for m in range(1, 6):
    n = 9 ** m
    error = math.pi - n * math.sin(math.pi / n)
    upper = math.pi ** 3 / (6 * n * n)
    check("odd_grid_bound_%d" % m,
          -1e-14 <= error <= upper + 1e-14, "numerical_bound_sample")

print(json.dumps({
    "status": "PASS_LIMITE_ESPACIAL_QUIRAL_CONTROLES_FOCALES",
    "checks": len(checks),
    "exact": sum(c["kind"] == "exact" for c in checks),
    "numerical_bound_samples": sum(c["kind"] != "exact" for c in checks),
    "results": checks,
}, ensure_ascii=False, indent=2))
