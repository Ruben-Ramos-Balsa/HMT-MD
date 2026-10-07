# Balance de frontera y transporte de hojas en una trayectoria enriquecida

Este auxiliar formaliza la corrección de extremos publicada en el artículo de la extrema y media razón holográfica y la compone con el motor N30 existente. La ecuación de extremos es contenido recuperado; su certificado sobre `N30.walk`, con separación del incremento espacial y del cambio de hoja, es un certificado nuevo. El archivo central, los selectores terminales y los manuscritos permanecen intactos.

APP evalúa sus dos hojas mediante `rawRead`: suma o producto de los valores de las dos coordenadas, comprendidos entre uno y nueve. TRIT determina la actualización de hoja por `rho9(raw) % 3`. TPK realiza aquí el transporte finito mediante `step`, `walk`, `finish` y `rewind`. El estado enriquecido conserva las aristas completas: estados anterior y posterior, dirección, fase trítica, hoja, entero, residuo, cociente, giro y cambio de hoja. El corte causal del resultado es esta trayectoria finita enriquecida. La construcción posterior del continuo conserva su unidad; este auxiliar no modifica ni vuelve a demostrar sus cinco construcciones.

Sea la trayectoria generada por una semilla `s` y una palabra de direcciones `w`. Para cualquier observable entero `f` sobre el estado local se demuestra

\[
 \sum_{e\in\operatorname{walk}(s,w)}f(e.\mathrm{after})
 -\sum_{e\in\operatorname{walk}(s,w)}f(e.\mathrm{before})
 =f(\operatorname{finish}(s,w))-f(s).
\]

La orientación de retorno evalúa los extremos posteriores de las mismas aristas registradas en orden inverso. `rewind_walk` certifica la recuperación de la semilla desde esa memoria. En consecuencia, la segunda lectura no recibe otra palabra independiente. La diferencia de ocupaciones desaparece exactamente cuando retorna el observable considerado; el retorno de fase por sí solo no impone esa igualdad. El balance se compone para bloques consecutivos, conservando los estados intermedios y cancelando únicamente los extremos realmente compartidos.

La particularidad aritmética del motor exige un paso adicional. La lectura de una arista usa la hoja anterior en la celda posterior. Definiendo

\[
 F(s)=\operatorname{rawRead}(s.\mathrm{sheet},s.\mathrm{row},s.\mathrm{column}),
 \qquad a(e)=e.\mathrm{raw}-F(e.\mathrm{before}),
 \qquad b(e)=F(e.\mathrm{after})-e.\mathrm{raw},
\]

se obtiene, para toda trayectoria generada,

\[
 \sum a(e)+\sum b(e)=F(\operatorname{finish}(s,w))-F(s).
\]

El primer sumando registra el desplazamiento con la hoja previa; el segundo registra el efecto de la actualización de hoja en la celda alcanzada. Se conservan asimismo las identidades `raw = digit + 9*quotient9`. El balance se demuestra antes de cualquier reducción decimal y luego se transporta módulo diez.

El testigo `s=(0,8,0,0,0)` y nueve pasos norte termina en `(0,8,1,0,0)`. Los índices de fila y columna son los internos `Fin 9`; sus valores APP son uno y nueve. Retornan posición, dirección y fase trítica, mientras cambia la hoja. Las lecturas son `10` y `9`; las sumas espacial y de hoja son `−56` y `55`. La diferencia total es `−1`. El residuo pasa de `1` a `9` y el cociente de `1` a `0`. El registro de memoria incorpora nueve aristas. Lean verifica este testigo y el verificador exige que Lean rechace la igualdad que omite el sumando de hoja.

La fase del tipo `N30.State` es `Fin 3`. Por tanto, `nine_step_balance` certifica su retorno trítico después de nueve pasos junto con el incremento de memoria. El módulo no identifica ese hecho con una demostración nueva de toda la holonomía nonádica sobre el estado enriquecido global.

## Empalme exacto con el trabajo de K

