#!/usr/bin/env python3
"""Seal one verified continuation after fields406 and normalization407.

Inputs are explicit SHA-bound receipts, sources and human-approved metadata.
The complete fields406 package is copied once; normalization and the new delta
are separate preserved receipts. No Lean source, object or antecedent receipt
is rewritten. A relocated --plan checks replay without compilation; ZIP sealing
checks CRC and SHA-256 of every entry. --plan creates no delivery.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile
import zlib

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUNNER_SHA = '288b259509c86ef7f89c120ae4daaabef38598fa220be4dfca0fc07c3198d98d'
FOCAL_SHA = '34bdc13bb338c8f5d873c3677ea941fb5bbe7353c97bf314ef8841e781ddb97b'
PREVIOUS_BUILDER_SHA = '2343e575e52b1fb920c675b93278ed5ec8c31825ec65d8e1dd462323d2c9e42d'
HELPER_SHA = '1ab909fed05cd8dfbde1d5d2a65a8caa1a84d88d3b35e9b1d9d1d80f9bb52d84'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path, expected, name):
    import importlib.util
    if sha(path) != expected:
        raise RuntimeError('Changed packaging dependency: '+str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wrapper(requested, normalization=False):
    runner = 'verificar_normalizacion.py' if normalization else 'verificar_continuacion.py'
    defaults = [('base', "root/'antecedente'")]
    if normalization:
        defaults += [('source', "root/'lean/normalization/LatticeTwistedChargeNormalization.lean'"),
                     ('report-dir', "root/'resultados_normalizacion_nuevos'")]
    else:
        defaults += [('source-dir', "root/'lean/continuation'"),
                     ('normalization-report-dir', "root/'recibos/normalizacion'"),
                     ('normalization-verifier', "root/'verificar_normalizacion.py'"),
                     ('report-dir', "root/'resultados_nuevos'")]
    commands = '\n'.join("    ('--"+flag+"', "+value+")," for flag,value in defaults)
    modules = '' if normalization else (
        "if not any(a == '--modules' or a.startswith('--modules=') for a in args):\n"
        "    defaults += ['--modules', *"+repr(requested)+"]\n")
    return '''#!/usr/bin/env python3
"""Explicit replay: connecting a USB does not execute code."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/''' + repr(runner) + '''
spec = importlib.util.spec_from_file_location('hmt_continuation_replay', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args, defaults = sys.argv[1:], []
''' + modules + '''for flag, value in [
''' + commands + '''
]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag, str(value)]
sys.argv = [str(path), *defaults, *args]
raise SystemExit(runner.main())
'''


def reproduction_readme(receipt):
    return f'''# Reproducción de esta continuación

La carpeta y su ZIP tienen el mismo contenido. Descomprima una sola vez si usa
el ZIP. No se ejecuta código al conectar el USB. Desde esta carpeta:

```sh
python3 -I -S reproducir.py --plan --report-dir plan_nuevo
python3 -I -S reproducir.py --report-dir resultados_nuevos
```

La primera orden autentica sin compilar. La segunda reutiliza 407 módulos
autenticados y compila sólo los {len(receipt['modules'])} del incremento,
con un sondeo separado de sus {receipt['public_declaration_count']} declaraciones
públicas. Use un directorio de resultados nuevo en cada ejecución.

La normalización ya comprobada se conserva en `recibos/normalizacion/`; no se
recompila al ejecutar la continuación. Para reproducirla por separado:

```sh
python3 -I -S reproducir_normalizacion.py --report-dir normalizacion_nueva
```

Esta orden compila únicamente su fuente y consulta sus declaraciones. No
sustituye automáticamente el recibo original usado por la continuación.

Se necesita el runtime externo exacto Lean 4.21.0 y Mathlib registrados en
los recibos. Este paquete relocaliza sus fuentes, objetos y rutas internas;
no instala ni descarga el runtime. Sus rutas externas se conservan en los
recibos y deben estar disponibles para esta reproducción. Los objetos
compilados no se declaran independientes de plataforma ni de versión.

