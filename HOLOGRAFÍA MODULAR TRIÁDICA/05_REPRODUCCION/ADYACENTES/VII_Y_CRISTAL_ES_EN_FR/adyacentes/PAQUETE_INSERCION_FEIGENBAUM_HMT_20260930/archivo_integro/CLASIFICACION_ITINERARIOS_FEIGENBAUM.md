# Clasificación de los retornos superestables anteriores al itinerario infinito y convergencia del selector global

## 1. Objeto y procedencia

Este apéndice conserva la familia publicada por el lector dodecafásico HMT:

\[
u_0(x)=\frac1{12}\sum_{m=1}^{12}\left(1-\cos\frac{2(3m-1)x}{\sqrt{899}}\right),
\qquad f_\lambda(x)=1-\lambda u_0(x).
\]

La construcción APP–TRIT–TPK del perfil, sus coeficientes y sus lectores precede a este argumento. El objeto del apéndice es el transporte del selector de raíces ya fijado en `c37_feigenbaum.tex`, líneas 247–256; se conserva íntegramente su definición. Las propiedades analíticas y de unimodalidad de esta familia constan en `DESARROLLO_DEMOSTRATIVO_FEIGENBAUM.md`; la existencia y compacidad del conjunto de parámetros con itinerario infinito, junto con sus márgenes de separación, están demostradas en §§6.1–6.2 de `PROLONGACION_NONADICA_Y_LIMITE_FEIGENBAUM.md`.

El argumento siguiente es propio y utiliza exclusivamente esas propiedades y las operaciones de retorno de la familia fijada. No utiliza como entrada un parámetro de otra familia ni el valor de una constante universal. Las hojas de los itinerarios aquí utilizados son las dos ramas monótonas del lector crítico; las restantes coordenadas y la memoria HMT conservan su residencia en el estado del que procede el lector.

Escribimos
\[
c_j(\lambda)=f_\lambda^j(0),\qquad
\tau_j=(-1)^{v_2(j)},\qquad
W_n=\tau_1\cdots\tau_{2^n-1}.
\]
El itinerario de una órbita crítica que retorna por primera vez al origen termina en el símbolo cero. El orden de itinerarios es el orden unimodal de máximo: antes de comparar el símbolo de índice \(j\), el factor de orientación es
\[
O_{j-1}(K)=\prod_{i=1}^{j-1}(-K_i).
\]
El orden ordinario de los símbolos es \(-1<0<1\).

## 2. Clasificación anterior a la palabra infinita

**Teorema 1.** Sea \(F:I\to I\), con \(I=[\ell,1]\), \(\ell<0\), un mapa continuo, estrictamente creciente a la izquierda de cero y estrictamente decreciente a su derecha, cuyo máximo satisface \(F(0)=1\). Supóngase que cero tiene período exacto \(2^n\), con \(n\ge1\), y que su itinerario crítico \(K\) satisface \(K<\tau\). Entonces
\[
\boxed{K=W_n0.}
\]
La conclusión se refiere al itinerario, y permite que parámetros distintos de una familia tengan ese mismo itinerario.

**Demostración.** Denotemos \(d_j=F^j(0)\). Para período dos el itinerario es \(+0=W_10\). Consideremos un período exacto \(p=2^n\ge4\).

Se tiene \(d_2<0\). En efecto, \(d_2=0\) daría período dos. Si \(d_2>0\), la monotonía de la rama positiva da
\[
F([d_2,1])=[d_2,d_3]\subset[d_2,1],
\]
y la órbita crítica permanece en un intervalo estrictamente positivo, incompatible con el retorno a cero.

Los signos iniciales son entonces \(+,-\). El factor de orientación para comparar el tercer signo es \(-1\); por ello \(K<\tau\) obliga a \(d_3>0\). Un cero en ese lugar produciría período tres.

