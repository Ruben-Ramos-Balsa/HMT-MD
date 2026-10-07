# Cartas nativas y expectativa: cálculo de los dos momentos

Fecha del corte: 11 de septiembre de 2026. Nota interna de desarrollo, no modificación de un artículo ni dictamen global sobre HMT. No se ha comunicado a otras tareas del usuario.

## 1. Resultado del corte

Se han recuperado y compuesto las acciones explícitas del odómetro, del lector de diferencias, de la inclusión uniforme, del refinamiento de Helmert, de la frontera bidireccional y de la carta polar. El cálculo produce:

1. Los momentos de las columnas positiva y negativa, consideradas separadamente, están determinados por operadores explícitos. Incluyen todos los productos cruzados entre pruebas.
2. La expectativa uniforme no coincide con el refinamiento de Helmert. Sobre el modo de acarreo da un factor exacto, calculado abajo; no convierte por sí misma una diferencia de traslación en el modo uniforme.
3. El resolvente de cola gamma sí realiza la conversión analítica y reconstruye exactamente todas las filas negativas, sobre toda ventana y antes de utilizar un signo.
4. La frase de 10b, líneas 349–365, que identifica simultáneamente el primer momento del codificador y el momento de su proyección, no se obtiene de las tres identidades de cartas anteriores por una simple suma directa. Se localiza a continuación la composición adicional concreta que debe verificarse. No se declara ausente el lector estructural ni se identifica este control focal con el TPK completo.

El avance es un cálculo de acción y de productos cruzados, no una reiteración de que la proyección es positiva.

## 2. Propietarios y lectura efectuada

Se utilizan estos propietarios, leídos completos en este corte:

- **P10**: [10b — prueba espectral polar](</Users/ruben/Documents/New project/output/ARTICULO_VIII_PRIMOS_ESTRUCTURA_ESPECTRAL_20260910/antecedentes/integral/manuscrito/sucesor_102/deltas_ley9/10b_prueba_espectral_polar_riemann_weil_rectificacion_probatoria_20260903.tex>), 1.166 líneas. Las columnas están en 151–235; la expectativa y el codificador nativo en 288–367; la transferencia derivada de los momentos en 369–452; el codificador escrito mediante el complemento, más adelante, utiliza la identidad energética ya obtenida.
- **PG**: [Forma y Gram](</Users/ruben/Documents/excelencia academica/ARTICULOS_CIENTIFICOS_HMT_MD_2026-08-14/RIEMANN_REDHEFFER_WEIL/manuscrito/secciones/00_forma_y_gram.tex>), 630 líneas. Fórmulas explícitas de los dos modos y del refinamiento: 133–191; columnas: 194–220; codificador y momentos comunes: 222–304.
- **PT**: [Conector de cola gamma](</Users/ruben/Documents/excelencia academica/ARTICULOS_CIENTIFICOS_HMT_MD_2026-08-14/RIEMANN_REDHEFFER_WEIL/manuscrito/secciones/02b_conector_cola_gamma.tex>), completo. Inversión: 1–45; elevación y frontera: 47–155; todas las filas negativas: 157–242; restricción alcanzable: 250–269.
- **PO**: [Odómetro y acarreo](</Users/ruben/Documents/excelencia academica/CLAUSURA_WEIL_HMT_PULSACION_NONADICA_2026-08-11/PUBLICACION_WEIL_RIEMANN_HMT_MD_REVISION_EDITORIAL_2026-08-12/manuscrito/sections/03_odometro_carry.tex>), completo.
- **PE**: [Pulsación y expectativa](</Users/ruben/Documents/excelencia academica/CLAUSURA_WEIL_HMT_PULSACION_NONADICA_2026-08-11/PUBLICACION_WEIL_RIEMANN_HMT_MD_REVISION_EDITORIAL_2026-08-12/manuscrito/sections/02_pulsacion_y_expectativa.tex>), completo.
- **PP**: [Carta polar modular](</Users/ruben/Documents/excelencia academica/CLAUSURA_WEIL_HMT_PULSACION_NONADICA_2026-08-11/PUBLICACION_WEIL_RIEMANN_HMT_MD_REVISION_EDITORIAL_2026-08-12/manuscrito/sections/06_canal_polar_modular.tex>), completo. Carta Witt–dodecafase: 134–181.
- [Acarreo ortogonal del residual](</Users/ruben/Documents/excelencia academica/ARTICULOS_CIENTIFICOS_HMT_MD_2026-08-14/RIEMANN_REDHEFFER_WEIL/manuscrito/secciones/00d_carry_ortogonal_app_weil.tex>), completo.

