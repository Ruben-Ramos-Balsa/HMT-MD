# Costura nonádica, balance de memoria y transporte de la positividad

Desarrollo focal del 11 de septiembre de 2026. No modifica las ediciones PDF entregadas. Procedencia: arquitectura autoral preexistente; formalización reunida de las identidades de compresión, con una extensión explícita al caso en que aún se comprueba la isometría de la costura. No se atribuye prioridad histórica a estas identidades operatorias.

## 1. Objeto de partida y corte causal

La construcción que se utiliza es APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. APP conserva sobre el mismo soporte las evaluaciones de suma y producto, sus cocientes y residuos. El TRIT conserva orientación y régimen; el TPK compone selección, transporte y actualización de memoria. La holonomía nonádica devuelve la fase y aumenta la profundidad de la historia. Los cinco aspectos correlativos del continuo no se separan ni se redefinen mediante la cuestión espectral que se estudia después.

Este desarrollo comienza en la realización del registro de vueltas de esa estructura. No pretende sustituir la construcción completa del continuo por un espacio de sucesiones. La memoria entera es una coordenada del estado, no su totalidad. Tampoco identifica el registro de fase reducido con el generador TPK.

El apunte autoral sobre suma y producto señala la procedencia de la matriz central. En la carta positiva conservada se obtiene

\[
B_c=\begin{pmatrix}7&2\\2&7\end{pmatrix}
=9P_++5P_-,\qquad
P_\pm=\frac12\begin{pmatrix}1&\pm1\\\pm1&1\end{pmatrix}.
\]

Así, después de normalizar el modo uniforme, el modo diferencial tiene razón \(q=5/9\). Los nombres «suma» y «producto» describen las operaciones APP que generan la carta; los proyectores \(P_+\) y \(P_-\) son sus modos simétrico y antisimétrico. La igualdad entre un modo y una hoja concreta necesita conservar el mapa que los relaciona.

## 2. Una identidad de costura que conserva todos los términos

Sea \(\mathcal K\) un espacio de Hilbert y sea \(C\) un operador acotado sobre él. En \(\mathcal K^9\), la carta de nueve fases con costura \(C\) actúa por

\[
S_C(v_0,\ldots,v_8)=(Cv_8,v_0,\ldots,v_7),
\qquad S_C^9=I_9\otimes C.
\]

La inclusión uniforme es

\[
Jv=\frac13(v,\ldots,v),\qquad J^*J=I.
\]

Escribimos la compresión visible y su componente complementaria como

\[
T=J^*S_CJ=\frac{8I+C}{9},\qquad
\eta=(I-JJ^*)S_CJ.
\]

**Proposición 1.** Sin suponer que \(C\) sea isométrico, se cumplen

\[
\eta^*\eta=\frac8{81}(I-C)^*(I-C),
\]

\[
\boxed{I-T^*T=\eta^*\eta+\frac19(I-C^*C).}
\tag{1}
\]

**Demostración.** La ortogonalidad de \(JJ^*\) da

\[
\eta^*\eta=J^*S_C^*S_CJ-T^*T.
\]

El primer término es \((8I+C^*C)/9\). El segundo es
\((64I+8C+8C^*+C^*C)/81\). La resta prueba la primera identidad. Restar ahora \(T^*T\) a \(I\) y separar \(I-(8I+C^*C)/9\) prueba (1). ∎

La fórmula no elimina memoria: muestra exactamente dos contribuciones. Una mide la dispersión entre las nueve fases; la otra mide el defecto de norma de la costura. Si la construcción previa ha dado \(C^*C=I\), queda la identidad positiva de compresión–expresión del corpus:

\[
I-T^*T=\eta^*\eta\succeq0.
\]

Este resultado explica qué contiene la positividad de la memoria y dónde debe intervenir la identificación del lector. No permite reemplazar esa identificación por el dibujo de una circunferencia.

## 3. Contracción visible y archivo completo de las vueltas

Supóngase ahora que \(C\) es unitario, como sucede para el desplazamiento bilateral de la memoria entera. La vuelta completa del modo diferencial se representa por \(M=qC\), no por nueve aplicaciones sucesivas del mismo factor \(q\).

Para cada entero \(N\geq1\), se define el registro de pérdidas y terminal

\[
L_Nv=\bigl(\sqrt{1-q^2}v,
\sqrt{1-q^2}qCv,\ldots,
\sqrt{1-q^2}q^{N-1}C^{N-1}v, q^NC^Nv\bigr).
\]

**Proposición 2.** \(L_N\) es isométrico. Al aumentar \(N\), el último componente se descompone en una nueva memoria publicada y un nuevo terminal, sin borrar el registro anterior. El registro infinito

\[
Lv=\left(\sqrt{1-q^2}q^jC^jv\right)_{j\geq0}
\]

también es isométrico.

**Demostración.** Para \(v,w\in\mathcal K\),

