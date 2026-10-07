# Centro, frontera y vacancias: conservación de la información en la conexión nonádica

Esta incorporación desarrolla los apuntes de Rubén sobre el centro de APP, la corona 3–6–9, el espejo nonádico y las vacancias. Se añade al expediente del doble círculo sin sustituir sus pruebas anteriores. Su objeto es hacer explícitas las operaciones que conectan posición, lectura aritmética, orientación y memoria. Los PDF y paquetes entregados permanecen intactos.

## 1. La tesis y el orden de construcción

La relación entre centro y frontera adquiere contenido matemático cuando se precisa qué datos se publican, qué transformaciones los transportan y con qué información se reconstruyen. En APP, un residuo se acompaña de su cociente; en TRIT, la orientación distingue operaciones que un agregado puede reunir; en TPK, una vuelta devuelve la fase y prolonga la memoria. El estado enriquecido reúne esas coordenadas. Su residencia en la estructura discreta conjunta del continuo conserva las dependencias entre las distintas lecturas posteriores.

El recorrido es APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. La presente nota efectúa cortes locales de ese recorrido: no reconstruye los cinco aspectos consustanciales del continuo desde una forma espectral ni los transforma en cinco módulos independientes. Las constantes internas se reciben en su etapa de publicación, sin utilizar sus valores convencionales para elegir semillas, rutas o coeficientes.

La intuición autoral puede expresarse así: **la publicación de un valor es una proyección de una construcción; para transportar esa construcción se conserva la información que permite distinguir sus realizaciones**. Las operaciones siguientes concretan esa afirmación. El lenguaje posterior de interpolación y de descomposición ortogonal demuestra propiedades de objetos ya especificados; no selecciona retrospectivamente el estado APP.

## 2. La corona local y la reconstrucción del centro

En la carta positiva se utiliza

\[
\rho_9(n)=1+[(n-1)]_9,\qquad
q_9(n)=\frac{n-\rho_9(n)}9,
\qquad n=\rho_9(n)+9q_9(n).
\]

La tabla producto es \(P(i,j)=ij\), con \(1\leq i,j\leq9\). La restricción a \(Q=\{3,4,5,6\}^2\) publica

\[
\left(\rho_9(ij)\right)_{i,j=3}^{6}=
\begin{pmatrix}
9&3&6&9\\
3&7&2&6\\
6&2&7&3\\
9&6&3&9
\end{pmatrix}.
\]

Su bloque interior es

\[
B_c=\begin{pmatrix}7&2\\2&7\end{pmatrix}.
\]

El perímetro de esta carta contiene doce posiciones: cuatro con valor \(3\), cuatro con \(6\) y cuatro con \(9\); su suma es \(72\). Se hace visible una corona radical alrededor del bloque central. El centro electrónico global es \((5,5)\), único punto fijo de la inversión de la APP completa; no se cambia su posición al elegir esta carta local, cuyo centro geométrico está en \((4.5,4.5)\).

### Proposición: recuperación desde la frontera levantada

Sea \(F(x,y)=a+bx+cy+dxy\) una ley multiafín en la carta \([3,6]^2\). Para
\(t=(x-3)/3\) y \(u=(y-3)/3\),

\[
\begin{aligned}
F(x,y)={}&(1-t)(1-u)F(3,3)+(1-t)uF(3,6)\\
&+t(1-u)F(6,3)+tuF(6,6).
\end{aligned}
\]

**Demostración.** Para \(y\) fijo, la afinidad en \(x\) recupera \(F(x,y)\) desde \(F(3,y)\) y \(F(6,y)\). La afinidad en \(y\) recupera cada uno de esos dos valores desde sus extremos. La composición da la fórmula. En particular, las cuatro esquinas determinan toda la carta dentro del espacio de leyes declarado.

