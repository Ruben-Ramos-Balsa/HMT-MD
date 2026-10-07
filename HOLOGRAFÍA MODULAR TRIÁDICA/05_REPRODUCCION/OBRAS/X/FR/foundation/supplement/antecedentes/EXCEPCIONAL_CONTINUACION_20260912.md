# Levantamiento covariante del registro y recuperación incidencial de memoria

Continuación focal, 12 de septiembre de 2026. Se conservan sin cambios los cuatro informes sellados, sus recibos y los PDF. Este archivo desarrolla una composición adicional; no declara novedad histórica global ni modifica la generación APP–TRIT–TPK.

## 1. Base utilizada y paso adicional

El punto de partida es el estado enriquecido producido por las dos hojas APP, con división en residuo y cociente; orientación y régimen TRIT; y selección, transporte, acarreo, frontera y actualización de memoria TPK. La prolongación `w6→w12→w18→w24→w30→R36→G9` y las cinco construcciones consustanciales del continuo permanecen antecedentes conjuntos. El registro K es una publicación de esa historia, no una entrada para escogerla. Los espacios lineales siguientes realizan esas publicaciones después de su generación.

Se han releído íntegramente [EXCEPCIONAL.md](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/EXCEPCIONAL.md>) y [CONSERVACION_ESTRUCTURAL.md](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/CONSERVACION_ESTRUCTURAL.md>). El segundo ya incorpora la isometría completa F, incluyendo la media de K. No se presenta aquí esa incorporación previa como un descubrimiento adicional.

El paso de esta continuación es demostrar que F transporta **dinámica, observables, refinamiento y registro de complementos con inversa explícita**; y especializarlo a marcos locales variables sobre el refinamiento cilíndrico documentado. La recuperación se enuncia sobre el espacio realmente representado, sin identificar un registro dodecafásico con toda la genealogía.

### Propietarios focales

- **P1 — Registro:** [IV, registro_k.tex](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/IV_MOONSHINE_DUALIDAD_TEORIA_M/sections/registro_k.tex:95>), líneas 95–104 y 177–239: historia, lectura firmada y dominio; 301–357: Hadamard e inversión integral.
- **P2 — Incidencia:** [IV, excepcional.tex](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/IV_MOONSHINE_DUALIDAD_TEORIA_M/sections/excepcional.tex:43>), líneas 43–130: marcos causales y truncamientos; 341–374: Gram y entrelazador de incidencia; 415–490: estrellas y dominio de Mathieu.
- **P3 — Registro y prolongación:** [IV, registro_imagen_integral.tex](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/IV_MOONSHINE_DUALIDAD_TEORIA_M/sections/registro_imagen_integral.tex:165>), líneas 165–199: acción de ventanas y prefijos posteriores al corte; 203–263: contribuciones de eventos y composición aditiva o afín.
- **P4 — Refinamiento torcido efectivo:** [Integral2249, 78_doble_circulo_campo_espectral_completo.tex](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex:943>), líneas 943–968: cociclo entero de memoria; 1023–1088: pesos proyectivos, isometría, composición y cambio de calibre; 1421–1458: carta nonádica para un unitario y defecto. La especialización de 1023–1088 usa la fibra de Weil; su prueba operatoria por pesos y unitariedad es la que se compone aquí con otra publicación tipada, sin identificar ambas fibras.
- **P5 — Memoria y etiquetas:** [Artículo espectral REV04, transporte_y_momentos.tex](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/PRIMOS_Y_ZETA_COMPLETO/ampliacion/transporte_y_momentos.tex:290>), líneas 55–137: balance y registro; 290–306: órbita bilateral reversible y conservación de etiquetas transversales. El paso al espacio bilateral se distingue de una transición sólo demostrada isométrica.
- **P6 — Covariancia de la energía:** [VII, 30b_variacion_energia_memoria.tex](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/VII_GRAVITACION/manuscrito/30b_variacion_energia_memoria.tex:165>), líneas 165–194 y 254–297: transporte de marcos, energía y diferencial. Esta continuación no necesita introducir una realización Lorentz ni otra especialización de Euler para demostrar su resultado lineal.

## 2. La isometría completa y su dominio

