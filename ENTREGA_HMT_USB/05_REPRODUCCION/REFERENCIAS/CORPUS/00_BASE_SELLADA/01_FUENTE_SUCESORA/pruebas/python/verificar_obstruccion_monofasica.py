"""Enumera la proyección monofásica de 108 pasos y certifica su imagen."""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
SIGMA12 = (1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1)
CYCLES = ((0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11))
ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / 'datos' / 'HMT_mass_route_signatures_10species.csv'
OUTPUT = ROOT / 'certificados' / 'obstruccion_monofasica.json'

def dr9(n: int) -> int:
    r = n % 9
    return 9 if r == 0 else r

def mov3(rho: int) -> int:
    if rho in (1, 4, 7):
        return 1
    if rho in (2, 5, 8):
        return -1
    return 0

def sign(x: int) -> int:
    return (x > 0) - (x < 0)

def digits(seed_r: int, seed_c: int, h0: int, v0: int) -> tuple[int, ...]:
    (r, c, h, v) = (seed_r, seed_c, h0, v0)
    out = []
    for t in range(1, 109):
        move = mov3(1 + (t - 1) % 9)
        if move == 1:
            d = dr9(r + c)
            c = 1 + (c - 1 + h) % 9
        elif move == -1:
            d = dr9(r * c)
            r = 1 + (r - 1 + v) % 9
        else:
            d = 9
        if t % 27 == 0 and t < 108:
            (h, v) = (-h, -v)
        out.append(d)
    return tuple(out)

def observable(ds: tuple[int, ...]) -> tuple[int, int, int, int, int]:
    (odds, evens) = ({1, 3, 5, 7}, {2, 4, 6, 8})
    nA = sum((d in odds for d in ds))
    sC = sum((1 if (t - 1) // 27 in (0, 2) else -1 for (t, d) in enumerate(ds, 1) if d in evens))
    sc_ev = tuple((SIGMA12[m] * sum((d in evens for d in ds[9 * m:9 * (m + 1)])) for m in range(12)))
    tau = tuple((sign(x) for x in sc_ev))
    K = sum((SIGMA12[m] for m in range(12) if tau[m] == 0))
    nu120 = sum((sign(sum((sc_ev[i] for i in cyc))) for cyc in CYCLES))
    nu270 = sum((tau[m] * tau[(m + 3) % 12] for m in range(12)))
    return (nA, sC, K, nu120, nu270)

def enumerate_rows() -> list[tuple[int, ...]]:
    rows = []
    for r in range(1, 10):
        for c in range(1, 10):
            for h in (-1, 1):
                for v in (-1, 1):
                    ds = digits(r, c, h, v)
                    rows.append((r, c, h, v, *observable(ds)))
    return rows

def main() -> None:
    rows = enumerate_rows()
    if not (len(rows) == 324 and len(set((tuple(row[:4]) for row in rows))) == 324):
        raise AssertionError('comprobación ejecutable fallida')
    if not rows == enumerate_rows():
        raise AssertionError('comprobación ejecutable fallida')
    for (_, _, _, _, nA, sC, K, nu120, nu270) in rows:
        if not 0 <= nA <= 108:
            raise AssertionError('comprobación ejecutable fallida')
        if not -108 <= sC <= 108:
            raise AssertionError('comprobación ejecutable fallida')
        if not -12 <= K <= 12:
            raise AssertionError('comprobación ejecutable fallida')
        if not -4 <= nu120 <= 4:
            raise AssertionError('comprobación ejecutable fallida')
        if not -12 <= nu270 <= 12:
            raise AssertionError('comprobación ejecutable fallida')
    payload = json.dumps(rows, separators=(',', ':'), ensure_ascii=True).encode()
    classes = Counter(((row[4], row[5]) for row in rows))
    image = {tuple(row[4:]) for row in rows}
    with TARGETS.open(newline='', encoding='utf-8') as handle:
        target_rows = list(csv.DictReader(handle))
    if not len(target_rows) == 10:
        raise AssertionError('comprobación ejecutable fallida')
    target_vectors = {row['species']: tuple((int(row[column]) for column in ('nA', 'sC', 'k_D4', 'nu120', 'nu270'))) for row in target_rows}
    matches = sorted((species for (species, vector) in target_vectors.items() if vector in image))
    if not matches == []:
        raise AssertionError('comprobación ejecutable fallida')
    coordinate_ranges = {name: sorted({vector[index] for vector in image}) for (index, name) in enumerate(('nA', 'sC', 'k', 'nu120', 'nu270'))}
    result = {'status': 'PASS', 'verifier': 'pruebas/python/verificar_obstruccion_monofasica.py', 'initial_conditions': len(rows), 'signature_vectors': len(image), 'signature_classes_nA_sC': len(classes), 'coordinate_ranges': coordinate_ranges, 'published_signatures_checked': len(target_vectors), 'published_signatures_in_image': matches, 'factorization_result': 'NO_FACTORIZATION_0_OF_10', 'sha256_rows': hashlib.sha256(payload).hexdigest()}
    serialized = json.dumps(result, sort_keys=True, indent=2) + '\n'
    OUTPUT.write_text(serialized, encoding='utf-8')
    print(serialized, end='')
if __name__ == '__main__':
    main()
