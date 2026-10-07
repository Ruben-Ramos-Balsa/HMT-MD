# Forma elíptica, radio modular y acción orientada

La elipse de acción y la inversión de radio admiten una composición explícita. El punto de partida de este cruce son las salidas angulares y de acción ya producidas en el desarrollo APP–TRIT–TPK: el ángulo \(A\), el contraángulo \(C^*\) y una sección positiva de acción reducida \(\hbar\). Ambos ángulos deben expresarse en la misma unidad. El cociente \(C^*/A\) procede de esas salidas; no se elige mediante un radio objetivo. Aquí se reúne su publicación posterior en forma, escala y orientación, conservando como antecedente el estado enriquecido que produjo los valores.

## Forma y módulo rectangular

Supongamos \(A\ne0\) y \(|C^*/A|<1\), el dominio real de la carta elíptica. Definimos su parámetro de forma y sus dos semiejes etiquetados por

\[
\eta_{\rm el}=\operatorname{artanh}(C^*/A),\qquad
a_S=\sqrt{2\hbar}\,e^{\eta_{\rm el}/2},\qquad
b_S=\sqrt{2\hbar}\,e^{-\eta_{\rm el}/2}.
\]

El subíndice distingue este parámetro del retorno temporal que otros pasajes también denominan eta. Se utiliza la carta canónica equilibrada de fase: ambas coordenadas y ambos semiejes tienen unidad de raíz de acción. No se suman directamente una posición y un momento físicos sin esa carta. Los semiejes son positivos y cumplen \(a_Sb_S=2\hbar\). Si se cambia el signo de la forma, se intercambian los ejes etiquetados: no se renombra silenciosamente el mayor.

La red rectangular \(\Lambda=a_S\mathbb Z+i b_S\mathbb Z\) publica el módulo

\[
\tau_{\rm el}=i\,\frac{b_S}{a_S}=i e^{-\eta_{\rm el}}.
\]

En el capítulo de dualidad de radio, la carta modular es \(\iota(R)=iR^2\), para \(R>0\). Ambas publicaciones se componen de manera única en el semieje imaginario positivo:

\[
R_{\rm el}=\sqrt{\frac{b_S}{a_S}}
=e^{-\eta_{\rm el}/2}
=\left(\frac{A-C^*}{A+C^*}\right)^{1/4},
\qquad
\iota(R_{\rm el})=\tau_{\rm el}.
\]

La raíz es la positiva. La identidad procede de
\(e^{2\operatorname{artanh}x}=(1+x)/(1-x)\), con \(x=C^*/A\); no introduce una constante convencional como generador. También proporciona la recuperación exacta de la razón angular:

\[
\frac{C^*}{A}=\frac{1-R_{\rm el}^{\,4}}{1+R_{\rm el}^{\,4}}.
\]

Por tanto, esta coordenada conserva la razón angular con signo, aunque no recupera por sí sola los dos ángulos absolutos ni su genealogía. La inversión etiquetada de forma, presentada como inversión de hoja en el propietario modular, produce

\[
\eta_{\rm el}\longmapsto-\eta_{\rm el},
\qquad
R_{\rm el}\longmapsto R_{\rm el}^{-1},
\qquad
\tau_{\rm el}\longmapsto-\frac1{\tau_{\rm el}}.
\]

El invariante modular \(j\) conserva la clase correspondiente: \(j(\tau_{\rm el})=j(-1/\tau_{\rm el})\). Su invariancia identifica esas publicaciones, mientras el marcado de los ejes conserva cuál se ha utilizado. En esta composición, \(R_{\rm el}\) es una coordenada adimensional de forma. Su identificación con un radio dimensional de una realización de cuerda debe conservar la carta de esa realización; no se obtiene convirtiendo una razón de semiejes en una longitud.

## La matriz que se transporta

Para los índices enteros \((m,w)\), la forma cuadrática del capítulo de dualidad, denominada aquí energía normalizada, es

\[
E_R(m,w)=\frac{m^2}{R^2}+w^2R^2.
\]

Con el radio anterior, su matriz en ese orden de coordenadas es

\[
D(\eta_{\rm el})
=\begin{pmatrix}e^{\eta_{\rm el}}&0\\0&e^{-\eta_{\rm el}}\end{pmatrix}
=\frac1{2\hbar}
\begin{pmatrix}a_S^2&0\\0&b_S^2\end{pmatrix}.
\]

Es la matriz de semiejes cuadrados normalizados. La ecuación de la elipse en las coordenadas de fase \((Q,P)\),

\[
\frac{Q^2}{a_S^2}+\frac{P^2}{b_S^2}=1,
\]

utiliza, tras multiplicar por \(2\hbar\), la matriz inversa \(D(-\eta_{\rm el})\). Esta distinción impide atribuir a una misma matriz dos papeles recíprocos.

Introduzcamos ahora dos transformaciones lineales:

