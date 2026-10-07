# Convención rectora de índices G9

Esta convención prevalece sobre cualquier uso ambiguo de `t`, `K` o “puerta”
en los documentos históricos.

## Estado, puerta y salida

Para cada paso distinguimos:

- `t`: índice cronológico del ledger;
- `K_before=K_t`: profundidad visible antes de atravesar la puerta;
- `u_t`: bloque ya presente en el estado de entrada;
- `G_K`: puerta o relación de transición desde ese estado;
- `u_next=u_{t+1}`: bloque emitido por la puerta;
- `delta_next`: tríada decimal nueva emitida;
- `K_after=K_{t+1}`: profundidad después de la transición;
- `phase_before=(K_before mod 9)`, con residuo cero leído como fase nueve;
- `phase_after=(K_after mod 9)`, con la misma convención;
- `stutter`: transición con `K_after=K_before`.

La notación matricial del paper es

`B_K=(u_K^pi,u_K^e,u_K^phi)`.

Por tanto, `B9` es un estado y la novena puerta es la flecha

`G9:B9→B10`.

No son el mismo objeto.

## Caso canónico de la novena puerta

Estado de entrada:

`B9=(100100,020112,010122)`.

Salidas localmente admisibles:

1. `(101222,112221,112002)` — salida real;
2. `(102221,111222,112002)` — espejo;
3. `(111221,102222,112002)` — espejo.

En las tres salidas:

`phi=112002`,  `pi+e=210110 (mod 3)`.

Perfil de supervivencia de N72:

`h0:3`, `h1:3`, `h2:1`, y la salida real sigue siendo la única hasta `h9`
en la ventana auditada.

La salida tiene `K_after=10`, luego `phase_after=1`. Esto es retorno de fase
con memoria, no reinicio del estado.

## Jerarquía documental

La cadena vigente es:

`N68 → N69 → N70 → N71 → N72 → N73 → N74`.

- N68: cilindros intervalares y borde cero;
- N69: calendario mecánico y stutters;
- N70: transición exacta una vez fijado el estado;
- N71: selector acoplado de pares;
- N72: supervivencia coinductiva finita;
- N73: orientación `pi/e`;
- N74: monodromía de nueve fases.

Los conteos N61–N67 basados sólo en el extremo inferior están superados por
la intersección intervalar N68. Pueden conservarse como historia, no como
datos vigentes.

## Alcance del verificador V2

`../G9_MONODROMIA/verificar_g9_monodromia.py` recalcula la lectura de las
doce tríadas desde los bloques, verifica las fases, los invariantes de espejo
y la coherencia de la selección `3→1` con los ledgers N72. Los ZIP N68–N74 no
incluían el programa original de enumeración; por ello los conteos de
supervivencia se tratan como testigos publicados, no como una enumeración raw
regenerada desde cero.
