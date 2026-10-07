# Tratado sistemático: programas, datos y pruebas

Esta carpeta reúne el material científico complementario del tratado. Los PDF
vigentes y sus fuentes completas están separados por idioma en la biblioteca.

## Lectura y fuentes

- Español: [PDF](../../../01_PDF_ESPANOL/G2_Tratado_sistematico_ES.pdf) · [fuentes LaTeX](../../../04_FUENTES_LATEX/ES/G2/LEER_FUENTES.txt).
- English: [PDF](../../../02_PDF_ENGLISH/G2_Tratado_sistematico_EN.pdf) · [LaTeX sources](../../../04_FUENTES_LATEX/EN/G2/LEER_FUENTES.txt).
- Français : [PDF](../../../03_PDF_FRANCAIS/G2_Tratado_sistematico_FR.pdf) · [sources LaTeX](../../../04_FUENTES_LATEX/FR/G2/LEER_FUENTES.txt).

La raíz LaTeX es `manuscrito/main.tex` dentro de cada carpeta lingüística.
Conserve completa esa carpeta para mantener capítulos, figuras, bibliografía e
inclusiones. Utilice `04_FUENTES_LATEX/construir_documento.py` desde la raíz de
la entrega para preparar una copia de trabajo externa. Los requisitos y la
entrada documental están identificados en el archivo `LEER_FUENTES.txt` de
cada edición. Las fuentes técnicas parciales de `source/` se conservan como
dependencias de los programas; la edición completa se encuentra en los enlaces
anteriores.

## Material científico

- `datos/`: tablas y certificados generativos.
- `propietarios/`: paquetes científicos de continuidad de K y del estado con campos.
- `complementos/`: desarrollos complementarios y conservación.
- `evidencia/`: datos, programas y certificados con su procedencia.
- `lean/`: fuentes formales APP, calendario y cadena común.
- `verificaciones/`: programas y recibos de las comprobaciones identificadas.
- `tools/`: programas de cálculo y comprobación conservados.
- `metadata/`: correspondencias de fuentes y recibos documentales.

La cadena de pruebas conserva su reproductor y sus instrucciones en
[lean/CADENA](lean/CADENA). La biblioteca común y las dependencias Lean de la
entrega están descritas en el [índice de reproducción](../../INDEX.html).
Las fuentes, hipótesis y alcance de cada comprobación permanecen en la unidad
correspondiente.

El programa de residuo regional se conserva en
[tools/residuo_regional_computable.py](tools/residuo_regional_computable.py).
En una copia de trabajo, desde esta carpeta, su comprobación específica se
invoca con `python3 -I -S tools/residuo_regional_computable.py --self-test`.
Ese comando ejecuta una comprobación científica; la organización de esta
entrega no la ha repetido.

Los recibos anteriores conservan sus identidades originales. La correspondencia
con las ubicaciones presentes se encuentra en
[RUTAS_PORTABLES.json](../../../06_VERIFICACION/RUTAS_PORTABLES.json).
El inventario de los archivos efectivamente entregados es
[MANIFIESTO.json](../../../06_VERIFICACION/MANIFIESTO.json).

## English

This folder contains supporting scientific programs, data and proof sources.
Use the links above for the current PDFs and complete language-specific LaTeX
sources. Retain each source folder intact. The shared reproduction index gives
the software requirements and existing proof entry points. Historical receipts
retain their original identities; the location map connects relocated files to
the current delivery. No scientific calculation or Lean proof was rerun for this
folder organisation.

## Français

Ce dossier contient les programmes scientifiques, les données et les sources de
preuves complémentaires. Les liens ci-dessus donnent accès aux PDF actuels et
aux sources LaTeX complètes dans chaque langue. Conserver chaque dossier source
intact. L'index de reproduction décrit les logiciels requis et les points
d'entrée des preuves. Les reçus antérieurs conservent leurs identités ; la table
des chemins relie les fichiers déplacés à la livraison actuelle. Aucun calcul
scientifique ni preuve Lean n'a été réexécuté pour cette organisation.
