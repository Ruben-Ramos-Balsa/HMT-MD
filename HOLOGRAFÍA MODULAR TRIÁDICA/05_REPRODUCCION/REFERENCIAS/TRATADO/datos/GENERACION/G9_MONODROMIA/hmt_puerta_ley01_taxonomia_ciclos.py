#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import json, zipfile, itertools, math, os
from pathlib import Path
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ROOT=Path('/mnt/data')
OUT_PDF=ROOT/'hmt_puerta_ley01_taxonomia_ciclos.pdf'
OUT_TEX=ROOT/'hmt_puerta_ley01_taxonomia_ciclos.tex'
OUT_WIN=ROOT/'hmt_puerta_ley01_window.tex'
OUT_JSON=ROOT/'hmt_puerta_ley01_taxonomia_ciclos_results.json'
OUT_ZIP=ROOT/'HMT_PUERTA_LEY01_TAXONOMIA_PACK.zip'

with zipfile.ZipFile(ROOT/'HMT_N38_HENSEL_LIFT_FLOW_PACK.zip') as z:
    DATA=json.loads(z.read('n38_lift_data.json'))

A=np.array(DATA['A'], dtype=int)%3
A_W=np.array([
 [0,1,1,1,1,1],
 [1,0,1,1,2,2],
 [1,1,0,2,1,2],
 [1,1,2,0,2,1],
 [1,2,1,2,0,1],
 [1,2,2,1,1,0],
], dtype=int)%3
channels=['pi','e','phi']
wphi=(1,2,1,2,0,0)
LOG=math.log(3,1000)
allcols=list(itertools.product(range(3), repeat=3))

