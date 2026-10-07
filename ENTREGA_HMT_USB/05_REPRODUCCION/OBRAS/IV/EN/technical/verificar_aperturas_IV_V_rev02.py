#!/usr/bin/env python3
"""Cotejo editorial focal de dos sucesoras. No valida resultados matemáticos."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

LABEL = 'Manuscrito de recopilación para transferencia académica'
AI = 'Integración y recopilación documental generadas por ChatGPT Astra.'
COAUTHOR = 'Coautoría sin prelación de contribución'
TITLE_IV = ('Extensión de la estructura discreta del continuo: álgebras de operadores '
            'de vértice, Moonshine, dualidad T y teoría M')
SUBTITLE_V = ('Distribuciones de Bose--Einstein y Fermi--Dirac y leyes de Planck, '
              'Stefan--Boltzmann y Wien')
JOBS = [
    ('IV', 'IV_MOONSHINE_DUALIDAD_TEORIA_M', 'main.tex', 'sections/iv_portada.tex',
     'sections/iv_resumen.tex', 'MOONSHINE_DUALIDAD_T_Y_TEORIA_M.pdf'),
    ('V', 'V_ESTADISTICA_CUANTICA_RADIACION', 'manuscrito/preambulo.tex',
     'manuscrito/sections/00_portada_V.tex', 'manuscrito/sections/00b_resumen_V.tex',
     'ESTADISTICA_CUANTICA_Y_RADIACION.pdf'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Patrón editorial no unívoco: ' + old)
    return text.replace(old, new, 1)


def expected_preamble(text, key):
    if key == 'IV':
        old = 'Moonshine, dualidad T y teoría M desde la estructura discreta del continuo'
        if text.count(old) != 2:
            raise ValueError('Dos residencias esperadas del título de IV')
        text = text.replace(old, TITLE_IV)
        text = replace_once(text, '\\raggedbottom',
            '\\clubpenalty=10000\\widowpenalty=10000\\displaywidowpenalty=10000\n\\raggedbottom')
    else:
        old = 'Estados genealógicos, evolución unitaria y distribuciones de ocupación'
        text = replace_once(text, 'pdfsubject={'+old+'}',
                            'pdfsubject={'+SUBTITLE_V.replace('--', '–')+'}')
        text = replace_once(text, '\\newcommand{\\TituloSegundo}{'+old+'}',
                            '\\newcommand{\\TituloSegundo}{'+SUBTITLE_V+'}')
    return replace_once(text, '\\AddToHook{cmd/subsection/before}',
        '\\AddToHook{cmd/section/before}{\\clearpage}\n\\AddToHook{cmd/subsection/before}')


def expected_opening(text, key):
    text = replace_once(text, '\\begin{center}\n',
        '\\begin{center}\n{\\fontsize{10}{12}\\selectfont '+LABEL+'\\par}\n\\vspace{8pt}\n')
    if key == 'IV':
        return replace_once(text,
            '{\\small Integración y recopilación documental generadas por ChatGPT Astra\\par}',
            '{\\small '+COAUTHOR+'\\par}\n\\vspace{3pt}\n{\\small '+AI+'\\par}')
    text = replace_once(text, '{\\small '+COAUTHOR+'\\par}',
        '{\\small '+COAUTHOR+'\\par}\n\\vspace{3pt}\n{\\small '+AI+'\\par}')
    obsolete = ('\\vspace{6pt}\n\\noindent{\\small La asistencia de inteligencia artificial se utiliza en la\n'
        'organización editorial, la redacción y las comprobaciones documentadas del\n'
        'manuscrito. La atribución de las construcciones y sus fuentes se conserva en\n'
        'el suplemento de procedencia.}\n\\par\\vspace{7pt}')
    return replace_once(text, obsolete, '\\vspace{7pt}')


def toc(path):
    entries = []
    for line in path.read_text().splitlines():
        if not line.startswith('\\contentsline'):
            continue
        match = re.fullmatch(r'(.*)\{(\d+)\}\{([^{}]*)\}%', line)
        if not match:
            raise ValueError('Entrada de índice no reconocida: '+line)
        entries.append((match[1], int(match[2]), match[3]))
    return entries


def pdfpages(poppler, pdf):
    return subprocess.check_output([str(poppler/'pdftotext'), '-layout', str(pdf), '-'], text=True).split('\f')[:-1]


def normalize(text):
    lines = text.splitlines()
    occupied = [i for i, value in enumerate(lines) if value.strip()]
    if occupied and lines[occupied[0]].strip().startswith(
            ('Moonshine, dualidad T y pantallas', 'Estadística cuántica y radiación')):
        lines[occupied[0]] = ''
    if occupied and re.fullmatch(r'\d+', lines[occupied[-1]].strip()):
        lines[occupied[-1]] = ''
    text = '\n'.join(lines)
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    return re.sub(r'\s+', ' ', text).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--previous', type=Path, required=True)
    parser.add_argument('--current', type=Path, required=True)
    parser.add_argument('--poppler', type=Path, required=True)
    args = parser.parse_args()
    reports = []
    for key, directory, preamble, opening, summary, pdfname in JOBS:
        source, target = args.previous/directory, args.current/directory
        initial = json.loads((args.current/(directory+'_COPIA_INICIAL.json')).read_text())
        original_changes = [r['path'] for r in initial['files'] if sha(source/r['path']) != r['sha256']]
        tex = [r['path'] for r in initial['files'] if r['path'].endswith('.tex')]
        changed = {rel for rel in tex if sha(source/rel) != sha(target/rel)}
        allowed = {preamble, opening}
        precise = (expected_preamble((source/preamble).read_text(), key) == (target/preamble).read_text()
                   and expected_opening((source/opening).read_text(), key) == (target/opening).read_text())
        patch = ''.join(''.join(difflib.unified_diff((source/rel).read_text().splitlines(True),
                         (target/rel).read_text().splitlines(True), fromfile='a/'+rel,tofile='b/'+rel))
                         for rel in sorted(changed))
        (target/'DELTA_APERTURA_REV02.patch').write_text(patch)
        oldtoc, newtoc = toc(source/'build_apertura/main.toc'), toc(target/'build_apertura/main.toc')
        toc_same = len(oldtoc) == len(newtoc) and all(a[0] == b[0] for a,b in zip(oldtoc,newtoc))
        oldpdf, newpdf = source/'output/pdf'/pdfname, target/'output/pdf'/pdfname
        oldpages, newpages = pdfpages(args.poppler,oldpdf), pdfpages(args.poppler,newpdf)
        oldsummary, newsummary = normalize(oldpages[0]), normalize(newpages[0])
        summary_same = oldsummary[oldsummary.index('Resumen'):] == newsummary[newsummary.index('Resumen'):]
        whole = normalize('\n'.join(newpages))
        intro_first = normalize(newpages[1]).startswith(('1 Introducción', 'Introducción'))
        body_checks = []
        oldtops = [e for e in oldtoc if e[0].startswith('\\contentsline {section}')]
        newtops = [e for e in newtoc if e[0].startswith('\\contentsline {section}')]
        for entry in newtops:
            heading = re.search(r'\\numberline \{([^}]+)\}', entry[0])
            if heading:
                first = normalize(newpages[entry[1]-1])
                body_checks.append({'heading':entry[0], 'page':entry[1],
                                    'at_page_top':first.startswith(heading[1]+' ')})
        compilation = json.loads((target/'COMPILACION_APERTURA_REV02.json').read_text())
        errors = []
        if original_changes or changed != allowed or not precise: errors.append('Cotejo exacto de fuentes')
        if not toc_same: errors.append('Identidad de entradas del índice')
        if not summary_same or sha(source/summary) != sha(target/summary): errors.append('Resumen')
        if not intro_first: errors.append('Introducción en página2')
        if any(not e['at_page_top'] for e in body_checks): errors.append('Inicio de sección principal')
        if whole.count(AI) != 1 or whole.count(LABEL) != 1 or whole.count(COAUTHOR) != 1:
            errors.append('Atribución literal única')
        if any(compilation['log_findings'].values()) or compilation['sha256'] != sha(newpdf):
            errors.append('Compilación')
        report = {'scope':'Presentación editorial: fuentes, apertura, índice y controles de paginación; no certificación matemática.',
            'document':key, 'source':str(source), 'target':str(target),
            'original_files_checked':len(initial['files']), 'original_changes':original_changes,
            'tex_files_checked':len(tex), 'tex_files_identical':len(tex)-len(changed),
            'changed_tex':sorted(changed), 'changes_match_authorized_exact_transform':precise,
            'summary_source_identical':sha(source/summary)==sha(target/summary),
            'summary_complete_on_first_page':summary_same, 'introduction_starts_page2':intro_first,
            'toc_entries':len(newtoc), 'toc_titles_identical':toc_same,
            'toc_repagination':[{'title':a[0], 'before':a[1], 'after':b[1]} for a,b in zip(oldtoc,newtoc) if a[1]!=b[1]],
            'numbered_main_sections_page_top':body_checks,
            'source_pdf_sha256':sha(oldpdf), 'source_pages':len(oldpages),
            'pdf':str(newpdf), 'pdf_sha256':sha(newpdf), 'pages':len(newpages),
            'compilation':compilation, 'errors':errors,
            'status':'PASS_CONSERVACION_EDITORIAL_REV02' if not errors else 'REVISAR'}
        if key == 'IV':
            rel='sections/continuo_conjunto.tex'
            report['continuo_conjunto']={'sha256':sha(target/rel),
                'identical':sha(source/rel)==sha(target/rel),
                'included_in_fls':'INPUT ./'+rel in (target/'build_apertura/main.fls').read_text()}
            if not all(report['continuo_conjunto'][k] for k in ('identical','included_in_fls')):
                report['errors'].append('Continuo conjunto');report['status']='REVISAR'
        (target/'RECIBO_APERTURA_REV02.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        reports.append(report)
        print(json.dumps({k:report[k] for k in ('document','status','pages','pdf_sha256','errors')},ensure_ascii=False))
    raise SystemExit(any(r['errors'] for r in reports))


if __name__ == '__main__':
    main()
