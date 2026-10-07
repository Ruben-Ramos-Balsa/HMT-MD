#!/usr/bin/env python3
"""Seal fields406 once plus normalization, continuation, descendants and consumers.

All four receipts are supplied with explicit hashes. This builder reuses the
frozen continuation packager, inventory helper and verifiers; it never compiles.
The final README and causal metadata are supplied by the coordinator, not
generated as new mathematical claims. --plan checks inputs without copying.
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
BUILDER_SHA = 'f1bf766faafa458fe548579d714635c7a7f59d67bb7608ac7069c365c67bd659'
DESCENDANTS_RUNNER_SHA = 'f106854e5e5c47e39058447c2b18e0b70c3527758086d50304aa6ca444a9f5a8'
TERMINAL_RUNNER_SHA = 'a906c8f772e96f9d3a5efceb0e8a870e7432b95e68d1865c19b32911b27d195e'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path, expected, name):
    import importlib.util
    if sha(path) != expected:
        raise RuntimeError('Changed frozen dependency: '+str(path))
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def descendant_wrapper(requested):
    return '''#!/usr/bin/env python3
"""Explicit replay of the delivered descendant delta, not USB autoexecution."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/'verificar_descendientes.py'
spec = importlib.util.spec_from_file_location('hmt_descendants_replay',path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args,defaults = sys.argv[1:],[]
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules',*''' + repr(requested) + ''']
for flag,value in [
    ('--base',root/'antecedente'),
    ('--normalization-report-dir',root/'recibos/normalizacion'),
    ('--normalization-verifier',root/'verificar_normalizacion.py'),
    ('--continuation-report-dir',root/'recibos/continuacion'),
    ('--continuation-verifier',root/'verificar_continuacion.py'),
    ('--continuation-source-dir',root/'lean/continuation'),
    ('--source-dir',root/'lean/descendants'),
    ('--report-dir',root/'resultados_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag,str(value)]
sys.argv = [str(path),*defaults,*args]
raise SystemExit(runner.main())
'''


def reproduction_readme(normalization, continuation, descendants):
    return f'''# Reproducción de campos y descendientes

Esta carpeta y el ZIP contienen los mismos archivos. Descomprima una sola vez
si recibe el ZIP. Conectar un USB no ejecuta nada. Desde esta carpeta:

```sh
python3 -I -S reproducir.py --plan --report-dir plan_nuevo
python3 -I -S reproducir.py --report-dir resultados_nuevos
```

El plan sólo autentica; no compila. La segunda orden reutiliza los 418 módulos
anteriores y compila únicamente los {len(descendants['modules'])} del último
incremento, consultando sus {descendants['public_declaration_count']} declaraciones
públicas. Los recibos originales no se sobreescriben.

Los dos incrementos intermedios se pueden reproducir separadamente:

```sh
python3 -I -S reproducir_normalizacion.py --report-dir normalizacion_nueva
python3 -I -S reproducir_continuacion.py --report-dir continuacion_nueva
```

La normalización consulta {len(normalization['public_declarations'])} declaraciones.
La continuación compila {len(continuation['modules'])} módulos y consulta
{continuation['public_declaration_count']} declaraciones; reutiliza la normalización
sellada. Los nuevos resultados no reemplazan automáticamente los recibos sellados.

`antecedente/` contiene íntegra y una sola vez la entrega de 406 módulos.
`lean/normalization/`, `lean/continuation/` y `lean/descendants/` separan las
fuentes de los tres incrementos. `recibos/` conserva sus snapshots, objetos,
logs y consultas de axiomas. Los Python de reproducción están en la raíz.

Se requiere el runtime externo exacto Lean 4.21.0 y Mathlib registrado en los
recibos, con sus rutas disponibles. Se comprueba la relocalización de los
archivos del paquete; no se afirma que objetos compilados de una plataforma
sean portables a otra ni se instala o descarga software automáticamente.

`README.md` explica el alcance matemático. El plan, el control causal y los
hashes son comprobaciones distintas de Lean. Ninguna cifra de módulos o archivos
equivale por sí sola a la formalización íntegra de FLM o Moonshine.
'''


def terminal_wrapper(requested, parent_sha):
    return '''#!/usr/bin/env python3
"""Replay only the terminal consumers of the authenticated state fields."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
path = root/'verificar_terminal.py'
spec = importlib.util.spec_from_file_location('hmt_terminal_replay',path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
args,defaults = sys.argv[1:],[]
if not any(a == '--modules' or a.startswith('--modules=') for a in args):
    defaults += ['--modules',*''' + repr(requested) + ''']
for flag,value in [
    ('--base',root/'antecedente'),
    ('--parent-report-dir',root/'recibos/descendientes'),
    ('--parent-receipt-sha256',''' + repr(parent_sha) + '''),
    ('--parent-verifier',root/'verificar_descendientes.py'),
    ('--parent-source-dir',root/'lean/descendants'),
    ('--normalization-report-dir',root/'recibos/normalizacion'),
    ('--normalization-verifier',root/'verificar_normalizacion.py'),
    ('--continuation-report-dir',root/'recibos/continuacion'),
    ('--continuation-verifier',root/'verificar_continuacion.py'),
    ('--continuation-source-dir',root/'lean/continuation'),
    ('--source-dir',root/'lean/terminal'),
    ('--report-dir',root/'resultados_terminales_nuevos')]:
    if not any(a == flag or a.startswith(flag+'=') for a in args):
        defaults += [flag,str(value)]
sys.argv = [str(path),*defaults,*args]
raise SystemExit(runner.main())
'''


def check_report(helper, vertex, verifier, receipt, root, source_dir, root_id):
    # Source planning is performed by the caller with the frozen inventory API.
    rows = {r['module']:r for r in receipt['modules']}
    if len(rows) != len(receipt['modules']) or set(rows) != set(receipt['sources']):
        raise RuntimeError('Inconsistent compiled module inventory')
    vertex.check_probe(verifier,receipt,receipt['public_declaration_owners'])
    for name,node in receipt['sources'].items():
        if node['root'] != root_id or node['path'] != name+'.lean':
            raise RuntimeError('Unsafe source locator: '+name)
        row = rows[name]
        for path,digest in ((source_dir/node['path'],node['sha256']),
                (root/'build'/(name+'.lean'),node['sha256']),
                (root/'build'/(name+'.olean'),row['object_sha256']),
                (root/'build'/(name+'.log'),row['log_sha256'])):
            helper.require_hash(path,digest)
        if row['exit_code'] or row['source_sha256'] != node['sha256'] or (root/'build'/(name+'.log')).read_text() != row['output']:
            raise RuntimeError('Changed compilation evidence: '+name)
    queries = [q for name in receipt['dependency_order'] for q in receipt['sources'][name]['public_declarations']]
    probe = ''.join('import '+name+'\n' for name in receipt['dependency_order'])+''.join('#print axioms '+q+'\n' for q in queries)
    if (root/'axiom_probe.lean').read_text() != probe or receipt['public_declaration_count'] != len(queries):
        raise RuntimeError('Changed complete public axiom query source')
    for name,key in (('axiom_probe.lean','source_sha256'),('axiom_probe.log','output_sha256')):
        helper.require_hash(root/name,receipt['axiom_probe'][key])
    if (root/'axiom_probe.log').read_text() != receipt['axiom_probe']['output']:
        raise RuntimeError('Changed public axiom transcript')
    files = helper.inventory(root)
    expected = {'axiom_probe.lean'} | {'build/'+m+s for m in rows for s in ('.lean','.olean')}
    if {n for n in files if Path(n).suffix in ('.lean','.olean')} != expected:
        raise RuntimeError('Unlisted source/object in verification report')
    return files


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('base','destination','normalization-verification','continuation-verification',
                 'descendants-verification','terminal-verification','readme','causal-receipt'):
        p.add_argument('--'+name,type=Path,required=True)
    for name in ('normalization-receipt-sha256','continuation-receipt-sha256',
                 'descendants-receipt-sha256','terminal-receipt-sha256','readme-sha256','causal-receipt-sha256'):
        p.add_argument('--'+name,required=True)
    p.add_argument('--source-dir',type=Path,default=HERE)
    p.add_argument('--previous-builder',type=Path,default=HERE/'package_twisted_continuation.py')
    p.add_argument('--packaging-helper',type=Path,default=HERE.parent/'translation_coherence/package_translation_coherence.py')
    p.add_argument('--normalization-verifier',type=Path,default=HERE/'verify_charge_normalization.py')
    p.add_argument('--continuation-verifier',type=Path,default=HERE/'verify_twisted_continuation.py')
    p.add_argument('--descendants-verifier',type=Path,default=HERE/'verify_twisted_descendants.py')
    p.add_argument('--terminal-verifier',type=Path,default=HERE/'verify_twisted_terminal.py')
    p.add_argument('--genealogy-receipt',type=Path); p.add_argument('--genealogy-receipt-sha256')
    p.add_argument('--genealogy-check',type=Path); p.add_argument('--genealogy-check-sha256')
    p.add_argument('--require-modules',nargs='*',default=[])
    p.add_argument('--support-files',type=Path,nargs='*',default=[])
    p.add_argument('--plan',action='store_true')
    args = p.parse_args()
    for key,value in vars(args).items():
        if isinstance(value,Path): setattr(args,key,value.expanduser().resolve())
    args.support_files = [p.expanduser().resolve() for p in args.support_files]
    reserved_history = {Path(__file__).name,args.previous_builder.name,args.packaging_helper.name}
    if len({p.name for p in args.support_files}) != len(args.support_files) or any(p.name in reserved_history for p in args.support_files):
        raise RuntimeError('Duplicate supporting-document basename')
    support_files = [(p,sha(p)) for p in args.support_files]
    old_builder = load(args.previous_builder,BUILDER_SHA,'statefields_packaging_previous')
    helper = old_builder.load(args.packaging_helper,old_builder.HELPER_SHA,'statefields_inventory')
    continuation_runner = old_builder.load(args.continuation_verifier,old_builder.RUNNER_SHA,'statefields_continuation')
    descendants_runner = load(args.descendants_verifier,DESCENDANTS_RUNNER_SHA,'statefields_descendants')
    terminal_runner = load(args.terminal_verifier,TERMINAL_RUNNER_SHA,'statefields_terminal')
    focal = old_builder.load(args.normalization_verifier,old_builder.FOCAL_SHA,'statefields_normalization')
    base,dest = args.base,args.destination
    fields = focal.authenticate(base); before = helper.inventory(base)
    old_manifest = helper.read(base/'MANIFIESTO.json')
    if set(before) != {r['path'] for r in old_manifest['files']} | {'MANIFIESTO.json'}:
        raise RuntimeError('Unmanifested predecessor files')
    for row in old_manifest['files']:
        if before[row['path']] != row: raise RuntimeError('Changed predecessor: '+row['path'])
    nr,cr,dr,tr = args.normalization_verification.parent,args.continuation_verification.parent,args.descendants_verification.parent,args.terminal_verification.parent
    for path,digest in ((args.normalization_verification,args.normalization_receipt_sha256),
            (args.continuation_verification,args.continuation_receipt_sha256),
            (args.descendants_verification,args.descendants_receipt_sha256),
            (args.terminal_verification,args.terminal_receipt_sha256)):
        helper.require_hash(path,digest)
    if args.normalization_receipt_sha256 != continuation_runner.NORMALIZATION_SHA or args.continuation_receipt_sha256 != descendants_runner.CONTINUATION_SHA:
        raise RuntimeError('Incorrect pinned intermediate receipt')
    descendants = helper.read(args.descendants_verification)
    terminal = helper.read(args.terminal_verification)
    if (descendants['status'] != 'PASS_TWISTED_DESCENDANTS_DELTA' or descendants['runner_sha256'] != DESCENDANTS_RUNNER_SHA
            or descendants['base_manifest_sha256'] != focal.MANIFEST_SHA or descendants['field_receipt_sha256'] != focal.RECEIPT_SHA
            or descendants['normalization_receipt_sha256'] != continuation_runner.NORMALIZATION_SHA
            or descendants['continuation_receipt_sha256'] != descendants_runner.CONTINUATION_SHA
            or descendants['inherited_module_count'] != 418 or not descendants['authenticated_inputs_unchanged']
            or descendants['predecessors_modified'] or descendants['predecessors_recompiled']
            or descendants['mathlib_rebuilt'] or not descendants['compiler_invoked']):
        raise RuntimeError('Successful final descendant receipt required')
    if (terminal['status'] != 'PASS_TWISTED_TERMINAL_DELTA' or terminal['runner_sha256'] != TERMINAL_RUNNER_SHA
            or terminal['parent_receipt_sha256'] != args.descendants_receipt_sha256
            or terminal['inherited_module_count'] != 418+len(descendants['modules'])
            or terminal['base_manifest_sha256'] != focal.MANIFEST_SHA
            or terminal['field_receipt_sha256'] != focal.RECEIPT_SHA
            or terminal['normalization_receipt_sha256'] != continuation_runner.NORMALIZATION_SHA
            or terminal['continuation_receipt_sha256'] != descendants_runner.CONTINUATION_SHA
            or not terminal['authenticated_inputs_unchanged'] or not terminal['compiler_invoked']
            or terminal['predecessors_modified'] or terminal['predecessors_recompiled'] or terminal['mathlib_rebuilt']):
        raise RuntimeError('Successful terminal consumer receipt required')
    vertex_root = base/'antecedente/antecedente/antecedente'
    locality = continuation_runner.load(vertex_root/'antecedente/antecedente/verificar_localidad.py',
        'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3','statefields_source_inventory')
    vertex = continuation_runner.load(vertex_root/'verificar_conforme.py',
        'a1a4d7f2a419403961cf8df6494c0d56393d7fa884a4be3a52d543a422ad396d','statefields_source_plan')
    core = vertex_root/'antecedente/antecedente/antecedente/antecedente/antecedente'
    verifier = continuation_runner.load(core/'verificar_lean.py',
        '92cbae6c42d918a2b4b61c6cc9771a0af031d78cb5a916fcf99785b4d8fb539e','statefields_axiom_parser')
    normalization,nb = continuation_runner.authenticate_normalization(nr,focal,locality,verifier)
    continuation,cb = descendants_runner.authenticate_continuation(cr,args.source_dir,continuation_runner,vertex,locality,verifier)
    inherited = continuation_runner.inherited_registry(base,core,fields)
    inherited[continuation_runner.NORMALIZATION] = dict(path=str(nb/(continuation_runner.NORMALIZATION+'.olean')),sha256=normalization['object_sha256'])
    report_files = {nr:helper.inventory(nr)}
    norm_code = {'build/'+continuation_runner.NORMALIZATION+s for s in ('.lean','.olean')}
    if {n for n in report_files[nr] if Path(n).suffix in ('.lean','.olean')} != norm_code:
        raise RuntimeError('Unlisted normalization source/object')
    terminal_runner.authenticate_parent(dr,args.descendants_receipt_sha256,args.source_dir,
        descendants_runner,vertex,locality,verifier)
    for receipt,root,root_id in ((continuation,cr,'continuation'),(descendants,dr,'descendants'),(terminal,tr,'terminal')):
        plan = vertex.source_plan(locality,verifier,{root_id:args.source_dir},receipt['requested_modules'],inherited)
        nodes,order,_,imports,owners = plan
        for key,value in (('sources',nodes),('dependency_order',order),('direct_inherited_imports',imports),('public_declaration_owners',owners)):
            if receipt[key] != value: raise RuntimeError('Changed '+root_id+' source closure: '+key)
        report_files[root] = check_report(helper,vertex,verifier,receipt,root,args.source_dir,root_id)
        if not set(receipt['axioms']) <= old_builder.ORDINARY: raise RuntimeError('Disallowed new axiom')
        inherited.update({r['module']:dict(path=str(root/'build'/(r['module']+'.olean')),sha256=r['object_sha256']) for r in receipt['modules']})
    if not set(args.require_modules) <= (descendants['sources'].keys() | terminal['sources'].keys()): raise RuntimeError('Required state-field module omitted')
    helper.require_hash(args.readme,args.readme_sha256); helper.require_hash(args.causal_receipt,args.causal_receipt_sha256)
    causal = helper.read(args.causal_receipt)
    if (Path(causal['artifact']).resolve() != dest/'README.md' or causal.get('artifact_sha256') != args.readme_sha256
            or causal.get('verification_receipt_sha256') != args.terminal_receipt_sha256):
        raise RuntimeError('Causal receipt must identify final destination, README and descendant verification')
    genealogy = []
    if any((args.genealogy_receipt,args.genealogy_receipt_sha256,args.genealogy_check,args.genealogy_check_sha256)):
        if not all((args.genealogy_receipt,args.genealogy_receipt_sha256,args.genealogy_check,args.genealogy_check_sha256)):
            raise RuntimeError('Supply both genealogy files and their hashes')
        for path,digest,name in ((args.genealogy_receipt,args.genealogy_receipt_sha256,'GENEALOGIA_V4.json'),
                (args.genealogy_check,args.genealogy_check_sha256,'CONTROL_GENEALOGIA_V4.json')):
            helper.require_hash(path,digest); genealogy.append((path,digest,name))
    archive,delivery,zr = dest.with_suffix('.zip'),dest.parent/(dest.name+'_ENTREGA.json'),dest.parent/(dest.name+'_ZIP_VERIFICACION.json')
    if any(x.exists() for x in (dest,archive,delivery,zr)): raise RuntimeError('Refusing to overwrite delivery')
    if any(dest.is_relative_to(x) or x.is_relative_to(dest) for x in (base,nr,cr,dr,tr)) or args.source_dir.is_relative_to(dest):
        raise RuntimeError('Destination overlaps protected inputs')
    result = dict(status='PASS_TWISTED_STATE_FIELDS_PACKAGE_INPUTS',previous_files=len(before),
        normalization_modules=1,continuation_modules=len(continuation['modules']),descendant_modules=len(descendants['modules']),terminal_modules=len(terminal['modules']),
        authenticated_modules=len(inherited),destination=str(dest),compilation_repeated=False,
        normalization_receipt_sha256=args.normalization_receipt_sha256,
        continuation_receipt_sha256=args.continuation_receipt_sha256,descendants_receipt_sha256=args.descendants_receipt_sha256,
        terminal_receipt_sha256=args.terminal_receipt_sha256,
        public_declarations_new=len(normalization['public_declarations'])+continuation['public_declaration_count']+descendants['public_declaration_count']+terminal['public_declaration_count'])
    if args.plan: print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    dest.mkdir(parents=True); shutil.copytree(base,dest/'antecedente')
    for root,label in ((nr,'normalizacion'),(cr,'continuacion'),(dr,'descendientes'),(tr,'terminal')):
        shutil.copytree(root,dest/'recibos'/label)
    (dest/'lean/normalization').mkdir(parents=True)
    shutil.copy2(nb/(continuation_runner.NORMALIZATION+'.lean'),dest/'lean/normalization'/(continuation_runner.NORMALIZATION+'.lean'))
    for receipt,label in ((continuation,'continuation'),(descendants,'descendants'),(terminal,'terminal')):
        (dest/'lean'/label).mkdir()
        for node in receipt['sources'].values(): shutil.copy2(args.source_dir/node['path'],dest/'lean'/label/node['path'])
    scripts = [(args.normalization_verifier,old_builder.FOCAL_SHA,'verificar_normalizacion.py'),
        (args.continuation_verifier,old_builder.RUNNER_SHA,'verificar_continuacion.py'),
        (args.descendants_verifier,DESCENDANTS_RUNNER_SHA,'verificar_descendientes.py'),
        (args.terminal_verifier,TERMINAL_RUNNER_SHA,'verificar_terminal.py')]
    for path,_,name in scripts: shutil.copy2(path,dest/name)
    shutil.copy2(args.readme,dest/'README.md'); shutil.copy2(args.causal_receipt,dest/'recibos/CAUSAL.json')
    for path,_,name in genealogy: shutil.copy2(path,dest/'recibos'/name)
    (dest/'reproducir.py').write_text(descendant_wrapper(descendants['requested_modules']))
    (dest/'reproducir_terminal.py').write_text(terminal_wrapper(terminal['requested_modules'],args.descendants_receipt_sha256))
    (dest/'reproducir_continuacion.py').write_text(old_builder.wrapper(continuation['requested_modules']))
    (dest/'reproducir_normalizacion.py').write_text(old_builder.wrapper([],normalization=True))
    terminal_instructions = f'''\n## Consumidores terminales incluidos\n\nDespués de los campos generales, `lean/terminal/` conserva {len(terminal['modules'])}
módulos con {terminal['public_declaration_count']} declaraciones públicas. Se reproducen sin
recompilar los {terminal['inherited_module_count']} módulos que consumen:\n\n```sh
python3 -I -S reproducir_terminal.py --plan --report-dir plan_terminal_nuevo
python3 -I -S reproducir_terminal.py --report-dir resultados_terminales_nuevos
```\n\nEl recibo terminal es `recibos/terminal/VERIFICATION.json`. «Terminal» designa
el consumidor de este incremento, no el cierre de todos los teoremas de Moonshine.\n'''
    (dest/'REPRODUCCION.md').write_text(reproduction_readme(normalization,continuation,descendants)+terminal_instructions)
    (dest/'historia').mkdir()
    for path in (Path(__file__),args.previous_builder,args.packaging_helper): shutil.copy2(path,dest/'historia'/path.name)
    for path,digest in support_files:
        helper.require_hash(path,digest)
        shutil.copy2(path,dest/'historia'/path.name)
    gate = Path.home()/'.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py'
    audit = subprocess.run([sys.executable,'-I','-S',str(gate),'--audit',str(dest/'README.md'),
        '--receipt',str(dest/'recibos/CAUSAL.json')],text=True,capture_output=True)
    helper.write(dest/'recibos/CONTROL_CAUSAL.json',dict(exit_code=audit.returncode,stdout=audit.stdout,stderr=audit.stderr,
        gate_sha256=sha(gate),artifact_sha256=sha(dest/'README.md'),receipt_sha256=sha(dest/'recibos/CAUSAL.json'),is_lean_theorem_verification=False))
    if audit.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in audit.stdout: raise RuntimeError('Causal audit failed')
    with tempfile.TemporaryDirectory(prefix='hmt-twisted-statefields-relocation-',dir=dest.parent) as temp:
        temp = Path(temp); relocated = temp/'paquete_relocalizado'; dest.rename(relocated)
        try:
            replay = subprocess.run([sys.executable,'-I','-S',str(relocated/'reproducir.py'),'--plan','--report-dir',str(temp/'plan')],cwd=temp,text=True,capture_output=True)
            if replay.returncode: raise RuntimeError('Relocated replay failed: '+replay.stdout+replay.stderr)
            plan = helper.read(temp/'plan/PLAN.json')
            if (plan['status'] != 'PASS_TWISTED_DESCENDANTS_SOURCE_PLAN_NOT_COMPILED' or plan['compiler_invoked'] or plan['modules']
                    or plan['inherited_module_count'] != 418 or plan['sources'] != descendants['sources']
                    or plan['dependency_order'] != descendants['dependency_order']
                    or plan['public_declaration_owners'] != descendants['public_declaration_owners'] or not plan['authenticated_inputs_unchanged']):
                raise RuntimeError('Relocated descendant plan differs from compiled closure')
            helper.write(relocated/'recibos/REPRODUCCION_RELOCALIZADA.json',plan)
            replay_terminal = subprocess.run([sys.executable,'-I','-S',str(relocated/'reproducir_terminal.py'),'--plan',
                '--report-dir',str(temp/'terminal_plan')],cwd=temp,text=True,capture_output=True)
            if replay_terminal.returncode: raise RuntimeError('Relocated terminal replay failed: '+replay_terminal.stdout+replay_terminal.stderr)
            terminal_plan = helper.read(temp/'terminal_plan/PLAN.json')
            if (terminal_plan['status'] != 'PASS_TWISTED_TERMINAL_SOURCE_PLAN_NOT_COMPILED'
                    or terminal_plan['compiler_invoked'] or terminal_plan['modules']
                    or terminal_plan['sources'] != terminal['sources']
                    or terminal_plan['dependency_order'] != terminal['dependency_order']
                    or terminal_plan['public_declaration_owners'] != terminal['public_declaration_owners']
                    or not terminal_plan['authenticated_inputs_unchanged']):
                raise RuntimeError('Relocated terminal plan differs from compiled closure')
            helper.write(relocated/'recibos/REPRODUCCION_TERMINAL_RELOCALIZADA.json',terminal_plan)
        finally: relocated.rename(dest)
    if helper.inventory(base) != before or helper.inventory(dest/'antecedente') != before: raise RuntimeError('Antecedent preservation mismatch')
    for root,label in ((nr,'normalizacion'),(cr,'continuacion'),(dr,'descendientes'),(tr,'terminal')):
        if helper.inventory(root) != report_files[root] or helper.inventory(dest/'recibos'/label) != report_files[root]:
            raise RuntimeError('Report changed during packaging: '+label)
    for receipt,label in ((continuation,'continuation'),(descendants,'descendants'),(terminal,'terminal')):
        for node in receipt['sources'].values():
            helper.require_hash(args.source_dir/node['path'],node['sha256']); helper.require_hash(dest/'lean'/label/node['path'],node['sha256'])
    helper.require_hash(dest/'lean/normalization'/(continuation_runner.NORMALIZATION+'.lean'),focal.SOURCE_SHA)
    bound = scripts+[(args.readme,args.readme_sha256,'README.md'),(args.causal_receipt,args.causal_receipt_sha256,'recibos/CAUSAL.json')]
    bound += [(path,digest,'recibos/'+name) for path,digest,name in genealogy]
    bound += [(path,digest,'historia/'+path.name) for path,digest in support_files]
    for path,digest,name in bound: helper.require_hash(path,digest); helper.require_hash(dest/name,digest)
    helper.write(dest/'VERIFICACION_CONSERVACION.json',dict(status='PASS_BASE406_AND_ALL_FOUR_VERIFIED_INCREMENTS',
        previous_manifest_sha256=focal.MANIFEST_SHA,previous_files=list(before.values()),
        increments={label:list(report_files[root].values()) for root,label in ((nr,'normalizacion'),(cr,'continuacion'),(dr,'descendientes'),(tr,'terminal'))},
        predecessor_copied_exactly_once=True,source_compilation_repeated=False))
    helper.write(dest/'MANIFIESTO.json',dict(schema='hmt.twisted.statefields.successor.v1',generated_at_utc=datetime.now(timezone.utc).isoformat(),
        predecessor='antecedente',previous_manifest_sha256=focal.MANIFEST_SHA,total_authenticated_modules=len(inherited),
        normalization_receipt='recibos/normalizacion/VERIFICATION.json',normalization_receipt_sha256=args.normalization_receipt_sha256,
        continuation_receipt='recibos/continuacion/VERIFICATION.json',continuation_receipt_sha256=args.continuation_receipt_sha256,
        descendants_receipt='recibos/descendientes/VERIFICATION.json',descendants_receipt_sha256=args.descendants_receipt_sha256,
        verification_receipt='recibos/terminal/VERIFICATION.json',verification_receipt_sha256=args.terminal_receipt_sha256,
        exact_source_modules={name:'lean/'+label+'/'+node['path'] for receipt,label in ((continuation,'continuation'),(descendants,'descendants'),(terminal,'terminal')) for name,node in receipt['sources'].items()},
        normalization_source='lean/normalization/'+continuation_runner.NORMALIZATION+'.lean',files=list(helper.inventory(dest).values())))
    complete = helper.inventory(dest)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as bundle:
        for name in complete: bundle.write(dest/name,dest.name+'/'+name)
    entries = []
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or len(bundle.namelist()) != len(complete): raise RuntimeError('ZIP CRC or count mismatch')
        for name,row in complete.items():
            path = dest.name+'/'+name; data = bundle.read(path); digest = hashlib.sha256(data).hexdigest(); crc = zlib.crc32(data)&0xffffffff
            if digest != row['sha256'] or len(data) != row['bytes'] or crc != bundle.getinfo(path).CRC: raise RuntimeError('ZIP entry mismatch: '+name)
            entries.append(dict(path=path,bytes=len(data),sha256=digest,crc32=f'{crc:08x}'))
    helper.write(zr,dict(status='PASS_ZIP_CRC_AND_SHA256_EVERY_ENTRY',archive=str(archive),archive_sha256=sha(archive),entries=entries))
    if helper.inventory(dest) != complete or helper.inventory(base) != before or any(helper.inventory(root) != files for root,files in report_files.items()):
        raise RuntimeError('Inputs or delivery changed during sealing')
    result.update(status='PASS_TWISTED_STATE_FIELDS_DELIVERY',files=len(complete),manifest_sha256=sha(dest/'MANIFIESTO.json'),
        zip_sha256=sha(archive),zip_verification=str(zr),zip_verification_sha256=sha(zr),
        relocated_plan_passed=True,causal_focal_audit_passed=True,mathematical_certificates_created=False)
    helper.write(delivery,result); print(json.dumps(result,ensure_ascii=False,indent=2)); return 0


if __name__ == '__main__':
    raise SystemExit(main())
