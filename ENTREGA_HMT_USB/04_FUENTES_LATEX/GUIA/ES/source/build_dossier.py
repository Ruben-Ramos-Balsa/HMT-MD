"""Composición compacta A4: portadas frontales y cuadros monocromos."""
from pathlib import Path
import json,hashlib,sys,re,io
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black,white,HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT
import matplotlib
matplotlib.rcParams['mathtext.fontset']='stix'
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'source';META=ROOT/'metadata'
W,H=A4;M=40;CW=W-2*M
FONT=Path('/System/Library/Fonts/Supplemental')
for n,f in [('Serif','Times New Roman.ttf'),('SerifB','Times New Roman Bold.ttf'),('SerifI','Times New Roman Italic.ttf'),('Sans','Arial.ttf'),('SansB','Arial Bold.ttf'),('Math','Arial Unicode.ttf')]:pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
pdfmetrics.registerFontFamily('Serif',normal='Serif',bold='SerifB',italic='SerifI',boldItalic='SerifB')
metrics=[]
def rich(s):
    widths=pdfmetrics.getFont('Serif').face.charWidths
    special={'ₖ':'<sub>k</sub>','ₙ':'<sub>n</sub>','𝒰':'<font name="SerifI">U</font>'}
    text=''.join(special[ch] if ch in special else (escape(ch) if ord(ch) in widths else '<font name="Math">'+escape(ch)+'</font>') for ch in s)
    return re.sub(r'([A-Za-zα-ωΑ-Ω])_([A-Za-z0-9]+(?:,[A-Za-z0-9]+)?)',r'\1<sub>\2</sub>',text)
def para(c,s,x,y,w,fs=10,lead=None,font='Serif',align=TA_JUSTIFY,markup=False):
    p=Paragraph(s if markup else rich(s),ParagraphStyle('p',fontName=font,fontSize=fs,leading=lead or fs*1.25,textColor=black,alignment=align,splitLongWords=False))
    _,h=p.wrap(w,2000);p.drawOn(c,x,y-h)
    metrics.append(dict(page=c.getPageNumber(),x=x,top=y,bottom=y-h,width=w,text=re.sub('<[^>]+>','',s)))
    return y-h
def line(c,x,y,w=CW,color='#777777'):
    c.setStrokeColor(HexColor(color));c.setLineWidth(.35);c.line(x,y,x+w,y)
def header(c,title,subtitle=''):
    c.setPageSize(A4)
    para(c,'Holografía Modular Triádica · Mecánica Dimensional',M,H-26,CW,7.2,9,'Serif',TA_LEFT)
    y=para(c,title,M,H-48,CW,16,19,'SerifB',TA_LEFT)-6
    if subtitle:y=para(c,subtitle,M,y,CW,9,11,'Serif',TA_LEFT)-7
    line(c,M,y);return y-15
def end(c):
    line(c,M,33)
    para(c,'Documentos para transferencia académica',M,25,CW-24,6.8,8,'Serif',TA_LEFT)
    para(c,str(c.getPageNumber()),W-M-20,25,20,7,8,'Serif',TA_CENTER)
    c.showPage()
def cover(c,d,x,top,h):
    from PIL import Image
    p=SRC/d['cover'];im=Image.open(p);w=h*im.width/im.height
    c.setFillColor(HexColor('#dddddd'));c.rect(x+1.2,top-h-1.2,w,h,fill=1,stroke=0)
    if d.get('cover_style')=='typographic_blue':
        c.setFillColor(white);c.rect(x,top-h,w,h,fill=1,stroke=0)
        blue='#173b68'
        def label(text,offset,size,leading,bold=False):
            style=ParagraphStyle('cover',fontName='SerifB' if bold else 'Serif',fontSize=h*size,leading=h*leading,textColor=HexColor(blue),alignment=TA_CENTER)
            p=Paragraph('<br/>'.join(rich(part) for part in text.split('<br/>')),style);_,hh=p.wrap(w*.84,h)
            p.drawOn(c,x+w*.08,top-h*offset-hh)
        label(d['title'],.14,.045,.054,True)
        label(d.get('cover_subtitle',d['subtitle']),.39,.029,.037)
        c.setStrokeColor(HexColor(blue));c.setLineWidth(.22);c.line(x+w*.25,top-h*.65,x+w*.75,top-h*.65)
        if d.get('cover_descriptor'):label(d['cover_descriptor'],.69,.022,.029)
        label('Oumar Haidara Fall<br/>Rubén Ramos Balsa',.87,.025,.032)
    else:
        c.drawImage(str(p),x,top-h,w,h,mask='auto')
    c.setStrokeColor(HexColor('#999999'));c.setLineWidth(.25);c.rect(x,top-h,w,h,fill=0,stroke=1)
    return w
