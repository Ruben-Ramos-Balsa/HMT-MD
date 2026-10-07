# Acoplamiento reversible, conservación de forma y memoria no estacionaria

Continuación aditiva, 12 de septiembre de 2026. Se conservan íntegramente la propuesta del cristal aperiódico, las notas anteriores y los PDF. El desarrollo retoma el balance de forma, componente terminal y complementos registrados, y construye su extensión a memoria entrante y transportes variables.

## 1. Antecedentes y alcance causal

APP genera sobre las mismas marcas horizontales y verticales las hojas aditiva y multiplicativa, con residuo y cociente. El TRIT orienta la emisión y su acarreo. El TPK compone selección, transporte y actualización de memoria; su prolongación w6→w12→w18→w24→w30→R36→G9 conserva los antecedentes de cada etapa.

El estado enriquecido contiene hoja, orientación, residuo, cociente, acarreo, ruta, frontera, memoria y supervivencia. El constructor conjunto produce sus operaciones espectral, solenoidal, de calibre, cohomológica y determinantal sobre la misma historia, con naturalidad y límite común. Las realizaciones siguientes se aplican a transportes y lectores de esa construcción; no constituyen cinco estados separados.

Las coordenadas π_HMT, φ_HMT, e_HMT y α_HMT, y el registro dodecafásico K, son salidas de sus lectores tipados. Su genealogía común conserva el orden constructivo de cada evaluación. El álgebra de operadores interviene como lenguaje de prueba posterior y no selecciona las emisiones mediante cifras objetivo.

La carta nonádica documentada utiliza nueve copias, una inclusión uniforme normalizada por 1/3 y un único patrón colectivo de diferencia entre la posición portadora del transporte E y las otras ocho posiciones. El balance y la compresión están en el integral [F1]. El transporte entre formas y su primera columna (T,D) están demostrados en [N1]. La incidencia completa de K está en [N3].

**Procedencia:** la conservación y su arquitectura son resultados preexistentes. Son formalizaciones añadidas en este expediente la segunda columna del acoplamiento, su composición con reentrada, el terminal positivo general no estacionario y la discriminación entre agotamiento y recuperación. La conjugación matricial y el análisis de operadores son métodos conocidos; no se reivindica prioridad matemática universal.

## 2. Extensión reversible del balance entre dos formas

Sean B,C:V→V′ isomorfismos que conservan una forma no degenerada b entre dos realizaciones:

\[
B^*b'B=C^*b'C=b.
\]

La forma puede ser una métrica positiva o una forma alternante. En espacios reales * denota transposición respecto de las coordenadas elegidas; la igualdad formula el transporte de la forma, no una elección de métrica común a regímenes distintos. En Hilbert se exige además que los operadores e inversos sean acotados.

Con s=√8 y Q_V=1/3 [[sI,−I],[I,sI]], definimos

