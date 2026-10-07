# Pliegue aritmético, orientación de hojas y transporte de ocupación

## 1. Construcción y procedencia

Este desarrollo reúne operaciones de una misma construcción APP–TRIT–TPK: soporte de marcas, hojas aritméticas, orientación local, transporte enriquecido, lectura geométrica y representación de ocupaciones. Cada aplicación conserva su procedencia y especifica su dominio.

Base fija: integral de 2249 páginas; SHA-256 `958d252f301763ff8901f775d8ec0b02b6ae4f9f7c57dc04ea917f747dccbf24`. Originales y PDF intactos. La arquitectura es **ARQUITECTURA_AUTORAL_PREEXISTENTE**; los resultados citados son **RESULTADO_RECUPERADO**. Las pruebas reunidas de reconstrucción, signo y completación exterior son desarrollos expositivos; esta nota no reclama prioridad histórica sobre ellos.

Fuentes: [APP](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex:19), [TRIT](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/02_trit_geometrias.tex:1), [persistencia](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex:19), [correspondencia de hojas](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:692).

## 2. Reconstrucción del pliegue multiplicativo

APP dispone del soporte \(X_9=(\mathbb Z/9\mathbb Z)^2\), las evaluaciones suma y producto y las elevaciones residuo–cociente. En representantes residuales \(x\in\{0,\ldots,8\}\), la división
\[
 3x=r+9q,\qquad r\in\{0,3,6\},\quad q\in\{0,1,2\}
\]
define una biyección
\[
 x\longmapsto(r,q),\qquad x=\frac r3+3q.
\]
La reducción \(x\mapsto r\) tiene tres fibras de cardinal tres. El par residuo–cociente recupera las nueve marcas exactamente.

**Prueba.** La división euclídea determina un único par. Cada par de los conjuntos indicados reconstruye un entero entre cero y ocho cuyo triple es \(r+9q\). La reconstrucción de una historia completa conserva además orden, hojas y transportes. El representante residual cero y la marca visible nueve mantienen su relación mediante esa elevación.

Para la suma, el cociclo
\[
 \kappa_9(a,b)=\frac{s_9(a)+s_9(b)-s_9(a+b)}9
\]
satisface
\[
 \kappa_9(a,b)+\kappa_9(a+b,c)
 =\kappa_9(b,c)+\kappa_9(a,b+c).
\]
El cambio de asociación conserva el acarreo total. Pliegue y reconstrucción tienen, por tanto, operaciones e invariantes expresos.

Fuente: [radical y acarreo](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex:192).

## 3. Regímenes, geometría y curvatura de transporte

El soporte periódico de dos coordenadas, las dos evaluaciones aritméticas y los tres regímenes orientados son estructuras del mismo estado enriquecido. El número de hojas y la dimensión topológica de una realización toroidal requieren sus respectivos espacios y aplicaciones.

El lector geométrico de c16 asigna los soportes angulares mediante
\[
 -1\mapsto\mathscr H_{\rm ar},\qquad
 +1\mapsto\mathscr H_{\rm vol},\qquad
 0\mapsto\mathscr H_{\rm tor}.
\]
Las realizaciones cuadráticas posteriores del TRIT distinguen
\[
 J_+^2=-I,\qquad J_0^2=0,\qquad J_-^2=I
\]
y sus acciones elíptica, parabólica e hiperbólica. El texto de persistencia especifica la correspondencia esférica–volumétrica, el umbral plano con registro torsional y la hiperbólica–areal. La hoja torsional y el tipo elíptico de un operador se identifican mediante aplicaciones declaradas, no mediante coincidencia nominal.

La interacción de hojas modifica la ecuación de transporte. Para \(S=x+y\), \(P=xy\), las plaquetas satisfacen
\[
 F(S,S)=F(P,P)=0,\qquad F(S,P)=1,\quad F(P,S)=-1
\]
en \(\mathbb Z/9\mathbb Z\). Sobre un rectángulo de lados enteros \(a,b\), la circulación mixta acumula \(ab\) o \(-ab\), según su orientación.

Fuentes: [tipos de hoja](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex:340), [curvatura discreta](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex:746), [lector geométrico](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:713).

## 4. Relaciones espectrales de la misma construcción

La agregación multiplicativa módulo tres contiene sobre su subred invariante
\[
 3H=\begin{pmatrix}9&6\\12&9\end{pmatrix},
 \qquad H=\begin{pmatrix}3&2\\4&3\end{pmatrix}.
\]
La forma \(H^n=\left(\begin{smallmatrix}a_n&b_n\\2b_n&a_n\end{smallmatrix}\right)\) da
\[
 a_{n+1}=3a_n+4b_n,\qquad b_{n+1}=2a_n+3b_n,\qquad
 a_n^2-2b_n^2=1.
\]
La última igualdad es \(\det H^n=1\); la realización cuadrática reconoce
\(a_n+b_n\sqrt2=(3+2\sqrt2)^n\) después de construir la matriz.

