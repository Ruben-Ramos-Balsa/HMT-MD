# Deformación de covolumen constante del retículo de Leech por la polarización dodecafásica

## Alcance y procedencia

Esta nota compone dos resultados ya materializados: la realización reticular excepcional del artículo IV y la polarización del registro dodecafásico del artículo X. La composición exponencial, el teorema de dualidad euclídea, su testigo de pérdida de integralidad y la realización duplicada son una formalización nueva de esos datos. La búsqueda focal aquí realizada no autoriza a atribuir esta fórmula exponencial específica a los artículos previos.

El dato se recibe después de APP, TRIT y TPK. Su cadena publicada es estado terminal enriquecido, registro dodecafásico, lectores de incidencia y orientación, y registro entero \(K\). La realización de representación actúa después sobre ese registro; no elige sus coordenadas. La realización reticular procede de la incidencia de frontera del mismo estado, con código de pegado y origen marcado. Las construcciones del continuo que anteceden a estas realizaciones mantienen su carácter conjunto; esta nota comienza en dos salidas posteriores ya construidas y no redefine el generador.

Se conserva una carta marcada común de doce posiciones. La asignación de la coordenada \(u_j\) al plano \(E_j\) es parte explícita de esta composición: fija una realización marcada, sin afirmar que sea independiente de toda permutación de las doce etiquetas.

## Datos exactos recuperados

El registro y su suma son
\[
 K=(234,543,140,729,659,824,621,58,914,794,146,601),
 \qquad \sum_{j=1}^{12}K_j=6263.
\]
En la representación por permutaciones de las doce clases de \(A_5/C_5\), con orden de representantes y distinción de clases de orden cinco fijados por el propietario, se define
\[
 P_3=\frac3{60}\sum_{a\in A_5}\chi_3(a^{-1})\rho(a),
 \qquad P_{11}=I_{12}-\frac1{12}\mathbf1\mathbf1^{\mathsf T}.
\]
La suma finita verifica
\[
 P_3=P_3^{\mathsf T}=P_3^2,\quad
 \operatorname{rank}P_3=3,\quad P_3\mathbf1=0,\quad
 P_3P_{11}=P_3.
\]
Por tanto la polarización publicada es
\[
 u=P_3P_{11}K=P_3K,\qquad
 \sum_j u_j=0,\qquad
 \|u\|^2=\frac{6638585+2275584\sqrt5}{20}>0.
\]
Su evaluación en el orden marcado es
\[
\begin{aligned}
u={}&(-495/4-233\sqrt5/10,\quad 403/4+169\sqrt5/10,\\
&-403/4-169\sqrt5/10,\quad 495/4+233\sqrt5/10,\\
&601/4+1031\sqrt5/10,\quad203/4+211\sqrt5/5,\\
&-203/4-211\sqrt5/5,\quad-601/4-1031\sqrt5/10,\\
&313/4+569\sqrt5/10,\quad162+219\sqrt5/20,\\
&-162-219\sqrt5/20,\quad-313/4-569\sqrt5/10).
\end{aligned}
\]

El espacio euclídeo ambiente del artículo IV es
\[
 E=\bigoplus_{j=1}^{12}E_j,\qquad
 B=\operatorname{diag}(B_2,\ldots,B_2),\qquad
 B_2=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}.
\]
Cada \(E_j\) es el plano real generado por un factor \(A_2\). La descomposición es ortogonal en el espacio ambiente; el retículo de Leech no es una suma directa de doce retículos \(A_2\). El código ternario \(C_W\) pega esos factores para construir \(N=N(C_W)\). El vecino marcado
\[
 v_\alpha=4\rho_1+\rho_2+\cdots+\rho_{12},\quad
 \rho_j=(1,1)_j,\quad v_\alpha^2=54,
\]
\[
 N_{\alpha,0}=\{x\in N:\langle x,v_\alpha\rangle_B\equiv0\bmod3\},
 \qquad \Lambda=N_{\alpha,0}+\mathbb Z\,v_\alpha/3
\]
es, en el propietario, positivo, par, unimodular y sin raíces de rango \(24\), y por ello una realización del retículo de Leech. En particular \(\Lambda^*=\Lambda\), donde el dual se toma respecto de \(B\).

