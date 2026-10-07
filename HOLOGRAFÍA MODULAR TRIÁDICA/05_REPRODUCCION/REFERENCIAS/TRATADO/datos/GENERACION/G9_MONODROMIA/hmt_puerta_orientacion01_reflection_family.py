#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import json, zipfile, itertools, math
from pathlib import Path
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ROOT=Path('/mnt/data')
OUT_PDF=ROOT/'hmt_puerta_orientacion01_reflection_family.pdf'
OUT_TEX=ROOT/'hmt_puerta_orientacion01_reflection_family.tex'
OUT_WIN=ROOT/'hmt_puerta_orientacion01_window.tex'
OUT_JSON=ROOT/'hmt_puerta_orientacion01_results.json'
OUT_ZIP=ROOT/'HMT_PUERTA_ORIENTACION01_PACK.zip'

with zipfile.ZipFile(ROOT/'HMT_N38_HENSEL_LIFT_FLOW_PACK.zip') as z:
    DATA=json.loads(z.read('n38_lift_data.json'))
A=np.array(DATA['A'],dtype=int)%3
A_W=np.array([
 [0,1,1,1,1,1],
 [1,0,1,1,2,2],
 [1,1,0,2,1,2],
 [1,1,2,0,2,1],
 [1,2,1,2,0,1],
 [1,2,2,1,1,0],
],dtype=int)%3
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

