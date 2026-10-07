# Momentos circulares antes de GNS: memoria nonádica y forma aritmética completa

Nota independiente de investigación matemática, 11 de septiembre de 2026.
No modifica un PDF, un índice ni un certificado de publicación. El resultado
propio es la composición explícita de dos construcciones anteriores a GNS:
un núcleo positivo de memoria y unos momentos circulares de la forma completa.
Su identificación no se presupone.

## 1. Base HMT utilizada y procedencia material

La cadena utilizada es APP → TRIT → TPK → historias enriquecidas del continuo
conjunto → lectores aritméticos y de memoria → representación circular.
Las cinco operaciones del continuo permanecen sobre las mismas historias;
esta nota estudia un lector de su memoria, no construye una quinta rama aislada.
La lectura prima usa los irreducibles producidos por el producto nativo; las
constantes ya publicadas por HMT intervienen sólo después en los lectores.

Propietarios y localizadores de esta lectura:

- Integral autoral de 2.249 páginas, propietario
  `output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex`.
  Se ha releído su cuerpo completo, 1–1929, en la copia conservada en el
  manuscrito de primos. El cociclo está en 943–968; el orden
  positividad → GNS → Stone → Cayley, en 525–612 y 969–987; el transporte
  cilíndrico torcido, en 1023–1118; la pérdida por vuelta, en 1171–1237;
  la costura de nueve fases, en 1421–1495; la fórmula aritmética, en 1578–1610.
- `output/ARITMETICA_GENEALOGICA_PRIMOS_DESARROLLO_DOBLE_CIRCULO_20260911/01_HALLAZGOS_PROPIETARIOS_DOBLE_CIRCULO.md`, leído completo. Conserva los
  localizadores de los antecedentes del bloque APP y de la memoria anteriores
  al GNS; no se confunde su lectura con una nueva lectura íntegra de cada
  antecedente que cita.
- `output/ARITMETICA_GENEALOGICA_PRIMOS_PRESENTACION_20260911/antecedentes/recuperacion_gamma/narrativa_205_paginas/CONSTANTES_ESTRUCTURA_Y_REALIDAD_FISICA_RECOPILACION_INTEGRA.md`, lectura focal 5710–5905. En 5740–5869 reúne producto nativo,
  irreducibles, ocupaciones, calor/Mellin, canal polar y los dos círculos.
  No ofrece allí una secuencia Toeplitz adicional anterior a GNS.
- `output/ARITMETICA_GENEALOGICA_PRIMOS_PRESENTACION_20260911/manuscrito/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.md`, §§2–3, para la forma completa,
  su continuidad y las dos columnas; en este corte se ha releído §2,
  líneas 119–191, y se conserva el análisis anterior de §3.
- `output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/TRAZA_GENERATIVA_COORDINADA.md`: consulta focal de lectores espectrales;
  desde 1524 remite a los momentos primos, no a una medida circular de Weil
  ya seleccionada por la memoria.

La puerta del núcleo permanente y su autocomprobación causal pasaron. La
puerta histórica `apply-hmt-first-principles` resuelve 2.084 páginas; se conserva
como control de ese testigo, no como sustituto de la selección autoral de
2.249 páginas. No se afirma lectura íntegra del corpus ni del documento de 205
páginas.

**Procedencia.** Cociclo, pérdida, dos hojas, grupos de memoria y doble círculo:
`ARQUITECTURA_AUTORAL_PREEXISTENTE` y `RESULTADO_RECUPERADO`. Las pruebas
reunidas que siguen son una `FORMALIZACION_NUEVA` de estos antecedentes.
No se reivindica prioridad histórica de los núcleos de Poisson, de Cayley ni
de las identidades Toeplitz. La procedencia de esta composición exacta dentro
del corpus no ha sido agotada fuera de los propietarios indicados.

## 2. Una representación de memoria efectivamente anterior a Weil

El bloque central de APP, con sus proyectores simétrico y antisimétrico, es

\[
B_c=\begin{pmatrix}7&2\\2&7\end{pmatrix}
=9P_++5P_-.
\]

La normalización del modo diferencial publica \(q=5/9\). La vuelta completa
del TPK conserva la fase e incrementa la memoria entera:

\[
m(\Gamma_9^n)=n,\qquad
m(\gamma_2\gamma_1)=m(\gamma_2)+m(\gamma_1).
\]

