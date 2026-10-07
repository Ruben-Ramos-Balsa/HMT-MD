# Desarrollo acumulado de la preparación de VII

Transcripción íntegra de los seis fragmentos incorporados en la copia de preparación. No agrega enunciados ni sustituye el ensamblador LaTeX; el agregado TeX es exclusivamente documental.

## 01_anuncio_resultado.tex

Ruta: `copia_vii/integracion_20260930/01_anuncio_resultado.tex`

SHA-256: `d22b4eab99607ea7bbe3bcb3d48f904078869a0b07e75836fff091d7515f2316`

```latex
% Adición al resumen de VII; no sustituye su contenido anterior.
La misma composición se prolonga a una acción total de geometría,
calibre y materia: incorpora conjuntamente la gravitación y las
interacciones fuerte, débil y electromagnética, conservando las
representaciones quirales y los acoplamientos previamente generados.
Se obtienen su corriente de espín, la fuente métrica total y los
términos torsionales cruzados entre especies. La transformación de
Legendre y las identidades de simetría producen restricciones
conjuntas de primera clase y su propagación. Sobre su superficie
regular se calcula la curvatura de la conexión canónica total y se
demuestra su anulación en las direcciones de deformación
características. El resultado conserva las condiciones de borde y
la posible holonomía global del estado enriquecido.

```

## 00_antecedentes_geometricos_materiales.tex

Ruta: `copia_vii/integracion_20260930/00_antecedentes_geometricos_materiales.tex`

SHA-256: `76cb2a12054ef14873718cf0015455c94262c53c246ef4cac8295357aa6f0b8b`

