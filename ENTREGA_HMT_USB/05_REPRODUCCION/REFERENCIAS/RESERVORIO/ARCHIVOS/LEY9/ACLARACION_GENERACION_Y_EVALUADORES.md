# Generación APP–TRIT–TPK y evaluación posterior: localizadores del paquete

6 de septiembre de 2026. Aclaración de la entrega de Ley 9 puertas; no es otra auditoría integral. Se conserva el corte de 2.249 páginas. No se han reejecutado censos ni campañas de cifras y no se han modificado los PDF, TeX, programas científicos o manifiestos del paquete.

## 1. Corrección de alcance de nuestra exposición

La composición APP–TRIT–TPK es el antecedente que declara y desarrolla el corpus. Presentar únicamente una serie, una raíz polinómica o una evaluación numérica omite ese antecedente. Una entrada de una función posterior tampoco es, por ese hecho, una entrada externa del modelo.

La prueba del capítulo 27 distingue expresamente dos etapas: caracteres exactos procedentes del estado enriquecido y publicación arquimediana de esos caracteres. Los intervalos de publicación calculan bloques coordenados; no deben llamarse «hijos de Ext» ni tomarse como prueba de que el modelo selecciona retrospectivamente un estado mediante una cifra.

Mi contraste estático anterior utilizaba las expresiones «hijo» y «descendencia material» al describir `publish_archimedean_blocks`. **La denominación correcta en ese tramo es subcilindro o bloque de publicación arquimediana.** Se rectifica esa terminología. Permanece la observación, limitada al programa inspeccionado, de que publicar bloques no equivale a ejecutar todas las coordenadas del estado enriquecido. No se convierte esta limitación de nuestra comprobación en negación del corpus.

Fuente: [profundidad arbitraria y separación de etapas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:553>), especialmente la demostración y el corolario de separación.

## 2. La documentación operativa sí está incluida

| Pieza | Función y límite |
|---|---|
| [README de la base](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/README.md:28>) | Expone APP→TRIT→TPK, la conexión nonádica, las publicaciones correlacionadas y el recorrido posterior. No necesita una skill para ser leído. |
| [START_HERE_HMT_MD.json](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/START_HERE_HMT_MD.json:45>) | Identifica generador, contratos, recibos, propietarios y sus huellas. Pertenece a la base conservada, no a la versión correctiva posterior por simple herencia. |
| [Verificador de arranque](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/verificar_START_HERE_HMT_MD.py:1018>) | Comprueba el grafo, las vinculaciones, los archivos, estados y recibos. No equivale a reejecutar cada demostración científica. |
| [Contrato causal](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/04_RECIBOS/RECIBO_CAUSAL_GENERACION_ANTES_PUBLICACION_ARQUIMEDIANA_20260905.json:1>) | Especifica hojas APP, orientación TRIT, operadores TPK, cadena nonádica y roles de π, φ, e y α. Su campo `material_status` conserva un estado de preparación; no se sustituye por un recibo de ejecución. |
| [Entrada de la copia correctiva](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/README_VALIDACION_CARACTERES.md:1>) | Documenta la resolución portable de nueve dependencias, la prueba de interfaz y el ensayo de integración. |
| [Recibo de interfaz e integración](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/RECIBO_VALIDACION_CARACTERES.json:1>) | Separa validación de e/φ, integración portable y resultados que ese control no certifica. |

El paquete contiene, por tanto, una guía y un contrato causal: no procede describirlo como si el lector necesitase recibir oralmente ese orden. La cuestión de implementación es comprobar que cada resultado atribuido a una ejecución coincide con las operaciones efectivamente llamadas.

## 3. Cadena de llamadas de la copia correctiva

Programa: [verificar_generacion_infinita_nonadica.py](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:2248>).

SHA-256 recomprobado: `0a5b0b8cee4ec477e5a255c4ba30ff6155a4b5cc28588ead3cebff652416c579`.