La misma fuente construye
\[
 C=\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\qquad
 R=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 c_*=(1,1,1,1,1,1,2,1,1,1,1,1)
\]
y
\[
 P_j=\begin{cases}R,&(c_*)_j=1,\\ I_2,&(c_*)_j=2,\end{cases}
 \qquad g_c=\bigoplus_jP_jCP_j^{-1}.
\]
Aquí \(P_j\) es un marco bidimensional; \(P_3\) es el proyector de rango tres anterior. La prueba del propietario establece
\[
 g_c^3=I,\quad g_c^2+g_c+I=0,\quad
 g_c^{\mathsf T}Bg_c=B,\quad g_c\Lambda=\Lambda.
\]
La estabilidad del vecino utiliza que las clases de
\((g_cv_\alpha-v_\alpha)/3\) y \((g_c^{-1}v_\alpha-v_\alpha)/3\)
son \(c_*\) y \(-c_*\) y que ambos productos con \(v_\alpha\) son \(-27\).

## Flujo anisótropo de covolumen constante

Para un parámetro real adimensional \(s\), definimos
\[
 H_u=\bigoplus_{j=1}^{12}u_jI_2,\qquad
 D_s=\exp(sH_u)=\bigoplus_{j=1}^{12}e^{su_j}I_2,\qquad
 \Lambda_s=D_s\Lambda.
\]
El operador escala cada plano por el coeficiente de polarización que corresponde a su etiqueta. La desigualdad \(e^{su_j}>0\) conserva su orientación local. La familia satisface
\[
 D_{s+t}=D_sD_t,\quad D_0=I,\quad D_s^{-1}=D_{-s},
 \quad D_s^\dagger=D_s,\quad D_sg_c=g_cD_s,
\]
donde \(A^\dagger=B^{-1}A^{\mathsf T}B\). Las primeras identidades se verifican bloque a bloque. La autoadjunción procede de que cada bloque es escalar, y la conmutación utiliza la misma descomposición por planos de \(g_c\). Finalmente,
\[
 \det D_s=\prod_{j=1}^{12}e^{2su_j}
 =\exp\!\left(2s\sum_j u_j\right)=1.
\]
Así, \(\Lambda_s\) es una red discreta de rango \(24\) y covolumen uno para todo \(s\), porque una aplicación lineal invertible transporta una red y multiplica su covolumen por su determinante absoluto. La isometría \(g_c\) preserva cada \(\Lambda_s\):
\[
 g_c\Lambda_s=g_cD_s\Lambda=D_sg_c\Lambda=D_s\Lambda.
\]
Conserva su orden tres y su ausencia de vectores fijos. La construcción preserva esta simetría explícita; no transporta automáticamente todo el grupo de automorfismos de Leech.

El parámetro \(s\) queda libre en esta familia. La nota deriva la dirección \(u\) del registro y construye su flujo; no selecciona un valor físico de \(s\). Una normalización \(u/\|u\|\) produciría la misma familia con otra parametrización.

## Dualidad euclídea exacta

Para una red \(L\subset E\), su dual es
\[
 L^*=\{y\in E:\langle y,x\rangle_B\in\mathbb Z
                    \text{ para todo }x\in L\}.
\]
Si \(A\) es invertible, la definición da
\[
 (AL)^*=A^{-\dagger}L^*.
\]
En efecto, \(\langle y,Ax\rangle_B=\langle A^\dagger y,x\rangle_B\) es entero para todo \(x\in L\) exactamente cuando \(A^\dagger y\in L^*\). Aplicando la identidad a \(A=D_s\), la autodualidad de la red inicial y la autoadjunción de \(D_s\) prueban
\[
 \boxed{\Lambda_s^*=\Lambda_{-s}}.
\]
La igualdad es entre el dual euclídeo de una red y la red del parámetro opuesto. La condición adicional \(\Lambda_s=\Lambda_s^*\) equivale a \(D_{2s}\Lambda=\Lambda\), y no se deduce de \(\det D_s=1\). Por esta razón, en el flujo euclídeo se utiliza «covolumen uno» y se reserva «unimodular» en sentido aritmético para las redes integrales autoduales.

