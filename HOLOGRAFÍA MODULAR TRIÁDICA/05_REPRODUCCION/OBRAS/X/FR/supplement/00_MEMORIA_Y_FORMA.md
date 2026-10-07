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
