#!/usr/bin/env python3
"""Controles adicionales acotados; no repite censos ni 1000 cifras."""
import ast
import copy
import hashlib
import itertools
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
PACKAGE = AUDIT.parent / 'REVISION_EDITORIAL_HMT_MD_20260905'
SOURCE = PACKAGE / '03_PRUEBAS/verificar_generacion_infinita_nonadica.py'
tree = ast.parse(SOURCE.read_text())
names = {'propagation_bounds', 'autoscale_bounds'}
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
if len(nodes) != 2:
    raise AssertionError('No se localizaron las dos funciones auditadas')

def require(condition, message):
    if not condition:
        raise AssertionError(message)

ns = {'Fraction': Fraction, 'itertools': itertools, 'require': require}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), 'exec'), ns)
echar = {'kind':'normalized_group_like_propagation_character',
         'normalization':'a_0=1', 'recurrence':'(n+1)*a_(n+1)=a_n'}
pchar = {'kind':'positive_autoscale_character',
         'orientation':'unique positive expanding ray',
         'incidence':[[0,1],[1,1]], 'characteristic_polynomial':[1,-1,-1]}
rejected = []
for fn, original, changes in (
    ('propagation_bounds', echar, [('normalization','a_0=2'), ('recurrence','a_(n+1)=a_n')]),
    ('autoscale_bounds', pchar, [('incidence',[[1,1],[1,1]]), ('characteristic_polynomial',[1,-2,-1]), ('orientation','contracting')]),
):
    ns[fn](original, 10**12)
    for field, value in changes:
        altered = copy.deepcopy(original)
        altered[field] = value
        try:
            ns[fn](altered, 10**12)
        except AssertionError as error:
            rejected.append({'field':field, 'reason':str(error)})
        else:
            raise AssertionError('Mutación causal aceptada: '+field)

replay = json.loads((AUDIT/'RECOMPROBACION_CONSTANTES/REPLAY_RESULTADOS.json').read_text())
alpha = next(r['result'] for r in replay['records'] if r['id']=='ALPHA_FINITE_TWO_WAY')
K = alpha['K']
B = 1000
kappa = Fraction(sum(v*B**(11-j) for j,v in enumerate(K)), B**12-1)

# La igualdad de series y esta suma geométrica no usan alpha como objetivo.
# Sólo se evalúa aquí la realización escalar de los caracteres publicados.
with localcontext() as ctx:
    ctx.prec = 100
    D = Decimal
    # Serie de Chudnovsky para evaluación posterior de pi (no selector TPK).
    m,l,x,k = 1,13591409,1,6
    total = D(l)
    for j in range(1,9):
        m = m*(k*k*k-16*k)//(j*j*j)
        l += 545140134
        x *= -262537412640768000
        total += D(m*l)/x
        k += 12
    pi = 426880*D(10005).sqrt()/total
    e = D(1).exp()
    phi = (1+D(5).sqrt())/2
    alpha_A = pi+e-phi-4-D(kappa.numerator)/D(kappa.denominator)
    alpha_finite = D('0.'+''.join(f'{v:03d}' for v in alpha['alpha_digits']))
    value_check = {'alpha_A_periodic_K':str(alpha_A),
                   'alpha_finite_12':str(alpha_finite),
                   'difference':str(alpha_A-alpha_finite),
                   'truncation_36':str(int(alpha_A*D(10)**36)),
                   'rounding_36':str(int(alpha_A*D(10)**36+D('0.5'))),
                   'kappa_exact':str(kappa)}
    require(value_check['truncation_36'].endswith('662'), 'truncamiento de frontera')
    require(value_check['rounding_36'].endswith('663'), 'redondeo de frontera')

AW = [[0,1,1,1,1,1],[1,0,1,2,2,1],[1,1,0,1,2,2],
      [1,2,1,0,1,2],[1,2,2,1,0,1],[1,1,2,2,1,0]]
square = [[sum(AW[i][k]*AW[k][j] for k in range(6)) % 3 for j in range(6)] for i in range(6)]
require(square == [[2*int(i==j) for j in range(6)] for i in range(6)], 'AW²=-I en F3')
payload = {'status':'PASS_LOCAL', 'source':str(SOURCE),
           'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
           'mutation_tests_rejected':rejected, 'alpha_series_check':value_check,
           'imaginary_structure_square_mod3':square,
           'scope':'valida dependencia de evaluadores corregidos y consecuencias de K periódico; no rederiva K, ni prueba igualdad infinita con la vía de jets, ni totalidad de Ext',
           'originals_modified':False}
(HERE/'RECIBO_CONTROLES_NUCLEO.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(payload,indent=2,ensure_ascii=False))
