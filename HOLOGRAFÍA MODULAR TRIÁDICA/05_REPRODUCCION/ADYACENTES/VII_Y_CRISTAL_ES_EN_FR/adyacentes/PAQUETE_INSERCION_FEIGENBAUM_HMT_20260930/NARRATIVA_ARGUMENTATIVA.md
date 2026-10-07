# Retorno, memoria y universalidad de la cascada dodecafásica

## La estructura generadora y la lectura crítica

La construcción de Feigenbaum en Holografía Modular Triádica enlaza una organización aritmética orientada con una ley asintótica de cambio de escala. Su punto de partida es la composición efectiva de APP, TRIT y TPK. APP evalúa suma y producto sobre las dos hojas de la retícula de dígitos y conserva los cocientes y residuos de esas operaciones. TRIT determina el régimen local y la orientación de su lectura. TPK selecciona y transporta los estados, actualiza sus registros y prolonga sus rutas con acarreo, frontera y memoria. La estructura discreta conjunta del continuo proporciona la residencia común de esos estados y de los lectores que actúan sobre ellos.

La prolongación
\[
w_6\longrightarrow w_{12}\longrightarrow w_{18}
\longrightarrow w_{24}\longrightarrow w_{30}
\longrightarrow R_{36}\longrightarrow G_9
\]
organiza esta persistencia. La semilla inicial se eleva conservando sus prefijos; las elevaciones sucesivas cambian el régimen sin perder orientación ni memoria; la frontera coinductiva permite continuar la construcción, y las nueve cartas reúnen sus lecturas locales. La holonomía nonádica expresa el retorno de fase acompañado de un incremento de memoria. Así, una vuelta visible conserva la posición que ocupa dentro de la historia completa. La operación de retorno adquiere desde el origen dos componentes inseparables: reiteración de una regla y conservación de su procedencia.

El lector crítico fijado sobre la rueda dodecafásica orientada convierte esta estructura en doce fases con una traza uniforme. Sus representantes son
\[
\phi_m=\frac{(3m-1)\pi_{\mathrm{HMT}}}{18},
\qquad w_m=\frac1{12},\qquad 1\le m\le12.
\]
La elección del representante orientado importa porque el segundo momento utiliza su magnitud. El cociente angular registra la fase, mientras el representante conserva la información necesaria para normalizarla. La coordenada \(\pi_{\mathrm{HMT}}\) procede de los lectores coinductivos del mismo núcleo APP–TRIT–TPK. Dentro de su imagen correlacionada, las coordenadas \(\pi,\varphi,e\) y el cierre dodecafásico de \(\alpha_{\mathrm{HMT}}\) conservan su orden constructivo y sus dominios propios. En el lector crítico aquí considerado se utiliza la coordenada angular ya generada.

