# Rango genealógico: regla, numerabilidad de niveles y cobertura

10 de septiembre de 2026. Desarrollo focal posterior a «Plegado, memoria y
cardinalidad». No modifica ni sustituye ese expediente, los manuscritos
compartidos o los PDFs.

## 1. Objeto heredado y tres condiciones de la investigación

La composición de partida es APP → TRIT → TPK → estado enriquecido
→ estructura discreta conjunta del continuo. APP conserva suma/producto,
residuo y cociente; TRIT conserva régimen y orientación; TPK transporta,
actualiza y prolonga. Se mantiene U_t → Γ_9 → K_ph: la publicación de
memoria reducida no sustituye a la holonomía generadora. El retorno de fase
avanza memoria y no reinicia el estado.

Se hereda el continuo conjunto, sin separar sus cinco construcciones.
El capítulo 18 aporta el sistema de estados finitos supervivientes, sus
restricciones, intervalos compatibles, contracción, cobertura y atlas.
Las lecturas que siguen son posteriores a esa construcción. No eligen
semillas, constantes ni estados mediante valores objetivo convencionales.

Notación:

- Ω es el espacio completo de historias del atlas, interpretado en V.
- Val:Ω→R^V es el lector por intersección de cilindros.
- x∼y significa Val(x)=Val(y); Q=Ω/∼.
- E y D designan el registro fiel de frontera y su inversa en el dominio
  acreditado por sus propietarios. No se amplía ese dominio por notación.
  La normalización y los resultados R1–R5 no requieren extenderlos a Ω.
- h codifica la presentación común APP–TRIT–TPK, no cada historia individual.
- M=L[h] y b_h:ω1^M→R^M son el modelo y la biyección recuperados del
  capítulo 19. Los argumentos cardinales posteriores se formulan en V,
  con elección, manteniendo M y V diferenciados.

La regla ordinal que se investiga debe satisfacer:

(R1) λ:Ω→ω1^V está definida en su dominio y es constante en cada fibra de Val.
(R2) C_ξ={Val(x):λ(x)=ξ} es numerable para cada ξ.
(R3) λ está definida sobre cada fibra del continuo ambiente.

Estas condiciones permitirían elegir e_ξ:C_ξ→ω inyectivas y construir

\[
 J(r)=\omega\cdot\lambda(r)+e_{\lambda(r)}(r)<\omega_1^V,
\]

donde λ(r) denota la función descendida al cociente. Los bloques ordinales
son disjuntos y las e_ξ son inyectivas. Así J sería inyectiva y produciría
el cierre cardinal. La familia e_ξ necesita una construcción o elección;
no se declara un algoritmo finito por escribir la fórmula.

## 2. Regla construida: normalización completa de la fibra de valor

### 2.1 Definición desde la cobertura ya existente

En cada conjunto finito de estados se fija un orden por su codificación
discreta completa. Es una convención de representación, no un nuevo
selector físico. Cambiar ese orden puede cambiar el representante, pero
no el valor ni las conclusiones siguientes.

Para una historia x, escribamos r=Val(x), una salida ya obtenida.
Se elige la primera carta K_m=[−m,m], m≥1, que contiene r.
Dentro de ella se define recursivamente:

\[
 a_0(r)=\min\{a\in S_0^{(m)}:r\in I_0(a)\},
\]
\[
 a_{n+1}(r)=\min\{b\in S_{n+1}^{(m)}:
             r_{n+1,n}(b)=a_n(r),\ r\in I_{n+1}(b)\}.
\]

Los mínimos se toman en conjuntos finitos no vacíos. La cobertura inicial
y la cobertura de cada cilindro por sus sucesores demuestran esa no vacuidad.
Se define

\[
 N(x)=(m,a_0(r),a_1(r),\ldots).
\]

La fórmula usa Val(x) para clasificar una historia ya producida.
No afirma generar x desde un real externo ni usa una constante objetivo
para seleccionar su genealogía.

### 2.2 Existencia, unicidad lectora y cobertura

**Teorema R1.** N está definida sobre Ω completo y satisface

\[
 \operatorname{Val}N(x)=\operatorname{Val}(x),\qquad N^2=N,
\]
\[
 N(x)=N(y)\ \Longleftrightarrow\
 \operatorname{Val}(x)=\operatorname{Val}(y).
\]

Sus coordenadas son compatibles:
r_{n+1,n}(N_{n+1}(x))=N_n(x) dentro de la carta seleccionada.

**Prueba.** La cobertura produce un candidato en el nivel cero y un
sucesor en cada paso. El orden finito fija uno solo. La cadena resultante
es compatible y todos sus intervalos contienen r. La contracción hace
que su intersección sea exactamente r. Dos historias de igual valor
eligen la misma carta y los mismos mínimos en cada paso. Si N(x)=N(y),
sus evaluaciones son iguales. Aplicar N nuevamente no cambia r ni sus
elecciones, lo que prueba la idempotencia. ∎

**Corolario R2.** Val restringida a N[Ω] es una biyección sobre R^V.

**Prueba.** La sobreyectividad de Val proporciona x para cada r.
N(x) publica r, y el bicondicional anterior da unicidad. ∎

La prueba vale también para historias que no pertenezcan a M. No se ha
añadido como premisa su constructibilidad en M. La cobertura utilizada es
la del capítulo 18, interpretada sobre las historias completas de V.

N no reconstruye la memoria de la historia original: normaliza su fibra
de valor. El estado original permanece intacto; cuando se usa su registro
de frontera acreditado, sigue siendo recuperable por D.
N es una publicación adicional; no sustituye a E ni al estado enriquecido.

