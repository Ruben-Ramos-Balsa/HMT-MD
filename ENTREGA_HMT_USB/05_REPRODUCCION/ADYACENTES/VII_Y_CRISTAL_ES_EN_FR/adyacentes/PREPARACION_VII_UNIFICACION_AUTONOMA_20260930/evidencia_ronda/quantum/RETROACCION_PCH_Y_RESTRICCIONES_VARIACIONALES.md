# Retroacción PCH–materia y compatibilidad de las restricciones variacionales

Composición focal del 29 de septiembre de 2026. La métrica ya construida
es aquí variable dinámica. No se solicita otra geometría ni se vuelve a
auditar su generación. Se reúnen la acción, su Legendre y una prueba
explícita de propagación de restricciones con la fuente total.

## 1. Antecedente y propietarios que ya contienen el acoplamiento

Se conserva la genealogía APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo del
[recibo vigente](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/RECIBO_GENEALOGIA.json>).
Ruta, hojas, orientación, memoria, acarreo y frontera preceden a la
realización geométrica. Los acoplamientos y secciones dimensionales
son salidas recibidas; ninguna magnitud objetivo selecciona la acción.

Los localizadores que se componen son:

- [VIII/30d](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30d_realizacion_geometrica.tex>), líneas 16–58: soldadura, coframe y holonomía realizada, incluido el lift de espín.
- [VIII/31](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex>), `vii:eq:accion-cartan-holst`, `vii:eq:ecuacion-cartan-holst`: acción y corriente; líneas 315–374: eliminación algebraica y borde; líneas 385–452: variación métrica de la fuente total y Noether.
- [VIII/33](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex>), líneas 50–119: acción espinorial en esa geometría; `vii:eq:coeficiente-cuadratico-espinorial`: interacción de corriente al eliminar contorsión.
- [11p](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex>), `eq:hamiltoniano-total-gravedad-hmt-rev11`: Legendre restringida de la misma acción.
- [INTEGRACION_MATEMATICA.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/INTEGRACION_MATEMATICA.md>), §5.1: conexiones SU(3), SU(2), U(1), acción Higgs–Weyl–Yukawa y prueba de equivariancia del mapa material.
- [HAMILTONIANO_FINITO_HIGGS_FOCK.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/HAMILTONIANO_FINITO_HIGGS_FOCK.md>), §§3 y 8: campos quirales recibidos, Higgs variable, energía de vacío retenida y corriente total con términos cruzados.

El dominio variacional es el ya declarado por 31: coframe no
degenerado, sección real γ≠0, acoplamientos fijos durante la variación,
materia afín en la contorsión y variaciones interiores o completación
de borde compatible. En el argumento canónico se trabaja en la carta
regular de la Legendre restringida de 11p. No se pretende invertir
las direcciones de lapse, shift o calibre que esa misma acción hace
degeneradas.

## 2. Misma acción, métrica variable y fuente conjunta

Con \(a=(2\kappa c)^{-1}\), \(\Sigma=e\wedge e\) y
\(P_\gamma=\star+\gamma^{-1}\), la acción recibida y compuesta es

\[
 S_{\rm tot}=a\int\Sigma_{IJ}\wedge(P_\gamma F_\omega)^{IJ}
 -2a\Lambda\int\mathrm{vol}_e
 +S_{\rm YM}[e,A]+S_H[e,A,H]
 +S_W[e,\omega,A,\Psi]+S_Y[e,H,\Psi].
 \tag{1}
\]

Las curvaturas y conexiones internas, sus normalizaciones y el mapa
Yukawa son los de la composición citada. La igualdad
\(Y(gH)\rho_R(g)=\rho_L(g)Y(H)\) prueba que el término material
usa la misma acción gauge. Todos sus índices espaciotemporales se
contraen con la misma e, que se varía: (1) no es una evolución de
campos sobre una métrica fijada externamente.

Escribamos \(\omega=\mathring\omega(e)+\mathfrak k\). La parte
dependiente de contorsión es la forma algebraica de 31,

\[
 Q_{e,\gamma}(\mathfrak k)-\tfrac12\mathfrak k^{IJ}\wedge\sigma_{IJ},
 \qquad \sigma=\sum_s\sigma_s.
 \tag{2}
\]