Sobre una órbita reversible de esa memoria, sus estados levantados se
identifican con \(e_n\), \(n\in\mathbb Z\), y la vuelta es el desplazamiento
\(Se_n=e_{n+1}\). La inyectividad de esa enumeración procede del incremento
de memoria. Si se parte sólo del semigrupo de vueltas positivas, el mismo
espacio bilateral es la extensión de desplazamiento que añade sus antecedentes;
no se atribuye reversibilidad a una transición que sólo se haya demostrado
isométrica. En un árbol completo se conservan las restantes etiquetas en un
factor transversal: el desplazamiento actúa sobre memoria, no identifica rutas.

Este \(S\) no es el Cayley de Weil insertado en la costura. Es la realización
regular de la operación entera de memoria. Su positividad hilbertiana se conoce
antes de formar un GNS de la forma aritmética.

### 2.1. Vector de pérdidas, correlaciones y terminal

La telescopía por vueltas produce pesos \((1-q^2)q^{2j}\). Su amplitud en la
memoria es el vector explícito

\[
v_q=\sqrt{1-q^2}\sum_{j=0}^{\infty}q^j e_j,
\qquad \|v_q\|^2=1.
\]

Con producto interior lineal en la primera variable, para \(n\ge0\),

\[
\langle S^n v_q,v_q\rangle
=(1-q^2)\sum_{j\ge0}q^j q^{j+n}=q^n.
\]

La conjugación y la unitariedad dan, para todo entero,

\[
\boxed{m_n^{\mathrm{mem}}=q^{|n|}.}
\]

El truncamiento \(v_{q,N}=\sqrt{1-q^2}\sum_{j=0}^{N-1}q^j e_j\) conserva
exactamente el terminal:

\[
\|v_{q,N}\|^2=1-q^{2N},\qquad
\langle S^n v_{q,N},v_{q,N}\rangle
=q^n\bigl(1-q^{2(N-n)}\bigr),\quad 0\le n<N.
\]

Para \(n\ge N\), esa correlación truncada vale cero. Por tanto, para cada
\(n\) fijo, la diferencia respecto del momento completo es
\(q^{2N-n}\) cuando \(N>n\), y tiende a cero. Esta fórmula no borra el
último registro ni equipara un truncamiento con toda la historia.

### 2.2. Toeplitz positiva, factorización triangular y determinante

Para índices \(0,\ldots,N\), defínase

\[
T_N=(q^{|i-j|})_{0\le i,j\le N}.
\]

Es un Gram de \(v_q,Sv_q,\ldots,S^Nv_q\), de modo que

\[
\sum_{i,j=0}^{N}\overline{c_i}c_j(T_N)_{ij}
=\left\|\sum_{j=0}^{N}c_jS^jv_q\right\|^2\ge0.
\]

Hay además una prueba exacta sin series infinitas. Sean

\[
L_{ij}=\begin{cases}q^{i-j},&i\ge j,\\0,&i<j,\end{cases}
\qquad D=\operatorname{diag}(1,1-q^2,\ldots,1-q^2).
\]

Entonces \(T_N=LDL^*\). Para \(i\ge j\), la entrada del producto es

\[
q^{i+j}+(1-q^2)\sum_{k=1}^{j}q^{i+j-2k}
=q^{i-j}.
\]

Por simetría se obtiene la identidad entera de matrices. Una Cholesky es
\(L D^{1/2}\), y, puesto que \(\det L=1\),

\[
\boxed{\det T_N=(1-q^2)^N=(56/81)^N>0.}
\]

Este núcleo positivo nace de la pérdida y de la memoria conservada. No
requiere ceros, una función zeta positiva ni un GNS de Weil.

## 3. Fase, refinamiento nonádico y límite de estados

Una representación por fase fija se obtiene de

\[
v_{r,\theta}=\sqrt{1-r^2}\sum_{j\ge0}r^j e^{-ij\theta}e_j,
\quad 0<r<1,
\]

y produce \(m_n=r^{|n|}e^{in\theta}\). Las Toeplitz son conjugadas
diagonalmente de las anteriores y tienen determinante \((1-r^2)^N\).
La fase \(\theta\) es aquí una coordenada de la familia de caracteres; no se
ha seleccionado una fase espectral aritmética.

Sobre el círculo, con Haar normalizada \(d\lambda\), esos momentos poseen
la medida explícita

\[
d\nu_{r,\theta}(z)
=\frac{1-r^2}{|1-r e^{-i\theta}z|^2}\,d\lambda(z).
\]

