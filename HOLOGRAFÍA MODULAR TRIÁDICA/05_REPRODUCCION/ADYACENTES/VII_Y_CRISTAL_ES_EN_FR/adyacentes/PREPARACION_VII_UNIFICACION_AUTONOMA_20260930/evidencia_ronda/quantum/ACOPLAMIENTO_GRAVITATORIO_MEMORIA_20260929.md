# Operador acoplado, Gauss y refinamiento dinámico con memoria

Formalización nueva focal, 29 de septiembre de 2026. Continúa
`MEMORIA_DOMINIO_Y_ALGEBRA.md`; no la sustituye y no modifica fuentes publicadas.

## 1. Objetos recibidos y construcción efectiva

La procedencia es APP → TRIT → TPK → estado enriquecido → estructura discreta
conjunta del continuo. Se reciben sus rutas, fibras, transportes, reloj completo,
incidencias y memoria, sin reemplazar el estado por el cociente visible. Se
reutiliza el recibo `../RECIBO_GENEALOGIA.json`. Las constantes y normalizaciones
que aparecen en las realizaciones son salidas anteriores, no objetivos
metrológicos. No se separan las cinco construcciones consustanciales del continuo.

Los propietarios materiales utilizados son:

- `VIII_ES/fuentes_conservadas/02_dinamica_tres_hojas.tex`, «Corona nonádica y energía torsional»: \(H_{\rm clk}+D_9^*WD_9\) y cuadrados de refinamiento; «Reducción de Feshbach–Schur»: resolvente con memoria.
- `VIII_ES/manuscrito/30b_variacion_energia_memoria.tex`: peso global positivo, diferencial completo y refinamiento.
- `VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex`, líneas 28–79 y 187–237: transportes invertibles, corriente efectiva de conexión y variación de todos los términos materiales antes de Cartan.
- `VIII_ES/manuscrito/30d_realizacion_geometrica.tex`: realización de holonomías y conservación de composición, inversión y subdivisión.
- `X_ES/sections/ym_complete.tex`, líneas 313–344, 415–425, 650–728 y 796–836: generador gauge, Gauss física, actualización Gibbs y límite.
- `X_ES/sections/hamiltonianos_curvatura.tex`, líneas 552–608: lectura energética \(H_E=\hbar cD^{\rm YM}\).

