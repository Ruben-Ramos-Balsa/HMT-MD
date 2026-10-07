#!/usr/bin/env python3
"""Publicación documental legible del catálogo congelado del Artículo VI.

No genera masas ni realiza selección física o comparación numérica. Lee los
JSON literales ya preservados y produce fuentes LaTeX, sin compilar. Los
apéndices de estructura son separables del volumen de datos completo.

Uso: python3 -I -S technical/generar_apendices_catalogo.py [--check] [--self-test] [--companion-only]
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TECH = ROOT / 'technical'
SOURCES = {'multisecciones': 13, 'familias': 56, 'clases': 23,
           'rutas': 324, 'rutas_enriquecidas': 324, 'masas': 471, 'anchuras': 384}
SPECIAL = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}',
           '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
           '_': r'\_', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
BREAK = r'\allowbreak{}'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def tex(value: str, *, empty: bool = True) -> str:
    """Escape every source character; break opportunities do not alter digits.

    No source text is emitted as a command or interpreted as trusted LaTeX.
    Empty fields remain distinguished from unavailable or inapplicable fields.
    """
    if not isinstance(value, str):
        raise TypeError('Las celdas deben conservar su tipo literal de cadena')
    if not value:
        return r'\textemdash{}' if empty else ''
    # Ordinary prose is left to language-aware hyphenation. Only long numeric
    # strings, hashes and pure technical codes receive fixed-size breaks.
    # Identifier components break at their delimiters, not inside normal words.
    chunk_ends = set()
    token_pattern = r'[A-Za-z0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?'
    for match in re.finditer(token_pattern, value):
        token = match.group()
        numeric = bool(re.fullmatch(r'[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?', token))
        hexadecimal = len(token) >= 16 and bool(re.fullmatch(r'[0-9A-Fa-f]+', token))
        pure_code = len(token) >= 16 and (
            token.isupper() or (token.isalnum() and any(c.isdigit() for c in token)))
        if len(token) > 8 and (numeric or hexadecimal or pure_code):
            chunk_ends.update(range(match.start() + 8, match.end(), 8))
    out = []
    for position, char in enumerate(value):
        if char in '\n\r\t':
            out.append(' ')
            continue
        if ord(char) < 32:
            raise ValueError('Carácter de control no publicable')
        out.append(SPECIAL.get(char, char))
        # A sign sequence is data, not TeX typography: -- and --- must keep
        # two and three individual signs, rather than becoming dash ligatures.
        if char == '-' and position + 1 < len(value) and value[position + 1] == '-':
            out.append(r'\kern0pt{}')
        at_delimiter = (char in '_|/:;,=>)' and position + 1 < len(value)
                        and not value[position + 1].isspace())
        if at_delimiter or position + 1 in chunk_ends:
            out.append(BREAK)
    return ''.join(out)


def joined(values: dict, fields: list[tuple[str, str]]) -> str:
    return r'\par '.join(r'\textit{' + tex(label) + '}: ' + tex(values[field])
                         for field, label in fields)


def marker(kind: str, ordinal: int) -> str:
    return f'% VI-CATALOG-ROW {kind} {ordinal}\n'


def table_start(columns: str, headings: list[str], caption: str, label: str,
                *, continuation: str = 'Continuación',
                continuation_footer: str = 'Continúa en la página siguiente',
                arraystretch: str = '1.13') -> str:
    head = ' & '.join(headings) + r' \\' + '\n'
    n = len(headings)
    return ('\n\\begingroup\n\\setlength{\\tabcolsep}{4pt}\n'
            '\\setlength{\\extrarowheight}{4pt}\n'
            '\\renewcommand{\\arraystretch}{' + arraystretch + '}\n'
            '\\begin{longtable}{' + columns + '}\n'
            '\\caption{' + caption + '}\\label{' + label + r'}\\' + '\n'
            '\\toprule\n' + head + '\\midrule\n\\endfirsthead\n'
            '\\multicolumn{' + str(n) + r'}{l}{\textit{' + continuation + r'}}\\' + '\n'
            '\\toprule\n' + head + '\\midrule\n\\endhead\n'
            '\\midrule\n\\multicolumn{' + str(n) + r'}{r}{' + continuation_footer + r'}\\'
            '\n\\endfoot\n\\bottomrule\n\\endlastfoot\n')


def table_end() -> str:
    return '\\end{longtable}\n\\endgroup\n'


def row(cells: list[str]) -> str:
    # The table-local ``\\extrarowheight`` makes the four points part of the
    # row box itself.  Longtable can therefore break only between complete
    # rows, with no detached ``\\noalign`` material capable of crossing an
    # ``\\endhead`` boundary or displacing a continuation header.
    return ' & '.join(cells) + r' \\' + '\n'


def cols(widths: list[float]) -> str:
    # Relative widths fit both the principal article (156 mm) and the companion
    # (170 mm). Subtract padding explicitly; never assume the caller's margins.
    total = sum(widths)
    return '@{}' + ''.join('>{\\raggedright\\arraybackslash}p{\\dimexpr '
                           + f'{w / total:.8f}'
                           + '\\linewidth-2\\tabcolsep\\relax}' for w in widths) + '@{}'


CLASS_STATUS = {
    'CLOSED_ELECTRON_TWO_WAY': 'Electrón: cierre bidireccional documentado.',
    'OPEN_PHYSICAL_SCALARIZATION': 'Escalarización física abierta en este corte.',
    'OPEN_MIXING_AND_SCALE': 'Mezcla y escala abiertas en este corte.',
    'OPEN_FLAVOR_COLOR_SCALARIZATION': 'Escalarización de sabor y color abierta en este corte.',
    'CLOSED_NULL_CHART': 'Carta nula cerrada en este corte.',
    'OPEN_ROUTE_AND_SCALARIZATION': 'Ruta y escalarización abiertas en este corte.',
    'OPEN_NAMED_STATE_SCALARIZATION': 'Escalarización del estado individualizado abierta en este corte.',
    'NOT_A_UNIVERSAL_MASS_SCALAR': 'La clase no se publica como un escalar universal de masa.',
}
OBS_STATUS = {
    'EXTERNAL_RECORD_ACCOUNTED__INDIVIDUAL_HMT_REALIZATION_NOT_YET_JOINED':
        'Registro externo censado; realización HMT individual todavía no enlazada en este corte.',
    'EXACT_COLOR_FIBER_OPERATOR__NOMINAL_SIGNATURE_CONDITIONED__SCHEME_OPEN':
        'Operador de fibra de color exacto; firma nominal condicionada; esquema abierto.',
    'NULL_SECTION_CLOSED': 'Sección nula cerrada.',
    'SCALAR_CLOSED_ELECTRON_BETA': 'Escalar electrónico beta cerrado.',
    'EXACT_FIBER_OPERATOR__NOMINAL_SIGNATURE_CONDITIONED__SCALARIZATION_OPEN':
        'Operador de fibra exacto; firma nominal condicionada; escalarización abierta.',
    'CONDITIONED_NOMINAL_SIGNATURE__ROUTE_AND_POLE_REALIZATION_OPEN':
        'Firma nominal condicionada; realización de ruta y polo abierta.',
}
MAP_NAMES = {
    'named_baryon_binding_map': 'Enlace de unión del barión individualizado.',
    'typed_gravitational_representation_map': 'Representación gravitatoria tipada.',
    'named_meson_binding_map': 'Enlace de unión del mesón individualizado.',
    'flavor_color_coupling_to_spectral_projection_then_scheme_scale_transport':
        'Acoplamiento sabor–color a la proyección espectral y transporte de esquema y escala.',
    'quark_identity_scheme_scale_map': 'Identidad del quark, esquema y escala.',
    'NONE_FOR_MASS_NULLITY': 'Ninguno para la nulidad de masa, según el registro.',
    'identity_to_public_sector_or_new_typed_sector': 'Identidad y sector público o nuevo sector tipado.',
    'NONE': 'Ninguno, según el registro.',
    'generation_coupling_to_spectral_projection_without_mass_target':
        'Acoplamiento generacional a la proyección espectral sin masa objetivo.',
    'join_named_boson_to_enriched_route_then_complex_pole_operator':
        'Bosón individualizado, ruta con memoria y operador de polo complejo.',
}


def codebook(values: set[str], prefix: str) -> dict[str, str]:
    return {value: f'{prefix}{i:02d}' for i, value in enumerate(sorted(values), 1)}


def legend(codes: dict[str, str], explanations: dict[str, str], caption: str, label: str) -> str:
    out = [table_start(cols([14, 66, 78]), ['Clave', 'Estado literal', 'Lectura documental'], caption, label)]
    for original, code in codes.items():
        if original not in explanations:
            raise ValueError('Estado no tipado en la leyenda: ' + original)
        out.append(row([tex(code), tex(original), tex(explanations[original])]))
    out.append(table_end())
    return ''.join(out)


def structural(docs: dict) -> str:
    out = [r'''% Generado por technical/generar_apendices_catalogo.py. No editar a mano.
\clearpage
\section{Catálogos de multisecciones, familias y clases}
\label{sec:vi-catalogos-estructurales}

Este apéndice organiza tres niveles distintos del inventario interno. Las
13 multisecciones reúnen celdas del atlas; las 56 familias clasifican rutas
internas; las 23 clases documentan la articulación con sectores y
representaciones físicas. Estos cardinales no cuentan el mismo objeto y
no se suman para obtener un número de partículas. Las tablas acompañan las
definiciones y demostraciones del artículo: su función es permitir localizar
cada registro, sus incidencias y sus lectores, no sustituir una prueba por un censo.

Se conserva el orden documental de las filas, sus identificadores y todas
las repeticiones que figuren en las fuentes. Los identificadores literales
permiten cotejar las tablas con los archivos JSON. Una raya indica una celda
vacía de la fuente; no representa un cero. Los archivos conservan además todos
los campos y cifras, los estados originales y la procedencia verificable.
\CatalogRouteReference
% La remisión depende del punto de entrada: artículo o catálogo.

\subsection{Las 13 multisecciones del atlas}

Para una multisección \(M\), sea \(\mathcal C(M)\) su conjunto de celdas y
sea \(\gamma_{B_1}(c)\) la ruta primaria que el atlas conserva en la celda
\(c\). En este apéndice estructural se define la fibra
\[
 B_1(M):=
 \operatorname{span}\bigl\{e_{\gamma_{B_1}(c)}:c\in\mathcal C(M)\bigr\}
 \subseteq \ell^2(\mathcal R_{\mathrm{adm}}).
\]
Las rutas primarias de celdas distintas determinan vectores básicos distintos;
por consiguiente,
\(\operatorname{rank}B_1(M)=\dim B_1(M)=\#\mathcal C(M)\).
Esta definición fija el objeto al que se refiere el rango de la tabla; la
columna de familias cuenta las
familias de ruta presentes, no especies físicas. Se conservan separadamente
los espectros enteros de los lectores \(K_D\) y \(K_\Omega\).
En la notación literal \texttt{x} indica multiplicidad. Las 13 filas tienen
el estado documental de operador diagonal exacto sobre la fibra \(B_1\).
Su publicación como escalar físico requiere el transporte declarado, salvo
la selección de rango uno prevista en el propio registro. Este enunciado
reproduce el alcance registrado y no convierte todos los espectros en masas únicas.
''']
    out.append(table_start(cols([31, 31, 48, 46]),
        ['Multisección', 'Rango e incidencia', 'Clasificación y profundidad', 'Lectores enteros'],
        'Las 13 multisecciones, sin selección de filas.', 'tab:vi-multisecciones'))
    for rec in docs['multisecciones']['records']:
        v = rec['values']
        out.append(marker('multisecciones', rec['source_ordinal']))
        out.append(row([tex(v['structural_multisection']),
            joined(v, [('rank_B1', 'Rango'), ('cells', 'Celdas (identificadores)'), ('route_family_count', 'Familias')]),
            joined(v, [('physical_families', 'Familia'), ('generation_depths', 'Profundidad'), ('colors', 'Color')]),
            joined(v, [('K_D_spectrum', 'K D'), ('K_Omega_spectrum', 'K Ω')])]))
    out.append(table_end())
    out.append(r'''\subsection{Las 56 familias de ruta}

La firma que identifica una familia se conserva literalmente, con sus signos
y separadores. Las celdas y multisecciones hacen visible que una familia de
ruta no equivale por definición a una especie física. Los perfiles conjuntos
cuentan las combinaciones registradas dentro de la familia. Los espectros
decimales del carácter y los espectros completos de firma permanecen íntegros
en \texttt{catalogo\_familias.json}; aquí se publican la incidencia y los
lectores enteros que permiten orientarse en esa información.
''')
    out.append(table_start(cols([34, 54, 34, 34]),
        ['Familia y firma', 'Incidencia', r'\(K_D\)', r'\(K_\Omega\)'],
        'Las 56 familias internas de ruta.', 'tab:vi-familias'))
    for rec in docs['familias']['records']:
        v = rec['values']
        out.append(marker('familias', rec['source_ordinal']))
        out.append(row([str(rec['source_ordinal']) + r'\par ' + tex(v['route_family_R']),
            joined(v, [('cell_count_B1', 'Número de celdas'), ('cells', 'Celdas (identificadores)'),
                       ('structural_multisections', 'Multisecciones'),
                       ('physical_families', 'Familias'), ('colors', 'Color'),
                       ('joint_profile_count', 'Perfiles conjuntos')]),
            tex(v['K_D_spectrum']), tex(v['K_Omega_spectrum'])]))
    out.append(table_end())
    out.append(r'''\subsection{Las 23 clases documentadas}

Estas filas reúnen sectores públicos, residencias y representación. La clave
de estado remite a la leyenda contigua y conserva el estatuto de la fuente.
En particular, un operador interno exacto, una evaluación condicionada y una
realización escalar cerrada se mantienen como afirmaciones distintas. La tabla
no actualiza su estatuto ni transforma un registro condicionado en una predicción.
''')
    statuses = codebook({r['values']['scalarization_status'] for r in docs['clases']['records']}, 'C')
    out.append(legend(statuses, CLASS_STATUS, 'Estados originales de las clases.', 'tab:vi-estados-clases'))
    out.append(table_start(cols([27, 60, 52, 17]),
        ['Clase', 'Representantes y residencia', 'Incidencia y representación', 'Estado'],
        'Las 23 clases del catálogo, en su orden documental.', 'tab:vi-clases',
        arraystretch='1.08'))
    for rec in docs['clases']['records']:
        v = rec['values']
        out.append(marker('clases', rec['source_ordinal']))
        out.append(row([tex(v['record_id']) + r'\par ' + tex(v['sector']),
            joined(v, [('representatives', 'Representantes'), ('hmt_residence', 'Residencia')]),
            joined(v, [('selected_cell_count', 'Celdas seleccionadas'),
                       ('structural_multisections', 'Multisecciones'),
                       ('physical_charge', 'Carga'), ('color_or_representation', 'Representación')]),
            tex(statuses[v['scalarization_status']])]))
    out.append(table_end())
    return ''.join(out)


ROUTE_GROUPS = [
    ('Identidad y orientación', [('candidate_id', 'Identificador'), ('cell_id', 'Celda'),
       ('r', 'Fila'), ('c', 'Columna'), ('h0', 'Orientación horizontal'), ('v0', 'Orientación vertical'),
       ('is_B1_route', 'Pertenencia a B1')]),
    ('Clasificación', [('coarse_class', 'Clase'), ('family', 'Familia'), ('sector', 'Sector'),
       ('generation', 'Generación'), ('color', 'Color'), ('structural_multisection', 'Multisección'),
       ('physical_family', 'Familia física'), ('generation_depth', 'Profundidad'),
       ('rho_orbit', 'Órbita de inversión'), ('route_family_R', 'Familia de ruta')]),
    ('Retornos', [('first_class_phase_return', 'Clase y fase'), ('first_orbit_phase_return', 'Órbita y fase'),
       ('first_cell_phase_return', 'Celda y fase'),
       ('first_kinematic_state_return_within_108', 'Estado cinemático en 108'),
       ('first_kinematic_state_return_extended', 'Estado cinemático, extensión')]),
    ('Memoria y transporte', [('turns', 'Giros'), ('sheet_switches', 'Cambios de hoja'),
       ('carry_debt_total', 'Deuda total'), ('carry_debt_final', 'Deuda final'),
       ('delayed_carry_blocks', 'Bloques diferidos'),
       ('stable_decimal_triads_final', 'Tríadas estables finales'),
       ('w6_repeat_K_to_Kplus9', 'Repeticiones en K y K+9'),
       ('prefix_memory_changes_K_to_Kplus9', 'Cambios de memoria en K y K+9')]),
    ('Firma y fase', [('nA_raw', 'n A crudo'), ('sC_raw', 's C crudo'), ('kappa0_raw', 'κ 0 crudo'),
       ('nu120_raw', 'ν 120 crudo'), ('nu270_raw', 'ν 270 crudo'), ('tau12', 'τ 12'),
       ('historic_signature_Z5', 'Firma histórica Z5')]),
    ('Diferencias y contadores', [('D1', 'D1'), ('D3', 'D3'), ('D4', 'D4'), ('D27', 'D27'),
       ('D36', 'D36'), ('Omega90_120', 'Ω 90/120'), ('P6', 'P6')]),
    ('Lectores enteros', [('K_D', 'K D'), ('K_Omega', 'K Ω')]),
    ('Evaluaciones de lectores', [('kappa_D', 'κ D'), ('kappa_Omega', 'κ Ω'),
       ('Ract_factor_D', 'Factor de acción D'), ('Ract_factor_Omega', 'Factor de acción Ω')]),
    ('Separación de prefijos', [('prefix_ambiguity_area', 'Área de ambigüedad'),
       ('prefix_log2_ambiguity_area', 'Área log2 de ambigüedad'),
       ('first_orbit_separation_block', 'Primer bloque de separación de órbita'),
       ('first_cell_separation_block', 'Primer bloque de separación de celda'),
       ('first_route_separation_block', 'Primer bloque de separación de ruta'),
       ('final_ambiguity', 'Ambigüedad final')]),
    ('Secuencias completas', [('w6_words', 'Bloques w6'), ('stable_triads_by_block', 'Tríadas estables por bloque')]),
    ('Estados documentados', [('route_status', 'Estado de ruta'),
       ('pareto_persistence_orbit', 'Persistencia de Pareto de órbita'),
       ('join_status', 'Estado de correspondencia'), ('tower_forward_status', 'Estado de torre')]),
    ('Huellas de procedencia', [('route_genealogy_sha256', 'Genealogía de ruta'),
       ('reader_sha256', 'Lector'), ('cell_ledger_108_sha256', 'Registro de celda en 108')]),
]


def route_navigation_index(records: list[dict]) -> str:
    """Publish every exact route identifier with its live LaTeX page reference."""
    out = [r'''\subsection*{Índice de identificadores y páginas}
\phantomsection
\addcontentsline{toc}{subsection}{Índice de las 324 rutas: identificador y página}
\label{sec:vi-indice-rutas}

Cada identificador enlaza con el comienzo de su ficha. La página indicada es
la numeración impresa del volumen. Los identificadores se leen por filas,
de izquierda a derecha, conservando el orden de la tabla unificada.
El panel de marcadores del PDF permite asimismo elegir primero la celda
y después la orientación horizontal y vertical. Las cuatro orientaciones
de una celda son rutas distintas, no versiones de una misma ficha.
''']
    out.append(table_start(cols([62, 15, 62, 15]),
        ['Identificador de ruta', 'Página', 'Identificador de ruta', 'Página'],
        'Índice completo de las 324 rutas orientadas.', 'tab:vi-indice-rutas',
        continuation='Índice de las 324 rutas: identificador y página (continuación)'))
    for start in range(0, len(records), 2):
        cells = []
        for rec in records[start:start + 2]:
            ident = tex(rec['values']['candidate_id'])
            label = 'nav:vi-ruta-' + str(rec['source_ordinal'])
            cells.extend([r'\hyperref[' + label + ']{' + ident + '}',
                          r'\pageref{' + label + '}'])
        cells.extend([''] * (4 - len(cells)))
        out.append(row(cells))
    out.append(table_end())
    out.append('\\clearpage\n')
    return ''.join(out)


def route_catalog(docs: dict) -> tuple[str, dict]:
    raw = docs['rutas']['records']
    enriched = docs['rutas_enriquecidas']['records']
    # Keys are checked one-to-one. No deduplication is used to obtain 324.
    akeys = [r['values']['candidate_id'] for r in raw]
    bkeys = [r['values']['candidate_id'] for r in enriched]
    if len(set(akeys)) != len(akeys) or len(set(bkeys)) != len(bkeys):
        raise ValueError('Identificador repetido: requiere tipar la relación, no deduplicar')
    if set(akeys) != set(bkeys):
        raise ValueError('Las dos tablas de rutas no tienen idéntico dominio de claves')
    enriched_index = {r['values']['candidate_id']: r for r in enriched}
    field_list = [field for _, fields in ROUTE_GROUPS for field, _ in fields]
    expected_fields = set(docs['rutas']['fields']) | set(docs['rutas_enriquecidas']['fields'])
    if len(field_list) != len(set(field_list)) or set(field_list) != expected_fields:
        raise ValueError('La ficha debe publicar exactamente la unión de campos de las dos tablas')
    out = [r'''\clearpage
\section{Las 324 rutas orientadas: fichas completas}
\label{sec:vi-324-rutas}

Cada ficha conserva todos los campos de la unión de las dos tablas de rutas.
La correspondencia se realiza por el identificador exacto, nunca por proximidad
de valores. Los campos comunes se cotejan literalmente antes de representarlos
una sola vez; los campos exclusivos de ambas tablas se incorporan íntegros.
Se imprimen los ordinales de ambas fuentes para reconstruir sus órdenes originales.
La ficha conserva las cifras decimales tal como estaban registradas; no las
recalcula ni les atribuye exactitud matemática por el solo hecho de imprimirlas.

Los retornos de clase, órbita, celda y estado cinemático son campos distintos.
Lo mismo ocurre con repetición de fase y cambio de memoria, con los lectores
\(K_D\) y \(K_\Omega\), y con una ruta interna y su eventual representación
física. Los estados documentales se reproducen literalmente. Las huellas
SHA-256 permiten localizar sus antecedentes, pero no sustituyen sus pruebas.
''']
    out.append(route_navigation_index(raw))
    seen_cells = set()
    navigation = []
    common_checks = 0
    for rec in raw:
        v = rec['values']
        other = enriched_index[v['candidate_id']]
        w = other['values']
        for field in v.keys() & w.keys():
            if v[field] != w[field]:
                raise ValueError(f'Campo común divergente: {v["candidate_id"]}:{field}')
            common_checks += 1
        merged = dict(v)
        merged.update(w)
        ordinal = rec['source_ordinal']
        out.append(marker('rutas', ordinal))
        out.append(r'\Needspace{18\baselineskip}' + '\n'
                   + r'\phantomsection' + '\n')
        cell = int(v['cell_id'])
        if cell not in seen_cells:
            seen_cells.add(cell)
            out.append(r'\pdfbookmark[2]{Celda ' + f'{cell:02d}'
                       + ' (fila ' + v['r'] + ', columna ' + v['c'] + ')}{vi-celda-'
                       + str(cell) + '}\n')
        ident = tex(v['candidate_id'])
        bookmark_ident = ident.replace(BREAK, '').replace(r'\kern0pt{}', '')
        orientation = 'h=' + v['h0'] + ', v=' + v['v0']
        out.append(r'\pdfbookmark[3]{Ruta ' + f'{ordinal:03d}' + ': '
                   + bookmark_ident + ' (' + orientation + ')}{vi-ruta-'
                   + str(ordinal) + '}\n'
                   + r'\phantomsection\label{nav:vi-ruta-' + str(ordinal) + '}\n'
                   + r'\subsection*{Ruta ' + f'{ordinal:03d}' + ' — ' + ident + '}\n')
        out.append(r'\noindent\textbf{Celda ' + f'{cell:02d}' + ': fila '
                   + v['r'] + ', columna ' + v['c'] + '. Orientación '
                   + orientation + '.}\\par\n'
                   + r'\hyperref[sec:vi-indice-rutas]{Volver al índice de identificadores.}' + '\n')
        out.append('Ordinal en la tabla unificada: ' + str(ordinal)
                   + '; ordinal en la tabla de memoria: ' + str(other['source_ordinal']) + '.\n')
        out.append(table_start(cols([36, 125]), ['Grupo', 'Datos de la ruta'],
                    'Ficha ' + f'{ordinal:03d}' + ': ' + ident, 'tab:vi-ruta-' + str(ordinal),
                    continuation='Ficha ' + f'{ordinal:03d}' + ' — ' + ident
                                 + ' (' + orientation + ') — Continuación',
                    continuation_footer='Ficha ' + f'{ordinal:03d}' + ' — ' + ident
                                        + ': continúa en la página siguiente'))
        for label, fields in ROUTE_GROUPS:
            # Bounded groups: at most three fields per row so no oversized row
            # can obstruct longtable page breaks. All fields remain represented.
            for offset in range(0, len(fields), 3):
                block = fields[offset:offset + 3]
                compact = (r';\enspace '.join(r'\textit{' + tex(name) + '}: ' + tex(merged[field])
                                             for field, name in block)
                           if all(len(merged[field]) <= 35 for field, _ in block)
                           else joined(merged, block))
                out.append(row([tex(label) if offset == 0 else tex(label + ' (cont.)'), compact]))
        out.append(table_end())
        navigation.append({'source_ordinal': ordinal, 'candidate_id': v['candidate_id'],
                           'cell_id': v['cell_id'], 'row': v['r'], 'column': v['c'],
                           'h0': v['h0'], 'v0': v['v0'],
                           'page_label': 'nav:vi-ruta-' + str(ordinal)})
    if len(seen_cells) != 81:
        raise ValueError('La navegación debe preservar las 81 celdas')
    orientation_counts = Counter((r['cell_id'], r['h0'], r['v0']) for r in navigation)
    if len(orientation_counts) != 324 or set(orientation_counts.values()) != {1}:
        raise ValueError('La navegación no es biyectiva sobre las rutas orientadas')
    return ''.join(out), {'same_key_domain': True, 'common_literal_field_checks': common_checks,
                         'fields_per_route': len(field_list), 'all_union_fields_published': True,
                         'navigation_cells': len(seen_cells), 'navigation_routes': navigation,
                         'all_continuations_identified': True,
                         'route_source_ordinals': list(range(1, len(raw) + 1)),
                         'enriched_source_ordinals': [enriched_index[k]['source_ordinal'] for k in akeys]}


def uncertainty(value: str) -> str:
    # These are labelled editorial abbreviations, never numeric substitutions.
    return {'UNAVAILABLE': 'ND', 'NOT_APPLICABLE': 'NA', '': 'Vacío'}.get(value, value)


def external_catalog(docs: dict) -> str:
    records = docs['masas']['records'] + docs['anchuras']['records']
    statuses = codebook({r['values']['HMT_internal_status'] for r in records}, 'E')
    maps = codebook({r['values']['required_forward_map'] for r in records}, 'M')
    for rec in records:
        v = rec['values']
        if v['scheme'] != 'UNAVAILABLE_IN_SNAPSHOT' or v['scale'] != 'UNAVAILABLE_IN_SNAPSHOT':
            raise ValueError('Esquema/escala ya no uniformes: deben imprimirse por fila')
        if v['source_edition'] != '2026' or v['source_cutoff'] != '2026-01-15':
            raise ValueError('El catálogo no coincide con la edición documental declarada')
        if v['external_value_used_as_selector'] != 'NO' or v['comparison_authorization'] != 'ONLY_AFTER_INTERNAL_FREEZE':
            raise ValueError('Las condiciones documentales requieren una presentación específica')
    out = [r'''\clearpage
\section{Inventario metrológico: 471 masas y 384 anchuras}
\label{sec:vi-inventario-metrologico}

Las tablas siguientes son un catálogo de observaciones externas y no un
recuento de predicciones HMT. Conservan el corte documental PDG 2026 con fecha
\texttt{2026-01-15}, tal como figura en los archivos preservados. La fecha de
consulta consignada en el integral es \texttt{2026-07-26}. No se ha actualizado
la edición ni se han reinterpretado sus observables durante esta transcripción.
El identificador estable distingue registros diferentes de una misma especie;
no se eliminan repeticiones ni se funden masa, polo, anchura o estimación.

La columna de valor conserva tanto la expresión literal como, cuando difiere,
su presentación de origen. No se reconstruye una incertidumbre a partir de
decimales ni se transforma un intervalo en una desviación estándar.
Se mantienen las incertidumbres positiva y negativa separadas, la unidad,
el tipo de límite y el nivel de confianza disponible. \texttt{ND} abrevia
\texttt{UNAVAILABLE}; \texttt{NA} abrevia \texttt{NOT\_APPLICABLE}.
Una raya significa un campo vacío. Los tipos originales \texttt{NONE},
\texttt{R} y \texttt{U} se conservan como códigos de la fuente, junto a la
expresión del valor: respectivamente, ausencia de marca de límite, rango y
límite superior. No se infiere un nivel de confianza donde el registro no lo da.

En este corte, los 855 registros indican que esquema y escala no están
disponibles en la instantánea. Todos conservan la condición de comparación
posterior a la fijación del resultado interno y declaran que el valor externo
no se utilizó como selector. Las claves de estado \(E\) y enlace \(M\)
son abreviaturas editoriales reversibles de los estados y mapas de la fuente,
descritos en las dos leyendas siguientes. La palabra «abierto» en esas leyendas
reproduce el estado documental de ese corte; no es una revisión matemática nueva.
''']
    out.append(legend(statuses, OBS_STATUS, 'Estados conservados del inventario externo.', 'tab:vi-estados-externos'))
    out.append(legend(maps, MAP_NAMES, 'Enlaces de realización consignados por el inventario.', 'tab:vi-enlaces-externos'))
    for source, title, number in [('masas', 'Masas', 471), ('anchuras', 'Anchuras', 384)]:
        out.append('\\clearpage\n\\subsection{' + title + ': ' + str(number) + ' registros}\n')
        out.append(table_start(cols([40, 44, 33, 39]),
             ['Identificador y observación', 'Especies y nota de estado', 'Valor y unidad', 'Incertidumbre y tipo'],
             f'Inventario completo de {number} ' + source + '.', 'tab:vi-externo-' + source))
        for rec in docs[source]['records']:
            v = rec['values']
            out.append(marker(source, rec['source_ordinal']))
            identity = str(rec['source_ordinal']) + r'.\par ' + tex(v['output_id']) + r'\par ' + tex(v['object_name'])
            note = tex(v['particle_names']) + r'\par ' + tex(v['HMT_target_sector'])
            note += r'\par ' + tex(statuses[v['HMT_internal_status']] + '; ' + maps[v['required_forward_map']])
            if rec.get('key_occurrence', 1) > 1:
                note += r'\par Repetición de clave: ' + str(rec['key_occurrence'])
            value = tex(v['value_text']) + r'\par ' + tex(v['unit'])
            if v['display_value'] != v['value_text']:
                value += r'\par Presentación: ' + tex(v['display_value'])
            unc = r'\(u_+\): ' + tex(uncertainty(v['uncertainty_positive']))
            unc += r'\par \(u_-\): ' + tex(uncertainty(v['uncertainty_negative']))
            unc += r'\par Tipo: ' + tex(v['limit_type'])
            unc += r'\par Confianza: ' + tex(uncertainty(v['confidence_level']))
            out.append(row([identity, note, value, unc]))
        out.append(table_end())
    return ''.join(out)


COMPANION = r'''% Volumen documental compañero. Fuente independiente, sin compilación automática.
\documentclass[a4paper,10pt]{article}
\usepackage[top=23mm,bottom=23mm,left=20mm,right=20mm,headheight=15pt]{geometry}
\usepackage{fontspec,amsmath,unicode-math}
\usepackage[spanish,es-nodecimaldot,es-noquoting]{babel}
\usepackage{microtype,booktabs,longtable,array,needspace,fancyhdr}
\usepackage[unicode,hidelinks,bookmarksopen=true,bookmarksopenlevel=1,bookmarksnumbered=false]{hyperref}
\setmainfont{STIXTwoText-Regular.otf}[BoldFont=STIXTwoText-Bold.otf,ItalicFont=STIXTwoText-Italic.otf,BoldItalicFont=STIXTwoText-BoldItalic.otf]
\setmathfont{STIXTwoMath-Regular.otf}
\renewcommand{\normalsize}{\fontsize{10.5}{13.4}\selectfont}\normalsize
\setlength{\parindent}{1em}\setlength{\parskip}{3pt}
\setlength{\emergencystretch}{2em}
\clubpenalty=10000\widowpenalty=10000\raggedbottom
\clubpenalties 3 10000 10000 0
\widowpenalties 3 10000 10000 0
\AddToHook{cmd/section/before}{\clearpage}
\AddToHook{cmd/subsection/before}{\Needspace{7\baselineskip}}
\AddToHook{cmd/subsubsection/before}{\Needspace{6\baselineskip}}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{Catálogo estructural y metrológico de partículas}
\fancyfoot[C]{\thepage}
\hypersetup{pdftitle={Catálogo estructural y metrológico de partículas},pdfauthor={Oumar Haidara Fall; Rubén Ramos Balsa},pdfsubject={Estados, rutas, masas y anchuras}}
\newcommand{\CatalogRouteReference}{Las secciones~\ref{sec:vi-324-rutas} y~\ref{sec:vi-inventario-metrologico} de este catálogo publican, respectivamente, las 324 rutas orientadas y los 855 registros metrológicos.}
\begin{document}
\thispagestyle{empty}
\begin{center}
{\fontsize{8}{10}\selectfont Manuscrito de recopilación para transferencia académica\par}
\vspace{12mm}
{\fontsize{17}{20.5}\selectfont\bfseries Catálogo estructural y metrológico de partículas\par}
\vspace{6pt}
{\fontsize{11}{13.5}\selectfont Estados, rutas, masas y anchuras\par}
\vspace{11pt}
{\fontsize{11.5}{14}\selectfont Oumar Haidara Fall \textperiodcentered\ Rubén Ramos Balsa\par}
\vspace{4pt}
{\fontsize{8}{10}\selectfont Coautoría sin prelación de contribución\par}
\vspace{3pt}
{\fontsize{7.5}{9.5}\selectfont Integración y recopilación documental generadas por ChatGPT -- Astra.\par}
\end{center}
\vspace{7pt}
\begin{center}\bfseries Presentación\end{center}
\begingroup
\fontsize{10.5}{12.8}\selectfont
\setlength{\parskip}{2pt plus 1pt minus .5pt}
\noindent
\begin{minipage}{\textwidth}
Este catálogo reúne el inventario estructural de \(324\) rutas orientadas
y \(855\) registros metrológicos de masas y anchuras. Su organización
permite consultar la identidad y los campos de cada ruta y localizar las
observaciones metrológicas, sin equiparar el número de registros documentales con el
de predicciones individualizadas. Acompaña a \emph{Partículas,
persistencia y derivación del espectro de masas}, donde se desarrollan
las definiciones y demostraciones que construyen la partícula, el atlas
y el operador de masa. Aquí se publica íntegro el dominio de datos
estructurales y de contraste utilizado por ese desarrollo.

La primera sección distingue \(13\) multisecciones, \(56\) familias de
ruta y \(23\) clases del inventario. La
sección~\ref{sec:vi-324-rutas} presenta las \(324\) rutas, conservando
todos los campos de sus dos registros concordantes. La
sección~\ref{sec:vi-inventario-metrologico} reúne \(471\) masas y
\(384\) anchuras de la edición metrológica fijada, con sus identificadores,
estados, unidades y fuentes. Valores centrales, intervalos, límites y
anchuras conservan su significado propio. La presencia de una
observación en el inventario permite localizarla para el contraste;
su identificación física requiere el lector y la carta especificados
en el artículo.

Cada ficha conserva su registro íntegro, incluidos los campos de
procedencia y las distinciones entre rutas, familias y observables. El
índice enlazado, los marcadores por celda y orientación y el identificador
repetido en las páginas de continuación permiten recorrer el conjunto y
regresar directamente a la ruta elegida. La separación de este anexo de
datos mantiene legibles las fichas sin abreviar sus registros.\par
\end{minipage}
\par\endgroup
\clearpage
\tableofcontents
\clearpage
\input{sections/10a_dependencia_activa_l_g.tex}
\input{sections/11_apendices_catalogo.tex}
\input{sections/12_catalogo_datos_companero.tex}
\end{document}
'''


def check_tex(text: str) -> dict:
    """Static syntax checks only; never represented as visual/PDF validation."""
    # Source cells cannot introduce raw TeX; inspect balanced generated braces
    # and environments after removing escaped specials and comments.
    clean = re.sub(r'(?<!\\)%[^\n]*', '', text)
    clean = re.sub(r'\\[{}%&#_$]', '', clean)
    depth = 0
    for char in clean:
        if char == '{': depth += 1
        elif char == '}':
            depth -= 1
            if depth < 0: raise ValueError('Llave de cierre sin apertura')
    if depth: raise ValueError('Llaves no equilibradas')
    stack = []
    for kind, name in re.findall(r'\\(begin|end)\{([^}]+)\}', text):
        if kind == 'begin': stack.append(name)
        elif not stack or stack.pop() != name: raise ValueError('Entornos no equilibrados')
    if stack: raise ValueError('Entorno abierto')
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    if len(labels) != len(set(labels)): raise ValueError('Etiquetas repetidas')
    return {'braces_balanced': True, 'environments_balanced': True,
            'unique_labels': len(labels), 'compiled': False, 'visual_QA': False}


def self_test() -> list[str]:
    cases = ['a_b & 50% {x} $y$ #1 \\input{bad}', '~^', '', '+++---+++---', 'Deltabar--',
             '001.230000000000000000', 'α Ω κ ± − π', 'a\nb\tc']
    for case in cases:
        result = tex(case)
        if '\\input' in result: raise AssertionError('Inyección TeX')
        check_tex(result)
    raw = '001.230000000000000000'
    if tex(raw).replace(BREAK, '') != raw: raise AssertionError('Cifras alteradas')
    for char, escape in SPECIAL.items():
        if tex(char).replace(BREAK, '') != escape: raise AssertionError('Escape incorrecto')
    for prose in ('Profundidad', 'Familias', 'neutrino', 'Multisecciones',
                  'Identificadores de las celdas', 'Incertidumbre y representación'):
        if BREAK in tex(prose): raise AssertionError('Partición artificial de prosa: ' + prose)
    if tex('charged_lepton_G0') != 'charged\\_' + BREAK + 'lepton\\_' + BREAK + 'G0':
        raise AssertionError('Partición de identificador fuera de sus delimitadores')
    for code in ('12345678901234567890', 'effeba5464fe6134ce328276caffda457d'):
        if BREAK not in tex(code): raise AssertionError('Código largo sin partición')
        if tex(code).replace(BREAK, '') != code: raise AssertionError('Código alterado')
    for signs in ('+++---+++---', 'Deltabar--', '---', '+0+---+0+---'):
        encoded = tex(signs)
        if '--' in encoded or encoded.replace(r'\kern0pt{}', '') != signs:
            raise AssertionError('Ligadura o alteración de signos literales')
    return ['source_text_cannot_inject_input', 'special_characters_escaped', 'literal_signs_not_ligated',
            'numeric_string_preserved', 'unicode_preserved', 'empty_cell_distinct', 'no_control_chars',
            'ordinary_words_not_split', 'identifiers_break_at_delimiters', 'long_codes_reversible']


def build() -> tuple[dict[str, bytes], dict]:
    docs = {}
    source_hashes = {}
    for name, expected in SOURCES.items():
        path = TECH / f'catalogo_{name}.json'
        data = path.read_bytes()
        doc = json.loads(data)
        if len(doc['records']) != expected or doc['row_count'] != expected:
            raise ValueError('Recuento documental divergente en ' + name)
        if [r['source_ordinal'] for r in doc['records']] != list(range(1, expected + 1)):
            raise ValueError('Orden documental irregular en ' + name)
        docs[name] = doc
        source_hashes[path.name] = sha(data)
    route_text, route_checks = route_catalog(docs)
    outputs = {
        'sections/11_apendices_catalogo.tex': structural(docs),
        'sections/12_catalogo_datos_companero.tex': route_text + external_catalog(docs),
        'main_catalogo.tex': COMPANION,
    }
    all_text = '\n'.join(outputs.values())
    counts = Counter(kind for kind, _ in re.findall(r'^% VI-CATALOG-ROW (\w+) (\d+)$', all_text, re.M))
    required = {k: n for k, n in SOURCES.items() if k != 'rutas_enriquecidas'}
    if dict(counts) != required: raise ValueError(f'Recuento de filas impresas incorrecto: {counts}')
    for kind, number in required.items():
        ordinals = [int(x) for x in re.findall(r'^% VI-CATALOG-ROW ' + kind + r' (\d+)$', all_text, re.M)]
        if ordinals != list(range(1, number + 1)): raise ValueError('Omisión o cambio de orden en ' + kind)
    checks = {name: check_tex(content) for name, content in outputs.items()}
    all_labels = re.findall(r'\\label\{([^}]+)\}', all_text)
    if len(all_labels) != len(set(all_labels)): raise ValueError('Colisión de etiquetas entre fuentes')
    encoded = {name: content.encode('utf-8') for name, content in outputs.items()}
    receipt = {
        'schema': 'HMT.VI.DOCUMENTARY_APPENDICES.v1',
        'status': 'PASS_FUENTES_APENDICES_DOCUMENTALES_VI',
        'role': 'DOCUMENTARY_RENDERING_ONLY_NOT_A_MASS_GENERATOR',
        'source_hashes': source_hashes,
        'printed_records': dict(counts),
        'source_ordinals_all_preserved': True,
        'duplicates_removed': False,
        'numeric_values_recalculated': False,
        'source_statuses_promoted': False,
        'route_checks': route_checks,
        'metrology_units_preserved': sorted({r['values']['unit'] for n in ('masas', 'anchuras') for r in docs[n]['records']}),
        'metrology_epoch': {'edition': 'PDG 2026', 'cutoff': '2026-01-15', 'updated': False},
        'metrology_abbreviations': {'ND': 'UNAVAILABLE', 'NA': 'NOT_APPLICABLE'},
        'typesetting': {'text_pt': 10.5, 'longtable': True, 'compiled': False,
                        'ordinary_prose_fixed_chunking': False,
                        'identifier_breaks_at_delimiters': True,
                        'long_numeric_and_pure_code_chunking': 8,
                        'visual_validation_pending': True,
                        'main_article_source_not_modified': True},
        'checks': checks,
        'escape_tests': self_test(),
        'output_sha256': {name: sha(raw) for name, raw in encoded.items()},
    }
    encoded['technical/apendices_catalogo_control.json'] = (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return encoded, receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Comprobar las fuentes existentes sin escribir')
    parser.add_argument('--self-test', action='store_true', help='Ejecutar sólo las pruebas de escapado')
    parser.add_argument('--companion-only', action='store_true',
                        help='Escribir sólo el catálogo compañero y su control; preservar el apéndice 11')
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps({'status': 'PASS_ESCAPE_TEX', 'tests': self_test()}, ensure_ascii=False))
        return
    outputs, receipt = build()
    if args.companion_only:
        existing = ROOT / 'sections/11_apendices_catalogo.tex'
        expected = outputs.pop('sections/11_apendices_catalogo.tex')
        if existing.read_bytes() != expected:
            raise SystemExit('FAIL_APENDICE_11_NO_SE_PUEDE_REGENERAR_SILENCIOSAMENTE')
    if args.check:
        for relative, expected in outputs.items():
            path = ROOT / relative
            if not path.exists() or path.read_bytes() != expected:
                raise SystemExit('FAIL_FUENTE_APENDICE_DIVERGENTE: ' + relative)
    else:
        for relative, raw in outputs.items():
            path = ROOT / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    print(json.dumps({'status': receipt['status'], 'outputs': len(outputs),
                      'printed_records': receipt['printed_records'],
                      'route_fields': receipt['route_checks']['fields_per_route'],
                      'compiled': False, 'read_only': args.check}, ensure_ascii=False))


if __name__ == '__main__':
    main()
