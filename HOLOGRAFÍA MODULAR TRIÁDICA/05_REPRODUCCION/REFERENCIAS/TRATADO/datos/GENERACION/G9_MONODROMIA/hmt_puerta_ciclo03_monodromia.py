#!/usr/bin/env python3
import json, math, zipfile
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ROOT=Path('/mnt/data')
OUT_JSON=ROOT/'hmt_puerta_ciclo03_monodromia_results.json'
OUT_TEX=ROOT/'hmt_puerta_ciclo03_monodromia_window.tex'
OUT_PDF=ROOT/'hmt_puerta_ciclo03_monodromia.pdf'
OUT_ZIP=ROOT/'HMT_PUERTA_CICLO03_MONODROMIA_PACK.zip'

D=json.load(open(ROOT/'hmt_fractal_app08_interval_cylinder_results.json'))
O=json.load(open(ROOT/'hmt_puerta_orientacion01_results.json'))
rows=(D.get('rows',[])+D.get('extended',[]))
rows=sorted(rows,key=lambda r:r['t'])
orient={d['t']:d for d in O['orientation_doors']}

def counts(r): return (r['pi']['interval_count'],r['e']['interval_count'],r['phi']['interval_count'])
def symmetry(c):
    if len(set(c))==1: return 'sync'
    if c[0]==c[1]: return 'pi=e'
    if c[0]==c[2]: return 'pi=phi'
    if c[1]==c[2]: return 'e=phi'
    return 'asym'
def abphase(K): return K%9 or 9

def typ(r):
    ts=[]
    if r['dK']==0: ts.append('stutter')
    if symmetry(counts(r))=='sync': ts.append('sync')
    if r['t'] in orient: ts.append('orient')
    return '+'.join(ts) if ts else 'poda'

first_cycle=[]
for r in rows:
    K=r['K']
    if 5<=K<=13:
        first_cycle.append({'door':K-4,'t':r['t'],'K':K,'abs_phase':abphase(K),'counts':counts(r),'sym':symmetry(counts(r)),'type':typ(r),'blocks':(r['pi']['block'],r['e']['block'],r['phi']['block'])})
second_cycle=[]
for r in rows:
    K=r['K']
    if 14<=K<=22:
        second_cycle.append({'door':K-13,'t':r['t'],'K':K,'abs_phase':abphase(K),'counts':counts(r),'sym':symmetry(counts(r)),'type':typ(r),'blocks':(r['pi']['block'],r['e']['block'],r['phi']['block'])})

# absolute phase summary from orientation/sync data available up to 60
phase_summary=[]
for g in range(1,10):
    rs=[r for r in rows if abphase(r['K'])==g]
    os=[d for d in O['orientation_doors'] if abphase(d['K'])==g]
    ss=[d for d in O['synchronized_doors_t5_60'] if abphase(d['K'])==g]
    phase_summary.append({
        'phase':g,
        'available_instances':[(r['t'],r['K'],counts(r),typ(r)) for r in rs[:6]],
        'sync_count_t5_60':len(ss),
        'orientation_count_t5_60':len(os),
        'orientation_examples':[(d['t'],d['K'],d['num_candidates'],d['phi_fixed'],d['pi_plus_e']) for d in os[:4]],
    })

# orientation details for t8 and t9
core={str(t):orient[t] for t in [8,9] if t in orient}

# compare phase returns: phase1 K10 vs K19 and K28 where available
returns=[]
for g in range(1,10):
    rs=[r for r in rows if abphase(r['K'])==g]
    if len(rs)>=2:
        returns.append({'phase':g,'returns':[(r['t'],r['K'],counts(r),typ(r)) for r in rs[:4]]})

