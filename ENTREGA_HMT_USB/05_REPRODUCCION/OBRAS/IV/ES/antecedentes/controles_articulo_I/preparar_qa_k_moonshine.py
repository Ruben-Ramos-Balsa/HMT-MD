from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader
import json
ROOT=Path(__file__).resolve().parent.parent
pages=sorted((ROOT/'qa/paginas').glob('pagina-*.jpg'))
for start in range(0,len(pages),20):
    canvas=Image.new('RGB',(1600,2340),'#d6d6d6')
    for k,path in enumerate(pages[start:start+20]):
        im=Image.open(path).convert('RGB')
        im.thumbnail((380,432))
        x=(k%4)*400+(400-im.width)//2
        y=(k//4)*468+20
        canvas.paste(im,(x,y))
        ImageDraw.Draw(canvas).text(((k%4)*400+12,(k//4)*468+3),str(start+k+1),fill='black')
    canvas.save(ROOT/f'qa/contacto-{start//20+1}.jpg',quality=88)
pdf=ROOT/'output/pdf/ARTICULO_I_K_MOONSHINE_DUALIDAD.pdf'
reader=PdfReader(pdf)
destinations={}
for name in ('exc:k-direccion','km:orden-tres-reticular','km:fricke','exc:pantallas-dualidad','sec:conclusiones'):
    if name in reader.named_destinations:
        destinations[name]=reader.get_destination_page_number(reader.named_destinations[name])+1
check={'pages':len(reader.pages),'rendered':len(pages),'named_locations':destinations,
 'review_status':'RENDERED_NOT_YET_VISUALLY_REVIEWED'}
(ROOT/'qa/RENDER.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
print(check)
