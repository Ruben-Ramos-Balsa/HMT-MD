#!/usr/bin/env python3
"""Censo desde la recurrencia declarada y reconstrucción desde el registro impreso.

Estas dos comprobaciones finitas no producen el registro de transiciones
regional desde Upd o Sel: su dependencia se declara en el recibo.
"""
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
from hashlib import sha256
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent
OWNER = ROOT / 'originales/PROPIETARIOS_NUCLEO/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex'
CATALOG = ROOT / 'originales/CENSO_REGIONAL/datos/TPK_U_catalog_468.json'
DIRS = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1)}
LOG9 = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def signature(seed, multiplicative):
    i, j, direction = seed
    di, dj = DIRS[direction]
    result = []
    for window in range(6):
        total = 0
        for tick in range(9 * window + 1, 9 * (window + 1) + 1):
            residue = 1 + (tick - 1) % 9
            active = residue in ((2, 5, 8) if multiplicative else (1, 4, 7))
            if active:
                value = (i + 1) * (j + 1) if multiplicative else i + j + 2
                reduced = 1 + (value - 1) % 9
                total += LOG9.get(reduced, 0) if multiplicative else reduced
                i, j = (i + di) % 9, (j + dj) % 9
            if tick in (27, 54):
                di, dj = -di, -dj
        result.append(total % 10)
    return tuple(result)