results={
    'title':'PUERTA-CICLO-03 -- ley de las nueve puertas: retorno de fase con memoria',
    'principle':'Door 10 repeats Door 1 only at the level of phase K mod 9. The state is not periodic: carry and frontier memory change it.',
    'first_cycle_post_w30':first_cycle,
    'second_cycle_post_w30':second_cycle,
    'phase_summary':phase_summary,
    'orientation_core_t8_t9':core,
    'phase_returns':returns,
    'conclusions':[
        'There are two calendars: absolute phase K mod 9 and local post-w30 doors. Confusing them hides the law.',
        'The phase cycle is period 9, but the state has monodromy: a return with memory, not a reset.',
        'The t=8/t=9 package is an orientation core: phi fixed, pi/e mirror, survival chooses orientation.',
        'The 10th door repeats phase 1, but after crossing the orientation core; it is a phase return with transformed state.',
        'Stutters are not the same as phase returns: they are openings without new decimal pruning.'
    ]
}
OUT_JSON.write_text(json.dumps(results,indent=2,ensure_ascii=False))

def cstr(c): return f"{c[0]},{c[1]},{c[2]}"
def table_rows(items):
    return '\n'.join(f"{x['door']} & {x['t']} & {x['K']} & {x['abs_phase']} & {cstr(x['counts'])} & {x['sym']} & {x['type']} \\" for x in items)

def phase_rows():
    lines=[]
    for s in phase_summary:
        inst='; '.join([f"t{t}/K{K}:{c[0]},{c[1]},{c[2]}:{ty}" for t,K,c,ty in s['available_instances'][:3]])
        ex='; '.join([f"t{t}/K{K}:n={n}:phi={phi}:pi+e={pe}" for t,K,n,phi,pe in s['orientation_examples'][:2]])
        lines.append(f"{s['phase']} & {s['sync_count_t5_60']} & {s['orientation_count_t5_60']} & {inst} & {ex} \\")
    return '\n'.join(lines)

