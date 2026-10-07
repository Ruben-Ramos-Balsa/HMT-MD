#!/usr/bin/env python3
"""Exact finite identities underlying the accompanying analytic proofs.

Read-only loading of the published projector owner; no PDF or corpus writes.
Run normally, with -O, or with -I -S. Assertions are deliberately not used.
This script does not replace Poisson summation with numerical truncation.
"""

from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[3]
OWNER_LOCAL = Path(__file__).resolve().parents[1]/"provenance/owners/X_variacional.py"
OWNER = OWNER_LOCAL if OWNER_LOCAL.exists() else ROOT / "output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/supplement/vendor/variacional/controles_articulo_I/propietarios_k_moonshine/variacional.py"
EXPECTED = "bd1bfff1abec55e2f03477875002d44c01a9732c15348c99f9e211148c900e57"
checks = []


def require(condition, name):
    if not condition:
        raise RuntimeError("FAIL: " + name)
    checks.append(name)


require(hashlib.sha256(OWNER.read_bytes()).hexdigest() == EXPECTED, "owner_sha256")
o = runpy.run_path(str(OWNER), run_name="leech_owner_readonly")
Z, ONE = o["ZERO"], o["ONE"]
add, sub, mul, scale = (o[n] for n in ("q5_add", "q5_sub", "q5_mul", "q5_scale"))
mm, tr, mv = (o[n] for n in ("matmul", "transpose", "matrix_vector"))
ma, ms, ident = (o[n] for n in ("matrix_add", "matrix_sub", "identity"))


def scalar(a, b=0):
    return (F(a), F(b))


def qsum(values):
    result = Z
    for v in values:
        result = add(result, v)
    return result


def block_diagonal(blocks):
    sizes = [len(b) for b in blocks]
    n = sum(sizes)
    result = [[Z for _ in range(n)] for _ in range(n)]
    start = 0
    for block, size in zip(blocks, sizes):
        for i in range(size):
            for j in range(size):
                result[start+i][start+j] = block[i][j]
        start += size
    return result


K = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
P = o["projector_three"]()
require(sum(K) == 6263, "K_sum")
require(P == tr(P), "P_symmetric")
require(mm(P, P) == P, "P_idempotent")
require(o["rank"](P) == 3, "P_rank_three")
require(mv(P, [ONE]*12) == [Z]*12, "P_annihilates_constant_vector")
u = mv(P, [scalar(k) for k in K])
expected_u = [
    scalar(F(-495,4), F(-233,10)), scalar(F(403,4), F(169,10)),
    scalar(F(-403,4), F(-169,10)), scalar(F(495,4), F(233,10)),
    scalar(F(601,4), F(1031,10)), scalar(F(203,4), F(211,5)),
    scalar(F(-203,4), F(-211,5)), scalar(F(-601,4), F(-1031,10)),
    scalar(F(313,4), F(569,10)), scalar(162, F(219,20)),
    scalar(-162, F(-219,20)), scalar(F(-313,4), F(-569,10)),
]
require(u == expected_u, "all_twelve_coordinates_exact")
require(qsum(u) == Z, "u_zero_sum")
require(o["dot"](u, u) == scalar(F(6638585,20), F(2275584,20)), "u_squared_norm")
for i, j in ((0,3), (1,2), (4,7), (5,6), (8,11), (9,10)):
    require(add(u[i], u[j]) == Z, "opposite_coefficients_%s_%s" % (i+1,j+1))

B2 = [[scalar(2),scalar(-1)], [scalar(-1),scalar(2)]]
C = [[Z,scalar(-1)], [ONE,scalar(-1)]]
Cinv = mm(C, C)
B = block_diagonal([B2]*12)
cstar = (1,1,1,1,1,1,2,1,1,1,1,1)
require(o["codeword"]((1,)*6) == cstar, "full_support_glue_word")
g = block_diagonal([Cinv if c == 1 else C for c in cstar])
I = ident(24)
g2 = mm(g,g)
require(mm(g2,g) == I, "g_order_three")
require(ma(ma(g2,g),I) == [[Z]*24 for _ in range(24)], "g_cyclotomic_polynomial")
require(mm(mm(tr(g),B),g) == B, "g_metric_isometry")
require(o["rank"](ms(g,I)) == 24, "g_has_no_fixed_vectors")
H = block_diagonal([[[x,Z],[Z,x]] for x in u])
require(mm(tr(H),B) == mm(B,H), "H_metric_self_adjoint")
require(mm(H,g) == mm(g,H), "H_commutes_with_g")
require(o["trace"](H) == Z, "trace_H_zero_determinant_exponential_one")

