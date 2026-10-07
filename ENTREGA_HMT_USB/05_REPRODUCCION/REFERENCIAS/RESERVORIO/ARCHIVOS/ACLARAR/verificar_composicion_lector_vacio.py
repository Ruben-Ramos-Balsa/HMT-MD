#!/usr/bin/env python3
"""Control racional de una ley posterior del lector, sin valores objetivo.

No genera constantes primarias ni prueba cierre de la imagen de semillas.
Las raíces racionales son casos algebraicos; no se atribuyen a estados físicos.
"""
from fractions import Fraction as Q
from itertools import product
import json


def F(s):
    assert s > 0
    return (1+s+s*s)/(1+s+s*s+s**3)


def polynomial(r, s):
    return r*s**3+(r-1)*(s*s+s+1)


def root_interval(r, steps=70):
    if not 0 < r < 1:
        raise ValueError("Coordenada fuera del dominio extendido")
    hi = Q(1)
    while F(hi) > r:
        hi *= 2
    if F(hi) == r:
        return hi, hi
    lo = Q(0)
    for _ in range(steps):
        mid = (lo+hi)/2
        if F(mid) == r:
            return mid, mid
        if F(mid) > r:
            lo = mid
        else:
            hi = mid
    return lo, hi


def composition_interval(r, t):
    a, b = root_interval(r)
    c, d = root_interval(t)
    # Lo > 0 para los casos de esta comprobación; F es decreciente.
    assert a*c > 0
    return F(b*d), F(a*c)


def multiply(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def transpose(A):
    return tuple(zip(*A))


def channels(a, b):
    return (((a+b)/2, (a-b)/2), ((a-b)/2, (a+b)/2))


def main():
    roots = (Q(1,4), Q(1,2), Q(2,3), Q(1), Q(3,2), Q(2), Q(4))
    unit = Q(3,4)
    pair_checks = 0
    for s, t in product(roots, repeat=2):
        r, u, result = F(s), F(t), F(s*t)
        assert polynomial(r, s) == polynomial(u, t) == 0
        assert polynomial(result, s*t) == 0
        lo, hi = composition_interval(r, u)
        assert lo <= result <= hi
        assert result == F(t*s)
        if s <= 1 and t <= 1:
            assert unit <= result < 1
            assert result >= max(r, u)
        pair_checks += 1
    for s, t, u in product(roots, repeat=3):
        assert F((s*t)*u) == F(s*(t*u))
    for s in roots:
        assert F(s*1) == F(s)
        assert F(1/s) == s*F(s)
        assert F(s*(1/s)) == unit
        a, b = root_interval(F(s))
        assert a <= s <= b

    ordinary = F(Q(1,2))**2
    induced = F(Q(1,4))
    assert ordinary == Q(196,225) and induced == Q(84,85)
    assert ordinary != induced

    L = ((Q(1), Q(0)), (Q(0), Q(-1)))
    q1, q2 = (Q(1,2), Q(2,3)), (Q(3,4), Q(1,3))
    T1, T2 = channels(*q1), channels(*q2)
    T12 = channels(q1[0]*q2[0], q1[1]*q2[1])
    assert multiply(T1,T2) == T12 == multiply(T2,T1)
    assert multiply(multiply(L,T1), L) == channels(q1[1], q1[0])
    spectra1 = tuple(F(q**30) for q in q1)
    spectra2 = tuple(F(q**30) for q in q2)
    correct = tuple(F((a*b)**30) for a,b in zip(q1,q2))
    assert tuple(a*b for a,b in zip(spectra1,spectra2)) != correct

    A = ((Q(1,2), Q(0)), (Q(0), Q(1,3)))
    B = ((Q(1,2), Q(1,6)), (Q(1,6), Q(1,2)))
    AB = multiply(A,B)
    assert AB != transpose(AB) and AB != multiply(B,A)
    rejected = 0
    for bad in (Q(-1), Q(0), Q(1), Q(2)):
        try:
            root_interval(bad)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Se aceptó una coordenada inadmisible")
    print(json.dumps({
        "status": "PASS_LOCAL_VACUUM_READER_COMPOSITION",
        "rational_roots": len(roots),
        "pair_composition_checks": pair_checks,
        "associativity_cases": len(roots)**3,
        "identity_and_extended_inverse_cases": len(roots),
        "coordinate_interval_inversion": True,
        "two_channel_operator_composition": True,
        "orientation_conjugation": True,
        "ordinary_product_counterexample": {"induced": str(induced), "ordinary": str(ordinary)},
        "noncommuting_product_not_selfadjoint": True,
        "invalid_coordinates_rejected": rejected,
        "primary_generation_tested": False,
        "seed_image_closure_tested": False,
        "physical_states_attributed_to_fixtures": False,
        "target_constants_used": False
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
