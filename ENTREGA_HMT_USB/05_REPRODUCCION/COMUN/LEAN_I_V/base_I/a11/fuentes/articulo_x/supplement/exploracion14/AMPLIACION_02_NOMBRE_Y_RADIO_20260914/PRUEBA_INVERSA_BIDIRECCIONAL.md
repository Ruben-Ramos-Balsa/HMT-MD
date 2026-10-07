# Prueba inversa, orientación ternaria y memoria bilateral completa

14 de septiembre de 2026. Ampliación focal autorizada: se utiliza la salida previa 10⁴α_A como **diagnóstico inverso posterior**, sin convertirla en entrada generadora, seleccionar un estado para obtenerla o modificar a=8. Los documentos anteriores, el paper de 326 páginas y sus fuentes permanecen intactos.

## 1. Propietarios, objeto y corte causal

Se parte del registro K generado y de sus lectores ya construidos, no de un vector elegido a partir de α. Los propietarios inmediatos son:

- [Registro e integralidad](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_k.tex:213>), líneas 213–296 y 322–375; [imagen, carga y eventos](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_imagen_integral.tex:17>), líneas 17–85 y 203–263.
- [Lectores 3/4 y reconstrucción](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/11.tex:7>), líneas 7–44 y 118–183.
- [Memoria completa no estacionaria](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/10.tex:140>), líneas 140–203: balance, terminal positivo, isometría y su inversa adjunta.
- [Transporte en la imagen incidencial](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/05.tex:26>), líneas 26–58: conservación de adjuntos y normas, covariancia y dominio exacto de la imagen.
- [Lectura ternaria completa](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_02_NOMBRE_Y_RADIO_20260914/LECTURA_TERNARIA_COMPLETA.md:7>), §§1–4: U=S⁴, P₀ de rango cuatro, seis objetos ya construidos, balance de todos los canales e intervalo de α_A.
- [Norma trítica y contraste](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_02_NOMBRE_Y_RADIO_20260914/CONSTANTE_Y_NORMA_TRITICA.md:90>), §§4–5; [radio generalizado](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_02_NOMBRE_Y_RADIO_20260914/RADIO_GENERALIZADO.md:50>), §§2–7: composiciones posteriores y parámetro algebraico a>0.

La genealogía se conserva en nueve campos: (1) APP y sus hojas, residuos y cocientes; (2) TRIT, régimen, orientación y acarreo; (3) TPK, estado enriquecido, ventanas y extracción hacia K; (4) coeficiente canónico 8 de la partición 8+1 y factor 3 de la órbita ternaria; (5) carga, orden y memoria diferenciados de perturbaciones de lectura; (6) corte en la publicación entera y su realización, no reconstrucción de toda la historia; (7) operadores y lecturas adicionales deducidos abajo; (8) comparación posterior con α_A, explícitamente diagnóstica; (9) propietarios anteriores y pruebas contiguas. El parámetro a sólo generaliza una familia algebraica posterior; no recibe un valor ajustado a α.

En H=R¹², con la métrica euclídea de la carta declarada, sean

\[
U=S^4,\quad U^3=I,\quad U^*=U^{-1}=U^2,\qquad
P_0=\frac{I+U+U^2}{3},\quad P_\perp=I-P_0.
\tag{1}
\]

P₀ proyecta sobre Fix(U), de dimensión cuatro; P⊥ tiene dimensión ocho. No son el proyector P₁₁ que elimina la media global ni el proyector isótipo P₃. Se escribe

\[
Q_{-,a}=aI-U,\qquad Q_{+,a}=(a+1)I+U,
\qquad p(a)=a^2+a+1,\quad a>0.
\tag{2}
\]

Q₋,ₐ es el operador llamado L en la nota ternaria. Esta notación evita confundirlo con la inversa de mínimos cuadrados L_a de RADIO_GENERALIZADO.md.

## 2. El Gram y el origen de 24

**Proposición 1.** Para todo a>0,

\[
\boxed{Q_{-,a}^*Q_{-,a}
=(a-1)^2P_0+p(a)P_\perp
=p(a)I-3aP_0.}
\tag{3}
\]

