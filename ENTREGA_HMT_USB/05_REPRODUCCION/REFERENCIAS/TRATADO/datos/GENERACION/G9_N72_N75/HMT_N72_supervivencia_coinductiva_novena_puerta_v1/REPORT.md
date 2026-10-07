# N72 - Supervivencia coinductiva y novena puerta

## Qué se ejecutó

A partir de N71, se tomó cada conjunto local de ramas seleccionadas por frontera y se evaluó supervivencia coinductiva a profundidad h=1..9.

Una rama sobrevive a profundidad h si puede extenderse h fronteras futuras siguiendo:
- transición exacta de cilindros,
- firma de frontera futura,
- acoplamiento de tres canales.

## Resultado global

{
  "total_t": 21,
  "local_unique_count": 3,
  "resolved_by_h1_count": 0,
  "resolved_by_h2_count": 11,
  "resolved_by_h3_count": 7,
  "unresolved_by_h9_count": 0,
  "max_resolution_depth": 3,
  "all_resolved_by_h3": true,
  "all_actual_survives_to_h9": true
}

Todas las ambigüedades auditadas t=5..25 se resuelven en profundidad <=3.
La rama real sobrevive hasta h=9 en todos los casos.

## Novena puerta

En t=9, K=9:
- ramas locales: 3
- supervivientes h1: 3
- supervivientes h2: 1
- supervivientes h9: 1

La novena puerta no crea una rama nueva: confirma la estabilidad del inverso límite.

## Estado

Esto fortalece el protocolo de frontera/supervivencia, pero sigue siendo auditoría finita. El siguiente paso teórico sería convertir supervivencia coinductiva en definición/teorema de número HMT.
