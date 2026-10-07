# La conexión de la acción total: cálculo y rectificación del alcance

## Procedencia conservada

APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo.
Las hojas, orientación, acarreo, rutas, supervivencia, frontera y memoria se
conservan en la composición. Las constantes son salidas HMT recibidas; no se
escogen para hacer cero la curvatura. El reconocimiento convencional posterior
es aquí el cálculo variacional y de conexiones sobre la realización geométrica
del transporte ya construido. No se sustituye la holonomía nonádica por una
conexión trivial ni se identifican historias que tienen los mismos extremos.

Esta nota añade una rectificación a los desarrollos anteriores, sin borrarlos.
No cambia los manuscritos publicados ni el paquete sellado del 30 de septiembre.
El antecedente probatorio inmediato es el fragmento
`20_accion_retroaccion_restricciones.tex`, con su acción, dominios, reducción
torsional, Legendre, álgebra de restricciones y prueba característica completas.

## 1. Qué objeto se calcula

La acción reunida contiene la cotetrada y la conexión de espín dinámicas, los
campos de color y electrodébiles, el campo Higgs, la materia quiral y sus mapas
de Yukawa. Todos utilizan la misma geometría. La eliminación estacionaria de
la contorsión se hace con la **corriente total**, conservando sus productos
cruzados; el potencial del Higgs conserva su término de volumen. Por ello el
potencial canónico reducido \(\Theta_{\rm tot}\) no es el de la gravedad
aislada, ni la fuente gravitatoria es la de un campo de prueba.

En la carta regular de esa acción, después de la reducción de segunda clase,
se tiene

\[
 \Omega_{\rm tot}=-d\Theta_{\rm tot},\qquad
 \iota_{X_f}\Omega_{\rm tot}=df,\qquad
 \{f,g\}_D=\Omega_{\rm tot}(X_f,X_g).
\]

Sean \(C_A\) las restricciones totales y \(\mathcal Z=\{C_A=0\}\) su
superficie regular. La primera clase demostrada para esa misma acción es

\[
 \{C_A,C_B\}_D=f_{AB}{}^C C_C.
\]

Los coeficientes de estructura conservan su dependencia geométrica. Las
variaciones tienen soporte interior, o el borde compatible especificado por
la acción. Una carga física de borde no se elimina denominándola restricción.

Para una deformación admisible \(N\), sea \(X_N\) su campo característico.
Con \(\hbar_{\rm HMT}\) fija en esta variación se define la conexión que
produce el potencial de la acción:

\[
 \nabla_N=X_N-\frac{i}{\hbar_{\rm HMT}}\Theta_{\rm tot}(X_N),
 \qquad H_N^{\rm tot,can}=-\Theta_{\rm tot}(X_N).
\]

El superíndice «total» incluye todos los sectores de la acción. «can» identifica
la realización concreta; no oculta una identificación con otro Hamiltoniano.

## 2. Cálculo de la curvatura total

En la fórmula solicitada, \(\delta_N=X_N\) y \([N,M]\) significa el
corchete de las deformaciones realizadas, incluidas sus componentes tangencial
y de calibre. Al ser coeficientes de una conexión de línea, los multiplicadores
\(H_N^{\rm tot,can}\) conmutan. No se omiten las derivadas de sus coeficientes:

\[
\begin{aligned}
 \mathcal F^{\rm tot,can}_{N,M}
 &=X_NH_M^{\rm tot,can}-X_MH_N^{\rm tot,can}
   -H_{[N,M]}^{\rm tot,can}
   +\frac{i}{\hbar_{\rm HMT}}
       [H_N^{\rm tot,can},H_M^{\rm tot,can}]\\
 &=-X_N\Theta_{\rm tot}(X_M)+X_M\Theta_{\rm tot}(X_N)
      +\Theta_{\rm tot}([X_N,X_M])\\
 &=-d\Theta_{\rm tot}(X_N,X_M)
   =\Omega_{\rm tot}(X_N,X_M).
\end{aligned}
\]

Si \(X_N=u^A X_{C_A}\) y \(X_M=v^B X_{C_B}\), la tensorialidad de la
forma exterior da, incluso cuando \(u,v\) dependen del estado,

\[
 \mathcal F^{\rm tot,can}_{N,M}
 =u^A v^B f_{AB}{}^C C_C,
 \qquad
 \boxed{\left.\mathcal F^{\rm tot,can}_{N,M}\right|_{\mathcal Z}=0.}
\]

