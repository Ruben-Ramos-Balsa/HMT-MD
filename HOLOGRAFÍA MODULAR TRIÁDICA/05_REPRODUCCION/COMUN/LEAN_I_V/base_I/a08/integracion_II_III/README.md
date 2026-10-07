# Entradas únicas de integración II–III — 21 de septiembre de 2026

Esta cápsula reúne **25 fuentes Lean idénticas a sus propietarios**, sus cinco
recibos de compilación anteriores y el mapa de imports para incorporarlas una
sola vez a la base central de 279 módulos. No crea otra implementación ni
modifica los paquetes anteriores. La ejecución focal posterior está cerrada
como se documenta en el apartado siguiente.

## Resultado focal vigente

`resultados_control_publico_20260921_02/VERIFICATION.json` registra
`PASS_25_COMPILACIONES_COBERTURA_PUBLICA_Y_HUELLAS_II_III`:

- 25 fuentes compiladas sin cambios, sobre 279 módulos autenticados reutilizados.
- 400 declaraciones públicas consultadas; las 212 consultas heredadas están
  incluidas. Cobertura completa y ningún axioma inesperado.
- Control público limitado a 300 segundos, terminado en 256,908 segundos
  contando también sus comprobaciones de identidad.
- `resultados_control_publico_20260921_02/CIERRE_HUELLAS.json` verifica los
  25 objetos nuevos, 55 imports resueltos (44 objetos únicos) y 728 rutas
  autenticadas. Ningún cambio de huellas; se efectuó un cotejo adicional final.
- Ningún módulo de la base ni Mathlib recompilado; ningún cambio matemático.

Las 25 compilaciones con `exit_code: 0`, comandos y logs están en
`resultados_integracion_279_25_20260921`. Su recibo general conserva `FAIL`
porque se interrumpió una sonda posterior demasiado amplia de los auxiliares
del entorno. No fue un fallo de compilación ni una refutación matemática y no
se convierte ese recibo interrumpido en `PASS`. La sonda original y el runner
permanecen intactos. El intento `resultados_control_publico_20260921` se detuvo
antes de invocar Lean al comprobar el parser de secciones; el vigente es `_02`.

Comando único del **control final acotado**, reutilizando y autenticando las
25 compilaciones conservadas, sin recompilarlas; la salida debe ser nueva:

```sh
python3 -I -S -B control_publico_y_cierre.py \
  --compiled resultados_integracion_279_25_20260921 \
  --output resultados_control_publico_NUEVO
```

Ejecutarlo desde esta carpeta. No reconstruye los 279 módulos ni todos los
artículos. Los comandos exactos de las compilaciones ya ejecutadas están en
sus recibos. No repetir la sonda global interrumpida.

El punto de entrada es `MANIFIESTO_ENTRADAS.json`: `sources` identifica cada
fuente, huella y recibo; `possible_incremental_compile_order` da un orden
topológico; `direct_central_imports` resuelve los 12 imports directos a la base.
No se copian bibliotecas, binarios de la base ni los 14 módulos ya presentes e
idénticos; los 25 objetos nuevos se guardan sólo en los resultados focales.

## Compatibilidad comprobada

Base central:
`/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_COVARIANCIA_Y_FIRMA_20260920`.
Recibo central: `resultados/lean_unificado/VERIFICATION.json`, SHA-256
`019297aa9975b55fd817d51b4460558cfbaa2a058783f103c052fc8fb6d20f4d`.

Los seis adaptadores del 18 de septiembre conservan su pin original de 143
módulos, cuyo recibo tiene SHA-256
`3125044b176c5f1c1f595c25e2013491c9c596ea3bf8b47ce2d1a69f38bfb092`.
Los **143 nombres y huellas están íntegros en la base central de 279**; los
archivos centrales correspondientes se cotejaron materialmente. El manifiesto
enumera esa correspondencia, no sustituye el recibo antiguo por uno nuevo.

La unión de los dos suplementos del 18 y del dossier del 20 contiene 39 fuentes
únicas: 14 ya centrales y 25 adicionales. No se encontraron colisiones de nombre
con contenido diferente ni imports locales sin resolver. Las 25 fuentes copiadas
coinciden con sus respectivos `source_sha256` y `exit_code: 0` preservados.