def eq(c,s,y,maxw=CW,fs=11.5,x=M):
    b=io.BytesIO();math_to_image(s,b,prop=FontProperties(size=fs),format='svg',color='black')
    b.seek(0);d=svg2rlg(b);scale=min(1,maxw/d.width);d.scale(scale,scale)
    w,h=d.width*scale,d.height*scale;renderPDF.draw(d,c,x+(maxw-w)/2,y-h)
    metrics.append(dict(page=c.getPageNumber(),x=x+(maxw-w)/2,top=y,bottom=y-h,width=w,text=s))
    return y-h-7
def section(c,title,y):
    y=para(c,title,M,y,CW,11,13,'SerifB',TA_LEFT)-5
    return y
def ph(s,w,fs,lead,font='Serif',markup=False):
    p=Paragraph(s if markup else rich(s),ParagraphStyle('measure',fontName=font,fontSize=fs,leading=lead,alignment=TA_JUSTIFY,splitLongWords=False))
    return p.wrap(w,2000)[1]
def eh(s,fs=11.5,maxw=CW):
    b=io.BytesIO();math_to_image(s,b,prop=FontProperties(size=fs),format='svg',color='black');b.seek(0)
    d=svg2rlg(b);return d.height*min(1,maxw/d.width)+7
def cell_para(v,w,fs,bold=False):
    cell=rich(str(v)).replace('\n','<br/>')
    cell=re.sub(r'([A-Za-zα-ωΑ-Ω])_([A-Za-z0-9]+)',r'\1<sub>\2</sub>',cell)
    p=Paragraph(cell,ParagraphStyle('t',fontName='SerifB' if bold else 'Serif',fontSize=fs,leading=fs*1.2,alignment=TA_LEFT,splitLongWords=False))
    return p,p.wrap(w-9,1500)[1]
def table(c,cols,rows,y,widths=None,fs=8.6):
    widths=[CW/len(cols)]*len(cols) if widths is None else [CW*v for v in widths]
    def cells(values,top,bold=False):
        ps=[]
        for v,w in zip(values,widths):
            p,h=cell_para(v,w,fs,bold);ps.append((p,h))
        rh=max(h for _,h in ps)+10;x=M
        for (p,h),w in zip(ps,widths):p.drawOn(c,x+4,top-5-h);x+=w
        line(c,M,top-rh,color='#bbbbbb');return top-rh
    line(c,M,y,color='#222222');y=cells(cols,y,True)
    for r in rows:y=cells(r,y)
    metrics.append(dict(page=c.getPageNumber(),x=M,top=y,bottom=y,width=CW,text='table end'))
    return y-10
def poster(c, docs):
    shared = ROOT.parent / 'shared'
    if str(shared) not in sys.path: sys.path.insert(0, str(shared))
    from poster_layout import draw_poster, FINAL_DOCUMENTARY_LABEL
    return draw_poster(c, docs, globals(), ROOT.name, FINAL_DOCUMENTARY_LABEL)