La expansión de ambas series geométricas prueba directamente sus
coeficientes de Fourier, sin usar una medida objetivo.

### 3.1. Raíces nonádicas del radio

Tomando \(r_m=q^{1/9^m}\), se cumple \(0<r_m<1\),
\(r_{m+1}^{9}=r_m\) y \(r_m\to1\). Para fase fija,

\[
r_m^{|n|}e^{in\theta}\longrightarrow e^{in\theta}
\quad\text{para cada }n\in\mathbb Z.
\]

Las medidas son probabilidades; la aproximación uniforme por polinomios
trigonométricos extiende la convergencia de los momentos a toda función
continua. En consecuencia,

\[
\nu_{r_m,\theta}\ \rightharpoonup\ \delta_{e^{i\theta}}.
\]

Esto muestra cómo una medida atómica puede surgir como límite débil de
estados de memoria. No es un límite fuerte de los vectores en la misma
representación regular: cada coeficiente de \(v_{r_m,\theta}\) tiende a
cero, pero sus normas siguen siendo uno.

Hay que conservar una precisión de naturalidad. Bajo \(p_9(z)=z^9\),

\[
(p_9)_*\nu_{r,\theta}=\nu_{r^9,9\theta}.
\]

Por tanto, el radio nonádico con fase fija **no** da por sí solo un sistema
proyectivo de medidas bajo \(p_9\). Para ello deben conservarse fases
levantadas con \(9\theta_{m+1}=\theta_m\pmod{2\pi}\), incluidas sus
elecciones de rama; o bien declararse que el refinamiento usado mantiene la
coordenada angular y sólo cambia el radio. Son operaciones distintas.

### 3.2. Qué fija la memoria y qué debe fijar su lector

La memoria produce el grupo, la positividad de sus Grams y estas familias
compatibles de correlación. Una fase concreta o una mezcla de fases exige
el lector que selecciona sus amplitudes. Por ejemplo, el vector \(e_0\)
produce \(m_n=\mathbf1_{n=0}\); \((e_0+e_1)/\sqrt2\) produce
\(m_0=1,m_{\pm1}=1/2\) y los demás momentos nulos. La misma operación de
memoria admite ambos estados positivos.

La representación regular tiene medidas vectoriales absolutamente continuas
respecto de Haar. Un filtro vectorial \(L^2\) fijo no puede producir una
medida puramente atómica no nula. El límite débil anterior muestra una vía
precisa para que cambie el tipo espectral al refinar: hay que conservar y
controlar ese límite de estados, no sólo aumentar la longitud de una órbita
de fase previamente elegida. Esto no niega la representación espectral del
corpus ni la generación conjunta HMT; distingue los dominios de dos lectores.

## 4. Un Cayley anterior al GNS sobre pruebas aritméticas

Ahora se construye un segundo objeto, sin suponer positividad de Weil.
El producto nativo y sus irreducibles ya proporcionan
\(\ell_{p,k}=k\log p\), \(w_{p,k}=(\log p)p^{-k/2}\). Las lecturas
gamma y polar completan la forma \(\mathscr W\) escrita en §5.
El papel de la memoria es ofrecer un índice entero de iteración; el operador
siguiente actúa efectivamente sobre las funciones de esa publicación.

El operador \(C_a\) es un lector analítico auxiliar de esta formalización.
La elección \(a>1/2\) no reemplaza silenciosamente la costura canónica
\(a=1/2\), ni se declara que esa elección haya sido ya seleccionada por
el TPK.

Fíjense \(a>b>1/2\). Sea \(\mathscr E_b\) el espacio de funciones suaves
tales que, para cada derivada de orden \(j\),
\(\sup_x e^{b|x|}|f^{(j)}(x)|<\infty\). Contiene todas las pruebas
compactamente soportadas. Defínanse

\[
(R_a^+f)(x)=\int_0^\infty e^{-at}f(x+t)\,dt,
\qquad
(R_a^-f)(x)=\int_0^\infty e^{-at}f(x-t)\,dt,
\]

\[
\boxed{C_af=f-2aR_a^+f,\qquad C_a^{-1}f=f-2aR_a^-f.}
\]

Estas integrales son lectores de traslación construidos sobre las pruebas;
no utilizan el espectro de los ceros. El parámetro \(a=1\), por ejemplo,
procede de la unidad y deja elegir \(1/2<b<1\); no calibra ningún cero.

