#!/usr/bin/env python3
"""Conservación tipográfica REV03; no certificación matemática."""
import argparse
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('editorial_rev02', HERE/'verificar_aperturas_IV_V_rev02.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def expected(text, key):
    text = old.replace_once(text, old.LABEL+'\\par}\n\\vspace{8pt}',
                            old.LABEL+'\\par}\n\\vspace{6mm}')
    text = old.replace_once(text, '{\\small Coautoría sin prelación de contribución\\par}',
        '{\\fontsize{8}{10}\\selectfont Coautoría sin prelación de contribución\\par}')
    text = old.replace_once(text,
        '{\\small Integración y recopilación documental generadas por ChatGPT Astra.\\par}',
        '{\\fontsize{8}{10}\\selectfont Integración y recopilación documental generadas por ChatGPT - Astra.\\par}')
    if key == 'IV':
        text = old.replace_once(text, '{\\fontsize{17}{20.5}\\selectfont\\bfseries\\Titulo\\par}',
            '{\\fontsize{17}{20.5}\\selectfont\\bfseries\n'
            'Extensión de la estructura discreta del continuo:\\\\\n'
            'álgebras de operadores de vértice,\\\\\n'
            'Moonshine, dualidad T y teoría M\\par}')
    return text


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--previous', type=Path, required=True)
    p.add_argument('--current', type=Path, required=True)
    p.add_argument('--poppler', type=Path, required=True)
    a = p.parse_args()
    failure = False
    for key, directory, preamble, opening, summary, name in old.JOBS:
        source, target = a.previous/directory, a.current/directory
        copy = json.loads((a.current/(directory+'_COPIA_INICIAL.json')).read_text())
        damaged = [r['path'] for r in copy['files'] if old.sha(source/r['path']) != r['sha256']]
        tex = [r['path'] for r in copy['files'] if r['path'].endswith('.tex')]
        changes = [rel for rel in tex if old.sha(source/rel) != old.sha(target/rel)]
        exact = expected((source/opening).read_text(), key) == (target/opening).read_text()
        pdfold, pdfnew = source/'output/pdf'/name, target/'output/pdf'/name
        before, after = old.pdfpages(a.poppler,pdfold), old.pdfpages(a.poppler,pdfnew)
        rest = len(before)==len(after) and all(old.normalize(x)==old.normalize(y) for x,y in zip(before[1:],after[1:]))
        abstract_before, abstract_after = old.normalize(before[0]), old.normalize(after[0])
        abstract_ok = abstract_before[abstract_before.index('Resumen'):] == abstract_after[abstract_after.index('Resumen'):]
        toc_ok = (source/'build_apertura/main.toc').read_bytes()==(target/'build_apertura/main.toc').read_bytes()
        compilation = json.loads((target/'COMPILACION_APERTURA_REV03.json').read_text())
        phrase = 'Integración y recopilación documental generadas por ChatGPT - Astra.'
        text = old.normalize('\n'.join(after))
        literal = all(text.count(s)==1 for s in (old.LABEL, old.COAUTHOR, phrase))
        errors = []
        if damaged or changes != [opening] or not exact: errors.append('Conservación de fuentes')
        if not rest or not toc_ok: errors.append('Cuerpo o índice')
        if not abstract_ok or old.sha(source/summary)!=old.sha(target/summary): errors.append('Resumen')
        if not literal: errors.append('Textos literales de atribución')
        if compilation['sha256']!=old.sha(pdfnew) or any(compilation['log_findings'].values()): errors.append('Compilación')
        report = {'scope':'Cambios autorales de presentación, conservación del cuerpo y comprobación focal de inclusión; no nueva certificación matemática.',
            'document':key,'source':str(source),'target':str(target),
            'original_files_checked':len(copy['files']),'original_changes':damaged,
            'tex_files_checked':len(tex),'tex_identical':len(tex)-len(changes),
            'changed_tex':changes,'exact_authorized_transform':exact,
            'pages':len(after),'body_pages_compared':len(after)-1,
            'body_page_text_identical':rest,'toc_byte_identical':toc_ok,
            'summary_source_identical':old.sha(source/summary)==old.sha(target/summary),
            'full_summary_first_page':abstract_ok,'literal_attribution_single':literal,
            'source_pdf_sha256':old.sha(pdfold),'pdf':str(pdfnew),'sha256':old.sha(pdfnew),
            'normalization':'Cabecera y folio, espacios y particiones tipográficas; todas las páginas desde2 cotejadas una a una.',
            'compilation':compilation,'errors':errors,
            'status':'PASS_CONSERVACION_EDITORIAL_REV03' if not errors else 'REVISAR'}
        if key=='IV':
            rel='sections/continuo_conjunto.tex'
            report['joint_continuum']={'source':rel,'sha256':old.sha(target/rel),
                'source_identical':old.sha(source/rel)==old.sha(target/rel),
                'included_fls':'INPUT ./'+rel in (target/'build_apertura/main.fls').read_text(),
                'section':'4','pages':[37,38,39,40,41,42,43,44],
                'scope':'Inclusión material de las operaciones y pruebas del bloque conjunto bajo sus dominios declarados.'}
            if not report['joint_continuum']['source_identical'] or not report['joint_continuum']['included_fls']:
                errors.append('Inclusión conjunto');report['status']='REVISAR'
        patch=''.join(difflib.unified_diff((source/opening).read_text().splitlines(True),
            (target/opening).read_text().splitlines(True),fromfile='a/'+opening,tofile='b/'+opening))
        (target/'DELTA_APERTURA_REV03.patch').write_text(patch)
        (target/'RECIBO_APERTURA_REV03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:report[k] for k in ('document','status','pages','sha256','errors')},ensure_ascii=False))
        failure = failure or bool(errors)
    raise SystemExit(failure)


if __name__ == '__main__':
    main()