def fiches(c,title,docs,perpage):
    from PIL import Image
    y=header(c,title)
    series=len(docs)==13
    annex=next((d for d in docs if d['id']=='VIa'),None)
    display_docs=[d for d in docs if d['id']!='VIa'] if series else docs
    planned_breaks={4,8} if series else set()
    for i,d in enumerate(display_docs):
        if i in planned_breaks:
            end(c);y=header(c,title)
        h=70 if d['id'].startswith('G') else 44
        im=Image.open(SRC/d['cover']);cw=h*im.width/im.height;x=M+cw+13;tw=CW-cw-13
        prefix='' if d['id'].startswith('G') else ('VI · Anexo documental. ' if d['id']=='VIa' else d['display_id']+'. ')
        subtitle=rich(d['subtitle'])
        if d['id']=='XI':subtitle=subtitle.replace('. Conservación', '.<br/>Conservación', 1)
        head=ph(prefix+d['title'],tw,10.3,11.7,'SerifB')+3
        if subtitle:head+=ph(subtitle,tw,9.1,10.3,'SerifI',markup=True)+4
        head+=ph(d['pages_label'],tw,8,9)+7
        bodyfs,bodylead=(9.0,10.4) if series else (9.5,11.8)
        fiche_gap=9 if series else 10
        extra=0
        if d['id']=='VI' and annex:
            annex_head='Anexo documental. '+annex['title']+'. '+annex['subtitle']+'. '+annex['pages_label']
            extra=ph(annex_head,CW,8.8,10.4,'SerifB')+5+ph(annex['body'],CW,9.0,10.8)+7
        height=max(head,h+7)+ph(d['body'],CW,bodyfs,bodylead)+extra+fiche_gap
        if y-height<47:
            if series:raise RuntimeError(('four-fiche group overflow',d['id'],height,y))
            end(c);y=header(c,title)
        top=y;c.bookmarkPage('doc_'+d['id']);c.addOutlineEntry(d['title'],'doc_'+d['id'],1)
        cover(c,d,M,top,h)
        z=para(c,prefix+d['title'],x,top,tw,10.3,11.7,'SerifB',TA_LEFT)-3
        if subtitle:z=para(c,subtitle,x,z,tw,9.1,10.3,'SerifI',TA_LEFT,markup=True)-4
        z=para(c,d['pages_label'],x,z,tw,8,9,'Serif',TA_LEFT)-7
        z=min(z,top-h-7)
        z=para(c,d['body'],M,z,CW,bodyfs,bodylead)
        if d['id']=='VI' and annex:
            c.bookmarkPage('doc_VIa');c.addOutlineEntry(annex['title'],'doc_VIa',1)
            z=para(c,annex_head,M,z-7,CW,8.8,10.4,'SerifB',TA_LEFT)-5
            z=para(c,annex['body'],M,z,CW,9.0,10.8)
        if z<47:raise RuntimeError(('fiche overflow',d['id'],z))
        y=z-fiche_gap
        if i<len(display_docs)-1:line(c,M,y+fiche_gap/2,color='#bbbbbb')
    end(c)