# Verify exp(su) exp(-su) coefficient identities through order ten.
# The analytic identity for all orders is proved by the binomial theorem.
for j, h in enumerate(u):
    powers = [ONE]
    for n in range(1,11):
        powers.append(mul(powers[-1],h))
    for n in range(11):
        coeff = qsum(scale(powers[n], F((-1)**(n-r), factorial(r)*factorial(n-r))) for r in range(n+1))
        require(coeff == (ONE if n == 0 else Z), "exponential_inverse_plane_%d_order_%d" % (j+1,n))

# Neighbour stability: exact discriminant classes and inner products.
v = [scalar(a) for a in ([4,4] + [1]*22)]
require(o["dot"](v,mv(B,v)) == scalar(54), "marked_vector_norm_54")
y = [scale(sub(a,b),F(1,3)) for a,b in zip(mv(g,v),v)]
z = [scale(sub(a,b),F(1,3)) for a,b in zip(mv(g2,v),v)]
for name, w, word in (("y",y,cstar),("z",z,tuple((-x)%3 for x in cstar))):
    require(o["dot"](w,mv(B,v)) == scalar(-27), name + "_inner_product_minus_27")
    for j in range(12):
        a,b = scale(w[2*j],3),scale(w[2*j+1],3)
        require(a[1] == b[1] == 0 and a[0].denominator == b[0].denominator == 1, name + "_rational_numerator_%d" % (j+1))
        require(int(a[0]-2*b[0])%3 == 0 and int(b[0])%3 == word[j], name + "_glue_class_%d" % (j+1))

f0 = scalar(F(2,9)*(16+11))
fprime = scale(add(scale(u[0],16),qsum(u[1:])),F(4,9))
require(f0 == scalar(6), "witness_norm_at_zero")
require(fprime == scalar(-825,F(-466,3)), "nonintegrality_derivative_exact")
require(o["q5_sign"](fprime) == -1, "nonintegrality_derivative_nonzero")

# Split form Q=[[0,B],[B,0]] and generator Hcal=diag(H,-H).
# Block identities are equivalent to Hcal^T Q+Q Hcal=0.
minusH = o["matrix_scale"](H,-1)
require(ma(mm(tr(H),B),mm(B,minusH)) == [[Z]*24 for _ in range(24)], "split_skew_adjoint_upper_block")
require(ma(mm(tr(minusH),B),mm(B,H)) == [[Z]*24 for _ in range(24)], "split_skew_adjoint_lower_block")
require(o["rank"](B) == 24, "split_signature_24_24_nondegenerate_B")
# Positive definiteness B2: Sylvester's criterion for the orthogonal blocks.
require(B2[0][0] == scalar(2) and sub(mul(B2[0][0],B2[1][1]),mul(B2[0][1],B2[1][0])) == scalar(3), "B_positive_by_block_sylvester")

report = {
    "status": "PASS_LEECH_K_FINITE_IDENTITIES",
    "checks": len(checks),
    "owner_sha256": EXPECTED,
    "field": "Q(sqrt(5)), exact rational pair arithmetic",
    "u": [o["q5_text"](x) for x in u],
    "witness_derivative": o["q5_text"](fprime),
    "analytic_proof": "LEECH_K_DEFORMACION_THETA.md",
    "scope": "Finite identities only; continuous-parameter duality, Poisson, lattice self-duality and operator-domain assertions use the contiguous proofs and the cited owner hypotheses.",
}
print(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2))