Para el producto, los cuatro valores levantados son \(9,18,18,36\). Sus residuos positivos son todos \(9\), pero sus cocientes son \(0,1,1,3\). La fórmula recupera \(16,20,20,25\) en las posiciones interiores; su publicación residual da \(7,2,2,7\). De este modo, la frontera determina el interior **conservando la ley y el levantamiento**. La interpolación se hace antes de la reducción modular: no se divide por \(3\) en \(\mathbb Z/9\mathbb Z\), donde \(3\) no es invertible.

Esto precisa el sentido de «conservar la información del centro». La corona residual por sí sola no individualiza todos los levantamientos: \(F\) y \(F+9\) tienen los mismos residuos en toda la frontera y distintos valores levantados. La pareja residuo–cociente elimina esa ambigüedad dentro de la reconstrucción indicada. La afirmación queda probada para las leyes multiafines; extenderla a estados completos requiere conservar también los operadores, las rutas y la memoria que actúan sobre ellos.

La recuperación multiafín es una **formalización nueva de la arquitectura autoral preexistente**. Las cartas y sus lecturas son resultados recuperados del corpus; esta presentación explícita de su inversa no se atribuye como un descubrimiento histórico independiente.

## 3. Suma, producto y los tres valores de la curvatura discreta

Las filas multiplicativas se construyen por acumulación aditiva. La diferencia entre ambas hojas aparece al variar simultáneamente las dos coordenadas. Con diferencias unitarias,

\[
\Delta_x\Delta_y(x+y)=0,
\qquad
\Delta_x\Delta_y(xy)=1.
\]

La misma propiedad se recupera en la frontera levantada:

\[
\frac{P(6,6)-P(6,3)-P(3,6)+P(3,3)}{3\cdot3}=1;
\]

para \(S(x,y)=x+y\), ese cociente vale \(0\). El producto registra la variación cruzada que la suma no introduce. El corpus expresa la versión orientada mediante

\[
\mathcal F(T_x,T_y)=\Delta_x\Delta_yT_y-\Delta_y\Delta_xT_x,
\]

\[
\mathcal F(S,S)=\mathcal F(P,P)=0,
\qquad \mathcal F(S,P)=+1,
\qquad \mathcal F(P,S)=-1.
\]

El orden de las hojas distingue el signo. La formulación «la suma acumula y el producto pliega o despliega» se apoya aquí en una operación verificable: al proyectar modularmente se conserva un residuo; al levantar se recupera el cociente que registra lo sobrepasado. La curvatura discreta registra además el orden de las variaciones. No se identifica esta diferencia finita con una curvatura diferencial de un espacio físico sin su mapa de realización correspondiente.

### La cruz radical global

En \(R=\mathbb Z/9\mathbb Z\), el ideal \(\mathfrak m=\{0,3,6\}\) satisface \(\mathfrak m^2=0\). Su publicación positiva es \(\{9,3,6\}\). La cruz

\[
(\mathfrak m\times R)\cup(R\times\mathfrak m)
\]

tiene \(27+27-9=45\) posiciones. La intersección contiene nueve valores \(9\), de suma \(81\); los brazos restantes tienen doce valores de cada clase \(3,6,9\), de suma \(216\). El total es

\[
297=216+81=3(72+27)=3\cdot99.
\]

Se distinguen cuatro fronteras: el perímetro local de doce posiciones, la cruz radical de cuarenta y cinco, el gnomon de diecisiete que completa \(8^2\) a \(9^2\), y la corona cúbica de \(271\). Cada una tiene dominio y operación propios. El cociente trítico \(R/\mathfrak m\) conserva una clase; transportar el estado requiere acompañarla de los datos levantados y de su historia.

## 4. Los lectores 72–27, 77–22 y la completación 729–271

Las filas ordenadas de \(B_c\) se publican decimalmente como \(72\) y \(27\); sus diagonales como \(77\) y \(22\). Resulta

\[
72+27=77+22=99.
\]

En la completación cúbica, el conteo de interior, caras, aristas y vértice da

\[
1000=729+243+27+1=729+271,
\]

\[
999=729+243+27=729+270.
\]

