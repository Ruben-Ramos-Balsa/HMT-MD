# Integración de la construcción correlativa del continuo

## Corte y responsabilidad

Antecedente preservado: `ARTICULO_IV_REV02_EDICION_INTEGRADA_20260910`,
**Moonshine, dualidad T y teoría M desde la estructura discreta del continuo**,
124 páginas. La presente carpeta es una sucesora de trabajo; los PDF y
manifiestos copiados de REV02 son antecedentes y no certifican esta ampliación.
La entrega nueva se distingue materialmente de esos antecedentes por su PDF
compilado y sus recibos propios; la revisión visual focal ya fue realizada
por raíz sobre el PDF definitivo.

La portada fue coordinada con la tarea «Ley 9 puertas», que uniforma la
presentación de la serie. Se incorporó `iv_portada.tex` y se preservó íntegro
el cuerpo del resumen en su página siguiente. Esa corrección no modifica las
pruebas ni sus condiciones.

## Cambios del cuerpo

1. Se conserva íntegramente el núcleo común y cada cuerpo preexistente.
2. Se incorpora `sections/continuo_conjunto.tex` después de `extension.tex` y
   antes de `generacion.tex`.
3. Se conserva el desarrollo recuperado del capítulo
   `05_CONSTRUCCION_CORRELATIVA_DEL_CONTINUO` del manuscrito de primos:
   cociclo, medida, transporte, Gram, cancelación, incidencia, complejo,
   ensamblaje terminal y lectura determinante.
4. Se especifica la base con etiqueta de hoja y el sentido de la fase neutra.
5. Se construyen los puertos como lecturas etiquetadas de las mismas historias;
   se demuestra su naturalidad por precomposición, con marcas compatibles,
   tanto al prolongar historias como al reducir coeficientes.
6. Se distingue `Det Γ` de `Det(Tot B)` y se escribe la fórmula de la segunda
   sobre todos los caminos a horizonte finito.
7. La introducción y las conclusiones reciben párrafos aditivos para explicar
   la función de esa incorporación.

La medida equiprobable es una elección explícita sobre los hijos admisibles;
las otras medidas positivas se exponen como familia de lectores, no como una
ley probabilística única deducida de las siglas TPK. La media del balance
tampoco se identifica con el recuento bruto de un prefijo.

## Estatuto

La arquitectura es autoral y preexistente. El capítulo es **RESULTADO_RECUPERADO**.
La identificación de puertos y la naturalidad explícita añadida son
**FORMALIZACION_NUEVA** de la compatibilidad del mismo árbol; no se presentan
como un descubrimiento de la arquitectura HMT ni como una resolución nueva de RH.

Se incorpora una construcción conjunta de operaciones locales con sus pruebas
y condiciones, no cinco problemas independientes. La publicación posterior
de Weil mantiene su identidad específica de momentos; la nota
`TRAZA_INTEGRAL_WEIL_20260911.md` documenta ese punto separado.

## Conservación y controles

El cotejo de raíz verificó las seis fuentes comunes byte por byte y la
conservación de los cuerpos anteriores. El delta final contiene ocho archivos:
`main.tex`, `continuo_conjunto.tex`, `iv_introduccion.tex`, `iv_conclusiones.tex`,
`iv_portada.tex`, `iv_resumen.tex`, `extension.tex` y `generacion.tex`.
La armonización de portada, la retirada de su envoltura del resumen y la
compactación tipográfica del índice se distinguen de la ampliación matemática.
Dos remisiones futuras al capítulo electrónico ausente se corrigieron para
declarar el orden real de K y alfa y su aplicación electrónica posterior;
la introducción explica el ámbito de esas remisiones del núcleo común.
Esas correcciones no retiran fórmulas ni pruebas. El corte de 135 páginas y su
QA preliminar se conservan como antecedentes, no como entrega activa.

El control `technical/verificar_identidades_continuo.py` procede del paquete de
primos y contrasta identidades locales exactas. Sus resultados no sustituyen
las pruebas ni certifican la positividad de Weil. Se requieren además revisión
del nuevo tipado, comprobación de dependencias de compilación e inspección
visual de las páginas añadidas.

## Estado compilado del corte final

El preflight canónico del corte `8f03f52de977edb5` emitió
`PASS_HMT_MD_PRECOMPILE`: 74 fuentes inventariadas, incluidas las fuentes
históricas conservadas, 74 residencias documentales y un certificado editorial.
El grafo activo de compilación reúne 55 fuentes TeX. Los dos recuentos tienen
dominios distintos y no se equiparan.

El PDF nuevo, distinto del copiado de REV02, es
`output/pdf/MOONSHINE_DUALIDAD_T_TEORIA_M_CONTINUO.pdf`: **134 páginas**,
764.603 bytes; SHA-256
`5649278f225c5b1d935fb85ebb41eb9443ea55eda3a2e09039a456660c7a0467`.
Tres pasadas completadas, sin referencias o citas faltantes, sin etiquetas
duplicadas, sin glifos ausentes y sin desbordamientos. Se conservan dos avisos
`underfull hbox`. El capítulo nuevo empieza en la página impresa 37; la
naturalidad de puertos aparece en la 41 y las conclusiones comienzan en la 130.

Recibo:
`technical/compilacion/20260911T000738Z_b7f53854/RECIBO_COMPILACION.json`.
El manifiesto de esa compilación se encuentra en el mismo directorio.

La suite actual ejecutó seis programas en normal y en modo optimizado:
**doce ejecuciones satisfactorias**. Incluye 43.503 controles exactos del
continuo y 9.072 de naturalidad de puertos por modo. El recibo está en
`technical/CONTROL_REPRODUCCION_LOCAL_FINAL_20260911.json`.
Los recibos genealógico y causal focales del corte de fuente compuesta
`b9da575d778d2a3b_bc8103ad` también pasaron sus verificadores. Sus objetos
son la causalidad declarada y la composición local incorporada; no prueban
el cierre global de Weil, RH o teoría M.

## Revisión visual y cierre material

Raíz inspeccionó directamente 25 páginas físicas del PDF final, incluido el
capítulo conjunto completo (38–45), el índice, las remisiones corregidas y
las figuras de estrella incidencial y disposición pentádica. El recibo
`technical/QA_VISUAL_FINAL_20260911.json` declara `PASS_QA_VISUAL_FOCAL`, sin
defectos críticos en las páginas examinadas. No se equipara ese alcance a la
revisión visual integral de las 134 páginas.

El cierre material utiliza `technical/empaquetar_continuo.py --seal` con ese
recibo y el de compilación final; preserva el manifiesto anterior en
`technical/historial_manifiestos/` y verifica la integridad del ZIP. La
distribución se denomina
`MOONSHINE_DUALIDAD_T_TEORIA_M_CONTINUO_20260911.zip`. Su comprobación portable
ejecuta sólo los controles locales incluidos, sin otra compilación ni una
certificación científica global.

Se conservan también `technical/IMPLICACION_ESTRUCTURAL_WEIL_20260911.md`
y la copia íntegra de la nota antecedente
`technical/antecedentes_editoriales/RECUPERACION_GENERATIVA_WEIL_20260911.md`.
Registran la contribución autoral y la tarea de composición precisa; no
promueven la incorporación local a prueba global de Weil.

El empaquetado sólo comienza después de congelar la documentación concurrente.
Ningún índice humano se ha modificado desde esta subtarea técnica.
