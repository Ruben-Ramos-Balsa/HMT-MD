"""Renderizado completo y hojas de contacto; no certifica contenido matemático."""
from pathlib import Path
import json
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output/pdf/ARTICULO_III_ESTRUCTURA_CONSTITUTIVA_VACIO_ELECTROMAGNETICO.pdf"
OUT = ROOT / "qa/completo"
OUT.mkdir(parents=True, exist_ok=True)
reader = PdfReader(PDF)
empty = []
for i, page in enumerate(reader.pages, 1):
    if len((page.extract_text() or "").strip()) < 20:
        empty.append(i)
subprocess.run(["pdftoppm", "-scale-to", "720", "-png", "-r", "60", str(PDF), str(OUT / "pagina")], check=True)
pages = sorted(OUT.glob("pagina-*.png"))
for k in range(0, len(pages), 12):
    sheet = Image.new("RGB", (1260, 1830), "#dddddd")
    draw = ImageDraw.Draw(sheet)
    for j, path in enumerate(pages[k:k+12]):
        im = Image.open(path).convert("RGB")
        im.thumbnail((400, 570))
        x, y = 10 + (j % 3)*420, 25 + (j // 3)*455
        # A4 reducida a altura 415 para cuatro filas por hoja.
        im.thumbnail((400, 415))
        sheet.paste(im, (x + (400-im.width)//2, y))
        draw.text((x, y-17), "Página física " + str(k+j+1), fill="black")
    sheet.save(OUT / ("contacto-%02d.png" % (k//12+1)))
report = {"pages": len(reader.pages), "pages_with_less_than_20_text_characters": empty,
          "rendered_pages": len(pages), "manual_visual_review_required": True}
(OUT / "informe_renderizado.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report))
