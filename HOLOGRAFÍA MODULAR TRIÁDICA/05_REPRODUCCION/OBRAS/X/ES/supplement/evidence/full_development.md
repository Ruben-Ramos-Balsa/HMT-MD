# Memoria recuperable, geometría positiva y refinamiento energético

La continuación del artículo parte del registro dodecafásico producido por la dinámica APP–TRIT–TPK. APP conserva las hojas aditiva y multiplicativa con sus residuos y cocientes; TRIT determina el régimen y la orientación local; el transporte y la actualización del TPK prolongan el estado enriquecido, con retorno de fase y avance de memoria. La construcción conjunta del continuo conserva las cinco estructuras consustanciales de ese mismo estado. El registro que empleamos es una lectura posterior de esta genealogía, y no su sustituto. En particular, las coordenadas de las constantes ya generadas y el registro comparten procedencia; ninguna coordenada convencional selecciona aquí los pesos de una red.

La dinámica efectiva compone \(U_t=\operatorname{Upd}_t\circ\operatorname{Tra}_t\circ\operatorname{Sel}_t\); su holonomía nonádica \(\Gamma_9\) actúa sobre la prolongación \(w_6\to w_{12}\to w_{18}\to w_{24}\to w_{30}\to R_{36}\to G_9\). El registro dodecafásico \(K\) y la publicación reducida de memoria \(K_{\mathrm{ph}}\) conservan sus dominios diferenciados. La notación \(K\) que sigue siempre designa el vector de doce coordenadas. Las publicaciones correlacionadas \((\pi_{\rm HMT},\varphi_{\rm HMT},e_{\rm HMT},\alpha_{\rm HMT})\) proceden de este mismo antecedente; su orden interno de evaluación se conserva en los lectores del corpus.

El punto de partida especializado es el resultado del artículo sobre la Extrema y Media Razón Holográfica que reconstruye las doce coordenadas del registro mediante dos memorias y su carga uniforme. Su composición con la geometría positiva previamente construida permite formular una afirmación precisa: **la forma positiva de esta realización se recupera de sus datos de memoria**. La afirmación comprende la red planar, sus menores, la forma canónica del polígono y la energía nodal; cada lector conserva su dominio y sus operaciones propias.

Sea \(K\in\mathbb R^{12}_{>0}\) el registro en la carta real posterior, y sea \(S\) el desplazamiento cíclico \((Sx)_i=x_{i+1}\), con índices \(i=0,\ldots,11\) tomados módulo doce. Definimos los lectores de compresión y sus complementos por

\[
T_j=\frac{8I+S^j}{9},\qquad
D_j=\frac{\sqrt8}{9}(S^j-I),\qquad j\in\{3,4\}.
\]

La ortogonalidad de \(S\) da \(T_j^*T_j+D_j^*D_j=I\). El registro se publica como una carga \(q=\sum_iK_i\) y dos memorias ordenadas

\[
m_0=D_3K,\qquad m_1=D_4T_3K,\qquad MK=(m_0,m_1).
\]

La segunda memoria se obtiene después de la primera compresión. Esa sucesión importa: el mapa recuperable es la composición completa, con sus dos complementos.

La inversa publicada en el corpus es explícita. Puesto que \((S^3)^4=I\),

\[
T_3^{-1}=\frac{512I-64S^3+8S^6-S^9}{455}.
\]

Por tanto, las memorias determinan

\[
b=-\frac9{\sqrt8}m_0=(I-S^3)K,
\qquad
c=-\frac9{\sqrt8}T_3^{-1}m_1=(I-S^4)K.
\]

Si \(w_i=c_i-b_{i+1}\), entonces \(w_i=K_i-K_{i+1}\). Con \(B_0=0\) y \(B_i=\sum_{j<i}w_j\), resulta

\[
\boxed{K_i=\frac{q+\sum_jB_j}{12}-B_i.}
\]

Estas identidades prueban la recuperación antes de toda interpretación geométrica. También prueban que \(\ker M=\mathbb R\mathbf1\): las dos memorias nulas fuerzan invariancia bajo \(S^3\) y \(S^4\), y por ello bajo \(S=S^4(S^3)^{-1}\). La carga \(q\) restaura la única componente que las diferencias anulan.

Sea \(L=(M^*M|_{\mathbf1^\perp})^{-1}M^*\) la pseudoinversa de \(M\), definida en todo el espacio de observaciones y con valores en \(\mathbf1^\perp\). Para datos compatibles, la reconstrucción toma la forma

\[
K=\frac q{12}\mathbf1+Lm,\qquad m=(m_0,m_1),\qquad \|L\|=\frac94.
\]

Así, los registros positivos corresponden exactamente al cono abierto

\[
\mathcal M_+=\left\{(q,m)\in\mathbb R\times\operatorname{im}M:
\frac q{12}\mathbf1+Lm>0\right\}.
\]

La desigualdad se interpreta coordenada a coordenada. La aplicación \(K\mapsto(q,MK)\) es un isomorfismo lineal entre \(\mathbb R^{12}\) y \(\mathbb R\times\operatorname{im}M\), por lo que este cono tiene dimensión doce. Fijar \(q>0\) deja once parámetros de forma. La compatibilidad \(m\in\operatorname{im}M\) evita tratar veinticuatro coordenadas de memoria como veinticuatro grados de libertad independientes.

Sobre este cono definimos \(d_j=K_j/q\), \(t_0=0\) y \(t_j=\sum_{i=1}^jd_i\), utilizando índices de uno a doce para los intervalos. Se obtiene \(0=t_0<t_1<\cdots<t_{12}=1\). La matriz de caminos de la red planar del artículo tiene columnas \((1,t_j)^\mathsf T\); sus menores ordenados son

\[
\Delta_{ij}=t_j-t_i=\sum_{i<r\le j}d_r>0.
\]

Por consiguiente, la positividad de la realización grassmanniana se expresa mediante las mismas doce desigualdades lineales de \(\mathcal M_+\), seguidas de la normalización positiva por \(q\). Los puntos \((t_j,t_j^2)\) determinan el polígono convexo cuya forma canónica, cobertura por triángulos y residuos ya se construyeron en el artículo. La presente composición proporciona su dependencia explícita respecto de las memorias. La realización conserva su alcance: un corte de once dimensiones en \(\mathrm{Gr}_{>0}(2,13)\) y el amplituedro de rango uno asociado a la elevación por potencias declarada.

La estabilidad también se transporta. Para perturbaciones de la carga y de las memorias, la reconstrucción por mínimos cuadrados satisface

\[
\|\delta K\|^2\le\frac{|\delta q|^2}{12}
+\frac{81}{16}\bigl(\|\delta m_0\|^2+\|\delta m_1\|^2\bigr).
\]

Si la raíz del segundo miembro es menor que \(\min_jK_j\), todas las coordenadas reconstruidas continúan positivas. Para el registro publicado, cuya coordenada mínima es \(58\), y con carga fija, basta

\[
\sqrt{\|\delta m_0\|^2+\|\delta m_1\|^2}<\frac{232}{9}.
\]

Se trata de una cota suficiente en la normalización declarada, y no de una tolerancia metrológica. Garantiza que los menores ordenados permanecen positivos y que el orden de los vértices se conserva. La identidad de memoria aporta así una condición cuantitativa de estabilidad de la forma.

Para observaciones perturbadas que salgan de \(\operatorname{im}M\), la pseudoinversa reconstruye desde su proyección compatible \(MLm\). El componente \((I-ML)m\), ortogonal a esa imagen, se conserva separadamente cuando se archiva la observación íntegra. La estabilidad del registro reconstruido y la conservación completa de los datos observados quedan así distinguidas.

La misma partición tiene una realización energética. Para valores \(f_0,\ldots,f_{12}\) en sus nodos, definimos

\[
\mathcal E_d(f)=\sum_{j=1}^{12}\frac{|f_j-f_{j-1}|^2}{d_j}.
\]