La coincidencia de lectores se expresa conservando el resto decimal:

\[
729=10\cdot72+9,\qquad271=10\cdot27+1.
\]

Por tanto, la lectura bidimensional publica \((72,27)\); la lectura cúbica publica \(((72,9),(27,1))\). La pareja de restos \((9,1)\) distingue las prolongaciones que compartirían un mismo cociente. Primero se efectúan las construcciones de las cartas; después se comparan esas publicaciones. La identidad de los enteros no invierte ese orden causal.

El capítulo de canales enteros proporciona otra composición específica. Con los recuentos internos \(\Delta=54\), \(\nu=\Delta/2=27\) y \(\Theta=5\nu=135\), obtiene

\[
\mathcal C_\alpha=\nu^2=729,
\qquad \mathcal C_e=2\Theta+1=271.
\]

Aquí se ha renombrado como \(\nu\) el entero local que ese propietario escribe \(\kappa\), para distinguirlo de la lectura racional del registro dodecafásico. Los canales son objetos enteros; su identificación con las constantes pasa por los lectores regionales y el cierre correspondiente, no por los primeros dígitos de una expansión. No se introduce el ángulo \(A\) en esta incorporación.

Para la referencia oral a una fracción de \(\pi\), el propietario localizado contiene

\[
\frac{396}{126}=\frac{22}{7},\qquad
396=18+72+108+198,\quad126=18+108.
\]

Es una razón racional de anillos alternos. Se conserva esa fórmula localizada; no se sustituye por una lectura conjeturada de «77 dividido por dos», ni se escribe que la razón sea exactamente \(\pi\).

## 5. El centro electrónico y sus vacancias conjugadas

La inversión de la APP positiva es \(\rho(r,c)=(10-r,10-c)\). Su único punto fijo es \((5,5)\). En la fibra aditiva central,

\[
\mathcal F_{10}=\{(5+t,5-t):t\in\mathbb Z,\ |t|\leq4\},
\]

el producto vale \(25-t^2\). Conservar su residuo central exige \(t^2\equiv0\pmod9\), equivalente a \(3\mid t\). Los únicos lugares son, por tanto,

\[
(5,5),\qquad(8,2),\qquad(2,8).
\]

Si \(\mathcal A\) conserva la pareja residuo–cociente en cada hoja,

\[
\begin{aligned}
\mathcal A(5,5)&=((1,1),(7,2)),\\
\mathcal A(8,2)=\mathcal A(2,8)&=((1,1),(7,1)).
\end{aligned}
\]

Las dos vacancias preservan la lectura aditiva y el residuo multiplicativo; el cociente producto disminuye exactamente una unidad. El espejo \(t\mapsto-t\) intercambia sus posiciones. El valor residual no distingue sus rutas, mientras la orientación sí las conserva. Esta es una realización precisa de la conexión que señalaba el apunte: **la vacancia se individualiza por una relación con el centro y por un defecto registrado, no por ser una casilla sin información**.

La orientación electrónica inicial \((h_0,v_0)=(1,1)\), invertida cada \(27\) pasos, publica después la firma dodecafásica \((+++\,---\,+++\,---)\). Se trata de un registro de orientación, distinto tanto de la posición \((5,5)\) como de la firma producto siguiente.

### La firma 555555 y la memoria que permite prolongarla

Para \(U_j=100d_{1j}+10d_{2j}+d_{3j}\), el lector

\[
\mathcal E_\times(U)=([d_{2j}-d_{1j}]_{10})_{j=1}^{6}
\]

aplicado a la región transversal

\[
U_\pi^\perp=(501,614,498,169,272,272)
\]

produce \(555555\); su reducción \(\Psi(U)=(-U_j\bmod3)_j\) produce \(010211\). La firma tiene veinticuatro representantes producto. El transporte los separa en tres hojas de ocho: tras el avance aparecen \(555177\), \(555717\) y \(555771\). La congruencia estable por avance y media vuelta refina las veintiséis firmas en veintiocho clases, con histograma \(27\cdot8+108=324\). Así queda expresado por qué hay que retener memoria de hoja para continuar una firma que inicialmente coincide.