**Dominio e inversa.** La desigualdad
\(e^{b|x|}|f(x\pm t)|\le M_0e^{bt}\) da la cota
\(\|R_a^\pm f\|_b\le\|f\|_b/(a-b)\), también para cada derivada.
Así, ambos operadores preservan \(\mathscr E_b\). Con la convención
\(\widehat f(z)=\int f(x)e^{-izx}\,dx\), sus multiplicadores son

\[
\widehat{C_af}(z)=c_a(z)\widehat f(z),\qquad
c_a(z)=\frac{z-ia}{z+ia},
\]

y el multiplicador del operador inverso es \(c_a(z)^{-1}\). La identidad
en Fourier real prueba ambas composiciones inversas. En \(L^2\),
\(|c_a(t)|=1\), de modo que \(C_a\) es unitario para la norma ordinaria,
sin utilizar la norma de Weil. Sobre pruebas puede escribirse
\(C_a=(H+ia)(H-ia)^{-1}\) con \(H=i\partial_x\); aquí la fórmula
integral, no un generador GNS, define los operadores.

**Advertencia de dominio exacta.** El parámetro \(a=1/2\) del Cayley del
propietario no puede introducirse sin más en estas integrales pre-GNS.
Para una prueba compacta, \(R_{1/2}^+f\) tiene en general una cola
proporcional a \(e^{x/2}\) hacia \(-\infty\); su evaluación polar negativa
no converge. No se ha probado una divergencia de la forma reunida, sino
que esta descomposición término a término exige el margen \(a>1/2\).
El Cayley del GNS puede usar después \(a=1/2\) sobre su dominio hilbertiano.

## 5. Conservación exacta de gamma, primos y polar

Para \(f,g\in\mathscr E_b\), sean

\[
C_{f,g}(u)=\int f(x)\overline{g(x-u)}\,dx,
\qquad P_f^\pm=\int f(x)e^{\pm x/2}\,dx.
\]

La forma completa se define por

\[
\begin{aligned}
\mathscr W(f,g)={}&c_\Gamma C_{f,g}(0)
+\int_0^\infty\frac{e^{-u/2}}{1-e^{-2u}}
 [2C_{f,g}(0)-C_{f,g}(u)-C_{f,g}(-u)]\,du\\
&-\sum_{p,k}w_{p,k}
 [C_{f,g}(\ell_{p,k})+C_{f,g}(-\ell_{p,k})]\\
&+P_f^+\overline{P_g^-}+P_f^-\overline{P_g^+},
\qquad c_\Gamma=\psi(1/4)-\log\pi.
\end{aligned}
\]

**Existencia.** La cota de correlación
\(|C_{f,g}(u)|\le M_fM_g(|u|+1/b)e^{-b|u|}\) prueba la
convergencia absoluta de la suma prima, dominada por una serie del tipo
\(\sum_{n\ge2}(\log n)(1+\log n)n^{-b-1/2}\).
La diferencia simétrica de correlaciones es \(O(u^2)\) en cero, mientras
el peso gamma es \(O(u^{-1})\); en infinito el peso es exponencial.
Las evaluaciones polares convergen porque \(b>1/2\). Estas cotas prueban
también la continuidad en los seminormas indicados. No se usa positividad.

**Identidad de conservación.** Como \(C_a\) es unitario en \(L^2\) y
conmuta con todas las traslaciones,

\[
C_{C_af,C_ag}(u)=C_{f,g}(u)\qquad(u\in\mathbb R).
\]

Por Fubini, los dos lectores polares verifican

\[
P_{C_af}^+=-\frac{a-1/2}{a+1/2}P_f^+,
\qquad
P_{C_af}^-=-\frac{a+1/2}{a-1/2}P_f^-.
\]

Los factores son reales y recíprocos, por lo que cada producto polar cruzado
queda exactamente conservado. Reuniendo los tres canales,

\[
\boxed{\mathscr W(C_af,C_ag)=\mathscr W(f,g).}
\]

La identidad vale para todas las potencias enteras y para todos los términos
cruzados. Demuestra invariancia de una forma hermítica, no su signo.

## 6. Momentos circulares aritméticos explícitos, anteriores a GNS

Defínanse

\[
m_n^{\mathrm{ar}}(f,g)=\mathscr W(C_a^n f,g),\qquad n\in\mathbb Z.
\]

La fórmula completa de §5, con \(C_a^nf\) en su primera entrada, calcula
estos momentos desde primos, gamma y polar. Cada evaluación existe en
\(\mathscr E_b\); no requiere una lista de ceros ni una métrica positiva.
La hermiticidad y la invariancia anterior dan

