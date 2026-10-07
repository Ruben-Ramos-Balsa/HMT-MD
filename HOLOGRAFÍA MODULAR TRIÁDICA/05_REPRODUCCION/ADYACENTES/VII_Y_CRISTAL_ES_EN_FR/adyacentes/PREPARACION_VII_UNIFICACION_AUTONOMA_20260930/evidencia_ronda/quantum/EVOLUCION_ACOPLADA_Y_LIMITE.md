# Evolución conjunta con geometría, calibre y materia: prueba sin corte de amplitud escalar

## 1. Procedencia y objeto preciso

APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo es el origen conservado de las rutas, el transporte, las hojas, la incidencia y la memoria utilizadas aquí. La escala de acción, los canales angulares, las masas y los lectores de respuesta se reciben como salidas de esa construcción, con sus condiciones; no se eligen mediante datos metrológicos. Las cinco construcciones del continuo permanecen correlacionadas en el objeto recibido.

El reconocimiento convencional posterior de esta composición es un Hamiltoniano autoadjunto sobre un espacio común. Esta nota demuestra una extensión nueva del corte finito: permite todas las amplitudes y excitaciones del campo escalar en una celularización espacial fija, conservando la geometría como registro cuántico. No equipara ese resultado con la eliminación simultánea de todos los reguladores espaciales ni con la representación completa de las restricciones gravitatorias.

Los propietarios y las pruebas de cada bloque están reunidos en `ACOPLAMIENTO_GRAVITATORIO_MEMORIA_20260929.md`, `HAMILTONIANO_FINITO_HIGGS_FOCK.md`, `REFINAMIENTO_DINAMICO_NONADICO.md` y `../INTEGRACION_MATEMATICA.md`. La presente prueba compone esos bloques; no afirma que aparezca literalmente en un propietario previo. En particular, el transporte covariante de segundo orden no se identifica por su nombre con un operador de Weyl de primer orden.

## 2. Un espacio y un operador, no cuatro evoluciones independientes

Se fija una celularización orientada finita, un registro geométrico finito X y su fibra fermiónica F de dimensión finita. Las variables escalares H_v recorren C² sin corte de amplitud ni de ocupación bosónica. Los enlaces internos recorren el producto compacto de grupos de la representación recibida. Sobre cada registro x se utiliza su medida gauge invariante μ_x. El espacio es

\[
\mathscr H=\bigoplus_{x\in X}L^2(G^E\times\mathbb C^{2|V|},\mu_x\otimes dH;\mathcal F).
\]

La identificación unitaria entre las medidas geométricas es la ya probada: `A_x f=√Z_x exp(S_x/2)f` si `dμ_x=Z_x^{-1}exp(−S_x)dμ₀`. En esta carta μ_x no depende de H. Se conserva así el reloj `H_clk^μ=A(H_clk⊗I)A*`, que puede mezclar registros geométricos.

El operador formal a realizar por su forma es

\[
\mathbb H=H_{\rm clk}^{\mu}+\hbar cK_{\rm gauge}
+d\Gamma(D_T^*WD_T)+H_{H,\rm cin}+V_H
+\widehat H_Y+\widehat H_{\rm tor}.
\tag{1}
\]

Aquí `T_a=U_a^sp⊗R_int(u_a)`, `D_T f=f_t−T_af_s`; W conserva los bloques cruzados recibidos. `H_Y` contiene `c_L†Y(H)c_R+h.c.`, con Y lineal en H y su conjugado y con masas y mezcla en la misma base. Cuando se incluye H_tor, todos los términos base de (1) se entienden en la carta efectiva reducida de §8 de la nota Higgs–Fock: no contienen como variable independiente la contorsión ya eliminada. Su lectura espinorial es

\[
H_{\rm tor}=-\sum_v\frac{N_vcC_\gamma}{\mathcal V_v}\widehat Q_{{\rm tot},v},
\qquad C_\gamma=\frac{3\kappa_{\rm grav}c\hbar^2}{16}\frac{\gamma^2}{1+\gamma^2},
\]
\[
\widehat Q_{\rm tot}=\sum_{a=1}^4s_a\{d\Gamma(\widetilde M_a)^2-d\Gamma(\widetilde M_a^2)\},
\qquad s=(-1,-1,-1,+1).
\]

