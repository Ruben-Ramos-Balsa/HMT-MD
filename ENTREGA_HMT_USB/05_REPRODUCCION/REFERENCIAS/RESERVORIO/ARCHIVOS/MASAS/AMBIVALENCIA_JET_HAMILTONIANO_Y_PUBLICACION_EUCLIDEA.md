# Ambivalencia, primer jet y publicación dinámica en la hoja presente

La relación entre acción, masa y movimiento debe conservar las dos lecturas del estado que preceden a su realización euclídea. El Principio de Ambivalencia no se agota en escribir un cociente de constantes: distingue la lectura areal, aditiva y de borde, la retención volumétrica y la memoria que permite coordinarlas. La descripción local del movimiento aparece después, cuando se especifican la proyección, la conexión y la normalización del presente.

En el desarrollo anterior de Bohr, Kepler y Sommerfeld se utilizaron las salidas de acción, carga y masa en un problema central ya realizado. La ampliación necesaria consiste en mostrar qué conserva esa realización de su antecedente: de dónde procede la razón entre lecturas, cómo se expresa la primera variación en la hoja nula y cómo la reducción del Hamiltoniano transporta memoria a la dinámica efectiva.

## La razón areal–volumétrica conserva la procedencia del estado

La dinámica TPK distingue el modo aditivo \(\Sigma\) y el multiplicativo \(\Pi\). Bajo el bloque de fase \((+1,-1,0)\), las reglas de selección y retención producen la órbita cíclica \((\Sigma,\Pi,\Pi)\). Sus pares consecutivos son \(\Sigma\to\Pi\), \(\Pi\to\Pi\) y \(\Pi\to\Sigma\). En el orden areal–volumétrico, el conteo determina la matriz
\[
F_{\mathrm{av}}=
\begin{pmatrix}
0&1\\
1&1
\end{pmatrix}.
\]
La ausencia de autorretención areal y la presencia de autorretención volumétrica tienen así una procedencia dinámica.

El envolvente de caminos que conserva esos pares tiene un vector positivo de Perron proporcional a \((1,\varphi_{\mathrm{HMT}})\). Como la matriz es simétrica, los pesos de vértice de su medida de Parry, denotados por \(\mu_{\mathrm{ar}}\) y \(\mu_{\mathrm{vol}}\), son proporcionales a \((1,\varphi_{\mathrm{HMT}}^2)\). Por tanto,
\[
\frac{\mu_{\mathrm{ar}}}{\mu_{\mathrm{vol}}}
=\varphi_{\mathrm{HMT}}^{-2}.
\]
Son pesos de historias admisibles del envolvente, no la frecuencia temporal \(1/3,2/3\) de la órbita de tres modos. La distinción conserva el papel de la memoria.

La clausura \(\pi_{\mathrm{HMT}}\) procede del lector coinductivo regional del mismo desarrollo. Se aplica una sola vez al retorno de frontera, no como una entrada convencional de la matriz. Las potencias de \(F_{\mathrm{av}}\) se expresan mediante \(F_0=0\), \(F_1=1\) y \(F_{n+1}=F_n+F_{n-1}\), los números de Fibonacci. Para \(n\geq1\), el retorno marcado tiene la forma
\[
\Theta_n=\pi_{\mathrm{HMT}}\frac{F_{n-1}}{F_{n+1}},
\qquad
\Theta_n\longrightarrow
r_{\mathrm{av}}:=\frac{\pi_{\mathrm{HMT}}}{\varphi_{\mathrm{HMT}}^2}.
\]
Así se compone la clausura con el modo estable de la memoria cuadrática.