\[
m_{-n}^{\mathrm{ar}}(g,f)=\overline{m_n^{\mathrm{ar}}(f,g)},\qquad
\mathscr W(C_a^j f,C_a^k g)=m_{j-k}^{\mathrm{ar}}(f,g).
\]

Para una sola prueba, la matriz
\(T_N^{\mathrm{ar}}(f)_{jk}=m_{k-j}^{\mathrm{ar}}(f,f)\)
es hermítica Toeplitz y satisface la identidad exacta

\[
c^*T_N^{\mathrm{ar}}(f)c
=\mathscr W\!\left(\sum_{k=0}^N c_k C_a^k f,
                    \sum_{k=0}^N c_k C_a^k f\right).
\]

Se ha construido la matriz sin asumir que sea positiva. La igualdad permite
contrastar su positividad con un Gram nativo de memoria; no la presupone.

### 6.1. Una obligación aritmética visible en el canal polar

Para \(a=1\), la contribución polar exacta a \(m_n^{\mathrm{ar}}(f,g)\) es

\[
(-1/3)^nP_f^+\overline{P_g^-}
+(-3)^nP_f^-\overline{P_g^+}.
\]

Para una prueba real, par y positiva no nula, \(P_f^+=P_f^-=p>0\), de
modo que aparece \(p^2[(-1/3)^n+(-3)^n]\). Si el momento total es
positivo definido, sus menores de orden dos obligan a

\[
|m_n^{\mathrm{ar}}(f,f)|\le m_0^{\mathrm{ar}}(f,f).
\]

Por ello, la identificación circular debe contabilizar la cancelación
concreta de ese crecimiento con los canales gamma y primo. Una simetría
formal de las dos hojas no sustituye ese cálculo. Esta observación no
declara que la cancelación falle; proporciona un falsador exacto para una
candidata a composición.

### 6.2. Cobertura: conservar momentos mixtos

Para una familia de pruebas \(f_1,\ldots,f_d\), el objeto adecuado es el
Toeplitz por bloques

\[
\mathsf T_{(j,r),(k,s)}
=m_{k-j}^{\mathrm{ar}}(f_s,f_r).
\]

Su forma cuadrática es \(\mathscr W(F,F)\), donde
\(F=\sum_{k,s}c_{k,s}C_a^k f_s\). Controlar sólo las matrices escalares
de algunas pruebas no controla los cruces entre pruebas diferentes.
Para una familia densa en cada \(C_c^\infty([-R,R])\), la continuidad
demostrada permite pasar al dominio completo, siempre que se hayan
establecido los Grams mixtos y las compatibilidades al aumentar \(R\).
El crecimiento de \(N\) de una única órbita no prueba esa cobertura.

### 6.3. Transporte exacto de una cota local a pruebas con colas

La identidad anterior tiene una aplicación positiva que no exige identificar
todavía todos los momentos con la memoria. Supóngase demostrada por el
complemento de Schur, en el intervalo \(I=(-1/18,1/18)\), la cota

\[
\mathscr W(f,f)\geq\tfrac12\|f\|_{L^2}^2,
\qquad f\in C_c^\infty(I).
\]

Este apartado recibe esa estimación como resultado del cálculo local
correspondiente; no la deduce de la existencia de \(C_a\). Sea
\((\tau_t f)(x)=f(x-t)\). La traslación conserva las correlaciones y
satisface

\[
P_{\tau_t f}^{\pm}=e^{\pm t/2}P_f^{\pm}.
\]

Sus productos polares cruzados también se conservan. Por tanto,
\(\mathscr W(\tau_t f,\tau_t g)=\mathscr W(f,g)\), y la norma
ordinaria \(L^2\) es invariante. Como \(C_a\) y \(\tau_t\) conmutan,
para todo entero \(n\), todo \(t\in\mathbb R\) y toda prueba local,

\[
\boxed{\mathscr W(C_a^n\tau_t f,C_a^n\tau_t f)
=\mathscr W(f,f)
\geq\tfrac12\|C_a^n\tau_t f\|_{L^2}^2.}
\]

Para \((n,t)\) fijo, ésta es una cota coerciva en todo el subespacio
\(C_a^n\tau_t C_c^\infty(I)\), no sólo en un ejemplo. Cuando
\(n\ne0\), las pruebas transformadas pueden tener colas exponenciales
no compactas. En su forma aritmética pueden intervenir infinitos relojes
primos; la igualdad exacta de los tres canales controla su composición,
y las cotas de §5 garantizan la convergencia. No se ha sustituido esa suma
por un truncamiento finito.

