GUÍA / DOSIER ACADÉMICO — FUENTES ES, EN Y FR
ACADEMIC GUIDE / DOSSIER — ES, EN AND FR SOURCES
GUIDE / DOSSIER ACADÉMIQUE — SOURCES ES, EN ET FR

ES — Esta carpeta contiene las fuentes completas de la guía de 20 páginas en
español, inglés y francés. Para leerla, abra el PDF del idioma correspondiente
en la colección de lectura. Para reconstruirla, utilice build_guia.py siguiendo
las instrucciones de esta página. Las fuentes son Python, JSON y PNG; la guía
no necesita un maestro LaTeX.

EN — This folder contains the complete sources for the 20-page academic guide
in Spanish, English and French. To read the guide, open the PDF for your language
in the reading collection. To rebuild it, use build_guia.py as described below.
The sources are Python, JSON and PNG; no LaTeX master is required.

FR — Ce dossier contient les sources complètes du guide académique de 20 pages
en espagnol, anglais et français. Pour le lire, ouvrez le PDF de votre langue
dans la collection de lecture. Pour le reconstruire, utilisez build_guia.py
selon les instructions ci-dessous. Les sources sont Python, JSON et PNG ;
aucun fichier maître LaTeX n’est nécessaire.

CONTENIDO / CONTENTS / CONTENU

ES/source, EN/source, FR/source : textos, tablas, datos, portadas y constructores
completos de cada idioma / complete texts, tables, data, covers and builders for
each language / textes, tableaux, données, couvertures et scripts de chaque langue.

shared/poster_layout.py : composición compartida / shared layout / mise en page
commune. El archivo conserva su contenido íntegro / unchanged source / source
intégralement conservée.

build_guia.py : punto de entrada portátil / portable entrypoint / lanceur portable.
INTEGRIDAD_FUENTES.json : inventario SHA-256 / SHA-256 inventory / inventaire SHA-256.

REQUISITOS / REQUIREMENTS / PRÉREQUIS

Python 3.9+; reportlab, matplotlib, svglib, Pillow, pypdf (requirements.txt).

ES — Instale las bibliotecas en un entorno virtual. Elija una instalación legal
de Times New Roman (regular, negrita, cursiva), Arial (regular, negrita) y Arial
Unicode MS. Los archivos tipográficos no se distribuyen aquí. Arial Unicode MS
puede requerir una licencia e instalación adicionales. Las ecuaciones emplean
las fuentes STIX suministradas con Matplotlib.

EN — Install the libraries in a virtual environment. Use legally installed Times
New Roman (regular, bold, italic), Arial (regular, bold) and Arial Unicode MS.
Font files are not distributed here. Arial Unicode MS may require an additional
licence and installation. Equations use the STIX fonts supplied with Matplotlib.

FR — Installez les bibliothèques dans un environnement virtuel. Utilisez des
polices légalement installées : Times New Roman (normal, gras, italique), Arial
(normal, gras) et Arial Unicode MS. Les fichiers de polices ne sont pas fournis.
Arial Unicode MS peut nécessiter une licence et une installation supplémentaires.
Les équations utilisent les polices STIX livrées avec Matplotlib.

INSTALACIÓN / INSTALLATION / INSTALLATION

macOS / Linux (terminal, desde esta carpeta / from this folder / dans ce dossier):
  python3 -m venv .venv
  .venv/bin/python -m pip install -r requirements.txt
  .venv/bin/python build_guia.py --check-only

Windows (PowerShell, misma carpeta / same folder / même dossier):
  py -3 -m venv .venv
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  .venv\Scripts\python.exe build_guia.py --check-only

ES — Copie fontmap.macos.example.json o fontmap.windows.example.json a
fontmap.local.json y ajuste las rutas a las fuentes instaladas. Las rutas
relativas se resuelven junto al mapa. El campo opcional sha256 fija la versión
binaria de cada fuente. Mantenga los ejemplos sin cambios.

EN — Copy fontmap.macos.example.json or fontmap.windows.example.json to
fontmap.local.json and set the paths to your installed fonts. Relative paths are
resolved beside the map. An optional sha256 field fixes the binary font version.
Keep the example files unchanged.

