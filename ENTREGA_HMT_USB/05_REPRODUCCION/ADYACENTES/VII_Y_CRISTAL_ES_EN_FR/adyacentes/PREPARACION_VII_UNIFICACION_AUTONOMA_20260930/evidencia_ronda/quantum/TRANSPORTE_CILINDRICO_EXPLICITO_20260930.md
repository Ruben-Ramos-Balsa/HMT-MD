# Transporte cilíndrico explícito: amplitudes, refinamiento y conexiones

Desarrollo separado del 30 de septiembre de 2026. No modifica la entrega
sellada, los manuscritos ni sus PDF. Se reúne un mapa efectivo contenido
implícitamente en la representación de amplitudes de 04ab y se calculan sus
operaciones. La conexión construida aquí es cinemática; no se la sustituye
por la conexión física total PCH ni por el Hamiltoniano compuesto de la ronda.

## 1. Propietario, genealogía y dominio de la construcción

Propietario principal:

[Reconstrucción del estado genealógico, 04ab](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/04ab_postulados_cuanticos_genealogicos_rev2.tex>).

Sus localizadores son: categoría y realización apuntada, líneas 31–86;
amplitudes de la medida, ecuación `eq:estado-amplitudes-medida-rev2`,
línea 219; reconstrucción cinemática, líneas 336–382. La fórmula del estado
y su regla cuadrática están en la fuente. El mapa explícito de refinamiento,
su derivada y la completación compatible siguientes se desarrollan aquí
desde esa fórmula; no se presentan como citas literales del propietario.

El antecedente sigue siendo APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo. Los prefijos etiquetan secciones
ya producidas, con ruta, hojas, frontera, orientación, acarreo y memoria.
Las cinco construcciones permanecen en ese estado común. La medida pertenece
a la preparación y las fases a su realización: no seleccionan retrospectivamente
las semillas ni las constantes. No se introduce ningún valor metrológico.

Sea \(\Omega_\infty\) el dominio de secciones compatibles del propietario y
\(\mathcal S_n\) una partición finita por prefijos. Si \(t\in\mathcal S_m\)
prolonga \(s\in\mathcal S_n\), \(m\ge n\), escribimos \(t\succ s\).
Cada prefijo tiene un único antecesor en cada nivel anterior. La preparación
proporciona una medida compatible y fases:
\[
p_s=\mu(C_s),\qquad p_s=\sum_{t\succ s}p_t,\qquad \theta_s\in\mathbb R.
\tag{1}
\]
Para derivar, estos datos dependen \(C^2\) de un parámetro \(b\) en una carta
\(B\). Se trabaja sobre soporte positivo fijo \(p_s(b)>0\). Una rama de
probabilidad nula en una preparación no se declara inexistente en HMT:
simplemente no admite el cociente de (1) en esta carta. Tampoco se prolonga
la fórmula a cambios de soporte sin tratar su dominio.

Sea \(E\) un Hilbert real con \(J_E^*=-J_E\), \(J_E^2=-I\), fijo en esta
trivialización. La carta compleja identifica \(J_E\) con \(i\).
Póngase \(\mathcal H_n=\ell^2(\mathcal S_n)\otimes E\).
Para un vector unitario \(u_0\), el estado propietario es
\[
\Psi_n=\sum_{s\in\mathcal S_n}\sqrt{p_s}\,
                 |s\rangle\otimes e^{\theta_sJ_E}u_0.
\tag{2}
\]
La profundidad del prefijo no se identifica con refinamiento espacial ni
con el tiempo de un Hamiltoniano.

## 2. Aplicación explícita y tres niveles de refinamiento

Para \(m\ge n\), definimos
\[
J_{mn}(|s\rangle\otimes u)
 =\sum_{\substack{t\in\mathcal S_m\\t\succ s}}
    \sqrt{\frac{p_t}{p_s}}\,
       |t\rangle\otimes e^{(\theta_t-\theta_s)J_E}u.
\tag{3}
\]
Incluye **todas** las prolongaciones de la preparación, no una continuación
marcada. En un refinamiento nonádico se retienen conjuntamente los nueve
hijos presentes.

