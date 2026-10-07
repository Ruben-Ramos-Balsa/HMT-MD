#!/usr/bin/env python3
"""Assemble the frozen selected I–V consumers without changing their owners."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
I_BASE = WORK / 'output/PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922'
FORMAL = WORK / 'output/AMPLIACION_FORMAL_LEAN_SERIE_20260916'
PRINCIPAL = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916')
IV = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/ENTREGA_ARTICULO_IV_PANTALLAS_SELECCIONADAS_20260922')
PARENT_SHA = '1c0b6133b4a17367294542ee21c750d9d824f9ca741473e32add034261c1ac28'
TARGETS = {
    'I': ['ArticleIExceptionalInterface', 'ArticleIPrincipalPublication'],
    'II': ['SelectedCKMPublication', 'SelectedActionGravityThermal',
           'SelectedAreaInformation', 'SelectedGravitationalArea', 'SelectedPentadicTensor'],
    'III': ['SelectedConstitutivePublication'],
    'IV': ['ArticleIVSelectedScreens'],
    'V': ['SelectedThermalPublication', 'SelectedBoltzmannRadiation'],
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def imports(path):
    text = Path(path).read_text()
    text = re.sub(r'/\-.*?\-/', '', text, flags=re.S)
    result = []
    for line in text.splitlines():
        if line.strip().startswith('import '):
            result.extend(line.split('--', 1)[0].strip().split()[1:])
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--plan-only', action='store_true')
    args = ap.parse_args()
    out = args.out.resolve()
    require(sha(I_BASE / 'MANIFIESTO.json') == PARENT_SHA, 'Different Article I edition')
    parent_manifest = read(I_BASE / 'MANIFIESTO.json')
    for rel, digest in parent_manifest['files'].items():
        require(sha(I_BASE / rel) == digest, 'Changed I artifact: ' + rel)
    base = read(I_BASE / 'REGISTRO_REPRODUCCION.json')
    modules = {}
    for name, row in base['modules'].items():
        modules[name] = dict(source=I_BASE / row['source'], object=I_BASE / row['object'],
                             origin='preserved_I', source_sha256=row['source_sha256'],
                             object_sha256=row['object_sha256'])

    candidates = {}

    def add(name, source, obj, origin):
        source, obj = Path(source), Path(obj)
        require(source.is_file(), 'Missing source ' + str(source))
        require(obj.is_file(), 'Missing object ' + str(obj))
        row = dict(source=source, object=obj, origin=origin,
                   source_sha256=sha(source), object_sha256=sha(obj))
        if name in modules:
            require(modules[name]['source_sha256'] == row['source_sha256'],
                    'Shared source conflict: ' + name)
            return
        if name in candidates:
            require(candidates[name]['source_sha256'] == row['source_sha256'],
                    'Ambiguous new source: ' + name)
            return
        candidates[name] = row

    add('ArticleIExceptionalInterface', I_BASE / 'lean/ArticleIExceptionalInterface.lean',
        I_BASE / 'verificacion/ArticleIExceptionalInterface.olean', 'principal_I')
    add('ArticleIPrincipalPublication', I_BASE / 'lean/ArticleIPrincipalPublication.lean',
        I_BASE / 'verificacion_principal/ArticleIPrincipalPublication.olean', 'principal_I')
    ckm = read(HERE / 'II_CENTRAL/CKM_VERIFICATION.json')
    require(ckm['status'] == 'PASS_SELECTED_CKM_PUBLICATION', 'CKM not compiled')
    for row in ckm['modules']:
        require(sha(row['source']) == row['source_sha256'] and
                sha(row['object']) == row['object_sha256'], 'Changed CKM module')
        add(row['module'], row['source'], row['object'], 'CKM_II')
    gravity = read(HERE / 'II_CENTRAL/verification_action_gravity_thermal/VERIFICATION.json')
    require(gravity['status'] == 'PASS_SELECTED_ACTION_GRAVITY_THERMAL', 'Thermal not compiled')
    add('SelectedActionGravityThermal', gravity['source'], gravity['object'], 'selected_II')
    for folder in ['II', 'II_TENSOR', 'III', 'V']:
        for source in sorted((HERE / folder).glob('*.lean')):
            obj = source.with_suffix('.olean')
            if obj.is_file():
                add(source.stem, source, obj, 'delta_' + folder)
    for name in ['ElectricQuanta', 'ActionElectricComposition']:
        add(name, FORMAL / 'angular_constitutive_bridge' / (name + '.lean'),
            HERE / 'III' / (name + '.olean'), 'preserved_III')
    for folder in ['V_FockTransport', 'V_FockBridge', 'V_QuantumOccupations',
                   'V_Radiation', 'V_BosonicMoments', 'V_ThermodynamicLimit']:
        for source in sorted((PRINCIPAL / folder).rglob('*.lean')):
            if source.with_suffix('.olean').is_file():
                name = '.'.join(source.relative_to(PRINCIPAL / folder).with_suffix('').parts)
                add(name, source, source.with_suffix('.olean'), 'preserved_' + folder)

    # The reviewer freezes this exact source/object map after its one reproduction.
    iv_map = HERE / 'IV_FROZEN_MODULES.json'
    if iv_map.exists():
        for name, row in read(iv_map)['modules'].items():
            require(sha(row['source']) == row['source_sha256'] and
                    sha(row['object']) == row['object_sha256'], 'Changed IV module ' + name)
            add(name, row['source'], row['object'], 'selected_IV')

    visiting, resolved = set(), set()
    external = set()

    def resolve(name):
        if name in resolved:
            return
        require(name not in visiting, 'Local import cycle: ' + name)
        if name not in modules:
            require(name in candidates, 'Unresolved local module: ' + name)
            modules[name] = candidates[name]
        visiting.add(name)
        row = modules[name]
        row['imports'] = imports(row['source'])
        for dependency in row['imports']:
            if dependency in base['external_objects'] or dependency == 'Mathlib' or dependency.startswith(('Mathlib.', 'Lean.', 'Std.', 'Batteries.')) or dependency in ('Lean', 'Std'):
                external.add(dependency)
            else:
                resolve(dependency)
        visiting.remove(name)
        resolved.add(name)

    for group in TARGETS.values():
        for name in group:
            resolve(name)
    # Preserve, type and authenticate all 477 shared registered modules, not only
    # the smaller transitive closure of this delivery's targets.
    for name in list(modules):
        resolve(name)
    for name, row in modules.items():
        require(sha(row['source']) == row['source_sha256'], 'Changed source: ' + name)
        require(sha(row['object']) == row['object_sha256'], 'Changed object: ' + name)
    report = dict(module_count=len(modules), targets=TARGETS,
                  new_modules=[n for n in modules if n not in base['modules']],
                  external_imports=sorted(external))
    if args.plan_only:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    require(not out.exists(), 'Output already exists; never overwrite a delivery')
    require((HERE / 'FREEZE_I_V.json').is_file(), 'Coordinator freeze not recorded')
    freeze = read(HERE / 'FREEZE_I_V.json')
    for path, digest in freeze['files'].items():
        require(sha(path) == digest, 'Changed frozen input: ' + path)
    out.mkdir(parents=True)
    shutil.copytree(I_BASE, out / 'base_I')
    registry = dict(compiler=base['compiler'], modules={}, targets=TARGETS,
                    external_objects=base['external_objects'], scope=report)
    external_roots = [PRINCIPAL / 'deps/mathlib4/.lake/build/lib/lean']
    external_roots += sorted((PRINCIPAL / 'deps/mathlib4/.lake/packages').glob('*/.lake/build/lib/lean'))
    external_roots += [Path(base['compiler']['executable']).parent.parent / 'lib/lean']
    for name in external:
        rel = Path(*name.split('.')).with_suffix('.olean')
        path = next((root / rel for root in external_roots if (root / rel).is_file()), None)
        require(path is not None, 'Unresolved external import: ' + name)
        digest = sha(path)
        if name in registry['external_objects']:
            require(registry['external_objects'][name]['sha256'] == digest,
                    'Changed pinned external object: ' + name)
        registry['external_objects'][name] = dict(sha256=digest)
    for name, row in modules.items():
        if row['source'].is_relative_to(I_BASE) and row['object'].is_relative_to(I_BASE):
            source_rel = Path('base_I') / row['source'].relative_to(I_BASE)
            object_rel = Path('base_I') / row['object'].relative_to(I_BASE)
        else:
            source_rel = Path('lean') / Path(*name.split('.')).with_suffix('.lean')
            object_rel = Path('objects') / Path(*name.split('.')).with_suffix('.olean')
            for dest, original in [(source_rel, row['source']), (object_rel, row['object'])]:
                (out / dest).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, out / dest)
        registry['modules'][name] = dict(source=str(source_rel), object=str(object_rel),
            source_sha256=row['source_sha256'], object_sha256=row['object_sha256'],
            imports=row['imports'], origin=row['origin'])
    (out / 'REGISTRO_UNIFICADO.json').write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')
    for folder in ['II', 'II_TENSOR', 'III', 'V', 'II_CENTRAL']:
        shutil.copytree(HERE / folder, out / 'procedencia' / folder,
                        ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(IV, out / 'procedencia/IV',
                    ignore=shutil.ignore_patterns('__pycache__', '.DS_Store'))
    for name in ['FREEZE_I_V.json', 'IV_FROZEN_MODULES.json', 'preparar_entrega.py']:
        shutil.copy2(HERE / name, out / 'procedencia' / name)
    shutil.copy2(HERE / 'ENTREGA_RADION.md', out / 'procedencia/ENTREGA_RADION.md')
    if (HERE / 'procedencia').is_dir():
        shutil.copytree(HERE / 'procedencia', out / 'procedencia/metadata_radion')
    shutil.copy2(HERE / 'reproducir_paquete.py', out / 'reproducir.py')
    shutil.copy2(HERE / 'README_ENTREGA.md', out / 'README.md')
    manifest = dict(schema='hmt.selected-I-V.package.v1', preserved_I_manifest_sha256=PARENT_SHA,
                    module_count=len(modules), targets=TARGETS,
                    pdfs_modified=False, full_classical_FLM_formalization_claimed=False,
                    files={str(p.relative_to(out)): sha(p)
                           for p in sorted(out.rglob('*')) if p.is_file()})
    (out / 'MANIFIESTO.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
