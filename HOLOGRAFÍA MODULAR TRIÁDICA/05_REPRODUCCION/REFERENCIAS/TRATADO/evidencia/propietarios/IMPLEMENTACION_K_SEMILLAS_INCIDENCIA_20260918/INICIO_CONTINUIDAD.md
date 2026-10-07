# Constante holográfica de acoplamiento aritmético–geométrico

## Generación, incidencia y conservación evolutiva de la unidad

Paquete de continuidad, 18 de septiembre de 2026. Reúne el texto completo del artículo X y las formalizaciones coordinadas que explicitan su cadena de generación. Los documentos entregados y las fuentes de otras tareas permanecen intactos.

La entrada matemática es la composición APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. Las regiones de cierre, autoescala y propagación se producen en esa composición; sus lecturas π, φ y e intervienen después en los lectores del registro y de α. La doble proyección conserva conjuntamente la realización arquimediana y la incidencia excepcional del estado. La finalidad de esta reunión es que esa dependencia resulte materialmente accesible, no que una colección de siglas ocupe su lugar.

## Qué abrir y en qué orden

1. **Este documento** presenta la jerarquía y los nombres matemáticos.
2. **`NOTA_DE_COMPOSICION.tex`** reúne las definiciones operativas, los operadores regionales, la incidencia, el descriptor inicial, la selección del registro, la composición con α y la recuperación. Es una nota adicional; no reemplaza el artículo.
3. **`FUENTES_INTEGRAS_PARA_LECTURA.md`** contiene todos los archivos LaTeX del artículo X en un único archivo de lectura. Mantiene el texto de cada fuente sin resumirlo.
4. **`fuentes/articulo_x/main.tex`** es el punto de compilación del artículo completo. Sus archivos incluidos, figuras y ganchos editoriales se conservan en su estructura original. Un documento LaTeX puede repartir sus capítulos en fuentes separadas sin ser varios artículos.
5. **`lean/`, `python/`, `datos/` y `recibos/`** contienen las implementaciones, los datos con sus roles explícitos y los certificados de las pruebas concretas. `MANIFIESTO.json` permite detectar cualquier alteración de las copias.

## Definiciones que sustituyen a los alias informáticos

| Objeto matemático | Construcción y función | Alias conservado para procedencia |
|---|---|---|
| Calendario de firmas regionales y reloj de conversión | Publica por bloques las bandas regionales, sus residuos, cocientes, ocupación y carga. El reloj compara potencias enteras de 3 y 1000. | N69 |
| Descriptor inicial por retorno nonádico y lectura fase–carga | Se obtiene del primer avance nulo del reloj, el retorno de nueve fases, los defectos de semibanda orientados y la lectura fase–carga. | W24; en la nota, Ω₂₄ |
| Repertorio terminal de bloques ternarios | Familia no ordenada de ocho palabras de seis trits sobre la que actúa el selector. Se conserva íntegramente su procedencia y su interfaz en el certificado. | S8 |
| Registro ordenado de acoplamiento | Doce bloques seleccionados por la incidencia y la condición orbital sobre los candidatos terminales. | K |
| Lectura racional periódica del registro | Lectura en base 1000 que conserva los doce bloques, incluidos sus ceros iniciales. | κ_ag |

El descriptor Ω₂₄ y la etapa regional w₂₄ tienen la misma longitud pero pertenecen a construcciones distintas. Sus nombres deben mantener esa diferencia sin fragmentar la composición que los relaciona.

## Centro, orientación y memoria: conexión ya escrita en el artículo

El desarrollo completo está en `fuentes/articulo_x/sections/centro_electronico_registros.tex`, incluido desde `sections/electron.tex`. La figura `figures/centro_y_vacancias.tex` también está presente.

La inversión del atlas fija únicamente la celda (5,5). Allí la hoja aditiva conserva residuo y cociente (1,1), mientras la multiplicativa conserva (7,2):

\[
5+5=1+9\cdot1,\qquad 5\cdot5=7+9\cdot2.
\]

