#!/usr/bin/env python3
import json, math, os, zipfile
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ROOT=Path('/mnt/data')
OUT_JSON=ROOT/'hmt_puerta_ciclo02_phase_law_results.json'
OUT_TEX=ROOT/'hmt_puerta_ciclo02_phase_law_window.tex'
OUT_PDF=ROOT/'hmt_puerta_ciclo02_phase_law.pdf'
OUT_ZIP=ROOT/'HMT_PUERTA_CICLO02_PHASE_LAW_PACK.zip'

D=json.load(open(ROOT/'hmt_fractal_app08_interval_cylinder_results.json'))
O=json.load(open(ROOT/'hmt_puerta_orientacion01_results.json'))
orientation={d['t']:d for d in O['orientation_doors']}
sync_by_phase={}
for d in O['synchronized_doors_t5_60']:
    g=d['K']%9 or 9
    sync_by_phase.setdefault(g,[]).append(d)
orient_by_phase={}
for d in O['orientation_doors']:
    g=d['K']%9 or 9
    orient_by_phase.setdefault(g,[]).append(d)

rows=[]
for row in D['rows']:
    t=row['t']; K=row['K']; g=K%9 or 9; dK=row['dK']
    counts=(row['pi']['interval_count'], row['e']['interval_count'], row['phi']['interval_count'])
    eq=len(set(counts))==1
    if eq:
        symmetry='sync'
    elif counts[0]==counts[1]:
        symmetry='pi=e'
    elif counts[0]==counts[2]:
        symmetry='pi=phi'
    elif counts[1]==counts[2]:
        symmetry='e=phi'
    else:
        symmetry='asym'
    typ=[]
    if dK==0: typ.append('stutter')
    if eq: typ.append('sync')
    if t in orientation: typ.append('orientation')
    if not typ: typ.append('ordinary')
    rows.append({'t':t,'K':K,'phase':g,'dK':dK,'counts':counts,'symmetry':symmetry,'type':'+'.join(typ), 'blocks':(row['pi']['block'],row['e']['block'],row['phi']['block'])})

# first chronologic 9 steps after w30
first9=[r for r in rows if 5 <= r['t'] <= 13]
# door phases 1..9 summary from t5..60
phase_summary=[]
for g in range(1,10):
    rs=[r for r in rows if r['phase']==g]
    phase_summary.append({
        'phase':g,
        'appearances':[(r['t'],r['K'],r['counts'],r['type']) for r in rs[:8]],
        'sync_count':len(sync_by_phase.get(g,[])),
        'orientation_count':len(orient_by_phase.get(g,[])),
        'orientation_examples':[(d['t'],d['K'],d['num_candidates'],d['phi_fixed'],d['pi_plus_e']) for d in orient_by_phase.get(g,[])[:5]],
    })

# orientation core t=8,9 details
core={str(t):orientation[t] for t in (8,9) if t in orientation}

# Identify first K-cycle relation from K=5..13 and next phase return K=14..20
cycle1=[r for r in rows if 5 <= r['K'] <= 13]
cycle2=[r for r in rows if 14 <= r['K'] <= 20]

results={
    'title':'PUERTA-CICLO-02 -- ciclo de fases 1..9, orientación especular y ley de retorno',
    'definition':'Door phase g = K mod 9, with 0 read as 9. Since w30 already contains four triads, the first post-w30 cycle begins at phase 5 and runs 5,6,7,8,9,1,2,3,4.',
    'first9_after_w30':first9,
    'cycle1_K5_13':cycle1,
    'cycle2_K14_20':cycle2,
    'phase_summary':phase_summary,
    'orientation_core_t8_t9':core,
    'stutters_t5_30':D['stutters_t5_30'],
    'point_failures_t5_22':D['point_failures_t5_22'],
    'conclusions':[
        'Door 10 repeats Door 1 only as phase K mod 9, not as identical state.',
        'The first post-w30 phase cycle starts at phase 5 because w30 already accounts for four triads.',
        'Phases 8 and 9 form the core orientation package: synchronized counts and phi-fixed pi/e mirror.',
        'The system alternates phase return and state drift: this is not a period, but a return with memory/carry.',
        'The correct law is a typed door grammar: opening/pruning, synchronization, orientation mirror, stutter/reopening, and future survival.'
    ]
}
OUT_JSON.write_text(json.dumps(results,indent=2,ensure_ascii=False))

def counts_str(c): return f"{c[0]},{c[1]},{c[2]}"
def first9_table():
    lines=[]
    for r in first9:
        lines.append(f"{r['t']} & {r['K']} & {r['phase']} & {counts_str(r['counts'])} & {r['symmetry']} & {r['type']} \\")
    return '\n'.join(lines)

def phase_table():
    lines=[]
    for s in phase_summary:
        apps=', '.join([f"t{t}/K{K}:{c[0]}:{c[1]}:{c[2]}:{typ}" for t,K,c,typ in s['appearances'][:4]])
        lines.append(f"{s['phase']} & {s['sync_count']} & {s['orientation_count']} & {apps} \\")
    return '\n'.join(lines)