La selección conjunta excepcional y temporal ya tiene su teorema propio: `terminal_selection_unique`, en `output/PAQUETE_ARTICULO_I_SELECTOR_ITERADO_20260919/lean/terminal/TerminalOrbitalSelection.lean`. Allí la cara excepcional se calcula desde el panel regional y la condición heterotípica actúa sobre los candidatos; el registro final aparece en la conclusión y no como argumento de `selectFrom`. La secuencia documentada es `19446 → 79 → 1`. Este resultado selecciona el registro dentro del dominio estructural declarado y se conserva íntegramente. El auxiliar presente trata el transporte de incidencias y memoria; complementa esa selección y no vuelve a plantearla como una inversión de Hadamard. En esta entrega se ha cotejado la fuente del selector y el teorema terminal, sin recompilarlos ni repetir el censo.

El extractor `\(\mathcal E_{108}^{90,120}\)` recibe el registro de incidencias anterior a K. La inversión posterior de diferencias y carga no sustituye esa evaluación. El presente auxiliar fija los términos de borde de las dos lecturas de una misma trayectoria registrada y puede importarse al componer los recuentos de una familia concreta.

En el código actual, `N30DirectedImpacts.Pair` recibe dos palabras desde una misma semilla. Su tipo no las identifica con una trayectoria y su inversa registrada. `DirectedTraceLedger.reverse` permuta los dos canales recibidos; esa operación no construye por sí misma la trayectoria inversa. La inversión geométrica del corpus comienza, en cambio, en el extremo final y transporta hojas y memoria. Se mantienen separados estos dominios.

La regla de la tabla de trazas o de su generador determina qué pareja corresponde al canal 120. Para ese empalme deben conservarse la elección de ventanas, la orientación, la multiplicidad y el predicado sobre aristas. Un observable sobre aristas que usa la hoja anterior no se reemplaza sin prueba por un observable sobre estados. La identidad de este auxiliar no se presenta como ecuación de selección numérica de K ni como cierre global de Lean. Su aportación concreta es hacer explícitos los términos de extremos y cambio de hoja y proporcionar un control que detecta su omisión en la comparación fiel de una historia consigo misma.

## Propietarios y pruebas

- `output/PAQUETE_ARTICULO_I_LECTURA_CONJUNTA_20260920/fuentes/articulo_x/sections/registro_incidencias.tex`, líneas 121–133: corrección de extremos antes del módulo diez.
- `output/PAQUETE_ARTICULO_I_LECTURA_CONJUNTA_20260920/fuentes/articulo_x/sections/tpk_desarrollo_integrado.tex`, líneas 423–471: inversión de trayectorias y transporte de datos.
- `output/PAQUETE_ARTICULO_I_LECTURA_CONJUNTA_20260920/lean/biblioteca/N30Transport.lean`: motor, lectura en hoja anterior, memoria, composición y `rewind_walk`.
- `output/PAQUETE_ARTICULO_I_LECTURA_CONJUNTA_20260920/lean/biblioteca/N30DirectedImpacts.lean`, líneas 13–39: dominio efectivo de la pareja de palabras.
- `PUBLICACION_HMT/SERIE_ARTICULOS_HMT/evidencias/INTEGRACION_VI_VII_20260910/DELTA_TRAZAS_DIRIGIDAS_20260910/prueba_transporte_impactos.tex`, líneas 60–91: predicado de impacto, recuentos de dos trazas e intercambio del lector.
- `N30BoundaryTransport.lean`: prueba por inducción sobre la palabra generada, composición por concatenación y testigo exacto.

La aritmética de enteros y el lenguaje de Lean actúan como lenguaje de prueba posterior de estas operaciones explícitas; ninguna constante objetivo define la semilla, la ruta o los coeficientes del transporte.

## Reproducción

Ejecutar `python3 -I -S verify_boundary_transport.py` desde este directorio. El verificador comprueba las huellas del compilador y de la clausura de dependencias, compila una copia objeto de `N30Transport` en este auxiliar, compila el módulo nuevo y revisa sus axiomas. Sólo se admiten `propext`, `Classical.choice` y `Quot.sound`. El control negativo debe ser rechazado. `VERIFICATION.json` registra comandos, huellas, resultados y alcance. El verificador no edita ninguna fuente de la biblioteca compartida.
