from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
final = json.loads((root/'metadata/VERIFICACION_EDITORIAL_FINAL.json').read_text())
package = json.loads((root/'metadata/RECIBO_PAQUETE_ENTREGA.json').read_text())
if final['status'] != 'PASS_COMPOSICION_DOCUMENTAL_FINAL' or package['status'] != 'PASS_PAQUETE_DOCUMENTAL':
    raise SystemExit('La entrega todavía requiere cerrar sus controles.')
pdf = root/'output/pdf/HOLOGRAFIA_MODULAR_TRIADICA_20260919.pdf'
archive = Path(package['archive'])
report = root/'INFORME_ENTREGA.md'
manifest = root/'metadata/MANIFIESTO_ENTREGA.json'
pages = f"{final['pages']:,}".replace(',', '.')
prefix = f'''Ya está terminada la entrega: **un único PDF de {pages} páginas**.

**Holografía Modular Triádica**  
*Exposición sistemática del núcleo formal, sus extensiones y derivaciones.*

- [PDF completo — {pages} páginas](<{pdf}>)
- [Paquete completo: LaTeX, figuras, Python, Lean, datos y recibos](<{archive}>)
- [Informe de entrega](<{report}>) · [Manifiesto de integridad](<{manifest}>)

Las 323 entradas del inventario están vinculadas a contenido incorporado. Compilación y enlaces internos comprobados; las versiones anteriores permanecen intactas. Los controles de continuidad y genealogía han guiado la conservación de dependencias. El informe distingue la verificación documental de las demostraciones formalizadas en Lean.

<details>
<summary>Corpus y referencias vigentes</summary>

'''
refs = (root.parent/'REFERENCIAS_ENTREGA_FINAL.md').read_text()
text = prefix + refs + '\nLa inclusión de estos documentos identifica el corpus; no certifica por sí sola sus resultados.\n\n</details>\n'
dest = root.parent/'RESPUESTA_ENTREGA_FINAL.md'
dest.write_text(text)
print(dest)
