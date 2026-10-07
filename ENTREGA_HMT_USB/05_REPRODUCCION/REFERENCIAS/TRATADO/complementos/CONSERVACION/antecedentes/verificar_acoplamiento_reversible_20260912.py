#!/usr/bin/env python3
"""Exact checks of reversible coupling and nonstationary memory balance.

The test matrices are declared algebraic examples, not selected HMT trajectories.
All arithmetic uses fractions. Checks remain active under python -O.
No publication, receipt, or global gate is modified by this script.

Coordinates are (v,z), with z=m/sqrt(8), and metric diag(G,8G).
The same identities apply to the alternating form diag(Omega,8Omega).
"""

from fractions import Fraction as Q
import json


CHECKS = 0


def matrix(rows):
    return tuple(tuple(Q(x) for x in row) for row in rows)


def identity(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def zero(n, m=None):
    return matrix([[0] * (n if m is None else m) for _ in range(n)])


def transpose(a):
    return tuple(zip(*a))


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br))
                 for ar, br in zip(a, b))


def scale(c, a):
    c = Q(c)
    return tuple(tuple(c * x for x in row) for row in a)


def subtract(a, b):
    return add(a, scale(-1, b))


def multiply(a, b):
    bt = transpose(b)
    return tuple(tuple(sum((x * y for x, y in zip(row, col)), Q(0))
                       for col in bt) for row in a)


def inverse(a):
    n = len(a)
    rows = [list(a[i]) + list(identity(n)[i]) for i in range(n)]
    for k in range(n):
        pivot = next((i for i in range(k, n) if rows[i][k]), None)
        if pivot is None:
            raise ArithmeticError("Singular matrix in exact inverse")
        rows[k], rows[pivot] = rows[pivot], rows[k]
        denominator = rows[k][k]
        rows[k] = [x / denominator for x in rows[k]]
        for i in range(n):
            if i != k:
                coefficient = rows[i][k]
                rows[i] = [x - coefficient * y
                           for x, y in zip(rows[i], rows[k])]
    return tuple(tuple(row[n:]) for row in rows)


def blocks(a, b, c, d):
    return tuple(tuple(ar) + tuple(br) for ar, br in zip(a, b)) + tuple(
        tuple(cr) + tuple(dr) for cr, dr in zip(c, d))


def block(a, row, col, n=2):
    return tuple(tuple(a[i][j] for j in range(col * n, (col + 1) * n))
                 for i in range(row * n, (row + 1) * n))


def pullback(operator, form):
    return multiply(transpose(operator), multiply(form, operator))


def weighted_form(form):
    z = zero(len(form))
    return blocks(form, z, z, scale(8, form))


def coupling(b, c):
    t = scale(Q(1, 9), add(scale(8, b), c))
    ell = scale(Q(1, 9), subtract(c, b))
    r = scale(Q(1, 9), add(b, scale(8, c)))
    return blocks(t, scale(8, ell), ell, r), t, ell, r


def check_equal(name, actual, expected):
    global CHECKS
    if actual != expected:
        raise AssertionError(f"{name}\nactual={actual}\nexpected={expected}")
    CHECKS += 1


def check_different(name, actual, forbidden):
    global CHECKS
    if actual == forbidden:
        raise AssertionError(f"{name}: negative control did not discriminate")
    CHECKS += 1


def check_condition(name, condition):
    global CHECKS
    if not condition:
        raise AssertionError(name)
    CHECKS += 1


def verify_local(name, b, c, source, target):
    """Check hypotheses and the rational reversible coupling."""
    check_equal(name + ": B preserves form", pullback(b, target), source)
    check_equal(name + ": C preserves form", pullback(c, target), source)
    u, t, ell, r = coupling(b, c)
    check_equal(name + ": augmented form",
                pullback(u, weighted_form(target)), weighted_form(source))
    check_equal(name + ": compressed balance",
                add(pullback(t, target), scale(8, pullback(ell, target))),
                source)
    ui = coupling(inverse(b), inverse(c))[0]
    check_equal(name + ": explicit inverse", ui, inverse(u))
    check_equal(name + ": inverse left", multiply(ui, u), identity(4))
    check_equal(name + ": inverse right", multiply(u, ui), identity(4))
    return u, t, ell, r