La corriente reúne las especies antes de elevarla al cuadrado: se conservan los términos cruzados. La composición define esta realización reducida; no afirma equivalencia con una acción previa distinta que añada otro término dependiente de la misma contorsión. En ese otro problema, su variación también tendría que entrar en la eliminación. No se suman dos veces la interacción lineal eliminada y su cuártico efectivo.

Las geometrías no son externas a (1): sus índices pertenecen al mismo espacio, el reloj los mezcla y tanto los pesos como el transporte y el volumen dependen de ellos. Por ejemplo, la diferencia mixta del bloque de salto de `D_T*WD_T`, con W=I, contiene `−ΔU^sp⊗ΔR_int`. El término Yukawa modifica conjuntamente las ocupaciones de materia y del escalar. Estas dos propiedades impiden convertir (1) en una suma de cuatro sistemas independientes por el mero hecho de escribirlo como suma de términos.

## 3. Existencia sin corte escalar

Se declara la carta en la que se demuestra el resultado. La cinética escalar de momentos tiene forma `∫⟨∇_HΨ,A(x,u)∇_HΨ⟩`, con A real simétrica, uniformemente positiva y acotada, independiente de H. Si O_g es la representación real de la transformación de los dobletes, se exige `A(x,u^g)=O_g A(x,u)O_g^T`; la elección `A=⊕_v a_v(x)I₄` con a_v>0 cumple esta condición. Así se prueba su invariancia, no se la infiere de positividad. La energía espacial `∑_e a_e∥H_t−ρ_H(u_e)H_s∥²` se incluye también en H_H,cin como potencial cuadrático positivo: está acotada por C_grad r² en la carta, no es un operador acotado sobre todo L². Los pesos de volumen satisfacen `0<w_min≤w_v(x)≤w_max`. El acoplamiento cuártico recibido satisface λ_H>0. Los transportes, W y los coeficientes de torsión están acotados en esta carta; el número de modos fermiónicos es finito. No se afirma que estas cotas permanezcan uniformes al variar la geometría o el número de celdas.

Escribamos `r²=Σ_v |H_v|²`. En la sección recibida `μ_H²=λ_Hv²`. El potencial conserva su valor absoluto:

\[
V_H=\sum_v w_v\{-\mu_H^2|H_v|^2+\lambda_H|H_v|^4\}
=\sum_vw_v\lambda_H(|H_v|^2-v^2/2)^2
-\sum_vw_v\lambda_Hv^4/4.
\tag{2}
\]

El último término no se elimina: depende del volumen geométrico. Por Cauchy–Schwarz,

\[
\sum_vw_v\lambda_H|H_v|^4\ge a r^4,
\qquad a=\lambda_Hw_{\min}/|V|>0.
\tag{3}
\]

La Fock finita y la linealidad de Yukawa dan constantes finitas C_Y,C_T con

\[
\|H_Y(H)\|\le C_Yr,\qquad \|H_{\rm tor}\|\le C_T.
\tag{4}
\]

Para cualquier ε>0 y r≥0 se tienen las cotas exactas

\[
C_Yr\le\varepsilon r^4+
\frac{3C_Y^{4/3}}{4^{4/3}\varepsilon^{1/3}},
\qquad br^2\le\varepsilon r^4+\frac{b^2}{4\varepsilon}.
\tag{5}
\]

La primera se obtiene maximizando `C_Yr−εr⁴`; la segunda completando el cuadrado en r². La parte negativa cuadrática de (2) tiene una cota br². La energía espacial escalar es positiva y, para la cota superior de forma, cumple la misma estimación (5). El reloj es acotado en esta carta; el bloque gauge y `dΓ(D_T*WD_T)` son acotados y positivos. Se concluye que la forma total satisface

\[
q(\Psi)\ge c_1\|\nabla_H\Psi\|^2+
\frac a2\|r^2\Psi\|^2-C\|\Psi\|^2
\tag{6}
\]

para constantes c₁>0 y C finita, tomando ε=a/4 en las dos cotas.

**Teorema 1.** En esta carta, la forma de (1) es cerrada y acotada inferiormente sobre

