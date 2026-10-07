# Cuaderno acumulativo: memoria, vacancias y acción

## Desarrollo actual

[Continuación narrativa: compatibilidad, acción y memoria operacional](NARRATIVA_CONTINUACION_COMPATIBILIDAD.md). Exposición extensa para el futuro PDF: qué aporta cada resultado, cómo enlaza con el par angular y qué conserva cada lectura. Se conserva junto a las pruebas, no en sustitución de ellas.

[Mapa de integración narrativa y demostrativa](MAPA_INTEGRACION_NARRATIVA.md). Orden de composición de los desarrollos y localización de los seis resultados destacados por Rubén, para su futura reunión sin pérdida.

[Compatibilidad constitutiva, holonomía relativa e información operacional](COMPATIBILIDAD_HOLONOMIA_E_INFORMACION.md). Desarrolla la reciprocidad diferencial velocidad–impedancia, su potencial de profundidad dos y la relación con Catalán; construye un lazo de los cuartos de giro conjugados, lo levanta a las doce fases y precisa qué información pierde una lectura escalar. Incluye demostraciones, estabilidad de la inversión y alcance de la interpretación física.

[Narrativa aprobada y mandato de desarrollo](NARRATIVA_APROBADA_Y_MANDATO_DESARROLLO.md). Conserva literalmente la explicación anterior y el mensaje de Rubén que selecciona los resultados destacados y autoriza esta continuación.

[Acción, masa y propagación: composición estructural y transporte](HIBRIDACION_ACCION_MASA_PROPAGACION.md). Continuación con la ley general de masas, frecuencias propias, reciprocidad espacial, pesos térmicos ternarios, convexidad constitutiva y transporte exacto de la elipse. Conserva la petición autoral y distingue la conexión de representación de una interacción física. [Programa de controles racionales](verificar_hibridacion.py).

[Contraángulo, electrón, Barbero y Catalán: composición y restitución](CONTRAANGULO_ELECTRON_BARBERO_CATALAN.md). Aclara la abreviatura B(α), conserva grados/radianes y la ecuación electrónica completa, y demuestra la restitución de los dos canales constitutivos desde velocidad normalizada y Barbero. Incluye la composición posterior con acción y los restantes lectores, con dominio explícito.

[Localización del patrón1828·1828 en la genealogía de e](LOCALIZACION_E_1828_Y_RETORNO.md): fuentes, páginas, elevaciones reproducidas y distinción entre repetición decimal y retorno trítico.

[Regularidad genealógica, restitución operatoria y geometría de la acción](REORIENTACION_GENEALOGICA_Y_RESULTADOS.md).

[Lectura narrativa: memoria operativa e invariantes de una estructura que evoluciona](LECTURA_NARRATIVA_Y_PROGRAMA_DE_CONTRASTE.md). Explica qué aportan las relaciones y propone tres contrastes, diferenciando resultados presentes y trabajo propuesto.

Contiene la jerarquía de investigación, tres pruebas focales, su procedencia y la interpretación conjunta. El archivo no sustituye a los manuscritos ni declara una nueva certificación integral.

## Historia conservada

- [91 intervenciones públicas, 19–22 de septiembre](HISTORIAL_PUBLICO_20260919_20260922.md).
- [39 intervenciones públicas de continuación, 22 de septiembre](HISTORIAL_CONTINUACION_PUBLICA_20260922.md), con un turno de solapamiento para preservar la continuidad.
- [Dos aclaraciones autorales sobre el contraángulo](ACLARACIONES_AUTORALES_CONTRAANGULO.md), conservadas literalmente como adiciones al hilo previo.
- [Nota inicial de memoria y vacancias](NOTA.md).
- [Transporte compensado](DESARROLLO_TRANSPORTE_COMPENSADO.md).
- [Acción, memoria y trabajo recuperable](ACCION_MEMORIA_TRABAJO_RECUPERABLE.md), conservado como aplicación auxiliar.

