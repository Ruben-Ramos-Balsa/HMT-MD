#!/usr/bin/env python3
"""Controles finitos exactos del añadido reticular y modular de Moonshine.

No demuestra los teoremas infinitos de VOA, orbifold o modularidad.
Comprueba sus datos reticulares construidos y prefijos formales, sin entradas
metrológicas ni valores objetivo en las operaciones generadoras.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb

B = ((2, -1), (-1, 2))
C = ((0, -1), (1, -1))
R = ((0, 1), (1, 0))
I = ((1, 0), (0, 1))
AW = (
    (0, 1, 1, 1, 1, 1), (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2), (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1), (1, 1, 2, 2, 1, 0),
)
checks = []


def verify(name, predicate):
    if not predicate:
        raise AssertionError(name)
    checks.append(name)


def mm(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def transpose(a):
    return tuple(zip(*a))


def mv(a, v):
    return tuple(sum(x*y for x, y in zip(row, v)) for row in a)


def inner(a, b):
    return sum(x*y for x, y in zip(a, mv(B, b)))


def disc(x):
    omega = (Q(2, 3), Q(1, 3))
    candidates = [k for k in range(3)
                  if all((z-k*w).denominator == 1 for z, w in zip(x, omega))]
    if len(candidates) != 1:
        raise AssertionError(("clase discriminante", x, candidates))
    return candidates[0]


Cinv = mm(C, C)
verify("C^3=I", mm(Cinv, C) == I)
verify("C^2+C+I=0", all(Cinv[i][j]+C[i][j]+I[i][j] == 0
                           for i in range(2) for j in range(2)))
verify("C isometrico", mm(mm(transpose(C), B), C) == B)
verify("R isometrico", mm(mm(transpose(R), B), R) == B)
verify("RCR=C^-1", mm(mm(R, C), R) == Cinv)
omega = (Q(2, 3), Q(1, 3))
verify("C fija discriminante", disc(mv(C, omega)) == 1)
verify("C^-1 fija discriminante", disc(mv(Cinv, omega)) == 1)
verify("R invierte discriminante", disc(mv(R, omega)) == 2)
verify("AW^2=-I modulo3", all(mm(AW, AW)[i][j] % 3 == (2 if i == j else 0)
                               for i in range(6) for j in range(6)))
words = {tuple(w)+tuple(sum(w[i]*AW[i][j] for i in range(6)) % 3
                         for j in range(6))
         for w in product(range(3), repeat=6)}
full = sorted(w for w in words if all(w))
cstar = (1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1)
verify("729 palabras", len(words) == 729)
verify("24 orientaciones completas", len(full) == 24)
verify("c* y -c* en codigo", cstar in words and tuple(-x % 3 for x in cstar) in words)

# Para cada orientación de soporte completo y cada punto marcado posible,
# se comprueban las dos congruencias que aseguran gN0=N0 y g(v/3)=v/3+y.
neighbor_ok = True
for c in full:
    for marked in range(12):
        ys, zs, ipy, ipz, norm = [], [], Q(0), Q(0), Q(0)
        for b, cb in enumerate(c):
            a = 4 if b == marked else 1
            v = (Q(a), Q(a))
            g = Cinv if cb == 1 else C
            gi = C if cb == 1 else Cinv
            y = tuple((x-z)/3 for x, z in zip(mv(g, v), v))
            z = tuple((x-vv)/3 for x, vv in zip(mv(gi, v), v))
            ys.append(disc(y)); zs.append(disc(z))
            ipy += inner(y, v); ipz += inner(z, v); norm += inner(v, v)
        neighbor_ok &= (tuple(ys) == c and tuple(zs) == tuple(-x % 3 for x in c)
                        and tuple(ys) in words and tuple(zs) in words
                        and ipy == ipz == -27 and norm == 54)
verify("vecino:24orientaciones*12marcas", neighbor_ok)

# Series truncadas en Z[[q]]: sólo se descartan monomios de grado superior.
N = 14


def mul(a, b):
    return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(N+1)]


def shift(a, d):
    return [0]*d+a[:N+1-d]


def inv(a):
    assert a[0] == 1
    b = [1]+[0]*N
    for i in range(1, N+1):
        b[i] = -sum(a[j]*b[i-j] for j in range(1, i+1))
    return b


def linear(*terms):
    return [sum(coef*a[i] for coef, a in terms) for i in range(N+1)]


one = [1]+[0]*N
a2 = one[:]
a3 = one[:]
for n in range(1, N+1):
    f2, numerator3, denominator3 = [0]*(N+1), [0]*(N+1), [0]*(N+1)
    for k in range(N//n+1):
        f2[k*n] = (-1)**k*comb(23+k, k)
        numerator3[k*n] = (-1)**k*comb(12, k) if k <= 12 else 0
    for k in range(N//(3*n)+1):
        denominator3[k*3*n] = comb(11+k, k)
    a2 = mul(a2, f2)
    a3 = mul(a3, mul(numerator3, denominator3))

verify("producto t2 prefijo", a2[:6] == [1, -24, 276, -2048, 11202, -49152])
verify("producto t3 prefijo", a3[:6] == [1, -12, 54, -76, -243, 1188])
u2, u3 = inv(a2), inv(a3)
verify("inversion formal2", mul(a2, u2) == one)
verify("inversion formal3", mul(a3, u3) == one)
qj2 = linear((1, a2), (768, shift(one, 1)),
             (196608, shift(u2, 2)), (16777216, shift(mul(u2, u2), 3)))
qj3 = linear((1, a3), (756, shift(one, 1)),
             (10*3**9, shift(u3, 2)), (4*3**14, shift(mul(u3, u3), 3)),
             (3**18, shift(mul(mul(u3, u3), u3), 4)))
verify("uniformizaciones:14 grados", qj2 == qj3)
verify("prefijo j", qj2[:5] == [1, 744, 196884, 21493760, 864299970])
qT2A = linear((1, a2), (24, shift(one, 1)), (4096, shift(u2, 2)))
verify("prefijo T2A", qT2A[:5] == [1, 0, 4372, 96256, 1240002])
verify("valuacion eta nivel3", Q(1, 24)-Q(3, 24) == -Q(1, 12))
verify("valuacion traza ternaria", 12*(Q(1, 24)-Q(3, 24)) == -1)

print("PASS_DATOS_FINITOS_MOONSHINE", len(checks))
print("24 orientaciones completas; 12 marcas; dos desplazamientos exactos")
print("Series: 14 grados; los teoremas infinitos conservan sus referencias primarias")