Tampoco puede ocurrir \(d_4<0\). Bajo esta hipótesis,
\[
d_2<d_4<0,
\qquad F([d_2,d_4])=[d_3,d_5]\subset(0,1],
\]
pues \(d_4=F(d_3)>F(1)=d_2\) y \(d_5=F(d_4)>F(d_2)=d_3\). La rama positiva es decreciente, de modo que
\[
F^2([d_2,d_4])=[d_6,d_4]\subset[d_2,d_4].
\]
Aquí \(d_6\ge d_2\), porque \(d_5\le1\), y \(d_6<d_4\), porque \(d_5>d_3\). Este intervalo estrictamente negativo atrapa los retornos pares de la órbita crítica, y excluye el retorno a cero. Por tanto \(d_4\ge0\). Si \(p=4\), se obtiene precisamente \(+-+0=W_20\).

Supongamos ahora \(p\ge8\). Entonces \(d_4>0\). Los factores de orientación para los signos quinto y sexto son, respectivamente, \(-1\) y \(+1\). Como \(\tau_5=+1\) y \(\tau_6=-1\), la desigualdad \(K<\tau\) obliga a
\[
\operatorname{sign}(d_1,\ldots,d_6)=(+,-,+,+,+,-).
\tag{1}
\]
Los signos cero en esos lugares están excluidos por el período exacto.

Construimos el intervalo de retorno
\[
J=[d_2,d_4].
\]
La desigualdad \(F(d_3)=d_4>0>d_6=F(d_5)\), junto con \(d_3,d_5>0\), implica \(d_3<d_5\); por tanto
\[
F(J)=[d_3,1].
\]
Además \(d_4<d_3\). Para comprobarlo, la imagen por \(F\) del intervalo de extremos \(d_3,d_4\) es estrictamente positiva, pues sus imágenes extremas son \(d_4,d_5>0\). En ese intervalo \(F^2\) es estrictamente creciente. Sus valores extremos satisfacen
\[
F^2(d_3)=d_5>0>d_6=F^2(d_4),
\]
lo que fuerza \(d_3>d_4\). En consecuencia,
\[
J\cap F(J)=\varnothing,
\qquad F^2(J)=F([d_3,1])=[d_2,d_4]=J.
\tag{2}
\]

El mapa \(F^2|_J\) posee un único mínimo en cero. La conjugación por \(h(x)=d_2x\), que invierte la orientación, define
\[
G=h^{-1}\circ F^2\circ h:
\left[\frac{d_4}{d_2},1\right]\longrightarrow
\left[\frac{d_4}{d_2},1\right].
\tag{3}
\]
Este mapa satisface las mismas hipótesis de máximo que \(F\), con \(G(0)=1\), y su crítico tiene período exacto \(p/2\). Su itinerario es
\[
K'_j=-K_{2j}.
\tag{4}
\]
Todos los símbolos impares de \(K\) son positivos, porque las posiciones pares pertenecen a \(J\) y las impares a \(F(J)\subset(0,1]\).