Cada sumando es la energía de la interpolación afín en el intervalo correspondiente. Al subdividir \(d_j\) en longitudes positivas \(d_{j,c}\) con suma \(d_j\), la minimización sobre los nodos nuevos da exactamente el mismo sumando. La prueba consiste en escribir

\[
|f_j-f_{j-1}|^2
=\left|\sum_c\Delta f_{j,c}\right|^2
\le\left(\sum_cd_{j,c}\right)
\left(\sum_c\frac{|\Delta f_{j,c}|^2}{d_{j,c}}\right).
\]

La igualdad se alcanza cuando \(\Delta f_{j,c}=d_{j,c}(f_j-f_{j-1})/d_j\). La extensión minimizante \(Hf\) es única para los extremos fijados. Toda configuración refinada admite la descomposición única \(\widetilde f=Hf+z\), donde \(z\) se anula en los nodos antiguos. La cancelación del término cruzado da

\[
\boxed{\mathcal E_{\widetilde d}(\widetilde f)
=\mathcal E_d(f)+\mathcal E_{\widetilde d}(z).}
\]

Esta igualdad distingue dos operaciones: la lectura efectiva conserva la energía mínima entre los nodos antiguos, mientras que el par \((f,z)\) conserva la configuración refinada completa. El complemento tiene energía no negativa, estrictamente positiva para \(z\ne0\), y un inverso de reconstrucción. Esa estructura es compatible con la conservación de memoria del corpus, mediante este lector energético explícito.

El laplaciano nodal \(L_d\) definido por \(\mathcal E_d(f)=f^*L_df\) recupera la geometría intervalar completa: sus entradas consecutivas cumplen \((L_d)_{j-1,j}=-1/d_j\). En cambio, conservar únicamente los extremos globales produce la respuesta \(\left(\begin{smallmatrix}1&-1\\-1&1\end{smallmatrix}\right)\), porque \(\sum_jd_j=1\). El lector nodal distingue formas que el lector de dos extremos identifica. Esta comparación fija exactamente qué observaciones bastan para la reconstrucción y cuáles requieren archivar componentes adicionales.

Finalmente, la dirección \(u=P_3P_{11}K\), previamente construida en el corpus, determina el flujo

\[
d_j(s)=\frac{K_je^{su_j}}{\sum_lK_le^{su_l}}.
\]

Si los hijos conservan la dirección de su padre y sus fracciones relativas \(\theta_{j,c}\), entonces \(d_{j,c}(s)=\theta_{j,c}d_j(s)\). La interpolación dentro de cada intervalo padre depende sólo de esas fracciones, por lo que es independiente de \(s\). La eliminación energética de los nodos nuevos conmuta con todo el flujo. A la invariancia de la función de partición y a la suma de formas canónicas bajo subdivisiones del mismo dominio se añade, por tanto, una conservación operatoria de la energía. Estas son tres identidades diferentes, con sus lectores expresos, sobre datos de refinamiento compatibles.

La consecuencia para el artículo es precisa. La red y el polígono dejan de presentarse como objetos adjuntos a doce números: sus coordenadas se recuperan de una lectura reversible de memoria; su positividad tiene un cono y una cota de estabilidad; y su refinamiento transporta una energía con complemento reconstructible. La extensión reticular a los doce planos de la realización excepcional constituye otra aplicación del mismo registro y de la misma dirección, con su dualidad y su forma bilineal propias. El vínculo entre estas realizaciones reside en esos mapas construidos, sin identificar sus respectivos espacios de llegada.


# Realización analítica de las energías compatibles

El registro positivo y sus refinamientos determinan, después de su construcción HMT, una familia de particiones de un intervalo. La conclusión siguiente concierne a este lector energético unidimensional. Su demostración precisa el paso desde las identidades finitas de subdivisión hasta una realización analítica; el continuo conjunto del corpus conserva su genealogía anterior y sus demás lectores.

Fijemos una partición inicial \(P_0\) de \([0,1]\) con longitudes \(d_j=K_j/\sum_iK_i>0\), y particiones finitas anidadas \(P_n\), cada una obtenida subdividiendo los intervalos anteriores. Supondremos que su malla máxima tiende a cero. Un refinamiento reiterado con un número fijo de hijos iguales satisface esta hipótesis; para otras reglas, la contracción de la malla es una condición que se comprueba en el lector correspondiente. Conservamos las etiquetas de los hijos y sus datos de acarreo como información del refinamiento.

Denotemos por \(V_n\) el espacio de funciones continuas afines en cada intervalo de \(P_n\). En este espacio la energía de la red es exactamente

\[
E_n(f)=\sum_{[a,b]\in P_n}\frac{|f(b)-f(a)|^2}{b-a}
=\int_0^1|f'(x)|^2\,dx.
\]

La segunda expresión reconoce analíticamente la suma ya construida. Para \(f\in V_n\), su extensión afín a cualquier subdivisión pertenece a \(V_{n+1}\) y conserva la energía. La inclusión \(V_n\subset V_{n+1}\), acompañada por el valor \(f(0)\), es por tanto isométrica para la norma \(|f(0)|^2+E_n(f)\).

**Teorema de reconstrucción energética.** Sea \(f_n\in V_n\) una familia compatible por restricción a los nodos antiguos: \(f_{n+1}(a)=f_n(a)\) para todo nodo \(a\) de \(P_n\). Si \(\sup_n E_n(f_n)<\infty\), existe una única función \(f\in H^1([0,1])\) cuyos valores en todos esos nodos son los prescritos. Además, \(f_n\to f\) uniformemente y en \(H^1\), y

\[
\int_0^1|f'(x)|^2\,dx=\lim_{n\to\infty}E_n(f_n).
\]

Recíprocamente, toda función de \(H^1([0,1])\), tomada en su representante continuo, produce mediante interpolación nodal una familia de esta clase.