Tampoco se afirma que N_n(x) se decida siempre con un prefijo finito de x.
En un extremo compartido por dos cilindros, resolver exactamente la
igualdad de valores puede requerir la historia completa. La compatibilidad
de las coordenadas de N no convierte esta selección en un transductor
finito uniforme ni en una operación continua.

**Estatuto:** formalización explícita de una selección permitida por la
cobertura del corpus. Es una normalización global; su codominio es un
espacio de historias, todavía no un ordinal.

## 3. Primer rango efectivo: primera aparición con h fijo

Se extiende el rango del capítulo 19 al dominio saturado

\[
 D_h=\{x\in\Omega:\operatorname{Val}(x)\in\mathbb R^M\}.
\]

Este dominio puede contener historias externas a M que publiquen valores
de M. No se exige x∈M. Para x∈D_h definimos

\[
 \lambda_h(x)=\min\{\alpha<\omega_1^M:
      \operatorname{Val}(x)^\flat\in L_\alpha[h]\},
\]

donde r^flat es una codificación real fija del valor, por ejemplo su corte
racional. La primera aparición y la numerabilidad de los niveles son los
resultados heredados de la condensación relativa del capítulo 19.

**Teorema R3.** λ_h es constante en las fibras de Val; cada uno de sus
niveles tiene imagen numerable en V; y cubre exactamente R^M por valores,
aunque se aplique a historias de D_h no pertenecientes a M.

**Prueba.** El criterio de primera aparición depende sólo de r^flat.
Cada nivel de valores inyecta en L_α[h], numerable en M para α<ω1^M.
Una enumeración existente en M sigue existiendo en V. Por tanto ese nivel
también es numerable en V. Cada r∈R^M tiene primera aparición y una
historia que lo publica por cobertura. Ningún r ajeno a M pertenece a
algún L_α[h], así que la imagen por valores es exactamente R^M. ∎

Se recupera igualmente el separador más fino

\[
 \rho_h^\uparrow(x)=b_h^{-1}(\operatorname{Val}(x)),\qquad x\in D_h,
\]

que separa exactamente las fibras, sin exigir que la historia esté en M.

### 3.1 Cuantificador ampliado a subconjuntos externos del portador conocido

**Teorema R4.** En V, para cada A⊆R^M, sin exigir A∈M, se cumple:

\[
 A\text{ es numerable}\quad\text{o}\quad |A|=|\mathbb R^M|.
\]

**Prueba.** Escribamos α=ω1^M. Cada ordinal numerable en M sigue siendo
numerable en V, de modo que α≤ω1^V. La biyección b_h sigue siendo una
biyección entre α y R^M en V.

Si α<ω1^V, entonces α y R^M son numerables en V; también lo es A.
Si α=ω1^V y A no es numerable, b_h^{-1}[A] es un subconjunto no
numerable de ω1^V. Su orden heredado tiene tipo ω1^V: cualquier segmento
inicial propio es numerable y el conjunto no lo es. Esto da una biyección
de A con α y, por composición con b_h, con R^M. ∎

Esta ampliación no supone R^V=R^M. El subconjunto A puede ser nuevo
respecto de M; lo que permanece fijado es que sus valores estén en R^M.
El teorema no sustituye R^M por R^V en la conclusión.

**Procedencia:** composición explicitada del rango recuperado, no una
nueva solución de CH ni una afirmación de prioridad matemática.

## 4. Numerabilidad: control de la clasificación por prefijos y profundidad

### 4.1 Los niveles finitos no son niveles cardinales numerables

La normalización N resuelve la elección coherente de un representante.
Consideremos ahora la candidata que clasifica mediante N_n(x), un prefijo
finito, o mediante una cantidad finita de esos registros.

**Teorema R5.** En una carta que publica un intervalo no degenerado, una
clasificación con sólo un conjunto numerable de etiquetas no puede tener
a la vez todas sus fibras de valores numerables y cubrir la carta.

**Prueba.** En V, una unión numerable de conjuntos numerables es
numerable. Si cada etiqueta tuviera una imagen numerable, el conjunto de
valores de la carta sería numerable. El intervalo no lo es. ∎

En particular, el candidato λ(x)=sup_n n=ω, para historias completas
con infinitos niveles, tiene un solo rango y su fibra de valores es toda
la recta. Confundir profundidad con rango no satisface (R2).

Esto no reduce el TPK a un reloj: descarta precisamente las candidatas
que sólo leen profundidad, fase o una cantidad finita de memoria.
Una candidata ordinal que cumpla (R1)–(R3) debe tener imagen no acotada
en ω1^V; cualquier conjunto acotado de ordinales numerables es numerable.

### 4.2 Familia explícita dentro de un mismo prefijo

La carta ternaria y la conjugación Hensel del capítulo 18 permiten dar
un testigo completo, no únicamente un censo finito. Para un prefijo
ternario de longitud n y numerador q, fijemos

\[
 r_{q,\varepsilon}
 =\frac{q}{3^n}+\frac{1}{3^{n+1}}
   +\sum_{k\geq1}\frac{2\varepsilon_k}{3^{n+1+k}},
 \qquad \varepsilon\in\{0,1\}^{\mathbb N}.
\]

Todos esos valores están estrictamente dentro del mismo cilindro de
profundidad n: entre (q+1/3)/3^n y (q+2/3)/3^n.
La cinta se forma con el prefijo q, después un trit 1 y después
los trits 2ε_k. Ψ^{-1} la levanta a la memoria Hensel; la cobertura
superviviente proporciona asimismo historias con esos valores.

Si ε y η difieren por primera vez en k, el término de diferencia
en k tiene módulo 2/3^(n+1+k), y toda la cola posterior tiene módulo
a lo sumo 1/3^(n+1+k). Por tanto

