# Elipse de acción, distancias focales y enlace con Bohr

Recuperación focal del corte fijo de 2249 páginas, 6 de septiembre de 2026. Sólo fuentes locales y álgebra exacta; no se generan decimales ni se modifican originales. Se leyó íntegro [06_03c_elipse_accion_holonomia_rev8][elipse], incluido su desarrollo de Hilbert–Beltrami–Klein y la figura vinculada; se siguieron los propietarios completos de [geometría espectral y acción][areal], [invariantes focales][invariantes] y [modularidad][modular]. Las composiciones algebraicas reunidas abajo no se presentan como un descubrimiento nuevo.

## 1. Forma y focos de la elipse espectral

El antecedente es el par angular ya producido por HMT y transferido a MD: \(A\) y \(C^*\) no se seleccionan desde una distancia observada. El propietario [05_03, 11–87][canales] conserva separadamente sus genealogías y la sección de acción. En la carta \(\kappa=\pi_{\mathrm{HMT}}/180\) y el dominio \(0<C^*<A\), se define

\[
B_1=AI+C^*R,\qquad R^2=I,\qquad
a_1^2=\kappa(A+C^*),\qquad b_1^2=\kappa(A-C^*).
\]

Los semiejes son positivos y \(a_1>b_1\). Sus cuadrados recuperan las entradas:

\[
A=\frac{a_1^2+b_1^2}{2\kappa},\qquad
C^*=\frac{a_1^2-b_1^2}{2\kappa}.
\]

Con \(\rho_1=\sqrt{A^2-C^{*2}}\) y \(\eta_{\mathrm{el}}=\operatorname{artanh}(C^*/A)\) se obtiene \(A\pm C^*=\rho_1\exp(\pm\eta_{\mathrm{el}})\). Aquí \(\eta_{\mathrm{el}}\) es la coordenada de forma geométrica que el propietario denomina \(\eta\); no es \(\eta_{\mathrm{ret}}\), la coordenada de retorno del refinamiento de acción. De aquí,

\[
a_1b_1=\kappa\rho_1,\qquad
\frac{b_1}{a_1}=\exp(-\eta_{\mathrm{el}}).
\]

El producto conserva escala; el cociente conserva forma. El propietario explicita los focos \(F_\pm=(\pm c_1,0)\), la **semidistancia focal** \(c_1\) y la **distancia entre focos** \(d_1\):

\[
\begin{aligned}
c_1^2&=a_1^2-b_1^2=2\kappa C^*,\\
d_1&=2c_1=2\sqrt{2\kappa C^*},\\
e_f^2&=\frac{c_1^2}{a_1^2}=\frac{2C^*}{A+C^*}.
\end{aligned}
\]

Localizador y prueba: [52.4.1, 10–83][areal]. Son identidades de la carta espectral, no longitudes espaciales SI. El bloque de referencia APP \(B_0=7I+2R=9P_++5P_-\) da \(d_0=4\sqrt{\kappa}\), y el mismo cuerpo prueba \((d_1/d_0)^2=C^*/2\) (93–119). Ése es el enlace focal explícito con el bloque APP; no una identificación por parecido decimal con \(54\).

Para precisar el otro uso de “distancias focales”, en una elipse \((a\cos\theta,b\sin\theta)\), con \(c^2=a^2-b^2\), las distancias del punto a cada foco son

\[
r_+(\theta)=a-c\cos\theta,\qquad
r_-(\theta)=a+c\cos\theta,\qquad r_++r_-=2a.
\]

Esta última línea es la consecuencia euclídea exacta de los semiejes, no una cita literal del propietario: al cuadrar la distancia a \((\pm c,0)\) se obtiene \((a\mp c\cos\theta)^2\); como \(a>c\), la raíz es positiva. Se distingue de \(d=2c\), que mide la separación entre los dos focos.

## 2. La misma forma sobre la recta de acción

Sea \(\hbar=\hbar_{\mathrm{HMT}}^{\mathrm{ret}}>0\) la sección de acción ya generada. [06_03c, 7–45][elipse] y [52.4.1, 137–198][arealAccion] construyen

