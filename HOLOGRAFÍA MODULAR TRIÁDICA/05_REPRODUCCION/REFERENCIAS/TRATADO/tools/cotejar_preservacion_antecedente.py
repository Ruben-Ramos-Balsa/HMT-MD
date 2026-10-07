"""Cotejo de contenido material del antecedente; no decide verdad matemática.

No modifica fuentes ni el cierre FLS. Conserva un diff completo y huellas del
instante observado; las reglas de normalización corresponden a hunks leídos.
"""
import collections
import datetime
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / 'metadata'
SOURCE = ROOT / 'source/integral'
MAN = SOURCE / 'fuente/manuscrito'
TRACKED = {}
GRAM_FILE = '04b2_operaciones_intrinsecas_correlativas.tex'
GRAM_ORIGINAL = 'a2cb047439971243b214ee14720bbecc68b4228a95c12de057cfbff508ea3437'
GRAM_CORRECTED = 'c3a160a67faa80ded25e9cbee1b0ee9b734cce0c59f3c317a4c4d223db8adf90'
PRIVATE_KEYS = ['HaidaraRamosCierre','HaidaraRamosMasa','HaidaraRamosContinuo']
PRIVATE_NOTE = ('Manuscrito no publicado; antecedente documental del presente tratado. '
 'Las construcciones y demostraciones utilizadas se incluyen en el cuerpo de esta edición; '
 'esta entrada registra su procedencia.')
RECONCILIATION_DESCRIPTION = [
 'Isometría total equivalente a normalización del Gram promedio de cada fibra; isometrías individuales suficientes, no necesarias.',
 'Balance general A* A + eta* eta = P U* U P + Q U* U Q; igualdad con el Gram íntegro cuando se anulan sus bloques cruzados.',
 'Prueba contigua por desarrollo de productos y complementariedad de proyectores; referencia a x_reciprocidad:iv:cont:gram ya incorporada.',
 'Balance de cada emisión alpha corregido con los proyectores de la fibra inicial.',
 'Hipótesis y falsador armonizados con la normalización del Gram promedio.'
]

def read(path):
    path = Path(path)
    data = path.read_bytes()
    TRACKED[str(path)] = hashlib.sha256(data).hexdigest()
    return data

def norm(text):
    """Retira sólo modificaciones de presentación identificadas en el diff."""
    text = re.sub(r'\\enlargethispage\{[^{}]*\}', '', text)
    text = re.sub(r'\\Needspace\{[^{}]*\}', '', text)
    text = re.sub(r'^% REMATE_LOCAL_.*$', '', text, flags=re.M)
    text = text.replace(r'\addtocontents{toc}{\protect}', r'\addtocontents{toc}{}')
    text = text.replace(r'\chaptermark{Formalización proyectiva de la unidad}',
                        r'\markboth{Introducción general}{Formalización proyectiva de la unidad}')
    # Sólo c44 contiene este intercambio, cotejado en su contexto longtable.
    text = re.sub(r'^\\(?:newpage|par)\s*$', '', text, flags=re.M)
    return '\n'.join(line.strip() for line in text.splitlines() if line.strip())

def bibitems(text):
    matches = list(re.finditer(r'\\bibitem(?:\[[^\n]*?\])?\{([^{}]+)\}', text))
    result = {}
    for i, match in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = text[match.end():end].split(r'\end{thebibliography}')[0]
        body = re.sub(r'(?m)^%.*$', '', body)
        body = body.replace(r'\allowbreak', '')
        result[match.group(1)] = re.sub(r'\s+', '', body)
    return result