`antecedente/` conserva íntegra una sola copia del paquete de 406 módulos.
`lean/normalization/` contiene la fuente normalizadora y `lean/continuation/`
las fuentes del incremento. `recibos/` conserva compilaciones, consultas,
objetos y controles. `README.md` delimita los resultados matemáticos.
El control causal, los hashes y el plan sin compilación no sustituyen una
comprobación Lean ni acreditan por sí solos el producto orbifold o FLM completo.
'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--destination', type=Path, required=True)
    p.add_argument('--verification', type=Path, required=True)
    p.add_argument('--receipt-sha256', required=True)
    p.add_argument('--normalization-verification', type=Path, required=True)
    p.add_argument('--normalization-receipt-sha256', required=True)
    p.add_argument('--source-dir', type=Path, default=HERE)
    p.add_argument('--runner', type=Path, default=HERE/'verify_twisted_continuation.py')
    p.add_argument('--normalization-verifier', type=Path, default=HERE/'verify_charge_normalization.py')
    p.add_argument('--previous-builder', type=Path, default=HERE/'package_twisted_fields.py')
    p.add_argument('--packaging-helper', type=Path, default=HERE.parent/'translation_coherence/package_translation_coherence.py')
    p.add_argument('--readme', type=Path, required=True)
    p.add_argument('--readme-sha256', required=True)
    p.add_argument('--causal-receipt', type=Path, required=True)
    p.add_argument('--causal-receipt-sha256', required=True)
    p.add_argument('--genealogy-receipt', type=Path)
    p.add_argument('--genealogy-receipt-sha256')
    p.add_argument('--genealogy-check', type=Path)
    p.add_argument('--genealogy-check-sha256')
    p.add_argument('--require-modules', nargs='*', default=[])
    p.add_argument('--plan', action='store_true')
    args = p.parse_args()
    for key,value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.expanduser().resolve())
    base, dest, reportdir, normdir = args.base, args.destination, args.verification.parent, args.normalization_verification.parent
    previous_builder = load(args.previous_builder, PREVIOUS_BUILDER_SHA, 'continuation_previous_packaging')
    if previous_builder.PACKAGING_HELPER != HELPER_SHA:
        raise RuntimeError('Inconsistent inherited inventory helper')
    helper = load(args.packaging_helper, HELPER_SHA, 'continuation_packaging_inventory')
    runner = load(args.runner, RUNNER_SHA, 'continuation_packaging_runner')
    focal = load(args.normalization_verifier, FOCAL_SHA, 'continuation_packaging_focal')
    old = focal.authenticate(base)
    before = helper.inventory(base)
    manifest = helper.read(base/'MANIFIESTO.json')
    if set(before) != {r['path'] for r in manifest['files']} | {'MANIFIESTO.json'}:
        raise RuntimeError('Unmanifested predecessor files must not be silently included')
    for row in manifest['files']:
        if before[row['path']] != row:
            raise RuntimeError('Changed predecessor: '+row['path'])
    helper.require_hash(args.verification, args.receipt_sha256)
    helper.require_hash(args.normalization_verification, args.normalization_receipt_sha256)
    if args.normalization_receipt_sha256 != runner.NORMALIZATION_SHA:
        raise RuntimeError('Continuation requires the exact sealed normalization receipt')
    receipt = helper.read(args.verification)
    if (receipt['status'] != 'PASS_TWISTED_CONTINUATION_DELTA' or receipt['runner_sha256'] != RUNNER_SHA
            or receipt['base_manifest_sha256'] != focal.MANIFEST_SHA
            or receipt['field_receipt_sha256'] != focal.RECEIPT_SHA
            or receipt['normalization_receipt_sha256'] != runner.NORMALIZATION_SHA
            or receipt['inherited_module_count'] != 407 or not receipt['authenticated_inputs_unchanged']
            or receipt['predecessors_modified'] or receipt['predecessors_recompiled']
            or receipt['mathlib_rebuilt'] or not receipt['compiler_invoked']):
        raise RuntimeError('Expected a successful independent continuation on 407 modules')
    vertex_root = base/'antecedente/antecedente/antecedente'
    locality = runner.load(vertex_root/'antecedente/antecedente/verificar_localidad.py',
        'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3', 'packaging_local_inventory')
    vertex = runner.load(vertex_root/'verificar_conforme.py',
        'a1a4d7f2a419403961cf8df6494c0d56393d7fa884a4be3a52d543a422ad396d', 'packaging_vertex_inventory')
    core = vertex_root/'antecedente/antecedente/antecedente/antecedente/antecedente'
    verifier = runner.load(core/'verificar_lean.py',
        '92cbae6c42d918a2b4b61c6cc9771a0af031d78cb5a916fcf99785b4d8fb539e', 'packaging_axiom_parser')
    normalization, nb = runner.authenticate_normalization(normdir, focal, locality, verifier)
    inherited = runner.inherited_registry(base, core, old)
    inherited[runner.NORMALIZATION] = dict(path=str(nb/(runner.NORMALIZATION+'.olean')), sha256=normalization['object_sha256'])
    plan = vertex.source_plan(locality, verifier, {'continuation':args.source_dir}, receipt['requested_modules'], inherited)
    nodes, order, _, imports, owners = plan
    for key,value in (('sources',nodes),('dependency_order',order),('direct_inherited_imports',imports),('public_declaration_owners',owners)):
        if receipt[key] != value:
            raise RuntimeError('Changed verified source closure: '+key)
    vertex.check_probe(verifier, receipt, owners)
    if not set(receipt['axioms']) <= ORDINARY or not set(args.require_modules) <= nodes.keys():
        raise RuntimeError('Axiom policy or required module mismatch')
    rows = {r['module']:r for r in receipt['modules']}
    if len(rows) != len(receipt['modules']) or set(rows) != set(nodes):
        raise RuntimeError('Inconsistent compiled-module inventory')
    for name,node in nodes.items():
        row = rows[name]
        for path,digest in ((args.source_dir/node['path'],node['sha256']),
                (reportdir/'build'/(name+'.lean'),node['sha256']),
                (reportdir/'build'/(name+'.olean'),row['object_sha256']),
                (reportdir/'build'/(name+'.log'),row['log_sha256'])):
            helper.require_hash(path,digest)
        if row['exit_code'] or row['source_sha256'] != node['sha256']:
            raise RuntimeError('Failed or changed compiled source: '+name)
    for name,key in (('axiom_probe.lean','source_sha256'),('axiom_probe.log','output_sha256')):
        helper.require_hash(reportdir/name,receipt['axiom_probe'][key])
    reports = {reportdir:helper.inventory(reportdir), normdir:helper.inventory(normdir)}
    expected = {'axiom_probe.lean'} | {'build/'+m+s for m in nodes for s in ('.lean','.olean')}
    if {n for n in reports[reportdir] if Path(n).suffix in ('.lean','.olean')} != expected:
        raise RuntimeError('Unlisted source/object in continuation report')
    expected_norm = {'build/'+runner.NORMALIZATION+s for s in ('.lean','.olean')}
    if {n for n in reports[normdir] if Path(n).suffix in ('.lean','.olean')} != expected_norm:
        raise RuntimeError('Unlisted source/object in normalization report')
    helper.require_hash(args.readme,args.readme_sha256)
    helper.require_hash(args.causal_receipt,args.causal_receipt_sha256)
    causal = helper.read(args.causal_receipt)
    if (Path(causal['artifact']).resolve() != dest/'README.md' or causal.get('artifact_sha256') != args.readme_sha256
            or causal.get('verification_receipt_sha256') != args.receipt_sha256):
        raise RuntimeError('Causal metadata must identify this destination, README and continuation receipt')
    genealogy = []
    if any((args.genealogy_receipt,args.genealogy_receipt_sha256,args.genealogy_check,args.genealogy_check_sha256)):
        if not all((args.genealogy_receipt,args.genealogy_receipt_sha256,args.genealogy_check,args.genealogy_check_sha256)):
            raise RuntimeError('Supply both genealogy files and their hashes')
        for path,digest,name in ((args.genealogy_receipt,args.genealogy_receipt_sha256,'GENEALOGIA_V4.json'),
                (args.genealogy_check,args.genealogy_check_sha256,'CONTROL_GENEALOGIA_V4.json')):
            helper.require_hash(path,digest); genealogy.append((path,digest,name))
    archive, delivery, zip_report = dest.with_suffix('.zip'), dest.parent/(dest.name+'_ENTREGA.json'), dest.parent/(dest.name+'_ZIP_VERIFICACION.json')
    if any(x.exists() for x in (dest,archive,delivery,zip_report)):
        raise RuntimeError('Refusing to overwrite a delivery or seal')
    if any(dest.is_relative_to(x) or x.is_relative_to(dest) for x in (base,reportdir,normdir)) or args.source_dir.is_relative_to(dest):
        raise RuntimeError('Destination overlaps protected inputs')
    result = dict(status='PASS_TWISTED_CONTINUATION_PACKAGE_INPUTS', previous_files=len(before),
        normalization_modules=1, normalization_public_declarations=len(normalization['public_declarations']),
        added_source_modules=len(nodes), authenticated_modules=407+len(nodes),
        public_declarations=receipt['public_declaration_count'], theorem_lemma_count=len(receipt['theorem_names']),
        destination=str(dest), compilation_repeated=False, receipt_sha256=args.receipt_sha256,
        normalization_receipt_sha256=args.normalization_receipt_sha256, readme_sha256=args.readme_sha256)
    if args.plan:
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    dest.mkdir(parents=True)
    shutil.copytree(base,dest/'antecedente')
    shutil.copytree(normdir,dest/'recibos/normalizacion')
    shutil.copytree(reportdir,dest/'recibos/continuacion')
    (dest/'lean/normalization').mkdir(parents=True)
    shutil.copy2(nb/(runner.NORMALIZATION+'.lean'),dest/'lean/normalization'/(runner.NORMALIZATION+'.lean'))
    (dest/'lean/continuation').mkdir()
    for name,node in nodes.items():
        shutil.copy2(args.source_dir/node['path'],dest/'lean/continuation'/node['path'])
    shutil.copy2(args.runner,dest/'verificar_continuacion.py')
    shutil.copy2(args.normalization_verifier,dest/'verificar_normalizacion.py')
    shutil.copy2(args.readme,dest/'README.md')
    shutil.copy2(args.causal_receipt,dest/'recibos/CAUSAL.json')
    for path,_,name in genealogy:
        shutil.copy2(path,dest/'recibos'/name)
    (dest/'reproducir.py').write_text(wrapper(receipt['requested_modules']))
    (dest/'reproducir_normalizacion.py').write_text(wrapper([],normalization=True))
    (dest/'REPRODUCCION.md').write_text(reproduction_readme(receipt))
    (dest/'historia').mkdir()
    for path in (Path(__file__),args.previous_builder,args.packaging_helper):
        shutil.copy2(path,dest/'historia'/path.name)
    gate = Path.home()/'.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py'
    audit = subprocess.run([sys.executable,'-I','-S',str(gate),'--audit',str(dest/'README.md'),
        '--receipt',str(dest/'recibos/CAUSAL.json')],text=True,capture_output=True)
    helper.write(dest/'recibos/CONTROL_CAUSAL.json',dict(exit_code=audit.returncode,stdout=audit.stdout,
        stderr=audit.stderr,gate_sha256=sha(gate),artifact_sha256=sha(dest/'README.md'),
        receipt_sha256=sha(dest/'recibos/CAUSAL.json'),is_lean_theorem_verification=False))
    if audit.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in audit.stdout:
        raise RuntimeError('Causal metadata audit failed: '+audit.stdout+audit.stderr)
    with tempfile.TemporaryDirectory(prefix='hmt-twisted-continuation-relocation-',dir=dest.parent) as temp:
        temp = Path(temp); relocated = temp/'paquete_relocalizado'; dest.rename(relocated)
        try:
            replay = subprocess.run([sys.executable,'-I','-S',str(relocated/'reproducir.py'),
                '--plan','--report-dir',str(temp/'plan')],cwd=temp,text=True,capture_output=True)
            if replay.returncode:
                raise RuntimeError('Relocated replay failed: '+replay.stdout+replay.stderr)
            relocated_plan = helper.read(temp/'plan/PLAN.json')
            if (relocated_plan['status'] != 'PASS_TWISTED_CONTINUATION_SOURCE_PLAN_NOT_COMPILED'
                    or relocated_plan['compiler_invoked'] or relocated_plan['modules']
                    or relocated_plan['inherited_module_count'] != 407
                    or relocated_plan['sources'] != nodes or relocated_plan['dependency_order'] != order
                    or relocated_plan['public_declaration_owners'] != owners
                    or not relocated_plan['authenticated_inputs_unchanged']):
                raise RuntimeError('Relocated source closure differs from compiled closure')
            helper.write(relocated/'recibos/REPRODUCCION_RELOCALIZADA.json',relocated_plan)
        finally:
            relocated.rename(dest)
    if helper.inventory(base) != before or helper.inventory(dest/'antecedente') != before:
        raise RuntimeError('Predecessor preservation mismatch')
    for original,relative in ((reportdir,'recibos/continuacion'),(normdir,'recibos/normalizacion')):
        if helper.inventory(original) != reports[original] or helper.inventory(dest/relative) != reports[original]:
            raise RuntimeError('Verified report changed during packaging')
    for name,node in nodes.items():
        helper.require_hash(args.source_dir/node['path'],node['sha256'])
        helper.require_hash(dest/'lean/continuation'/node['path'],node['sha256'])
    for source,digest,target in [(args.runner,RUNNER_SHA,'verificar_continuacion.py'),
            (args.normalization_verifier,FOCAL_SHA,'verificar_normalizacion.py'),
            (args.readme,args.readme_sha256,'README.md'),
            (args.causal_receipt,args.causal_receipt_sha256,'recibos/CAUSAL.json'),
            *[(path,digest,'recibos/'+name) for path,digest,name in genealogy]]:
        helper.require_hash(source,digest); helper.require_hash(dest/target,digest)
    helper.write(dest/'VERIFICACION_CONSERVACION.json',dict(status='PASS_BASE406_AND_NORMALIZATION407_AND_CONTINUATION',
        previous_manifest_sha256=focal.MANIFEST_SHA,previous_files=list(before.values()),
        normalization_files=list(reports[normdir].values()),continuation_files=list(reports[reportdir].values()),
        predecessor_copied_exactly_once=True,source_compilation_repeated=False))
    helper.write(dest/'MANIFIESTO.json',dict(schema='hmt.twisted.continuation.successor.v1',
        generated_at_utc=datetime.now(timezone.utc).isoformat(),predecessor='antecedente',
        previous_manifest_sha256=focal.MANIFEST_SHA,
        normalization_receipt='recibos/normalizacion/VERIFICATION.json',normalization_receipt_sha256=args.normalization_receipt_sha256,
        verification_receipt='recibos/continuacion/VERIFICATION.json',verification_receipt_sha256=args.receipt_sha256,
        exact_source_modules={name:'lean/continuation/'+node['path'] for name,node in nodes.items()},
        normalization_source='lean/normalization/'+runner.NORMALIZATION+'.lean',
        total_authenticated_modules=result['authenticated_modules'],new_declaration_axioms=sorted(ORDINARY),
        files=list(helper.inventory(dest).values())))
    complete = helper.inventory(dest)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as bundle:
        for name in complete:
            bundle.write(dest/name,dest.name+'/'+name)
    entries = []
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or len(bundle.namelist()) != len(complete):
            raise RuntimeError('ZIP CRC or count mismatch')
        for name,row in complete.items():
            path = dest.name+'/'+name; data = bundle.read(path); digest = hashlib.sha256(data).hexdigest()
            crc = zlib.crc32(data) & 0xffffffff
            if digest != row['sha256'] or len(data) != row['bytes'] or crc != bundle.getinfo(path).CRC:
                raise RuntimeError('ZIP entry changed: '+name)
            entries.append(dict(path=path,bytes=len(data),sha256=digest,crc32=f'{crc:08x}'))
    helper.write(zip_report,dict(status='PASS_ZIP_CRC_AND_SHA256_EVERY_ENTRY',archive=str(archive),archive_sha256=sha(archive),entries=entries))
    if helper.inventory(dest) != complete or helper.inventory(base) != before:
        raise RuntimeError('Delivery or predecessor changed during sealing')
    for original,files in reports.items():
        if helper.inventory(original) != files:
            raise RuntimeError('Original verification evidence changed during sealing')
    result.update(status='PASS_TWISTED_CONTINUATION_DELIVERY',files=len(complete),
        manifest_sha256=sha(dest/'MANIFIESTO.json'),zip_sha256=sha(archive),
        zip_verification=str(zip_report),zip_verification_sha256=sha(zip_report),
        relocated_plan_passed=True,causal_focal_audit_passed=True,mathematical_certificates_created=False)
    helper.write(delivery,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