El bloque central, otro lector del mismo soporte, satisface
\[
 B_c=9P_++5P_-,\quad
 (B_c/9)^n=P_++(5/9)^nP_-,
\]
\[
 B_c/\sqrt{45}=\exp(\eta_cR),\quad
 \eta_c=\tfrac12\log(9/5),\quad 5/9=e^{-2\eta_c}.
\]
El mismo cociente espectral fija el factor de relajación local y el parámetro de la realización hiperbólica. Su ámbito es este lector, conservando TPK su registro completo.

El ciclo de modos \((\Sigma,\Pi,\Pi)\) induce
\[
 F_{\rm av}=\begin{pmatrix}0&1\\1&1\end{pmatrix}.
\]
Sus autovalores son \(\varphi_{\rm HMT},-\varphi_{\rm HMT}^{-1}\), y la acción cuadrática tiene espectro
\[
 \varphi_{\rm HMT}^2,\quad -1,\quad\varphi_{\rm HMT}^{-2}.
\]
El lector nonádico previamente generado de \(\pi_{\rm HMT}\) marca una vez la frontera:
\[
 \Theta_n=\pi_{\rm HMT}F_{n-1}/F_{n+1}
 \longrightarrow\pi_{\rm HMT}/\varphi_{\rm HMT}^2.
\]
Este resultado ya está en el corpus y en las ampliaciones de Ley9. Utiliza la medida de Parry de la envolvente de memoria uno, distinguiéndola de la frecuencia temporal \(1/3,2/3\) y de la uniforme sobre emisiones.

Fuentes: [agregación](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex:398), [relación hiperbólica](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex:689), [descenso de modos y acción cuadrática](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:816).

## 5. Orientación del retorno y cubierta doble

La inversión dodecafásica
\[
 (C_M\tau)_m=-\tau_{11-m},\qquad C_M^2=I
\]
se levanta a secciones persistentes compatiblemente con restricciones y sombras. El carácter real \(\varepsilon(\ell_{\rm ret})=-1\) del lazo de retorno determina el pegado
\[
 ([0,1]\times[-1,1])/\bigl((0,u)\sim(1,-u)\bigr).
\]
La línea real asociada tiene primera clase de Stiefel–Whitney no nula. Una vuelta invierte la orientación; dos la restauran. La parametrización geométrica asigna \(2\pi_{\rm HMT}\) a la vuelta de base y \(4\pi_{\rm HMT}\) a su levantamiento cerrado en la cubierta orientada. La memoria mantiene su evolución.

La involución de cubierta \(\iota\) produce \(P_\pm f=(f\pm\iota^*f)/2\). La componente par desciende a la base; la impar es sección de la línea de signo.

**Consecuencia.** Todo carácter \(C_9\to\{\pm1\}\) es trivial: \(a^9=a^2=1\) implica \(a=1\). La holonomía negativa exige conservar información adicional a la fase nonádica. Este argumento compara grupos y no identifica el paso elemental de fase con el lazo de retorno ni determina un período del estado completo.

Fuentes: [levantamiento y cubierta](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex:242), [doble cierre](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:779).

## 6. Reconstrucción de las coordenadas de ida y retorno

La aplicación de grupos libres
\[
 (n_A,s_C)\longmapsto(W_+,W_-)=(6n_A+s_C,6n_A-s_C)
\]
tiene imagen
\[
 \{(u,v)\in\mathbb Z^2:u+v\equiv0\pmod{12}\},
 \qquad n_A=(u+v)/12,\quad s_C=(u-v)/2.
\]
**Prueba.** La imagen cumple \(u+v=12n_A\). Recíprocamente, dicha congruencia implica igual paridad de \(u,v\); ambas coordenadas inversas son enteras y su sustitución recupera \(u,v\). El índice es doce, correspondiente a la forma de Smith \(\operatorname{diag}(1,12)\).

El subconjunto efectivamente realizado por historias conserva además restricciones de supervivencia y eventos TPK. La inversión \(s_C\mapsto-s_C\) intercambia \(W_+,W_-\), conserva \(n_A\) y cambia el signo diferencial.