\[
S=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
J_{\rm rot}=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

Ambas satisfacen

\[
S^{\mathsf T}D(-\eta_{\rm el})S
=J_{\rm rot}^{\mathsf T}D(-\eta_{\rm el})J_{\rm rot}
=D(\eta_{\rm el}).
\]

La primera intercambia las coordenadas; la segunda las intercambia invirtiendo además una de ellas. Por eso, al invertir la forma, las dos conservan la energía cuadrática correspondiente. La igualdad se verifica multiplicando las matrices diagonales: los signos desaparecen en los cuadrados. Sin embargo, \(S^2=I\), mientras \(J_{\rm rot}^2=-I\). Ya aquí aparece información operatoria que el escalar energético no distingue.

## Acción, orientación y memoria conservada

En el plano de fase fijemos \(\omega=dQ\wedge dP\). Entonces

\[
S^*\omega=-\omega,
\qquad
J_{\rm rot}^*\omega=\omega.
\]

La diferencia no es terminológica. Si \(\lambda=P\,dQ\) y \(\gamma\) es una curva cerrada orientada, su acción firmada es \(\mathcal I(\gamma)=\oint_\gamma\lambda\). Los dos transportes dan

\[
S^*\lambda=Q\,dP=d(PQ)-\lambda,
\qquad
J_{\rm rot}^*\lambda=-Q\,dP=\lambda-d(PQ).
\]

La diferencial exacta se integra a cero en una curva cerrada. Se sigue, para toda esa clase de curvas y no sólo para un ejemplo numérico,

\[
\mathcal I(S\gamma)=-\mathcal I(\gamma),
\qquad
\mathcal I(J_{\rm rot}\gamma)=\mathcal I(\gamma).
\]

Esta convención de acción firmada se declara aparte de la elección de recorrido positivo de la fuente areal. El signo de una parametrización no altera las identidades de transporte. A sección de acción fija, el factor de fase \(\exp(i\mathcal I/\hbar)\) se conjuga bajo \(S\) y se conserva bajo \(J_{\rm rot}\). Si lleva además una holonomía discreta, ésta debe transportarse mediante su regla propia, no deducirse del valor de la energía.

Así, conservar energía y clase modular no determina todavía el transporte de acción. La información suficiente para distinguir estos dos mapas incluye el marcado de ejes y su orientación. Esa marca tampoco sustituye toda la memoria del estado TPK: es la parte concreta de esa memoria que interviene en este cálculo. No se identifica \(J_{\rm rot}\) con otros operadores del corpus llamados \(J\) sin un entrelazador que lo justifique.

## Cambio de escala y reciprocidad gravitatoria

Existe un segundo cambio, diferente de invertir la forma. Entre las secciones de acción compatibles del corpus, sea \(\lambda_{\rm act}=\hbar'/\hbar>0\). Si la forma y las cantidades \(c,t_0,\theta\) permanecen fijas, la expresión genealógica reunida para la sección gravitatoria es

\[
G=\theta\frac{c^5t_0^2}{\hbar},
\qquad
\ell_P^2=\frac{G\hbar}{c^3}.
\]

Aquí \(c\) es la velocidad interna, \(t_0\) la unidad temporal y \(\theta\) el selector geométrico previamente publicado. La sustitución de sección produce

\[
a_S'=\sqrt{\lambda_{\rm act}}\,a_S,\qquad
b_S'=\sqrt{\lambda_{\rm act}}\,b_S,\qquad
G'=\frac{G}{\lambda_{\rm act}}.
\]

Se conservan simultáneamente

\[
R_{\rm el}'=R_{\rm el},\qquad
\tau_{\rm el}'=\tau_{\rm el},\qquad
G'a_S'b_S'=Ga_Sb_S=2c^3\ell_P^2.
\]

La forma no cambia, pero sí cambia la escala de acción; la respuesta gravitatoria recíproca conserva el área de Planck de esa sección, antes de su evaluación metrológica. Esta comparación entre secciones declaradas no afirma una variación física arbitraria de constantes. Tampoco sustituye el corrector electrónico por una multiplicación simple: ese lector mantiene su exponente específico.

## Alcance del cruce y controles decisivos

La composición reúne tres operaciones que no deben confundirse: invertir la forma, transportar la orientación y cambiar de sección de acción. Su contenido no es sumar coincidencias de valores: determina qué datos se conservan, cuáles cambian y cómo se recuperan.

Los controles son algebraicos. Usar \(e^{+\eta_{\rm el}/2}\) como radio daría el módulo de la hoja intercambiada, no el de partida. Confundir la matriz de semiejes cuadrados con la ecuación de la elipse invierte la anisotropía. Tratar \(S\) como simpléctico contradice \(S^*\omega=-\omega\). Conservar ambos semiejes al variar \(\hbar\) contradice \(a_Sb_S=2\hbar\). En la forma circular \(\eta_{\rm el}=0\), el radio es uno, pero las dos transformaciones siguen distinguiéndose por la orientación.

Se recupera aquí la elipse y la modularidad ya escritas, y se explicita su composición con el radio y las secciones de acción. No se presenta como un redescubrimiento de esa arquitectura ni como sustituto del desarrollo de teoría M. Es una conexión concreta de su red estructural, con sus mapas y con la información que cada uno conserva.