| Tramo | Operaciones localizadas | Qué hace ese tramo |
|---|---|---|
| Catálogo y regiones | `select_structural_orbits`, línea 468 | Lee el catálogo de 468 emisiones, verifica sus censos y selecciona las órbitas mediante predicados. No reenumera en esta llamada todos los pares originales de semillas. |
| Transportes finitos | `reconstruct_lifts_and_calendar`, 829; `finite_chain`, 943 | Reconstruye y contrasta matrices/calendario con las biografías y prolonga hasta w30. La derivación anterior de las biografías no se reemplaza por su literal de regresión. |
| Primera frontera | `generate_target_free_r36`, 1017; `verify_typed_r36_aw_bridge` | Construye candidatos y la frontera R36, preserva los controles estructurales y transporta el calibre AW. |
| Caracteres | `generate_structural_characters`, 1321 | Forma los objetos exactos de clausura, propagación y autoescala y registra su procedencia conjunta; α conserva su propietario y su orden interno. |
| Extensión y conexión | `verify_forward_character_extension`, 1472; `verify_connection_identities` | Comprueba anclas, metadatos e identidades paramétricas de truncamiento/fase/memoria. El alcance concreto de esos controles se distingue de la ejecución de todas las coordenadas del estado. |
| Evaluación | `evaluate_generated_characters`, 1809 | Consume los caracteres anteriores: clausura, recurrencia de propagación e incidencia de autoescala. |
| Publicación | `publish_archimedean_blocks`, 1881 | Publica bloques mediante cotas racionales. La selección aquí es de coordenadas arquimedianas, no de una órbita APP. |
| Contraste | `verify_finite_forward_witness` y `verify_prefix_stability` | Coteja anclas finitas y estabilidad de prefijos; no define retrospectivamente los caracteres. |

El orden se lee directamente en `run`, líneas 2248–2335. La copia correctiva aplica realmente los campos de recurrencia e incidencia; no debe atribuirse a ella la indiferencia de la copia anterior ante mutaciones de esos campos.

### Invocación documentada y ejecución conservada

La invocación del ensayo de integración está en el README citado; se transcribe como localizador reproducible, **no se ha vuelto a ejecutar**:

```text
python3 -I -S 03_PRUEBAS/verificar_generacion_infinita_nonadica.py \
  --digits 8 --guard-digits 4 \
  --certificate 03_PRUEBAS/SMOKE_8/certificado_generacion_infinita_nonadica_smoke_8.json \
  --r36-receipt 03_PRUEBAS/SMOKE_8/recibo_r36_smoke_8.json \
  --ext-receipt 03_PRUEBAS/SMOKE_8/recibo_ext_smoke_8.json
```

Se ejecuta desde la raíz de la revisión. Es una orden con escritura de recibos: para repetirla sin alterar la instantánea deben utilizarse una copia o destinos nuevos. La precisión del ensayo no limita el parámetro de precisión del programa ni el enunciado de profundidad arbitraria.

El [certificado conservado](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/SMOKE_8/certificado_generacion_infinita_nonadica_smoke_8.json>) tiene SHA-256 `d234d3f712b764201bbbc083f6c5dea010c08b0e7d6de25bf1ff4f0be22ca003`, coincidente con el recibo. Acredita que aquella ejecución recorrió las funciones del programa; los nombres de sus estados de aprobación no amplían por sí solos lo que cada función comprueba.

## 4. α: el productor, los registros y los controles no son una sola función

La fuente conserva el origen común de P/E/Φ y del registro firmado; su uso posterior dentro de la clausura dodecafásica no introduce constantes convencionales.

Hay dos propietarios ejecutables distintos que deben citarse sin confundirlos:

