# El patrón 1828·1828 en la genealogía de e

Localización y reproducción focal — 22 de septiembre de 2026.

## Residencia documental

El desarrollo está en el capítulo 15, sección 15.1, páginas impresas 310–313 de la [monografía del cristal temporal aperiódico](</Users/ruben/Documents/New project/output/DOBLE_PROYECCION_HOLOGRAFICA_CRISTAL_TEMPORAL_APERIODICO_MONOGRAFIA_AUTOSUFICIENTE/output/pdf/DOBLE_PROYECCION_HOLOGRAFICA_DE_UN_CRISTAL_TEMPORAL_APERIODICO_MONOGRAFIA_AUTOSUFICIENTE.pdf>).

La fuente efectivamente ensamblada es `manuscrito/flattened/main_autosuficiente.tex`; la firma está en las líneas 39032–39045. Las etiquetas del AUX `manuscrito/build_flat/main_autosuficiente.aux` fijan la selección en p. 310, el censo y la proposición 15.3 en p. 311 y el teorema 15.4 sobre memoria en p. 312.

En el integral de referencia, el propietario está en:

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/pi_e_phi/U013_biografia_estructural_e_body.tex`.

Localizadores por líneas: selección orbital 37–63; elevaciones 65–81; firma 83–95; censo y unicidad 99–137; estados y memoria 141–208. La residencia común `colaboracion/partes_i_ii/source/base_residencias/base_c09_sin_encabezado.tex` conserva las mismas operaciones y la firma en 746–760. El propietario `manuscrito/sections/hmt/06d_biografias_numeros_rev6.tex`, sección sobre e, reúne su significado funcional.

## Selección y elevación anteriores a la lectura decimal

El texto selecciona la emisión 201101 por el predicado orbital conjunto: fibra de tamaño 1, multiplicidad 144, soporte diagonal {0,3,6}, censo trítico (2,3,1), diagonal 6 y orientación ES. La proposición declara la unicidad dentro del catálogo de 243 emisiones visibles y 43 órbitas. El censo y la procedencia APP–TRIT–TPK son antecedentes del pasaje, no una selección mediante los decimales de e.

El calendario de elevación L0, L0, L1, L1 produce:

    201101 | 121221 | 102011 | 012222 | 102011

Las mismas matrices y el mismo calendario están declarados para las tres emisiones regionales de π, e y φ; las semillas y los estados regionales se conservan distintos. La frontera siguiente de e, recogida en el manuscrito, es 021222. Esta consulta no vuelve a certificar la generación infinita ni la selección de todo el catálogo.

## Comprobación exacta del paso a cifras

He reproducido las cuatro elevaciones módulo 3 desde 201101, leyendo únicamente las matrices literales del programa propietario. Después se forma el entero N de la cadena trítica y el cilindro semiabierto [N/3^L,(N+1)/3^L). La lectura se realiza sobre la parte fraccionaria; la carta del canal añade 2.

Las cifras estables en todo el cilindro son:

- 6 trits: 2.71…
- 12 trits: 2.71828…
- 18 trits: 2.7182818…
- 24 trits: 2.7182818284…
- 30 trits: 2.71828182845904…

La prueba de estabilidad utiliza divisiones enteras: el mínimo y el máximo prefijo decimal de los extremos del cilindro coinciden. No se utiliza una expansión tabulada de e ni una suma factorial para escoger los bloques.

Con 24 trits se obtiene N=202864003874 y 3^24=282429536481. Su cilindro ya fija las dos copias de 1828 y la cifra 4 que sigue. Por tanto, la repetición decimal completa queda determinada antes de incorporar el quinto bloque trítico.

Con 30 trits se obtiene N=147887858824447 y 3^30=205891132094649. La lectura de doce decimales es:

\[
718281828459=7\,\underbrace{1828\,1828}_{\text{cuadrado posicional}}\,459.
\]

El programa [reproducir_prefijo_e_1828.py](reproducir_prefijo_e_1828.py) y su [salida](RESULTADO_PREFIJO_E_1828.json) conservan esta reproducción. El valor 1828 se extrae después de emitir la cadena; no interviene en las elevaciones.

## Qué significa estructuralmente el episodio

La fuente distingue dos hechos relacionados dentro de una misma trayectoria, pero de tipos diferentes.

Primero, el prefijo decimal contiene un cuadrado de longitud 4 situado después de una cifra. El censo publicado examina las 243 lecturas: registra únicamente dos cuadrados de longitud 4. El otro es la concatenación 5751|5751, situada al comienzo de 575157518472. La posición distingue al episodio de e. No he repetido aquí ese censo completo; he reproducido las elevaciones y el lector del canal concreto.

Segundo, en el registro ternario reaparece 102011 en las posiciones 3 y 5. Sus preestados módulo 27 son (25,11,7,17,8,16) y (7,8,4,23,26,7); los cocientes posteriores son (6,13,9,2,13,1) y (15,0,3,19,23,25). Se conserva el valor del bloque visible, pero no el estado que lo produce.

Esto aporta un caso concreto, ya documentado por Rubén, de repetición visible con genealogía diferenciada. La reiteración local del decimal tampoco impone una repetición infinita: una tercera copia de 1828 empezaría por 1 y la continuación producida empieza por 4.

La repetición 1828|1828 no se identifica directamente con B3=B5: los bloques pertenecen a bases y cortes distintos. El lector de cilindros enlaza la cadena trítica con las cifras. Que el patrón decimal ya esté fijado a 24 trits impide atribuirlo exclusivamente a la reaparición del quinto bloque. La explicación causal debe conservar las elevaciones anteriores completas y el estado, tal como exige la lectura HMT.

## Consecuencia para la investigación en curso

Este ejemplo proporciona material más específico que la afirmación genérica de que existen algoritmos para calcular e. Hay un selector interno anterior a las cifras, una elevación común de regiones, una firma decimal localizada y un retorno visible con memoria distinta. Esos objetos concretos deben formar el punto de partida de la discusión comparativa.

También corrige la prioridad de mi propuesta anterior: el corpus ya ofrece pares de estados con igual bloque visible y memoria diferente. La siguiente investigación debe partir de ellos y de sus operadores efectivos, no plantear su existencia como una búsqueda abstracta desde cero. Para contrastar respuestas bajo una misma continuación hay que conservar también las fases y cartas: este pasaje no autoriza a atribuir toda diferencia futura exclusivamente a la memoria.

Estatuto: resultado autoral recuperado; reproducción focal adicional de elevaciones y lectura. No se afirma prioridad histórica universal ni se sustituye la demostración de profundidad arbitraria por un prefijo finito.
