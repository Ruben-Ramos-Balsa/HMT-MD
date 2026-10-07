#!/usr/bin/env python3
"""Reproduce el tramo finito de U013 desde su semilla y elevaciones declaradas.

No reconstruye aquí el catálogo APP–TRIT ni certifica la prolongación infinita.
La inspección decimal ocurre después de las cuatro elevaciones modulares.
"""
import ast
import hashlib
import json
from pathlib import Path

PROJECT = Path('/Users/ruben/Documents/New project')
OWNER = PROJECT/'certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py'


def load_lifts():
    tree = ast.parse(OWNER.read_text())
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('L0', 'L1'):
                    found[target.id] = ast.literal_eval(node.value)
    assert set(found) == {'L0', 'L1'}
    return found


def emit(seed, lifts):
    b = tuple(map(int, seed))
    result = [seed]
    for key in ('L0', 'L0', 'L1', 'L1'):
        matrix = lifts[key]
        b = tuple(sum(b[i]*matrix[i][j] for i in range(6)) % 3 for j in range(6))
        result.append(''.join(map(str, b)))
    return result


def stable_decimal(word):
    numerator, denominator = int(word, 3), 3**len(word)
    stable = ''
    for depth in range(1, 30):
        scale = 10**depth
        lower = numerator*scale//denominator
        upper = ((numerator+1)*scale-1)//denominator
        if lower != upper:
            break
        stable = str(lower).zfill(depth)
    return dict(trits=len(word), numerator=numerator,
                denominator=denominator, stable_decimal_fraction=stable)


if __name__ == '__main__':
    lifts = load_lifts()
    blocks = emit('201101', lifts)
    readings = [stable_decimal(''.join(blocks[:n])) for n in range(1, 6)]
    decimal = readings[-1]['stable_decimal_fraction']
    square = decimal[1:5]
    assert square == decimal[5:9]
    assert decimal[9] != square[0]
    assert blocks[2] == blocks[4]
    assert readings[3]['stable_decimal_fraction'][1:9] == square+square
    print(json.dumps(dict(
        status='PASS_TRAMO_FINITO_E_Y_LECTOR_DECIMAL',
        scope='Semilla y matrices recibidas de propietarios; no nueva prueba integral.',
        matrix_owner=str(OWNER),
        matrix_owner_sha256=hashlib.sha256(OWNER.read_bytes()).hexdigest(),
        seed='201101', calendar=['L0','L0','L1','L1'],
        blocks=blocks, readings=readings,
        square=square, square_start_decimal_position=2,
        next_digit=decimal[9],
        square_already_fixed_at_24_trits=True,
        full_state_return_asserted=False), ensure_ascii=False, indent=2))