El manifiesto de preparación conserva su estado **de fuentes e imports**; la
ejecución posterior 279+25 tiene el recibo separado identificado arriba. No
debe ejecutarse un runner antiguo ligado a base143 simplemente cambiándole el
nombre de carpeta. El integrador debe conservar el orden y las huellas y
reutilizar los objetos comprobados sin duplicar la biblioteca.

## Frontera de confianza: no restringirla a un namespace ajeno

Los recibos conservan `propext`, `Classical.choice`, `Quot.sound` y, por el
selector finito heredado, `Lean.ofReduceBool`. No se introducen axiomas nuevos.

En los tres módulos `Selected*` hay consultas que heredan `Lean.ofReduceBool`:

- `SelectedAngularBarbero`: las siete declaraciones consultadas, incluida
  `HMT.SelectedAngularBarbero.selected_action_incidence_functional`.
- `SelectedCKM`: `angular_input_bounds`, `jarlskog_positive`,
  `no_real_rephasing` y `selected_ckm_principal_chain`, bajo
  `HMT.II.CKM.Selected`.
- `SelectedJointCoupling`: las tres declaraciones consultadas bajo
  `HMT.SelectedJointCoupling`.

También heredan esta frontera declaraciones de los seis adaptadores
`ArticleIIFromSharedBase`, `ArticleIIIFromSharedBase`,
`ArticleIIIIISharedComposition`, `ArticleIIIDimensionalReading`,
`ArticleIICKMFromSharedBase` y `ArticleIIICatalanPellFromSharedBase`.
Los recibos contienen los nombres exactos; **no reutilizar una excepción de
axiomas limitada a `SelectedStateField`** ni convertir esta lista en aceptación
de cualquier declaración futura.

## Correspondencia editorial que motiva la incorporación

En la entrega `ENTREGA_SERIE_ARCHIVOS_REUNIDOS_20260919`, las unidades ES/EN
de II y III conservan sus índices Stage10. Se cotejaron 50 referencias fuente–
huella de II y 79 de III, sin discrepancias. Sus `PROOF_TARGETS.json`,
`PROOF_BINDINGS.json` y `MANIFEST_STAGE10.json` coinciden entre ES y EN.
Los dos PDF ES coinciden con sus huellas seleccionadas en `SOURCE_MAP.json`.
No se recompilaron ni se afirma una nueva comprobación visual.

Los seis adaptadores del 18 y los tres cierres seleccionados del 20 no están
incorporados como tales en esas unidades Stage10. Es una incorporación pendiente
de resultados existentes, no una ausencia de desarrollo matemático en los textos.
La coordinación previa lo registra en
`/Users/ruben/Documents/New project/output/IMPLEMENTACION_VOA_MOONSHINE_20260918/COORDINACION_II_III_20260918.md`.

Localizadores dentro de las unidades españolas:

- II: `documentacion_original/payload/manuscript_es/main.tex:57` inicia el
  núcleo común; `sections/05_accion.tex:55` contiene la década de acción;
  `sections/06_barbero.tex:60`, el funcional; el índice formal remite a
  `GeneratedActionDomain`, `ObservedBarbero` y `SchurResolventBridge`.
- III: `documentacion_original/payload/spanish_source/main.tex:52` y los
  archivos `manuscrito/INCLUIR_NUCLEO_I_REV02.tex:6` e
  `INCLUIR_DEPENDENCIAS_II_REV02.tex:80` conservan la herencia causal;
  `manuscrito/sections/04_respuesta_constitutiva.tex:140` contiene la
  inversión constitutiva; `06_pell_barbero.tex:87`, Catalán–Pell, y
  `06_pell_barbero.tex:312`, la expresión constitutiva orientada de Barbero.
  El índice formal remite a `GeneratedConstitutivePublication`,
  `ConstitutiveLCRecovery` y `PellTangentTripling`.

Alcance: correspondencia documental e integración focal preservativa II–III.
Ningún PDF, manuscrito, árbol central, biblioteca o contrato rector fue editado.
