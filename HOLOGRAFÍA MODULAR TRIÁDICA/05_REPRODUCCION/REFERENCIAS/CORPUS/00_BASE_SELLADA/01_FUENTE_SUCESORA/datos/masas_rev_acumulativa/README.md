# Infraestructura acumulativa para la tabla completa de masas

Esta residencia sustituye como instrumento de trabajo a las ventanas abreviadas de diez o doce entradas. No las abre ni las usa como fuente de selección. Su dominio científico es el inventario completo de veintitrés clases y mantiene separados los cuatro niveles combinatorios de HMT:

- 81 posiciones de la carta;
- 56 familias de ruta;
- 13 multisecciones;
- 324 rutas orientadas.

## Regla causal

La fase estructural calcula primero, sin masas externas, la cadena

`clase física → posición/fibra → ruta → registro → (K_D,K_Omega) → firma → carácter/torre → operador`.

El payload estructural se congela antes de abrir el catálogo externo. La fase de contraste une cada fila mediante un `external_output_id` declarado; el valor PDG no selecciona rutas, celdas, firmas ni coeficientes.

## Salida electrónica y sectores nulos

La fila electrónica usa como resultado vigente

`m_e^beta = 0.5109989506900008086082571648… MeV/c^2`,

con ruta `(5,5,++)` y coincidencia exacta de ambos lectores en `(80,54,6)`. El valor no se fija por separado: el generador evalúa una sola expresión, `m_e^beta=m_e^(0)R_act^(80-54 alpha_HMT+6 Delta4)`, y exige igualdad exacta con la evaluación de la ruta nominal. El valor basal `0.510998922488… MeV` se conserva únicamente como etapa causal.

Fotón y gluones pertenecen a la carta nula: `m_HMT=0` y `kappa=N/A`. No se fabrican mediante `R_act^0`.

## Rutas nominales, carácter escalar y refinamientos de fibra

Ninguna especie se elimina ni se reduce al par operatorial. Para (e,\mu,\tau,u,d,s,c,b,t,W,Z,H), la ruta nominal CT--108 se fija antes de abrir el catálogo metrológico y publica:

- huella entera de 108 pasos, eje, hoja y residuo;
- firma angular `(n_A,s_C)` y devanados `W_+`, `W_-`;
- carácter adimensional y sección positiva de la ley de masas;
- posiciones, fibras y espectros de `K_D` y `K_Omega` cuando pertenecen al atlas 13.

El morfismo sabor--generación--ruta está cerrado en el dominio nominal recuperado; la masa no se usa para seleccionar la ruta. La tabla científica publica además los espectros adimensionales completos `R_act^(kappa_D-kappa_e)` y `R_act^(kappa_Omega-kappa_e)`. En (W,Z,H), la ausencia de una asignación adicional `K_D/K_Omega` no anula el carácter escalar nativo ya publicado por su ruta CT--108.

Las once evaluaciones elementales son evaluaciones exactas de firmas de rutas nominales. Las seis evaluaciones compuestas se mantienen tipadas por estado: el carácter evalúa exactamente una firma explícita, mientras el selector anterior de esa firma conserva su propio estatuto y nunca se sustituye por el valor externo.

No se elige ningún autovalor. El electrón, cuya fibra central tiene rango uno, conserva separadamente el paso absoluto `e_0 R_act^kappa_e`.

## Reproducción

```bash
python3 pruebas/generar_tabla_completa_masas_rev_acumulativa.py
python3 pruebas/generar_tabla_completa_masas_rev_acumulativa.py --check
```

El primer comando genera las tablas de los cuatro dominios internos, las vistas científica y pública, el resumen legible y el certificado. El segundo exige coincidencia byte a byte con el certificado almacenado.

## Artefactos

- `manifiesto_join_especies_hmt_sm.tsv`: unión explícita de las 23 clases.
- `salidas/tabla_completa_masas_hmt_sm.tsv`: tabla científica principal; sus columnas se ordenan desde la genealogía interna hasta el contraste externo.
- `salidas/tabla_comparativa_masas_compacta.tsv`: vista de diez columnas preparada para composición corporal, con rangos de los factores relativos dependientes de ruta.
- `salidas/tabla_comparativa_masas_publica.tsv`: vista académica en español de las 23 clases, con definición, salida HMT, contraste, estatuto y morfismo de realización.
- `salidas/tabla_comparativa_masas_publica.tex`: `longtable` de 23 filas para integración tipográfica; conserva los espectros dependientes de ruta y no selecciona autovalores mediante los valores externos.
- `salidas/atlas_celdas_81_con_lectores.tsv`: censo de posiciones.
- `salidas/familias_ruta_56_con_espectros.tsv`: censo de familias.
- `salidas/operadores_multiseccion_13.tsv`: espectros de operadores por multisección.
- `salidas/rutas_orientadas_324_con_lectores.tsv`: dominio orientado completo.
- `salidas/comparabilidad_fisica_23.tsv`: capa biyectiva de comparabilidad, con una fila para cada una de las veintitrés clases y su codominio nativo.
- `../../manuscrito/generated/tabla_masas_comparabilidad_fisica_23.tex`: tabla corporal de comparabilidad 23/23, sin escalarizaciones inventadas.
- `procedencia_firmas_condicionadas.tsv`: nombre histórico conservado por compatibilidad; contiene los once pares angulares de rutas nominales recuperadas y su estatuto positivo.
- `salidas/procedencia_firmas_condicionadas_evaluada.tsv`: evaluación digital de esas firmas, separada del contraste externo.
- `../../manuscrito/generated/tabla_masas_evaluaciones_firmas_explicitas.tex`: tabla corporal de once rutas elementales y seis firmas compuestas, sin aplanar sus estatutos.
- `salidas/tabla_comparativa_masas_resumen.md`: lectura compacta de las 23 clases.
- `../../certificados/tabla_completa_masas_rev_acumulativa.json`: hashes, gates y contrato epistemológico.

La razón de acción se lee del certificado interno `certificados/escala_accion_determinantal.json`; el generador verifica sus hashes y deriva `R_act=H5/etaRet` antes de abrir el catálogo metrológico.