Sea \(\mathcal M(x)>0\) la amplitud de memoria compartida por las dos lecturas de un estado enriquecido \(x\). En la realización areal–volumétrica se escriben
\[
\mathcal I_{\mathrm{av}}(x)=\mu_{\mathrm{vol}}\mathcal M(x),
\qquad
\mathcal G_{\mathrm{av}}(x)
=\pi_{\mathrm{HMT}}\mu_{\mathrm{ar}}\mathcal M(x).
\]
La amplitud común se cancela en el cociente:
\[
\frac{\mathcal G_{\mathrm{av}}}{\mathcal I_{\mathrm{av}}}
=r_{\mathrm{av}},
\qquad
\frac{\mathcal G_{\mathrm{av}}-\mathcal I_{\mathrm{av}}}
{\mathcal I_{\mathrm{av}}}
=r_{\mathrm{av}}-1.
\]
El corpus utiliza estos funcionales para distinguir las respuestas gravitatoria e inercial de la interfaz. La letra \(\mathcal G\) de este cociente no es la constante dimensional de Newton \(G\).

En la carta euclídea local de la L gnomónica, ambos lectores descienden a una normalización común:
\[
\frac{\mathcal G_L}{\mathcal I_L}=1
\]
cuando el denominador es no nulo. La igualdad local y la razón anterior pertenecen a dominios de lectura distintos. La igualdad de las publicaciones locales no permite identificar retrospectivamente sus historias ni imponer equipartición entre hojas.

La exposición gravitatoria distingue dos regímenes del lector, no dos valores incompatibles de una misma masa observada. Para convertir una lectura en el coeficiente cinético o gravitatorio de una acción concreta se conservan además el transductor, las unidades y la conexión. Esta precisión permite expresar la distinción inercial–gravitatoria sin sustituirla por una desigualdad escalar universal que el cociente, por sí solo, no afirma.

El intercambio de las dos orientaciones mantiene el enlace electrónico ya reunido:
\[
\mathscr R(x,y)=\frac{x}{y^2},
\qquad
\mathsf J(x,y)=(y,x),
\]
\[
\mathscr R(\pi_{\mathrm{HMT}},\varphi_{\mathrm{HMT}})
=\frac{\pi_{\mathrm{HMT}}}{\varphi_{\mathrm{HMT}}^2},
\qquad
(\mathscr R\circ\mathsf J)
(\pi_{\mathrm{HMT}},\varphi_{\mathrm{HMT}})
=\frac{\varphi_{\mathrm{HMT}}}{\pi_{\mathrm{HMT}}^2}.
\]
La segunda razón interviene exponenciada en la coordenada electrónica. El intercambio actúa sobre el par antes de evaluarlo; no es el inverso escalar de la primera razón.

La transformación conjunta permite seguir qué retorna y qué avanza. Para \(x,y>0\), sean
\[
\mathcal Q(x,y)=\left(\frac{x}{y^2},\frac{y}{x^2}\right),
\qquad P=xy,\qquad O=\frac{x}{y}.
\]
El producto y la razón orientada se transforman exactamente como
\[
(P,O)\longmapsto(P^{-1},O^3)
\longmapsto(P,O^9).
\]
Tras dos aplicaciones retorna el producto, mientras la razón orientada eleva a nueve su exponente; en coordenadas logarítmicas, \((\log P,\log O)\mapsto(\log P,9\log O)\). Por eso \(\mathcal Q\) no es la involución \(\mathsf J\): el retorno de una lectura no es el retorno del estado completo. Para las dos razones anteriores,
\[
\frac{\varphi_{\mathrm{HMT}}}{\pi_{\mathrm{HMT}}^2}
\left(\frac{\pi_{\mathrm{HMT}}}{\varphi_{\mathrm{HMT}}^2}\right)^2
=\varphi_{\mathrm{HMT}}^{-3}.
\]
Este enlace conserva simultáneamente la orientación electrónica y la areal sin identificarlas.

## La hoja nula conserva la primera variación

