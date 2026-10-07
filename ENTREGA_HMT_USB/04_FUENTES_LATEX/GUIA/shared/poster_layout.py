"""Exact shared A4 poster composition; content and receipt checks are upstream."""
FINAL_DOCUMENTARY_LABEL = "FINAL_DOCUMENTARY_LABEL"
NARRATIVE_SELF_TOTAL = "NARRATIVE_SELF_TOTAL"
LABELS = {'ES': {'outline': 'Corpus y serie de desarrollos monográficos', 'title': 'Documentos de referencia del corpus fundamental', 'discipline': 'Holografía Modular Triádica · Mecánica Dimensional', 'series': 'Serie de desarrollos monográficos', 'series_subtitle': 'Construcciones, demostraciones y aplicaciones organizadas para su estudio académico', 'annex_label': 'VI · Anexo', 'annex_prefix': 'Anexo · ', 'page_suffix': ' páginas', 'm_theory': ['teoría M', 'teoría\xa0M']}, 'EN': {'outline': 'Corpus and Series of Monographic Developments', 'title': 'Reference Documents of the Fundamental Corpus', 'discipline': 'Triadic Modular Holography · Dimensional Mechanics', 'series': 'Series of Monographic Developments', 'series_subtitle': 'Constructions, Proofs, and Applications Organized for Academic Study', 'annex_label': 'VI · Appendix', 'annex_prefix': 'Appendix · ', 'page_suffix': ' pages', 'm_theory': ['M-theory', 'M-theory']}, 'FR': {'outline': 'Corpus et série de développements monographiques', 'title': 'Documents de référence du corpus fondamental', 'discipline': 'Holographie modulaire triadique · Mécanique dimensionnelle', 'series': 'Série de développements monographiques', 'series_subtitle': 'Constructions, preuves et applications organisées pour l’étude académique', 'annex_label': 'VI · Annexe', 'annex_prefix': 'Annexe · ', 'page_suffix': ' pages', 'm_theory': ['théorie M', 'théorie\xa0M']}}

