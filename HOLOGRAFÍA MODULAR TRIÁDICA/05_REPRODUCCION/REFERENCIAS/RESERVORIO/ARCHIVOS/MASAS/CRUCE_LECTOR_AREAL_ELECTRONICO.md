# El lector areal y la estructura electrónica

La conexión entre la lectura areal y el electrón ya está escrita en el capítulo de construcción electrónica. Las coordenadas positivas \(\pi_{\rm HMT}\) y \(\varphi_{\rm HMT}\), junto con \(e_{\rm HMT}\) y \(\alpha_{\rm HMT}\), pertenecen a las salidas correlacionadas del desarrollo APP–TRIT–TPK. Aquí se componen lectores posteriores de esas salidas; no se eligen sus valores a partir de una masa observada. Para aligerar la notación se escriben \(\pi,\varphi,e,\alpha\).

## Dos orientaciones, una operación

Sean
\[
\mathscr R(x,y)=\frac{x}{y^2},\qquad
\mathsf J(x,y)=(y,x),\qquad x,y>0.
\]
El intercambio satisface \(\mathsf J^2=I\). La lectura antes y después de ese intercambio produce
\[
\rho_A=\mathscr R(\pi,\varphi)=\frac{\pi}{\varphi^2},
\qquad
\rho_E=(\mathscr R\circ\mathsf J)(\pi,\varphi)
=\frac{\varphi}{\pi^2}.
\]
El propietario conserva la procedencia de ambas orientaciones: el calendario de modos induce la incidencia areal–volumétrica \(F_{\rm av}\); su acción de segundo orden tiene el modo estable positivo \(\varphi^{-2}\); el marcado de cierre produce \(\rho_A\); el intercambio de las coordenadas produce el exponente electrónico \(\rho_E\). No se identifica la matriz de incidencia con el electrón entero.

La identidad que permite cruzar las dos exposiciones es
\[
\varphi^3\rho_A^2\rho_E=1,
\qquad
\rho_E=\frac1{\varphi^3\rho_A^2}.
\]
Su prueba es sustitución:
\[
\varphi^3\left(\frac{\pi}{\varphi^2}\right)^2
\frac{\varphi}{\pi^2}=1.
\]
Así, la función electrónica puede escribirse íntegramente conservando su lectura areal:
\[
\mathfrak e_e^\beta
=\frac{\sqrt3}{4}
\left[
 \exp\!\left(\frac1{\varphi^3\rho_A^2}\right)-22\alpha^3
\right](1+15\Delta_4)\,R_{\rm act}^{\kappa_e},
\qquad
\kappa_e=80-54\alpha+6\Delta_4.
\]
Aquí \(\Delta_4\) es el corrector global de la ecuación electrónica, \(R_{\rm act}=\hbar_{\rm pre}/\hbar_{\rm ret}>0\) la razón de sus secciones de acción y \(\kappa_e\) la evaluación de los lectores centrales. Las definiciones completas se conservan en [la sustitución electrónica][electron]. La energía y masa posteriores son \(E_e^\beta=u_E\mathfrak e_e^\beta\) y \(m_e^\beta=E_e^\beta/c^2\), en una misma carta energética \(u_E\). El factor \(c^2\) de esta última conversión no es el denominador \(\pi^2\) del exponente adimensional.

## Qué conservan conjuntamente las dos lecturas

Al conservar ambas orientaciones se obtiene el mapa positivo
\[
\mathcal Q(x,y)=\left(\frac{x}{y^2},\frac{y}{x^2}\right).
\]
No es una involución: el intercambio \(\mathsf J\), la inversa de \(\mathcal Q\) y el recíproco de un escalar son operaciones diferentes. En particular,
\[
\rho_A\rho_E=\frac1{\pi\varphi},
\qquad
\frac{\rho_A}{\rho_E}=\left(\frac{\pi}{\varphi}\right)^3.
\]
La pareja conserva el producto y la razón orientada del par de origen. De manera equivalente,
\[
\rho_A\rho_E^2=\pi^{-3},\qquad
\rho_A^2\rho_E=\varphi^{-3},
\]
de donde
\[
\pi=(\rho_A\rho_E^2)^{-1/3},
\qquad
\varphi=(\rho_A^2\rho_E)^{-1/3}.
\]
Las raíces positivas son únicas. Esto demuestra recuperabilidad del par de coordenadas en este dominio. No reconstruye por sí solo la historia enriquecida ni convierte la masa física en una entrada del generador.

La ampliación de \(\mathcal Q\) al dominio complejo, desarrollada en [la nota de Ley 9][dinamica], tiene fibras de fase y requiere conservar la rama correspondiente. Esa ampliación no introduce ambigüedad en las raíces positivas anteriores ni autoriza a confundir todas las realizaciones modulares por compartir un cociente.

## Control inverso de la publicación electrónica

El cruce también permite comprobar qué información conserva la publicación final del electrón. Con \(\alpha,\Delta_4,R_{\rm act},\kappa_e,u_E\) y la carta fijados,
\[
E_e^\beta=
\frac{\sqrt3}{4}u_E R_{\rm act}^{\kappa_e}
(1+15\Delta_4)\bigl(e^{\rho_E}-22\alpha^3\bigr)
\]
se invierte exactamente como
\[
\rho_E=
\log\!\left[
22\alpha^3+
\frac{4E_e^\beta}
{\sqrt3\,u_E R_{\rm act}^{\kappa_e}(1+15\Delta_4)}
\right].
\]
El cociente energético dentro del logaritmo es adimensional. Se exige \(u_E>0\), \(R_{\rm act}>0\), \(1+15\Delta_4\ne0\) y argumento positivo; sobre la imagen de \(\rho_E>0\), dicho argumento es mayor que uno. La prueba consiste en despejar la exponencial. La derivada respecto de \(\rho_E\), manteniendo esos antecedentes, es un factor no nulo por \(e^{\rho_E}\), por lo que la inversión es única sobre su imagen.

Esta operación inversa comprueba la lectura, no vuelve a generar sus antecedentes. Una energía aislada no determina simultáneamente los correctores, la razón areal, las constantes y la historia electrónica. La dirección generativa permanece desde el estado HMT hacia sus publicaciones; la dirección inversa es un control posterior de la información que la fórmula conserva.

## Procedencia del cruce

El intercambio y la identidad \(\varphi^3\rho_A^2\rho_E=1\) son resultados recuperados del [capítulo electrónico, sección segunda][bisagra] y del [sistema operatorio de Euler, principio de ambivalencia][ambivalencia]. La inversión positiva de \(\mathcal Q\) está reunida en el desarrollo ya cerrado por Ley 9. El despeje electrónico y su sustitución areal se presentan aquí como composiciones algebraicas explícitas de esas fórmulas, no como otra derivación independiente del electrón ni como reivindicación de prioridad.

[bisagra]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/06f_biografia_electron_rev6.tex:130>
[ambivalencia]: </Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c57_sistema_operatorio_euler_hmt.tex:134>
[electron]: </Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/SUSTITUCION_ELECTRON_ACCION_MASAS.md:5>
[dinamica]: </Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/DINAMICA_ORIENTADA_Q_FRICKE_Y_RECUPERACION.md:68>