FR — Copiez fontmap.macos.example.json ou fontmap.windows.example.json vers
fontmap.local.json et adaptez les chemins aux polices installées. Les chemins
relatifs partent du dossier de cette carte. Le champ facultatif sha256 fixe la
version binaire de chaque police. Conservez les exemples sans modification.

COMPROBACIÓN / CHECK / VÉRIFICATION

ES — El primer comando verifica inventario, huellas, sintaxis y equivalencia del
código de dibujo sin generar PDF. El segundo verifica bibliotecas y tipografías.
EN — The first command checks inventory, hashes, syntax and drawing-code
equivalence without generating a PDF. The second checks libraries and fonts.
FR — La première commande vérifie l’inventaire, les empreintes, la syntaxe et
l’équivalence du code de dessin sans PDF. La seconde vérifie bibliothèques et polices.

  python build_guia.py --check-only
  python build_guia.py --check-environment --fontmap fontmap.local.json

GENERAR PDF / BUILD PDF / PRODUIRE LE PDF

  python build_guia.py --render --language ES --fontmap fontmap.local.json --output salida/GUIA_ES.pdf
  python build_guia.py --render --language EN --fontmap fontmap.local.json --output salida/GUIA_EN.pdf
  python build_guia.py --render --language FR --fontmap fontmap.local.json --output salida/GUIA_FR.pdf

ES — Sustituya python por .venv/bin/python (macOS/Linux) o
.venv\Scripts\python.exe (Windows). Entrecomille las rutas con espacios.
El destino debe ser nuevo. Se escriben el PDF y dos informes técnicos contiguos:
.layout_metrics.json y .build.json, con paginación, bibliotecas y fuentes usadas.

EN — Replace python with .venv/bin/python (macOS/Linux) or
.venv\Scripts\python.exe (Windows). Quote paths containing spaces.
Choose a new destination. The PDF receives two adjacent technical reports:
.layout_metrics.json and .build.json, recording pagination, libraries and fonts.

FR — Remplacez python par .venv/bin/python (macOS/Linux) ou
.venv\Scripts\python.exe (Windows). Placez les chemins avec espaces entre guillemets.
Choisissez une nouvelle destination. Deux rapports techniques accompagnent le PDF :
.layout_metrics.json et .build.json, avec pagination, bibliothèques et polices.

ALCANCE TÉCNICO / TECHNICAL SCOPE / PORTÉE TECHNIQUE

ES — Las fuentes de contenido y los cuerpos de dibujo se conservan íntegros.
La entrada de composición es contenido.json con sus portadas y poster_layout.py.
El inventario permite detectar cambios de archivos; no es una firma digital.
La identidad visual y binaria del PDF también depende de las versiones de las
bibliotecas y tipografías. Compruebe las 20 páginas, tablas, glifos y ecuaciones
de una reconstrucción antes de usarla como nueva edición. Este empaquetado no
recalcula los resultados científicos. Se han verificado sintaxis y equivalencia
del dibujo; no se ha generado un PDF ni probado la ejecución en Windows.

EN — Content sources and drawing code are preserved in full. Composition uses
contenido.json, its covers and poster_layout.py. The inventory detects changed
files; it is not a digital signature. Visual and binary PDF identity also depends
on library and font versions. Review all 20 pages, tables, glyphs and equations
before using a rebuilt PDF as a new edition. Packaging does not recalculate
scientific results. Syntax and drawing-code equivalence were checked; no PDF
was generated and Windows execution was not tested.

FR — Les sources de contenu et le code de dessin sont intégralement conservés.
La composition utilise contenido.json, ses couvertures et poster_layout.py.
L’inventaire détecte les fichiers modifiés ; il ne constitue pas une signature
numérique. L’identité visuelle et binaire du PDF dépend également des versions
des bibliothèques et des polices. Vérifiez les 20 pages, tableaux, caractères et
équations avant d’utiliser une reconstruction comme nouvelle édition. Ce paquet
ne recalcule pas les résultats scientifiques. La syntaxe et l’équivalence du
dessin ont été vérifiées ; aucun PDF n’a été produit, et Windows n’a pas été testé.
