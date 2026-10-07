#!/usr/bin/env python3
"""Control focal exacto de indices, no certificado global del corpus.

Se evalua el lector logaritmico posterior definido en la fuente, sin usar
constantes objetivo ni seleccionar estados HMT. Los suelos se certifican con
intervalos racionales: no se emplea float ni Decimal.ln.

ln(r) = 2 sum_{j=0}^{N-1} x^(2j+1)/(2j+1) + R_N,
x=(r-1)/(r+1), 0 < R_N < 2*x^(2N+1)/((2N+1)*(1-x*x)).
"""

from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json


ROOT = Path('/Users/ruben/Documents/New project')
SOURCE = ROOT / 'output/INVESTIGACION_HOLONOMIA_NONADICA_CRISTAL_APERIODICO_20260903/DESARROLLO_MATEMATICO.md'
DEFAULT_OUT = Path(__file__).with_name('CONTROL_RELOJES_VACANCIAS.json')
DIGITS = 100
Q = 10 ** DIGITS


def log_interval(r, terms):
    x = (r - 1) / (r + 1)
    x2 = x * x
    power = x
    total = F(0)
    for j in range(terms):
        total += power / (2 * j + 1)
        power *= x2
    lower = 2 * total
    upper = lower + 2 * power / ((2 * terms + 1) * (1 - x2))
    return lower, upper


def down(x):
    return x.numerator // x.denominator