\[
 |r_{q,\varepsilon}-r_{q,\eta}|
 \geq 3^{-(n+1+k)}>0.
\]

Se obtiene una inyección de {0,1}^N dentro del conjunto de valores
del mismo prefijo ternario. Por diagonalización, {0,1}^N no es numerable.
La prueba utiliza historias completas; las instancias finitas de Python
sólo comprueban la fórmula y sus bordes.

La afirmación específica de «mismo prefijo» se refiere a la carta ternaria
publicada, no a identificar retrospectivamente cada sucesión con una
emisión local de Ext. Para los estados supervivientes concretos, R5 da
el control independiente sin imponer una partición que su emisor no use.

### 4.3 No imponer continuidad al rango ordinal buscado

Si λ:Ω→ω1^V fuera continua en las cartas compactas, usando la topología
de orden en ω1, su imagen en cada carta sería compacta y acotada por un
ordinal numerable. Habría sólo una cantidad numerable de niveles.
R5 impediría entonces (R2) y la cobertura simultáneas.
Éste es el control del capítulo 19, extendido de fibras singleton a fibras
de valores numerables.

No demuestra que sea imposible cualquier rango genealógico.
Sí determina que un rango exitoso no puede ser sólo un lector continuo
de prefijos hacia ω1 con esa topología.

## 5. Segunda variación: incorporar la memoria de cada historia al rango

La variación usa los datos de una historia ya producida, no un parámetro
metrológico. Sea b(x) una codificación real de su sucesión numerable de
estados discretos. En el dominio de un registro de frontera efectivo E,D,
esa codificación se recupera también desde E(x). No se afirma aquí que un
registro de dominio menor se haya extendido al atlas entero.
El código común h describe cómo leer estados y extremos de cilindros.

Esta codificación auxiliar no se ofrece como una generación nueva de x:
se usa para examinar el efecto de permitir un parámetro variable en el
rango. Su recuperabilidad, por sí misma, no aporta una conclusión cardinal.

En lugar de L[h], se considera L[h,b(x)]. Cada historia y su valor son
recuperables a partir de h y b(x). Esta variación permite estudiar (R3)
sin exigir que la historia perteneciera a L[h].

**Teorema R6.** Val(x) pertenece a L[h,b(x)] para cada x∈Ω, bajo los
lectores y la reconstrucción efectivos anteriores.

**Prueba.** El modelo contiene el código b(x) y la regla de lectura descrita por h.
La descodificación devuelve la misma sucesión numerable de estados.
Sus extremos racionales de cilindros se calculan desde esa sucesión.
El corte racional del límite queda determinado por

\[
 r^\flat=\{k\in\omega:\exists n\ (q_k<\ell_n(x))\},
\]

para una enumeración fija de Q y los extremos inferiores anidados.
Si q_k<r, la contracción hace que finalmente q_k<ℓ_n(x).
Si q_k≥r, ningún extremo inferior es mayor que q_k. La fórmula
reconstruye el corte completo dentro del modelo. ∎

La existencia del límite se prueba antes mediante los cilindros;
la fórmula del corte no introduce r como dato. Tampoco demuestra que
b(x) pertenezca a L[h]: el parámetro adicional es precisamente la memoria
completa que se decidió conservar.

### 5.1 Prueba conjunta de las condiciones, no sólo cobertura

Para hacer visible el efecto sobre los niveles, definimos

\[
 H_0(h,b)=\operatorname{TC}(\{h,b,\omega,\operatorname{HF}\}),\qquad
 H_1(h,b)=\operatorname{Def}(H_0(h,b)).
\]

HF es el conjunto numerable de los conjuntos hereditariamente finitos.
Su inclusión permite cuantificar sobre las ejecuciones y funciones finitas
que interpretan la aritmética; no se supone que suma y producto sean
definibles usando únicamente el orden de los naturales. Los códigos h,b
son subconjuntos de ω. H_0 es numerable.
H_1 contiene sólo una cantidad numerable de subconjuntos definibles con
fórmulas y una cantidad finita de parámetros de H_0.

El mismo programa aritmético del corte de R6 define r^flat como
subconjunto de H_0, usando h y b como parámetros. Por tanto

\[
 r^\flat\in H_1(h,b(x)).
\]

Una candidata que atribuya a x su primera etapa entre H_0 y H_1 tiene,
pues, valores en {0,1}. Si dos historias del mismo valor dieran etapas
distintas, se puede tomar la menor etapa existente dentro de su fibra
para obtener una etiqueta que dependa sólo del valor. Sigue teniendo
como máximo dos etiquetas.

**Corolario R7.** Esa candidata cubre R^V y puede hacerse constante en
cada fibra, pero al menos uno de sus niveles contiene una cantidad no
numerable de valores.

**Prueba.** La cobertura se sigue de R6 y la fórmula anterior.
Si ambos niveles fueran numerables, R^V lo sería por R5. ∎

El punto exacto es la variación del parámetro b. Cada H_1(h,b) es
numerable por separado; su unión cuando b recorre las memorias completas
no tiene por ello que ser numerable. Omitir b al contar los niveles
perdería la información que se conservó para alcanzar la cobertura.
Conservar b como parte de la etiqueta mantiene el dato, pero deja una
etiqueta real, no un ordinal numerable construido.

Esta conclusión corresponde a esta variación específica de rango.
No se generaliza a toda posible regla del TPK ni modifica el núcleo HMT.

## 6. Balance de los tres requisitos

