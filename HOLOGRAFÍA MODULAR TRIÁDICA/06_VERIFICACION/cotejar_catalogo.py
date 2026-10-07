"""Read-only comparison of 20 preserved LaTeX rows; no mass calculation.

Run from any directory using Python 3.9+. The input locations are relative to
this delivery. Whitespace and allowbreak are normalised; prose and units are
outside the comparison's scope.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import sys

USB = Path(__file__).resolve().parents[1]
OLD = USB / '05_REPRODUCCION/DATOS/MASAS/SECCION_CERTIFICADA/07_contraste_metrologico.tex'
EXPECTED = '52267ec3c4f342def152eb336226e4932ca3b0ef25036fb35ee944b03966330b'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def rows(path):
    text = path.read_text(encoding='utf-8')
    start = text.index(r'\(e^\pm\) &')
    end = text.index(r'\(n,\bar n\) &', start)
    end = text.index(r'\\', end) + 2
    result = []
    for line in text[start:end].split(r'\\'):
        if '&' not in line:
            continue
        cols = line.split('&')
        if len(cols) != 4:
            raise ValueError(f'Unexpected row in {path}: {line}')
        result.append({
            'state': re.sub(r'\s+', '', cols[0]),
            'hmt_expression': re.sub(r'\s+', '', cols[1].replace(r'\allowbreak', '')),
            'reference_numerals': re.findall(r'[-+]?\d+(?:[.,]\d+)?', cols[2]),
            'type': re.sub(r'\s+', '', cols[3]),
        })
    if len(result) != 20:
        raise ValueError(f'Expected 20 rows in {path}, got {len(result)}')
    return result


def main():
    if digest(OLD) != EXPECTED:
        raise ValueError('The certified source fingerprint differs.')
    original = rows(OLD)
    records = []
    for work in ['VI', 'VIa']:
        for lang in ['ES', 'EN', 'FR']:
            unit = USB / '05_REPRODUCCION/OBRAS' / work / lang
            source = unit / 'sections/07_contraste_metrologico.tex'
            current = rows(source)
            differences = [{'row':i+1, 'fields':[k for k in a if a[k] != b[k]]}
                           for i, (a, b) in enumerate(zip(original, current)) if a != b]
            records.append({'work':work, 'language':lang,
                            'source':source.relative_to(USB).as_posix(),
                            'sha256':digest(source), 'rows':len(current),
                            'differences':differences})
    passed = all(not r['differences'] for r in records)
    print(json.dumps({'status':'PASS_DOCUMENTARY_20_ROWS' if passed else 'DOCUMENTARY_DIFFERENCES_FOUND',
                      'scope':'Literal LaTeX expressions, states, types and reference numeral sequences only. No scientific evaluation, prose equivalence or unit validation.',
                      'sections':records}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
