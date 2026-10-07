# Recuperación de la dinámica y conservación bajo refinamiento

Continuación de la investigación del 11 de septiembre de 2026. Fecha de esta ampliación: 12 de septiembre de 2026.

## 1. Objeto de la ampliación

El balance precedente conserva el producto interior al distribuir un estado entre la lectura terminal y los registros sucesivos de memoria. La presente ampliación determina cómo recuperar también el transporte que produjo esa distribución. Obtiene su representación exacta sobre el registro, conserva esa representación bajo refinamiento y calcula dos regímenes diferentes de acumulación de memoria.

Se mantiene la investigación de conservación, incidencia y acción. La posibilidad autoral de reunir las constantes en una expresión compacta orienta la búsqueda de composiciones; cada constante conserva su operador generador y su etapa de lectura. Esta ampliación se añade a los cuatro desarrollos anteriores, que permanecen íntegros.

**Procedencia.** La conexión nonádica, la conservación de memoria, la realización bilateral del registro y la relación entre valor e incidencia son arquitectura autoral preexistente. Los teoremas de esta nota son una formalización adicional de sus realizaciones documentadas. Se declara `FORMALIZACION_NUEVA` en este expediente, con procedencia histórica global pendiente de revisión; no se atribuye prioridad universal a identidades de teoría de operadores.

## 2. Genealogía efectiva y dominio

APP genera sobre las mismas marcas horizontales y verticales las hojas aditiva y multiplicativa, conservando residuo y cociente. El TRIT orienta la emisión y conserva el acarreo de su división ternaria. El TPK compone selección, transporte y actualización; el registro de una ruta es una palabra ordenada de emisiones. La holonomía devuelve la fase mientras aumenta la memoria entera de vueltas. La prolongación es \(w_6\to w_{12}\to w_{18}\to w_{24}\to w_{30}\to R_{36}\to G_9\).

El estado enriquecido contiene las hojas, orientación, residuo, cociente, acarreo, ruta, frontera, memoria y supervivencia. El constructor conjunto produce sobre esa misma historia sus operaciones espectral, solenoidal, de calibre, cohomológica y determinantal. Sus mapas de truncamiento y naturalidad son los que utiliza el refinamiento de esta investigación; se mantienen las pruebas heredadas de generación conjunta, no cinco estados seleccionados por separado.

Las coordenadas \(\pi_{\rm HMT},\varphi_{\rm HMT},e_{\rm HMT},\alpha_{\rm HMT}\) y el registro dodecafásico \(K\) son salidas de sus lectores tipados. El uso posterior de esas salidas conserva su genealogía común y su orden constructivo. El corte de la presente nota es la realización lineal del transporte de memoria. El espacio de Hilbert, la representación espectral y el cálculo asintótico intervienen después como lenguaje de prueba; no seleccionan las emisiones APP–TRIT–TPK.

Fuentes de este recorrido:

- [Estado, emisiones y medida común](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:15>): APP, líneas 15–95; TRIT, 97–174; memoria afín, 358–446; estado y truncamiento, 730–834; medida, 1277–1468.
- [Constructor de las cinco operaciones correlativas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b2_operaciones_intrinsecas_correlativas.tex:872>): acciones comunes, constructor, naturalidad y totalidad, líneas 872–1244.
- [Terminal y límite conjunto](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b3_terminal_naturalidad_limite.tex:898>): persistencia simultánea, 898–945.
- [Carta nonádica y memoria bilateral](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/PRIMOS_Y_ZETA_COMPLETO/ampliacion/transporte_y_momentos.tex:55>): transporte, compresión, balance y círculo dual, líneas 55–178.
- [Desarrollo precedente](CONSERVACION_ESTRUCTURAL.md), §§2–6, y [refinamiento precedente](REFINAMIENTO.md), §§2–7: pruebas utilizadas a continuación.

## 3. Representación recuperable del transporte

Sea \(C\) la realización unitaria del transporte de memoria sobre \(\mathcal H\). La carta de nueve fases, su inclusión uniforme y su compresión son

\[
S_C(v_0,\ldots,v_8)=(Cv_8,v_0,\ldots,v_7),\qquad
Jv=(v,\ldots,v)/3,\qquad T=(8I+C)/9.
\]

Sea \(\eta=(I-JJ^*)S_CJ\). Su acción es