```latex
% Preparación autónoma de VII, 2026-09-30. Fragmento sin inputs adicionales.
% RESULTADOS_RECUPERADOS, pruebas reunidas sin modificación de los originales:
% /Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/29_retorno_y_memoria_traslacional.tex
% /Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30_pantalla_y_respuesta.tex
% /Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30b_variacion_energia_memoria.tex
% /Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex
% /Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30d_realizacion_geometrica.tex
% /Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex
% /Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex
% Dependencias internas ya presentes: núcleo común, rutas, lectores y unidades.
% Las inversas de 31 están demostradas en 10, hmtcuatro:gea:torsion.
% Legendre, fuente completa y restricciones permanecen en 20.
% Se incluye de 33 sólo lo utilizado por 10+20, no sus estados cosmológicos.
\section{Antecedentes geométricos y materiales de la acción conjunta}
\label{hmtcuatro:ant:seccion}

Las semillas y las operaciones de APP, la orientación y el régimen
del TRIT y el transporte del TPK producen las rutas enriquecidas sobre
las que actúan los lectores del núcleo común. Se conservan conjuntamente
hoja, orientación, acarreo, frontera y memoria; el retorno de fase no
reinicia ese estado. Las construcciones del continuo pertenecen al mismo
objeto y no se convierten aquí en sectores independientes. La
realización que sigue transporta a la geometría y a la materia esa
estructura ya construida. Sus unidades y acoplamientos son salidas
HMT anteriores: ninguna comparación numérica interviene como generador.

Para que la acción y su reducción puedan leerse dentro de este
manuscrito, reunimos las operaciones de pantalla, la variación efectiva
del transporte y la corriente espinorial que aquéllas utilizan. La
eliminación de Cartan--Holst se demuestra en
\ref{hmtcuatro:gea:torsion}; la acción total y su reducción canónica,
en \ref{hmtcuatro:accion-retroaccion-restricciones}. Las fórmulas de
esta sección especifican los datos y los cálculos que entran en ambas.

\subsection{Incidencia, pantalla y soldadura}
\label{hmtcuatro:ant:pantalla}

La representación cúbica de la frontera de una ruta tiene las seis
caras \(F=\{(i,\epsilon):1\leq i\leq3,\ \epsilon=\pm1\}\).
Sobre \(H_F=\mathbb R^F\), la oposición es
\(Re_{i,\epsilon}=e_{i,-\epsilon}\). Con
\[
 u=\sum_{i,\epsilon}e_{i,\epsilon},\qquad
 P_u=\frac{uu^{\mathsf T}}6,\qquad
 P_-=\frac{I-R}2,\qquad
 P_0=\frac{I+R}2-P_u ,
\]
los tres proyectores son ortogonales, suman \(I\) y tienen rangos
\(1,3,2\). La incidencia entre caras y vértices
\(\nu\in\{-1,1\}^3\) es
\(M_{(i,\epsilon),\nu}=\mathbf1_{\{\nu_i=\epsilon\}}\).

\begin{proposition}[Pantalla de la incidencia orientada]
\label{hmtcuatro:ant:prop-pantalla}
Se cumple
\[
 MM^{\mathsf T}=12P_u+4P_-,\qquad
 \ker M^{\mathsf T}=P_0H_F .
\]
El cociente \(Q=H_F/P_0H_F\), identificado con
\((P_u+P_-)H_F\), es de dimensión cuatro. La forma
\(B=P_--P_u\) sobre \(Q\) tiene firma \((-+++)\).
\end{proposition}
\begin{proof}
Cada cara contiene cuatro vértices; dos caras opuestas no comparten
ninguno y dos caras de ejes distintos comparten dos. Por tanto,
\[
 MM^{\mathsf T}=4I+2(uu^{\mathsf T}-I-R)
              =12P_u+4P_- .
\]
La identidad
\(\|M^{\mathsf T}x\|^2=\langle x,MM^{\mathsf T}x\rangle\)
determina el núcleo. En la base ortonormal
\[
 t=u/\sqrt6,\qquad d_i=(e_{i,+}-e_{i,-})/\sqrt2
\]
de \(Q\), la matriz de \(B\) es \(\operatorname{diag}(-1,1,1,1)\).
\end{proof}

Sea \(W_\square=\sqrt6P_u+\sqrt2P_-\). Entonces
\[
 W_\square e_{i,\epsilon}=t+\epsilon d_i=:n_{i,\epsilon},
 \qquad B(n_{i,\epsilon},n_{i,\epsilon})=0,\qquad
 MM^{\mathsf T}|_Q=2W_\square^*W_\square|_Q .
\]
Estas igualdades se obtienen aplicando los proyectores a la base de
caras. Las rotaciones propias del cubo preservan los proyectores,
la orientación temporal \(t\) y la forma \(B\).

La ruta enriquecida proporciona a cada arista \(a\) su cara,
su signo \(\sigma_m(a)\) y el transporte
\(U_m(a):Q_{s(a)}\to Q_{t(a)}\). Su soldadura celular es
\begin{equation}
 \beta_m(a)=\ell_m\sigma_m(a)n_{\lambda(\underline a)}^{s(a)},
 \quad \ell_m=\ell_0\,9^{-m},\quad
 \beta_m(\bar a)=-U_m(a)\beta_m(a).
 \label{hmtcuatro:ant:soldadura}
\end{equation}
La inversión \(U_m(\bar a)=U_m(a)^{-1}\) implica que invertir dos
veces recupera la soldadura. Se conserva además el registro ordenado
del acarreo: no se sustituye por el vector de llegada.

\begin{proposition}[Naturalidad de la soldadura]
\label{hmtcuatro:ant:refinamiento-soldadura}
Sea \(a=a_1\cdots a_9\) un refinamiento compatible: las incidencias
hijas transportadas al origen del predecesor conservan cara y signo,
y \(\ell_{m+1}=\ell_m/9\). Si
\(\mathcal U_j:Q_{m,s(a)}\to Q_{m+1,s(a_j)}\) incluye la
identificación por refinamiento y el transporte hasta \(s(a_j)\),
entonces
\[
 \beta_m(a)=\sum_{j=1}^9\mathcal U_j^{-1}\beta_{m+1}(a_j).
\]
\end{proposition}
\begin{proof}
Cada sumando en la fibra de origen es
\((\ell_m/9)\sigma_m(a)n_{\lambda(\underline a)}\). Su suma da
\eqref{hmtcuatro:ant:soldadura}. Invertir la ruta invierte el orden
de los transportes y cada transporte; la fórmula de inversión de
la soldadura da el signo global. La concatenación conserva en el
mismo orden la memoria de las nueve incidencias. La igualdad se
itera por composición de refinamientos compatibles.
\end{proof}

\subsection{Representación del transporte y realización geométrica}
\label{hmtcuatro:ant:geometria}

El registro de una ruta \(\gamma\) cuenta las inversiones y los
cambios efectivos de hoja mediante el cociclo
\(c(\gamma)=(c_g(\gamma),c_s(\gamma))\in\mathbb Z^2\).
El recuento es acumulativo en las rutas hacia adelante; su
extensión al grupoide es orientada y asigna incrementos opuestos
a la ruta inversa.
Para rutas composables,
\(c(\gamma_2\gamma_1)=c(\gamma_2)+c(\gamma_1)\), y
\(c(\bar\gamma)=-c(\gamma)\). Sea \(R_4\) un elemento de orden
cuatro en \(\operatorname{Spin}^+(3,1)\) cuya representación
vectorial \(\Lambda(R_4)\) fija el vector temporal unitario \(u_0\).
La representación afín recibida es
\[
 \rho_{\rm C}^{\rm disc}(\gamma)
 =\bigl(R_4^{c_g(\gamma)},\ell_0c_s(\gamma)u_0\bigr).
\]
Con el producto
\((R,a)(S,b)=(RS,a+\Lambda(R)b)\), la fijación de \(u_0\) y la
aditividad de \(c\) prueban directamente que \(\rho_{\rm C}^{\rm disc}\)
conserva identidad, concatenación e inversión. Cuando la componente
rotacional retorna a la identidad, la traslación de memoria permanece
determinada por \(c_s(\gamma)\), que no se reinicia.

La normalización
\[
 N_{\ell_0}(R,a)=(\Lambda(R),a/\ell_0),\qquad
 \rho_{\rm C}=N_{\ell_0}\circ\rho_{\rm C}^{\rm disc}
\]
también es un homomorfismo, pues
\((a+\Lambda(R)b)/\ell_0=a/\ell_0+\Lambda(R)(b/\ell_0)\).
El levantamiento \(R_4^{c_g(\gamma)}\) se conserva cuando actúan
espinores; no se recupera sólo a partir de \(\Lambda(R_4^{c_g(\gamma)})\),
cuya representación tiene núcleo \(\{1,-1\}\).

En una realización de pantalla \(J_{{\rm scr},m}\) que transporta
la forma y la soldadura, \(e_m=J_{{\rm scr},m}\beta_m\).
La realización suave considerada consiste en una región orientada
\(\mathcal U\) de dimensión cuatro, una cotetrada no degenerada
\(e\), una conexión de Lorentz \(\omega\) y una realización de rutas
\(\mathfrak R_{\rm C}\) con la condición de compatibilidad
\begin{equation}
 \operatorname{Hol}_{\mathcal A_{\ell_0}}
          (\mathfrak R_{\rm C}(\gamma))
 =\rho_{\rm C}(\operatorname{Hol}_{\rm TPK}(\gamma)),\qquad
 \mathcal A_{\ell_0}=
 \begin{pmatrix}\omega&\ell_0^{-1}e\\0&0\end{pmatrix}.
\label{hmtcuatro:ant:compatibilidad-holonomia}
\end{equation}
El argumento de \(\rho_{\rm C}\) conserva el cociclo de la
holonomía enriquecida; no se sustituye por su sola fase reducida.
La escala \(\ell_0>0\) es constante en la coordenatización. Éstos
son los datos y la condición de la realización suave utilizada;
preservar la composición de caminos no identifica entre sí caminos
distintos de iguales extremos ni elimina su memoria. La métrica
es \(g=\eta_{IJ}e^I\otimes e^J\), \(\eta=\operatorname{diag}(-1,1,1,1)\).

\begin{proposition}[Curvatura, covariancia y Bianchi]
\label{hmtcuatro:ant:curvatura}
Con \(F_\omega=\mathrm d\omega+\omega\wedge\omega\) y
\(T=\mathrm de+\omega\wedge e\),
\[
 \mathcal F_{\ell_0}=
 \begin{pmatrix}F_\omega&\ell_0^{-1}T\\0&0\end{pmatrix},
 \qquad D_\omega T=F_\omega\wedge e,\quad D_\omega F_\omega=0 .
\]
Un cambio de marco \(g_L:\mathcal U\to SO^+(3,1)\) actúa por
\(e'=g_Le\),
\(\omega'=g_L\omega g_L^{-1}-\mathrm dg_L\,g_L^{-1}\);
entonces \(T'=g_LT\), \(F_{\omega'}=g_LF_\omega g_L^{-1}\).
\end{proposition}
\begin{proof}
La multiplicación de matrices de formas da el bloque diagonal
\(\mathrm d\omega+\omega\wedge\omega\) y el traslacional
\(\ell_0^{-1}(\mathrm de+\omega\wedge e)\). Al sustituir los
campos transformados, los términos con \(\mathrm dg_L\) se
cancelan. Expandir \(D_\omega T\) deja
\((\mathrm d\omega+\omega\wedge\omega)\wedge e\).
En \(D_\omega F_\omega\), las derivadas de \(\omega\) y los
productos cúbicos se cancelan por pares.
\end{proof}

La hoja trítica \(\tau\in\{+1,0,-1\}\) conserva su régimen en la
realización de Cartan con generadores \(J_{ab},P_a^{(\tau)}\),
acción vectorial de Lorentz y
\([P_a^{(\tau)},P_b^{(\tau)}]=-\tau J_{ab}\). Para
\(\mathcal A_\tau=\frac12\omega^{ab}J_{ab}+\ell^{-1}e^aP_a^{(\tau)}\),
\[
 \mathcal F_\tau=
 \tfrac12(F_\omega^{ab}-\tau\ell^{-2}e^a\wedge e^b)J_{ab}
 +\ell^{-1}T^aP_a^{(\tau)} .
\]
En efecto, el corchete de Lorentz da \(F_\omega\), el mixto
da \(D_\omega e\) y el traslacional da el término
\(-\tau e\wedge e/(2\ell^2)\). La condición
\eqref{hmtcuatro:ant:compatibilidad-holonomia} corresponde a la
hoja central; las hojas extremas utilizan su representación
\(\rho_{{\rm C},\tau}\) y su condición de holonomía propias.

\subsection{Diferencial del transporte y corriente material}
\label{hmtcuatro:ant:corriente-transporte}

En una realización celular finita, sea
\(U_a:\mathcal H_{s(a)}\to\mathcal H_{t(a)}\) un transporte
invertible entre fibras hermíticas. No se presupone que todo
transporte de Lorentz sea unitario para el producto energético.
Se toma una orientación por arista. Para
\[
 (Df)_a=f_{t(a)}-U_af_{s(a)},\quad r=Df,\quad
 q=\mathsf W r,\quad v_a=U_af_{s(a)},\quad
 E=\langle r,\mathsf W r\rangle ,
\]
el peso \(\mathsf W=\mathsf W^*>0\) puede acoplar aristas.
Este peso no es \(W_\square\). Las variaciones corresponden a
la representación de la conexión y al problema de borde elegido.

\begin{proposition}[Variación completa]
\label{hmtcuatro:ant:variacion-completa}
Para una curva diferenciable de datos, con
\(A_a=\dot U_aU_a^{-1}\), se cumple
\begin{equation}
 \dot E=2\operatorname{Re}\sum_a
 \langle q_a,\dot f_{t(a)}-U_a\dot f_{s(a)}-A_av_a\rangle
 +\langle r,\dot{\mathsf W}r\rangle .
 \label{hmtcuatro:ant:variacion}
\end{equation}
A campo y peso fijos, el gradiente completo del transporte es
\(G_a=-2q_av_a^*\):
\[
 \delta_U E=\sum_a\operatorname{Re}\operatorname{Tr}(G_a^*A_a).
\]
En la subclase unitaria \(A_a^*=-A_a\), basta su parte
antihermítica \(J_a=v_aq_a^*-q_av_a^*\).
\end{proposition}
\begin{proof}
La regla del producto da
\(\dot E=2\operatorname{Re}\langle\mathsf W r,\dot r\rangle+
\langle r,\dot{\mathsf W}r\rangle\).
Derivar cada residuo produce \eqref{hmtcuatro:ant:variacion}.
Como \(\operatorname{Tr}(v_aq_a^*A_a)=q_a^*A_av_a\), se obtiene
\(G_a\). La parte hermítica de \(G_a\) es ortogonal, para
\(\operatorname{Re}\operatorname{Tr}(X^*Y)\), a las variaciones
antihermíticas. Esta reducción sólo se aplica en esa subclase.
\end{proof}

Para una ruta con \(U_\gamma=U_N\cdots U_1\), sea
\(B_k=U_N\cdots U_{k+1}\). La regla del producto demuestra
\begin{equation}
 \dot U_\gamma U_\gamma^{-1}
 =\sum_k B_kA_kB_k^{-1}.
 \label{hmtcuatro:ant:variacion-ruta}
\end{equation}
Consecuentemente un gradiente \(G_\gamma\) se transporta hacia
la arista \(k\) como
\(G_k=B_k^*G_\gamma(B_k^{-1})^*\). La ciclicidad de la traza
prueba esta fórmula incluso si \(B_k\) no es unitario.

Si las coordenadas reales de variación de conexión son
\(\theta_b\), se escribe su diferencial efectivo como
\(A_a(\theta)=\sum_b B_{ab}\theta_b\). Para
\(S_{\rm mem}=\mathfrak a E\), a campo, peso y sección de acción
\(\mathfrak a\) fijos,
\begin{equation}
 \delta S_{\rm mem}=-\tfrac12\sum_b\theta_b s_b,\qquad
 s_b=4\mathfrak a\,\operatorname{Re}
          \sum_a\langle q_a,B_{ab}v_a\rangle .
 \label{hmtcuatro:ant:corriente-celular}
\end{equation}
Sustituir \(A_a(\theta)\) en la variación demuestra la igualdad
y fija el factor \(4\). Si el emparejamiento celular orientado es
una matriz invertible \(\mathsf M\), definida por
\(\delta S_{\rm mem}=-\frac12\theta^{\mathsf T}\mathsf M\sigma\),
la corriente es \(\sigma=\mathsf M^{-1}s\). Esta matriz conserva
los volúmenes y la orientación; no puede sustituirse por una
división escalar sin fijar una base en la que corresponda.
Si también varían \(f,\mathsf W,\mathfrak a\), se conservan todos
los términos de \eqref{hmtcuatro:ant:variacion} y \(E\delta\mathfrak a\).

Para un peso por arista, su inversión conserva la respuesta completa
al transformar conjuntamente
\[
 U_{\bar a}=U_a^{-1},\qquad
 r_{\bar a}=-U_a^{-1}r_a,\qquad
 \mathsf W_{\bar a}=U_a^*\mathsf W_aU_a .
\]
La sustitución da
\(r_{\bar a}^*\mathsf W_{\bar a}r_{\bar a}=r_a^*\mathsf W_ar_a\).
Su derivada conserva necesariamente
\(\dot{\mathsf W}_{\bar a}
=U_a^*(A_a^*\mathsf W_a+\dot{\mathsf W}_a+\mathsf W_aA_a)U_a\):
eliminar este término alteraría la corriente. Si el peso acopla varias
aristas, se aplica la misma congruencia a la matriz completa con el
transporte diagonal por bloques; se conservan también sus bloques
cruzados.

\begin{proposition}[Compatibilidad variacional por refinamiento]
\label{hmtcuatro:ant:refinamiento-corriente}
Para mapas fijos \(J_m,K_m\), supóngase que, a lo largo de la
variación considerada,
\[
 D_{m+1}J_m=K_mD_m,\qquad
 K_m^*\mathsf W_{m+1}K_m=\mathsf W_m .
\]
Entonces \(E_{m+1}(J_mf)=E_m(f)\) y sus diferenciales coinciden.
Si además las acciones coinciden y \(P_m\) transporta las
variaciones de conexión al refinamiento, sus corrientes cumplen
\[
 s_m=P_m^{\mathsf T}s_{m+1},\qquad
 \mathsf M_m\sigma_m=P_m^{\mathsf T}\mathsf M_{m+1}\sigma_{m+1}.
\]
\end{proposition}
\begin{proof}
Sustituir \(D_{m+1}J_m=K_mD_m\) en la energía y después la
congruencia del peso prueba la primera igualdad para toda la
curva. Derivarla y utilizar
\(-\frac12\theta^{\mathsf T}s_m
=-\frac12(P_m\theta)^{\mathsf T}s_{m+1}\)
prueba las restantes. Si \(J_m\) varía, su diferencial aporta
\(2\operatorname{Re}\langle D_{m+1}J_mf,
\mathsf W_{m+1}D_{m+1}\dot J_m f\rangle\); no se descarta.
\end{proof}

La corriente de memoria así obtenida procede de su acción.
La corriente espinorial siguiente procede de la acción afín de
los campos. Se componen cuando son términos de una misma acción;
no se identifican sólo por compartir el transporte. En particular,
eliminar una contorsión de la que dependen también el campo
preparado, la incidencia o su mínimo exige conservar esos
diferenciales. La fórmula lineal de Cartan utilizada a continuación
corresponde al problema material afín expresamente declarado.

\subsection{Representación espinorial y corriente afín}
\label{hmtcuatro:ant:espinores}

Se fija la estructura de espín de la realización geométrica. Las
matrices heredadas, después de complejificar el módulo real, son
\begin{equation}
 \begin{gathered}
 J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
 R=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\\
 g^0=J\otimes I_2,\quad g^1=R\otimes I_2,\quad
 g^2=Z\otimes R,\quad g^3=Z\otimes Z .
 \end{gathered}
 \label{hmtcuatro:ant:clifford}
\end{equation}
Sus cuadrados son \(-I_4,I_4,I_4,I_4\) y las matrices
distintas anticonmutan. De ello se sigue
\(\{g^I,g^J\}=2\eta^{IJ}I_4\). Definimos
\[
 g_I=\eta_{IJ}g^J,\quad
 \mathbb B_{IJ}=\tfrac14[g_I,g_J],\quad
 A_D=-ig^0,\quad \bar\psi=\psi^\dagger A_D,\quad
 \Omega=\tfrac12\omega^{IJ}\mathbb B_{IJ}.
\]
La expansión del conmutador de tres matrices da
\([\mathbb B_{IJ},g^K]=\delta_J^Kg_I-\delta_I^Kg_J\).
Por tanto \(\Omega\) representa la misma conexión métrica, con
\(D\psi=\mathrm d\psi+\Omega\psi\) y
\(D\bar\psi=\mathrm d\bar\psi-\bar\psi\Omega\).
La matriz \(A_D\) es hermítica y \(A_Dg^I\) es antihermítica;
éstas fijan el adjunto y el factor de la acción en firma \((-+++)\).

Sea \(\eta_I=\iota_{E_I}\operatorname{vol}_e\), de modo que
\(e^J\wedge\eta_I=\delta_I^J\operatorname{vol}_e\). La acción afín es
\begin{equation}
 S_D=\int_M\left\{
 \frac{\hbar}{2}
 [\bar\psi g^ID\psi-(D\bar\psi)g^I\psi]\wedge\eta_I
 -mc\,\bar\psi\psi\operatorname{vol}_e\right\}.
 \label{hmtcuatro:ant:accion-dirac}
\end{equation}
La masa y las secciones positivas \(c,\hbar\) son las lecturas
recibidas, y \([\psi]=L^{-3/2}\). La notación alternativa
\(\Gamma^I=-ig^I\), con término principal
\(i\hbar\Gamma^ID_I\), cambia a la firma de Clifford opuesta;
no se mezclan ambas convenciones.

\begin{proposition}[Corriente espinorial normalizada]
\label{hmtcuatro:ant:corriente-spin}
Con \(B^{IJK}=\bar\psi g^{[I}g^Jg^{K]}\psi\), donde la
antisimetrización está normalizada, la convención
\(\delta_\omega S_D=-\frac12\int\delta\omega^{JK}\wedge\sigma_{JK}\)
da
\begin{equation}
 \sigma_{JK}
 =-\frac{\hbar}{2}\bar\psi\{g^I,\mathbb B_{JK}\}\psi\,\eta_I
 =-\frac{\hbar}{2}B^I{}_{JK}\eta_I .
 \label{hmtcuatro:ant:sigma-spin}
\end{equation}
La corriente es independiente de la contorsión al fijar \(e,\psi\).
\end{proposition}
\begin{proof}
Se tiene
\(\delta\Omega=\frac12\delta\omega^{JK}\mathbb B_{JK}\).
Los dos términos cinéticos de \eqref{hmtcuatro:ant:accion-dirac}
dan
\[
 \delta_\omega S_D=\frac{\hbar}{4}\int
 \delta\omega^{JK}\wedge\eta_I\,
          \bar\psi\{g^I,\mathbb B_{JK}\}\psi .
\]
Comparar con la convención variacional determina signo y factor.
Al desarrollar el anticonmutador mediante Clifford, las
contracciones de grado uno se cancelan y queda
\(\{g^I,\mathbb B_{JK}\}=g^{[I}g_Jg_{K]}\).
La acción es lineal en \(\Omega\), lo que prueba la independencia.
\end{proof}

Si se incluyen conexiones internas, actúan sobre el factor
material del módulo espinorial, mientras que
\(\mathbb B_{IJ}\) actúa sobre el factor de espín. Así,
\([\,\mathbb B_{IJ}\otimes I,I\otimes\rho(A)\,]=0\).
Variar \(\omega\) produce la misma fórmula, contraída sobre
las componentes internas y sumada sobre los multipletes presentes.
Esto preserva sus representaciones quirales, de color y de familia;
no añade multipletes a los ya construidos.

\subsection{Contracción torsional y cruces entre especies}
\label{hmtcuatro:ant:contraccion}

La inversión real de Cartan--Holst y de la aplicación
\(T^I\mapsto T^I\wedge e^J-e^I\wedge T^J\), demostrada en
\ref{hmtcuatro:gea:torsion}, fija sin ambigüedad la contorsión
\(\mathfrak k_*\) para la corriente afín
\eqref{hmtcuatro:ant:sigma-spin}. En esas fórmulas se conserva
\(\gamma\in\mathbb R\setminus\{0\}\), una cotetrada no degenerada
y las secciones \(G,c,\hbar,\gamma\) fijas durante la variación.
La eliminación utiliza una sola vez la interacción lineal y da
\(-\frac14\mathfrak k_*^{IJ}\wedge\sigma_{IJ}\).

\begin{theorem}[Coeficiente de la contracción espinorial]
\label{hmtcuatro:ant:coeficiente}
Sea \(\kappa=8\pi G/c^4\). La interacción efectiva es
\[
 \mathcal L_{\rm spin}^{\rm ef}
 =C_\gamma q(B)\operatorname{vol}_e,\qquad
 C_\gamma=\frac{3\kappa c\hbar^2}{16}
                    \frac{\gamma^2}{1+\gamma^2},
\]
donde
\[
 q(B)=\frac1{3!}B^{IJK}B_{IJK}
 =-(B^{012})^2-(B^{013})^2-(B^{023})^2+(B^{123})^2 .
\]
\end{theorem}
\begin{proof}
Se calcula primero
\[
 \mathcal Y^{IJ}
 =\kappa c\frac{\gamma^2}{1+\gamma^2}
       (-\star+\gamma^{-1}I)\sigma^{IJ},\quad
 \mathcal B^I=\sum_J\iota_{E_J}\mathcal Y^{IJ},\quad
 T^I=\mathcal B^I-\tfrac14e^I\wedge\sum_L\iota_{E_L}\mathcal B^L,
\]
y después
\(\mathfrak k_{IJK}=(T_{KIJ}-T_{IJK}-T_{JKI})/2\).
Estas son composiciones lineales de las inversas ya demostradas.
Para explicitar todos los coeficientes de la contracción, se
ordena el trivector como \((012,013,023,123)\) y se extrae el factor
\(\kappa c\hbar^2\gamma^2/(1+\gamma^2)\). La sustitución de
\(\sigma_{JK}/\hbar=-\frac12B^I{}_{JK}\eta_I\) en esas composiciones
y en \(-\frac14\mathfrak k^{IJ}\wedge\sigma_{IJ}\) da
\[
 \begin{array}{c|rrrr|c}
  \text{operador sobre }\sigma&012&013&023&123&
           \text{seis coeficientes de polarización}\\ \hline
  -\star&-3/16&-3/16&-3/16&3/16&0\\
  I&0&0&0&0&0
 \end{array}
\]
Cada entrada usa \(e^I\wedge\eta_J=\delta_J^I\operatorname{vol}_e\)
y las contracciones escritas arriba. Las cuatro entradas diagonales
y las seis polarizaciones enumeran la forma cuadrática completa.
La parte \(\gamma^{-1}I\) se anula y la restante es
\((3/16)q(B)\), lo que prueba la fórmula.
\end{proof}

Para varias especies, la variación se efectúa sobre su acción
común: \(\sigma=\sum_s\sigma_s\). Como la respuesta
\(\mathfrak k_*=\mathsf C_e(\sigma)\) es lineal,
\begin{equation}
 -\tfrac14\mathsf C_e\!\left(\sum_s\sigma_s\right)
       \wedge\sum_t\sigma_t
 =-\tfrac14\sum_{s,t}\mathsf C_e(\sigma_s)\wedge\sigma_t .
 \label{hmtcuatro:ant:cruces-especies}
\end{equation}
Esta expansión demuestra que los términos \(s\ne t\) permanecen.
Calcular respuestas separadas y conservar sólo \(s=t\) cambiaría
la acción total.

\subsection{Orden normal de la corriente total}
\label{hmtcuatro:ant:car}

En la realización fermiónica finita de una celda se utiliza
\(\mathcal F=\bigoplus_n\Lambda^n V\), con las relaciones
\(\{a_r,a_s^\dagger\}=\delta_{rs}\), \(\{a_r,a_s\}=0\) y el
vacío de ocupación como referencia del orden normal.
Escribimos \(d\Gamma(M)=\sum_{r,s}a_r^\dagger M_{rs}a_s\);
esta \(\Gamma\) denota segunda cuantización, no la holonomía nonádica.
Para el módulo espinorial de cuatro componentes, las matrices son
\[
 \begin{array}{c|cccc}
 abc&012&013&023&123\\ \hline
 M_{abc}=A_Dg^ag^bg^c&
 iJ\otimes R&iJ\otimes Z&iI_2\otimes J&iZ\otimes J
 \end{array}.
\]
Multiplicar \eqref{hmtcuatro:ant:clifford} da estas matrices;
son hermíticas, de traza cero y cuadrado \(I_4\).

\begin{proposition}[Contracción normal y conservación de los cruces]
\label{hmtcuatro:ant:orden-normal}
Para toda matriz \(M\),
\[
 :d\Gamma(M)^2:
 =d\Gamma(M)^2-d\Gamma(M^2).
\]
En el módulo de cuatro componentes,
\[
 \widehat{\mathscr Q}_{\rm sp}
 =\sum_{a=1}^4s_a d\Gamma(M_a)^2+2\widehat N,
 \qquad s=(-1,-1,-1,+1),\quad \widehat N=d\Gamma(I_4).
\]
El operador es autoadjunto y conserva la ocupación.
En una suma de multipletes se emplea la misma primera identidad
con las matrices totales \(\widetilde M_a\); se conservan las
contracciones entre especies.
\end{proposition}
\begin{proof}
En \(d\Gamma(M)^2\), la relación
\(a_sa_t^\dagger=\delta_{st}-a_t^\dagger a_s\) separa la
contracción \(d\Gamma(M^2)\) del término con dos creadores y
dos aniquiladores. Este último es, por definición, el producto
normal. Como \(M_a^2=I_4\) y \(\sum_a s_a=-2\), la sustracción
de contracciones vale \(+2\widehat N\). La hermiticidad de las
matrices hace autoadjuntos los sumandos y cada monomio conserva
la ocupación.

Si \(\widetilde M=\bigoplus_s M_s\), entonces
\(d\Gamma(\widetilde M)=\sum_s d\Gamma(M_s)\) y
\(d\Gamma(\widetilde M^2)=\sum_s d\Gamma(M_s^2)\).
Los bilineales de multipletes distintos conmutan; al elevar la
primera suma al cuadrado quedan
\(2d\Gamma(M_s)d\Gamma(M_t)\) para \(s<t\). La sustracción de
una ocupación no elimina estos cruces. Es la versión operatoria
de \eqref{hmtcuatro:ant:cruces-especies}.
\end{proof}

La invariancia bajo los cambios unitarios internos se obtiene
porque éstos actúan sobre los índices materiales y entrelazan las
matrices de corriente: la segunda cuantización transporta la
fórmula completa por conjugación. La densidad y su evaluación
sobre un estado utilizan, además, el volumen de la celda y el
estado material declarados. No se identifican la corriente media
y su segundo momento. Estos datos completan los antecedentes
utilizados por la acción conjunta, sin introducir una segunda
eliminación de torsión ni modificar sus condiciones de borde.
```