La normalización se determina mediante una suma entera:
\[
\sum_{m=1}^{12}(3m-1)^2=5394=6\cdot899,
\qquad k_m=\frac{2(3m-1)}{\sqrt{899}}.
\]
El factor común \(\pi_{\mathrm{HMT}}\) se cancela al fijar el segundo momento. Esta cancelación conserva la procedencia de las fases y produce una representación particularmente precisa de su lectura normalizada. Se obtiene
\[
u_0(x)=\frac1{12}\sum_{m=1}^{12}\bigl(1-\cos(k_mx)\bigr),
\qquad f_\lambda(x)=1-\lambda u_0(x),
\qquad \sum_mw_mk_m^2=2.
\]
El perfil es par y entero; satisface \(u_0(0)=u_0'(0)=0\) y \(u_0''(0)=2\). Para \(0<\lambda\le2/u_0(1)\), la familia lleva \([-1,1]\) en sí mismo y tiene un máximo crítico cuadrático con \(f_\lambda''(0)=-2\lambda\). El parámetro \(\lambda\) recorre esta familia después de fijados el lector, la orientación, los pesos y la escala. La cifra universal que se reconocerá al final queda así separada de la selección de los coeficientes.

## Doce fases, momentos y representación espectral

El perfil admite una segunda expresión que reúne sus fases en un operador finito. Los nodos
\[
s_m=k_m^2=\frac{4(3m-1)^2}{899}
\]
determinan la medida positiva \(\mu_0=12^{-1}\sum_m\delta_{s_m}\). Sus momentos \(M_r=\int s^r\,d\mu_0(s)\) definen formas de Hankel estrictamente positivas hasta el rango doce. Esta positividad procede de la evaluación de un polinomio sobre doce nodos distintos: un polinomio de grado menor que doce conserva al menos una evaluación no nula. En grado doce, el producto de los doce factores nodales anula la norma y determina exactamente el rango del lector.

La ortogonalización de estos momentos produce una matriz de Jacobi \(J_{12}\), real simétrica, con subdiagonales positivas. Su cálculo funcional recupera el perfil completo:
\[
u_0(x)=e_0^{\mathsf T}
\bigl[I-\cos(x\sqrt{J_{12}})\bigr]e_0.
\]
La suma de cosenos y el operador de Jacobi son dos realizaciones del mismo lector. Los momentos mantienen todas las frecuencias y sus pesos; las marcas de orientación, ruta y memoria permanecen en el estado que las genera. El rango doce identifica la dimensión espectral de esta lectura concreta. La profundidad de sus prolongaciones pertenece a otra dimensión de la construcción: la longitud de las historias compatibles y la resolución con que se evalúan.

La geometría analítica también se hace explícita. Para la deformación ponderada \(u_\eta\), en la franja \(|\eta|\le1/40\), los pesos siguen siendo positivos y el segundo momento permanece normalizado. En \(|\operatorname{Re}z|<\pi/3\) existe una función holomorfa impar y univalente \(b_\eta\), normalizada por \(b_\eta'(0)=1\), tal que \(u_\eta=b_\eta^2\). La rueda produce, por tanto, una deformación conforme del pliegue cuadrático. Su conjugación dinámica conserva esa deformación a través de \(b_\eta(1-\lambda w^2)\). El teorema de escalado paramétrico que se desarrolla aquí corresponde al miembro uniforme \(\eta=0\); las propiedades estructurales de la franja ponderada y la persistencia local de sus raíces conservan sus cuantificadores específicos.

## Profundidad de lectura y restitución de las historias

La profundidad nonádica refina la lectura de un parámetro, mientras la duplicación dinámica cambia el horizonte de retorno. El refinamiento con acarreo expresa la primera operación mediante
\[
L_c(x,y)=(Bx-c,By+c),\qquad
C_m=\sum_{j=1}^m c_jB^{m-j},
\]
\[
(x_m,y_m)=(B^mx_0-C_m,B^my_0+C_m).
\]
El soporte exterior crece como \(B^m\), y el cilindro normalizado del registro tiene diámetro \(B^{-m}\). La pareja entera, la profundidad y la marca de frontera conservan la reconstrucción de cocientes, residuos y prefijos. Crecimiento exterior y resolución interior describen así operaciones compatibles sobre una misma historia.

La composición exacta \(L_D^{[b]}L_C^{[a]}=L_{B^bC+D}^{[a+b]}\) permite agrupar una historia en bloques sin alterar sus datos. Un retorno de duplicación reúne dos transiciones; el calendario nonádico reúne nueve. Ambos agrupamientos se comparan sobre un horizonte común de \(9\,2^N\) eventos, conservando el orden de los subbloques y sus acarreos.

La contribución de la memoria puede observarse directamente en las ramas inversas del perfil. Si \(v=(u_0|_{[0,1]})^{-1}\), las dos ramas son
\[
\beta_\sigma(y)=\sigma v\!\left(\frac{1-y}{\lambda}\right),
\qquad \sigma\in\{-1,+1\}.
\]
El valor final, junto con la última hoja, reconstruye el valor anterior. Una sucesión de hojas permite recuperar todos los pasos intermedios. La palabra de ramas acompaña los registros APP–TRIT–TPK de ruta, frontera, acarreo y memoria; cada registro conserva su función. Esta restitución concreta explica qué información requiere la inversión de la lectura crítica.

La resolución de cada retorno dispone además de una cota explícita. Con \(t=\lambda u_\eta(1)/2\), \(z=(x+1)/2\) y
\[
F_{t,\eta}(z)=1-t\frac{u_\eta(2z-1)}{u_\eta(1)},
\]
se obtiene
\[
\left|F_{t,\eta}^{q}(1/2)-F_{s,\eta}^{q}(1/2)\right|
\le S_q|t-s|,\qquad S_q=\sum_{j=0}^{q-1}(6\sqrt2)^j<9^q.
\]
Un cilindro de base nueve y profundidad \(m=2^N+r\) permite, por ello, leer el retorno de horizonte \(2^N\) con diámetro inferior a \(9^{-r}\). Esta estimación da contenido cuantitativo a la profundidad arbitraria: para cada horizonte y precisión solicitados determina una profundidad suficiente. La evaluación de las funciones analíticas y el redondeo poseen sus propios restos, que se propagan junto con la incertidumbre del parámetro.

Las vacancias intervienen en el balance de capacidad del registro. La comparación entre bloques de 729 y 1000 posibilidades distingue capacidad acumulada y longitud cronológica, conservando los pasos en que la primera permanece constante. Esta contabilidad determina el espacio requerido para conservar una lectura y su profundidad. La admisibilidad de las historias procede, a su vez, de las reglas de supervivencia. Ambas operaciones colaboran en la construcción y mantienen objetos matemáticos distintos.

## Cronología nonádica y combinatoria de duplicación

La palabra crítica de duplicación tiene una expresión a toda profundidad:
\[
\tau_j=(-1)^{v_2(j)},\qquad
\tau_{2j}=-\tau_j,\qquad \tau_{2j+1}=+1.
\]
Sus prefijos satisfacen \(W_{n+1}=W_n(-1)^nW_n\). La regla determina cómo se orientan las dos copias del retorno y dónde aparece su separación. La lectura nonádica de la cronología conserva el entero completo \(K=\rho_9(K)+9q_9(K)\). Al reducirlo módulo \(2^n\), la holonomía que avanza nueve eventos induce la traslación por nueve sobre ese ciclo. Puesto que nueve es impar, esta traslación visita todas sus posiciones. La permutación \(j\mapsto9j\pmod{2^n}\), que la conjuga con el avance unitario, preserva la valoración diádica de cada posición no nula. El residuo y el cociente cronológicos sostienen conjuntamente esa compatibilidad.

La memoria bilateral posee asimismo una realización operatoria compatible con el refinamiento. Sobre los ciclos de longitud \(2^n\), el operador de avance \(C_n\) se incorpora en
\[
\mathbb U_n=P_0\otimes I+P_1\otimes C_n,
\]
con los proyectores complementarios del lector nonádico. En el límite, sus componentes visible y complementaria satisfacen
\[
\|T_{\infty,a}v\|^2+\|D_{\infty,a}v\|^2=\|v\|^2,
\qquad
v=T_{\infty,a}^*T_{\infty,a}v+D_{\infty,a}^*D_{\infty,a}v.
\]
Estas identidades describen conservación y restitución dentro del espacio y la representación declarados. La contracción de los mapas renormalizados, que aparecerá después, mide otra operación: la aproximación de sus perfiles a una forma estable. La historia conservada por el levantamiento y la convergencia de una lectura funcional se articulan en niveles diferentes.

## La carta ordenada y la selección global de las raíces

La publicación arquimediana del continuo HMT transporta las operaciones mediante un isomorfismo de cuerpos ordenados completos, dentro del universo declarado \(\mathfrak G\):
\[
\iota:\mathbb R_{\mathrm{HMT}}^{\mathfrak G}
\longrightarrow\mathbb R^{\mathfrak G}.
\]
La construcción interna del coseno por su serie, la raíz positiva de 899, el perfil y sus iterados precede a la selección de ceros. La conservación de suma, producto, orden y límites convergentes da
\[
\iota\bigl(S_n^{\mathrm H}(a)\bigr)=S_n\bigl(\iota(a)\bigr),
\qquad S_n(\lambda)=f_\lambda^{2^n}(0).
\]
La sobreyectividad cubre todas las raíces del dominio de esa carta; el orden conserva los retornos anteriores, el período exacto y la condición de encontrarse a la derecha de la raíz precedente. De este modo se transporta también el mínimo de cada conjunto de candidatos. La genealogía llega hasta la selección efectiva del parámetro, con la segunda proyección y sus marcas conservadas sobre el mismo antecedente.

El selector queda fijado por \(\lambda_1=1/u_0(1)\) y por la primera raíz nueva de período crítico exacto \(2^n\) situada a la derecha de \(\lambda_{n-1}\). La clasificación de itinerarios demuestra que cada raíz seleccionada tiene palabra \(W_n0\). Los retornos restrictivos reducen su período a la mitad conservando el orden unimodal, y la inducción restituye la palabra completa. La analiticidad de los retornos no idénticamente nulos aísla sus ceros en cada compacto; la comparación de los signos antes del primer parámetro de itinerario infinito garantiza la existencia de una raíz nueva en todos los niveles.

Sea \(\Lambda_\tau\) el conjunto compacto no vacío de parámetros que realizan la palabra infinita, y sea \(a_*\) su mínimo. Se demuestra
\[
\lambda_n\nearrow a_*.
\]
El paso al límite conserva cada signo mediante una cota uniforme a horizonte fijo. Si \(c_p=f_\lambda^p(0)\), los signos opuestos de \(c_p\) y \(c_{2p}\), junto con \((f_\lambda^p)'(0)=0\), implican
\[
|c_p|>\frac2{B_p},\qquad
B_p=16^p\frac{16^p-1}{15}.
\]
Así, los prefijos de períodos crecientes preservan la palabra infinita al acumularse. La prueba utiliza la sucesión original de primeras raíces desde su definición global.

## La hoja estable y la identificación del límite seleccionado

El retorno normalizado
\[
(Rf)(x)=-\frac{f(f(-ax))}{a},\qquad a=-f(1)>0,
\]
reúne dos transiciones, cambia la escala y conserva la orientación necesaria para restituir un máximo de valor uno. Los dominios restrictivos acreditan su interpretación como retorno real. La derivada de este operador incluye la variación de la escala \(a\); esa contribución determina la sensibilidad paramétrica de la transformación completa.

En la carta \(f(x)=1-x^2V((x^2-1)/(5/2))\), con coordenadas \(u=10v_0\) y \(\nu=(v_1,v_2,\ldots)\), el cuarto retorno de la familia entra en un entorno cuantificado del punto fijo \(g\). La curva cruza transversalmente su hoja estable en un único parámetro local
\[
1.874038<\lambda_*<1.874039,
\]
y satisface
\[
\|R^{4+n}f_{\lambda_*}-g\|_{\mathcal A}
<0.001666(0.83996)^n.
\]
La hoja estable es una gráfica de pendiente a lo sumo \(0.16\). Las secantes paramétricas pertenecen a un cono transversal expansivo. Ambas propiedades distinguen la disminución de las deformaciones estables y el crecimiento de la separación entre parámetros.

La identificación de \(a_*\) y \(\lambda_*\) reúne esta geometría local con el mínimo global. Primero se excluye el intervalo entre la octava raíz y el extremo inferior de la caja local. Después, el orden \(a_*\le\lambda_*\) permite estudiar una hipotética separación mediante el cono negativo. Mientras su coordenada transversal tiene módulo inferior a \(0.006\), la secante permanece en el dominio analítico y crece por un factor comprendido entre \(4.4034\) y \(8.0887\). Una separación persistente produciría, por tanto, una primera salida de amplitud comprendida entre \(0.006\) y \(0.0485322\).

El residuo de la órbita estable conserva información más precisa que su norma: sus componentes satisfacen \(|e_u|\le0.16\|e_\nu\|_1\). Esta relación permite acotar conjuntamente sus efectos sobre la órbita crítica. La cobertura de toda la región de primera salida muestra en cada caso un signo incompatible con \(\tau\), o un retorno contractivo que obliga a dos valores críticos diádicos sucesivos a tener el mismo signo. La palabra infinita exige signos opuestos. La contradicción identifica los parámetros:
\[
\lambda_n\nearrow a_*=\lambda_*.
\]
La demostración combina una inducción válida a toda profundidad con una exclusión finita uniforme de la región a la que llegaría cualquier separación. El alcance infinito descansa en esa composición.

## Escalado universal y significado de la precisión

La realización holomorfa de grado dos de los retornos y la transversalidad acreditada permiten comparar sus clases híbridas. Para cada período suficientemente alto, la clase canónica posee una única intersección local con la familia. Las primeras raíces globales ya convergen al cruce y conservan la combinatoria de duplicación; por ello coinciden finalmente con los centros locales al igualar sus períodos físicos. La prueba transporta la selección original hasta la ley métrica universal.

Existen \(C>0\), \(M<\infty\) y \(0<\theta<1\) tales que
\[
\lambda_*-\lambda_n=C\delta_{\mathrm F}^{-n}(1+e_n),
\qquad |e_n|\le M\theta^n,
\]
y, en consecuencia,
\[
\lim_{n\to\infty}
\frac{\lambda_{n-1}-\lambda_{n-2}}
{\lambda_n-\lambda_{n-1}}=\delta_{\mathrm F}.
\]
El factor \(\delta_{\mathrm F}\) es el autovalor expansivo del operador de duplicación reconocido al final de la construcción. La familia concreta conserva sus doce fases, sus momentos y su historia de procedencia; el límite de sus razones paramétricas pertenece a la misma clase universal de criticidad cuadrática. Esta relación explica conjuntamente la especificidad del generador y la universalidad de la salida.

La precisión posee aquí tres residencias. Los intervalos de las raíces controlan su evaluación finita. La estimación \(0.001666(0.83996)^n\) controla la convergencia operatorial sobre la hoja estable. El término \(M\theta^n\) controla el traslado de esa geometría a la escala paramétrica mediante la holonomía transversal. Cada estimación responde a su variable y a su operación. El octavo cociente queda encerrado alrededor de \(4.669212189150204154556096215889663928\), con anchura inferior a \(5.808\cdot10^{-37}\); esa anchura mide la evaluación de \(\delta_{\mathrm F,8}\). La distancia de \(\delta_{\mathrm F,8}\) al límite requiere cuantificar las constantes del resto paramétrico, cuya existencia ya queda demostrada.

La notación mantiene separados \(\delta_{\mathrm F}\), factor de escalado paramétrico de Feigenbaum; \(\alpha_{\mathrm F}\), constante espacial asociada a su problema de renormalización; y \(\alpha_{\mathrm{HMT}}\), constante de estructura fina del corpus. El resultado presente identifica \(\delta_{\mathrm F}\) mediante las primeras raíces del sector uniforme \(\eta=0\). La franja ponderada conserva sus teoremas estructurales y de existencia, y su extensión métrica cuantificada constituye un enunciado específico distinto.

La aportación del encadenamiento reside en la continuidad entre generación, lectura, memoria, selección y límite. La aritmética orientada determina el perfil; la representación espectral conserva sus doce componentes; los cilindros permiten resolverlo con precisión arbitraria a cada horizonte; el transporte de historias restituye sus recorridos; la carta ordenada conserva todas las raíces y sus mínimos; la clasificación prolonga el selector; y la expansión transversal, junto con la contracción estable, determina su ley asintótica. La universalidad aparece como una propiedad demostrada de esta construcción completa y de su realización analítica.