**Proposición 1.** \(J_{mn}\) es isométrico; su adjunto es
\[
(J_{mn}^*v)_s
 =\sum_{t\succ s}\sqrt{\frac{p_t}{p_s}}\,
                  e^{-(\theta_t-\theta_s)J_E}v_t.
\tag{4}
\]
Además,
\[
J_{mn}\Psi_n=\Psi_m,\qquad J_{mn}^*\Psi_m=\Psi_n,\qquad
J_{\ell m}J_{mn}=J_{\ell n}\quad(\ell\ge m\ge n).
\tag{5}
\]

**Prueba.** Hijos de padres diferentes tienen soporte disjunto. Para un
mismo padre, la ortogonalidad de \(e^{\phi J_E}\) y (1) dan
\[
\|J_{mn}(|s\rangle\otimes u)\|^2
 =\sum_{t\succ s}\frac{p_t}{p_s}\|u\|^2=\|u\|^2.
\]
La polarización prueba \(J_{mn}^*J_{mn}=I\); tomar adjuntos de los
coeficientes da (4). Aplicar (3) a (2) cancela \(\sqrt{p_s}\) y suma las
fases \(\theta_t-\theta_s+\theta_s\), produciendo \(\Psi_m\).
El adjunto y la isometría dan la segunda igualdad.

Para \(u\in\mathcal S_\ell\) sobre \(s\), hay un único antecesor
\(t\in\mathcal S_m\). El coeficiente compuesto es
\[
\sqrt{p_u/p_t}\sqrt{p_t/p_s}=\sqrt{p_u/p_s},
\]
y el transporte de fase es
\(e^{(\theta_u-\theta_t)J_E}e^{(\theta_t-\theta_s)J_E}
=e^{(\theta_u-\theta_s)J_E}\).
Esto prueba el último cuadrado de (5), sin descartar las otras ramas. ∎

La prueba no identifica los puntos de una ruta por compartir un histograma.
Las etiquetas de todos los prefijos permanecen explícitas en (3).

## 3. Derivada del mapa y conexión métrica de las medidas

Pongamos \(q_{t|s}=p_t/p_s\), \(\phi_{ts}=\theta_t-\theta_s\).
En la carta de soporte positivo, la derivada direccional es
\[
\begin{split}
(\delta_NJ_{mn})(|s\rangle\otimes u)
 =\sum_{t\succ s}\sqrt{q_{t|s}}\,|t\rangle\otimes
 e^{\phi_{ts}J_E}
 \left[\frac12\delta_N\log q_{t|s}
                         +(\delta_N\phi_{ts})J_E\right]u.
\end{split}
\tag{6}
\]
Es la regla del producto aplicada a (3), con \(J_E\) fijo. Diferenciar
(5) da el cuadrado móvil completo:
\[
\delta_NJ_{\ell n}
 =(\delta_NJ_{\ell m})J_{mn}
                  +J_{\ell m}(\delta_NJ_{mn}).
\tag{7}
\]
No se reemplaza por una identidad de matrices congeladas. En cada nivel
los conjuntos son finitos: las derivadas son operadores acotados localmente
en la carta positiva. No se deduce de ello una cota uniforme en \(n\).

Hay asimismo un mapa explícito entre las realizaciones con producto
ponderado. Fijado \(b_0\in B\), sea
\(\rho_s(b)=p_s(b)/p_s(b_0)\). La aplicación
\[
A_n(b):L^2(\mathcal S_n,p(b_0);E)\longrightarrow
       L^2(\mathcal S_n,p(b);E),\qquad
(A_nf)_s=\rho_s^{-1/2}f_s
\tag{8}
\]
es unitaria. Su conexión métrica natural es
\[
\nabla_N^\mu=\delta_N+\frac12\delta_N\log\rho,\qquad
\nabla_N^\mu A_n=A_n\delta_N .
\tag{9}
\]
La segunda expresión se aplica a secciones y se prueba usando
\(\delta_N\rho^{-1/2}
=-\tfrac12(\delta_N\log\rho)\rho^{-1/2}\).
La identidad métrica se comprueba directamente:
\[
\delta_N\langle f,g\rangle_{p(b)}
 =\langle\nabla_N^\mu f,g\rangle_{p(b)}
  +\langle f,\nabla_N^\mu g\rangle_{p(b)} .
\]
La escala y la fase son datos distintos. Si se incluye además
\(R_\theta=e^{(\theta(b)-\theta(b_0))J_E}\), el mapa
\(R_\theta A_n\) es entrelazante para
\(\delta_N+\tfrac12\delta_N\log\rho-(\delta_N\theta)J_E\).
Estas identidades no eliminan ni recalibran la acción HMT.