1. [verificar_alpha_dos_vias.py](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_alpha_dos_vias.py:1>). `k_from_hadamard` reconstruye K desde U; `k_from_differences` lo reconstruye desde D3, D4 y Q; `alpha_by_carry` aplica el acarreo a las tríadas publicadas y K. Este archivo serializa esos registros. Su función `vacancy_root` utiliza `pi_chudnovsky` para reevaluar un núcleo polinómico ya fijado: **esa reevaluación es nuestra comprobación posterior, no el origen APP–TRIT–TPK de π o α**. Mi replay había ejecutado también esa función; su resultado no se debe atribuir como ejecución de la genealogía completa.
2. [generar_alpha_T1_10000.py](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/00_CORPUS_RECTOR_PRESERVADO/11_MONOGRAFIA_APP_TRIT_TPK_CONSTANTES/evidencia/procedencia_1063_generacion_10000_rev9/generar_alpha_T1_10000.py:1>). Lee bloques ternarios y su certificado, obtiene sus proyecciones decimales, lee la coordenada K_R12 y ejecuta `propagate_branch` para las cinco condiciones remotas de acarreo. Publica únicamente el prefijo común. No calcula α desde un objetivo α ni consulta CODATA. Este módulo consume K: su ejecución no debe presentarse también como producción anterior de K.

La copia correctiva nonádica contiene el registro de procedencia de α, pero su diccionario de bloques evaluados contiene π/e/φ. No existe una llamada desde ese `run` a los dos programas α anteriores. Esto delimita una llamada particular; no elimina el otro propietario del paquete ni su conexión matemática.

## 5. Correcciones concretas en la entrega

- Anteponer siempre la composición APP–TRIT–TPK al describir caracteres y evaluadores.
- Referirse a «bloques de publicación» en el publicador arquimediano, no a «hijos de Ext».
- Separar la fuente anterior `6ec66d…` de la correctiva `0a5b0b…`; están conservadas las dos.
- Distinguir contrato causal, comprobación de integridad, ejecución integrada y reevaluación local.
- Mantener, al final y sólo con alcance local, la verificación aún no completada del productor de todas las coordenadas firmadas y del transporte de todos los coeficientes de la segunda vía. No calificarlos por ello como entradas externas ni ausentes de todo el corpus.

## 6. Productores anteriores y ecuaciones estructurales recuperadas

Esta ampliación sigue los antecedentes que faltaban en la tabla de llamadas; no inicia otra campaña numérica.

### Catálogo anterior a la selección orbital

[verificar_catalogo_app.py](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_catalogo_app.py:1>) contiene la enumeración del censo, no sólo su importación. Forma 324 semillas por hoja —posición en 9×9 y una de cuatro orientaciones—, calcula las firmas de las hojas suma y producto y recorre 104.976 pares. Sus operaciones incluyen raíz digital, reglas de movimiento, cambios de fase y acumulación en seis ventanas. Construye el contador de U6 antes de compararlo con el CSV.

La palabra literal PI_WORD se utiliza para reunir una microfibra particular en esa revisión; no es el argumento del cálculo del contador U6. Esta separación es visible en el código. Este archivo no se ha vuelto a ejecutar durante la presente ampliación.

La llamada select_structural_orbits del programa correctivo consume el catálogo serializado y utiliza además diag_c y hplus_type. La correspondencia completa entre el productor anterior y **todos** los campos de ese JSON no se acredita por haber localizado el contador U6. Se mantienen identificados el producto construido y los campos adicionales utilizados.

### Caracteres: no sustituir el constructor por su evaluación