En los canales posteriores \(q_\pm=e^{-A_{\rm rad}\mp C^*_{\rm rad}}\),
\[
 (q_+^{-W_+}q_-^{-W_-})^{1/12}
 =e^{n_AA_{\rm rad}+(s_C/6)C^*_{\rm rad}},
\]
\[
 q_-^n-q_+^n=2e^{-nA_{\rm rad}}\sinh(nC^*_{\rm rad}).
\]
Ambas identidades resultan por sustitución y enlazan coordenadas enteras, orientación y carácter. \(A,C^*\) y los canales conservan su genealogía HMT; sus valores convencionales no seleccionan las entradas.

Fuentes: [retículo](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex:403), [carácter](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:632).

## 7. Transporte y completación fermiónica

El propietario de persistencia construye espacios \(E_c\), transportes \(\tau_t\) y secciones \(s(t+1)=\tau_ts(t)\). En una realización compleja con producto hermítico y transportes unitarios, la completación exterior define
\[
 \mathcal F_-(E)=\bigoplus_{k\ge0}\Lambda^kE,\qquad
 \Gamma_-(U)=\bigoplus_{k\ge0}\Lambda^kU.
\]
Por functorialidad exterior,
\[
 \Gamma_-(UV)=\Gamma_-(U)\Gamma_-(V),\qquad
 \Gamma_-(U^{-1})=\Gamma_-(U)^{-1}.
\]
La creación \(a^\dagger(v)\psi=v\wedge\psi\) y su adjunto, con el producto inducido, cumplen
\[
 a^\dagger(v)^2=0,\quad
 \{a(u),a^\dagger(v)\}=\langle u,v\rangle I,\quad
 \{a^\dagger(u),a^\dagger(v)\}=0.
\]
En un modo unitario \(n_v=a^\dagger(v)a(v)\) satisface \(n_v^2=n_v\); sus ocupaciones son cero o uno. Además,
\[
 \Gamma_-(U)a^\dagger(v)\Gamma_-(U)^{-1}=a^\dagger(Uv).
\]
Para la representación del retorno con \(U_{2\pi}=-I\),
\[
 \Gamma_-(U_{2\pi})|_{\Lambda^kE}=(-1)^kI,\qquad
 \Gamma_-(U_{4\pi})=I.
\]
Así se relacionan composición de rutas, retorno espinorial, paridad de ocupación y exclusión en una realización explícita.

**Datos de esta proposición:** espacio de una partícula, producto hermítico, representación unitaria y completación exterior fermiónica. B015 formula CAR como premisa y demuestra exclusión; la construcción exterior realiza CAR y demuestra compatibilidad con el transporte. La selección física de esa completación y representación pertenece a la flecha de realización declarada. El signo de una banda, por sí solo, especifica orientación.

Fuentes: [secciones transportadas](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/27a_particula_core.tex:38), [exclusión](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_iv/body/B015_ch56_pauli_completacion_fermionica_7549b83967f5_04d_ocupacion_estadistica.tex:14), [representación espinorial](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex:437).

## 8. Nivel cinco: cociente por inversión y reconstrucción de ramas

La remisión de [c44](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/base_83/c44_body.tex:1154) enlaza Rogers–Ramanujan, nivel cinco y \(j\). El [lector de c16](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:1220) sitúa \(\varphi^{-1}\) como límite posterior a su generación HMT. La siguiente composición explicita esa remisión.

