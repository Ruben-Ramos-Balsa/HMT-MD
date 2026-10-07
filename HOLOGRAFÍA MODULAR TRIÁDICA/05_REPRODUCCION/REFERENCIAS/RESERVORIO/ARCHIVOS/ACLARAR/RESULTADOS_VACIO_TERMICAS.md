# Resultados comprobados: respuesta del vacío, cuantos eléctricos y relaciones térmicas

## Resultado de la revisión

El corpus contiene una construcción operatoria explícita de las cuatro respuestas constitutivas del vacío, una composición coherente de los cuantos eléctricos y un desarrollo térmico que incluye la relación de Boltzmann en la escala cronológica, los dos extremos de Wien, el flujo de Stefan–Boltzmann y los momentos del gas fotónico. Las fórmulas no están reducidas a una lista de decimales: se especifican sus antecedentes y existen demostraciones algebraicas reproducibles.

Las comprobaciones siguientes reutilizan los valores ya calculados por MASAS y añaden únicamente controles distintos: la identidad polinómica que demuestra monotonía del funcional constitutivo, cotas racionales de los extremos de Wien y evaluaciones de las composiciones térmicas. No se han vuelto a generar las mil cifras de π, φ y e, ni el contraángulo, ni las tablas de masas. No se han modificado fuentes o PDF.

## 1. Antecedente angular y respuesta constitutiva

El punto de partida de este tramo es la pareja angular previamente construida a partir del núcleo APP–TRIT–TPK. Sean \(x=\pi A/180\), \(y=\pi C^*/180\), con \(x>y>0\), y \(q_\pm=\exp(-x\mp y)\). La involución autoadjunta \(R\) determina \(P_\pm=(I\pm R)/2\) y la contracción positiva \(T=q_+P_++q_-P_-\). Los exponentes 90 y 120 conservan los antecedentes de incidencia de los sectores de seis y ocho componentes, respectivamente; no se eligen mediante ajuste de las respuestas finales.

La operación efectiva es

\[
V=(I-T^{90})(I-T^{120})^{-1},\qquad
r_\pm=\frac{1-q_\pm^{90}}{1-q_\pm^{120}}.
\]

La inversa existe porque \(0<q_\pm<1\). El documento determina conjuntamente

\[
\widehat\varepsilon=r_+^2,\quad
\widehat\mu=r_-^2,\quad
\widehat Z=r_-/r_+,\quad
\widehat c=(r_+r_-)^{-1}.
\]

Se siguen exactamente

\[
\widehat\mu\widehat\varepsilon=\widehat c^{-2},\qquad
\widehat\mu/\widehat\varepsilon=\widehat Z^2.
\]

La prueba contiene más información que estas dos igualdades. Con \(s=q^{30}\),

\[
F(s)=\frac{1+s+s^2}{1+s+s^2+s^3},\qquad
F'(s)=-\frac{s^2(3+2s+s^2)}{(1+s+s^2+s^3)^2}.
\]

El numerador de la derivada se ha comprobado como identidad polinómica exacta. Por tanto, \(F\) es estrictamente decreciente, su imagen es \((3/4,1)\), y el orden de las dos respuestas se deduce antes de evaluar decimales. El intercambio de hojas conserva \(\widehat c\), intercambia \(\widehat\mu\) con \(\widehat\varepsilon\) e invierte \(\widehat Z\). El producto conserva el modo común; el cociente conserva la orientación relativa.

| Resultado | Evaluación reutilizada, redondeada |
|---|---:|
| Permitividad normalizada | 0,999999257096636702760442 |
| Permeabilidad normalizada | 0,999448350479326935089982 |
| Impedancia normalizada | 0,999724508538937215455554 |
| Velocidad normalizada | 1,000276310486157526106386 |

Los residuos numéricos de las identidades, sobre las evaluaciones guardadas a cien cifras de trabajo, son de orden \(10^{-99}\). La demostración de las identidades es algebraica y no depende de esa tolerancia.