La identidad fuera de \(\mathcal Z\) se refiere a esas extensiones de los
campos; si se toman \(X_{u^AC_A}\), aparecen además términos proporcionales
a las restricciones, que también se anulan al restringir. No se confunden las
dos extensiones fuera de la superficie. La prueba sobre \(\mathcal Z\) vale
para todas las combinaciones suaves de sus direcciones características.

Así, la anulación se deduce de la **acción total y su primera clase**; no se
introduce como una condición elegida a posteriori. Tampoco afirma que la forma
simpléctica sea cero en toda la fase. La planitud característica local es
compatible con memoria y monodromía global no trivial.

Esta \(\mathcal F_{N,M}\) es la curvatura de compatibilidad entre
deformaciones, no el tensor de Riemann ni las intensidades de campo
electromagnética, débil o fuerte. Su anulación no elimina ninguna interacción.

## 3. Expresión operatoria asociada

En el dominio de secciones suaves de la carta, el operador diferencial
asociado es

\[
 Q(f)=-i\hbar_{\rm HMT}\nabla_{X_f}+f.
\]

La expansión, con \(X_f(g)=-\{f,g\}_D\), da

\[
 [Q(f),Q(g)]=i\hbar_{\rm HMT}Q(\{f,g\}_D),
 \qquad
 Q(aC)=aQ(C)+C\bigl(Q(a)-a\bigr).
\]

Sobre \(\mathcal Z\), \(Q(C_A)=-i\hbar_{\rm HMT}\nabla_{X_{C_A}}\).
Es la realización diferencial del mismo cierre; no basta sustituir un
subíndice para convertirla en una representación de campos distinta. Esta
precisión identifica el operador probado, no retira el acoplamiento de la
gravedad ni su fuente conjunta.

## 4. Rectificación de la exigencia añadida en esta ronda

El operador \(h_x\), y \(H_{\rm loc}=\bigoplus_xh_x\), de las notas del
29 de septiembre es una realización interactuante adicional construida en
esta ronda. No es una transcripción literal del \(\mathcal Q(H_{\rm tot})\)
de 11p. Sus propietarios lo declaran expresamente; conserva, entre otros
términos, el operador de respuesta de segundo orden \(D_T^*WD_T\).

Por tanto, comparar ese \(h_x\) con la conexión anterior es pertinente si se
afirma que **ambas realizaciones son la misma**. No es una condición retrospectiva
para la acción conjunta, su fuente total, el cierre calculado arriba, las
relaciones radiales o los observables espinoriales ya demostrados. Convertir
esa comparación adicional en el centro del encargo anterior fue un error de
alcance. La comparación se conserva como extensión identificada, no se borra
ni se presenta como refutación de los resultados anteriores.

Tampoco se cambia silenciosamente el significado del operador para afirmar
un resultado mayor: la igualdad enmarcada corresponde exactamente a la
conexión total definida en §1. No es, por sí sola, una prueba de identidad
con cualquier regularización espacial o Hamiltoniano posterior.

## 5. Localizadores materiales e inserción

- Prueba reunida: [acción total y cierre](</Users/ruben/Documents/New project/output/ENTREGA_INTEGRACION_GRAVEDAD_CUATRO_INTERACCIONES_20260930/latex/20_accion_retroaccion_restricciones.tex>), etiquetas `hmtcuatro:accion-total`, `hmtcuatro:algebra-restricciones`, `hmtcuatro:curvatura-calculada`, `hmtcuatro:cierre-caracteristico` y `hmtcuatro:representacion-precuantica`.
- [Realización geométrica de VIII](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/30d_realizacion_geometrica.tex:30>): mapa de holonomía del transporte, composición, inversión y subdivisión.
- [Corriente y respuesta Cartan](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex>) y [realización espinorial](</Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex>).
- [Propietario integral 11p](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex:7>): realización mediante espacio, dominio y mapa \(\mathcal Q\); no identifica por nombre el \(h_x\) posterior.
- [Realización adicional Higgs–Fock](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/HAMILTONIANO_FINITO_HIGGS_FOCK.md:18>) y [evolución acoplada](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/EVOLUCION_ACOPLADA_Y_LIMITE.md:9>): procedencia del operador nuevo.

La demostración de acción y cierre se inserta en «Gravitación, torsión y
dinámica cosmológica» después de la sección 33 y antes de `50_dilucion_y_rebote`.
La comparación con \(h_x\) permanece aparte; no interrumpe la conclusión del
resultado que acaba de probarse. Las relaciones radiales y autoinerciales se
insertan en «Relaciones estructurales entre las constantes físicas» después
de `normalizacion_conjunta`. Esta nota no ejecuta esas inserciones.
