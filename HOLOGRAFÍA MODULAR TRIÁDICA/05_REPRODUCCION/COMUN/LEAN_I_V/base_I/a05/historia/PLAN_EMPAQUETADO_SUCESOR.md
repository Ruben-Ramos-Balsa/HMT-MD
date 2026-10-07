# Plan del sucesor único del corte conforme

Estado: planificación de empaquetado; no se han creado copias, ZIP ni recibos
de compilación nuevos mediante este plan. La lista final de fuentes y su SHA
se tomarán exclusivamente del futuro recibo integrado satisfactorio.

## Antecedente fijado

- Carpeta: `output/PAQUETE_ARTICULO_I_VERTEX_CONFORME_20260921`.
- 2228 archivos físicos, incluido su manifiesto (2227 entradas manifestadas).
- `MANIFIESTO.json` SHA-256:
  `9adef915383dded4ba6a1e26a50828f501264472ac154914f098e76091aae3d0`.
- Empaquetador anterior conservado, `vertex_extension/package_vertex_conformal.py`:
  `b27ae758a6e6763eb4d7b190d935a78c9b089e2fce80a934ad4c7c158b801892`.
- Helper de inventario que ese empaquetador importa y autentica,
  `translation_coherence/package_translation_coherence.py`:
  `1ab909fed05cd8dfbde1d5d2a65a8caa1a84d88d3b35e9b1d9d1d80f9bb52d84`.

El empaquetador sucesor reutilizará las funciones `inventory`, `require_hash`,
`read`, `write` y `sha` de ese helper congelado. No invocará el `main` de ningún
empaquetador anterior ni recreará entregas anteriores.

## Condición para empezar a copiar

El futuro `VERIFICATION.json` debe tener `PASS_ORBIFOLD_INPUT_DELTA`, exactamente
354 módulos antecedentes autenticados, `authenticated_inputs_unchanged=true`,
`predecessors_modified=false`, `predecessors_recompiled=false` y
`mathlib_rebuilt=false`. Su SHA se fijará explícitamente cuando exista; no se
seleccionará un recibo por fecha o por nombre de carpeta.

El runner que lo produce es `orbifold_input/verify_orbifold_input.py`, SHA
`de7770bccc4291cc483b2a7b5e7b6a8f43005c96253fc7ad17f368ef7f56ab08`.
La lista de módulos procederá de `sources` y `dependency_order`, no de un
glob de fuentes en desarrollo. `modules`, hashes de fuente/snapshot/objeto,
inventario de declaraciones públicas y salida de consulta deben coincidir.
Las nuevas declaraciones sólo admiten `propext`, `Classical.choice` y
`Quot.sound`; los axiomas del selector permanecen en el antecedente sellado.

## Única disposición de la entrega sucesora

```text
sucesor/
  README.md                         redacción final suministrada por root
  reproducir.py                     entrada única con rutas relativas
  verificar_orbifold.py             copia literal del runner congelado
  lean/orbifold/*.lean               sólo fuentes del recibo integrado
  lean/twisted/*.lean                sólo fuentes del recibo integrado
  recibos/incremento/                recibo, consultas, snapshots, logs y objetos
  recibos/CAUSAL.json                recibo focal correspondiente al README nuevo
  recibos/CONTROL_CAUSAL.json         control focal, separado de las pruebas Lean
  recibos/REPRODUCCION_RELOCALIZADA.json
  antecedente/                      los 2228 archivos íntegros una sola vez
  historia/package_orbifold_input.py
  VERIFICACION_CONSERVACION.json
  MANIFIESTO.json
```

Los programas y testigos anteriores ya residen dentro de `antecedente/`; no se
vuelven a copiar en raíces nuevas. El README y el recibo causal nuevos no
alteran ni reutilizan como aval propio el README/recibo del antecedente.

## Rutas del ejecutor portátil

Sea `root` la nueva carpeta y `old=root/'antecedente'` el paquete conforme:

- Nuevos roots: `root/'lean/orbifold'` y `root/'lean/twisted'`.
- `--products-helper`: `old/'verificar_productos.py'`.
- `--vertex-helper`: `old/'verificar_conforme.py'`.
- Roots antiguos: `old/'lean/vertex'`, `old/'lean/conformal'`,
  `old/'lean/involution'`.
- Recibos products/conformal/involution: `old/'recibos/productos'`,
  `old/'recibos/conforme'`, `old/'recibos/involucion'`.
- Rutas translation/locality/coherence/base: las del `reproducir.py` anterior,
  anteponiendo exactamente `antecedente/` a su ruta relativa completa.
- `--modules`: exactamente `requested_modules` del recibo nuevo.
- `--report-dir`: directorio nuevo, nunca `recibos/incremento`.

El wrapper mantiene disponibles `--lean`, `--mathlib`, roots y report-dirs para
relocalización explícita. No descarga herramientas ni reconstruye Mathlib.

## Comprobaciones del sellado

1. Verificar manifiesto y todos los 2228 hashes del antecedente antes de copiar.
2. Verificar recibo nuevo fijado, fuentes, objetos, consultas e inventario exacto.
3. Copiar una sola vez el antecedente y únicamente el nuevo incremento.
4. Auditar el README final con su propio recibo causal; no confundir este control
   documental con la compilación Lean ya ejecutada.
5. Mover temporalmente la nueva carpeta y ejecutar **una sola** reproducción
   relocalizada `--plan`: sin compilar, sin duplicar carpetas históricas.
6. Exigir que ese plan reproduzca fuentes y orden del recibo nuevo y reutilice
   los 354 antecedentes; devolver la carpeta a su destino incluso si falla.
7. Cotejar origen y copia del antecedente, y origen y copia de cada fuente/recibo.
8. Crear manifiesto, ZIP exclusivo sin sobreescritura y comprobación CRC/SHA de
   cada entrada. El número nuevo de archivos se calcula, no se inventa.

Este plan no declara construido el módulo torcido completo ni el producto
orbifold. El alcance de la entrega se tomará de las nuevas declaraciones Lean
realmente comprobadas y de su integración con el corte conforme preservado.
