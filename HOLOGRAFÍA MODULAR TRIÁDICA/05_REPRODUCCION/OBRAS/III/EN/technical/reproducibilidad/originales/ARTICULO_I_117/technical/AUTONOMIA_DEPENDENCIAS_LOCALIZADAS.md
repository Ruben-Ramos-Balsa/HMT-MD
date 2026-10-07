# Dependencias demostrativas remitidas fuera del artículo

## Ámbito y criterio

Lectura focal del sucesor `ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909`, realizada el 9 de septiembre de 2026. Se examinan únicamente las remisiones sustantivas al suplemento, a notas de procedencia y al integral. No es una auditoría del corpus HMT–MD, una nueva comprobación numérica ni un dictamen sobre resultados no examinados.

El criterio aplicado es el de `preserve-hmt-continuity/references/publication_dependency_closure.md`: una dependencia propia de HMT necesaria para un resultado anunciado debe tener definición y prueba dentro del PDF autónomo. Una cita bibliográfica, una nota privada o un programa adjunto pueden documentar procedencia y reproducibilidad, pero no sustituyen esa residencia. Los teoremas externos establecidos conservan el uso académico ordinario de las referencias.

Las ubicaciones siguientes corresponden a las fuentes TeX del sucesor, no a una paginación nueva todavía no comprobada. Los archivos técnicos citados no están incluidos como apéndices en `main.tex`. La revisión localiza **tres núcleos de dependencia**, con dos operaciones distintas dentro del segundo; no infiere de ellos que el resto del artículo esté plenamente conciliado.

## 1. Producción de las transiciones y selección del calendario nonádico

**Lugar:** sección «Generación coinductiva de π, φ, e», apartado «Transporte finito y frontera de prolongación»; `sections/generacion.tex:46–82`.

**Frase que externaliza la dependencia:**

> «La procedencia de su registro y el examen de los dieciséis calendarios binarios se documentan en el suplemento técnico.»

**Dependencia exacta:** la producción de los pares de transiciones por la composición de los pasos TPK, antes de formar las matrices de orígenes y destinos `X₀,Y₀,X₁,Y₁`; después, la selección del calendario `(L₀,L₀,L₁,L₁)` entre los 16 candidatos binarios de longitud 4.

**Contenido ya incorporado:** el artículo da la tabla de los pares, los determinantes de las matrices de origen, las matrices resultantes y la fórmula `Lₐ=Xₐ⁻¹Yₐ`. La unicidad algebraica desde esos pares queda expuesta. El propio párrafo diferencia expresamente esta inversión de la producción de las transiciones.

**Contenido público que la remisión no aporta:** el recorrido que produce la tabla desde los estados y operaciones anteriores, y el contraste finito que determina el calendario anunciado. Incorporar ese recorrido y su criterio de selección permitiría seguir la procedencia sin recibir la tabla como punto de partida de la prueba. No se pide sustituir TPK por un generador convencional ni repetir una campaña de decimales.

**Resultado afectado:** procedencia operativa de la prolongación `w₆→w₁₂→w₁₈→w₂₄→w₃₀`. Las demostraciones posteriores sobre horquillas y prefijos no reconstruyen retrospectivamente esta etapa.

## 2. Determinación terminal y extracción de los canales que anteceden a K

### 2.1. Selección finita del estado terminal visible

**Lugar:** «Dos lecturas del estado terminal», `sections/registro_k.tex:172–209`, etiqueta `subsec:k-terminal`.

**Frase pertinente:**

> «El selector terminal de la construcción de referencia opera sobre catálogos de tamaños 196, 197 y 196.»

Se cita `hmtintegral`. El cuerpo anuncia la reducción `196·197·196=7 567 952→331→2` y exhibe las dos matrices finales. La condición axial sobre sus cargas se comprueba expresamente y selecciona `B₁`.

**Dependencia aún remitida:** la construcción de los tres catálogos, los predicados concretos de firmas que reducen las ternas a 331 y la procedencia del margen de columnas `q∂=(1,2,2,1,2,0)`. El texto distingue correctamente la inspección de las dos matrices de la enumeración que las produjo; esta enumeración anterior no queda sustituida por la comprobación axial.

Este subcaso afecta a la determinación de la lectura terminal visible. **No introduce una flecha `Bterm→U`: el artículo mantiene expresamente que son dos lecturas del mismo estado.**

### 2.2. Acción del extractor sobre el registro de incidencias

**Lugar:** continuación del mismo apartado, `sections/registro_k.tex:211–237`, etiqueta `eq:k-lector-firmado`.

**Frase que externaliza la dependencia:**

> «El rastro material del extractor anterior y el alcance de su transcripción autónoma se conservan en la nota técnica de procedencia.»

**Dependencia exacta:**

\[
\mathcal R_{12}(x_{\rm term})
\xrightarrow{\mathcal E_{108}^{90,120}}
(b^{90},b^{120},Q_{\rm TPK})\in\mathbb Z^{25}.
\]

El cuerpo especifica el tipo, el orden causal y las 25 coordenadas resultantes. Desde ellas sí desarrolla la acción de `Π_H`, el vector firmado `U`, la inversión de Hadamard y `K`, además de las reconstrucciones transversales.