\[
\begin{aligned}
a_S&=\sqrt{2\hbar\exp(\eta_{\mathrm{el}})},&
b_S&=\sqrt{2\hbar\exp(-\eta_{\mathrm{el}})},\\
Q&=a_S\cos\theta,& P&=b_S\sin\theta.
\end{aligned}
\]

Las elipses espectral y de acción son homotéticas mediante

\[
\lambda_{\mathrm{act}}^2=\frac{2\hbar}{\kappa\rho_1},\qquad
(a_S,b_S,c_S)=\lambda_{\mathrm{act}}(a_1,b_1,c_1).
\]

Comparten excentricidad y razón de semiejes, **no dimensión física**. En esta carta simétrica \(Q\) y \(P\), los semiejes tienen dimensión raíz de acción; su producto tiene dimensión de acción. No son automáticamente una posición espacial y un momento sin reescalado declarado. Las distancias focales en esa misma carta satisfacen, por sustitución,

\[
c_S^2=4\hbar\sinh\eta_{\mathrm{el}},\qquad
d_S=2c_S,\qquad d_S^2=16\hbar\sinh\eta_{\mathrm{el}}.
\]

La ley areal se demuestra directamente:

\[
\mathcal A(\theta)
=\frac12\int_0^\theta(QP'-PQ')\,dt
=\frac12a_Sb_S\theta
=\hbar\theta.
\]

Así, un radián **de fase paramétrica** barre \(\hbar\) y una vuelta barre \(h=2\pi_{\mathrm{HMT}}\hbar\). No se identifica \(\theta\) con el ángulo polar euclídeo de cada punto ni con una longitud de arco de la elipse. La holonomía \(\varepsilon_\gamma\exp(iJ_\gamma/\hbar)=1\) distingue el cierre cilíndrico del doble retorno de Möbius ([06_03c, 48–64][elipseHolonomia]); no cambia la razón de forma ni convierte el semieje en una longitud espacial.

**Convención de orientación que debe conservarse.** La fórmula positiva de área utiliza \(dQ\wedge dP\), escrita expresamente en 52.4.1:174. La lista de datos de 06_03c:135 escribe \(dP\wedge dQ\), de signo contrario. Este fragmento adopta la orientación de la prueba areal; si se usa la forma invertida con el mismo recorrido, el área orientada cambia de signo. No se ha corregido silenciosamente el original.

## 3. Elipse, geometría interior y módulo complejo: objetos distintos

La normalización \((Q,P)\mapsto(Q/a_S,P/b_S)\) lleva el interior al disco. La razón doble de los cuatro puntos de una cuerda define la distancia de Hilbert, y su invariancia proyectiva prueba la realización de Beltrami–Klein ([06_03c, 75–141][klein]). La forma simpléctica de la órbita y la métrica proyectiva del interior son estructuras distintas sobre datos relacionados.

Existe además un **enlace modular efectivo**, que no consiste en llamar “elíptica” a la figura. [52.10.1, 6–55][modular] declara el retículo rectangular de períodos y después su cociente complejo:

\[
\Lambda_{\eta_{\mathrm{el}}}=a_S\mathbb Z+i b_S\mathbb Z,\qquad
\mathbb C/\Lambda_{\eta_{\mathrm{el}}},\qquad
\tau_{\eta_{\mathrm{el}}}=i\frac{b_S}{a_S}
=i\exp(-\eta_{\mathrm{el}}).
\]

La línea 12 de esa fuente contiene la errata tipográfica \(i,b_S\); la fórmula del módulo en 17 fija inequívocamente el producto \(i b_S\) usado aquí. La elipse no es por sí sola el toro: el retículo y el cociente son datos de la realización posterior.

Al invertir la hoja, \(\eta_{\mathrm{el}}\mapsto-\eta_{\mathrm{el}}\), se intercambian los ejes y

\[
\tau_{-\eta_{\mathrm{el}}}
=i\exp(\eta_{\mathrm{el}})
=-\frac1{\tau_{\eta_{\mathrm{el}}}},\qquad
j(\tau_{-\eta_{\mathrm{el}}})=j(\tau_{\eta_{\mathrm{el}}}).
\]

