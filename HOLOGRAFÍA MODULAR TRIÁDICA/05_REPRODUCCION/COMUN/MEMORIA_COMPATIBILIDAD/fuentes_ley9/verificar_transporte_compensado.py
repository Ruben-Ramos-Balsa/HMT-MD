"""Controles racionales de una composición de realizaciones TRIT.

No genera constantes, no identifica esta composición con Gamma_9 y no
certifica una realización eléctrica. La identidad general se prueba en
DESARROLLO_TRANSPORTE_COMPENSADO.md; los casos finitos son controles.
Sólo biblioteca estándar; no modifica fuentes ni produce certificados globales.
"""
from fractions import Fraction as F
import json


I = ((F(1), F(0)), (F(0), F(1)))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a):
    d = det(a)
    return ((a[1][1]/d, -a[0][1]/d),
            (-a[1][0]/d, a[0][0]/d))


def trace(a):
    return a[0][0] + a[1][1]


def reduced_covariance(h):
    hh = mul(h, transpose(h))
    return tuple(tuple((8*I[i][j]+hh[i][j])/9 for j in range(2))
                 for i in range(2))


def golden_loop(n):
    return ((F(1+n), F(n*n)), (F(n), F(n*n-n+1)))


def comm(a, b):
    return mul(mul(mul(a, b), inv(a)), inv(b))


def rotation(t):
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    return ((c, s), (-s, c)), s


def boost(t):
    u, v = (1+t*t)/(1-t*t), 2*t/(1-t*t)
    return ((u, v), (v, u)), v


def matvec(a, v):
    return tuple(sum(a[i][j]*v[j] for j in range(2)) for i in range(2))


def transpose(a):
    return tuple(zip(*a))


def residual_energy(a, f):
    af = matvec(a, f)
    return sum((x-y)**2 for x, y in zip(f, af))


def main():
    count = 0
    for p in range(-6, 7):
        for q in range(-6, 7):
            r, s = rotation(F(p, 7))
            b, v = boost(F(q, 7))
            c = comm(r, b)
            assert det(c) == 1
            assert trace(c) == 2 + 4*s*s*v*v
            assert trace(mul(c, transpose(c))) - 2 == 16*s*s*v*v*(1+v*v)
            assert det(reduced_covariance(c)) == 1+F(128,81)*s*s*v*v*(1+v*v)
            assert comm(b, r) == inv(c)
            assert mul(mul(mul(r, b), inv(b)), inv(r)) == I
            if s*v:
                assert trace(c) > 2 and c != I
            else:
                assert c == I
            # Positividad y área de una covarianza explícita, sin unidades.
            sigma = ((F(2), F(1)), (F(1), F(3)))
            sigma1 = mul(mul(c, sigma), transpose(c))
            assert det(sigma1) == det(sigma)
            assert sigma1[0][0] > 0
            count += 1

    loop_count = 0
    for n in range(-30, 31):
        h = golden_loop(n)
        assert det(h) == 1
        ratio = det(reduced_covariance(h))
        assert ratio == 1+F(8,81)*n*n*(2*n*n-2*n+5)
        assert det(reduced_covariance(golden_loop(-n)))-ratio == F(32,81)*n**3
        loop_count += 1

    r, s = rotation(F(1, 2))  # cos=3/5, sin=4/5
    b, v = boost(F(1, 3))     # cosh=5/4, sinh=3/4
    c = comm(r, b)
    f = (F(1), F(1))
    output = {
        "status": "CONTROLES_ALGEBRAICOS_LOCALES_CORRECTOS",
        "rational_cases": count,
        "integer_loop_cases": loop_count,
        "example_C": [[str(x) for x in row] for row in c],
        "example_trace": str(trace(c)),
        "example_determinant": str(det(c)),
        "example_reduced_covariance_determinant_ratio": str(det(reduced_covariance(c))),
        "golden_loop_plus_1_ratio": str(det(reduced_covariance(golden_loop(1)))),
        "golden_loop_minus_1_ratio": str(det(reduced_covariance(golden_loop(-1)))),
        "example_residual_f_1_1_W_identity": str(residual_energy(c, f)),
        "example_true_retrace_residual": str(residual_energy(I, f)),
        "scope": "Realizaciones matriciales TRIT; sin certificacion de ruta TPK ni de dispositivo fisico",
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