\[
\eta v=\frac1{27}\bigl(8(C-I)v,-(C-I)v,\ldots,-(C-I)v\bigr).
\]

La normalización de nueve copias determina \(1/3\); el reparto de la costura determina \(8/81\) en

\[
I-T^*T=\eta^*\eta=\frac8{81}(I-C)^*(I-C).
\tag{1}
\]

Escribimos \(P=\operatorname{proj}\ker(I-C)\). El teorema precedente prueba la convergencia fuerte \(T^N\to P\). Por tanto,

\[
\mathcal Vv=(Pv,\eta v,\eta Tv,\eta T^2v,\ldots)
\quad\text{en}\quad
\mathcal R=P\mathcal H\oplus\ell^2(\mathbb N_0;\mathcal H^9)
\tag{2}
\]

es una isometría. Denotamos su imagen cerrada por \(\mathcal M\).

En el espacio de registros definimos el desplazamiento de bloques

\[
\mathcal B(a,m_0,m_1,m_2,\ldots)=(a,m_1,m_2,\ldots).
\tag{3}
\]

El primer componente conserva el sector fijo; los demás componentes son los registros vectoriales completos, incluidas sus correlaciones.

**Teorema 1.** El transporte original tiene la representación exacta

\[
\boxed{\mathcal V C=(9\mathcal B-8I)\mathcal V.}
\tag{4}
\]

La restricción \(\mathcal C=(9\mathcal B-8I)|_{\mathcal M}\) es unitaria sobre \(\mathcal M\), y

\[
C=\mathcal V^*\mathcal C\mathcal V.
\tag{5}
\]

**Prueba.** Como \(PT=P\), la definición (2) da componente a componente

\[
\mathcal VT=(Pv,\eta Tv,\eta T^2v,\ldots)=\mathcal B\mathcal Vv.
\]

La identidad algebraica \(C=9T-8I\) implica (4). La isometría \(\mathcal V:\mathcal H\to\mathcal M\) es sobreyectiva por definición de su imagen. La igualdad (4) identifica la restricción con \(\mathcal V C\mathcal V^{-1}\), que es unitaria porque \(C\) lo es. Esto demuestra además que \(\mathcal C\mathcal M=\mathcal M\) y (5). ∎

La restricción al subespacio de registros compatibles es esencial: \(9\mathcal B-8I\) sobre todo \(\mathcal R\) no es unitario. El teorema caracteriza el transporte sobre registros que proceden efectivamente de una misma trayectoria lineal de la carta documentada.

**Corolario 1.1.** Para \(v,w\in\mathcal H\) y \(k\in\mathbb Z\),

\[
\langle C^kv,w\rangle
=\langle\mathcal C^k\mathcal Vv,\mathcal Vw\rangle.
\tag{6}
\]

Así se conservan todos los momentos cruzados de la dinámica realizada. Las potencias negativas pertenecen a la inversa de \(\mathcal C\) en \(\mathcal M\), no a una inversión del desplazamiento unilateral sobre el espacio ambiente.

**Corolario 1.2.** Para todo observable acotado \(A\), su realización en la imagen es \(\widehat A=\mathcal V A\mathcal V^*|_{\mathcal M}\). Se preservan productos, adjuntos y conmutadores. En particular,

\[
[A,C]=0\quad\Longleftrightarrow\quad[\widehat A,\mathcal C]=0.
\tag{7}
\]

La prueba consiste en usar \(\mathcal V^*\mathcal V=I\) y que \(\mathcal V\mathcal V^*\) es la identidad de \(\mathcal M\). La conservación de simetría queda expresada mediante el transporte íntegro de sus operadores, además de mediante una igualdad de normas.

## 4. Reconstrucción explícita y profundidad del registro

Sea \(m_j=\eta T^jv\). La identidad telescópica da para cada \(N\)

\[
\boxed{v=T^{*N}T^Nv+\sum_{j=0}^{N-1}T^{*j}\eta^*m_j.}
\tag{8}
\]

Al pasar al límite fuerte,

\[
\boxed{v=Pv+\sum_{j=0}^{\infty}T^{*j}\eta^*m_j.}
\tag{9}
\]

La reconstrucción parcial con terminal fijo,
\(v_N=Pv+\sum_{j<N}T^{*j}\eta^*m_j\), tiene error exacto