def run():
    i = identity(2)
    omega = matrix([[0, 1], [-1, 0]])
    coxeter = matrix([[0, -1], [1, -1]])
    threshold = matrix([[1, 1], [0, 1]])
    fav2 = matrix([[1, 1], [1, 2]])
    a2_form = matrix([[2, -1], [-1, 2]])
    quarter_turn = matrix([[0, -1], [1, 0]])
    reflection_x = matrix([[-1, 0], [0, 1]])
    swap = matrix([[0, 1], [1, 0]])
    minus_i = scale(-1, i)

    # Each regime has its own declared representation; Omega is the common
    # alternating form. Positive forms are tested only where actually invariant.
    for name, e in (("Coxeter", coxeter),
                    ("threshold", threshold), ("Fav2", fav2)):
        verify_local(name + " alternating", i, e, omega, omega)
    verify_local("Coxeter positive A2", i, coxeter, a2_form, a2_form)
    for name, e in (("quarter turn", quarter_turn),
                    ("reflection", reflection_x), ("swap", swap)):
        verify_local(name + " Euclidean", i, e, i, i)

    # Variable symplectic coordinate frames, retaining the baseline B.
    frames = [matrix([[a, 0], [0, Q(1, a)]]) for a in (1, 2, 3, 5)]
    for k, (name, e) in enumerate(
            (("Coxeter", coxeter), ("threshold", threshold), ("Fav2", fav2))):
        m0, m1 = frames[k], frames[k + 1]
        b = multiply(m1, inverse(m0))
        c = multiply(m1, multiply(e, inverse(m0)))
        verify_local(name + " variable alternating", b, c, omega, omega)

    positive_cases = (("Coxeter", coxeter, a2_form),
                      ("quarter turn", quarter_turn, i))
    for name, e, base_form in positive_cases:
        m0, m1 = frames[1], frames[2]
        g0 = pullback(inverse(m0), base_form)
        g1 = pullback(inverse(m1), base_form)
        b = multiply(m1, inverse(m0))
        c = multiply(m1, multiply(e, inverse(m0)))
        verify_local(name + " variable positive", b, c, g0, g1)
        wrong_u = coupling(i, c)[0]
        check_different(name + ": omitting baseline is detected",
                        pullback(wrong_u, weighted_form(g1)),
                        weighted_form(g0))

    # Ordered composition: no commutation assumption on the two branches.
    b1, b2 = threshold, fav2
    c1, c2 = coxeter, threshold
    u1, t1, l1, _ = coupling(b1, c1)
    u2, t2, l2, _ = coupling(b2, c2)
    ordered = multiply(u2, u1)
    expected = coupling(multiply(b2, b1), multiply(c2, c1))[0]
    check_equal("ordered composition", ordered, expected)
    check_different("composition really noncommutative",
                    ordered, multiply(u1, u2))
    check_equal("composed alternating form",
                pullback(ordered, weighted_form(omega)), weighted_form(omega))
    check_equal("inverse of ordered product",
                inverse(ordered), multiply(inverse(u1), inverse(u2)))
    reinjected = add(multiply(t2, t1), scale(8, multiply(l2, l1)))
    check_equal("visible reinjection", block(ordered, 0, 0), reinjected)
    check_different("reinjection is nonzero", multiply(l2, l1), zero(2))
    check_different("omitted reentry detected", block(ordered, 0, 0),
                    multiply(t2, t1))

    # Distinct protocols: two reversible steps keep their memory coupled;
    # repeated compression archives each new memory as a separate component.
    u, t, ell, _ = coupling(i, minus_i)
    check_equal("stationary two-step reversible return",
                multiply(u, u), identity(4))
    check_equal("stationary reset visible after two steps",
                multiply(t, t), scale(Q(49, 81), i))
    check_different("reset versus reinjection",
                    block(multiply(u, u), 0, 0), multiply(t, t))

    # Exact nonstationary terminal: C_0=-I and C_n=I for every n>=1.
    terminal = pullback(t, i)
    memory = scale(8, pullback(ell, i))
    check_equal("variable terminal 49/81", terminal, scale(Q(49, 81), i))
    check_equal("variable memory 32/81", memory, scale(Q(32, 81), i))
    check_equal("variable full balance", add(terminal, memory), i)
    check_different("terminal is not a projection",
                    multiply(terminal, terminal), terminal)
    check_equal("all future steps are identity", coupling(i, i)[0], identity(4))
    check_equal("one later constant-minus-I step differs",
                scale(Q(49, 81), terminal), scale(Q(2401, 6561), i))
    check_different("constant versus variable terminal",
                    scale(Q(49, 81), terminal), terminal)

    # Noncommuting orthogonal sequence: exact finite Gram telescoping.
    sequence = [reflection_x, swap, quarter_turn, minus_i,
                transpose(quarter_turn), reflection_x, swap]
    check_different("test sequence noncommutes",
                    multiply(sequence[1], sequence[0]),
                    multiply(sequence[0], sequence[1]))
    p = i
    accumulated = zero(2)
    for n, c in enumerate(sequence):
        _, tn, ln, _ = coupling(i, c)
        check_equal(f"sequence {n}: orthogonal", pullback(c, i), i)
        old_a = pullback(p, i)
        bn = multiply(ln, p)
        gram = scale(8, pullback(bn, i))
        p = multiply(tn, p)
        new_a = pullback(p, i)
        accumulated = add(accumulated, gram)
        check_equal(f"sequence {n}: Gram difference",
                    subtract(old_a, new_a), gram)
        check_equal(f"sequence {n}: telescoping",
                    add(new_a, accumulated), i)
        # For a symmetric 2x2 rational matrix these principal minors certify PSD.
        check_equal(f"sequence {n}: symmetric loss", transpose(gram), gram)
        check_condition(f"sequence {n}: positive semidefinite loss",
                        gram[0][0] >= 0 and gram[1][1] >= 0
                        and gram[0][0] * gram[1][1]
                        - gram[0][1] * gram[1][0] >= 0)

    print(json.dumps({
        "result": "PASS_EXACT_REVERSIBLE_COUPLING",
        "checks": CHECKS,
        "arithmetic": "fractions.Fraction",
        "checks_survive_optimization": True,
        "scope": [
            "rational reversible coupling and inverse",
            "ordered noncommutative composition and memory reinjection",
            "variable positive and alternating forms",
            "three declared Euler matrix examples",
            "nonprojective terminal and finite nonstationary telescoping",
            "negative controls for omitted baseline and reentry"
        ],
        "not_certified": [
            "selection of any particular HMT trajectory",
            "infinite-dimensional limit theorem by finite computation",
            "physical realization or global corpus correctness"
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()