Los términos cruzados entre subespacios con exponentes o traslaciones
distintos conservan, en cambio, sus momentos completos. Por ejemplo,

\[
\mathscr W(C_a^n\tau_t f,C_a^m\tau_s g)
=\mathscr W(C_a^{n-m}\tau_{t-s}f,g).
\]

La cota de cada subespacio individual no implica la positividad de su
suma algebraica. Ésta se decide mediante los Grams mixtos de §6.2.
Así queda aislado un alcance positivo efectivo —familias enteras de
pruebas con colas— sin promoverlo a todo el dominio por la sola
invariancia del transporte.

## 7. Composición exacta que debe contrastarse con el estado HMT

La memoria ya produce un Hilbert positivo \(\mathcal K_{\rm mem}\), su
operación de vuelta \(S\) o su dilatación isométrica, y Grams positivos.
Los canales aritméticos ya producen \(C_a\) y
\(m_n^{\mathrm{ar}}\) sin GNS. Una identificación prospectiva tiene forma

\[
\boxed{m_n^{\mathrm{ar}}(f,g)
=\langle S^n\mathcal E f,\mathcal E g\rangle_{\rm mem}}
\]

para un lector \(\mathcal E\) construido desde las operaciones de las
mismas historias y no definido como \(\mathscr W^{1/2}\). En ese caso
todos los Toeplitz mixtos son Grams; el GNS aritmético llega después como
realización de un producto ya obtenido.

Es suficiente demostrar la identidad de momento cero y el entrelazamiento
\(\mathcal E C_a=S\mathcal E\), con los dominios y compatibilidades
indicados. El momento cero es la identificación de la energía completa,
no una condición menor: no puede darse por probado sólo porque exista
\(\mathcal E\) con algún Gram positivo.

En la forma de las dos columnas del manuscrito, el cálculo sigue siendo

\[
\Xi^*\Xi=J_+^*J_+,\qquad
\Xi^*P\Xi=J_-^*J_-,\qquad
\mathcal E=(I-P)\Xi.
\]

Si \(P\) es proyección ortogonal, estas dos igualdades producen
\(\mathcal E^*\mathcal E=J_+^*J_+-J_-^*J_-\).
No basta verificar una de ellas ni reemplazar las columnas completas por
las de un bloque gamma aislado. Las fases y momentos de esta nota hacen
explícito qué debe transmitir esa composición a todas las vueltas.

El núcleo \(q^{|n|}\) no se identifica aquí con
\(m_n^{\mathrm{ar}}(f,g)\). Es un antecedente positivo efectivo y ofrece
una factorización local; el lector \(\mathcal E\) debe conservar también
las etiquetas primas, pesos, contribuciones polares y el límite de estados
si el tipo espectral cambia. Declarar esa igualdad por definición introduciría
el resultado que se intenta construir.

## 8. Controles ejecutados y balance

El archivo `verificar_momentos_memoria.py` conserva 1.046 comprobaciones exactas con
fracciones racionales: factorización \(LDL^*\) y determinantes en dimensiones
1–13 para \(q=5/9\), correlaciones truncadas hasta 20 posiciones y factores
polares recíprocos para cuatro valores racionales de \(a>1/2\). Se ejecuta
con `/usr/bin/python3 -I -S` y admite también `-O`; sus condiciones no
dependen de instrucciones `assert`. Los recibos focales son
`CONTROL_MOMENTOS_MEMORIA_NORMAL.json` y
`CONTROL_MOMENTOS_MEMORIA_OPTIMIZADO.json`. No se ejecutó aquí una campaña intervalar de momentos
de Weil, ni se convierten esos controles en una prueba global.

El avance utilizable es doble: la memoria de pérdidas produce un núcleo
Toeplitz positivo con Cholesky y terminal explícitos, y la forma completa
admite un Cayley integral anterior a GNS que construye sus momentos
circulares y conserva cada canal. La regularización nonádica muestra además
cómo pasar de estados regulares a átomos por límite débil, con su condición
de fase correctamente separada. La unión de ambas construcciones conserva
como ecuación precisa la identificación de los dos momentos completos.

Esta nota no refuta esa unión, no prueba su ausencia en todo el corpus y
no la declara establecida por las identidades locales. Deja una composición
concreta que puede ser contrastada y desarrollada por el editor principal.