Sobre la fibra de suma diez, las posiciones conjugadas (8,2) y (2,8) conservan el residuo siete y reducen el cociente multiplicativo en una unidad. Esta es la relación concreta entre centro, vacancia y memoria que acompaña el transporte.

El bloque central evaluado en las posiciones adyacentes 4,5 es

\[
B_c=\begin{pmatrix}7&2\\2&7\end{pmatrix}=9P_++5P_-.
\]

Su lectura por concatenación conserva 72+27=77+22=99 y 77−22=55=54+1. El centro del atlas, los modos de este bloque y las orientaciones de la ruta se componen mediante lectores específicos. La orientación inicial (1,1) produce las ventanas de signos +++−−−+++−−− del retorno electrónico. La firma 555555 pertenece a la región transversal de π y la fuente demuestra tanto su evaluación como la memoria de transporte necesaria para actualizarla. El dato 111111 de la quinta frontera nonádica tiene asimismo su localización propia. El artículo conserva estas relaciones; no necesita sustituirlas por una identificación entre cadenas de cifras.

## Cadena de formalización reunida

Las semillas seleccionadas producen sus soportes de Paley. La intersección pertinente determina la tétrada; la condición de incidencia (4,3,2) selecciona la hexada y el origen marcado. Los módulos de la biblioteca conservan la elevación hexada–octada y la realización reticular. `GeneratedMarkedIncidence.lean` reúne esa composición sin recibir K como entrada.

En la publicación regional, los prefijos generan las bandas, el calendario y el panel. `RegionalW24.lean` produce el descriptor inicial desde el reloj y la regla orientada, en lugar de recibir una cadena literal. La evaluación obtiene 020022222111211201021101. Su teorema de igualdad está compilado con los axiomas fundacionales ordinarios de Lean, sin `native_decide`.

La composición `SelectedFromRegionalInputs.lean` utiliza ese descriptor, el panel y el calendario generados. Sobre el repertorio terminal no ordenado, el selector examina 40.320 ordenaciones, obtiene 19.446 candidatos diferentes, conserva 79 en la cara excepcional y selecciona un registro:

\[
K=(234,543,140,729,659,824,621,058,914,794,146,601).
\]

El valor esperado aparece en la conclusión de igualdad, no como entrada del selector. `regional_terminal_alpha` compone el registro seleccionado con la raíz analítica única y sus publicaciones a toda profundidad. El repertorio terminal sigue siendo una interfaz explícita de esta formalización; sus documentos de procedencia se conservan en `historia/`. Esto describe exactamente el alcance del código adjunto, no una declaración de inexistencia matemática en el corpus.

El lector de incidencias completas permite recuperar los doce componentes. `WeightedIncidenceRecovery.lean` construye una carta de doce hexadas y su inversa racional, y demuestra la inyectividad del lector completo. Recuperar un registro desde sus lecturas y seleccionarlo desde sus antecedentes son dos operaciones compuestas en la documentación; la primera no se utiliza como sustituto de la segunda.

La ampliación `SelectedRegionalIncidence.lean` **ya compone la lectura aritmética y la incidencia del mismo registro seleccionado**. Su teorema `arithmetic_and_incidence_of_same_register` reúne la raíz única y las publicaciones de α a toda profundidad con la tétrada de bloques altos, la hexada del preacarreo negativo, el origen marcado y el retículo de rango 24, par, integral, autodual y de mínimo 4 alcanzado. Los lectores concretos son Kᵢ≥729 y Pᵢ+Eᵢ−Φᵢ−Kᵢ<0; no se reemplazan por soportes módulo tres. El recibo conserva sus doce teoremas comprobados y la evaluación nativa heredada del selector.

## Conservación evolutiva y recuperación

La conexión aritmética central continúa como

\[
(72,27)\longrightarrow(73,27)\longrightarrow(729,271).
\]

La primera operación incorpora la contribución de frontera; la segunda cambia de escala y transfiere una unidad entre coordenadas. `libro/03_refinamiento.tex` contiene las pruebas, el acarreo y su inversa; `libro/05_levantamiento.tex` contiene la elevación unitaria y la transformación de observables. El balance bilateral conserva la norma total y transporta los lectores con pesos 72/73 y 1/73 en el caso nonádico. La profundidad y los complementos archivados forman parte de la recuperación.

