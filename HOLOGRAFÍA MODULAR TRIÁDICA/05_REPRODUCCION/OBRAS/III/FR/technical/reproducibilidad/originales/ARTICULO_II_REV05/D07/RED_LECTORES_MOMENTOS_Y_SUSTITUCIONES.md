# Composición de lectores, normalización y sustituciones espectrales

Ampliación exclusiva de OVERLEAF para la red común; corte fijo de 2.249 páginas. Se conservan los originales. Las construcciones fuente son RESULTADO_RECUPERADO. Las composiciones y demostraciones aquí reunidas desarrollan sus consecuencias, sin atribuir novedad histórica a identidades analíticas conocidas. La procedencia de una eventual prioridad adicional no se declara establecida.

## 1. Antecedente estructural y ámbito

La construcción APP–TRIT–TPK suministra, mediante sus realizaciones espectrales documentadas, el operador de numeración \(N\), los lectores residuales orientados y el funcional \(\mathcal Z_3\). El cuarto de giro procede de la incidencia y de su realización de \(C_4\); el lector módulo tres conserva las clases orientadas; su composición determina el carácter dodecafásico. La generación y selección de esos lectores anteceden a los momentos que se tratan aquí.

Las relaciones de este anexo operan en la realización posterior \(\ell^2(\mathbb N_{>0})\), con \(Ne_n=ne_n\), y en la continuación meromorfa que el corpus demuestra para \(\mathcal Z_3\). Es una prolongación del árbol ya documentado: no selecciona semillas con valores de Catalán, Apéry, Euler–Mascheroni, Glaisher ni datos metrológicos.

Fuentes: [lector residual y cuarto de giro](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c33_catalan_apery_euler.tex:23>), [límite de calor y funcional de Mellin](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/18_funcionales_espectrales_triadicos.tex:510>).

## 2. Del lector periódico a una familia completa de momentos

Sea \(a:\mathbb Z/q\mathbb Z\to\mathbb C\) la tabla de un lector residual ya construido y \(Q_a e_n=a(n)e_n\). La tabla fija signos, orientaciones y clases antes de evaluar. Para \(t>0\),
\[
K_a(t)=\operatorname{Tr}(e^{-tN}Q_a)
=\frac{P_a(e^{-t})}{1-e^{-qt}},
\qquad
P_a(r)=\sum_{j=1}^{q}a(j)r^j.
\]
Aquí \(j=q\) representa la clase cero. La prueba agrupa \(n=qk+j\) y suma una progresión geométrica absolutamente convergente.

Para \(\operatorname{Re}s>1\), el operador \(N^{-s}Q_a\) es traza–clase y
\[
\boxed{
M_a(s)=\operatorname{Tr}(N^{-s}Q_a)
=\frac1{\Gamma(s)}\int_0^\infty t^{s-1}K_a(t)\,dt.}
\]
En efecto, la suma de las integrales de valores absolutos está acotada por
\(\|a\|_\infty\Gamma(\operatorname{Re}s)\sum n^{-\operatorname{Re}s}\).
Para \(k\ge0\), la convergencia local uniforme en ese semiplano permite
\[
M_a^{(k)}(s)=
\operatorname{Tr}\bigl((- \log N)^kN^{-s}Q_a\bigr).
\]
Los valores, derivadas y partes finitas son operaciones diferentes sobre una función producida por la misma tabla residual.

**Recuperación.** Con el período declarado, la función completa \(K_a\) recupera
\[
P_a(r)=(1-r^q)K_a(-\log r),\qquad 0<r<1;
\]
los coeficientes de ese polinomio recuperan la tabla. Un único momento \(M_a(s_0)\) es sólo un funcional lineal de sus \(q\) coeficientes y, en general, no determina la tabla. Incluso la tabla completa conserva menos información que la historia enriquecida que la produce. El carácter residual y el estado fuente no se identifican.

La pérdida al conservar sólo un momento se exhibe dentro de los lectores periódicos: sea \(a(n)=1\) para \(n\) impar y \(a(n)=-3\) para \(n\) par. Entonces \(Q_a\ne0\), mientras
\[
M_a(2)=\left(\frac34-3\cdot\frac14\right)\mathcal Z_3(2)=0.
\]
Por tanto, ese momento coincide con el del lector nulo, aunque sus tablas y núcleos son diferentes. El ejemplo no identifica este lector auxiliar con un carácter de Dirichlet ni modifica los lectores seleccionados por HMT.

## 3. Componer lectores y multiplicar sus valores

Para dos tablas \(a,b\), extendidas al período común, se tiene
\[
Q_aQ_b=Q_{ab},\qquad
\operatorname{Tr}(N^{-s}Q_aQ_b)
=\sum_{n\ge1}a(n)b(n)n^{-s}.
\]
Esta composición mantiene el mismo índice espectral. En particular,
\(Q_{12}=Q_3Q_4\) compone los datos módulo tres y cuatro.

