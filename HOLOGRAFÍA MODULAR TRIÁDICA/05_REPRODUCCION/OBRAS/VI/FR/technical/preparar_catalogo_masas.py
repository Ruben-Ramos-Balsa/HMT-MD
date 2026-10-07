#!/usr/bin/env python3
"""Conservación documental del catálogo de VI; no es un generador de masas.

Uso: python3 -I -S technical/preparar_catalogo_masas.py [--check] [--self-test]
Las cadenas numéricas, estados, vacíos y duplicados se conservan literalmente.
--check reconstruye en memoria las salidas esperadas y no escribe archivos.
Ningún módulo científico externo se importa, ni se consulta la red.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import csv
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import sys


DEFAULT_REV2 = Path('/Users/ruben/Documents/New project/PUBLICACION_HMT/TEORIA_HOLOGRAFICA_INTEGRAL_MASA_HMT_MD_REV2_2026-08-20')
DEFAULT_INTEGRAL = Path('/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito')
OUT = Path(__file__).resolve().parent
SPECS = (
    ('celdas', 'datos/canon/resultados/atlas_celdas_81_con_lectores.tsv', 81, 'INTERNAL_ATLAS'),
    ('familias', 'datos/canon/resultados/familias_ruta_56_con_espectros.tsv', 56, 'INTERNAL_ROUTE_FAMILIES'),
    ('multisecciones', 'datos/canon/resultados/operadores_multiseccion_13.tsv', 13, 'INTERNAL_MULTISECTIONS'),
    ('rutas', 'datos/canon/resultados/rutas_324_unificadas.tsv', 324, 'INTERNAL_ORIENTED_ROUTES'),
    ('rutas_enriquecidas', 'datos/canon/resultados/rutas_324_enriquecidas.tsv', 324, 'INTERNAL_ENRICHED_ROUTES'),
    ('sectores', 'datos/canon/resultados/sectores_23_desarrollo.tsv', 23, 'DOCUMENTED_SECTOR_CLASSIFICATION'),
    ('soportes', 'datos/canon/resultados/soportes_sectoriales_23.tsv', 23, 'DOCUMENTED_SECTOR_SUPPORTS'),
    ('clases', 'datos/canon/tabla_completa_masas_hmt_sm.tsv', 23, 'DOCUMENTED_CLASSES_AND_COMPARISONS'),
    ('clases_publicas', 'datos/canon/tabla_comparativa_masas_publica.tsv', 23, 'DOCUMENTED_HUMAN_PRESENTATION'),
    ('evaluaciones_e3', 'datos/canon/refinamiento_torres_e3_beta.tsv', 10, 'DOCUMENTED_SIGNATURE_CONDITIONED_EVALUATIONS'),
    ('masas', 'datos/canon/resultados/inventario_masas_471_desarrollo.tsv', 471, 'EXTERNAL_MASS_INVENTORY'),
    ('anchuras', 'datos/canon/resultados/inventario_anchuras_384_desarrollo.tsv', 384, 'EXTERNAL_WIDTH_INVENTORY'),
    ('resumen_fuente', 'datos/canon/resultados/resumen_inventario_471_384.tsv', 6, 'DOCUMENTED_INVENTORY_SUMMARY'),
    ('malla_historica', 'datos/historicos/malla_resonancias_extendida_v8.csv', 12, 'HISTORICAL_COMPARISON_ONLY'),
)
INVENTORY_TEX = 'integracion_83/masas_p0/tex/apendice_inventario_471_384_sucesor.tex'
COMPARISON_TEX = 'integracion_83/masas_p0/corpus/source/masas/19_comparacion_cuantitativa_posterior.tex'
META_FIELDS = ['_catalog_source', '_catalog_ordinal', '_catalog_role', '_catalog_key_occurrence']


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def csv_bytes(fields: list[str], rows: list[list[str]]) -> bytes:
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(fields)
    writer.writerows(rows)
    return stream.getvalue().encode('utf-8')


def parse_table(raw: bytes, delimiter: str) -> tuple[list[str], list[list[str]]]:
    rows = list(csv.reader(io.StringIO(raw.decode('utf-8'), newline=''), delimiter=delimiter))
    if not rows:
        raise ValueError('Tabla vacía')
    fields, body = rows[0], rows[1:]
    if len(set(fields)) != len(fields):
        raise ValueError('Encabezados repetidos: se requiere representación posicional explícita')
    for ordinal, row in enumerate(body, 1):
        if len(row) != len(fields):
            raise ValueError(f'Anchura irregular en fila {ordinal}: {len(row)} != {len(fields)}')
    return fields, body


def source_document(source_id: str, relative: str, role: str, raw: bytes) -> dict:
    delimiter = ',' if relative.endswith('.csv') else '\t'
    fields, rows = parse_table(raw, delimiter)
    if any(field in fields for field in META_FIELDS):
        raise ValueError('Colisión con metadatos del catálogo')
    key = next((k for k in ('output_id', 'record_id', 'candidate_id', 'id') if k in fields), None)
    key_index = fields.index(key) if key else None
    occurrences: Counter = Counter()
    records = []
    for ordinal, cells in enumerate(rows, 1):
        identity = cells[key_index] if key_index is not None else str(ordinal)
        occurrences[identity] += 1
        records.append({
            'source_ordinal': ordinal,
            'key_occurrence': occurrences[identity],
            'values': dict(zip(fields, cells)),
        })
    exact = Counter(tuple(row) for row in rows)
    return {
        'schema': 'HMT.VI.LITERAL_TABLE.v1',
        'source_id': source_id, 'source_relative_path': relative,
        'causal_role': role, 'source_sha256': sha(raw),
        'source_bytes_base64': base64.b64encode(raw).decode('ascii'),
        'source_delimiter': delimiter, 'fields': fields, 'records': records,
        'row_count': len(rows), 'field_count': len(fields),
        'key_field': key,
        'duplicate_keys': {k: n for k, n in occurrences.items() if n > 1},
        'exact_duplicate_extra_rows': sum(n - 1 for n in exact.values()),
        'blank_cells': sum(cell == '' for row in rows for cell in row),
        'all_values_are_literal_strings': True,
        'deduplication_performed': False,
        'states_reinterpreted': False,
    }


def rows_of(doc: dict) -> list[dict[str, str]]:
    return [r['values'] for r in doc['records']]


def table_output(doc: dict) -> bytes:
    fields = META_FIELDS + doc['fields']
    body = []
    for row in doc['records']:
        body.append([
            doc['source_id'], str(row['source_ordinal']), doc['causal_role'],
            str(row['key_occurrence']),
        ] + [row['values'][field] for field in doc['fields']])
    return csv_bytes(fields, body)


def integral_inventory(raw: bytes) -> list[dict]:
    lines = raw.decode('utf-8').splitlines()
    found = []
    for i, line in enumerate(lines):
        match = re.fullmatch(r'% HMTINV\|(MASS|WIDTH)\|(.+)', line.strip())
        if match:
            if i + 1 >= len(lines):
                raise ValueError('Registro TeX sin fila contigua')
            found.append({
                'observable_kind': match[1], 'output_id': match[2],
                'source_line': i + 1, 'table_line': i + 2,
                'table_row_tex_verbatim': lines[i + 1],
            })
    return found


def combined_observables(docs: dict, tex_records: list[dict]) -> tuple[dict, bytes]:
    locators: dict = defaultdict(list)
    for row in tex_records:
        locators[(row['observable_kind'], row['output_id'])].append(row)
    records = []
    fields = list(dict.fromkeys(docs['masas']['fields'] + docs['anchuras']['fields']))
    for source_id, kind in (('masas', 'MASS'), ('anchuras', 'WIDTH')):
        doc = docs[source_id]
        for record in doc['records']:
            values = record['values']
            if values['observable_kind'] != kind:
                raise ValueError('Tipo inesperado de observable')
            records.append({
                'source_id': source_id,
                'source_ordinal': record['source_ordinal'],
                'key_occurrence': record['key_occurrence'],
                'causal_role': doc['causal_role'],
                'values': dict(values),
                'integral_occurrences': locators[(kind, values['output_id'])],
            })
    # A multiset is used: a duplicate must remain a duplicate, not be collapsed.
    source_keys = Counter((r['values']['observable_kind'], r['values']['output_id']) for r in records)
    tex_keys = Counter((r['observable_kind'], r['output_id']) for r in tex_records)
    if source_keys != tex_keys:
        raise ValueError(f'Inventario TeX y tablas no coinciden: {source_keys - tex_keys}; {tex_keys - source_keys}')
    complete = {
        'schema': 'HMT.VI.COMPLETE_EXTERNAL_INVENTORY.v1',
        'row_count': len(records), 'fields_union': fields, 'records': records,
        'edition': 'PDG 2026 (corte documental conservado)',
        'source_cutoff': '2026-01-15',
        'consultation_date_as_documented_in_integral': '2026-07-26',
        'source_snapshot_sha256': sorted({r['values']['source_snapshot_sha256'] for r in records}),
        'not_an_update_of_PDG': True, 'not_a_prediction_count': True,
        'no_numeric_join_or_nearest_value_matching': True,
    }
    body = [[r['source_id'], str(r['source_ordinal']), r['causal_role'], str(r['key_occurrence'])]
            + [r['values'].get(f, '') for f in fields] for r in records]
    return complete, csv_bytes(META_FIELDS + fields, body)


def documented_evaluations(docs: dict) -> list[dict[str, str]]:
    full = {r['record_id']: r for r in rows_of(docs['clases'])}
    e3 = {r['state_key']: r for r in rows_of(docs['evaluaciones_e3'])}
    order = ['SM-LC-1', 'SM-LC-2', 'SM-LC-3', 'SM-Q-U1', 'SM-Q-D1',
             'SM-Q-U2', 'SM-Q-D2', 'SM-Q-U3', 'SM-Q-D3', 'SM-GA-EM',
             'SM-GA-GL', 'SM-GA-W', 'SM-GA-Z', 'SM-H-1']
    records = []
    for identifier in order:
        row = full[identifier]
        v = {
            'id': identifier, 'name': row['representatives'],
            'internal_table': 'clases', 'internal_source_id': identifier,
            'external_value_verbatim': row['external_value'],
            'external_display_verbatim': row['external_value_text'],
            'external_unit_verbatim': row['external_unit'],
            'external_id_verbatim': row['external_output_id'],
            'external_source_verbatim': row['external_source'],
            'external_scheme_verbatim': row['external_scheme'],
            'external_scale_verbatim': row['external_scale'],
            'source_scalarization_status_verbatim': row['scalarization_status'],
            'source_comparison_status_verbatim': row['comparison_status'],
            'source_owner_verbatim': row['owner'],
            'recalculated_delta_ppm_informative': '',
        }
        if identifier == 'SM-LC-1':
            v.update(hmt_value_verbatim=row['HMT_refined_value_MeV'],
                     hmt_unit='MeV/c^2', type='ELECTRON_BETA',
                     condition='Ruta central y lectores bidireccionales',
                     source_evaluation_status_verbatim=row['HMT_refined_output_description'])
        elif identifier in ('SM-GA-EM', 'SM-GA-GL'):
            v.update(hmt_value_verbatim='0', hmt_unit='MeV/c^2', type='NULL_SECTOR',
                     condition='Carta nula de calibre', source_evaluation_status_verbatim=row['HMT_refined_output_description'])
        elif identifier in e3:
            item = e3[identifier]
            v.update(hmt_value_verbatim=item['mass_E3_beta_MeV'], hmt_unit='MeV/c^2',
                     type='SIGNATURE_CONDITIONED',
                     condition='(' + ','.join(item[k] for k in ('n_A','s_C','k_Delta4','nu120','nu270')) + ')',
                     source_evaluation_status_verbatim=item['evaluation_status'],
                     source_assignment_status_verbatim=item['assignment_status'],
                     source_proof_strength_verbatim=item['proof_strength'],
                     source_reference_locator_verbatim=item['external_reference_locator'])
        else:
            v.update(hmt_value_verbatim=row['conditioned_angular_value_MeV'], hmt_unit='MeV/c^2',
                     type='ANGULAR_CONDITIONED', condition=row['conditioned_descriptor'],
                     source_evaluation_status_verbatim=row['conditioned_status'])
        if identifier.startswith('SM-Q-'):
            v['comparison_type'] = 'REFERENCE_ONLY_SCHEME_AND_SCALE_NOT_SUPPLIED_IN_CUT'
        elif identifier in ('SM-GA-W', 'SM-GA-Z', 'SM-H-1'):
            v['comparison_type'] = 'ARITHMETIC_DIFFERENCE_ONLY_RESONANCE_CONVENTION_NOT_RESOLVED_HERE'
        elif identifier in ('SM-GA-EM', 'SM-GA-GL'):
            v['comparison_type'] = 'NULL_OUTPUT_WITH_LIMIT_OR_NO_REFERENCE'
        else:
            v['comparison_type'] = 'DOCUMENTED_COORDINATE_DIFFERENCE_NOT_GLOBAL_INFERENCE'
        records.append(v)
    for item in rows_of(docs['evaluaciones_e3']):
        if item['domain'] != 'compound':
            continue
        records.append({
            'id': item['state_key'], 'name': item['display_name'],
            'internal_table': 'evaluaciones_e3', 'internal_source_id': item['record_id'],
            'hmt_value_verbatim': item['mass_E3_beta_MeV'], 'hmt_unit': 'MeV/c^2',
            'type': 'COMPOSITE_SIGNATURE_CONDITIONED',
            'condition': '(' + ','.join(item[k] for k in ('n_A','s_C','k_Delta4','nu120','nu270')) + ')',
            'source_evaluation_status_verbatim': item['evaluation_status'],
            'source_assignment_status_verbatim': item['assignment_status'],
            'source_proof_strength_verbatim': item['proof_strength'],
            'source_reference_locator_verbatim': item['external_reference_locator'],
            'external_value_verbatim': item['external_reference_MeV'],
            'external_display_verbatim': item['external_reference_MeV'],
            'external_unit_verbatim': 'MeV',
            'comparison_type': 'DOCUMENTED_COMPOSITE_REFERENCE_METADATA_NOT_COMPLETED_HERE',
            'recalculated_delta_ppm_informative': '',
        })
    if len(records) != 20:
        raise ValueError(f'Esperadas 20 evaluaciones documentadas, halladas {len(records)}')
    with localcontext() as context:
        context.prec = 110
        for row in records:
            if row['type'] == 'NULL_SECTOR' or row['id'].startswith('SM-Q-'):
                continue
            external = row['external_value_verbatim']
            unit = row['external_unit_verbatim']
            if external and unit in ('MeV', 'GeV'):
                value = Decimal(external) * (Decimal(1000) if unit == 'GeV' else Decimal(1))
                if value:
                    row['recalculated_delta_ppm_informative'] = str((Decimal(row['hmt_value_verbatim']) / value - 1) * 1000000)
    return records


def self_tests() -> list[str]:
    tests = []
    raw = b'id\tx\tstatus\nA\t0.0100\tCONDITIONED\nA\t0.0100\tCONDITIONED\nB\t\tUNAVAILABLE\n'
    doc = source_document('test', 'test.tsv', 'TEST', raw)
    assert doc['row_count'] == 3 and doc['duplicate_keys'] == {'A': 2}
    assert doc['exact_duplicate_extra_rows'] == 1
    assert [r['key_occurrence'] for r in doc['records']] == [1, 2, 1]
    tests.append('duplicate_rows_and_occurrence_indices_preserved')
    assert doc['records'][0]['values']['x'] == '0.0100'
    assert doc['records'][2]['values']['x'] == ''
    assert doc['records'][0]['values']['status'] == 'CONDITIONED'
    tests.append('decimal_text_blanks_and_original_status_preserved')
    assert base64.b64decode(doc['source_bytes_base64']) == raw
    tests.append('original_bytes_recoverable')
    fields, rows = parse_table(table_output(doc), ',')
    assert [r[4:] for r in rows] == [['A', '0.0100', 'CONDITIONED'], ['A', '0.0100', 'CONDITIONED'], ['B', '', 'UNAVAILABLE']]
    tests.append('csv_round_trip_is_lossless')
    try:
        parse_table(b'a\tb\n1\n', '\t')
    except ValueError:
        tests.append('malformed_row_rejected')
    else:
        raise AssertionError('Malformed row was accepted')
    # Counterexample to identifying scalar compression with spectral purity:
    # M=diag(1,3), P=|v><v|, v=(1,1)/sqrt(2). Work over Q through P.
    half = Fraction(1, 2)
    projector = ((half, half), (half, half))
    mass = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(3)))
    def product(a, b):
        return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                           for j in range(2)) for i in range(2))
    mp = product(mass, projector)
    pmp = product(projector, mp)
    two_p = tuple(tuple(2 * x for x in row) for row in projector)
    mean = sum(product(projector, mass)[i][i] for i in range(2))
    second = sum(product(projector, product(mass, mass))[i][i] for i in range(2))
    assert pmp == two_p and mp != two_p
    assert mean == 2 and second - mean * mean == 1
    tests.append('scalar_compression_counterexample_mean_2_variance_1_exact_rational')
    return tests


def check_section(evaluations: list[dict]) -> tuple[dict, list[str]]:
    path = OUT.parent / 'sections' / '07_contraste_metrologico.tex'
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    printed = re.findall(r'^\\\([^&]*?\\\)\s*&\s*\\\((.*?)\\\)\s*&', text, re.M)
    if len(printed) != 20:
        raise ValueError(f'La sección debe presentar 20 coordenadas, halladas {len(printed)}')
    with localcontext() as context:
        context.prec = 110
        for value, source in zip(printed, evaluations):
            normalized = value.replace('\\allowbreak', '').replace(' ', '')
            decimal_places = len(normalized.partition('.')[2])
            quantum = Decimal(1).scaleb(-decimal_places)
            if Decimal(normalized) != Decimal(source['hmt_value_verbatim']).quantize(quantum):
                raise ValueError(f'Coordenada tipográfica no conciliada: {source["id"]}')
    stack = []
    for action, environment in re.findall(r'\\(begin|end)\{([^}]+)\}', text):
        if action == 'begin':
            stack.append(environment)
        elif not stack or stack.pop() != environment:
            raise ValueError(f'Entorno LaTeX no balanceado: {environment}')
    if stack:
        raise ValueError(f'Entornos LaTeX sin cierre: {stack}')
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    if len(labels) != len(set(labels)):
        raise ValueError('Etiquetas duplicadas en la sección')
    return {'path': 'sections/07_contraste_metrologico.tex', 'sha256': sha(raw), 'numeric_rows': len(printed),
            'layout_rendered': False}, [
        'section_20_numeric_coordinates_match_literal_source_at_printed_precision',
        'section_latex_environments_balanced_and_labels_unique',
    ]


def build(rev2: Path, integral: Path) -> dict[str, bytes]:
    outputs: dict[str, bytes] = {}
    docs = {}
    sources = []
    checks = self_tests()
    for identifier, relative, expected, role in SPECS:
        path = rev2 / relative
        raw = path.read_bytes()
        doc = source_document(identifier, relative, role, raw)
        if doc['row_count'] != expected:
            raise ValueError(f'{identifier}: {doc["row_count"]} filas, esperadas {expected}')
        docs[identifier] = doc
        outputs[f'catalogo_{identifier}.json'] = json_bytes(doc)
        outputs[f'catalogo_{identifier}.csv'] = table_output(doc)
        # Test emitted CSV against every original field of every record.
        fields, rows = parse_table(outputs[f'catalogo_{identifier}.csv'], ',')
        assert fields[4:] == doc['fields']
        assert [r[4:] for r in rows] == [[r['values'][f] for f in doc['fields']] for r in doc['records']]
        assert base64.b64decode(doc['source_bytes_base64']) == raw
        checks.append(f'{identifier}:all_fields_rows_order_status_and_bytes_preserved')
        sources.append({k: doc[k] for k in ('source_id','source_relative_path','source_sha256','row_count','field_count','causal_role','duplicate_keys','exact_duplicate_extra_rows')})
    inventory_raw = (integral / INVENTORY_TEX).read_bytes()
    comparison_raw = (integral / COMPARISON_TEX).read_bytes()
    tex_records = integral_inventory(inventory_raw)
    complete, csv_complete = combined_observables(docs, tex_records)
    outputs['catalogo_observables.json'] = json_bytes(complete)
    outputs['catalogo_observables.csv'] = csv_complete
    checks.append('855_external_records_match_integral_tex_as_multiset')
    comparison_text = comparison_raw.decode('utf-8')
    active_text = comparison_text.split('\\endinput', 1)[0]
    documented_ids = re.findall(r'Identificador catalográfico:\} ([A-Z0-9-]+)\.', active_text)
    evaluations = documented_evaluations(docs)
    if Counter(documented_ids) != Counter(r['id'] for r in evaluations):
        raise ValueError('Las 20 evaluaciones no corresponden al propietario activo del integral')
    section, section_checks = check_section(evaluations)
    checks.extend(section_checks)
    eval_fields = list(dict.fromkeys(key for row in evaluations for key in row))
    outputs['catalogo_evaluaciones_documentadas.json'] = json_bytes({
        'schema': 'HMT.VI.DOCUMENTED_EVALUATIONS.v1', 'records': evaluations,
        'not_new_mass_derivations': True, 'historic_conditional_statuses_preserved': True,
        'comparison_tex_sha256': sha(comparison_raw),
        'excluded_from_active_comparison_after_endinput': True,
    })
    outputs['catalogo_evaluaciones_documentadas.csv'] = csv_bytes(eval_fields, [[r.get(f, '') for f in eval_fields] for r in evaluations])
    checks.append('20_documented_evaluations_match_active_integral_before_endinput')
    counts = Counter((r['values']['HMT_target_sector'], r['values']['observable_kind']) for r in complete['records'])
    sectors = sorted({s for s, _ in counts})
    summary = [{'sector_original': s, 'masas': str(counts[s, 'MASS']), 'anchuras': str(counts[s, 'WIDTH'])} for s in sectors]
    outputs['catalogo_resumen_sectores.json'] = json_bytes({'records': summary, 'counts_are_external_observables_not_predictions': True})
    outputs['catalogo_resumen_sectores.csv'] = csv_bytes(['sector_original','masas','anchuras'], [[r['sector_original'],r['masas'],r['anchuras']] for r in summary])
    status_counts = {}
    for source_id in ('masas', 'anchuras', 'sectores', 'evaluaciones_e3'):
        doc = docs[source_id]
        status_fields = [f for f in doc['fields'] if any(word in f.lower() for word in ('status', 'strength', 'authorization'))]
        status_counts[source_id] = {f: dict(Counter(r[f] for r in rows_of(doc))) for f in status_fields}
    outputs['catalogo_estados_originales.json'] = json_bytes(status_counts)
    # This is a documentary manifest, not a theorem or prediction certificate.
    manifest = {
        'schema': 'HMT.VI.DOCUMENTARY_CATALOG_MANIFEST.v1',
        'scope': 'Literal conservation and typed presentation of frozen source records',
        'provenance': 'RESULTADO_RECUPERADO; CERTIFICADO_NUEVO documental',
        'canonical_rev2_root': str(DEFAULT_REV2),
        'canonical_integral_manuscript_root': str(DEFAULT_INTEGRAL),
        'relocated_source_roots_allowed_if_bytes_identical': True,
        'builder_sha256': sha(Path(__file__).read_bytes()),
        'sources': sources,
        'integral_sources': [
            {'path': INVENTORY_TEX, 'sha256': sha(inventory_raw), 'records': len(tex_records)},
            {'path': COMPARISON_TEX, 'sha256': sha(comparison_raw), 'active_evaluations': len(documented_ids)},
        ],
        'internal_cardinalities': {'cells':81,'route_families':56,'multisections':13,'oriented_routes':324},
        'external_observables': {'mass':471,'width':384},
        'public_classification_rows':23,
        'documented_numeric_presentations':dict(Counter(r['type'] for r in evaluations)),
        'no_new_external_sources':True, 'no_network':True,
        'no_deduplication':True, 'no_numerical_matching':True,
        'section_control': section,
        'preservation_checks':checks,
        'check_count':len(checks),
        'outputs':{name:{'sha256':sha(data),'bytes':len(data)} for name,data in sorted(outputs.items())},
        'control_scope_exclusion':'Does not certify global mathematical completeness, causal independence of the original generators, or physical prediction status.',
        'status':'PASS_CATALOGO_DOCUMENTAL_VI',
    }
    outputs['catalogo_manifiesto.json'] = json_bytes(manifest)
    # Check that no source was changed during catalog preparation.
    for source in sources:
        if sha((rev2 / source['source_relative_path']).read_bytes()) != source['source_sha256']:
            raise ValueError('Fuente modificada durante la lectura')
    if (integral / INVENTORY_TEX).read_bytes() != inventory_raw or (integral / COMPARISON_TEX).read_bytes() != comparison_raw:
        raise ValueError('Propietario integral modificado durante la lectura')
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rev2-root', type=Path, default=DEFAULT_REV2)
    parser.add_argument('--integral-root', type=Path, default=DEFAULT_INTEGRAL)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps({'self_tests':self_tests()}, ensure_ascii=False))
        if not args.check:
            return 0
    outputs = build(args.rev2_root, args.integral_root)
    for name, data in outputs.items():
        if not re.fullmatch(r'catalogo_[a-z0-9_]+\.(json|csv)', name):
            raise ValueError('Destino fuera del ámbito autorizado')
        target = OUT / name
        if args.check:
            if not target.exists() or target.read_bytes() != data:
                raise ValueError(f'Salida divergente o ausente: {name}')
        else:
            target.write_bytes(data)
    manifest = json.loads(outputs['catalogo_manifiesto.json'])
    print(json.dumps({'status':manifest['status'],'files':len(outputs),
                      'checks':manifest['check_count'],'read_only':args.check}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, AssertionError, OSError) as exc:
        print(f'FAIL_CATALOGO_DOCUMENTAL_VI: {exc}', file=sys.stderr)
        raise SystemExit(1)
