# Dinámica de lectores: transporte triádico, fase y correspondencia de Fricke

## Procedencia y propósito

Se desarrollan consecuencias de dos operadores ya escritos en el corpus: el lector de ambivalencia \(\mathcal Q\) y la correspondencia de Fricke de la rama Moonshine de orden dos. Sus definiciones y su posición en la genealogía son **ARQUITECTURA_AUTORAL_PREEXISTENTE**. Las fórmulas reunidas de recuperación, las fibras y el control algebraico se presentan como **FORMALIZACION_NUEVA candidata**; la búsqueda focal no encontró estas formulaciones juntas, pero no se reivindica novedad histórica.

La finalidad es precisar la estructura dinámica: composición, transporte, información de fase y recuperación. No se identifican entre sí operadores de dominios distintos por compartir un nueve, un espejo o una letra J.

## 1. Antecedentes operativos documentados

El capítulo 57 recibe de APP–TRIT–TPK las realizaciones de clausura, propagación y autoescala, y documenta
\[
 \mathcal Q(x,y)=(x/y^2,y/x^2),\qquad x,y>0.
\]
En \(P=xy\), \(O=x/y\), cumple
\[
 P\circ\mathcal Q=P^{-1},\quad O\circ\mathcal Q=O^3,
 \qquad
 P\circ\mathcal Q^2=P,\quad O\circ\mathcal Q^2=O^9.
\]
La fuente aplica el lector a \((\pi,\varphi)\) y obtiene las razones areal y electrónica. Esta aplicación utiliza publicaciones anteriores; no introduce valores objetivo para elegir el operador.

El mismo capítulo conserva las realizaciones \(J_{+1}^2=-I\), \(J_0^2=0\), \(J_{-1}^2=I\), con exponenciales circular, de primer orden e hiperbólica. Sus antecedentes y espacios están tipados en el capítulo de álgebras cuadráticas. No se han confundido esos \(J_\tau\) con el invariante modular \(j\), ni se han multiplicado operadores de espacios diferentes sin un transporte declarado.

En la rama excepcional, la fuente recibe el retículo de Leech y su negación. El conteo de osciladores produce
\[
 t=t_2(\tau)=q^{-1}\prod_{m\ge1}(1+q^m)^{-24}.
\]
La completación documentada y la lectura modular son
\[
 T=T_{2A}=t+24+4096/t,\qquad j=(t+256)^3/t^2.
\]
Se usan esas expresiones ya construidas como premisas de la exploración. No se recalculan sus series ni se reemplaza su genealogía por estas identidades.

## 2. Iteración exacta de la ambivalencia

En coordenadas logarítmicas positivas, \(\mathcal Q\) tiene matriz
\[
 B=\begin{pmatrix}1&-2\\-2&1\end{pmatrix}.
\]
Para todo \(n\ge0\),
\[
 B^n=\begin{pmatrix}a_n&b_n\\b_n&a_n\end{pmatrix},
 \quad
 a_n=\frac{(-1)^n+3^n}{2},\qquad
 b_n=\frac{(-1)^n-3^n}{2}.
\]
Se demuestra porque los vectores \((1,1)\) y \((1,-1)\) son propios, de valores \(-1\) y \(3\); equivalentemente, por inducción en las potencias enteras. Así,
\[
 \mathcal Q^n(x,y)=(x^{a_n}y^{b_n},x^{b_n}y^{a_n}).
\]
La dirección del producto tiene periodo dos; la razón orientada registra la potencia \(3^n\). El retorno del producto no equivale a retorno de la pareja completa.

## 3. Prolongación algebraica con fase y sus fibras

La fórmula de Laurent anterior define una prolongación explícita de \(\mathcal Q\) al grupo \((\mathbb C^\times)^2\). Es una extensión matemática añadida al dominio positivo de la fuente, no una identificación automática con todos los estados enriquecidos del TPK.

Para \(n\ge1\), \(\mathcal Q^n\) es un recubrimiento no ramificado de grado \(3^n\) y
\[
 \boxed{\ker\mathcal Q^n
 =\{(\zeta,\zeta^{-1}):\zeta^{3^n}=1\}.}
\]