**Prueba.** Expandir el producto da (a²+1)I−a(U+U²). Como U+U²=3P₀−I, el resultado es p(a)I−3aP₀. La diferencia entre los dos coeficientes espectrales es

\[
p(a)-(a-1)^2=3a.
\]

Las propiedades de proyección ortogonal de P₀ se deducen de U³=I y U*=U². ∎

Para v≠0,

\[
w(v)=\frac{\|P_0v\|^2}{\|v\|^2},\qquad
s_{-,a}(v)=\frac{\|Q_{-,a}v\|^2}{\|v\|^2}
=p(a)-3a w(v).
\tag{4}
\]

En a=8, p=73 y 3a=24, de modo que s₋=73−24w. **El origen de 24 en esta identidad es 3×8**: 3 procede de la suma de los tres elementos del ciclo que define P₀, y 8 del coeficiente del lector. La igualdad numérica 24=2×12 no es la derivación de ese coeficiente.

Esto se distingue sin apelar a una ausencia documental: la misma identidad tiene coeficiente 24 sobre un solo ciclo de tres posiciones y sobre cualquier suma de m ciclos ternarios. Cambiar el número de copias cambia los rangos y las multiplicidades, pero no 3a. Para m ciclos,

\[
\operatorname{rank}P_0=m,\quad \dim H=3m,\qquad
\operatorname{tr}(Q_{-,a}^*Q_{-,a})=3m(a^2+1).
\]

En el caso m=4, a=8, el término de corrección de la traza es 24·4=96 y la traza total es 12·65=780. Aquí se ve exactamente dónde entra la dimensión doce: en la multiplicidad, no en la formación del salto espectral 24.

## 3. Tres operaciones distintas de inversión o cambio de marco

### 3.1. Invertir la orientación U→U⁻¹

Al sustituir U por U⁻¹, P₀ permanece idéntico porque I+U+U² no cambia. Además,

\[
Q_{-,a}(U^{-1})=Q_{-,a}(U)^*,\qquad
Q_{+,a}(U^{-1})=Q_{+,a}(U)^*.
\tag{5}
\]

Ambos operadores son normales, por ser polinomios del unitario U. Por tanto sus Grams, valores singulares, determinantes y lecturas s sobre un mismo v permanecen iguales. También se conservan las distancias entre sus imágenes de dos vectores cualesquiera. Se invierte la orientación dentro del sector ternario, no su escala de semejanza.

Esta operación **no** equivale a sustituir Q₋ por Q₋⁻¹. Para a≠1,

\[
Q_{-,a}^{-1}
=\frac1{a-1}P_0+\frac1{p(a)}Q_{+,a}P_\perp.
\tag{6}
\]

Sobre P⊥, Q₊ es el adjunto de Q₋ y p veces su inversa; sobre el sector fijo esa identificación debe corregirse. En a=1, Q₋ anula Fix(U) y no tiene inversa en todo H.

### 3.2. Conjugación con métrica y estado transportados

Sea R:H→H' invertible. Transportamos simultáneamente

\[
v'=Rv,\quad U'=RUR^{-1},\quad P'_0=RP_0R^{-1},
\quad Q'_{\pm,a}=RQ_{\pm,a}R^{-1},\qquad
G'=(R^{-1})^*R^{-1}.
\tag{7}
\]

El producto en H' es ⟨x,y⟩_{G'}=⟨R⁻¹x,R⁻¹y⟩. Con ese adjunto, U' es unitario, P'₀ es una proyección ortogonal y