**Conclusión publicable:** determinación espectral conjunta, monotonía, reconstrucción de las hojas y paridad bajo la involución, con el antecedente angular y las normalizaciones explícitos. La conservación en las amplificaciones \(V\otimes I_{9^m}\) se deduce de la expectativa por traza normalizada; no necesita repetir una evaluación para cada nivel.

## 2. Carga y cuantos eléctricos

El tramo siguiente conserva la dirección causal: primero \(\alpha\), la sección de acción \(h_a\) y la impedancia \(Z\); después la sección positiva de carga

\[
e_a=\sqrt{2\alpha h_a/Z}.
\]

Las cuatro expresiones consecuentes son

\[
R_K=\frac{Z}{2\alpha},\qquad G_0=\frac{4\alpha}{Z},\qquad
\Phi_{0,a}=\sqrt{\frac{h_aZ}{8\alpha}},\qquad K_{J,a}=\Phi_{0,a}^{-1}.
\]

Se han comprobado las identidades \(R_KG_0=2\), \(G_0Z=4\alpha\), \(K_{J,a}\Phi_{0,a}=1\) y \(e_a^2Z=2\alpha h_a\). Las dos primeras cantidades son invariantes al cambio de la orientación de acción; flujo y constante de Josephson se transforman recíprocamente con factores \(R_{\rm act}^{1/2}\) y \(R_{\rm act}^{-1/2}\).

En la normalización del cálculo conservado, \(R_K\simeq68,4991234181970752\) y \(G_0\simeq0,0291974539263766948\). Son coeficientes en las rectas dimensionales declaradas; la tabla no los rotula como ohmios o siemens. La acción y las unidades deben acompañar asimismo cualquier cifra de carga, flujo o frecuencia.

**Conclusión publicable:** una familia de consecuencias exactas del mismo lector de carga, con covariancia de orientación explícita. No son cuatro ajustes numéricos separados.

## 3. Relación de Boltzmann y escala cronológica

El texto establece la ecuación

\[
k_B\Theta_{\rm clk}\log3=\frac{h_{\rm int}}{108t_0},\qquad
\frac{k_B\Theta_{\rm clk}t_0}{h_{\rm int}}
=\frac1{108\log3}
\simeq0,00842814098728553142235408.
\]

El factor \(\log3\) tiene construcciones residual e informacional anteriores. Su uso térmico conserva el dominio de energía, la escala temporal y la normalización de temperatura. La igualdad determina una relación exacta, no una coincidencia decimal aislada. El capítulo 70 desarrolla la interpretación de \(k_B\) como transformación entre las rectas de temperatura y energía; el capítulo 48 conserva expresamente esa normalización al emplearla en radiación.

**Conclusión publicable:** la relación térmica cronológica y las consecuencias que conservan su normalización. La distinción entre esa relación y la coordenada de una constante en una elección de unidades se trata al final, sin suprimir el resultado.

## 4. Extremos de Wien

Para las dos densidades espectrales consideradas, las raíces estrictamente positivas satisfacen

\[
3(1-e^{-x_3})=x_3,\qquad 5(1-e^{-x_5})=x_5.
\]

