#!/usr/bin/env python3
"""Relocaliza los recibos S0 REV07 sin volver a formular su contenido.

Sólo escribe el directorio nuevo genealogia_s0_rev04. Ensambla el main real,
conserva los rangos desplazados de REV07 y ejecuta los dos validadores focales.
No ejecuta campañas algebraicas ni edita fuentes, registros o recibos anteriores.
"""
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('/Users/ruben/Documents/New project')
EXPECTED = PROJECT / 'output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/VII_GRAVITACION'
OLD = PROJECT / 'output/ARTICULO_VII_REV07_EDICION_INTEGRADA_20260910'
BASE = ROOT / 'gestion/genealogia_s0_rev07'
OUT = ROOT / 'gestion/genealogia_s0_rev04'
HELPER = PROJECT / 'output/ARTICULO_II_REV09_ENTREGA_20260910/herramientas_portables.py'


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def loc(path):
    return {'path': str(path), 'sha256': sha(path)}


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    require(ROOT == EXPECTED, 'Raíz distinta de la sucesora autorizada.')
    require(not OUT.exists(), 'El directorio ya existe: preservar el corte previo.')
    names = ('RECIBO_GENEALOGIA_S0.json', 'RECIBO_CONSTANTES_S0.json')
    originals = {name: load(BASE / name) for name in names}
    for name in names:
        require(sha(BASE / name) == sha(OLD / 'gestion/genealogia_s0_rev07' / name),
                'La copia del recibo REV07 difiere de su propietario: ' + name)
    owners = originals[names[1]]['material_owners']
    for key, item in owners.items():
        old = Path(item['path'])
        current = ROOT / old.relative_to(OLD)
        require(old.read_bytes() == current.read_bytes() and sha(current) == item['sha256'],
                'Propietario S0 no idéntico: ' + key)

    relocated, kept = {}, {}

    def translate_path(value, expected_hash=None):
        old = Path(value)
        if not old.is_absolute() or not old.is_relative_to(OLD):
            return value
        require(old.is_file(), 'Propietario anterior ausente: ' + value)
        digest = sha(old)
        require(expected_hash is None or digest == expected_hash, 'Huella anterior alterada: ' + value)
        current = ROOT / old.relative_to(OLD)
        if current.is_file() and current.read_bytes() == old.read_bytes():
            relocated[value] = {'before': value, 'after': str(current), 'sha256': digest,
                                'byte_identical': True, 'line_ranges_changed': False}
            return str(current)
        kept[value] = {'path': value, 'sha256': digest, 'reason': 'Sin copia local idéntica; se conserva el testigo histórico.'}
        return value

    def rebind(value):
        if isinstance(value, dict):
            result = {key: rebind(item) for key, item in value.items() if key != 'path'}
            if 'path' in value:
                path = Path(value['path'])
                if 'sha256' in value:
                    require(path.is_file() and sha(path) == value['sha256'], 'Localizador heredado no verificable: ' + str(path))
                result['path'] = translate_path(value['path'], value.get('sha256'))
            return result
        if isinstance(value, list):
            return [rebind(item) for item in value]
        if isinstance(value, str) and value.startswith(str(OLD) + '/'):
            return translate_path(value)
        return value

    genealogy = rebind(originals[names[0]])
    constants = rebind(originals[names[1]])
    module_spec = importlib.util.spec_from_file_location('rev04_readonly_assembly', HELPER)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    assembled = module.assemble(ROOT / 'manuscrito')
    sources = [loc(path) for path in assembled['files']]
    for item in constants['material_owners'].values():
        require(Path(item['path']) in assembled['files'], 'Propietario no incluido en main real: ' + item['path'])
    anchors, cursor = [], -1
    for old_anchor in originals[names[0]]['artifact']['anchors']:
        anchor = copy.deepcopy(old_anchor)
        index = assembled['text'].find(anchor['text'], cursor + 1)
        require(index >= 0, 'Ancla heredada ausente o fuera de orden: ' + anchor['stage'])
        anchor['line'] = assembled['text'][:index].count('\n') + 1
        anchors.append(anchor)
        cursor = index

    OUT.mkdir()
    composite = OUT / 'FUENTE_COMPUESTA_VII.tex.txt'
    write(composite, assembled['text'])
    genealogy['artifact'] = {**copy.deepcopy(originals[names[0]]['artifact']), **loc(composite), 'anchors': anchors}
    genealogy['receipt_id'] = originals[names[0]]['receipt_id'] + '_REV04_20260911'
    genealogy['provenance'] = 'RESULTADO_RECUPERADO'
    binding = {
        'revision': 'SERIE_REV04_20260911',
        'prior_genealogy_receipt': loc(BASE / names[0]),
        'prior_constants_receipt': loc(BASE / names[1]),
        'prior_editorial_revision': originals[names[0]]['editorial_revision'],
        'local_owner_sources_byte_identical_to_rev07': True,
        'rev07_line_ranges_preserved_without_new_shift': True,
        'new_scientific_proof': False,
        'new_pdf_is_global_hmt_demonstration': False,
        'reader_80_covered_by_s0': False,
        'reader_80_review': 'Revisión focal independiente, no certificada por estos recibos S0.',
        'inherited_algebraic_runs_reexecuted': False,
        'scope': 'Nueva vinculación documental de S0 recuperado; contenido, dominios e hipótesis focales REV07 inalterados.'
    }
    genealogy['documentary_successor'] = copy.deepcopy(binding)
    constants['documentary_successor'] = copy.deepcopy(binding)
    constants['provenance'] = 'RESULTADO_RECUPERADO'
    constants['local_artifact_sha256'] = sha(constants['artifact'])
    write(OUT / names[0], genealogy)
    write(OUT / names[1], constants)
    write(OUT / 'VINCULACION_FOCAL_VII.json', {
        'schema': 'hmt.vii.s0.documentary_successor_binding.v1',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        **binding, 'main': loc(ROOT / 'manuscrito/main.tex'), 'helper': loc(HELPER),
        'producer': loc(Path(__file__)), 'source_count': len(sources), 'sources': sources,
        'edges': assembled['edges'], 'undefined_references': assembled['undefined_references'],
        'duplicate_labels': assembled['duplicate_labels'],
        'relocated_byte_identical_references': list(relocated.values()),
        'kept_historical_references': list(kept.values()),
        'anchors_before': originals[names[0]]['artifact']['anchors'], 'anchors_after': anchors,
        'artifact': loc(composite), 'mathematical_claims_changed': False,
        'manuscript_or_canonical_registry_modified': False
    })
    commands = [
        ([sys.executable, '-I', '-S', '-B', str(PROJECT / 'tools/verificar_genealogia_unica_hmt.py'),
          '--receipt', str(OUT / names[0])], 'PASS_GENEALOGIA_UNICA_APP_TRIT_TPK'),
        ([sys.executable, '-I', '-S', '-B', '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
          '--audit', constants['artifact'], '--receipt', str(OUT / names[1])], 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY')
    ]
    results = []
    for command, expected in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        lines = result.stdout.splitlines()
        results.append({'command': command, 'returncode': result.returncode, 'stdout': result.stdout,
                        'stderr': result.stderr, 'expected': expected,
                        'passed': result.returncode == 0 and bool(lines) and lines[-1].startswith(expected)})
        print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, file=sys.stderr, end='')
    unchanged = all(sha(item['path']) == item['sha256'] for item in sources)
    passed = all(item['passed'] for item in results) and unchanged
    write(OUT / 'VALIDACION_FOCAL_VII.json', {
        'status': 'PASS_VINCULACION_FOCAL_S0_REV04' if passed else 'FAIL_VINCULACION_FOCAL_S0_REV04',
        'validated_at_utc': datetime.now(timezone.utc).isoformat(), 'results': results,
        'sources_unchanged_during_validation': unchanged,
        'genealogy_receipt': loc(OUT / names[0]), 'constants_receipt': loc(OUT / names[1]),
        'binding': loc(OUT / 'VINCULACION_FOCAL_VII.json'),
        'whole_article_mathematically_certified': False, 'reader_80_covered_by_s0': False,
        'algebraic_checks_reexecuted': False
    })
    write(OUT / 'README.md', '# Recibos focales S0 REV04\n\n'
          'Relocalización documental de RESULTADO_RECUPERADO: los siete propietarios locales son byteidénticos a REV07. '
          'Se conservan exactamente sus rangos corregidos y se ensambla el main actual para ligar huella y anclas.\n\n'
          'Los resultados reales de las dos puertas están en VALIDACION_FOCAL_VII.json. '
          'Su alcance es el contrato genealógico/causal focal de S0; no una nueva prueba global HMT, '
          'ni una certificación integral del PDF, ni una prueba de los lectores añadidos a 80. '
          'No se reejecutaron campañas algebraicas y no se editaron manuscritos o registros canónicos.\n')
    print('PASS_VINCULACION_FOCAL_S0_REV04' if passed else 'FAIL_VINCULACION_FOCAL_S0_REV04')
    print(str(OUT))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