\[
\boxed{
\mathcal U(B,C)=Q_{V'}^*\operatorname{diag}(B,C)Q_V
=\frac19\begin{pmatrix}8B+C&\sqrt8(C-B)\\\sqrt8(C-B)&B+8C\end{pmatrix}.}
\tag{1}
\]

Escribimos T=(8B+C)/9, D=√8(C−B)/9, R=(B+8C)/9. La actualización completa es

\[
\binom{x'}{m'}=\begin{pmatrix}T&D\\D&R\end{pmatrix}\binom{x}{m}.
\tag{2}
\]

**Teorema 1.** La aplicación (1) es reversible y conserva b⊕b:

\[
\mathcal U(B,C)^*(b'\oplus b')\mathcal U(B,C)=b\oplus b,
\quad\mathcal U(B,C)^{-1}=\mathcal U(B^{-1},C^{-1}).
\tag{3}
\]

**Prueba.** Q*Q=I por 8+1=9. Sus bloques escalares hacen que Q preserve b⊕b para cualquier b. La aplicación diagonal conserva las formas por hipótesis. La composición prueba (3), y la inversión de los tres factores da la inversa declarada. ∎

Para memoria entrante m=0, se recupera exactamente el balance anterior b=T*b′T+D*b′D. La segunda columna determina la respuesta a memoria entrante arbitraria. Una igualdad positiva de normas y una igualdad de área orientada son especializaciones distintas de (3).

### Residencia exacta en las nueve copias

En V⁹, sea W_E=diag(I,…,I,E), con E en la novena posición. Sea A(a,b)=(a/√8,…,a/√8,b) y L=AQ. Entonces L(x,0)=Jx y

\[
W_E L=L\mathcal U(I,E).
\tag{4}
\]

**Prueba.** W_E A=A diag(I,E); multiplicar por Q y usar AQ=L da (4). La ortogonalidad de la media de las ocho primeras posiciones con sus siete diferencias muestra además que el complemento queda fijo bajo W_E. ∎

El paso cíclico original es S_E=P_cyc W_E. Por ello S_E L=(P_cyc L)U(I,E), con cartas de entrada y salida distintas. La reducción colectiva conserva el patrón correspondiente y no identifica las iteraciones de S_E con las de W_E: S_E⁹=I₉⊗E, mientras W_E⁹=diag(I₈,E⁹). Cuando un lector utiliza las nueve etiquetas individuales, éstas se conservan en su representación original.

## 3. Composición exacta y reentrada de memoria

Para B₁,C₁:V₀→V₁ y B₂,C₂:V₁→V₂,

\[
\boxed{\mathcal U(B_2,C_2)\mathcal U(B_1,C_1)
=\mathcal U(B_2B_1,C_2C_1).}
\tag{5}
\]

**Prueba.** En (1) se cancelan Q_V₁Q_V₁*, y los dos bloques diagonales se multiplican en el orden indicado. No se utiliza conmutación entre etapas. La inducción extiende la fórmula a cualquier número finito de transportes. ∎

El bloque de lectura contiene la identidad

\[
\boxed{T_2T_1+D_2D_1=\frac{8B_2B_1+C_2C_1}{9}.}
\tag{6}
\]

Desde (x,0), la primera etapa produce (T₁x,D₁x). La segunda lectura es T₂T₁x+D₂D₁x. El segundo término es exactamente la contribución de la memoria reintroducida. Al almacenar D₁x fuera del siguiente acoplamiento y continuar sólo con T₁x se obtiene otro procedimiento, cuya lectura es T₂T₁x. El balance previo para registros separados sigue válido; (6) precisa la diferencia entre ambos procedimientos.

La realización U conserva el estado de este acoplamiento y los productos ordenados B_N⋯B₁, C_N⋯C₁. Estos productos por sí solos no recuperan cada factor de una historia. La conservación de todos los prefijos requiere mantener también el registro de emisiones ya presente en HMT.

### Ecuación covariante de incremento

Para registro separado x_{n+1}=T_nx_n, m_n=D_nx_n se tiene, exactamente,

\[
x_{n+1}-B_nx_n=m_n/\sqrt8.
\tag{7}
\]

Con G₀=I y G_{n+1}=B_nG_n, la telescopía da

\[
x_0=G_N^{-1}x_N-\frac1{\sqrt8}\sum_{n<N}G_{n+1}^{-1}m_n.
\tag{8}
\]

La memoria es, en esta realización, el incremento respecto del transporte entre formas B_n, con normalización determinada. (8) es una reconstrucción finita algebraica; su paso a una serie infinita requiere convergencia. El teorema positivo siguiente construye una inversa estable sin presuponer ese límite vectorial.

## 4. Memoria de una sucesión no estacionaria

En una realización de Hilbert H, sean C_n unitarios, sin hipótesis de conmutación. Escribimos

\[
T_n=(8I+C_n)/9,\quad D_n=\sqrt8(C_n-I)/9,
\quad P_0=I,\quad P_{n+1}=T_nP_n,\quad A_N=P_N^*P_N.
\]

El índice N cuenta compresiones con almacenamiento separado. No designa el transporte completo con reentrada de §3. Para métricas variables con B_n isomorfismos isométricos, la conjugación por G_n lleva los transportes a un Hilbert fijo y produce este mismo caso, con C̃_n=G_{n+1}^{−1}C_nG_n. La afirmación utiliza las métricas de sus fibras; no las sustituye por una norma euclídea común sin cotas.

**Teorema 2.** Existe un operador positivo 0≤A_∞≤I, límite fuerte de A_N, y

\[
\boxed{I=A_\infty+\sum_{n\ge0}P_n^*D_n^*D_nP_n.}
\tag{9}
\]

La aplicación

\[
\boxed{\mathcal Vv=(A_\infty^{1/2}v,(D_nP_nv)_{n\ge0})}
\tag{10}
\]

es isométrica y tiene inversa izquierda estable

\[
\mathcal V^*(a,(m_n))=A_\infty^{1/2}a+
\sum_{n\ge0}P_n^*D_n^*m_n,\qquad\|\mathcal V^*\|=1.
\tag{11}
\]

**Prueba.** La identidad local T_n*T_n+D_n*D_n=I da A_N−A_{N+1}=P_N*D_N*D_NP_N≥0. La sucesión positiva decreciente y acotada tiene límite fuerte A_∞: las formas cuadráticas convergen a la de un operador positivo, y para B_N=A_N−A_∞ se tiene 0≤B_N²≤B_N, lo que convierte la convergencia de formas en fuerte. La telescopía finita y ese límite prueban (9). Evaluar sobre v prueba la isometría (10). Su adjunto es (11); la serie converge en norma porque las truncaciones de un registro cuadrado-sumable convergen y el adjunto es acotado. ∎

La reconstrucción con el terminal límite y N registros tiene error exacto (A_N−A_∞)v. El resultado no presupone que P_N converja. A_∞^{1/2}v es la realización positiva canónica del terminal de norma, no un supuesto límite de x_N.

## 5. Tres propiedades diferentes: agotamiento, distinción y estabilidad

Sea Mv=(D_nP_nv)_n. De (9), M*M=I−A_∞. Por tanto:

1. Toda la norma de v pasa al registro exactamente cuando A_∞v=0.
2. El registro distingue cada estado exactamente cuando ker(I−A_∞)={0}.
3. La recuperación desde memoria sola tiene inversa acotada exactamente cuando I−A_∞≥εI para algún ε>0. En ese caso una inversa izquierda es (I−A_∞)^{-1}M*.

Además,

\[
\boxed{\ker M=\bigcap_{n\ge0}\operatorname{Fix}(C_n).}
\tag{12}
\]

**Prueba.** Si Mv=0, D₀v=0 implica C₀v=v y P₁v=v. Inductivamente D_nP_nv=0 da C_nv=v y P_{n+1}v=v. El recíproco es inmediato. Las tres equivalencias se deducen del operador de Gram M*M y de la caracterización de operadores acotados inferiormente. ∎

### Ejemplo exacto que separa las tres propiedades

En el ensayo algebraico C₀=−I y C_n=I para n≥1,

\[
A_\infty=\frac{49}{81}I,\qquad M^*M=\frac{32}{81}I,
\qquad m_0=-\frac{2\sqrt8}{9}v,
\qquad v=-\frac9{2\sqrt8}m_0.
\tag{13}
\]

La memoria contiene 32/81 de la norma al cuadrado y, sin embargo, permite recuperar el vector completo. El terminal retiene 49/81 y no es una proyección. Una fracción de norma conservada en un componente no mide por sí sola qué fracción del estado resulta distinguible: eso depende del núcleo y del condicionamiento del lector. No son dos copias físicas independientes del estado; son componentes correlacionadas de una isometría.

Este ejemplo separa consecuencias lógicas del teorema y no se presenta como una trayectoria física seleccionada por el TPK. Para aplicar una sucesión específica al corpus se conserva la procedencia efectiva de sus C_n.

## 6. Criterio cuantitativo para transferencia completa

Para P_{j,n}=T_{j−1}⋯T_n y P_{n,n}=I, una ventana de longitud L tiene Gram

\[
G_{n,L}=\sum_{j=n}^{n+L-1}P_{j,n}^*D_j^*D_jP_{j,n}
=I-P_{n+L,n}^*P_{n+L,n}.
\]

Si G_{n,L}≥κI con κ>0 en cada bloque consecutivo de longitud L, entonces

\[
\|P_N\|^2\le(1-\kappa)^{\lfloor N/L\rfloor},\qquad A_\infty=0.
\tag{14}
\]

Cada bloque contrae la norma al cuadrado por 1−κ; la composición y la contractividad de los pasos restantes prueban (14).

Un criterio suficiente anterior a los productos es

\[
\sum_{j=n}^{n+L-1}D_j^*D_j\ge\alpha I
\quad\Longrightarrow\quad
G_{n,L}\ge\frac{\alpha}{[1+2(L-1)/9]^2}I.
\tag{15}
\]

**Prueba.** Para y_j=P_{j,n}v, se tiene y_{j+1}−y_j=D_jy_j/√8 y ||D_j||≤2√8/9. Por ello ||D_jv||≤||D_jy_j||+(2/9)Σ_{i=n}^{j−1}||D_iy_i||. La matriz triangular de sumas parciales tiene norma a lo sumo L−1; aplicar la norma ℓ² de la ventana y la hipótesis de Gram da (15). ∎

La ausencia de un vector fijo común da distinción, mientras (15) añade una separación uniforme cuantitativa. Ninguna de las dos condiciones se presume por mencionar simetrías: se aplica a los transportes efectivos de la secuencia.

## 7. Realización incidencial íntegra y cambios de régimen

Para el registro de doce coordenadas, [N3] construye Fk=(μ(k),IP₀k/6), con inversa y producto interno ponderado en Y=R⊕I(1⊥). La transformación F⊕F lleva el acoplamiento completo a

\[
\mathcal U_Y=(F'\oplus F')\mathcal U(B,C)(F^{-1}\oplus F^{-1})
=\mathcal U(F'BF^{-1},F'CF^{-1}).
\tag{16}
\]

Esta identidad conserva la segunda columna, la reentrada y la composición. Para formas variables se transporta también la forma mediante F. En la realización real de las doce fibras A₂ se usa F⊗Id_{V_A₂}, con V_A₂=A₂⊗_Z R; esta fórmula real-lineal no declara un automorfismo del retículo entero. Las etiquetas genealógicas permanecen; F recupera K y no sustituye los otros registros de la historia.

La versión positiva de (9)–(15) usa transportes unitarios en las métricas declaradas. La versión de forma alternante de (1)–(8) admite los tres regímenes de Euler ya construidos. Ambas pertenecen a realizaciones tipadas del mismo balance. Su distinción es sustantiva: con E=F_av²=[[1,1],[1,2]], se tiene det T=89/81 y det D=−8/81. Las sumas orientadas finitas telescopan, pero los terminales de área crecen como (89/81)^N. Una igualdad de áreas firmadas no autoriza a aplicar automáticamente el límite positivo de Hilbert.

Esto determina un objetivo de integración preciso: conservar cada forma y su dominio, usar la evolución completa reversible para la reentrada y aplicar el teorema de registro ilimitado en las realizaciones positivas que satisfacen sus hipótesis. La acción física y la autoinercia mantienen los lectores, conexiones y escalas heredados; esta nota construye una composición operatoria, no una identificación empírica adicional.

## 8. Consecuencia para el artículo y archivos conservados

La propuesta anterior permanece en [CRISTAL_APERIODICO_GENERACION_Y_RECUPERACION_20260912.md](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/CRISTAL_APERIODICO_GENERACION_Y_RECUPERACION_20260912.md>). Esta continuación permite centrar el artículo en una pregunta más delimitada: cómo una lectura comprimida se integra en un transporte reversible que conserva forma, memoria y capacidad de reconstrucción cuando varían sus operadores.

Los resultados centrales candidatos son (5)–(6), composición con reentrada; (9)–(11), registro ilimitado no estacionario; y (12)–(15), distinción entre transferencia y recuperación. El cristal temporal aperiódico y la incidencia proporcionan aplicaciones documentadas; el título definitivo se decidirá después de fijar la clausura de esas dependencias. No se compila un PDF en esta etapa.

Fuentes utilizadas:

- **F1:** [Integral, carta nonádica y defecto](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex:1421>), líneas 1421–1458.
- **F2:** [Monografía, balance compresión–memoria](</Users/ruben/Documents/New project/output/DOBLE_PROYECCION_HOLOGRAFICA_CRISTAL_TEMPORAL_APERIODICO_MONOGRAFIA_AUTOSUFICIENTE/manuscrito/flattened/main_autosuficiente.tex:20680>), líneas 20680–20780.
- **N1:** [Conservación entre formas variables](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/ACCION_CONTINUACION_20260912.md>), §§2–6; primera columna, criterio escalar de rotaciones, tres regímenes y refinamiento.
- **N2:** [Recuperación estacionaria](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/RECUPERACION_DINAMICA_20260912.md>), §§3–5; terminal proyectivo, inversa y naturalidad.
- **N3:** [Incidencia y marcos](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/EXCEPCIONAL_CONTINUACION_20260912.md>), §§2–7; F, su inversa y compatibilidad.
- **N4:** [Conservación estructural](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/CONSERVACION_ESTRUCTURAL.md>), §§2–6; balances y diferencia de iteraciones.
- **N5:** [Refinamiento común](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/REFINAMIENTO.md>), §§2–7; propietarios APP–TRIT–TPK y cinco operaciones inseparables.

Las pruebas generales preceden a los controles racionales separados. Los ensayos matriciales comprueban las identidades y detectan omisiones; no sustituyen el límite funcional ni certifican una nueva ley física.

[Verificador racional separado](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/verificar_acoplamiento_reversible_20260912.py>): 139 comprobaciones exactas con aritmética racional, activas también con optimización de Python. Comprueba ejemplos finitos y controles negativos; las pruebas generales se encuentran en el texto anterior.
