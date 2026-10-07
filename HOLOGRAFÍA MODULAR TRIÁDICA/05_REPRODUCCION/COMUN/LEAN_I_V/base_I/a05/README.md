# Continuación del mismo retículo: parte par y sector torcido

## Punto de partida conservado

El corte anterior es `PAQUETE_ARTICULO_I_VERTEX_CONFORME_20260921`: conserva
2.228 archivos y autentica 354 módulos Lean. No se vuelve a elegir K, la marca
de Witt, el retículo, el cociclo ni la correspondencia estado–campo. El origen
APP–TRIT–TPK → estado enriquecido → estructura discreta conjunta del continuo
y su selección conjunta excepcional y temporal permanecen íntegros en los
antecedentes. Los operadores que se construyen aquí son realizaciones
posteriores sobre ese mismo retículo; no reemplazan la generación por una
entrada convencional.

La cadena escrita se consulta en el artículo I,
`sections/excepcional.tex`, apartado «El álgebra de operadores de vértice y el
Monstruo». Allí se construye el álgebra reticular, se introduce el módulo
torcido de la negación y se aplica el teorema clásico de
Frenkel–Lepowsky–Meurman. El artículo distingue expresamente esa aplicación de
una nueva demostración del teorema clásico. Esta continuación implementa
operaciones de esa construcción; no declara desconocida su presencia en el
LaTeX ni vuelve a abrir la selección anterior.

## Construcciones efectivas añadidas

1. **Productos de la parte par.** `LatticeEvenProducts` transporta las dos
   sumas residuales puntualmente finitas por la inclusión del subespacio fijo.
   Prueba que el campo del estado producido coincide con el producto residual
   para todo índice entero, conservando ambos órdenes de composición.
   No recibe esa compatibilidad como hipótesis.
2. **Graduación de la parte par.** `LatticeEvenGrading` usa el proyector par
   ya existente, demuestra que preserva cada peso y proyecta la descomposición
   completa del portador. Cada peso es finito, los pesos no negativos generan
   todo el subespacio fijo y los coeficientes tienen el peso demostrado.
3. **Osciladores semienteros.** `LatticeHalfIntegerHeisenberg` conserva la
   misma álgebra simétrica y el mismo emparejamiento reticular. Reindexa las
   frecuencias por `m+1/2` y normaliza las derivaciones heredadas. Sus
   conmutadores se deducen de esas operaciones, no de un axioma de
   representación. `LatticeHalfIntegerField` construye el campo Laurent
   genuino en la coordenada ramificada `z=t²` y prueba su truncación puntual.
4. **Cociente finito de la negación.** `LatticeTwistedFiniteQuotient` reduce
   las coordenadas del mismo cociclo módulo dos. Construye un homomorfismo
   sobreyectivo desde la extensión central reticular y prueba que su núcleo
   es exactamente el conjunto de desplazamientos `theta(a)*a⁻¹`.
   Se obtiene una equivalencia del cociente con el grupo finito de cardinal
   `2^(rango+1)`; el valor `2^25` usa el rango 24 ya probado del retículo.
5. **Centro del cociente.** `LatticeParityNondegenerate` deduce la no
   degeneración módulo dos de la autodualidad integral del mismo retículo.
   Si todos los emparejamientos de un vector son pares, su mitad pertenece
   al dual y por tanto al retículo. Con ello identifica exactamente el
   centro del cociente: son los dos elementos de la coordenada central.
6. **Representación conforme de los osciladores semienteros.** Los modos
   cuadráticos se construyen mediante las dos sumas normales puntualmente
   finitas, usando la inversa del mismo Gram. Sus conmutadores con todos
   los modos de Heisenberg se calculan antes de introducir el defecto
   conforme. El cálculo sobre el vacío en los índices `(1,−1)` determina
   el desplazamiento `rango/16`; el de `(2,−2)` determina el término central.
   La generación del álgebra simétrica por sus creadores convierte estas
   igualdades del vacío en igualdades de operadores. La energía anula el
   defecto fuera de resonancia; Jacobi fija la recurrencia cúbica y todas
   las resonancias. `LatticeHalfVirasoroRelations` concluye, para todos los
   índices enteros, las relaciones completas de Virasoro con carga central
   24 y peso del vacío `3/2`. Ni estas relaciones ni sus dos constantes se
   reciben como hipótesis.

El cociente es un grupo, no su representación irreducible. El álgebra
`C_epsilon[Lambda]`, el grupo finito anterior y el módulo finito del sector
torcido tienen tipos y funciones diferentes. Tampoco se identifica ese módulo
con la representación de `ZMod 9` conservada en otro desarrollo.
El portador de las relaciones semienteras es su álgebra simétrica de
osciladores; no se lo renombra como el módulo reticular torcido completo.

## Reproducción

`verify_orbifold_input.py` autentica los 354 módulos anteriores, incluidas sus
fuentes, objetos compilados y consultas de axiomas. Sólo compila el cierre
nuevo solicitado en las raíces `orbifold_input` y `twisted_sector`, y exige
axiomas ordinarios para todas sus declaraciones públicas. Un directorio de
resultados nuevo evita sustituir un recibo anterior. `--plan` sólo comprueba
rutas y dependencias; no equivale a compilación.

La aceptación conjunta ha concluido con `PASS_ORBIFOLD_INPUT_DELTA`:
17 módulos nuevos, 154 declaraciones públicas y 126 teoremas/lemas. Todas
las declaraciones nuevas dependen únicamente de `propext`, `Classical.choice`
y `Quot.sound`; no contienen `sorryAx` ni un axioma nuevo de Virasoro.
Los 354 módulos anteriores fueron autenticados sin recompilación. El recibo
integrado tiene SHA-256
`f3fc574feea5f73d2e7234e7386d651af5e81075a368044361b1b65e3634a095`.
Los recibos de preservación de archivos, las pruebas aritméticas ejecutables
y las pruebas comprobadas por Lean tienen alcances separados.

## Procedencia y alcance

Arquitectura: `ARQUITECTURA_AUTORAL_PREEXISTENTE` en la prolongación reticular
del artículo y su corpus. Pruebas Lean de estas operaciones:
`FORMALIZACION_NUEVA` y `CERTIFICADO_NUEVO`. La nueva formalización no atribuye
la construcción clásica de los osciladores o de FLM a un descubrimiento nuevo.

El álgebra reticular conforme y su parte fija no se identifican por definición
con el álgebra Moonshine. El producto de la extensión que incluye el módulo
torcido y la identificación de su grupo completo de automorfismos conservan
sus obligaciones matemáticas propias. Ninguna coincidencia de carácter o
cardinal se usa como sustituto de esas operaciones.
