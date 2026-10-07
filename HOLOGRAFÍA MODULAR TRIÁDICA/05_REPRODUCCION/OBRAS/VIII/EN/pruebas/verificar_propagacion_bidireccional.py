#!/usr/bin/env python3
"""Identidades finitas de rutas, Green cronológicos y absorción de borde.

Biblioteca estándar y Fraction. No escribe archivos. No identifica el canal
cronológico con una teoría de campos tetradimensional ni fija amplitud física.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json


counts = {}


def require(condition, group, detail):
    counts[group] = counts.get(group, 0) + 1
    if not condition:
        raise ValueError(group + ": " + detail)


def mat(rows):
    return tuple(tuple(Q(x) for x in row) for row in rows)


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def zero(n, m):
    return mat([[0] * m for _ in range(n)])


def tr(a):
    return tuple(zip(*a))


def add(*items):
    return tuple(tuple(sum(a[i][j] for a in items) for j in range(len(items[0][0])))
                 for i in range(len(items[0])))


def scale(q, a):
    return tuple(tuple(q * x for x in row) for row in a)


def mul(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in tr(b))
                 for row in a)


def inv2(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if determinant == 0:
        raise ValueError("Matriz singular")
    return scale(1 / determinant,
                 mat([[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]]))


def dot(a, b):
    return mul(tr(a), b)[0][0]


def route_checks():
    group = "accion_de_rutas"
    alphabet = tuple(product(range(4), range(2)))

    def counts_of(word):
        return (sum(a[0] != b[0] for a, b in zip(word, word[1:])),
                sum(a[1] != b[1] for a, b in zip(word, word[1:])))

    def c(word):
        return tuple((d, 1 - leaf) for d, leaf in word)

    def p(word):
        return tuple((-d % 4, leaf) for d, leaf in word)

    def t(word):
        return tuple(((d + 2) % 4, leaf) for d, leaf in reversed(word))

    for n in range(4):
        for word in product(alphabet, repeat=n):
            original = counts_of(word)
            for transform in (c, p, t, lambda w: c(p(t(w)))):
                changed = transform(word)
                require(counts_of(changed) == original, group, "recuentos invariantes")
            for transform in (c, p, t):
                require(transform(transform(word)) == word, group, "involución")


I2 = eye(2)
J2 = mat([[0, -1], [1, 0]])
C0 = mat([[1, 0], [0, -1]])


def step(n):
    return J2 if n % 3 == 0 else (scale(-1, I2) if n % 3 == 1 else I2)


@lru_cache(maxsize=None)
def transport(n, k):
    if n < k:
        return tr(transport(k, n))
    result = I2
    for index in range(k, n):
        result = mul(step(index), result)
    return result


def involution(n):
    return mul(mul(transport(-n, 0), C0), transport(0, n))


def kernel(n, k, advanced=False):
    coefficient = max(k - n, 0) if advanced else max(n - k, 0)
    return scale(coefficient, transport(n, k))


def value(section, n):
    return section.get(n, zero(2, 1))


def difference(section, n):
    return add(value(section, n + 1), scale(-1, mul(step(n), value(section, n))))


def kinetic(section, n):
    return add(mul(tr(step(n)), value(section, n + 1)),
               scale(-2, value(section, n)),
               mul(step(n - 1), value(section, n - 1)))


def green(source, n, advanced=False):
    return add(zero(2, 1), *(mul(kernel(n, k, advanced), j) for k, j in source.items()))


def transport_and_green_checks():
    group = "transporte_y_green"
    for n, k, l in product(range(-3, 4), repeat=3):
        require(mul(transport(n, k), transport(k, l)) == transport(n, l),
                group, "composición")
    for n in range(-5, 6):
        require(mul(involution(-n), involution(n)) == I2, group, "reflexión transportada")
        require(mul(involution(n + 1), step(n))
                == mul(tr(step(-n - 1)), involution(n)), group, "inversión de paso")
        for k in range(-3, 4):
            for advanced in (False, True):
                first = mul(tr(step(n)), kernel(n + 1, k, advanced))
                last = mul(step(n - 1), kernel(n - 1, k, advanced))
                result = add(first, scale(-2, kernel(n, k, advanced)), last)
                require(result == (I2 if n == k else zero(2, 2)),
                        group, "L G = identidad")
            require(kernel(n, k, True) == tr(kernel(k, n)), group, "adjunción de Green")
            conjugated = mul(mul(involution(-n), kernel(-n, -k)), involution(k))
            require(conjugated == kernel(n, k, True), group, "intercambio causal")
    require(mul(mul(C0, J2), C0) == scale(-1, J2), group, "estructura compleja conjugada")
    h = scale(3, I2)
    generator = scale(Q(-1, 5), mul(J2, h))
    require(tr(generator) == scale(-1, generator), group, "generador antiadjunto")
    require(mul(mul(C0, generator), C0) == scale(-1, generator), group, "generador revertido")


def hessian_checks():
    group = "hessiano_y_fuentes_compactas"
    psi = {n: mat([[Q(n + 4, 3)], [Q(n * n - 2, 5)]]) for n in range(-2, 3)}
    direction = {-1: mat([[Q(2, 7)], [1]]), 2: mat([[-1], [Q(3, 2)]])}
    energy = sum(dot(difference(psi, n), difference(psi, n)) for n in range(-3, 3))
    require(energy == -sum(dot(v, kinetic(psi, n)) for n, v in psi.items()),
            group, "E = - <psi,Lpsi>")
    jet = 2 * sum(dot(difference(direction, n), difference(psi, n)) for n in range(-3, 3))
    expected = -2 * sum(dot(v, kinetic(psi, n)) for n, v in direction.items())
    require(jet == expected, group, "variación de energía")
    source = {n: kinetic(psi, n) for n in range(-3, 4)}
    for n in range(-7, 8):
        require(green(source, n) == value(psi, n), group, "Gret Lpsi = psi")
        require(green(source, n, True) == value(psi, n), group, "Gadv Lpsi = psi")


def absorption_checks():
    group = "momentos_y_absorcion"
    for N in range(1, 7):
        size = N + 1
        b = mat([[1] * size, list(range(size))])
        projection = add(eye(size), scale(-1, mul(mul(tr(b), inv2(mul(b, tr(b)))), b)))
        require(mul(b, projection) == zero(2, size), group, "momentos nulos")
        require(mul(projection, projection) == projection, group, "idempotencia")
        require(tr(projection) == projection, group, "ortogonalidad")
        require(sum(projection[i][i] for i in range(size)) == N - 1, group, "rango")
        ret = mat([[max(n - k, 0) for k in range(size)] for n in range(size)])
        adv = tr(ret)
        sym = scale(Q(1, 2), add(ret, adv))
        rad = scale(Q(1, 2), add(ret, scale(-1, adv)))
        boundary = mat([rad[0], rad[-1]])
        require(mul(boundary, projection) == zero(2, size), group, "igualdad de borde")
        j = mat([[Q(k * k + 1, k + 1)] for k in range(size)])
        variation = mat([[Q((-1) ** k, k + 2)] for k in range(size)])
        pj, ph = mul(projection, j), mul(projection, variation)
        derivative = Q(1, 2) * (dot(ph, mul(sym, pj)) + dot(pj, mul(sym, ph)))
        gradient = mul(mul(projection, sym), pj)
        require(derivative == dot(variation, gradient), group, "gradiente restringido")
        if N == 2:
            witness = mat([[1], [-2], [1]])
            require(mul(projection, witness) == witness, group, "testigo absorbido")
            field = mul(sym, witness)
            require(field == mat([[0], [1], [0]]), group, "respuesta simétrica del testigo")
            require(mul(projection, field) != field, group, "respuesta distinta de gradiente restringido")
    # Dos momentos vectoriales transportados y factor de diferencia causal.
    source = {k: mul(transport(k, 0), mat([[k + 1], [Q(1, k + 1)]])) for k in range(4)}
    m0 = add(*(mul(transport(0, k), v) for k, v in source.items()))
    m1 = add(*(scale(k, mul(transport(0, k), v)) for k, v in source.items()))
    for n in range(-4, 8):
        lhs = add(green(source, n), scale(-1, green(source, n, True)))
        rhs = mul(transport(n, 0), add(scale(n, m0), scale(-1, m1)))
        require(lhs == rhs, group, "identidad de momentos con memoria transportada")


def refinement_checks():
    group = "refinamiento_y_control_negativo"
    r = mat([[1, 0], [0, 1], [0, 0]])
    a = mat([[1, 0]])
    p = mat([[0, 0], [0, 1]])
    aprime = mat([[1, 0, 1]])
    pprime = add(eye(3), scale(Q(-1, 2), mul(tr(aprime), aprime)))
    require(mul(aprime, r) == a, group, "entrelazamiento de frontera")
    require(mul(pprime, r) != mul(r, p), group, "entrelazar frontera no basta para proyectores")
    aprime_compatible = mat([[1, 0, 0]])
    pprime_compatible = add(eye(3), scale(-1, mul(tr(aprime_compatible), aprime_compatible)))
    require(mul(pprime_compatible, r) == mul(r, p), group, "compatibilidad ortogonal suficiente")


def main():
    route_checks()
    transport_and_green_checks()
    hessian_checks()
    absorption_checks()
    refinement_checks()
    print(json.dumps({
        "status": "PASS_CONTROLES_FINITOS_PROPAGACION_BIDIRECCIONAL",
        "count": sum(counts.values()),
        "groups": counts,
        "arithmetic": "Fraction exacta; matrices reales racionales",
        "scope": "Rutas finitas, diferencia covariante, Green cronológicos, momentos, proyección absorbente y variación restringida; no identificación automática con campos4D.",
        "physical_amplitude_selected": False,
        "whole_theory_validation": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
