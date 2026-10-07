#!/usr/bin/env python3
"""Corrección mecánica de delimitadores del primer corte Markdown."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize(text):
    output = []
    display = False
    for line in text.splitlines(keepends=True):
        if line.strip() == r"\[":
            display = True
            output.append(line)
            continue
        if line.strip() == r"\]":
            display = False
            output.append(line)
            continue
        if display or line.startswith("#"):
            output.append(line)
            continue
        # Sólo párrafos con fórmulas entre paréntesis, no texto entre comillas
        # de código. Los paréntesis externos eran delimitadores matemáticos.
        chars = []
        i = 0
        while i < len(line):
            if line[i] == "(":
                depth, j = 1, i + 1
                while j < len(line) and depth:
                    depth += (line[j] == "(") - (line[j] == ")")
                    j += 1
                if depth == 0:
                    content = line[i + 1:j - 1]
                    chars.append("$" + content + "$")
                    i = j
                    continue
            chars.append(line[i])
            i += 1
        output.append("".join(chars))
    return "".join(output)


if __name__ == "__main__":
    for name in ("01_CONSTRUCCION_ARITMETICA.md", "02_ORDEN_ESPECTRAL_Y_MOMENTOS.md"):
        path = ROOT / "manuscrito" / name
        original = path.read_text(encoding="utf-8")
        # Se usa una sola vez sobre el primer corte, antes de registrar sus huellas.
        if "$" in original:
            raise RuntimeError(f"El archivo ya tiene delimitadores normalizados: {path}")
        path.write_text(normalize(original), encoding="utf-8")
        print(path.name)
