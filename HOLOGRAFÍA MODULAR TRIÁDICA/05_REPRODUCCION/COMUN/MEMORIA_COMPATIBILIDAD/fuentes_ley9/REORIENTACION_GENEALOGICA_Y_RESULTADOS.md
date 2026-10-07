# Regularidad genealógica, restitución operatoria y geometría de la acción

22 de septiembre de 2026. Cuaderno acumulativo de investigación. Autoría del corpus y de la arquitectura HMT–MD: Rubén. Elaboración focal de las consecuencias expresamente identificadas abajo: asistente, sobre las fuentes citadas.

## 1. Pregunta rectora y conservación del trabajo

La pregunta de Rubén no consiste en sustituir una constante en una ecuación física conocida. Concierne a la relación entre la producción de valores, la compatibilidad de sus estructuras y la restitución de las operaciones que los producen. En particular: ¿qué ocurre cuando una lectura retiene una cifra, una fase o un balance, pero separa la memoria que participa en el siguiente transporte?

El punto de partida se conserva: APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. La actualización efectiva precede a la holonomía nonádica; el operador de memoria reducida es posterior. Las regiones de π, φ, e y α pertenecen a la generación correlacionada del corpus; su reconocimiento convencional y la comparación metrológica son posteriores. Este cuaderno estudia consecuencias de lectores ya construidos, sin sustituir la generación por esas consecuencias.

Se conservan íntegros:

- [Intercambio público de esta investigación](HISTORIAL_PUBLICO_20260919_20260922.md): 91 intervenciones desde la discusión de K del 19 de septiembre hasta la petición de reorientación del día 22. Incluye las respuestas cuestionadas como historia, no como resultados ratificados.
- [Primera nota sobre memoria y vacancias](NOTA.md).
- [Desarrollo de transporte compensado](DESARROLLO_TRANSPORTE_COMPENSADO.md).
- [Desarrollo sobre acción, memoria y trabajo recuperable](ACCION_MEMORIA_TRABAJO_RECUPERABLE.md).
- Sus programas y recibos, que permanecen sin modificación.

La realización gaussiana y el trabajo recuperable quedan como una aplicación auxiliar. La expresión coloquial «electricidad fría» no gobierna el objetivo. No se cambia ningún PDF, fuente editorial o certificado sellado. Esta nota no se presenta como una nueva certificación global del corpus.

## 2. Jerarquía recuperada

El fenómeno primario es una dinámica que conserva procedencia al producir nuevas observaciones. Hay tres operaciones que conviene exponer juntas y distinguir matemáticamente:

1. **Producción:** la actualización APP–TRIT–TPK prolonga el estado y sus regiones correlacionadas. La fase puede retornar mientras la memoria avanza.
2. **Compatibilidad:** las lecturas regionales, angulares, de acción y de incidencia obedecen relaciones comunes. No son parámetros que puedan variarse arbitrariamente uno por uno conservando el mismo estado.
3. **Restitución:** conservar la información complementaria permite recuperar no sólo un valor anterior, sino productos de operadores y diferencias entre órdenes de composición.

La comparación entre procedimientos para obtener π debe atender a esos tres niveles. La tesis específica de HMT reside en la construcción conjunta y sus relaciones, no en la mera existencia de un algoritmo para un decimal. Ni una coincidencia decimal ni la periodicidad de una fase describen por sí solas el alcance de esa construcción. Esta nota no pretende establecer una prioridad histórica mundial: formula qué objeto matemático habría que comparar para estudiarla seriamente.

## 3. Vacancias: tres regímenes recorridos no implican retorno nonádico

### Antecedentes del corpus

El lector de capacidad recibe la compactificación interna 729/1000 y distingue el índice de refinamiento del índice de capacidad. En la convención de la fuente:

\[
\delta=\log_{10}(10/9),\qquad
p_j=\lfloor j/\delta\rfloor,\qquad
v_j=p_j-j,\qquad j\geq1.
\]

Los intervalos entre eventos son

\[
h_j=p_{j+1}-p_j\in\{21,22\},\qquad s_j=22-h_j.
\]

La clase trítica obedece

\[
[v_{j+1}]_3=[v_j-s_j]_3.
\]

Un intervalo corto cambia la clase; uno largo la conserva. Las separaciones 6/7 describen las mesetas de este régimen inducido. No se identifican aquí con dos signos de carga ni con los decimales de π o e. Esta construcción es un factor de observación del estado TPK, no su sustituto.