La inversión explícita de 31 determina una única
\(\mathfrak k_*[e,\sigma]\). El resultado es

\[
 \boxed{S_{\rm red}=
 \frac1{2\kappa c}\int(R[g]-2\Lambda)\mathrm{vol}_e
 +S_m^{\rm LC}[e,A,H,\Psi]
 -\frac14\int\mathfrak k_*^{IJ}\wedge\sigma_{IJ}
 +S_\partial[e,\mathfrak k_*].}
 \tag{3}
\]

El último término se conserva o se sustituye por la completación de
borde de la misma variación. Puesto que \(\mathfrak k_*\) es lineal
en la corriente total, el término efectivo contiene las contribuciones
\(\mathfrak k_*[\sigma_s]\wedge\sigma_t\) entre especies, no sólo
sus cuadrados separados. No se vuelve a introducir la contorsión
eliminada como variable independiente en (3).

Definiendo \(\mathcal T^S_{\mu\nu}\) mediante la variación de **todos**
los términos materiales de (3), incluido el término de corriente,

\[
 \delta_g S_{m,\rm red}
 =-\tfrac12\int\mathcal T^S_{\mu\nu}\delta g^{\mu\nu}\mathrm{vol}_e,
 \qquad
 G_{\mu\nu}+\Lambda g_{\mu\nu}=\kappa c\mathcal T^S_{\mu\nu}.
 \tag{4}
\]

Las restantes variaciones dan a la vez las ecuaciones gauge, Higgs y
espinoriales con esa métrica y esa interacción de corriente. Ésta es
la retroacción: los campos determinan la fuente de (4), y la geometría
que resuelve (4) determina sus conexiones, volumen y propagación. No se
elige un tensor externo para cerrar la ecuación métrica. Tampoco se
resta silenciosamente la constante del potencial Higgs: su variación
de volumen contribuye a (4).

## 3. Recuperar Lagrangiano desde Hamiltoniano conserva la misma dinámica

La formulación de primer orden siempre retiene la información de
Legendre en su forma canónica:

\[
 S_{\rm can}=\int d\tau\,[\Theta_{\rm red}(z)(\dot z)
 -\mathcal C[N]-\mathcal D[\xi]-\mathcal G[\lambda]]+S_\partial.
 \tag{5}
\]

\(\Theta_{\rm red}\) es el potencial obtenido de la **misma** acción,
con las reducciones de segunda clase incluidas. No se presupone que
la forma simpléctica geométrica y la material permanezcan separadas
en una carta donde el marco de los espinores depende de e.

En una dirección bosónica regular, variar los momentos en (5) recupera
\(\dot q=\partial H/\partial p\); sustituir su inversa devuelve el
Lagrangiano correspondiente. Por ejemplo, para las coordenadas reales
del Higgs recibidas, un término

\[
 H_H=N\left(\frac{p^2}{2w}+wV+H_{\rm grad}\right),
 \qquad w=\sqrt{\det q}\ \text{en la carta de volumen},
\]

da \(p=(w/N)D_\tau\phi\) y

\[
 L_H=\frac{w}{2N}|D_\tau\phi|^2-NwV-NH_{\rm grad}.
 \tag{6}
\]

La derivada Dτ contiene shift y conexión temporal. El volumen w es
variable geométrica; variar (6) respecto de él y de q conserva la
fuente de (4). No se congela al reconstruir el Lagrangiano.

Para la parte geométrica, usando un parámetro de foliación compatible
con la recta de longitud del coframe y
\(K_{ij}=(\dot q_{ij}-\mathcal L_\xi q_{ij})/(2N)\), la contribución
gravitatoria al momento es

\[
 \Pi^{ij}=\frac{\sqrt q}{2\kappa c}(K^{ij}-q^{ij}K),\qquad
 K_{ij}=\frac{2\kappa c}{\sqrt q}
             (\Pi_{ij}-\tfrac12q_{ij}\Pi).
 \tag{7}
\]

La inversa existe en los seis componentes simétricos aunque la forma
de DeWitt no sea positiva. La restricción geométrica correspondiente
es

\[
 \mathcal C_{\rm grav}=
 \frac{2\kappa c}{\sqrt q}(\Pi^{ij}\Pi_{ij}-\tfrac12\Pi^2)
 -\frac{\sqrt q}{2\kappa c}(R^{(3)}-2\Lambda).
 \tag{8}
\]

