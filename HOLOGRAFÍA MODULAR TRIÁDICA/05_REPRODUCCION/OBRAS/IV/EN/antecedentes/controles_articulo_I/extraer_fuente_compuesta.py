"""Expande entradas locales para control editorial previo; no compila ni prueba tesis."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
seen = set()

def expand(path):
    path = path.resolve()
    if path in seen:
        raise ValueError(f"Entrada repetida: {path}")
    seen.add(path)
    text = path.read_text(encoding="utf-8")
    def include(match):
        name = match.group(1)
        child = ROOT / (name if name.endswith(".tex") else name + ".tex")
        return "\n% FUENTE: " + str(child) + "\n" + expand(child)
    return re.sub(r"\\input\{([^}]+)\}", include, text)

output = ROOT / "technical/FUENTE_COMPUESTA.tex.txt"
output.write_text(expand(ROOT / "main.tex"), encoding="utf-8")
print(output)