**Prueba y cobertura.** Escribamos \(m=3^n\), \(\epsilon=(-1)^n\). Dados valores no nulos \((u,v)\), el producto de una preimagen debe ser
\[
 p=xy=(uv)^\epsilon.
\]
Como \(a_n-b_n=m\), la primera ecuación equivale a
\[
 x^m=u\,p^{-b_n},\qquad y=p/x.
\]
El segundo miembro es no nulo: existen exactamente \(m\) raíces complejas distintas, y cada una produce una solución de ambas ecuaciones. Para \((u,v)=(1,1)\) se obtiene el núcleo indicado. Toda fibra es un trasladado de ese núcleo; numerarla exige elegir una preimagen inicial.

La matriz diferencial es no singular. En general,
\[
 \det D\mathcal Q^n=(-3)^n(xy)^{\epsilon-1}\ne0.
\]
Por tanto, no hay ramificación dentro de \((\mathbb C^\times)^2\).

En el cuadrante positivo hay una sola raíz positiva y una sola preimagen. Para un paso:
\[
 x=(uv^2)^{-1/3},\qquad y=(u^2v)^{-1/3}.
\]
Sobre los complejos no se eligen ambas raíces independientemente: debe mantenerse \(xy=(uv)^{-1}\).

**Precisión de coordenadas.** \(P=xy,O=x/y\) son coordenadas globales en el cuadrante positivo, pero sobre los complejos la aplicación es dos a uno, con núcleo \(\{(1,1),(-1,-1)\}\). El argumento de cobertura anterior conserva \(x,y\) y no añade una ambigüedad artificial de signo.

## 4. Dinámica de fase y memoria de acarreo

En el toro unitario, el lector conserva
\[
 (e^{2\pi i\theta},e^{-2\pi i\theta})
 \longmapsto
 (e^{2\pi i\,3\theta},e^{-2\pi i\,3\theta}).
\]
Sobre ese subgrupo antidiagonal, dos pasos inducen \(\theta\mapsto9\theta\pmod1\).

El representante \(\theta_j\in[0,1)\) y el dígito de acarreo
\[
 d_j=\lfloor3\theta_j\rfloor,\qquad
 \theta_{j+1}=3\theta_j-d_j
\]
dan el registro acumulado
\[
 C_n=\sum_{j=0}^{n-1}d_j3^{n-1-j},\qquad
 \boxed{\theta_0=\frac{\theta_n+C_n}{3^n}.}
\]
La prueba es telescópica, o por inducción usando \(C_{n+1}=3C_n+d_n\). El dato de fase reducido admite \(3^n\) preimágenes; \(n\) dígitos ternarios conservan cuál era la inicial. Para dos pasos, el dígito de base nueve es \(3d_0+d_1\).

Las ramas inversas \(B_d(\theta)=(\theta+d)/3\) satisfacen
\[
 B_a\circ B_b(\theta)=\frac{\theta+b+3a}{9}.
\]
El orden de composición se conserva en el registro. Ni el residuo ni el cardinal de preimágenes sustituyen esa información.

Esto proporciona un ejemplo operatorio exacto de reducción con recuperación por acarreo. Su identificación con la conexión nonádica completa requeriría componer el mapa de estados correspondiente: aquí no se afirma que este registro de fase reconstruya hojas, vacancias, torsión y supervivencia de todo el TPK.

## 5. Fricke: el valor invariante y el parámetro orientado

Sea \(s=4096/t\). La transformación \(t\mapsto s\) es una involución y conserva \(T=t+s+24\), pero generalmente no conserva \(j\).

Denotemos
\[
 j_1=\frac{(t+256)^3}{t^2},\qquad
 j_2=\frac{(s+256)^3}{s^2}.
\]
Entonces
\[
 \boxed{j_1-j_2=(s-t)(T+23),}
\]
\[
 \boxed{j_1+j_2=T^2+T-7256,\qquad
        j_1j_2=(T+248)^3.}
\]
Por tanto, ambos valores son raíces de
\[
 X^2-(T^2+T-7256)X+(T+248)^3=0.
\]
Su discriminante factoriza:
\[
 \boxed{\Delta=(T-152)(T+104)(T+23)^2.}
\]

**Prueba.** Se tiene \(ts=4096\) y
\(j_1=t+768+48s+s^2\), con la expresión conjugada para \(j_2\). Restar y sumar produce las dos primeras identidades. Para el producto,
\[
 j_1j_2
 =\frac{((t+256)(s+256))^3}{(ts)^2}
 =(T+248)^3.
\]
La diferencia al cuadrado da la factorización del discriminante, pues
\((s-t)^2=(T-24)^2-16384=(T-152)(T+104)\).

Es una correspondencia dinámica entre dos lecturas modulares del mismo par involutivo, no una identidad entre los operadores Fricke y la involución anterior de ambivalencia.