La realización cuadrática de las tres hojas se escribe
\[
\mathbb A_\tau
=\mathbb R[J_\tau]/(J_\tau^2+\tau I),
\qquad
\tau\in\{+1,0,-1\}.
\]
Sus exponenciales son
\[
e^{tJ_{+1}}=I\cos t+J_{+1}\sin t,
\qquad
e^{tJ_0}=I+tJ_0,
\qquad
e^{tJ_{-1}}=I\cosh t+J_{-1}\sinh t.
\]
Aquí \(I\) es la unidad del álgebra. La expresión real de estas álgebras es una realización posterior del tipado TRIT. En la hoja nula, \(\epsilon:=J_0\) satisface \(\epsilon^2=0\). La prolongación de un funcional diferenciable \(F\) al álgebra dual conserva exactamente el primer jet:
\[
F(x+\epsilon v)=F(x)+\epsilon\,dF_x(v).
\]
El símbolo \(\epsilon\) no designa aquí un número real pequeño. Es un elemento nilpotente; su coeficiente conserva la variación que desaparece al tomar solamente la parte escalar.

Para una acción \(S\), la identidad queda
\[
S(z+\epsilon\,\delta z)=S(z)+\epsilon\,\delta S_z.
\]
La estacionariedad para todas las variaciones admisibles equivale a que ese coeficiente nilpotente se anule. En una acción local regular
\[
S[q]=\int_{t_a}^{t_b}L(q,\dot q,t)\,dt,
\]
su despliegue es
\[
\delta S
=\int_{t_a}^{t_b}
\left(
\frac{\partial L}{\partial q}
-\frac{d}{dt}\frac{\partial L}{\partial\dot q}
\right)\delta q\,dt
+
\left[
\frac{\partial L}{\partial\dot q}\,\delta q
\right]_{t_a}^{t_b}.
\]
La integral contiene la ecuación de movimiento y el término extremo conserva la información de frontera. Fijar los extremos anula este último término para esas variaciones; no significa que el funcional carezca de estructura de borde.

Éste es el enlace preciso entre primer jet y presente variacional. El jet y \(r_{\mathrm{av}}\) son componentes coordinadas del desarrollo, no el mismo objeto: uno conserva la primera variación, mientras el otro compara dos lecturas con memoria.

## El Hamiltoniano efectivo conserva la respuesta de las otras hojas

Sea
\[
\mathcal H=\mathcal H_0\oplus\mathcal H_{\mathrm{ext}},
\qquad
H_{\mathrm{glob}}=
\begin{pmatrix}
H_{00}&V\\
V^*&H_{\mathrm{ext}}
\end{pmatrix}.
\]
La primera componente representa la hoja presente en esta realización; la segunda reúne los grados retenidos de las hojas complementarias. El operador \(V\) acopla ambas. Para escribir la reducción sin cuestiones de dominios no acotados, consideremos un nivel finito o bloques operatorios acotados. Sea \(z\) una energía compleja tal que \(z-H_{\mathrm{ext}}\) y el complemento \(z-H_{00}-V(z-H_{\mathrm{ext}})^{-1}V^*\) sean invertibles.

