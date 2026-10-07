# Restitución aritmética y calendario enriquecido

Este directorio formaliza la representación residual positiva del primer capítulo del tratado. La fuente utiliza únicamente `Std` de Lean 4.21.0, instalado localmente.

## Enunciados

Para un entero natural positivo `n`, se definen `rho9 n = (n-1)%9+1` y `q9 n = (n-1)/9`. Se demuestran la pertenencia del residuo a `1,…,9`, la identidad `n = rho9 n + 9*q9 n` y las dos recuperaciones de `r` y `q` cuando `1 ≤ r ≤ 9`.

Los tipos `Positive` y `Digit9` incorporan las condiciones del dominio. Las funciones `encode` y `decode` se componen en ambas direcciones con la identidad. Los teoremas `encode_injective`, `encode_surjective` y `encode_bijective` formalizan por tanto la biyección descrita en `thm:app-reconstruccion`.

## Reproducción

Desde la raíz de REV03, con Lean 4.21.0 disponible en `PATH`, en su instalación de Elan o mediante la variable `LEAN`:

```bash
python3 lean/check_lean_app.py
python3 lean/check_lean_calendar.py
```

La ejecución produce `lean/build/APPRestitution.olean`, conserva la impresión de axiomas en `lean/build/lean-output.txt` y escribe `metadata/RECIBO_LEAN_APP.json` con las huellas y el alcance de cada enunciado.

El primer control comprende diez declaraciones de restitución aritmética APP; el segundo, ocho declaraciones del calendario. Las formalizaciones son universales sobre los dominios declarados; los controles finitos de las tablas pertenecen a certificados distintos.

La clausura formal de 251 módulos se conserva aparte, en `propietarios/CAMPOS`, con sus programas, datos y recibos. El recibo de reproducción de esta edición está en `lean/CADENA/resultados/lean_unificado/VERIFICATION.json`: distingue módulos recompilados, caché validada y consultas de axiomas. Ninguno de estos controles declara formalizadas todas las páginas del tratado.
