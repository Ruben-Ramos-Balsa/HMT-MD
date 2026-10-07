#!/usr/bin/env python3
"""Convierte la redacción Markdown conservando literalmente sus ecuaciones.

Conversión editorial, no prueba matemática. Usa únicamente la biblioteca estándar.
No modifica el núcleo común ni los Markdown de origen.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BACKTICK = chr(96)


def escape(s):
    mapping = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
               "_": r"\_", "#": r"\#", "{": r"\{", "}": r"\}",
               "$": r"\$", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(mapping.get(c, c) for c in s)


def inline(s):
    saved = []
    pattern = re.compile(r"\\\([\s\S]*?\\\)|(?<!\\)\$[^$\n]+?(?<!\\)\$|"
                         +BACKTICK+"[^"+BACKTICK+r"\n]+"+BACKTICK)

    def hold(m):
        item = m.group()
        if item.startswith(BACKTICK):
            item = r"\texttt{" + escape(item[1:-1]) + "}"
        saved.append(item)
        return "TOKENPROTEGIDO" + str(len(saved)-1) + "FINAL"
    text = pattern.sub(hold, s)
    text = escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: r"\textbf{"+m[1]+"}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: r"\emph{"+m[1]+"}", text)
    text = text.replace("∎", r"\hfill\(\square\)")
    for i, value in enumerate(saved):
        text = text.replace("TOKENPROTEGIDO"+str(i)+"FINAL", value)
    return text


def convert(text):
    out, paragraph = [], []
    math_mode = False
    list_mode = None

    def flush():
        if paragraph:
            out.append(inline(" ".join(paragraph)) + "\n")
            paragraph.clear()

    def end_list():
        nonlocal list_mode
        if list_mode:
            out.append(r"\end{" + list_mode + "}")
            list_mode = None

    for line in text.splitlines():
        stripped = line.strip()
        if math_mode:
            out.append(line)
            if stripped == r"\]":
                math_mode = False
            continue
        if stripped == r"\[":
            flush(); end_list()
            out.append(line)
            math_mode = True
            continue
        if not stripped:
            flush()
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush(); end_list()
            level, title = len(heading[1]), heading[2]
            if level == 2:
                title = re.sub(r"^\d+\.\s+", "", title)
            command = {1:"section", 2:"subsection", 3:"subsubsection*"}[level]
            out.append("\\"+command+"{"+inline(title)+"}")
            continue
        item = re.match(r"^(\d+\.|[-*])\s+(.+)$", stripped)
        if item:
            flush()
            target = "enumerate" if item[1][0].isdigit() else "itemize"
            if target != list_mode:
                end_list()
                out.append(r"\begin{"+target+"}")
                list_mode = target
            out.append(r"\item "+inline(item[2]))
            continue
        end_list()
        paragraph.append(stripped)
    flush(); end_list()
    if math_mode:
        raise ValueError("Bloque matemático sin cerrar")
    return "\n".join(out) + "\n"


def main():
    receipts = []
    for source in sorted((ROOT/"manuscrito").glob("[0-9][0-9]_*.md")):
        output = ROOT/"sections"/(source.stem+".tex")
        raw = source.read_text(encoding="utf-8")
        result = convert(raw)
        original_math = re.findall(r"\\\[[\s\S]*?\\\]", raw)
        converted_math = re.findall(r"\\\[[\s\S]*?\\\]", result)
        if original_math != converted_math:
            raise ValueError("Se alteró una ecuación en "+source.name)
        output.write_text(result, encoding="utf-8")
        receipts.append({"source":str(source.relative_to(ROOT)),
                         "output":str(output.relative_to(ROOT)),
                         "source_sha256":hashlib.sha256(raw.encode()).hexdigest(),
                         "output_sha256":hashlib.sha256(result.encode()).hexdigest(),
                         "display_equations_preserved":len(original_math)})
    receipt = {"scope":"Conversión tipográfica, no comprobación matemática",
               "files":receipts}
    (ROOT/"gestion/RECIBO_CONVERSION_TEX.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