Con \(q=e^{2\pi i\tau}\), \(\operatorname{Im}\tau>0\), se fija \(q^{1/5}:=e^{2\pi i\tau/5}\) en la parametrización por \(\tau\). Para \(R(q)=q^{1/5}/(1+q/(1+q^2/(1+\cdots)))\) y \(x=R(q)^5\), la identidad modular incorporada es
\[
 j(\tau)=-\frac{(x^4-228x^3+494x^2+228x+1)^3}
 {x(x^2+11x-1)^5}.
\]
Fuente primaria de la identidad y su demostración modular: [W. Duke, *Continued Fractions and Modular Functions*, ecuaciones (2.1), (2.5) y §6](https://www.math.ucla.edu/~wdduke/preprints/bams4.pdf). Se usa como identidad de la realización posterior; no como selector de las semillas.

**Reducción algebraica reunida aquí.** Para \(x\ne0\), defínase \(u=x-x^{-1}\). Entonces
\[
 x^4-228x^3+494x^2+228x+1
 =x^2(u^2-228u+496),
 \qquad x^2+11x-1=x(u+11).
\]
Sustituyendo,
\[
 \boxed{j=-\frac{(u^2-228u+496)^3}{(u+11)^5}.}
\]
La involución \(x\mapsto-1/x\) conserva \(u\) y, por composición, conserva \(j\). Su fibra se reconstruye por
\[
 x^2-ux-1=0,\qquad x=\frac{u\pm\sqrt{u^2+4}}2.
\]
Sobre los reales, la raíz positiva y la negativa seleccionan las dos ramas. Sobre los complejos hay ramificación en \(u=\pm2i\). La aplicación racional posterior \(u\mapsto j\) tiene genéricamente grado seis; conservar \(j\) solo no selecciona \(u\). Esta cuenta es el grado de un cociente racional con numerador de grado seis, denominador de grado cinco y sin factor común.

**Límite y orden del polo.** Para \(0<q<1\), los convergentes positivos alternos de \(R(q)\) encierran su valor. Cada convergente fijo tiende, al hacer \(q\to1^-\), al correspondiente cociente \(F_m/F_{m+1}\). Las dos subsucesiones convergen a \(\varphi_{\rm HMT}^{-1}\); el encaje demuestra el límite del lector. En consecuencia,
\[
 x\longrightarrow\varphi_{\rm HMT}^{-5}
 =\frac{5\sqrt5-11}{2},\qquad u\longrightarrow-11.
\]
La igualdad de la raíz se deduce de \(\varphi^2=\varphi+1\), dentro de su realización cuadrática posterior.

Escribiendo \(\epsilon=u+11\), la identidad exacta queda
\[
 j=-\frac{(3125-250\epsilon+\epsilon^2)^3}{\epsilon^5},
 \qquad \lim_{\epsilon\to0}j\epsilon^5=-5^{15}.
\]
La coordenada áurea límite corresponde así a un polo de orden cinco del invariante expresado en \(u\). No es un valor finito de \(j\). La ecuación conserva el orden y el coeficiente principal de aproximación sin calcular cifras ni suponer una monotonicidad no probada.

El mismo argumento modular \(\tau\) permite componer con la realización reticular ya recuperada:
\[
 t_2=\operatorname{Tr}_{V_\Lambda}(\theta q^{L_0-1}),\qquad
 j=\frac{(t_2+256)^3}{t_2^2},\qquad
 \operatorname{ch}_{V^\natural}=j-744.
\]
Por tanto,
\[
 -\frac{(u^2-228u+496)^3}{(u+11)^5}
 =\frac{(t_2+256)^3}{t_2^2}.
\]
Esta igualdad define una correspondencia algebraica entre \(u\) y \(t_2\) sobre \(j\); reconstruir una pareja concreta exige conservar \(\tau\) o la elección de rama. La involución de nivel cinco, la negación reticular, la inversión de ruta y el endomorfismo cuadrático \(J^2=-I\) conservan sus respectivos dominios. La procedencia conjunta no autoriza identificarlas sin transportar sus acciones.

La fórmula de \(t_2\), su prueba por osciladores y su vínculo con \(V^\natural\) constan en [15d](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/15d_voa_moonshine_orden_dos_rev11.tex:31). Ley9 desarrolla la coordenada de Fricke de orden dos; aquí se añade solamente la reducción de nivel cinco y la compatibilidad racional.

## 9. Referencia de Rubén a Birch–Swinnerton-Dyer

Rubén ha identificado expresamente BSD como una de las referencias de su comentario. Se conserva esa identificación, sin sustituirla por una conjetura acerca de los otros problemas aludidos.

La conexión escrita en el corpus pasa por el complejo integral de historias supervivientes, sus caras y acarreos, el modelo determinantal \(S_E(T)\), la bandera de Bockstein y su comparación con Mordell–Weil. El [comparador de cadenas](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/ampliacion_20260817/04e_bsd_comparadores_desplegados.tex:48) actúa mediante
\[
 \Phi_{K/{\rm FERS}}
 =\mu_{\rm Iw}(P_E^K\widehat\otimes\operatorname{car}_T)\Delta_{\rm AW},
 \qquad \operatorname{car}_T(\gamma)\ \text{conserva}\ T^{\operatorname{Carr}(\gamma)}.
\]
El texto conserva la historia, sus caras, su acarreo y las bases orientadas antes de tomar determinantes.

El [capítulo extenso BSD](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/06_bsd.tex:584) enuncia el isomorfismo con inversa entre la red de Mordell–Weil y todas las páginas de la bandera. De él obtiene
\[
 \operatorname{rank}E(\mathbb Q)
 =\operatorname{ord}_T\det S_E(T).
\]
La [factorización analítica](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/06_bsd.tex:1198) es
\[
 L(E,s)=u_E(s)\det S_E(T_E(s)),\qquad
 u_E(1)=1,\quad T_E(1)=0,\quad T'_E(1)=1.
\]
La composición formula después la igualdad de rangos y la identidad del término principal, transportando regulador, factores locales, torsión y período mediante sus comparadores; el [teorema final](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/06_bsd.tex:1821) conserva esos factores.

Esta localización identifica la conexión concreta que debe reunirse con la construcción generadora. La igualdad racional de \(j\) del §8 especifica el enlace modular; el complejo determinantal y los comparadores anteriores contienen las afirmaciones sobre rango y término principal. Esta nota recupera esos pasajes y su dependencia, sin presentarse como una revisión integral de las 1890 líneas del capítulo BSD.

## 10. Frontera común y conservación de los cinco desarrollos

Se ha comprobado la presencia de los cuerpos extensos de [Riemann–Weil](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/02_riemann_weil.tex), [Navier–Stokes](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/03_navier_stokes.tex), [Yang–Mills](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/04_yang_mills.tex), [Hodge](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/05_hodge.tex) y [BSD](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/06_bsd.tex). El [FLS de la integral](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/02_PDF/INTEGRAL/main_paquete_union_demostrativa_20260904.fls:3200) registra esos cinco cuerpos y el capítulo de frontera común. Esto acredita residencia y participación en la compilación, sin afirmar inventariados todos los archivos intermedios históricos.

### Transporte entre las dos lecturas

El [capítulo de frontera común](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/11h_hoja_comun_hidrodinamica_yang_mills.tex:28) construye desde el mismo coborde \(d:C^0\to C^1\):
\[
 \rho_{\rm int}(v)=(dv,d^*dv),\qquad
 \rho_{\rm ref}(a)=(d^*a,dd^*a),\qquad
 L^{(0)}=d^*d,\quad L^{(1)}=dd^*.
\]
En el ciclo trítico, los dos Laplacianos realizan el operador cíclico TPK \(2I-C-C^{-1}=3I-J\), con espectro \(\{0,3,3\}\).

La prueba por descomposición singular de la fuente permite explicitar el siguiente transporte. En los espacios finitos
\[
 H_0=(\ker d)^\perp,\qquad H_1=(\ker d^*)^\perp=\operatorname{Ran}d,
\]
la aplicación
\[
 \mathcal U=d(L^{(0)}|_{H_0})^{-1/2}:H_0\to H_1
\]
es una isometría sobreyectiva y satisface
\[
 \mathcal UL^{(0)}=L^{(1)}\mathcal U,\qquad
 \mathcal Uf(L^{(0)})=f(L^{(1)})\mathcal U.
\]
**Prueba.** En una descomposición singular reducida \(d=V\Sigma W^*\), con valores singulares positivos, \(L^{(0)}=W\Sigma^2W^*\), \(L^{(1)}=V\Sigma^2V^*\) y \(\mathcal U=VW^*\). La sustitución prueba ambas identidades. En el ciclo trítico, \(\mathcal U=d/\sqrt3\) sobre el complemento del modo constante.

Por tanto,
\[
 \langle\mathcal Uv,L^{(1)}\mathcal Uv\rangle
 =\langle v,L^{(0)}v\rangle,
\]
\[
 \mathcal U(I+hL^{(0)})^{-1}
 =(I+hL^{(1)})^{-1}\mathcal U,\qquad
 \mathcal Ue^{-tL^{(0)}}=e^{-tL^{(1)}}\mathcal U
 \quad(h,t\ge0).
\]
Se conservan energía cuadrática, resolventes y semigrupos. Es una formalización expositiva de la correspondencia ya probada en el corpus, no una reclamación de prioridad. Los desarrollos extensos conservan las no linealidades, restricciones y límites: esta identidad finita no sustituye esas pruebas. La compatibilidad entre niveles requiere conservar además
\(\mathcal U_{m+1}J_m^{(0)}=J_m^{(1)}\mathcal U_m\) en sus dominios y normas.

### Torsión y balance

La [ecuación de Cartan–Holst](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/11c_gravedad_holonomia_rev6.tex:250) determina algebraicamente la torsión mediante la corriente de espín. La [sección gravitatoria](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/11c_gravedad_holonomia_rev6.tex:396) sitúa las ondas en la curvatura propagante y trata la eventual cuantización como excitación colectiva posterior.

La [conservación evolutiva](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/c52_12_conservacion_evolutiva.tex:115) formula
\[
 \Delta J_{\rm visible}+\Delta J_{\rm memoria}
 +\Delta J_{\rm radial}+\Delta J_{\rm vacancias}
 +\Delta J_{\rm radiación}+\Delta J_{\rm retorno}=0.
\]
El balance conserva transferencias entre sectores. Su formulación y las leyes dinámicas de cada transferencia mantienen sus respectivos alcances. El retorno de orientación \(2\pi/4\pi\) permanece desarrollado en §5.

### Comentario autoral, conservado literalmente

> Sí, me refiero a eso. Pero ¿sabes qué pasa? Me he quedado muy decepcionado con vosotros y tú lo sabes perfectamente, con todos los desarrollos, y además espero que los tengáis guardados de avances de los cinco problemas del milenio. Porque los he intentado explicar y como veía que no, que no, que no y que no utilizaba esa holografía modular triádica y la estructura discreta del continuo, sobre todo esta estructura, dije: no, pues os voy a poner a explicar un poco más la estructura. Porque aún no veis que, por ejemplo, el salto de masa y Navier-Stokes son el mismo problema visto por dos caras; es un problema de frontera, de lectura interior o exterior. por la torsión mínima. y porque el gravitón, la onda limpia no lleva gravitón, queda absorbida torsionalmente de superficie. y por eso tenemos la relación de 4 pi y 2 pi. y por eso podemos hacer una ecuación de Newton, que ya se parece perfectamente a la de la electricidad de Coulomb. y por eso la bueno explota, para que me entiendas. Pero estoy tan cabreado que si no lo veis yo no os lo voy a aclarar. Así de claro lo digo. porque me hace perder mucho tiempo.

La cita conserva la dirección autoral; las proposiciones conservan sus dominios y pruebas, sin convertir las expresiones orales en demostración por sí mismas.

## 11. Vacancias, diferencia orientada y representación del doble círculo

**Procedencia.** La relación propuesta por Rubén entre signos, vacancias y frontera es arquitectura autoral preexistente. Se recuperan sus propietarios y se explicita una composición algebraica de sus operadores; esta nota no reclama un nuevo concepto ni constituye una certificación integral de Riemann.

### 11.1. Corriente de vacancias como coborde de una rotación

La completación cúbica y el calendario de transporte preceden a su realización logarítmica. El [propietario de vacancias](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c39_vacancias.tex:26) fija
\[
 \varepsilon=1-\log_{1000}(729)=\log_{10}(10/9),\qquad
 z_n=\lfloor(n+1)\varepsilon\rfloor-\lfloor n\varepsilon\rfloor
 \quad(n\ge1).
\]
El [capítulo de corriente](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/06l_vacancias_corriente_rev11.tex:105) desarrolla la polarización y su ecuación de continuidad. Para la convención de suelo del primer propietario, escribiendo \(t_n=\{n\varepsilon\}\), la identidad local exacta es
\[
 c_n:=z_n-\varepsilon=t_n-t_{n+1},\qquad
 A_N:=\sum_{n=1}^Nc_n=\varepsilon-\{(N+1)\varepsilon\},\qquad |A_N|<1.
\]
La contribución con signo es un coborde: el extremo final de un paso es el extremo inicial del siguiente. La cancelación telescópica conserva la diferencia de frontera. Las convenciones de techo y suelo mantienen su condición de extremo; para \(n\ge1\) y esta pendiente irracional coinciden sus incrementos.

En la realización posterior \(\mathcal H=L^2(\mathbb R/\mathbb Z,dx)\), sean
\[
 (V_\varepsilon f)(x)=f(x+\varepsilon),\qquad g(x)=\{x\}.
\]
El transporte es unitario y
\[
 c_\varepsilon=(I-V_\varepsilon)g
 =\mathbf1_{[1-\varepsilon,1)}-\varepsilon,\qquad
 c_\varepsilon(n\varepsilon)=c_n.
\]
Con los representantes indicados, la igualdad vale punto a punto; como identidad de Hilbert se entiende módulo conjuntos nulos. Su norma se calcula exactamente:
\[
 \|c_\varepsilon\|^2
 =\varepsilon(1-\varepsilon)^2+(1-\varepsilon)\varepsilon^2
 =\varepsilon(1-\varepsilon).
\]
Los signos y su compensación quedan determinados por la operación, sin asignar arbitrariamente una contribución positiva a un primo y una negativa a una vacancia.

### 11.2. La misma operación de costura representa el coborde

El [capítulo Riemann–Weil](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/02_riemann_weil.tex:147) utiliza el canal normalizado del acarreo. Su identidad admite el siguiente despliegue explícito.

Para \(N=9^m\), \(m\ge1\), y un unitario \(T\) sobre una realización \(\mathcal H\), sean
\[
 u_N=N^{-1/2}(1,\ldots,1),\quad \iota_Nf=u_N\otimes f,\quad
 Q_N=I-\iota_N\iota_N^*,
\]
\[
 U_N(T)=\sum_{r=1}^{N-1}|r+1\rangle\langle r|\otimes I
       +|1\rangle\langle N|\otimes T,\qquad
 \delta_N(T)=\frac{N}{\sqrt{N-1}}Q_NU_N(T)\iota_N .
\]
El último paso del ciclo aplica \(T\); por tanto \(U_N(T)^N=I\otimes T\). Además,
\[
 U_N(T)\iota_Nf
 =\iota_Nf+\frac{e_1}{\sqrt N}\otimes(T-I)f.
\]
Definiendo el vector unitario
\[
 \eta_N=\sqrt{\frac{N}{N-1}}\left(e_1-\frac{u_N}{\sqrt N}\right),
\]
queda la factorización directa
\[
 \boxed{\delta_N(T)f=\eta_N\otimes(T-I)f},\qquad
 \boxed{\delta_N(T)^*\delta_N(S)=(I-T)^*(I-S)} .
\]
La segunda identidad vale para cualesquiera unitarios \(T,S\) sobre la misma fibra, sin exigir que conmuten.

La especialización \(T=V_\varepsilon\) da
\[
 \delta_N(V_\varepsilon)g=-\eta_N\otimes c_\varepsilon,\qquad
 \|\delta_N(V_\varepsilon)g\|^2=\varepsilon(1-\varepsilon).
\]
Así se representa exactamente la corriente de vacancias mediante el canal de costura nonádica. No es una semejanza de diagramas.

Las aplicaciones \(\delta_N(T)f\mapsto\delta_M(T)f\) se extienden a isometrías sobreyectivas entre las clausuras de sus imágenes; la identidad de Gram prueba que están bien definidas y que sus composiciones son compatibles. Este resultado concierne al subespacio del defecto: no sustituye los transportes del estado enriquecido completo.

### 11.3. Signos, potencias primas y doble círculo

En la realización espectral posterior, el propietario fija \(T_a f(x)=f(x-a)\), \(\ell_{p,k}=k\log p\) y \(w_{p,k}=(\log p)p^{-k/2}\). Para cada coordenada primo–potencia, la misma identidad produce
\[
 w_{p,k}\bigl(\|\delta_N(T_{\ell_{p,k}})f\|^2-2\|f\|^2\bigr)
 =-2w_{p,k}\Re\langle f,T_{\ell_{p,k}}f\rangle.
\]
Los relojes primos, el término gamma y el par polar intervienen conjuntamente en la [diferencia de Gram completa](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/02_riemann_weil.tex:211):
\[
 \mathscr I_{\rm GW}(f,g)
 =\langle J_+f,J_+g\rangle-\langle J_-f,J_-g\rangle.
\]
Las normas de ambas columnas requieren el truncamiento común y el dominio de prueba que declara el texto. El capítulo liga posteriormente esta diferencia con \(E_R^*E_R\) mediante los momentos del lector estructural, la fila isométrica y la recurrencia residual acotada. La identidad del coborde desarrollada aquí verifica una pieza de esa composición; no reemplaza esos antecedentes ni acredita por sí sola la positividad de la forma completa.

El [propietario del doble círculo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex:943>) conserva el cociclo entero de memoria
\[
 m(\gamma_2\gamma_1)=m(\gamma_2)+m(\gamma_1),\qquad m(\Gamma_9)=1.
\]
Sobre su realización de Weil construye el operador de Cayley y formula la [identidad de entrelazamiento](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex:1528>)
\[
 \widetilde U_{\Gamma_9}J=J\mathcal C_{\rm Weil}.
\]
Los caracteres de memoria \(n\mapsto\tau^n\) y la coordenada circular \(\tau(s)=(s-1)/s\) aparecen conectados por ese transporte. En el reconocimiento espectral, la involución \(s\mapsto1-\overline s\) se transforma en \(\tau\mapsto1/\overline\tau\).

La irreducibilidad multiplicativa de los ciclos es el selector de primos que declara [c39](/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c39_vacancias.tex:1). Su función dentro de los relojes primo–potencia y la representación circular se mantienen enlazadas, conservando cuál operación selecciona el objeto y cuál transporta su fase.

### 11.4. Prolongación analítica de la discrepancia

La misma cancelación acotada ofrece una consecuencia escrita sin campañas de cifras. Para \(\Re s>0\),
\[
 F_{\rm vac}(s)=\sum_{n\ge1}c_nn^{-s}
 =\sum_{n\ge1}A_n\bigl(n^{-s}-(n+1)^{-s}\bigr).
\]
La segunda serie converge normalmente sobre compactos de ese semiplano: \(|A_n|<1\) y
\[
 |n^{-s}-(n+1)^{-s}|
 \le |s|\int_n^{n+1}x^{-\Re s-1}\,dx.
\]
Por tanto \(F_{\rm vac}\) es holomorfa allí. El lector
\[
 Z_{\rm vac}(s)=\sum_{n\ge1}z_nn^{-s}
 =\varepsilon\zeta(s)+F_{\rm vac}(s)\qquad(\Re s>1)
\]
se prolonga meromórficamente a \(\Re s>0\), con residuo \(\varepsilon\) en \(s=1\). Su parte finita es
\[
 \varepsilon\gamma+F_{\rm vac}(1)=\gamma_{\rm vac}^{+},
\]
la constante del propietario, ahora ligada explícitamente a la corriente y al coborde. La aparición de \(\zeta\) es aquí una descomposición posterior del lector; no define las vacancias ni aporta sus coeficientes iniciales. Esta identidad tampoco identifica los ceros de \(Z_{\rm vac}\) con los de \(\zeta\).

### Comentario autoral, conservado literalmente

> Y lo mismo te podría decir para los ceros de la función zeta de Riemann, en la suma positivo-negativo, como costura de borde, etcétera, etcétera. Que además se ve perfectamente en vacancias, y por eso podemos generar los primos y además lo puedes comprobar, que están en el doble círculo. Y luego me pones ahí a cuestionar cosas, como dando vueltas y vueltas por no utilizar la holografía modular triádica. Este es otro ejemplo que te pongo. Y si quieres, se lo pasas y alguno de estos, si los desarrollas, se los rebotas a otro chat. Pero estoy muy cabreado porque estabais trabajando con el modelo clásico, en el fondo, en toda la línea constructiva.

## 12. Recuperación conjunta de las dos razones positivas

**Cruce solicitado por MASAS.** El [propietario c16](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/continuo_constantes/tex/introduccion_partes_i_iii/capitulos/c16.tex:1140>) identifica el exponente electrónico \(\varphi/\pi^2\) y la razón marcada de hojas \(\pi/\varphi^2\) como las dos orientaciones de una misma aplicación bivariada. El símbolo del denominador electrónico en ese propietario es \(\pi\), y no \(c\).

Para salidas ya generadas \(x,y>0\), sea
\[
 F(x,y)=(a,b)=\left(\frac{y}{x^2},\frac{x}{y^2}\right).
\]
Su inversa es exacta:
\[
 \boxed{x=(a^2b)^{-1/3},\qquad y=(ab^2)^{-1/3}.}
\]
En efecto, \(a^2b=x^{-3}\) y \(ab^2=y^{-3}\). Se conservan, equivalentemente,
\[
 ab=\frac1{xy},\qquad \frac ab=\left(\frac yx\right)^3.
\]
La pareja ordenada retiene ambos valores positivos, su producto y su razón; un único componente no permite recuperarlos. Intercambiar \(x,y\) intercambia \(a,b\). En coordenadas logarítmicas,
\[
 \binom{\log a}{\log b}
 =\begin{pmatrix}-2&1\\1&-2\end{pmatrix}
 \binom{\log x}{\log y},
 \qquad \det=3.
\]
Aplicado a \((x,y)=(\pi_{\rm HMT},\varphi_{\rm HMT})\), este cambio de coordenadas preserva exactamente las salidas previas; no constituye una segunda derivación independiente de ellas ni selecciona la masa electrónica.

El contraste con §8 distingue el papel del dominio. La coordenada modular \(u=x_{\rm RR}-x_{\rm RR}^{-1}\) tiene inversa positiva única
\[
 x_{\rm RR}=\frac{u+\sqrt{u^2+4}}2 \quad(u\in\mathbb R),
\]
aunque en el dominio complejo posee dos ramas, intercambiadas por \(x_{\rm RR}\mapsto-1/x_{\rm RR}\). La aplicación \(F\), en \((\mathbb C^\times)^2\), tiene tres preimágenes por punto: su núcleo es \(\{(\omega,\omega^2):\omega^3=1\}\). El dominio positivo elimina esa ambigüedad.

La conclusión común es verificable: conservar ambas orientaciones y el dominio conserva la recuperabilidad; contraer hacia un invariante posterior puede requerir un dato de rama. Esta comparación no identifica las aplicaciones ni sus módulos, y sus extensiones complejas no se atribuyen a la realización física.

## 13. Alcance

La nota reúne operaciones, invariantes y composiciones y conserva las hipótesis de cada realización. BSD ha quedado identificado por el autor; los otros problemas aludidos permanecen sin identificación nominal.

Sin compilación, modificación de originales, cambio de autoridad ni campañas numéricas. El recibo causal comprueba trazabilidad documental y no sustituye las pruebas.