Fuente: artículo IX, `sections/vacancias_capacidad.tex`, líneas 58–95; monografía del cristal, `cristal_relojes_sincronizacion.tex`, líneas 931–1031. El selector canónico es \(M_{\rm ph}(1+[v_j]_9)\), cuya pauta depende de la clase módulo tres.

### Consecuencia reunida en esta nota

Sea

\[
\beta=22-\delta^{-1},\qquad q_k=\lfloor k/\beta\rfloor,\quad k\geq1.
\]

Las posiciones \(q_k\) son los índices de los intervalos cortos. En efecto,

\[
p_j=22j-\lceil j\beta\rceil,
\quad s_j=\lceil(j+1)\beta\rceil-\lceil j\beta\rceil.
\]

La irracionalidad de δ se obtiene por las valuaciones de 2, 3 y 5 en la igualdad que impondría \((10/9)^q=10^p\); implica la de β. Por ello no hay ambigüedad de extremos para los índices positivos. La discontinuidad que corresponde al entero k ocurre en \(j=\lfloor k/\beta\rfloor\).

**Proposición.** Entre los eventos de índices \(q_k\) y \(q_{k+3}\), tomando los intervalos con índices en \([q_k,q_{k+3})\), vuelve la clase TRIT, pero la fase de capacidad módulo nueve cambia.

**Demostración.** Hay exactamente tres intervalos cortos en ese tramo. Las cotas \(1/7<\beta<3/20\) dan \(20<3/\beta<21\), por lo que

\[
m_k=q_{k+3}-q_k\in\{20,21\}.
\]

La suma de longitudes y la ganancia de capacidad son, respectivamente,

\[
\Delta p=22m_k-3\in\{437,459\},\qquad
\Delta v=21m_k-3\in\{417,438\}.
\]

En ambos casos \(\Delta v\equiv0\pmod3\). En cambio,

\[
\boxed{\Delta v\equiv3\text{ o }6\pmod9.}
\]

Esto prueba la afirmación. Las cotas de β tienen certificados enteros: \(10^{146}>9^{153}\) implica \(\delta>7/153\), y \(10^{417}<9^{437}\) implica \(\delta<20/437\). Por monotonía de \(22-1/x\), se obtiene \(1/7<\beta<3/20\). El programa adjunto verifica estas desigualdades enteras y utiliza además intervalos racionales de logaritmos para comprobar los índices, sin depender de decimales redondeados. ∎

El valor del selector \(\tau_j=M_{\rm ph}(1+[v_j]_9)\) retorna porque depende de la clase módulo tres. No se ha afirmado retorno del estado TRIT completo ni identificado este tramo con una vuelta cronológica de \(\Gamma_9\). Ambas duraciones aparecen infinitas veces por la densidad de la rotación irracional de pendiente \(1/\beta\).

**Interpretación.** La regularidad tiene niveles distintos: se restaura el régimen local mientras sigue desplazada la fase de capacidad. El retorno nonádico del estado tiene, además, su propio incremento de memoria. No hay una única periodicidad que pueda atribuirse indistintamente a todos esos objetos. Los números 437 y 459 son duraciones de esta observación inducida, no nuevas constantes universales.

Este resultado es una composición explícita de fórmulas autorales existentes. No se localizó enunciado así en la búsqueda focal de I, IX y la monografía temporal. Esa búsqueda no establece prioridad histórica.

## 4. La memoria participa en la composición, no sólo en la conservación

### Estructura de partida

El artículo X construye una representación de lectura y memoria a partir de nueve componentes. En una misma fibra, con transporte de referencia identidad, el transporte interno C induce

\[
T_C=\frac{8I+C}{9},\quad
D_C=\frac{\sqrt8(C-I)}9,\quad
R_C=\frac{I+8C}{9},
\]

\[
\mathcal U_C=
\begin{pmatrix}T_C&D_C\\D_C&R_C\end{pmatrix}.
\]

El acoplamiento resulta de separar ocho componentes y una novena, mediante el cambio de base que el corpus construye. Para transportes que conservan la forma declarada, conserva la forma ampliada. La identidad fundamental existente es

