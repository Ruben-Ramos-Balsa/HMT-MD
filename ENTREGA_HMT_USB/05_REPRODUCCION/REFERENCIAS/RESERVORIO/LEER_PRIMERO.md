# Reservorio estructural común

Idioma / Language: ES

## Lectura / Reading

Esta carpeta conserva los documentos y archivos seleccionados. Puede copiarse íntegra a otro equipo. Los PDF se abren con un lector PDF, sin instalar Python, TeX ni Lean.

Keep this folder complete when copying it. PDFs require only a PDF reader; Python, TeX and Lean are needed only for the corresponding reproduction commands.


## Archivos y reproducción / Files and reproduction

Los archivos ZIP originales permanecen intactos. Las carpetas desplegadas conservan su organización para no romper las importaciones. Use las instrucciones de la edición activa, no scripts históricos de preparación.

Original ZIP archives remain unchanged. Expanded source trees preserve their relative structure. Use the active edition’s reproduction instructions rather than historical preparation scripts.

- [Lectura independiente del reservorio / Independent repository reading](GUIA_RESERVORIO.md).
- [Traza generativa coordinada](ARCHIVOS/TRAZA_GENERATIVA_COORDINADA.md).

Residencia estructural separada. No se afirma su fusión dentro del PDF integral. / Separate structural repository; it is not presented as merged into the integral PDF.

La reunión de archivos no amplía el alcance declarado de las pruebas. Las herramientas científicas generales se suministran por separado; no se instala ni ejecuta nada al conectar el USB.

Packaging does not enlarge the stated proof coverage. Scientific software tools are external prerequisites; nothing is installed or run automatically when the USB is connected.

## Comprobar esta carpeta / Verify this folder

Desde esta carpeta, ejecute el siguiente comando con Python 3.9 o posterior. El informe debe escribirse fuera de esta carpeta. / Run from this folder with Python 3.9 or later; write the report outside this folder.

```sh
python3 -B HERRAMIENTAS/verificar_digital.py --root . --report /EXTERNAL/informe.json
```

En Windows puede usar `py -3` en lugar de `python3` y una ruta externa de Windows. Este control verifica archivos, no ejecuta las pruebas científicas. / Windows may use `py -3` and an external Windows path. This checks files; it does not execute scientific proofs.
