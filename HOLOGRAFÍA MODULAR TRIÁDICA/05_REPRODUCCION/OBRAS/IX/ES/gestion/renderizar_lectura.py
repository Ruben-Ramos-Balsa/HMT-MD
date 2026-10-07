#!/usr/bin/env python3
"""Render completo de lectura y planchas; no certifica resultados matemáticos."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--poppler-bin", type=Path)
    ap.add_argument("--dpi", type=int, default=90)
    a = ap.parse_args()
    from PIL import Image, ImageDraw
    def tool(n):
        p = a.poppler_bin / n if a.poppler_bin else None
        return str(p) if p and p.is_file() else shutil.which(n) or n
    def run(cmd):
        return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    pdf = a.pdf.resolve()
    fingerprint = hashlib.sha256(pdf.read_bytes()).hexdigest()
    out = a.output.resolve()
    for path in [out, out / "pages", out / "contacts"]:
        path.mkdir(parents=True, exist_ok=True)
    info = run([tool("pdfinfo"), str(pdf)])
    count = int(re.search(r"^Pages:\s+(\d+)", info, re.M)[1])
    (out / "pdfinfo.txt").write_text(info)
    (out / "pdffonts.txt").write_text(run([tool("pdffonts"), str(pdf)]))
    run([tool("pdftotext"), "-layout", str(pdf), str(out / "texto.txt")])
    for first in range(1, count + 1, 12):
        last = min(first + 11, count)
        run([tool("pdftoppm"), "-f", str(first), "-l", str(last), "-r", str(a.dpi), "-png", str(pdf), str(out / "pages/page")])
        print(f"Render {first}–{last}/{count}", flush=True)
    images = sorted((out / "pages").glob("page-*.png"), key=lambda p: int(p.stem.rsplit("-",1)[1]))
    if [int(p.stem.rsplit("-",1)[1]) for p in images] != list(range(1,count+1)):
        raise RuntimeError("Número de PNG inconsistente; utilizar directorio de salida limpio")
    contacts = []
    for first in range(0,count,12):
        canvas = Image.new("RGB", (1200, 2300), "#cccccc")
        draw = ImageDraw.Draw(canvas)
        for i, path in enumerate(images[first:first+12]):
            with Image.open(path) as page:
                page.thumbnail((380,540))
                x, y = 10+(i%3)*400, 28+(i//3)*575
                canvas.paste(page.convert("RGB"),(x,y))
                draw.text((x,y-20),f"Página física {first+i+1}",fill="black")
        dst = out / "contacts" / f"contact-{first+1:03d}-{min(first+12,count):03d}.png"
        canvas.save(dst)
        contacts.append(str(dst))
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != fingerprint:
        raise RuntimeError("El PDF cambió durante el render")
    receipt = {"pdf":str(pdf), "sha256":fingerprint,"pages":count,
               "dpi":a.dpi,"all_pages_rendered":True,"contacts":contacts,
               "visual_review_completed":False,"scope":"Render material para revisión visual, no certificado científico"}
    (out / "RENDER.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(receipt,ensure_ascii=False))

if __name__ == "__main__":
    main()