\[
\mathcal U_{C_2}\mathcal U_{C_1}=\mathcal U_{C_2C_1},
\qquad T_2T_1+D_2D_1=\frac{8I+C_2C_1}{9}.
\]

El segundo término es la memoria producida en la primera operación y reintroducida en la segunda. Apartarla cambia el procedimiento: se obtiene \(T_2T_1\), no la lectura de la composición completa. Fuente: X, `nuclear/10.tex`, líneas 19–111.

### Consecuencia: reparto exacto de la sensibilidad al orden

**Proposición.** Con \([A,B]=AB-BA\), se cumplen

\[
[T_2,T_1]=\frac1{81}[C_2,C_1],\qquad
[D_2,D_1]=\frac8{81}[C_2,C_1].
\]

Por tanto, la diferencia de lectura entre los dos órdenes, con memoria reintroducida, es

\[
\boxed{
(T_2T_1+D_2D_1)-(T_1T_2+D_1D_2)
=\frac19[C_2,C_1].}
\]

**Demostración.** Al expandir ambos productos de T, los términos constantes y lineales se cancelan en la resta; queda el conmutador dividido por 81. Al expandir los productos de D ocurre la misma cancelación y el factor es 8/81. Su suma es 1/9. ∎

El mecanismo de reentrada ya pertenece al corpus. La resta de ambos órdenes explicita aquí una consecuencia: **en esta representación, la contribución de memoria a la respuesta antisimétrica es ocho veces la retenida por la composición de lecturas aisladas**. La respuesta completa es nueve veces esta última. Son proporciones de operadores de respuesta, no porcentajes de energía.

La restitución conserva la no conmutatividad y su intensidad de lectura. En este caso la compresión por sí sola no anula un conmutador no nulo; lo atenúa. El resultado no identifica por sí solo fuerzas físicas: para esa aplicación se deben conservar los operadores de interacción y el funcional de trabajo que correspondan.

### Contraste exacto, independiente de ajustes decimales

Para el patrón algebraico general \((n-1)+1\), las mismas cuentas dan factores \(1/n^2\), \((n-1)/n^2\) y \(1/n\). La arquitectura nonádica fija n=9. Esto separa la ley de composición del valor particular que toma su normalización.

Si las operaciones efectivas en una aplicación se representan por \(C_1,C_2\), dos procedimientos —apartando la memoria o reintroduciéndola— predicen respuestas de orden distintas. El contraste no consiste en ajustar una constante: consiste en comprobar la composición operacional y la accesibilidad de la memoria.

### Por qué 32/81 no cuenta automáticamente 64 celdas

El mismo corpus da, para C=−I,

\[
T^*T=49I/81,\qquad D^*D=32I/81.
\]

El 32 procede de \(8\,|{-1}-1|^2\). En las nueve componentes de la memoria, la norma incluye \(8^2+8=72\), con denominador \(27^2\). El cuadrado 64 participa en ese cálculo, pero también las otras ocho contribuciones. Identificar el resultado con una región de 64 casillas requiere el mapa de incidencia de esa región, no duplicar 32. La lectura geométrica 8×8 frente a 9×9 permanece una pregunta autoral a conectar con su aplicación concreta; esta nota no la sustituye por una igualdad numérica.

## 5. H5: del carácter genealógico a una coordenada completa de reciprocidad

### Coeficientes y continuación conservados

La matriz central y los invariantes utilizados son

\[
B_c=\begin{pmatrix}7&2\\2&7\end{pmatrix},\quad
\lambda_+=9,\quad\lambda_-=5,
\]

la órbita de longitud cuatro del paso tres, el calendario de longitud doce y el cociente censal 104976/1944=54. La fuente explica

\[
\frac9{16}=\frac{\lambda_+}{4^2},\quad
\frac59=\frac{\lambda_-}{\lambda_+},\quad
\frac7{48}=\frac{\operatorname{tr}B_c/2}{4\cdot12},\quad
\frac1{54}=\frac{1944}{104976}.
\]

La asignación a los grados y los signos pertenece a la definición del carácter; no se deduce de los cardinales aislados. El lector completo utilizado es

\[
H_5=\frac12\sqrt{\frac{1000\alpha}{\varphi}}-\alpha
+\frac9{16}\alpha^2-\frac59\alpha^3
+\frac7{48}\alpha^4-\frac1{54}\alpha^5,
\]

