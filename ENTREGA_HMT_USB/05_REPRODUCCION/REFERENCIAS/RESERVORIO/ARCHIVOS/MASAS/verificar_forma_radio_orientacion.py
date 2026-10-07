#!/usr/bin/env python3
"""Exact Laurent identities for the ellipse/radius/orientation bridge.

R and U are formal nonzero variables; physically R>0 and U=sqrt(lambda_act)>0.
This checks the downstream identities, not the antecedent HMT generator,
the modular j theorem, or a physical string-radius identification.
No numerical constants, target decimals, external modules, or file writes.
"""
import json
import sys


def mon(r=0, u=0, coefficient=1):
    return {(r, u): coefficient} if coefficient else {}


def add(a, b):
    result = dict(a)
    for exponent, coefficient in b.items():
        result[exponent] = result.get(exponent, 0) + coefficient
        if result[exponent] == 0:
            del result[exponent]
    return result


def neg(a):
    return {exponent: -coefficient for exponent, coefficient in a.items()}


def mul(a, b):
    result = {}
    for (r1, u1), c1 in a.items():
        for (r2, u2), c2 in b.items():
            result = add(result, mon(r1 + r2, u1 + u2, c1 * c2))
    return result


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    bt = transpose(b)
    return tuple(tuple(add(mul(row[0], col[0]), mul(row[1], col[1]))
                       for col in bt) for row in a)


def matneg(a):
    return tuple(tuple(neg(x) for x in row) for row in a)


def congruence(transform, form):
    return matmul(matmul(transpose(transform), form), transform)


Z, ONE = mon(coefficient=0), mon()
I = ((ONE, Z), (Z, ONE))
S = ((Z, ONE), (ONE, Z))
Jrot = ((Z, neg(ONE)), (ONE, Z))
Omega = ((Z, ONE), (neg(ONE), Z))
D = ((mon(-2), Z), (Z, mon(2)))
D_inverse = ((mon(2), Z), (Z, mon(-2)))
checks = []


def check(name, condition):
    if not condition:
        raise RuntimeError(name)
    checks.append(name)


check("normalized_axes_product", mul(mon(-1), mon(1)) == ONE)
check("normalized_axes_ratio_R_squared", mul(mon(1), mon(1)) == mon(2))
check("squared_axes_matrix_first_entry", mul(mon(-1), mon(-1)) == D[0][0])
check("squared_axes_matrix_second_entry", mul(mon(1), mon(1)) == D[1][1])
check("ellipse_equation_matrix_is_inverse", matmul(D, D_inverse) == I)
check("swap_energy_congruence", congruence(S, D_inverse) == D)
check("rotation_energy_congruence", congruence(Jrot, D_inverse) == D)
check("swap_involution", matmul(S, S) == I)
check("rotation_square_minus_identity", matmul(Jrot, Jrot) == matneg(I))
check("swap_reverses_symplectic_form", congruence(S, Omega) == matneg(Omega))
check("rotation_preserves_symplectic_form", congruence(Jrot, Omega) == Omega)

# One-form coefficients in the basis (P dQ, Q dP).
liouville = (1, 0)
d_pq = (1, 1)
check("swap_liouville_exact_remainder",
      (0, 1) == tuple(b - a for a, b in zip(liouville, d_pq)))
check("rotation_liouville_exact_remainder",
      (0, -1) == tuple(a - b for a, b in zip(liouville, d_pq)))

# If tau=i R^2, then tau(R)*tau(1/R)=-1 exactly.
check("modular_reciprocity",
      neg(mul(mon(2), mon(-2))) == neg(ONE))
# Cross-multiply x=(1-R^4)/(1+R^4), so (1-x)/(1+x)=R^4.
num = add(ONE, neg(mon(4)))
den = add(ONE, mon(4))
check("angular_ratio_reconstruction",
      add(den, neg(num)) == mul(mon(4), add(den, num)))

# U rescales both axes. G rescales by U^-2.
check("action_scale_from_axes",
      mul(mon(-1, 1), mon(1, 1)) == mon(0, 2))
check("shape_unchanged_by_common_scale",
      mul(mon(1, 1), mon(1, -1)) == mon(2))
check("gravity_times_action_invariant",
      mul(mon(0, -2), mon(0, 2)) == ONE)
check("gravity_times_axes_product_invariant",
      mul(mon(0, -2), mul(mon(-1, 1), mon(1, 1))) == ONE)

# Adversarial identities must fail as formal Laurent identities.
check("reject_wrong_signed_radius_same_module", mon(2) != mon(-2))
check("reject_same_matrix_for_axes_and_equation", D != D_inverse)
check("reject_symplectic_swap", congruence(S, Omega) != Omega)
check("reject_involutive_quarter_rotation", matmul(Jrot, Jrot) != I)
check("reject_fixed_axes_under_changed_action", ONE != mon(0, 2))
check("reject_action_loss_from_energy_only", S != Jrot)

print(json.dumps({
    "result": "PASS_EXACT_ELLIPSE_RADIUS_ORIENTATION_IDENTITIES",
    "scope": "downstream Laurent and two-dimensional matrix identities",
    "method": "formal polynomial equality; not finite decimal sampling",
    "checks": len(checks),
    "check_names": checks,
    "limitations": [
        "Does not rerun APP-TRIT-TPK or generate its angle and action outputs.",
        "Does not prove a physical string radius or full theory M identification.",
        "Modular j invariance is the cited mathematical theorem, not this code."
    ]
}, ensure_ascii=False, indent=2))

