# Selector iterado, registros y firma conjunta del artículo I

Esta entrega integra una sola vez el selector y su ejecución recursiva con
los registros y los campos de firma que producen los mismos bloques.
Conserva íntegro el paquete anterior de 257 módulos y no modifica ningún PDF.

El contexto de procedencia se mantiene: APP → TRIT → TPK → estado enriquecido
→ estructura discreta conjunta del continuo. Esta formalización reúne el
tramo efectivo de refinamiento, registros e incidencia. No reemplaza el
estado enriquecido por una coordenada escalar ni llama estado completo a
un producto de operaciones independientes.

## Resultado comprobado

La ejecución comienza obteniendo la parte entera desde cotas racionales.
El guard exacto es `floor(lower) = floor(upper)`; su terminación está
demostrada. Cada paso recorta los candidatos al cilindro padre calculado
en el paso anterior, selecciona únicamente cuando queda un hijo y prolonga
ese prefijo. No recibe un prefijo futuro, cifras objetivo o registros finales.

Se demuestra que esta ejecución no falla a ninguna profundidad natural y
coincide con las publicaciones regionales. Sus palabras producen los cuatro
registros de transición; éstos satisfacen las ecuaciones y determinan las
dos elevaciones ternarias `L0` y `L1`. La inversión anterior se reutiliza.

Los mismos bloques elegidos actualizan los cilindros ternario y decimal y
producen la firma conjunta. Se demuestran compatibilidad, recuperación de
ambos prefijos previos, actualización del defecto entero, reconstrucción
por residuo y acarreo, recuperación del eje y carga dual de Witt. No hay una
segunda selección de bloques para obtener esas propiedades.

La cadena nueva reside en cuatro archivos:

1. `deltas/selector/RationalCellIntegerShift.lean`: traslación exacta entre
   la representación fraccionaria y la representación con parte entera.
2. `deltas/selector/FiniteCylinderSelector.lean`: operación finita de
   selección por recorte e hijo único; incluye dos pruebas ejecutables.
3. `deltas/selector/IteratedCylinderSelector.lean`: inicialización,
   ejecución desde el padre anterior, palabras, registros y elevaciones.
4. `deltas/selector/SelectedCylinderSignature.lean`: composición de esa
   ejecución con los cilindros, la firma, el acarreo y la carga de Witt.

Los teoremas se prueban sin `sorry` ni axiomas locales nuevos. El bloque
incorporado utiliza `propext`, `Classical.choice` y `Quot.sound`. El
antecedente conserva su dependencia declarada de `Lean.ofReduceBool` en
una comprobación finita; no se oculta ni se presenta como axioma matemático
adicional introducido por estos cuatro módulos.

## Reproducción desde las fuentes

Se requiere Python 3, Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`, con sus dependencias compiladas.
Desde esta carpeta:

```sh
python3 -I -S reproducir_selector.py --plan
python3 -I -S reproducir_selector.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

El primer comando comprueba inventario, imports y orden. El segundo comprueba
los datos de incidencia y compila la clausura completa de 261 módulos.
Los recibos están en `recibos/selector/`; el resultado reproducido se escribe
en `resultados/lean_unificado/VERIFICATION.json`. Una caché sólo se reutiliza
si coinciden las huellas de fuentes, compilador, dependencias y objetos.
El ZIP contiene las fuentes, no la caché actual como sustituto de la prueba.

## Correspondencia con la fuente y alcance

El selector corresponde a `fractional_bounds` y `generate_blocks`, líneas
855–885 del productor `verificar_generacion_infinita_nonadica.py` conservado
en el paquete probatorio común. El guard inicial coincide literalmente. La
búsqueda formal de precisión es por `Nat.find` sobre cotas internas; no se
identifica con los incrementos de precisión concretos del programa Python.
La subrutina finita `choose` es ejecutable; la búsqueda terminante y la
composición global están expresadas en una sección no computable de Lean.

Este resultado une refinamiento, registros y firma. No afirma todavía la
igualdad entre esa ejecución y las nueve actualizaciones elementales de
**todas** las fibras históricas de `Upd∘Tra∘Sel` antes de `R36`. Tampoco es
una formalización íntegra de FLM/Moonshine ni del artículo. Los resultados
anteriores comprobados no se retiran: se incorporan por sus imports y
recibos; estas delimitaciones no afirman ausencia en el corpus.

## Conservación

El manifiesto anterior y su README se conservan sin cambios en
`versiones_previas/`. La conservación de archivos y la compilación son
controles distintos. Los recibos causales describen procedencia y alcance;
no sustituyen a los teoremas compilados ni prueban otros resultados del PDF.
