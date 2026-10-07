#!/usr/bin/env python3
"""Controles focales exactos: censo APP, modo TRIT, espectro y fronteras.

No lee CODATA ni valores físicos objetivo. La enumeración 1..9 produce N.
Las pruebas universales de telescopía están en el fragmento TeX; la malla
racional es un control de implementación, no una prueba de irracionalidad.
No verifica identificación electromagnética, masa electrónica ni todo III.
"""
from fractions import Fraction as F
from itertools import product
import json


def ensure(condition, message):
    if not condition:
        raise RuntimeError(message)


def rho9(n):
    return 1 + (n - 1) % 9


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    r = 0
    for col in range(len(a[0])):
        pivot = next((k for k in range(r, len(a)) if a[k][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        divisor = a[r][col]
        a[r] = [x / divisor for x in a[r]]
        for k in range(len(a)):
            if k != r:
                factor = a[k][col]
                a[k] = [x - factor * y for x, y in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def floor(q):
    return q.numerator // q.denominator


def ceil(q):
    return -floor(-q)


def check_app():
    n = [[0] * 9 for _ in range(9)]
    for x, y, z in product(range(1, 10), repeat=3):
        n[rho9(x+y+z)-1][rho9(x*y*z)-1] += 1
    expected = [
        [0,1,1,0,1,1,0,1,4], [1,0,1,1,0,1,1,0,4],
        [1,0,2,0,1,2,0,0,3], [0,1,1,0,1,1,0,1,4],
        [1,0,1,1,0,1,1,0,4], [0,0,2,1,0,2,0,1,3],
        [0,1,1,0,1,1,0,1,4], [1,0,1,1,0,1,1,0,4],
        [0,1,2,0,0,2,1,0,3],
    ]
    ensure(n == [[9*x for x in row] for row in expected], 'Censo APP')
    ensure(all(sum(row) == 81 for row in n), 'Sumas de fila')
    masses = [sum(row[b] for row in n) for b in range(9)]
    ensure(masses == [36,36,108,36,36,108,36,36,297], 'Sumas de columna')
    m = [1,-1,0] * 3
    ensure(matvec(n, m) == [-27*x for x in m], 'N modo TRIT')
    ensure(matvec(list(zip(*n)), m) == [-27*x for x in m], 'N transpuesto TRIT')
    ensure(all(masses[b] == 36 for b in range(9) if m[b]), 'Normalizacion modo')
    matrix = [[sum(F(n[a][b]*n[c][b], 81*masses[b]) for b in range(9))
               for c in range(9)] for a in range(9)]
    eigenpairs = [([1]*9, F(1)), (m, F(1,4)), ([1,1,-2]*3, F(7,132))]
    for support, eigenvalue in [([2,5,8], F(1,18)),
                               ([0,3,6], F(0)), ([1,4,7], F(0))]:
        for j in [0,1]:
            v = [0] * 9
            v[support[j]], v[support[2]] = 1, -1
            eigenpairs.append((v, eigenvalue))
    for vector, value in eigenpairs:
        ensure(matvec(matrix, vector) == [value*x for x in vector],
               'Identidad de autovector ' + str(value))
    ensure(rank([v for v, _ in eigenpairs]) == 9, 'Base espectral completa')
    norm_squared = max(value*(1-value) for _, value in eigenpairs)
    ensure(norm_squared == F(3,16), 'Norma al cuadrado')
    return {'triples': 729, 'rank_M': rank(matrix),
            'basis_dimension': 9, 'commutator_norm_squared': str(norm_squared),
            'trit_singular_value': '1/2', 'quadratic_defect': '3/4'}


def check_boundaries():
    checks = 0
    for delta in [F(1,22), F(2,43), F(3,7), F(7,11)]:
        for theta in [F(-2), F(-1,3), F(0), F(1,5), F(7,4)]:
            sums = {'up': F(0), 'down': F(0)}
            for n in range(200):
                x, y = n*delta+theta, (n+1)*delta+theta
                up, down = ceil(y)-ceil(x), floor(y)-floor(x)
                ensure(up in (0,1) and down in (0,1), 'Alfabeto mecanico')
                b0, b1 = int(x.denominator == 1), int(y.denominator == 1)
                ensure(up-down == b0-b1, 'Termino de frontera local')
                sums['up'] += up-delta
                sums['down'] += down-delta
                target_up = ceil(y)-ceil(theta)-(n+1)*delta
                target_down = floor(y)-floor(theta)-(n+1)*delta
                ensure(sums['up'] == target_up, 'Telescopia superior')
                ensure(sums['down'] == target_down, 'Telescopia inferior')
                ensure(abs(target_up) < 1 and abs(target_down) < 1, 'Cota estricta')
                ensure(target_up-target_down == int(theta.denominator == 1)-b1,
                       'Termino de frontera acumulado')
                checks += 1
    for k in range(1, 131):
        u = F(k,131)
        numerator = 1+u+u*u
        denominator = numerator+u**3
        ensure(4*numerator-3*denominator == (1-u)*(3*u*u+2*u+1),
               'Factorizacion de respuesta')
        ensure(F(3,4) < numerator/denominator < 1, 'Intervalo constitutivo')
    return {'exact_rational_boundary_cases': checks, 'response_cases': 130,
            'scope': 'Control focal; prueba universal de limites en el manuscrito'}


if __name__ == '__main__':
    result = {'status': 'PASS_VACANCIAS_PREFACTOR_FOCAL',
              'app': check_app(), 'boundary': check_boundaries()}
    print(json.dumps(result, ensure_ascii=False, indent=2))
