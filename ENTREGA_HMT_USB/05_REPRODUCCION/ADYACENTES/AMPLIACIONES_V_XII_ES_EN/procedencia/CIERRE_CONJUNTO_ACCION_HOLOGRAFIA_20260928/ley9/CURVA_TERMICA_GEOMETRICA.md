# Restitución conjunta de la acción: del contraste térmico al giro electrónico

## 1. Composición que reúne los dos desarrollos

Este resultado recibe la misma estructura APP–TRIT–TPK de los deltas precedentes y de `RECUPERACION_Y_ENERGIA_LIBRE.md`. Las publicaciones α, π, H₅, η y el par angular pertenecen a esa genealogía antes de evaluar el protocolo. Las dos realizaciones posteriores —frontera térmica y transporte del bloque electrónico— conservan sus mapas propios. Su enlace efectivo es la dependencia común de η, que se elimina algebraicamente a continuación.

No se reconstruyen aquí las constantes desde una observación experimental. Se obtiene un procedimiento de restitución de las salidas ya generadas y una relación cruzada entre observables de las realizaciones declaradas. La comparación entre las secciones anterior y posterior al retorno conserva α y f_π; no supone una familia física de constantes libremente variables.

Los propietarios `DELTA_01_SUSTITUCION_TOTAL/SUSTITUCION_TOTAL_Y_GEOMETRIA.md`, su comprobador y `DELTA_03_CIERRE_HOLOGRAFICO/GEOMETRIA_DE_TRANSPORTES.md` fijan

\[
A=1000\alpha,\quad C^*=2(\eta+\alpha),\quad
\xi=C^*/A=\tanh s,
\]
\[
d=\frac{\pi f_\pi}{2430}(499\alpha-\eta),
\qquad f_\pi=1-\frac{7\pi}{8748}.
\tag{1}
\]

A y C* son las coordenadas expresadas en grados en esos lectores; ξ es un cociente adimensional. La conversión π/180 ya está incluida en el origen de d. s es una rapidez de forma adimensional, no una medida en grados.

## 2. Eliminación exacta y relación de compatibilidad

La primera ecuación da η=500αξ−α. Sustituyendo en la segunda,

\[
\boxed{d=d_*(1-\xi)=d_*(1-\tanh s),
\qquad d_*:=\frac{50\pi f_\pi\alpha}{243}.}
\tag{2}
\]

d_* es una escala compuesta de las salidas anteriores; su símbolo abrevia la fórmula y no designa una constante universal nueva. El dominio geométrico es 0<ξ<1, equivalente a 0<d<d_*. La sección de acción positiva η>0 precisa el subdominio 1/500<ξ<1, equivalente a 0<d<(499/500)d_* y 0<η<499α. El valor heredado satisface estas condiciones.

Esta igualdad une el sesgo térmico con la deformación geométrica, en lugar de tratarlos como ajustes independientes. En una comparación de lectores con α fija,

\[
\frac{\partial d}{\partial\eta}=-\frac{\pi f_\pi}{2430},
\qquad
\frac{\partial s}{\partial\eta}=
\frac{1}{500\alpha(1-\xi^2)}.
\tag{3}
\]

El descenso de η en el retorno aumenta el sesgo térmico y disminuye la rapidez de forma. El desarrollo de «Aclarar la tarea» verifica esa variación entre las dos secciones concretas H₅ y η_ret, conservando sus demás dependencias. La oposición de signos tiene un origen común demostrable.

## 3. La asimetría de probabilidades restituye la coordenada de acción

La distribución de trabajo del intercambio sectorial ya demostrada cumple

\[
\frac{P(M=m)}{P(M=-m)}=e^{dm},\qquad m=1,\ldots,36.
\tag{4}
\]

Por tanto cada pareja de niveles ofrece el mismo lector

\[
\widehat d_m=\frac1m\log\frac{P(M=m)}{P(M=-m)}=d.
\tag{5}
\]

Es una relación entre probabilidades y ocupaciones; la extracción de d no requiere fijar una unidad de energía ni conocer el radio R. En un experimento, las frecuencias empíricas estiman esas probabilidades y conservan su incertidumbre estadística; la igualdad exacta corresponde al modelo.

De (2) y (5) se recuperan

\[
\boxed{\xi=1-\frac d{d_*},\quad
\eta=499\alpha-\frac{2430d}{\pi f_\pi},\quad
C^*=A\!\left(1-\frac d{d_*}\right).}
\tag{6}
\]

Conservar un único promedio no es el contraste más fuerte. Comprobar que los treinta y seis lectores \(\widehat d_m\) coinciden prueba simultáneamente la forma exponencial, los signos y la compatibilidad del transporte. También se puede efectuar el contraste dentro de cada fibra N con ambos niveles presentes.

