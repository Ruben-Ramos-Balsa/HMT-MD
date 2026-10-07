#!/usr/bin/env python3
"""Snapshot complete sources; never rewrite a concurrent source or its proof.

The manifest checks document preservation, not mathematical completeness.
Only successful, matching regional proof receipts enter the verified layer.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
DEST = PROJECT / 'output/PAQUETE_CONTINUIDAD_K_UNIDAD_20260918'
X = PROJECT / 'output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/source'
LIB = PROJECT / 'output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/delivery/HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B/lean'
TERM = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ARTICULO_I_20260917/TerminalSelector')
REG = PROJECT / 'output/IMPLEMENTACION_N69_REGIONAL_20260918'
HIST = PROJECT / '16_CIERRE_GLOBAL_HMT_MD_2026-07-22'
READER = HIST / '01_SELECTOR_CONSTANTES/selector_global_por_funcionales.py'
CSV = PROJECT / '03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/HMT_N69_ley_transicion_o_axioma_cilindrico_v1/N69_signatures_t0_t99.csv'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    DEST.mkdir(exist_ok=True)
    records = []
    def copy(source, target, role, expected=None):
        source, target = Path(source), DEST/target
        before = source.read_bytes()
        if expected is not None and sha(before) != expected:
            raise RuntimeError('Source differs from proof receipt: '+str(source))
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != before:
            old = DEST/'versiones_previas'/sha(target.read_bytes())/target.relative_to(DEST)
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, old)
        target.write_bytes(before)
        if source.read_bytes() != before:
            raise RuntimeError('Concurrent source changed: '+str(source))
        records.append(dict(source=str(source), path=str(target.relative_to(DEST)),
                            sha256=sha(before), bytes=len(before), role=role))
    for f in sorted(X.rglob('*')):
        if f.is_file():
            copy(f, Path('fuentes/articulo_x')/f.relative_to(X), 'SOURCE_COMPLETE')
    local_receipt=json.loads((HERE/'VERIFICATION_LEAN.json').read_text())
    if not local_receipt['status'].startswith('PASS_'):
        raise RuntimeError('Local proof receipt is not successful')
    local_hashes={item['source']:item['sha256'] for item in local_receipt['modules']}
    for f in sorted(LIB.rglob('*.lean')):
        copy(f, Path('lean/biblioteca')/f.relative_to(LIB), 'ARTICLE_I_LIBRARY',local_hashes.get(str(f)))
    for name in ['GeneratedMarkedIncidence.lean', 'WeightedIncidenceRecovery.lean']:
        copy(HERE/name, Path('lean/incidencia')/name, 'VERIFIED_LOCAL_PROOF',local_hashes[str(HERE/name)])
    for name in ['VERIFICATION_LEAN.json', 'RECIBO_GENEALOGICO.json', 'RECIBO_CAUSAL.json']:
        copy(HERE/name, Path('recibos/incidencia')/name, 'INHERITED_RECEIPT')
    receipt = json.loads((TERM/'VERIFICATION_INCREMENTAL.json').read_text())
    if not receipt['status'].startswith('PASS_'):
        raise RuntimeError('Terminal receipt is not successful')
    for item in receipt['sources']:
        source = TERM/item['path']
        if sha(source.read_bytes()) != item['sha256']:
            raise RuntimeError('Terminal source changed since proof: '+str(source))
        copy(source, Path('lean/terminal')/item['path'], 'VERIFIED_TERMINAL_PROOF_NATIVE',item['sha256'])
    for name in ['README.md', 'VERIFICATION_INCREMENTAL.json', 'verify.py']:
        copy(TERM/name, Path('lean/terminal')/name, 'TERMINAL_DOCUMENTATION_OR_RUNNER')
    composition = json.loads((TERM/'REGIONAL_COMPOSITION_VERIFICATION.json').read_text())
    if not composition['status'].startswith('PASS_'):
        raise RuntimeError('Regional composition receipt is not successful')
    for item in composition['new_compositions']:
        source = TERM/item['source']
        if sha(source.read_bytes()) != item['sha256']:
            raise RuntimeError('Composition source changed since proof: '+str(source))
        copy(source, Path('lean/terminal')/item['source'], 'VERIFIED_REGIONAL_TERMINAL_COMPOSITION',item['sha256'])
    for name in ['REGIONAL_COMPOSITION_VERIFICATION.json', 'CheckReaders.lean']:
        copy(TERM/name, Path('lean/terminal')/name, 'COMPOSITION_RECEIPT_OR_DIAGNOSTIC')
    regional_status = {}
    coordinated_hashes={Path(item['source']).name:item['sha256'] for item in
        composition['coordinated_sources']+[composition['additional_coordinated_source']]}
    for name, receipt_name in [
        ('RegionalSixHundred','REGIONAL_LEAN_VERIFICATION.json'),
        ('N69RegionalSignature','N69RegionalSignature.receipt.json'),
        ('GeneratedN69Rows','GeneratedN69Rows.receipt.json'),
        ('RegionalW24','RegionalW24.receipt.json')]:
        file = REG/receipt_name
        if not file.exists():
            regional_status[name] = 'NO_RECEIPT_IN_SNAPSHOT'
            continue
        proof = json.loads(file.read_text())
        status = proof.get('status','')
        expected = proof.get('source_sha256') or proof.get('sha256')
        actual = sha((REG/(name+'.lean')).read_bytes())
        if status.startswith('PASS_') and expected == actual:
            if coordinated_hashes.get(name+'.lean') != expected:
                raise RuntimeError('Regional composition/source receipt mismatch: '+name)
            copy(REG/(name+'.lean'), Path('lean/regional')/(name+'.lean'), 'VERIFIED_REGIONAL_PROOF',expected)
            copy(file, Path('recibos/regional')/receipt_name, 'INHERITED_RECEIPT')
            regional_status[name] = status
        else:
            regional_status[name] = 'NOT_IMPORTED_AS_VERIFIED: '+status
    incidence_receipt=json.loads((REG/'SelectedRegionalIncidence.receipt.json').read_text())
    if not incidence_receipt['status'].startswith('PASS_'):
        raise RuntimeError('Selected incidence receipt is not successful')
    copy(REG/'SelectedRegionalIncidence.lean','lean/incidencia/SelectedRegionalIncidence.lean',
         'VERIFIED_SAME_REGISTER_ARITHMETIC_INCIDENCE',incidence_receipt['source_sha256'])
    copy(REG/'SelectedRegionalIncidence.receipt.json','recibos/incidencia/SelectedRegionalIncidence.receipt.json',
         'INHERITED_RECEIPT')
    for source, target, role in [
        (REG/'regenerate_n69.py', 'python/regenerate_n69_original.py', 'REGIONAL_SIGNATURE_PRODUCER'),
        (READER, 'python/lectores_regionales.py', 'REGIONAL_READER_IMPLEMENTATION'),
        (CSV, 'datos/N69_TESTIGO_POSTERIOR.csv', 'POSTERIOR_COMPARISON_ONLY'),
        (REG/'N69_REGENERATION.json', 'recibos/N69_REGENERATION.json', 'INHERITED_RECEIPT'),
        (HIST/'15_SELECTOR_GLOBAL_DOBLE_LECTURA/verificar_selector_orbital_etiquetado.py', 'python/selector_orbital_original.py', 'TERMINAL_SELECTOR_OWNER'),
        (HIST/'15_SELECTOR_GLOBAL_DOBLE_LECTURA/verificar_cierre_afin_monodromico_terminal.py', 'historia/verificar_cierre_afin_monodromico_terminal.py', 'HISTORICAL_OWNER'),
        (HIST/'15_SELECTOR_GLOBAL_DOBLE_LECTURA/TEOREMA_CIERRE_AFIN_MONODROMICO_TERMINAL.md', 'historia/TEOREMA_CIERRE_AFIN_MONODROMICO_TERMINAL.md', 'HISTORICAL_PROOF'),
        (HIST/'15_SELECTOR_GLOBAL_DOBLE_LECTURA/DICTAMEN_PROCEDENCIA_SUPERVIVENCIA_S8.md', 'historia/DICTAMEN_PROCEDENCIA_SUPERVIVENCIA_S8.md', 'PROVENANCE_SCOPE'),
        (HIST/'02_LECTURA_DODECAFASICA/continuacion_fases/verificar_caracter_fase_dual.py', 'historia/verificar_caracter_fase_dual.py', 'PHASE_CHARGE_DESCRIPTOR_OWNER'),
        (HIST/'02_LECTURA_DODECAFASICA/continuacion_fases/verificar_obstruccion_y_dato_minimo_w72.py', 'historia/verificar_obstruccion_y_dato_minimo_w72.py', 'REPERTOIRE_PROVENANCE_OWNER'),
        (HIST/'02_LECTURA_DODECAFASICA/continuacion_fases/RESULTADO_OBSTRUCCION_Y_DATO_MINIMO_W72.json', 'datos/REPERTORIO_PROCEDENCIA.json', 'REPERTOIRE_SOURCE_NOT_NEW_PROOF'),
        (HIST/'01_SELECTOR_CONSTANTES/CERTIFICADO_SELECTOR_GLOBAL.json', 'datos/LECTORES_REGIONALES_TESTIGO.json', 'FUNCTIONAL_PANEL_SOURCE'),
        (PROJECT/'03_PAPER/HMT_MACROPAPER_V3/CURRENT.json', 'datos/RECONOCIMIENTO_POSTERIOR.json', 'POSTERIOR_RECOGNITION_ONLY'),
        (HERE/'COMPOSICION_GENERATIVA_Y_RECUPERACION_K.tex', 'NOTA_DE_COMPOSICION.tex', 'EXPOSITORY_DELTA'),
        (HERE/'README.md', 'CONTEXTO_DEL_DELTA.md', 'CONTEXT')]:
        copy(source,target,role)
    for name in ['reproducir_paquete.py','INICIO_CONTINUIDAD.md','APORTACIONES_AUTORALES_INTEGRAS.md']:
        if not (HERE/name).exists():
            raise RuntimeError('Missing mandatory entry: '+name)
        target = {'reproducir_paquete.py':'reproducir.py','INICIO_CONTINUIDAD.md':'INICIO_AQUI.md'}.get(name,name)
        copy(HERE/name, target, 'PACKAGE_ENTRY')
    if (HERE/'verificar_lean_paquete.py').exists():
        copy(HERE/'verificar_lean_paquete.py','verificar_lean.py','UNIFIED_COMPILATION_RUNNER')
    # One lossless reading file; source bytes remain authoritative individually.
    chunks = ['# Fuentes LaTeX íntegras del artículo X\n\nArchivo de lectura; no sustituye la compilación de fuentes/articulo_x/main.tex.\n']
    copied_x=DEST/'fuentes/articulo_x'
    for f in sorted(copied_x.rglob('*.tex')):
        content = f.read_text()
        fence = '`'*(max([len(m.group()) for m in re.finditer(r'`+',content)]+[2])+1)
        chunks += ['\n## '+str(f.relative_to(copied_x))+'\n\n'+fence+'latex\n'+content+
                   ('' if content.endswith('\n') else '\n')+fence+'\n']
    linear = DEST/'FUENTES_INTEGRAS_PARA_LECTURA.md'
    linear.write_text(''.join(chunks))
    records.append(dict(source='GENERATED_LOSSLESS_READING_ORDER',path=linear.name,
                        sha256=sha(linear.read_bytes()),bytes=linear.stat().st_size,role='READING_COPY'))
    manifest = dict(schema='hmt.documentary.snapshot.v1',
        status='DOCUMENTARY_SNAPSHOT_NOT_A_GLOBAL_PROOF',
        article_x_tex_count=sum(item['path'].startswith('fuentes/articulo_x/') and item['path'].endswith('.tex') for item in records),
        regional_proofs=regional_status, files=records,
        external_runtime_dependencies=['Python 3 standard library','Lean 4.21.0 and Mathlib 308445d7985027f538e281e18df29ca16ede2ba3','LaTeX packages and STIX fonts for typesetting'],
        claim='Complete article X source tree and focal proven Lean source deltas; not a new proof that every upstream selector has been formalized.')
    (DEST/'MANIFIESTO.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    archive=DEST.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for relative in sorted({item['path'] for item in records}|{'MANIFIESTO.json'}):
            z.write(DEST/relative,Path(DEST.name)/relative)
    print(json.dumps(dict(directory=str(DEST),files=len(records),tex=manifest['article_x_tex_count'],
        regional=regional_status,zip=str(archive),zip_sha256=sha(archive.read_bytes())),ensure_ascii=False))

if __name__ == '__main__':
    main()
