#!/usr/bin/env python3
"""Checks exactos de la nota CURVATURA_TPK_Y_REFINAMIENTO.md.

No accede a la red, no modifica archivos, no usa datos objetivo ni constantes
físicas externas. Los fixtures prueban identidades algebraicas y falsadores;
no reemplazan la selección de estados de los propietarios HMT.
"""
from fractions import Fraction as Q
import json


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def adj(a):
    return [[a[i][j].conjugate() for i in range(len(a))]
            for j in range(len(a[0]))]


def add(a, b, s=1):
    return [[a[i][j] + s*b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def scale(a, s):
    return [[s*x for x in r] for r in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def comm(a, b):
    return add(mul(a, b), mul(b, a), -1)


def inv2(a):
    d = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [[Q(a[1][1], d), Q(-a[0][1], d)],
            [Q(-a[1][0], d), Q(a[0][0], d)]]


def pair(a, w, b):
    return mul(mul(adj(a), w), b)[0][0]


def compose(a, b):
    """a after b, affine pairs (linear, column translation)."""
    ca, ka = a
    cb, kb = b
    return mul(ca, cb), add(mul(ca, kb), ka)


def inverse(a):
    ci = inv2(a[0])
    return ci, scale(mul(ci, a[1]), -1)


checks = []


def check(name, ok):
    if not ok:
        raise AssertionError(name)
    checks.append(name)


# Cocycle and two-route comparison, with rational exact coefficients.
a = ([[1, 1], [0, 1]], [[1], [2]])
b = ([[1, 0], [1, 1]], [[-1], [3]])
c = ([[0, -1], [1, 0]], [[4], [-2]])
ident = (eye(2), [[0], [0]])
check("affine_associativity", compose(a, compose(b, c)) == compose(compose(a, b), c))
check("affine_inverse", compose(inverse(a), a) == ident)
loop = compose(inverse(a), compose(inverse(b), compose(a, b)))
lin = mul(mul(mul(inv2(a[0]), inv2(b[0])), a[0]), b[0])
trans = mul(mul(inv2(a[0]), inv2(b[0])),
            add(mul(add(a[0], eye(2), -1), b[1]),
                mul(add(b[0], eye(2), -1), a[1]), -1))
check("ordered_affine_loop", loop == (lin, trans))
check("nonzero_loop_is_retained", loop != ident)
check("inverse_route_reverses_memory", compose(inverse(loop), loop) == ident)
phase, turns, sheets = 0, 0, 0
for _ in range(4):
    phase = (phase + 1) % 4
    turns += 1
    sheets += 18
check("source_return_108_keeps_4_72", (phase, turns, sheets) == (0, 4, 72))

# Full mixed coefficient of E=<r,W r> in the ring x^2=y^2=0.
r = {(0, 0): [[1], [1j]], (1, 0): [[2], [-1j]],
     (0, 1): [[1j], [3]], (1, 1): [[1-1j], [2]]}
w = {(0, 0): [[3, 1+1j], [1-1j, 4]],
     (1, 0): [[1, 2j], [-2j, -1]],
     (0, 1): [[0, 2], [2, 1]],
     (1, 1): [[-2, 1j], [-1j, 3]]}
coefficient = 0
for p, rp in r.items():
    for q, wq in w.items():
        for s, rs in r.items():
            if tuple(p[k]+q[k]+s[k] for k in range(2)) == (1, 1):
                coefficient += pair(rp, wq, rs)
r0, rx, ry, rxy = (r[k] for k in ((0, 0), (1, 0), (0, 1), (1, 1)))
w0, wx, wy, wxy = (w[k] for k in ((0, 0), (1, 0), (0, 1), (1, 1)))
formula = 2*(pair(rx, w0, ry)+pair(r0, wx, ry)
             +pair(r0, wy, rx)+pair(r0, w0, rxy)).real + pair(r0, wxy, r0)
check("Hessian_complete_mixed_coefficient", coefficient == formula)
swapped = 2*(pair(ry, w0, rx)+pair(r0, wy, rx)
             +pair(r0, wx, ry)+pair(r0, w0, rxy)).real + pair(r0, wxy, r0)
check("Hessian_mixed_symmetry", formula == swapped)
check("omitting_weight_variation_detected", formula != 2*(pair(rx, w0, ry)+pair(r0, w0, rxy)).real)

# Covariant scalar Hessian cancels curvature only in the scalar pairing.
sx = [[0, 1], [1, 0]]
sy = [[0, -1j], [1j, 0]]
sz = [[1, 0], [0, -1]]
curv = scale(sz, 1j)
weight = add(scale(eye(2), 2), sx)
vec = [[1], [1j]]
t1 = 2*pair(vec, weight, mul(curv, vec)).real
t2 = pair(vec, comm(curv, weight), vec)
check("covariant_Hessian_curvature_cancellation", t1+t2 == 0)
check("two_nonzero_terms_4_minus4", (t1, t2) == (4, -4))
check("curvature_is_not_zero", curv != [[0, 0], [0, 0]])

# Two individually zero sector curvatures need not sum to total curvature.
cross = scale(comm(sx, sy), 1j)
check("total_cross_sector_term", cross == scale(sz, -2))
check("sectorwise_zero_does_not_imply_total_zero", cross != [[0, 0], [0, 0]])

# Plaquette Z2: fixed gauge transformations change edges at their endpoints.
configs = list(range(16))
gauge = list(range(16))


def act(g, u):
    result = u
    for edge in range(4):
        flip = ((g >> edge) & 1) ^ ((g >> ((edge+1) % 4)) & 1)
        if flip:
            result ^= 1 << edge
    return result


def project(f):
    return [sum(Q(f[act(g, u)], 16) for g in gauge) for u in configs]


one = [1]*16
wilson = [(-1)**bin(u).count("1") for u in configs]
check("Wilson_gauge_invariant", all(wilson[act(g, u)] == wilson[u] for g in gauge for u in configs))
check("physical_constant", project(one) == one)
check("physical_nontrivial_Wilson", project(wilson) == wilson)
check("Ward_finite_measure", all(sum((act(g, u)**2-u**2) for u in configs) == 0 for g in gauge))
check("gauge_average_idempotent", project(project([u*u for u in configs])) == project([u*u for u in configs]))
check("holonomy_not_identity_on_physical", project(wilson) != one)
check("true_gauge_action_is_identity_on_physical", all([wilson[act(g, u)] for u in configs] == wilson for g in gauge))

# Explicit nonadic diagonal: numerical depth controls curvature extraction.
for m in range(1, 7):
    eps = Q(1, 9**m)
    precision_error = Q(4, 729**m)
    check("precision_o_area_%d" % m, precision_error/(eps*eps) == 4*eps)

# Exact scalar coefficients of a unitary Cayley counterexample.
for n in (1, 9, 81):
    for eps in (Q(1, 9), Q(1, 81), Q(1, 729)):
        t = eps*eps/(1+n*eps*eps)
        re = (1-t*t)/(1+t*t)
        im = 2*t/(1+t*t)
        check("Cayley_unitarity_%s_%s" % (n, eps), re*re+im*im == 1)
        check("uniform_loop_bound_%s_%s" % (n, eps), t <= Q(1, n))
print(json.dumps({
    "status": "PASS_CURVATURA_TPK_REFINAMIENTO_FOCAL",
    "checks": len(checks),
    "arithmetic": "exact integer/complex integer and Fraction",
    "scope": "Identities and falsifiers in the companion note; not total PCH closure",
    "results": checks,
}, ensure_ascii=False, indent=2))