Para una fuente \(f_0\in\mathcal H_0\), la ecuación \((z-H_{\mathrm{glob}})(\psi_0,\psi_{\mathrm{ext}})=(f_0,0)\) tiene un bloque exterior que permite escribir
\[
\psi_{\mathrm{ext}}
=(z-H_{\mathrm{ext}})^{-1}V^*\psi_0.
\]
Su sustitución en la ecuación central produce
\[
\left[z-H_{00}-\Sigma_0(z)\right]\psi_0=f_0,
\qquad
\Sigma_0(z)=V(z-H_{\mathrm{ext}})^{-1}V^*.
\]
Por tanto, para el proyector \(P_0\) sobre la hoja presente y restringiendo la compresión a \(\mathcal H_0\),
\[
P_0(z-H_{\mathrm{glob}})^{-1}P_0
=
\left[z-H_{00}-\Sigma_0(z)\right]^{-1}.
\]
La proyección no sustituye el Hamiltoniano completo por \(H_{00}\) sin más. El término \(\Sigma_0\) conserva la respuesta de los grados eliminados de la descripción explícita. Su representación temporal produce un núcleo de memoria \(K_0(t,t')\) y la acción efectiva
\[
\begin{aligned}
S_{\mathrm{eff}}[\psi_0]
={}&\int
\psi_0^\dagger(i\hbar\partial_t-H_{00})\psi_0\,dt\\
&-\iint
\psi_0^\dagger(t)K_0(t,t')\psi_0(t')\,dt\,dt'.
\end{aligned}
\]
Una expansión regular en energía alrededor de un punto permitido organiza una descripción local efectiva. Una singularidad espectral mantiene una respuesta no local. Por eso el paso al Lagrangiano del presente debe mostrar cómo se transporta la memoria, además de exhibir una fórmula local.

En un sector mecánico regular, la transformación de Legendre relaciona los generadores mediante \(L=p\cdot\dot q-H\), con \(p=\partial L/\partial\dot q\). Cuando permanecen restricciones o núcleos de memoria, esas estructuras acompañan la transformación. La recuperación de una acción local es una operación sobre un sistema especificado, no un cambio de nombre entre dos expresiones.

## La corona conserva positividad y compatibilidad de refinamiento

En la corona nonádica, para una arista orientada \(a\), sean \(s(a)\) y \(t(a)\) su origen y extremo, y \(U_a\) el transporte de hoja, orientación y acarreo. El defecto covariante de una sección \(f\) es
\[
(D_{9,m}f)(a)=f(t(a))-U_a f(s(a)).
\]
Con un peso \(W_m>0\) y el operador de reloj \(H_{\mathrm{clk},m}\), el Hamiltoniano y la energía de defecto se expresan como
\[
H_m=H_{\mathrm{clk},m}+D_{9,m}^*W_mD_{9,m},
\qquad
\mathcal E_m(f)
=\langle D_{9,m}f,W_mD_{9,m}f\rangle\geq0.
\]
La ausencia de defecto significa transporte compatible a lo largo de cada enlace; una discrepancia contribuye mediante una forma cuadrática positiva.

Sean \(J_m\) y \(K_m\) los transportes de refinamiento de secciones y defectos. Si satisfacen
\[
D_{9,m+1}J_m=K_mD_{9,m},
\qquad
K_m^*W_{m+1}K_m=W_m,
\]
entonces
\[
\begin{aligned}
\mathcal E_{m+1}(J_mf)
&=\langle K_mD_{9,m}f,
W_{m+1}K_mD_{9,m}f\rangle\\
&=\langle D_{9,m}f,W_mD_{9,m}f\rangle
=\mathcal E_m(f).
\end{aligned}
\]
Esta igualdad muestra qué debe conservarse al ampliar la profundidad. La energía de defecto se transporta exactamente por los cuadrados escritos. El texto no identifica por tamaño o por el nombre “corona” esta corona nonádica con cualquier otro complemento cardinal del corpus.

## Relación con las acciones físicas posteriores

La recuperación de la descripción física utiliza también los desarrollos sectoriales. El corpus construye una acción gauge de color en una celularización finita, una diferencia covariante para la materia y un potencial de Higgs con autoacoplamiento calculado desde los lectores angulares en su realización de árbol. La acción gravitatoria conserva por separado co-tétrada, conexión, curvatura, torsión, transductor dimensional y acoplamiento de materia.

Estos cuerpos permiten conducir la exposición hacia las acciones conocidas conservando el origen de sus coeficientes. El Hamiltoniano global, la acción efectiva del presente y el Hamiltoniano modular de frontera cumplen funciones distintas: evolución, variación local y memoria informacional. No se reemplazan mutuamente.

La identificación con una acción conjunta gauge, fermiónica, de Yukawa y de Higgs requiere conservar los términos, las representaciones y los mapas efectivos de cada sector. La fórmula de Schur explica cómo se reduce la dinámica; el primer jet explica cómo se expresa su variación; las acciones sectoriales especifican qué interacciones se realizan. Son operaciones complementarias, y la identificación física completa se formula mediante su composición, no sustituyendo unas por otras.

La ampliación del relato orbital queda así determinada: las ecuaciones centrales de Bohr, Kepler y Sommerfeld pertenecen a una realización que debe leerse junto con su antecedente de dos hojas, su publicación euclídea y su memoria dinámica. La equivalencia local no borra la Ambivalencia; el término efectivo no elimina la historia; y el primer jet hace explícito el lugar donde la acción produce ecuaciones y términos de frontera.