- **π.** La fuente U012, desde la línea 350, fija \(P_5=\frac15\mathbf1\mathbf1^{\mathsf T}\), su punto fijo normalizado, la composición de pendientes y el retorno a la diagonal. Obtiene \(1/5\), \(5/12\), \(120/119\) y 239; la identidad gaussiana identifica después la media vuelta. La función generate_structural_characters calcula esos parámetros desde los invariantes regionales. No debe describirse ese tramo como una tabla de cifras.
- **e.** U013, desde la línea 213, especifica \(P(s+t)=P(s)P(t)\) y \(a_0=a_1=1\); comparar coeficientes produce \((n+1)a_{n+1}=a_n\). La normalización y la ley de composición forman parte de la estructura declarada del lector. La copia correctiva hace depender la evaluación de esos campos.
- **φ.** U014, desde la línea 153, cuenta las tres transiciones del calendario \((\Sigma,\Pi,\Pi)\). Obtiene \(N_3\) y publica \(F_{\rm av}\); sólo después calcula el rayo propio positivo y sus potencias. La matriz impresa en una rutina de regresión no puede clasificarse como dato externo sin recorrer esta construcción.
- **i.** La fuente base_83/c26_body.tex, desde la línea 3, conserva la conferencia de Paley, la reducción \(A_W^2=-I\) sobre \(\mathbb F_3\) y la fuente integral \(\mathbb Z[u]/(u^2+1)\). La realización real y la finita tienen codominios distintos.

Para las biografías que reconstruyen \(L_0,L_1\), el programa utiliza REGRESSION_BIOGRAPHIES_FROM_ENRICHED_LEDGER. La inversión de los sistemas, sus rangos y la unicidad del calendario son verificaciones concretas. No se confunden con la construcción anterior de todas las biografías: esa procedencia exige su propio enlace, aunque la fuente declare que pertenecen al estado completo.

### Registro firmado: lo recuperado y el límite exacto de esta inspección

La [proposición del registro](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:428>) y la [doble lectura terminal](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/alpha/08a_alpha_dos_vias_t1_rev8_body.tex:12>) dan
\[
x_{\rm term}\longmapsto(B_{\rm term},U),\qquad
U\longleftrightarrow K\longleftrightarrow(D_3K,D_4K,Q).
\]
Explican por qué no se debe buscar una función \(B_{\rm term}\to U\): la proyección visible ha olvidado coordenadas.

En los programas focales efectivamente leídos, verificar_alpha_dos_vias.py reconstruye K a partir de U o de las diferencias y Q serializadas; generar_alpha_T1_10000.py lee K_R12 y aplica el acarreo a las publicaciones de los tres canales. Ninguno de esos dos cuerpos es, además, el productor anterior de todas las coordenadas U. La proposición localiza y tipa \(R_{\rm sgn}\), pero **esta inspección no ha reconstruido una rutina anterior que evalúe sus doce coordenadas desde las semillas**.

Éste es un límite preciso del cotejo realizado, no una conclusión de que U sea metrología externa ni de que el productor no exista en otro propietario. La búsqueda focal incluyó los programas Python de la fuente sucesora, el módulo correctivo y la monografía de constantes conservada; no se atribuye exhaustividad a una búsqueda de literales. El grafo mantiene esa arista como producción documentada en TeX cuya ejecución completa no se ha enlazado todavía.

## 7. Entrega estructural para la edición común

[La aportación de estructuras y significados](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/APORTE_ESTRUCTURAS_SIGNIFICADOS_NUCLEO.md>) contiene ahora las ecuaciones y la jerarquía de los caracteres, la familia exponencial, las dos orientaciones del lector \(\mathscr R(x,y)=x/y^2\), el centro electrónico y el funcional dodecafásico anterior a γ. [El grafo JSON](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/ARBOL_ESTRUCTURAL_NUCLEO.json>) distingue dependencias documentadas, composiciones, realizaciones y compatibilidades cuya verificación no ha concluido.

La centralidad estructural no se identifica con el orden de evaluación: el centro electrónico precede a su masa y la cadena de doce sectores con una costura precede a la evaluación de Barbero. Esta precisión organiza los resultados recuperados; no altera las fuentes científicas ni promete una comprobación global por un control documental.

Procedencia: recuperación y aclaración documental de arquitectura autoral preexistente. No se ha producido una nueva demostración ni sustituido material científico.