Sea H = R¹², con producto euclídeo; \(P_0=I-\mathbf1\mathbf1^*/12\), \(\mu(k)=\mathbf1^*k/12\), y \(\mathcal I:H\to\mathbb R^{132}\) la matriz de incidencia de P2. Escribimos \(E_{\rm inc}=\mathcal I(\mathbf1^\perp)\) y

\[
Y=\mathbb R\oplus E_{\rm inc},\qquad
\langle(\mu,y),(\nu,z)\rangle_Y=12\mu\nu+\langle y,z\rangle.
\]

La aplicación del informe sellado es

\[
F:H\longrightarrow Y,\qquad Fk=(\mu(k),\mathcal I P_0k/6),
\]
\[
F^{-1}(\mu,y)=\mu\mathbf1+P_0\mathcal I^*y/6.
\]

El Gram \(\mathcal I^*\mathcal I=36I+30\mathbf1\mathbf1^*\) prueba ambas composiciones inversas y \(F^*F=I_H\), \(FF^*=I_Y\), con el producto ponderado indicado. Por ello F es ortogonal entre H e Y. Puede complejificarse sin cambiar las pruebas.

El codominio es Y, de dimensión doce, no todo R⊕R¹³². Extender un operador desde Y a su complemento en ese ambiente requiere una elección adicional; no forma parte de la dinámica transportada de manera única. En coordenadas firmadas normalizadas se usa \(FJ_H\), con \(J_H=H_{12}/2\). La inversión integral sigue siendo \(H_{12}/4\) en su subred, no un normalizador métrico alternativo.

## 3. Teorema de levantamiento covariante en la imagen

**Teorema A.** Para un operador acotado D sobre H, existe un único operador sobre Y que satisface \(D_YF=FD\). Es

\[
D_Y=FDF^{-1}.
\]

La correspondencia conserva sumas, productos, adjuntos, norma, positividad e identidad. En particular, lleva unitarios a unitarios y observables autoadjuntos a observables autoadjuntos. Para un unitario C y un observable A,

\[
C^*AC=A\quad\Longleftrightarrow\quad C_Y^*A_YC_Y=A_Y.
\]

Si R es un cambio unitario de carta, \(R_Y=FRF^{-1}\), entonces

\[
F(RDR^{-1})F^{-1}=R_YD_YR_Y^{-1}.
\]

**Demostración.** La primera fórmula se obtiene multiplicando el entrelazamiento por F⁻¹. La unicidad se sigue de la sobreyectividad hacia Y. Las identidades de productos y adjuntos resultan de F⁻¹=F*, y la igualdad de normas de la isometría sobreyectiva. La última igualdad es una composición asociativa de esas aplicaciones. No interviene ninguna hipótesis de conmutación entre R y D. ∎

Para \(g\in\operatorname{Aut}(\mathcal H)\), P2 proporciona

\[
F\rho_{12}(g)=\bigl(1\oplus\rho_{\rm hex}(g)\bigr)F.
\]

Así, el cambio de carta posee una acción combinatoria concreta sobre las hexadas. En cambio, para un unitario general D, D_Y es un operador de la representación incidencial, no necesariamente una permutación del diseño. Preservar el producto interno de esa representación no convierte a todos sus unitarios en automorfismos combinatorios ni en elementos del Monstruo.

### Control concreto contra la conmutación ficticia

Sea C el avance \(Ce_p=e_{p+1}\) cíclico en las doce posiciones, es decir, el sentido inverso de la convención S de P3. Es una operación de la carta de ventanas, no la holonomía temporal completa. Sea R la estrella ya construida

\[
R=(1\ 3)(2\ 11)(5\ 7)(8\ 12).
\]

