#!/usr/bin/env python3
"""Conversión editorial del desarrollo conservado; no certifica sus teoremas."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'ampliacion/expediente/02_CENTRO_BORDE_VACANCIAS_Y_MEMORIA.md'
spec = importlib.util.spec_from_file_location('conversion_heredada', ROOT/'gestion/convertir_manuscrito.py')
conversion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conversion)

raw = SOURCE.read_text(encoding='utf-8')
body = raw[raw.index('## 1.'):raw.index('## Procedencia, controles')]
tex = conversion.convert('# Centro, frontera y vacancias en la conexión nonádica\n\n' + body)
tex = tex.replace('\\section{Centro, frontera y vacancias en la conexión nonádica}',
                  '\\section{Centro, frontera y vacancias en la conexión nonádica}\n\\label{sec:centro-frontera}')
tex = tex.replace('\\subsubsection*{Proposición: recuperación desde la frontera levantada}',
                  '\\begin{proposition}[Recuperación desde la frontera levantada]\n\\label{prop:centro-frontera-recuperacion}')
tex = tex.replace('\\textbf{Demostración.} Para', '\\end{proposition}\n\\begin{proof}\nPara', 1)
needle = 'En particular, las cuatro esquinas determinan toda la carta dentro del espacio de leyes declarado.'
tex = tex.replace(needle, needle + '\n\\end{proof}', 1)
tex = tex.replace('\\textbf{Prueba.} La irracionalidad', '\\begin{proof}\nLa irracionalidad', 1)
tex = tex.replace('Una vacancia retiene capacidad mientras avanza la historia.',
                  '\\end{proof}\nUna vacancia retiene capacidad mientras avanza la historia.', 1)
tex = tex.replace('\\subsection{El factor 8/81 como balance de publicación y complemento}',
                  '\\input{ampliacion/vacancias_21_22_6_7.tex}\n\n\\subsection{El factor 8/81 como balance de publicación y complemento}')
tex = tex.replace('###', '')
tex = tex.replace('La prueba de esos recuentos y su inserción está conservada en el artículo I; esta nota la reúne,',
                  'La prueba de esos recuentos se obtiene de la inyección explícita anterior: sus cinco imágenes son distintas; este desarrollo la reúne,')
# Estas frases documentan una operación editorial en el expediente original.
# Se conserva su procedencia fuera del cuerpo científico, sin retirar resultados.
tex = tex.replace('No se introduce el ángulo \\(A\\) en esta incorporación.',
                  'Esta comparación utiliza los canales enteros y no necesita la realización angular posterior.')
tex = tex.replace('Se conserva esa fórmula localizada; no se sustituye por una lectura conjeturada de «77 dividido por dos», ni se escribe que la razón sea exactamente \\(\\pi\\).',
                  'Esta razón de anillos es una lectura racional exacta; su función se distingue de la publicación regional de \\(\\pi\\).')
tex = tex.replace('la presente nota', 'este desarrollo')
tex = tex.replace('La presente nota', 'Este desarrollo')
tex = tex.replace('la nota anterior', 'el desarrollo del transporte del doble círculo')
tex = tex.replace('esta nota', 'esta sección')
anchor = 'Su bloque interior es'
tex = tex.replace(anchor, '\\input{ampliacion/figura_centro_frontera.tex}\n\n\\Needspace{6\\baselineskip}\n' + anchor, 1)
anchor = 'El enlace con la ecuación electrónica pasa por las regiones.'
tex = tex.replace(anchor, '\\input{ampliacion/memoria_firma_555.tex}\n\n' + anchor, 1)
out = ROOT/'ampliacion/centro_frontera.tex'
out.write_text(tex, encoding='utf-8')
original = re.findall(r'\\\[[\s\S]*?\\\]', body)
converted = re.findall(r'\\\[[\s\S]*?\\\]', tex)
if original != converted:
    raise ValueError('Las ecuaciones de la incorporación deben conservarse literalmente')
receipt = {
    'source': str(SOURCE.relative_to(ROOT)),
    'source_sha256': hashlib.sha256(raw.encode()).hexdigest(),
    'destination': str(out.relative_to(ROOT)),
    'destination_sha256': hashlib.sha256(tex.encode()).hexdigest(),
    'display_equations_preserved': len(original),
    'scientific_sections': 'Secciones 1–7 íntegras, con desarrollo adicional de firmas y vacancias',
    'editorial_changes': ['Rótulo de proposición y pruebas tipografiados como entornos',
                         'Dos frases conversacionales trasladadas al registro de procedencia',
                         'Procedencia y localizadores conservados en el expediente incluido, no impresos como rutas de archivo'],
    'scope': 'Conservación y conversión editorial, no certificación matemática global'
}
(ROOT/'technical/CONVERSION_CENTRO.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