\[
\mathcal Q=\{\Psi:\nabla_H\Psi\in L^2,\quad r^2\Psi\in L^2\}.
\]

Determina un único operador autoadjunto asociado H, y `exp(−itH/ℏ)` es unitario para todo tiempo. No se impone un corte a las amplitudes del campo H ni a sus excitaciones bosónicas.

**Prueba.** La norma `∥Ψ∥²+∥∇_HΨ∥²+∥r²Ψ∥²` es completa, por cierre de la derivada débil y del operador de multiplicación. La positividad uniforme de la cinética y (3) hacen equivalente a ella la norma de la forma positiva base. Las cotas (5) muestran que la forma de Yukawa y la parte cuadrática son infinitesimalmente acotadas respecto de esa base. Los restantes términos son acotados en la carta. Tras sumar una constante suficiente, (6) y la cota superior correspondiente hacen equivalente la norma de la forma completa a la norma base: por tanto es cerrada. El teorema de representación de formas cerradas produce el operador autoadjunto asociado, y su cálculo espectral da la evolución unitaria. La unicidad aquí es la del operador asociado a la forma y a su dominio declarados; no es una afirmación de esencial autoadjunción de cualquier expresión formal o dominio alternativo. ∎

## 4. Restricción interna y retirada del corte computacional

La representación compacta conjunta actúa por cambio de enlaces, transformación del doblete y segunda cuantización sobre la materia. Por la covariancia `D_{T^g}ρ(g)=E(g)D_T`, la transformación de W, la invariancia de μ_x y la identidad

\[
Y(gH)\rho_R(g)=\rho_L(g)Y(H),
\]

la forma q es invariante. La contracción torsional incluida es un singlete interno. El dominio Q también es invariante, pues las transformaciones escalares son unitarias y conservan r.

**Corolario 2.** El proyector de Haar Π sobre estados gauge invariantes reduce al operador H y a su evolución: `Π exp(−itH/ℏ)=exp(−itH/ℏ)Π`. No se necesita obtener esta propiedad mediante un promedio correctivo del Hamiltoniano.

**Prueba.** La invariancia de la forma y la unicidad de su operador asociado dan `R(g)H=HR(g)` en el dominio transportado. El promedio de la representación compacta es un proyector ortogonal; integra esa conmutación. ∎

Se pueden calcular aproximaciones finitas mediante bloques completos de Peter–Weyl en los enlaces y capas isotrópicas completas de grado total de Hermite en las coordenadas reales de H, junto con todos los índices de la carta finita. Las funciones suaves en los enlaces y Schwartz en H constituyen un núcleo de forma: truncamiento espacial suave, regularización y expansión de Hermite aproximan la norma de Q. En la carta compacta se supone la densidad de μ_x positiva, acotada y con inversa acotada, como ocurre para una acción S_x continua: la densidad y las normas equivalentes justifican también esa aproximación en μ_x. Los subespacios finitos anidados correspondientes tienen unión densa en Q y conservan la representación compacta. P_N es su proyección ortogonal respecto del producto con μ_x, no una proyección de Fourier de Haar reutilizada cuando las medidas difieren. El hecho de que Q no incluya derivadas respecto de los enlaces utiliza el carácter acotado de K_gauge en esta realización.

**Teorema 3.** Los operadores de Galerkin H_N de estas restricciones satisfacen, para λ>C,

\[
(H_N+\lambda)^{-1}P_N f\longrightarrow(H+\lambda)^{-1}f.
\tag{7}
\]

**Prueba.** La ecuación variacional coerciva de q+λ tiene solución única. Restar su versión de Galerkin da ortogonalidad; continuidad y coercividad acotan el error en norma de forma por una constante por el mejor error de aproximación. Éste tiende a cero por la densidad anterior, luego también el error L². La cota inferior (6) es independiente de este corte N. ∎

Los teoremas 1–3 son más fuertes que comprobar matrices hermíticas finitas: retiran ese corte computacional en el escalar y en las funciones de enlace para la carta espacial fija. No retiran el corte espacial, el del registro geométrico ni el de los modos fermiónicos. Tampoco autorizan una traza térmica finita: la dinámica de enlace acotada puede impedir que `exp(−tH)` sea de clase traza. La positividad temporal por núcleos de Gram sigue disponible con estados vectoriales, sin inventar una función de partición finita.

