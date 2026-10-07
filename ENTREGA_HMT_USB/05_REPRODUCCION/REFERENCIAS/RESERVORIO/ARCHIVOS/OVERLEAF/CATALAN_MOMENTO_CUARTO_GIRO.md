# Catalán: momento espectral orientado y núcleo de cuarto de giro

Ampliación focal de OVERLEAF. Se mantiene el corte fijo de 2.249 páginas. Procedencia: la definición operatoria y su genealogía son RESULTADO_RECUPERADO del capítulo 33; las identidades integrales siguientes se desarrollan aquí desde esa definición, sin atribuirles novedad histórica ni modificar el corpus.

## 1. Objeto generador, orientación y realización

El capítulo 33 compone APP–TRIT–TPK con la reducción ternaria de la matriz de conferencia de Paley. El operador resultante \(J\) cumple \(J^2=-I\) sobre \(\mathbb F_3^6\), por lo que determina una acción de \(C_4\). Su realización espectral conserva la orientación elegida:
\[
U_4 e_n=i^n e_n,\qquad
Q_4=\frac{U_4-U_4^*}{2i},\qquad
N e_n=n e_n,\quad n\ge1.
\]
La tabla de \(Q_4\) es \((1,0,-1,0)\) en las clases \(1,2,3,0\pmod4\). Esos signos preceden al cálculo del momento. El carácter complejo realiza la acción del grupo cíclico; no es una identificación de los campos \(\mathbb F_9\) y \(\mathbb C\).

**Definición operatoria recuperada.** La constante de Catalán es el momento espectral inverso de orden dos de este lector orientado:
\[
G_{\rm cat}=\operatorname{Tr}(N^{-2}Q_4).
\]
Se usa \(G_{\rm cat}\) para distinguirla de la constante gravitatoria. El calificativo «inverso» precisa que el peso es \(n^{-2}\), no \(n^2\).

La inversión de la orientación compleja \(U_4\mapsto U_4^*\) cambia \(Q_4\) por \(-Q_4\) y cambia el signo de este momento. Por ello, el generador de orden cuatro y la orientación forman parte de la definición; la identidad abstracta \(J^2=-I\), aislada de esa elección, no fija el signo positivo.

Fuente: [capítulo 33, selección y levantamiento](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c33_catalan_apery_euler.tex:23>).

## 2. Núcleo térmico exacto del lector de cuarto de giro

Para \(t>0\), sea
\[
K_4(t)=\operatorname{Tr}(e^{-tN}Q_4).
\]
La convergencia absoluta permite agrupar las clases residuales y sumar la progresión geométrica:
\[
K_4(t)=\sum_{k\ge0}(-1)^k e^{-(2k+1)t}
=\frac{e^{-t}}{1+e^{-2t}}
=\frac1{2\cosh t}.
\]
Esta es una caracterización funcional del lector, anterior a fijar un número de cifras.

Como \(\int_0^\infty t e^{-nt}\,dt=n^{-2}\) y
\(\sum_{n\ge1}|\chi_{-4}(n)|n^{-2}<\infty\), la integración término a término está justificada y proporciona
\[
\boxed{
G_{\rm cat}
=\int_0^\infty\frac{t}{2\cosh t}\,dt
=\int_0^1\frac{-\log x}{1+x^2}\,dx.}
\]
La segunda igualdad utiliza \(x=e^{-t}\). Además,
\[
\boxed{
G_{\rm cat}
=\int_0^1\int_0^1\frac{dx\,dy}{1+x^2y^2}.}
\]
En efecto, para \(|a|<1\) se puede desarrollar \(1/(1+a x^2y^2)\), integrar y obtener \(\sum_{k\ge0}(-a)^k/(2k+1)^2\). El paso \(a\uparrow1\) está dominado en la integral, y la serie integrada converge absolutamente. Así se obtiene la igualdad sin intercambiar una serie no uniformemente convergente en el vértice \((1,1)\).

La estructura común queda expresada por
\[
\text{acción orientada de }C_4
\longrightarrow Q_4
\longrightarrow K_4(t)
\longrightarrow G_{\rm cat}.
\]
Los pesos espectrales y la orientación especifican el momento. El número escalar conserva ese funcional; no reconstruye por sí solo las coordenadas, la representación completa ni la historia enriquecida.

## 3. Finitud y aproximación certificada

