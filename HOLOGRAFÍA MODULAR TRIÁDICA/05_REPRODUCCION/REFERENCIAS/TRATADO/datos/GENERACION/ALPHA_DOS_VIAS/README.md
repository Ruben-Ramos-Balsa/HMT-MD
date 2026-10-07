# Alfa: significado auditable de «dos vías»

Este certificado separa tres afirmaciones que aparecen mezcladas en borradores
históricos:

1. El sello `K` se reconstruye exactamente tanto desde el observable Hadamard
   como desde `(D3K,D4K,Q)`.
2. Dados el sello, las tres palabras de entrada y la condición de borde, las
   doce triadas de alfa se evalúan exactamente por el acarreo dodecafásico de
   derecha a izquierda. Es un mapa condicionado, no una segunda procedencia
   upstream independiente.
3. El kernel E21/22 de vacancias da una raíz numérica independiente una vez
   fijados sus coeficientes; aquí se verifica la raíz, no se deriva el kernel.

El mismo programa verifica además las dos descripciones publicadas de la cara
`B_K`: corona alta del sello e intersección `H_e ∩ P_pi`. La reconstrucción de
estos soportes desde la matriz en el calibre correcto se hace de manera
independiente en `../M12_WITT/verificar_m12_witt.py`.

Ejecutar:

```text
python3 verificar_alpha_dos_vias.py
```

El resultado queda en `verificacion_alpha_dos_vias.json`.
