# Modelo de exposición: normalización bidireccional de la incidencia pentagonal

## Residencia del fragmento

Este texto constituye un modelo de redacción para la sección CKM del futuro tratado. Su posición es posterior a la generación de las palabras regionales, su codificación de incidencia, la selección del soporte pentagonal y la construcción de las coordenadas angulares. El comienzo del tratado seguirá siendo la construcción de APP y sus operaciones; este fragmento no adelanta CKM como fundamento.

Se conserva la arquitectura autoral del semicuadrado y se recupera su formalización orbital ya escrita. La fuente es [08g_normalizacion_bidireccional.tex](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_ARGUMENTAL_APERTURAS_CIERRES_20260915/II/manuscript_es/sections/08g_normalizacion_bidireccional.tex:1>).

## Autocruce e inversión de los pares orientados

La incidencia pentagonal proporciona un soporte P de cinco posiciones. Una vez construido este soporte, su autocruce reúne todos los pares ordenados de posiciones. El orden forma parte del dato: el par (x,y) distingue la posición de partida de la posición de llegada. La inversión bidireccional intercambia esas dos posiciones y define una involución sobre P × P.

Esta operación tiene dos comportamientos. Si las posiciones son distintas, el par (x,y) y su inverso (y,x) forman una órbita de dos elementos. Si coinciden, el par (x,x) permanece fijo. Los veinticinco pares ordenados se distribuyen, por tanto, en diez órbitas de dos elementos y cinco órbitas de un elemento.

La lectura normalizada conserva esa diferencia. A cada órbita le asigna el inverso del número de simetrías que dejan fijo uno de sus representantes. Una órbita no diagonal tiene estabilizador trivial y contribuye una unidad. Una órbita diagonal tiene estabilizador de orden dos y contribuye media unidad. La respuesta de la inversión completa es

\[
10\cdot1+5\cdot\frac12=\frac{25}{2}.
\]

El factor un medio expresa así el tratamiento de los puntos fijos dentro de la operación bidireccional. Su aparición está ligada a una acción definida sobre un soporte previamente producido, con una regla de lectura explícita.

## Demostración de la medida orbital

Para un soporte finito de cardinal p, hay p pares diagonales y p(p−1) pares no diagonales. Los primeros forman p órbitas fijas; los segundos forman p(p−1)/2 órbitas libres. Al sumar sus pesos se obtiene

\[
\frac{p(p-1)}2+\frac p2=\frac{p^2}{2}.
\]

La misma identidad se deduce directamente de órbita–estabilizador: el peso de cada órbita es su número de elementos dividido por dos. Al sumar las órbitas se recupera la mitad del cardinal total de P × P. La especialización p=5 produce 25/2.

Esta lectura debe distinguirse del conteo de clases. El conjunto ordinario de órbitas contiene quince elementos. La medida orbital vale 25/2 porque registra además los estabilizadores. Son dos evaluaciones distintas de una misma acción, y la normalización sectorial utiliza la segunda.

## Incorporación al sistema angular

La regla del canal 23 combina la coordenada de acción correspondiente con la contribución orientada del autocruce. En la carta del manuscrito se expresa como

\[
\theta_{23}=7u-\frac{25}{2}d.
\]

Aquí u y d son las coordenadas ya generadas y transportadas a esa carta. El entero 7 identifica el pivote orientado definido en la incidencia anterior. La contribución 25/2 corresponde a la medida del autocruce recién calculada. La posición de cada término y su signo forman parte del sistema sectorial que se expone junto a los otros dos canales.

La explicación completa enlaza, por consiguiente, tres hechos: la construcción del soporte, la normalización de su inversión y la acción del funcional angular. Conservar los tres permite justificar la fórmula sin reducir su origen a una coincidencia entre números pequeños. La independencia del marco admitido y la recuperación de coordenadas se demuestran a continuación sobre la carta completa.

## Regla de estilo que se extrae del ejemplo

El lector debe poder reconstruir la operación antes de encontrar su nombre especializado. La denominación «cardinalidad de un grupoide de acción» resume exactamente la construcción anterior, pero no reemplaza la exposición de los pares, la inversión, los estabilizadores y sus pesos.

Este modelo se aplicará también al residuo y el acarreo, a los levantamientos ternarios, a la selección regional, a la recurrencia de K y a la continuación nonádica. Cada capítulo conservará el mecanismo que determina sus coeficientes, la demostración pertinente y el enlace con el siguiente resultado.