\[
v-v_N=T^{*N}T^N(I-P)v.
\tag{10}
\]

La serie converge para cada estado. Si el registro completo presenta un error \(\delta r\) en norma de \(\mathcal R\), su reconstrucción mediante \(\mathcal V^*\) cambia en una norma a lo sumo \(\|\delta r\|\), porque \(\|\mathcal V^*\|=1\). Ésta es una estabilidad uniforme de la lectura completa.

### Diferencia entre profundidad finita e ilimitada

Para el desplazamiento bilateral \(Ce_k=e_{k+1}\) en \(\ell^2(\mathbb Z)\), se tiene \(P=0\). Considérese

\[
v_L=L^{-1/2}\sum_{k=1}^{L}e_k.
\]

Entonces \(\|(I-C)v_L\|^2=2/L\). La conmutación de \(T\) con \(I-C\), la contracción de \(T\) y (1) implican

\[
\sum_{j=0}^{N-1}\|\eta T^jv_L\|^2
\leq\frac{16N}{81L}.
\tag{11}
\]

Para cualquier profundidad fija \(N\), el lado derecho tiende a cero cuando \(L\to\infty\), aunque \(\|v_L\|=1\). El registro de memoria de profundidad fija, separado del terminal, carece de una cota inferior uniforme. En cambio, el registro ilimitado tiene norma exactamente uno para cada \(v_L\).

La diferencia corresponde a dos cuantificadores distintos: cada estado queda conservado al completar su registro; una profundidad prefijada no recupera uniformemente todos los estados sin su terminal. La conservación a profundidad arbitraria posee aquí una expresión funcional exacta.

### Información vectorial e intensidad

El teorema conserva \(m_j\), no únicamente \(\|m_j\|^2\). Por ejemplo, en la realización bilateral, \(v=e_0\) y \(w=e_1\) tienen idénticas intensidades en cada profundidad porque el desplazamiento conmuta con \(T\) y transporta \(\eta\) unitariamente. Sus registros vectoriales son diferentes y (9) recupera los dos estados distintos. Las intensidades sirven para el balance; los registros con sus correlaciones sirven además para la reconstrucción.

## 5. Naturalidad de la recuperación bajo refinamiento

Sean \(\iota_n:\mathcal H_n\to\mathcal H_{n+1}\) las isometrías de refinamiento obtenidas de las emisiones comunes, y \(C_n\) realizaciones unitarias con

\[
C_{n+1}\iota_n=\iota_nC_n.
\tag{12}
\]

La relación vale también para los adjuntos: multiplicar por \(C_{n+1}^*\) y \(C_n^*\) da \(C_{n+1}^*\iota_n=\iota_nC_n^*\). Por tanto las imágenes son reductoras. Las fórmulas polinómicas de \(T_n\), \(\eta_n\) y el límite fuerte de \(T_n^N\) dan

\[
T_{n+1}\iota_n=\iota_nT_n,\quad
\eta_{n+1}\iota_n=\iota_n^{\oplus9}\eta_n,\quad
P_{n+1}\iota_n=\iota_nP_n.
\tag{13}
\]

Sea \(\mathfrak I_n\) el refinamiento que aplica \(\iota_n\) al terminal y \(\iota_n^{\oplus9}\) a cada registro. Entonces

\[
\boxed{\mathcal V_{n+1}\iota_n=\mathfrak I_n\mathcal V_n,\qquad
\mathcal B_{n+1}\mathfrak I_n=\mathfrak I_n\mathcal B_n.}
\tag{14}
\]

**Prueba.** Cada componente de la primera igualdad es una identidad de (13), iterada a la potencia correspondiente de \(T_n\). La segunda igualdad afirma que refinar cada bloque conmuta con desplazar el índice de bloques, lo cual se comprueba directamente. Ambas aplicaciones son acotadas, de modo que las igualdades pasan de los registros de soporte finito a su completación. ∎

Por (4) y (14), la reconstrucción de la dinámica también conmuta con el refinamiento. Se mantienen distintos el índice de profundidad genealógica \(n\) y el de compresiones sucesivas \(j\). La igualdad expresa su compatibilidad cuando actúan mediante los cuadrados documentados, en lugar de identificarlos nominalmente.

## 6. Dos regímenes exactos de distribución de memoria

Para un estado unitario \(v\) con \(Pv=0\), definimos

