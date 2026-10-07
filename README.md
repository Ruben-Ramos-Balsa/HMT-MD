# Biblioteca HMT–MD

Documentos, fuentes y materiales de reproducción del paquete editorial cerrado el 1 de octubre de 2026. La colección de lectura reúne 52 PDF en español, inglés y francés. Los programas, datos y dependencias se comparten entre idiomas.

[Descargar el paquete completo](https://github.com/Ruben-Ramos-Balsa/HMT-MD/releases/download/edicion-2026-10-01/ENTREGA_HMT_USB_2026-10-01_TRANSPORTE.zip) · [Ver la edición y sus comprobadores](https://github.com/Ruben-Ramos-Balsa/HMT-MD/releases/tag/edicion-2026-10-01)

**Autores:** Oumar Haidara Fall y Rubén Ramos Balsa.

## Empezar por la guía

| Idioma | Guía del corpus | Colección de PDF |
| --- | --- | --- |
| Español | [Abrir guía](ENTREGA_HMT_USB/01_PDF_ESPANOL/00_Guia_del_corpus_ES.pdf) | [PDF en español](ENTREGA_HMT_USB/01_PDF_ESPANOL/) |
| English | [Read the guide](ENTREGA_HMT_USB/02_PDF_ENGLISH/00_Guia_del_corpus_EN.pdf) | [PDF collection in English](ENTREGA_HMT_USB/02_PDF_ENGLISH/) |
| Français | [Lire le guide](ENTREGA_HMT_USB/03_PDF_FRANCAIS/00_Guia_del_corpus_FR.pdf) | [Collection PDF en français](ENTREGA_HMT_USB/03_PDF_FRANCAIS/) |

El integral G1 se conserva en español y forma parte de la lectura compartida por las tres colecciones.

## Consultar fuentes y datos

| Carpeta | Contenido |
| --- | --- |
| [04_FUENTES_LATEX](ENTREGA_HMT_USB/04_FUENTES_LATEX/) | Fuentes organizadas por idioma y obra; la guía incluye fuentes Python y JSON. |
| [05_REPRODUCCION](ENTREGA_HMT_USB/05_REPRODUCCION/) | Programas, datos, archivos Lean, certificados y dependencias compartidas. |
| [06_VERIFICACION](ENTREGA_HMT_USB/06_VERIFICACION/) | Catálogo, correspondencias documentales e inventario original con huellas SHA-256. |

El [mapa por obra](ENTREGA_HMT_USB/05_REPRODUCCION/MAPA_CIENTIFICO_POR_OBRA.json) relaciona documentos y materiales técnicos. Las instrucciones de ejecución se encuentran en [LEER_DEPENDENCIAS.txt](ENTREGA_HMT_USB/05_REPRODUCCION/LEER_DEPENDENCIAS.txt) y en la documentación de cada unidad.

## Descargar la edición completa

Para reproducir el paquete, utiliza el archivo `ENTREGA_HMT_USB_2026-10-01_TRANSPORTE.zip` de la sección **Releases** de este repositorio. Conserva toda la carpeta `ENTREGA_HMT_USB` al extraerlo. Abre `00_EMPEZAR_AQUI.html`, `00_START_HERE.html` o `00_COMMENCER_ICI.html` para utilizar los índices con sus enlaces locales.

La descarga completa incluye las nueve carpetas internas `.git` que fijan las revisiones de las dependencias. La vista navegable de este repositorio conserva los restantes archivos del paquete y sus rutas. Los ZIP automáticos de **Code → Download ZIP** o **Source code** contienen esa vista y no sustituyen al archivo completo de la edición.

En Windows, extrae la carpeta directamente bajo una ruta corta, por ejemplo `C:\ENTREGA_HMT_USB`. Instala las herramientas indicadas para tu sistema antes de ejecutar los programas.

## Comprobar los archivos descargados

Descarga también `verificar_transporte.py` desde la misma Release. Guárdalo junto a la carpeta extraída y ejecuta:

```bash
python3 -I -B -S verificar_transporte.py --root ENTREGA_HMT_USB
```

En Windows:

```powershell
py -3 -I -B -S verificar_transporte.py --root ENTREGA_HMT_USB
```

El comprobador de transporte coteja el manifiesto original y los 29.013 archivos conservados que enumera, incluidos los metadatos de las dependencias Git. No ejecuta cálculos científicos. El [registro de transporte](transporte/MANIFIESTO_TRANSPORTE.json) documenta las rutas, tamaños y huellas correspondientes.

Se excluyen únicamente los archivos `.DS_Store`, preferencias de visualización de carpetas creadas por macOS. El manifiesto original contiene una entrada para ese archivo volátil en la raíz. Se conserva sin modificación: su verificador estricto informa esa diferencia. El comprobador de transporte declara expresamente la exclusión y usa el resultado distinto `PASS_TRANSPORT_CONTENT` cuando los demás archivos coinciden. Los detalles figuran en la [nota de procedencia](transporte/NOTA_PROCEDENCIA_TRANSPORTE.json).

## Citar la edición

La referencia de esta biblioteca está disponible en [formato BibTeX](CITATION.bib). Al utilizar una obra concreta, cita también su título y edición tal como aparecen en el documento.

## English

Start with the English guide above. For the complete reproducible package, download `ENTREGA_HMT_USB_2026-10-01_TRANSPORTE.zip` and `verificar_transporte.py` from **Releases**, extract the folder, and run the command above. Open `00_START_HERE.html` locally to follow the reading and reproduction links. The browsable repository and GitHub's automatic source archives omit the nine internal `.git` directories; the complete release asset preserves them. Only volatile macOS `.DS_Store` files are excluded from the transport edition. The original manifest remains unchanged; the separate transport check verifies the remaining 29,013 listed files and the manifest itself.

## Français

Commencez par le guide français ci-dessus. Pour obtenir le paquet complet, téléchargez `ENTREGA_HMT_USB_2026-10-01_TRANSPORTE.zip` et `verificar_transporte.py` depuis **Releases**, extrayez le dossier et exécutez la commande ci-dessus. Ouvrez ensuite `00_COMMENCER_ICI.html` localement. Le dépôt consultable et les archives automatiques de GitHub omettent les neuf dossiers `.git` internes ; l'archive complète les conserve. Seuls les fichiers volatils `.DS_Store` de macOS sont exclus de l'édition de transport. Le manifeste original reste inchangé ; le contrôle séparé vérifie les 29 013 autres fichiers répertoriés et le manifeste lui-même.