| Candidata efectivamente desarrollada | Regla y constancia en fibras | Numerabilidad por nivel | Cobertura de valores |
|---|---|---|---|
| Normalización N por sucesores mínimos | Sí, con codominio de historias; no es todavía rango ordinal | Sus etiquetas finitas no la proporcionan | R^V completo |
| Primera aparición λ_h con h fijo | Sí, sobre D_h | Sí, heredada de los niveles de L[h] | R^M, incluidas historias externas que publican valores de M |
| Primera etapa con memoria variable b(x), saturada por fibra | Sí, como etiqueta en {0,1} | No: R7 demuestra una fibra no numerable | R^V completo |

Se han trabajado los tres requisitos, pero ninguna de estas candidatas
satisface simultáneamente (R1), (R2) y (R3) sobre R^V.
El resultado positivo adicional es R4: ya se controlan los subconjuntos
externos del portador R^M, además de los pertenecientes a M.

El problema residual queda situado en los valores de R^V\R^M, no en
subconjuntos nuevos formados exclusivamente por valores del portador conocido.
La vía de reindexación del expediente anterior permanece íntegra.

La próxima construcción tendría que reemplazar el parámetro variable b por
una jerarquía ordinal con imágenes de valores numerables, demostrando que
cubre cada fibra nueva. No basta conservar b y renombrarlo «rango», ni
declarar agotada una fibra al enumerar sus prefijos. Este expediente no
construye todavía esa jerarquía y no declara CH universal.

## 7. Procedencia, comprobación y conservación

Antecedentes recuperados: cobertura, contracción, conjugación Hensel, memoria
con inversa y rango constructible con h fijo. Formalizaciones en esta nota:
selección mínima de cada fibra, extensión a D_h, cuantificador de R4 y
análisis de las dos candidatas de niveles. No se reclama novedad histórica
de los argumentos elementales de selección o cardinalidad.

El programa adjunto comprueba normalización ternaria, convenciones de
frontera y familias finitas de la construcción de R5. No ejecuta el
generador completo, no decide pertenencia a L[h] y no verifica CH.
Las pruebas generales son las anteriores, no sus muestras finitas.

No se han modificado PDFs ni archivos fuente compartidos. Se conserva el
expediente anterior y se comprueban sus hashes antes de reutilizarlo.
La autocomprobación causal y el núcleo formal pasan. En esta ejecución,
el arranque del proyecto pasa; el resolutor global devuelve
FAIL_ULTIMA_AUTORIDAD_HMT_MD expected_one_mass_non_regression_witness.
No se modifica ese índice global ajeno a esta derivación ni se declara
una nueva edición integral sellada. La selección autoral sigue siendo el
integral de 2249 páginas y sus propietarios focales verificados.

## 8. Fuentes

- [Capítulo 18: cobertura, fibras y atlas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c18_sin_encabezado.tex:92>); carta Hensel y ternaria desde línea 440.
- [Capítulo 19: rango, límites del lector continuo y L[h]](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c19_sin_encabezado.tex:537>).
- [Capítulo 9: minimización finita en un lector posterior](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c09_sin_encabezado.tex:2011>). No se identifica su mínimo de certificación con un rango cardinal.
- [Expediente previo: potencia plena, rango y reindexación](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/PLEGADO_MEMORIA_CARDINALIDAD_20260910.md:388>).
- [Reconstrucción de memoria antecedente](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/ACOPLAMIENTO_PRESENTE_Y_RECONSTRUCCION_20260910.md>).
- [Corpus activo](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/CORPUS_ACTIVO.md>).

Se trata de una lectura focal con pruebas y candidatos específicos, no de
una auditoría integral de cada afirmación de los PDFs.


## 9. Composición completa como regla: síntesis fiel y prueba de su tipo

### 9.1 Dirección autoral y procedencia

Formulación literal recibida:

> pues para mi esa regla es APP+TRIT+TPK+estado enriquezido+la estrcutura discreta del continuo. que ella se pueda sintetizar mas , seguro, pero es sólo eso, hacerla y listo

La arquitectura indicada es preexistente. Esta sección reúne su escritura
operatoria; no atribuye al agente una generación nueva ni añade una premisa
física o una selección de cifras. Se mantienen conjuntamente las cinco
construcciones del continuo ya heredadas.

El propietario del estado común escribe cada estado con células, ambas hojas,
residuos, cocientes, orientación, carry, reloj, memoria, frontera, ruta y
ledger. Las emisiones se conservan con su procedencia: coincidir en la célula
terminal no identifica dos historias.

### 9.2 Fórmula compacta del mecanismo, conservando sus tipos

La transición canónica del TPK es

\[
 U_t=\operatorname{Upd}_t\circ\operatorname{Tra}_t
                         \circ\operatorname{Sel}_t.
\]

Selección, transporte y actualización actúan sobre el estado enriquecido.
No se sustituye esta transición por su publicación reducida de Markov.

En el árbol completo del propietario, escribimos las operaciones de emisión
como \(\epsilon_*\). Su acción se obtiene de las reglas APP, TRIT y TPK,
incluida la actualización de la pareja de hojas y del ledger. La formulación
recursiva es

\[
 \widehat X_0=\{\text{estados iniciales producidos por APP–TRIT–TPK}\},
\]
\[
 \widehat X_{k+1}
 =\{\epsilon_*x:\ x\in\widehat X_k,\ 
                    \epsilon\in\operatorname{Out}_k(x)\},
 \qquad \rho_{k+1,k}(\epsilon_*x)=x.
\]

La realización completa es

\[
 \boxed{\quad
 \mathcal G_H=\varprojlim_k(\widehat X_k,\rho_{k+1,k}),
 \qquad
 Q_H=\mathcal G_H/{\sim_{\rm Val}}.
 \quad}
\]

Para la recta entera se usa el atlas numerable de cartas ya construido.
El código de una carta se conserva al aplicar las fórmulas.

