#!/usr/bin/env python3
"""Identidades de propagación desde ∇_μ E^{μν}=0, con aritmética racional.

En un punto con derivadas espaciales del marco métrico anuladas, q y K son
matrices generales. Calcula los Christoffel y la divergencia, no la presupone.
"""
from fractions import Fraction as F


def inverse(a):
    n = len(a)
    b = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(j for j in range(k, n) if b[j][k])
        b[k], b[pivot] = b[pivot], b[k]
        d = b[k][k]
        b[k] = [x/d for x in b[k]]
        for j in range(n):
            if j != k:
                d = b[j][k]
                b[j] = [x-d*y for x, y in zip(b[j], b[k])]
    return [row[n:] for row in b]


def add(*items):
    result = {}
    for item in items:
        for key, value in item.items():
            result[key] = result.get(key, F(0)) + value
    return {k: v for k, v in result.items() if v}


def scale(item, c):
    return {k: F(c)*v for k, v in item.items() if F(c)*v}


def variable(name):
    return {name: F(1)}


def linear_sum(items):
    return add(*items)


qs = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
      [[2, 1, 0], [1, 3, 1], [0, 1, 2]],
      [[3, 0, 1], [0, 2, 0], [1, 0, 2]]]
ks = [[[0, 1, 2], [1, 0, -1], [2, -1, 0]],
      [[1, 0, 0], [0, 2, 0], [0, 0, -3]],
      [[2, 1, 0], [1, -1, 2], [0, 2, 4]]]
checks = 0

for q in qs:
    qi = inverse(q)
    for k in ks:
        g = [[F(-1 if i == j == 0 else 0) for j in range(4)] for i in range(4)]
        gi = [[F(-1 if i == j == 0 else 0) for j in range(4)] for i in range(4)]
        for i in range(3):
            for j in range(3):
                g[i+1][j+1], gi[i+1][j+1] = F(q[i][j]), qi[i][j]

        def dg(direction, i, j):
            return F(2*k[i-1][j-1]) if direction == 0 and i and j else F(0)

        gamma = [[[sum((gi[a][d]*(dg(b, d, c)+dg(c, d, b)-dg(d, b, c))/2
                            for d in range(4)), F(0))
                   for c in range(4)] for b in range(4)] for a in range(4)]
        trace_k = sum((qi[i][j]*k[i][j] for i in range(3) for j in range(3)), F(0))
        cup = [linear_sum(scale(variable(f'C{j}'), qi[i][j]) for j in range(3))
               for i in range(3)]
        e = [[{} for _ in range(4)] for _ in range(4)]
        e[0][0] = variable('C')
        for i in range(3):
            e[0][i+1] = e[i+1][0] = scale(cup[i], -1)

        # The chain rule for E^{0i}=-q^{ij}C_j retains dot(q^{-1}).
        partial = [add(variable('dotC'), linear_sum(
            scale(variable(f'd{i}C{j}'), -qi[i][j])
            for i in range(3) for j in range(3)))]
        for i in range(3):
            partial.append(add(
                linear_sum(scale(variable(f'dotC{j}'), -qi[i][j]) for j in range(3)),
                linear_sum(scale(cup[b], 2*qi[i][a]*k[a][b])
                           for a in range(3) for b in range(3))))

        divergence = []
        for nu in range(4):
            div = partial[nu]
            for mu in range(4):
                for lam in range(4):
                    div = add(div, scale(e[lam][nu], gamma[mu][mu][lam]),
                              scale(e[mu][lam], gamma[nu][mu][lam]))
            divergence.append(div)

        expected0 = add(variable('dotC'), scale(variable('C'), trace_k),
                        linear_sum(scale(variable(f'd{i}C{j}'), -qi[i][j])
                                   for i in range(3) for j in range(3)))
        assert divergence[0] == expected0, 'dotC - D_i C^i + K C'
        checks += 1
        for i in range(3):
            lower = linear_sum(scale(divergence[j+1], q[i][j]) for j in range(3))
            expected = add(scale(variable(f'dotC{i}'), -1),
                           scale(variable(f'C{i}'), -trace_k))
            assert lower == expected, '-dotC_i - K C_i'
            checks += 1

print(f'PASS_RETROACCION_RESTRICCIONES_VARIACIONALES: {checks} identidades exactas Q')