Se ha comprobado la unicidad: para \(m>1\), \(f_m(x)=m(1-e^{-x})-x\) es estrictamente cóncava, \(f_m'(0)>0\), y \(f_m(m)<0\). Además de la raíz nula, tiene exactamente una raíz positiva. Su aislamiento se ha efectuado con aritmética racional, cota de Taylor positiva para la exponencial y 85 bisecciones. Cada intervalo tiene anchura exacta \(2^{-85}\):

\[
2,8214393721220788934031913107292824
<x_3<
2,8214393721220788934031913365786767,
\]

\[
4,9651142317442763036987591107636129
<x_5<
4,9651142317442763036987591366130071.
\]

Los extremos físicos correspondientes son \(\lambda_{\max}/\ell_0=108\log3/x_5\simeq23,8967567790425841\) y \(\nu_{\max}t_0=x_3/(108\log3)\simeq0,0237794888153232479\). El cambio de densidad espectral introduce un jacobiano; por ello estos máximos no se identifican mediante una simple inversión.

## 5. Stefan–Boltzmann y momentos fotónicos

En el espectro bosónico expresamente declarado por el corpus, integrar el momento de energía da

\[
j_\star(\Theta_{\rm clk})=
\frac{2\pi^5}{15\,108^4(\log3)^4}
\frac{h_{\rm int}}{\ell_0^2t_0^2}.
\]

El coeficiente calculado es \(2,05880525386443260516\times10^{-7}\). La dimensión de \(h_{\rm int}/(\ell_0^2t_0^2)\) es la de flujo energético por superficie. La integral bosónica \(\int_0^\infty x^3/(e^x-1)\,dx=6\zeta(4)=\pi^4/15\) se obtiene por expansión positiva e integración término a término; se trata de una composición posterior con las secciones de acción, propagación y temperatura, tal como declara el texto.

También quedan evaluados, reutilizando el valor de Apéry ya calculado:

| Coeficiente | Expresión | Evaluación |
|---|---|---:|
| Número fotónico | \(n_\gamma\ell_P^3=2\zeta(3)/(\pi^2\log^3 3)\) | 0,1837053986849809923 |
| Energía fotónica | \(u_\gamma\ell_P^3/E_P=\pi^2/(15\log^4 3)\) | 0,4516798078584186446 |
| Entropía fotónica | \(s_\gamma\ell_P^3/k_B=4\pi^2/(45\log^3 3)\) | 0,6616279832753457923 |
| Conductancia térmica | \(\kappa_Qt_0/k_B=\pi^2/(324\log3)\) | 0,0277274724603716310 |

**Conclusión publicable:** estas composiciones exactas, con el espectro bosónico y las unidades que intervienen. El valor de \(\zeta(3)\) no se confunde con el factor informacional \(\log3\).

## 6. Alcances que se mantienen separados al cerrar la auditoría

Las cifras precedentes tienen antecedentes definidos y verificables. Las siguientes distinciones no cancelan esos resultados:

1. Las cuatro respuestas con acento circunflejo son coeficientes normalizados. Su expresión en unidades SI exige las cartas de acción, carga y velocidad que el texto distingue. Una tabla de coeficientes no se renombra como tabla SI.
2. El capítulo térmico determina \(k_B\Theta_{\rm clk}\), y es invariante bajo \(k_B\mapsto s k_B\), \(\Theta_{\rm clk}\mapsto\Theta_{\rm clk}/s\). Esta sola ecuación no selecciona las dos coordenadas independientemente. Es una propiedad explícita de la fuente, no una afirmación de que Boltzmann no figure en ella.
3. La composición con Planck, Wien y la distribución bosónica tiene esas hipótesis declaradas. No se presenta como una nueva deducción de la estadística bosónica completa.
4. Las identidades eléctricas son consecuencias del lector definido. Una demostración de las realizaciones físicas Hall y Josephson no se sustituye por las tres identidades escalares. Su evaluación experimental corresponde al cierre físico, no a este control algebraico.

## Fuentes y reproducción

Fuentes leídas completas en este corte, correspondientes a las páginas físicas 828–834 y 883–884 del PDF fijo:

- [Respuesta constitutiva del vacío](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c31_vacio.tex>).
- [Sección de carga y cuantos eléctricos](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c32_cuantos_electricos.tex>).
- [Relaciones térmicas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c40_termicas.tex>).
- [Cálculo focal ejecutado](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/verificar_vacio_termicas.py>) y [resultados con cotas racionales](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/COMPROBACION_VACIO_TERMICAS.json>).

Las evaluaciones anteriores se han reutilizado desde `VALORES_RECALCULADOS_CORPUS.json` y `VALORES_ESPECTRALES_RECALCULADOS.json`; sus huellas se conservan en el resultado focal. No se reclama como descubrimiento nuevo una identidad recuperada del corpus. Este informe es el cierre del bloque asignado, no la afirmación de haber comprobado íntegramente las 2.249 páginas.