manifest_path = META / 'PRESERVACION_BASE_INTEGRAL.json'
fls_path = META / 'CIERRE_MATERIAL_FLS.json'
manifest = json.loads(read(manifest_path))
fls = json.loads(read(fls_path))
rows, absent, unchanged, drift = [], [], [], []
counts = collections.Counter()
for e in manifest['files']:
    origin = Path(e['source'])
    destination = ROOT / e['destination']
    if not origin.is_file() or not destination.is_file():
        absent.append({'source':str(origin),'destination':str(destination)})
        continue
    before_b, after_b = read(origin), read(destination)
    before_h, after_h = TRACKED[str(origin)], TRACKED[str(destination)]
    if before_h != e['sha256']:
        drift.append({'source':str(origin),'manifest_sha256':e['sha256'],'actual':before_h})
    if before_b == after_b:
        unchanged.append(str(destination))
        continue
    before, after = before_b.decode(), after_b.decode()
    removed, added, hunks = [], [], []
    sm = difflib.SequenceMatcher(None, before.splitlines(), after.splitlines(), autojunk=False)
    for op, a,b,c,d in sm.get_opcodes():
        if op == 'equal':
            continue
        old, new = before.splitlines()[a:b], after.splitlines()[c:d]
        removed.extend(old); added.extend(new)
        hunks.append({'operation':op,'original_lines':[a+1,b],'current_lines':[c+1,d],
                      'removed':old,'added':new})
    categories = []
    enl = len(re.findall(r'\\enlargethispage\{', '\n'.join(removed)))
    need = len(re.findall(r'\\Needspace\{', '\n'.join(added)))
    flush = len(re.findall(r'\\HMTFlushCurrentChapter', '\n'.join(added)))
    newinputs = re.findall(r'\\input\{([^{}]+)\}', '\n'.join(added))
    if enl:
        categories.append('RETIRADA_ENLARGETHISPAGE'); counts['enlargethispage_commands_removed'] += enl
    if need:
        categories.append('NEEDSPACE_UNIDAD_LOGICA'); counts['Needspace_commands_added'] += need
    if flush:
        categories.append('ENVOLTORIO_INSERCION_RESIDENCIAS'); counts['Flush_commands_added'] += flush
    if newinputs:
        categories.append('ENVOLTORIO_AMPLIACION_INPUTS'); counts['input_commands_added_in_wrappers'] += len(newinputs)
    if r'\newpage' in '\n'.join(removed):
        categories.append('SUPRESION_SALTO_ANTES_LONGTABLE')
    if r'\chaptermark' in '\n'.join(removed):
        categories.append('CORRECCION_MARCA_CABECERA')
    is_wrapper = destination.name in {
        'parte_i_ii_1_26_editor_unico.tex','parte_iii_27_57_editor_unico.tex',
        'parte_iv_58_94_editor_unico.tex','parte_v_95_102_editor_unico.tex'}
    if is_wrapper:
        nonblank_removed = [x for x in removed if x.strip()]
        equivalent = not nonblank_removed
        method = 'Todos los cambios son inserciones; ninguna línea original no vacía se retira ni reemplaza.'
    else:
        equivalent = norm(before) == norm(after)
        method = 'Identidad del cuerpo tras retirar exclusivamente comandos tipográficos de los hunks cotejados.'
    reconciled = (destination.name == GRAM_FILE and before_h == GRAM_ORIGINAL
                  and after_h == GRAM_CORRECTED)
    if reconciled:
        categories.append('RECONCILIACION_MATEMATICA_GRAM_EXPLICITA')
        method = ('Cinco afirmaciones precisadas y una prueba añadida. Diff cotejado '
                  'íntegramente; antecedente original inalterado. No es identidad tipográfica.')
    proof_before = len(re.findall(r'\\begin\{proof\}', before))
    proof_after = len(re.findall(r'\\begin\{proof\}', after))
    rows.append({'source':str(origin),'destination':str(destination),
                 'original_sha256':before_h,'current_sha256':after_h,
                 'categories':categories,'body_preserved':equivalent,'method':method,
                 'mathematical_reconciliation_reviewed':reconciled,
                 'proof_environment_count':[proof_before,proof_after],
                 'input_additions':newinputs,'hunks':hunks,
                 'diff':''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
                            fromfile=str(origin),tofile=str(destination),n=3))})

# El nuevo main es un envoltorio separado de los archivos originales modificados.
original_main = MAN / 'main_paquete_union_demostrativa_20260904.tex'
new_main = MAN / 'main.tex'
old_main_text = read(original_main).decode()
new_main_text = read(new_main).decode()
main_diff = ''.join(difflib.unified_diff(old_main_text.splitlines(True),new_main_text.splitlines(True),n=3))

old_bbl = SOURCE / 'output/final_20260905_v3/main_paquete_union_demostrativa_20260904.bbl'
archived_bbl = MAN / 'references_integral.bbl'
unified_path = MAN / 'ampliacion_20260919/bibliografia_unificada.tex'
spiral_path = MAN / 'sucesor_102/espirales/bibliografia_especifica.tex'
old_bbl_b, archived_bbl_b = read(old_bbl), read(archived_bbl)
unified_text, spiral_text = read(unified_path).decode(), read(spiral_path).decode()
unified_entries = bibitems(unified_text)
bibliography = {'original_bbl':str(old_bbl),'archive_copy':str(archived_bbl),
                'bbl_bytes_identical':old_bbl_b == archived_bbl_b,
                'unified':str(unified_path),'controls':[]}