## 4. Conexión transportada y conexión proyectada: cálculo que las distingue

Sea \(J=J_{mn}\), \(P=JJ^*\), \(\mathcal M_b=\operatorname{Im}J(b)\).
Transportar una conexión \(\nabla^{(n)}\) significa definir, para \(v=Ju\),
\[
\nabla^{\rm tr}(Ju)=J\nabla^{(n)}u.
\tag{10}
\]
Está bien definida porque \(J^*J=I\). Aplicarla dos veces demuestra
\(R^{\rm tr}J=JR^{(n)}\). Por tanto una conexión plana recibida se
transporta plana sobre esa imagen. Esto no afirma que la derivada ambiental
ordinaria preserve \(\mathcal M_b\).

La conexión de proyección \(\nabla^P=P\,d\) es otra operación. Al llevarla
de vuelta al dominio por \(J\), se obtiene
\[
J^*\nabla^P J=d+J^*dJ,\qquad
(J^*dJ)_s=J_E\,b_s,\quad
b_s=\sum_{t\succ s}q_{t|s}\,d\phi_{ts}.
\tag{11}
\]
En efecto, la parte real de (6) suma
\(\frac12\sum_t dq_{t|s}=\frac12d1=0\); queda la parte de fase.
Las matrices son diagonales en el padre y proporcionales al mismo
\(J_E\), por lo que la curvatura es
\[
J^*R^P J
 =\operatorname{diag}_s\left(
 J_E\sum_{t\succ s}dq_{t|s}\wedge d\phi_{ts}\right).
\tag{12}
\]
No es nula en general.

**Control nonádico.** Para nueve hijos, tómense
\(q_1=p\), \(q_2=\cdots=q_9=(1-p)/8\), \(0<p<1\), y
\(\phi_1=t\), \(\phi_2=\cdots=\phi_9=0\).
Entonces \(b=p\,dt\) y
\[
J^*R^P J=J_E\,dp\wedge dt\ne0.
\tag{13}
\]
Todas las probabilidades son positivas y están presentes las nueve ramas.
Es un control de la diferencia entre conexiones, no una evaluación física
ni una refutación de la compatibilidad HMT.

En particular, transportar la conexión plana \(d\) exige en el subfibrado
la conexión
\[
\nabla^{\rm tr}v=P\,dv-J(J^*dJ)J^*v.
\tag{14}
\]
Para \(v=Ju\), los términos \(J(J^*dJ)u\) se cancelan y queda \(J\,du\).
Así (14) tiene curvatura cero sobre la imagen. La cancelación está calculada;
no se ha declarado que \(P\,d\) fuera plano. Una expresión ambiental que
incluya \((dJ)J^*\) tampoco se interpreta como un Hamiltoniano autoadjunto
en todo el complemento: su objeto es esta conexión de subfibrado.

## 5. Una trivialización compatible construida en todos los niveles

Puede extenderse la conexión a las fibras completas sin postular un
entrelazamiento. Damos una construcción explícita local, con referencia
\(b_0\), que no se identifica con una dinámica física elegida previamente.

Para cada padre \(s\in\mathcal S_n\), sean los vectores reales unitarios
positivos
\[
a_s(b)=(\sqrt{q_{t|s}(b)})_{t\succ s},\quad
a_s^0=a_s(b_0),\quad c_s=\langle a_s,a_s^0\rangle>0,
\]
\[
K_s=a_s(a_s^0)^{\mathsf T}-a_s^0a_s^{\mathsf T},\qquad
O_s=I+K_s+\frac{K_s^2}{1+c_s}.
\tag{15}
\]
Entonces \(O_s^{\mathsf T}O_s=I\) y \(O_sa_s^0=a_s\).

