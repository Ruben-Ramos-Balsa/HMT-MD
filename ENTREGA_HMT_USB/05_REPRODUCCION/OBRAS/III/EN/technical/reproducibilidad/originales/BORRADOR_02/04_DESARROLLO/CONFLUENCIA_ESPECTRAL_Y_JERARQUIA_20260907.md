# Transporte orientado, respuesta del vacío y funcional de Barbero–Immirzi

Nota de desarrollo separada — 7 de septiembre de 2026. No modifica el manuscrito, las fuentes copiadas ni el PDF del borrador 02.

## 1. Objeto y precedencia

El objeto de esta nota es reunir y componer realizaciones posteriores del mismo desarrollo APP–TRIT–TPK. El punto de corte está después de sus publicaciones π, φ, e y α y de sus operadores de orientación, profundidad e incidencia. Las ecuaciones siguientes reciben esas publicaciones internas; no seleccionan sus semillas a partir de constantes convencionales o mediciones.

La nota aporta dos composiciones algebraicas explícitas entre lectores que las fuentes describen por separado. Sus antecedentes son autorales y preexistentes. La forma final de las composiciones no se localizó en los propietarios focales consultados; no se reivindica novedad histórica. La verificación de estas identidades no constituye una nueva verificación de toda la generación primaria de constantes ni de sus identificaciones físicas.

### Bifurcación que debe permanecer visible

El propietario A07 construye primero

\[
H_5=\frac12\sqrt{\frac{1000\alpha}{\varphi}}-\alpha
+\frac9{16}\alpha^2-\frac59\alpha^3+\frac7{48}\alpha^4-\frac1{54}\alpha^5,
\]
\[
x_A=\frac{50\pi}{9}\alpha,\qquad D_A=e^{-2x_A},\qquad
\mathscr C_\pi=169\alpha^6+\frac{D_A\alpha^7}{1-D_A\alpha},
\qquad \eta_{\rm ret}=H_5-\frac{90}{\pi}\mathscr C_\pi.
\]

La rama determinantal publica \(\Sigma_H=\varphi\alpha^{16}\) y la década \(\varepsilon_H=-34\). La confluencia da

\[
\hbar_{\rm ret}=\eta_{\rm ret}10^{\varepsilon_H}U_S,
\qquad h_{\rm ret}=2\pi\hbar_{\rm ret}.
\]

La aplicación angular utiliza α y la componente adimensional ya construida:

\[
(A_{\deg},C^*_{\deg})=
([1000\alpha]_{360},[2(\eta_{\rm ret}+\alpha)]_{360}).
\]

La acción evalúa después esos ángulos mediante
\(S(\theta)=\hbar_{\rm ret}\theta_{\rm rad}=h_{\rm ret}\theta_{\deg}/360\).
Esta precedencia no debe comprimirse en una flecha que haga de la magnitud dimensional h el selector de los valores angulares. La fuente ordena primero la construcción de acción y luego la publicación angular; las dependencias funcionales muestran la componente adimensional que comparten.

En las proposiciones siguientes se fija la carta levantada sin reducción adicional módulo 360 y se abrevia \(A=A_{\deg}\), \(C=C^*_{\deg}\), con \(A>|C|\). En esta carta \(A=1000\alpha\). Una igualdad de clases angulares no sustituye la elección de este levantamiento: las exponenciales reales utilizadas no son periódicas módulo 360.

## 2. Catalán, Pell y el cociente constitutivo: composición explícita

### Operadores anteriores al valor

La traza coordinada, sección 10.27, obtiene del desplazamiento dodecafásico \(\mathsf C\) dos espacios de incidencia \(H_3,H_4\), de dimensiones 3 y 4. En ellos:

\[
F(s)=\frac{\det_{H_3}(I-s\mathsf C)}{\det_{H_4}(I-s\mathsf C)}
=\frac{1-s^3}{1-s^4}
=\frac{1+s+s^2}{1+s+s^2+s^3},\qquad 0<s<1.
\]

La misma fuente construye un plano orientado con base ortonormal u,v tal que \(\mathsf C u=v\), \(\mathsf C v=-u\). Su coeficiente resolvente es

\[
k_4(s)=\langle v,(I-s\mathsf C)^{-1}u\rangle=\frac{s}{1+s^2}.
\]