La prueba es sustitución en la transformación modular \(S\); la igualdad de \(j\) usa la invariancia modular declarada. El módulo conserva la forma; \(j\) olvida la orientación que el marcado de ejes y focos todavía distingue. Esto no produce por sí solo una acción del Monstruo sobre los focos.

Un **punto elíptico modular** es un punto del semiplano superior con estabilizador no trivial en \(\mathrm{PSL}(2,\mathbb Z)\); no es un foco euclídeo. Se usa el grupo proyectivo precisamente para no contar \(-I\), cuya acción es trivial. Por ejemplo, la transformación \(S\) del propio propietario fija \(i\): \(\tau=-1/\tau\) da \(\tau^2=-1\) y en el semiplano superior \(\tau=i\). En esta familia \(\tau_{\eta_{\mathrm{el}}}=i\) sólo en \(\eta_{\mathrm{el}}=0\), límite circular fuera del dominio estricto \(0<C^*<A\). Esa igualdad tampoco identifica \(i\) con \(F_+\) o \(F_-\). El régimen operatorio denominado elíptico, \(J^2=-I\), constituye a su vez otra noción, expresamente separada del régimen bicapa \(R^2=I\) en [52.7.1][regimenes].

## 4. Enlace exacto con Bohr: por acción, no por identidad focal

El propietario de Bohr declara la composición descendente

\[
a_B=\frac{\hbar}{m_e c\alpha_{\mathrm{HMT}}},
\]

con acción, velocidad, estructura fina y masa electrónica compatibles ([atlas, 1090–1102][bohr]). La elipse de acción aporta el producto \(a_Sb_S=2\hbar\). Por tanto, conservando **la misma sección de acción y carta electrónica**, la composición algebraica efectiva es

\[
a_B=\frac{a_Sb_S}{2m_e c\alpha_{\mathrm{HMT}}}.
\]

También, puesto que \(\eta_{\mathrm{el}}>0\),

\[
a_B
=\frac{c_S^2}{4m_e c\alpha_{\mathrm{HMT}}\sinh\eta_{\mathrm{el}}}
=\frac{d_S^2}{16m_e c\alpha_{\mathrm{HMT}}\sinh\eta_{\mathrm{el}}}.
\]

Estas identidades se obtienen sustituyendo las ecuaciones ya escritas; no afirman que el corpus nombre literalmente este último cociente ni atribuyen prioridad a reunirlo. Explican el enlace tipado: la acción de la elipse se transduce a longitud usando masa, velocidad y acoplamiento. El radio \(a_B\) no es \(c_1\), \(d_1\), \(c_S\) ni \(d_S\). La fórmula involucra el cuadrado de la distancia de la carta de acción y datos adicionales; no convierte los focos en órbitas electrónicas.

La residencia [52.10.2, 8–41][orbitas] refuerza esta distinción: una elipse kepleriana vive en espacio de configuración y responde a un potencial central; la elipse del radión vive en espacio de fases. Compartir una ley areal no identifica sus focos ni establece por sí solo una órbita de Bohr.

## 5. Reciprocidad de acción, gravedad y escala electrónica

La composición con la familia de Planck permite situar esa misma elipse en el mapa de escalas ya reunido. Para las dos secciones compatibles de acción, el [cierre cronológico y su familia de Planck][planck] conserva
\[
G_a\hbar_a=c^3\ell_P^2,
\]
a velocidad, escala temporal y cierre fijados. La elipse de retorno tiene \(a_Sb_S=2\hbar_{\rm ret}\). La sustitución da inmediatamente
\[
G_{\rm ret}\,a_Sb_S=2c^3\ell_P^2.
\]
La igualdad no identifica dos áreas de dimensión diferente: \(a_Sb_S\) es acción, mientras \(\ell_P^2\) es área espacial. El factor \(G_{\rm ret}/c^3\) realiza la conversión dimensional precisa. La prueba consiste en reemplazar el producto de semiejes por la acción y utilizar el cierre anterior, no en comparar dos cifras.