El enlace con la ecuación electrónica pasa por las regiones. La región transversal tiene multiplicidad \(432=18\cdot24\); cada una de las otras cuatro tiene \(144=18\cdot8\). Sus cinco identidades se insertan, en el calibre declarado del artículo I, en

\[
\mathcal K_e=\mathbb Z/9\mathbb Z\times\mathbb F_3
\]

mediante \((4,0),(5,0),(6,0),(6,1),(6,2)\). Una vez fijada esa inserción, su complemento tiene \(27-5=22\) lugares y sus tres hojas por región tienen \(5\cdot3=15\) lugares. El déficit orientado y la memoria torsional son \(-22\) y \(15\). La prueba de esos recuentos y su inserción está conservada en el artículo I; esta nota la reúne, no elige sus lugares a partir de una masa objetivo.

Hay, por tanto, dos recorridos vinculados en la composición: **centro → vacancias conjugadas → orientación**, y **firma regional → hojas de transporte → incidencia de las cinco regiones → coeficientes electrónicos**. Identificar sin más \((5,5)\) con \(555555\) borraría precisamente las operaciones que explican su relación.

## 6. Espejo nonádico, capacidad y retorno con memoria

En la fibra regional, el espejo actúa por

\[
\mathfrak c(u^\pi,u^e,u^\varphi)=(u^e,u^\pi,u^\varphi).
\]

Conserva \(s=u^\pi+u^e\) e invierte \(d=u^\pi-u^e\). En \(\mathbb F_3\),

\[
u^\pi=2(s+d),\qquad u^e=2(s-d).
\]

La suma conserva el agregado; la diferencia orientada conserva el reparto. El eje \(u^\varphi\) queda fijo bajo esa involución, aunque puede evolucionar bajo el transporte. El espejo regional y el espejo celular de las vacancias tienen dominios distintos: sus respectivas fórmulas permiten seguir qué preserva cada uno.

La vacancia de capacidad añade un enlace temporal explícito. En la normalización del refinamiento \(729\) frente a \(1000\), sean \(\rho_c=\log_{10}9\), \(\delta=1-\rho_c\) y \(\mathcal C_t=\lfloor(t+1)\rho_c\rfloor\). Si

\[
z_t=\lfloor(t+1)\delta\rfloor-\lfloor t\delta\rfloor,
\]

entonces, para \(t\geq1\),

\[
\mathcal C_t-\mathcal C_{t-1}=1-z_t,
\qquad
\mathcal C_b-\mathcal C_a+\sum_{t=a+1}^b z_t=b-a.
\]

**Prueba.** La irracionalidad de \(\log_{10}9\) se sigue de la imposibilidad de \(9^n=10^m\) para enteros positivos. Por ello, \(\mathcal C_t=t-\lfloor(t+1)\delta\rfloor\). Restar y sumar telescópicamente da ambas identidades. Una vacancia retiene capacidad mientras avanza la historia.

Si \(p_j=\lfloor j/\delta\rfloor\), \(v_j=p_j-j\) y \(h_j=p_{j+1}-p_j\), el desarrollo heredado establece \(h_j\in\{21,22\}\). Para \(s_j=22-h_j\),

\[
[v_{j+1}]_3=[v_j-s_j]_3,\qquad
\tau_j=M_{\rm ph}(1+[v_j]_9).
\]

Las vacancias actúan así sobre la fase retenida que lee el selector trítico. Esta sucesión de capacidad no se convierte automáticamente en la trayectoria celular del electrón: el manuscrito conserva sus mecanismos respectivos y su composición dentro del mismo núcleo.

## 7. El factor 8/81 como balance de publicación y complemento

En el desarrollo del doble círculo, la inclusión uniforme de nueve fases es \(Jv=(v,\ldots,v)/3\). Con la costura

