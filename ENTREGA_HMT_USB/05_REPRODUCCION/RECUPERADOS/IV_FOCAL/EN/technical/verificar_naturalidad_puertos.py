#!/usr/bin/env python3
"""Exact finite controls for the port pullbacks added on 2026-09-11.

This tests modular and history refinement on complete rectangular modules,
including children over the marked parent. It does not test a restriction to
an admissible-incidence support or certify the global continuum or Weil.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def delta(w, modulus):
    return tuple(tuple((w[i][j] - w[i][0] - w[0][j] + w[0][0]) % modulus
                       for j in range(len(w[0]))) for i in range(len(w)))


def pull(w, row_parents, column_parents):
    return tuple(tuple(w[i][j] for j in column_parents) for i in row_parents)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    count = 0

    def require(condition, message):
        nonlocal count
        count += 1
        if not condition:
            raise RuntimeError(message)

    # Index 0 is marked; further indices may also map to the marked parent.
    surjections = ((0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 0, 1, 1))
    for modulus in (3, 9):
        for entries in itertools.product(range(3), repeat=4):
            w = (entries[:2], entries[2:])
            for rows, columns in itertools.product(surjections, repeat=2):
                refined = pull(w, rows, columns)
                require(delta(refined, modulus) == pull(delta(w, modulus), rows, columns),
                        'delta is not natural under marked prefix pullback')
                if modulus == 9:
                    reduced = tuple(tuple(x % 3 for x in row) for row in refined)
                    require(delta(reduced, 3) == tuple(tuple(x % 3 for x in row)
                                                     for row in delta(refined, 9)),
                            'coefficient reduction does not commute with delta')
                # A further surjection repeats the marked child and every child.
                rows2 = (0,) + tuple(range(len(rows)))
                columns2 = (0,) + tuple(range(len(columns)))
                require(pull(refined, rows2, columns2) ==
                        pull(w, tuple(rows[x] for x in rows2),
                             tuple(columns[x] for x in columns2)),
                        'composition of prefix pullbacks failed')
        for u, v in itertools.product(itertools.product(range(3), repeat=2), repeat=2):
            w = tuple(tuple((x-y) % modulus for y in v) for x in u)
            for rows, columns in itertools.product(surjections, repeat=2):
                require(pull(w, rows, columns) ==
                        tuple(tuple((u[i]-v[j]) % modulus for j in columns) for i in rows),
                        'kappa is not natural under prefix pullback')
    result = {
        'status': 'PASS_NATURALIDAD_RECTANGULAR_FINITA',
        'checks': count,
        'scope': 'Exact finite checks of the displayed local identities, not a global theorem certificate',
        'moduli': [3, 9],
        'includes_unmarked_children_of_marked_parent': True,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    if args.receipt:
        args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