## 02_color_y_representacion_interna.tex

Ruta: `copia_vii/integracion_20260930/02_color_y_representacion_interna.tex`

SHA-256: `ff30bdcc295e196e7581a833722abb6753f35758c258718dbd8d11fd9ac814e6`

```latex
% Preparación separada del 30-09-2026; no modifica manuscritos publicados.
% Propietarios: VI_ES/sections/04_atlas_familias.tex:140--163;
% md/04d_ocupacion_estadistica.tex:305--319;
% md/06e_color_qutrit_gauge_finito.tex:1--194.
% Carta qutrit y forma compacta recibidas con sus hipótesis explícitas.
% Inserción: después de 00_antecedentes_geometricos_materiales y antes de 10.
\section{Residuo cromático y representación interna de la acción conjunta}
\label{hmtcuatro:color:seccion}

La cadena APP--TRIT--TPK conserva el estado enriquecido, sus rutas,
orientaciones, hojas y memoria dentro de la estructura discreta conjunta
del continuo. El residuo que se lee a continuación es una publicación
finita de ese estado; no lo sustituye ni reinicia su historia. Las
coordenadas de fase, incluida la unidad compleja y la coordenada regional
\(\pi\), son salidas HMT recibidas antes de esta realización algebraica.
La representación se construye sobre el soporte residual con la carta,
la orientación y el carácter de fase declarados. No se infiere un grupo
de calibre a partir del solo número de etiquetas.

\subsection{Soporte residual y orientación conservada}
\label{hmtcuatro:color:residuo}

En la copia posicional de APP, sean
\[
 I_9=\{1,\ldots,9\},\qquad
 \mathcal C=I_9\times I_9,\qquad
 \mathcal C_q=\{(r,c)\in\mathcal C:r\text{ es par}\}.
\]
El observable residual y la inversión celular son
\[
 \kappa_{\rm col}(r,c)=r-c\pmod3,\qquad
 \rho_{\rm c}(r,c)=(10-r,10-c).
\]
El símbolo \(\kappa_{\rm col}\) no designa el coeficiente gravitatorio
de la acción. La elevación de este observable a las secciones
persistentes se efectúa por la proyección al atlas y conserva los
restantes registros; no selecciona una celda por su masa evaluada.

\begin{proposition}[Fibras ternarias y balance cromático]
\label{hmtcuatro:color:balance}
El funcional \(\kappa_3:\mathbb F_3^2\to\mathbb F_3\),
\(\kappa_3(r,c)=r-c\), tiene tres fibras afines de cardinal tres.
Sobre \(\mathcal C_q\), los tres residuos tienen cardinales
\(12,12,12\). La inversión celular niega el residuo.
\end{proposition}
\begin{proof}
Para cada \(j\in\mathbb F_3\), la fibra es
\(\{(c+j,c):c\in\mathbb F_3\}\), una traslación del núcleo
\(\{(c,c)\}\). En \(\mathcal C_q\) existen cuatro valores pares
de \(r\); para cada uno, \(c=1,\ldots,9\) recorre tres veces
cada clase módulo tres. Cada residuo posee \(4\cdot3=12\)
representantes. Finalmente,
\[
 \kappa_{\rm col}(\rho_{\rm c}(r,c))
 =(10-r)-(10-c)=-(r-c)\pmod3.
\]
La clase cero queda fija y las clases uno y dos se intercambian.
\end{proof}

Este balance no identifica sabor, profundidad y color. Tampoco afirma
que las tres rectas que se construirán sean tres estados completos:
las rutas y la memoria que comparten una lectura residual permanecen
en la fibra enriquecida.

\subsection{Carta qutrit, par de Weyl y álgebra de color}
\label{hmtcuatro:color:weyl}

Se fija la carta
\[
 V_{\rm col}=\mathbb C[\mathbb F_3]\simeq\mathbb C^3,
 \qquad (e_0,e_1,e_2),\qquad
 \omega_3=e^{2\pi i/3},
\]
con base delta ortonormal, orientación \(j\mapsto j+1\) y carácter
\(j\mapsto\omega_3^j\). Los operadores son
\[
 Xe_j=e_{j+1\bmod3},\qquad Ze_j=\omega_3^j e_j,
 \qquad X^3=Z^3=I,\quad ZX=\omega_3XZ.
\]
La última igualdad se comprueba aplicando ambos miembros a cada
\(e_j\). La aplicación del atlas a esta carta es
\[
 (r,c)\longmapsto\mathbb C e_{\kappa_{\rm col}(r,c)}.
\]
Así, \(X\) permuta las rectas y \(Z\) registra sus fases. Cambiar
la carta afín y transportar conjuntamente base, orientación y carácter
conjuga los operadores por la correspondiente matriz unitaria de
cambio de base. No equivale a cambiar sólo una etiqueta y dejar fijos
los demás datos.

\begin{theorem}[Álgebra matricial y forma real compacta]
\label{hmtcuatro:color:algebra}
Los nueve operadores \(W_{ab}=X^aZ^b\),
\((a,b)\in\mathbb F_3^2\), forman una base ortogonal de
\(\operatorname{End}_{\mathbb C}(V_{\rm col})\). Los ocho índices
no nulos generan linealmente \(\mathfrak{sl}_3(\mathbb C)\), cuya
forma real de matrices antihermíticas es \(\mathfrak{su}(3)\).
\end{theorem}
\begin{proof}
Si \(a\ne0\), la matriz \(X^aZ^b\) no tiene entradas diagonales.
Si \(a=0\), su traza es \(1+\omega_3^b+\omega_3^{2b}\), que
vale cero para \(b\ne0\) y tres para \(b=0\). La relación de
Weyl da entonces
\[
 \operatorname{tr}(W_{ab}^{\dagger}W_{cd})
 =3\delta_{ac}\delta_{bd}.
\]
La independencia y la dimensión nueve prueban la primera afirmación;
los ocho restantes forman la base del subespacio de traza cero.
Además,
\[
 W_{ab}^{\dagger}=\omega_3^{ab}W_{-a,-b}.
\]
Los ocho índices no nulos forman cuatro pares adjuntos. Tomando
\(\mathcal R=\{(1,0),(0,1),(1,1),(1,2)\}\), las matrices
\[
 A_u=W_u-W_u^{\dagger},\qquad
 B_u=i(W_u+W_u^{\dagger}),\qquad u\in\mathcal R,
\]
son antihermíticas y de traza cero. Su independencia real se deduce
de la independencia compleja de los ocho \(W_u,W_{-u}\): en cada
par, los coeficientes de una combinación real nula fuerzan a cero
los dos coeficientes reales. Forman una base real de dimensión ocho.
Por tanto,
\[
 \{A\in\mathfrak{sl}_3(\mathbb C):-A^{\dagger}=A\}
 =\mathfrak{su}(3).
\]
\end{proof}

La forma hermítica y la orientación compleja fijadas determinan el
grupo de realización
\[
 SU(V_{\rm col})=\{U:U^{\dagger}U=I,\ \det U=1\}.
\]
Su álgebra tangente es exactamente la anterior: diferenciar ambas
ecuaciones en la identidad da \(A^{\dagger}=-A\) y
\(\operatorname{tr}A=0\); recíprocamente, \(e^{tA}\) satisface
ambas. Todo elemento del grupo se escribe como exponencial de una
matriz de esa álgebra. En efecto, diagonalícese unitariamente \(U\)
con autovalores \(e^{i\theta_j}\); como el determinante es uno,
\(\sum_j\theta_j=2\pi n\). Restar \(2\pi n\) a uno de los
ángulos no altera \(U\) y produce un logaritmo antihermítico de
traza cero. Esta realización continua no se identifica con el grupo
finito generado únicamente por \(X,Z\). Conserva la forma compacta
y no introduce un valor para el acoplamiento fuerte.

\subsection{Transporte cromático y factores internos independientes}
\label{hmtcuatro:color:transporte}

En una celularización finita orientada compatible con las rutas,
se asignan \(U_e\in SU(V_{\rm col})\) y
\(U_{\bar e}=U_e^{-1}\). Para \(g_v\in SU(V_{\rm col})\),
\[
 U_e^g=g_{t(e)}U_eg_{s(e)}^{-1},\qquad
 \psi_v^g=g_v\psi_v.
\]
Por sustitución,
\[
 U_e^g\psi_{s(e)}^g-\psi_{t(e)}^g
 =g_{t(e)}(U_e\psi_{s(e)}-\psi_{t(e)}).
\]
El signo opuesto, utilizado en \(D_T\), tiene la misma covariancia.
La transformación de un producto orientado alrededor de una cara
es conjugación por el calibre del vértice base: los factores de
los vértices intermedios se cancelan consecutivamente. En particular,
para \(\beta\ge0\),
\[
 S_{\rm col}^{(\mathcal K,\beta)}[U]
 =\frac\beta3\sum_f(3-\operatorname{Re}\operatorname{tr}U_f)
\]
es invariante y no negativa. La invariancia usa la traza cíclica;
la positividad resulta de \(\operatorname{Re}\operatorname{tr}U_f\le3\).
El parámetro y la celularización conservan su condición de datos de
esta realización. Esta prueba no los determina por comparación con
valores cromodinámicos.

La materia de la acción conjunta utiliza este factor, no otra
partición del atlas. Para los quarks izquierdos, su fibra interna
tiene factores \(V_{\rm col}\otimes\mathbb C^2\otimes F\),
donde \(F\) conserva las familias; para cada tipo derecho se usa
\(V_{\rm col}\otimes F\). El factor de color es trivial en los
leptones. El factor espinorial se conserva aparte. Para matrices
\(A\) de color y \(B\) débiles se cumple
\[
 [A\otimes I,I\otimes B]=0,
\]
pues los dos productos son \(A\otimes B\). Los caracteres de
hipercarga actúan como escalares sobre cada multiplete y también
conmutan. Esta identidad permite componer las conexiones internas
y la de espín en la misma derivada sin confundir color, quiralidad
y sabor.

Los mapas Yukawa de la acción posterior son la identidad en el
factor cromático y mapas en los factores Higgs--familia. Por ello
\(Y_q(H)(g_{\rm col}\otimes I)
=(g_{\rm col}\otimes I)Y_q(H)\). La compatibilidad débil y de
hipercarga se demuestra allí con sus columnas y sus pesos explícitos;
no se obtiene del censo \(12+12+12\).
Así se conserva la cadena residual--qutrit--álgebra--transporte
que requiere la acción común, sin afirmar en este antecedente un
límite cuántico de Yang--Mills ni reemplazar sus propietarios.
```

## 10_gravedad_energia_autoinercia.tex

Ruta: `copia_vii/integracion_20260930/10_gravedad_energia_autoinercia.tex`

SHA-256: `90b7ceeb233b87aaa71ba0a9a403d27cabb7ef6b2942397ad78b509f1e7d7b8d`