El producto de los valores tiene otra realización, que conserva pares de índices:
\[
\boxed{
M_a(s)M_b(s)=
\operatorname{Tr}_{\mathcal H\otimes\mathcal H}
\bigl((N\otimes N)^{-s}(Q_a\otimes Q_b)\bigr),
\quad \operatorname{Re}s>1.}
\]
La suma doble absoluta factoriza, pues el valor propio de \(N\otimes N\) en
\(e_m\otimes e_n\) es \(mn\). Una vez agrupada por \(k=mn\), se obtiene
\[
M_a(s)M_b(s)
=\sum_{k\ge1}\frac{(a*b)(k)}{k^s},
\qquad
(a*b)(k)=\sum_{d\mid k}a(d)b(k/d).
\]
El producto diagonal usa \(a(n)b(n)\); el producto de valores usa la convolución de divisores. La agrupación conserva la multiplicidad total y puede perder la identificación individual de los pares. Una tabla periódica multiplicada punto a punto sigue siendo periódica; la convolución de divisores no tiene por qué serlo.

Estas identidades proporcionan reglas de sustitución, no generadores independientes. La descomposición tensorial se realiza después de fijar ambos lectores; no afirma independencia estadística entre las historias HMT de las que proceden.

La estructura suma–producto también se distingue a nivel de semigrupos:
\[
\operatorname{Tr}\bigl(e^{-t(N\otimes N)}(Q_a\otimes Q_b)\bigr)
=\sum_{m,n\ge1}a(m)b(n)e^{-tmn},
\]
mientras
\[
K_a(t)K_b(t)
=\operatorname{Tr}\bigl(e^{-t(N\otimes I+I\otimes N)}(Q_a\otimes Q_b)\bigr).
\]
Ambas sumas convergen absolutamente para \(t>0\). La primera retiene el producto \(mn\); la segunda, la suma \(m+n\). Esta realización espectral conserva la distinción de operaciones; su correspondencia con transportes adicionales del estado enriquecido exige los entrelazadores propios y no se deduce de la notación tensorial.

## 4. Transporte de normalización y coeficientes de Laurent

Se considera un cambio positivo y adimensional de normalización del lector posterior, \(N\mapsto aN\), \(a>0\). No representa por sí mismo una nueva prolongación TPK ni una nueva constante física. En el semiplano de convergencia,
\[
\mathcal Z_a(s)=a^{-s}\mathcal Z_3(s).
\]
La identidad continúa meromórficamente junto con \(\mathcal Z_3\).

El corpus fija
\[
\mathcal Z_3(s)=\frac1{s-1}
+\sum_{n\ge0}\frac{(-1)^n\gamma_n}{n!}(s-1)^n.
\]
Para comparar coeficientes con residuo uno, se normaliza
\(\widehat{\mathcal Z}_a=a\mathcal Z_a\), y se escribe
\[
\widehat{\mathcal Z}_a(s)=\frac1{s-1}
+\sum_{n\ge0}\frac{(-1)^n\gamma_n(a)}{n!}(s-1)^n.
\]
Si \(\ell=\log a\), multiplicar por \(e^{-\ell(s-1)}\) da
\[
\boxed{
\gamma_n(a)=
\sum_{j=0}^{n}\binom nj\gamma_j\ell^{\,n-j}
-\frac{\ell^{\,n+1}}{n+1}.}
\]
Los dos primeros casos son
\[
\gamma_0(a)=\gamma_0-\ell,\qquad
\gamma_1(a)=\gamma_1+\gamma_0\ell-\frac{\ell^2}{2}.
\]
La transformación es triangular afín, invertible al sustituir \(\ell\) por \(-\ell\), y su composición corresponde a multiplicar las escalas. Los coeficientes transformados registran el cambio de normalización; no se confunden con los valores de la normalización original.

**Prueba del término polar.** El producto de \(1/(s-1)\) por la serie exponencial contribuye en grado \(n\) con
\((-1)^{n+1}\ell^{n+1}/(n+1)!\); su combinación con los términos regulares produce exactamente la fórmula. Omitir este término altera ya \(\gamma_0(a)\).

Fuente de la expansión: [Euler–Mascheroni y Stieltjes](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c33_catalan_apery_euler.tex:262>). La ley de cambio de normalización se explicita aquí por multiplicación de series.

## 5. Derivadas regularizadas, Glaisher y valores impares

