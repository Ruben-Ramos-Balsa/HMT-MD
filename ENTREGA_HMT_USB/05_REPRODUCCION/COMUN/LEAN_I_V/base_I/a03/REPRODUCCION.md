# Reproducción del incremento entregado

Esta carpeta y su ZIP contienen los mismos archivos. Descomprima el ZIP una
sola vez si utiliza esa presentación. Conectar un USB **no ejecuta nada**:
las órdenes siguientes se lanzan explícitamente desde una terminal situada
en esta carpeta.

```sh
python3 -I -S reproducir.py --plan --report-dir plan_nuevo
python3 -I -S reproducir.py --report-dir resultados_nuevos
```

La primera orden autentica fuentes, dependencias y objetos; no compila y no
equivale a demostrar. La segunda compila únicamente los 18
módulos nuevos del recibo y consulta sus 270
declaraciones públicas. Ambas reutilizan los 388 módulos anteriores después
de autentificarlos; no reconstruyen Mathlib. Use un directorio de resultados
nuevo para cada ejecución: los recibos originales quedan en `recibos/`.

El runtime externo debe ser Lean 4.21.0 y el checkout de Mathlib cuyo commit
figura en `recibos/incremento/VERIFICATION.json`, junto con su biblioteca y
dependencias ya compiladas. No se descarga ni instala software automáticamente.
En otra máquina se pueden indicar sus ubicaciones:

```sh
python3 -I -S reproducir.py --lean /ruta/bin/lean --mathlib /ruta/mathlib4 \
  --report-dir resultados_nuevos
```

`README.md` explica los resultados y su alcance. `lean/` contiene las nuevas
fuentes; `antecedente/` conserva íntegra la entrega anterior; el manifiesto
identifica cada archivo. El control documental causal, la preservación de
archivos y las comprobaciones Lean son controles distintos. Este ejecutor
reproduce las declaraciones enumeradas, no añade una afirmación de cierre
completo del producto orbifold, FLM o del grupo de automorfismos del Monstruo.