El lector ilimitado de profundidad, sobre \(N\delta_n=n\delta_n\), conserva el carácter orientado \(Q_4\delta_n=\sin(n\pi/2)\delta_n\). Su segundo momento satisface

\[
\mathcal C_2(s)=\operatorname{Tr}(N^{-2}s^NQ_4)
=\sum_{k\ge0}\frac{(-1)^k s^{2k+1}}{(2k+1)^2},
\quad \mathcal D=s\partial_s,
\quad \mathcal D^2\mathcal C_2(s)=k_4(s).
\]

Dos integraciones logarítmicas con condiciones nulas en cero reconstruyen el momento. Su límite en \(s\uparrow1\) es la constante de Catalán \(G_{\rm Cat}\). Se distingue de la constante gravitatoria G.

### Proposición 1. Relación diferencial constitutiva

En la orientación anterior y para \(0<s<1\),

\[
\boxed{F(s)=\frac{1+s+s^2}{s(1+s)}\,\mathcal D^2\mathcal C_2(s).}
\]

**Prueba.** Sustituir \(\mathcal D^2\mathcal C_2=s/(1+s^2)\) y utilizar \((1+s)(1+s^2)=1+s+s^2+s^3\). Todos los denominadores son positivos en el dominio. La representación resolvente y el plano orientado identifican el antecedente operatorio; no se trata sólo de ajustar una igualdad entre números finales.

Con los canales ya construidos

\[
q_\pm=e^{-\pi(A\pm C)/180},\qquad s_\pm=q_\pm^{30},\qquad r_\pm=F(s_\pm),
\]

las publicaciones normalizadas del vacío quedan expresadas como

\[
\boxed{\widehat\varepsilon=
\left[\frac{1+s_++s_+^2}{s_+(1+s_+)}\mathcal D^2\mathcal C_2(s_+)\right]^2,
\quad
\widehat\mu=
\left[\frac{1+s_-+s_-^2}{s_-(1+s_-)}\mathcal D^2\mathcal C_2(s_-)\right]^2.}
\]

La incidencia de Catalán es, por tanto, la de su familia de momentos y su núcleo orientado. No se sustituye esa familia por el único número \(\mathcal C_2(1)\).

### La escala de Pell dentro de la misma familia

La fuente D07 ya prueba, para \(\lambda_{\rm Pell}=2+\sqrt3\) y \(\rho_{\rm Pell}=\lambda_{\rm Pell}^{-1}\),

\[
\mathcal C_2(\rho_{\rm Pell})=
\frac23G_{\rm Cat}-\frac{\pi}{12}\log\lambda_{\rm Pell},
\quad
\mathcal D\mathcal C_2(\rho_{\rm Pell})=\frac\pi{12},
\quad
\mathcal D^2\mathcal C_2(\rho_{\rm Pell})=\frac14.
\]

La última identidad equivale a \(\rho_{\rm Pell}+\rho_{\rm Pell}^{-1}=4\). La realización helicoidal del capítulo 63 añade la compatibilidad
\(\nu\log\lambda_{\rm Pell}+\ell\pi/2\in2\pi\mathbb Z\).
Aquí Pell es la dilatación del transporte con cuarto de giro; Catalán es el momento de profundidad del carácter orientado. Ninguna de estas relaciones impone \(s_\pm=\rho_{\rm Pell}\): introducir esa igualdad cambiaría la construcción angular.

La orientación de \(k_4\) es parte de la proposición. Invertir \(\mathsf C\) conservando las marcas u,v cambia su signo, mientras deja invariante el cociente determinantal; la fórmula escrita corresponde a la orientación fijada, no a una identificación sin marcas.

## 3. Barbero como funcional del operador de vacío con orientación conservada

El lector dodecafásico preexistente es

\[
S_m(q)=\frac{q^m}{1-q^{3m}},
\qquad
\gamma=\frac{\pi AC}{180}
+12\bigl[S_{90}(q_-)-S_{90}(q_+)\bigr]
-\bigl[S_{120}(q_-)-S_{120}(q_+)\bigr].
\]

El factor 3 del denominador es esencial. Sus residuos conservan
\(12/270-1/360=1/24\); usar \(1-q^m\) daría otra expresión.

