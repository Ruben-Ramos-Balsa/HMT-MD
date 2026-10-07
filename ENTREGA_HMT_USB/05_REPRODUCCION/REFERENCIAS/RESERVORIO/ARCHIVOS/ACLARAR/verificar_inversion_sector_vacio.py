#!/usr/bin/env python3
"""Control racional del lector inverso de V_90,120.

No genera las constantes primarias, no calibra una carta SI y no usa sus
decimales como entradas. Las parejas racionales son casos algebraicos de
prueba del lector, no estados fisicos atribuidos a las semillas HMT.
"""

from fractions import Fraction as Q
from itertools import combinations
from math import gcd, isqrt
import json


def trit_phase(tick):
    phase = 1 + (tick - 1) % 9
    return 1 if phase in (1, 4, 7) else -1 if phase in (2, 5, 8) else 0


def incidence_exponents():
    calendar = tuple(range(1, 10))
    active = tuple(t for t in calendar if trit_phase(t) != 0)
    before_return = calendar[:-1]
    pairs = tuple(combinations(active, 2))
    f6 = {(t, p) for t in active for p in pairs}
    f8 = {(t, p) for t in before_return for p in pairs}
    return len(f6), len(f8)


def sector(q, exponents):
    a, b = exponents
    return (1 - q**a) / (1 - q**b)


def reduced_sector(s):
    return (1 + s + s*s) / (1 + s + s*s + s**3)


def cubic(r, s):
    return r*s**3 + (r - 1)*(1 + s + s*s)


def isolate_s(r, steps=80):
    if not Q(3, 4) < r < 1:
        raise ValueError("sector fuera del dominio abierto")
    lo, hi = Q(0), Q(1)
    for _ in range(steps):
        mid = (lo + hi) / 2
        # F es estrictamente decreciente en (0,1).
        if reduced_sector(mid) > r:
            lo = mid
        else:
            hi = mid
    return lo, hi


def exact_positive_sqrt(x):
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    if a*a != x.numerator or b*b != x.denominator:
        raise ValueError("el caso de control no posee raiz racional")
    return Q(a, b)


def admissible_coordinates(z, c):
    return z > 0 and c > 0 and 1 < z*c < Q(16, 9) and Q(9, 16) < z/c < 1


def main():
    exponents = incidence_exponents()
    divisor = gcd(*exponents)
    assert exponents == (90, 120)
    assert tuple(n // divisor for n in exponents) == (3, 4)
    fixtures = tuple(combinations((Q(1, 4), Q(1, 3), Q(1, 2), Q(2, 3), Q(3, 4)), 2))
    for qp, qm in fixtures:
        rp, rm = sector(qp, exponents), sector(qm, exponents)
        mu, eps = rm*rm, rp*rp
        z, c = rm/rp, 1/(rp*rm)
        assert admissible_coordinates(z, c)
        assert mu*eps == 1/(c*c)
        assert mu/eps == z*z
        rp_back = exact_positive_sqrt(1/(z*c))
        rm_back = exact_positive_sqrt(z/c)
        assert (rp_back, rm_back) == (rp, rm)
        for q, r in ((qp, rp_back), (qm, rm_back)):
            s = q**divisor
            assert reduced_sector(s) == r
            assert cubic(r, s) == 0
            lo, hi = isolate_s(r)
            assert lo <= s <= hi
            assert hi - lo == Q(1, 2**80)
        # El intercambio de hojas conserva c e invierte z.
        assert 1/(rm*rp) == c
        assert rp/rm == 1/z
        assert admissible_coordinates(1/z, c)
    rejected = 0
    for bad in (Q(0), Q(3, 4), Q(1), Q(2)):
        try:
            isolate_s(bad)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("se acepto un sector no admisible")
    outside_coordinates = (
        (Q(1), Q(1)), (Q(1), Q(16, 9)),
        (Q(0), Q(4, 3)), (Q(-1), Q(4, 3)),
        (Q(2), Q(4, 3)), (Q(1, 2), Q(4, 3)),
    )
    assert not any(admissible_coordinates(z, c) for z, c in outside_coordinates)
    print(json.dumps({
        "status": "PASS_LOCAL_RATIONAL_VACUUM_SECTOR_INVERSION",
        "incidence_exponents": exponents,
        "common_exponent": divisor,
        "reduced_exponents": [3, 4],
        "rational_channel_pairs": len(fixtures),
        "exact_cubic_roots_checked": 2*len(fixtures),
        "rational_bracket_width": "2^-80",
        "inadmissible_sectors_rejected": rejected,
        "coordinate_domain_checks": 2*len(fixtures),
        "outside_coordinate_pairs_rejected": len(outside_coordinates),
        "scope": "Inversion del lector espectral, no generacion primaria ni reconstruccion de todo el estado con memoria",
        "target_constants_used": False,
        "original_sources_modified": False
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