\[
\langle L_Nv,L_Nw\rangle
=\left[(1-q^2)\sum_{j=0}^{N-1}q^{2j}+q^{2N}\right]
\langle v,w\rangle=\langle v,w\rangle.
\]

En el último componente, \(q^NC^Nv\) se transforma en
\((\sqrt{1-q^2}q^NC^Nv,q^{N+1}C^{N+1}v)\); esa transformación conserva el producto interior. El terminal tiene norma \(q^N\|v\|\), que tiende a cero; la suma infinita converge y conserva la norma. ∎

Para dos estados iniciales, esta prueba conserva sus productos cruzados; no consiste sólo en sumar energías de trayectorias aisladas. El signo positivo de la memoria procede de la ortogonalidad de sus residencias y de la isometría del transporte que ya se ha construido.

## 4. La posición del doble círculo

El registro entero de vueltas admite el desplazamiento bilateral \(Se_n=e_{n+1}\) sobre \(\ell^2(\mathbb Z)\). Sus caracteres \(n\mapsto z^n\), \(|z|=1\), dan el círculo dual de la memoria. La fase visible \(r\in\{0,\ldots,8\}\) retorna; el entero \(n\) no se reduce módulo \(12\) en el estado completo.

Si se impone esa reducción, un carácter sólo desciende cuando \(z^{12}=1\). Por tanto, la memoria sin reinicio tiene una consecuencia precisa: permite el círculo completo de caracteres, mientras que el calendario finito sólo conserva una selección finita. No se deduce de ello qué medida aritmética se realiza sobre ese círculo.

El segundo círculo que aparece en el capítulo espectral del integral es una carta de la realización de Cayley. El desarrollo complementario de este expediente construye un operador de Cayley directamente sobre las funciones de prueba antes de construir un espacio de Hilbert mediante la forma de Weil. Así se puede comparar el transporte aritmético con el de memoria sin introducir las alturas de los ceros como entradas.

### 4.1. El mismo balance en la forma aritmética, antes de conocer su signo

La invariancia aritmética del lector de Cayley auxiliar permite una composición
adicional. Para \(a>b>1/2\), sea \(C_a\) el operador construido en la
nota de momentos y sea \(\mathcal T_a=(8I+C_a)/9\). La igualdad
\(\mathscr W(C_af,C_ag)=\mathscr W(f,g)\) implica, por expansión,

\[
\boxed{\mathscr W(f,g)=\mathscr W(\mathcal T_af,\mathcal T_ag)
+\frac8{81}\mathscr W((I-C_a)f,(I-C_a)g).}
\tag{4}
\]

Esta identidad conserva el canal gamma, los relojes primos y el término
polar conjuntamente. No presupone que la forma sea positiva. El cálculo
consiste en sumar los coeficientes: los términos mixtos tienen coeficientes
\(8\) y \(-8\), que se cancelan, mientras que los dos términos diagonales
aportan \(72+9=81\) veces la forma inicial. Su iteración finita da

\[
\mathscr W(f,g)=\mathscr W(\mathcal T_a^Nf,\mathcal T_a^Ng)
+\frac8{81}\sum_{j=0}^{N-1}
\mathscr W((I-C_a)\mathcal T_a^jf,(I-C_a)\mathcal T_a^jg).
\tag{5}
\]

En la representación ordinaria \(L^2\), donde \(C_a\) ya es unitario,
el mismo cálculo es una descomposición positiva de norma. Sobre la forma
aritmética es, inicialmente, una conservación exacta de energía firmada.
La diferencia entre esas dos afirmaciones queda situada en una identidad
común; no se oculta en un cambio de representación.

En una carta circular \(z=e^{i\theta}\), la compresión envía
\(z\) a \(t(z)=(8+z)/9\). Por tanto,

\[
1-|t(z)|^2=\frac8{81}|1-z|^2
=\frac{32}{81}\sin^2(\theta/2).
\]

La separación angular tiene así una expresión exacta como energía
complementaria. Ésta es la imagen de la compresión nonádica de una carta
de fase; no se identifica por el dibujo con otro operador del corpus.
Tampoco se confunde este mapa \(t(z)\) con el factor radial \(5/9\),
que procede de los dos modos de la carta APP central.

El desarrollo local de Schur da signo positivo a la forma aritmética en
un dominio funcional concreto y a sus imágenes por transporte. Las
identidades (4)–(5) no autorizan por sí solas a declarar positivos todos
sus sumandos para una prueba arbitraria: permiten localizar exactamente
qué energías y correlaciones debe conservar una extensión de ese dominio.

## 5. Criterio suficiente de cierre mediante transporte y momentos

Sea \(\mathcal D\) el dominio común de los lectores previamente construidos. Sea \(\mathscr W\) la forma sesquilineal que publican sus canales gamma, primos y polar. La fórmula analítica se recibe después del generador nativo; no selecciona las semillas ni los coeficientes anteriores.