**Prueba de estas identidades.** \(K_s^*=-K_s\) y
\(K_s^3=-(1-c_s^2)K_s\). Sustituir estas identidades en
\(O_s^*O_s\) anula los términos no constantes.
Además,
\(K_sa_s^0=a_s-c_sa_s^0\) y
\(K_s^2a_s^0=(c_s^2-1)a_s^0\); sustituyendo en (15) se obtiene
\(O_sa_s^0=a_s\). El denominador no se anula en la carta positiva. ∎

Sea \(D_s(b)\) diagonal en los hijos, con bloques \(e^{\theta_t(b)J_E}\).
La aplicación unitaria sobre el bloque de hijos de \(s\),
\[
R_s(b)=e^{-(\theta_s(b)-\theta_s(b_0))J_E}
 D_s(b)(O_s(b)\otimes I_E)D_s(b_0)^*,
\tag{16}
\]
satisface \(R_sJ_{n+1,n}(b_0)|_s=J_{n+1,n}(b)|_s\).
Por suma directa, \(R_n=\bigoplus_sR_s\) cumple
\[
R_nJ_n^0=J_n(b),\qquad J_n^0=J_{n+1,n}(b_0).
\tag{17}
\]
La acción de (16) sobre la columna inicial cancela exactamente la fase del
padre y aplica \(O_sa_s^0=a_s\).

Incluyamos un nivel raíz \(\mathcal S_0=\{*\}\), \(p_*=1\).
Póngase
\(\mathcal U_0(b)=e^{(\theta_*(b)-\theta_*(b_0))J_E}\).
Recursivamente,
\[
\mathcal U_{n+1}(b)=R_n(b)
 \left[J_n^0\mathcal U_n(b)(J_n^0)^*
                    +(I-J_n^0(J_n^0)^*)\right].
\tag{18}
\]
El corchete es unitario: actúa como \(\mathcal U_n\) sobre la imagen de
\(J_n^0\) y como identidad en su complemento ortogonal. Por (17),
\[
\boxed{\mathcal U_{n+1}(b)J_n^0
             =J_{n+1,n}(b)\mathcal U_n(b).}
\tag{19}
\]
Ésta es una igualdad calculada. Induciendo en \(n\) también se obtiene
\(\mathcal U_n(b)\Psi_n(b_0)=\Psi_n(b)\).

La conexión
\[
\nabla^{(n)}=\mathcal U_n\,d\,\mathcal U_n^*
            =d-(d\mathcal U_n)\mathcal U_n^*
\tag{20}
\]
conserva (19), incluida su derivada:
\(\nabla^{(n+1)}J_{n+1,n}=J_{n+1,n}\nabla^{(n)}\).
Su curvatura es cero. Para comprobarlo sin asumir la conclusión, sea
\(A=(d\mathcal U_n)\mathcal U_n^*\). Diferenciar la unitariedad da
\(dA=A\wedge A\); la curvatura de \(d-A\) es
\(-dA+A\wedge A=0\).
Con una sección de acción fija, el coeficiente en la notación
\(d+(i/\hbar)H^{\rm cin}\) es
\(H^{\rm cin}=i\hbar(d\mathcal U_n)\mathcal U_n^*\), hermítico en cada
dirección real. No es por esta notación el Hamiltoniano \(h_x\).

La extensión (18) es una elección cinemática explícita de la acción en los
complementos. No se atribuye unicidad física a esa elección. Las fórmulas
(3)–(7) no dependen de haber elegido esta completación.

## 6. Límite inductivo y su alcance exacto

La torre \((\mathcal H_n,J_{n+1,n}(b))\) tiene un límite hilbertiano por
isometrías. Se puede realizar concretamente en
\(L^2(\Omega_\infty,\mu_b;E)\), restringido a la sigma-álgebra generada por
los prefijos, mediante
\[
(\iota_n(b)u)(\omega)
 =p_s(b)^{-1/2}e^{-\theta_s(b)J_E}u_s,\qquad \omega\in C_s.
\tag{21}
\]
La integral de su norma cuadrada es \(\sum_s\|u_s\|^2\).
Para \(\omega\in C_t\subset C_s\), sustituir (3) en (21) cancela
\(p_t^{1/2}\) y la fase \(\theta_t\), de modo que
\[
\iota_m(b)J_{mn}(b)=\iota_n(b).
\tag{22}
\]
Las funciones cilíndricas son densas en ese espacio (o se toma
explícitamente su clausura si se usa una realización de medida mayor).
Por tanto (21) identifica el límite, sin confundirlo con la representación
atómica \(\ell^2(X)\) del archivo nuclear09.

