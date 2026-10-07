#!/usr/bin/env python3
"""Control estático de fuentes VI; no compila ni certifica demostraciones.

Examina todas las secciones, figuras y las dos fuentes maestras, distingue el
ensamblaje actual de la disponibilidad material de secciones todavía sueltas.
Escribe únicamente su informe JSON y Markdown bajo technical. --check compara
el informe con el estado de fuentes, sin editar archivos.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'technical'


def strip_comments(text):
    # Preserve line numbers; a percent preceded by an odd slash run is escaped.
    rows = []
    for line in text.splitlines(keepends=True):
        cut = None
        for i, char in enumerate(line):
            if char != '%': continue
            k = i - 1
            while k >= 0 and line[k] == '\\': k -= 1
            if (i - k - 1) % 2 == 0:
                cut = i
                break
        rows.append(line if cut is None else line[:cut] + ('\n' if line.endswith('\n') else ''))
    return ''.join(rows)


def loc(path, text, start):
    return {'file': str(path.relative_to(ROOT)), 'line': text.count('\n', 0, start) + 1}


def resolve_input(name, source, graphics=False):
    if '\\' in name or '#' in name:
        return None, 'dynamic_path'
    exts = ['', '.pdf', '.png', '.jpg', '.jpeg', '.svg'] if graphics else ['', '.tex']
    for ext in exts:
        candidate = (ROOT / (name + ext)).resolve()
        if candidate.is_file(): return candidate, 'root_relative'
    for ext in exts:
        candidate = (source.parent / (name + ext)).resolve()
        if candidate.is_file(): return candidate, 'source_relative_only'
    return None, 'missing'


def inspect_file(path):
    original = path.read_text()
    text = strip_comments(original)
    info = {'file': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(original.encode()).hexdigest(),
            'lines': len(original.splitlines()), 'labels': [], 'references': [],
            'citations': [], 'bibitems': [], 'inputs': [], 'graphics': [],
            'syntax_findings': []}
    for regex, target in [(r'\\label\s*\{([^{}]+)\}', 'labels'),
                          (r'\\(?:eqref|pageref|autoref|[cC]ref|[cC]pageref|ref)\*?\s*\{([^{}]+)\}', 'references'),
                          (r'\\hyperref\s*\[([^\]]+)\]', 'references'),
                          (r'\\(?:cite|citep|citet|parencite|textcite)\*?(?:\s*\[[^\]]*\])*\s*\{([^{}]+)\}', 'citations'),
                          (r'\\bibitem(?:\[[^\]]*\])?\s*\{([^{}]+)\}', 'bibitems')]:
        for m in re.finditer(regex, text):
            for key in m.group(1).split(','):
                info[target].append({'key': key.strip(), **loc(path, text, m.start())})
    for regex, target, graphics in [(r'\\(?:input|include)\s*\{([^{}]+)\}', 'inputs', False),
                                     (r'\\includegraphics(?:\s*\[[^\]]*\])?\s*\{([^{}]+)\}', 'graphics', True)]:
        for m in re.finditer(regex, text):
            resolved, status = resolve_input(m.group(1), path, graphics)
            info[target].append({'path': m.group(1), 'resolution': status,
                                 'resolved': str(resolved.relative_to(ROOT)) if resolved and resolved.is_relative_to(ROOT) else str(resolved) if resolved else None,
                                 **loc(path, text, m.start())})
    # Braces and environments, with escaped literal braces removed first.
    brace_text = re.sub(r'\\(?:textbackslash\{\}|[{}%&#_$])', '', text)
    stack = []
    for i, char in enumerate(brace_text):
        if char == '{': stack.append(i)
        elif char == '}':
            if stack: stack.pop()
            else: info['syntax_findings'].append({'kind': 'unmatched_close_brace', **loc(path, brace_text, i)})
    for i in stack: info['syntax_findings'].append({'kind': 'unclosed_brace', **loc(path, brace_text, i)})
    stack = []
    for m in re.finditer(r'\\(begin|end)\s*\{([^{}]+)\}', text):
        kind, name = m.groups()
        if kind == 'begin': stack.append((name, m.start()))
        elif stack and stack[-1][0] == name: stack.pop()
        else: info['syntax_findings'].append({'kind': 'environment_mismatch', 'environment': name, **loc(path, text, m.start())})
    for name, start in stack:
        info['syntax_findings'].append({'kind': 'unclosed_environment', 'environment': name, **loc(path, text, start)})
    for opening, closing in [(r'\(', r'\)'), (r'\[', r'\]')]:
        opened = len(re.findall(r'(?<!\\)' + re.escape(opening), text))
        closed = len(re.findall(r'(?<!\\)' + re.escape(closing), text))
        if opened != closed:
            info['syntax_findings'].append({'kind': 'math_delimiter_count', 'opening': opening,
                                            'open': opened, 'close': closed,
                                            'file': info['file']})
    suspicious = [
        (r'\\mathcal[A-Za-z]+', 'joined_mathcal_command'),
        (r'\\mathbb[A-Za-z]+', 'joined_mathbb_command'),
        (r'\^\s*\{\s*,\s*\d', 'comma_in_exponent'),
        (r'\\(?:label|ref|eqref)\s*\{\s*\}', 'empty_reference_key'),
        (r'(?i)TPK\s+actualizado|HMT[- ]?full|EQUIVALENCIA_PENDIENTE', 'editorial_or_internal_label'),
    ]
    for regex, kind in suspicious:
        for m in re.finditer(regex, text):
            info['syntax_findings'].append({'kind': kind, 'match': m.group(), **loc(path, text, m.start())})
    info['commands'] = sorted(set(re.findall(r'(?<!\\)\\([A-Za-z@]+)', text)))
    info['declared_commands'] = sorted(set(re.findall(r'\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator)\*?\s*\{?\\([A-Za-z@]+)', text)))
    return info


def aggregate(files):
    labels = defaultdict(list)
    for info in files:
        for entry in info['labels']: labels[entry['key']].append(entry)
    refs = [entry for info in files for entry in info['references']]
    bibitems = {entry['key'] for info in files for entry in info['bibitems']}
    return {'label_count': sum(len(v) for v in labels.values()),
            'duplicate_labels': {k:v for k,v in labels.items() if len(v)>1},
            'unresolved_references': [r for r in refs if r['key'] not in labels],
            'citations_without_local_bibitem': [r for info in files for r in info['citations'] if r['key'] not in bibitems],
            'missing_or_contextual_inputs': [r for info in files for r in info['inputs'] + info['graphics'] if r['resolution'] != 'root_relative'],
            'syntax_findings': [r for info in files for r in info['syntax_findings']]}


def build():
    paths = sorted(set(ROOT.glob('sections/*.tex')) | set(ROOT.glob('figures/*.tex'))
                   | {ROOT/'main.tex', ROOT/'main_catalogo.tex'})
    infos = {str(p.relative_to(ROOT)): inspect_file(p) for p in paths}
    closures = {}
    for master in ['main.tex', 'main_catalogo.tex']:
        ordered = []
        recursion = []
        cycles = []
        def visit(name):
            if name in recursion:
                cycles.append(recursion + [name]); return
            if name not in infos: return
            ordered.append(name)
            recursion.append(name)
            for entry in infos[name]['inputs']:
                if entry['resolved'] in infos: visit(entry['resolved'])
            recursion.pop()
        visit(master)
        closures[master] = {'ordered_files': ordered, 'cycles': cycles,
                             'repeated_inputs': {k:v for k,v in Counter(ordered).items() if v>1},
                             **aggregate([infos[p] for p in ordered])}
    all_files = aggregate(list(infos.values()))
    section_paths = [p for p in infos if p.startswith('sections/')]
    missing_current = [p for p in section_paths if p not in closures['main.tex']['ordered_files']]
    # No unknown-command verdict: packages define commands not visible here.
    known_typical = set('''AddToHook APP Autores CC CCat CF FF Id Needspace QQ RR Span TPK TRIT ZZ
    Gamma gamma begingroup bfseries boxtimes cite emergencystretch endgroup enspace footnote iota jmath mathbf
    mp newpage notin oint parindent simeq sqcup textwidth tfrac thesection thesubsection thesubsubsection varnothing varprojlim
    addlinespace allowbreak alpha angle arccos arctan arraybackslash ast asymp atop author bar baselineskip begin
    beta bgroup big Big bigl Bigl bigm bigr Bigr bigskip bigwedge binom boldsymbol bot bottomrule boxed bullet
    cap caption cdot cdots centering chi circ clearpage clubpenalty cmidrule cong cos coth cosh cot csname cup
    date ddot deg delta Delta det diag dim dimexpr displaystyle displaywidowpenalty div documentclass dot dots
    downarrow egroup ell emph empty end endfirsthead endfoot endhead endlastfoot epsilon eqref equiv eta exp
    fancyfoot fancyhead fancyhf fequal fill fontsize footnotesize frac fbox gcd ge geq global hbar headrulewidth
    hfill hline hookrightarrow hphantom href hspace huge Huge hyperref hypersetup i id ifdefined iff imath implies
    in includegraphics inf infty input int item kappa ker label Lambda lambda land langle large Large lceil ldots
    left leftrightarrow le leq lim linewidth log longmapsto longrightarrow Longrightarrow mapsto mathbb mathcal
    mathfrak mathit mathop mathrel mathrm mathscr mathsf mathstrut mathtt max mdlgwhtsquare medskip mho mid midrule
    min mod mu multicolumn nabla ne neg neq newcommand newtheorem noindent nolimits nonumber norm normalsize not
    notag nu numberwithin odd omega Omega oplus operatorname oslash otimes over overbrace overline overrightarrow
    owns pagestyle par paragraph parskip partial perp phantom phi Phi pi Pi pm pmod prec prod propto protect psi
    Psi qquad quad rangle rceil ref relax renewcommand rho right rfloor rgroup rm rule scriptscriptstyle scriptsize
    section selectfont setcounter setlength setlist setmainfont setmathfont sgn sigma Sigma sim sin sinh small
    smallskip space sqrt square star subset subseteq subsection subsubsection sum sup tau text textasciicircum
    textasciitilde textbackslash textbar textbf textdegree textemdash textendash textit textnormal textperiodcentered
    textrm textsc textsf textstyle textsuperscript texttt thepage theoremstyle theta Theta thinspace tilde times
    title titleformat titlespacing to top topological topsep top rule toprule tr triangleq underbrace underline
    usepackage usetikzlibrary varepsilon vareta varphi varrho varsigma vartheta vec vfill vspace wedge widehat
    widetilde widownpenalty widowpenalty wlog wp xi Xi zeta zetaup ensuremath foreach coordinate node draw path
    filldraw matrix pgfmathsetmacro pgfmathtruncatemacro tikzset ifnum fi else edef def pgfplotsset tableofcontents
    raggedbottom raggedright tabcolsep arraystretch fracbox lfloor rfloor mathbin lvert rvert lVert rVert
    bmod constr intop overleftarrow texorpdfstring DeclareMathOperator leftarrow Re Im langle minipage nostruts
    tikzstyle selectlanguage usefont textcolor color boxplus beginproof endproof vdots ddots cancels checkmark
    acute breve hat tilde check dot commandlimits limits setminus bigcap bigcup bigoplus bigotimes bigvee vee
    substack mathbbm bbm xrightarrow xleftarrow lhd rhd unlhd unrhd leadsto rightsquigarrow topsep linewidth
    '''.split())
    declared = set(c for info in infos.values() for c in info['declared_commands'])
    unusual = defaultdict(list)
    for name, info in infos.items():
        for command in set(info['commands']) - known_typical - declared:
            unusual[command].append(name)
    report = {
        'schema': 'HMT.VI.STATIC_SOURCE_REVIEW.v1',
        'scope': 'Static editorial/LaTeX inspection, not mathematical or visual certification',
        'compiled': False, 'sections_modified': False,
        'snapshot': {k:{'sha256':v['sha256'], 'lines':v['lines']} for k,v in infos.items()},
        'all_sources': all_files, 'masters': closures,
        'sections_not_yet_reachable_from_main': missing_current,
        'commands_requiring_manual_review_not_errors': dict(sorted(unusual.items())),
        'limitations': ['No macro expansion or TeX compilation.',
                       'No theorem validation or source proof completeness certified.',
                       'References in dynamic macros require manual inspection.',
                       'Citation absence refers to this local snapshot, not external bibliography.'],
    }
    md = ['# Control estático editorial y LaTeX del Artículo VI\n',
          'No se ha compilado ni modificado ninguna sección. Este informe describe '
          'un corte de fuentes; no certifica demostraciones ni maquetación.\n',
          f'Archivos examinados: {len(infos)}.\n',
          '## Fuentes disponibles como conjunto\n',
          '```json\n'+json.dumps(all_files, ensure_ascii=False, indent=2)+'\n```\n',
          '## Secciones todavía fuera de main.tex\n']
    md += ['- `'+p+'`\n' for p in missing_current]
    md += ['\nEsto distingue disponibilidad material de inclusión efectiva. El volumen '
           'de datos 12 está destinado al maestro compañero.\n',
           '## Referencias en el ensamblaje actual\n',
           '```json\n'+json.dumps(closures['main.tex'], ensure_ascii=False, indent=2)+'\n```\n',
           '## Comandos para inspección manual\n',
           'Esta lista no declara comandos indefinidos: puede contener comandos de '
           'paquetes o TikZ. Sirve para localizar posibles erratas.\n',
           '```json\n'+json.dumps(dict(sorted(unusual.items())), ensure_ascii=False, indent=2)+'\n```\n']
    return report, ''.join(md)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report, md = build()
    outputs = {'CONTROL_ESTATICO_FUENTES_VI.json': json.dumps(report, ensure_ascii=False, indent=2)+'\n',
               'CONTROL_ESTATICO_FUENTES_VI.md': md}
    for name, value in outputs.items():
        path = OUT/name
        if args.check:
            if not path.is_file() or path.read_text() != value:
                raise SystemExit('SNAPSHOT_DIVERGENTE: '+name)
        else: path.write_text(value)
    a = report['all_sources']
    print(json.dumps({'status': 'STATIC_REVIEW_COMPLETE_NOT_COMPILATION',
                      'files': len(report['snapshot']),
                      'duplicate_labels': len(a['duplicate_labels']),
                      'unresolved_refs_all_files': len(a['unresolved_references']),
                      'missing_or_contextual_inputs': len(a['missing_or_contextual_inputs']),
                      'syntax_findings': len(a['syntax_findings']),
                      'citation_keys_without_bibitem': sorted({c['key'] for c in a['citations_without_local_bibitem']}),
                      'read_only': args.check}, ensure_ascii=False))


if __name__ == '__main__': main()