Estos textos se incluyen íntegros, junto con `libro/04_bilateral.tex` y su incorporación `libro/memoria_reducida_20260916.tex`. La relación con la incidencia excepcional y las realizaciones dimensionales permanece en `sections/excepcional.tex` y sus fuentes, incluidas las secciones de dualidad T y pantallas coordinadas. La lectura de κ_ag, la inversión de Hadamard, el recuperador y la conservación de información conservan así su posición dentro del artículo, no sólo su fórmula final.

## Jerarquía de la serie y alcance de esta entrega

La generación regional y el cierre del registro anteceden a las aplicaciones que los utilizan. El artículo X conserva la escala de acción, los caracteres de Planck, los ángulos, la sección electrónica, el funcional hexada–octada, área, entropía, gravitación y realizaciones electromagnéticas en sus lugares demostrativos. La repetición del núcleo en los artículos sectoriales tiene una función de autonomía, no introduce un origen distinto para cada sector. La relación con mezclas y demás aplicaciones se mantiene en sus fuentes propias y no se declara nuevamente formalizada por compilar los módulos de K.

Esta entrega preserva **todas las fuentes del artículo X**, además de la biblioteca Lean de referencia y los deltas focales. No sustituye ni modifica los artículos I–IX ni los PDF entregados. El lector no debe inferir de un control de archivos una certificación integral de todos los resultados matemáticos o físicos de la serie.

## Reproducción desde esta carpeta

Con Python 3 y su biblioteca estándar:

```sh
python3 -I -S reproducir.py --check
python3 -I -S reproducir.py --n69
```

El primer control coteja huellas, fuentes incluidas y dependencias locales. El segundo genera las cien firmas antes de abrir el CSV histórico de comparación y verifica sus 1.100 campos. Las implementaciones HMT que utiliza residen en esta misma carpeta; el CSV es testigo posterior.

Para volver a compilar la cadena regional–terminal, los módulos de incidencia y su composición sobre el mismo registro, con Lean 4.21.0 y Mathlib del commit `308445d7985027f538e281e18df29ca16ede2ba3`:

```sh
python3 -I -S reproducir.py --lean --mathlib /ruta/a/mathlib4 --lean-binary /ruta/a/lean
```

El verificador unificado reutiliza únicamente cachés que satisfacen sus comprobaciones de huellas. La primera ejecución compila toda la clausura local. Mathlib, Lean y los paquetes tipográficos son dependencias de ejecución externas, no datos HMT externos. Los recibos originales se conservan y la nueva compilación escribe su propio resultado en `resultados/lean_unificado/`. El modo `python3 -I -S verificar_lean.py --root . --plan` comprueba las fuentes y su clausura sin compilar y guarda un recibo de planificación separado.

Los certificados regionales y los dos módulos locales de incidencia utilizan los axiomas fundacionales declarados de Lean. La enumeración del selector terminal utiliza `native_decide` y declara `Lean.ofReduceBool`. Los recibos mantienen esta distinción. Se conservan las verificaciones incrementales originales; la entrega no las renombra como reconstrucción limpia de toda la biblioteca.

## Procedencia y conservación

La arquitectura central y la ley de conservación son `ARQUITECTURA_AUTORAL_PREEXISTENTE`; la reunión de sus fuentes es `RESULTADO_RECUPERADO`; las nuevas formalizaciones y sus compilaciones se identifican en cada recibo como certificados focales. Los alias históricos siguen presentes para localizar sus propietarios, pero el texto de entrada utiliza los nombres matemáticos definidos arriba.

Las observaciones recientes del autor se conservan literalmente en `APORTACIONES_AUTORALES_INTEGRAS.md`. El manifiesto fija el estado de esta entrega; los cambios posteriores de otros equipos no se incorporan sin comprobar de nuevo sus fuentes y recibos.