Para comparar hojas, se aplica la misma construcción de semiejes a cada sección positiva \(\hbar_a\), conservando la forma \(\eta_{\rm el}>0\). Sea
\[
R_{\rm act}=\frac{\hbar_{\rm pre}}{\hbar_{\rm ret}}>0.
\]
Como cada cuadrado de semieje es lineal en \(\hbar_a\), y \(c_{S,a}^2=4\hbar_a\sinh\eta_{\rm el}\),
\[
\frac{a_{S,\rm pre}}{a_{S,\rm ret}}
=\frac{b_{S,\rm pre}}{b_{S,\rm ret}}
=\frac{c_{S,\rm pre}}{c_{S,\rm ret}}
=\frac{d_{S,\rm pre}}{d_{S,\rm ret}}
=\sqrt{R_{\rm act}}.
\]
El producto de semiejes crece como \(R_{\rm act}\) y \(G\) cambia como \(R_{\rm act}^{-1}\). Por eso \(G_a a_{S,a}b_{S,a}\) permanece igual. La razón de semiejes, la excentricidad y el módulo complejo conservan su forma. Si se alcanza el límite circular \(\eta_{\rm el}=0\), ambos focos coinciden: la igualdad de escala de \(c_S\) continúa siendo cierta, pero el cociente \(0/0\) no se utiliza.

Con la misma masa electrónica, velocidad y acoplamiento, la longitud de Bohr cambia entre esas dos secciones como
\[
\frac{a_{B,\rm pre}}{a_{B,\rm ret}}=R_{\rm act}.
\]
No es la ley de escala de un semieje: el radio de Bohr depende de la acción, esto es, de su producto. Si también cambia la masa, debe conservarse expresamente el factor \(m_{e,\rm ret}/m_{e,\rm pre}\); no se puede mezclar una comparación de hojas con el paso electrónico basal a final.

Finalmente, sustituyendo el electrón completo ya expuesto en el [desarrollo electrónico][electron],
\[
E_e^\beta=u_E\mathfrak e_0R_{\rm act}^{\kappa_e},
\qquad m_e^\beta=E_e^\beta/c^2,
\]
la sección de retorno de Bohr queda
\[
a_B^{\rm ret,\beta}
=\frac{a_Sb_S\,c}
{2\alpha_{\rm HMT}u_E\mathfrak e_0R_{\rm act}^{\kappa_e}}
=\frac{d_S^2\,c}
{16\alpha_{\rm HMT}u_E\mathfrak e_0R_{\rm act}^{\kappa_e}
 \sinh\eta_{\rm el}}.
\]
Aquí \(\mathfrak e_0\) es la coordenada electrónica basal y \(\kappa_e\) su exponente de retorno; ambos mantienen las fórmulas y lectores definidos en ese desarrollo. Así, el producto areal y la separación focal de la elipse, la acción de Planck, la reciprocidad gravitatoria y la escala electrónica quedan enlazados por sustituciones explícitas. Son composiciones de relaciones del corpus con sus cartas, no una afirmación de que las constantes varíen temporalmente ni una identificación de un foco con una órbita espacial.

## Localizadores

[elipse]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/06_03c_elipse_accion_holonomia_rev8.tex:7>
[elipseHolonomia]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/06_03c_elipse_accion_holonomia_rev8.tex:48>
[klein]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/06_03c_elipse_accion_holonomia_rev8.tex:75>
[canales]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/05_03_canales_contraangulo.tex:11>
[areal]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/c52_04_01_ley_areal.tex:10>
[arealAccion]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/c52_04_01_ley_areal.tex:137>
[invariantes]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/c52_04_02_invariantes_focales.tex:32>
[modular]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/c52_10_01_modularidad.tex:6>
[regimenes]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/c52_07_01_tres_regimenes.tex:6>
[orbitas]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/c52_10_02_orbitas_caminos.tex:8>
[bohr]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c44_atlas_genealogico_purificado.tex:1090>
[planck]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c42_gravedad_escalar.tex:33>
[electron]: </Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/SUSTITUCION_ELECTRON_ACCION_MASAS.md:5>