for name, txt in [('integral_bbl',old_bbl_b.decode()),('espirales',spiral_text)]:
    entries = bibitems(txt)
    missing = [key for key in entries if key not in unified_entries]
    altered = [key for key in entries if key in unified_entries and entries[key] != unified_entries[key]]
    annotated = [key for key in altered if key in PRIVATE_KEYS
                 and unified_entries[key] == entries[key] + re.sub(r'\s+', '', PRIVATE_NOTE)]
    unexpected = [key for key in altered if key not in annotated]
    details = []
    for key in altered:
        details.append({'key':key,'original_normalized':entries[key],'unified_normalized':unified_entries[key]})
    bibliography['controls'].append({'source':name,'entry_count':len(entries),
             'missing_keys':missing,'changed_body_keys':altered,
             'private_status_notes_added':annotated,'unexpected_changes':unexpected,
             'changed_body_details':details})
bibliography['private_entries'] = PRIVATE_KEYS
bibliography['exact_note_added'] = PRIVATE_NOTE
bibliography['private_notes_present'] = {
    key:unified_entries.get(key,'').endswith(re.sub(r'\s+', '', PRIVATE_NOTE))
    for key in PRIVATE_KEYS}

stable = []
for path, sha in TRACKED.items():
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != sha:
        stable.append(path)
reconciled_rows = [x for x in rows if x['mathematical_reconciliation_reviewed']]
body_control = (all(x['body_preserved'] or x['mathematical_reconciliation_reviewed'] for x in rows)
                and not absent and not drift and not stable)
bib_control = (bibliography['bbl_bytes_identical']
               and all(not x['missing_keys'] and not x['unexpected_changes'] for x in bibliography['controls'])
               and all(bibliography['private_notes_present'].values()))
report = {
 'scope':'Preservación material de los 516 archivos del antecedente y cotejo de los cambios de cuerpo. No certifica la verdad de los teoremas, su alcance físico ni la completitud del nuevo tratado.',
 'observed_at':datetime.datetime.now().astimezone().isoformat(),
 'manifest_sha256':TRACKED[str(manifest_path)],'fls_metadata_sha256':TRACKED[str(fls_path)],
 'manifest_total':len(manifest['files']),'unchanged':len(unchanged),'changed':len(rows),
 'missing':absent,'source_drift_vs_initial_manifest':drift,
 'modified_files_body_preserved':sum(x['body_preserved'] for x in rows),
 'modified_files_mathematically_reconciled':len(reconciled_rows),
 'initial_typographic_snapshot':{'unchanged':489,'changed':27,'body_preserved':27,
    'observed_at':'2026-09-19T22:57:22.975106+08:00'},
 'mathematical_reconciliation':{
    'status':'RECONCILIACION_MATEMATICA_EXPLICITA_CON_ANTECEDENTE_PRESERVADO' if len(reconciled_rows)==1 else 'REQUIERE_COTEJO_ADICIONAL',
    'original_sha256':GRAM_ORIGINAL,'reviewed_current_sha256':GRAM_CORRECTED,
    'original_localizers':[264,300,1013,1228,1257],
    'current_localizers':[264,306,1043,1259,1289],
    'changes':RECONCILIATION_DESCRIPTION,
    'later_owner':'ampliacion_20260919/propietarios/X_RECIPROCIDAD/sections__continuo_conjunto.tex:102-154',
    'body_note':'Los cuerpos, definiciones y pruebas anteriores se conservan; cinco afirmaciones se precisan matemáticamente y se añade una prueba. Esta intervención no se clasifica como identidad tipográfica.'},
 'presentation_counts':dict(counts),'rows':rows,
 'main_wrapper':{'original':str(original_main),'current':str(new_main),'diff':main_diff,
    'scope':'Nuevo envoltorio independiente del conjunto de archivos antecedentes modificados: metadatos, portada nueva, presentación, ampliaciones, aliases y bibliografía unificada; conserva la estructura original102 y todos los inputs de cuerpos/apéndices.',
    'intentional_replacements':['Portada antecedente por portada con título y subtítulo pedidos.','Bibliografía de espirales y llamada BibTeX por fichero unificado.']},
 'bibliography':bibliography,'files_changed_during_observation':stable,
 'snapshots_sha256':TRACKED,
 'status':'CONSERVACION_CON_RECONCILIACION_GRAM_Y_ANOTACION_DE_PROCEDENCIA' if body_control and bib_control and len(reconciled_rows)==1 else 'REQUIERE_COTEJO_ADICIONAL'}