Se contrastó además el propietario de las cinco realizaciones del continuo del 17 de agosto, sección de Riemann desde su objeto hasta el transporte del complemento, sin disgregar esas construcciones: allí se vuelve a formular el mismo par de momentos nativos. La consulta de esa sección no equivale a una lectura íntegra de todo ese manuscrito.

Los antecedentes de agosto se consultan como propietarios de las fórmulas que P10 reutiliza, no como sustitutos de la selección autoral del integral de 2.249 páginas. Los localizadores globales que todavía resuelven 2.084 páginas quedan registrados como históricos para esta serie.

## 3. Convenciones y corte genealógico

El punto de partida relevante es el estado APP–TRIT–TPK, su refinamiento con memoria y sus lectores nativos. En este corte:

- APP proporciona el soporte y el selector de irreducibles. P10, 258–286, conserva el producto nativo, la coproductividad y el selector antes de publicar las etiquetas primo–potencia.
- TRIT y el transporte de hojas conservan orientación y costura.
- El TPK conserva el paso de fase y el registro de acarreo; su odómetro induce la diferencia de traslación. La publicación logarítmica de los relojes produce \(\ell_{p,k}=k\log p\) y \(w_{p,k}=(\log p)p^{-k/2}\).
- Las cartas de frontera y polar son realizaciones posteriores de los mismos lectores. No se selecciona un estado mediante ceros de zeta ni mediante un valor objetivo.

La presente nota calcula la flecha entre esos lectores y la expectativa, después de la generación común; no pretende reconstruir ni sustituir el continuo conjunto.

Trabajamos con coordenadas ortonormales de historia. En ellas \(u_N=N^{-1/2}(1,\ldots,1)\). Si se usan funciones con medida de probabilidad uniforme, las coordenadas constantes y los promedios se conjugan por el factor de normalización correspondiente; las proyecciones y todos los cocientes de normas siguientes son los mismos.

Sea \(H=L^2(\mathbb R)\), \(T_af(x)=f(x-a)\), \(\mathcal D_R=C_c^\infty((-R/2,R/2))\). Se escribe \(d_a=T_a-I\); cambiar simultáneamente a \(I-T_a\) conserva sus Grams, pero cambia el signo de la cotraza inversora.

## 4. Acción del odómetro sobre generadores

Para \(N=9^m\), \(m\ge1\), y la costura situada en el primer vector,

\[
U_{a,N}(e_r\otimes f)=
\begin{cases}
e_{r+1}\otimes f,&r<N-1,\\
e_0\otimes T_af,&r=N-1.
\end{cases}
\]

La uniformización \(i_Nf=u_N\otimes f\) da

\[
U_{a,N}i_Nf
=u_N\otimes f+N^{-1/2}e_0\otimes d_af.
\]

Por tanto, para \(P_N=|u_N\rangle\langle u_N|\otimes I\),

\[
i_N^*U_{a,N}i_N=I+\frac{d_a}{N},
\qquad
(I-P_N)U_{a,N}i_N
=\frac{\sqrt{N-1}}{N}\eta_N\otimes d_a,
\]

donde

\[
\eta_N=\frac{Ne_0-\mathbf1_N}{\sqrt{N(N-1)}}.
\]

De aquí se recupera el lector normalizado de PG:

\[
\widehat\delta_{a,m}f=\eta_N\otimes u_{81}\otimes d_af,
\qquad
j_mf=u_N\otimes u_{81}\otimes f.
\]

La acción sobre cualquier combinación de generadores, sin eliminar sus cruces, es

\[
\left\langle\sum_i\widehat\delta_{a_i,m}f_i,
                  \sum_j\widehat\delta_{b_j,m}g_j\right\rangle
=\sum_{i,j}\langle d_{a_i}f_i,d_{b_j}g_j\rangle.
\]

En particular,

\[
\widehat\delta_{a,m}^*\widehat\delta_{b,m}=d_a^*d_b,\qquad
j_m^*j_m=I,\qquad
j_m^*\widehat\delta_{a,m}=0.
\tag{1}
\]

El último producto cruzado procede de \(\langle u_N,\eta_N\rangle=0\). Es información material de orientación de los modos, adicional a las dos normas aisladas.