\[
D_A=\exp(-100\pi\alpha/9),\qquad
\mathcal C_\pi=169\alpha^6+\frac{D_A\alpha^7}{1-D_A\alpha},
\qquad \eta_{\rm ret}=H_5-\frac{90}{\pi}\mathcal C_\pi.
\]

La fracción conserva una continuación infinita definida por
\(\mathscr R(z)=D_Az^7+D_Az\mathscr R(z)\), con peso inicial unitario. No se sustituye por un polinomio truncado. Fuente: X, `sections/iv_accion_antecedente.tex`, líneas 119–213.

### Reunión geométrica

Las fuentes dan \(A=1000\alpha\), \(C^*=2(\eta_{\rm ret}+\alpha)\) y la reciprocidad radial. Para conservar ambas orientaciones, sean

\[
\varepsilon\in\{+1,-1\},\quad q=R^4>0,\qquad
\Xi=\varepsilon\frac{1-q}{1+q}.
\]

El recuperador del corpus es

\[
\frac{\eta_{\rm ret}}\alpha=500\Xi-1.
\]

La involución \((\varepsilon,q)\mapsto(-\varepsilon,q^{-1})\) conserva esa acción. Introducimos para reunir esta estructura la coordenada

\[
\boxed{\chi=\varepsilon\log q.}
\]

**Proposición.** χ clasifica exactamente las órbitas de esa involución sobre \(\{\pm1\}\times\mathbb R_{>0}\).

**Demostración.** Cambiar simultáneamente el signo e invertir q conserva χ. Si dos pares tienen el mismo χ, con igual signo tienen igual q; con signos opuestos sus radios cuárticos son recíprocos. Son exactamente los dos casos de pertenencia a una misma órbita. También vale en q=1, cuya órbita conserva las dos orientaciones. ∎

Usando \((1-q)/(1+q)=-\tanh(\log q/2)\), obtenemos

\[
\Xi=-\tanh(\chi/2),\qquad
\boxed{\eta_{\rm ret}=\alpha[-500\tanh(\chi/2)-1].}
\]

La compatibilidad con el carácter completo adopta entonces la forma

\[
\boxed{
\chi=-2\operatorname{artanh}
\left(\frac{H_5+\alpha-(90/\pi)\mathcal C_\pi}{500\alpha}\right).}
\]

El término −α de H5 se cancela con el +α del contraste angular antes de esta lectura. El denominador de la continuación regional permanece completo. Esta igualdad no define retroactivamente α: recibe las salidas y lectores HMT anteriores y reúne sus dos representaciones.

En la rama positiva de acción y radio finito,

\[
0<\eta_{\rm ret}<499\alpha,\quad
\chi<-2\operatorname{artanh}(1/500).
\]

Con α fija,

\[
\frac{\partial\eta_{\rm ret}}{\partial\chi}
=-250\alpha\operatorname{sech}^2(\chi/2)<0.
\]

Por tanto, la sección adimensional de acción determina unívocamente la clase radial orientada en esta representación, y recíprocamente. Para variaciones conjuntas:

\[
d\eta_{\rm ret}=\frac{\eta_{\rm ret}}\alpha\,d\alpha
-250\alpha\operatorname{sech}^2(\chi/2)\,d\chi.
\]

**Contenido conceptual.** H5, la corrección regional y la anisotropía radial orientada no son tres parámetros independientes. El carácter analítico y la geometría de reciprocidad representan la misma sección de retorno. Éste es el nivel de la ecuación de Planck que queda oculto si se pasa directamente a multiplicar h por una frecuencia.

La década de acción conserva su genealogía determinantal independiente de esta reparametrización, y

\[
\hbar_{\rm ret}=10^{-34}\mathcal U_S\eta_{\rm ret},\qquad
\hbar_{\rm pre}=10^{-34}\mathcal U_SH_5.
\]

Se conservan además la acción por vuelta \(h=2\pi\hbar\) y la lectura térmica
\(k_B\Theta_{\rm clk}\log3=h/T_{108}\) en su ámbito. El reloj físico de una realización no se obtiene sólo de renombrar χ. La coordenada χ clasifica esta reciprocidad, no la totalidad de historias TPK.

Procedencia: los recuperadores, la hipérbola y la equivalencia radial están en X, `libro/reciprocidad_radial.tex`, líneas 22–76 y 134–196. La clasificación por χ y la relación diferencial se reúnen aquí como formalización focal; no son una segunda derivación independiente de Planck.