def draw_poster(c, docs, context, language, mode=FINAL_DOCUMENTARY_LABEL):
    if language not in LABELS:
        raise ValueError("Unsupported poster language")
    if mode not in (FINAL_DOCUMENTARY_LABEL, NARRATIVE_SELF_TOTAL):
        raise ValueError("Unsupported poster pagination mode")
    if mode == NARRATIVE_SELF_TOTAL and language not in ("ES", "EN", "FR"):
        raise ValueError("Unsupported self-referential narrative language")
    if len(docs) != 17 or len({d['id'] for d in docs}) != 17:
        raise ValueError("The poster requires exactly seventeen distinct records")
    W,H,M,CW,SRC = (context[k] for k in ('W','H','M','CW','SRC'))
    para,line,cover,end,HexColor,TA_CENTER,TA_LEFT = (context[k] for k in ('para','line','cover','end','HexColor','TA_CENTER','TA_LEFT'))
    labels = LABELS[language]
    anchor = None
    c.bookmarkPage('poster');c.addOutlineEntry(labels['outline'],'poster')
    para(c,labels['title'],M,H-23,CW,15.5,19,'SerifB',TA_CENTER)
    para(c,labels['discipline'],M,H-49,CW,9.3,11,'Serif',TA_CENTER)
    line(c,M,H-69)
    by={d['id']:d for d in docs};width=CW/4
    for j,key in enumerate(['G1','G2']):
        d=by[key];x=M+j*130;tw=122;center=x+tw/2;h=128
        from PIL import Image
        im=Image.open(SRC/d['cover']);w=h*im.width/im.height
        top=H-88
        cover(c,d,center-w/2,top,h)
        y=H-225
        y=para(c,d['title'],x,y,tw,7.7,8.6,'SerifB',TA_CENTER)-4
        y=para(c,d['subtitle'],x,y,tw,6.4,7.1,'Serif',TA_CENTER)-4
        para(c,d['pages_label'],x,y,tw,6.3,7,'Serif',TA_CENTER)
    # Dos lecturas del corpus principal: temporal arriba, narrativa abajo.
    for key,top in [('G4',H-88),('G3',H-204)]:
        d=by[key];x=M+296;h=76;cw=cover(c,d,x,top,h)
        tx=x+cw+9;tw=W-M-tx
        y=para(c,d['title'],tx,top,tw,7.7,8.6,'SerifB',TA_LEFT)-4
        y=para(c,d['subtitle'],tx,y,tw,6.1,6.8,'Serif',TA_LEFT)-4
        if key == 'G3' and mode == NARRATIVE_SELF_TOTAL:
            if any(d.get(k) is not None for k in ('pdf','pdf_sha256','pages')) or d.get('pages_label') not in (None,''):
                raise ValueError("Narrative self-reference must not carry invented pagination or a PDF")
            anchor = dict(schema='HMT_POSTER_SELF_TOTAL_ANCHOR_V1', document_id='G3',
                language=language, origin='BOTTOM_LEFT_PHYSICAL_A4', unit='bp',
                page_width=W, page_height=H, x=tx, top=y, bottom=y-7,
                baseline=y-6.3, width=tw, font='Times New Roman', font_size=6.3,
                leading=7, alignment='LEFT', suffix=labels['page_suffix'])
        else:
            para(c,d['pages_label'],tx,y,tw,6.3,7,'Serif',TA_LEFT)
    c.setStrokeColor(HexColor('#555555'));c.setLineWidth(.6)
    x=M+269;y=H-170;c.line(x-10,y,x,y)
    for yy in [H-125,H-241]:
        c.line(x,y,x,yy);c.line(x,yy,x+20,yy)
        c.line(x+20,yy,x+15,yy+3);c.line(x+20,yy,x+15,yy-3)
    # Llave clásica, del corpus completo a la serie.
    y=H-320;x0=M+8;x1=W-M-8;mid=W/2;p=c.beginPath();p.moveTo(x0,y+6)
    p.curveTo(x0,y,x0+7,y,x0+15,y);p.lineTo(mid-15,y);p.curveTo(mid-6,y,mid-3,y-2,mid,y-7)
    p.curveTo(mid+3,y-2,mid+6,y,mid+15,y);p.lineTo(x1-15,y);p.curveTo(x1-7,y,x1,y,x1,y+6);c.drawPath(p)
    para(c,labels['series'],M,H-339,CW,11.5,13,'SerifB',TA_CENTER)
    para(c,labels['series_subtitle'],M,H-357,CW,7.1,8.4,'Serif',TA_CENTER)
    series=[d for d in docs[4:] if d['id']!='VIa'];tops=[H-383,H-523,H-663]
    for n,d in enumerate(series):
        col=n%4;row=n//4;x=M+col*width+4;w=width-8;center=x+w/2;top=tops[row]
        label=labels['annex_label'] if d['id']=='VI' else d['display_id']
        para(c,label,x,top,w,8,9,'SerifB',TA_CENTER)
        if d['id']=='VI':
            h=42;cw=h*.7071
            cover(c,by['VIa'],center-cw/2-7,top-12,h)
            cover(c,d,center-cw/2+7,top-19,h)
            y=para(c,d['title'],x,top-66,w,6.6,7.1,'SerifB',TA_CENTER)-2
            y=para(c,d['pages_label'],x,y,w,6,6.6,'Serif',TA_CENTER)-3
            y=para(c,labels['annex_prefix']+by['VIa']['title'],x,y,w,6.4,7,'Serif',TA_CENTER)-2
            y=para(c,by['VIa']['pages_label'],x,y,w,6,6.6,'Serif',TA_CENTER)
            if y<top-132:raise RuntimeError(('annex poster overflow',y,top))
            if row<2:line(c,x,top-133,w,color='#dddddd')
            continue
        h=43 if d['id']=='II' else 50;from PIL import Image
        im=Image.open(SRC/d['cover']);cw=h*im.width/im.height
        cover(c,d,center-cw/2,top-13,h)
        title=d['title'].replace(*labels['m_theory'])
        y=para(c,title,x,top-19-h,w,6.8,7.35,'SerifB',TA_CENTER)-3
        if d['subtitle']:y=para(c,d['subtitle'],x,y,w,6.2,6.9,'Serif',TA_CENTER)-3
        y=para(c,d['pages_label'],x,y,w,6,6.7,'Serif',TA_CENTER)
        if y<39:raise RuntimeError(('poster overflow',d['id'],y))
        if row<2:line(c,x,top-133,w,color='#dddddd')
    end(c)
    if mode == NARRATIVE_SELF_TOTAL and anchor is None:
        raise ValueError('Missing G3 pagination anchor')
    return anchor