No se igualan los índices \(t\), \(K\) y \(k\), ni una emisión genérica del
árbol con una arista del catálogo nonádico. La síntesis mantiene esa distinción
de sus propietarios; no crea una identificación arista a arista que ellos
no hayan utilizado.

El paso al límite conserva la historia y su ledger completo. Val actúa
después sobre ella; el cociente sólo identifica los valores cuando ése sea
el objeto preguntado. Las demás publicaciones del estado no se eliminan.

### 9.3 Recodificación íntegra, con inversa y compatibilidad

Cada \(\widehat X_k\) es finito. Ordenando sus códigos completos se obtiene
una biyección de representación

\[
 \iota_k:\widehat X_k\longrightarrow C_k
       =\{0,\ldots,|\widehat X_k|-1\}.
\]

Esta ordenación no cambia la admisibilidad, no selecciona una continuación
ni se presenta como un orden físico privilegiado. Se define

\[
 \widehat\rho_{k+1,k}
       =\iota_k\circ\rho_{k+1,k}\circ\iota_{k+1}^{-1},
\]
\[
 \operatorname{Code}(x)
       =(\iota_k(x_k))_{k\geq0}.
\]

**Teorema R8.** Code es una biyección

\[
 \mathcal G_H\longleftrightarrow
       \varprojlim_k(C_k,\widehat\rho_{k+1,k}).
\]

Su inversa reconstruye cada estado completo mediante
\(x_k=\iota_k^{-1}(c_k)\). Ambas aplicaciones conmutan con las restricciones.
Ningún campo del estado se identifica con su resumen escalar.

**Prueba.** Si \(x\) es compatible, entonces

\[
 \widehat\rho_{k+1,k}(\iota_{k+1}x_{k+1})
 =\iota_k\rho_{k+1,k}x_{k+1}
 =\iota_kx_k.
\]

Recíprocamente, una sucesión de códigos compatible produce estados
compatibles al aplicar las inversas de las \(\iota_k\). Las composiciones
son la identidad en cada nivel y, por tanto, sobre cada historia. ∎

Para cualquier operación tipada \(F:X_k\to X_j\) ya construida en el
dominio correspondiente, su expresión en códigos es exactamente

\[
 \widehat F=\iota_j F\iota_k^{-1},
 \qquad \widehat F\iota_k=\iota_jF.
\]

Esta igualdad es un transporte de representación, no una prueba nueva de F.
Cuando F tiene compatibilidad de refinamiento acreditada, la misma igualdad
la conserva en el límite. Incluye las acciones reversibles y las
actualizaciones con memoria en sus respectivos dominios.

La regla completa puede así escribirse compactamente sin sustituirla por
APP mínima, un prefijo, una cifra ni un registro de menor alcance.

### 9.4 Qué prueba esta síntesis respecto del rango

Code tiene por salida una sucesión completa de enteros finitos, es decir,
un código en \(\omega^\omega\), sujeto a compatibilidad. Eso no lo convierte
en un elemento de \(\omega_1\). Son tipos de objeto diferentes.

La composición con la normalización del teorema R1 da

\[
 \operatorname{Code}\circ N:
 \Omega\longrightarrow\varprojlim_k(C_k,\widehat\rho_{k+1,k}),
\]

con la carta explícita cuando haga falta, y satisface

\[
 (\operatorname{Code}N)(x)=(\operatorname{Code}N)(y)
       \ \Longleftrightarrow\ \operatorname{Val}(x)=\operatorname{Val}(y).
\]

Se obtiene, por tanto, un código completo separador de valores con cobertura
ambiente. No se ofrece este hecho de recodificación como una demostración
de CH.

**Control exacto sobre la etapa de construcción.** Si se etiqueta cada
historia completa por el paso de completar simultáneamente sus niveles
finitos —denotado aquí \(\omega\)—, la etiqueta es la misma para cada
historia de esa completación. Su nivel de valores contiene el intervalo
completo de la carta por la cobertura heredada. No es numerable.

Este control no identifica la memoria TPK con \(\omega\), ni asigna un
tiempo límite al reloj. Examina únicamente la candidata que usa como rango
la etapa expositiva de la completación. La historia completa permanece
distinta y recuperable mediante Code.

### 9.5 Composición cardinal que sí bastaría y estado de esta aplicación

Sobre los códigos normalizados, una relación \(\prec_H\) obtenida del
mecanismo completo cerraría el objetivo si se demuestra que:

1. es un buen orden sobre la totalidad del cociente de valores;
2. cada segmento inicial estricto es numerable.

Entonces, sin imponer un ordinal como entrada, se publicaría

\[
 \lambda_H([x])
   =\operatorname{otp}
       \{[y]\in Q_H:[y]\prec_H[x]\}<\omega_1.
\]

Los segmentos iniciales de dos elementos diferentes tienen tipos distintos,
de modo que \(\lambda_H\) sería inyectiva. La cobertura ya reunida trasladaría
esa inyección a la recta ambiente. Ésta es una implicación probada: no se
afirma haber construido en esta sección una relación con ambas propiedades.

La respuesta constructiva a la dirección autoral es R8 y la fórmula de
\(\mathcal G_H\): la composición completa está reunida, sin quitar
coordenadas, y puede transportarse fielmente entre representaciones.
El cierre ordinal universal no se deduce solamente de esa recodificación.
La propiedad aún no acreditada por los intentos de este expediente es la
ordenación global con segmentos iniciales numerables, no la existencia del
mecanismo APP–TRIT–TPK.

### 9.6 Localizadores y alcance