De (19) surge una aplicación unitaria bien definida:
\[
\mathcal U_\infty(b)\bigl(\iota_n(b_0)u\bigr)
 =\iota_n(b)\mathcal U_n(b)u.
\tag{23}
\]
Si un vector se representa en un nivel más fino, (19)–(22) producen el
mismo resultado. La isometría y la densidad de la unión prueban que (23)
se prolonga unitariamente y de forma sobreyectiva.

La conexión límite se define sobre secciones cilíndricas suaves por
\(\nabla^\infty=\mathcal U_\infty d\mathcal U_\infty^*\).
El valor y su derivada son independientes del nivel por el cuadrado
diferenciado de (19). Dos derivadas y su corchete se calculan en cualquier
nivel que contenga la sección: por (20), la curvatura es cero.
Se obtiene así planitud en el núcleo cilíndrico y transporte unitario
entre fibras por
\(\mathcal U_\infty(b_2)\mathcal U_\infty(b_1)^*\).

No se necesita uniformar en \(n\) los coeficientes de (6) para esta
afirmación sobre el núcleo y el fibrado trivializado. Eso no afirma que
dichos coeficientes definan un operador acotado en todo el límite, ni un
generador autoadjunto físico de deformaciones. Tampoco pasa (8) al límite
por una supuesta densidad de Radon–Nikodym: medidas de producto con pesos
distintos pueden ser mutuamente singulares, aunque cada nivel finito sea
equivalente. (23) es la construcción que se utiliza, no una normalización
infinita no demostrada.

El resultado es local en la carta de soporte y fases fijados. No elimina
la holonomía que un transporte físico global conserve fuera de esa carta,
ni identifica dos historias distintas por tener iguales extremos.

## 7. Comprobaciones exactas y distinción respecto de la acción total

Se ejecutaron controles con Python 3 y `fractions.Fraction`, sin coma
flotante. El test de (15) utilizó nueve componentes:
\[
a^0=(1/3,\ldots,1/3),\quad
a=(17/75,31/75,1/3,\ldots,1/3),\quad
c=223/225.
\]
Ambos vectores son unitarios y positivos. Se comprobaron exactamente
\(O^*O=I_9\), \(Oa^0=a\), la composición \(1\to9\to81\), la isometría
de las inclusiones y las 729 entradas del cuadrado recursivo (19).
Para (13), en \(p=1/9\) el coeficiente de conexión es \(1/9\) y el
coeficiente de curvatura es \(1\), no cero.
Salidas obtenidas:
`PASS_EXACT_CYLINDRICAL_TRANSPORT` y
`PASS_RECURSIVE_UNITARY_COMPLETION_INTERTWINING`.
Son controles focales racionales; no sustituyen las pruebas de arriba ni
son certificados de toda la teoría.

La realización (20) es una conexión plana **construida y tipada** desde las
amplitudes, probabilidades y fases recibidas. Prueba compatibilidad
cinemática con refinamiento y límite. El cálculo (12) evita confundirla con
la conexión de proyección sin su término compensador.

No se afirma aquí que (20) sea la conexión derivada de la acción PCH ni
que \(H^{\rm cin}\) sea el operador \(h_x\) construido en la ronda. En
particular, no se usa esta planitud para certificar la curvatura física
total. 11p tiene por objeto su realización canónica declarada, y el
archivo/reloj conservan las pruebas ya reunidas. Este desarrollo agrega
el mapa y su cálculo sin reemplazar esos objetos ni convertirlos en
obligaciones nuevas.

Propietarios de contraste de tipos, conservados:
[11p](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex>),
[archivo nuclear09 actualizado](</Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/XII_ES/nuclear/09.tex>)
y [realización hilbertiana nonádica](</Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/XII_ES/sections/01_hilbert_nonadico.tex>).