Para demostrar la primera dirección, escribamos \(g_n=f_n'\). La compatibilidad en los extremos de cada intervalo de \(P_n\) implica, para \(m\ge n\),

\[
\frac1{b-a}\int_a^b g_m(x)\,dx
=\frac{f_n(b)-f_n(a)}{b-a}=g_n|_{(a,b)}.
\]

En consecuencia, \(g_n\) es la proyección ortogonal de \(g_m\) sobre las funciones constantes en cada intervalo de \(P_n\). Se obtiene la identidad

\[
\|g_m-g_n\|_{L^2}^2=E_m(f_m)-E_n(f_n).
\]

Las energías son crecientes y acotadas. Por ello \((g_n)\) es de Cauchy y converge en \(L^2\) a una función \(g\). Definamos \(f(x)=f_0(0)+\int_0^xg(t)\,dt\). Entonces

\[
\sup_{x\in[0,1]}|f_n(x)-f(x)|\le\|g_n-g\|_{L^2}\longrightarrow0.
\]

Esta estimación prueba convergencia uniforme, conserva los valores nodales y, junto con la convergencia de las derivadas, prueba convergencia en \(H^1\). Las normas de las derivadas dan la identidad energética. La unión de los nodos es densa porque la malla tiende a cero; dos representantes continuos con esos mismos valores coinciden, lo que prueba unicidad.

Para la recíproca, sea \(g=f'\in L^2\). La derivada de la interpolación nodal es el promedio de \(g\) sobre cada intervalo de la partición. Estos promedios son proyecciones ortogonales contractivas en \(L^2\). Para una función continua, su error frente a los promedios está acotado uniformemente por su módulo de continuidad evaluado en la malla máxima, que tiende a cero. La densidad de las funciones continuas en \(L^2\), junto con la contractividad, extiende la convergencia a \(g\). Se siguen las convergencias de funciones y energías, con los mismos argumentos anteriores.

La reconstrucción admite una descomposición de memoria por escalas. Sea \(H_n\) la extensión afín de los valores de \(P_n\) a \(P_{n+1}\), y

\[
z_{n+1}=f_{n+1}-H_nf_n.
\]

El detalle \(z_{n+1}\) se anula en todos los nodos de \(P_n\). Su derivada es ortogonal a todas las funciones constantes en los intervalos antiguos. Por ello los detalles de niveles diferentes son ortogonales en energía y, para toda profundidad finita \(N\),

\[
E_N(f_N)=E_0(f_0)+\sum_{n=0}^{N-1}E_{n+1}(z_{n+1}).
\]

En el límite, la misma suma converge exactamente a \(\int|f'|^2\). Los datos \(f_0\) y todos los detalles recuperan la familia completa. La eliminación de los nodos interiores corresponde a escoger el detalle nulo; su archivo permite recuperar cualquier configuración de energía finita. Así queda exhibida, para este lector, la distinción entre publicación efectiva y conservación de la información de refinamiento.

El flujo determinado por \(u=P_3P_{11}K\) transporta esta construcción. En cada intervalo inicial sea

\[
a_j(s)=\frac{d_j(s)}{d_j(0)}>0,
\qquad d_j(s)=\frac{K_je^{su_j}}{\sum_lK_le^{su_l}}.
\]

La aplicación \(F_s\) que envía los nodos iniciales a sus posiciones nuevas y es afín entre ellos tiene pendiente \(a_j(s)\). Si cada subdivisión hereda las fracciones y la dirección de su intervalo padre, todos sus nodos se transportan por el mismo \(F_s\). Para \(s\) en un compacto, los doce factores \(a_j(s)\) tienen cota superior finita y cota inferior positiva. La condición de malla decreciente y las normas energéticas se conservan por equivalencia: para \(U_sf=f\circ F_s^{-1}\),

\[
\int_0^1|(U_sf)'(y)|^2\,dy
=\sum_j\frac1{a_j(s)}\int_{t_{j-1}(0)}^{t_j(0)}|f'(x)|^2\,dx.
\]

Esta es la ley exacta de transporte de la energía; expresa una equivalencia de normas y explicita los factores métricos. Los espacios completados se transportan coherentemente, y la minimización de los detalles conmuta con la evolución, como en cada nivel finito.

El resultado proporciona una realización analítica completa del lector de energía del artículo: las configuraciones de energía finita se reconstruyen de su refinamiento y de su memoria. Su relación con las formas canónicas conserva el dominio ya probado: ambas construcciones son compatibles con subdivisiones de dominio fijo, mediante suma de formas en un caso y eliminación energética con detalle archivado en el otro. La fórmula de energía no identifica por sí sola una forma canónica amplituhedral de rango superior, ni altera las condiciones de cobertura y residuos que correspondan a esa promoción.


% Desarrollo acotado: lector energético intervalar del registro K.
% Estatuto: formalización añadida sobre K y sobre las identidades de Schur
% ya presentes en el corpus. No se atribuye novedad histórica a Schur.
\section{Energía del intervalo y conservación exacta bajo refinamiento}
\label{sec:energia-refinamiento-k}

La publicación positiva del registro dodecafásico define una partición
ordenada mediante
\[
 K=(234,543,140,729,659,824,621,58,914,794,146,601),
 \qquad d_j=K_j/6263,
 \qquad t_i=\sum_{j=1}^id_j.
\]
El registro se recibe de la composición
\(x_{\rm term}\mapsto\mathcal R_{12}\mapsto
(b^{90},b^{120},Q_{\rm TPK})\mapsto U_{\rm sgn}\mapsto K\),
posterior a APP--TRIT--TPK y a su estado enriquecido. Esta sección aplica
un lector cuadrático a la partición resultante. La comparación entre
profundidades se efectuará por restricciones a extremos heredados, de modo
que cada coeficiente de la energía conserve su origen en una separación
positiva ya producida.

El corpus contiene una energía ponderada de diferencias para el grafo de
las dos memorias y una reducción de Schur de las formas completas. Aquí se
reúnen esas operaciones sobre la red intervalar del registro. La
especialización a conductancias \(1/d_j\), el operador de interpolación
y su compatibilidad con la deformación de las separaciones constituyen
la formalización desarrollada en esta sección.

\subsection{Matriz de rigidez y flujo de frontera}

Sea \(d=(d_1,\ldots,d_m)\), con \(d_j>0\), y sean
\(f=(f_0,\ldots,f_m)\in\mathbb C^{m+1}\) los valores de un observable
en los extremos de la partición. Definimos
\begin{equation}
 \mathcal E_d(f)=\sum_{j=1}^{m}\frac{|f_j-f_{j-1}|^2}{d_j},
 \qquad L_d=D^*\operatorname{diag}(d_1^{-1},\ldots,d_m^{-1})D,
 \label{eq:energia-intervalar}
\end{equation}
donde \((Df)_j=f_j-f_{j-1}\). Así \(\mathcal E_d(f)=f^*L_df\).
La matriz de rigidez tiene entradas
\[
 (L_d)_{00}=d_1^{-1},\quad (L_d)_{mm}=d_m^{-1},\quad
 (L_d)_{ii}=d_i^{-1}+d_{i+1}^{-1}\quad(1\le i<m),
\]
\[
 (L_d)_{i-1,i}=(L_d)_{i,i-1}=-d_i^{-1},
\]
y las demás son nulas. Es hermítica positiva semidefinida, su núcleo
consiste en las funciones constantes y su forma es positiva definida
en el cociente por ese núcleo. La matriz completa recupera las
separaciones mediante
\begin{equation}
 d_j=-\frac1{(L_d)_{j-1,j}}.
 \label{eq:recuperacion-d-rigidez}
\end{equation}

\begin{proposition}[Equivalencia entre separaciones y lector nodal completo]
\label{prop:energia-bidireccional}
La aplicación \(d\mapsto L_d\) es una biyección entre
\((0,\infty)^m\) y el conjunto de matrices reales simétricas
tridiagonales cuyas entradas inmediatamente adyacentes a la diagonal son
negativas y cuya suma en cada fila es cero. Su inversa es
\eqref{eq:recuperacion-d-rigidez}. La normalización \(\sum_jd_j=1\)
equivale a \(\sum_{j=1}^m-1/(L_d)_{j-1,j}=1\).
\end{proposition}
\begin{proof}
Las fórmulas explícitas de \(L_d\) verifican todas las condiciones.
Recíprocamente, las entradas adyacentes negativas determinan separaciones
positivas únicas por \eqref{eq:recuperacion-d-rigidez}. La suma nula de
cada fila determina sus entradas diagonales como la suma de las
conductancias incidentes. La tridiagonalidad fija en cero las restantes
entradas. Se recupera exactamente la matriz de
\eqref{eq:energia-intervalar}; su semidefinitud positiva sigue entonces
de la factorización \(D^*\operatorname{diag}(1/d_j)D\).
\end{proof}

La derivada discreta ponderada
\(J_j=(f_j-f_{j-1})/d_j\) es el flujo orientado de la arista \(j\).
En los vértices interiores, \((L_df)_i=J_i-J_{i+1}\); en los extremos,
\((L_df)_0=-J_1\) y \((L_df)_m=J_m\). La ecuación interior
\(L_df=0\) expresa que el flujo tiene el mismo valor en cada arista.
Esta definición es la de un observable cuadrático del lector intervalar;
su realización como magnitud física requiere la carta dimensional pertinente.

\subsection{Interpolación armónica y reducción exacta}

Refinemos cada separación como
\(d_j=\sum_{c=1}^{r_j}\delta_{j,c}\), con \(\delta_{j,c}>0\).
Sea \(\widetilde d\) la concatenación de esas separaciones, \(R\) la
restricción a los extremos antiguos y \(H\) la interpolación definida por
\begin{equation}
 (Hf)_{j,c}=(1-\theta_{j,c})f_{j-1}+\theta_{j,c}f_j,
 \qquad
 \theta_{j,c}=\frac{\sum_{a=1}^c\delta_{j,a}}{d_j}.
 \label{eq:interpolacion-armonica-k}
\end{equation}
Los extremos compartidos se cuentan una sola vez. Se cumple \(RH=I\).

\begin{theorem}[Refinamiento isométrico de la energía]
\label{thm:energia-schur-refinamiento}
Para todo vector de valores antiguos \(f\),
\begin{equation}
 H^*L_{\widetilde d}H=L_d,
 \qquad L_{\widetilde d}H=R^*L_d,
 \qquad
 \min_{Rg=f}\mathcal E_{\widetilde d}(g)=\mathcal E_d(f).
 \label{eq:isometria-energia-k}
\end{equation}
El minimizador es único y vale \(Hf\). Todo \(g\) admite la
descomposición única
\begin{equation}
 g=H(Rg)+z,\qquad Rz=0,
 \qquad
 \mathcal E_{\widetilde d}(g)
 =\mathcal E_d(Rg)+\mathcal E_{\widetilde d}(z).
 \label{eq:detalle-energia-k}
\end{equation}
\end{theorem}
\begin{proof}
En una arista antigua escribamos \(h_c=g_{j,c}-g_{j,c-1}\), de modo
que \(\sum_ch_c=f_j-f_{j-1}=a\). Si
\(h_c=\delta_{j,c}a/d_j+r_c\), entonces \(\sum_cr_c=0\) y
\[
 \sum_c\frac{|h_c|^2}{\delta_{j,c}}
 =\frac{|a|^2}{d_j}+\sum_c\frac{|r_c|^2}{\delta_{j,c}}.
\]
La igualdad se obtiene expandiendo; el término cruzado es proporcional a
\(\sum_cr_c\) y se anula. El mínimo se alcanza exactamente cuando
todos los \(r_c\) son cero, condición que determina
\eqref{eq:interpolacion-armonica-k}. Al sumar las aristas se obtienen
el mínimo y la descomposición energética. El flujo de \(Hf\) es
constante dentro de cada arista antigua, por lo que sus componentes
interiores de \(L_{\widetilde d}Hf\) son cero y sus componentes heredadas
coinciden con \(L_df\). Esto prueba la segunda identidad matricial; al
multiplicar por \(H^*\), usando \(RH=I\), se obtiene la primera.
\end{proof}

La pareja \((Rg,z)\) conserva el vector refinado completo y permite
recuperarlo por \(g=H(Rg)+z\). La minimización selecciona su
componente armónica; el archivo del detalle \(z\) mantiene la
información que la sola forma reducida no distingue. La conservación
de la energía observada y la conservación del estado refinado quedan
así expresadas por mapas diferentes y explícitos.

Ordenando los vértices como extremos heredados \(E\) e interiores \(I\),
escribimos
\[
 L_{\widetilde d}=\begin{pmatrix}A&B^*\\B&C\end{pmatrix}.
\]
El bloque \(C\) es positivo definido: una función nula en los extremos
que tenga energía cero es constante en cada subintervalo y, por tanto,
idénticamente nula. Se obtiene
\begin{equation}
 H=\begin{pmatrix}I\\-C^{-1}B\end{pmatrix},\qquad
 \operatorname{Schur}_{I}(L_{\widetilde d})
 =A-B^*C^{-1}B=L_d.
 \label{eq:schur-intervalar-k}
\end{equation}
El orden de eliminación de refinamientos sucesivos conserva el resultado:
minimizar primero sobre la profundidad última y después sobre la intermedia
es minimizar sobre todos los detalles con los mismos extremos fijados.
La unicidad implica también
\(H_{n+2\leftarrow n}=H_{n+2\leftarrow n+1}H_{n+1\leftarrow n}\).

\subsection{Operador de Dirichlet a Neumann y residual positivo}

Si sólo se conservan los extremos inicial y final, sea
\(D_0=\sum_{j=1}^md_j\). Para valores \((a,b)\), la solución
armónica es
\[
 f_i=a+(b-a)\frac{\sum_{j=1}^id_j}{D_0},\qquad
 J_j=(b-a)/D_0.
\]
Su operador de Dirichlet a Neumann, que transforma valores de frontera en
flujos salientes, es
\begin{equation}
 \Lambda_d=\frac1{D_0}
 \begin{pmatrix}1&-1\\-1&1\end{pmatrix},\qquad
 \min\mathcal E_d=\frac{|b-a|^2}{D_0}.
 \label{eq:dtn-intervalar-k}
\end{equation}
Con todos los extremos antiguos se obtiene de igual manera \(\Lambda=L_d\).

Una extensión aproximada \(g=(f,z)\) tiene residual interior
\(r=Bf+Cz\). La identidad exacta
\begin{equation}
 \mathcal E_{\widetilde d}(g)-f^*\Lambda f
 =r^*C^{-1}r\ge0
 \label{eq:residual-dtn-k}
\end{equation}
se deduce de \(z+C^{-1}Bf=C^{-1}r\). En particular, si una
extensión lineal es \(\widetilde H=(I,Z)^{\mathsf T}\), su matriz de
residuales es \(\mathscr R=B+CZ\) y
\[
 \widetilde H^*L_{\widetilde d}\widetilde H-\Lambda
 =\mathscr R^*C^{-1}\mathscr R\succeq0.
\]
El residual nulo caracteriza la interpolación armónica exacta. Este
residual energético vive en el espacio de vértices interiores; la
cancelación de residuos de formas meromorfas pertenece a otro mapa de
frontera y conserva su definición propia.

\subsection{Compatibilidad con la deformación dirigida por el registro}

Sea \(u=P_3P_{11}K\) la dirección ya recuperada y definamos
\[
 d_j(s)=\frac{K_je^{su_j}}{\sum_\ell K_\ell e^{su_\ell}}.
\]
Fijadas fracciones positivas \(\vartheta_{j,c}\) de suma uno para cada
\(j\), el refinamiento heredado es
\[
 \delta_{j,c}(s)=\vartheta_{j,c}d_j(s),\qquad
 u_{j,c}=u_j.
\]
Producir primero los pesos refinados \(K_j\vartheta_{j,c}\) y
deformarlos da la misma familia: los hijos tienen idéntico exponencial y
sus coeficientes suman \(K_j\). Para todo \(s\),
\begin{equation}
 \operatorname{Schur}_{I}(L_{\widetilde d(s)})=L_{d(s)},
 \qquad H^*L_{\widetilde d(s)}H=L_{d(s)}.
 \label{eq:schur-flujo-k}
\end{equation}
En esta comparación padre--hijos, \(H\) es constante: sus coeficientes
son las sumas parciales de \(\vartheta_{j,c}\). En cambio, la
interpolación desde los dos extremos globales usa
\(t_i(s)=\sum_{j\le i}d_j(s)\) y cambia con el parámetro. Ambas
afirmaciones corresponden a restricciones diferentes de la misma red.

La normalización \(\sum_jd_j(s)=1\) hace que el operador global de dos
extremos permanezca igual a
\(\left(\begin{smallmatrix}1&-1\\-1&1\end{smallmatrix}\right)\).
La matriz de todos los nodos \(L_{d(s)}\) sí conserva la deformación y
la recupera mediante \eqref{eq:recuperacion-d-rigidez}. La pérdida de
información en el lector de dos extremos queda identificada exactamente:
retiene la longitud total y sus flujos, mientras el lector nodal retiene
todas las separaciones. El archivo de detalles proporciona el complemento
necesario para reconstruir el observable refinado.


# Compresión nonádica, espejo espectral y reconstrucción de K

Nota interna de investigación. Consulta de propietarios existentes; ningún artículo anterior ha sido editado. La fuente numérica primaria sigue siendo APP–TRIT–TPK. Los operadores de esta nota actúan sobre publicaciones ya construidas del mismo estado enriquecido. No se utilizan alturas de ceros, valores metrológicos ni una geometría objetivo para seleccionar K.

## Fuentes y localizadores

Raíz VIII:
`/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/08_PRIMOS_Y_ZETA_ES/documentacion_original/payload/spanish_source`

Raíz X:
`/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/source`

- VIII, `sections/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.tex:347–461`: representación de la forma de Weil positiva, traslaciones, generador autoadjunto, representación espectral y Cayley canónico.
- VIII, `sections/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.tex:465–610`: árbol de historias, pesos, cociclo de memoria, refinamiento isométrico, retorno nonádico, calendario y compresión.
- VIII, `ampliacion/transporte_y_momentos.tex:55–101`: compresión para C acotado y balance con defecto de costura.
- VIII, `ampliacion/transporte_y_momentos.tex:105–176`: registro de pérdidas, memoria bilateral, balance de la forma aritmética y círculo comprimido.
- VIII, `ampliacion/transporte_y_momentos.tex:425–497`: Cayley auxiliar sobre pruebas exponenciales y conservación conjunta de gamma, primo y polar.
- VIII, `antecedentes/integral/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex:203–242`: transformación de Möbius y espejo recíproco.
- X, `nuclear/01.tex:34–94`: masa de cilindros, pullback isométrico y unital, esperanza condicional.
- X, `nuclear/02.tex:39–153`: compresión, balance de observables, telescopía, sector fijo y cambio unitario de carta.
- X, `nuclear/02.tex:172–204`: realización excepcional de orden tres sin vectores fijos; factor cuadrático 19/27, con dominio propio.
- X, `nuclear/11.tex:7–177`: lectores S³/S⁴, dos memorias, inversa exacta, núcleo y estabilidad.
- X, `nuclear/11.tex:188–225`: registros numéricos de memoria, reconstrucción del K publicado.
- X, `nuclear/11.tex:234–307`: composición efectiva memoria→u_K→P_10(K).
- X, `sections/01_hilbert_nonadico.tex:222–279`: conservación de unidad y traza normalizada al mantener toda la fibra; reducción de traza por nueve al seleccionar una esquina.
- X, `nuclear/12.tex:529–577`: realización simpléctica/gaussiana, covarianza W=(8I+HHᵀ)/9 y sus valores simplécticos; objeto distinto de una compresión euclídea unitaria.

## 1. El espejo r→1/r y el operador C tienen tipos diferentes

**Resultado recuperado.** La carta espectral es τ(z)=(z−1)/z, z≠0. Para el espejo z♯=1−conj(z), y restringiendo a z∉{0,1} cuando ambas expresiones se escriben en la carta finita,

τ(z♯)=1/conj(τ(z)).

Si τ(z)=r exp(iθ), r>0, el espejo conserva θ y transforma r en 1/r. Para z=σ+it,

r²=((σ−1)²+t²)/(σ²+t²),

de donde r=1 equivale a σ=1/2. El conjunto fijo del espejo es la circunferencia unidad. Esta identidad algebraica determina una equivalencia entre cartas; por sí sola no selecciona las posiciones de los ceros. La conjugación z→conj(z) es otra involución: sobre la recta crítica cambia t por −t e invierte la orientación angular. No se la identifica con el espejo anterior.

El C de VIII, sección espectral, es

C=(H+iI/2)(H−iI/2)^{-1}: H_W→H_W,

donde H es el generador autoadjunto de las traslaciones en la realización hilbertiana de la forma de Weil. Por cálculo funcional, C es unitario y su multiplicador en la coordenada espectral γ es (γ+i/2)/(γ−i/2). Su construcción en ese propietario aparece después del antecedente de positividad global que permite el cociente hilbertiano. No es una involución ni una permutación finita ni un operador de orden tres por esa definición.

El artículo VIII conserva además una realización auxiliar anterior a ese cociente. Para a>b>1/2, sea E_b el espacio de funciones suaves cuyas derivadas decrecen al menos como exp(−b|x|). Entonces

C_a f(x)=f(x)−2a∫₀∞exp(−at)f(x+t)dt,
C_a^{-1}f(x)=f(x)−2a∫₀∞exp(−at)f(x−t)dt.

Su multiplicador Fourier es c_a(ξ)=(ξ−ia)/(ξ+ia). Es unitario en L² y conserva E_b. La forma aritmética completa satisface W(C_a f,C_a g)=W(f,g), incluyendo los términos polares cruzados. El propietario distingue expresamente esta conservación de una forma hermítica de una prueba de su signo. La elección a>1/2 protege la convergencia término a término de los lectores polares; no reemplaza silenciosamente al Cayley canónico a=1/2.

La memoria entera tiene, a su vez, C=S sobre ℓ²(Z), Se_n=e_{n+1}, unitario de orden infinito. En X, sobre R¹², aparecen C=S³ y C=S⁴, con (Sx)_i=x_{i+1}; sus órdenes son cuatro y tres respectivamente. El operador excepcional g_c de X actúa en otra realización y cumple g_c³=I y ker(I−g_c)=0. Compartir la forma de compresión no identifica estos operadores.

La diferencia de sectores fijos tiene un efecto numérico preciso: para S⁴, P_fix=(I+S⁴+S⁸)/3 tiene rango cuatro y T₄*T₄=P_fix+(19/27)(I−P_fix). Para g_c, el proyector fijo es cero y el factor 19/27 actúa en todo su dominio. El orden tres, sin el dato de los vectores fijos, no autoriza el segundo resultado.

## 2. Conservación de compresión, complemento y memoria

**Resultado recuperado.** Para C acotado en H, sobre H⁹ se definen

S_C(v₀,…,v₈)=(Cv₈,v₀,…,v₇),  Jv=(v,…,v)/3,
T=J* S_C J=(8I+C)/9,
η=(I−JJ*)S_CJ.

La fórmula explícita es ηv=(8(C−I)v,−(C−I)v,…,−(C−I)v)/27. Por expansión,

η*η=(8/81)(I−C)*(I−C),
I−T*T=η*η+(I−C*C)/9.

Si C es unitario, T*T+η*η=I. Para todo observable acotado autoadjunto A que satisface C*AC=A, la misma expansión da

A=T*AT+(8/81)(I−C)*A(I−C).

La compresión N veces conserva el balance de todos los productos cruzados:

A=T*ᴺATᴺ+Σ_{j=0}^{N−1} T*ʲη*(I₉⊗A)ηTʲ.

El transporte completo cumple S_C⁹=I₉⊗C, mientras Tᴺ describe compresiones sucesivas con almacenamiento de sus complementos. Son operaciones distintas. Para C unitario, Tᴺ tiende fuertemente a P_fix, proyector sobre ker(I−C), y el límite mantiene dicho sector fijo. La memoria bilateral tiene P_fix=0; un ciclo finito conserva su dirección uniforme. La extinción fuerte no impone una contracción uniforme: en la realización bilateral puede ocurrir ||Tᴺ||=1 para todo N.

**Corolario algebraico reunido para este desarrollo.** Con D=√8(I−C)/9, el par (T,D) es una isometría H→H⊕H. Sobre operadores de clase traza X,

Q_C(X)=TXT*+DXD*=(8X+CXC*)/9.

Para C unitario, esta aplicación conserva la traza y la unidad; su completa positividad sigue de la expresión con dos operadores. La fórmula conserva las coherencias internas de X en ambos términos. No se identifica esta reducción de registro con un Hamiltoniano físico ni con la forma de Weil. La búsqueda focal en nuclear/10–12 y en las fuentes X por Kraus/unital/canal no localizó esta identidad escrita en esta forma; la consecuencia algebraica procede del balance recuperado.

El otro dueño de unidad y traza es la prolongación de álgebras a→a⊗I₉: conserva la traza normalizada. La esquina a→a⊗p_j la divide por nueve. En el árbol completo, μ(hε)=μ(h)/d(h) conserva Σ_hijos μ=μ(h); el pullback Rf(hε)=f(h) satisface R*R=I y R1=1. Estos balances tienen dominios distintos y son compatibles al conservar explícitamente sus mapas.

## 3. Dos memorias reconstruyen K y su dirección geométrica

**Resultado recuperado, no analogía.** En V=R¹², sean S el desplazamiento cíclico anterior,

T_j=(8I+S^j)/9,  D_j=√8(S^j−I)/9,  j=3,4,
m₀=D₃K,  m₁=D₄T₃K,  q=Σ_i K_i.

La memoria m₁ lee el resultado de la primera compresión. La inversa exacta es

T₃^{-1}=(512I−64S³+8S⁶−S⁹)/455.

Por tanto b=−9m₀/√8=(I−S³)K y c=−9T₃^{-1}m₁/√8=(I−S⁴)K. Definiendo w_i=c_i−b_{i+1} y B_i=Σ_{j<i}w_j, se tiene

w_i=K_i−K_{i+1},  B_i=K₀−K_i,
K_i=(q+Σ_jB_j)/12−B_i.

Anular ambas memorias equivale a S³K=K y S⁴K=K, luego SK=S⁴(S³)^{-1}K=K. Su núcleo común es exactamente la recta uniforme. La aplicación M:K→(m₀,m₁) tiene rango once y

M*M=I−(T₄T₃)*(T₄T₃).

El propietario obtiene la inversa centrada L con LM=P₁₁ y norma 9/4. De ahí la composición ya escrita en X:

u_K=P₃L(m₀,m₁),
P₁₀(K)=P₁₁−P₃L(m)[P₃L(m)]*/||P₃L(m)||².

El flujo geométrico dirigido por u_K recibe así una dirección recuperable de memorias efectivas, no un coeficiente añadido por coincidencia formal. La carga q hace recuperable también el registro completo y sus pesos positivos d_i=K_i/q. No se afirma por ello que cada vector del espacio ambiente V sea una historia TPK admisible.

Testigo exacto reproducido por `verify_nonadic_k.py`, usando como entrada las memorias publicadas z_i=m_i/√8:

9z₀=(495,116,684,−108,−601,90,173,88,−313,−560,397,−461),
81z₁=(2729,2503,3818,−5843,2583,−920,−4051,4338,−5312,−1583,233,1505),
q=6263.

Su inversa produce K=(234,543,140,729,659,824,621,58,914,794,146,601), exactamente. El script verifica además rango once, norma por suma de Grams, inversa T₃ y reconstrucción con q=0 del centrado.

## 4. Composición con el flujo geométrico: igualdad efectiva y frontera de tipo

La dirección u_K define, después de su construcción, un flujo diagonal g(s)=exp(sA_K) en V, con A_K diagonal proporcional a u_K. Como Σ_i(u_K)_i=0, det g(s)=1. Sus componentes positivas permiten actuar sobre coordenadas positivas, pero g(s) no es en general unitario euclídeo. Sustituir C por g(s) en el balance general produce

T*T+D*D=(8I+g(s)*g(s))/9,

que no es I en general. El testigo racional g=diag(2,1/2) tiene determinante uno pero T=diag(10/9,17/18), de modo que una coordenada se expande. La propiedad simpléctica de un levantamiento cotangente tampoco implica unitariedad euclídea.

**Formalización nueva acotada: covariancia con métrica transportada.** Sobre el mismo V, partiendo de uno de los lectores unitarios C₀=S³ o S⁴, se define

C_s=g(s)C₀g(s)^{-1},  G_s=g(s)^{-*}g(s)^{-1}.

Entonces C_s*G_sC_s=G_s, T_s=g(s)T₀g(s)^{-1}, y

T_s*G_sT_s+(8/81)(I−C_s)*G_s(I−C_s)=G_s.

La demostración consiste en cancelar las g(s) inversas en cada producto. La fórmula de η da simultáneamente η_sg(s)=g(s)^{⊕9}η₀. La memoria y la compresión se transportan por un cuadrado conmutativo real, con una métrica indicada, sin exigir que g(s) conmute con C₀ en una carta fija. Esta extensión no compone por sí sola un operador en H_W con un flujo en V: tales dominios siguen separados hasta proporcionar la aplicación entre ellos.

El espejo g(−s)=g(s)^{-1} y el espejo r→1/r son recíprocos en sus respectivas cartas. La identidad del tipo de involución no suministra por sí sola un mapa entre V y el plano espectral. La composición firme recuperada es memoria→K→u_K/P₁₀; el transporte métrico anterior es una consecuencia nueva verificable de esa realización finita.

## Comprobación material

`verify_nonadic_k.py` usa únicamente `fractions` y `json`, no escribe archivos, no consulta red y no contiene `assert`. Los modos ordinario, `-O` y `-I -S` deben terminar en `PASS_NONADIC_K_EXACT`. El recibo corresponde a controles algebraicos finitos y no sustituye los enunciados generales ni convierte los distintos C del corpus en un único operador.


# Deformación de covolumen constante del retículo de Leech por la polarización dodecafásica

## Alcance y procedencia

Esta nota compone dos resultados ya materializados: la realización reticular excepcional del artículo IV y la polarización del registro dodecafásico del artículo X. La composición exponencial, el teorema de dualidad euclídea, su testigo de pérdida de integralidad y la realización duplicada son una formalización nueva de esos datos. La búsqueda focal aquí realizada no autoriza a atribuir esta fórmula exponencial específica a los artículos previos.

El dato se recibe después de APP, TRIT y TPK. Su cadena publicada es estado terminal enriquecido, registro dodecafásico, lectores de incidencia y orientación, y registro entero \(K\). La realización de representación actúa después sobre ese registro; no elige sus coordenadas. La realización reticular procede de la incidencia de frontera del mismo estado, con código de pegado y origen marcado. Las construcciones del continuo que anteceden a estas realizaciones mantienen su carácter conjunto; esta nota comienza en dos salidas posteriores ya construidas y no redefine el generador.

Se conserva una carta marcada común de doce posiciones. La asignación de la coordenada \(u_j\) al plano \(E_j\) es parte explícita de esta composición: fija una realización marcada, sin afirmar que sea independiente de toda permutación de las doce etiquetas.

## Datos exactos recuperados

El registro y su suma son
\[
 K=(234,543,140,729,659,824,621,58,914,794,146,601),
 \qquad \sum_{j=1}^{12}K_j=6263.
\]
En la representación por permutaciones de las doce clases de \(A_5/C_5\), con orden de representantes y distinción de clases de orden cinco fijados por el propietario, se define
\[
 P_3=\frac3{60}\sum_{a\in A_5}\chi_3(a^{-1})\rho(a),
 \qquad P_{11}=I_{12}-\frac1{12}\mathbf1\mathbf1^{\mathsf T}.
\]
La suma finita verifica
\[
 P_3=P_3^{\mathsf T}=P_3^2,\quad
 \operatorname{rank}P_3=3,\quad P_3\mathbf1=0,\quad
 P_3P_{11}=P_3.
\]
Por tanto la polarización publicada es
\[
 u=P_3P_{11}K=P_3K,\qquad
 \sum_j u_j=0,\qquad
 \|u\|^2=\frac{6638585+2275584\sqrt5}{20}>0.
\]
Su evaluación en el orden marcado es
\[
\begin{aligned}
u={}&(-495/4-233\sqrt5/10,\quad 403/4+169\sqrt5/10,\\
&-403/4-169\sqrt5/10,\quad 495/4+233\sqrt5/10,\\
&601/4+1031\sqrt5/10,\quad203/4+211\sqrt5/5,\\
&-203/4-211\sqrt5/5,\quad-601/4-1031\sqrt5/10,\\
&313/4+569\sqrt5/10,\quad162+219\sqrt5/20,\\
&-162-219\sqrt5/20,\quad-313/4-569\sqrt5/10).
\end{aligned}
\]

El espacio euclídeo ambiente del artículo IV es
\[
 E=\bigoplus_{j=1}^{12}E_j,\qquad
 B=\operatorname{diag}(B_2,\ldots,B_2),\qquad
 B_2=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}.
\]
Cada \(E_j\) es el plano real generado por un factor \(A_2\). La descomposición es ortogonal en el espacio ambiente; el retículo de Leech no es una suma directa de doce retículos \(A_2\). El código ternario \(C_W\) pega esos factores para construir \(N=N(C_W)\). El vecino marcado
\[
 v_\alpha=4\rho_1+\rho_2+\cdots+\rho_{12},\quad
 \rho_j=(1,1)_j,\quad v_\alpha^2=54,
\]
\[
 N_{\alpha,0}=\{x\in N:\langle x,v_\alpha\rangle_B\equiv0\bmod3\},
 \qquad \Lambda=N_{\alpha,0}+\mathbb Z\,v_\alpha/3
\]
es, en el propietario, positivo, par, unimodular y sin raíces de rango \(24\), y por ello una realización del retículo de Leech. En particular \(\Lambda^*=\Lambda\), donde el dual se toma respecto de \(B\).

La misma fuente construye
\[
 C=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\qquad
 R=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 c_*=(1,1,1,1,1,1,2,1,1,1,1,1)
\]
y
\[
 P_j=\begin{cases}R,&(c_*)_j=1,\\ I_2,&(c_*)_j=2,\end{cases}
 \qquad g_c=\bigoplus_jP_jCP_j^{-1}.
\]
Aquí \(P_j\) es un marco bidimensional; \(P_3\) es el proyector de rango tres anterior. La prueba del propietario establece
\[
 g_c^3=I,\quad g_c^2+g_c+I=0,\quad
 g_c^{\mathsf T}Bg_c=B,\quad g_c\Lambda=\Lambda.
\]
La estabilidad del vecino utiliza que las clases de
\((g_cv_\alpha-v_\alpha)/3\) y \((g_c^{-1}v_\alpha-v_\alpha)/3\)
son \(c_*\) y \(-c_*\) y que ambos productos con \(v_\alpha\) son \(-27\).

## Flujo anisótropo de covolumen constante

Para un parámetro real adimensional \(s\), definimos
\[
 H_u=\bigoplus_{j=1}^{12}u_jI_2,\qquad
 D_s=\exp(sH_u)=\bigoplus_{j=1}^{12}e^{su_j}I_2,\qquad
 \Lambda_s=D_s\Lambda.
\]
El operador escala cada plano por el coeficiente de polarización que corresponde a su etiqueta. La desigualdad \(e^{su_j}>0\) conserva su orientación local. La familia satisface
\[
 D_{s+t}=D_sD_t,\quad D_0=I,\quad D_s^{-1}=D_{-s},
 \quad D_s^\dagger=D_s,\quad D_sg_c=g_cD_s,
\]
donde \(A^\dagger=B^{-1}A^{\mathsf T}B\). Las primeras identidades se verifican bloque a bloque. La autoadjunción procede de que cada bloque es escalar, y la conmutación utiliza la misma descomposición por planos de \(g_c\). Finalmente,
\[
 \det D_s=\prod_{j=1}^{12}e^{2su_j}
 =\exp\!\left(2s\sum_j u_j\right)=1.
\]
Así, \(\Lambda_s\) es una red discreta de rango \(24\) y covolumen uno para todo \(s\), porque una aplicación lineal invertible transporta una red y multiplica su covolumen por su determinante absoluto. La isometría \(g_c\) preserva cada \(\Lambda_s\):
\[
 g_c\Lambda_s=g_cD_s\Lambda=D_sg_c\Lambda=D_s\Lambda.
\]
Conserva su orden tres y su ausencia de vectores fijos. La construcción preserva esta simetría explícita; no transporta automáticamente todo el grupo de automorfismos de Leech.

El parámetro \(s\) queda libre en esta familia. La nota deriva la dirección \(u\) del registro y construye su flujo; no selecciona un valor físico de \(s\). Una normalización \(u/\|u\|\) produciría la misma familia con otra parametrización.

## Dualidad euclídea exacta

Para una red \(L\subset E\), su dual es
\[
 L^*=\{y\in E:\langle y,x\rangle_B\in\mathbb Z
                    \text{ para todo }x\in L\}.
\]
Si \(A\) es invertible, la definición da
\[
 (AL)^*=A^{-\dagger}L^*.
\]
En efecto, \(\langle y,Ax\rangle_B=\langle A^\dagger y,x\rangle_B\) es entero para todo \(x\in L\) exactamente cuando \(A^\dagger y\in L^*\). Aplicando la identidad a \(A=D_s\), la autodualidad de la red inicial y la autoadjunción de \(D_s\) prueban
\[
 \boxed{\Lambda_s^*=\Lambda_{-s}}.
\]
La igualdad es entre el dual euclídeo de una red y la red del parámetro opuesto. La condición adicional \(\Lambda_s=\Lambda_s^*\) equivale a \(D_{2s}\Lambda=\Lambda\), y no se deduce de \(\det D_s=1\). Por esta razón, en el flujo euclídeo se utiliza «covolumen uno» y se reserva «unimodular» en sentido aritmético para las redes integrales autoduales.

## Testigo explícito de deformación efectiva

El vector \(v_\alpha/3\) pertenece a \(\Lambda\). Su norma transportada es
\[
 f(s)=\left\|D_s\frac{v_\alpha}{3}\right\|_B^2
 =\frac29\left(16e^{2su_1}+\sum_{j=2}^{12}e^{2su_j}\right).
\]
Se obtiene
\[
 f(0)=6,\qquad
 f'(0)=\frac49\left(16u_1+\sum_{j=2}^{12}u_j\right)
       =\frac{20}{3}u_1
       =-825-\frac{466}{3}\sqrt5\ne0.
\]
Por continuidad de \(f'\), existe \(\delta>0\) tal que \(f\) es estrictamente monótona en \((-\delta,\delta)\). Reduciendo \(\delta\), también se cumple \(11/2<f(s)<13/2\). Por tanto, para \(0<|s|<\delta\), el valor \(f(s)\) es distinto de \(6\) y no es entero. Una red integral tiene norma entera en todos sus vectores; se concluye que \(\Lambda_s\) no es integral y, en particular, no es isométrica al retículo de Leech en ese intervalo perforado.

Esta prueba distingue deformación geométrica de cambio de coordenadas isométrico. Los coeficientes aparecen en pares opuestos, pero una permutación ambiental que intercambie esos pares no ha sido demostrada aquí como automorfismo del retículo pegado. La reciprocidad del dual no depende de esa afirmación adicional.

## Función theta y reciprocidad por Poisson

Para \(s\in\mathbb R\) y \(t>0\), sea
\[
 \Theta_s(t)=\sum_{\lambda\in\Lambda}
                  \exp\!\left(-\pi t\|D_s\lambda\|_B^2\right).
\]
Si \(M=\max_j|u_j|\), entonces
\[
 e^{-2|s|M}\|x\|_B^2\leq\|D_sx\|_B^2
                  \leq e^{2|s|M}\|x\|_B^2.
\]
La cota inferior compara la serie con una gaussiana sobre una red fija. Esto prueba convergencia absoluta y uniforme sobre compactos de \(\mathbb R\times(0,\infty)\), así como la legitimidad de las derivadas de orden finito después de incorporar sus factores polinomiales.

Tomamos el volumen euclídeo asociado a \(B\) y la convención de Fourier
\[
 \widehat f(y)=\int_E f(x)e^{-2\pi i\langle x,y\rangle_B}\,dx.
\]
La transformada de \(e^{-\pi t\|x\|_B^2}\) es
\(t^{-12}e^{-\pi\|y\|_B^2/t}\). La suma de Poisson, el covolumen uno y la identidad del dual dan
\[
 \boxed{\Theta_s(t)=t^{-12}\Theta_{-s}(t^{-1})}.
\]
En particular, \(\Theta_s(1)=\Theta_{-s}(1)\). Es una identidad analítica de series completas; el verificador finito no la sustituye por una suma truncada.

La extensión holomorfa
\[
 \theta_s(\tau)=\sum_{\lambda\in\Lambda}
        e^{\pi i\tau\|D_s\lambda\|_B^2},
 \qquad \operatorname{Im}\tau>0,
\]
converge normalmente y satisface
\[
 \theta_s(-1/\tau)=(-i\tau)^{12}\theta_{-s}(\tau).
\]
La transformación relaciona dos miembros de la familia. La periodicidad bajo \(\tau\mapsto\tau+1\), y por ello la promoción a una forma modular escalar del mismo tipo que la theta de Leech, requiere condiciones aritméticas adicionales. El testigo anterior muestra que la paridad e integralidad euclídeas se pierden para pequeños parámetros no nulos. Por la misma razón, la construcción de un álgebra de vértices reticular y sus resultados Moonshine no se transporta sin verificar sus hipótesis.

La suma de Poisson puede verificarse aquí directamente. Para una red \(L\) y la gaussiana \(f_t(x)=e^{-\pi t\|x\|_B^2}\), periodizamos
\[
 F_t(x)=\sum_{\ell\in L}f_t(x+\ell).
\]
La convergencia normal, también de las derivadas, hace de \(F_t\) una función suave sobre \(E/L\). Para \(\xi\in L^*\), su coeficiente de Fourier es
\[
 c_\xi=\frac1{\operatorname{covol}(L)}
       \int_{E/L}F_t(x)e^{-2\pi i\langle x,\xi\rangle_B}\,dx
 =\frac{\widehat f_t(\xi)}{\operatorname{covol}(L)}.
\]
La segunda igualdad descompone \(E\) en traslaciones de un dominio fundamental; el carácter vale uno sobre \(L\). El producto de las integrales gaussianas unidimensionales en una base ortonormal da
\(\widehat f_t(\xi)=t^{-12}e^{-\pi\|\xi\|_B^2/t}\).
Evaluar la serie de Fourier absolutamente convergente en \(x=0\) prueba la fórmula usada. Esta demostración y las convenciones de theta pueden cotejarse en [Noam D. Elkies, *Theta functions and weighted theta functions of Euclidean lattices, with some applications*, teorema 2, pp. 10–11](https://people.math.harvard.edu/~elkies/aws09.pdf). La fuente usa el signo positivo en Fourier; ambas convenciones coinciden sobre la gaussiana par.

## Realización integral duplicada de signatura \((24,24)\)

Sobre \(E\oplus E\) consideramos la forma bilineal
\[
 \mathcal B((x,p),(x',p'))=\langle x,p'\rangle_B+
                                      \langle p,x'\rangle_B.
\]
Su signatura es \((24,24)\). Definimos
\[
 \mathcal D_s=D_s\oplus D_{-s},\qquad
 \Gamma_s=\mathcal D_s(\Lambda\oplus\Lambda)
         =\{(D_s\lambda,D_{-s}\mu):\lambda,\mu\in\Lambda\}.
\]
La autoadjunción y reciprocidad de los bloques prueban
\(\mathcal B(\mathcal D_s\xi,\mathcal D_s\eta)=\mathcal B(\xi,\eta)\).
Por tanto \(\mathcal D_s\in O(\mathcal B)\).

La red \(\Gamma_0=\Lambda\oplus\Lambda\) es integral y par para \(\mathcal B\), porque los productos cruzados son enteros y
\[
 \mathcal B((\lambda,\mu),(\lambda,\mu))=2\langle\lambda,\mu\rangle_B
 \in2\mathbb Z.
\]
Su dual respecto de \(\mathcal B\) es ella misma: al emparejar con \((\lambda,0)\) y \((0,\mu)\), las dos coordenadas de un vector dual deben pertenecer a \(\Lambda^*=\Lambda\). Como \(\mathcal D_s\) es isometría de \(\mathcal B\), toda \(\Gamma_s\) es integral, par y autodual para esta forma partida.

La integralidad partida sobrevive incluso cuando la proyección euclídea \(\Lambda_s\) deja de ser integral. Son dos afirmaciones con métricas y dominios diferentes. Las \(\Gamma_s\) son isométricas como redes abstractas partidas; su presentación mediante las dos proyecciones euclídeas varía con \(s\).

La involución \(J(x,p)=(p,x)\) verifica
\[
 J\Gamma_s=\Gamma_{-s},\qquad
 J\mathcal D_sJ=\mathcal D_{-s}.
\]
En las coordenadas \(p_L=(x+p)/\sqrt2\), \(p_R=(x-p)/\sqrt2\),
\[
 \mathcal B((x,p),(x,p))=\|p_L\|_B^2-\|p_R\|_B^2;
\]
\(J\) fija \(p_L\) e invierte \(p_R\). Esta es una dualidad exacta de la construcción reticular duplicada; una identificación física específica conserva además los datos de representación que requiera su dominio.

## Energía positiva y conjugación unitaria

El análogo reticular de la energía de radio recíproco del artículo IV es
\[
 \mathcal E_s(\lambda,\mu)=
       \|D_s\lambda\|_B^2+\|D_{-s}\mu\|_B^2.
\]
Satisface
\[
 \mathcal E_s(\lambda,\mu)=\mathcal E_{-s}(\mu,\lambda).
\]
En \(\ell^2(\Lambda\oplus\Lambda)\), el operador de multiplicación
\[
 (H_s\psi)(\lambda,\mu)=\mathcal E_s(\lambda,\mu)\psi(\lambda,\mu)
\]
tiene dominio
\[
 \mathcal D(H_s)=
 \left\{\psi:\sum_{\lambda,\mu}
       \mathcal E_s(\lambda,\mu)^2|\psi(\lambda,\mu)|^2<\infty\right\}.
\]
Es positivo y autoadjunto. La cota cuadrática inferior implica que sólo existen finitos pares de red por debajo de cada nivel de energía, y por ello su resolvente es compacto. La aplicación unitaria
\((U\psi)(\lambda,\mu)=\psi(\mu,\lambda)\) satisface
\[
 U\mathcal D(H_s)=\mathcal D(H_{-s}),\qquad UH_sU^{-1}=H_{-s}.
\]
La igualdad conserva los dominios, además de los autovalores. Esta composición recupera la estructura del teorema de dualidad escalar del artículo IV y la realiza en los doce planos marcados.

## Localizadores internos y alcance del certificado

Raíz IV:

/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/04_MOONSHINE_DUALIDAD_TEORIA_M_ES/documentacion_original/payload/

- sections/excepcional.tex:601–750: doce factores, pegado de Niemeier y vecino de Leech; etiquetas exc:leech, exc:vector, exc:vecino y exc:teorema-leech.
- sections/moonshine_comparacion.tex:28–120: marcos, isometría de orden tres y estabilidad del vecino; etiquetas km:coxeter-reflexion, km:palabra-total, km:isometria-ternaria, km:estabilidad-vecino.
- sections/moonshine_comparacion.tex:128–190: continuación reticular hacia el álgebra de vértices y orbifold; sus hipótesis de paridad e integralidad no se trasladan al flujo euclídeo automáticamente.
- sections/02_dualidad_t.tex:14–140: energía de radio recíproco, dominio y conjugación unitaria; etiquetas iv:thm:dualidad-escalar e iv:thm:t-unitaria.

Raíz X:

/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/

- source/libro/01_acoplamiento.tex:52–125: genealogía del registro dodecafásico y \(K\).
- source/sections/k_direccion_dimensional.tex:13–98: representación marcada, proyector \(P_3\), vector \(u\), suma nula y norma exacta.
- supplement/vendor/variacional/controles_articulo_I/propietarios_k_moonshine/variacional.py:77–234 y 306–364: operaciones exactas en \(\mathbb Q(\sqrt5)\), suma de carácter, proyector y código.

La huella del propietario ejecutable utilizado es

bd1bfff1abec55e2f03477875002d44c01a9732c15348c99f9e211148c900e57

El certificado adjunto comprueba con racionales exactos el proyector, las doce coordenadas, la métrica, la acción de orden tres, la conmutación infinitesimal, los desplazamientos del vecino y la derivada no integral. También comprueba la forma partida y las identidades formales que sostienen el flujo. Las afirmaciones para todos los parámetros, la convergencia y Poisson tienen las pruebas analíticas contiguas anteriores; el cálculo finito no se presenta como prueba autónoma de esos teoremas.