tex=rf"""
\section*{{PUERTA--CICLO--02: ciclo de fases 1--9}}

Se define la fase de puerta por
\[
\boxed{{g(K)=K\bmod 9,\quad 0\equiv9.}}
\]
Como el prefijo \(w_{{30}}\) ya contiene cuatro triadas, el primer ciclo posterior no empieza en la fase 1, sino en
\[
\boxed{{5,6,7,8,9,1,2,3,4.}}
\]
Por tanto, cuando se dice que la puerta 10 repite la 1, la frase correcta es:
\[
\boxed{{K=10\text{{ vuelve a la fase }}1,\text{{ pero no vuelve al mismo estado.}}}}
\]
Hay retorno de fase, no periodicidad simple. La memoria/carry cambia el estado.

\subsection*{{Primer ciclo posterior a \(w_{{30}}\)}}
\[
\begin{{array}}{{c|c|c|c|c|c}}
 t & K & g & (|\pi|,|e|,|\varphi|) & \text{{simetria}} & \text{{tipo}}\\
\hline
{first9_table()}
\end{{array}}
\]

La zona clave es
\[
\boxed{{K=8,9,10}}
\]
con sincronizacion completa. En particular, \(K=9\) tiene
\[
\boxed{{|C^\pi|=|C^e|=|C^\varphi|=43.}}
\]

\subsection*{{Resumen por fases}}
\[
\begin{{array}}{{c|c|c|p{{9cm}}}}
 g & \#\text{{sync}} & \#\text{{orientacion}} & \text{{primeras apariciones}}\\
\hline
{phase_table()}
\end{{array}}
\]

\subsection*{{Nucleo especular}}
En \(t=8\), la firma de orientacion deja tres matrices locales, todas con \(\varphi\) fijo y \(\pi+e\) constante. La supervivencia futura selecciona la matriz central. En \(t=9\), la firma deja dos matrices, otra vez con \(\varphi\) fijo y \(\pi/e\) como par movil. La supervivencia selecciona una sola.

\[
\boxed{{\varphi=\text{{eje fijo}},\qquad \pi/e=\text{{espejo movil}},\qquad \text{{el futuro orienta.}}}}
\]

\subsection*{{Ley de puerta}}
La torre no tiene una unica clase de evento. Tiene una gramatica tipada:
\[
\boxed{{\text{{poda}}}}
\quad
\boxed{{\text{{sincronizacion}}}}
\quad
\boxed{{\text{{orientacion especular}}}}
\quad
\boxed{{\text{{stutter/reapertura}}}}
\quad
\boxed{{\text{{supervivencia futura}}}}.
\]
La puerta 10 repite la fase 1, pero con otro estado; esto es exactamente el retorno con memoria. La ley general no es periodo, sino ciclo de fase con carry.

\[
\boxed{{\text{{cada ciclo de 9 puertas devuelve la fase, pero no borra la memoria.}}}}
\]
"""
OUT_TEX.write_text(tex)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=8, leading=10))
doc=SimpleDocTemplate(str(OUT_PDF), pagesize=A4, rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36)
story=[]
story.append(Paragraph('PUERTA-CICLO-02 -- ciclo de fases 1..9, orientacion y retorno con memoria', styles['Title']))
story.append(Paragraph('La puerta se define por la fase g=K mod 9, con 0=9. Como w30 ya contiene cuatro triadas, el primer ciclo posterior entra por las fases 5,6,7,8,9,1,2,3,4. Por eso K=10 repite la fase 1, pero no el estado: hay retorno con memoria/carry, no periodo simple.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('Primer ciclo posterior a w30', styles['Heading2']))
tdata=[['t','K','fase','counts','sim','tipo']]
for r in first9:
    tdata.append([r['t'],r['K'],r['phase'],counts_str(r['counts']),r['symmetry'],r['type']])
table=Table(tdata, colWidths=[35,35,40,90,70,105])
table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),8)]))
story.append(table)
story.append(Spacer(1,8))
story.append(Paragraph('Lectura: K=8,9,10 forman un nucleo sincronizado; K=9 tiene 43:43:43. K=10 vuelve a la fase 1, pero con estado contraido 32:32:32.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('Resumen por fase', styles['Heading2']))
pdata=[['fase','sync','orient.','ejemplos']]
for s in phase_summary:
    apps='; '.join([f"t{t}/K{K}:{c[0]},{c[1]},{c[2]}:{typ}" for t,K,c,typ in s['appearances'][:3]])
    pdata.append([s['phase'], s['sync_count'], s['orientation_count'], apps])
tab=Table(pdata, colWidths=[35,35,45,360])
tab.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'TOP')]))
story.append(tab)
story.append(Spacer(1,8))
story.append(Paragraph('Nucleo especular', styles['Heading2']))
story.append(Paragraph('En t=8 y t=9 la firma de orientacion deja varias matrices locales con phi fijo y pi+e constante. La supervivencia futura rompe el espejo pi/e y selecciona la orientacion real. Por tanto la novena puerta es una puerta de orientacion, no una rareza aislada.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('Ley de puerta', styles['Heading2']))
story.append(Paragraph('La torre tiene una gramatica tipada: poda, sincronizacion, orientacion especular, stutter/reapertura y supervivencia futura. Cada ciclo de nueve devuelve la fase, pero no borra la memoria; el carry modifica el estado. Esta es la forma correcta de la intuicion puerta 10 = puerta 1.', styles['BodyText']))
doc.build(story)

with zipfile.ZipFile(OUT_ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for p in [OUT_PDF,OUT_TEX,OUT_JSON,Path(__file__) if '__file__' in globals() else ROOT/'hmt_puerta_ciclo02_phase_law.py']:
        if Path(p).exists(): z.write(str(p), arcname=Path(p).name)
print('wrote',OUT_PDF,OUT_TEX,OUT_JSON,OUT_ZIP)
