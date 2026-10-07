# Controles ejecutados y límites de esta entrega

Los resultados de ejecución siguientes fueron obtenidos por los revisores
auxiliares y comunicados al editor principal durante esta revisión. Se
registran aquí para no repetir campañas innecesariamente. Ninguna salida se
presenta como certificado del manuscrito entero.

## Primos y zeta

Directorio de trabajo:
`/Users/ruben/Documents/New project/output/APERTURAS_PAPER_RESTAURADAS_20260911_REV03/PRIMOS_Y_ZETA_COMPLETO`.

| Control | Comando | Resultado |
|---|---|---|
| Schur normal | `/usr/bin/python3 -B ampliacion/expediente/verificar_schur_ventana_nonadica.py` | PASS_SCHUR_FIXED_WINDOW_ONE_NINTH, 21 controles |
| Schur optimizado | Igual con `-O -B` | Mismo resultado |
| Memoria normal | Python bundled 3.12.14 con `-I -S -B ampliacion/expediente/verificar_momentos_memoria.py` | PASS_IDENTIDADES_RACIONALES_LOCALES, 1046 |
| Memoria optimizada | `/usr/bin/python3 -I -S -O -B ampliacion/expediente/verificar_momentos_memoria.py` | Mismo resultado, Python 3.9.6 |
| Expectativas | `runpy.run_path("ampliacion/expediente/verificar_expectativa_modos.py")["verify"]()` | 25/25 |

No se usó `--receipt` ni se escribieron fuentes. El primer intento de
Schur con Python aislado no encontró mpmath; los PASS corresponden al
entorno de usuario existente, sin instalar dependencias nuevas.

Intervalos comunicados por Schur:

- η: [1.00363976543713133046770653887330656,
  1.00363976543713133046770653887356475].
- A: [0.97233071366517740170742868961608837,
  0.97672846173315715722008852411903876].
- Cota de ||B||²: [0.19926357337268538427867368394447755,
  0.19926357337268538427867368394447756].

Son las cotas utilizadas por la prueba de la ventana 1/9. No certifican
la positividad global de Weil.

## Gravitación

Directorio de las pruebas: la copia
`PRIMERA_ENTREGA/GRAVITACION/pruebas`.

Con Python bundled, una vez con `-I -S -B` y otra con `-O -I -S -B`,
se cargó `verificar_propagacion_bidireccional.py` mediante runpy con
nombre distinto de `__main__` y se llamaron:

`route_checks`, `transport_and_green_checks`, `hessian_checks`,
`absorption_checks` y `refinement_checks`.

Resultado en ambos modos:

```text
PASS_CONTROLES_FINITOS_PROPAGACION_BIDIRECCIONAL
count=4857
accion_de_rutas=4095
transporte_y_green=676
hessiano_y_fuentes_compactas=32
momentos_y_absorcion=51
refinamiento_y_control_negativo=3
```

También se cargó `verificar_rebote_polvo.py` mediante runpy.
Este programa ejecuta controles al cargar el módulo. Ambos modos dieron:

```text
PASS_REBOTE_POLVO_VII
exact_checks=3356
initial_amplitude_selected=false
```

No se ejecutaron los main ni se escribieron recibos. No seleccionan la
amplitud inicial ni constituyen una validación empírica de la cosmología.

## Fuente, conservación y parches

El editor principal ejecutó `auditar_fuentes.py` antes y después de los
cambios, materializó las diferencias con `materializar_delta.py` y
comprobó cada parche sobre su entrada exacta mediante `git apply --check`.
Los dos parches se aplican sin conflicto según esa comprobación de sólo
lectura; no se aplicaron sobre los originales.

El inventario recoge inclusiones, huellas, etiquetas, referencias, fórmulas
separadas y marcadores de enunciado. Las referencias bibliográficas incluyen
las redirecciones locales `HMTSetCite`, que no son entradas bibitem
ausentes. No se encontraron remisiones nuevas sin destino.

La revisión independiente de los nueve archivos de zeta no detectó
regresiones de signo, dominio ni alcance en el diccionario Mellin y la
distinción de representaciones. La revisión de VII detectó una colisión
de P_− en una propuesta intermedia; el editor la corrigió usando el autovalor
del bloque sin reutilizar aquel símbolo. Las diferencias de etiquetas fuera
del núcleo se registran expresamente.

## No realizado

- Recompilación de PDF, recuento nuevo de páginas y QA visual del corte modificado.
- Emisión o reutilización de un PASS_HMT_MD_PRECOMPILE para las nuevas huellas.
- Aprobación autoral de las modificaciones o promoción de afirmaciones globales.
- Campaña integral de los ocho artículos y de todos sus catálogos.