## 6. Recuperación por dos lecturas y una excepción estructural

Si \(T\ne-23\), el par ordenado \((T,j_1)\) recupera \(t\):
\[
 \boxed{t=\frac{T^2-j_1-3904}{T+23}.}
\]
La prueba consiste en sustituir \(s^2=(T-24)s-4096\) en la expresión de \(j_1\). Elegir cuál de los dos valores \(j_1,j_2\) se publica conserva la orientación que \(T\) solo identifica.

En \(T=-23\) aparecen dos parámetros distintos,
\[
 t_\pm=\frac{-47\pm45i\sqrt7}{2},
 \qquad t_+t_-=4096,
\]
que comparten
\[
 (T,j)=(-23,-3375).
\]
No son puntos fijos de Fricke. Los puntos fijos son \(t=\pm64\), que publican respectivamente \((152,8000)\) y \((-104,1728)\).

Incluso dos valores escalares pueden, por tanto, coincidir sin determinar la posición en esta correspondencia. La derivada recupera la diferencia. La identidad
\[
 j_1=(T+23)s+T-3352
\]
implica
\[
 \frac{dj_1}{dt}
 =(s+1)\frac{dT}{dt}+(T+23)\frac{ds}{dt}.
\]
En los dos parámetros excepcionales \(dT/dt\ne0\), y
\[
 \left.\frac{dj_1}{dT}\right|_{T=-23}=s+1
 =\frac{-45\pm45i\sqrt7}{2}.
\]
Las dos pendientes son diferentes. En ese punto, el primer jet distingue lo que el par de valores no distingue. Dado el jet \(p=dj_1/dT\), se recupera \(s=p-1\) y \(t=-46-p\).

**Estructura cuadrática seleccionada por la coincidencia de lectores.** La ecuación de los dos parámetros es \(t^2+47t+4096=0\), de discriminante \(-45^2\cdot7\). Por ello
\[
 \mathbb Q(t_+)=\mathbb Q(t_-)=\mathbb Q(\sqrt{-7}),\qquad
 \lambda=\frac{2t+47}{45},\quad\lambda^2=-7.
\]
No se introdujo ese cuerpo para escoger la coincidencia: se obtiene después de resolverla. En él, Fricke \(t\mapsto4096/t\) coincide con la conjugación cuadrática, con traza \(-47\) y norma \(4096\). Las dos orientaciones se intercambian mientras \(T\) y \(j\) permanecen iguales. El jet conserva el mismo cuerpo: \((2p+45)^2=-45^2\cdot7\). Ésta es una relación adicional entre involución, campo de definición y dato diferencial; no una identificación numérica con otros usos de \(7\) o \(45\) en APP.

No se atribuye este fenómeno a la totalidad del estado HMT: se ha demostrado en la correspondencia modular documentada. Es un caso preciso en el que conservar la ley local, y no sólo su resultado numérico, cambia la capacidad de recuperación.

## 7. Acoplamiento de niveles dos y cinco sobre la misma lectura modular

La contribución coordinada de Overleaf demuestra la reducción de Klein–Ramanujan. Con \(x=R(q)^5\), \(u=x-x^{-1}\),
\[
 j=-\frac{(u^2-228u+496)^3}{(u+11)^5}.
\]
Se conserva el mismo argumento modular o la rama elegida para componerla con el lector \(t=t_2\). Eliminar \(j\) da
\[
 \boxed{(t+256)^3(u+11)^5
       +t^2(u^2-228u+496)^3=0.}
\]
Ésta reúne en una relación algebraica el lector pentádico, la traza de la involución reticular y el carácter modular. No identifica sus involuciones ni permite elegir independientemente sus ramas.

El límite de autoescala del lector de nivel cinco es
\[
 x\to\varphi^{-5}=\frac{5\sqrt5-11}{2},\qquad u\to-11.
\]
Sea \(\epsilon=u+11\). El mismo enlace adopta la forma
\[
 j=-\frac{(3125-250\epsilon+\epsilon^2)^3}{\epsilon^5}
   =\frac{(t+256)^3}{t^2}.
\]
El orden de aproximación depende de la rama conservada:

- Si \(\epsilon\to0\) y \(t\to0\),
\[
 \boxed{\frac{t^2}{(-\epsilon)^5}\longrightarrow
        \frac{256^3}{3125^3}=\frac{2^{24}}{5^{15}}.}
\]
- Si \(\epsilon\to0\) y \(t\to\infty\),
\[
 \boxed{t\,\epsilon^5\longrightarrow-5^{15}.}
\]