Todos esos caminos son relativos a
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`.
El antecedente Einstein–Schrödinger es
`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex`.

Se trabaja en una carta celular finita del mismo registro, sin congelar su
coordenada geométrica. Sea \(x\) un estado geométrico enriquecido de esa carta,
\(a:s(a)\to t(a)\) una incidencia y \(u_a\) la conexión interna representada
sobre el portador material ya construido. En la fibra común definimos

\[
T_a(x,u)=U_a^{\rm sp}(x)\otimes R_{\rm int}(u_a),\qquad
(D_Tf)_a=f_{t(a)}-T_a(x,u)f_{s(a)}.\tag{1}
\]

Se usa la representación quiral/material correspondiente; no se identifica el
SU(2) de espín con SU(2) débil. En una suma de representaciones, (1) se toma
por bloques. La construcción Yukawa y sus entrelazadores se conservan en el
propietario focal `COMPATIBILIDAD_QUIRAL_Y_ANOMALIAS.md` y su sucesor dinámico.

Con el peso global positivo \(W_m(x,u)\) del propietario —incluidos sus
bloques entre incidencias—, el operador de respuesta es

\[
\boxed{B_m(x,u)=D_T(x,u)^*W_m(x,u)D_T(x,u).}\tag{2}
\]

Ésta no es una suma de una matriz de gravedad y otra de materia. Por ejemplo,
en una sola arista con peso identidad y transportes unitarios,

\[
B(T)=\begin{pmatrix}I&-T^*\\-T&I\end{pmatrix}.
\]

La diferencia mixta de sus bloques de salto es
\(-\Delta U^{\rm sp}\otimes\Delta R_{\rm int}\), generalmente no nula.
El transporte de la materia contiene ambas conexiones antes de tomar su
energía o sus corrientes.

El bloque \(D_T^*WD_T\) es de segundo orden. Su positividad y covariancia
no lo convierten en el cinético Weyl de primer orden ni demuestran una
discretización quiral sin duplicación. (4) incorpora este bloque como respuesta
energética/geometría acoplada; cualquier identificación con el cinético
relativista de materia conserva el entrelazador y el tratamiento quiral propios.

## 2. Hamiltoniano cuántico común en la carta finita

La geometría permanece en el espacio del registro \(\ell^2(X_m)\), no en un
parámetro fijo elegido posteriormente. Sobre cada \(x\), las configuraciones
internas residen en los enlaces de la misma pantalla. Su medida es la medida
gauge invariante ya construida, o la extensión finita al producto de grupos
mediante su acción representada. Esta última extensión no importa una prueba
de brecha para U(1): aquí sólo se demuestra autoadjunción y Gauss.

En una carta compacta finita, si
\(d\mu_x=Z_x^{-1}e^{-S_x}d\mu_0\), el mapa

\[
A_x:L^2(\mu_0)\to L^2(\mu_x),\qquad
A_xf=\sqrt{Z_x}\,e^{S_x/2}f\tag{3}
\]

es unitario. Su densidad es gauge invariante. Permite transportar el reloj
heredado a las distintas fibras de medida sin declararlas idénticas:
\(H_{\rm clk}^{\mu}=A(H_{\rm clk}\otimes I)A^*\), donde
\(A=\bigoplus_xA_x\). En presencia de transporte de espín del reloj se
conserva ese transporte; no actúa como una carga gauge interna.

Para las actualizaciones de enlace, sea \(E_{e,x}\) la esperanza condicional
respecto de todos los enlaces salvo \(e\). Su fórmula efectiva es

\[
(E_{e,x}F)(u_{\ne e})=
\frac{\int F(u_{\ne e},v)e^{-S_x(u_{\ne e},v)}d\lambda_e(v)}
{\int e^{-S_x(u_{\ne e},v)}d\lambda_e(v)}.
\]

Es una proyección ortogonal en \(L^2(\mu_x)\), aunque para una acción
acoplada las distintas proyecciones no tienen por qué conmutar. Para la carta
finita,

\[
K_{m,x}=3\kappa_{\rm av}\sum_e(I-E_{e,x})
\]

es un operador acotado, positivo y autoadjunto. El sumando del propietario
Yang–Mills se recupera cuando se usa su coordenatización y su acción concreta.

En el portador fermiónico finito \(\mathcal F_m=\Lambda^*V_m\),
\(d\Gamma(B)=\sum_{ij}B_{ij}a_i^*a_j\). Definimos

\[
\boxed{H_m^{\rm ac}=H_{{\rm clk},m}^{\mu}
+\hbar c\,K_m+d\Gamma(B_m).}\tag{4}
\]

Todos los términos actúan sobre la misma suma de fibras
\(\bigoplus_xL^2(\mu_x;\mathcal F_m)\). El reloj mezcla estados
geométricos y (2) depende de esos estados; por ello (4) permite entrelazamiento
y transferencia de energía entre registro geométrico y materia. Si
\([H_{\rm clk}^{\mu},B_m]\ne0\), el sector geométrico no es un fondo
estático de esta evolución.

**Teorema finito.** Con un registro geométrico finito, transportes y pesos
acotados en la carta, y el reloj autoadjunto heredado, (4) es un operador
acotado autoadjunto sobre todo el espacio. Genera el grupo unitario
\(e^{-itH_m^{\rm ac}/\hbar}\). Si sólo el reloj es no acotado y los otros
términos conservan esas cotas, el mismo resultado vale con dominio
\(D(H_{{\rm clk},m}^{\mu})\), por perturbación autoadjunta acotada.

**Prueba.** Cada \(E_e\) es una proyección ortogonal; la suma es finita.
\(B_m\ge0\) por (2), con norma uniformemente acotada en las fibras de la
carta. En la Fock fermiónica de \(N_m\) modos,
\(\|d\Gamma(B_m)\|\le N_m\|B_m\|\). La conjugación (3) conserva
autoadjunción del reloj. La suma acotada de operadores autoadjuntos es
autoadjunta; en el caso no acotado se aplica el teorema de perturbación
acotada sobre el dominio declarado. ∎

Las cotas son de la carta finita; no se anuncian como uniformes en el número
de celdas o en el número de modos. El término de Higgs–Yukawa que construye el
otro desarrollo se añade en su dominio demostrado, sin cambiar las pruebas
de Gauss cuando conserva la misma representación.

## 3. Gauss exacta y corrientes de la misma respuesta

Para una transformación interna \(k=(k_v)\), sean
\(V_k=\bigoplus_vR(k_v)\) en las fibras de vértice y
\(E_k=\bigoplus_aR(k_{t(a)})\) en las de incidencia. El espín se conserva
como factor distinto. Por transformación de los extremos,

\[
T_a^k=R(k_{t(a)})T_aR(k_{s(a)})^{-1},\quad
D_{T^k}V_k=E_kD_T,\quad W^k=E_kWE_k^*.
\]

En consecuencia,

\[
B(x,u^k)V_k=V_kB(x,u).\tag{5}
\]

Sobre las funciones cuánticas, la transformación actúa simultáneamente por
cambio de configuración \(u\mapsto u^k\) y por \(\Gamma(V_k)\) en la
Fock. La invariancia de la medida hace unitaria esta acción. La disintegración
de la medida prueba que las esperanzas condicionales se transportan bajo esa
acción; (3) también la entrelaza. De (5) resulta

\[
[\mathcal U(k),H_m^{\rm ac}]=0,\qquad
P_m^{\rm G}=\int\mathcal U(k)dk,\quad
[P_m^{\rm G},H_m^{\rm ac}]=0.\tag{6}
\]

No se afirma que \(B(x,u)\) con una conexión fija conmute con toda
\(R(k)\): lo probado es la covariancia (5) y su realización cuántica (6).

Para el producto compacto conectado de grupos internos, los generadores
\(G_a=i\hbar\,d\mathcal U(X_a)\) satisfacen sobre los vectores suaves

\[
[G_a,G_b]=i\hbar f_{ab}{}^cG_c,\qquad
H_m^{\rm ac}\bigcap_a\ker G_a\subset\bigcap_a\ker G_a.
\]

El dominio suave es invariante por \(H_m^{\rm ac}\) en el caso acotado,
pues éste conmuta con la representación y sus convoluciones suavizantes.
Éstas son las restricciones Gauss internas. No se ha identificado el promedio
compacto con un promedio de Haar normalizado sobre el grupo de Lorentz no
compacto ni con la restricción Hamiltoniana de Einstein.

Las dos corrientes proceden de (2), no de acciones añadidas a posteriori.
Para \(r=D_Tf\), \(q=Wr\),

\[
\delta\langle f,Bf\rangle
=-2\operatorname{Re}\sum_a\langle q_a,\delta T_a f_{s(a)}\rangle
+\langle r,\delta W r\rangle,\tag{7}
\]

con
\(\delta T_a=\delta U_a^{\rm sp}\otimes R(u_a)
+U_a^{\rm sp}\otimes\delta R(u_a)\).
Las variaciones geométrica y gauge conservan el mismo residuo, peso y estado.
La segunda cuantización conserva la identidad en cada matriz de un cuerpo;
su expectativa se calcula en el mismo estado cuántico de (4).

## 4. El cuadrado dinámico exacto usa el resolvente completo

Sea \(J:\mathcal H_b\to\mathcal H\) una inclusión isométrica de datos
retenidos; el complemento contiene los datos de memoria, no un descarte físico.
En esa descomposición del Hamiltoniano acoplado,

\[
H=\begin{pmatrix}H_{bb}&V\\V^*&H_{ii}\end{pmatrix}.
\]

Para \(\operatorname{Im}z\ne0\), en el caso acotado ya construido,

\[
\boxed{J^*(H-z)^{-1}J=K_b(z)^{-1},\quad
K_b(z)=H_{bb}-z-V(H_{ii}-z)^{-1}V^*.}\tag{8}
\]

Esta igualdad es el cuadrado de reducción dinámica: el dato que pasa al nivel
retenido incluye la dependencia espectral, equivalente a memoria temporal.
No se sustituye por \(H_{bb}-VH_{ii}^{-1}V^*\) salvo para la lectura
estática correspondiente.

**Prueba.** Resolver la segunda fila de \((H-z)(b,i)=(f,0)\) da
\(i=-(H_{ii}-z)^{-1}V^*b\); la primera fila es \(K_b(z)b=f\).
Las dos inversas existen para \(z\) no real por autoadjunción. ∎

Eliminar memorias en dos etapas o de una vez da exactamente el mismo
\(K_b(z)\), siempre que se conserve el mismo \(z\) y todos los bloques
cruzados. Es la asociatividad de la resolución del mismo sistema lineal, no
una igualdad escalar aislada. Si la representación gauge preserva las
subdivisiones retenida/interior, cada bloque transforma covariantemente y
también lo hace \(K_b(z)\). Así Gauss y reducción dinámica conmutan.

## 5. Refinamiento nonádico evaluado: nueve incidencias y norma temporal

Se evalúa (8) en una arista subdividida en nueve, con transportes unitarios
\(T_1,\ldots,T_9\) y el peso homogéneo de refinamiento \(9\) respecto del
peso grueso uno. Este peso sale de sumar nueve resistencias \(1/9\), no
de una calibración física. Sea \(R_j=T_j\cdots T_1\), \(R_0=I\),
\(T_\gamma=R_9\). La transformación \(f_j=R_j\xi_j\) reduce la forma a

\[
9\sum_{j=1}^9\|\xi_j-\xi_{j-1}\|^2.
\]

Dados \(f_0=a,f_9=b\), su extensión minimizante es

\[
f_j=R_j\left((1-j/9)a+(j/9)T_\gamma^*b\right).
\]

Su energía es \(\|b-T_\gamma a\|^2\). Por tanto el operador de frontera
estático es exactamente

\[
H_b=\begin{pmatrix}I&-T_\gamma^*\\-T_\gamma&I\end{pmatrix}.\tag{9}
\]

Pero la norma de la extensión completa es \(\langle(a,b),Z(a,b)\rangle\),
donde el cálculo de las diez fibras da

\[
\boxed{Z=\begin{pmatrix}
\frac{95}{27}I&\frac{40}{27}T_\gamma^*\\
\frac{40}{27}T_\gamma&\frac{95}{27}I
\end{pmatrix}.}\tag{10}
\]

En efecto, \(\sum_{j=0}^9(1-j/9)^2=95/27\) y
\(\sum_{j=0}^9(j/9)(1-j/9)=40/27\). No se supone que los nueve
transportes conmuten: sólo se usa su producto ordenado y su unitariedad.

La expansión exacta del resolvente alrededor de cero es

\[
K_b(z)=H_b-zZ-z^2VH_{ii}^{-3}V^*-\cdots.\tag{11}
\]

Los polos de \(H_{ii}\) delimitan esta serie; (8) conserva la respuesta
fuera de ese régimen. (9) cierra el cuadrado estático y (8)–(11) cierran el
cuadrado dinámico con memoria. El supuesto salto directo
\(H_{\rm fino}J=JH_b\) no se deduce de (9) y normalmente falla:
la métrica temporal (10) no es la identidad.

## 6. Restricción Hamiltoniana: cálculo de la flecha, sin renombrarla

También puede calcularse el álgebra exacta de las densidades de (2). Para un
peso diagonal por incidencias, sea \(b_a=D_a^*W_aD_a\), y publiquemos
\(C_m(N)=\sum_aN_ab_a\). Entonces, sobre el dominio finito,

\[
\boxed{[C_m(N),C_m(M)]
=\sum_{a<b}(N_aM_b-M_aN_b)[b_a,b_b].}\tag{12}
\]

Las incidencias de soporte disjunto conmutan; las que comparten una fibra
producen transportes ordenados de dos pasos. En un peso global se mantiene
la expresión completa por bloques, sin borrar sus cruces. La fórmula (12)
es un cálculo nuevo de la densidad energética acoplada: determina qué
operador debe transportar el lado de deformaciones de pantalla.

En concreto, para dos incidencias consecutivas, pesos uno y transportes
unitarios \(T_1,T_2\), sobre sus tres fibras de vértice,

\[
[b_1,b_2]=
\begin{pmatrix}
0&-T_1^*&T_1^*T_2^*\\
T_1&0&-T_2^*\\
-T_2T_1&T_2&0
\end{pmatrix}.\tag{12a}
\]

El término de dos pasos y su orientación están calculados, no se ocultan en
una denominación. \(C_m(N)\) designa aquí la respuesta ponderada del bloque
(2), no una declaración de que se hayan identificado ya todas las densidades
de restricción de (4) con las del Hamiltoniano PCH.

La identificación Einstein–Schrödinger exige comparar este operador con la
imagen del generador de deformaciones ya fijado por la realización geométrica,
no definir ese generador como el propio conmutador. El cuadrado concreto es

\[
\mathcal R_m\!\left([C_m(N),C_m(M)]\right)
\stackrel{?}{=}i\hbar\,\widehat V_m
\!\left(q_m^{ab}(N\partial_bM-M\partial_bN)\right),\tag{13}
\]

con \(\mathcal R_m\), \(q_m\) y \(\widehat V_m\) del mismo portador
geométrico. Esta nota entrega el lado izquierdo por (12), el operador común
por (4), Gauss por (5)–(6) y la reducción dinámica por (8); no reemplaza el
lado derecho por una definición circular ni declara comprobada (13) por
mera autoadjunción. Es la flecha exacta que delimita la promoción de este
resultado cuántico acoplado a las restricciones Einstein–Schrödinger completas.

## 7. Verificación y alcance

`verificar_acoplamiento_gravitatorio_memoria.py` evalúa transportes tensoriales
de espín, SU(3), SU(2) y fase U(1) con aritmética racional compleja; comprueba
la covariancia del operador acoplado, diferencias mixtas no nulas, y que el
reloj geométrico no conmuta con su interacción. Calcula además la eliminación
nonádica directa y por etapas, su operador estático y los coeficientes exactos
\(95/27,40/27\) de la norma temporal. Son falsadores de estas pruebas y no
seleccionan valores físicos ni una rama del generador por ajuste.

Resultado nuevo demostrado: un operador cuántico común en la carta finita,
su conservación Gauss y su refinamiento dinámico con memoria. El tratado de
dominios infinitos y las restricciones de deformación de (13) no se sustituyen
por este corte finito ni por el número de comprobaciones del script.