def flowing_tables(c,tables):
    y=header(c,'Constantes, relaciones fundamentales y datos físicos')
    def newpage(title):
        end(c);z=header(c,'Constantes, relaciones fundamentales y datos físicos')
        return para(c,title+' · continuación',M,z,CW,11.3,13.5,'SerifB',TA_LEFT)-10
    def rh(r):
        z=ph(r['name'],CW,11,13,'SerifB')+5+6
        z+=sum(eh(e) for e in r.get('equations',[]))
        if r.get('explanation'):z+=ph(r['explanation'],CW,9.2,11.5)+7
        if r.get('value'):z+=ph(r['value'],CW,8.8,11)+7
        return z
    for ti,t in enumerate(tables):
        intro=t.get('intro','');first=rh(t['rows'][0]) if t.get('rows') else 90
        needed=ph(t['title'],CW,13,15.5,'SerifB')+8+ph(intro,CW,9.3,11.7)+12+first
        if t.get('kind')=='grid':
            ws=[CW*v for v in t.get('widths',[1/len(t['columns'])]*len(t['columns']))];f=t.get('fs',8.3)
            gridh=max(cell_para(v,w,f,True)[1] for v,w in zip(t['columns'],ws))+10
            gridh+=sum(max(cell_para(v,w,f)[1] for v,w in zip(rr,ws))+10 for rr in t['grid'])+10
            gridh+=sum(eh(e,10.5) for e in t.get('equations',[]))
            if t.get('note'):gridh+=ph(t['note'],CW,8.2,10.4)+7
            needed=needed-first+gridh
        if y-needed<47:
            end(c);y=header(c,'Constantes, relaciones fundamentales y datos físicos')
        y=para(c,t['title'],M,y,CW,13,15.5,'SerifB',TA_LEFT)-8
        if intro:y=para(c,intro,M,y,CW,9.3,11.7)-12
        if t.get('kind')=='grid':
            for e in t.get('equations',[]):y=eq(c,e,y,fs=10.5)
            widths=[CW*v for v in t.get('widths',[1/len(t['columns'])]*len(t['columns']))];fs=t.get('fs',8.3)
            hh=max(cell_para(v,w,fs,True)[1] for v,w in zip(t['columns'],widths))+10
            remaining=list(t['grid'])
            while remaining:
                chunk=[];used=hh+10
                for rr in remaining:
                    height=max(cell_para(v,w,fs)[1] for v,w in zip(rr,widths))+10
                    noteh=ph(t.get('note',''),CW,8.2,10.4)+7 if len(chunk)+1==len(remaining) else 0
                    if y-used-height-noteh<48:break
                    chunk.append(rr);used+=height
                if not chunk:
                    y=newpage(t['title']);continue
                y=table(c,t['columns'],chunk,y,t.get('widths'),fs)
                remaining=remaining[len(chunk):]
                if remaining:y=newpage(t['title'])
            if t.get('note'):y=para(c,t['note'],M,y,CW,8.2,10.4)-7
        else:
            for r in t['rows']:
                if y-rh(r)<47:y=newpage(t['title'])
                y=section(c,r['name'],y)
                for e in r.get('equations',[]):y=eq(c,e,y)
                if r.get('explanation'):y=para(c,r['explanation'],M,y,CW,9.2,11.5)-7
                if r.get('value'):y=para(c,r['value'],M,y,CW,8.8,11)-7
                y-=6
        if y<44:raise RuntimeError(('table overflow',t['title'],y))
        if ti<len(tables)-1:line(c,M,y-4);y-=22
    end(c)
def rows_page(c,title,rows,intro=''):
    y=header(c,title)
    if intro:y=para(c,intro,M,y,CW,9.5,12)-11
    for r in rows:
        y=section(c,r['name'],y)
        for e in r.get('equations',[]):y=eq(c,e,y)
        if r.get('explanation'):y=para(c,r['explanation'],M,y,CW,9.2,11.5)-7
        if r.get('value'):y=para(c,r['value'],M,y,CW,8.8,11)-7
        y-=6
    if y<47:raise RuntimeError(('row page overflow',title,y))
    end(c)
def require(condition,message):
    if not condition:raise RuntimeError(message)
def check_final_document_reception():
    from pypdf import PdfReader
    selection=json.loads((ROOT.parent/'metadata/MANIFIESTO_DOCUMENTAL_PENDIENTE.json').read_text())
    require(selection.get('compilation_allowed') is True,'Final document reception is pending; PDF construction is blocked')
    records=selection['documents'][ROOT.name]
    for d in records:
        require(d.get('status')=='VERIFIED_FINAL_RECEPTION','Unreceived document '+d['id'])
        require(d.get('title_status') in ('CONFIRMED_SOURCE','CONFIRMED_TRANSLATION'),'Unconfirmed title '+d['id'])
        require(type(d.get('pages')) is int and d['pages']>0,'Unconfirmed page count '+d['id'])
        pdf=Path(d['pdf'])
        require(pdf.is_file() and hashlib.sha256(pdf.read_bytes()).hexdigest()==d['pdf_sha256'],'PDF source mismatch '+d['id'])
        require(len(PdfReader(str(pdf)).pages)==d['pages'],'PDF page count mismatch '+d['id'])
    content=json.loads((SRC/'contenido.json').read_text())
    by={d['id']:d for d in records}
    require(set(by)=={d['id'] for d in content['documents']},'Document inventory mismatch')
    for d in content['documents']:
        r=by[d['id']]
        require(all(d[k]==r[k] for k in ('title','subtitle','pages')),'Content is not synchronised with final reception: '+d['id'])
        if d['id']=='G3':
            require(all(k in r and d.get(k)==r[k] for k in ('cover_style','cover_subtitle','cover_descriptor')),'Narrative cover identity differs from final reception')