**Prueba.** Para la primera rama, la igualdad racional da exactamente
\[
 \frac{t^2}{(-\epsilon)^5}
 =\frac{(t+256)^3}{(3125-250\epsilon+\epsilon^2)^3};
\]
se toma el límite. Para la segunda, \((t+256)^3/t^2=t(1+256/t)^3\), y la misma igualdad proporciona el límite. Estas conclusiones se refieren a las ramas con los límites indicados; no escogen una trayectoria HMT mediante el valor final.

Los órdenes dos y cinco y sus coeficientes proceden de los lectores ya declarados. La relación establece una ley de escalas entre sus parámetros, no otra campaña de aproximación de \(\varphi\). El valor límite áureo queda conectado con el modo de divergencia de \(j\) y con las distintas ramas de su realización reticular.


## 8. Qué añade al mapa dinámico

- El lector de ambivalencia tiene una ley de iteración exacta, no una estructura estática. Su extensión con fase distingue la inversión positiva única del recubrimiento complejo.
- El registro de acarreo hace reversible una reducción de fase. La memoria tiene una regla de actualización y de composición explícita.
- La lectura Moonshine reúne una involución, un invariante y una correspondencia entre valores \(j\). Las fibras y su excepción se calculan, no se presuponen.
- Un jet puede conservar información no recuperable ni siquiera desde dos valores escalares. Este mecanismo da una tarea concreta para otros lectores: determinar cuál es el dato estructural mínimo que los hace separadores.
- Los regímenes cuadráticos, la conexión nonádica, el toro de fases, Fricke y los \(J_\tau\) conservan sus tipos. Sus enlaces requieren los mapas efectivos; no se renombran todos como «la misma dinámica».

El antecedente de nivel cinco también queda localizado: el capítulo16, sección de identidad pentádica, conserva \(R(q)\to\varphi^{-1}\) al aproximarse \(q\) a \(1\) desde abajo y, para dos canales que tienden a uno, el producto tiende a \(\varphi^{-2}\). La introducción enlaza además \(j\) con una expresión racional en \(R(q)^5\). Este reconocimiento límite es contenido previo; no se presenta como resultado nuevo de esta nota. El desarrollo focal de Rogers–Ramanujan permanece coordinado con Overleaf, sin inferir identidades entre sus parámetros y la coordenada de Fricke de nivel dos.

Los ejemplos de curvatura y reloj siguen siendo antecedentes y líneas de exploración, no una lista exhaustiva de HMT.

## 9. Verificación y límites del incremento

El programa adjunto verifica trece identidades y controles de Laurent, tres controles de la coincidencia cuadrática —incluidas fórmulas que deben rechazarse—, trece potencias matriciales, los núcleos de las primeras cinco iteraciones, 231 preimágenes de fases racionales y 420 reconstrucciones de acarreo. Las pruebas anteriores son generales; esos controles son finitos e independientes de campañas de cifras.

La construcción conserva el corte material de trabajo. No se alteran PDFs, manuscritos originales ni scripts científicos previos. El resultado no afirma una nueva fase física de cristal de tiempo ni identifica las distintas involuciones sin un entrelazador. El lector posee una dinámica matemática explícita aun cuando tales identificaciones posteriores no formen parte de este incremento.

## Fuentes y archivos

- [Reducción coordinada de nivel cinco, prueba y fuente primaria](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/PLIEGUE_HOJAS_RETORNO_Y_OCUPACION.md:183>).

- [Antecedente pentádico y límite de autoescala](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:1220>).
- [Enlace declarado entre nivel cinco y j](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/introduccion_general.tex:1306>).

- [Lector de ambivalencia en el capítulo57](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c57_sistema_operatorio_euler_hmt.tex:134>).
- [Antecedente positivo y memoria nonádica](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/02_dinamica_tres_hojas.tex:253>).
- [Álgebras y realizaciones cuadráticas del TRIT](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/09b_algebras_cuadraticas.tex:289>).
- [Reloj observable y extensión con acarreo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03g_ciclo_dodecafasico_tpk_rev7.tex:68>).
- [Traza de Leech, Fricke e invariante modular](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/15d_voa_moonshine_orden_dos_rev11.tex:30>).
- [Código de identidades exactas](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/verificar_dinamica_lectores_Q_Fricke.py>).
- [Recibo de ejecución](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/RECIBO_DINAMICA_Q_FRICKE.json>).
