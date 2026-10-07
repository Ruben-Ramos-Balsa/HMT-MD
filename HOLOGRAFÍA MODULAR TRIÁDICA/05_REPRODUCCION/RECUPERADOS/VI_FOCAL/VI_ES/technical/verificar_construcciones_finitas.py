#!/usr/bin/env python3
"""Controles exactos de las nuevas exposiciones finitas del Artículo VI.

No introduce valores físicos ni certifica por extensión todo el artículo.
"""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json

ROOT = Path(__file__).resolve().parents[1]

def family(r, c):
    return {(1, 1): 'ell', (1, 0): 'nu', (0, 1): 'd', (0, 0): 'u'}[(r % 2, c % 2)]

def encode(events):
    p = [events[i]+events[i+6] for i in range(6)]
    a = [events[i]-events[i+6] for i in range(6)]
    return sum(p), [p[i]-p[5] for i in range(5)], a

def decode(total, differences, oriented):
    base = Fraction(total-sum(differences), 6)
    p = [base+x for x in differences]+[base]
    return tuple((p[i]+oriented[i])/2 for i in range(6))+tuple((p[i]-oriented[i])/2 for i in range(6))

def main():
    checks = []
    def check(name, condition, detail):
        checks.append({'id': name, 'pass': bool(condition), 'detail': detail})
        if not condition:
            raise AssertionError(name)
    cells = list(product(range(1, 10), repeat=2))
    fibers = defaultdict(list)
    for r, c in cells:
        fibers[(family(r, c), max(abs(r-5), abs(c-5)))].append((r, c))
    expected = {'ell': {0:1, 2:8, 4:16}, 'nu': {1:2, 2:4, 3:6, 4:8},
                'd': {1:2, 2:4, 3:6, 4:8}, 'u': {1:4, 3:12}}
    actual = {f: {g:len(v) for (ff,g),v in fibers.items() if ff==f} for f in expected}
    check('ATLAS_81_13', len(cells)==81 and len(fibers)==13 and actual==expected, actual)
    rho = lambda c: (10-c[0],10-c[1])
    fixed = [c for c in cells if rho(c)==c]
    orbits = {tuple(sorted([c,rho(c)])) for c in cells}
    check('CENTRO_ORBITAS', fixed==[(5,5)] and len(orbits)==41, {'fixed':fixed,'orbits':len(orbits)})
    check('ESTABILIDAD_MULTISECCIONES', all(rho(c) in v for v in fibers.values() for c in v), 'Las 13 fibras son estables.')
    colors = Counter((r-c)%3 for r,c in cells if r%2==0)
    check('COLOR_12_12_12', dict(colors)=={0:12,1:12,2:12}, dict(colors))
    check('COLOR_CONJUGADO', all(((10-r)-(10-c))%3==(-(r-c))%3 for r,c in cells), 'Negación modular.')
    count = 0
    # Base, amplitudes variadas y todas las palabras ternarias de 12 eventos.
    for events in product((-1,0,1), repeat=12):
        if decode(*encode(events)) != events:
            raise AssertionError('RECONSTRUCCION_1_5_6')
        count += 1
    for i in range(12):
        for amplitude in (-9,-5,2,7,11):
            event = tuple(amplitude if j==i else 0 for j in range(12))
            if decode(*encode(event)) != event:
                raise AssertionError('BASE_INTEGRAL')
    check('RECONSTRUCCION_1_5_6', True, {'ternary_vectors':count,'additional_basis_vectors':60,
                                      'scope':'Control finito complementario a la prueba algebraica del cuerpo.'})
    malformed = decode(1,[0]*5,[0]*6)
    check('CONTROL_NEGATIVO_IMAGEN', any(x.denominator!=1 for x in malformed),
          'Un total incompatible con las congruencias no produce eventos enteros.')
    # Testigos finitos de identidades universales demostradas en el texto.
    qp, qm = Fraction(1,3), Fraction(2,3)
    c = lambda n: qm**n+qp**n
    s = lambda n: qm**n-qp**n
    for m,n in product(range(9),repeat=2):
        assert c(m+n)==(c(m)*c(n)+s(m)*s(n))/2
        assert s(m+n)==(s(m)*c(n)+c(m)*s(n))/2
        assert c(n)**2-s(n)**2==4*(qp*qm)**n
    check('MOMENTOS_BICAPA', True, {'pairs':81,'scope':'Testigos racionales; no evaluación de los canales físicos.'})
    generated={90*a+120*b for a in range(101) for b in range(101)}
    target={90,120}|{30*r for r in range(6,301)}
    check('SEMIGRUPO_HASTA_9000', (generated & set(range(1,9001)))==target,
          'Complementa la demostración por inducción; no limita el semigrupo.')
    result={'status':'PASS_CONTROLES_FINITOS_VI',
            'scope':'Censos, reconstrucción de eventos e identidades finitas. No valida identificaciones físicas ni el cierre de dependencias.',
            'checks':checks,'count':len(checks)}
    (ROOT/'technical/CONTROLES_FINITOS_VI.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(result['status'], result['count'])

if __name__=='__main__':
    main()
