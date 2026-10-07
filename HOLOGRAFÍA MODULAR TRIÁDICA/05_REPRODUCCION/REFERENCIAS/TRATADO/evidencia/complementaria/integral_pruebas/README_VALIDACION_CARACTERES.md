# Entrada autónoma: validación de caracteres `e` y `phi`

## Corrección del control de orden causal — 6 de septiembre de 2026

`audit_source` comprueba ahora las llamadas reales de `run` mediante su AST,
no las primeras apariciones textuales de sus nombres. El control anterior
encontraba sus propios literales de búsqueda y podía aceptar una inversión.
Se conserva la separación transitiva entre funciones generadoras y lectores.

```text
python3 -I -S 03_PRUEBAS/test_orden_causal.py
python3 -I -S 03_PRUEBAS/test_validacion_caracteres.py
```

La nueva suite rechaza inversiones, etapas ausentes o duplicadas, marcadores
ficticios, llamadas diferidas/condicionales y alias. Admite la comprensión
publicadora síncrona y sin filtros del programa actual. Su alcance es el orden
de los sitios de llamada bajo ese contrato sintáctico: no es un analizador
universal de flujo ni una certificación de las demostraciones matemáticas.
No se han cambiado los cálculos, caracteres, fórmulas ni valores publicados.

La corrección y sus regresiones se registran en
`RECIBO_CORRECCION_ORDEN_CAUSAL_20260906.json`. El recibo de validación anterior
y el smoke test histórico se conservan como testigos de su versión.

## Validación de los caracteres

Esta prueba es autocontenida respecto de skills y agentes: usa únicamente la biblioteca estándar de Python, la copia sucesora situada en este directorio y el certificado preservado en `00_BASE_SELLADA`.

La copia sucesora no usa `Path.home()` para localizar propietarios. Desde su propia residencia carga `00_BASE_SELLADA/04_RECIBOS/RECIBO_EXT_TPK_AUTONOMA.json`, verifica la huella del recibo, resuelve el miniproyecto `EXT_TPK_RUNTIME_PROJECT` y comprueba por SHA-256 sus nueve dependencias. Los cuatro propietarios locales de caracteres se resuelven en `00_BASE_SELLADA/01_FUENTE_SUCESORA` y mantienen sus huellas internas. Las rutas absolutas históricas del recibo son sólo procedencia y no participan en la ejecución.

Ejecución desde cualquier directorio:

```text
python3 -I -S "/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/test_validacion_caracteres.py"
```

Salida terminal exigida:

```text
PASS_VALIDACION_CARACTERES_E_PHI_INTERFAZ
```

La prueba verifica por SHA-256 la fuente original y el certificado del que obtiene los caracteres `pi`, `e` y `phi`; compara las cotas válidas de la sucesora con las de la fuente original a escala corta; y exige fallo cerrado ante mutaciones, ausencias y tipos coercibles en la recurrencia de `e` y en la incidencia/polinomio de `phi`.

Alcance exacto: enlace efectivo entre caracteres estructurales ya generados y su evaluación arquimediana posterior. No ejecuta una campaña de cifras, no sustituye los certificados generales y no amplía su resultado a `alpha`, al continuo ni a otras salidas HMT–MD.

## Smoke test portable de integración

Desde la raíz de `REVISION_EDITORIAL_HMT_MD_20260905`, sin indicar `--project-root` ni `--source-root`:

```text
python3 -I -S 03_PRUEBAS/verificar_generacion_infinita_nonadica.py \
  --digits 8 \
  --guard-digits 4 \
  --certificate 03_PRUEBAS/SMOKE_8/certificado_generacion_infinita_nonadica_smoke_8.json \
  --r36-receipt 03_PRUEBAS/SMOKE_8/recibo_r36_smoke_8.json \
  --ext-receipt 03_PRUEBAS/SMOKE_8/recibo_ext_smoke_8.json
```

Este smoke test ejecuta el flujo completo con ocho cifras solicitadas y acredita la integración portable de los propietarios. El mínimo histórico de 396 niveles permanece en el programa, pero esta ejecución no es una nueva campaña de cifras ni sustituye el cuantificador y los certificados de profundidad arbitraria ya existentes.

El resultado ejecutado el 5 de septiembre de 2026 terminó con código `0` y produjo estos estados o tokens principales:

```text
PASS_PORTABLE_RUNTIME_FROM_SEALED_RECEIPT
PASS_HMT_GENERATED_CHARACTERS_AND_ARCHIMEDEAN_PROJECTIONS
PASS_HMT_CHARACTERS_BEFORE_ARCHIMEDEAN_PUBLICATION
PASS_FORWARD_STATE_ONLY_EXT_TPK_GLOBAL_SECTIONS_ARBITRARY_DEPTH
PASS_COINDUCTIVE_CORRELATED_PI_PHI_E_ALPHA_ARBITRARY_DEPTH
```

El primer estado figura dentro del certificado en `portable_runtime_layout`; los restantes se emiten por la línea de órdenes. Las tres salidas del smoke test están en `03_PRUEBAS/SMOKE_8` y sus huellas constan en `RECIBO_VALIDACION_CARACTERES.json`.