- [Estado completo, dominio generado y finitud](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/fuentes/integral/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:744>).
- [Multisección completa y no vacuidad](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/fuentes/integral/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:1239>).
- [Transición canónica y campos conservados](</Users/ruben/Documents/New project/PUBLICACION_HMT/REGISTRO_DE_CONTINUIDAD_ACADEMICA/NUCLEO_FORMAL_HMT_PERMANENTE/TPK_GRAFO_OPERATORIO_TIPADO.json:1151>).
- La cobertura y los propietarios cardinales son los de la sección 8.
- R8 es una formalización de recodificación y conjugación de mapas ya
  construidos, no una afirmación de novedad histórica ni un nuevo generador.
- No se han recalculado decimales, modificado PDFs ni contactado otras tareas.


## 10. Trabajo sobre el orden y las prolongaciones del estado íntegro

Esta sección cambia de tarea respecto de R8: no vuelve a recodificar el
estado. Examina tres construcciones concretas de orden o selección sobre
el espacio completo que el corpus ya proporciona. No modifica las fuentes
ni los PDFs; tampoco atribuye a esta lectura una auditoría de cada resultado
del tratado.

### 10.1 Base operatoria efectivamente considerada

Se han leído los dominios, codominios, acciones, dependencias y campos
conservados de los 39 nodos del grafo permanente: OP01–OP34, M_PH,
SEL_T, TRA_T, UPD_T y U_T. Se ha considerado también la construcción
conjunta G_cont, con sus cinco aspectos inseparables, como antecedente
heredado. Este inventario de lectura no se presenta como una nueva prueba
de sus 39 definiciones ni del corpus global.

Para el problema de rango se distinguen las acciones siguientes:

- Las divisiones APP y TRIT, los emisores, los prefijos, las firmas finitas,
  el reloj y los registros finitos no se confunden con historias completas.
  Una regla que sólo lea uno de esos registros finitos tiene a lo sumo una
  cantidad numerable de etiquetas posibles. Se aplica R5, aunque se
  conserve el estado completo aparte.
- H, Ext, U_t y Γ_9 conservan compatibilidad y prolongan el estado. Su acción
  se usa sobre el árbol íntegro, no mediante K_ph desligado de la memoria.
- X_chi y la multisección contienen las prolongaciones completas. Aquí es
  donde se estudian el orden de ledgers y los rangos de eliminación.
- Los lectores y las cinco construcciones correlativas posteriores se
  conservan sobre ese antecedente. No se presupone que sus codominios
  sean ordinales, ni que una acción reversible defina un buen orden.

El propietario 04b1 determina Out(x) mediante la actualización conjunta
del estado completo, mantiene diferentes las rutas con ledgers diferentes
y prueba finitud, no vacuidad y sobreyectividad de las restricciones.
El capítulo 18 proporciona las identidades exactas de cobertura de sus
cilindros. El capítulo 19 conserva la doble dirección temporal, el orden
genealógico y la clausura constructible, cada uno con su tipo.

Trabajamos en una carta compacta X de historias completas, con
\(f=\operatorname{Val}:X\to K=[a,b]\) continua y sobreyectiva, a<b.
Cada cilindro es abierto y cerrado en X. Las pruebas siguientes mantienen
el estado que porta sus puntos; no convierten X en un espacio de cifras
sin memoria. El universo ambiente V y el uso de elección son los de §1.

### 10.2 Subárbol de historias con valores separados

**Teorema R9.** Dentro de cualquier cilindro cuyo intervalo publicado sea
no degenerado puede construirse un subárbol binario de prolongaciones
admisibles, con aplicaciones

\[
 j_X:2^{\mathbb N}\longrightarrow X,\qquad
 j_R=f\circ j_X:2^{\mathbb N}\longrightarrow K
\]

continuas e inyectivas. Las historias conservan cada coordenada enriquecida.

**Construcción y prueba.** Partimos de una palabra admisible u cuyo
intervalo I(u)=[l,v] tiene longitud L>0. Tomamos dos intervalos abiertos
con cierres disjuntos en su interior, por ejemplo

\[
 J_0=(l+L/8,l+3L/8),\qquad
 J_1=(l+5L/8,l+7L/8).
\]

La cobertura iterada del corpus da

\[
 I(u)=\bigcup_{w\succeq u,\ |w|=N}I(w).
\]

Se aumenta N hasta que la cota uniforme de diámetros sea menor que L/32
y que \(2^{-|s|-2}\), donde s es la dirección binaria construida hasta
ese paso. Los descendientes que cubren un pequeño intervalo cerrado
alrededor del centro de J_i quedan contenidos en J_i. Como son una
familia finita y cubren un intervalo no degenerado, al menos uno tiene
longitud positiva. Se elige el primero de esos descendientes según la
codificación finita de sus emisiones. Así se obtienen u_{s0},u_{s1}.

Se repite la operación. Para cada dirección binaria β, las palabras
u_{β|n} son compatibles y sus longitudes tienden a infinito. Su unión
es una historia admisible, por la definición de multisección y las
restricciones heredadas. Los intervalos anidados tienen diámetros que
tienden a cero, de modo que publican un valor único.

Dos direcciones que se separan en un vértice tienen valores en intervalos
hermanos disjuntos. Por tanto, las dos aplicaciones son inyectivas.
La compatibilidad de prefijos y las cotas de diámetros dan continuidad.
Las emisiones, el carry, la frontera y el ledger son los de cada estado
producido; no se reconstruyen retrospectivamente desde el valor. ∎

Los intervalos J_i son una selección posterior para construir un testigo
de separación dentro del sistema ya generado. No seleccionan las semillas
ni las constantes HMT. El procedimiento utiliza la cobertura acreditada;
no se afirma aquí haber ejecutado un enumerador del árbol entero.

### 10.3 El orden lexicográfico del ledger no es un buen orden

**Teorema R10.** El orden por primera emisión diferente de los ledgers
completos admite una cadena estrictamente descendente de historias cuyos
valores también son diferentes.

