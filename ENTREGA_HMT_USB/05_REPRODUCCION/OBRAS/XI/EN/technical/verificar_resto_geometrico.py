#!/usr/bin/env python3
"""Regresión algebraica del resto geométrico; no genera ninguna constante HMT."""
from fractions import Fraction as F

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def partial_tail(x, q, coefficient, depth):
    return coefficient * x**10 * sum(
        ((q * x**3)**n for n in range(depth + 1)), F(0)
    )

def full_tail(x, q, coefficient):
    return coefficient * x**10 / (1 - q * x**3)

def remainder(x, q, coefficient, depth):
    return coefficient * x**10 * (q*x**3)**(depth+1)/(1-q*x**3)

cases = 0
for x in (F(1,256), F(3,512), F(1,128)):
    for q in (F(1,729), F(1,81)):
        for coefficient in (F(-1,100000), F(-3,100000)):
            for depth in (0, 1, 2, 5, 10, 24):
                require(0 < q*x**3 < 1, "dominio")
                partial = partial_tail(x,q,coefficient,depth)
                full = full_tail(x,q,coefficient)
                rem = remainder(x,q,coefficient,depth)
                require(full-partial == rem, "identidad exacta del resto")
                require(rem < 0, "signo del resto")
                # Ejemplo racional de control, no dato ni generador de alfa:
                # se escoge un término constante para que x sea una raíz exacta.
                e9_at_x = -full
                e_infinite_at_x = e9_at_x + full
                e_partial_at_x = e9_at_x + partial
                require(e_infinite_at_x == 0, "raíz exacta del ejemplo")
                require(e_partial_at_x == -rem > 0, "truncamiento en raíz")
                require(not e_partial_at_x <= 0, "falsador del signo débil")
                require(partial - abs(rem) == full, "recuperación con resto")
                cases += 1
print("PASS_REGRESION_RESTO_GEOMETRICO casos=" + str(cases))
print("Scope: rational identity and sign falsifier; it neither proves the origin of K nor generates alpha.")