Las notas y los programas anteriores no se han sobrescrito. El historial contiene también formulaciones discutidas: su conservación no ratifica su contenido.

## Comprobaciones del desarrollo actual

El desarrollo de compatibilidad y holonomía se reproduce con `python3 -I -S verificar_compatibilidad_holonomia.py`. Comprueba el Jacobiano y sus cotas, la identidad de momentos, el conmutador general, su energía relativa, la covariancia del detector, el levantamiento dodecafásico, su iteración y la restitución del coeficiente de acción. [Resultados focales](RESULTADOS_COMPATIBILIDAD_HOLONOMIA.json) · [Procedencia y alcance](RECIBO_COMPATIBILIDAD_HOLONOMIA.json). El único contraste numérico no racional —logaritmo frente a una serie truncada— se identifica por separado; las pruebas generales están en la nota. La puerta de constantes comprueba el orden causal declarado y no certifica una identificación física global.

El [recibo genealógico focal](RECIBO_GENEALOGIA_COMPATIBILIDAD.json) hereda los antecedentes documentados de III, añade el lector elíptico de X y enlaza las composiciones de esta nota. La puerta `verificar_genealogia_unica_hmt.py` emitió `PASS_GENEALOGIA_UNICA_APP_TRIT_TPK` sobre sus doce mapas. Esa salida comprueba vínculos, dominios declarados, huellas y orden causal; el alcance matemático sigue siendo el de las pruebas locales, sin recertificación integral. [Recibo de la narrativa](RECIBO_NARRATIVA_COMPATIBILIDAD.json).

La hibridación se reproduce mediante `python3 -I -S verificar_hibridacion.py`: 432 controles de masa, frecuencia y radios; 699 de la desigualdad constitutiva; 125 transportes discretos; 75 identidades diferenciales; 75 determinantes de positividad, 284 relaciones de pesos térmicos y 375 transportes de acción normalizada, todos con fracciones exactas. Cuatro controles negativos detectan omisiones o signos incorrectos. [Resultados](RESULTADOS_HIBRIDACION.json) · [Procedencia y alcance](RECIBO_HIBRIDACION.json). Las pruebas para todo el dominio están en la nota, no se sustituyen por estos casos.

Composición contraángulo–electrón–Barbero–Catalán, con la biblioteca estándar de Python:

```text
python3 -I -S verificar_composicion_constantes.py
```

Se verificaron seis identidades matriciales exactas en Q[r,r⁻¹], 25 inversiones sintéticas de los canales (error máximo 2,23·10⁻¹⁶) y 99 comprobaciones racionales del cociente utilizado en la prueba de monotonía. La demostración para todo el dominio está en §7 de la nota; los casos finitos son controles adicionales.

[Resultados de composición](RESULTADOS_COMPOSICION_CONSTANTES.json) · [Procedencia y alcance causal de la composición](RECIBO_COMPOSICION_CONSTANTES.json). La puerta focal de constantes emitió `PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY`; comprueba conservación del orden causal declarado, no las identificaciones físicas del corpus.

Desarrollos anteriores, conservados:

```text
python3 -I -S verificar_reorientacion.py
```

- 2.000 ventanas con cotas e índices certificados mediante enteros e intervalos racionales.
- 2.500 casos de composición matricial exacta.
- 3.200 pares radiales orientados comprobados con fracciones.

[Resultados de ejecución](RESULTADOS_REORIENTACION.json) · [Recibo de procedencia y alcance causal](RECIBO_REORIENTACION.json).

La comprobación focal de causalidad emitió `PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY`. Este control clasifica entradas y salidas; no demuestra por sí mismo las matemáticas del corpus. Las pruebas generales de los resultados focales están en la nota, y los casos finitos las acompañan como controles.

El desarrollo se mantiene separado de las ediciones selladas. No se modificó ningún PDF.