**Prueba.** En cada bifurcación de R9, llamamos 0 a la prolongación
lexicográficamente menor y 1 a la mayor. Los prefijos son incompatibles
porque sus intervalos publicados son disjuntos. Esta eventual permutación
de nombres no cambia las historias ni sus valores.

Sea \(x_n=j_X(0^n10^\infty)\). Por comparación en la primera bifurcación
distinta,

\[
 x_{n+1}<_{\rm lex}x_n\qquad(n\geq0).
\]

R9 demuestra a la vez que \(f(x_n)\neq f(x_m)\) para n≠m.
Por consiguiente, el descenso no se elimina identificando solamente
historias de igual valor. Un ordinal que preservase esta comparación
produciría una sucesión estrictamente descendente de ordinales, lo cual
contradice su buen fundamento. ∎

Éste es un falsador de esta comparación precisa. No afirma que ninguna
otra relación construida desde HMT pueda ordenar el cociente.

### 10.4 Eliminación transfinita de historias aisladas

Se considera ahora una candidata de rango más fuerte que la profundidad
finita: la eliminación transfinita de puntos aislados en el espacio de
estados íntegros. Para F cerrado en X, sea D(F) su conjunto de puntos de
acumulación. Definimos

\[
 X^0=X,\qquad X^{\alpha+1}=D(X^\alpha),\qquad
 X^\lambda=\bigcap_{\alpha<\lambda}X^\alpha.
\]

**Teorema R11.** El proceso se estabiliza en un ordinal numerable α*.
Su núcleo P=X^{α*} cumple

\[
 X\setminus P\text{ es numerable},\qquad f(P)=K.
\]

Además, cada homeomorfismo de X inducido por una familia coherente de
simetrías reversibles de estados conserva P y los estratos de eliminación.

**Prueba.** X tiene una base numerable de cilindros. Si x se elimina en
la etapa α+1, hay un cilindro básico B tal que
\(B\cap X^\alpha=\{x\}\). Elegimos el de menor índice.

Un mismo B no puede ser elegido para dos puntos eliminados: en la misma
etapa sólo aísla uno, y después de esa etapa ya no contiene ningún punto
de la sucesión decreciente. Esta asignación inyecta el conjunto de puntos
eliminados en la base numerable.

Si el proceso no se estabilizara antes de ω1, en cada etapa sucesora se
eliminaría al menos un punto y se obtendrían no numerablemente muchos
cilindros básicos diferentes, contradicción. Una igualdad
\(X^{\alpha+1}=X^\alpha\) es un punto fijo y persiste en cada etapa
posterior. No aparecen pérdidas nuevas por primera vez en una etapa
límite: no pertenecer a una intersección significa haber faltado ya en
alguna etapa anterior. Esto prueba estabilización y numerabilidad del
complemento.

P es compacto. Por tanto f(P) es cerrado en K. Cada valor que no esté en
f(P) tiene una preimagen en X\P, luego K\f(P) es numerable. Pero es además
abierto relativo en un intervalo no degenerado: si fuera no vacío,
contendría un intervalo no degenerado y sería no numerable. Por tanto
f(P)=K.

Finalmente, un homeomorfismo preserva los puntos aislados, el derivado y
las intersecciones. Una inducción transfinita da
\(g[X^\alpha]=X^\alpha\) y \(g[P]=P\). La familia coherente de biyecciones
finitas del grupoide HMT y su inversa inducen precisamente un homeomorfismo
en el límite. No se aplica esta afirmación a un lector no invertible. ∎

Así, incluso con memoria completa, el núcleo no eliminado sigue publicando
el intervalo entero. Asignarle una sola etiqueta ∞ no satisface la
numerabilidad por nivel. Asignar a un valor el menor rango eliminado de
alguna de sus historias sólo alcanza a lo sumo una cantidad numerable de
valores, pues las historias eliminadas son numerables.

El teorema no exige destruir la memoria para obtener esa conclusión:
las transformaciones reversibles que la conservan transportan el mismo
problema de rango.

### 10.5 Una vía de selección por prolongaciones, sin empezar por ordinales

Para A⊆K consideramos el siguiente juego de prueba sobre el árbol completo.
No es un nuevo generador de A, sino un examen de selección de historias:

- Desde el prefijo actual, el participante I propone dos prolongaciones
  admisibles con intervalos disjuntos, longitud estrictamente mayor y
  diámetro a lo sumo \(2^{-n}\) en el turno n.
- El participante II elige una de ellas, que pasa a ser el prefijo actual.
- Si I no puede proponer esa pareja, pierde. En una partida infinita,
  las prolongaciones compatibles publican un valor r. I gana si r∈A;
  II gana si r∉A.

Se puede usar una raíz auxiliar que reúna las finitísimas raíces de la
carta. No se omite por ello ninguna historia. Se permiten intervalos
degenerados entre las propuestas; si II escoge uno que no admite una
pareja posterior, I pierde.

**Teorema R12.** Para este juego:

\[
 I\text{ tiene estrategia ganadora}
 \ \Longrightarrow\ A\text{ contiene una copia perfecta de }2^{\mathbb N};
\]
\[
 II\text{ tiene estrategia ganadora}
 \ \Longrightarrow\ A\text{ es numerable}.
\]

**Prueba de la primera implicación.** Una estrategia ganadora de I
proporciona una pareja legal después de cada sucesión finita de elecciones
de II; ninguna de esas partidas se atasca. Las elecciones binarias forman
un árbol completo. Sus historias límite publican valores de A.
Los intervalos disjuntos prueban inyectividad y los diámetros decrecientes
prueban continuidad. La imagen de \(2^{\mathbb N}\), compacta y sin
puntos aislados, es un subconjunto perfecto de A.