## 5. Refinamiento que conserva memoria y respuesta

La reducción del sistema completo se aplica al resolvente del mismo H:

\[
J^*(H-z)^{-1}J=
[H_{bb}-z-V(H_{ii}-z)^{-1}V^*]^{-1}.
\tag{8}
\]

En el caso acotado, esta identidad y la asociación de eliminaciones están probadas sin condiciones adicionales en la nota de acoplamiento. Para operadores no acotados, (8) requiere una descomposición que preserve los dominios, o su formulación mediante formas cerradas con bloques controlados; no se extiende automáticamente a cualquier proyección ortogonal.

La nota de refinamiento construye una realización explícita en rutas: `N=9^m`, energía `NΣ∥f_j−U_jf_{j−1}∥²` y norma L² exacta de la interpolación. Su respuesta de frontera converge a

\[
K(-\kappa^2)=\frac{\kappa}{\sinh\kappa}
\begin{pmatrix}\cosh\kappa I&-T^*\\-T&\cosh\kappa I\end{pmatrix},
\quad T=U_N\cdots U_1.
\tag{9}
\]

Los dos primeros coeficientes son el operador estático y su norma temporal `Z=[[I/3,T*/6],[T/6,I/3]]`. La prueba de (9) conserva el transporte conjunto; no reemplaza el estado enriquecido por su fase visible. El teorema de ruta y el teorema 3 retiran reguladores diferentes, por lo que no se intercambian sus límites sin cotas uniformes comunes.

Finalmente, el lector gravitatorio recibido utiliza

\[
L=\frac{5759}{23040}\alpha^{16}L_*,\quad
G=\frac{c^3L^2}{\hbar},\quad
R_X=\frac{G}{c^4}H_X,\quad H_X\Lambda_X=\hbar cI.
\tag{10}
\]

Estas son igualdades operatorias de su realización, no cuatro ajustes escalares independientes. La identificación de H con el H_X de esa realización debe conservar su carácter y sus dominios; (10) no selecciona por sí sola un Hamiltoniano arbitrario. Del mismo modo, la restricción radial no se confunde con el tensor de Einstein.

## 6. Conclusión matemática de esta intervención

Se ha construido y probado una evolución interactuante común, con geometría operatoria, transporte interno, Fock y campo escalar sin corte de amplitud, en la carta finita declarada. La reducción gauge es exacta. Hay además una reducción dinámica con memoria y un límite nonádico explícito para la realización de ruta. Las constantes conservan su procedencia y actúan como lectores anteriores de la composición.

No se ha probado aquí el cierre cuántico completo solicitado de las cuatro interacciones. El punto exacto que no cubren estos teoremas es la composición simultánea del límite espacial y quiral con la representación de todas las restricciones geométricas Einstein–Schrödinger del mismo operador. La nota de acoplamiento calcula el conmutador de las densidades de ruta; su identificación con el generador geométrico de deformaciones no se deduce de Gauss interna, autoadjunción o (10). Esta delimitación describe esta prueba y no declara que ese resultado no exista en el corpus.

El contraste focal de los propietarios vigentes sí recupera la composición positiva `holonomía TPK → e_m=J_scr,m β_m → corriente σ=M^{-1}s` y la identidad `M_mσ_m=P_m^T M_{m+1}σ_{m+1}`. Están en `VIII_ES/manuscrito/30d_realizacion_geometrica.tex`, líneas 18–59 y 97–123, y `30c_composicion_corriente_conexion.tex`, líneas 194–250, bajo el árbol de fuentes del 28 de septiembre citado por las notas. La variación de lapse de `33_corriente_espinorial_y_densidad.tex`, desde la línea 357, fija la energía en la realización homogénea. El rastreo focal de esas fuentes y de `AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929` no recuperó una prueba posterior de la identidad de restricciones para lapsos espaciales arbitrarios. No se convierte este resultado de búsqueda limitado en una afirmación de inexistencia en todo el corpus.

Las pruebas nuevas están completas en sus dominios. Los comprobadores adjuntos ejercitan sus identidades y controles negativos, pero no sustituyen los argumentos de forma cerrada, densidad ni paso al límite.
