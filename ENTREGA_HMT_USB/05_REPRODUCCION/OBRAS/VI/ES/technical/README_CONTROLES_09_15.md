# Controles reproducibles de las secciones09 y15

Estos dos programas de biblioteca estándar preservan los controles finitos realizados durante la reunión de dependencias. No son los gates canónicos del corpus y no certifican autosuficiencia global, metrología ni generación del libro completo de E108. Cada recibo conserva la huella del programa y de la sección presente al ejecutarlo.

## Ejecución ordinaria

Desde la raíz del ArtículoVI:

```sh
python3 -I -S technical/verificar_controles_dependencias_09.py
python3 -I -S technical/verificar_controles_historias_15.py
```

Se generan respectivamente `RECIBO_CONTROLES_DEPENDENCIAS_09.json` y `RECIBO_CONTROLES_HISTORIAS_15.json` en `technical/`. También se admite `--root /ruta/al/articulo` y `--receipt /ruta/recibo.json`; los programas no dependen de las rutas históricas de los artículos anteriores.

## Alcance matemático

- **09:** enumeración de729ternasAPP³; matriz de incidencia; cardinales de fibras; base completa de nueve autovectores racionales; norma cuadrada3/16 y bloque de Clifford; reconstrucción deK desde sus25coordenadas publicadas; ΠH y Hadamard; producción de la trayectoria central por la recurrencia de108pasos; desacuerdos, correlaciones y coincidenciaKD=KΩ=(80,54,6); desigualdades enteras de la década deφα16 a partir de los encierros explícitos.
- **15:** etiquetas y entornos de la fuente;729triples del cociclo;11664productos de fase/memoria enC108; un testigo finito de indicadores y precomposición unital. Las demostraciones generales de asociatividad, límites y evaluación están en el texto y no se presentan como resultados de una enumeración finita.

Las listas b90,b120,Q de09 son entradas publicadas de la prueba inversa. El programa no pretende que ésa sea la dirección que produce el libro anterior. La huella del TeX identifica la versión de trabajo vinculada al control; no convierte el cálculo independiente en una comparación semántica automática de cada frase del manuscrito.

## Controles con optimización

No se usa `assert`: cada condición llama a `require` y genera una excepción explícita si falla. Se han ejecutado también:

```sh
python3 -I -S -O technical/verificar_controles_dependencias_09.py --receipt technical/RECIBO_CONTROLES_DEPENDENCIAS_09_OPTIMIZADO.json
python3 -I -S -O technical/verificar_controles_historias_15.py --receipt technical/RECIBO_CONTROLES_HISTORIAS_15_OPTIMIZADO.json
```

Las cuatro ejecuciones resultaron satisfactorias. Un control posterior verificó por el árbol sintáctico la ausencia de instrucciones `assert`, comprobó bajo `-O` que `require(False,...)` levanta `ValueError`, y comparó íntegramente los objetos `controls` de las ejecuciones normal y optimizada: fueron idénticos. Los recibos conservan respectivamente `python_optimization=0` y1.

Los estados de éxito son `PASS_CONTROLES_FINITOS_DEPENDENCIAS_09` y `PASS_CONTROLES_FINITOS_HISTORIAS_15`. Ante una condición fallida se guarda el estadoFAIL correspondiente y el proceso termina con código1. Ninguno equivale a unPASSde cierre del artículo.