Π en (7)–(8) denota la contribución geométrica. Si la carta material
añade una conexión al momento total p, se sustituye Π=p−p_m; no se
descarta p_m. Los espinores de primer orden conservan sus restricciones
canónicas en vez de exigirles una inversa de velocidades inexistente.
Así se recupera el Lagrangiano sin perder la dependencia geométrica ni
confundir esa operación con la selección de una acción diferente.

## 4. Reducción de segunda clase y restricciones de primera clase

La contorsión de (2) no tiene velocidad después de conservar la
divergencia de borde declarada. Sus restricciones son

\[
 \pi_{\mathfrak k}=0,\qquad
 \chi_{\mathfrak k}=\partial Q/\partial\mathfrak k-\sigma/2=0.
 \tag{9}
\]

El bloque mixto de su matriz de Poisson es el Hessiano algebraico
de Q, invertible por las inversas torsionales de 31. La matriz completa
tiene la forma
\(\left(\begin{smallmatrix}0&-M\\M^T&B\end{smallmatrix}\right)\)
con M invertible, luego también es invertible. Por tanto (9) es un
par de segunda clase, no una restricción gravitatoria física nueva.
El corchete de Dirac

\[
 \{F,G\}_D=\{F,G\}-\{F,\chi_a\}(C^{-1})^{ab}\{\chi_b,G\}
 \tag{10}
\]

realiza su eliminación canónica. Para funciones de las variables
restantes, que no dependen de la pareja contorsión–momento, el bloque
inferior derecho de C⁻¹ es cero; esta eliminación no inventa un
corchete adicional entre esas variables. Se conservan separadamente
las restricciones fermiónicas de primer orden y su corchete graduado
cuando los campos son impares. Su matriz procede del producto de
corriente no degenerado. La reducción completa es la que define
\(\Theta_{\rm red}\) en (5).

**Teorema de compatibilidad canónica total.** En el sector regular
de (3)–(5), los generadores totales de difeomorfías y calibre son de
primera clase respecto del corchete reducido. Para parámetros de
soporte interior, sus corchetes de hipersuperficie tienen, módulo
Gauss, la forma

\[
 \begin{aligned}
 \{\mathcal D[\xi],\mathcal D[\eta]\}_D
   &\simeq\mathcal D[[\xi,\eta]],\\
 \{\mathcal D[\xi],\mathcal C[N]\}_D
   &\simeq\mathcal C[\mathcal L_\xi N],\\
 \{\mathcal C[N],\mathcal C[M]\}_D
   &\simeq\mathcal D[q^{ij}(N\partial_jM-M\partial_jN)\partial_i].
 \end{aligned}
 \tag{11}
\]

Se usa la convención canónica en que D genera el Lie de los campos
espaciales y una normal temporal de norma −1. Los términos verticales
se conservan si se utiliza el generador covariantizado en lugar del
Lie ordinario.

**Prueba.** La acción (1) es covariante y la eliminación estacionaria
conserva esa covariancia. Sus corrientes de Noether son los generadores
de (5), como muestra la identidad Noether–Legendre ya reunida. La
reducción de segunda clase transporta su acción a la forma simpléctica
reducida: no cambia el álgebra de las transformaciones que preservan
la superficie eliminada. Dos transformaciones tangenciales tienen el
corchete de Lie; una tangencial transporta N como escalar. Para dos
normales, variar la ortogonalidad y la norma de la normal da
\(\delta_Nn=\operatorname{grad}_qN\) con la convención temporal
empleada; su conmutador es tangencial y la conversión canónica produce
la última línea de (11). La métrica q varía con el estado: no se
congela la función de estructura q⁻¹. Las diferencias verticales son
los generadores Gauss de la misma acción. Al ser transformaciones
gauge de una acción covariante, son tangentes a su superficie de
restricciones, lo que prueba primera clase. En el dominio interior
no se añade un cargo central de borde. ∎

Si hay un borde físico, los generadores diferenciables contienen sus
cargos, y el álgebra incluye su contribución. El resultado no los
suprime: coincide con el problema variacional interior o con la
completación de borde de 31. No se utiliza una transformación gauge
impropia con cargo no nulo como si fuera una restricción cero.

## 5. Prueba explícita de propagación con retroacción

