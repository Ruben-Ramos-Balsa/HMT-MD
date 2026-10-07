#!/usr/bin/env python3
"""Weyl–Heisenberg orientado sobre Z/9Z: controles exactos y portátiles.

Sin argumentos sólo ejecuta el álgebra finita. No requiere el manuscrito,
bibliotecas externas, red, valores decimales ni rutas personales. Conserva
las comprobaciones con python -O. --auditar-instalacion es un modo separado
de preservación documental que recibe explícitamente sus tres referencias.
Ese modo escribe exclusivamente QA_REV04.json junto a este programa.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import re
import shutil
import subprocess
import sys
import tempfile


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def multiply(g, h):
    a, b, t = g
    c, d, s = h
    return ((a+c) % 9, (b+d) % 9, (t+s+b*c) % 9)


def inverse(g):
    a, b, t = g
    return (-a % 9, -b % 9, (-t+a*b) % 9)


def representation(g):
    a, b, t = g
    # Action on delta_r: destination and exponent of the ninth root.
    return tuple(((r+a) % 9, (t+b*r) % 9) for r in range(9))


def verify_weyl():
    plane = tuple(itertools.product(range(9), repeat=2))
    group = tuple(itertools.product(range(9), repeat=3))
    add = lambda u, v: ((u[0]+v[0]) % 9, (u[1]+v[1]) % 9)
    cocycle = lambda u, v: u[1]*v[0] % 9
    area = lambda u, v: (u[0]*v[1]-u[1]*v[0]) % 9
    cocycles = 0
    for u, v, w in itertools.product(plane, repeat=3):
        check((cocycle(u,v)+cocycle(add(u,v),w)
               -cocycle(v,w)-cocycle(u,add(v,w))) % 9 == 0,
              'Falla la identidad del cociclo')
        cocycles += 1
    ordered_actions = 0
    central_translations = []
    for u in plane:
        central = True
        for v in plane:
            a, b = u
            c, d = v
            commutator = (cocycle(u,v)-cocycle(v,u)) % 9
            check((commutator+area(u,v)) % 9 == 0,
                  'Falla el signo de la orientación')
            central = central and commutator == 0
            for r in range(9):
                actual = (d*r+b*((r+c) % 9)) % 9
                predicted = (b*c+(b+d)*r) % 9
                check(actual == predicted, 'Falla la composición X^a Z^b')
                ordered_actions += 1
        if central:
            central_translations.append(u)
    check(central_translations == [(0,0)], 'Centro inesperado')
    operators = {representation(g) for g in group}
    check(len(operators) == 729, 'Falla la fidelidad')
    for g in group:
        check(multiply(g,inverse(g)) == (0,0,0), 'Falla la inversa derecha')
        check(multiply(inverse(g),g) == (0,0,0), 'Falla la inversa izquierda')
    # Three false conventions are rejected against the actual action.
    u, v = (0,1), (1,0)
    check(cocycle(u,v) != u[0]*v[1] % 9,
          'Se aceptó sustituir bc por ad en la sección ordenada')
    u, v = (1,0), (0,1)
    check((cocycle(u,v)-cocycle(v,u)) % 9 != area(u,v),
          'Se aceptó el signo contrario del conmutador')
    check(multiply((1,1,0),(-1 % 9,-1 % 9,0)) != (0,0,0),
          'Se aceptó suprimir ab en la inversa')
    return {
        'status': 'PASS_WEYL_ORIENTADO_REV04',
        'domain': '(Z/9Z)^2; extension central (Z/9Z)^3 con producto torcido',
        'cocycle': 'c((a,b),(c,d))=bc mod9',
        'alternating_area': 'ad-bc mod9',
        'commutator_exponent': 'bc-ad mod9, convenio ghg^-1h^-1',
        'counts': {'cocycle_triples': cocycles,
                   'ordered_actions_on_basis': ordered_actions,
                   'distinct_represented_group_elements': len(operators),
                   'two_sided_inverse_checks': 2*len(group),
                   'negative_controls': 3},
        'central_translations': central_translations,
        'scope': 'Identidades algebraicas finitas y signo de la representación; no selección de historias, datos terminales ni constantes HMT.',
        'global_mathematical_certification': False,
        'program_sha256': sha(__file__),
    }


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def mathblocks(text):
    pattern = r'\\\[(.*?)\\\]|\\\((.*?)\\\)|\\begin\{(?:equation\*?|align\*?|gather\*?)\}(.*?)\\end\{(?:equation\*?|align\*?|gather\*?)\}'
    result = []
    for match in re.finditer(pattern, text, re.S):
        value = next(x for x in match.groups() if x is not None)
        value = re.sub(r'\\label\{[^}]+\}', '', value)
        if norm(value) != r'\square':
            result.append(norm(value))
    return Counter(result)


def audit_installation(baseline, proposal, ii_source, compilation_receipt=None):
    root = Path(__file__).resolve().parents[1]
    edited = ('sections/extension.tex', 'sections/01_hilbert_nonadico.tex',
              'sections/continuo_conjunto.tex')
    common = ('sections/nucleo.tex', 'sections/trit_desarrollo.tex',
              'sections/tpk_desarrollo_integrado.tex', 'sections/memoria_resolvente.tex',
              'figures/app.tex', 'figures/regimenes_trit.tex')
    installed = []
    for name in edited:
        check((root/name).read_bytes() == (proposal/name).read_bytes(),
              'No coincide con la propuesta congelada: '+name)
        before, after = mathblocks((baseline/name).read_text()), mathblocks((root/name).read_text())
        check(not (before-after), 'Bloque matemático anterior alterado: '+name)
        installed.append({'file': name, 'sha256': sha(root/name),
                          'equals_proposal': True, 'old_math_blocks_preserved': sum(before.values())})
    old = (baseline/edited[2]).read_text()
    new = (root/edited[2]).read_text()
    pattern = (r'\\subsubsection\*\{(Proposición|Teorema) (\d+)\. ([^}]+)\}'
               r'(.*?)\\textbf\{Demostración\.\}\s*(.*?)\\hfill\\\(\\square\\\)')
    matches = list(re.finditer(pattern,old,re.S))
    check(len(matches) == 8, 'Se esperaban ocho enunciados manuales')
    crosswalk = []
    for match in matches:
        kind, number, title, statement, proof = match.groups()
        env = 'theorem' if kind == 'Teorema' else 'proposition'
        found = re.search(r'\\begin\{'+env+r'\}\['+re.escape(title)+r'\]'
                          r'\s*\\label\{([^}]+)\}(.*?)\\end\{'+env+r'\}'
                          r'\s*\\begin\{proof\}(.*?)\\end\{proof\}',new,re.S)
        check(found is not None, 'No se encontró el enunciado: '+title)
        label, new_statement, new_proof = found.groups()
        for anchor, n in {'iv:cont:gram':'3', 'iv:cont:concatenacion':'1',
                          'iv:cont:memoria-natural':'7'}.items():
            new_proof = new_proof.replace('proposición~\\ref{'+anchor+'}', 'proposición '+n)
        check(norm(statement) == norm(new_statement), 'Enunciado alterado: '+title)
        check(norm(proof) == norm(new_proof), 'Prueba alterada: '+title)
        crosswalk.append({'old': kind+' '+number, 'label': label,
                          'title': title, 'statement_and_proof_preserved': True})
    previous_auto = re.search(r'\\begin\{proposition\}\[Naturalidad del complejo rectangular bajo prolongación\].*?\\end\{proof\}',old,re.S).group()
    check(previous_auto in new, 'Se alteró la proposición automática anterior')
    common_records = []
    main = (root/'main.tex').read_text()
    nucleus = (root/'sections/nucleo.tex').read_text()
    check(r'\input{sections/nucleo.tex}' in main, 'Núcleo fuera del main')
    for name in common:
        check((root/name).read_bytes() == (baseline/name).read_bytes(),
              'Cambió el núcleo común: '+name)
        if name != 'sections/nucleo.tex':
            check('\\input{'+name+'}' in nucleus, 'Común sin inclusión: '+name)
        common_records.append({'file': name, 'sha256': sha(root/name),
                               'byte_equal_REV03': True, 'source_inclusion_present': True})
    k_file = root/'sections/registro_imagen_integral.tex'
    check(k_file.read_bytes() == ii_source.read_bytes(), 'Propietario K distinto de II')
    k_text = (root/'sections/registro_k.tex').read_text()
    input_literal = r'\input{sections/registro_imagen_integral.tex}'
    check(k_text.count(input_literal) == 1, 'Inclusión de K ausente o duplicada')
    check(k_text.index(input_literal) < k_text.index(r'\subsection{Dos lecturas racionales:'),
          'Inclusión K fuera del lugar acordado')
    records = []
    # Copy only this program to a temporary directory, then run it from a
    # separate empty cwd. This checks that the algebra has no file dependency.
    with tempfile.TemporaryDirectory(prefix='weyl-rev04-') as temporary:
        temporary = Path(temporary)
        standalone = temporary/'verificar_weyl_orientado_rev04.py'
        shutil.copyfile(__file__,standalone)
        empty = temporary/'cwd_vacio'
        empty.mkdir()
        for mode, flags in (('normal',[]),('optimized',['-O'])):
            command = [sys.executable,'-I','-S']+flags+[str(standalone)]
            result = subprocess.run(command,cwd=empty,text=True,capture_output=True,check=False)
            check(result.returncode == 0, 'Falló ensayo portátil '+mode+': '+result.stderr)
            data = json.loads(result.stdout)
            check(data['status'] == 'PASS_WEYL_ORIENTADO_REV04', 'Estado inesperado')
            check(data['program_sha256'] == sha(__file__), 'Programa portátil diferente')
            records.append({'mode':mode,'command_options':['-I','-S']+flags,
                            'returncode':result.returncode,'stdout':data,
                            'standalone_copy':True,'empty_working_directory':True})
    check(records[0]['stdout'] == records[1]['stdout'], 'Normal y -O discrepan')
    signed_program = root/'technical/verificar_imagen_firmada.py'
    with tempfile.TemporaryDirectory(prefix='signed-image-rev04-') as empty:
        signed_run = subprocess.run([sys.executable,'-I','-S',str(signed_program)],
                                    cwd=empty,text=True,capture_output=True,check=False)
    check(signed_run.returncode == 0, 'Falló imagen firmada normal: '+signed_run.stderr)
    signed_output = json.loads(signed_run.stdout)
    check(signed_output['status'] == 'PASS_EXACT_SIGNED_IMAGE_ALGEBRA',
          'Estado inesperado en imagen firmada')
    compilation = None
    if compilation_receipt is not None:
        compiled = json.loads(compilation_receipt.read_text())
        compiled_pdf = root/compiled['pdf']['path']
        check(sha(compiled_pdf) == compiled['pdf']['sha256'], 'PDF distinto del recibo de compilación')
        compilation = {'receipt':str(compilation_receipt),
                       'receipt_sha256':sha(compilation_receipt),
                       'pdf':compiled['pdf'],
                       'scope':'Identidad de PDF y metadatos del recibo externo; no nueva compilación ni inspección visual.'}
    return {
        'schema_version':'1.0', 'status':'PASS_QA_DOCUMENTAL_FOCAL_IV_REV04',
        'scope':'Instalación, preservación de fuentes, álgebra finita Weyl e imagen firmada. No se ejecuta compilación ni revisión visual.',
        'package':str(root), 'baseline_REV03':str(baseline),
        'proposal':str(proposal), 'program':str(Path(__file__).resolve()),
        'program_sha256':sha(__file__), 'python_version':sys.version,
        'installed_matches_proposal':installed,
        'prior_mathematical_blocks_preserved':sum(x['old_math_blocks_preserved'] for x in installed),
        'mathematical_block_definition':'Delimitadores \\( \\), \\[ \\] y entornos equation/align/gather, conservando multiplicidades y excluyendo sólo cuadrados de fin de prueba. No es un censo universal de expresiones con delimitador dólar. Enunciados y cuerpos de prueba se cotejan por separado.',
        'manual_statement_crosswalk':crosswalk,
        'previous_automatic_proposition_preserved':True,
        'common_sources':common_records,
        'k_image':{'file':'sections/registro_imagen_integral.tex','source_II':str(ii_source),
                   'sha256':sha(k_file),'byte_equal_II':True,'input_count':1,
                   'before_two_rational_readings':True},
        'weyl_executions':records,
        'signed_image_verifier':{'file':'technical/verificar_imagen_firmada.py',
                                 'sha256':sha(signed_program),
                                 'executed_in_this_task':True,
                                 'returncode':signed_run.returncode,
                                 'command_options':['-I','-S'],
                                 'stdout':signed_output,
                                 'optimization_supported':False,
                                 'reason':'Se ejecutó únicamente normal: el propietario exige aserciones y rechaza -O.'},
        'compilation_identity':compilation,
        'pages':compilation['pdf']['pages_from_log'] if compilation else None,
        'pagination_status':'RECIBO_EXTERNO_COTEJADO' if compilation else 'PENDIENTE_DE_COMPILACION',
        'pdf_visual_QA':False,'global_mathematical_certification':False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--auditar-instalacion',action='store_true')
    parser.add_argument('--baseline',type=Path)
    parser.add_argument('--proposal',type=Path)
    parser.add_argument('--ii-source',type=Path)
    parser.add_argument('--compilation-receipt',type=Path)
    args = parser.parse_args()
    if args.auditar_instalacion:
        if not all((args.baseline,args.proposal,args.ii_source)):
            parser.error('La auditoría de instalación exige baseline, proposal e ii-source')
        report = audit_installation(args.baseline.resolve(),args.proposal.resolve(),args.ii_source.resolve(),
                                    args.compilation_receipt.resolve() if args.compilation_receipt else None)
        receipt = Path(__file__).resolve().parent/'QA_REV04.json'
        receipt.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    else:
        report = verify_weyl()
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