La función F anterior es una biyección de \((0,1)\) sobre \((3/4,1)\), pues

\[
F'(s)=-\frac{s^2(s^2+2s+3)}{(1+s+s^2+s^3)^2}<0.
\]

Su inversa \(\psi\) es la única raíz en \((0,1)\) de
\(rs^3+(r-1)(s^2+s+1)=0\). Definamos

\[
\mathcal H(s)=\frac{12s^3}{1-s^9}
-\frac{s^4}{1-s^{12}}
-\frac{(\log s)^2}{20\pi}.
\]

### Proposición 2. Factorización orientada de γ

En la carta y dominio declarados,

\[
\boxed{\gamma=\mathcal H(s_-)-\mathcal H(s_+)
=\mathcal H(\psi(r_-))-\mathcal H(\psi(r_+)).}
\]

**Prueba.** La sustitución \(s=q^{30}\) da \(S_{90}(q)=s^3/(1-s^9)\) y \(S_{120}(q)=s^4/(1-s^{12})\). Además,

\[
\log s_\pm=-\frac\pi6(A\pm C),\qquad
\frac{(\log s_+)^2-(\log s_-)^2}{20\pi}=\frac{\pi AC}{180}.
\]

La suma de estas identidades prueba la primera igualdad. La segunda usa \(\psi(F(s_\pm))=s_\pm\). Es una inversión posterior del lector; no convierte μ o ε medidos en generadores de α o γ.

Sobre el cociente de dos canales, con \(R=\operatorname{diag}(1,-1)\) y \(V=\operatorname{diag}(r_+,r_-)\), la misma relación se escribe

\[
\boxed{\gamma=-\operatorname{tr}_2\bigl[R\,\mathcal H(\psi(V))\bigr].}
\]

La marca R distingue los canales. El espectro sin ordenar de V no determina el signo de γ. Esta traza bidimensional no se identifica con la traza sobre todo el estado enriquecido.

También se puede utilizar el par de coordenadas normalizadas

\[
\widehat Z=r_-/r_+,\quad\widehat c=(r_-r_+)^{-1},\quad
r_+=(\widehat Z\widehat c)^{-1/2},\quad
r_-=(\widehat Z/\widehat c)^{1/2}.
\]

La rama positiva exige \(1<\widehat Z\widehat c<16/9\) y \(9/16<\widehat Z/\widehat c<1\), además de la compatibilidad con los canales previamente generados. El intercambio orientado conserva \(\widehat c\), invierte \(\widehat Z\) y cambia el signo de γ. Una lectura que conserve sólo \(\widehat c\) omite esa distinción.

## 4. De área a información: la segunda coordenada necesaria

La fuente B03 define el operador areal adimensional, que aquí se distingue de su realización física mediante el subíndice «adim»:

\[
\widehat{\mathcal A}_{\rm adim}=\gamma a_0N,
\quad N=N_{90}+N_{120},
\quad a_0=\frac{1+2\cos10^\circ}{3}\,\frac{C\pi}{1080}.
\]

La fuente B04 declara la lectura modular con

\[
\Delta_{\rm mod}=\frac{(A-C)\pi/180}{9\cdot90}
\left(1-\frac7{12}\frac\pi{729}\right),\qquad
K_\Omega=c_\Omega I+\Delta_{\rm mod}\mathscr D,
\quad\mathscr D=90N_{90}+120N_{120}.
\]

El manuscrito debe reproducir esta fórmula y su procedencia al introducir \(\Delta_{\rm mod}\), no usar el símbolo como un coeficiente inexplicado. En esta nota se recupera la fórmula de su propietario; no se adjudica por esa recuperación una nueva prueba del origen de todos sus factores.

La matriz de incidencia tiene determinante 30. Por eso:

\[
\boxed{N_{90}=\frac{120N-\mathscr D}{30},\qquad
N_{120}=\frac{\mathscr D-90N}{30}.}
\]

Área y observable modular conservan conjuntamente las dos ocupaciones. Para inferir N y \(\mathscr D\) desde observables normalizados se requiere conocer los factores anteriores y que \(\gamma a_0\) y \(\Delta_{\rm mod}\) sean no nulos. No se infieren automáticamente las correlaciones del estado completo de dos ocupaciones.

