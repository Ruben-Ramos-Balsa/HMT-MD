#!/usr/bin/env python3
"""Controles focales exactos; no regeneran constantes ni certifican el corpus."""
from fractions import Fraction as F
import json


def ln_interval(x, terms=48):
    """Cotas racionales de ln(x), x>1, por la serie de atanh."""
    z = (x - 1) / (x + 1)
    assert 0 < z < 1
    lower = 2 * sum((z ** (2*k+1) / (2*k+1) for k in range(terms)), F(0))
    error = 2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
    return lower, lower+error


def floor_interval(lo, hi):
    a, b = lo.numerator//lo.denominator, hi.numerator//hi.denominator
    assert a == b, "La precisión del intervalo no decide este índice."
    return a


def clock_checks(count=2000):
    assert 10**146 > 9**153
    assert 10**417 < 9**437
    l, u = ln_interval(F(10, 9))
    l2, u2 = ln_interval(F(2))
    l54, u54 = ln_interval(F(5, 4))
    dl, du = l/(3*u2+u54), u/(3*l2+l54)
    bl, bu = 22-1/dl, 22-1/du
    assert F(1, 7) < bl < bu < F(3, 20)

    def q(k):
        return floor_interval(F(k)/bu, F(k)/bl)

    def p(j):
        return floor_interval(F(j)/du, F(j)/dl)

    outcomes = {}
    examples = []
    for k in range(1, count+1):
        start, stop = q(k), q(k+3)
        m = stop-start
        short = sum(22-(p(j+1)-p(j)) for j in range(start, stop))
        dp = p(stop)-p(start)
        dv = dp-m
        assert m in (20, 21) and short == 3
        assert dp == 22*m-3 and dv == 21*m-3
        assert dv % 3 == 0 and dv % 9 in (3, 6)
        selector = (1, -1, 0)
        assert selector[(p(start)-start) % 3] == selector[(p(stop)-stop) % 3]
        outcomes[str(m)] = outcomes.get(str(m), 0)+1
        if k in (1, 5):
            examples.append(dict(k=k, start=start, stop=stop, intervals=m,
                                 blocks=dp, capacity=dv, phase_shift=dv % 9))
    assert set(outcomes) == {'20', '21'}
    return dict(windows=count, exact_integer_bounds=True,
                floor_indices_certified_by_rational_intervals=True,
                outcomes=outcomes, examples=examples)


I = ((F(1), F(0)), (F(0), F(1)))


def add(a, b):
    return tuple(tuple(a[i][j]+b[i][j] for j in range(2)) for i in range(2))


def scale(c, a):
    return tuple(tuple(c*x for x in row) for row in a)


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(2)), F(0))
                       for j in range(2)) for i in range(2))


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def operator_checks():
    # Matrices de contraste en SL(2,Q), no trayectorias físicas seleccionadas.
    fixtures = [((F(1), F(a)), (F(b), F(1+a*b)))
                for a in range(-2, 3) for b in range(-2, 3)]
    cases = 0
    for n in (2, 3, 5, 9):
        for c1 in fixtures:
            for c2 in fixtures:
                t1 = scale(F(1, n), add(scale(n-1, I), c1))
                t2 = scale(F(1, n), add(scale(n-1, I), c2))
                e1, e2 = sub(c1, I), sub(c2, I)
                # D2D1=(n-1)/n² (C2-I)(C1-I): sin redondear sqrt(n-1).
                memory21 = scale(F(n-1, n*n), mul(e2, e1))
                memory12 = scale(F(n-1, n*n), mul(e1, e2))
                intrinsic = comm(c2, c1)
                direct = comm(t2, t1)
                memory = sub(memory21, memory12)
                assert direct == scale(F(1, n*n), intrinsic)
                assert memory == scale(F(n-1, n*n), intrinsic)
                assert add(direct, memory) == scale(F(1, n), intrinsic)
                assert add(mul(t2, t1), memory21) == scale(
                    F(1, n), add(scale(n-1, I), mul(c2, c1)))
                cases += 1
    return dict(matrix_pairs_and_dimensions=cases,
                dimensions=[2, 3, 5, 9], arithmetic='Fraction',
                physical_trajectory_claim=False)


def reciprocity_checks():
    count = 0
    def eta_normalized(eps, q):
        return 500*eps*(1-q)/(1+q)-1
    for a in range(1, 41):
        for b in range(1, 41):
            q = F(a, b)
            for eps in (-1, 1):
                v = eta_normalized(eps, q)
                assert v == eta_normalized(-eps, 1/q)
                assert eta_normalized(eps, 1/q) == -v-2
                xi = eps*(1-q)/(1+q)
                assert xi == (v+1)/500
                assert F(1) - eps*xi > 0 and F(1) + eps*xi > 0
                assert (1-eps*xi)/(1+eps*xi) == q
                assert (v > 0) == (eps*(1-q)/(1+q) > F(1, 500))
                count += 1
    assert F(9, 16) == F(9, 4**2)
    assert F(5, 9) == F(5, 9)
    assert F(7, 48) == F(14, 2*4*12)
    assert F(1, 54) == F(1944, 104976)
    return dict(oriented_rational_charts=count,
                coefficients_checked_as_identities=True,
                coefficient_assignment_derived_by_this_test=False)


if __name__ == '__main__':
    print(json.dumps(dict(
        status='PASS_COMPROBACIONES_FOCALES_REORIENTACION',
        scope='Controles adicionales a las pruebas escritas; no certificación integral.',
        clocks=clock_checks(), operators=operator_checks(),
        reciprocity=reciprocity_checks()), ensure_ascii=False, indent=2))