## 4. Predicción cruzada del analizador electrónico

La composición de los dos ejes del bloque electrónico, con la compensación polar declarada, produce

\[
\tan\frac{\omega_e}{2}=
\frac{\sqrt3\,z}{2-z},\qquad
z=\tanh^2\frac s2
=\frac{1-\sqrt{1-\xi^2}}{1+\sqrt{1-\xi^2}}.
\tag{7}
\]

El coeficiente √3 procede del solapamiento de los proyectores P,Q; el prefactor electrónico p=√3/4 determina la susceptibilidad mixta del giro. La contribución de «Aclarar la tarea» demuestra que el analizador C, sobre la preparación P y los dos órdenes conjugados de ese protocolo, da un contraste condicionado sin ω_e. Usando (7),

\[
\boxed{\mathcal C_{\rm spin}(d)=
\frac{\sqrt3\,z(d)[2-z(d)]}{2[1-z(d)+z(d)^2]},
\quad
z(d)=\frac{1-\sqrt{1-(1-d/d_*)^2}}
{1+\sqrt{1-(1-d/d_*)^2}}.}
\tag{8}
\]

Ésta es la relación cruzada buscada: una lectura de asimetría térmica determina una respuesta de orientación del bloque electrónico, después de especificar las dos realizaciones. α y π provienen de las salidas HMT; η se ha eliminado y no se reajusta para concordar con la segunda medida. Tampoco se identifica por esta composición la lectura electrónica con una asimetría CP.

Para la realización mediante los tres filtros completos del chat colaborador,

\[
r=\operatorname{arcosh}(1+\tfrac12\sinh^2s),\quad
p_{\rm ex}=e^{-2s-r},\quad
\mathcal C_{\rm por\ ensayo}=p_{\rm ex}\mathcal C_{\rm spin}.
\tag{9}
\]

La probabilidad p_ex corresponde a ese instrumento concreto, cuyo compensador polar actúa primero; otro control que implemente el mismo unitario puede tener distinta probabilidad de éxito. Las ramas de fallo y el puerto complementario se incluyen en la prueba de normalización de `../aclarar/`. El mapa directo d→contraste está determinado; la lectura de sin ω por sí sola no es globalmente inyectiva en el dominio geométrico, porque ω puede superar π/2. El punto heredado pertenece a la rama creciente de sin ω.

## 5. Restitución de Barbero y del funcional de área

El mismo d conserva los canales utilizados por el funcional de Barbero:

\[
q_-=\exp\!\left(-\frac{27d}{f_\pi}\right),\quad
q_+=\frac{D_A}{q_-},\quad D_A=e^{-100\pi\alpha/9}.
\tag{10}
\]

Recibiendo S_m(q)=q^m/(1-q^{3m}), la fórmula anterior del corpus queda

\[
\gamma(d)=\frac{\pi A C^*(d)}{180}
+12[S_{90}(q_-)-S_{90}(q_+)]
-[S_{120}(q_-)-S_{120}(q_+)].
\tag{11}
\]

Análogamente,

\[
a_0(d)=\frac{1+2\cos(\pi/18)}3\frac{\pi C^*(d)}{1080},
\quad
\widehat{\mathcal A}=\gamma(d)a_0(d)L_\alpha^2N.
\tag{12}
\]

Así, el contraste térmico, el giro electrónico y el coeficiente del operador de área pertenecen a una misma curva de compatibilidad de lectores. El área agregada de un estado todavía no determina M: recuperar el **coeficiente constitutivo** del operador y recuperar la **orientación de una configuración** son operaciones distintas.

## 6. Valores, falsadores y consecuencia editorial

El comprobador adjunto evalúa (2), (6), (8), (9), (11) y (12) desde los archivos de salidas heredadas, con trazas SHA-256. Contrasta el resultado con las evaluaciones independientes de ambos chats. La prueba de (2) es algebraica; el resto son composiciones de fórmulas demostradas, con su dominio explícito. Los decimales son evaluaciones multiprecisión, no cotas por intervalos.

Los controles contrastables son: linealidad de la razón logarítmica en m; invariancia del histograma de área durante el intercambio; igualdad entre la ξ restituida y la forma angular; respuesta sin ω en el analizador con preparación y orden fijados; contabilidad íntegra del éxito y del fallo. Una discrepancia debe analizarse con esas condiciones de preparación y lectura antes de atribuirla al generador.

La residencia principal propuesta es VII, después de la composición térmica de constantes. V conserva la distribución de trabajo y el instrumento térmico; VI conserva el instrumento electrónico; II recibe la restitución del funcional de Barbero. La prueba de enlace (2) y las sustituciones necesarias deben repetirse donde las utilice un PDF autónomo. Esta curva evita presentar como descubrimientos separados resultados que comparten una misma coordenada estructural.
