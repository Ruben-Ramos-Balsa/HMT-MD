#!/usr/bin/env python3
"""Evaluaciones racionales posteriores al productor nativo de palabras.

Entradas: horizonte entero N, orden de Euler--Maclaurin p y longitud M de
la serie del logaritmo. No recibe cifras de constantes ni una tabla de primos.
No certifica la positividad de Weil ni el cierre global del Artículo VIII.
Todos los extremos y errores se calculan como fracciones exactas; el decimal
se publica al final mediante división entera dirigida.
"""
from __future__ import annotations

from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("native_words", Path(__file__).with_name("a9_native.py"))
NATIVE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NATIVE
SPEC.loader.exec_module(NATIVE)


def require_positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(name + " debe ser un entero positivo")


def factorial(n):
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def binomial(n, k):
    return factorial(n) // (factorial(k) * factorial(n-k))


def bernoulli(n):
    """Coeficientes de t/(exp(t)-1), con B1=-1/2, por recurrencia racional."""
    out = [F(1)]
    for m in range(1, n + 1):
        out.append(-sum((F(binomial(m+1, k))*out[k] for k in range(m)), F()) / (m+1))
    return out


def native_initial_segment(n):
    require_positive_integer(n, "N")
    word = ()
    for _ in range(n):
        word = NATIVE.add_words(word, (1,))
        yield word, NATIVE.word_value(word)


def log_ratio_interval(x, terms=120):
    """log(x), x racional positivo. Reducción exacta a [1,2), sin log externo."""
    require_positive_integer(terms, "M")
    x = F(x)
    if x <= 0:
        raise ValueError("El argumento del logaritmo debe ser positivo")
    if x < 1:
        lo, hi = log_ratio_interval(1/x, terms)
        return -hi, -lo

    def reduced(y):
        z = (y-1)/(y+1)
        total = 2*sum((z**(2*j+1)/(2*j+1) for j in range(terms)), F())
        error = 2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
        return total, total+error

    power = 0
    while x >= 2:
        x /= 2
        power += 1
    lo, hi = reduced(x)
    if power:
        lo2, hi2 = reduced(F(2))
        lo += power*lo2
        hi += power*hi2
    return lo, hi


def gamma_interval(n=81, order=8, log_terms=120):
    require_positive_integer(order, "p")
    numbers = [v for _, v in native_initial_segment(n)]
    harmonic = sum((F(1, v) for v in numbers), F())
    b = bernoulli(2*order)
    correction = sum((b[2*k]/(2*k*n**(2*k)) for k in range(1, order+1)), F())
    radius = abs(b[2*order])/(2*order*n**(2*order))
    loglo, loghi = log_ratio_interval(F(n), log_terms)
    centre_without_log = harmonic-F(1, 2*n)+correction
    return centre_without_log-loghi-radius, centre_without_log-loglo+radius


def rising(s, length):
    out = F(1)
    for j in range(length):
        out *= s+j
    return out


def zeta_positive_integer_interval(s=3, n=81, order=8):
    if type(s) is not int or s < 2:
        raise ValueError("La serie convergente requiere s entero >= 2")
    require_positive_integer(order, "p")
    numbers = [v for _, v in native_initial_segment(n)]
    partial = sum((F(1, v**s) for v in numbers), F())
    b = bernoulli(2*order)
    correction = sum((b[2*k]*rising(s, 2*k-1)/
                      (factorial(2*k)*n**(s+2*k-1))
                      for k in range(1, order+1)), F())
    centre = partial+F(1, (s-1)*n**(s-1))-F(1, 2*n**s)+correction
    radius = abs(b[2*order])*rising(s, 2*order-1)/(factorial(2*order)*n**(s+2*order-1))
    return centre-radius, centre+radius


def regularized_minus_one(n=81):
    """Evaluación de la continuación EM en s=-1, no suma ordinaria infinita."""
    numbers = [v for _, v in native_initial_segment(n)]
    b2 = bernoulli(2)[2]
    return sum(numbers)-F(n*n, 2)-F(n, 2)-b2/2


def decimal_bound(value, digits=42, upper=False):
    scale = 10**digits
    numerator = value.numerator*scale
    quotient = -((-numerator)//value.denominator) if upper else numerator//value.denominator
    sign = "-" if quotient < 0 else ""
    integer, tail = divmod(abs(quotient), scale)
    return f"{sign}{integer}.{tail:0{digits}d}"


def publish(interval):
    lo, hi = interval
    if not lo < hi:
        raise ArithmeticError("Intervalo no orientado")
    return {"lower": decimal_bound(lo), "upper": decimal_bound(hi, upper=True),
            "exact_width_numerator": str((hi-lo).numerator),
            "exact_width_denominator": str((hi-lo).denominator)}


def main():
    output = {
        "scope": "Rational interval evaluation after native integer publication; not a global HMT or RH certificate",
        "generator": "APP two-sheet native successor -> positive integer modes -> analytic functional",
        "inputs": {"N": 81, "Euler_Maclaurin_order": 8, "logarithm_terms": 120},
        "external_constant_targets_used": False,
        "Euler_Mascheroni": publish(gamma_interval()),
        "Apery": publish(zeta_positive_integer_interval()),
        "regularized_Z_minus_one": str(regularized_minus_one()),
        "bernoulli_even": [str(bernoulli(16)[2*k]) for k in range(1, 9)],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