def main():
    check_final_document_reception()
    data=json.loads((SRC/'contenido.json').read_text());docs=data['documents']
    run=Path(json.loads((META/'preflight/CORTE_ACTUAL.json').read_text())['run'])
    receipt=json.loads((run/'RECIBO_PRECOMPILACION.json').read_text())
    require(receipt['status']=='PASS_HMT_MD_PRECOMPILE','Missing canonical precompile PASS')
    require(Path(receipt['artifact']['entrypoint']).resolve()==Path(__file__).resolve(),'Wrong entrypoint')
    contract=Path(receipt['contract']['path'])
    require(hashlib.sha256(contract.read_bytes()).hexdigest()==receipt['contract']['sha256'],'Contract hash mismatch')
    manifest=receipt['editorial_ledgers']['manuscript_manifest']
    require(hashlib.sha256(Path(manifest['path']).read_bytes()).hexdigest()==manifest['sha256'],'Manifest hash mismatch')
    cert=json.loads((run/'CERTIFICADO_CONTINUIDAD_EDITORIAL.json').read_text())
    for f in cert['source_files']:require(hashlib.sha256((SRC/f['path']).read_bytes()).hexdigest()==f['sha256'],'Source hash mismatch: '+f['path'])
    out=ROOT/'output/pdf';out.mkdir(parents=True,exist_ok=True)
    target=out/'HMT_MD_DOSSIER_TRANSFERENCIA_ACADEMICA_ES_REV12_20260930.pdf'
    require(Path(receipt['artifact']['output_pdf']).resolve()==target.resolve(),'Wrong output path')
    c=canvas.Canvas(str(target),pagesize=A4,pageCompression=1)
    c.setTitle('Holografía Modular Triádica y Mecánica Dimensional · Documentos y contenidos')
    c.setAuthor('Oumar Haidara Fall · Rubén Ramos Balsa')
    c.bookmarkPage('presentacion');c.addOutlineEntry('Presentación del conjunto','presentacion')
    para(c,'Holografía Modular Triádica\ny Mecánica Dimensional'.replace('\n','<br/>'),M,H-35,CW,20,23,'SerifB',TA_CENTER,True)
    y=para(c,'Documentos y contenidos para transferencia académica',M,H-91,CW,11,14,'Serif',TA_CENTER)-13
    y=para(c,'Oumar Haidara Fall · Rubén Ramos Balsa',M,y,CW,9.4,12,'Serif',TA_CENTER)-15
    line(c,M,y);y-=17
    for p in data['synthesis']:y=para(c,p,M,y,CW,10.1,13)-9
    if y<49:raise RuntimeError(('synthesis overflow',y))
    end(c)
    c.bookmarkPage('organizacion');c.addOutlineEntry('Organización y finalidad del material','organizacion')
    y=header(c,'Organización y finalidad del material')
    for p in data['document_presentation']:y=para(c,p,M,y,CW,10.1,13)-11
    if y<49:raise RuntimeError(('document presentation overflow',y))
    end(c);poster(c,docs)
    c.bookmarkPage('corpus');c.addOutlineEntry('Documentos de referencia del corpus fundamental','corpus')
    fiches(c,'Documentos de referencia del corpus fundamental',docs[:4],2)
    c.bookmarkPage('serie');c.addOutlineEntry('Serie de desarrollos monográficos','serie')
    fiches(c,'Serie de desarrollos monográficos',docs[4:],4)
    c.bookmarkPage('cuadros');c.addOutlineEntry('Constantes, relaciones fundamentales y datos físicos','cuadros')
    flowing_tables(c,data['tables'])
    c.save();(META/'layout_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
    print(target)
if __name__=='__main__':main()
