#!/usr/bin/env python3
"""Convierte los cinco manuscritos sin resumir y compila la edición de lectura.

Las fuentes de entrada y las seis fuentes comunes no se modifican. La conversión
es mecánica y comprueba la identidad literal de todas las fórmulas delimitadas.
La compilación no constituye una certificación científica.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("conversion_original", ROOT / "gestion/convertir_manuscrito.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inline(text):
    protected = []
    pattern = re.compile(r"\\\([\s\S]*?\\\)|(?<!\\)\$[^$\n]+?(?<!\\)\$|`[^`\n]+`")
    def hold(m):
        item = m.group()
        if item.startswith("`"):
            chunks = re.split(r"([/_;:=.\-])", item[1:-1])
            item = r"\texttt{" + "".join(module.escape(x) + (r"\allowbreak{}" if i % 2 else "") for i, x in enumerate(chunks)) + "}"
        protected.append(item)
        return "TOKENPROTEGIDO" + str(len(protected)-1) + "FINAL"
    text = module.escape(pattern.sub(hold, text))
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: r"\textbf{" + m[1] + "}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: r"\emph{" + m[1] + "}", text)
    text = text.replace("∎", r"\hfill\(\square\)")
    for i, item in enumerate(protected):
        text = text.replace("TOKENPROTEGIDO" + str(i) + "FINAL", item)
    return text


module.inline = inline


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--passes", type=int, default=3)
    args = ap.parse_args()
    subprocess.run([os.sys.executable, "-B", str(ROOT / "gestion/preparar_antecedentes_lectura.py")], check=True)
    manifest = json.loads((ROOT / "nucleo_comun/MANIFIESTO.json").read_text())
    common = []
    for entry in manifest["files"]:
        p = ROOT / entry["path"]
        archival = ROOT / "nucleo_comun" / entry["path"]
        if sha(p) != entry["sha256"] or sha(archival) != entry["sha256"]:
            raise RuntimeError("Diferencia en fuente común: " + entry["path"])
        common.append({"path": entry["path"], "sha256": sha(p)})
    output = ROOT / "gestion/lectura_generada"
    output.mkdir(exist_ok=True)
    files = []
    for src in sorted((ROOT / "manuscrito").glob("[0-9][0-9]_*.md")):
        raw = src.read_text()
        converted = module.convert(raw)
        converted = converted.replace("\\section{", "\\section{", 1)
        first_end = converted.index("\n")
        converted = converted[:first_end] + "\n\\label{lectura:manuscrito-" + src.name[:2] + "}" + converted[first_end:]
        for pattern, kind in [(r"\\\[[\s\S]*?\\\]", "display"), (r"\\\([\s\S]*?\\\)", "inline")]:
            a, b = re.findall(pattern, raw), re.findall(pattern, converted)
            if kind == "inline":
                b = [x for x in b if x != r"\(\square\)"]
                a = [re.sub(r"\s+", " ", x) for x in a]
                b = [re.sub(r"\s+", " ", x) for x in b]
            if a != b:
                raise RuntimeError("Se alteró matemática " + kind + " en " + src.name)
        # Maquetación exclusivamente: los dos encierros de 42 cifras ocupan
        # tres renglones, con la misma secuencia de números y desigualdades.
        interval_layout = re.compile(r"\\begin\{aligned\}\n([0-9.]+)\n&<([^\n]+?)\\\\\n&<([0-9.,]+)\n\\end\{aligned\}")
        converted, interval_count = interval_layout.subn(lambda m: r"\begin{gathered}" + "\n" + m[1] + r"\\" + "\n<" + m[2] + r"<\\" + "\n" + m[3] + "\n" + r"\end{gathered}", converted)
        if src.name.startswith("05_"):
            converted = converted.replace(r"\subsection{Procedencia, comprobación y alcance}", r"\enlargethispage{2\baselineskip}" + "\n" + r"\subsection{Procedencia, comprobación y alcance}")
        dst = output / (src.stem + ".tex")
        dst.write_text(converted)
        files.append({"source": str(src.relative_to(ROOT)), "source_sha256": sha(src),
                      "output": str(dst.relative_to(ROOT)), "output_sha256": sha(dst),
                      "long_intervals_reflowed_without_token_change": interval_count,
                      "display_equations": len(re.findall(r"\\\[[\s\S]*?\\\]", raw)),
                      "inline_equations": len(re.findall(r"\\\([\s\S]*?\\\)", raw))})
    receipt = {"scope": "Conservación y compilación editorial; no certificación matemática", "files": files, "common_sources": common}
    if args.compile:
        build = ROOT / "build_lectura"
        build.mkdir(exist_ok=True)
        env = dict(os.environ)
        env["TEXMFCACHE"] = str(build / "texcache")
        env["TEXMFVAR"] = str(build / "texcache")
        engine = shutil.which("lualatex") or "/Library/TeX/texbin/lualatex"
        for number in range(1, args.passes + 1):
            result = subprocess.run([engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-recorder", "-output-directory=build_lectura", "main_lectura.tex"], cwd=ROOT, env=env, capture_output=True, text=True)
            (build / f"pasada_{number}.txt").write_text(result.stdout + result.stderr)
            if result.returncode:
                print((result.stdout + result.stderr)[-7000:])
                raise SystemExit(result.returncode)
        final = ROOT / "output/pdf/ARITMETICA_GENEALOGICA_PRIMOS_Y_ESTRUCTURA_ESPECTRAL_ZETA.pdf"
        final.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(build / "main_lectura.pdf", final)
        fls = (build / "main_lectura.fls").read_text()
        receipt["pdf"] = {"path": str(final.relative_to(ROOT)), "sha256": sha(final)}
        for entry in common:
            entry["included_in_fls"] = "INPUT ./" + entry["path"] in fls or "INPUT " + entry["path"] in fls
        if not all(x["included_in_fls"] for x in common):
            raise RuntimeError("Una fuente común no aparece en el FLS")
    (ROOT / "gestion/RECIBO_EDICION_LECTURA.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