\[
(Q'_{-,a})^{\dagger}Q'_{-,a}
=p(a)I-3aP'_0,\qquad
w_{G'}(Rv)=w(v),\quad s'_{-,a}(Rv)=s_{-,a}(v).
\tag{8}
\]

**Prueba.** El adjunto transportado de RAR⁻¹ es RA*R⁻¹. Aplicarlo a (3) prueba la primera igualdad; R es isométrico entre las dos métricas declaradas, lo que prueba las razones de normas. ∎

No se exige [R,U]=0. Si R es ortogonal se puede conservar la matriz I de la métrica. Si R no es ortogonal pero se mantiene artificialmente la norma euclídea anterior, se ha cambiado la lectura métrica; ya no se está efectuando sólo el cambio de marco (7).

### 3.3. Cambiar sólo el vector en una carta fija

Para un R ortogonal, manteniendo U y P₀ fijos,

\[
s_{-,a}(Rv)=s_{-,a}(v)\text{ para todo }v
\quad\Longleftrightarrow\quad R^*P_0R=P_0.
\tag{9}
\]

La equivalencia sigue de (4) y la igualdad de formas cuadráticas. El grupo de esta invariancia escalar es O(Fix U)×O(P⊥H), es decir O(4)×O(8) en esta realización. Puede ser mayor que el grupo que conmuta con U: conservar el Gram no obliga a conservar cada orientación del operador.

Fuera de esas órbitas el peso puede variar. Por ejemplo, para un filtro posterior R=c₀P₀+c₁P⊥,

\[
w(Rv)=\frac{|c_0|^2w(v)}{|c_0|^2w(v)+|c_1|^2[1-w(v)]},
\tag{10}
\]

cuando el denominador es positivo. Aunque R conmute con U, un cambio desigual de las dos normas cambia s. Se trata de una operación sobre el vector, no de una conjugación isométrica. En el espacio real libre, todos los pesos entre 0 y 1 son realizables; el conjunto de publicaciones HMT admitidas sigue determinado por su genealogía propia, no por esa parametrización libre.

## 4. Socio bilateral, balance exacto e imagen computable

**Teorema 2.** Los dos operadores de (2) satisfacen, para todo a>0,

\[
\begin{aligned}
Q_{+,a}-Q_{-,a}^*&=3P_0,\\
Q_{+,a}Q_{-,a}=Q_{-,a}Q_{+,a}&=p(a)I-3P_0,\\
Q_{+,a}^*Q_{+,a}&=p(a)I+3(a+1)P_0.
\end{aligned}
\]

\[
\boxed{(a+1)Q_{-,a}^*Q_{-,a}+aQ_{+,a}^*Q_{+,a}
=(2a+1)p(a)I.}
\tag{11}
\]

**Prueba.** La primera igualdad es I+U+U²=3P₀. La segunda resulta de a(a+1)I−U−U². La tercera se obtiene expandiendo el Gram de (a+1)I+U. En la última, los términos de P₀ son −3a(a+1) y +3a(a+1), por lo que se cancelan exactamente. ∎

En a=8,

\[
Q_-=8I-U,\quad Q_+=9I+U,\qquad
9Q_-^*Q_-+8Q_+^*Q_+=17\cdot73 I=1241I.
\tag{12}
\]

En el modo fijo los Grams son 49 y 100; en el complemento son ambos 73. Así, 9·49+8·100=1241 y 9·73+8·73=1241: el balance incluye el modo fijo, no sólo el módulo de aumento.

### Isometría bilateral y reconstrucción

La aplicación

\[
\boxed{W_a v=
\frac1{\sqrt{(2a+1)p(a)}}
\bigl(\sqrt{a+1}\,Q_{-,a}v,\sqrt a\,Q_{+,a}v\bigr)}
\tag{13}
\]

es isométrica, pues Wₐ*Wₐ=I por (11). Su inversa sobre la imagen es Wₐ*. Con errores aditivos en esos canales normalizados, aplicar Wₐ* no aumenta la norma del error.

Si se almacenan los canales sin normalizar x=Q₋,ₐv e y=Q₊,ₐv, se tiene la reconstrucción particularmente simple

\[
\boxed{v=\frac{x+y}{2a+1},\qquad
Uv=\frac{a y-(a+1)x}{2a+1}.}
\tag{14}
\]

Provienen de Q₋,ₐ+Q₊,ₐ=(2a+1)I. La fórmula es válida incluso en a=1, aunque Q₋ por separado sea singular. En los canales sin normalizar, la inversa por suma tiene norma √2/(2a+1); esta es otra normalización de ruido, distinta de la de Wₐ.

La imagen se caracteriza exactamente, sin recibir v:

\[
\boxed{(x,y)\text{ es una pareja compatible}
\quad\Longleftrightarrow\quad Q_{+,a}x=Q_{-,a}y.}
\tag{15}
\]

**Prueba.** La necesidad usa la conmutación de Q₋ y Q₊. Para la suficiencia, definir v=(x+y)/(2a+1). Entonces

\[
Q_{-,a}v-x
=\frac{Q_{-,a}y-Q_{+,a}x}{2a+1}=0,
\]

y análogamente Q₊,ₐv=y. ∎

El residuo Q₊x−Q₋y es así un control exacto de compatibilidad. Este control no genera el registro ni selecciona una historia; caracteriza la imagen de la composición posterior. Wₐ es una nueva isometría explícita de dos canales en este expediente, no una identificación automática con toda la evolución TPK o con el acoplamiento previo de compresión nonádica.

Las lecturas de cada socio obedecen

\[
s_{+,a}(v)=p(a)+3(a+1)w(v),\qquad
(a+1)s_{-,a}(v)+a s_{+,a}(v)=(2a+1)p(a).
\tag{16}
\]

Un déficit respecto de p en el primer canal tiene un exceso complementario determinado en el segundo. No es una corrección desconocida de 73, sino un balance bilateral con coeficientes exactos.

## 5. Qué conserva la memoria completa V

Sea V:H→Y una isometría completa del manuscrito, incluyendo el terminal cuando no se agota. Escribamos M=im V y Π_M=VV*. Sobre M se transportan

\[
U^V=VUV^*,\quad P_0^V=VP_0V^*,\quad
Q_{-,a}^V=VQ_{-,a}V^*.
\]

La identidad de M es Π_M, no la identidad de todo Y. Por ello

\[
(U^V)^3=\Pi_M,\qquad
(Q_{-,a}^V)^*Q_{-,a}^V
=p(a)\Pi_M-3aP_0^V,
\tag{17}
\]

y para todo v≠0,

\[
\|Vv\|=\|v\|,\qquad
\|P_0^VVv\|=\|P_0v\|,\qquad
\|Q_{-,a}^VVv\|=\|Q_{-,a}v\|.
\tag{18}
\]

Así la memoria completa conserva w y s exactamente con el operador transportado. La demostración sólo usa V*V=I y no exige una conmutación ficticia de operadores que actúen en dominios distintos.

En el caso V₂v=(T₄T₃v,D₃v,D₄T₃v), sus tres canales son polinomios en S y sí entrelazan U con tres copias de U. Entonces P₀ y Q₋ pueden leerse diagonalmente en cada canal, y

\[
s_{-,a}(V_2v)
=\frac{\sum_j\|v_j\|^2s_{-,a}(v_j)}{\sum_j\|v_j\|^2}
=s_{-,a}(v).
\tag{19}
\]

Se omiten sólo canales nulos. No es una media sin pesos. La misma propiedad se aplica a Wₐ porque sus canales son polinomios de U. Por tanto el par bilateral conserva la lectura inicial si se evalúan todos sus canales con el observable transportado; sus lecturas individuales no deben confundirse con la lectura de la totalidad.

Si se selecciona un solo canal, se descarta un terminal no nulo o se aplica un filtro no isométrico, s puede cambiar. Son operaciones efectivas de lectura o selección, no formas alternativas de escribir el mismo balance completo. La segunda memoria D₄T₃v, cuando es no nula, tiene P₀D₄T₃v=0 y s₋,₈=73 exactamente.

## 6. Extensión efectiva: iteraciones y ley escalar cerrada

Cambiar de orientación o guardar la memoria completa no cambia w; aplicar otra vez Q₋ al vector sí puede cambiarlo. Esta distinción da un ensayo inverso de toda una familia, no sólo de objetos aislados.

Sea b=(a−1)², p=a²+a+1. Para v=f+g, con f=P₀v y g=P⊥v, (3) y la conmutación dan

\[
\|Q_{-,a}^n f\|^2=b^n\|f\|^2,\qquad
\|Q_{-,a}^n g\|^2=p^n\|g\|^2.
\]

Si a≠1 y 0<w₀<1, para todo entero n≥0,

\[
\boxed{w_n:=w(Q_{-,a}^n v)
=\frac{b^n w_0}{b^n w_0+p^n(1-w_0)},\qquad
\frac{w_n}{1-w_n}=\left(\frac bp\right)^n\frac{w_0}{1-w_0}.}
\tag{20}
\]

Como 0<b/p<1, w_n disminuye estrictamente a cero, y s_n=p−3aw_n aumenta estrictamente a p. En a=1, el sector fijo se anula en el primer paso; si g≠0, s_n=p=3 desde n=1. Si g=0, Q₋v=0 y ya no se define la razón s para el vector anulado.

Para a≠1, la evolución de s sola cierra exactamente:

\[
\boxed{s_{n+1}=p+b-\frac{bp}{s_n},\qquad
s_{n+1}-s_n=\frac{(s_n-b)(p-s_n)}{s_n}>0.}
\tag{21}
\]

La identidad resulta de dividir b²w+p²(1−w) por bw+p(1−w). Si se aplica Q₋⁻¹ en lugar de Q₋, el paso inverso es s_prev=bp/(p+b−s); el peso fijo aumenta y s disminuye. Si se invierte solamente U, Q₋ pasa a su adjunto y la sucesión de pesos y lecturas es exactamente la misma, no la sucesión inversa.

Para el socio Q₊, el factor de ganancia fija es c=(a+2)²>p. En consecuencia,

\[
\frac{w(Q_{+,a}^n v)}{1-w(Q_{+,a}^n v)}
=\left(\frac cp\right)^n\frac{w_0}{1-w_0},
\tag{22}
\]

y la lectura s₋ de esos vectores disminuye estrictamente. La ecuación (22) no identifica Q₊ con Q₋⁻¹; precisa la variación del peso para otro filtro explícito.

Estas iteraciones son composiciones posteriores de un lector fijado. No se presentan como nuevas trayectorias temporales HMT por mera pertenencia a H ni como una dinámica física seleccionada mediante α.

## 7. Ensayo inverso exacto para todas las iteraciones enteras del caso canónico

Se fija a=8. Por tanto b=49, p=73 y el cociente que gobierna los pesos es 49/73. El intervalo de la salida α_A, tomado del prefijo completo con su acarreo en la nota propietaria, implica

\[
\ell:=72.97352569283800997285105472380662
<10^4\alpha_A<
h:=72.97352569283800997285105472380663.
\tag{23}
\]

Los extremos son racionales exactos escritos en decimal finito, no sustitutos de la salida completa. La condición inversa s₋,₈(v)=10⁴α_A requiere

\[
w(v)=w_*:=\frac{73-10^4\alpha_A}{24},\qquad
w_L<w_*<w_H,
\tag{24}
\]

con

\[
\begin{aligned}
w_L&=\frac{73-h}{24}
=\frac{2647430716199002714894527619337}
{2400000000000000000000000000000000},\\
w_H&=\frac{73-\ell}{24}
=\frac{441238452699833785815754603223}
{400000000000000000000000000000000}.
\end{aligned}
\tag{25}
\]

Se reciben de los lectores anteriores, sin ajustar sus componentes,

\[
w(K)=\frac{10684363}{12753771},\qquad
w(P_{11}K)=\frac{3512283}{11789915},\qquad
w(D_3K)=\frac{1052377}{2890011}.
\tag{26}
\]

Escribiendo w₀=A/(A+B), toda la sucesión queda determinada exactamente por

\[
w_n=\frac{A49^n}{A49^n+B73^n},\qquad
s_n=73-24\frac{A49^n}{A49^n+B73^n}.
\tag{27}
\]

Los cruces exactos son:

| Entrada | A | B | n | Desigualdad exacta |
|---|---:|---:|---:|---|
| K | 10684363 | 2069408 | 21 | \(w_{21}>w_H>w_L>w_{22}\) |
| P₁₁K | 3512283 | 8277632 | 14 | \(w_{14}>w_H>w_L>w_{15}\) |
| D₃K | 1052377 | 1837634 | 15 | \(w_{15}>w_H>w_L>w_{16}\) |

Cada desigualdad se comprobó mediante productos cruzados de enteros usando Fraction, con las expresiones (25)–(27). Para facilitar la lectura, las respuestas a ambos lados son aproximadamente:

| Entrada | Respuesta anterior al cruce | Respuesta posterior al cruce |
|---|---:|---:|
| K | s₂₁≈72.97136264842803 | s₂₂≈72.98077012438719 |
| P₁₁K | s₁₄≈72.96167997982852 | s₁₅≈72.97426483341773 |
| D₃K | s₁₅≈72.96527892867391 | s₁₆≈72.97668298511348 |

Las fórmulas (25)–(27), no esos redondeos, son los valores utilizados en la comparación.

**Teorema 3. Cierre de las tres familias.** Para cada una de las entradas K, P₁₁K y D₃K y para todo entero n≥0,

\[
s_{-,8}(Q_{-,8}^n v)\ne10^4\alpha_A.
\tag{28}
\]

**Prueba.** Por (20), w_n es estrictamente decreciente. Para n hasta el índice izquierdo de su fila, w_n≥w_left>w_H; para n desde el índice derecho, w_n≤w_right<w_L. No hay otro entero entre índices consecutivos. Por tanto ningún w_n pertenece al intervalo que contiene w_*, y (4) prueba (28). La cobertura de todos los enteros proviene de la monotonía y el único cruce, no de haber muestreado una cantidad finita de pasos. ∎

La orientación U⁻¹ da las mismas sucesiones y el mismo cierre. La familia Q₊,₈ⁿv tampoco alcanza el objetivo: por (22), s₋ disminuye desde su valor inicial, que es menor que 72, mientras que el objetivo es mayor que 72. Las potencias inversas Q₋,₈⁻ⁿ tienen la misma exclusión por monotonía descendente de s₋. Finalmente, D₄T₃K tiene w₀=0; sus iteraciones por ambos socios permanecen en el complemento ternario y su lectura es exactamente 73.

El resultado no se extiende por esta prueba a cualquier producto mixto o a todo el corpus. Por ejemplo, para un producto declarado Q₋ⁿQ₊ᵐ, los operadores conmutan y el peso obedecería la condición exacta

\[
\frac{w_{n,m}}{1-w_{n,m}}
=\left(\frac{49}{73}\right)^n
\left(\frac{100}{73}\right)^m\frac{w_0}{1-w_0}.
\tag{29}
\]

Esta es una clase matemática distinta, con dos índices. (29) describe su acción sin seleccionar índices para afirmar α ni convertir el cierre de (28) en un dictamen global.

## 8. Resultado positivo del diagnóstico y alcance

La prueba inversa distingue operaciones que el lenguaje de «dar la vuelta» podría confundir:

- Invertir U conserva exactamente la escala, el peso y la lectura.
- Conjugar transportando métrica, estado y lector conserva lo mismo.
- Guardar toda la memoria con sus pesos y su operador transportado conserva lo mismo.
- Seleccionar un canal o volver a aplicar un lector no isométrico puede cambiar s; las leyes (20)–(22) cuantifican ese cambio.
- El par bilateral nuevo conserva una norma completa, caracteriza su imagen por (15) y reconstruye el estado por (14), incluso donde un canal aislado deja de ser invertible.

La relación con α utilizada aquí es un ensayo inverso legítimo y separado de la generación. Identifica qué peso exigiría una igualdad y permite probar, para familias efectivamente especificadas, si el recorrido lo alcanza. En las tres familias de (28) no hay coincidencia; el cierre conserva su alcance exacto. No se rebaja ni se reabre la generación anterior de α, K, la incidencia o las dimensiones algebraicas.

Los nuevos resultados reunidos en esta nota son la clasificación de invariancias de la lectura, el balance bilateral con su isometría e imagen, la recurrencia escalar y el cierre infinito de las familias ensayadas. Se presentan como formalizaciones y consecuencias adicionales del expediente, no como una identificación de toda la dinámica TPK con estos lectores posteriores. Los controles exactos se realizaron sin modificar scripts o recibos existentes; la prueba sustantiva permanece contigua en el texto.