\[
S_C(v_0,\ldots,v_8)=(Cv_8,v_0,\ldots,v_7),
\]

se obtiene \(T=J^*S_CJ=(8I+C)/9\). Si \(z=(C-I)v\), el complemento de la publicación es exactamente

\[
\eta v=(I-JJ^*)S_CJv=\frac1{27}(8z,-z,\ldots,-z).
\]

Por tanto,

\[
\|\eta v\|^2=\frac{64+8}{729}\|z\|^2
=\frac8{81}\|(C-I)v\|^2.
\]

Aquí aparece el \(8/81\) mencionado por el autor: una fase transportada frente a otras ocho, con la normalización uniforme de nueve fases. El resultado no depende de cuál de las nueve posiciones se marque. El balance operatorio completo es

\[
I-T^*T=\frac8{81}(I-C)^*(I-C)+\frac19(I-C^*C).
\]

Si \(C\) es isométrico, la energía omitida por la publicación queda exactamente en su complemento. Para una costura arbitraria se conserva además su defecto explícito. El entero \(72=64+8\) cuenta aquí pesos cuadráticos; en la corona local cuenta una suma de valores; en \(72/27\) pertenece a una lectura decimal ordenada. Especificar esos tipos permite relacionar las construcciones sin suponer que una coincidencia numérica ya proporciona todos los mapas entre ellas.

Este balance sigue siendo el de la nota anterior. Cuando se aplica a la forma aritmética \(\mathscr W\), produce una identidad firmada; demostrar positividad global requiere el control global de sus términos, no solamente la recuperación del centro o la positividad de una norma auxiliar. Se conservan íntegros los resultados ya probados sobre memoria, transporte y la ventana coerciva.

## Procedencia, controles y continuación editorial

**Arquitectura autoral preexistente:** centro–frontera, suma–producto, corona radical, espejo, vacancias y conservación de memoria. **Resultados recuperados:** cartas y recuentos, canales enteros, vacancias celulares, firma y hojas de \(555555\), inserción de las cinco regiones y balance de capacidad. **Formalización nueva:** reconstrucción multiafín explícita desde la frontera levantada y reunión narrativa de los dos recorridos. **Certificado nuevo:** controles racionales finitos de `verificar_centro_borde_vacancias.py`.

El verificador no reproduce toda la generación de constantes ni prueba un teorema global sobre Weil. Comprueba las operaciones finitas que declara. Las pruebas de capacidad, transporte de firmas y regiones conservan sus propietarios específicos. Esta incorporación está escrita en el expediente de desarrollo; **todavía no se ha integrado en el PDF**.

### Propietarios materiales

- [APP: cartas, hojas, centro y curvatura orientada](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c01_sin_encabezado.tex:229>), y completación cúbica en la misma fuente, líneas 1938–2088.
- [Ortograma APP y cruz radical](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex:205>).
- [Red radical, potencia, vacancia y torsión](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/vacancias/red_radical_potencia_vacancia_euler_torsion.tex:27>).
- [Canales enteros de constantes](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/06c_canales_enteros_constantes.tex>).
- [Firmas, producto de canales y congruencias de transporte](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/05b_extensiones_dinamica_cociente.tex:305>), con la prueba de las 28 y 162 clases en líneas 741–813.
- [Artículo I: centro, registros y firma transversal](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910_REV02/sections/centro_electronico_registros.tex:25>).
- [Artículo I: vacancias conjugadas](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910_REV02/sections/electron.tex:112>) e inserción regional y coeficientes, líneas 356–407.
- [Artículo I: espejo regional](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910_REV02/sections/revision_monodromia.tex:257>) y [capacidad y vacancias](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910_REV02/sections/vacancias_capacidad.tex:1>).
- [Prueba del balance nonádico en este expediente](01_COSTURA_NONADICA_BALANCE_Y_CRITERIO_DE_TRANSPORTE.md) y [transporte aritmético con dominios explícitos](AGENTE_MOMENTOS_CIRCULARES.md).