En un punto \(-k\) donde la continuación es regular,
\[
\mathcal Z_a'(-k)
=a^k\bigl(\mathcal Z_3'(-k)-\log(a)\mathcal Z_3(-k)\bigr).
\]
Definiendo \(D_k(a)=\exp[-\mathcal Z_a'(-k)]\), resulta
\[
\boxed{
D_k(a)=D_k(1)^{a^k}\,
a^{\,a^k\mathcal Z_3(-k)}.}
\]
El corpus utiliza
\[
A_k=\exp\left(\frac{H_kB_{k+1}}{k+1}
-\mathcal Z_3'(-k)\right).
\]
Por tanto, \(D_k(1)=A_k\exp[-H_kB_{k+1}/(k+1)]\). Se conserva el término normalizador de Bernoulli: \(D_k\) y \(A_k\) coinciden sólo en los niveles donde ese término se anula.

En los niveles pares positivos,
\(\mathcal Z_3(-2n)=0\) y \(B_{2n+1}=0\), de modo que
\[
\frac{\log D_{2n}(a)}{a^{2n}}
=\log A_{2n}
=(-1)^{n+1}
\frac{(2n)!}{2(2\pi_{\rm HMT})^{2n}}\,
\mathcal Z_3(2n+1).
\]
Así, el cociente de la izquierda es invariante bajo ese transporte de normalización. Para \(n=1\),
\[
\boxed{\mathcal Z_3(3)=4\pi_{\rm HMT}^{\,2}\log A_2.}
\]
Se relacionan un valor convergente positivo y una derivada en la continuación negativa mediante la ecuación funcional que el corpus demuestra; no se sustituye uno por el otro por semejanza decimal.

Fuente: [definición de la familia y demostración](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c35_bendersky_glaisher.tex:1>).

## 6. Composición dodecafásica y término finito de Euler–Kronecker

Sea \(L_{12}(s)=M_{\chi_{12}}(s)\), continuación del momento del lector compuesto. El producto
\(\mathcal Z_3(s)L_{12}(s)\) se realiza tensorialmente en el semiplano de convergencia, según la sección 3. Al continuar hasta \(s=1\),
\[
\mathcal Z_3(s)L_{12}(s)
=\frac{L_1}{s-1}+\gamma_0L_1+L_1'+O(s-1).
\]
Su término finito dividido por el residuo es
\[
\boxed{\gamma_{12}=\gamma_0+\frac{L_1'}{L_1}.}
\]
El residuo
\(L_1=\log(2+\sqrt3)/\sqrt3\) vincula el mismo carácter al momento de Pell. El término adicional mide la derivada logarítmica del lector dodecafásico.

Si se aplica el mismo cambio de normalización \(F(s)\mapsto a^{-s}F(s)\) a ambos funcionales con polo simple, sus cocientes «término finito/residuo» cambian por \(-\log a\). Por consiguiente,
\[
\boxed{\gamma_{12}(a)-\gamma_0(a)=L_1'/L_1.}
\]
Aquí se escala una vez cada funcional total; no se escalan independientemente sus dos factores, lo que produciría otro exponente. La diferencia conserva una información residual que el cambio común de unidades espectrales no altera.

Fuente: [factorización y prueba del término finito](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c34_euler_kronecker_primos.tex:1>).

## 7. Sustitución física exacta: momento de Apéry y número de fotones

Se recibe del capítulo térmico, con su continuo bosónico, temperatura y normalización de Planck declarados,
\[
n_\gamma\ell_P^3=
\frac{2\mathcal Z_3(3)}{\pi_{\rm HMT}^2(\log3)^3}.
\]
La sustitución de la sección 5 da
\[
\boxed{
n_\gamma\ell_P^3=
\frac{8\log A_2}{(\log3)^3}
=-\frac{8\mathcal Z_3'(-2)}{(\log3)^3}.}
\]
La constante del gas fotónico queda vinculada directamente a la derivada regularizada del mismo funcional espectral. El factor \(\pi_{\rm HMT}^2\) se cancela algebraicamente; su función en las normalizaciones precedentes permanece documentada.

Con las otras dos ecuaciones del mismo capítulo,
\[
\frac{u_\gamma\ell_P^3}{E_P}
=\frac{\pi_{\rm HMT}^2}{15(\log3)^4},
\qquad
\frac{s_\gamma\ell_P^3}{k_B}
=\frac{4\pi_{\rm HMT}^2}{45(\log3)^3},
\]
y \(E_P=k_B\Theta_{\rm clk}\log3\), se deduce
\[
\boxed{
\frac{u_\gamma}{n_\gamma k_B\Theta_{\rm clk}}
=\frac{\pi_{\rm HMT}^2}{120\log A_2},
\qquad
\frac{s_\gamma}{n_\gamma k_B}
=\frac{\pi_{\rm HMT}^2}{90\log A_2}.}
\]
La razón adimensional de entropía por fotón, dividida por la razón adimensional de energía por fotón, es \(4/3\). Los productos con \(\ell_P^3\) desaparecen al formar estas razones; la derivación de \(\ell_P,E_P,k_B\) sigue en los sectores de acción y térmica ya asignados. Se reutilizan sus identidades, no se recalculan sus cifras ni se seleccionan parámetros desde observaciones.

**Sustitución admisible.** En estas ecuaciones escalares, sustituir
\(\mathcal Z_3(3)\) por \(4\pi_{\rm HMT}^2\log A_2\) conserva exactamente el resultado, su dominio y su normalización. La identidad escalar no convierte el operador de número de fotones en el operador de derivación zeta: proporciona una representación equivalente del coeficiente que interviene en su valor esperado.

Fuentes: [familia Bendersky, nivel dos](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c35_bendersky_glaisher.tex:35>) y [gas fotónico y escala térmica](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c40_termicas.tex:1>).

## 8. Relaciones incorporables al archivo común

| Origen recibido | Operación y salida | Información conservada / identificada | Sustitución y consecuencia |
|---|---|---|---|
| Lector residual periódico construido | Tabla → núcleo racional → Mellin y derivadas | Núcleo completo y período recuperan la tabla; un momento aislado generalmente no | Reemplazar el valor por su traza o integral en su dominio de convergencia |
| Lectores trítico y de cuarto de giro | Producto diagonal → carácter dodecafásico | Mantiene un mismo índice y ambos residuos | \(Q_{12}=Q_3Q_4\); momentos de Pell y término finito del producto |
| Dos valores espectrales | Producto tensorial → convolución de divisores | La pareja de índices se conserva antes de agrupar | Producto de momentos como traza de \((N\otimes N)^{-s}\), no como composición diagonal |
| Funcional meromorfo normalizado | Cambio de escala → transformación triangular de Laurent | Escala y torre completa permiten la inversión | Euler y Stieltjes deben transformarse junto con el polo |
| Derivadas en niveles negativos pares | Ecuación funcional → valores impares positivos | Índice, normalización y signo | Apéry equivale a \(4\pi_{\rm HMT}^2\log A_2\) |
| Producto con el carácter dodecafásico | Parte finita/residuo → Euler–Kronecker | La diferencia con Euler es invariante ante escala común | \(\gamma_{12}-\gamma_0=L_1'/L_1\) |
| Momento bosónico y escala térmica | Sustitución de Apéry → densidad y razones termodinámicas | Unidades, temperatura y espectro declarado | Densidad \(8\log A_2/(\log3)^3\); razones de energía y entropía por fotón |

El archivo común incorpora estas relaciones mediante sus fuentes y pruebas. Las familias indexadas no equivalen a una afirmación de independencia algebraica de todas sus constantes; una identidad de sustitución no constituye una nueva predicción empírica. La unidad generativa se conserva junto con las operaciones que permiten pasar de una representación a otra.


## 9. Momento orientado, dilatación de Pell y composición de retornos

### Antecedentes y operación efectiva

El capítulo 46 construye la ley \(V^{-1}\mathscr S V=\lambda i\mathscr S\), con \(\lambda=2+\sqrt3\); el capítulo de confluencia sitúa el momento de Catalán en el registro de profundidad de esa construcción. La procedencia de la relación entre profundidad, giro y constante es, por tanto, **ARQUITECTURA_AUTORAL_PREEXISTENTE**. El anexo [Catalán y cuarto de giro][cuarto-giro] ya reúne el lector orientado. Aquí se desarrolla su composición con la dilatación recibida de Pell y se prueba una evaluación exacta.

Después de la construcción APP–TRIT–TPK y de su realización espectral, el dominio es
\[
\mathcal H=\ell^2(\mathbb N_{>0}),\qquad
N\delta_n=n\delta_n,\qquad U_4\delta_n=i^n\delta_n.
\]
La fase \(i\), el índice de profundidad y su orientación son los antecedentes construidos, no parámetros elegidos por el valor de Catalán. Definimos
\[
Q_4=\frac{U_4-U_4^*}{2i},\qquad
C_4=\frac{U_4+U_4^*}{2}.
\]
Para \(0<r<1\), la aplicación \(r^N:\delta_n\mapsto r^n\delta_n\) pondera cada profundidad conservando su índice y su residuo módulo cuatro. Los momentos son
\[
F_s(r)=\operatorname{Tr}(N^{-s}r^NQ_4),\qquad
H_s(r)=\operatorname{Tr}(N^{-s}r^NC_4).
\]
Son trazas absolutamente convergentes para todo \(s\in\mathbb C\); la convergencia es uniforme en compactos de \(s\) y de \(0<r<1\). Esta familia es un lector posterior; especializar \(r\) no reconstruye ni modifica las semillas.

### Ecuación del momento y evaluación en la escala recibida

Para \(D=r\partial_r\), la suma geométrica y dos integraciones dan
\[
F_2(r)=\sum_{k\ge0}\frac{(-1)^kr^{2k+1}}{(2k+1)^2},
\quad DF_2(r)=\arctan r,\quad
\boxed{D^2F_2(r)=\frac{r}{1+r^2}},
\]
\[
F_2(r)=\int_0^r\frac{\arctan t}{t}\,dt
=\int_0^\infty\frac{t\,r e^{-t}}{1+r^2e^{-2t}}\,dt.
\]
Las condiciones \(F_2(0)=DF_2(0)=0\) fijan las constantes de integración. La dominación por \(\sum n^{-2}\) prueba \(F_2(r)\to G_{\rm Cat}\) cuando \(r\uparrow1\).

La escala contractiva del tornillo es
\[
\rho=\lambda^{-1}=2-\sqrt3.
\]
La igualdad \(\rho=\tan(\pi_{\rm HMT}/12)\) reconoce posteriormente ese valor. La evaluación exacta es
\[
\boxed{
F_2(\rho)=\frac23G_{\rm Cat}
-\frac{\pi_{\rm HMT}}{12}\log\lambda,\qquad
DF_2(\rho)=\frac{\pi_{\rm HMT}}{12},\qquad
D^2F_2(\rho)=\frac14.}
\]

**Demostración.** Con \(t=\tan x\), la integración por partes proporciona
\[
F_2(\tan\theta)=
\theta\log(\tan\theta)-\int_0^\theta\log(\tan x)\,dx.
\]
La expansión de Fourier de \(\log(\tan x)\), integrada mediante regularización de Abel en cero, da
\[
-\int_0^\theta\log(\tan x)\,dx
=\sum_{\substack{n\ge1\\n\ {\rm impar}}}\frac{\sin(2n\theta)}{n^2}.
\]
Para índices impares,
\[
2\sin(n\pi_{\rm HMT}/6)=
\chi_{-4}(n)+3\,\mathbf1_{3\mid n}\chi_{-4}(n/3).
\]
La suma con peso \(n^{-2}\) vale \(\tfrac12(1+3/9)G_{\rm Cat}=2G_{\rm Cat}/3\). Se toma \(\theta=\pi_{\rm HMT}/12\) y \(\log\rho=-\log\lambda\). La última derivada también se obtiene de \(\rho+\rho^{-1}=4\).

La evaluación enlaza el cuarto de giro, la escala de Pell y el momento de Catalán con coeficientes fijados por el carácter y la subdivisión angular. No se ha usado el decimal de ninguna de las constantes como selector.

### Orientación, composición y profundidad

El momento real conserva la otra componente:
\[
H_2(r)=\frac14\sum_{k\ge1}\frac{(-r^2)^k}{k^2},\qquad
DH_2(r)=-\frac12\log(1+r^2),\quad
D^2H_2(r)=-\frac{r^2}{1+r^2}.
\]
Por tanto,
\[
\operatorname{Tr}(N^{-2}r^NU_4)=H_2(r)+iF_2(r).
\]
La denominación posterior \(\operatorname{Li}_2(z)=\sum_{n\ge1}z^n/n^2\) identifica esta traza con \(\operatorname{Li}_2(ir)\); no la selecciona. En \(r=\rho\),
\[
\operatorname{Tr}(N^{-2}\rho^NU_4)
=\frac14\operatorname{Li}_2(-\rho^2)
+i\left(\frac23G_{\rm Cat}-\frac{\pi_{\rm HMT}}{12}\log\lambda\right).
\]
Sustituir \(U_4\) por \(U_4^*\) conserva \(H_2\) e invierte \(F_2\). Conjugar el número real \(F_2\) no cambia su signo: lo cambia invertir el lector orientado.

La composición retiene más información que una traza escalar. Para \(a\in\mathbb Z/4\mathbb Z\),
\[
B(r,a)=r^NU_4^a,\qquad
B(r,a)B(s,b)=B(rs,a+b).
\]
De aquí,
\[
B(r,1)^m=r^{mN}U_4^m,\qquad
\boxed{B(r,1)^4=r^{4N}\ne I\quad(0<r<1).}
\]
El cuarto retorno restituye la fase y conserva la contracción acumulada. El operador sigue siendo diagonal en la profundidad; la traza posterior agrega sus componentes y no permite recuperar por sí sola todas las historias TPK.

En la órbita escalar \(z_n=(\lambda i)^nz_0\), el recorrido inverso tiene razón \(-i\rho\). Su lector de potencias sobre profundidad es \(B(\rho,-1)\), no \(B(\rho,1)\). Por eso su momento imaginario tiene signo contrario. Esta identificación se refiere a los multiplicadores de la órbita documentada; no identifica \(V\), \(\mathscr S\) y \(U_4\) como operadores de un mismo espacio.

**Falsadores concretos.** Deben conservarse
\[
F_2(r)=r-r^3/9+O(r^5),\qquad
H_2(r)=-r^2/4+r^4/16+O(r^6).
\]
El cambio de orientación debe afectar sólo al momento imaginario. El retorno de cuatro factores debe dejar \(r^{4N}\), y el límite \(H_2(1)\) debe ser \(-\pi_{\rm HMT}^2/48\). El límite \(D^2F_2(r)\to1/2\) en \(r\uparrow1\) es un límite de Abel: \(Q_4\) no se convierte en operador traza–clase.

**Cruce acumulativo.** Aclarar ha demostrado que componer canales exige transportar la operación por el lector, no multiplicar sus valores finales. La identidad de \(B(r,a)\) exhibe ese principio sobre profundidad y orientación. Ley9 conserva el acarreo al reducir fases; aquí se conserva el índice \(n\) antes de tomar la traza. Son composiciones explícitas de realizaciones del origen común, con sus dominios respectivos. La prueba anterior no identifica entre sí el cuarto de giro, Fricke, la inversión de hoja y la holonomía nonádica completa.

## 10. Momentos primos y dos constantes de la misma estructura multiplicativa

### Procedencia y dominio

El producto nativo y sus irreducibles preceden al espacio de modos primos: esa procedencia ya se reúne en [el informe estructural previo][procedencia-primos]. El capítulo 18 contiene después el Hamiltoniano de una partícula
\[
H_{\mathbb P}|p\rangle=(\log p)|p\rangle
\]
y su levantamiento bosónico. La presente sección compone esos lectores existentes; no deduce la primalidad desde un laplaciano ni selecciona primos a partir de una lista de valores de una constante.

En \(\mathcal H_{\mathbb P}^{(1)}=\ell^2(\mathbb P)\), definimos para \(\Re s>1\)
\[
P(s)=\operatorname{Tr}(e^{-sH_{\mathbb P}})
=\sum_p p^{-s}.
\]
La factorización multiplicativa del propietario proporciona
\[
\mathcal Z_3(s)=\prod_p(1-p^{-s})^{-1},\qquad
\log\mathcal Z_3(s)=\sum_{k\ge1}\frac{P(ks)}k.
\]
El logaritmo designa la rama holomorfa fijada por el producto de Euler, con límite cero cuando \(\Re s\to+\infty\). La convergencia absoluta permite ordenar por primo o por multiplicidad \(k\). El índice \(p\) conserva el irreducible y \(k\) su ocupación multiplicativa; reemplazar ambos por un escalar pierde esa descomposición.

### Meissel–Mertens: sustracción del primer orden local

La fórmula del propietario
\[
B_1=\gamma+\sum_p\bigl(\log(1-p^{-1})+p^{-1}\bigr)
\]
da directamente
\[
\boxed{B_1=\gamma-\sum_{k\ge2}\frac{P(k)}k.}
\]
La sustracción cancela exactamente el orden \(p^{-1}\). La corrección restante es positiva y absolutamente sumable con signo negativo en \(B_1\); no es una serie oscilatoria de ceros de zeta.

Para \(K\in\mathbb N\), \(K\ge1\), la cola positiva satisface
\[
0<\sum_{k>K}\frac{P(k)}k
\le\frac{2P(K+1)}{K+1}
\le\frac{2^{-K}}{K+1}\left(1+\frac2K\right).
\]
**Prueba.** Para cada \(p\ge2\),
\(\sum_{k>K}p^{-k}/k\le p^{-(K+1)}/((K+1)(1-p^{-1}))\).
Se suma y se usa
\(\sum_{n\ge2}n^{-(K+1)}
\le2^{-(K+1)}+\int_2^\infty x^{-(K+1)}dx\).

En un corte por primos \(p\le Y\), con \(Y\ge2\) entero, sea \(B_1(Y)\) la fórmula anterior restringida. Entonces
\[
B_1(Y)-\frac1{2Y}\le B_1\le B_1(Y).
\]
En efecto,
\(-\log(1-p^{-1})-p^{-1}\le1/(2p(p-1))\),
y la suma sobre enteros \(n>Y\) telescopa a \(1/(2Y)\). Ambos tipos de corte conservan un error explícito: por nivel de ocupación o por irreducible.

### Constante de primos gemelos: dos exclusiones residuales

Para el patrón documentado \(H=\{0,2\}\), la ocupación prohibida módulo \(p\) es \(\nu_p(H)\). El factor de \(p=2\) en la serie singular completa es dos; para \(p>2\), el factor es
\[
\frac{1-2/p}{(1-1/p)^2}.
\]
El producto de estos últimos factores es \(C_2\), de modo que la serie singular del patrón es \(2C_2\). Al desarrollar el logaritmo,
\[
\log(1-2/p)-2\log(1-1/p)
=-\sum_{k\ge2}\frac{2^k-2}{k\,p^k}.
\]
Por convergencia absoluta,
\[
\boxed{
\log C_2
=-\sum_{k\ge2}\frac{2^k-2}{k}
\bigl(P(k)-2^{-k}\bigr).}
\]
El término \(2^{-k}\) elimina el modo \(p=2\) antes de aplicar los pesos; omitirlo destruye la fórmula. Los coeficientes \(2^k-2\) registran la diferencia entre dos exclusiones conjuntas y dos normalizaciones de una exclusión.

Para \(K\in\mathbb N\), \(K\ge1\), y \(S_K=\sum_{k=2}^K(2^k-2)(P(k)-2^{-k})/k\),
\[
0<-\log C_2-S_K
\le B_K,\qquad
B_K=\frac3{K+1}\left(\frac23\right)^{K+1}
\left(1+\frac3K\right).
\]
**Prueba.** Se acota \(2^k-2\le2^k\) y se amplía \(p>2\) a todos los enteros \(n\ge3\). Para cada \(n\),
\[
\sum_{k>K}\frac{(2/n)^k}{k}
\le \frac3{K+1}(2/n)^{K+1}.
\]
Finalmente,
\(\sum_{n\ge3}n^{-(K+1)}
\le3^{-(K+1)}(1+3/K)\).
Resultan los encierros
\[
e^{-S_K-B_K}\le C_2\le e^{-S_K}.
\]
Se conservan también los encierros por producto local del propietario:
\[
\frac{Y-1}{Y}C_2(Y)\le C_2\le C_2(Y).
\]

### Información común y diferencia de operación

Los dos valores dependen de la misma jerarquía \(P(k)\), con acciones distintas: \(B_1-\gamma\) cancela el primer orden de cada modo; \(\log C_2\) mide dos exclusiones residuales después de retirar el modo dos. Las constantes no son nombres yuxtapuestos: sus lectores y sus coeficientes quedan relacionados por la estructura multiplicativa ya construida.

La incidencia residual pertenece a esta lectura local. La forma global de Weil y el doble círculo tienen sus transportes y pruebas en los capítulos 96–97, leídos en el trabajo precedente; las identidades presentes no sustituyen esos transportes. Tampoco la convergencia del producto \(C_2\) demuestra por sí sola infinitud de pares gemelos. Son proposiciones distintas, como indica el propio propietario.

**Procedencia y falsadores.** Las definiciones \(B_1,C_2,H_{\mathbb P}\) son **RESULTADO_RECUPERADO**. La reunión de ambas constantes mediante \(P(k)\), sus dos clases de truncamiento y sus pruebas es una formalización añadida al anexo, sin reivindicación de novedad histórica. Refutan la composición: perder el modo excluido \(2^{-k}\), comenzar las series en \(k=1\), confundir \(C_2\) con \(2C_2\), o dar a las colas el signo contrario. No se ha ejecutado otra campaña decimal.

## 11. Invariantes de acción, carga y respuesta gravitatoria

### Composición de los antecedentes coordinados

MASAS conserva la sección de acción y sus lectores electrónicos; Aclarar conserva la identidad constitutiva del vacío; el propietario electrogravitatorio conserva su composición. Con \(E_{\rm el}:=e_{\rm el}^2>0\), distinto del número de Euler, las ecuaciones recibidas son
\[
ZE_{\rm el}=2\alpha_{\rm HMT}h,\qquad
G_\sigma\hbar_\sigma=\theta c^5t_0^2,\qquad
h_\sigma=2\pi_{\rm HMT}\hbar_\sigma.
\]
Los valores \(\pi_{\rm HMT},\alpha_{\rm HMT}\) proceden de la generación anterior; \(Z,c,t_0,\theta\) conservan la carta y los lectores de la fuente. Ninguna de estas ecuaciones los selecciona mediante un valor experimental.

El paso entre las secciones pre/ret conserva
\[
(G,h,E_{\rm el})_{\rm pre}
=(R_{\rm act}^{-1}G,R_{\rm act}h,
R_{\rm act}E_{\rm el})_{\rm ret}.
\]
Esta transformación no es el intercambio de canales \(q_+\leftrightarrow q_-\). Las dos operaciones se mantienen con sus dominios, aunque actúen en realizaciones relacionadas del mismo estado enriquecido.

### Clasificación exacta de los invariantes

Para estudiar algebraicamente el cambio de sección, extendemos su fórmula a
\[
T_R(G,h,E_{\rm el})=(R^{-1}G,Rh,RE_{\rm el}),\qquad R>0,
\]
sobre ternas positivas en una carta fija. La extensión es una acción matemática auxiliar; no se afirma que cada \(R>0\) sea generado por una historia TPK. La comparación física recibida corresponde a \(R=R_{\rm act}\).

Un monomio \(M=G^ah^bE_{\rm el}^d\) transforma con peso \(-a+b+d\):
\[
M\circ T_R=R^{-a+b+d}M.
\]
Por tanto,
\[
\boxed{
M\ \text{es invariante para todo }R>0
\ \Longleftrightarrow\ a=b+d
\ \Longleftrightarrow\
M=(Gh)^b(GE_{\rm el})^d.}
\]
Para exponentes enteros, \((1,1,0)\) y \((1,0,1)\) forman una base del núcleo entero del peso. Los monomios polinómicos invariantes corresponden a \(b,d\ge0\); la versión de Laurent permite exponentes negativos.

Además, la pareja
\[
\mathcal I(G,h,E_{\rm el})=(Gh,GE_{\rm el})
\]
separa exactamente las órbitas positivas de esta acción auxiliar. Si dos ternas tienen los mismos productos, tomar \(R=h'/h\) proporciona \(G'=G/R\) y \(E'_{\rm el}=RE_{\rm el}\). La otra dirección sigue de la invariancia. Así se clasifica qué información conserva el cociente por cambio de sección; no se reconstruye a partir de él toda la historia de acarreo.

### Restricción constitutiva y unidades

En la carta HMT con \(\alpha_{\rm HMT}\) y \(Z\) fijados, los dos invariantes ambientes satisfacen
\[
\boxed{GE_{\rm el}=\frac{2\alpha_{\rm HMT}}Z\,Gh.}
\]
No constituyen dos constantes libres independientes. Sustituyendo la identidad de acción,
\[
Gh=2\pi_{\rm HMT}\theta c^5t_0^2,\qquad
GE_{\rm el}=\frac{4\pi_{\rm HMT}\alpha_{\rm HMT}\theta c^5t_0^2}{Z},
\]
\[
\boxed{\frac{ZGe_{\rm el}^2}{c^5t_0^2}
=4\pi_{\rm HMT}\theta\alpha_{\rm HMT}.}
\]
Para la realización circular del propietario, \(\theta=\theta_{108}=(54/\pi_{\rm HMT})^2\). Se recupera su ecuación electrogravitatoria como restricción de la clasificación anterior.

La invariancia de sección no equivale a adimensionalidad. Con dimensiones fundamentales \(L,M,T,\mathsf Q\),
\[
[Gh]=L^5T^{-3},\qquad
[Ge_{\rm el}^2]=L^3\mathsf Q^2M^{-1}T^{-2}.
\]
El cociente \((Ge_{\rm el}^2)/(Gh)=2\alpha_{\rm HMT}/Z\) tiene dimensión de conductancia. La combinación normalizada del recuadro es adimensional. El transporte mantiene las unidades, además de los pesos.

**Procedencia y falsadores.** \(G_\sigma e_\sigma^2\), \(G_\sigma\hbar_\sigma\) y su normalización son **RESULTADO_RECUPERADO** del propietario; la clasificación de monomios y la separación de órbitas son la formalización reunida aquí. La prueba consiste en la acción sobre exponentes y el despeje positivo, no en coincidencias decimales. Refutan su aplicación: cambiar \(G\) con el mismo peso que \(h\), confundir carga con su cuadrado, perder \(2\pi_{\rm HMT}\) al pasar de \(h\) a \(\hbar\), o declarar independientes los dos invariantes después de imponer la relación constitutiva. Una sola comparación con \(R_{\rm act}=1\) no distingue pesos; la clasificación usa toda la acción auxiliar, o una comparación no trivial.

## 12. Resultado del cruce y localizadores

Los §§9–11 añaden tres composiciones demostradas al trabajo existente: momento de profundidad con giro y dilatación; ocupación de irreducibles con exclusión residual; y cambio de sección con invariantes constitutivos. Los antecedentes son los operadores y salidas del corpus, no los decimales reconocidos. Cada composición conserva el dato que necesita —profundidad y orientación, primo y multiplicidad, o sección y unidades— antes de formar su resultado escalar.

La referencia conceptual cruzada es precisa. Ley9 estudia fibras, fase y recuperación por acarreo; Aclarar estudia composición e inversión del lector de vacío; MASAS conserva las dependencias de acción y del lector electrónico. El presente aporte compone operaciones en esos puntos de contacto y distingue en cada caso el antecedente recuperado de la consecuencia demostrada aquí. Ninguna equivalencia global de dinámicas ni prioridad histórica nueva se deduce de estas identidades locales.

Los manuscritos, PDF y programas originales permanecen intactos. El desarrollo se añade a este anexo de trabajo; el recibo registra procedencia y alcance documental, no sustituye las pruebas anteriores.

[cuarto-giro]: </Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/CATALAN_MOMENTO_CUARTO_GIRO.md>
[procedencia-primos]: </Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/PROCEDENCIA_ESTRUCTURAL_MATEMATICAS_Y_COSMOLOGIA.md>
[Fuente Pell, ley y órbita](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/espirales/cap46_tornillo_espectral_pell.tex:9>).
[Fuente de confluencia, profundidad y Catalán](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_iv/body/B006_ch51_teorema_confluencia_hmt_md_13895c417b2c_28_teorema_confluencia_general.tex:344>).
[Fuente de productos locales y Hamiltoniano primo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/18_funcionales_espectrales_triadicos.tex:908>).
[Fuente de pareja de acción y covariancia](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/03_pareja_planck_respuesta.tex:182>).
[Fuente del producto electrogravitatorio](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/04_forma_electrogravitatoria.tex:227>).
[Composición del lector de vacío, Aclarar](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/INTERRELACIONES_ESTRUCTURALES_VACIO.md:149>).
[Dinámica y recuperación, Ley9](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/DINAMICA_ORIENTADA_Q_FRICKE_Y_RECUPERACION.md:37>).
[Dependencias del lector electrónico, MASAS](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/CRUCE_LECTOR_AREAL_ELECTRONICO.md:20>).
