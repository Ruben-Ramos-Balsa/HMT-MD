"""Acumulador documental append-only; conserva textos completos y sus versiones.

No valida los teoremas. No incluye mensajes de razonamiento interno.
Una corrección posterior se añade como otra versión, sin borrar la anterior.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'ACUMULADO_RESPUESTAS_Y_DESARROLLOS.md'
sources = [ROOT / 'CONVERSACION_CONSERVADA_20260929.md',
           ROOT / 'INTEGRACION_MATEMATICA.md']
sources += sorted(ROOT.glob('RESPUESTA_AL_USUARIO_*.md'))
sources += sorted(p for p in (ROOT / 'quantum').glob('*.md') if p.name != 'README.md')
previous = DEST.read_text() if DEST.exists() else (
    '# Acumulado de respuestas y desarrollos — cuatro interacciones HMT–MD\n\n'
    'Archivo de conservación literal. APP → TRIT → TPK → estado enriquecido → '
    'estructura discreta conjunta del continuo es la procedencia declarada por '
    'los desarrollos; las constantes se reciben como salidas. El reconocimiento '
    'convencional posterior y el alcance de cada prueba se explican en sus fuentes.\n\n'
    'Cada entrada conserva íntegro su texto, ruta y huella. Las revisiones se '
    'añaden; no se sustituyen silenciosamente. Un mensaje histórico puede contener '
    'una expresión corregida después: su conservación no es ratificación. '
    'El estado vigente de una nota es su última entrada. Los archivos Python, '
    'recibos y fuentes originales permanecen al lado, sin modificaciones.\n\n')
additions = []
for path in sources:
    content = path.read_text()
    digest = sha256(content.encode()).hexdigest()
    marker = f'<!-- source:{path.relative_to(ROOT)} sha256:{digest} -->'
    if marker in previous:
        continue
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    additions.append(f'\n---\n\n## Entrada: {path.name}\n\n{marker}\n\n'
                     f'Incorporación: {stamp}\n\nFuente: [{path.name}](<{path}>)\n\n'
                     f'SHA-256: `{digest}`\n\n### Texto íntegro\n\n{content}\n')
if additions:
    DEST.write_text(previous + ''.join(additions))
current = DEST.read_text()
for path in sources:
    content = path.read_text()
    digest = sha256(content.encode()).hexdigest()
    marker = f'<!-- source:{path.relative_to(ROOT)} sha256:{digest} -->'
    assert marker in current and content in current, path
print(f'CONSERVACION_LITERAL_OK: {len(sources)} fuentes; {len(additions)} entradas nuevas; '
      f'{len(current)} caracteres. No certifica resultados matemáticos.')
