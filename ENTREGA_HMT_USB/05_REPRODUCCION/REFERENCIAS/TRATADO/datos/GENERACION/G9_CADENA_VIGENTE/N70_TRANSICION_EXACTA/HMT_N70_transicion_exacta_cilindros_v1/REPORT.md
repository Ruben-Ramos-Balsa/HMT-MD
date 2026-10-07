# N70 - Transicion exacta de cilindros

## Resultado

El estado correcto no es solo B_t, sino el cilindro:
[N/3^L,(N+1)/3^L) junto al cilindro decimal [D/1000^K,(D+1)/1000^K).

Definimos:
A=N*1000^K-D*3^L
B=(N+1)*1000^K-D*3^L

Supervivencia:
A < 3^L and B > 0.

## Transicion exacta

Si dK=0:
A' = 729 A + u*1000^K.

Si dK=1:
A' = 729000 A + u*1000^(K+1) - delta*729*3^L.

B' = A' + 1000^(K+dK).

Verificado en pi,e,phi hasta t=35:
True

## Interpretacion

Esto ya no es heuristica. Es la ley exacta de arrastre/carry del cilindro.
Lo que queda no es la dinamica del cilindro, sino el selector de frontera que elige (u,delta).
