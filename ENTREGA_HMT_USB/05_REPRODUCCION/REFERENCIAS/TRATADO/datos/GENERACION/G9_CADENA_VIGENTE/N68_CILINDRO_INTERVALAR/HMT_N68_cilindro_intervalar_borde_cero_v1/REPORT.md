# N68 - Cilindro intervalar, borde cero y supervivencia

## Correccion matematica

El test correcto para un prefijo ternario no es:
floor(1000^K N / 3^L) = D.

Ese test usa solo el extremo inferior del cilindro y pierde casos de borde/carry.

El test correcto es interseccion de cilindros:
[N/3^L, (N+1)/3^L) intersects [D/1000^K, (D+1)/1000^K).

Equivalente:
N*1000^K < (D+1)*3^L
(N+1)*1000^K > D*3^L

## Resultado

Auditado t=5..20 con cilindros intervalares.
Todos los bloques reales entran en sus soluciones intervalares: True

Conteo de dictamen:
{'unique local': 13, 'survival selects': 3}

Los valores t donde el extremo inferior fallaba pero el cilindro intervalar funciona:
[20]

## Stutter

t=21 es un stutter de K: no entra nueva triada decimal. Se audita aparte por firma-only.
 t  K      actual_solution  signature_only_solutions  actual_in_signature_only column_option_sizes      q      a      c   colw dual   r                                                                                          note
21 20 221022|020100|211021                         5                      True         2,1,2,2,2,2 122110 000101 110011 232122  200 001 t=21 is a K-stutter/no new decimal triad; signature-only test avoids 729^3 interval cylinder.
22 21 201100|001211|101021                         2                      True         2,1,1,2,2,2 000002 101020 101110 203222  020 122 t=21 is a K-stutter/no new decimal triad; signature-only test avoids 729^3 interval cylinder.

## Lectura HMT

Este es el formalismo de borde:
- el bulk protege informacion por cola/carry;
- el cero de corona no es nueve activo;
- la supervivencia no se lee desde el extremo inferior, sino desde el cilindro completo.