## 5. Dos refinamientos distintos y sus expectativas

### 5.1 Inclusión uniforme de P10

Escribamos \(M=9N\) y \(\mathbb C^M=\mathbb C^N\otimes\mathbb C^9\). La inclusión y su adjunta son

\[
\iota_Nx=x\otimes u_9,\qquad
E_N=I_N\otimes\langle u_9|,\qquad P_N^{\rm unif}=\iota_NE_N.
\]

Actuando en coordenadas,

\[
E_Nu_M=u_N,\qquad
E_N\eta_M=a_N\eta_N,\qquad
a_N=\sqrt{\frac{N-1}{9N-1}}.
\tag{2}
\]

Prueba: \(E_Ne_0^{(M)}=e_0^{(N)}/3\) y \(E_N\mathbf1_M=3\mathbf1_N\). Sustituir en
\(\eta_M=(Me_0-\mathbf1_M)/\sqrt{M(M-1)}\) produce (2).

Por consiguiente,

\[
(E_N\otimes I)\widehat\delta_{a,m+1}=a_N\widehat\delta_{a,m},
\qquad
(E_N\otimes I)j_{m+1}=j_m.
\tag{3}
\]

Todos los momentos proyectados quedan determinados:

\[
\begin{aligned}
\widehat\delta_{a,m+1}^*(P_N^{\rm unif}\otimes I)\widehat\delta_{b,m+1}
 &=a_N^2d_a^*d_b,\\
j_{m+1}^*(P_N^{\rm unif}\otimes I)j_{m+1}&=I,\\
j_{m+1}^*(P_N^{\rm unif}\otimes I)\widehat\delta_{b,m+1}&=0.
\end{aligned}
\tag{4}
\]

La fracción complementaria del acarreo es \(1-a_N^2=8N/(9N-1)\). Para \(N=9\), la fracción publicada es \(1/10\), no \(1\), y su salida sigue siendo una diferencia.

No se confunden aquí \(P_N^{\rm unif}\), que promedia el último dígito, y la proyección sobre la única línea global \(u_M\): esta última anula \(\eta_M\) enteramente.

### 5.2 Refinamiento de Helmert de PG

El operador \(W_N\) de PG, 143–191, está fijado por la base de Helmert y cumple

\[
W_Nu_N=u_M,\qquad W_N\eta_N=\eta_M,\qquad W_N^*W_N=I.
\]

Así, \(E_N^{\rm H}=W_N^*\), \(P_N^{\rm H}=W_NW_N^*\) dan

\[
E_N^{\rm H}j_{m+1}=j_m,\qquad
E_N^{\rm H}\widehat\delta_{a,m+1}=\widehat\delta_{a,m}.
\tag{5}
\]

El producto cruzado uniforme–acarreo sigue siendo cero y el de dos diferencias sigue siendo \(d_a^*d_b\). Por ello el refinamiento es natural para ambos modos, pero no transforma uno en otro. En concreto, \(W_N\ne\iota_N\).

### 5.3 ¿Una expectativa conjugada resuelve el problema?

Existe una unitaria \(S_M\) sobre \(\mathbb C^M\) que lleva \(\iota_N\mathbb C^N\) a \(W_N\mathbb C^N\), con \(W_N=S_M\iota_N\). Basta enviar las dos bases ortonormales y completar los complementos. Entonces

\[
P_N^{\rm H}=S_MP_N^{\rm unif}S_M^*.
\]

Conjugando simultáneamente el estado \(C\) y su proyección,

\[
(S_MC)^*(S_MP S_M^*)(S_MC)=C^*PC,\qquad
(S_MC)^*(S_MC)=C^*C.
\tag{6}
\]

No cambia ninguno de los dos momentos. Si se cambia sólo la proyección, se pasa en este caso de la fracción \(a_N^2\) a \(1\), pero el operador analítico continúa siendo \(d_a\), no \(I\).

Más generalmente, para cualquier proyección que actúe únicamente en la fibra finita de historia, el momento de un único canal es
\(\langle\eta,P\eta\rangle d_a^*d_b\). No se convierte por ese cambio de base en \(2I\). Un eventual acoplamiento efectivo entre canales analíticos es otra operación y debe escribirse, no inferirse de la conjugación.

## 6. Qué prueban exactamente las cartas de frontera y polar

### 6.1 Frontera bidireccional