Al desarrollar la traza se recupera
\[
G_{\rm cat}=\sum_{k=0}^\infty\frac{(-1)^k}{(2k+1)^2}.
\]
La convergencia absoluta de la serie de valores absolutos prueba finitud. La representación integral prueba positividad. Las sumas alternadas dan, estrictamente,
\[
\frac89<G_{\rm cat}<1.
\]
Para
\[
S_N=\sum_{k=0}^{N-1}\frac{(-1)^k}{(2k+1)^2},
\]
el resto satisface
\[
0<(-1)^N(G_{\rm cat}-S_N)<\frac1{(2N+1)^2}.
\]
Por tanto, \(S_{2m}<G_{\rm cat}<S_{2m+1}\). Esta es una familia de intervalos racionales demostrada para todo \(m\), sin una campaña numérica. Permite aproximación con error absoluto arbitrariamente pequeño.

El algoritmo que imprime una cantidad creciente de cifras, la existencia de una expansión decimal y la irracionalidad son proposiciones diferentes. La convergencia y la cota del resto prueban las dos primeras capacidades en el sentido de aproximación; no prueban que la expansión sea no periódica. La estabilidad de un bloque decimal concreto requiere que su intervalo racional certificado quede dentro de la misma celda decimal.

Fuente: [capítulo 33, traza y prueba](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c33_catalan_apery_euler.tex:143>). Las cotas anteriores son consecuencias elementales explicitadas aquí.

## 4. Composición con el lector trítico y la escala de Pell

El lector trítico \(Q_3\) conserva las clases orientadas módulo tres. El capítulo 33 demuestra
\[
Q_{12}=Q_3Q_4,\qquad
\chi_{12}=\chi_{-3}\chi_{-4}.
\]
Es un producto de operadores diagonales que compone los dos datos residuales. Su núcleo térmico es
\[
K_{12}(t)
=\frac{e^{-t}-e^{-5t}-e^{-7t}+e^{-11t}}{1-e^{-12t}}
=\frac{e^{-t}(1-e^{-4t})}{1+e^{-6t}}.
\]
No es el producto escalar \(K_3(t)K_4(t)\): la traza de un producto diagonal suma productos con el mismo índice espectral; el producto de trazas suma sobre dos índices independientes.

La fuente evalúa los momentos de ese carácter compuesto:
\[
L(1,\chi_{12})=\frac{\log(2+\sqrt3)}{\sqrt3},
\qquad
L(2,\chi_{12})=\frac{\pi_{\rm HMT}^2}{6\sqrt3}.
\]
De este modo, el cuarto de giro que determina \(G_{\rm cat}\), combinado con la orientación trítica, interviene en los momentos vinculados a la unidad de Pell \(2+\sqrt3\) y a la coordenada \(\pi_{\rm HMT}\). La primera expresión corresponde a la serie de Dirichlet convergente agrupada; \(N^{-1}Q_{12}\) no se denomina operador traza–clase, pues la suma de valores absolutos diverge.

Fuente: [capítulo 33, composición y evaluaciones](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c33_catalan_apery_euler.tex:179>).

## 5. Alcance de esta ampliación

Quedan expuestas la definición operatoria, la orientación que fija el signo, el núcleo térmico exacto, tres expresiones integrales equivalentes, una cota de aproximación universal y la composición trítico–cuaternaria. Ninguna usa el decimal objetivo como selector.

La clasificación aritmética de \(G_{\rm cat}\) debe acompañarse de su prueba propia. Este anexo no infiere irracionalidad, trascendencia o periodicidad de las cifras a partir de las identidades anteriores. La comprobación documental focal de ese alcance se recoge al cierre, sin convertirla en una auditoría global ni en un dictamen sobre todo el corpus.

### Localización documental del alcance aritmético

En el corte consultado, la identidad operatoria es la ecuación 41.6, folio 835, junto con las ecuaciones 41.4–41.5 del levantamiento de cuarto de giro. El apartado de clasificación y el atlas remiten a esa identidad: [clasificación probatoria](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c23_clasificacion_probatoria.tex:43>) y [atlas genealógico](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c44_atlas_genealogico_purificado.tex:752>).

Los cuerpos focales leídos prueban la identidad y la convergencia, e imprimen una evaluación decimal. No contienen una demostración de irracionalidad o de no periodicidad decimal de Catalán. Esta observación describe únicamente esos cuerpos y sus remisiones; no atribuye ausencia a todo el corpus. Para esta ampliación, el resultado positivo establecido es el momento exacto de cuarto de giro y sus relaciones demostradas en las secciones 1–4.

