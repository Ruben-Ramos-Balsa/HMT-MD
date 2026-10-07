#!/usr/bin/env python3
"""Cotejo editorial de la sucesora; no realiza una auditoría matemática."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    from PIL import Image, ImageChops
    from pypdf import PdfReader
    initial = json.loads((ROOT/'gestion/PRESERVACION_PRESENTACION_INICIAL.json').read_text())
    source = Path(initial['source'])
    checks = []
    for entry in initial['unchanged_content']:
        a,b = source/entry['path'],ROOT/entry['path']
        match = sha(a)==sha(b)==entry['sha256']
        checks.append({**entry,'source_current_sha256':sha(a),'successor_sha256':sha(b),'identical':match})
    if not all(x['identical'] for x in checks):
        raise RuntimeError('Diferencia de contenido protegido')
    originals = []
    for key in ['original_pdf','original_zip']:
        entry = initial[key]
        got = sha(Path(entry['path']))
        if got!=entry['sha256']:
            raise RuntimeError('Se ha alterado un original: '+key)
        originals.append({**entry,'unchanged':True})
    new_pdf = ROOT/'output/pdf/ARITMETICA_GENEALOGICA_PRIMOS_Y_ESTRUCTURA_ESPECTRAL_ZETA.pdf'
    old_reader = PdfReader(initial['original_pdf']['path'])
    new_reader = PdfReader(new_pdf)
    if len(old_reader.pages)!=len(new_reader.pages):
        raise RuntimeError('Cambio de paginación no previsto')
    normalize = lambda s: re.sub(r'\s+',' ',s).strip()
    old_cover = old_reader.pages[0].extract_text()
    new_cover = new_reader.pages[0].extract_text()
    for text in ['Artículo VIII','Edición de lectura del manuscrito de trabajo']:
        old_cover = old_cover.replace(text,'')
        if text in new_cover:
            raise RuntimeError('Rótulo no retirado de portada')
    if normalize(old_cover)!=normalize(new_cover):
        raise RuntimeError('La portada cambió más allá de los dos rótulos')
    metadata = {str(k):str(v) for k,v in new_reader.metadata.items()}
    for forbidden in ['Artículo VIII','Edición de lectura del manuscrito de trabajo','Edición de lectura']:
        if any(forbidden.casefold() in v.casefold() for v in metadata.values()):
            raise RuntimeError('Rótulo no retirado de metadatos')
    if any('edición de lectura' in normalize(p.extract_text()).casefold() for p in new_reader.pages):
        raise RuntimeError('Denominación actual no retirada del texto público')
    # Cotejo de cada fuente TeX local realmente incluida: sólo las sustituciones
    # léxicas autorizadas pueden diferir; no se permite cambiar las matemáticas.
    allowed = {
        'main_lectura.tex': [
            ('{\\Large\\scshape Artículo VIII\\par}\n',''),
            ('{\\large Edición de lectura del manuscrito de trabajo\\par}\n','')],
        'preambulo_lectura.tex': [
            ('\\fancyhead[R]{\\fontsize{8}{10}\\selectfont Edición de lectura}', '\\fancyhead[R]{}'),
            ('pdfsubject={Edición de lectura del manuscrito de trabajo. La positividad global no se demuestra en esta edición.}',
             'pdfsubject={La positividad global no se demuestra en esta edición.}')],
        'gestion/lectura_resumen.tex': [('esta edición de lectura','este manuscrito')],
        'gestion/lectura_conclusiones.tex': [('Conclusiones y alcance de la edición de lectura','Conclusiones y alcance del manuscrito')],
    }
    fls = (ROOT/'build_lectura/main_lectura.fls').read_text()
    included = set()
    for line in fls.splitlines():
        if not line.startswith('INPUT '):
            continue
        p = Path(line[6:])
        p = p if p.is_absolute() else ROOT/p
        try:
            relative = p.resolve().relative_to(ROOT.resolve())
        except ValueError:
            continue
        if relative.suffix=='.tex' and (source/relative).exists():
            included.add(str(relative))
    tex_checks = []
    for relative in sorted(included):
        expected = (source/relative).read_text()
        changes = []
        for before,after in allowed.get(relative,[]):
            count = expected.count(before)
            if count!=1:
                raise RuntimeError('Sustitución autorizada no única: '+relative)
            expected = expected.replace(before,after)
            changes.append({'before':before,'after':after,'count':count})
        actual = (ROOT/relative).read_text()
        if expected!=actual:
            raise RuntimeError('Cambio TeX no autorizado: '+relative)
        tex_checks.append({'path':relative,'source_sha256':sha(source/relative),
                           'successor_sha256':sha(ROOT/relative),'authorized_substitutions':changes,
                           'otherwise_identical':True})
    if not set(allowed).issubset(included):
        raise RuntimeError('Una fuente de presentación no fue incluida')
    old_images = source/'gestion/qa_lectura_final/pages'
    new_images = ROOT/'gestion/qa_presentacion/pages'
    rendered = []
    changed = []
    for number in range(2,len(new_reader.pages)+1):
        filename=f'page-{number:03d}.png'
        with Image.open(old_images/filename) as old,Image.open(new_images/filename) as new:
            if old.size!=new.size:
                raise RuntimeError('Tamaño de render diferente')
            box = (0,80,old.width,old.height)
            identical = ImageChops.difference(old.convert('RGB').crop(box),new.convert('RGB').crop(box)).getbbox() is None
        (rendered if identical else changed).append(number)
    log=(ROOT/'build_lectura/main_lectura.log').read_text()
    findings={key:len(re.findall(pattern,log)) for key,pattern in {
        'overfull':r'Overfull \\hbox|Overfull \\vbox',
        'undefined_references':r'Reference .* undefined',
        'missing_glyphs':r'Missing character',
        'underfull':r'Underfull \\hbox|Underfull \\vbox'}.items()}
    compile_receipt=json.loads((ROOT/'gestion/RECIBO_EDICION_LECTURA.json').read_text())
    if not all(x['included_in_fls'] for x in compile_receipt['common_sources']):
        raise RuntimeError('Fuente común no incluida')
    receipt={'scope':'Cambio de presentación exclusivamente; alcance científico inalterado',
             'pdf':str(new_pdf),'sha256':sha(new_pdf),'pages':len(new_reader.pages),
             'preserved_content':checks,'originals_unchanged':originals,
             'cover_only_authorized_labels_removed':True,
             'metadata':metadata,'metadata_rejected_labels_absent':True,
             'all_included_tex_sources_checked':tex_checks,
             'public_current_edition_label_absent':True,
             'all_noncover_body_images_identical':not changed,
             'body_pages_with_authorized_lexical_reflow':changed,
             'identical_body_pages':rendered,'image_comparison_crop_top_pixels':80,
             'dpi':90,'common_inclusion_fls':'6/6','compilation_passes':3,
             'log_findings':findings,'human_visual_review':'Registro separado: gestion/QA_VISUAL_PRESENTACION_20260911.md; la inspección humana no es evaluada por este script'}
    (ROOT/'gestion/RECIBO_PRESENTACION_20260911.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'pages':receipt['pages'],'sha256':receipt['sha256'],'identical_body_pages':len(rendered),'reflowed_body_pages':changed,'included_tex_sources':len(tex_checks),'protected_files':len(checks),'log':findings},ensure_ascii=False))

if __name__=='__main__':
    main()