```latex
% Fragmento integrable en VII: Relaciones estructurales entre las constantes físicas.
% Insertar después de desarrollos/normalizacion_conjunta.tex.
% Fuentes y cobertura íntegra: editorial/INSERCION_VII.md.
% Sin preámbulo ni macros; usa amsmath y los entornos ya definidos por VII.
\section{Gravedad, energía y autoinercia del sistema conjunto}
\label{hmtcuatro:gea:seccion}

La normalización conjunta permite formular una pregunta operatoria:
cómo intervienen la geometría, la materia y la memoria en una misma
realización. Se reúnen tres enlaces. El carácter positivo conserva
simultáneamente sus lecturas energética, másica y radial; la variación
del transporte conjunto produce corrientes geométricas e internas de
una misma energía; y la respuesta autoinercial se expresa mediante el
radio gravitatorio de ese carácter. Se demuestran la conservación de
estos enlaces bajo reducción de memoria y la propagación de las
restricciones de la acción acoplada durante su evolución regular.

El antecedente es el núcleo común del artículo. APP produce las dos
hojas con sus residuos, cocientes e incidencias; TRIT conserva régimen
y orientación: $+1$ corresponde a retorno y memoria, $0$ al umbral
presente y $-1$ a apertura. TPK selecciona, transporta, pliega, retorna
y conserva el estado enriquecido y su historia. La prolongación
$w_6\to w_{12}\to w_{18}\to w_{24}\to w_{30}\to R_{36}\to G_9$
mantiene prefijo, acarreo, supervivencia, ruta y frontera. La dinámica,
su holonomía nonádica y la publicación reducida tienen el orden
$U_t\to\Gamma_9\to K_{\rm ph}$: retorna la fase, avanza la memoria
y no se reinicia el estado. Las cinco construcciones consustanciales
de la estructura discreta del continuo no se separan al realizar sus lectores.

Las constantes y escalas empleadas son salidas de esta genealogía.
La cuadrirrelación $(\pi,\varphi,e,\alpha)$ conserva su origen común
y su orden constructivo interno; acción, velocidad constitutiva y
Barbero--Immirzi se reciben con sus lectores. El lenguaje operatorio
y variacional compone y reconoce esas salidas, sin introducir valores
metrológicos para seleccionar estados o coeficientes.

\subsection{Energía, masa y radio del mismo carácter}
\label{hmtcuatro:gea:caracter}

Se conserva la realización marcada de la sección anterior:
\[
\Omega=\{(j,k,q,u,v):j,k\in\mathbb Z/12\mathbb Z,\ 
k-j\in\{0,3,6,9\},\ 1\leq q\leq8,\ 
u<v,\ u,v\in\{1,2,4,5,7,8\}\}.
\]
Su cardinal $N_\Omega=12\cdot4\cdot8\binom62=5760$ cuenta incidencias,
no estados de materia ni lapsos. Para el inversor transportado
$B:V_{\rm in}\to V_{\rm out}$, con $B^*B=BB^*=I/4$, el proyector
$P=uu^*$ del modo común tiene $|u_i|^2=1/N_\Omega$. El archivo retiene
\[
C_0=(I-P)B,\qquad M_0=PB,\qquad C_0+M_0=B,\qquad\mathsf U=2B.
\]
Las imágenes de $C_0,M_0$ son ortogonales y $\mathsf U$ es unitario.
La expectativa marcada $\Delta_\Omega(A)=\sum_iP_iAP_i$,
$P_i=e_ie_i^*$, es única entre las expectativas bimodulares hacia
el álgebra diagonal que fijan los $P_i$: sobre una unidad matricial,
la bimodularidad exige
$\mathcal E(E_{ij})=P_i\mathcal E(E_{ij})P_j$, que es cero si $i\ne j$
y vale $E_{ii}$ si $i=j$.

De $C_0C_0^*=(I-P)/4$ y $P_iPP_i=P_i/N_\Omega$ resulta
\begin{equation}
\Delta_\Omega(C_0C_0^*)=r_\Omega I,\qquad
\Delta_\Omega(M_0M_0^*)=\frac{I}{4N_\Omega},\qquad
r_\Omega=\frac{5759}{23040}.
\label{hmtcuatro:gea:retorno}
\end{equation}
Ambas lecturas suman $I/4$. La regla constitutiva longitudinal aplica
linealmente el primer coeficiente a una sección de longitud:
\begin{equation}
L=\alpha^{16}r_\Omega L_*,\qquad D=L\mathsf U.
\label{hmtcuatro:gea:longitud}
\end{equation}
La norma local $\alpha^{16}$ y la sección $L_*$ son antecedentes
explícitos; tomar una raíz de intensidad sería otro lector.
La regla métrica radial es $\|R_Xv\|^2=\|XD^*v\|^2$.
Para $X=X^*>0$ en la fibra finita, la polarización y la raíz positiva
única dan $R_X^2=DX^2D^*=L^2\mathsf UX^2\mathsf U^*$ y
$R_X=LY$, con $Y=\mathsf UX\mathsf U^*>0$.
El espectro no se selecciona a partir de una respuesta gravitatoria deseada.

La misma sección $\hbar>0$ y el reloj conjugado $\omega L=c$
determinan $E_L=\hbar c/L$ y los lectores
\begin{equation}
H_X=E_LY,\qquad M_X=H_X/c^2,\qquad
R_X=LY,\qquad\Lambda_X=LY^{-1}.
\label{hmtcuatro:gea:lectores}
\end{equation}
La notación $H_X$ queda reservada a este lector del carácter.
El Hamiltoniano conjunto $\mathbb H$ introducido después tiene otro
dominio y no se identifica con $H_X$ por compartir el nombre de energía.

\begin{proposition}[Coeficiente radial común]
\label{hmtcuatro:gea:coeficiente}
En la identificación explícita de $R_X$ como radio gravitatorio reducido,
$R_X=GM_X/c^2$, existe un único coeficiente compatible:
\begin{equation}
G=\frac{c^3L^2}{\hbar},\qquad
R_X=\frac{G}{c^4}H_X=\frac{G}{c^2}M_X,\qquad
R_X\Lambda_X=L^2I,\quad H_X\Lambda_X=\hbar cI.
\label{hmtcuatro:gea:radial}
\end{equation}
\end{proposition}
\begin{proof}
Multiplicar los lectores prueba los dos productos. La identificación
radial equivale a $LY=G\hbar Y/(c^3L)$.
Cancelar el carácter invertible determina $G$; la sustitución inversa
verifica la igualdad para cada carácter positivo. Si dos coeficientes
la satisfacen, su diferencia multiplicada por $Y$ es cero y ambos coinciden.
\end{proof}

Las reglas longitudinal y métrica fijan la realización; la convención
de radio reducido fija el significado físico de $G$. El radio
Schwarzschild de la misma masa es $2R_X$. La igualdad conserva
superposiciones y elementos no diagonales en cualquier base transportada,
no sólo valores medios. Para una familia diferenciable y una conexión
de marco común $\mathcal A_t$, con $G,c$ fijos,
\begin{equation}
\mathcal D_tR_X=\frac{G}{c^4}\mathcal D_tH_X,\qquad
\mathcal D_tM_X=c^{-2}\mathcal D_tH_X,\qquad
\mathcal D_tO=\dot O+[\mathcal A_t,O].
\label{hmtcuatro:gea:derivada}
\end{equation}
Se obtiene diferenciando la identidad completa, incluido el marco.
No implica inmovilidad del estado.

Para modos positivos, o para operadores en factores tensoriales distintos,
\begin{equation}
m(y)=\frac{\hbar}{cL}y,\qquad
\frac{Gm_1m_2}{\hbar c}=y_1y_2,\qquad
\frac{R(y)}{\bar\lambda(y)}=y^2,\quad \bar\lambda(y)=L/y.
\label{hmtcuatro:gea:adimensional}
\end{equation}
La sustitución cancela las secciones dimensionales; los operadores en
factores distintos conmutan. El tamaño adimensional depende del carácter,
sin otro parámetro libre por especie. No se deduce de ello una ley
espacial de fuerza ni una evaluación numérica sin evaluar el carácter.

El calendario conserva $t_P=L/c$, $t_0=\pi L/(54c)$ y
$108t_0=2\pi t_P$. Por tanto $L=(54/\pi)\ell_0$, con $\ell_0=ct_0$;
las dos longitudes no se identifican. Entre secciones
$\hbar_b=\rho\hbar_a$, $\rho>0$, con $L,c,y_i$ fijos, se tiene
$G_b=G_a/\rho$, $m_{i,b}=\rho m_{i,a}$ y la cantidad
$Gm_1m_2/(\hbar c)$ permanece invariante. Se comparan secciones
conjuntas, no una variación temporal con las demás coordenadas
dimensionales mantenidas artificialmente fijas.

\subsection{Memoria estática, dinámica y dominio espectral}
\label{hmtcuatro:gea:memoria}

En dimensión finita, o con bloques acotados y coercivos, escribamos
\[
Y=\begin{pmatrix}A&F\\F^*&C\end{pmatrix}>0,\quad
Y_{\rm ef}=A-FC^{-1}F^*,\quad \eta=y+C^{-1}F^*b.
\]
Completar el cuadrado demuestra
\begin{equation}
\left\langle\binom b y,Y\binom b y\right\rangle
=\langle b,Y_{\rm ef}b\rangle+\langle\eta,C\eta\rangle.
\label{hmtcuatro:gea:schur-prueba}
\end{equation}
De aquí $Y_{\rm ef}>0$, la extensión minimizante
$y=-C^{-1}F^*b$ y la reconstrucción $y=\eta-C^{-1}F^*b$.
El residuo $\eta$ se conserva. Como
$\operatorname{Schur}(sY)=sY_{\rm ef}$ para $s>0$, se obtienen
$H_{X,\rm ef}=E_LY_{\rm ef}$ y $R_{X,\rm ef}=LY_{\rm ef}$.
Resolver $Y(x,y)=(f,0)$ muestra que el bloque de frontera de $Y^{-1}$
es $Y_{\rm ef}^{-1}$, luego $\Lambda_b=LY_{\rm ef}^{-1}$.
La compresión directa de $Y$ daría $A$: no es la misma operación.

Sea $\chi=L/E_L=G/c^4>0$ y $R_X=\chi H_X$.
En una descomposición compatible con los dominios, definimos
\[
\mathcal K_{H_X}(z)=H_{bb}-zI-V(H_{ii}-zI)^{-1}V^*.
\]
\begin{proposition}[Memoria dinámica completa]
\label{hmtcuatro:gea:resolvente-prop}
En el dominio resolvente del bloque interior,
\begin{equation}
\mathcal K_{R_X}(\chi z)=\chi\mathcal K_{H_X}(z).
\label{hmtcuatro:gea:resolvente}
\end{equation}
Si ambos complementos son invertibles, sus inversas llevan el factor
$\chi^{-1}$.
\end{proposition}
\begin{proof}
Cada bloque radial es $\chi$ veces el energético y
$(\chi H_{ii}-\chi zI)^{-1}=\chi^{-1}(H_{ii}-zI)^{-1}$.
La sustitución deja un factor $\chi$ en cada término, conservando el
orden. Invertir prueba la última afirmación.
\end{proof}
El parámetro energético $z$ se transporta a la longitud $\chi z$;
la identidad conserva cada orden de memoria espectral.
Para $|z|<\|H_{ii}^{-1}\|^{-1}$, la serie del resolvente da
\[
\mathcal K_{H_X}(z)=H_{\rm est}-zZ+O(z^2),\quad
H_{\rm est}=H_{bb}-VH_{ii}^{-1}V^*,\quad
Z=I+VH_{ii}^{-2}V^*\geq I.
\]
La positividad sigue de
$Z-I=(H_{ii}^{-1}V^*)^*(H_{ii}^{-1}V^*)$.
La extensión estática $(b,-H_{ii}^{-1}V^*b)$ tiene norma cuadrada
$\langle b,Zb\rangle$: energía y norma temporal proceden de la misma extensión.

Si $T=Z^{1/2}$ es acotado e invertible, el transporte es dual:
\begin{equation}
H_{X,c}=T^{-*}H_{X,\rm ef}T^{-1},\quad
R_{X,c}=T^{-*}R_{X,\rm ef}T^{-1},\quad
\Lambda_c=T\Lambda_bT^*.
\label{hmtcuatro:gea:dual}
\end{equation}
Multiplicar prueba $R_{X,c}=\chi H_{X,c}$,
$R_{X,c}\Lambda_c=L^2I$ y $H_{X,c}\Lambda_c=\hbar cI$,
sin conmutatividad de $T$ con el carácter.
Si $\psi=T(t)b$, se conserva $\dot\psi=\dot Tb+T\dot b$.
El término temporal de conexión del generador no se incorpora
retrospectivamente al carácter radial sin declarar su mapa.

\begin{proposition}[Extensión espectral y refinamiento compatible]
\label{hmtcuatro:gea:limite}
Sea $X$ autoadjunto, positivo e inyectivo, y $\mathsf U$ unitario.
Los lectores de \eqref{hmtcuatro:gea:lectores}, definidos por cálculo
espectral de $Y=\mathsf UX\mathsf U^*$, satisfacen
$R_X=\chi H_X$ en $\operatorname{Dom}(Y)$.
Sus productos con $\Lambda_X$ valen en $\operatorname{Dom}(Y^{-1})$
y tienen las prolongaciones acotadas de \eqref{hmtcuatro:gea:radial}.
Si inscripciones isométricas satisfacen $X'J=JX$,
$\mathsf U'J=K\mathsf U$ y conservan $L,E_L$, entonces
$R'_XK=KR_X$ y $H'_XK=KH_X$ en los dominios transportados.
\end{proposition}
\begin{proof}
Sobre $P_{\varepsilon,M}=\mathbf1_{[\varepsilon,M]}(Y)$, lectores e
inversos son acotados y las identidades son multiplicaciones de
funciones de $Y$. Para $\psi\in\operatorname{Dom}(Y)$,
\[
\|Y(P_{\varepsilon,M}-I)\psi\|^2
=\int_{(0,\infty)\setminus[\varepsilon,M]}
\lambda^2\,d\langle\psi,E_Y(\lambda)\psi\rangle\longrightarrow0.
\]
La inyectividad elimina masa espectral en cero y también
$P_{\varepsilon,M}\psi\to\psi$. Es convergencia en norma de grafo.
Si $\psi\in\operatorname{Dom}(Y^{-1})$, entonces
$Y^{-1}\psi\in\operatorname{Dom}(Y)$ y $YY^{-1}\psi=\psi$,
lo que prueba los productos y sus prolongaciones.
Sustituir los entrelazamientos en $R'_X=L\mathsf U'X'\mathsf U'^*$
prueba $R'_XK=KR_X$; la cuenta energética es igual.
\end{proof}
El sector nulo permanece separado. Se precisa así la extensión no
acotada de la normalización anterior. Una proyección ortogonal
arbitraria no queda habilitada para las fórmulas de bloques:
en operadores no acotados se requieren dominios compatibles o formas
cerradas con bloques controlados.

\subsection{Retroacción en el mismo transporte}
\label{hmtcuatro:gea:retroaccion}

El registro geométrico $x$, los enlaces internos $u$ y los campos $f$
proceden del mismo estado enriquecido. En una celularización orientada,
\begin{equation}
E(f,x,u)=\langle r,W(x,u)r\rangle,\quad r=D_Tf,\quad
(D_Tf)_a=f_{t(a)}-T_af_{s(a)},\quad
T_a=U_a^{\rm sp}(x)\otimes R_{\rm int}(u_a).
\label{hmtcuatro:gea:energia-memoria}
\end{equation}
$W=W^*>0$ conserva los bloques entre incidencias. Espín y
representación interna tienen factores distintos; la realización
quiral conserva sus bloques y el mapa Higgs--Yukawa equivariante.

\begin{proposition}[Diferencial de una misma energía]
\label{hmtcuatro:gea:variacion}
Con campos fijos y $q=Wr$,
\begin{align}
\delta E&=-2\operatorname{Re}\sum_a
\langle q_a,\delta T_af_{s(a)}\rangle+\langle r,\delta Wr\rangle,
\label{hmtcuatro:gea:diferencial}\\
\delta T_a&=\delta U_a^{\rm sp}\otimes R_{\rm int}(u_a)
+U_a^{\rm sp}\otimes\delta R_{\rm int}(u_a).\nonumber
\end{align}
\end{proposition}
\begin{proof}
Derivar la forma cuadrática da dos términos conjugados por
$W=W^*$ y el término $\langle r,\delta Wr\rangle$.
Usar $\delta r_a=-\delta T_af_{s(a)}$ prueba la primera fórmula;
la regla del producto prueba la segunda.
Ambas variaciones actúan sobre los mismos $r,q$, sin corrientes
elegidas independientemente.
\end{proof}

\subsubsection{Un espacio cuántico y un operador conjunto}
\label{hmtcuatro:gea:cuantica}

Se fija una celularización finita, un conjunto finito de registros
geométricos $\mathcal X$ y una Fock fermiónica finita $\mathcal F$.
Los enlaces recorren el producto compacto $\mathcal G^E$ recibido;
los dobletes $\Phi_v\in\mathbb C^2$ no tienen corte de amplitud.
Las medidas invariantes $d\mu_x=Z_x^{-1}e^{-S_x}d\mu_0$ tienen
densidades positivas acotadas con inversa acotada y no dependen de
$\Phi$ en esta carta. El espacio es
\[
\mathscr H=\bigoplus_{x\in\mathcal X}
L^2(\mathcal G^E\times\mathbb C^{2|V|},
\mu_x\otimes d\Phi;\mathcal F).
\]
Las identificaciones $A_xf=\sqrt{Z_x}e^{S_x/2}f$ son unitarias
desde la medida común y transportan el reloj a
$H_{\rm clk}^{\mu}=A(H_{\rm clk}\otimes I)A^*$.
El reloj mezcla registros geométricos del mismo espacio.
El operador se realiza mediante la forma de
\begin{equation}
\mathbb H=H_{\rm clk}^{\mu}+\hbar cK_{\rm gauge}
+d\Gamma(D_T^*WD_T)+H_{\Phi,\rm cin}+V_\Phi
+\widehat H_Y+\widehat H_{\rm tor}.
\label{hmtcuatro:gea:total}
\end{equation}
El mapa Yukawa es lineal en $\Phi,\bar\Phi$ y satisface
$Y(g\Phi)\rho_R(g)=\rho_L(g)Y(\Phi)$.
La contorsión eliminada no se conserva simultáneamente como variable
independiente en los términos base de esta carta efectiva.

La cinética de momentos escalares tiene forma
$\int\langle\nabla_\Phi\Psi,A(x,u)\nabla_\Phi\Psi\rangle$,
con $A$ acotada, uniformemente positiva e independiente de $\Phi$.
Se exige $A(x,u^g)=O_gA(x,u)O_g^{\mathsf T}$ para la acción real
$O_g$ de los dobletes; positividad sola no prueba esa covarianza.
La energía espacial escalar es un potencial cuadrático positivo
acotado por $C_{\rm grad}r^2$, $r^2=\sum_v|\Phi_v|^2$,
no un operador acotado sobre todo $L^2$.
Los volúmenes satisfacen
$0<w_{\min}\leq w_v(x)\leq w_{\max}$ y $\lambda_\Phi>0$.
Reloj, bloque gauge, transportes, $W$ y coeficientes torsionales
son acotados en la carta. El potencial conserva su valor absoluto:
\begin{equation}
V_\Phi=\sum_vw_v\lambda_\Phi(|\Phi_v|^2-v_0^2/2)^2
-\sum_vw_v\lambda_\Phi v_0^4/4.
\label{hmtcuatro:gea:potencial}
\end{equation}
La última contribución depende del volumen y no se sustrae.

\begin{theorem}[Forma cerrada y evolución conjunta]
\label{hmtcuatro:gea:forma}
La forma de \eqref{hmtcuatro:gea:total} es cerrada y acotada
inferiormente en
$\mathcal Q=\{\Psi\in\mathscr H:\nabla_\Phi\Psi\in L^2,\
r^2\Psi\in L^2\}$.
Determina un único operador autoadjunto asociado $\mathbb H$
y la evolución unitaria $e^{-it\mathbb H/\hbar}$.
\end{theorem}
\begin{proof}
Cauchy--Schwarz da
$\sum_vw_v\lambda_\Phi|\Phi_v|^4\geq ar^4$,
$a=\lambda_\Phi w_{\min}/|V|>0$.
Fock finita y Yukawa lineal dan
$\|\widehat H_Y(\Phi)\|\leq C_Yr$; la torsión está acotada.
Para $\varepsilon>0$,
\[
C_Yr\leq\varepsilon r^4+
\frac{3C_Y^{4/3}}{4^{4/3}\varepsilon^{1/3}},\qquad
br^2\leq\varepsilon r^4+\frac{b^2}{4\varepsilon}.
\]
La primera cota maximiza $C_Yr-\varepsilon r^4$; la segunda
completa el cuadrado en $r^2$. Aplicarlas con $\varepsilon=a/4$
a Yukawa y al cuadrático negativo da
\[
q(\Psi)\geq c_1\|\nabla_\Phi\Psi\|^2+
(a/2)\|r^2\Psi\|^2-C\|\Psi\|^2,\qquad c_1>0.
\]
La norma
$\|\Psi\|^2+\|\nabla_\Phi\Psi\|^2+\|r^2\Psi\|^2$
es completa por cierre de la derivada débil y la multiplicación.
Estas cotas y las superiores hacen equivalente la norma de forma,
tras sumar una constante, a esa norma completa.
El teorema de representación de formas cerradas produce el operador
asociado y su cálculo espectral da la evolución.
La unicidad se refiere a esta forma y dominio, no a cada dominio
formal alternativo.
\end{proof}

Covarianza de $D_T,W$, invariancia de medidas, identidad Yukawa y
contracción torsional interna conservan $q$ y $\mathcal Q$.
La unicidad del operador asociado implica que la representación
compacta conmuta con $\mathbb H$; su promedio de Haar reduce
el operador y su evolución. No es un promedio correctivo posterior.

Se retira el corte computacional con bloques completos de Peter--Weyl
y capas isotrópicas completas de Hermite.
Regularización y truncamiento suave aproximan derivadas y peso
$r^2$; las densidades acotadas preservan normas equivalentes.
Su unión es densa en $\mathcal Q$. Para las proyecciones ortogonales
$P_n$ en las medidas $\mu_x$ y los operadores de Galerkin
$\mathbb H_n$,
\[
(\mathbb H_n+\lambda)^{-1}P_nf\longrightarrow
(\mathbb H+\lambda)^{-1}f\qquad(\lambda>C).
\]
La ecuación coerciva de forma y su versión de Galerkin dan
ortogonalidad del error; continuidad y coercividad lo acotan por
el mejor error de aproximación, que tiende a cero.
Se retira el corte escalar y funcional de enlace de esta carta,
no el espacial, geométrico ni fermiónico.
Autoadjunción tampoco implica clase traza de $e^{-t\mathbb H}$.

\subsubsection{Intercambio y conservación}
\label{hmtcuatro:gea:intercambio}

Para $V=\sum_xP_x\otimes B_x$ y un elemento $h_{xy}$ del reloj,
multiplicar bloques da
\begin{equation}
[H_{\rm clk}\otimes I,V]_{xy}=h_{xy}(B_y-B_x).
\label{hmtcuatro:gea:conmutador}
\end{equation}
Si $h_{xy}\ne0$ y $B_y\ne B_x$, hay intercambio
geométrico--material. Si $\mathbb H=A+B+V$, para operadores
acotados o un núcleo común que justifique las derivadas,
\[
\frac d{dt}\langle A\rangle=\frac i\hbar\langle[\mathbb H,A]\rangle,
\quad
\frac d{dt}\langle B\rangle=\frac i\hbar\langle[\mathbb H,B]\rangle,
\quad
\frac d{dt}\langle V\rangle=\frac i\hbar\langle[\mathbb H,V]\rangle.
\]
La suma es cero por $[\mathbb H,\mathbb H]=0$.
Se conserva la energía incluyendo interacción, no cada sector
por separado. La geometría está en el espacio cuántico, no añadida
como fondo externo. Las historias ampliadas retienen memoria y retorno;
su refinamiento no equivale por definición al refinamiento espacial.

\subsection{La misma acción y sus corrientes}
\label{hmtcuatro:gea:accion}

La realización geométrica emplea cotetrada no degenerada $e$,
conexión de Lorentz $\omega$ y conexiones internas de la misma
materia. Sean $\Sigma^{IJ}=e^I\wedge e^J$,
$P_\gamma=\star+\gamma^{-1}I$,
$\gamma\in\mathbb R\setminus\{0\}$ y $\star^2=-I$ en bivectores.
Los acoplamientos permanecen fijos durante la variación.
Con $\kappa=8\pi G/c^4$, la misma acción es
\begin{equation}
S_{\rm tot}=\frac{\hbar}{16\pi L^2}
\int\Sigma_{IJ}\wedge(P_\gamma F_\omega)^{IJ}
-\frac{\Lambda\hbar}{8\pi L^2}\int\operatorname{vol}_e+S_m,
\label{hmtcuatro:gea:accion-total}
\end{equation}
donde $S_m=S_{\rm YM}+S_\Phi+S_{\rm Weyl}+S_Y$ contrae sus
índices con la misma $e$, que se varía.
Los coeficientes siguen de
$(2\kappa c)^{-1}=\hbar/(16\pi L^2)$.

Con $\delta_\omega S_m=-\tfrac12\int
\delta\omega^{IJ}\wedge\sigma_{IJ}$,
$\delta F=D_\omega\delta\omega$ y la integración por partes,
\begin{equation}
D_\omega(P_\gamma\Sigma)=\kappa c\sigma.
\label{hmtcuatro:gea:cartan}
\end{equation}
Se usan variaciones interiores o la completación de borde compatible.
Corriente de espín y fuente métrica son derivadas de la misma
materia, no dos entradas independientes.

\subsubsection{Eliminación torsional y términos cruzados}
\label{hmtcuatro:gea:torsion}

La inversa real es
$P_\gamma^{-1}=\gamma^2(-\star+\gamma^{-1}I)/(1+\gamma^2)$:
el producto de los dos polinomios en $\star$ antes de normalizar
vale $(1+\gamma^{-2})I$.
Denótese por $\mathcal Y^{IJ}=\kappa c(P_\gamma^{-1}\sigma)^{IJ}$
la forma bivectorial de grado tres, distinta del carácter $Y$.
Para $T^I=D_\omega e^I$,
$D_\omega\Sigma^{IJ}=T^I\wedge e^J-e^I\wedge T^J$.
Con el marco dual $E_I$, su inversa es
\[
\mathcal B^I=\sum_J\iota_{E_J}\mathcal Y^{IJ},\qquad
\vartheta=\tfrac14\sum_I\iota_{E_I}\mathcal B^I,\qquad
T^I=\mathcal B^I-e^I\wedge\vartheta.
\]
En efecto, si $t=\sum_J\iota_{E_J}T^J$, las contracciones dan
$\mathcal B^I=T^I+e^I\wedge t$ y después $4t$.
El mapa tiene núcleo nulo entre espacios de dimensión veinticuatro,
luego es un isomorfismo. Para
$\omega=\mathring\omega(e)+\mathfrak k$,
\[
T_{IJK}=\mathfrak k_{IKJ}-\mathfrak k_{IJK},\qquad
\mathfrak k_{IJK}=\tfrac12(T_{KIJ}-T_{IJK}-T_{JKI}).
\]
La combinación cíclica y la antisimetría en los dos primeros índices
prueban estas fórmulas.
Para materia afín en $\mathfrak k$, con corriente independiente
de ella, hay una única $\mathfrak k_*[e,\sigma]$ lineal en
la corriente total $\sigma=\sum_s\sigma_s$.

La expansión de curvatura conserva el borde
\[
S_\partial[e,\mathfrak k]=\frac1{2\kappa c}
\int_{\partial M}\Sigma_{IJ}\wedge(P_\gamma\mathfrak k)^{IJ}.
\]
La densidad interior dependiente de contorsión es
$\mathcal Q_{e,\gamma}(\mathfrak k)
-\tfrac12\mathfrak k^{IJ}\wedge\sigma_{IJ}$,
donde $\mathcal Q$ es homogénea de grado dos.
Su estacionariedad evaluada en
$\delta\mathfrak k=\mathfrak k_*$ da
$2\mathcal Q(\mathfrak k_*)=
\tfrac12\mathfrak k_*^{IJ}\wedge\sigma_{IJ}$.
Por tanto,
\begin{equation}
\mathcal L_{\rm spin}^{\rm ef}
=-\tfrac14\mathfrak k_*^{IJ}\wedge\sigma_{IJ}
=-\mathcal Q_{e,\gamma}(\mathfrak k_*).
\label{hmtcuatro:gea:spin}
\end{equation}
La linealidad conserva los cruces entre especies.
Se elimina la contorsión una vez; no se añaden simultáneamente
su interacción lineal eliminada y el cuártico efectivo.

En la especialización espinorial, el coeficiente recibido
$C_\gamma=3\kappa c\hbar^2\gamma^2/[16(1+\gamma^2)]$ da
\begin{equation}
\frac{C_\gamma}{\hbar}
=\frac{3\pi}{2}L^2\frac{\gamma^2}{1+\gamma^2}.
\label{hmtcuatro:gea:coeficiente-torsion}
\end{equation}
Basta sustituir $\kappa=8\pi G/c^4$ y $\hbar G=c^3L^2$,
sin cambiar la rama de $\gamma$.
En la Fock de la carta, la corriente total conserva la contracción
\[
\widehat Q_{{\rm tot},v}=\sum_{a=1}^4s_a
\{d\Gamma(\widetilde M_{a,v})^2-d\Gamma(\widetilde M_{a,v}^2)\},
\quad s=(-1,-1,-1,+1),
\]
\[
\widehat H_{\rm tor}
=-\sum_v\frac{N_vcC_\gamma}{\mathcal V_v}\widehat Q_{{\rm tot},v}.
\]
Las matrices $\widetilde M_{a,v}$ representan las componentes
de corriente. $N_v$ es el lapse, distinto de $N_\Omega$ y de
una ocupación. La identidad de orden normal retira la contracción
de una partícula, no los cruces entre especies.
La signatura permanece en $s_a$.

\subsubsection{Fuente métrica y Legendre de la misma acción}
\label{hmtcuatro:gea:legendre}

La eliminación estacionaria preserva la variación de las demás
variables: la regla de la cadena contiene un término en
$\delta\mathfrak k_*$ multiplicado por la ecuación de conexión,
que es cero. La acción reducida es
\[
S_{\rm red}=\frac1{2\kappa c}\int(R[g]-2\Lambda)\operatorname{vol}_e
+S_m^{\rm LC}+S_{\rm spin}^{\rm ef}+S_\partial.
\]
Definimos la fuente de acción por
$\delta_g(S_m^{\rm LC}+S_{\rm spin}^{\rm ef})
=-\tfrac12\int\mathcal T^S_{\mu\nu}\delta g^{\mu\nu}
\operatorname{vol}_e$.
La variación gravitatoria interior produce
\begin{equation}
G_{\mu\nu}+\Lambda g_{\mu\nu}
=\kappa c\mathcal T^S_{\mu\nu}
=\kappa(T^{\rm LC}_{\mu\nu}+U^{\rm spin}_{\mu\nu}),
\quad T^{\rm LC}+U^{\rm spin}=c\mathcal T^S.
\label{hmtcuatro:gea:metrica}
\end{equation}
Se incluye la variación de volumen del término constante del
potencial. El factor $c$ corresponde a la cotetrada en la recta
de longitud; no se mezclan las fuentes de acción y físicas.

Con $a=(2\kappa c)^{-1}$ y
$\mathcal B_{IJ}=(P_\gamma\Sigma)_{IJ}$, el potencial geométrico
es $\theta_{\rm geom}=a\mathcal B_{IJ}\wedge\delta\omega^{IJ}$.
Descomponer $\omega=\omega_0dt+\underline\omega$ y
$F_{0a}=\dot\omega_a-D_a\omega_0$ identifica el término cinético;
integrar por partes conserva Gauss y borde.
Con $e_0=Nn+N^ae_a$ y la Legendre de la misma materia,
\begin{equation}
S_{\rm tot}=\int dt\,[\Theta_{\rm red}(\dot z)
-\mathcal C[N]-\mathcal V[N^a]-\mathcal G_L[\omega_0]
-\mathcal G_{\rm int}[A_0]]+S_\partial.
\label{hmtcuatro:gea:canonica}
\end{equation}
Lapse, shift y calibre mantienen sus direcciones degeneradas.
Las restricciones de segunda clase se reducen antes de usar
$\Theta_{\rm red}$ o se conservan expresamente.
Los espinores de primer orden no reciben una inversa ficticia
de velocidades.

Para contorsión y su momento, las restricciones son
$\pi_{\mathfrak k}=0$ y
$\partial\mathcal Q/\partial\mathfrak k-\sigma/2=0$.
Su matriz tiene bloques
$\left(\begin{smallmatrix}0&-M\\M^{\mathsf T}&B\end{smallmatrix}\right)$,
con $M$ invertible por la reconstrucción anterior; por tanto es
invertible. El corchete de Dirac efectúa esa eliminación y conserva
separadamente las restricciones fermiónicas graduadas.
En una dirección bosónica regular,
\[
H_\Phi=N\left(\frac{p^2}{2w}+wV+H_{\rm grad}\right),\quad
p=\frac wN D_t\phi,\quad
L_\Phi=\frac{w}{2N}|D_t\phi|^2-NwV-NH_{\rm grad}.
\]
El volumen $w=\sqrt{\det q}$ no se congela.
Para $K_{ij}=(\dot q_{ij}-\mathcal L_{N^a}q_{ij})/(2N)$,
\[
\Pi^{ij}=\frac{\sqrt q}{2\kappa c}(K^{ij}-q^{ij}K),\qquad
K_{ij}=\frac{2\kappa c}{\sqrt q}
(\Pi_{ij}-\tfrac12q_{ij}\Pi).
\]
La traza y la parte sin traza prueban la inversa.
Si el momento total contiene una contribución material de marco,
se usa $\Pi=p-p_m$, conservando $p_m$.
Así se recupera la misma acción y su fuente. La Legendre no
demuestra por sí sola que una cuantización arbitraria de
\eqref{hmtcuatro:gea:canonica} coincida con
\eqref{hmtcuatro:gea:total}.

\subsection{Propagación de restricciones con la fuente total}
\label{hmtcuatro:gea:restricciones}

Sea $E_{\mu\nu}=G_{\mu\nu}+\Lambda g_{\mu\nu}
-\kappa c\mathcal T^S_{\mu\nu}$.
Sobre las ecuaciones materiales, la invariancia por difeomorfismos
del funcional reducido implica
$\nabla^\mu\mathcal T^S_{\mu\nu}=0$:
una variación interior generada por $\xi$ deja la integral de
$\mathcal T^S_{\mu\nu}\nabla^\mu\xi^\nu$, mientras las ecuaciones
materiales anulan los demás términos. Integrar por partes y variar
$\xi$ prueba la divergencia nula, antes de imponer $E=0$.
Bianchi y los acoplamientos fijos dan $\nabla_\mu E^{\mu\nu}=0$.

\begin{proposition}[Conservación de los datos de restricción]
\label{hmtcuatro:gea:propagacion}
Una solución regular de las ecuaciones materiales y evolutivas
métricas conserva las restricciones satisfechas inicialmente
durante su intervalo de existencia regular.
\end{proposition}
\begin{proof}
En coordenadas gaussianas
$g=-d\tau^2+q_{ij}(\tau,x)dx^idx^j$ se imponen $E_{ij}=0$ y
se escribe
$C=E_{00}$, $C_i=E_{0i}$,
$K_{ij}=\dot q_{ij}/2$ y $\mathcal K=q^{ij}K_{ij}$.
Se tiene $E^{00}=C$, $E^{0i}=-C^i$, $E^{ij}=0$,
$\Gamma^i{}_{0j}=K^i{}_j$ y
$\Gamma^\mu{}_{\mu0}=\mathcal K$.
La componente temporal de la divergencia y la espacial dan
\[
\partial_\tau C-D_iC^i+\mathcal KC=0,\qquad
\partial_\tau C^i+\mathcal KC^i+2K^i{}_jC^j=0.
\]
Al bajar el índice, $\dot q_{ij}=2K_{ij}$ cancela el último
término espacial. Quedan exactamente
\begin{equation}
\partial_\tau C-D_iC^i+\mathcal KC=0,\qquad
\partial_\tau C_i+\mathcal KC_i=0.
\label{hmtcuatro:gea:propagacion-sistema}
\end{equation}
La segunda ecuación homogénea mantiene $C_i=0$ y la primera
queda $\dot C+\mathcal KC=0$, conservando $C=0$.
$q$ y $\mathcal K$ son los de la solución acoplada, no un fondo prescrito.
\end{proof}
La carta gaussiana prueba localmente una afirmación tensorial,
sin congelar $q^{-1}$ ni sustituir la fuente.
No se afirma existencia global sin singularidades para cada dato.
La propagación variacional tampoco es por sí sola una identidad
de conmutadores cuánticos para deformaciones normales arbitrarias.

\subsection{Frontera y operador autoinercial}
\label{hmtcuatro:gea:autoinercia}

Sea $b:\mathcal X_\infty^{\rm enr}\to B_{\rm ef}$,
$B_{\rm ef}=\operatorname{im}(b)$.
Una respuesta $I_v$ factoriza unívocamente como
$I_v=\overline I_v\circ b$ si y sólo si es constante en las
fibras de $b$. La necesidad es inmediata; para la suficiencia,
$\overline I_v(\beta)=I_v(x)$ con $b(x)=\beta$ es independiente
del representante. La imagen efectiva da unicidad.
La dependencia machiana fuerte añade estados con igual restricción
local y respuestas distintas.

La bisagra del mismo estado produce
$r_{\rm av}=\pi/\varphi^2$ y $r_{\rm av}^J=\varphi/\pi^2$.
En el sector de amplitud común,
$\mathcal L_{\rm ar}=\pi\mu_{\rm ar}\mathcal M(x)$ y
$\mathcal L_{\rm vol}=\mu_{\rm vol}\mathcal M(x)$,
$\mathcal M(x)>0$, con
$\mu_{\rm ar}/\mu_{\rm vol}=\varphi^{-2}$.
Dividir por $\mathcal L_{\rm vol}$ da lectores del mismo tipo
$A_\partial=r_{\rm av}$ y $V_\partial=1$.
El cociente cancela la amplitud, no la historia conservada en el archivo.

Para una orientación $a$,
$q_a(x)=h_a(x)/(108t_0(x))=\hbar_a(x)/t_P(x)$
desciende a $Q:B_{\rm ef}\to\mathcal L_E^+$
si y sólo si $b(x)=b(x')$ implica
$h_a(x)/t_0(x)=h_a(x')/t_0(x')$.
Es el criterio de factorización aplicado al reloj.
Lo satisfacen las cartas fijas y las variables cuyo cociente
desciende. En la carta radial $Q=\hbar_ac/L$.
Con energías de esa misma recta, $E_1E_2/Q^2$ es adimensional
e independiente de base.

Para proyecciones ortogonales complementarias,
\begin{align}
w_A&=\frac{A_\partial r_{\rm av}}
{A_\partial r_{\rm av}+V_\partial r_{\rm av}^J}
=\frac{\pi^4}{\pi^4+\varphi^5},\qquad w_V=1-w_A,
\label{hmtcuatro:gea:pesos}\\
W_{\rm av}&=w_AP_A+w_VP_V,\qquad
\overline I_v=\frac{E_1E_2}{Q^2}W_{\rm av}.
\label{hmtcuatro:gea:respuesta}
\end{align}
Multiplicar numerador y denominador de
$r_{\rm av}^2/(r_{\rm av}^2+r_{\rm av}^J)$ por
$\varphi^4\pi^2$ prueba la evaluación.
Se conserva la diferencia entre lector areal y ponderación:
la marca regional se genera una vez.
$0<w_A,w_V<1$ hace positivo e invertible a $W_{\rm av}$ y
\[
\langle z,\overline I_vz\rangle
=\frac{E_1E_2}{Q^2}
(w_A\|P_Az\|^2+w_V\|P_Vz\|^2)>0\quad(z\ne0).
\]
Intercambiar completamente
$(A_\partial,r_{\rm av},P_A)$ y
$(V_\partial,r_{\rm av}^J,P_V)$ permuta los sumandos.
Un transporte unitario conjuga la respuesta y conserva su espectro;
implementar el intercambio dentro de un espacio exige iguales
dimensiones sectoriales.
Una reescala común de $A_\partial,V_\partial$ no cambia los pesos
y no prueba dependencia global.
Con energías y pesos fijos, $Q\mapsto qQ$ cambia la respuesta
por $q^{-2}$; el testigo fuerte conserva además la misma
restricción local.

\begin{theorem}[Autoinercia y radio del mismo carácter]
\label{hmtcuatro:gea:autoinercial-radial}
Con el mismo reloj y orientación,
\begin{equation}
\overline I_v=\frac{G_aE_1E_2}{\hbar_ac^5}W_{\rm av}
=\frac{G_am_1m_2}{\hbar_ac}W_{\rm av}.
\label{hmtcuatro:gea:mach-gravedad}
\end{equation}
Para una sonda $y_p>0$, $E_p=Qy_p$ y
$\bar\lambda_p=L/y_p$, la extensión espectral satisface
\begin{equation}
\widehat I_{p,Y}=y_pY\otimes W_{\rm av}
=\frac{E_p}{Q^2}H_X\otimes W_{\rm av}
=\frac{R_X}{\bar\lambda_p}\otimes W_{\rm av}
=\frac{G_am_p}{\hbar_ac}M_X\otimes W_{\rm av}.
\label{hmtcuatro:gea:identidad-autoinercial}
\end{equation}
\end{theorem}
\begin{proof}
$Q^2=\hbar_a^2c^2/L^2$ y $\hbar_aG_a=c^3L^2$ dan
$Q^{-2}=G_a/(\hbar_ac^5)$; después se usa $E_i=m_ic^2$.
Para $Y=\sum_jy_jP_j$, aplicar el lector a cada energía $Qy_j$
produce $\sum_jy_py_jP_j\otimes W_{\rm av}$, independientemente
de base propia. El cálculo espectral extiende el lector lineal
al carácter autoadjunto positivo general.
La descomposición por $P_A,P_V$ da los operadores
$y_pw_AY$ y $y_pw_VY$, con sus multiplicidades:
son autoadjuntos positivos en el dominio de $Y\otimes I$.
Sustituir los lectores radiales prueba las otras expresiones.
\end{proof}

Si una realización adicional identifica efectivamente su operador
completo con $H_X=QY$, conserva esa identificación y sus dominios.
Para $H_X=\sum_rH_r$ en un núcleo común,
$\widehat I_{p,Y}=(E_p/Q^2)\sum_rH_r\otimes W_{\rm av}$.
No se requiere positividad de cada sumando; sí la del carácter
del operador identificado. No se suprimen términos ni se cambia
el origen de energía para imponerla.
El teorema no asigna automáticamente este lector a $\mathbb H$.

En los bloques de \eqref{hmtcuatro:gea:schur-prueba}, el inverso
interior de $y_pY\otimes W_{\rm av}$ es
$y_p^{-1}C^{-1}\otimes W_{\rm av}^{-1}$.
La multiplicación da
\begin{equation}
\operatorname{Schur}(\widehat I_{p,Y})
=y_pY_{\rm ef}\otimes W_{\rm av}
=\frac{R_{X,\rm ef}}{\bar\lambda_p}\otimes W_{\rm av}.
\label{hmtcuatro:gea:schur-autoinercia}
\end{equation}
No se borran los bloques cruzados.
Para $a_s=y_pw_s>0$, $s=A,V$, la misma cuenta da
$\mathcal K_{a_sY}(a_sz)=a_s\mathcal K_Y(z)$
en el dominio resolvente interior, conservando la memoria completa.
Si $Y'K=KY$ y $W'_{\rm av}J=JW_{\rm av}$, con
$y_p$ y sección intensiva fijos,
\begin{equation}
\widehat I'_{p,Y'}(K\otimes J)
=(K\otimes J)\widehat I_{p,Y}.
\label{hmtcuatro:gea:naturalidad}
\end{equation}
Se prueba por sustitución.
Los cortes espectrales de la proposición
\ref{hmtcuatro:gea:limite} convergen en norma de grafo;
los dos pesos fijos transmiten la convergencia a la respuesta.
La naturalidad es la de estos entrelazadores efectivos, no la
de una familia distinta de mapas espaciales identificada sólo por nombre.

\subsection{Autoinercia del estado y aceleración de su proyección}
\label{hmtcuatro:gea:proyeccion}

En una realización diferenciable, el estado conjunto
$\Gamma=(x,\mathcal O,m)$ tiene conexión $\nabla^{\rm tot}$
en $\mathcal N$. Una proyección suave
$\pi_S:\mathcal N\to\mathcal N_S$, con conexión $\nabla^S$,
conserva los transportes y lectores que realiza.
El marco observado es
$\mathfrak F_{\mathcal O}(\Gamma)
=\operatorname{Res}_{\mathcal O}(\Gamma,\nabla^{\rm tot})$.
Para una curva dos veces diferenciable y
$\gamma_S=\pi_S\circ\Gamma$, la autoinercia significa
$\nabla^{\rm tot}_{\dot\Gamma}\dot\Gamma=0$.
El defecto es
\[
\mathcal K_{\pi_S}(\dot\Gamma,\dot\Gamma)
=\nabla^S_{\dot\gamma_S}\dot\gamma_S
-d\pi_S(\nabla^{\rm tot}_{\dot\Gamma}\dot\Gamma).
\]
\begin{proposition}[Aceleración publicada]
\label{hmtcuatro:gea:aceleracion}
Para una trayectoria autoinercial,
\begin{equation}
a_S=\mathcal K_{\pi_S}(\dot\Gamma,\dot\Gamma),\qquad
(\mathcal K_{\pi_S})^a{}_{BC}
=\partial_B\partial_C\pi_S^a
+(\Gamma^S)^a{}_{bc}\partial_B\pi_S^b\partial_C\pi_S^c
-\partial_D\pi_S^a(\Gamma^{\rm tot})^D{}_{BC}.
\label{hmtcuatro:gea:defecto}
\end{equation}
\end{proposition}
\begin{proof}
La regla de la cadena da
$\ddot\gamma_S^a=\partial_B\pi_S^a\ddot\Gamma^B
+\partial_B\partial_C\pi_S^a\dot\Gamma^B\dot\Gamma^C$.
Sumar la conexión del subsistema y restar la imagen de la
aceleración total cancela los términos en $\ddot\Gamma$.
Los restantes son el tensor mostrado contraído con las velocidades.
La autoinercia anula la aceleración total y deja la igualdad.
\end{proof}
La respuesta geométrica factoriza por $b$ cuando conexión,
proyección y dato cinemático descienden a la frontera, o éste
se fija en la comparación. Si cambia la velocidad, se conserva
como argumento. Así, el conjunto autoinercial puede publicar
subsistemas acelerados sin un marco absoluto exterior.

Autoinercia no anula por sí sola curvatura ni holonomía.
Un dato transportado por un lazo retorna si y sólo si está en
el espacio fijo de su holonomía. El retorno del estado completo
requiere además una realización inyectiva en el sector comparado:
retorno visible y retorno de historia siguen siendo distintos.

\subsection{Resultado y controles de alcance}
\label{hmtcuatro:gea:conclusion}

El mismo carácter fija masa, energía y radio; su proporcionalidad
conserva memoria estática, espectral y normalización dual.
Los transportes geométrico e interno entran en el diferencial
de una sola energía. La acción conjunta produce las fuentes
geométrica y torsional y conserva las restricciones sobre su
solución regular. El operador autoinercial es el radio del
carácter dividido por la longitud conjugada de la sonda,
mientras la aceleración es el defecto de proyección del estado.

Los dos últimos objetos tienen tipos distintos:
$\widehat I_{p,Y}$ no se identifica con $\mathcal K_{\pi_S}$
ni con el tensor de Einstein. La incorporación probada tampoco
se sustituye por la exigencia diferente de anular una curvatura
cuántica total para deformaciones normales arbitrarias.
Ese enunciado posee sus generadores y dominios; no se afirma aquí
ni se declara ausente del corpus por no ser esta conclusión.

Los falsadores son concretos. Cambiar sólo $G$ o $\hbar$ con
$L,Y$ fijos rompe \eqref{hmtcuatro:gea:radial}; sustituir
$L$ por $\ell_0$ sin $54/\pi$ altera el reloj; borrar $F$
modifica la reducción; reescalar juntos los lectores areal y
volumétrico no prueba separación machiana; un mapa que no
entrelace $Y$ no satisface \eqref{hmtcuatro:gea:naturalidad}.
Los ensayos racionales son controles finitos reproducibles,
no valores objetivo del generador ni sustitutos de las pruebas
de dominio y límite.
```

