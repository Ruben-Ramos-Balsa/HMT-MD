#!/usr/bin/env python3
"""Traza focal íntegra; compara el emisor local con su implementación propietaria.

No ejecuta owner.main(), no abre catálogos ni recibe constantes objetivo.
La única condición inicial es el primer par en la enumeración de semillas.
Los JSON/TSV producidos son datos de esta ejecución, no fuentes del emisor.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

ROOT = Path('/Users/ruben/Documents/New project')
OWNER = Path(__file__).resolve().parent / '../../../../../../COMUN/CERTIFICADOS_K/lectura_conjunta/fuentes/articulo_x/supplement/emission/verificar_catalogo_app.py'
SOURCE = Path(__file__).resolve().parent / '../../../../../../COMUN/CERTIFICADOS_K/lectura_conjunta/fuentes/articulo_x/sections/extension.tex'
DIRS = ('N', 'E', 'S', 'O')
VEC = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1)}
OPP = {'N': 'S', 'E': 'O', 'S': 'N', 'O': 'E'}
LOG9 = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cursor(x=0, y=0, d='N'):
    return {'x': x, 'y': y, 'd': d}


def chart(c):
    return {'i': c['x'] % 9, 'j': c['y'] % 9,
            'a': c['x'] % 9 + 1, 'b': c['y'] % 9 + 1,
            'winding_x': c['x'] // 9, 'winding_y': c['y'] // 9}


def reading(c, sheet):
    m = chart(c)
    raw = m['a'] + m['b'] if sheet == '+' else m['a'] * m['b']
    r, q = 1 + (raw - 1) % 9, (raw - 1) // 9
    assert raw == r + 9 * q
    return {'chart': m, 'raw': raw, 'residue': r, 'quotient': q,
            'unit': r in LOG9, 'log9_extended': LOG9.get(r, 0)}


def active(t):
    return ('+', '-', '0')[(t - 1) % 3]


def step(c, moves, flip):
    x, y, d = c['x'], c['y'], c['d']
    dx, dy = VEC[d]
    return cursor(x + (dx if moves else 0), y + (dy if moves else 0),
                  OPP[d] if flip else d)


def unstep(c, moved, flipped):
    d = OPP[c['d']] if flipped else c['d']
    dx, dy = VEC[d]
    return cursor(c['x'] - (dx if moved else 0), c['y'] - (dy if moved else 0), d)


def trace(seed_plus=(0, 0, 'N'), seed_times=(0, 0, 'N'), after_read=False):
    p, q = cursor(*seed_plus), cursor(*seed_times)
    rows, windows, s = [], [], [0, 0, 0]
    for t in range(1, 55):
        if (t - 1) % 9 == 0:
            s = [0, 0, 0]
        a, flip = active(t), t in (27, 54)
        before_p, before_q, before_s = p.copy(), q.copy(), s.copy()
        np, nq = step(p, a == '+', flip), step(q, a == '-', flip)
        rp, rq = reading(np if after_read else p, '+'), reading(nq if after_read else q, '*')
        inc = [rp['residue'], 0, 0] if a == '+' else ([0, rq['log9_extended'], 0] if a == '-' else [0, 0, 1])
        s = [x + y for x, y in zip(s, inc)]
        assert unstep(np, a == '+', flip) == p
        assert unstep(nq, a == '-', flip) == q
        row = {'tick': t, 'window': (t - 1) // 9 + 1, 'local_tick': (t - 1) % 9 + 1,
               'phase_before': t - 1, 'phase_after': t, 'nonadic_phase': (t - 1) % 9 + 1,
               'event': a, 'plus_before': before_p, 'times_before': before_q,
               'plus_reading': rp, 'times_reading': rq,
               'accumulators_before': before_s, 'increment': inc, 'accumulators_after': s.copy(),
               'flip_after_movement': flip, 'plus_after': np.copy(), 'times_after': nq.copy(),
               'memory_length_after': t, 'emission': None}
        if t % 9 == 0:
            S, E, Z = s
            digits = [S % 10, (S + E) % 10, (3 * S + 5 * E + 7 * Z) % 10]
            U = 100 * digits[0] + 10 * digits[1] + digits[2]
            row['emission'] = {'S': S, 'E': E, 'Z': Z, 's': S % 10, 'e': E % 10,
                               'digits': digits, 'U': U, 'ternary': (-U) % 3}
            windows.append({'window': row['window'], 'final_tick': t, **row['emission']})
        rows.append(row)
        p, q = np, nq
    return rows, windows


def flatten(row):
    f = {key: row[key] for key in ('tick', 'window', 'local_tick', 'phase_before', 'phase_after', 'nonadic_phase', 'event')}
    for key in ('plus_before', 'times_before', 'plus_after', 'times_after'):
        f.update({f'{key}_{k}': v for k, v in row[key].items()})
    for key in ('plus_reading', 'times_reading'):
        f.update({f'{key}_{k}': v for k, v in row[key].items() if k != 'chart'})
        f.update({f'{key}_chart_{k}': v for k, v in row[key]['chart'].items()})
    for key in ('accumulators_before', 'increment', 'accumulators_after'):
        f.update({f'{key}_{k}': v for k, v in zip(('S', 'E', 'Z'), row[key])})
    f['flip_after_movement'] = row['flip_after_movement']
    f['memory_length_after'] = row['memory_length_after']
    f['emission_U'] = '' if row['emission'] is None else row['emission']['U']
    f['emission_ternary'] = '' if row['emission'] is None else row['emission']['ternary']
    return f


def write_tsv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('owner_emitter_read_only', OWNER)
    owner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owner)
    seed = (0, 0, 'N')
    rows, windows = trace(seed, seed)
    U = tuple(w['U'] for w in windows)
    ss, es = tuple(w['s'] for w in windows), tuple(w['e'] for w in windows)
    assert U == owner.direct_u6(seed, seed)
    assert ss == owner.channel_signature(seed, 'plus')
    assert es == owner.channel_signature(seed, 'times')
    assert owner.combine(ss, es) == U
    assert owner.recover_signatures(U) == (ss, es)
    word = ''.join(str(w['ternary']) for w in windows)
    assert word == owner.w6(U)
    assert Counter(r['event'] for r in rows) == Counter({'+': 18, '-': 18, '0': 18})
    assert all(Counter(r['event'] for r in rows[9*m:9*m+9]) == Counter({'+': 3, '-': 3, '0': 3}) for m in range(6))
    for r in rows:
        for ckey, rkey in (('plus_before', 'plus_reading'), ('times_before', 'times_reading')):
            c, m = r[ckey], r[rkey]['chart']
            assert c['x'] == 9 * m['winding_x'] + m['i']
            assert c['y'] == 9 * m['winding_y'] + m['j']
    assert all(w['Z'] == 3 for w in windows)
    assert [r['tick'] for r in rows if r['flip_after_movement']] == [27, 54]
    assert len(rows) == 54 and all(r['memory_length_after'] == r['tick'] for r in rows)
    for r, nxt in zip(rows, rows[1:]):
        assert (r['plus_after'], r['times_after']) == (nxt['plus_before'], nxt['times_before'])
    seeds = list(product(range(9), range(9), DIRS))
    sc, ec = defaultdict(list), defaultdict(list)
    for nu, s0 in enumerate(seeds):
        sc[owner.channel_signature(s0, 'plus')].append(nu)
        ec[owner.channel_signature(s0, 'times')].append(nu)
    emissions, ternary = {}, defaultdict(list)
    for sp, ep in product(sorted(sc), sorted(ec)):
        u = owner.combine(sp, ep)
        assert u not in emissions
        assert owner.recover_signatures(u) == (sp, ep)
        emissions[u] = {'s_signature': sp, 'e_signature': ep, 'multiplicity': len(sc[sp]) * len(ec[ep])}
        ternary[owner.w6(u)].append(u)
    assert (len(sc), len(ec), len(emissions), len(ternary)) == (18, 26, 468, 243)
    assert sum(x['multiplicity'] for x in emissions.values()) == 324 ** 2
    pairs = [{'nu_plus': i, 'nu_times': j, 'pair_id': 324 * i + j}
             for i, j in product(sc[ss], ec[es])]
    for p in pairs:
        assert owner.direct_u6(seeds[p['nu_plus']], seeds[p['nu_times']]) == U
    collision_word = next(w for w in sorted(ternary) if len(ternary[w]) > 1)
    collision = [dict(U=list(u), **emissions[u]) for u in sorted(ternary[collision_word])[:2]]
    changed = tuple(w['U'] for w in trace(seed, seed, after_read=True)[1])
    assert changed != U
    wrong_sign = ''.join(str(u % 3) for u in U)
    assert wrong_sign != word
    result = {
        'schema': 'HMT_FINITE_EMITTER_TRACE_1.0', 'scope': 'one complete 54-step case plus exact finite signature fibers',
        'causal_cut': 'APP -> phase reading TRIT -> finite TPK emission; no coinductive constant evaluation in this artifact',
        'selection_rule': 'first ordered pair under nu=4*(9*i+j)+direction_index; directions N,E,S,O',
        'seed_plus': list(seed), 'seed_times': list(seed), 'seed_ids': [0, 0],
        'owner': str(OWNER), 'owner_sha256': sha(OWNER), 'source': str(SOURCE), 'source_sha256': sha(SOURCE),
        'script_sha256': sha(Path(__file__)),
        'owner_functions_used': ['direct_u6', 'channel_signature', 'combine', 'recover_signatures', 'w6'],
        'owner_main_executed': False, 'target_catalog_read': False,
        'trace': rows, 'windows': windows, 'U6': U, 's_signature': ss, 'e_signature': es, 'w6': word,
        'fiber': {'plus_seed_ids': sc[ss], 'times_seed_ids': ec[es], 'pair_count': len(pairs), 'pairs': pairs,
                  'U6_catalog_fiber_over_w6': ternary[word],
                  'all_histories_over_w6': sum(emissions[u]['multiplicity'] for u in ternary[word])},
        'global_finite_signature_check': {'plus_classes': len(sc), 'times_classes': len(ec), 'emissions': len(emissions),
              'ternary_image': len(ternary), 'seed_pairs': sum(x['multiplicity'] for x in emissions.values()),
              'plus_fiber_histogram': dict(sorted(Counter(map(len, sc.values())).items())),
              'times_fiber_histogram': dict(sorted(Counter(map(len, ec.values())).items())),
              'emission_fiber_histogram': dict(sorted(Counter(x['multiplicity'] for x in emissions.values()).items()))},
        'first_ternary_collision': {'selection_rule': 'lexicographically first generated word having at least two catalog emissions',
                                  'w6': collision_word, 'two_emissions': collision},
        'negative_controls': {'read_after_move_U6': changed, 'read_after_move_detected': changed != U,
                              'opposite_ternary_sign': wrong_sign, 'opposite_sign_detected': wrong_sign != word},
        'checks': {'local_inverse_all_54': True, 'owner_direct_case': True, 'owner_factorization_case': True,
                   'owner_recovery_case': True, 'direct_owner_all_selected_144_seed_pairs': True,
                   'finite_catalog_by_648_single_cursor_signatures': True,
                   'full_104976_direct_campaign_executed': False},
        'status': 'PASS_TRAZA_FOCAL_EMISOR_54_Y_FIBRAS'}
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / '21_TRAZA_EMISOR_54.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    write_tsv(out / '21_TRAZA_EMISOR_54.tsv', [flatten(r) for r in rows])
    write_tsv(out / '21_FIBRA_144_CONDICIONES.tsv', pairs)
    summary = {k: result[k] for k in ('status', 'U6', 's_signature', 'e_signature', 'w6', 'first_ternary_collision', 'negative_controls')}
    summary['fiber_pair_count'] = len(pairs)
    summary['trace_steps'] = len(rows)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
