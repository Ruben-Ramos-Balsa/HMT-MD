# N71 - Selector de pares (u,delta) por frontera

## Qué se ejecutó

A partir de N70, para cada canal se generan todos los pares (u,delta) compatibles con la transición exacta de cilindro.
Luego se acoplan los tres canales por firma de frontera:
(q,a,c,colw,rho_W,r).

## Resultado

Auditado t=5..25.
La rama real aparece siempre dentro del selector:
actual rows in selected = True
actual delta in selected = True

Conteos de dictamen:
{'survival selects': 11, 'ambiguous': 7, 'unique': 3}

## Importante

El selector por firma no siempre es unico. La supervivencia al siguiente cilindro reduce ambiguedades en varios casos, pero no se convierte aqui en una ley autonoma universal.

Los selectores por metrica de un solo canal fallan.

## Estado

Esto convierte N70 en selector acoplado de pares (u,delta), no solo en dinamica de cilindro.
Pero la pieza fuerte que falta sigue siendo la transicion autonoma de firmas.