PT, 85–155, da

\[
K_2=\mathbb C^{81}\otimes u_9^\perp,\quad
\Delta_a=j_{\rm APP}(\eta_9\otimes d_a),\quad
\beta_0=R_{\rm tw}(L^3+\varepsilon\nabla_x)FI_{Q_9}|_{K_2}.
\]

Con \(V_\beta=\beta_0(\beta_0^*\beta_0)^{-1/2}\) y
\(U_{\rm tw}=(\Lambda_{\rm tw}^{\#})^{-1/2}V_\beta\),

\[
G_a=(U_{\rm tw}\otimes I)\Delta_a,\qquad
G_a^*(\Lambda_{\rm tw}^{\#}\otimes I)G_b=d_a^*d_b.
\tag{7}
\]

Esta igualdad conserva todos los cruces. \(U_{\rm tw}\) es isométrico para la métrica declarada \(\Lambda_{\rm tw}^{\#}\). En coordenadas hilbertianas ordinarias la unitaria es \((\Lambda_{\rm tw}^{\#})^{1/2}U_{\rm tw}=V_\beta\).

La identidad (7) no contiene una expectativa ni su valor sobre \(G_a\). Para transportar una proyección se debe conjugarla con esa misma isometría y su adjunta en la métrica correcta. Hecho así, (6) conserva el momento comprimido anterior: cambiar a la frontera no crea el segundo momento.

### 6.2 Carta polar efectiva

PP, 134–181, construye cinco octadas y

\[
T^*T=4I_5+\frac43J_5,\qquad
\widehat T=T(T^*T)^{-1/2},\qquad
F_{34}=(f_3,f_6,f_9,f_4,f_8).
\]

La carta con sus espacios explícitos es

\[
U=F_{34}\widehat T^*:
\operatorname{Ran}\widehat T\subset\mathbb C^{24}
\longrightarrow\operatorname{span}(f_3,f_6,f_9,f_4,f_8)\subset\mathbb C^{12}.
\]

Para \(\eta=\operatorname{diag}(1,1,1,-1,-1)\),

\[
U^*J_{34}U=\widehat T\eta\widehat T^*,\qquad
\widehat T^*U^*J_{34}U\widehat T=\eta.
\tag{8}
\]

Ésta es la escritura tipada de la igualdad con la matriz diagonal de P10. Los cinco roles son efectivos; la identificación de coordenadas no debe borrarse.

Para las dos evaluaciones polares,

\[
b_\pm(f)=\frac{A_f\pm B_f}{\sqrt2},\qquad
b_+(f)\overline{b_+(g)}-b_-(f)\overline{b_-(g)}
=A_f\overline{B_g}+B_f\overline{A_g}.
\tag{9}
\]

(8) transporta la firma y (9) transporta sus cruces. Ninguna identifica la línea positiva aislada con una fuente suficiente de la negativa: para \(f\) real, impar y no nulo, elegido con \(f(x)>0\) en el semieje positivo de su soporte, se tiene \(b_+(f)=0\) y \(b_-(f)>0\). La recuperación debe involucrar el estado analítico común, como efectivamente hace PT.

## 7. Diagnóstico preciso de la suma directa literal

Tomar como codificador la columna explícita \(\Xi_+\) de PG satisface por cálculo su primer momento. Aplicar después la expectativa uniforme de P10 produce en cada canal primo

\[
w_\ell a_N^2\langle d_\ell f,d_\ell g\rangle,
\]

mientras que la fila negativa requerida es

\[
2w_\ell\langle f,g\rangle.
\]

No son la misma identidad. Por ejemplo, elíjanse \(R>\ell>0\) y \(f\in\mathcal D_R\) real, no negativo, con soporte que se solape con su traslación por \(\ell\). Entonces

\[
\|d_\ell f\|^2
=2\|f\|^2-2\langle f,T_\ell f\rangle
<2\|f\|^2.
\tag{10}
\]

Ninguna proyección contractiva aplicada únicamente a ese canal puede producir \(\sqrt2f\). Para el refinamiento de Helmert se elimina el factor \(a_N^2\), pero persiste (10). Éste es un falsador de la identificación **canal por canal**, no una refutación de una transferencia común que redistribuya energía entre los canales.

Por otra parte, introducir directamente \(j_mf\), sus copias primo–escalares y \(b_-(f)\) como sumandos ortogonales del codificador asegura sus salidas, pero añade sus normas al primer momento. Para mantener el primer momento original se necesita una redistribución isométrica explícita. Esa redistribución es precisamente la operación que la frase de P10, 349–365, debe exhibir.

La invariancia del subespacio cíclico bajo \(P\), por sí sola, tampoco determina el valor de \(PCf\); sólo garantiza que ese valor permanece en el subespacio.

## 8. Composición efectiva recuperada: de la cola gamma a todas las filas

Aquí sí hay una acción explícita sobre todo generador y toda combinación lineal. Sea

\[
\mu(a)=\frac{e^{-a/2}}{1-e^{-2a}},\quad
A_R=[R+1,R+2],\quad \nu_R=\int_{A_R}\mu(a)\,da>0,
\quad M_R=\mathbf1_{(-R/2,R/2)}.
\]

Para el signo \(d_a=T_a-I\) de PG, definimos la cotraza

\[
\epsilon_m=\langle\eta_{9^m}|\otimes\langle u_{81}|\otimes M_R,
\qquad
\mathcal R^-_{m,R}F
=-\nu_R^{-1}\int_{A_R}\sqrt{\mu(a)}\,\epsilon_m F(a)\,da.
\tag{11}
\]

El signo menos desaparece si se usa \(I-T_a\), que es la convención del lector de cola de PT. Para \(f\in\mathcal D_R\) y \(a>R\), \(M_RT_af=0\). En consecuencia,

\[
\mathcal R^-_{m,R}
\bigl(a\mapsto\sqrt{\mu(a)}\widehat\delta_{a,m}f\bigr)=f.
\tag{12}
\]

Además \(\|\mathcal R^-_{m,R}\|\le\nu_R^{-1/2}\) por Cauchy–Schwarz. No se invierte una traslación individual ni se utiliza positividad de Weil.

Escribamos

\[
S_Rf=\left(\sqrt{-c_\Gamma}\,j_mf,\,
              (\sqrt{2w_\ell}\,j_mf)_{\ell\le R}\right),
\quad B_-f=\zeta_-b_-(f).
\]

La fila común concreta, definida sobre el ambiente positivo completo, es

\[
\mathcal C_R^{\rm tail}
=
\begin{pmatrix}
0&S_R\mathcal R^-_{m,R}&0\\
0&B_-\mathcal R^-_{m,R}&0
\end{pmatrix}.
\tag{13}
\]

De (12),

\[
\mathcal C_R^{\rm tail}J_{+,R}f=J_{-,R}f
\quad\hbox{para todo }f\in\mathcal D_R.
\tag{14}
\]

Esta acción contiene las filas escalar, primo–potencia y polar, con sus constantes y orientaciones intactas. Para cualquier par \(f,g\),

\[
\begin{aligned}
\langle\mathcal C_R^{\rm tail}J_+f,\mathcal C_R^{\rm tail}J_+g\rangle
={}&\left(-c_\Gamma+2\sum_{\ell\le R}w_\ell\right)\langle f,g\rangle\\
&+b_-(f)\overline{b_-(g)}.
\end{aligned}
\tag{15}
\]

Para \(f=\sum_i f_i\), \(g=\sum_j g_j\), el miembro derecho contiene la suma completa en \(i,j\); no se han reemplazado las pruebas por celdas ortogonales. Los cruces primo–gamma de (7) se conservan al cambiar las representaciones de entrada. La forma final es

\[
J_+^*\left(I-(\mathcal C_R^{\rm tail})^*\mathcal C_R^{\rm tail}\right)J_+
=J_+^*J_+-J_-^*J_-=\mathcal W_R.
\tag{16}
\]

Es una igualdad efectiva de formas, sin suponer todavía que el operador entre paréntesis sea positivo. El operador es acotado; una cota explícita es

\[
\|\mathcal C_R^{\rm tail}\|
\le\nu_R^{-1/2}
\sqrt{-c_\Gamma+2\sum_{\ell\le R}w_\ell+2\sinh(R/2)-R}.
\]

La cota fija el tipo, no prueba norma menor o igual que uno.

## 9. Condición exacta para reunir ambos momentos en una expectativa

Sea \(\mathcal M_+=\overline{J_+\mathcal D_R}\). La transferencia alcanzable

\[
C_{\rm rea}(J_+f)=J_-f
\]

está bien definida porque la cola gamma prueba que \(J_+\) es inyectivo. Es la restricción de (13), luego es acotada. Cualquier otra transferencia acotada que dé las mismas salidas coincide con ella sobre \(\mathcal M_+\).

Un cambio de coordenadas no proporciona una transferencia alcanzable diferente. El dato por establecer para que (13) tenga una dilatación isométrica con la expectativa nativa es

\[
\|C_{\rm rea}x\|\le\|x\|,
\qquad x\in\mathcal M_+.
\tag{17}
\]

Su relación con los dos momentos puede escribirse sin ambigüedad. **Si** (17) se demuestra desde los operadores nativos, \(D=(I-C_{\rm rea}^*C_{\rm rea})^{1/2}\) existe y

\[
\mathfrak C_{\rm dil}f
=u_9\otimes(J_-f,0)+\eta_9\otimes(0,DJ_+f)
\tag{18}
\]

satisface, para \(P=|u_9\rangle\langle u_9|\otimes I\),

\[
\mathfrak C_{\rm dil}^*\mathfrak C_{\rm dil}=J_+^*J_+,\qquad
\mathfrak C_{\rm dil}^*P\mathfrak C_{\rm dil}=J_-^*J_-.
\]

(18) es una forma normal de la dilatación una vez probado (17), **no** una nueva prueba prospectiva de (17). Permite identificar exactamente qué debe producir la coligación nativa: el defecto de esa transferencia común, con todos sus cruces, y no sólo el defecto de cada reloj por separado.

La tarea siguiente concreta consiste en componer el presupuesto energético del conector completo con las identidades locales y de refinamiento recuperadas. Si una coligación nativa alternativa realiza (14) y es contractiva sobre todo \(\mathcal M_+\), por unicidad alcanzable prueba (17). No hace falta inventar otro lector; sí calcular su acción y su energía común.

## 10. Controles y procedencia

- Las acciones (1), (7), (8), (12)–(16) reúnen resultados y operadores preexistentes. Estatuto: **RESULTADO_RECUPERADO / FORMALIZACIÓN_REUNIDA**.
- Las composiciones explícitas (2)–(6) y el control (10) son cálculos de este corte sobre esas fórmulas; no se les atribuye prioridad matemática ni se los presenta como ausencia global de otros operadores. Procedencia exhaustiva de la forma exacta de esos cálculos: no investigada.
- Se ejecutaron 25 controles racionales sobre las coordenadas sin normalizar \(v_{9N}=9Ne_0-\mathbf1\), para \(N=2,3,9,81,729\). Verificaron la acción del promedio, la fracción \((N-1)/(9N-1)\), la media nula, la ortogonalidad del detalle y la fracción complementaria \(8N/(9N-1)\). Se conservaron en el [script reproducible](</Users/ruben/Documents/New project/output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911/verificar_expectativa_modos.py>), sin uso de aserciones eliminables. Pasaron los mismos 25 controles en modo normal y los 25 en modo optimizado: [recibo normal](</Users/ruben/Documents/New project/output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911/CONTROL_EXPECTATIVA_MODOS_NORMAL.json>) y [recibo optimizado](</Users/ruben/Documents/New project/output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911/CONTROL_EXPECTATIVA_MODOS_OPTIMIZADO.json>). Son controles de (2)–(4), no de positividad global.
- Pasaron el núcleo formal permanente, la autocomprobación causal de constantes, el comprobador del resolutor y la puerta de principios operativos. El resolutor conserva la referencia histórica de 2.084 páginas; este corte respeta la selección autoral de 2.249 y no modifica ese registro.
- No se han alterado PDFs, índices, fuentes propietarias, paquetes entregados ni las comprobaciones del doble círculo ya conservadas por la tarea principal.

Para repetir los controles desde esta carpeta:

    python3 -I -S verificar_expectativa_modos.py --receipt CONTROL_EXPECTATIVA_MODOS_NORMAL.json
    python3 -I -S -O verificar_expectativa_modos.py --receipt CONTROL_EXPECTATIVA_MODOS_OPTIMIZADO.json

**Conclusión operacional:** el estado y los dos lectores no han desaparecido. El cálculo recupera su acción y demuestra exactamente la diferencia entre transporte isométrico de modos, expectativa uniforme y recuperación analítica de canales. La segunda identidad de P10 tiene una vía concreta de comprobación mediante el conector común; la conjugación de cartas, por sí sola, no realiza esa comprobación.