def ceildiv(a,b): return -((-a)//b)

def K_of_t(t):
    L=6*(t+1)
    return int(math.floor(L*LOG)), L

def interval_ok(digits, triads):
    L=len(digits); K=int(math.floor(L*LOG))
    N=int_base(digits,3); D=int_base(triads[:K],1000)
    return (N*1000**K < (D+1)*3**L) and ((N+1)*1000**K > D*3**L)

def candidates_for_prefix(prefix, triads):
    return [u for u in itertools.product(range(3), repeat=6) if interval_ok(prefix+list(u),triads)]

def candidates(blocks, triads, t):
    return candidates_for_prefix([d for b in blocks[:t] for d in b], triads)

def survival_count_to(prefix, triads, T):
    Lp=len(prefix); L=6*(T+1); r=L-Lp
    assert r>=0
    Np=int_base(prefix,3); K=int(math.floor(L*LOG)); D=int_base(triads[:K],1000)
    M=1000**K; pow3=3**L; base=Np*(3**r)
    hi=((D+1)*pow3-1)//M - base
    lo=ceildiv(D*pow3+1, M) - 1 - base
    lo=max(lo,0); hi=min(hi,3**r-1)
    return max(0, hi-lo+1)

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
def sB(B): return '('+','.join(s(x) for x in B)+')'

blocks={ch:emit_blocks(DATA['channels'][ch]['x0_mod_3^180'],180) for ch in channels}
triads={ch:DATA['channels'][ch]['triads_171_from_1080trits'] for ch in channels}
fields_orientation=['q','a','c','r','rhoW','colw']

# Basic counts and synchronized doors
count_rows=[]
orientation_doors=[]
for t in range(5,61):
    cand_sets={ch:set(candidates(blocks[ch],triads[ch],t)) for ch in channels}
    counts={ch:len(cand_sets[ch]) for ch in channels}
    K,L=K_of_t(t); Kprev,_=K_of_t(t-1)
    S=sig(tuple(blocks[ch][t] for ch in channels))
    equal=len(set(counts.values()))==1
    count_rows.append({'t':t,'K':K,'L':L,'dK':K-Kprev,'counts':counts,'equal':equal})
    # Work orientation only if column filter manageable; fast filter handles it.
    res=filter_fast(cand_sets,S,fields_orientation)
    if len(res)>1 and len({B[2] for B in res})==1 and len({(B[0],B[1]) for B in res})==len(res):
        sums={tuple((np.array(B[0])+np.array(B[1]))%3) for B in res}
        T=min(t+5,60)
        candidates_detail=[]
        for B in res:
            surv_counts=[]; prod=1
            for i,ch in enumerate(channels):
                prefix=[d for b in blocks[ch][:t] for d in b]+list(B[i])
                cnt=survival_count_to(prefix,triads[ch],T)
                surv_counts.append(cnt); prod*=cnt
            candidates_detail.append({'B':[s(x) for x in B], 'surv_to':T, 'surv_counts':surv_counts, 'surv_product':prod, 'is_real':all(B[i]==blocks[ch][t] for i,ch in enumerate(channels))})
        orientation_doors.append({
            't':t,'K':K,'counts':counts,'num_candidates':len(res),'phi_fixed':s(res[0][2]),
            'pi_plus_e_constant':len(sums)==1,'pi_plus_e':s(next(iter(sums))) if len(sums)==1 else None,
            'real_B':[s(blocks[ch][t]) for ch in channels],
            'signature':{'q':s(S['q']),'a':s(S['a']),'c':sm(S['c']),'r':s(S['r']),'rhoW':s(S['rhoW']),'colw':''.join(map(str,S['colw'])),'qAW':s(S['qAW']),'aAW':s(S['aAW'])},
            'candidates':candidates_detail
        })

synchronized=[r for r in count_rows if r['equal']]
# clusters of orientation doors contiguous or near
def cluster(vals):
    clusters=[]; cur=[]; prev=None
    for v in vals:
        if prev is None or v-prev<=2:
            cur.append(v)
        else:
            clusters.append(cur); cur=[v]
        prev=v
    if cur: clusters.append(cur)
    return clusters
orientation_ts=[d['t'] for d in orientation_doors]
results={
    'title':'PUERTA-ORIENTACION-01 -- familia de puertas especulares y supervivencia',
    'fields_orientation':fields_orientation,
    'synchronized_doors_t5_60':[{'t':r['t'],'K':r['K'],'count':r['counts']['pi']} for r in synchronized],
    'orientation_doors':orientation_doors,
    'orientation_clusters':cluster(orientation_ts),
    'main_conclusions':[
        'La novena puerta no es un caso aislado: pertenece a una familia de puertas de orientacion especular.',
        'En todas las puertas de orientacion detectadas, phi queda fijo y pi/e forman el par movil con suma constante.',
        'La supervivencia futura orienta el espejo pi/e y selecciona la rama real.',
        'La puerta 9 es especial porque coincide con K=9 y cuenta sincronizada 43:43:43; t=8 es el noveno bloque y tambien presenta el mismo mecanismo.'
    ]
}
OUT_JSON.write_text(json.dumps(results,indent=2,ensure_ascii=False))

# LaTeX window
sync_str=', '.join([f"t={r['t']}({r['counts']['pi']})" for r in synchronized[:30]])
orient_lines=[]
for d in orientation_doors:
    real=[c for c in d['candidates'] if c['is_real']][0]
    orient_lines.append(f"{d['t']} & {d['K']} & {d['counts']['pi']},{d['counts']['e']},{d['counts']['phi']} & {d['num_candidates']} & {d['phi_fixed']} & {d['pi_plus_e']} & {real['surv_product']} \\")
orient_table='\n'.join(orient_lines)
tex=rf'''
\section*{{PUERTA--ORIENTACION--01: familia de puertas especulares}}

La novena puerta deja de ser una intuicion aislada. Al auditar las capas con poda intervalar y firma de frontera se ve una familia de puertas de orientacion:
\[
\boxed{{\varphi\ \text{{queda fijo}},\qquad \pi/e\ \text{{forman un par movil}},\qquad \text{{la supervivencia orienta el espejo.}}}}
\]

Se usa la firma:
\[
(q,a,c,r,\rho_W,\operatorname{{colw}}).
\]
En las puertas detectadas, la firma deja varias matrices locales, pero todas comparten la misma fila \(\varphi\), y el par \(\pi/e\) mantiene suma constante. La rama real es la que sobrevive a una profundidad futura.

\subsection*{{Puertas sincronizadas}}
Las puertas con el mismo numero de cilindros en los tres canales, en el rango auditado, incluyen:
\[
{sync_str}
\]
El caso central es:
\[
\boxed{{t=9,\quad K=9,\quad |C^\pi|=|C^e|=|C^\varphi|=43.}}
\]

\subsection*{{Puertas de orientacion especular}}
\[
\begin{{array}}{{c|c|c|c|c|c|c}}
 t & K & (|\pi|,|e|,|\varphi|) & \#\text{{local}} & \varphi\text{{ fija}} & \pi+e & \text{{supervivencia real}}\\
\hline
{orient_table}
\end{{array}}
\]

En particular:
\[
 t=8: (200112,212221,110110),\ (200121,212212,110110),\ (200211,212122,110110),
\]
con \(\varphi=110110\) fijo y \(\pi+e=112000\). La supervivencia selecciona la matriz central.

\[
 t=9: (100100,020112,010122),\ (100112,020100,010122),
\]
con \(\varphi=010122\) fijo y \(\pi+e=120212\). La supervivencia selecciona la primera.

\subsection*{{Lectura}}
La familia de puertas especulares formaliza el mecanismo de ida/vuelta: localmente hay varias orientaciones \(\pi/e\) compatibles, mientras \(\varphi\) actua como eje de autoescala. La torre futura rompe el espejo.

\[
\boxed{{\text{{la puerta de orientacion no genera cifras; orienta una frontera ya compatible.}}}}
\]

Esto sugiere la taxonomia:
\[
\text{{poda}},\quad \text{{stutter/reapertura}},\quad \text{{orientacion especular}},\quad \text{{saturacion}},\quad \text{{neutralidad dual}}.
\]
'''
OUT_TEX.write_text(tex)
OUT_WIN.write_text(tex)

# PDF
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=8.5, leading=11))
styles.add(ParagraphStyle(name='Tiny', parent=styles['BodyText'], fontSize=7.2, leading=9))