## 20_accion_retroaccion_restricciones.tex

Ruta: `copia_vii/integracion_20260930/20_accion_retroaccion_restricciones.tex`

SHA-256: `e3d97712bda4708c20c70b7c1ef286d1cde6b870d8755e93be83db6a04710073`

```latex
% Fragmento integrable; no documento autónomo y no orden de compilación.
% Fecha: 2026-09-30. No modifica fuentes publicadas.
% Procedencia: reunión de RETROACCION_PCH_Y_RESTRICCIONES_VARIACIONALES.md,
% PRECUANTIZACION_PCH_Y_FIDELIDAD.md y CIERRE_CANONICO_TOTAL_Y_REPRESENTACION.md.
% Prerrequisitos de inserción: núcleo común APP--TRIT--TPK; VIII/30d,
% VIII/31 y VIII/33; lectores de acción, gamma y acoplamientos.
% Los nuevos labels usan exclusivamente el prefijo hmtcuatro:.
\section{Acción conjunta, retroacción y cierre canónico de las restricciones}
\label{hmtcuatro:accion-retroaccion-restricciones}

La secuencia causal de este desarrollo es
\[
 \mathrm{APP}\longrightarrow\mathrm{TRIT}\longrightarrow\mathrm{TPK}
 \longrightarrow\text{estado enriquecido}
 \longrightarrow\text{estructura discreta conjunta del continuo}.
\]
Se conservan las hojas, la orientación, los residuos, el acarreo, las rutas,
la frontera y la memoria de esa construcción. La escala de acción y los
acoplamientos son salidas HMT recibidas antes de emplear el lenguaje
variacional y simpléctico. No se seleccionan por valores objetivo ni por
la conclusión de curvatura que se va a demostrar. El retorno de fase
tampoco reinicia el estado enriquecido.

La realización geométrica previamente construida proporciona una
cotetrada no degenerada \(e\), su conexión métrica y el levantamiento
espinorial del transporte. Aquí esa geometría se varía junto con los
campos materiales. Reuniremos en una sola demostración la acción común,
su reducción torsional, la transformación de Legendre, la primera clase,
la propagación de las restricciones y la planitud característica de la
conexión canónica que resulta de la misma acción. Esta última realización
no se identifica por su nombre con otro Hamiltoniano interactuante.

\subsection{Estructura de partida y acción con fuente completa}
\label{hmtcuatro:datos-accion-total}

Sea \(M\) una región lisa orientada de dimensión cuatro con estructura
de espín, firma \((-+++)\) y una foliación espacial regular. La cotetrada
toma valores en la recta de longitud de la realización recibida.
Escribimos
\[
 \Sigma^{IJ}=e^I\wedge e^J,\qquad
 F_\omega=\mathrm d\omega+\omega\wedge\omega,\qquad
 \mathsf P_\gamma=\star+\gamma^{-1}I,\qquad \star^2=-I.
\]
La estrella de esta fórmula actúa sobre bivectores internos; no es la
dualidad exterior de formas. Durante la variación permanecen fijas las
secciones recibidas \(c>0,\hbar>0,G>0,\gamma\in\mathbb R\setminus\{0\}\)
y \(\Lambda\). Con \(\kappa=8\pi G/c^4\), la acción total es
\begin{equation}
 \begin{split}
 S_{\rm tot}={}&\frac1{2\kappa c}
   \int_M\Sigma_{IJ}\wedge(\mathsf P_\gamma F_\omega)^{IJ}
 -\frac{\Lambda}{\kappa c}\int_M\operatorname{vol}_e\\
 &+S_{\rm YM}[e,A]+S_H[e,A,H]
   +S_W[e,\omega,A,\Psi]+S_Y[e,H,\Psi]+S_{\partial}.
 \end{split}
 \label{hmtcuatro:accion-total}
\end{equation}
El símbolo \(H\) sin subíndice designa aquí el campo Higgs, no un
Hamiltoniano. Todas las contracciones espaciotemporales de la materia
utilizan la misma \(e\). El problema de borde es el recibido de la
variación Cartan--Holst: variaciones interiores, datos de borde fijos
compatibles o una completación que anule el mismo término fronterizo.

Para fijar el contenido de \eqref{hmtcuatro:accion-total}, las conexiones
internas actúan sobre el fibrado quiral
\[
 (S_L\otimes E_L)\oplus(S_R\otimes E_R).
\]
No se sustituye ese fibrado por un acoplamiento vectorial. En la
normalización entera \(y=6Y\), los multipletes recibidos tienen pesos
\(1,4,-2,-3,-6\), respectivamente para \(q_L,u_R,d_R,\ell_L,e_R\);
el doblete \(H\) tiene peso \(3\). El color actúa en el factor
\(\mathbb C^3\) de los quarks y trivialmente en los leptones. El factor
de familias y sus mapas \(Y_u,Y_d,Y_e\) se conservan. No se añade en
este bloque un compañero derecho a un multiplete que no lo tenga.

Con \(\widetilde H=i\sigma_2\overline H\), el mapa material es
\begin{equation}
 \begin{split}
 \mathsf Y_q(H)(u,d)&=
       \widetilde H\otimes Y_u u+H\otimes Y_d d,\\
 \mathsf Y_\ell(H)e&=H\otimes Y_e e .
 \end{split}
 \label{hmtcuatro:yukawa}
\end{equation}
Se entiende la identidad sobre el factor de color en la primera línea.
El término de acción es
\(-(\bar\Psi_L\mathsf Y(H)\Psi_R+\mathrm{h.c.})\), con las secciones
dimensionales recibidas. La equivariancia no es sólo nominal: para
\(U\in SU(2)\), \(i\sigma_2\overline U=U i\sigma_2\), de modo que
\(\widetilde H\mapsto U\widetilde H\). Los pesos de las tres columnas
son \(-3+4=1\), \(3-2=1\) y \(3-6=-3\). El color se entrelaza por la
identidad y los mapas de familia conmutan con la acción interna.
Por tanto, para cada transformación interna \(u\),
\begin{equation}
 \mathsf Y(uH)\rho_R(u)=\rho_L(u)\mathsf Y(H).
 \label{hmtcuatro:equivariancia-yukawa}
\end{equation}
Si la realización material precedente contiene además otros
multipletes, sus mapas se incorporan con su identidad de equivariancia
propia; esta prueba no inventa estados nuevos.

En una carta de unidades \(\hbar=c=1\), la densidad material que resume
estas acciones tiene la forma
\begin{equation}
 \begin{split}
 \mathcal L_m={}&-\frac14 F_{B,\mu\nu}F_B^{\mu\nu}
 -\frac14\sum_a F_{W,\mu\nu}^aF_W^{a,\mu\nu}
 -\frac14\sum_a F_{C,\mu\nu}^aF_C^{a,\mu\nu}\\
 &-(\nabla_\mu H)^\dagger\nabla^\mu H-V(H)
 +\mathcal L_W(\Psi_L,\nabla_L)+\mathcal L_W(\Psi_R,\nabla_R)\\
 &-\bigl(\bar\Psi_L\mathsf Y(H)\Psi_R+\mathrm{h.c.}\bigr).
 \end{split}
 \label{hmtcuatro:densidad-material}
\end{equation}
Las curvaturas incluyen sus acoplamientos; éstos y las normalizaciones
de componentes son los de sus propietarios. La escritura en esa carta
no elimina la sección de acción ni recalibra los coeficientes.
En particular, no se introduce aquí un valor numérico nuevo para el
acoplamiento fuerte. La conexión de espín de \(\nabla_L,\nabla_R\)
es la de \(e,\omega\); las conexiones \(B,W,C\) actúan en las
representaciones recién descritas. La constante de \(V\) se conserva,
pues su variación de volumen pertenece a la fuente gravitatoria.

La parte espinorial conserva las convenciones explícitas del desarrollo
precedente: \(\{g^I,g^J\}=2\eta^{IJ}I\),
\(\mathbb B_{IJ}=\frac14[g_I,g_J]\), \(A_D=-ig^0\),
\(\bar\psi=\psi^\dagger A_D\) y
\(D\psi=\mathrm d\psi+\frac12\omega^{IJ}\mathbb B_{IJ}\psi+A\psi\).
Su cinética simétrica es
\[
 \frac{\hbar}{2}
 [\bar\psi g^I D\psi-(D\bar\psi)g^I\psi]\wedge\eta_I,
 \qquad \eta_I=\iota_{E_I}\operatorname{vol}_e .
\]
La suma se toma sobre los campos realmente presentes, con sus
proyecciones quirales, no sobre una duplicación vectorial del catálogo.
Los términos Yukawa son algebraicos y no dependen de \(\omega\).
La corriente total queda fijada por
\begin{equation}
 \delta_\omega S_m=-\frac12\int_M\delta\omega^{IJ}\wedge\sigma_{IJ},
 \qquad
 \sigma_{JK}=\sum_s-\frac{\hbar}{2}
   \bar\psi_s\{g^I,\mathbb B_{JK}\}\psi_s\,\eta_I.
 \label{hmtcuatro:corriente-total}
\end{equation}

\subsection{Una demostración de compatibilidad, propagación y cierre}
\label{hmtcuatro:demostracion-unica}

\begin{theorem}[Compatibilidad canónica de la acción conjunta]
\label{hmtcuatro:teorema-canonico-total}
Considérese \eqref{hmtcuatro:accion-total} en el dominio no degenerado
anterior, con materia afín en la contorsión, y en una carta regular de
la transformación de Legendre restringida. Reténganse las restricciones
fermiónicas de primer orden y elimínense las de segunda clase mediante
su corchete de Dirac. Para parámetros de soporte interior, o con el
borde compatible sin cargos impropios, se cumplen conjuntamente:
la ecuación métrica tiene la fuente material total de esa misma acción;
sus generadores de difeomorfías y calibre son de primera clase; las
restricciones se propagan sobre toda solución acoplada regular; y el
potencial canónico total induce una conexión precuántica plana en las
direcciones características de la superficie regular de restricciones.

La afirmación es sobre esta acción y esta realización canónica.
No identifica automáticamente su conexión con un Hamiltoniano
interactuante distinto ni prueba su límite espacial--quiral.
\end{theorem}

\begin{proof}
\paragraph{1. Eliminación torsional sin duplicación.}
Escribamos \(\omega=\mathring\omega(e)+\mathfrak k\).
La expansión \(F_\omega=F_{\mathring\omega}
+D_{\mathring\omega}\mathfrak k+\mathfrak k\wedge\mathfrak k\)
y \(D_{\mathring\omega}\Sigma=0\) separan la contribución de borde
\[
 S_{\partial,\mathfrak k}
 =\frac1{2\kappa c}\int_{\partial M}
                  \Sigma_{IJ}\wedge(\mathsf P_\gamma\mathfrak k)^{IJ}
\]
de la densidad algebraica
\begin{equation}
 \mathcal Q_{e,\gamma}(\mathfrak k)
       -\frac12\mathfrak k^{IJ}\wedge\sigma_{IJ},\qquad
 \mathcal Q_{e,\gamma}(\mathfrak k)=\frac1{2\kappa c}
       \Sigma_{IJ}\wedge
       \mathsf P_\gamma(\mathfrak k\wedge\mathfrak k)^{IJ}.
 \label{hmtcuatro:cuadratica-contorsion}
\end{equation}
La variación original da
\(D_\omega(\mathsf P_\gamma\Sigma)=\kappa c\,\sigma\).
La inversa de Holst y la inversa torsión--contorsión del desarrollo
precedente son invertibles para el coframe y \(\gamma\) declarados.
Así determinan una única \(\mathfrak k_*[e,\sigma]\), lineal en
\(\sigma\). La variación radial de
\eqref{hmtcuatro:cuadratica-contorsion} en su estacionario da
\(2\mathcal Q(\mathfrak k_*)=\frac12\mathfrak k_*^{IJ}\wedge\sigma_{IJ}\).
En consecuencia,
\begin{equation}
 S_{\rm red}=\frac1{2\kappa c}\int_M(R-2\Lambda)\operatorname{vol}_e
       +S_m^{\rm LC}
       -\frac14\int_M\mathfrak k_*^{IJ}\wedge\sigma_{IJ}
       +S_{\partial,\rm red}.
 \label{hmtcuatro:accion-reducida}
\end{equation}
La primera identidad de Bianchi anula el término Holst de
Levi--Civita en esta escritura. La regla de la cadena conserva las
ecuaciones de \(e,A,H,\Psi\), pues el coeficiente de
\(\delta\mathfrak k_*\) se anula por estacionariedad.
Como \(\sigma=\sum_s\sigma_s\), la contribución efectiva incluye
\(\mathfrak k_*[\sigma_s]\wedge\sigma_t\) para \(s\ne t\).
No se reemplaza por cuadrados de especies aisladas ni se conserva
simultáneamente la misma \(\mathfrak k\) como variable independiente.

\paragraph{2. Fuente completa y retroacción.}
Definamos el tensor de acción por la variación de todos los términos
materiales de \eqref{hmtcuatro:accion-reducida}:
\begin{equation}
 \delta_g S_{m,\rm red}=-\frac12\int_M
       \mathcal T^S_{\mu\nu}\,\delta g^{\mu\nu}\operatorname{vol}_e,
 \qquad
 E_{\mu\nu}:=G_{\mu\nu}+\Lambda g_{\mu\nu}
                   -\kappa c\,\mathcal T^S_{\mu\nu}.
 \label{hmtcuatro:fuente-completa}
\end{equation}
La ecuación métrica es \(E_{\mu\nu}=0\).
El factor \(\kappa c\) corresponde a la cotetrada de longitud;
si \(T^{\rm phys}=c\mathcal T^S\), se escribe \(\kappa T^{\rm phys}\).
Se varían también los campos materiales y las conexiones internas.
Por ello los campos determinan la fuente y la geometría que resuelve
la ecuación determina a su vez sus conexiones, volumen y evolución.
Ésta es retroacción, no evolución sobre un fondo fijado.
La variación incluye el volumen del potencial Higgs y la dependencia
métrica de la corriente torsional, además de sus términos cruzados.

\paragraph{3. Legendre restringida y reducción canónica.}
El potencial canónico total se obtiene de
\(\delta L=\mathcal E\delta z+\mathrm d\theta(\delta z)\),
integrando \(\theta\) sobre la hoja espacial y efectuando la reducción
de segunda clase. Su parte geométrica antes de esa reducción es
\[
 \theta_{\rm geom}(\delta)=
   \frac1{2\kappa c}(\mathsf P_\gamma\Sigma)_{IJ}
                       \wedge\delta\omega^{IJ}.
\]
La descomposición \(F_{0a}=\dot\omega_a-D_a\omega_0\), junto con la
misma descomposición de las acciones materiales, produce
\begin{equation}
 S_{\rm can}=\int d\tau\,
 \bigl[\Theta_{\rm red}(\dot z)-\mathcal C[N]-\mathcal D[\xi]
       -\mathcal G_{\rm L}[\lambda]-\mathcal G_{\rm int}[\chi]\bigr]
       +S_{\partial,\rm red}.
 \label{hmtcuatro:legendre-total}
\end{equation}
No se invierten artificialmente las velocidades ausentes de lapse,
shift o conexiones temporales.

La contorsión algebraica tiene restricciones
\(\pi_{\mathfrak k}=0\) y
\(\partial\mathcal Q/\partial\mathfrak k-\sigma/2=0\).
Su matriz de corchetes tiene el bloque
\[
 \begin{pmatrix}0&-M\\ M^T&B\end{pmatrix},
 \qquad M=\frac{\partial^2\mathcal Q}{\partial\mathfrak k^2}.
\]
La inversa torsional hace invertible \(M\), y por tanto esta matriz.
Son restricciones de segunda clase. Se usa
\begin{equation}
 \{F,G\}_D=\{F,G\}
       -\{F,\chi_a\}(C^{-1})^{ab}\{\chi_b,G\}.
 \label{hmtcuatro:corchete-dirac}
\end{equation}
En las variables que no dependen de la pareja contorsión--momento,
el bloque inferior derecho de \(C^{-1}\) es cero. No aparece por esa
eliminación un corchete suplementario entre ellas. Se retienen,
separadamente, las restricciones espinoriales de primer orden; en la
fase graduada se emplea el corchete graduado y los generadores pares.
\(\Theta_{\rm red}\) designa el resultado completo, no sólo su parte
geométrica.

La inversión de Legendre en direcciones regulares recupera la misma
acción. Por ejemplo, \(N[p^2/(2w)+wV+H_{\rm grad}]\), con
\(w=\sqrt{\det q}\), da \(p=(w/N)D_\tau\phi\), y por sustitución
\[
 L_H=\frac{w}{2N}|D_\tau\phi|^2-NwV-NH_{\rm grad}.
\]
\(D_\tau\) conserva shift y conexión temporal; \(w\) no se congela.
Para \(K_{ij}=(\dot q_{ij}-\mathcal L_\xi q_{ij})/(2N)\), la
contribución gravitatoria al momento y su inversa son
\begin{equation}
 \Pi^{ij}=\frac{\sqrt q}{2\kappa c}(K^{ij}-q^{ij}K),\qquad
 K_{ij}=\frac{2\kappa c}{\sqrt q}
                  (\Pi_{ij}-\tfrac12q_{ij}\Pi).
 \label{hmtcuatro:legendre-geometrica}
\end{equation}
De ellas resulta
\[
 \mathcal C_{\rm grav}
 =\frac{2\kappa c}{\sqrt q}
       (\Pi^{ij}\Pi_{ij}-\tfrac12\Pi^2)
  -\frac{\sqrt q}{2\kappa c}(R^{(3)}-2\Lambda).
\]
Si la carta de espinores aporta un desplazamiento material del momento
total \(p\), se usa \(\Pi=p-p_m\); no se descarta \(p_m\).
El carácter indefinido de la forma de DeWitt no impide esta inversa algebraica.
No se exige una inversa de velocidades a la cinética fermiónica de
primer orden.

\paragraph{4. Identidad Noether--Legendre y primera clase.}
La coincidencia de los generadores con las restricciones de la misma
acción puede verse antes de imponer sus ecuaciones.
Pónganse \(a=(2\kappa c)^{-1}\), \(B=\mathsf P_\gamma\Sigma\),
\(u^I=\iota_\zeta e^I\) y \(\lambda^{IJ}=\iota_\zeta\omega^{IJ}\).
De \(\mathcal L_\zeta\omega=\iota_\zeta F+D_\omega\lambda\) se obtiene
\begin{equation}
 \begin{split}
 j_\zeta^{\rm geom}
 ={}&\mathrm d(a B_{IJ}\lambda^{IJ})
   -a(D_\omega B_{IJ})\lambda^{IJ}\\
 &-2a u^Ie^J\wedge(\mathsf P_\gamma F)_{IJ}
       +2a\Lambda u^I\eta_I .
 \end{split}
 \label{hmtcuatro:noether-legendre}
\end{equation}
La parte material añade exactamente sus contribuciones a las
ecuaciones de \(e,\omega,A\), sus generadores verticales y su borde.
Descomponer la misma expresión en una hoja espacial da
\eqref{hmtcuatro:legendre-total}. La reducción estacionaria y la
reducción de Dirac transportan esas transformaciones, en vez de
sustituirlas por momentos de una acción externa.

Con la convención canónica usual para las restricciones, los corchetes
totales son, módulo los generadores Gauss conservados,
\begin{equation}
 \begin{aligned}
 \{\mathcal D[\xi],\mathcal D[\eta]\}_D
    &\simeq\mathcal D[[\xi,\eta]],\\
 \{\mathcal D[\xi],\mathcal C[N]\}_D
    &\simeq\mathcal C[\mathcal L_\xi N],\\
 \{\mathcal C[N],\mathcal C[M]\}_D
    &\simeq\mathcal D[
       q^{ij}(N\partial_jM-M\partial_jN)\partial_i].
 \end{aligned}
 \label{hmtcuatro:algebra-restricciones}
\end{equation}
En efecto, las transformaciones tangenciales tienen el corchete de
Lie, y transportan el lapse como escalar. Para las normales,
diferenciar su ortogonalidad con los vectores tangentes y
\(g(n,n)=-1\) determina la variación tangencial de \(n\);
con \(K_{ij}\) de \eqref{hmtcuatro:legendre-geometrica} se obtiene
\(\delta_N n=\operatorname{grad}_qN\). El conmutador de deformaciones,
convertido al corchete canónico con estas convenciones, da la última
línea de \eqref{hmtcuatro:algebra-restricciones}. El uso de transporte
covariantizado conserva además las rotaciones de marco y de calibre.
Las transformaciones son tangentes a la superficie de restricciones
de la acción invariante, de donde resulta la primera clase.
Las funciones \(q^{ij}\) dependen del estado y no se congelan.
Con soporte interior no se añade un cargo central de borde; un
generador impropio con cargo no nulo no se declara restricción cero.

\paragraph{5. Propagación en la geometría que responde a la materia.}
La invariancia por difeomorfías de \(S_{m,\rm red}\), evaluada sobre
sus ecuaciones materiales, da por integración por partes
\(\mathring\nabla^\mu\mathcal T^S_{\mu\nu}=0\). La identidad usa el
tensor completo de \eqref{hmtcuatro:fuente-completa}; no postula
conservación separada de cada contribución.
Bianchi implica entonces
\(\mathring\nabla_\mu E^{\mu\nu}=0\), aun antes de imponer
todas las ecuaciones métricas.

En una carta gaussiana local,
\(ds^2=-d\tau^2+q_{ij}dx^idx^j\), impongamos las ecuaciones
evolutivas \(E_{ij}=0\) y pongamos
\(C=E_{00}\), \(C_i=E_{0i}\),
\(K_{ij}=\dot q_{ij}/2\), \(K=q^{ij}K_{ij}\).
Aquí \(K\) es sólo la traza de la segunda forma fundamental.
Las dos componentes de la identidad divergente son
\begin{equation}
 \partial_\tau C-D_iC^i+KC=0,\qquad
 \partial_\tau C_i+KC_i=0.
 \label{hmtcuatro:propagacion}
\end{equation}
Para comprobar los signos se usan
\(E^{00}=C\), \(E^{0i}=-C^i\), \(E^{ij}=0\),
\(\Gamma^i{}_{0j}=K^i{}_j\) y
\(\Gamma^\mu{}_{\mu0}=K\). Al bajar el índice de la ecuación
espacial, \(\dot q_{ij}=2K_{ij}\) cancela los dos términos de conexión.
Si inicialmente \(C_i=0\), su ecuación homogénea mantiene \(C_i=0\);
la primera queda \(\dot C+KC=0\) y conserva \(C=0\).
\(q\) y \(K\) son los de la solución acoplada. La elección gaussiana
prueba la afirmación local; su forma tensorial permite cambiar lapse
y shift. Análogamente, la identidad gauge de Noether relaciona la
divergencia covariante de la ecuación de calibre con las ecuaciones
materiales y propaga Gauss cuando se cumplen las ecuaciones espaciales.
No se infiere existencia global ni ausencia de singularidades de
toda solución.

\paragraph{6. La misma acción induce el cierre característico.}
Sea \(\mathcal P_{\rm red}\) la carta canónica regular obtenida y
\(\mathcal Z=\{C_A=0\}\) su superficie regular de restricciones
totales, incluida Gauss. Usamos un símbolo distinto de \(\Sigma^{IJ}\)
para esa superficie. Se conserva el potencial \(\Theta=\Theta_{\rm red}\)
de \eqref{hmtcuatro:legendre-total}, incluidos los términos materiales
y mixtos. Fijamos
\begin{equation}
 \Omega=-\mathrm d_{\mathcal P}\Theta,\qquad
 \iota_{X_f}\Omega=\mathrm d_{\mathcal P}f,\qquad
 \{f,g\}_D=\Omega(X_f,X_g).
 \label{hmtcuatro:convenciones-simpecticas}
\end{equation}
En una pareja canónica, \(\Theta=p\,\mathrm dq\) da
\(X_f=f_p\partial_q-f_q\partial_p\), \(\{q,p\}_D=1\),
\(X_f(g)=-\{f,g\}_D\) y
\([X_f,X_g]=-X_{\{f,g\}_D}\). En la fase graduada esta escritura
se aplica a las funciones y restricciones pares pertinentes.

En la línea de fase trivializada sobre esta carta, construimos
\begin{equation}
 \nabla_X=X-\frac{i}{\hbar}\Theta(X)
       =\delta_X+\frac{i}{\hbar}H_X^{\rm can},
 \qquad H_X^{\rm can}=-\Theta(X).
 \label{hmtcuatro:conexion-canonica}
\end{equation}
No se escoge una conjugación arbitraria para hacerla plana:
su coeficiente proviene del potencial de la acción.
Para cualesquiera campos \(X,Y\) de la carta, el cálculo da
\begin{equation}
 \begin{aligned}
 \mathcal F^{\rm can}_{X,Y}
 &=XH_Y^{\rm can}-YH_X^{\rm can}-H_{[X,Y]}^{\rm can}
       +\frac{i}{\hbar}[H_X^{\rm can},H_Y^{\rm can}]\\
 &=-X\Theta(Y)+Y\Theta(X)+\Theta([X,Y])\\
 &=-\mathrm d_{\mathcal P}\Theta(X,Y)=\Omega(X,Y).
 \end{aligned}
 \label{hmtcuatro:curvatura-calculada}
\end{equation}
Los \(H_X^{\rm can}\) son multiplicadores de la línea, por lo que
su conmutador es cero; las derivadas de los coeficientes y de los
campos no se suprimen.

La primera clase ya probada significa
\(\{C_A,C_B\}_D=f_{AB}{}^D C_D\).
Para \(V\) tangente a \(\mathcal Z\),
\(\Omega(X_{C_A},V)=\mathrm d_{\mathcal P}C_A(V)=0\).
Los campos de las restricciones son, por tanto, característicos.
Bajo la regularidad declarada generan la distribución característica
de la superficie coisótropa. La tensorialidad de \(\Omega\) extiende
el cálculo a todas sus combinaciones suaves y prueba
\begin{equation}
 \left.\mathcal F^{\rm can}_{X,Y}\right|_{\mathcal Z}=0
 \quad\hbox{para }X,Y\hbox{ característicos}.
 \label{hmtcuatro:cierre-caracteristico}
\end{equation}
Para dos lapsos se incluye en \([X,Y]\) la deformación tangencial
y las acciones Gauss de \eqref{hmtcuatro:algebra-restricciones}.
Si se pasa al cociente gauge, la igualdad se expresa módulo esas
acciones verticales. No se afirma que \(\Omega\) sea cero en toda
la fase ni que toda holonomía global de una hoja sea trivial.

\paragraph{7. Expresión precuántica del mismo cierre.}
La realización diferencial asociada a
\eqref{hmtcuatro:conexion-canonica}, sobre secciones suaves donde
están definidos los productos, es
\begin{equation}
 Q_{\rm pre}(f)=-i\hbar\nabla_{X_f}+f
            =-i\hbar X_f+f-\Theta(X_f).
 \label{hmtcuatro:operador-precuantico}
\end{equation}
Con \(R^\nabla=(i/\hbar)\Omega\), la expansión del conmutador y
\(X_f(g)=-\{f,g\}_D\) dan
\begin{equation}
 [Q_{\rm pre}(f),Q_{\rm pre}(g)]
           =i\hbar Q_{\rm pre}(\{f,g\}_D).
 \label{hmtcuatro:representacion-precuantica}
\end{equation}
La regla de producto que conserva las funciones de estructura es
\begin{equation}
 Q_{\rm pre}(aC)
   =aQ_{\rm pre}(C)+C\bigl(Q_{\rm pre}(a)-a\bigr).
 \label{hmtcuatro:funciones-estructura}
\end{equation}
Se deduce de \(X_{aC}=aX_C+CX_a\) y de
\eqref{hmtcuatro:operador-precuantico}. No se elimina el segundo
término fuera de \(\mathcal Z\).
Sobre \(\mathcal Z\), \(Q_{\rm pre}(C_A)=-i\hbar\nabla_{X_{C_A}}\);
así \eqref{hmtcuatro:representacion-precuantica} y
\eqref{hmtcuatro:cierre-caracteristico} son las expresiones operatoria
y geométrica del mismo cierre canónico, no dos incorporaciones
independientes de gravedad.
\end{proof}

\subsection{Dominio del resultado y comparación de realizaciones}
\label{hmtcuatro:alcance-canonico}

La prueba reúne una acción con gravedad dinámica y fuente conjunta,
su Legendre y su conexión característica. El calificativo
\emph{arbitrario} para las deformaciones se refiere a los lapsos y
desplazamientos admisibles que generan direcciones características en
esa región regular; no a cualquier vector de fase, cualquier borde
o cualquier solución singular. La planitud local conserva la posible
monodromía global y no identifica dos historias TPK por tener iguales
extremos.

El coeficiente \(H_X^{\rm can}\) de una conexión de línea no es por
definición el operador de reloj y respuesta \(H_{\rm clk}+D^*WD\),
ni su extensión interactuante. \(Q_{\rm pre}(C)\) incluye además
una derivación en la fase; tampoco es un nombre alternativo de esos
operadores. Para identificar una realización concreta mediante un
mapa \(I\) se requiere la igualdad tipada
\[
 \nabla_N^{\rm op}I=I\nabla_N^{\rm can}
\]
sobre sus dominios efectivos. Si \(I\) depende de la geometría, su
derivada forma parte de esta igualdad.

La distinción tiene un control exacto: en la carta
\(\Theta=p\,\mathrm dq\),
\begin{equation}
 Q_{\rm pre}(p^2/2)=-i\hbar p\,\partial_q-p^2/2.
 \label{hmtcuatro:control-polarizacion}
\end{equation}
Al actuar sobre la función \(1\), produce \(-p^2/2\).
Por tanto no preserva por mera restricción la polarización de
funciones independientes de \(p\), y no es allí
\(-\hbar^2\partial_q^2/2\). El control no refuta el Hamiltoniano
recibido: impide sustituir una representación por otra sin su mapa.

No se ha supuesto una medida de Liouville infinito-dimensional ni
se deduce autoadjunción de las identidades diferenciales anteriores.
Si inclusiones de refinamiento entrelazan las conexiones y conservan
un núcleo común, sus curvaturas se entrelazan por composición; un
límite exige además los controles de dominio y convergencia propios.
No se presenta aquí esa condición como comprobada para el operador
interactuante y el límite espacial--quiral conjunto. Las construcciones
cuánticas anteriores se conservan; el resultado presente precisa
exactamente el cierre canónico que se acaba de demostrar.
```

