#!/usr/bin/env python3
"""Preserva las dependencias seleccionadas de I y II sin editar sus textos.

Las envolturas relocalizan inputs y distinguen etiquetas de las dos fuentes.
El control acredita identidad de archivos y referencias declaradas; no compila.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

PROJECT = Path('/Users/ruben/Documents/New project')
SOURCE_I = PROJECT / 'output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909'
SOURCE_II = PROJECT / 'output/ARTICULO_II_AUTONOMIA_20260909_REVISION_05_TRABAJO'
I_ROOTS = ['sections/' + x + '.tex' for x in
           ('nucleo', 'extension', 'generacion', 'registro_k', 'alpha', 'excepcional')]
II_ROOTS = ['sections/' + x + '.tex' for x in (
    '03_actualizacion', '04_determinantes', '05_accion',
    '05b_coordenadas_angulares', '06_barbero', '06b_significado_incidencia',
    '07_elipse', '07b_geometria_elipse', 'revision_planck_contraste')]
OWNER_B01 = 'fuentes/propietarios_II/B01/c43_precedencia_dodecafasica_20260905.tex'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active(text: str) -> str:
    return '\n'.join(re.split(r'(?<!\\)%', line, 1)[0]
                     for line in text.splitlines())


def closure(source: Path, roots: list[str]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}

    def visit(relative: str) -> None:
        if relative in graph:
            return
        path = (source / relative).resolve()
        if source.resolve() not in path.parents or not path.is_file():
            raise SystemExit(f'Dependencia ausente o externa: {relative}')
        names = re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',
                           active(path.read_text()))
        graph[relative] = [n if Path(n).suffix else n + '.tex' for n in names]
        for name in graph[relative]:
            visit(name)

    for root in roots:
        visit(root)
    return graph


def unchanged_write(path: Path, text: str) -> None:
    raw = text.encode('utf-8')
    if path.exists() and path.read_bytes() != raw:
        raise SystemExit(f'Destino editado: se preserva sin sobrescribir {path}')
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


def copy_files(pairs: list[tuple[Path, Path]], destination: Path) -> list[dict]:
    for source, dest in pairs:
        if not source.is_file():
            raise SystemExit(f'Fuente ausente: {source}')
        if dest.exists() and dest.read_bytes() != source.read_bytes():
            raise SystemExit(f'Destino divergente preservado: {dest}')
    records = []
    for source, dest in pairs:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.copy2(source, dest)
        a, b = digest(source), digest(dest)
        if a != b:
            raise SystemExit(f'Fallo de identidad: {dest}')
        records.append({'source': str(source),
                        'destination': str(dest.relative_to(destination)),
                        'bytes': source.stat().st_size,
                        'sha256_source': a, 'sha256_destination': b})
    return records


def symbols(source: Path, paths: list[str]) -> tuple[dict, list, set]:
    labels, references, citations = {}, [], set()
    for relative in paths:
        for number, line in enumerate((source / relative).read_text().splitlines(), 1):
            line = active(line)
            for key in re.findall(r'\\label\{([^}]+)\}', line):
                labels.setdefault(key, []).append([relative, number])
            for key in re.findall(r'\\(?:ref|eqref|pageref|cref|Cref|autoref|nameref)\*?\{([^}]+)\}', line):
                references.append({'key': key, 'file': relative, 'line': number})
            for keys in re.findall(r'\\cite\w*\*?(?:\[[^]]*\])*\{([^}]+)\}', line):
                citations.update(keys.split(','))
    return labels, references, citations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-i', type=Path, default=SOURCE_I)
    parser.add_argument('--source-ii', type=Path, default=SOURCE_II)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    source_i, source_ii, root = args.source_i.resolve(), args.source_ii.resolve(), args.root.resolve()
    for source in (source_i, source_ii):
        if root == source or source in root.parents:
            raise SystemExit('La entrega no puede escribirse dentro de un original.')
    base_i, base_ii = root / 'base_articulo_I', root / 'base_articulo_II'
    original_manifest = base_i / 'MANIFIESTO_COPIA_NUCLEO.json'
    original_hash = digest(original_manifest)
    old_paths = {record['relative_path'] for record in json.loads(original_manifest.read_text())['files']}
    gi = closure(source_i, I_ROOTS)
    extra_i = sorted(set(gi) - old_paths)
    if len(gi) != 37 or len(extra_i) != 9:
        raise SystemExit(f'El cierre I cambió: {len(gi)} total; {len(extra_i)} adicionales.')
    records_i = copy_files([(source_i / p, base_i / p) for p in extra_i], base_i)
    manifest_i = {
        'scope': 'ADDITIVE_BYTE_IDENTICAL_COPY_NOT_MATHEMATICAL_CERTIFICATION',
        'previous_manifest': original_manifest.name, 'previous_manifest_sha256': original_hash,
        'new_file_count': len(records_i), 'active_tex_closure_count': len(gi),
        'graph': dict(sorted(gi.items())), 'files': records_i,
    }
    unchanged_write(base_i / 'MANIFIESTO_ADICION_EXCEPCIONAL.json',
                    json.dumps(manifest_i, ensure_ascii=False, indent=2) + '\n')
    manuscript_ii = source_ii / 'manuscrito'
    gii = closure(manuscript_ii, II_ROOTS)
    if len(gii) != 13:
        raise SystemExit(f'El cierre II cambió: {len(gii)} en lugar de 13.')
    pairs = [(manuscript_ii / p, base_ii / p) for p in sorted(gii)]
    owner_dest = 'propietarios/c43_precedencia_dodecafasica_20260905.tex'
    pairs.append((source_ii / OWNER_B01, base_ii / owner_dest))
    provenance = {
        'gestion/ESTADO_REVISION.json': 'procedencia/ESTADO_REVISION_II.json',
        'manuscrito/main.tex': 'procedencia/main_II_original.tex',
        'manuscrito/referencias_internas.tex': 'procedencia/referencias_internas_NO_ACTIVAR.tex',
        'manuscrito/sections/15_bibliografia_II.tex': 'procedencia/bibliografia_II_actual.tex',
        'fuentes/procedencia_editorial/bibliografia_predecesora.tex': 'procedencia/bibliografia_predecesora.tex',
        'fuentes/propietarios_II/A03/c35_componente_adimensional_retorno.tex': 'procedencia/c35_componente_adimensional_retorno.tex',
    }
    pairs += [(source_ii / p, base_ii / q) for p, q in provenance.items()]
    records_ii = copy_files(pairs, base_ii)
    ii_paths = sorted(gii) + [owner_dest]
    li, ri, ci = symbols(source_i, sorted(gi))
    lii, rii, cii = symbols(base_ii, ii_paths)
    unresolved_i = [r for r in ri if r['key'] not in li and r['key'] not in lii]
    unresolved_ii = [r for r in rii if r['key'] not in lii and r['key'] not in li]
    duplicate_labels = sorted(set(li) & set(lii))
    manifest_ii = {
        'scope': 'BYTE_IDENTICAL_SELECTED_DEPENDENCIES_NOT_GLOBAL_AUTONOMY_CERTIFICATE',
        'source_root': str(source_ii), 'source_revision': 'REVISION_05_TRABAJO',
        'source_state': json.loads((source_ii / 'gestion/ESTADO_REVISION.json').read_text()),
        'entry_points': II_ROOTS, 'literal_tex_closure_count': len(gii),
        'additional_public_owner': owner_dest, 'active_tex_count': len(ii_paths),
        'graph': dict(sorted(gii.items())), 'files': records_ii,
        'label_namespace': 'hmtII:', 'duplicate_original_labels': duplicate_labels,
        'unresolved_I_references': unresolved_i, 'unresolved_II_references': unresolved_ii,
        'required_I_citation_keys': sorted(ci), 'required_II_citation_keys': sorted(cii),
        'private_citation_remapper_not_activated': True,
    }
    unchanged_write(base_ii / 'MANIFIESTO_DEPENDENCIAS_II.json',
                    json.dumps(manifest_ii, ensure_ascii=False, indent=2) + '\n')

    i_wrapper = [
        '% Copia literal del núcleo seleccionado de I y su prolongación excepcional.',
        '% Compilar desde la raíz del artículo III. No sustituye el preámbulo.',
        r'\begingroup', r'\makeatletter',
        r'\def\input@path{{base_articulo_I/}}', r'\makeatother',
    ]
    i_wrapper += [r'\clearpage\input{base_articulo_I/' + p + '}' for p in I_ROOTS]
    i_wrapper += [r'\endgroup', '']
    unchanged_write(base_i / 'INCLUIR_NUCLEO_Y_EXCEPCIONAL_I.tex', '\n'.join(i_wrapper))

    wrapper = [
        '% Dependencias literales del artículo II, revisión 05.',
        '% Compilar desde la raíz III. Los rótulos técnicos se distinguen sin editar fuentes.',
        '% Las tres entradas de BIBITEMS_ADICIONALES_II.tex van dentro de la bibliografía final.',
        r'\begingroup', r'\makeatletter',
        r'\def\input@path{{base_articulo_II/}{base_articulo_I/}}', r'\makeatother',
        r'\providecommand{\HMT}{\mathrm{HMT}}', r'\providecommand{\Tr}{\operatorname{Tr}}',
        r'\providecommand{\dd}{\mathrm d}', r'\providecommand{\R}{\mathbb R}',
        r'\providecommand{\Z}{\mathbb Z}',
        r'\definecolor{ink}{HTML}{183D4A}', r'\definecolor{accent}{HTML}{8C3D2E}',
        r'\ifcsname apunte\endcsname\else',
        r'\newenvironment{apunte}[1]{\par\Needspace{6\baselineskip}\begin{quote}\small\raggedright\noindent\textbf{Nota de revisión: #1.} }{\end{quote}}',
        r'\fi', r'\let\HMTIILabelOriginal\label', r'\let\HMTIIRefOriginal\ref',
    ]
    for key in sorted(lii):
        wrapper.append(r'\expandafter\def\csname HMTIILabel@' + key + r'\endcsname{1}')
    wrapper += [
        r'\renewcommand{\label}[1]{\HMTIILabelOriginal{hmtII:#1}}',
        r'\RenewDocumentCommand{\ref}{s m}{\ifcsname HMTIILabel@#2\endcsname\IfBooleanTF{#1}{\HMTIIRefOriginal*{hmtII:#2}}{\HMTIIRefOriginal{hmtII:#2}}\else\IfBooleanTF{#1}{\HMTIIRefOriginal*{#2}}{\HMTIIRefOriginal{#2}}\fi}',
    ]
    for relative in II_ROOTS:
        if relative == 'sections/06_barbero.tex':
            wrapper.append(r'\clearpage\input{base_articulo_II/' + owner_dest + '}')
        prefix = r'\clearpage' if relative in (
            'sections/03_actualizacion.tex', 'sections/04_determinantes.tex',
            'sections/05_accion.tex', 'sections/06_barbero.tex', 'sections/07_elipse.tex') else ''
        wrapper.append(prefix + r'\input{base_articulo_II/' + relative + '}')
    wrapper += [r'\endgroup', '']
    unchanged_write(base_ii / 'INCLUIR_DEPENDENCIAS_II.tex', '\n'.join(wrapper))

    bibliography = (base_ii / 'procedencia/bibliografia_predecesora.tex').read_text()
    entries = {}
    chunks = re.split(r'(?=\\bibitem\{)', bibliography)
    for chunk in chunks:
        match = re.match(r'\\bibitem\{([^}]+)\}', chunk)
        if match and match.group(1) in {'registro', 'precedencia', 'elipse'}:
            entries[match.group(1)] = chunk.split(r'\end{thebibliography}', 1)[0].rstrip()
    if set(entries) != {'registro', 'precedencia', 'elipse'}:
        raise SystemExit('No se localizaron las tres entradas bibliográficas originales.')
    bib_add = '% Entradas literales de la bibliografía predecesora preservada por II.\n'
    bib_add += '% Insertar dentro de thebibliography, no como una segunda bibliografía.\n'
    bib_add += '\n\n'.join(entries[k] for k in ('registro', 'precedencia', 'elipse')) + '\n'
    unchanged_write(base_ii / 'BIBITEMS_ADICIONALES_II.tex', bib_add)
    if digest(original_manifest) != original_hash:
        raise SystemExit('Se alteró el manifiesto previo, operación prohibida.')
    result = {
        'status': 'PASS_COPIAS_LITERALMENTE_IDENTICAS_REFERENCIAS_DECLARADAS_RESUELTAS'
                  if not unresolved_i and not unresolved_ii else 'UNRESOLVED_REFERENCES',
        'I_extra_files': len(records_i), 'II_copied_files': len(records_ii),
        'II_active_tex': len(ii_paths), 'duplicate_labels_isolated': duplicate_labels,
        'manifests': {str(p.relative_to(root)): digest(p) for p in (
            original_manifest, base_i / 'MANIFIESTO_ADICION_EXCEPCIONAL.json',
            base_ii / 'MANIFIESTO_DEPENDENCIAS_II.json')},
        'compilation_performed': False, 'mathematical_certification_performed': False,
    }
    unchanged_write(root / 'technical/RECIBO_COPIAS_DEPENDENCIAS_I_II.json',
                    json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
