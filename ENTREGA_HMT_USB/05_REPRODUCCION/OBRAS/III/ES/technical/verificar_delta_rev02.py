#!/usr/bin/env python3
"""Controles exactos focales del delta REV02; sólo biblioteca estándar.

Comprueba identidades matriciales por sus coeficientes, identidades
polinómicas y monomiales, y casos enteros/racionales deterministas.
No produce el registro primario E108 ni certifica una identificación física.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from random import Random


N = 12


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def mv(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def scale(a, c):
    return [[v * c for v in row] for row in a]


def rank(a):
    a = [[F(v) for v in row] for row in a]
    pivot = 0
    for j in range(len(a[0])):
        k = next((i for i in range(pivot, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        c = a[pivot][j]
        a[pivot] = [v / c for v in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][j]:
                c = a[i][j]
                a[i] = [x - c * y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def basis(n, i):
    return [int(i == j) for j in range(n)]


def matrix_of(fn, domain):
    return [list(row) for row in zip(*(fn(basis(domain, i))
                                      for i in range(domain)))]


def extract(z):
    return ([z[i] - z[(i + 3) % N] for i in range(N)]
            + [z[i] - z[(i + 4) % N] for i in range(N)]
            + [sum(z)])


def increments(data):
    b, c, q = data[:12], data[12:24], data[24]
    w = [c[i] - b[(i + 1) % N] for i in range(N)]
    p = [0]
    for wi in w:
        p.append(p[-1] + wi)
    return b, c, q, w, p, sum(p[:12])


def constraints(data):
    b, _, _, w, _, _ = increments(data)
    return [b[i] - sum(w[(i + j) % N] for j in range(3))
            for i in range(N)] + [sum(w)]


def inverse_rational(data):
    _, _, q, _, p, total = increments(data)
    return [F(q + total, N) - p[i] for i in range(N)]


def inverse_integer(data):
    require(len(data) == 25 and all(type(x) is int for x in data),
            "El dominio de la inversa integral es Z^25")
    require(not any(constraints(data)), "Relaciones lineales incompatibles")
    _, _, q, _, _, total = increments(data)
    require((q + total) % N == 0, "Congruencia modulo 12 incumplida")
    result = inverse_rational(data)
    require(all(v.denominator == 1 for v in result), "Inversa no integral")
    return [int(v) for v in result]


H4 = [[1, 1, 1, 1], [1, 1, -1, -1],
      [1, -1, 1, -1], [1, -1, -1, 1]]


def harmonic(z):
    result = [0] * N
    for r in range(3):
        block = [z[r + 3*j] for j in range(4)]
        for j, value in enumerate(mv(H4, block)):
            result[r + 3*j] = value
    return result


def pi_h(data):
    b, c, q = data[:12], data[12:24], data[24]
    big_b = [sum(c[r + 3*j] for j in range(4)) for r in range(3)]
    a0 = F(q + 2*big_b[0] + big_b[1], 3)
    a = [a0, a0 - big_b[0], a0 - big_b[0] - big_b[1]]
    out = [0] * N
    for r in range(3):
        values = [a[r], b[r+3]-b[r+9], b[r]+b[r+6], b[r]-b[r+6]]
        for j, value in enumerate(values):
            out[r + 3*j] = value
    return out


def decimal_blocks(counts):
    return [100*(a % 10) + 10*(c % 10) + v % 10 for a, c, v in counts]


def reject(fn):
    try:
        fn()
    except AssertionError:
        return True
    return False


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def padd(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    return trim(out)


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def pscale(a, c):
    return trim([c*x for x in a])


def pderiv(a):
    return trim([i*a[i] for i in range(1, len(a))] or [0])


def f(s):
    return (1+s+s*s)/(1+s+s*s+s*s*s)


def constitutive(rp, rm):
    return {'epsilon': rp*rp, 'mu': rm*rm, 'Z': rm/rp, 'c': 1/(rp*rm)}


def change_units(v, a, b, d):
    return {'epsilon': a*d/(b*b)*v['epsilon'],
            'mu': d*b*b/a*v['mu'],
            'Z': b*b/a*v['Z'], 'c': v['c']/d}


def undo_units(v, a, b, d):
    return {'epsilon': b*b/(a*d)*v['epsilon'],
            'mu': a/(d*b*b)*v['mu'],
            'Z': a/(b*b)*v['Z'], 'c': d*v['c']}


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def mono_mul(a, b):
    return tuple(x+y for x, y in zip(a, b))


def mono_power(a, n):
    return tuple(n*x for x in a)


def main_checks():
    results = {}
    dmat = matrix_of(extract, 12)
    invmat = matrix_of(inverse_rational, 25)
    cmat = matrix_of(constraints, 25)
    hmat = matrix_of(harmonic, 12)
    pmat = matrix_of(pi_h, 25)
    require(mm(invmat, dmat) == eye(12), 'Inversa izquierda D')
    require(rank(dmat) == 12, 'Rango D')
    require(rank(cmat) == 13, 'Independencia de las 13 relaciones')
    require(not any(map(any, mm(cmat, dmat))), 'Relaciones sobre imagen D')
    require(mm(hmat, hmat) == scale(eye(12), 4), 'H12^2=4I')
    require(mm(pmat, dmat) == hmat, 'Pi_H D=H12')
    require(mm(scale(hmat, F(1, 4)), mm(pmat, dmat)) == eye(12),
            'Reconstruccion Hadamard sobre imagen')
    # En Q^25, ker C=im D se deduce de C D=0 y de los dos rangos.
    results['linear_coefficient_identities'] = {
        'status': 'PASS', 'rank_D': 12, 'rank_constraints': 13,
        'domain': 'Identidades de matrices racionales completas, no muestreo',
        'identities': ['L D = I12', 'C D = 0', 'rank C = 13',
                       'H12^2 = 4 I12', 'Pi_H D = H12']}

    rng = Random(20260909)
    cases = [[0]*12, [1]*12, list(range(12))]
    cases += [basis(12, i) for i in range(12)]
    cases += [[rng.randrange(-10**5, 10**5) for _ in range(12)]
              for _ in range(1000)]
    for z in cases:
        data = extract(z)
        require(inverse_integer(data) == z, 'Ida y vuelta integral')
        u = pi_h(data)
        require(harmonic(u) == [4*x for x in z], 'Congruencia Hadamard')
        require(extract(inverse_integer(data)) == data, 'Vuelta integral')
    bad_q = [0]*25
    bad_q[-1] = 1
    require(not any(constraints(bad_q)), 'Control de congruencia independiente')
    require(reject(lambda: inverse_integer(bad_q)), 'Debe rechazar q=1 sin w')
    false_channels = [0]*25
    false_channels[12] = 1
    false_channels[15] = -1
    require(pi_h(false_channels) == [0]*12, 'Contraejemplo Pi_H=0')
    require(any(constraints(false_channels)), 'Contraejemplo fuera de imagen')
    require(reject(lambda: inverse_integer(false_channels)), 'Rechazo contraejemplo')
    require(reject(lambda: inverse_integer([0]*24)), 'Rechazo dimension')
    results['integer_roundtrip_and_negative_controls'] = {
        'status': 'PASS', 'deterministic_integer_cases': len(cases),
        'negative_cases': 3,
        'counterexample': {'b': false_channels[:12],
                           'c': false_channels[12:24], 'q': 0,
                           'Pi_H': pi_h(false_channels),
                           'linear_residual': constraints(false_channels)}}

    for _ in range(500):
        counts = [[rng.randrange(-500, 501) for _ in range(3)] for _ in range(12)]
        z = decimal_blocks(counts)
        require(inverse_integer(extract(z)) == z, 'Recuentos a bloques y vuelta')
        shifted = [[x + 10*rng.randrange(-20, 21) for x in row] for row in counts]
        require(extract(decimal_blocks(shifted)) == extract(z), 'Mismas 36 clases')
        conjugated = [[a, -c, v] for a, c, v in reversed(counts)]
        expected = [z[11-i] + 100*int(counts[11-i][1] % 10 != 0)
                    - 20*(counts[11-i][1] % 10) for i in range(12)]
        require(decimal_blocks(conjugated) == expected, 'Conjugacion decimal')
        require([[a, -c, v] for a, c, v in reversed(conjugated)] == counts,
                'Conjugacion es involucion')
        for i in range(12):
            for j in range(3):
                altered = [row[:] for row in counts]
                altered[i][j] += 1
                require(extract(decimal_blocks(altered)) != extract(z),
                        'Residuo individual no eliminable en dominio completo')
    # Prueba coeficiente a coeficiente de la identidad de extremos.
    endpoint_cases = 0
    for n in range(1, 109):
        left = Counter(range(1, n+1))
        right = Counter(range(n))
        right[n] += 1
        right[0] -= 1
        require(all(left[k] == right[k] for k in range(n+1)), 'Extremos')
        endpoint_cases += 1
    results['decimal_and_orientation_controls'] = {
        'status': 'PASS', 'deterministic_count_records': 500,
        'individual_residue_perturbations': 18000,
        'endpoint_coefficient_cases': endpoint_cases,
        'scope': 'Recuentos sinteticos, no enumeracion primaria TPK'}

    numerator, denominator = [1, 1, 1], [1, 1, 1, 1]
    derivative_numerator = padd(pmul(pderiv(numerator), denominator),
                                pscale(pmul(numerator, pderiv(denominator)), -1))
    require(derivative_numerator == [0, 0, -3, -2, -1], 'Derivada racional')
    cubic_numerator = padd(pmul(numerator, [0, 0, 0, 1]),
                           pmul(padd(numerator, pscale(denominator, -1)), numerator))
    require(cubic_numerator == [0], 'Identidad cubica tras limpiar denominador')
    require(padd(denominator, pscale(numerator, -1)) == [0, 0, 0, 1],
            'Defecto cubico')
    results['rational_function_coefficients'] = {
        'status': 'PASS', 'derivative_numerator': derivative_numerator,
        'cubic_identity_numerator': cubic_numerator,
        'scope': 'Identidades polinomicas exactas; sin aproximacion de raices'}

    # Exponentes de monomios en (r_+,r_-,a,b,d), validos en dominio positivo.
    eps, mu = (2,0,0,0,0), (0,2,0,0,0)
    z, c = (-1,1,0,0,0), (-1,-1,0,0,0)
    ep = mono_mul(eps, (0,0,1,-2,1))
    mp = mono_mul(mu, (0,0,-1,2,1))
    zp = mono_mul(z, (0,0,-1,2,0))
    cp = mono_mul(c, (0,0,0,0,-1))
    require(mono_mul(mu, eps) == mono_power(c, -2), 'Producto cuadratico')
    require(mono_mul(mu, mono_power(eps, -1)) == mono_power(z, 2), 'Cociente cuadratico')
    require(mono_mul(z, mono_power(c, -1)) == mu, 'Unicidad mu positiva')
    require(mono_power(mono_mul(z, c), -1) == eps, 'Unicidad epsilon positiva')
    require(mono_mul(mp, ep) == mono_power(cp, -2), 'Covariancia producto')
    require(mono_mul(mp, mono_power(ep, -1)) == mono_power(zp, 2),
            'Covariancia cociente')
    require(mono_mul(ep, (0,0,-1,2,-1)) == eps, 'Deshacer unidades epsilon')
    require(mono_mul(mp, (0,0,1,-2,-1)) == mu, 'Deshacer unidades mu')
    require(mono_mul(zp, (0,0,1,-2,0)) == z, 'Deshacer unidades Z')
    require(mono_mul(cp, (0,0,0,0,1)) == c, 'Deshacer unidades c')
    results['constitutive_laurent_identities'] = {
        'status': 'PASS', 'variables': ['r_plus','r_minus','a','b','d'],
        'domain': 'Variables positivas no nulas',
        'scope': 'Comparacion exacta de exponentes, sin muestreo'}

    jmat, rmark = [[0, 1], [1, 0]], [[1, 0], [0, -1]]
    require(mm(jmat, jmat) == eye(2), 'Involucion intercambio')
    require(mm(mm(jmat, rmark), jmat) == scale(rmark, -1), 'Marca cambia de signo')
    for n in range(2, 82):
        sp, sm = F(1, n+1), F(n, n+1)
        rp, rm = f(sp), f(sm)
        require(F(3,4) < rm < rp < 1, 'Camara monotona')
        for s, r in [(sp, rp), (sm, rm)]:
            require(r*s**3+(r-1)*(1+s+s*s) == 0, 'Raiz cubica exacta en muestra')
        vals = constitutive(rp, rm)
        a, b, d = F(n+2, n), F(n+3, 2), F(3, n+1)
        converted = change_units(vals, a, b, d)
        require(undo_units(converted, a, b, d) == vals, 'Ida y vuelta de unidades')
        require(converted['mu']*converted['epsilon']*converted['c']**2 == 1,
                'Identidad producto en nueva carta')
        require(converted['mu']/converted['epsilon'] == converted['Z']**2,
                'Identidad cociente en nueva carta')
        swapped = constitutive(rm, rp)
        require(swapped['epsilon'] == vals['mu'] and swapped['mu'] == vals['epsilon']
                and swapped['Z'] == 1/vals['Z'] and swapped['c'] == vals['c'],
                'Conjugacion con marcas fijas')
        v = [[rp, 0], [0, rm]]
        vj = mm(mm(jmat, v), jmat)
        rj = mm(mm(jmat, rmark), jmat)
        require(trace(mm(rmark, vj)) == -trace(mm(rmark, v)), 'Lectura fija impar')
        require(trace(mm(rj, vj)) == trace(mm(rmark, v)), 'Transporte simultaneo invariante')
        require(f(sp*sm) != f(sp)*f(sm), 'Determinante y funcion no intercambiables')
    results['rational_evaluations_and_conjugation'] = {
        'status': 'PASS', 'positive_rational_pairs': 80,
        'scope': 'Casos exactos racionales, no valores fisicos objetivo',
        'negative_control': 'f(s_plus*s_minus) != f(s_plus)*f(s_minus) en las 80 parejas'}
    return results


def encoded(obj):
    if isinstance(obj, F):
        return int(obj) if obj.denominator == 1 else f'{obj.numerator}/{obj.denominator}'
    raise TypeError(type(obj).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path,
                        default=Path(__file__).resolve().parent/'recibos/DELTA_REV02_EXACTO.json')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    sources = ['manuscrito/sections/02_registro_incidencial.tex',
               'manuscrito/sections/04_respuesta_constitutiva.tex',
               'manuscrito/sections/08_evaluacion_y_realizacion.tex',
               'technical/verificar_delta_rev02.py']
    hashes = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in sources}
    try:
        result = main_checks()
        receipt = {'schema': 'hmt.iii.rev02.exact_delta.v1',
                   'status': 'PASS_DELTA_REV02_EXACTO_FOCAL',
                   'arithmetic': 'Python int/Fraction; ninguna conversion float',
                   'source_sha256': hashes, 'checks': result,
                   'primary_E108_production_certified': False,
                   'canonical_terminal_register_generated': False,
                   'physical_identification_certified': False,
                   'global_alpha_equality_certified': False,
                   'scope': 'Identidades finitas de coeficientes y casos sinteticos. Las pruebas '
                            'universales de imagen integral y unicidad positiva residen en el texto. '
                            'No se certifica la produccion primaria del registro, limites universales, '
                            'seleccion de incidencias ni correspondencia metrologica.'}
    except Exception as exc:
        receipt = {'schema': 'hmt.iii.rev02.exact_delta.v1',
                   'status': 'FAIL_DELTA_REV02_EXACTO_FOCAL',
                   'source_sha256': hashes, 'error': f'{type(exc).__name__}: {exc}',
                   'primary_E108_production_certified': False}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2,
                                       sort_keys=True, default=encoded)+'\n', encoding='utf-8')
    print(receipt['status'])
    print(args.receipt.resolve())
    if receipt['status'].startswith('FAIL'):
        print(receipt['error'])
        raise SystemExit(1)


if __name__ == '__main__':
    main()