Definamos el residuo métrico de la ecuación total,

\[
 E_{\mu\nu}=G_{\mu\nu}+\Lambda g_{\mu\nu}
                   -\kappa c\mathcal T^S_{\mu\nu}.
 \tag{12}
\]

La covariancia de la acción material reducida implica
\(\nabla^\mu\mathcal T^S_{\mu\nu}=0\) **sobre sus ecuaciones
materiales**, incluso antes de imponer E=0. Junto con Bianchi,
\(\nabla_\mu E^{\mu\nu}=0\). Ésta es la identidad Noether de la
fuente conjunta de 31; incluye gauge, Higgs, Yukawa y corriente.

**Proposición.** Toda solución regular de las ecuaciones materiales
y de las ecuaciones evolutivas métricas, cuyos datos iniciales
satisfacen las restricciones, conserva dichas restricciones durante
su evolución regular.

**Prueba local sin congelar la métrica.** En coordenadas gaussianas
\(ds^2=-d\tau^2+q_{ij}(\tau,x)dx^idx^j\), impónganse las
ecuaciones evolutivas \(E_{ij}=0\), y escríbanse

\[
 C=E_{00},\quad C_i=E_{0i},\quad
 K_{ij}=\tfrac12\dot q_{ij},\quad K=q^{ij}K_{ij}.
\]

Aquí K es la traza de la segunda forma fundamental, no el registro
dodecafásico ni una matriz de densidad de corriente. Las dos componentes
de \(\nabla_\mu E^{\mu\nu}=0\) son exactamente

\[
 \boxed{\partial_\tau C-D_iC^i+KC=0,\qquad
        \partial_\tau C_i+KC_i=0.}
 \tag{13}
\]

Para verificarlo, se usan \(E^{00}=C\), \(E^{0i}=-C^i\),
\(E^{ij}=0\), \(\Gamma^i{}_{0j}=K^i{}_j\) y
\(\Gamma^\mu{}_{\mu0}=K\). En la ecuación de C_i, la derivada
\(\dot q_{ij}=2K_{ij}\) cancela los dos términos de conexión al
bajar el índice. Si C_i es inicialmente cero, su ecuación ordinaria
homogénea lo mantiene cero en cada punto; la primera ecuación queda
\(\dot C+KC=0\), que conserva C=0. Toda la geometría q(τ,x) y
su K son los de la solución acoplada, no un fondo prescrito. ∎

La elección gaussiana sirve sólo para demostrar la afirmación local;
la identidad tensorial y la propagación se conservan al cambiar lapse
y shift. La invariancia gauge da análogamente una identidad entre la
divergencia covariante de la ecuación Yang–Mills y las ecuaciones
materiales. Si se imponen sus ecuaciones espaciales, la ecuación Gauss
temporal evoluciona homogéneamente y se conserva desde los datos.

No se ha afirmado existencia global sin singularidades de toda
solución: el resultado es una identidad exacta de compatibilidad
y propagación sobre la solución regular de la misma acción. Esa
distinción no añade otra métrica ni una interacción por construir.

## 6. Resultado y relación con la realización cuántica

Queda cerrada en este dominio la incorporación variacional y canónica
de la gravedad **dinámica**: misma acción, retroacción de todos sus
campos, eliminación torsional consistente, Legendre recuperable,
reducción de segunda clase y propagación de las restricciones totales.
No es únicamente una suma de etiquetas ni una covariancia de campos
sobre un fondo fijo.

Las construcciones cuánticas anteriores siguen formando parte del
acumulado. Esta prueba precisa el acoplamiento variacional que debe
representar su operador, pero un corchete de Dirac clásico no es por
sí mismo una igualdad de conmutadores cuánticos sobre un dominio
común. No se presenta (11) como el cálculo completo de la curvatura
operatoria cuántica \(\mathcal F_{NM}\). Esa separación es entre
dos resultados matemáticos tipados, no una etiqueta global
«clásico/cuántico» impuesta al corpus HMT.

El [verificador focal](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/verificar_retroaccion_restricciones.py>) calcula los Christoffel desde q y dot q,
conserva la derivada de q⁻¹ al levantar el índice del residuo, y
comprueba (13) mediante 36 identidades racionales. La prueba de
propagación es la de §5; los controles fijan sus signos y cancelaciones.