**Prueba de la segunda implicación.** Fijemos una estrategia ganadora σ
de II. Hay sólo numerablemente muchas posiciones finitas, porque cada
posición consiste en una lista finita de prefijos de un árbol numerable.

En una posición p llamamos bloqueado a un valor r del cilindro actual si
ninguna pareja legal consigue que σ elija una prolongación que contenga r.
En cada posición hay a lo sumo un valor bloqueado. En efecto, si r≠s
fueran ambos bloqueados, la cobertura y la contracción producirían dos
prolongaciones con intervalos disjuntos que contengan respectivamente r
y s. σ debe elegir una: el valor contenido en la elegida no estaría
bloqueado, contradicción.

Ahora sea r∈A. Si nunca se bloqueara siguiendo σ, se podría elegir
recursivamente una pareja cuya respuesta por σ conserve r. La primera
pareja disponible en una enumeración fija basta como selección matemática.
Se obtendría una partida infinita, compatible con σ, cuyos intervalos
contienen r y cuyo valor final es r. Eso contradice que σ gane.

Por tanto, cada r∈A se bloquea en alguna posición finita. Hay a lo sumo
un valor bloqueado por posición y numerablemente muchas posiciones;
A es numerable. ∎

En consecuencia, si este juego particular está determinado para A,
se obtiene la dicotomía cardinal buscada para A. Las dos implicaciones
son pruebas sobre el árbol completo; la existencia de una estrategia
ganadora no se presupone.

### 10.6 Prueba del alcance exacto de esa vía sobre la potencia plena

**Teorema R13, con elección en V.** Existe A⊆K para el que ninguno de
los dos participantes del juego de R12 posee estrategia ganadora.
Ese A tiene cardinal del continuo. Esto no refuta CH.

**Construcción y prueba.** Escribamos κ=|K|. Cada cerrado de K se codifica
por los elementos de una base numerable contenidos en su complemento:
la unión de esos elementos recupera exactamente ese abierto. Por tanto,
hay a lo sumo κ cerrados. Hay al menos κ perfectos no vacíos:
los intervalos [a,t], con a<t≤b, proporcionan esa cantidad. Enumeramos
entonces los perfectos no vacíos como \((P_\xi)_{\xi<\kappa}\).

Cada P_ξ tiene cardinal κ. Para comprobar la desigualdad inferior, en
cada abierto relativo no vacío de P_ξ se eligen dos abiertos relativos
con cierres disjuntos y diámetros decrecientes; la ausencia de puntos
aislados permite repetir el proceso y produce una copia de \(2^\mathbb N\).
La desigualdad superior procede de P_ξ⊆K.

Por recursión, elegimos dos puntos distintos a_ξ,b_ξ∈P_ξ que no hayan
sido elegidos antes. Es posible porque en la etapa ξ se han usado a lo
sumo \(2|\xi|<\kappa\) puntos y P_ξ tiene cardinal κ. No se presupone
regularidad de κ. La elección se realiza usando un buen orden auxiliar
de K; no se atribuye ese orden al generador HMT.

Ponemos \(A=\{a_\xi:\xi<\kappa\}\). Sus puntos son distintos, por lo que
|A|=κ. Cada perfecto no vacío intersecta A y su complemento, pues
contiene los puntos a_ξ y b_ξ correspondientes. En particular, A no
contiene ningún perfecto no vacío.

Si I tuviera estrategia ganadora, R12 proporcionaría un perfecto dentro
de A, contradicción. Si II la tuviera, R12 haría A numerable, también
contradicción. ∎

La construcción anterior es un control de la pretensión «cada subconjunto
admite esta estrategia de selección». No es una entrada del generador HMT,
no es una refutación de la cobertura del continuo y no es un conjunto de
cardinal intermedio: su cardinal es precisamente κ. Por eso no puede
utilizarse para afirmar ¬CH.

Lo que excluye es cerrar CH universal afirmando, sin una prueba adicional,
que la selección por este juego funciona sobre cualquier subconjunto.
El éxito de la fusión en la clase analítica del capítulo 19 conserva
íntegro su estatuto.

### 10.7 Resultado de este tramo de investigación

Se han obtenido pruebas completas para tres intentos concretos:

1. El orden lexicográfico de la genealogía íntegra falla el buen fundamento
   mediante historias admisibles de valores distintos (R9–R10).
2. El rango por eliminación transfinita conserva niveles eliminados
   numerables, pero su núcleo restante publica aún todo el intervalo;
   las simetrías reversibles conservan este resultado (R11).
3. La selección por prolongaciones da la dicotomía cuando hay estrategia;
   no existe tal estrategia para cada subconjunto bajo elección
   (R12–R13). El control adversarial no depende de ¬CH.

Estas conclusiones no se extrapolan a una imposibilidad global de HMT,
ni se sustituyen por una afirmación de que ya esté construida la ordenación
ordinal ambiente. Los lemas heredados de L[h] y la ampliación R4 permanecen
intactos. El cierre universal solicitado no ha sido demostrado en este
expediente.

Procedencia: la arquitectura y la dicotomía analítica son recuperadas del
corpus. Las pruebas aquí reunidas aplican argumentos de orden, topología
y selección al árbol íntegro; no se reclama novedad histórica de esos
argumentos. La clasificación de posibles antecedentes adicionales en
otras fuentes permanece distinta de la prueba de estos intentos.

Localizadores adicionales:

- [Out, árbol íntegro y realización de Γ_9](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/fuentes/integral/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:922>).
- [Grupoide reversible y compatibilidad de estados](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/fuentes/integral/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:853>).
- [Publicaciones analíticas y prueba de fusión](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c19_sin_encabezado.tex:285>).
