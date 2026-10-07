#!/usr/bin/env python3
"""Compilación exacta de incidencias declaradas, anterior al inversor de K.

No contiene K, U, alfa ni las 25 coordenadas canónicas. El constructor recibe
visitas APP y trazas dirigidas, calcula los tres recuentos sectoriales y produce
los canales transversales. No reemplaza el productor TPK de esas incidencias.
Un recibo de compilación no certifica que el archivo suministrado sea el registro
terminal canónico: la procedencia del selector y la exhaustividad de trazas se
declaran separadamente. No se acepta ningún valor por defecto.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


class IncidenceError(ValueError):
    pass


def require(test, message):
    if not test:
        raise IncidenceError(message)


def integer(value, name):
    require(type(value) is int, name + ': se requiere un entero')
    return value


def exact_keys(value, names, context):
    require(isinstance(value, dict), context + ': objeto requerido')
    require(set(value) == set(names), context + ': campos distintos de ' + ','.join(names))


def positive(value, name):
    integer(value, name)
    require(value > 0, name + ': debe ser positivo')
    return value


def sign(value):
    return (value > 0) - (value < 0)


def split9(n):
    r = 1 + (n - 1) % 9
    return r, (n - r) // 9


def channels_from_counts(counts):
    """Z^(12x3) -> residuos módulo10 -> bloques -> D3,D4,Q.

    Las componentes de counts están ordenadas (A,C,9). No se recibe ninguna
    coordenada de salida esperada y no se utiliza el inversor transversal.
    """
    require(len(counts) == 12, 'se requieren exactamente 12 sectores')
    blocks, residues, quotients = [], [], []
    for m, row in enumerate(counts):
        require(len(row) == 3, f'sector {m+1}: se requieren tres recuentos')
        qr = [divmod(integer(n, 'recuento'), 10) for n in row]
        q, r = [pair[0] for pair in qr], [pair[1] for pair in qr]
        quotients.append(q)
        residues.append(r)
        blocks.append(100*r[0] + 10*r[1] + r[2])
    return {
        'raw_counts_A_C_9': counts,
        'residues_mod10': residues,
        'division_quotients10': quotients,
        'blocks_generated': blocks,
        'b90': [blocks[m]-blocks[(m+3)%12] for m in range(12)],
        'b120': [blocks[m]-blocks[(m+4)%12] for m in range(12)],
        'Q': sum(blocks),
    }


def conjugate_counts(counts):
    """Cas où la conjugaison préserve A/9 et inverse les canaux des traces.

    L'identification de cette action avec une involution TPK donnée doit être
    établie sur ses incidences; les occupations d'un chemin ouvert peuvent
    recevoir des termes d'extrémité. Ce n'est pas un sélecteur de registre.
    """
    return [[a,-c,v] for a,c,v in reversed(counts)]


def compile_ledger(data):
    exact_keys(data, ('schema', 'provenance', 'routes', 'visits', 'traces120',
                     'trace_coverage'), 'entrada')
    require(data['schema'] == 'HMT_INCIDENCE_LEDGER_12_V1', 'esquema desconocido')
    prov = data['provenance']
    exact_keys(prov, ('ledger_owner', 'family_selector', 'boundary_operator',
                     'trace_generator', 'trit_operator'), 'procedencia')
    for key, value in prov.items():
        require(isinstance(value, str) and bool(value.strip()), 'procedencia vacía: '+key)
    routes = data['routes']
    require(isinstance(routes, list) and routes, 'familia de rutas vacía')
    require(all(isinstance(r, str) and r for r in routes), 'identificador de ruta')
    require(len(set(routes)) == len(routes), 'rutas duplicadas')
    visits = {}
    counts = [[0, 0, 0] for _ in range(12)]
    arithmetic = []
    for v in data['visits']:
        exact_keys(v, ('id', 'route', 'tick', 'i', 'j', 'sheet', 'trit',
                       'multiplicity', 'nine_incidence'), 'visita')
        require(isinstance(v['id'], str) and v['id'] not in visits, 'id de visita no único')
        require(v['route'] in routes, 'ruta de visita no declarada')
        t = positive(v['tick'], 'tick')
        i, j = integer(v['i'], 'i'), integer(v['j'], 'j')
        require(1 <= i <= 9 and 1 <= j <= 9, 'posición fuera de APP')
        require(v['sheet'] in ('sum', 'product', 'threshold'), 'hoja no reconocida')
        integer(v['trit'], 'trit')
        require(v['trit'] in (-1, 0, 1), 'trit fuera del dominio')
        mult = positive(v['multiplicity'], 'multiplicidad de incidencia')
        raw = i+j if v['sheet'] == 'sum' else i*j if v['sheet'] == 'product' else 9
        digit, quotient = split9(raw)
        if digit == 9:
            require(v['nine_incidence'] in ('crown', 'interior'),
                    'todo 9 requiere clasificación incidencial explícita')
        else:
            require(v['nine_incidence'] == 'not-nine', 'clasificación de 9 en otro dígito')
        visits[v['id']] = {**v, 'raw': raw, 'digit': digit, 'quotient9': quotient}
        arithmetic.append({'id':v['id'], 'raw':raw, 'digit':digit, 'quotient9':quotient})
        if t <= 108:
            m = (t-1)//9
            counts[m][0] += mult * (digit in (1,3,5,7))
            if digit == 9:
                counts[m][2] += mult * (1 if v['nine_incidence']=='crown' else -1)
    for route in routes:
        ticks = [v['tick'] for v in visits.values() if v['route']==route]
        require(len(ticks) == len(set(ticks)), 'tick duplicado en '+route)
        require(set(range(1,109)).issubset(ticks), 'historia de 108 pasos incompleta: '+route)
    ids = set()
    trace_records = []
    for tr in data['traces120']:
        exact_keys(tr, ('id','window','members','multiplicity','length_unit',
                       'length_unit_owner'), 'traza120')
        require(isinstance(tr['id'], str) and tr['id'] not in ids, 'traza repetida')
        ids.add(tr['id'])
        m = integer(tr['window'], 'ventana')
        require(1 <= m <= 12, 'ventana de traza fuera del dominio')
        members = tr['members']
        require(isinstance(members, list) and members, 'traza sin miembros')
        require(all(key in visits for key in members), 'miembro de traza ausente')
        unit = positive(tr['length_unit'], 'unidad de longitud reducida')
        require(isinstance(tr['length_unit_owner'],str) and tr['length_unit_owner'].strip(),
                'la conversión de longitud necesita procedencia explícita')
        # Se distinguen número de incidencias y longitud reducida. El programa
        # no identifica por omisión120con120ticks del calendario108.
        length = len(members)*unit
        require(length % 120 == 0 and (length//120-1) % 3 == 0,
                'longitud distinta de 120(1+3j)')
        jtrace = (length//120-1)//3
        events = [visits[key] for key in members]
        require(len({e['route'] for e in events}) == 1, 'traza atraviesa rutas distintas')
        require(all(b['tick'] == a['tick']+1 for a,b in zip(events, events[1:])),
                'traza no consecutiva')
        require((m-1)*9+1 <= events[0]['tick'] <= m*9, 'origen fuera de su ventana')
        orientation_sum = sum(e['trit'] for e in events)
        orientation = sign(orientation_sum)
        require(orientation != 0, 'traza neutral: no se asigna un canal por defecto')
        mult = positive(tr['multiplicity'], 'multiplicidad de traza')
        counts[m-1][1] -= mult * orientation
        trace_records.append({'id':tr['id'], 'window':m, 'j':jtrace,
                              'length':length, 'members_count':len(members),
                              'length_unit':unit,'length_unit_owner':tr['length_unit_owner'],
                              'channel':orientation,
                              'trit_sum':orientation_sum, 'multiplicity':mult})
    coverage = data['trace_coverage']
    exact_keys(coverage, ('finite_support', 'proof_locator', 'enumeration_id'), 'cobertura')
    require(coverage['finite_support'] is True,
            'el recuento entero requiere soporte finito o una construcción distinta explícita')
    require(all(isinstance(coverage[k],str) and coverage[k].strip()
                for k in ('proof_locator','enumeration_id')), 'cobertura no documentada')
    out = channels_from_counts(counts)
    out.update({
        'status':'PASS_COMPILACION_INCIDENCIAL_CON_DATOS_DECLARADOS',
        'canonical_E108_produced':False,
        'scope':'Evaluación del funcional sobre las incidencias suministradas; no selección canónica de ellas',
        'target_values_used':False,
        'ledger_provenance':prov, 'trace_coverage_declaration':coverage,
        'coverage_declaration_is_verified_proof':False,
        'observations_count':len(visits), 'traces_count':len(trace_records),
        'trace_records':trace_records, 'arithmetic_visits':arithmetic,
    })
    return out


def invert_transverse(b3, b4, total):
    """Control posterior de inyectividad; nunca se usa en compile_ledger."""
    d = {0:0}
    pending = [0]
    while pending:
        m = pending.pop()
        for step, b in ((3,b3),(4,b4)):
            n, value = (m+step)%12, d[m]-b[m]
            if n in d:
                require(d[n]==value, 'canales incompatibles')
            else:
                d[n]=value
                pending.append(n)
    origin = Fraction(total-sum(d.values()),12)
    require(origin.denominator==1, 'carga incompatible con integralidad')
    return [int(origin)+d[m] for m in range(12)]


def self_test():
    # Un ejemplo estructural de prueba; no es una semilla canónica de alfa.
    data={'schema':'HMT_INCIDENCE_LEDGER_12_V1',
          'provenance':{k:'EXEMPLE_DE_TEST_NON_CANONIQUE' for k in
                        ('ledger_owner','family_selector','boundary_operator',
                         'trace_generator','trit_operator')},
          'routes':['r'], 'visits':[], 'traces120':[],
          'trace_coverage':{'finite_support':True,'proof_locator':'TEST_ONLY',
                            'enumeration_id':'TEST_ONLY'}}
    for t in range(1,229):
        data['visits'].append({'id':str(t),'route':'r','tick':t,'i':1,'j':2,
                               'sheet':'sum','trit':1,'multiplicity':1,
                               'nine_incidence':'not-nine'})
    data['traces120']=[{'id':'r120','window':1,'members':[str(t) for t in range(1,121)],
                       'multiplicity':1,'length_unit':1,'length_unit_owner':'TEST_ONLY'}]
    out=compile_ledger(data)
    require(out['raw_counts_A_C_9'][0]==[9,-1,0], 'comptage exact')
    require(invert_transverse(out['b90'],out['b120'],out['Q'])==out['blocks_generated'],
            'inversión posterior')
    # Identidad exacta del núcleo: cada una de las 36 coordenadas módulo10
    # es esencial. Ensayo en cada generador y sus traslaciones de diez.
    zero=[[0,0,0] for _ in range(12)]
    ref=channels_from_counts(zero)
    essential=0
    for m,a in product(range(12),range(3)):
        changed=deepcopy(zero); changed[m][a]=1
        shifted=deepcopy(zero); shifted[m][a]=10
        x,y=channels_from_counts(changed),channels_from_counts(shifted)
        require((x['b90'],x['b120'],x['Q'])!=(ref['b90'],ref['b120'],ref['Q']),
                'coordenada esencial')
        require((y['b90'],y['b120'],y['Q'])==(ref['b90'],ref['b120'],ref['Q']),
                'núcleo módulo10')
        essential+=1
    conjugation_cases=0
    for a,c,v in product(range(10),repeat=3):
        n=[[a,c,v] for _ in range(12)]
        ni=conjugate_counts(n)
        x,y=channels_from_counts(n),channels_from_counts(ni)
        require(y['blocks_generated'][0]==x['blocks_generated'][0]+100*(c!=0)-20*c,
                'conjugación decimal exacta')
        require(conjugate_counts(ni)==n, 'involución de recuentos')
        conjugation_cases+=1
    negatives=0
    for mutate in (
        lambda d:d.pop('trace_coverage'),
        lambda d:d['provenance'].pop('trace_generator'),
        lambda d:d['visits'][0].pop('multiplicity'),
        lambda d:d['visits'][0].update(nine_incidence='crown'),
        lambda d:d['traces120'][0].update(members=['1']),
        lambda d:d['trace_coverage'].update(finite_support=False),
        lambda d:d['visits'].pop(0),
        lambda d:d.update(K=[0]*12),
    ):
        bad=deepcopy(data);mutate(bad)
        try:
            compile_ledger(bad)
        except IncidenceError:
            negatives+=1
        else:
            raise IncidenceError('entrada incompleta no rechazada')
    return {'status':'PASS_TESTS_COMPILATEUR_INCIDENCIEL', 'essential_residues':essential,
            'negative_tests':negatives, 'conjugation_digit_cases':conjugation_cases,
            'canonical_E108_produced':False,
            'example_is_synthetic':True, 'target_values_used':False,
            'proven_theorem':'E(n)=E(n_prime) iff n-n_prime belongs to 10 Z^36',
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--incidences',type=Path)
    action.add_argument('--self-test',action='store_true')
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    result=self_test() if args.self_test else compile_ledger(json.loads(args.incidences.read_text()))
    if args.incidences:
        result['input_sha256']=sha256(args.incidences.read_bytes()).hexdigest()
    if args.receipt:
        args.receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='arithmetic_visits'},
                     ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