## Testigo explícito de deformación efectiva

El vector \(v_\alpha/3\) pertenece a \(\Lambda\). Su norma transportada es
\[
 f(s)=\left\|D_s\frac{v_\alpha}{3}\right\|_B^2
 =\frac29\left(16e^{2su_1}+\sum_{j=2}^{12}e^{2su_j}\right).
\]
Se obtiene
\[
 f(0)=6,\qquad
 f'(0)=\frac49\left(16u_1+\sum_{j=2}^{12}u_j\right)
       =\frac{20}{3}u_1
       =-825-\frac{466}{3}\sqrt5\ne0.
\]
Por continuidad de \(f'\), existe \(\delta>0\) tal que \(f\) es estrictamente monótona en \((-\delta,\delta)\). Reduciendo \(\delta\), también se cumple \(11/2<f(s)<13/2\). Por tanto, para \(0<|s|<\delta\), el valor \(f(s)\) es distinto de \(6\) y no es entero. Una red integral tiene norma entera en todos sus vectores; se concluye que \(\Lambda_s\) no es integral y, en particular, no es isométrica al retículo de Leech en ese intervalo perforado.

Esta prueba distingue deformación geométrica de cambio de coordenadas isométrico. Los coeficientes aparecen en pares opuestos, pero una permutación ambiental que intercambie esos pares no ha sido demostrada aquí como automorfismo del retículo pegado. La reciprocidad del dual no depende de esa afirmación adicional.

## Función theta y reciprocidad por Poisson

Para \(s\in\mathbb R\) y \(t>0\), sea
\[
 \Theta_s(t)=\sum_{\lambda\in\Lambda}
                  \exp\!\left(-\pi t\|D_s\lambda\|_B^2\right).
\]
Si \(M=\max_j|u_j|\), entonces
\[
 e^{-2|s|M}\|x\|_B^2\leq\|D_sx\|_B^2
                  \leq e^{2|s|M}\|x\|_B^2.
\]
La cota inferior compara la serie con una gaussiana sobre una red fija. Esto prueba convergencia absoluta y uniforme sobre compactos de \(\mathbb R\times(0,\infty)\), así como la legitimidad de las derivadas de orden finito después de incorporar sus factores polinomiales.

Tomamos el volumen euclídeo asociado a \(B\) y la convención de Fourier
\[
 \widehat f(y)=\int_E f(x)e^{-2\pi i\langle x,y\rangle_B}\,dx.
\]
La transformada de \(e^{-\pi t\|x\|_B^2}\) es
\(t^{-12}e^{-\pi\|y\|_B^2/t}\). La suma de Poisson, el covolumen uno y la identidad del dual dan
\[
 \boxed{\Theta_s(t)=t^{-12}\Theta_{-s}(t^{-1})}.
\]
En particular, \(\Theta_s(1)=\Theta_{-s}(1)\). Es una identidad analítica de series completas; el verificador finito no la sustituye por una suma truncada.

La extensión holomorfa
\[
 \theta_s(\tau)=\sum_{\lambda\in\Lambda}
        e^{\pi i\tau\|D_s\lambda\|_B^2},
 \qquad \operatorname{Im}\tau>0,
\]
converge normalmente y satisface
\[
 \theta_s(-1/\tau)=(-i\tau)^{12}\theta_{-s}(\tau).
\]
La transformación relaciona dos miembros de la familia. La periodicidad bajo \(\tau\mapsto\tau+1\), y por ello la promoción a una forma modular escalar del mismo tipo que la theta de Leech, requiere condiciones aritméticas adicionales. El testigo anterior muestra que la paridad e integralidad euclídeas se pierden para pequeños parámetros no nulos. Por la misma razón, la construcción de un álgebra de vértices reticular y sus resultados Moonshine no se transporta sin verificar sus hipótesis.

La suma de Poisson puede verificarse aquí directamente. Para una red \(L\) y la gaussiana \(f_t(x)=e^{-\pi t\|x\|_B^2}\), periodizamos
\[
 F_t(x)=\sum_{\ell\in L}f_t(x+\ell).
\]
La convergencia normal, también de las derivadas, hace de \(F_t\) una función suave sobre \(E/L\). Para \(\xi\in L^*\), su coeficiente de Fourier es
\[
 c_\xi=\frac1{\operatorname{covol}(L)}
       \int_{E/L}F_t(x)e^{-2\pi i\langle x,\xi\rangle_B}\,dx
 =\frac{\widehat f_t(\xi)}{\operatorname{covol}(L)}.
\]
La segunda igualdad descompone \(E\) en traslaciones de un dominio fundamental; el carácter vale uno sobre \(L\). El producto de las integrales gaussianas unidimensionales en una base ortonormal da
\(\widehat f_t(\xi)=t^{-12}e^{-\pi\|\xi\|_B^2/t}\).
Evaluar la serie de Fourier absolutamente convergente en \(x=0\) prueba la fórmula usada. Esta demostración y las convenciones de theta pueden cotejarse en [Noam D. Elkies, *Theta functions and weighted theta functions of Euclidean lattices, with some applications*, teorema 2, pp. 10–11](https://people.math.harvard.edu/~elkies/aws09.pdf). La fuente usa el signo positivo en Fourier; ambas convenciones coinciden sobre la gaussiana par.

## Realización integral duplicada de signatura \((24,24)\)

Sobre \(E\oplus E\) consideramos la forma bilineal
\[
 \mathcal B((x,p),(x',p'))=\langle x,p'\rangle_B+
                                      \langle p,x'\rangle_B.
\]
Su signatura es \((24,24)\). Definimos
\[
 \mathcal D_s=D_s\oplus D_{-s},\qquad
 \Gamma_s=\mathcal D_s(\Lambda\oplus\Lambda)
         =\{(D_s\lambda,D_{-s}\mu):\lambda,\mu\in\Lambda\}.
\]
La autoadjunción y reciprocidad de los bloques prueban
\(\mathcal B(\mathcal D_s\xi,\mathcal D_s\eta)=\mathcal B(\xi,\eta)\).
Por tanto \(\mathcal D_s\in O(\mathcal B)\).

La red \(\Gamma_0=\Lambda\oplus\Lambda\) es integral y par para \(\mathcal B\), porque los productos cruzados son enteros y
\[
 \mathcal B((\lambda,\mu),(\lambda,\mu))=2\langle\lambda,\mu\rangle_B
 \in2\mathbb Z.
\]
Su dual respecto de \(\mathcal B\) es ella misma: al emparejar con \((\lambda,0)\) y \((0,\mu)\), las dos coordenadas de un vector dual deben pertenecer a \(\Lambda^*=\Lambda\). Como \(\mathcal D_s\) es isometría de \(\mathcal B\), toda \(\Gamma_s\) es integral, par y autodual para esta forma partida.

La integralidad partida sobrevive incluso cuando la proyección euclídea \(\Lambda_s\) deja de ser integral. Son dos afirmaciones con métricas y dominios diferentes. Las \(\Gamma_s\) son isométricas como redes abstractas partidas; su presentación mediante las dos proyecciones euclídeas varía con \(s\).

La involución \(J(x,p)=(p,x)\) verifica
\[
 J\Gamma_s=\Gamma_{-s},\qquad
 J\mathcal D_sJ=\mathcal D_{-s}.
\]
En las coordenadas \(p_L=(x+p)/\sqrt2\), \(p_R=(x-p)/\sqrt2\),
\[
 \mathcal B((x,p),(x,p))=\|p_L\|_B^2-\|p_R\|_B^2;
\]
\(J\) fija \(p_L\) e invierte \(p_R\). Esta es una dualidad exacta de la construcción reticular duplicada; una identificación física específica conserva además los datos de representación que requiera su dominio.

## Energía positiva y conjugación unitaria

El análogo reticular de la energía de radio recíproco del artículo IV es
\[
 \mathcal E_s(\lambda,\mu)=
       \|D_s\lambda\|_B^2+\|D_{-s}\mu\|_B^2.
\]
Satisface
\[
 \mathcal E_s(\lambda,\mu)=\mathcal E_{-s}(\mu,\lambda).
\]
En \(\ell^2(\Lambda\oplus\Lambda)\), el operador de multiplicación
\[
 (H_s\psi)(\lambda,\mu)=\mathcal E_s(\lambda,\mu)\psi(\lambda,\mu)
\]
tiene dominio
\[
 \mathcal D(H_s)=
 \left\{\psi:\sum_{\lambda,\mu}
       \mathcal E_s(\lambda,\mu)^2|\psi(\lambda,\mu)|^2<\infty\right\}.
\]
Es positivo y autoadjunto. La cota cuadrática inferior implica que sólo existen finitos pares de red por debajo de cada nivel de energía, y por ello su resolvente es compacto. La aplicación unitaria
\((U\psi)(\lambda,\mu)=\psi(\mu,\lambda)\) satisface
\[
 U\mathcal D(H_s)=\mathcal D(H_{-s}),\qquad UH_sU^{-1}=H_{-s}.
\]
La igualdad conserva los dominios, además de los autovalores. Esta composición recupera la estructura del teorema de dualidad escalar del artículo IV y la realiza en los doce planos marcados.

## Localizadores internos y alcance del certificado

Raíz IV:

/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/04_MOONSHINE_DUALIDAD_TEORIA_M_ES/documentacion_original/payload/

- sections/excepcional.tex:601–750: doce factores, pegado de Niemeier y vecino de Leech; etiquetas exc:leech, exc:vector, exc:vecino y exc:teorema-leech.
- sections/moonshine_comparacion.tex:28–120: marcos, isometría de orden tres y estabilidad del vecino; etiquetas km:coxeter-reflexion, km:palabra-total, km:isometria-ternaria, km:estabilidad-vecino.
- sections/moonshine_comparacion.tex:128–190: continuación reticular hacia el álgebra de vértices y orbifold; sus hipótesis de paridad e integralidad no se trasladan al flujo euclídeo automáticamente.
- sections/02_dualidad_t.tex:14–140: energía de radio recíproco, dominio y conjugación unitaria; etiquetas iv:thm:dualidad-escalar e iv:thm:t-unitaria.

Raíz X:

/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/

- source/libro/01_acoplamiento.tex:52–125: genealogía del registro dodecafásico y \(K\).
- source/sections/k_direccion_dimensional.tex:13–98: representación marcada, proyector \(P_3\), vector \(u\), suma nula y norma exacta.
- supplement/vendor/variacional/controles_articulo_I/propietarios_k_moonshine/variacional.py:77–234 y 306–364: operaciones exactas en \(\mathbb Q(\sqrt5)\), suma de carácter, proyector y código.

La huella del propietario ejecutable utilizado es

bd1bfff1abec55e2f03477875002d44c01a9732c15348c99f9e211148c900e57

El certificado adjunto comprueba con racionales exactos el proyector, las doce coordenadas, la métrica, la acción de orden tres, la conmutación infinitesimal, los desplazamientos del vecino y la derivada no integral. También comprueba la forma partida y las identidades formales que sostienen el flujo. Las afirmaciones para todos los parámetros, la convergencia y Poisson tienen las pruebas analíticas contiguas anteriores; el cálculo finito no se presenta como prueba autónoma de esos teoremas.
