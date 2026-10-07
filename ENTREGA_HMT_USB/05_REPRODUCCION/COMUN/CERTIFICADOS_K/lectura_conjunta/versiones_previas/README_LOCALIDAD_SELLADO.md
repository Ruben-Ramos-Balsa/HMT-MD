# Localidad de los campos reticulares construidos

Entrada conjunta: `deltas/localidad/SelectedFieldLocality.lean`.

Esta continuación demuestra la localidad de los campos cargados originales
sobre todo su portador algebraico: para cada par de cargas existe un exponente
entero no negativo, independiente del estado, que iguala los productos en los
dos órdenes después de aplicar la potencia correspondiente de la diferencia
de variables. La prueba utiliza la finitud efectiva, las dos expansiones del
factor de contracción, el orden normal, la simetría del producto y el cociclo
reticular construido. No sustituye los campos por un producto definido para
que la igualdad se cumpla.

La especialización utiliza el mismo `selectedOrigin` de la cadena conservada:
APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del
continuo → publicación de incidencia → portador y campos reticulares.
`selected_incidence_generation_products_and_locality` reúne la publicación de
incidencia, la generación del portador, los productos sobre el vacío y la
localidad comprobada. No se suministra otro registro ni se rehace la selección.
Las condiciones explícitas heredadas, incluida la interfaz S8 del selector,
permanecen sin alteración.

## Reproducción

Con Python 3, Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`, con sus dependencias compiladas:

```text
python3 -I -S reproducir_localidad.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

El ejecutor comprueba primero los datos y los programas Python conservados;
después verifica la clausura de imports Lean y las declaraciones nominales.
No requiere las rutas del ordenador de procedencia: éstas se conservan sólo
en los recibos históricos. `--plan` comprueba las fuentes e imports sin
compilar. Una ejecución posterior reutiliza únicamente objetos cuya huella,
fuente, dependencias y compilador coinciden. La caché actual de los 238 módulos
no se incluye en el ZIP. Se conservan tres `.olean` históricos de
`FoundationContract` (contratos 03, 04 y 05), ya manifestados en el predecesor,
como archivos de procedencia; no se utilizan como certificación nueva ni como
caché de esta ejecución. La reproducción desde el ZIP compila las fuentes.

El nuevo bloque contiene 22 módulos y conserva los 216 anteriores. Los seis
archivos del núcleo común y las fuentes, datos, Python y documentos del
predecesor permanecen íntegros. Su anterior README y manifiesto se guardan en
`versiones_previas/`; sus declaraciones de alcance son antecedentes, no el
estado de esta continuación. La igualdad de huellas acredita conservación,
no sustituye las pruebas Lean.

## Alcance y comprobaciones

La localidad completa aquí afirmada se refiere a estos campos construidos,
para todas las cargas y todos los estados del portador indicado. No se declara
concluida por ello la construcción de una VOA, el sector torcido, el orbifold,
FLM ni Moonshine. No se añade un axioma de localidad ni de FLM. El selector
finito heredado conserva su uso documentado de `Lean.ofReduceBool`. Las
pruebas simbólicas generales de localidad utilizan sólo los axiomas estándar;
la entrada `SelectedFieldLocality` conserva también `Lean.ofReduceBool` por
sus dependencias finitas heredadas.

El manifiesto liga cada fuente a su SHA-256. `recibos/localidad/` contiene el
recibo conjunto, los siete recibos del trabajo revisor, los controles focales
y la procedencia de ensamblaje. Los recibos causales son metadatos de
continuidad separados de la comprobación matemática por Lean. El estado final
de compilación figura en `recibos/localidad/LEAN_CONJUNTO.json`.