**Dependencia pública precisa:** la acción de `E₁₀₈^{90,120}` sobre los generadores efectivos del registro de incidencias, acompañada de la evaluación que produce esas 25 coordenadas. En `tpk_desarrollo_integrado.tex:337–361` se recuperan la composición, el dominio y la carta de eventos; el pasaje remite nuevamente al capítulo de K. Los cardinales de incidencia 90 y 120 construidos en el apartado siguiente no son por sí solos la fórmula del extractor.

La nota existente `technical/procedencia_alpha.md:43–51` delimita expresamente esta misma transcripción. Se conserva su alcance: **no se declara ausente el resultado en el corpus ni se reclasifican las coordenadas como entradas metrológicas**. Se localiza la operación anterior a la cual comienza la reconstrucción explícita de esta edición.

**Resultados afectados:** la reproducción autónoma de la generación de `K` desde el estado terminal y, por dependencia, su utilización en alfa y en la bandera de incidencia. La inversión de Hadamard y la reversibilidad de K tienen sus pruebas propias incorporadas; no son el objeto de esta observación.

## 3. Prolongación analítica completa y compatibilidad de las dos vías de alfa

**Lugar:** «Compatibilidad de las dos determinaciones a toda profundidad», `sections/alpha.tex:519–583`, etiqueta `subsec:alpha-limite-dos-vias`.

**Frases pertinentes:**

> «La segunda vía determina su raíz positiva única [...] con la unicidad y la compatibilidad del lector completo establecidas en las demostraciones de referencia.»

> «Las demostraciones de la prolongación coinductiva y de las dos vías establecen que ambos sistemas determinan, a cada profundidad, el mismo cilindro superviviente.»

Ambas remiten a `hmtintegral`. La observación contigua de alcance documental ya precisa que estas remisiones no se computan como demostración autónoma en el artículo actual.

**Dependencia exacta:** la regla que produce todos los grados posteriores al truncamiento de orden 9, su realización en un dominio donde tenga sentido la raíz analítica, y los cuadrados efectivos que identifican esa construcción con los cilindros posicionales a cada profundidad.

**Contenido ya incorporado:** la normalización posicional completa; la firma y la expresión del truncamiento; el resolvente nilpotente de grados 7–9; existencia, unicidad y simplicidad de su raíz; y la proposición condicional `prop:alpha-dos-limites`, cuya prueba identifica dos valores cuando ya pertenecen a los mismos cilindros de diámetro tendente a cero.

**Contenido remitido:** la construcción que establece precisamente esa pertenencia común para todos los niveles. La prueba elemental de identificación de límites no produce por sí misma los cuadrados de compatibilidad. El texto actual lo reconoce; su observación no debe suprimirse por haber compilado el manuscrito.

`technical/ALFA_REVISION_PROCEDENCIA.md:56–70` y `technical/procedencia_alpha.md:73–82` conservan antecedentes de esta delimitación. Su presencia en la carpeta no constituye la incorporación de una regla de continuación al PDF. Esta lectura focal no añade una conclusión sobre fuentes nuevas no recorridas ni sustituye la investigación de dicha regla.

## Remisiones que no se han contado como carencias sustantivas

- **Censo inicial:** `extension.tex:55` remite a un anexo de firmas. El cuerpo ya especifica el dominio finito, la recurrencia de los cursores, el acoplamiento y la reducción, de modo que el catálogo puede reproducirse mediante esas reglas. La remisión nominal al anexo debe conciliarse editorialmente, pero no se equipara aquí a un extractor sin acción coordenada.
- **Memoria de la firma central:** `centro_electronico_registros.tex:136–138` cita un certificado adjunto; el propio apartado define el dominio de 324 posiciones, ambos operadores, el lector y el refinamiento de particiones. No se lo clasifica como una operación mantenida exclusivamente en un archivo privado.
- **Familia de estrellas de Witt:** `excepcional.tex:472–476` remite a los seis generadores usados en una enumeración abreviada. El cuerpo define todas las 495 permutaciones y la comprobación por cierre. Los seis generadores facilitan la reproducción del cálculo, pero no son necesarios para definir el grupo generado por la familia completa. No se confunde esta referencia con un mapa generador omitido.
- **Aislamiento estrecho de la raíz del truncamiento:** `alpha.tex:479–509` remite a evaluaciones dirigidas del certificado. El operador y la prueba pública de existencia y unicidad ya están escritos. El respaldo racional de los extremos estrechos puede incorporarse como control breve, pero no se cuenta como otro problema estructural independiente de los anteriores.
- **FLM, clasificación reticular y Moonshine:** las atribuciones a resultados externos establecidos conservan el uso bibliográfico ordinario. No se exige reproducir en el artículo toda la teoría clásica para eliminar una cita.

## Uso del inventario

Este inventario permite distinguir la compilación y preservación del manuscrito de la clausura pública de sus dependencias. Los puntos 1 y 2 localizan etapas de procedencia operativa; el punto 3 localiza la compatibilidad analítica-posicional de alcance infinito. No se modificaron las fuentes TeX, los cálculos ni los PDFs durante esta lectura. La skill de continuidad HMT se utilizó para fijar ese criterio y conservar la distinción entre remisión documental y ausencia matemática.