def census():
    seeds = list(product(range(9), range(9), DIRS))
    plus, times = defaultdict(list), defaultdict(list)
    for seed in seeds:
        plus[signature(seed, False)].append(seed)
        times[signature(seed, True)].append(seed)
    emissions = {}
    for s, e in product(plus, times):
        u = tuple(100 * a + 10 * ((a + b) % 10) + (3 * a + 5 * b + 1) % 10
                  for a, b in zip(s, e))
        require(u not in emissions, 'Acoplamiento no inyectivo')
        require(tuple(value // 100 for value in u) == s, 'Inversa aditiva')
        require(tuple(((value // 10) % 10 - value // 100) % 10 for value in u) == e,
                'Inversa multiplicativa')
        emissions[u] = len(plus[s]) * len(times[e])
    ternary_fibres = Counter(tuple(-value % 3 for value in u) for u in emissions)
    ternary = set(ternary_fibres)
    require(len(seeds) == 324 and len(plus) == 18 and len(times) == 26, 'Cardinales de firmas')
    require(Counter(map(len, plus.values())) == Counter({18: 18}), 'Fibras aditivas')
    require(Counter(map(len, times.values())) == Counter({8: 24, 24: 1, 108: 1}), 'Fibras multiplicativas')
    require(len(emissions) == 468 and len(ternary) == 243, 'Cardinales de emisiones y proyección')
    require(sum(emissions.values()) == 104976, 'Dominio completo de parejas')
    require(Counter(emissions.values()) == Counter({144: 432, 432: 18, 1944: 18}), 'Fibras de emisión')
    require(Counter(ternary_fibres.values()) == Counter({1: 132, 2: 66, 3: 18, 4: 3, 5: 6, 6: 18}),
            'Censo de fibras ternarias')
    # Comparaison postérieure : le catalogue ne participe pas à la construction.
    reference = json.loads(CATALOG.read_text(encoding='utf-8'))
    expected = {tuple(map(int, row['U6'].split('|'))): int(row['count']) for row in reference}
    require(emissions == expected, 'Comparación posterior con el catálogo preservado')
    def classes(data):
        return [{'signature': list(s), 'multiplicity': len(data[s]),
                 'preimages': [list(seed) for seed in data[s]]} for s in sorted(data)]
    return {'scope': 'ENUMERACION_EXHAUSTIVA_DESDE_REGLA_FINITA_DECLARADA',
            'seed_count_per_cursor': len(seeds), 'pair_count': len(seeds) ** 2,
            'plus_classes': classes(plus), 'times_classes': classes(times),
            'emission_count': len(emissions), 'ternary_count': len(ternary),
            'ternary_fibre_histogram': dict(sorted(Counter(ternary_fibres.values()).items())),
            'emissions': [{'U6': list(u), 'count': emissions[u], 'word': list(-v % 3 for v in u)}
                          for u in sorted(emissions)],
            'comparison_catalogue_after_generation': True,
            'catalogue_sha256': sha256(CATALOG.read_bytes()).hexdigest()}

def matrix(text, name):
    pattern = re.escape(name) + r'\s*&?=\s*\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}'
    found = re.search(pattern, text, re.S)
    require(found is not None, 'Matriz fuente no encontrada: ' + name)
    rows = [[int(x.strip()) % 3 for x in row.strip().split('&')]
            for row in found.group(1).strip().split('\\\\') if row.strip()]
    require(len(rows) == 6 and all(len(r) == 6 for r in rows), 'Dimensión de ' + name)
    return rows

def inverse_det(a):
    n = len(a)
    b = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    det = 1
    for col in range(n):
        pivot = next((i for i in range(col, n) if b[i][col]), None)
        require(pivot is not None, 'Matriz singular')
        if pivot != col:
            b[col], b[pivot] = b[pivot], b[col]
            det = -det % 3
        value = b[col][col]
        det = det * value % 3
        b[col] = [v * pow(value, -1, 3) % 3 for v in b[col]]
        for i in range(n):
            if i != col:
                k = b[i][col]
                b[i] = [(v - k * w) % 3 for v, w in zip(b[i], b[col])]
    return [row[n:] for row in b], det

def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) % 3
             for j in range(len(b[0]))] for i in range(len(a))]

def rowmul(row, a):
    return mm([row], a)[0]

def transport():
    text = OWNER.read_text(encoding='utf-8')
    xs = [matrix(text, 'X_0'), matrix(text, 'X_1')]
    ys = [matrix(text, 'Y_0'), matrix(text, 'Y_1')]
    inv_det = [inverse_det(x) for x in xs]
    lifts = [mm(inv_det[i][0], ys[i]) for i in range(2)]
    require([d for _, d in inv_det] == [1, 2], 'Déterminants modulo 3')
    require(lifts == [matrix(text, 'L_0'), matrix(text, 'L_1')], 'Reconstruction des matrices imprimées')
    biographies = []
    for i in range(3):
        require(xs[0][2*i+1] == ys[0][2*i], 'Cohérence b1')
        require(xs[1][2*i] == ys[0][2*i+1], 'Cohérence b2')
        require(xs[1][2*i+1] == ys[1][2*i], 'Cohérence b3')
        biographies.append([xs[0][2*i], ys[0][2*i], ys[0][2*i+1], ys[1][2*i], ys[1][2*i+1]])
    def mismatch(matrices, calendar):
        return sum(rowmul(bio[k], matrices[calendar[k]]) != bio[k+1]
                   for bio in biographies for k in range(4))
    calendar_rows = [{'calendar': list(c), 'failed_transitions': mismatch(lifts, c)}
                     for c in product(range(2), repeat=4)]
    survivors = [r['calendar'] for r in calendar_rows if not r['failed_transitions']]
    require(survivors == [[0, 0, 1, 1]], 'Calendrier unique relatif aux biographies')
    mutations = []
    for a, i, j, step in product(range(2), range(6), range(6), (1, 2)):
        mutated = [[row[:] for row in m] for m in lifts]
        mutated[a][i][j] = (mutated[a][i][j] + step) % 3
        failed = mismatch(mutated, survivors[0])
        require(failed > 0, 'Perturbation non détectée')
        mutations.append({'matrix': a, 'row': i, 'column': j, 'increment_mod3': step,
                          'failed_transitions': failed})
    return {'scope': 'RECONSTRUCCION_Y_CENSOS_EXHAUSTIVOS_DESDE_TRANSICIONES_IMPRESAS',
            'not_produced_here': 'La acción coordinada de Sel/Tra/Upd que produce X0,Y0,X1,Y1.',
            'source_sha256': sha256(OWNER.read_bytes()).hexdigest(),
            'X': xs, 'Y': ys, 'L_reconstructed': lifts,
            'determinants_mod3': [d for _, d in inv_det],
            'biographies': biographies, 'calendars': calendar_rows,
            'survivor': survivors[0], 'mutations': mutations}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    result = {'status': 'PASS_NUCLEO_FINITO_REGLA_Y_REGISTRO_DECLARADOS',
              'scope': 'Dos comprobaciones finitas distintas; no cierre de la generación coinductiva global.',
              'census': census(), 'transport': transport()}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'cursor_states': 324, 'pair_states': 104976,
                      'emissions': 468, 'ternary_words': 243, 'calendars': 16, 'mutations': 144}, ensure_ascii=False))

if __name__ == '__main__':
    main()