Entonces \(RCe_1=e_{11}\), mientras \(CRe_1=e_4\). No conmutan. Sin embargo, para \(C'=RCR^{-1}\), se cumplen exactamente \(T(C')R=RT(C)\) y \(\eta(C')R=R^{\oplus9}\eta(C)\), y lo mismo en Y mediante F. La covariancia de carta sí funciona en un ejemplo donde la conmutación en carta fija falla.

## 4. Recuperación explícita desde el registro incidencial de complementos

Sean C unitario, \(T=(8I+C)/9\), \(\eta=(I-JJ^*)S_CJ:H\to H^9\), y P la proyección sobre Fix(C), como en el informe sellado. Escribimos \(F_9=F^{\oplus9}\). La versión incidencial del registro finito es

\[
\mathcal W_Nk=\left(FT^Nk,F_9\eta k,F_9\eta Tk,\ldots,F_9\eta T^{N-1}k\right).
\]

**Teorema B.** Esta aplicación es isométrica y posee la inversa izquierda explícita

\[
\mathcal W_N^*(a,b_0,\ldots,b_{N-1})
=T^{*N}F^{-1}a+
\sum_{j=0}^{N-1}T^{*j}\eta^*F_9^{-1}b_j.
\]

En particular, aplicar esta fórmula a \(\mathcal W_Nk\) recupera exactamente k. El registro infinito

\[
\mathcal W_\infty k=\left(FPk,(F_9\eta T^jk)_{j\ge0}\right)
\]

también es isométrico, y su inversa izquierda es

\[
k=PF^{-1}a+\sum_{j\ge0}T^{*j}\eta^*F_9^{-1}b_j
\quad\text{para }(a,(b_j))=\mathcal W_\infty k.
\]

La serie converge en norma. Para datos arbitrarios cuadrado-sumables la misma fórmula define el adjunto acotado, aunque no todo dato del codominio pertenece a la imagen de \(\mathcal W_\infty\).

**Demostración.** Aplicar F y F9 a cada componente de V_N o V_infinito conserva el producto interno. Tomar el adjunto de esa composición da las fórmulas. La identidad telescópica del informe sellado prueba \(\mathcal W_N^*\mathcal W_N=I\), y su límite fuerte prueba \(\mathcal W_\infty^*\mathcal W_\infty=I\). La convergencia de la serie procede de aplicar un operador acotado a las truncaciones de una sucesión en suma directa hilbertiana. ∎

Esta reconstrucción no conserva k como una primera coordenada intacta: el primer componente es el terminal comprimido o su sector fijo; el resto procede de los complementos sucesivos. Cuando P=0, **los complementos incidenciales por sí solos recuperan k**. La contribución recuperada a partir de los primeros N bloques es

\[
k_N=\sum_{j<N}T^{*j}\eta^*F_9^{-1}b_j
=\bigl(I-T^{*N}T^N\bigr)k.
\]

El residuo es \(T^{*N}T^Nk\), que tiende a cero si P=0. Con un sector fijo no nulo debe conservarse FPk; la memoria de complementos sola no recupera ese sector. Las tasas de reconstrucción y la dinámica sobre el índice de bloques se desarrollan por separado en la investigación principal para evitar duplicación.

Si A es autoadjunto y \([A,C]=0\), la forma del observable se conserva también:

\[
\langle k,Ak\rangle
=\langle FPk,A_YFPk\rangle_Y
+\sum_{j\ge0}\langle F_9\eta T^jk,(I_9\otimes A_Y)F_9\eta T^jk\rangle.
\]

La serie escalar converge absolutamente porque A es acotado y la suma de las normas cuadradas de los componentes es finita. La hipótesis expresa conservación de A por C; no exige conmutación de C con los cambios de carta excepcionales.

## 5. Levantamiento natural del refinamiento con marcos locales

P4 aporta conjuntos de estados cilíndricos enriquecidos Z_n, truncamientos y medidas proyectivas de soporte completo. Para un descendiente z′ de z,

\[
w_n(z'|z)=\sqrt{\mu_{n+1}(z')/\mu_n(z)},\qquad
\sum_{\tau z'=z}w_n(z'|z)^2=1.
\]

La etiqueta z′ conserva ledger, orientación, acarreo, frontera, memoria, ruta y terminal. El refinamiento de un estado no identifica descendientes distintos.

Sean q(z) el registro entero de memoria, C un unitario sobre H, y R_z cambios ortogonales de marco de la fibra. Para marcos incidenciales concretos puede usarse \(R_z=\rho_{12}(g_z)\), con \(g_z\in\operatorname{Aut}(\mathcal H)\), transportando sus marcas. Definimos

\[
G_z=R_zC^{q(z)},\qquad
U_{z',z}=G_{z'}G_z^*
=R_{z'}C^{q(z')-q(z)}R_z^*.
\]

Esta construcción prolonga la equivalencia de calibre explícita de P4. No requiere \([R_z,C]=0\), y deja visible el orden de las operaciones.

Sobre \(\mathscr H_n=\ell^2(Z_n)\otimes H\),