Sean \(C_a\) el transporte reversible sobre pruebas y \(S\) el desplazamiento de la memoria. Se utiliza explícitamente \(C_a(\mathcal D)=\mathcal D\) y la identidad \(\mathscr W(C_af,C_ag)=\mathscr W(f,g)\), demostrada para la clase exponencial de pruebas en la nota complementaria. Para una familia \(\mathcal E\subset\mathcal D\), supóngase construido un mapa lineal \(V:\operatorname{span}\mathcal E\to\mathcal K\) tal que, para todo \(f,g\) de esa familia y todo entero \(n\),

\[
\boxed{\mathscr W(C_a^n f,g)=\langle S^nVf,Vg\rangle.}
\tag{2}
\]

**Proposición 3.** La identidad (2) implica la positividad de \(\mathscr W\) sobre el espacio generado por las órbitas \(C_a^n\mathcal E\). Si ese espacio es denso en \(\mathcal D\) para la norma conjunta de los lectores, y éstos son continuos para esa norma, la positividad se extiende a \(\mathcal D\).

**Demostración.** Para \(F=\sum_j C_a^{n_j}f_j\), la invariancia de \(\mathscr W\) bajo \(C_a\) y (2) dan

\[
\begin{aligned}
\mathscr W(F,F)
&=\sum_{i,j}\mathscr W(C_a^{n_i-n_j}f_i,f_j)\\
&=\left\|\sum_i S^{n_i}Vf_i\right\|^2\geq0.
\end{aligned}
\]

Si una combinación representa la función cero, la misma identidad fuerza que la combinación de vectores tenga norma cero; la realización queda bien definida. El paso a la clausura usa la continuidad de los dos lectores, no una elección posterior del signo. ∎

Éste es un criterio de construcción con dominios explícitos, no una afirmación de que (2) haya sido demostrada para todos los lectores del corpus. Para extender desde la familia inicial a sus órbitas hay que conservar todos los momentos cruzados: demostrarlo sólo con \(n=0\) sobre esa familia inicial no completa dicha extensión. Naturalmente, una identidad de Gram ya demostrada para \(n=0\) sobre todo \(\mathcal D\) probaría directamente la positividad en ese dominio.

## 6. Cómo se relaciona con las dos columnas

El corpus conserva dos columnas \(J_+\) y \(J_-\) y un conector analítico efectivo entre ellas. También describe una codificación nativa \(\Xi\) y una proyección ortogonal \(P\). Cuando las dos identidades de momentos se calculan en el mismo dominio,

\[
\langle\Xi f,\Xi g\rangle=\langle J_+f,J_+g\rangle,
\qquad
\langle P\Xi f,P\Xi g\rangle=\langle J_-f,J_-g\rangle,
\]

la resta da

\[
\mathscr W(f,g)=\langle(I-P)\Xi f,(I-P)\Xi g\rangle.
\tag{3}
\]

El expediente calcula la expectativa uniforme y el refinamiento de Helmert por separado. Su conjugación conjunta conserva los dos Grams y no puede, por un mero cambio de notación, convertir un operador de diferencia en uno de evaluación. El conector gamma recuperado realiza una operación analítica adicional, que debe conservar su presupuesto de energía. Esta precisión reúne las operaciones existentes; no declara inexistente la arquitectura del TPK.

Las fórmulas (2) y (3) son dos expresiones compatibles de la vía que se quiere completar: la primera organiza los retornos y sus correlaciones, la segunda organiza la parte visible y la memoria complementaria. La estimación por complemento de Schur del expediente da un control efectivo de esa energía en una ventana completa y en todos sus refinamientos. Su alcance se declara con la ventana concreta, sin sustituir con ella el dominio global.

## 7. Localizadores materiales y continuidad

- APP central, modos \(9/5\): `base_c01_sin_encabezado.tex`, construcción de la carta central; capítulo `78_doble_circulo_campo_espectral_completo.tex`, entorno de líneas 1276–1280.
- Memoria anterior a la representación espectral: `cap08_holonomia_helice_memoria.tex`, especialmente la cubierta entera y la publicación \(C_{108}\).
- Conexión y compresión–expresión: `certificados/ley_nueve_puertas_2026-07-30/DELTA_CONEXION_NONADICA_CONJUNTA_COMPRESION_EXPRESION_2026-08-16.md`, §§1–3.
- Doble círculo y transporte cilíndrico: propietario `78_doble_circulo_campo_espectral_completo.tex`, líneas 940–1260.
- Dos momentos nativos: propietario `10b_prueba_espectral_polar_riemann_weil_rectificacion_probatoria_20260903.tex`, líneas 235–452.
- Propietarios completos y rutas absolutas: [recuperación conservada](../ARITMETICA_GENEALOGICA_PRIMOS_DESARROLLO_DOBLE_CIRCULO_20260911/01_HALLAZGOS_PROPIETARIOS_DOBLE_CIRCULO.md).

La selección editorial sigue siendo el integral de 2.249 páginas y sus desarrollos adyacentes. Los verificadores históricos que devuelven 2.084 páginas no cambian esa selección. Ningún control de huellas o de compilación se utiliza aquí como prueba de positividad global.