(META/'COTEJO_PRESERVACION_ANTECEDENTE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

lines = ['# Cotejo de preservación del antecedente integral','',
 '## Ámbito y método','',report['scope'],'',
 'Se leyó íntegramente el diff de cada archivo modificado. La identidad normalizada sólo elimina los comandos tipográficos identificados en esos hunks; los cuatro envoltorios se cotejan como inserciones sin retirada de líneas originales. El fichero JSON conserva cada hunk, sus localizadores y las huellas observadas. No se actualiza el cierre FLS ni se modifica ninguna fuente.','',
 '## Resultado de archivos y cuerpos','',
 f"- Archivos registrados: {report['manifest_total']}; idénticos: {report['unchanged']}; modificados: {report['changed']}; ausentes: {len(absent)}.",
 f"- Cuerpos con cambios exclusivamente tipográficos o ampliativos: {report['modified_files_body_preserved']}; reconciliaciones matemáticas explícitas: {len(reconciled_rows)}.",
 f"- Orígenes divergentes de la huella inicial: {len(drift)}. Archivos que cambiaron durante la observación: {len(stable)}.",
 '- El cotejo tipográfico inicial comprende23 cuerpos y cuatro envoltorios ampliativos. Se añade una reconciliación matemática del balance de Gram: cinco afirmaciones precisadas, prueba contigua y antecedente inalterado. La diferencia matemática se registra separadamente de los cambios de presentación.','',
 '## Clasificación individual','',
 '| Archivo relativo al manuscrito o colaboración | Intervención | Cuerpo |','|---|---|---|']
for row in rows:
    name = str(Path(row['destination']).relative_to(SOURCE/'fuente'))
    state = ('Conservado' if row['body_preserved'] else
             'Reconciliación matemática explícita' if row['mathematical_reconciliation_reviewed'] else 'Revisar')
    lines.append('| '+name+' | '+', '.join(row['categories'])+' | '+state+' |')
lines += ['', '## Envoltorio principal y bibliografía','',report['main_wrapper']['scope'],
 'El main antecedente continúa archivado. Su portada se sustituye intencionadamente por la nueva portada; la sustitución no afecta al cuerpo demostrativo. La bibliografía cambia de residencia, no de función probatoria.','',
 f"La copia `references_integral.bbl` es idéntica byte a byte al BBL antecedente: {bibliography['bbl_bytes_identical']}."]
for item in bibliography['controls']:
    lines.append(f"- {item['source']}: {item['entry_count']} entradas; claves ausentes {item['missing_keys']}; notas de procedencia añadidas {item['private_status_notes_added']}; otros cambios de texto {item['unexpected_changes']}.")
lines += ['', 'Las tres fichas autorales de espirales conservan autores, títulos, ediciones y fechas; incorporan expresamente su estatuto de manuscritos no publicados. La nota añadida es:','',
 '> '+bibliography['exact_note_added'],'',
 '## Reconciliación matemática del balance de Gram','',
 f"El archivo `{GRAM_FILE}` conserva su antecedente con SHA-256 `{GRAM_ORIGINAL}`. La copia reconciliada cotejada tiene SHA-256 `{GRAM_CORRECTED}`. Sus localizadores originales son264,300,1013,1228 y1257.",'',
 *['- '+x for x in RECONCILIATION_DESCRIPTION],'',
 'La proposición posterior `x_reciprocidad:iv:cont:gram`, en `sections__continuo_conjunto.tex:102–154`, ya contenía la identidad general correcta y la isometría de la realización sobre historias completas. La reconciliación conserva las definiciones y pruebas previas, precisa los cinco enunciados afectados y añade una demostración contigua. El control exige las huellas exactas de los dos cuerpos cotejados; cualquier modificación adicional vuelve a requerir inspección.','',
 '## Distinción de controles','',
 'La presencia de archivos comprueba conservación del soporte. El diff identifica cambios tipográficos y la reconciliación matemática autorizada; no los confunde. La inclusión efectiva en compilación se verifica en el cierre FLS; ni el hash ni el diff sustituyen ese control. La completitud de dependencias y la corrección global de los teoremas son controles separados, fuera del alcance de este cotejo.','']
(META/'COTEJO_PRESERVACION_ANTECEDENTE.md').write_text('\n'.join(lines))
print(json.dumps({k:report[k] for k in ['manifest_total','unchanged','changed','modified_files_body_preserved','modified_files_mathematically_reconciled','missing','source_drift_vs_initial_manifest','files_changed_during_observation','presentation_counts','status']},ensure_ascii=False,indent=2))
print(json.dumps(bibliography['controls'],ensure_ascii=False,indent=2))
sys.exit(0 if report['status']=='CONSERVACION_CON_RECONCILIACION_GRAM_Y_ANOTACION_DE_PROCEDENCIA' else 1)