\[
a_N=\|T^Nv\|^2,\qquad b_N=\|\eta T^Nv\|^2=a_N-a_{N+1}.
\tag{15}
\]

Se tiene \(a_0=1\), \(a_N\to0\), \(b_N\geq0\) y \(\sum b_N=1\). Los pesos \(b_N\) describen la distribución entre profundidades del registro de memoria. Este índice cuenta compresiones; su identificación con una duración física requeriría aplicar el lector temporal correspondiente.

### 6.1. Transporte excepcional de orden tres

El operador ortogonal fijo-libre \(g_c\) del integral satisface \(g_c^2+g_c+I=0\). Para la composición explícita \(C=g_c\), el desarrollo precedente obtuvo

\[
T^*T=\frac{19}{27}I,
\qquad a_N=\left(\frac{19}{27}\right)^N,
\qquad b_N=\frac8{27}\left(\frac{19}{27}\right)^N.
\tag{16}
\]

La profundidad media, contando el primer registro como profundidad uno, es

\[
\sum_{N\geq0}(N+1)b_N=\frac{27}{8}.
\tag{17}
\]

Es un resultado de esa composición de la carta nonádica con el transporte excepcional ya construido; conserva el dominio y no identifica por su orden a \(g_c\) con la holonomía temporal completa.

### 6.2. Registro bilateral de vueltas

Para \(C e_k=e_{k+1}\) y \(v=e_0\), el binomio determina todos los términos:

\[
T^Ne_0=9^{-N}\sum_{k=0}^{N}{N\choose k}8^{N-k}e_k,
\quad
a_N=81^{-N}\sum_{k=0}^{N}{N\choose k}^{\!2}64^{N-k}.
\tag{18}
\]

Esta fórmula es exacta a cualquier profundidad. La representación circular posterior proporciona

\[
a_N=\frac1{2\pi}\int_{-\pi}^{\pi}
\left(\frac{65+16\cos\theta}{81}\right)^N\,d\theta.
\tag{19}
\]

**Teorema 2.** En esta realización bilateral,

\[
\boxed{a_N\sim\frac9{4\sqrt{2\pi}}N^{-1/2},\qquad
b_N\sim\frac9{8\sqrt{2\pi}}N^{-3/2}.}
\tag{20}
\]

**Prueba.** Escribimos \(r(\theta)=(65+16\cos\theta)/81\) y \(q=8/81\). En torno a cero,

\[
r(\theta)=1-q\theta^2+O(\theta^4),\qquad
\log r(\theta)=-q\theta^2+O(\theta^4).
\]

Fijado un entorno suficientemente pequeño, existen constantes positivas \(c_1,c_2\) que acotan \(-\log r(\theta)\) entre \(c_1\theta^2\) y \(c_2\theta^2\). Fuera de ese entorno, \(r\leq\rho<1\). El cambio \(x=\sqrt N\theta\), la cota gaussiana y la convergencia dominada dan

\[
\lim_{N\to\infty}\sqrt N\,a_N
=\frac1{2\pi}\int_{\mathbb R}e^{-qx^2}\,dx
=\frac1{2\sqrt{\pi q}}=\frac9{4\sqrt{2\pi}}.
\]

Para el segundo límite se aplica el mismo procedimiento directamente a

\[
b_N=\frac1{2\pi}\int_{-\pi}^{\pi}r(\theta)^N(1-r(\theta))\,d\theta.
\]

En la variable \(x\), \(N(1-r(x/\sqrt N))\to qx^2\), dominado localmente por una constante por \(x^2\); fuera del entorno la contribución es exponencialmente pequeña incluso tras multiplicar por \(N^{3/2}\). Por tanto

\[
\lim_{N\to\infty}N^{3/2}b_N
=\frac q{2\pi}\int_{\mathbb R}x^2e^{-qx^2}\,dx
=\frac1{4\sqrt{\pi q}}=\frac9{8\sqrt{2\pi}}.
\]

Esta prueba del segundo límite usa su integral propia, sin diferenciar una equivalencia asintótica no controlada. ∎

Por Tonelli y la identidad de colas de una sucesión positiva,

\[
\sum_{N\geq0}(N+1)b_N=\sum_{N\geq0}a_N=+\infty.
\tag{21}
\]