def up(x):
    return -((-x.numerator) // x.denominator)


def decimal_enclosure(lo, hi):
    return down(lo * Q), up(hi * Q)


def fixed(x):
    return str(x // Q) + '.' + str(x % Q).zfill(DIGITS)


def make_interval():
    a_lo, a_hi = log_interval(F(10, 9), 60)
    b_lo, b_hi = log_interval(F(3), 220)
    # delta=a/(a+2*b), monotonically increasing in a, decreasing in b.
    d_lo = a_lo / (a_lo + 2 * b_hi)
    d_hi = a_hi / (a_hi + 2 * b_lo)
    dlo, dhi = decimal_enclosure(d_lo, d_hi)
    assert dhi - dlo == 1
    return dlo, dhi


def run(events=4096, blocks=100000):
    dlo, dhi = make_interval()
    diagnostics = {'floors_certified': 0, 'ambiguous_floors': 0}

    def floor_pair(low_num, low_den, high_num, high_den):
        a = low_num // low_den
        b = high_num // high_den
        if a != b:
            diagnostics['ambiguous_floors'] += 1
            raise ArithmeticError('interval straddles a floor boundary')
        diagnostics['floors_certified'] += 1
        return a

    def fd(m):
        return floor_pair(m * dlo, Q, m * dhi, Q)

    def capacity(t):
        return floor_pair((t + 1) * (Q - dhi), Q,
                          (t + 1) * (Q - dlo), Q)

    def event(n):
        return floor_pair(n * Q, dhi, n * Q, dlo)

    def inverse(k):
        # k/rho is irrational for k>0; ceil(x)-1=floor(x).
        assert k > 0
        return floor_pair(k * Q, Q - dlo, k * Q, Q - dhi)

    theta_lo = F(22) - F(Q, dlo)
    theta_hi = F(22) - F(Q, dhi)
    assert F(21) < F(Q, dhi) < F(Q, dlo) < F(22)
    assert F(6) < 1 / theta_hi < 1 / theta_lo < F(7)
    thlo, thhi = decimal_enclosure(theta_lo, theta_hi)
    invdlo, invdhi = decimal_enclosure(F(Q, dhi), F(Q, dlo))
    invthlo, invthhi = decimal_enclosure(1 / theta_hi, 1 / theta_lo)

    capacities = [capacity(t) for t in range(blocks + 1)]
    z = [fd(t + 1) - fd(t) for t in range(1, blocks + 1)]
    assert all(v in (0, 1) for v in z)
    assert all(capacities[t] - capacities[t - 1] == 1 - z[t - 1]
               for t in range(1, blocks + 1))
    assert capacities[0] == 0

    ps = [event(n) for n in range(1, events + 2)]
    cs = [capacity(p) for p in ps]
    assert all(c == p - n for n, (p, c) in enumerate(zip(ps, cs), 1))
    assert all(fd(p + 1) - fd(p) == 1 for p in ps)
    hs = [b - a for a, b in zip(ps, ps[1:])]
    ss = [22 - h for h in hs]
    assert set(hs) == {21, 22}
    assert all(b - a == h - 1 for a, b, h in zip(cs, cs[1:], hs))
    assert all((b - a + s) % 3 == 0 for a, b, s in zip(cs, cs[1:], ss))

    shorts = [n for n, h in enumerate(hs, 1) if h == 21]
    short_distances = [b - a for a, b in zip(shorts, shorts[1:])]
    assert set(short_distances) == {6, 7}
    for j, n in enumerate(shorts, 1):
        # q_j=floor(j/theta): evaluate both exact rational interval ends.
        expected = floor_pair(j * theta_hi.denominator, theta_hi.numerator,
                              j * theta_lo.denominator, theta_lo.numerator)
        assert n == expected

    classes = [c % 3 for c in cs]
    runs = []
    start = 1
    for n in range(2, len(classes) + 1):
        if classes[n - 1] != classes[n - 2]:
            runs.append({'event_start': start, 'event_end': n - 1,
                         'length': n - start, 'class_mod3': classes[n - 2],
                         'left_truncated': start == 1,
                         'right_truncated': False})
            start = n
    runs.append({'event_start': start, 'event_end': len(classes),
                 'length': len(classes) - start + 1,
                 'class_mod3': classes[-1], 'left_truncated': start == 1,
                 'right_truncated': True})
    assert runs[0]['length'] == 6
    assert all(r['length'] in (6, 7) for r in runs[:-1])
    assert classes[:20] == [2] * 6 + [1] * 7 + [0] * 7

    inverse_event_positions = []
    for k in range(1, 10001):
        roof = inverse(k + 1) - inverse(k)
        assert roof in (1, 2)
        if roof == 2:
            inverse_event_positions.append(k)
    assert inverse_event_positions[:10] == [20, 41, 62, 83, 104, 125, 145, 166, 187, 208]
    assert set(b - a for a, b in zip(inverse_event_positions, inverse_event_positions[1:])) == {20, 21}
    returns = {}
    for m, expected in [(6, {6, 7}), (9, {9, 10}), (108, {113, 114})]:
        observed = {inverse(k + m) - inverse(k) for k in range(1, 10001)}
        assert observed == expected
        returns[str(m)] = sorted(observed)

    block_censuses = []
    for t in [20, 21, 22, 43, 108, 132, 396, 1000, 2376, 10000, 100000]:
        count = fd(t + 1)
        assert count == sum(z[:t])
        assert capacities[t] + count == t
        block_censuses.append({'block_interval_inclusive': [1, t],
                               'vacancies': count,
                               'capacity_increments': capacities[t]})
    gap_censuses = []
    for n in [20, 100, 396, 1000, events]:
        if n <= events:
            counts = Counter(hs[:n])
            gap_censuses.append({'gap_indices_inclusive': [1, n],
                                'gap21': counts[21], 'gap22': counts[22]})

    rows = []
    for n in range(1, 33):
        c = cs[n - 1]
        r = 1 + c % 9
        m_ph = {0: 1, 1: -1, 2: 0}[c % 3]
        rows.append({'n': n, 'p_n': ps[n - 1], 'c_n': c,
                     'h_n_to_next': hs[n - 1], 's_n_to_next': ss[n - 1],
                     'c_mod3': c % 3, 'r_positive_mod9': r, 'M_ph': m_ph})

    return {
        'status': 'PASS_LOCAL_INDEX_IDENTITIES_WITH_ONE_SOURCE_WORDING_OFFSET',
        'scope': 'Control focal de lectores posteriores e indices; no sustituye recibos ni puertas globales HMT.',
        'provenance_status': 'CERTIFICADO_NUEVO de identidades ya formuladas; no nueva arquitectura.',
        'source': str(SOURCE), 'source_sha256': sha256(SOURCE.read_bytes()).hexdigest(),
        'source_sections': {'38': [3058, 3143], '39': [3144, 3200],
                            '40': [3201, 3286], '50': [4035, 4138]},
        'notation': 'C_t en este control corresponde a K_t de la fuente; c_n corresponde a kappa_n.',
        'method': {'arithmetic': 'Fraction e integer exactos; intervalos cerrados con extremos dirigidos',
                   'log_10_over_9_terms': 60, 'log_3_terms': 220,
                   'decimal_scale_digits': DIGITS, 'log_tail_bound': '2*x^(2*N+1)/((2*N+1)*(1-x^2))',
                   'delta_lower': fixed(dlo), 'delta_upper': fixed(dhi),
                   'inverse_delta_lower': fixed(invdlo), 'inverse_delta_upper': fixed(invdhi),
                   'theta_definition': 'theta=22-1/delta',
                   'theta_lower': fixed(thlo), 'theta_upper': fixed(thhi),
                   'inverse_theta_lower': fixed(invthlo), 'inverse_theta_upper': fixed(invthhi),
                   **diagnostics},
        'exact_derivation': [
            'delta es irracional: si log10(10/9)=a/b racional con b>0, (10/9)^b=10^a contradice la valoracion en el primo 3.',
            'Para t>=0, C_t=t-floor((t+1)*delta). Para t>=1, C_t-C_(t-1)=1-z_t.',
            'Para n>=1, p_n*delta<n<(p_n+1)*delta; z_(p_n)=1 y c_n=C_(p_n)=p_n-n.',
            '21<1/delta<22 implica h_n en {21,22}. c_(n+1)-c_n=h_n-1=21-s_n; modulo 3 es -s_n.',
            'Con theta=22-1/delta irracional, p_n=22*n-ceil(n*theta) y s_n=ceil((n+1)*theta)-ceil(n*theta).',
            'Los indices n>=1 con s_n=1 son q_j=floor(j/theta), j>=1. 6<1/theta<7 da q_(j+1)-q_j en {6,7}.',
            'La transicion de clase se produce de c_(q_j) a c_(q_j+1). Mesetas completas: eventos q_j+1,...,q_(j+1), longitud q_(j+1)-q_j.',
            'El inicio n=1 trunca la primera meseta: eventos 1,...,q_1=6. No es una excepcion al alfabeto 6/7, pero no debe llamarse una meseta bilateral completa.',
            'Para k>=1, T(k)=ceil(k/rho)-1=floor(k/rho). T(0)=0 por definicion del minimo; no extender la formula de techo de k>=1 a k=0.',
        ],
        'finite_checks': {'block_steps': blocks, 'event_gaps': events,
                          'inverse_capacities': [1, 10000],
                          'complete_noninitial_plateau_lengths': sorted({r['length'] for r in runs[1:-1]}),
                          'return_times_by_capacity_increment': returns,
                          'not_a_global_proof_by_enumeration': True},
        'source_offset': {'location': 'DESARROLLO_MATEMATICO.md:4123',
                          'source_wording': 'la pareja (kappa_n,s_n) reconstruye el incremento anterior',
                          'finding': 'La regla local 21-s_n reconstruye el incremento siguiente c_(n+1)-c_n; aplicarla al anterior produce un desfase. Esto no niega una recuperacion global del pasado a partir de la capacidad y el lector completo.',
                          'minimal_correction': 'Sustituir anterior por siguiente; si se desea hablar del anterior, usar s_(n-1).',
                          'witness': {'n': 6, 'previous_increment': cs[5] - cs[4],
                                      'next_increment': cs[6] - cs[5], 's_n': ss[5]}},
        'endpoint_warnings': [
            'z_t esta declarado para t>=1; C_t-C_(t-1) no debe usarse en t=0 sin definir C_(-1).',
            'Sum_{t=1}^T z_t=floor((T+1)*delta), mientras sum_{t=0}^{T-1} z_t=floor(T*delta); fijar la ventana.',
            'Un hueco corto con indice n=q_j cambia la clase en el evento n+1, no en el evento n.',
            'El ultimo tramo de cualquier censo finito puede estar truncado y tener longitud menor que 6; excluirlo como falso contraejemplo.',
            'La coordenada theta_t={t*delta} lee z_t despues del avance: z_t=1 iff theta_t>=1-delta. Si se usa theta_(t-1), componer primero la rotacion.',
        ],
        'first_32_events': rows,
        'first_20_short_gap_indices': shorts[:20],
        'first_19_short_gap_separations': short_distances[:19],
        'first_12_plateaus': runs[:12],
        'first_20_inverse_exceptional_capacities': inverse_event_positions[:20],
        'block_censuses': block_censuses, 'gap_censuses': gap_censuses,
    }


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    report = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(report['status'])
    print('delta interval:', report['method']['delta_lower'], report['method']['delta_upper'])
    print('first short-gap indices:', report['first_20_short_gap_indices'])
    print('first plateaus:', [(r['event_start'], r['event_end'], r['length'], r['class_mod3'])
                              for r in report['first_12_plateaus']])
    print('source wording offset:', report['source_offset']['witness'])
    print('block censuses:', report['block_censuses'])
    print('gap censuses:', report['gap_censuses'])
    print('output:', args.output)