La fuente construye el estado reducido de cada enlace y su producto; una purificación global identifica la entropía reducida con entrelazamiento a través del corte. Esta purificación, el espectro y las normalizaciones forman parte de la exposición: escribir sólo «Barbero → entropía» elimina la operación que debe explicarla.

## 5. Propuesta editorial derivada de estas ecuaciones

El centro del artículo no debería ser una lista de constantes. Propongo presentar una pregunta estructural concreta: **qué información del transporte orientado permanece en la acción, en el operador constitutivo y en el área, y qué observables adicionales permiten recuperarla**.

La secuencia de exposición sería:

1. Construcción APP–TRIT–TPK necesaria para las publicaciones previas, orientación, memoria e incidencia; generación de α antes del par angular.
2. Bifurcación regional y determinantal de la acción; confluencia adimensional y publicación de los ángulos, manteniendo los levantamientos.
3. Operador angular, sus dos canales y cálculo funcional: cociente del vacío, funcional dodecafásico y proposición 2. Aquí queda demostrada una relación horizontal concreta, no solamente el origen compartido.
4. Plano de cuarto de giro y lector de profundidad: proposición 1, escala de Pell y momento de Catalán. La conexión con el vacío justifica su presencia; no se inserta un catálogo separado.
5. Área, Hamiltoniano modular, recuperación sectorial y purificación. Las representaciones CKM se sitúan en la sección donde se explicite el transporte de la involución; las tablas fenomenológicas completas pueden ir en un trabajo posterior.
6. Realización gravitatoria: mantener la dependencia de acción, escala y marco geométrico explícita. El capítulo de confluencia aporta \(\ell_P/E_P=G/c^4\) y \(E_P\ell_P=\hbar c\); reunir sus constructores es más sustantivo que añadir G al título. El alcance cosmológico más extenso necesita su propia exposición.

Título provisional coherente con este núcleo: **«Transporte orientado y relaciones constitutivas en Holografía Modular Triádica: acción, vacío y estructura de área»**. Es una propuesta, no un cambio de portada.

Cada interludio narrativo debe explicar una pérdida o recuperación concreta: determinante frente a coeficiente orientado; producto frente a cociente de canales; área frente a ocupaciones sectoriales; retorno de fase frente a memoria de transporte. Esa narrativa tiene contenido matemático verificable y permite conservar jerarquía sin convertir el artículo en una lista de instrucciones internas.

## 6. Procedencia y alcance de la comprobación

- Bifurcación y ángulos: [A07](../01_FUENTES/A07/capitulo_14_apertura_causal_accion_parangular.tex), ecuaciones `c14-eta-directa`, `c14-hbar-tipado`, `c14-mapa-parangular`.
- Vacío e inversión: [D06](../01_FUENTES/D06/INTERRELACIONES_ESTRUCTURALES_VACIO.md), secciones 1–4 y 7.
- Pell y Catalán: [D07](../01_FUENTES/D07/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md), sección 9.
- Cuerpo de Barbero: [B06](../01_FUENTES/B06/c51_barbero_area_informacion.tex), funcional orientado.
- Incidencia y pesos: [B01](../01_FUENTES/B01/c43_precedencia_dodecafasica_20260905.tex).
- Área: [B03](../01_FUENTES/B03/c43_operador_area.tex).
- Estado modular: [B04](../01_FUENTES/B04/parte_iv_area_hamiltoniano_memoria.tex).
- Plano, resolvente y entrelazador: [traza coordinada, §10.27](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/TRAZA_GENERATIVA_COORDINADA.md:1676>).
- Compatibilidad electromagnética de Pell: [capítulo 63](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/espirales/cap63_realizacion_electromagnetica.tex:100>).

El programa adjunto comprueba identidades polinómicas generales con coeficientes racionales, los factores y signos sensibles, y ejemplos racionales separados de las pruebas generales. La monotonía, los límites, las identidades logarítmicas y la composición de cálculo funcional se justifican en el texto; el programa no es un asistente de pruebas de análisis. No calcula prefijos de π, φ, e o α ni evalúa ajustes metrológicos. Las proposiciones 1 y 2 son composiciones posteriores; no reemplazan los propietarios de la generación.