Toda la norma se conserva en memoria, pero su profundidad media diverge en este estado bilateral. La ley de reparto depende de la representación efectiva del transporte: el sector excepcional de orden tres posee tasa geométrica, mientras el registro bilateral aquí considerado posee tasa algebraica.

## 7. Composición con la identidad de Euler y la incidencia

La [identidad de Euler extendida del integral](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/09b_algebras_cuadraticas.tex:289>) realiza los tres regímenes mediante el Coxeter de \(A_2\), un transporte nilpotente y \(F_{\rm av}^2\), con sus antecedentes declarados. Sus generadores normalizados satisfacen \(J_\tau^2=-\tau I\) y tienen traza cero. En sus cartas bidimensionales,

\[
C_\tau(t)=\exp(tJ_\tau),\qquad
\Omega=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
C_\tau(t)^\mathsf T\Omega C_\tau(t)=\Omega.
\]

La traza cero da \(\det C_\tau(t)=1\), y la identidad \(M^\mathsf T\Omega M=(\det M)\Omega\) en dimensión dos prueba la última igualdad. Para

\[
T_\tau=\frac{8I+C_\tau}{9},\qquad
D_\tau=\frac{\sqrt8}{9}(C_\tau-I),
\]

se obtiene una ley de conservación orientada común:

\[
\boxed{\Omega=T_\tau^\mathsf T\Omega T_\tau+D_\tau^\mathsf T\Omega D_\tau.}
\tag{22}
\]

**Prueba.** Al expandir los dos términos, las contribuciones cruzadas de \(C_\tau\) tienen coeficientes opuestos. Quedan \(72\Omega/81+9C_\tau^\mathsf T\Omega C_\tau/81=\Omega\). ∎

Esta forma alternante corresponde al área orientada del plano canónico. Su conservación permite comparar los tres regímenes respetando sus diferencias. Para los representantes concretos \(C\) de Coxeter, \(I+N\) y \(F_{\rm av}^2\), respectivamente,

\[
(\det T,\det D)=
\left(\frac{19}{27},\frac8{27}\right),\qquad
(1,0),\qquad
\left(\frac{89}{81},-\frac8{81}\right).
\tag{23}
\]

La suma es uno en los tres casos. En el parabólico, \(D\) es de rango uno y puede conservar información aunque su área sea cero. En el hiperbólico, el complemento tiene orientación opuesta; el balance es de área firmada. El teorema 1, en cambio, utiliza una realización unitaria y positiva: se conservan expresamente las hipótesis de cada resultado.

El [desarrollo de acción y forma variable](ACCION_CONTINUACION_20260912.md) prueba la versión entre cartas diferentes, su integración sobre curvas cerradas y su compatibilidad con refinamiento. El [desarrollo de incidencia](EXCEPCIONAL_CONTINUACION_20260912.md) compone la reconstrucción con \(F(k)=(\mu(k),\mathcal I P_0k/6)\), manteniendo las doce coordenadas de \(K\); transporta también los operadores y sus marcos locales. Así, una misma identidad de conservación admite realizaciones tipadas de norma, incidencia y acción orientada.

## 8. Resultado de conjunto y continuación editorial

La conservación obtenida posee ahora un contenido más preciso: el registro conserva el estado, admite una inversa estable, representa el transporte original y conserva sus conmutadores y momentos cruzados. El refinamiento respeta simultáneamente esa representación y su inversa. Los ritmos de acumulación de memoria se deducen de la costura efectiva, con dos casos documentados y calculados exactamente.

La composición con la incidencia conserva esos registros mediante el mapa completo de media e incidencia de las doce coordenadas de \(K\). La composición con la acción transporta la forma cuadrática de una profundidad a otra. La ecuación (22) reúne además los tres regímenes de Euler mediante el área orientada que comparten. Ambas prolongaciones están desarrolladas en las notas aditivas enlazadas, conservando sus dominios respectivos.

Para el PDF posterior, el orden demostrativo resultante es: emisiones y estado común; medida y refinamiento; balance de lectura y memoria; recuperación de la dinámica; transporte de incidencia; acción con forma variable; especializaciones y comparación de tasas. Las fuentes precedentes aportan sus pruebas, y las presentes ampliaciones se distinguen de ellas por procedencia. Este archivo guarda el desarrollo matemático; no crea ni sustituye un PDF.
