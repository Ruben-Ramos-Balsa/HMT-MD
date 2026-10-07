# Mathlib y sus dependencias de fuente

Esta unidad conserva Mathlib en la revisión
`308445d7985027f538e281e18df29ca16ede2ba3`, correspondiente a Lean 4.21.0,
y los ocho repositorios indicados por `lake-manifest.json`, con sus revisiones
exactas, fuentes, licencias y metadatos Git. No incluye el ejecutable de Lean
para macOS, bibliotecas compiladas ni cachés de construcción.

Antes de reproducir las pruebas Lean de la cápsula I–V:

1. Instalar Lean **4.21.0** para el sistema del destinatario y disponer de Git.
2. Copiar esta unidad a un directorio local escribible, conservando `.git`
   y `.lake/packages`. Comprobar `git rev-parse HEAD` en su raíz: debe devolver
   la revisión indicada arriba. Las revisiones de cada paquete están fijadas
   en `lake-manifest.json`.
3. Preparar la biblioteca compilada mediante `lake build` desde esta raíz.
   No ejecutar `lake update`, que puede cambiar las revisiones fijadas.
4. Cuando existan `.lake/build/lib/lean` y las bibliotecas de los paquetes,
   pasar esa raíz y el Lean local al `reproducir.py` original de la cápsula,
   usando `--from-sources --portable-toolchain` y una carpeta nueva de
   resultados externa al paquete. El reproductor original no se ha editado.

Los ocho repositorios de fuentes Lean ya están presentes: no es necesario
clonarlos para disponer de su código. Esto no acredita una construcción
integral sin red. En esta revisión, `lakefile.lean` configura ProofWidgets
con `errorOnBuild`; su construcción puede solicitar la publicación/caché
correspondiente. La reconstrucción de sus componentes JavaScript usa Node y
npm. No se han descargado ni construido esos componentes durante el traslado,
y no se incluye `node_modules`. El resultado de `lake build` no se ha probado
en esta entrega documental.

Se conservan las licencias y los avisos originales: Apache 2.0 para Mathlib y
la mayoría de sus paquetes; MIT para Cli y para componentes incluidos en el
HTML de importGraph. Los avisos de autoría de los archivos permanecen intactos.

Única adaptación de representación: el enlace relativo de documentación
`.lake/packages/batteries/docs/README.md` a `../README.md` se entrega como un
archivo normal con el mismo contenido. Su representación original queda en
el repositorio Git. No cambia ningún módulo Lean; una comprobación Git de ese
archivo puede mostrar esta diferencia documental. No hay enlaces a objetos
Git externos ni rutas `objects/info/alternates` que dependan del ordenador de
origen.