\[
\mathscr U_n(e_z\otimes v)
=\sum_{\tau z'=z}w_n(z'|z)e_{z'}\otimes U_{z',z}v.
\]

Definimos \(\mathscr F_n=I_{\ell^2(Z_n)}\otimes F\), con codominio \(\mathscr Y_n=\ell^2(Z_n)\otimes Y\).

**Teorema C.** El refinamiento es isométrico y satisface

\[
\mathscr U^Y_n\mathscr F_n=\mathscr F_{n+1}\mathscr U_n,
\quad
\mathscr U^Y_n=\mathscr F_{n+1}\mathscr U_n\mathscr F_n^{-1}.
\]

La fórmula de cada término es la anterior con \(U^Y_{z',z}=FU_{z',z}F^{-1}\). Los sistemas de varias profundidades conservan composición y admiten una isometría sobreyectiva entre sus límites inductivos. Se preservan exactamente todos los coeficientes de fibra con sus etiquetas z.

**Demostración.** Los descendientes de padres distintos son ortogonales; cada U_z′,z es unitario; y los pesos tienen suma cuadrática uno. Esto prueba la isometría. En una trayectoria, los factores intermedios G_z*G_z se cancelan y los cocientes de medidas telescopan. La composición no depende de la partición de la trayectoria. El cuadrado con F se verifica sobre e_z⊗v, término a término. Las aplicaciones y sus inversas son isometrías compatibles, por lo que se extienden inversamente a las completaciones inductivas. ∎

### Observables y dinámica compatibles

Si A0 es un observable acotado de la fibra, sea

\[
(\mathscr A_n\psi)_z=G_zA_0G_z^*\psi_z.
\]

Entonces \(\mathscr A_{n+1}\mathscr U_n=\mathscr U_n\mathscr A_n\), de donde \(\mathscr U_n^*\mathscr A_{n+1}\mathscr U_n=\mathscr A_n\). Se obtiene sustituyendo U_z′,z=G_z′G_z*. Esta es conservación de un **campo de observables transportado por refinamiento**; no afirma que A0 conmute con C en una carta fija.

La dinámica unitaria por nivel

\[
(\mathscr C_n\psi)_z=G_zCG_z^*\psi_z
\]

satisface \(\mathscr C_{n+1}\mathscr U_n=\mathscr U_n\mathscr C_n\). También entrelazan sus adjuntos: como ambas C son unitarias, la identidad se multiplica por sus inversas. Por tanto entrelazan T, sus complementos nonádicos y sus proyecciones fijas. El registro finito y el infinito del teorema B son naturales con respecto a este refinamiento. Al aplicar \(\mathscr F_n\), esos mismos cuadrados valen en las fibras incidenciales. Para que \(\mathscr A_n\) sea conservado además por esa dinámica en un nivel fijo, la condición precisa es \([A_0,C]=0\); la covariancia entre marcos sigue sin requerir \([R_z,C]=0\).

### Especialización de memoria bilateral con marcos variables

En la órbita reversible de P5 puede representarse una publicación de coordenadas por \(\psi=(\psi_m)_{m\in\mathbb Z}\in\ell^2(\mathbb Z;H)\). Su avance es \((C_0\psi)_m=\psi_{m-1}\). F actúa punto a punto. Para marcos \(R_m=\rho_{12}(g_m)\), el cambio unitario \((\mathscr R\psi)_m=R_m\psi_m\) produce

