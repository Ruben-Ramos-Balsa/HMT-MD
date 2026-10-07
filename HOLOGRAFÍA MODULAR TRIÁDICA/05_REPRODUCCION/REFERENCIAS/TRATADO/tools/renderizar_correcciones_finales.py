from pathlib import Path
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
pdf = ROOT / 'output/pdf/HOLOGRAFIA_MODULAR_TRIADICA_20260919.pdf'
out = ROOT / 'qa/correcciones_finales'
out.mkdir(parents=True, exist_ok=True)
reader = PdfReader(pdf)
destinations = reader.named_destinations
centers = {name: reader.get_destination_page_number(destinations[name]) + 1
           for name in ['equation.5.2.127', 'theorem.51.14', 'theorem.51.16', 'cite.hmt-bib-nuclear--bibliografia-1', 'cite.hmt-bib-nuclear--bibliografia-4']}
pages = sorted({1, *range(centers['equation.5.2.127'] - 1, centers['equation.5.2.127'] + 2),
                *range(centers['theorem.51.14'] - 1, centers['theorem.51.16'] + 4),
                *range(centers['cite.hmt-bib-nuclear--bibliografia-1'], centers['cite.hmt-bib-nuclear--bibliografia-4'] + 1)})
exe = '/Users/ruben/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
def render(page):
    subprocess.run([exe, '-f', str(page), '-l', str(page), '-singlefile', '-scale-to', '1600',
                    '-png', str(pdf), str(out / f'p{page}')], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(render, pages))
for i in range(0, len(pages), 4):
    canvas = Image.new('RGB', (1200, 1740), '#cccccc')
    draw = ImageDraw.Draw(canvas)
    for j, page in enumerate(pages[i:i+4]):
        im = Image.open(out / f'p{page}.png').convert('RGB')
        im.thumbnail((590, 830))
        x, y = (j % 2) * 600, (j // 2) * 870
        canvas.paste(im, (x, y + 25))
        draw.text((x + 10, y + 6), f'Página {page}', fill='black')
    canvas.save(out / f'contacto{i//4+1}.jpg', quality=94)
(out / 'PAGINAS.json').write_text(json.dumps({'pages': pages, 'centers': centers}, indent=2) + '\n')
print(json.dumps({'pages': pages, 'centers': centers, 'contacts': (len(pages)+3)//4}))