tex=rf"""
\section*{{PUERTA--CICLO--03: ley de las nueve puertas}}

La correccion conceptual es distinguir dos calendarios. El calendario absoluto es
\[
\theta(K)=K\bmod 9,\qquad 0\equiv9.
\]
El calendario local posterior a \(w_{{30}}\) empieza en \(K=5\), porque \(w_{{30}}\) ya contiene cuatro triadas. Por eso el primer ciclo local es:
\[
1,2,3,4,5,6,7,8,9\quad\leftrightarrow\quad K=5,6,7,8,9,10,11,12,13.
\]
La frase ``la puerta 10 repite la 1'' es correcta solo en el calendario absoluto:
\[
K=10\equiv1\pmod9.
\]
Pero no repite el estado. La ley correcta es:
\[
\boxed{{\text{{retorno de fase con memoria, no periodo simple.}}}}
\]

\subsection*{{Primer ciclo local posterior a \(w_{{30}}\)}}
\[
\begin{{array}}{{c|c|c|c|c|c|c}}
\text{{puerta}}&t&K&\theta&(\pi,e,\varphi)&\text{{simetria}}&\text{{tipo}}\\
\hline
{table_rows(first_cycle)}
\end{{array}}
\]

\subsection*{{Segundo ciclo local}}
\[
\begin{{array}}{{c|c|c|c|c|c|c}}
\text{{puerta}}&t&K&\theta&(\pi,e,\varphi)&\text{{simetria}}&\text{{tipo}}\\
\hline
{table_rows(second_cycle)}
\end{{array}}
\]

\subsection*{{Resumen por fase absoluta}}
\[
\begin{{array}}{{c|c|c|p{{6cm}}|p{{4cm}}}}
\theta&\#sync&\#orient&\text{{primeras apariciones}}&\text{{ejemplos orientacion}}\\
\hline
{phase_rows()}
\end{{array}}
\]

\subsection*{{Nucleo de orientacion}}
En \(t=8\) y \(t=9\) aparece el nucleo especular: \(\varphi\) queda fijo, \(\pi/e\) forman el par movil, y la supervivencia futura selecciona una orientacion.

\[
\boxed{{\varphi=\text{{eje fijo}},\qquad \pi/e=\text{{espejo movil}},\qquad \text{{el futuro orienta.}}}}
\]

\subsection*{{Ley de puerta}}
La torre no tiene una sola clase de evento. Tiene una gramatica tipada:
\[
\boxed{{\text{{poda}}}}\quad
\boxed{{\text{{sincronizacion}}}}\quad
\boxed{{\text{{orientacion especular}}}}\quad
\boxed{{\text{{stutter/reapertura}}}}\quad
\boxed{{\text{{supervivencia futura}}}}.
\]
Cada ciclo de nueve devuelve la fase, pero no borra la memoria. Esto es monodromia discreta:
\[
\boxed{{\mathcal S_{{K+9}}=\mathcal M_K(\mathcal S_K),\quad \mathcal M_K\neq I\ \text{{en general}}.}}
\]
"""
OUT_TEX.write_text(tex)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=8, leading=10))
styles.add(ParagraphStyle(name='Tiny', parent=styles['BodyText'], fontSize=7, leading=9))
doc=SimpleDocTemplate(str(OUT_PDF), pagesize=A4, rightMargin=32,leftMargin=32,topMargin=32,bottomMargin=32)
story=[]
story.append(Paragraph('PUERTA-CICLO-03 - ley de las nueve puertas', styles['Title']))
story.append(Paragraph('Se distingue calendario absoluto theta=K mod 9 y calendario local posterior a w30. La puerta 10 repite la fase 1, pero no el estado: hay retorno de fase con memoria, no periodo simple.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('Primer ciclo local posterior a w30', styles['Heading2']))
cols=['puerta','t','K','theta','counts','sim','tipo']
tdata=[cols]+[[x['door'],x['t'],x['K'],x['abs_phase'],cstr(x['counts']),x['sym'],x['type']] for x in first_cycle]
tab=Table(tdata, colWidths=[42,32,32,42,88,55,90])
tab.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),8)]))
story.append(tab)
story.append(Spacer(1,8))
story.append(Paragraph('Segundo ciclo local', styles['Heading2']))
tdata=[cols]+[[x['door'],x['t'],x['K'],x['abs_phase'],cstr(x['counts']),x['sym'],x['type']] for x in second_cycle]
tab=Table(tdata, colWidths=[42,32,32,42,88,55,90])
tab.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),8)]))
story.append(tab)
story.append(Spacer(1,8))
story.append(Paragraph('Lectura', styles['Heading2']))
story.append(Paragraph('Las puertas 8 y 9 del calendario absoluto forman un nucleo de orientacion: phi queda fijo, pi/e se espejan, y la supervivencia futura rompe el espejo. La fase 1 posterior no reinicia; vuelve con memoria/carry. Esta es la monodromia de puerta: retorno de fase sin borrado de estado.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('Resumen por fase absoluta', styles['Heading2']))
pdata=[['theta','sync','orient','primeras apariciones']]
for s in phase_summary:
    inst='; '.join([f"t{t}/K{K}:{c[0]},{c[1]},{c[2]}:{ty}" for t,K,c,ty in s['available_instances'][:2]])
    pdata.append([s['phase'],s['sync_count_t5_60'],s['orientation_count_t5_60'],inst])
tab=Table(pdata, colWidths=[36,36,42,380])
tab.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'TOP')]))
story.append(tab)
story.append(Spacer(1,8))
story.append(Paragraph('Ley de puerta', styles['Heading2']))
story.append(Paragraph('La torre tiene eventos tipados: poda, sincronizacion, orientacion especular, stutter/reapertura y supervivencia futura. La ecuacion conceptual es S_{K+9}=M_K(S_K), con M_K no trivial en general.', styles['BodyText']))
doc.build(story)

with zipfile.ZipFile(OUT_ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for p in [OUT_PDF,OUT_TEX,OUT_JSON,ROOT/'hmt_puerta_ciclo03_monodromia.py']:
        z.write(str(p), arcname=p.name)
print('wrote', OUT_PDF, OUT_TEX, OUT_JSON, OUT_ZIP)