\[
(C'\psi)_m=R_mR_{m-1}^*\psi_{m-1}.
\]

El operador incidencial tiene la misma fórmula con \(1\oplus\rho_{\rm hex}(g_mg_{m-1}^{-1})\). No se imponen marcos constantes ni conmutación con el desplazamiento. Como C′ es conjugado a C0, no tiene vectores fijos no nulos en este espacio cuadrado-sumable. El teorema B recupera la publicación lineal completa desde sus complementos incidenciales. Se trata de la órbita y de las coordenadas representadas: no de una identificación de todas las historias TPK con Z.

## 6. Extensión directa a las doce fibras A2

La construcción excepcional del integral conserva doce fibras A2 y el operador g_c de orden tres localizado en EXCEPCIONAL.md. Sea \(V_{A_2}=A_2\otimes_{\mathbb Z}\mathbb R\) su realización euclídea bidimensional. La misma isometría posicional puede tensorizarse sobre \(\mathbb R\) con ese espacio:

\[
F_{A_2}=F\otimes I_{V_{A_2}}:
\mathbb R^{12}\otimes_{\mathbb R}V_{A_2}
\longrightarrow Y\otimes_{\mathbb R}V_{A_2}.
\]

Su primera componente es la media vectorial y su segunda son las sumas incidenciales centradas, ahora con valores en A2. El Gram de incidencia, tensorizado con la identidad, prueba de nuevo la isometría completa y la inversa. Por ello \(g_c^Y=F_{A_2}g_cF_{A_2}^{-1}\) es ortogonal, de orden tres y fijo-libre. La composición nonádica ya incorporada en el informe sellado puede publicarse y recuperarse en esta pantalla A2-valuada mediante los teoremas A y B. No se confunden los doce escalares de K con las veinticuatro coordenadas de las fibras A2, ni se convierte la acción en una permutación de hexadas cuando la elevación también actúa dentro de las fibras.

## 7. Alcance exacto respecto de las historias

Sea k:X→H el lector del registro sobre un dominio de historias, y sea \(\ell=F\circ k\). Entonces

\[
\ell(x)=\ell(y)\quad\Longleftrightarrow\quad k(x)=k(y).
\]

La pantalla completa añade **cero pérdida** respecto de K, pero tampoco cambia las fibras de ese lector. Un mapa d:X→X desciende a una dinámica sobre los valores de K si y sólo si

\[
k(x)=k(y)\Longrightarrow k(d x)=k(d y).
\]

La misma condición es necesaria y suficiente para descender sobre la imagen incidencial. La prueba consiste en definir D(k(x))=k(dx); la condición equivale a que la definición sea independiente del representante. Si ese D es lineal y unitario en la realización declarada, se aplica el teorema A. Si es no lineal, F sigue conjugándolo como aplicación, pero no lo convierte en un unitario.

Este criterio no declara que falte una dinámica del corpus: distingue el descenso a K de la dinámica enriquecida ya construida. P1 declara que el lector usa subruta, orientación, acarreo e incidencias; P2 distingue recuperación de palabra visible, soporte y memoria profunda. Cuando se trabaja sobre \(\ell^2(Z_n)\otimes H\), el teorema C conserva materialmente las etiquetas enriquecidas y cambia sólo la representación de la fibra. Esa conservación es una equivalencia posterior, no una nueva prueba de generación del continuo por empaquetar etiquetas.

Para un corte ya construido, P3 fija \(K_N=K_{108}\circ\tau_{N,108}\): F conserva exactamente esa naturalidad. Una sucesión de nuevos eventos puede actualizar K; la composición aditiva o afín de P3 conserva la independencia de la partición, no la constancia del valor al añadir eventos.

## 8. Procedencia, falsadores y resultado

**Recuperado:** Gram e isometría de incidencia, inversión integral de K, cociclo de memoria, refinamiento torcido y sus pesos, covariancia de marco, registro isométrico y separación entre memoria y fase.

**Formalización añadida en esta continuación:** teoremas A–C como composición conjunta; inversa explícita de la publicación incidencial de complementos; marcos locales variables; extensión F⊗Id_A2; y criterio exacto de descenso sobre las fibras del lector. Su prioridad global dentro del corpus no ha sido auditada y no se afirma.

**Falsadores concretos:** eliminar la media impide recuperar K completo; identificar Y con todo el ambiente de 133 coordenadas hace falsa la unicidad de la extensión; pesos que no sumen cuadráticamente uno rompen la isometría; olvidar el orden de marcos produce transportes distintos; confundir un observable transportado con uno fijo elimina una hipótesis real de conservación; retirar el sector fijo rompe la reconstrucción desde complementos cuando existe; y promover recuperación de K a recuperación de toda historia sin analizar las fibras del lector cambia el dominio del teorema.

**Resultado:** la incidencia puede transportar una dinámica y recuperar su registro de memoria de manera exacta, covariante y compatible con refinamientos reales del corpus. La conclusión es más fuerte que conservar una norma aislada: incluye inversa, observables, operadores, etiquetas, composición y límite. Ninguna de estas pruebas exige atribuir al Monstruo una conmutación con la holonomía temporal ni recibir constantes convencionales como entradas del generador.