def emit_blocks(x0, steps=180):
    x=list(map(int,x0)); blocks=[]
    for _ in range(steps):
        y=[sum(x[i]*int(A[i,j]) for i in range(6)) for j in range(6)]
        u=tuple(v%3 for v in y)
        blocks.append(u)
        x=[(y[j]-u[j])//3 for j in range(6)]
    return blocks

def int_base(ds,b):
    n=0
    for d in ds: n=n*b+int(d)
    return n

def K_of_t(t:int):
    L=6*(t+1)
    return int(math.floor(L*LOG)), L

def ceildiv(a,b):
    return -((-a)//b)

def interval_ok(digits, triads):
    L=len(digits); K=int(math.floor(L*LOG))
    N=int_base(digits,3); D=int_base(triads[:K],1000)
    return (N*1000**K < (D+1)*3**L) and ((N+1)*1000**K > D*3**L)

def candidates_for_prefix(prefix, triads):
    return [u for u in itertools.product(range(3), repeat=6) if interval_ok(prefix+list(u), triads)]

def dot(u,v): return sum(int(a)*int(b) for a,b in zip(u,v))%3

def sig(B):
    B=np.array(B,dtype=int)%3
    q=tuple(B.sum(axis=0)%3)
    a=tuple((B[0]+B[1]-B[2])%3)
    c=tuple(((B[0]+B[1]+B[2]-np.array(q))//3).tolist())
    h=tuple(((B[0]+B[1]-B[2]-np.array(a))//3).tolist())
    r=tuple(B.sum(axis=1)%3)
    colw=tuple((B!=0).sum(axis=0).tolist())
    roww=tuple((B!=0).sum(axis=1).tolist())
    dotphi=tuple(dot(B[i],wphi) for i in range(3))
    gram=tuple(tuple(dot(B[i],B[j]) for j in range(3)) for i in range(3))
    hamm=tuple(int(np.sum(B[i]!=B[j])) for i,j in [(0,1),(0,2),(1,2)])
    rhoW=tuple((B.dot(A_W).sum(axis=1)%3).tolist())
    qAW=tuple((np.array(q).dot(A_W)%3).tolist())
    aAW=tuple((np.array(a).dot(A_W)%3).tolist())
    return {'q':q,'a':a,'c':c,'h':h,'r':r,'colw':colw,'roww':roww,'dotphi':dotphi,'gram':gram,'hamming':hamm,'rhoW':rhoW,'qAW':qAW,'aAW':aAW}

def filter_fast(cand_sets,S,fields):
    cols=[]
    for j in range(6):
        C=[]
        for p,e,f in allcols:
            q=(p+e+f)%3; a=(p+e-f)%3
            c=(p+e+f-q)//3; h=(p+e-f-a)//3
            colw=(p!=0)+(e!=0)+(f!=0)
            if 'q' in fields and q!=S['q'][j]: continue
            if 'a' in fields and a!=S['a'][j]: continue
            if 'c' in fields and c!=S['c'][j]: continue
            if 'h' in fields and h!=S['h'][j]: continue
            if 'colw' in fields and colw!=S['colw'][j]: continue
            C.append((p,e,f))
        cols.append(C)
    res=[]
    for choices in itertools.product(*cols):
        B=(tuple(c[0] for c in choices), tuple(c[1] for c in choices), tuple(c[2] for c in choices))
        if any(B[i] not in cand_sets[ch] for i,ch in enumerate(channels)): continue
        S2=sig(B)
        if all(S2[f]==S[f] for f in fields): res.append(B)
    return res

def s(v): return ''.join(str(int(x)%3) for x in v)
def sm(v): return ''.join('-' if int(x)<0 else str(int(x)) for x in v)

def cluster(vals, gap=2):
    out=[]; cur=[]; prev=None
    for v in vals:
        if prev is None or v-prev<=gap:
            cur.append(v)
        else:
            out.append(cur); cur=[v]
        prev=v
    if cur: out.append(cur)
    return out

blocks={ch:emit_blocks(DATA['channels'][ch]['x0_mod_3^180'],180) for ch in channels}
triads={ch:DATA['channels'][ch]['triads_171_from_1080trits'] for ch in channels}

fields_orientation=['q','a','c','r','rhoW','colw']
rows=[]; orientation=[]; synchronized=[]; stutters=[]
for t in range(0,121):
    K,L=K_of_t(t)
    prevK,_=K_of_t(t-1) if t>0 else (None,None)
    dK=None if t==0 else K-prevK
    if dK==0: stutters.append(t)
    cand_sets={}
    counts={}
    for ch in channels:
        prefix=[d for b in blocks[ch][:t] for d in b]
        cands=set(candidates_for_prefix(prefix,triads[ch]))
        cand_sets[ch]=cands; counts[ch]=len(cands)
    equal=len(set(counts.values()))==1
    if equal: synchronized.append({'t':t,'K':K,'count':counts['pi']})
    B_real=tuple(blocks[ch][t] for ch in channels)
    S=sig(B_real)
    res=filter_fast(cand_sets,S,fields_orientation)
    phifix = (len(res)>0 and len({B[2] for B in res})==1)
    pisum_const = (len(res)>0 and len({tuple((np.array(B[0])+np.array(B[1]))%3) for B in res})==1)
    type_list=[]
    if t==0: type_list.append('seed')
    if 1<=t<=4: type_list.append('w30-lift')
    if dK==0: type_list.append('stutter')
    if equal: type_list.append('sync')
    if len(res)>1 and phifix and pisum_const: type_list.append('orientation')
    if t==5: type_list.append('R36-EF')
    if len(res)==1 and t>=5: type_list.append('unique-local')
    rows.append({
        't':t,'K':K,'phase':K%9,'dK':dK,'counts':counts,'equal':equal,
        'orient_candidates':len(res),'phi_fixed':phifix,'pi_plus_e_const':pisum_const,
        'type':'+'.join(type_list) if type_list else 'mixed',
        'real_B':[s(blocks[ch][t]) for ch in channels],
        'q':s(S['q']),'a':s(S['a']),'c':sm(S['c']),'r':s(S['r']),'rhoW':s(S['rhoW']),'colw':''.join(map(str,S['colw']))
    })
    if len(res)>1 and phifix and pisum_const:
        sums={tuple((np.array(B[0])+np.array(B[1]))%3) for B in res}
        T=min(t+5,120)
        cand_detail=[]
        for B in res:
            # Count survival to T using interval arithmetic from previous script
            surv=[]; prod=1
            for i,ch in enumerate(channels):
                prefix=[d for b in blocks[ch][:t] for d in b]+list(B[i])
                # survival count to T: exact count of extension R of length rest that intersects decimal cylinder
                Lp=len(prefix); L=6*(T+1); rbits=L-Lp
                if rbits<0: cnt=0
                else:
                    Np=int_base(prefix,3); KK=int(math.floor(L*LOG)); D=int_base(triads[ch][:KK],1000)
                    M=1000**KK; pow3=3**L; base=Np*(3**rbits)
                    # interval for R such that [N/3^L,(N+1)/3^L) intersects decimal interval
                    lo=ceildiv(D*pow3 + 1, M) - 1 - base
                    hi=((D+1)*pow3 - 1)//M - base
                    lo=max(0,lo); hi=min(3**rbits-1,hi)
                    cnt=max(0,hi-lo+1)
                surv.append(int(cnt)); prod*=int(cnt)
            cand_detail.append({'B':[s(x) for x in B], 'surv_to':T, 'surv_counts':surv, 'surv_product':prod, 'is_real':all(B[i]==blocks[ch][t] for i,ch in enumerate(channels))})
        orientation.append({
            't':t,'K':K,'phase':K%9,'counts':counts,'num_candidates':len(res),'phi_fixed':s(res[0][2]),
            'pi_plus_e':s(next(iter(sums))) if len(sums)==1 else None,
            'real_B':[s(blocks[ch][t]) for ch in channels],
            'signature':{'q':s(S['q']),'a':s(S['a']),'c':sm(S['c']),'r':s(S['r']),'rhoW':s(S['rhoW']),'colw':''.join(map(str,S['colw']))},
            'candidates':cand_detail
        })

orientation_clusters=cluster([x['t'] for x in orientation],gap=2)
sync_clusters=cluster([x['t'] for x in synchronized],gap=2)

# phase table by K mod 9
phase_stats={}
for p in range(9):
    rr=[r for r in rows if r['phase']==p and r['t']>=5]
    phase_stats[p]={
        'n':len(rr),
        'sync':sum(1 for r in rr if r['equal']),
        'orientation':sum(1 for r in rr if 'orientation' in r['type']),
        'stutter':sum(1 for r in rr if 'stutter' in r['type']),
        'first_examples':[(r['t'],r['K'],r['type']) for r in rr[:5]]
    }

results={
    'title':'PUERTA-LEY-01 -- taxonomia de puertas, ciclo mod-9 y rebote especular',
    'K_formula':'K(t)=floor(6*(t+1)*log_1000(3))',
    'stutters_t0_120':stutters,
    'orientation_clusters':orientation_clusters,
    'sync_clusters':sync_clusters,
    'phase_stats_K_mod_9':phase_stats,
    'first_23_rows':rows[:23],
    'orientation_doors_sample':orientation[:20],
    'claims':{
        'not_literal_10_equals_1':'La puerta 10 no repite literalmente la puerta 1 en conteos o firmas; lo que reinicia es la fase K mod 9 de la lectura dr9.',
        'sturmian_open_prune':'El calendario abrir/podar es una palabra sturmiana de pendiente 6 log_1000(3): casi siempre dK=1 y hay stutters cada ~22 bloques.',
        'orientation_family':'Las puertas de orientacion se agrupan en paquetes; en ellas phi queda fijo y pi/e forman un espejo con suma constante.',
        'future_breaks_mirror':'La supervivencia futura rompe la simetria pi/e y selecciona la orientacion real.'
    }
}
OUT_JSON.write_text(json.dumps(results,indent=2,ensure_ascii=False))

# Generate LaTeX
def rows_tex(rows_sel):
    lines=[]
    for r in rows_sel:
        counts=f"{r['counts']['pi']},{r['counts']['e']},{r['counts']['phi']}"
        lines.append(f"{r['t']} & {r['K']} & {r['phase']} & {counts} & {r['orient_candidates']} & {r['type'].replace('+','/')} \\")
    return '\n'.join(lines)

first_rows_tex=rows_tex(rows[:23])
orient_lines=[]
for d in orientation[:30]:
    real=[c for c in d['candidates'] if c['is_real']]
    surv=real[0]['surv_product'] if real else None
    counts=f"{d['counts']['pi']},{d['counts']['e']},{d['counts']['phi']}"
    orient_lines.append(f"{d['t']} & {d['K']} & {d['phase']} & {counts} & {d['num_candidates']} & {d['phi_fixed']} & {d['pi_plus_e']} & {surv} \\")
orient_tex='\n'.join(orient_lines)
phase_lines=[]
for p,st in phase_stats.items():
    phase_lines.append(f"{p} & {st['n']} & {st['sync']} & {st['orientation']} & {st['stutter']} \\")
phase_tex='\n'.join(phase_lines)

tex=rf'''
\section*{{PUERTA--LEY--01: taxonomía de puertas y rebote especular}}

La corrección de nivel es: no hay que buscar una ``siguiente cifra'' sino una gramática de puertas. Cada puerta combina cuatro datos:
\[
\boxed{{\text{{capacidad }}K(t),\quad\text{{fase }}K(t)\bmod9,\quad\text{{poda/stutter}},\quad\text{{firma de frontera}}.}}
\]

La capacidad decimal viene dada por:
\[
\boxed{{K(t)=\left\lfloor 6(t+1)\log_{{1000}}3\right\rfloor.}}
\]
Cada bloque abre \(3^6=729\) subceldas; cada nueva triada poda por \(1000\). El calendario de poda no es periódico ordinario: es una palabra sturmiana de pendiente \(6\log_{{1000}}3\). Los stutters auditados son:
\[
{', '.join(map(str,stutters[:15]))}.
\]

\subsection*{{1. Puertas iniciales}}
\[
\begin{{array}}{{c|c|c|c|c|c}}
 t & K & K\bmod9 & (|\pi|,|e|,|\varphi|) & \#\text{{orient}} & \text{{tipo}}\\
\hline
{first_rows_tex}
\end{{array}}
\]

La ventana inicial muestra tres hechos: \(w_6\to w_{{30}}\) ocupa \(t=0,\ldots,4\); la frontera no trivial \(R36\) empieza en \(t=5\); y el paquete \(t=7,8,9\) es una puerta de orientación.

\subsection*{{2. Puertas de orientación}}
En una puerta de orientación la firma deja varias matrices locales, pero todas tienen:
\[
\boxed{{\varphi\text{{ fijo}},\qquad \pi+e\text{{ constante}}.}}
\]
La ambigüedad vive sólo en el reparto espejo \(\pi/e\), y la supervivencia futura selecciona una orientación.

\[
\begin{{array}}{{c|c|c|c|c|c|c|c}}
 t & K & K\bmod9 & (|\pi|,|e|,|\varphi|) & \# & \varphi & \pi+e & \text{{surv real}}\\
\hline
{orient_tex}
\end{{array}}
\]

\subsection*{{3. La puerta nueve}}
Hay dos lecturas coherentes de la novena puerta.

Noveno bloque, \(t=8\):
\[
|\pi|=|e|=|\varphi|=59,
\]
la firma deja tres orientaciones con \(\varphi=110110\) fijo y \(\pi+e=112000\). La supervivencia elige la rama central.

Novena triada decimal, \(t=9\):
\[
|\pi|=|e|=|\varphi|=43,
\]
la firma deja dos orientaciones con \(\varphi=010122\) fijo y \(\pi+e=120212\). La supervivencia elige la primera.

\[
\boxed{{\text{{la novena puerta es una puerta de orientación: }}\varphi\text{{ fija escala y }}\pi/e\text{{ se espejan.}}}}
\]

\subsection*{{4. Por qué el diez no es una repetición literal del uno}}
La puerta 10 no repite literalmente la puerta 1 en conteos ni firmas. Lo que se reinicia es la fase digital:
\[
K=9\Rightarrow K\bmod9=0,
\qquad
K=10\Rightarrow K\bmod9=1.
\]
Como \(1000\equiv1\pmod9\), el retorno \(10\to1\) es retorno de fase \(dr_9\), no igualdad de frontera. La frontera queda transformada por la memoria de carry y supervivencia.

\subsection*{{5. Estadística por fase}}
\[
\begin{{array}}{{c|c|c|c|c}}
K\bmod9 & \#\text{{capas}} & \#\text{{sync}} & \#\text{{orient}} & \#\text{{stutter}}\\
\hline
{phase_tex}
\end{{array}}
\]

\subsection*{{6. Ley de puerta}}
La taxonomía ya no es plana. Una puerta puede ser:
\[
\boxed{{\text{{poda}}}},\quad
\boxed{{\text{{stutter/reapertura}}}},\quad
\boxed{{\text{{orientación especular}}}},\quad
\boxed{{\text{{saturación}}}},\quad
\boxed{{\text{{neutralidad dual}}}}.
\]
La ley general debe leerse como un autómata de frontera:
\[
\boxed{{\text{{abrir }}729\to\text{{poda/cilindro}}\to\text{{firma}}\to\text{{orientación}}\to\text{{supervivencia}}.}}
\]

\subsection*{{Dictamen}}
\[
\boxed{{\text{{verde: la puerta 9 pertenece a una familia de orientación, no es anécdota.}}}}
\]
\[
\boxed{{\text{{verde: los stutters forman el calendario de reapertura por la ley }}729/1000.}}
\]
\[
\boxed{{\text{{verde: el retorno 10=1 es retorno de fase }}K\bmod9\text{{, no repetición literal de la frontera.}}}}
\]
\[
\boxed{{\text{{amarillo: falta convertir esta taxonomía en un transductor EF automático completo.}}}}
\]
'''
OUT_TEX.write_text(tex)
OUT_WIN.write_text(tex)

# PDF via reportlab
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=8.5, leading=11))
styles.add(ParagraphStyle(name='Tiny', parent=styles['BodyText'], fontSize=7.0, leading=8.2))
styles.add(ParagraphStyle(name='HMTCodeSmall', parent=styles['BodyText'], fontName='Courier', fontSize=7.2, leading=8.4))
doc=SimpleDocTemplate(str(OUT_PDF), pagesize=A4, rightMargin=1.5*cm,leftMargin=1.5*cm, topMargin=1.3*cm,bottomMargin=1.3*cm)
story=[]
story.append(Paragraph('PUERTA-LEY-01 - taxonomia de puertas y rebote especular', styles['Title']))
story.append(Paragraph('Este documento corrige la lectura superficial de la puerta 9: no es una anecdota aislada, sino un miembro de una familia de puertas de orientacion. Ademas separa el retorno de fase K mod 9 de la repeticion literal de fronteras.', styles['Small']))
story.append(Spacer(1,0.25*cm))
story.append(Paragraph('1. Ley de capacidad', styles['Heading2']))
story.append(Paragraph('K(t)=floor(6(t+1) log_1000(3)). Cada bloque abre 729 subceldas; cada triada decimal poda por 1000. Los stutters son pasos con dK=0.', styles['Small']))
story.append(Preformatted('stutters: '+', '.join(map(str,stutters[:15])), styles['HMTCodeSmall']))
story.append(Paragraph('2. Puertas iniciales', styles['Heading2']))
table_data=[['t','K','K mod 9','counts','orient#','tipo']]
for r in rows[:23]:
    table_data.append([str(r['t']),str(r['K']),str(r['phase']),f"{r['counts']['pi']},{r['counts']['e']},{r['counts']['phi']}",str(r['orient_candidates']),r['type'].replace('+','/')])
t=Table(table_data, colWidths=[0.7*cm,0.7*cm,1.0*cm,2.2*cm,1.0*cm,7.0*cm])
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.2,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),6.5),('VALIGN',(0,0),(-1,-1),'TOP')]))
story.append(t)
story.append(PageBreak())
story.append(Paragraph('3. Familia de orientacion', styles['Heading2']))
story.append(Paragraph('En las puertas de orientacion, phi queda fijo y pi/e forman un espejo movil con suma constante. La supervivencia futura rompe el espejo.', styles['Small']))
table_data=[['t','K','phase','counts','#','phi','pi+e','surv real']]
for d in orientation[:32]:
    real=[c for c in d['candidates'] if c['is_real']]
    surv=str(real[0]['surv_product']) if real else '-'
    table_data.append([str(d['t']),str(d['K']),str(d['phase']),f"{d['counts']['pi']},{d['counts']['e']},{d['counts']['phi']}",str(d['num_candidates']),d['phi_fixed'],d['pi_plus_e'],surv])
t=Table(table_data, colWidths=[0.65*cm,0.65*cm,0.75*cm,2.0*cm,0.55*cm,1.4*cm,1.4*cm,2.0*cm])
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.2,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),6.0),('VALIGN',(0,0),(-1,-1),'TOP')]))
story.append(t)
story.append(Paragraph('4. Dictamen', styles['Heading2']))
for p in [
    'La puerta 9 pertenece a una familia de orientacion especular.',
    'El retorno 10=1 es retorno de fase K mod 9, no repeticion literal de frontera.',
    'Los stutters son el calendario de reapertura; los paquetes de orientacion aparecen alrededor de ellos.',
    'La taxonomia de puertas es: poda, stutter/reapertura, orientacion, saturacion, neutralidad dual.'
]: story.append(Paragraph(p, styles['Small']))
doc.build(story)

# zip
with zipfile.ZipFile(OUT_ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for p in [OUT_PDF,OUT_TEX,OUT_WIN,OUT_JSON,Path(__file__)]:
        z.write(p,arcname=p.name)
print('wrote',OUT_PDF,OUT_JSON,OUT_ZIP)