## 40_conclusion_integracion.tex

Ruta: `copia_vii/integracion_20260930/40_conclusion_integracion.tex`

SHA-256: `4b11bec3ff6944cd6130e4f513306ab24c430fe00ebc580e09b5134a17a47fe3`

```latex
% Adición a las conclusiones de VII; las conclusiones anteriores se conservan.
\paragraph{Integración de las cuatro interacciones y cierre canónico total.}
La gravitación y las interacciones fuerte, débil y electromagnética
actúan sobre una misma realización material de la estructura
APP--TRIT--TPK. El transporte conserva las hojas, la orientación,
la memoria y la incidencia del estado enriquecido; sus realizaciones
de espín y calibre se componen sobre las mismas fibras materiales.
La componente electromagnética pertenece a la realización
electrodébil: no se introduce como una interacción adicional
desconectada de ella. La acción total utiliza los coeficientes y
lectores ya construidos, incluidos la sección de Planck, la longitud
radial y el funcional de Barbero--Immirzi.

El contenido de esta integración no se limita a reunir términos en
una expresión. La variación de la misma acción produce la corriente
total de espín y la fuente métrica conjunta. La eliminación de la
contorsión conserva los términos cruzados entre especies; la
transformación de Legendre conserva los momentos materiales y
produce las restricciones totales. Las pruebas de las
secciones~\ref{hmtcuatro:gea:seccion}
y~\ref{hmtcuatro:accion-retroaccion-restricciones}
establecen la retroacción, la primera clase y la propagación de
esas restricciones en la realización regular especificada.

En particular, sea $\Theta_{\rm tot}$ el potencial canónico total
obtenido en esa transformación, $\mathcal Z=\{C_A=0\}$ la superficie
regular de restricciones y $X_N=N^AX_{C_A}$,
$X_M=M^BX_{C_B}$ dos deformaciones características admisibles.
La conexión inducida por la acción tiene
$H_N^{\rm tot,can}=-\Theta_{\rm tot}(X_N)$. Su curvatura, calculada
sin omitir las derivadas de los coeficientes de deformación, es
\begin{equation}
\begin{aligned}
\mathcal F^{\rm tot,can}_{N,M}
&=\delta_NH_M^{\rm tot,can}-\delta_MH_N^{\rm tot,can}
 -H_{[X_N,X_M]}^{\rm tot,can}
 +\frac{i}{\hbar}[H_N^{\rm tot,can},H_M^{\rm tot,can}]\\
&=-\mathrm d\Theta_{\rm tot}(X_N,X_M)
 =N^AM^B f_{AB}{}^{D}C_D.
\end{aligned}
\label{hmtcuatro:conclusion-curvatura-total}
\end{equation}
Por tanto,
\[
 \left.\mathcal F^{\rm tot,can}_{N,M}\right|_{\mathcal Z}=0.
\]
La fórmula incluye la deformación tangencial y las acciones de
calibre del corchete total; si se trabaja en el cociente, expresa
la misma igualdad módulo esas direcciones verticales. La
representación precuántica conserva este cierre mediante la
identidad de conmutadores demostrada en
\eqref{hmtcuatro:representacion-precuantica}.

Así, la incorporación gravitatoria es parte de la misma acción,
de sus fuentes y de su álgebra de restricciones, no una ecuación
yuxtapuesta después de construir las otras interacciones. La
anulación probada es la de la curvatura característica canónica;
no exige que sean nulas la curvatura del espacio-tiempo ni las
intensidades de los campos de calibre. Su dominio conserva el
coframe no degenerado, la carta regular y las condiciones de
borde utilizadas en la prueba. Tampoco suprime la memoria ni la
monodromía global de las historias que dieron lugar a la
realización.
```