## 6. Una distinción decisiva para el estudio de fuerzas y conservación

La holonomía nonádica del corpus restaura la fase e incrementa la memoria. Si un recorrido cerrado en las fases aumenta el contador entero, ese incremento no puede escribirse como la diferencia de un potencial que dependa sólo de la fase.

La demostración es inmediata y precisa: la suma de diferencias \(F(g_{j+1})-F(g_j)\) en un circuito de fases es cero por telescopía; el incremento de memoria de una vuelta es uno. En cambio, sobre el estado ampliado, el contador m sí registra ese incremento. Un recorrido cerrado en la proyección no era cerrado en el estado completo.

Esto sitúa la cuestión planteada por Rubén sobre conservatividad en el lugar correcto: primero hay que declarar en qué espacio se cierra el recorrido y qué coordenadas participan en la dinámica. No conmutatividad y no conservatividad son propiedades diferentes. La sección 4 controla el orden de operaciones; esta sección controla la diferencia entre un circuito proyectado y un circuito completo. Para estudiar una fuerza concreta, el funcional de acción/trabajo debe actuar sobre el mismo espacio de estados y el mismo transporte.

El hecho de que la memoria aumente tampoco asigna por sí mismo una producción termodinámica. El cuaderno inicial ya prueba que la información de bloques puede crecer con tasa entrópica nula. La restitución operatoria añade ahora otra precisión: conservar información puede significar conservar qué transformaciones se pueden componer, no únicamente cuántos símbolos se almacenan.

## 7. Mi lectura de conjunto

La unidad de estudio que considero más fértil es la **compatibilidad dinámica entre observaciones**, con la memoria como parte de la operación. El valor de una constante es una lectura; su estructura contiene además restricciones sobre otras lecturas y sobre las transformaciones admisibles. El objetivo de ir más lejos se concreta así: obtener relaciones que ya no permitan modificar independientemente valor, orientación, memoria, forma y acción.

Las tres elaboraciones focales recorren ese mismo eje:

- Un ciclo completo de regímenes TRIT aún conserva un desplazamiento nonádico de capacidad: la regularidad no agota el retorno.
- La reentrada de memoria cambia de forma exacta la respuesta al orden de dos operaciones: el historial interviene causalmente.
- El carácter H5 y la geometría radial orientada determinan mutuamente su sección de retorno: la acción tiene una representación estructural recuperable.

No se propone reemplazar la genealogía de π, φ, e y α por estos resultados. Se explicita qué significa conservar esa genealogía al continuar hacia las operaciones y la acción. La investigación siguiente debe componer estos niveles mediante los mapas del corpus que ya comparten, sin identificar sus índices o sus memorias sólo porque usen el mismo nombre.

## 8. Fuentes, verificación y alcance de la entrega

Raíz de las fuentes activas citadas:

`/Users/ruben/Documents/New project/output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/`

- I: `01/ES/source/sections/revision_monodromia.tex`, 13–66 y 129–177: estado, retorno, fases, memoria y capacidad.
- IX: `09/ES/source/sections/vacancias_capacidad.tex`, 58–95: eventos, intervalos y régimen inducido.
- X: `10/ES/source/nuclear/09.tex`, 98–145: restitución de operadores, productos y conmutadores.
- X: `10/ES/source/nuclear/10.tex`, 19–111 y 238–253: acoplamiento, composición y ejemplo 32/81.
- X: `10/ES/source/sections/iv_accion_antecedente.tex`, 119–265: H5, continuación y secciones de acción.
- X: `10/ES/source/libro/reciprocidad_radial.tex`, 22–76 y 134–196: coordenadas hiperbólicas, cancelación y recuperador.
- II: `02/ES/source/sections/10b_boltzmann.tex`, 66–73: identidad térmica de reloj.

El programa `verificar_reorientacion.py` comprueba con aritmética racional las cotas del reloj, los intervalos de las primeras ventanas, las identidades matriciales y la involución del recuperador. Las pruebas generales están escritas arriba; los casos finitos son controles adicionales, no sustitutos de esas pruebas ni certificación del corpus completo.

El expediente es acumulativo y exploratorio. Los antecedentes quedan identificados; los resultados focales mantienen sus dominios y condiciones. No se han recalculado las expansiones de las constantes ni modificado el generador.