La transformación (4) conserva el orden de comparación con \(\tau\). En efecto, \(\tau_{2j-1}=+1\) y \(\tau_{2j}=-\tau_j\). Si \(q\) es el primer lugar en que \(K'\) y \(\tau\) difieren, el primer lugar de diferencia entre \(K\) y \(\tau\) es \(2q\), y
\[
O_{2q-1}(K)=-O_{q-1}(K'),
\qquad K_{2q}-\tau_{2q}=-(K'_q-\tau_q).
\tag{5}
\]
El producto que determina el orden es idéntico. Las identidades siguen siendo válidas cuando el primer símbolo distinto es el cero final. Así \(K'<\tau\).

La inducción aplicada a \(G\) da \(K'=W_{n-1}0\). Las posiciones impares positivas y (4) reconstruyen exactamente \(K=W_n0\). Queda demostrado el teorema. □

El teorema demuestra también que cada mapa clasificado posee los retornos restrictivos de duplicación anteriores a su retorno superestable, con los dominios de (2)–(3). No presupone una monotonía del parámetro de una familia.

**Normalización simétrica de la familia fijada.** Cuando \(F\) es par y está definido sobre \([-1,1]\), las desigualdades anteriores dan además
\[
F(d_4)=d_5>d_3=F(d_2)=F(-d_2).
\]
Como ambos argumentos \(d_4,-d_2\) son positivos y \(F\) decrece en esa rama,
\[
0<d_4<-d_2<1.
\tag{5a}
\]
Por tanto \(F^2([d_2,-d_2])=[d_2,d_4]\), y la misma conjugación \(h(x)=d_2x\) define sobre todo \([-1,1]\) un mapa par de máximo cuya imagen es \([d_4/d_2,1]\subset[-1,1]\). Coincide exactamente con el operador \(RF=-F(F(-ax))/a\), \(a=-F(1)\), utilizado en el corpus. Esta ampliación simétrica conserva el retorno crítico, su período y su itinerario.

## 3. Primer parámetro de itinerario infinito

Trabajamos sobre el intervalo compacto ya utilizado en la demostración de existencia,
\[
L=\left[\frac1{2u_0(1)},\frac2{u_0(1)}\right].
\]
Sea
\[
\Lambda_\tau=\{\lambda\in L:
\operatorname{sign}c_j(\lambda)=\tau_j\text{ para todo }j\ge1\}.
\]
Por §§6.1–6.2 del desarrollo de prolongación, este conjunto es no vacío y compacto. Por tanto existe
\[
a=\min\Lambda_\tau.
\tag{6}
\]

**Lema 2.** Para todo \(\lambda\in[1/(2u_0(1)),a)\), se tiene \(K_\lambda<\tau\).

**Demostración.** En el extremo izquierdo, el itinerario es \(+^\infty<\tau\). El argumento de separación de §6.1 demuestra que los conjuntos de comparación estricta con \(\tau\) son abiertos: en un itinerario infinito distinto de \(\tau\), la primera diferencia finita persiste por continuidad; en un parámetro superestable, las dos palabras periódicas vecinas y la palabra con cero final se sitúan en el mismo lado de \(\tau\), por su maximalidad estricta. El intervalo anterior a \(a\) carece, por definición, de parámetros con itinerario \(\tau\). Su conexidad mantiene la comparación inicial en todo ese intervalo. □

## 4. Existencia de cada primera raíz nueva

Conservamos el selector original. La primera raíz es
\[
\lambda_1=\frac1{u_0(1)},
\]
y, para \(n\ge2\), \(\lambda_n\) es la primera raíz de \(c_{2^n}\) situada a la derecha de \(\lambda_{n-1}\) que satisface
\[
c_{2^j}(\lambda_n)\ne0\quad(1\le j<n).
\tag{7}
\]
Como cualquier primer período que divida \(2^n\) es una potencia de dos, (7) equivale a exigir período crítico exacto \(2^n\).

**Lema 3.** Todas las raíces de este selector existen y cumplen
\[
\lambda_1<\lambda_2<\cdots<\lambda_n<a.
\tag{8}
\]

**Demostración.** El signo \(c_2(a)<0\) implica \(\lambda_1<a\). Supongamos construida \(\lambda_{n-1}<a\), y pongamos \(p=2^{n-1}\). La función analítica \(c_p(\lambda)\) no es idénticamente cero, puesto que \(c_p(a)\ne0\). Su conjunto de ceros en \([\lambda_{n-1},a]\) es finito, no vacío y carece de \(a\). Sea \(z<a\) su último cero.

En \((z,a]\), el signo de \(c_p\) es constante e igual a \(s=\tau_p\). Para \(g_\lambda=f_\lambda^p\), se tiene
\[
g_\lambda(0)=c_p(\lambda),\qquad g'_\lambda(0)=0.
\]
Una cota uniforme local de la segunda derivada da
\[
c_{2p}(\lambda)
=g_\lambda(c_p(\lambda))
=c_p(\lambda)+O(c_p(\lambda)^2).
\tag{9}
\]
Al aproximarse \(\lambda\) a \(z\) por la derecha, el término de primer orden domina; por tanto \(c_{2p}(\lambda)\) tiene signo \(s\). En \(a\), su signo es
\[
\tau_{2p}=-\tau_p=-s.
\]
El teorema del valor intermedio proporciona un cero \(\beta\in(z,a)\) de \(c_{2p}\). Como \(c_p\ne0\) en ese intervalo, el período crítico en \(\beta\) es exactamente \(2p\).

La analiticidad y \(c_{2p}(a)\ne0\) implican que los ceros de \(c_{2p}\) en \([\lambda_{n-1},a]\) son finitos. Entre sus ceros de período exacto \(2p\), situados a la derecha de \(\lambda_{n-1}\), existe así un primero. Es el selector original \(\lambda_n\), y satisface \(\lambda_n\le\beta<a\). □

La utilización del último cero auxiliar \(z\) pertenece únicamente a la prueba de existencia. El parámetro seleccionado continúa siendo la **primera raíz nueva** \(\lambda_n\).

## 5. Convergencia del selector global al primer itinerario infinito

**Teorema 4.** Para la familia HMT fijada y el selector original, todos los itinerarios seleccionados son canónicos y
\[
\boxed{K_{\lambda_n}=W_n0,\qquad
\lambda_n\nearrow\min\Lambda_\tau.}
\tag{10}
\]

**Demostración.** Los lemas 2–3 sitúan cada parámetro seleccionado por debajo de \(a\), con itinerario menor que \(\tau\). El teorema 1 identifica ese itinerario con \(W_n0\). La sucesión es creciente y acotada por \(a\); sea \(b\le a\) su límite.

Fijemos \(p\ge1\). Para \(n\) suficientemente grande, \(2p<2^n\). Entonces los signos de \(c_p(\lambda_n)\) y \(c_{2p}(\lambda_n)\) coinciden con \(\tau_p\) y \(\tau_{2p}=-\tau_p\), respectivamente. La cota de §6.2,
\[
\|(f_\lambda^p)''\|\le B_p,
\qquad B_p=16^p\frac{16^p-1}{15},
\]
y la identidad \((f_\lambda^p)'(0)=0\) implican
\[
|c_{2p}(\lambda_n)-c_p(\lambda_n)|
\le\tfrac12B_p|c_p(\lambda_n)|^2.
\]
Como los dos términos del lado izquierdo tienen signos contrarios,
\[
|c_p(\lambda_n)|>2/B_p.
\tag{11}
\]
Por continuidad, \(c_p(b)\) conserva el signo \(\tau_p\) y satisface \(|c_p(b)|\ge2/B_p>0\). Esto vale para cada \(p\), de modo que \(b\in\Lambda_\tau\). La minimalidad de \(a\) da \(b\ge a\), y por tanto \(b=a\). □

La prueba completa conserva el selector global y produce sus itinerarios y su límite. La información de los primeros ocho niveles es compatible con el resultado, pero la demostración de (10) no extrapola esos ocho niveles: utiliza inducción, intervalos invariantes y separación uniforme de cada signo.

## 6. Relación exacta con el cruce local certificado

Sea \(J=[J_{\rm lo},J_{\rm hi}]\) el intervalo del cruce local \(\lambda_*\) construido en `TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md`, §§5–8. Allí \(\lambda_*\in\Lambda_\tau\), y por ello
\[
a\le\lambda_*.
\]
Si se demuestra
\[
\Lambda_\tau\cap[\lambda_8,J_{\rm lo}]=\varnothing,
\tag{12}
\]
el teorema 4 implica
\[
J_{\rm lo}<a\le\lambda_*<J_{\rm hi}.
\tag{13}
\]
La identificación ulterior \(a=\lambda_*\) se deduce, por ejemplo, de que \(\lambda_*\) sea el único parámetro de \(J\) con itinerario \(\tau\). La unicidad de un cruce con una **hoja estable local** y la unicidad de todos los parámetros de itinerario \(\tau\) en \(J\) son afirmaciones distintas: para pasar de la primera a la segunda se debe controlar que los retornos de cualquier realización de \(\tau\) en \(J\) permanezcan en el dominio local, o demostrar un enunciado de aislamiento equivalente.

Análogamente, una vez identificado \(a=\lambda_*\), la igualdad eventual de las primeras raíces \(\lambda_n\) con los centros \(\mu_j\) de la continuación local se obtiene si, para cada período suficientemente grande, el centro local es el único centro de itinerario \(W_n0\) en un entorno pertinente de \(\lambda_*\) que contenga la cola de \(\lambda_n\). La correspondencia conserva el desplazamiento fijo de índices de §8. Estas son las condiciones concretas de transporte del selector; la conclusión (10) ya está demostrada sin ellas.

## 7. Controles lógicos y falsadores

1. El teorema 1 requiere un máximo unimodal estricto y un intervalo invariante. Si alguno de los dos ramos pierde monotonía, los intervalos (2) pueden dejar de ser restrictivos y la clasificación debe comprobarse de nuevo.
2. La condición \(K<\tau\) es esencial. Después de la palabra límite pueden existir centros de período \(2^n\) con otras combinatorias; el teorema no los identifica con \(W_n0\).
3. La analiticidad en el parámetro proporciona aislamiento y finitud de los ceros sobre el compacto. Para una familia solamente continua, la existencia de una primera raíz estrictamente posterior requiere un argumento adicional.
4. Un límite de raíces críticas puede, en general, perder signos al alcanzar un retorno de período menor. La desigualdad (11) excluye precisamente ese fenómeno para esta sucesión y cada horizonte fijo.
5. La convergencia de las primeras raíces al primer parámetro de itinerario \(\tau\) no equivale a la unicidad de todos los parámetros de ese itinerario ni determina por sí misma una tasa métrica. El cruce transversal y la identificación de la rama aportan esas conclusiones posteriores.

## 8. Transferencia métrica al selector original bajo la identificación del límite

En esta sección se conserva como hipótesis explícita la identificación
\[
\boxed{a_*:=\min\Lambda_\tau=\lambda_*.}
\tag{H}
\]
Su comprobación corresponde al aislamiento paramétrico de §6 y a su certificado específico. La demostración siguiente establece la consecuencia de (H); no utiliza la existencia de la cascada local como prueba de (H). Así queda separada la comprobación de aislamiento de la transferencia métrica.

**Nota de activación.** La hipótesis (H) queda demostrada en `TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md`, §16, mediante la primera salida del cono negativo y la cobertura racional completa de 64 bandas, sin huecos, de `CERTIFICADO_CAP_NEGATIVA_PRIMERA_SALIDA.json`. El enunciado condicional se conserva para exhibir esta dependencia de la transferencia; el resultado de §16 la satisface para la familia uniforme aquí estudiada.

La familia, el perfil dodecafásico, los retornos y el selector se mantienen exactamente como en §§1–5. Los resultados externos empleados a continuación reconocen la dinámica de ese objeto ya construido. Sus valores universales no intervienen en la selección de coeficientes ni de parámetros de la familia HMT.

**Teorema 5.** Supóngase (H), además de las cotas de entrada, admisibilidad y transversalidad de `TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md`, §§4–7. Entonces la sucesión original de primeras raíces nuevas satisface, para ciertas constantes \(C>0\) y \(0<\theta<1\),
\[
\boxed{\lambda_*-\lambda_n=C\delta^{-n}
\bigl(1+O(\theta^n)\bigr),}
\tag{14}
\]
donde \(\delta>1\) es el autovalor inestable del operador de duplicación en el punto fijo reconocido. En particular,
\[
\frac{\lambda_{n-1}-\lambda_{n-2}}
     {\lambda_n-\lambda_{n-1}}
=\delta+O(\theta^n).
\tag{15}
\]
La sucesión coincide eventualmente con los centros de la continuación local, una vez que ambos índices se refieren al mismo período físico. La prueba mantiene el selector de primera raíz de §1.

### 8.1. Obtención de un dominio cuadrático semejante común

Escribamos \(g\) para el punto fijo de la renormalización y
\(\Gamma(\lambda)=R^4f_\lambda\). La carta analítica utilizada en el certificado es
\[
f(x)=1-x^2V\!\left(\frac{x^2-1}{2.5}\right),\qquad
V(z)=\frac{u}{10}+\sum_{k\ge1}\nu_kz^k,
\]
con norma de diferencias \(|\Delta u|+\|\Delta\nu\|_1\). Las desigualdades de admisibilidad prueban que \(g\) es par, analítico, unimodal, cuadrático y de tipo de duplicación; además, \(g(x)=\varphi(x^2)\) con \(\varphi'<0\) en \([0,1]\).

El teorema 2.1 de de Faria–de Melo–Pinto, aplicado al conjunto de combinatorias formado únicamente por la duplicación, proporciona un conjunto límite de un solo punto con extensión cuadrática semejante. Como \(Rg=g\), la convergencia real de ese teorema identifica dicho punto con \(g\). El lema 3.2 proporciona, en un entorno analítico de \(g\), una iteración finita de renormalización con dominio cuadrático semejante y módulo uniformemente positivo. Los localizadores son §2.1–2.3, pp. 736–738, y §3.1, lema 3.2, p. 745, de [de Faria–de Melo–Pinto, *Global hyperbolicity of renormalization for Cr unimodal mappings*](https://annals.math.princeton.edu/wp-content/uploads/annals-v164-n3-p01.pdf).

Para comprobar la pertenencia al entorno de ese lema, sea \(\Omega_\epsilon\) un entorno complejo suficientemente pequeño de \([-1,1]\), con
\[
\rho_\epsilon:=\sup_{x\in\Omega_\epsilon}
\left|\frac{x^2-1}{2.5}\right|<1,
\qquad M_\epsilon:=\sup_{x\in\Omega_\epsilon}|x|^2<\infty.
\]
La restricción de la carta certificada satisface
\[
\|\Delta f\|_{\Omega_\epsilon}
\le M_\epsilon\left(\frac{|\Delta u|}{10}
          +\rho_\epsilon\|\Delta\nu\|_1\right)
\le C_\epsilon\|\Delta f\|_{\mathcal A}.
\tag{16}
\]
El certificado da
\[
\|R^m\Gamma(\lambda_*)-g\|_{\mathcal A}
<0.001666(0.83996)^m.
\]
Se elige por ello un entero fijo \(m\) que sitúe esta imagen en el entorno del lema 3.2. La continuidad de la composición finita proporciona un intervalo \(I_*\) alrededor de \(\lambda_*\) donde las mismas operaciones están definidas. Si \(N\) es la iteración suministrada por dicho lema, ponemos
\[
d=4+m+N,\qquad
\mathcal F_\lambda=R^df_\lambda,\quad \lambda\in I_*.
\tag{17}
\]
La familia \(\mathcal F\) posee representantes cuadráticos semejantes de grado dos, sobre un dominio común y con módulo positivo uniforme. Su dependencia analítica real admite una complejificación local del parámetro. El número \(d\) es fijo y cuenta las duplicaciones realizadas antes de aplicar el resultado paramétrico.

Esta construcción prueba la existencia del dominio y de \(d\); no les atribuye valores numéricos que el certificado local no haya calculado. La asintótica utiliza su finitud, no una estimación numérica de su tamaño.

### 8.2. Transporte de la transversalidad certificada

La dirección de \(\Gamma\) satisface el cono
\[
\|\dot\nu\|_1\le\tfrac14|\dot u|,\qquad \dot u\ne0.
\]
Las cotas diferenciales certificadas implican invariancia de este cono y
\[
|\dot u_{k+1}|\ge4.381|\dot u_k|
\tag{18}
\]
a lo largo de la órbita de \(\Gamma(\lambda_*)\). Todos sus puntos permanecen en el dominio certificado. En particular, la dirección transportada por los pasos finitos de (17) conserva una componente expansiva no nula.

La clase híbrida del punto fijo coincide con su variedad estable en el espacio de gérmenes cuadráticos semejantes: [Lyubich, *Feigenbaum–Coullet–Tresser universality and Milnor's hairiness conjecture*, teorema 6.1, pp. 371–372](https://www.maths.tcd.ie/EMIS/journals/Annals/149_2/lyubich.pdf). La transversalidad sigue siendo válida al pasar a ese espacio, como puede comprobarse sin identificar normas de Banach diferentes. En efecto, si \(\partial_\lambda\mathcal F_{\lambda_*}\) fuese tangente a la clase híbrida, sería la tangente de un disco analítico contenido en ella. La convergencia exponencial uniforme de la renormalización sobre un subdisco compacto, seguida de la estimación de Cauchy en su parámetro, haría converger a cero la evaluación en \(x=1\) de sus tangentes renormalizadas. Sin embargo, en la carta anterior,
\[
\dot f(1)=-\dot u/10,
\]
y (18) hace crecer su valor absoluto. Ambas derivadas representan el mismo germen y tienen la misma evaluación real. La contradicción demuestra
\[
\partial_\lambda\mathcal F_{\lambda_*}
\notin T_{\mathcal F_{\lambda_*}}\mathcal H_{c_\infty}.
\tag{19}
\]
Así, \(S=\{\mathcal F_\lambda\}\) es una transversal analítica compleja a la clase híbrida del límite de duplicación.

### 8.3. Identificación eventual de las primeras raíces por su período

Denotemos por \(c_r\) el centro cuadrático canónico de período \(2^r\), obtenido mediante \(r\) duplicaciones sucesivas del centro de período uno. Este símbolo designa el parámetro de la familia cuadrática de reconocimiento; se distingue de las funciones orbitales \(c_j(\lambda)=f_\lambda^j(0)\) de las secciones anteriores. Si se desea evitar cualquier coincidencia tipográfica, puede escribirse \(c_r^{\rm quad}\).

El teorema 4 y (H) dan \(\lambda_n\to\lambda_*\), por lo que \(\lambda_n\in I_*\) para \(n\) suficientemente grande. La clasificación e intervalos restrictivos de §2 muestran que, cuando \(n>d\),
\[
\mathcal F_{\lambda_n}=R^df_{\lambda_n}
\quad\text{tiene período crítico exacto }2^{n-d}
\quad\text{e itinerario }W_{n-d}0.
\tag{20}
\]
Su órbita crítica permanece en el intervalo real invariante, contenido en el dominio cuadrático semejante; su conjunto de Julia lleno es, por tanto, conexo. La rectificación conserva la órbita postcrítica y las ramas reales. Al recorrer sus retornos restrictivos se obtienen \(n-d\) duplicaciones canónicas y, al final, un punto crítico fijo. Este último rectifica al centro \(0\); las inversas sucesivas de la rectificación de las copias de duplicación dan el centro único \(c_{n-d}^{\rm quad}\). Esta es la aplicación concreta de la parametrización por combinatoria y del homeomorfismo de rectificación de las copias, descritos en Lyubich, §5.1–5.3, pp. 362–364. Se concluye
\[
\mathcal F_{\lambda_n}\in\mathcal H_{c_{n-d}^{\rm quad}}.
\tag{21}
\]

El teorema 7.4 de Lyubich, pp. 387–388, da una única intersección local de \(S\) con cada clase \(\mathcal H_{c_r^{\rm quad}}\) para \(r\) suficientemente grande. Sus hipótesis de cotas complejas a priori se cumplen para la cascada cuadrática real de duplicación, conforme al teorema 5.6, p. 367, del mismo trabajo. Escribamos \(\zeta_r\) para el parámetro de esa intersección. Las ecuaciones (20)–(21), la convergencia al cruce y la unicidad local implican
\[
\boxed{\lambda_n=\zeta_{n-d}\quad\text{para todo }n\text{ suficientemente grande}.}
\tag{22}
\]
La unicidad utilizada aquí corresponde a **cada clase híbrida canónica** en un entorno fijo del cruce. No se infiere de la mera existencia de una cascada local ni de la unicidad del cruce con la hoja estable. La ecuación (22) identifica el selector original, ya definido globalmente, con las intersecciones locales; no introduce un selector sustitutorio.

En particular, sea \(\mu_j\) la cascada local de §8 del documento principal, y sea \(s\) el entero fijo determinado por su período físico exacto:
\[
\operatorname{per}_{\rm crit}(f_{\mu_j})=2^{j+s}.
\]
En la presentación con curva \(R^4f_\lambda\) y blanco de período dos, \(s=5\); los pasos fijos adicionales usados para localizar el blanco modifican \(s\). Por (21) y la misma unicidad,
\[
\mu_j=\zeta_{j+s-d},\qquad
\boxed{\lambda_n=\mu_{n-s}\quad(n\text{ suficientemente grande}).}
\tag{23}
\]
El desplazamiento \(d\) de la preparación cuadrática semejante y el desplazamiento \(s\) de los períodos del blanco son objetos distintos. La identificación se efectúa por el período físico, no igualando esos dos enteros.

### 8.4. Resto de potencia mediante holonomía transversal

El lema 7.3 de Lyubich, p. 384 y demostración en pp. 384–387, aporta regularidad \(C^{1+\beta}\)-conforme, para algún \(\beta>0\), de la holonomía entre transversales a la clase híbrida del punto de Feigenbaum. Su definición en p. 384 se refiere a los conjuntos de conexidad sobre las transversales; contiene, en particular, los centros considerados aquí. Podemos reducir el exponente para que \(0<\beta\le1\).

Sea \(h\) la holonomía desde \(S\) hacia la variedad inestable y sea \(z\) una coordenada analítica que linealiza la restricción unidimensional de la renormalización:
\[
z(g)=0,\qquad z(Rq)=\delta z(q).
\tag{24}
\]
La existencia de esta coordenada se obtiene aplicando la linealización de un germen holomorfo repulsor, de multiplicador \(\delta>1\), a la variedad inestable analítica. La dirección expansiva de (18), la invariancia del cono y el retorno estacionario identifican ese multiplicador con el autovalor inestable positivo empleado en el certificado.

Si \(q_r\) es el centro de la clase \(\mathcal H_{c_r^{\rm quad}}\) situado en la variedad inestable, la compatibilidad de rectificación y renormalización da \(Rq_r=q_{r-1}\). Esta identidad es la que se utiliza en la demostración del teorema 7.4, p. 388. Por (24), existe \(b\ne0\), que absorbe cualquier índice inicial fijo, tal que
\[
z(q_r)=b\delta^{-r}
\tag{25}
\]
para todo \(r\) suficientemente grande.

La regularidad de \(h\) y la transversalidad (19) dan, sobre el conjunto de conexidad cercano a \(\lambda_*\),
\[
H(\lambda):=z\bigl(h(\mathcal F_\lambda)\bigr)
=A(\lambda-\lambda_*)
+O\!\left(|\lambda-\lambda_*|^{1+\beta}\right),
\qquad A\ne0.
\tag{26}
\]
Como \(H(\zeta_r)=b\delta^{-r}\), la estimación inferior
\(|H(\lambda)|\ge |A|\,|\lambda-\lambda_*|/2\) en un entorno suficientemente pequeño implica primero
\(|\zeta_r-\lambda_*|=O(\delta^{-r})\). Sustituyendo esta cota en el resto de (26), resulta
\[
\zeta_r-\lambda_*=rac bA\delta^{-r}
+O\!\left(\delta^{-(1+\beta)r}\right).
\tag{27}
\]
Aplicamos (22) con \(r=n-d\). El desplazamiento finito modifica el coeficiente principal y la constante del resto. Puesto que \(\lambda_n<\lambda_*\), se obtiene (14), con
\[
C=-\frac bA\delta^d>0,
\qquad \theta=\delta^{-\beta}\in(0,1).
\]
Finalmente,
\[
\lambda_n-\lambda_{n-1}
=C(\delta-1)\delta^{-n}\bigl(1+O(\theta^n)\bigr),
\]
lo que demuestra (15). □

### 8.5. Alcance cuantitativo y condición de activación

El argumento prueba la existencia de un resto geométrico para las **primeras raíces globales** cuando se verifica (H). La tasa \(0.83996\) ya certificada controla la convergencia de los mapas renormalizados sobre la hoja estable. La tasa \(\theta=\delta^{-\beta}\) de (14) controla la transferencia al parámetro mediante la holonomía; ambas conservan sus dominios respectivos.

Esta sección no asigna valores certificados a \(\beta\), \(\theta\), \(C\), al tamaño del entorno \(I_*\), al número de retornos preparatorios \(d\) ni al primer índice de coincidencia de (22)–(23). La prueba asintótica requiere que existan, y las construcciones anteriores acreditan esa existencia. Para activar el teorema 5 en la familia concreta se incorpora la demostración material de (H); un certificado de primeras raíces finitas o un cruce estable único, considerados aisladamente, no sustituyen esa identificación.