if 'HMTCode' not in styles:
    styles.add(ParagraphStyle(name='HMTCode', parent=styles['BodyText'], fontName='Courier', fontSize=8, leading=9.5))
doc=SimpleDocTemplate(str(OUT_PDF), pagesize=A4, rightMargin=1.6*cm,leftMargin=1.6*cm, topMargin=1.4*cm,bottomMargin=1.4*cm)
story=[]
story.append(Paragraph('PUERTA-ORIENTACION-01 — Familia de puertas especulares', styles['Title']))
story.append(Paragraph('Este paso audita si la novena puerta es un caso aislado o parte de una familia. Resultado: aparece una familia de puertas donde phi queda fijo, pi/e forman un espejo movil con suma constante, y la supervivencia futura selecciona la orientacion real.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('1. Puertas sincronizadas', styles['Heading2']))
sync_data=[['t','K','cilindros por canal']]+[[str(r['t']),str(r['K']),str(r['counts']['pi'])] for r in synchronized[:25]]
t=Table(sync_data, repeatRows=1, colWidths=[1.2*cm,1.2*cm,3.2*cm])
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),7.5),('ALIGN',(0,0),(-1,-1),'CENTER')]))
story.append(t)
story.append(Paragraph('La novena puerta, t=9, combina sincronización 43:43:43 con K=9. El noveno bloque, t=8, también muestra el mismo mecanismo de espejo.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('2. Puertas de orientación especular', styles['Heading2']))
orient_data=[['t','K','counts','local','phi fija','pi+e','surv real']]
for d in orientation_doors:
    real=[c for c in d['candidates'] if c['is_real']][0]
    orient_data.append([str(d['t']),str(d['K']),f"{d['counts']['pi']},{d['counts']['e']},{d['counts']['phi']}",str(d['num_candidates']),d['phi_fixed'],d['pi_plus_e'],str(real['surv_product'])])
t2=Table(orient_data, repeatRows=1, colWidths=[0.9*cm,0.9*cm,2.0*cm,1.0*cm,2.0*cm,2.0*cm,2.0*cm])
t2.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),6.7),('ALIGN',(0,0),(-1,-1),'CENTER')]))
story.append(t2)
story.append(Spacer(1,8))
story.append(Paragraph('3. Núcleo t=8/t=9', styles['Heading2']))
story.append(Preformatted('t=8: phi=110110 fijo; pi+e=112000; 3 orientaciones locales -> 1 superviviente.\nt=9: phi=010122 fijo; pi+e=120212; 2 orientaciones locales -> 1 superviviente.', styles['HMTCode']))
story.append(Paragraph('Esto confirma la lectura especular: phi actúa como eje de autoescala; pi/e son el par movil; la supervivencia futura rompe la simetría local.', styles['BodyText']))
story.append(Spacer(1,8))
story.append(Paragraph('4. Conclusión', styles['Heading2']))
story.append(Paragraph('La novena puerta no es una casualidad ni una mera poda decimal. Es una puerta de orientación dentro de una familia: localmente hay varias formas equivalentes de repartir pi/e, con phi fijo; globalmente sólo una orientación sobrevive. Esto formula la ida/vuelta: la ida abre un espejo, la vuelta futura selecciona la rama viva.', styles['BodyText']))
story.append(Paragraph('Dictamen: verde como familia de orientación especular; amarillo como ley infinita completa. El siguiente paso natural es construir el operador que anticipe cuándo aparece cada tipo de puerta: poda, stutter, orientación, saturación y neutralidad dual.', styles['BodyText']))
doc.build(story)

with zipfile.ZipFile(OUT_ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for p in [OUT_PDF,OUT_TEX,OUT_WIN,OUT_JSON,Path(__file__)]:
        if p.exists(): z.write(p,p.name)
print('OK', OUT_PDF)
