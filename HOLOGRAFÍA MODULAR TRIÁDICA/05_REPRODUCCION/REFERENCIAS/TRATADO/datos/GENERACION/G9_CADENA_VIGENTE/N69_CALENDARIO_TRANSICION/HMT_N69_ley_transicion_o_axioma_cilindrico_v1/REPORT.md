# N69 - Ley de transicion o axioma cilindrico

## Qué se ejecutó

1. Se generaron firmas t=0..99 de pi,e,phi.
2. Se derivó el calendario mecanico K(t)=floor(6(t+1)log_1000 3).
3. Se probaron leyes afines globales y con fase para B_t y firmas.
4. Se formalizó el protocolo coinductivo de frontera.

## Resultado

Stutters iniciales:
[20, 42, 64, 86, 108]

Gaps:
[22, 22, 22, 22]

Los tests afines no dan una ley autónoma robusta. Por tanto el siguiente blanco sigue siendo:
F_HMT(B_t, cilindro_t) -> firma_(t+1).

Si no se deriva, debe formularse como axioma/coinductive verification protocol, no como teorema.

## Recomendación

Seguir intentando la generación infinita, pero con disciplina:
- Teorema ya probado: calendario K y criterio cilíndrico.
- Evidencia fuerte: frontera + supervivencia.
- No probado: transición autónoma de firma.
