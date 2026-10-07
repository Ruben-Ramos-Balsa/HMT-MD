#!/usr/bin/env python3
"""Rational checks of finite recovery on K and exterior area decomposition.

K uses the documented shift S, its third/fourth powers, and the total q.
Coxeter tests are algebraic realizations with the A2 metric, not a selection
of any physical trajectory or identification of K with twelve A2 fibres.
All checks are explicit and remain active under python -O. No files are written.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json
import runpy

COUNT = 0
VARIATIONAL_OWNER = str(
    Path(__file__).resolve().parents[1] / "vendor" / "variacional"
    / "controles_articulo_I" / "propietarios_k_moonshine" / "variacional.py"
)


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def zero(n):
    return mat([[0] * n for _ in range(n)])


def tr(a):
    return tuple(zip(*a))


def plus(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br))
                 for ar, br in zip(a, b))


def times(c, a):
    return tuple(tuple(F(c) * x for x in row) for row in a)


def minus(a, b):
    return plus(a, times(-1, b))


def mul(a, b):
    return tuple(tuple(sum((x*y for x, y in zip(row, col)), F(0))
                       for col in tr(b)) for row in a)


def power(a, n):
    out = eye(len(a))
    for _ in range(n):
        out = mul(out, a)
    return out


def inv(a):
    n = len(a)
    rows = [list(a[i]) + list(eye(n)[i]) for i in range(n)]
    for k in range(n):
        pivot = next((j for j in range(k, n) if rows[j][k]), None)
        if pivot is None:
            raise ArithmeticError("Singular exact matrix")
        rows[k], rows[pivot] = rows[pivot], rows[k]
        q = rows[k][k]
        rows[k] = [x/q for x in rows[k]]
        for j in range(n):
            if j != k:
                q = rows[j][k]
                rows[j] = [x-q*y for x, y in zip(rows[j], rows[k])]
    return tuple(tuple(row[n:]) for row in rows)


def gram(a, g):
    return mul(tr(a), mul(g, a))


def kron(a, b):
    return tuple(tuple(a[i][j]*b[u][v]
                       for j in range(len(a[0])) for v in range(len(b[0])))
                 for i in range(len(a)) for u in range(len(b)))


def column(xs):
    return mat([[x] for x in xs])


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def check(name, actual, expected):
    global COUNT
    if actual != expected:
        raise AssertionError(f"{name}\nactual={actual}\nexpected={expected}")
    COUNT += 1


def condition(name, truth):
    global COUNT
    if not truth:
        raise AssertionError(name)
    COUNT += 1


def lector(c):
    i = eye(len(c))
    return times(F(1, 9), plus(times(8, i), c)), times(
        F(1, 9), minus(c, i))


def recover_differences(z0, z1, q, t3_inverse):
    b = times(-9, z0)
    c = times(-9, mul(t3_inverse, z1))
    w = [c[i][0] - b[(i+1) % 12][0] for i in range(12)]
    partials, running = [], F(0)
    for wi in w:
        partials.append(running)
        running += wi
    k0 = (F(q) + sum(partials, F(0))) / 12
    return column([k0 - x for x in partials])


def minor2(a, rows, cols):
    i, j = rows
    k, l = cols
    return a[i][k]*a[j][l] - a[i][l]*a[j][k]


def check_variational_projection(z0, z1, t3_inverse, canonical):
    """Recover the mean-zero input using q=0, then use the actual source P3.

    run_name differs from __main__: the owner's main(), which writes its
    certificate, is never called. Only its exact Q(sqrt(5)) definitions run.

    Uniform error argument (not an inference from testing one vector): let
    A=(D3,D4*T3) on 1-perp. The spectral resolution checked below gives
    A* A >= (16/81) I, so ||A^dagger|| <= 9/4. Thus data error of norm eps
    gives ||delta kappa|| <= 9 eps/4, and the orthogonal P3 cannot increase
    it. For f(x)=||P3*x||/||x||=sqrt(eta), y!=0 and x!=0,
    |f(y)-f(x)| <= | ||P3*y||-||P3*x|| |/||x||
                     + f(y)*| ||x||-||y|| |/||x||
                 <= 2||y-x||/||x||.
    Consequently |delta sqrt(eta)| <= 9 eps/(2||kappa||); eps <
    4||kappa||/9 ensures the reconstructed nonzero denominator. This bound
    concerns the readout ratio, not a norm-square promoted to a probability.

    For P10=P11-E_u, E_u=uu*/||u||^2, u=P3*kappa, let u'=P3*kappa'.
    If eps < 4||u||/9 then u' != 0. Rank-one orthogonal projectors obey
    ||E_u'-E_u||=sin(angle(u,u'))=dist(u,span(u'))/||u||,
    hence ||P10'-P10|| <= ||u'-u||/||u|| <= 9 eps/(4||u||).
    The denominator is sqrt(eta)*||kappa||, not eta*||kappa||. This is a
    consequence of the exact two-dimensional span calculation and applies
    to every perturbation satisfying the stated bound.
    """
    owner = runpy.run_path(VARIATIONAL_OWNER, run_name="hmt_variational_owner_read_only")
    p3 = owner["projector_three"]()
    qzero = owner["ZERO"]
    qone = owner["ONE"]
    qmul = owner["matmul"]
    qsub = owner["matrix_sub"]
    qtranspose = owner["transpose"]
    qrank = owner["rank"]
    qmv = owner["matrix_vector"]
    qdot = owner["dot"]
    qscale = owner["q5_scale"]
    qsign = owner["q5_sign"]
    qidentity = owner["identity"](12)
    qmean = [[(F(1,12), F(0)) for _ in range(12)] for _ in range(12)]
    p11 = qsub(qidentity, qmean)
    # Neither this call nor its inputs use q=6263 or the reference K.
    recovered = recover_differences(z0, z1, 0, t3_inverse)
    kappa = [(row[0], F(0)) for row in recovered]
    reference = [(row[0], F(0)) for row in canonical]
    check("q=0 recovery: mean zero", sum((row[0] for row in recovered), F(0)), F(0))
    check("q=0 recovery: equals P11 K afterwards", kappa, qmv(p11, reference))
    check("source P3 symmetric", qtranspose(p3), p3)
    check("source P3 idempotent", qmul(p3,p3), p3)
    check("source P3 rank three", qrank(p3), 3)
    check("P11 rank eleven", qrank(p11), 11)
    check("source P3 lies in P11", qmul(p3,p11), p3)
    check("source P3 annihilates mean", qmul(p3,qmean), [[qzero]*12 for _ in range(12)])
    projected = qmv(p3,kappa)
    check("P3 reconstruction from q=0 records", projected, qmv(p3,reference))
    norm_squared = qdot(projected,projected)
    centered_norm_squared = qdot(kappa,kappa)
    check("source P3 projected norm squared", norm_squared,
          (F(6638585,20), F(2275584,20)))
    check("q=0 centered norm squared", centered_norm_squared, (F(11789915,12),F(0)))
    eta = qscale(norm_squared, F(12,11789915))
    check("eta exact quotient", owner["q5_mul"](eta,centered_norm_squared), norm_squared)
    condition("eta strictly positive", qsign(eta) > 0)
    condition("eta strictly below one", qsign(owner["q5_sub"](qone,eta)) > 0)
    # Definition and proof owner: sections/k_direccion_dimensional.tex:105--139
    # and sections/03_pantallas_coordinadas.tex:123--166 in the same article.
    def direction_projector(vector):
        norm_inverse = owner["q5_inv"](qdot(vector,vector))
        return [[owner["q5_mul"](norm_inverse, owner["q5_mul"](x,y))
                 for y in vector] for x in vector]
    direction = direction_projector(projected)
    p10 = qsub(p11,direction)
    reference_p10 = qsub(p11,direction_projector(qmv(p3,reference)))
    check("P10 from q=0 records matches source definition", p10, reference_p10)
    check("direction projector symmetric", qtranspose(direction), direction)
    check("direction projector idempotent", qmul(direction,direction), direction)
    check("direction projector rank one", qrank(direction), 1)
    check("direction lies in P11", qmul(p11,direction), direction)
    check("direction lies in P3", qmul(p3,direction), direction)
    check("P10 symmetric", qtranspose(p10), p10)
    check("P10 idempotent", qmul(p10,p10), p10)
    check("P10 rank ten", qrank(p10), 10)
    check("P10 remains in P11", qmul(p10,p11), p10)
    check("P10 annihilates the recovered direction", qmv(p10,projected), [qzero]*12)
    check("P10 readout from recovered mean-zero input", qmv(p10,kappa),
          qmv(reference_p10,reference))
    transverse = qmv(p10,kappa)
    check("P10 subtracts precisely the P3 component of this K", transverse,
          owner["vector_add"](kappa, owner["vector_scale"](projected,-1)))
    check("P10 squared norm balance", owner["q5_add"](qdot(transverse,transverse),norm_squared),
          centered_norm_squared)
    check("P10 retains the two P3 directions orthogonal to u",
          qmul(p3,p10), qsub(p3,direction))
    check("retained P3 sector rank two", qrank(qmul(p3,p10)), 2)
    return {"projected_norm_squared": owner["q5_text"](norm_squared),
            "mean_zero_norm_squared": "11789915/12",
            "eta": owner["q5_text"](eta),
            "P10_rank": 10,
            "P10_recovered_from_zero_charge_records": True,
            "general_error_bounds": {
                "kappa_and_u": "9 eps/4",
                "sqrt_eta": "9 eps/(2 ||kappa||)",
                "P10_operator_norm": "9 eps/(4 ||u||)",
                "P10_nonzero_condition": "eps < 4 ||u||/9"
            },
            "source": VARIATIONAL_OWNER,
            "source_main_executed": False,
            "reconstruction_charge": 0}


def run():
    i = eye(12)
    s = mat([[int(j == (r+1) % 12) for j in range(12)] for r in range(12)])
    s3, s4 = power(s, 3), power(s, 4)
    t3, l3 = lector(s3)
    t4, l4 = lector(s4)
    m1 = mul(l4, t3)
    pmean = times(F(1, 12), mat([[1]*12 for _ in range(12)]))
    t3_inverse = times(F(1, 455), plus(
        minus(times(512, i), times(64, s3)),
        minus(times(8, power(s, 6)), power(s, 9))))
    check("S has order 12", power(s, 12), i)
    check("T3 explicit inverse", t3_inverse, inv(t3))
    check("T3 inverse left", mul(t3_inverse, t3), i)
    check("T3 inverse right", mul(t3, t3_inverse), i)

    gram_z = plus(gram(l3, i), gram(m1, i))
    g = times(8, gram_z)
    p2 = mul(t4, t3)
    check("finite terminal-memory identity", plus(g, gram(p2, i)), i)
    check("mean is kernel", mul(g, pmean), zero(12))

    # Exact spectral resolution by polynomial projectors, with rational eigenvalues.
    spectrum = {
        F(0): 1, F(16, 81): 2, F(8, 27): 2, F(32, 81): 1,
        F(952, 2187): 4, F(1256, 2187): 2,
    }
    projectors = {}
    total = zero(12)
    for value, multiplicity in spectrum.items():
        proj = i
        for other in spectrum:
            if other != value:
                proj = mul(proj, times(1/(value-other), minus(g, times(other, i))))
        projectors[value] = proj
        total = plus(total, proj)
        check(f"projector {value}: symmetric", tr(proj), proj)
        check(f"projector {value}: idempotent", mul(proj, proj), proj)
        check(f"projector {value}: eigenvalue", mul(g, proj), times(value, proj))
        check(f"projector {value}: rank", trace(proj), F(multiplicity))
    check("spectral completeness", total, i)
    check("zero spectral projector", projectors[F(0)], pmean)
    check("sharp lower bound on mean zero", min(x for x in spectrum if x), F(16, 81))

    inverse_regularized = inv(plus(gram_z, pmean))
    # Reconstruction receives only the published two records and the charge.
    # The reference K is introduced afterwards, solely as the expected result.
    record_a = column([495, 116, 684, -108, -601, 90,
                       173, 88, -313, -560, 397, -461])
    record_b = column([2729, 2503, 3818, -5843, 2583, -920,
                       -4051, 4338, -5312, -1583, 233, 1505])
    supplied_z0, supplied_z1 = times(F(1,9), record_a), times(F(1,81), record_b)
    reconstructed_from_records = recover_differences(
        supplied_z0, supplied_z1, 6263, t3_inverse)
    record_adjoint = plus(mul(tr(l3), supplied_z0), mul(tr(m1), supplied_z1))
    reconstructed_from_records_ls = plus(column([F(6263,12)]*12),
                                          mul(inverse_regularized, record_adjoint))
    canonical = column([234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601])
    check("canonical K total", sum((row[0] for row in canonical), F(0)), F(6263))
    check("literal records alone: difference inverse", reconstructed_from_records, canonical)
    check("literal records alone: least-squares inverse", reconstructed_from_records_ls, canonical)
    check("literal first record after reconstruction", times(9, mul(l3, canonical)), record_a)
    check("literal second record after reconstruction", times(81, mul(m1, canonical)), record_b)
    variational_result = check_variational_projection(
        supplied_z0, supplied_z1, t3_inverse, canonical)
    tests = [(f"basis {j}", column([int(k == j) for k in range(12)]))
             for j in range(12)] + [("canonical K", canonical)]
    for name, k in tests:
        q = sum((row[0] for row in k), F(0))
        z0, z1 = mul(l3, k), mul(m1, k)
        recovered = recover_differences(z0, z1, q, t3_inverse)
        check(name + ": difference reconstruction", recovered, k)
        adjoint_data = plus(mul(tr(l3), z0), mul(tr(m1), z1))
        least_squares = plus(column([q/12]*12),
                             mul(inverse_regularized, adjoint_data))
        check(name + ": rational least-squares reconstruction", least_squares, k)
        check(name + ": finite energy balance",
              plus(gram(mul(p2, k), i), times(8, plus(gram(z0, i), gram(z1, i)))),
              gram(k, i))

    # A third S3 (or S^-3) reading raises the sharp lower bound to 8/27.
    g_third3 = minus(i, gram(mul(t3, p2), i))
    tminus3, _ = lector(power(s, 9))
    check("third S3 or inverse same Gram", g_third3,
          minus(i, gram(mul(tminus3, p2), i)))
    third_spectrum = {
        F(0): F(0), F(16,81): F(2336,6561), F(8,27): F(8,27),
        F(32,81): F(4160,6561), F(952,2187): F(96872,177147),
        F(1256,2187): F(131528,177147),
    }
    for old_value, new_value in third_spectrum.items():
        proj = projectors[old_value]
        check(f"third S3 on {old_value}", mul(g_third3, proj), times(new_value, proj))
    check("third S3 sharp bound", min(v for v in third_spectrum.values() if v), F(8,27))
    g_third4 = minus(i, gram(mul(t4, p2), i))
    weak = projectors[F(16,81)]
    check("third S4 leaves weakest modes unchanged",
          mul(g_third4, weak), times(F(16,81), weak))

    # Tensoring the position reader by a 2D fibre preserves the Gram constant.
    g2 = mat([[2, -1], [-1, 2]])
    fibre_metric = kron(i, g2)
    lifted_gram = times(8, plus(
        gram(kron(l3, eye(2)), fibre_metric),
        gram(kron(m1, eye(2)), fibre_metric)))
    check("two-dimensional fibre tensor", lifted_gram, kron(g, g2))

    # Concrete A2 Coxeter model of C^2+C+I=0; not the full exceptional matrix g_c.
    c = mat([[0, -1], [1, -1]])
    ii = eye(2)
    check("Coxeter polynomial", plus(plus(mul(c, c), c), ii), zero(2))
    check("Coxeter preserves A2 form", gram(c, g2), g2)
    t, ell = lector(c)
    a, b = F(19,27), F(8,27)
    check("Coxeter visible Gram", gram(t, g2), times(a, g2))
    check("Coxeter memory Gram", times(8, gram(ell, g2)), times(b, g2))
    ell_inverse = times(-3, plus(c, times(2, ii)))
    check("first normalized complement inverse", mul(ell_inverse, ell), ii)
    check("first normalized complement inverse right", mul(ell, ell_inverse), ii)
    mtwo = mul(ell, t)
    check("two complement Gram", times(8, plus(gram(ell, g2), gram(mtwo, g2))),
          times(F(368,729), g2))
    g2_inverse = inv(g2)
    ell_adjoint = mul(g2_inverse, mul(tr(ell), g2))
    t_adjoint = mul(g2_inverse, mul(tr(t), g2))
    for j in range(2):
        k = column([int(z == j) for z in range(2)])
        z0, z1 = mul(ell, k), mul(mtwo, k)
        check(f"Coxeter basis {j}: first complement", mul(ell_inverse, z0), k)
        recovered = times(F(729,46), plus(mul(ell_adjoint, z0),
                           mul(t_adjoint, mul(ell_adjoint, z1))))
        check(f"Coxeter basis {j}: two complements", recovered, k)

    # Source: capitulo_22_c20_lineas_2613_3270.tex, lines 180--225, 311--313.
    # Its c_* selects C^-1 when the component is 1, C when it is 2.
    # This is the real 24-dimensional block action, not a lift of the K vector.
    cstar = [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
    blocks = [power(c, 2) if component == 1 else c for component in cstar]
    gc = mat([[blocks[r//2][r%2][j%2] if r//2 == j//2 else 0
               for j in range(24)] for r in range(24)])
    i24 = eye(24)
    check("source gc real block action: order three", power(gc, 3), i24)
    check("source gc real block action: fixed-free polynomial",
          plus(plus(power(gc, 2), gc), i24), zero(24))
    check("source gc real block action: A2^12 metric", gram(gc, fibre_metric), fibre_metric)
    rho = column([1, 1])
    check("source rho: forward Coxeter difference", minus(mul(c, rho), rho), column([-2,-1]))
    check("source rho: reverse Coxeter difference", minus(mul(power(c,2), rho), rho), column([-1,-2]))
    v = column([4,4] + [1,1]*11)
    tc, lc = lector(gc)
    check("source vector v has norm squared 54", gram(v, fibre_metric), mat([[54]]))
    check("source vector visible norm squared 38", gram(mul(tc,v), fibre_metric), mat([[38]]))
    check("source vector memory norm squared 16",
          times(8, gram(mul(lc,v), fibre_metric)), mat([[16]]))
    lc_inverse = times(-3, plus(gc, times(2,i24)))
    check("source gc normalized complement inverse", mul(lc_inverse, lc), i24)
    check("source vector recovered from first complement", mul(lc_inverse, mul(lc,v)), v)

    # Finite realizations of the ordered Coxeter/shear loop. The integer n is
    # an algebraic parameter here, not a selected physical TPK calendar.
    shear = mat([[1,1],[0,1]])
    shear_inverse, c_inverse = inv(shear), inv(c)
    omega = mat([[0,1],[-1,0]])
    loop_parameters = [-3,-2,-1,1,2,3,10]
    for n in loop_parameters:
        pn = power(shear,n) if n >= 0 else power(shear_inverse,-n)
        loop = mul(c_inverse,mul(inv(pn),mul(c,pn)))
        expected_loop = mat([[1+n,n*n],[n,n*n-n+1]])
        fn = mat([[1,n],[1,n-1]])
        check(f"ordered loop n={n}: explicit matrix", loop, expected_loop)
        check(f"ordered loop n={n}: F square", power(fn,2), loop)
        check(f"ordered loop n={n}: F polynomial", minus(minus(power(fn,2),times(n,fn)),ii), zero(2))
        check(f"ordered loop n={n}: shear conjugation", fn,
              mul(shear,mul(mat([[0,1],[1,n]]),shear_inverse)))
        check(f"ordered loop n={n}: preserves alternating form", gram(loop,omega), omega)
        check(f"ordered loop n={n}: det F is negative one", minor2(fn,(0,1),(0,1)), F(-1))
    h_one = mat([[2,1],[1,1]])
    t_one, l_one = lector(h_one)
    check("ordered loop n=1: visible oriented coefficient", gram(t_one,omega), times(F(89,81),omega))
    check("ordered loop n=1: memory oriented coefficient", times(8,gram(l_one,omega)), times(F(-8,81),omega))
    check("ordered loop n=1: exact oriented balance", plus(gram(t_one,omega),times(8,gram(l_one,omega))), omega)

    # Actual weighted Cauchy-Binet calculation of bivector sectors.
    embedding = tuple(t) + tuple(ell)
    weighted = tuple(tuple(g2[r][j] if j < 2 else 0 for j in range(4))
                     for r in range(2)) + tuple(
        tuple(0 if j < 2 else 8*g2[r][j-2] for j in range(4)) for r in range(2))
    pairs = list(combinations(range(4), 2))
    minors = {pair: minor2(embedding, pair, (0,1)) for pair in pairs}
    input_area2 = minor2(g2, (0,1), (0,1))
    sectors = {}
    for memory_degree in range(3):
        indices = [pair for pair in pairs if sum(i >= 2 for i in pair) == memory_degree]
        sectors[memory_degree] = sum(
            (minors[row] * minor2(weighted, row, col) * minors[col]
             for row in indices for col in indices), F(0)) / input_area2
    check("visible bivector", sectors[0], F(361,729))
    check("mixed bivector", sectors[1], F(304,729))
    check("memory bivector", sectors[2], F(64,729))
    check("bivector total", sum(sectors.values(), F(0)), F(1))
    for degree in range(25):
        weights = [F(comb(degree, j)) * a**(degree-j) * b**j
                   for j in range(degree+1)]
        check(f"binomial exterior weights degree {degree}", sum(weights, F(0)), F(1))
        condition(f"nonnegative exterior weights degree {degree}", all(x >= 0 for x in weights))

    print(json.dumps({
        "result": "PASS_EXACT_DIMENSIONAL_APPLICATION",
        "checks": COUNT,
        "arithmetic": "fractions.Fraction and exact pairs for Q(sqrt(5))",
        "K_total": 6263,
        "two_readers_sharp_mean_zero_gram": "16/81",
        "third_S3_sharp_mean_zero_gram": "8/27",
        "Coxeter_first_complement_gram": "8/27",
        "Coxeter_two_complements_gram": "368/729",
        "source_vector_visible_memory_norms_squared": ["38", "16"],
        "ordered_loop_integer_parameters": loop_parameters,
        "ordered_loop_n1_visible_memory_oriented_coefficients": ["89/81", "-8/81"],
        "bivector_visible_mixed_memory": ["361/729", "304/729", "64/729"],
        "variational_projection": variational_result,
        "scope": "finite rational identities, reconstruction, spectral projectors, A2 metric, weighted bivector sectors",
        "not_certified": "physical trajectory, Niemeier/Leech glue preservation, infinite limits, or global corpus"
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
