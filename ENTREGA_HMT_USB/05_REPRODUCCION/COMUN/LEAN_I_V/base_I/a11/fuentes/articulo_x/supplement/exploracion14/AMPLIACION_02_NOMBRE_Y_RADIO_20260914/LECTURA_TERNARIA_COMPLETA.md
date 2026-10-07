# Lectura ternaria del registro, sus proyecciones y la memoria completa

14 de septiembre de 2026. Cálculo focal exacto de los objetos ya utilizados en el manuscrito; no se seleccionan estados nuevos ni se ajustan componentes mediante alfa.

## 1. Operador sobre las doce posiciones

Se recibe K de su producción APP–TRIT–TPK conservada en el manuscrito. En la carta lineal posterior `H=R^12`, con producto euclídeo, se usa el desplazamiento ya definido `Sx_i=x_(i+1)`, índices módulo doce. El lector de esta nota es

\[
 U=S^4,\qquad U^3=I,\qquad
 P_0=\frac{I+U+U^2}{3},\qquad L=8I-U.
\tag{1}
\]

Se escribe L en lugar de H para distinguir el operador del espacio. El símbolo `P0` de esta nota es el proyector sobre los vectores fijos de U, de rango cuatro. No es `P11`, que elimina únicamente el modo uniforme y tiene rango once; tampoco es el proyector isótipo `P3`.

El valor ocho proviene del contraste colectivo `8+1` de las nueve posiciones que fija los acoplamientos del manuscrito. La presente operación `8I-U`, con su signo y su carta, se estudia como lector posterior concreto. No se la identifica con toda la dinámica TPK por el hecho de usar sus operadores de fase.

**Proposición 1.** Se cumple

\[
 \boxed{L^*L=49P_0+73(I-P_0)=73I-24P_0.}
\tag{2}
\]

**Prueba.** Como `U*=U^-1=U²`, se tiene `L*L=65I-8(U+U²)`. Sustituir `U+U²=3P0-I` da (2). Las identidades `P0²=P0=P0*` proceden de `U³=I`. La realización contiene cuatro ciclos de longitud tres, por lo que el sector fijo tiene dimensión cuatro y su complemento dimensión ocho.

Para todo vector no nulo v definimos

\[
 w(v)=\frac{\|P_0v\|^2}{\|v\|^2},\qquad
 s(v)=\frac{\|Lv\|^2}{\|v\|^2}.
\]

Entonces

\[
 \boxed{s(v)=73-24w(v),\qquad 49\le s(v)\le73.}
\tag{3}
\]

El número 73 permanece exacto en el complemento ternario. La razón dependiente del estado de (3) es otra magnitud; no reemplaza un determinante por una aproximación. Sobre cada par real correspondiente a las raíces cúbicas no triviales, `det(8I-U)=73`. Sobre todo el portador de doce posiciones,

\[
 \det(8I-U)=(8^3-1)^4=7^4\,73^4=68184176641.
\]

El sector fijo contribuye `7^4`; el complemento de dimensión ocho contribuye `73^4`. Esta distinción conserva la multiplicidad y el dominio del índice 73.

## 2. Objetos evaluados y valores exactos

Se utiliza exclusivamente el registro documentado

\[
 K=(234,543,140,729,659,824,621,58,914,794,146,601),
 \qquad \mathbf1^*K=6263.
\]

Las otras cinco entradas del ensayo son salidas de lectores ya definidos:

\[
 k=\Pi K,\quad\Pi=P_{11}=I-\mathbf1\mathbf1^*/12,
\]

\[
 m_0=D_3K,\qquad m_1=D_4T_3K,
 \quad T_j=(8I+S^j)/9,\quad D_j=\sqrt8(S^j-I)/9,
\]

\[
 u=P_3\Pi K,\qquad Q_K=P_{10}(K),\qquad q=Q_KK=k-u.
\]

El proyector `P3` es exactamente el de la representación `A5/C5`, con carácter y representantes especificados en el [propietario de la dirección](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/k_direccion_dimensional.tex:12>). Todas las evaluaciones se efectúan en esa carta fija. En particular, no se modifica P3 para acercar una lectura a alfa.

La siguiente tabla contiene las normas exactas, antes de dividir. Con `a=||v||²` y `b=||P0v||²`, **las respuestas exactas son `w=b/a` y `s=(73a-24b)/a`**.

| Objeto v | a | b |
|---|---:|---:|
| K | `4251257` | `10684363/3` |
| `Pi K` | `11789915/12` | `1170761/4` |
| `D3 K` | `15413392/81` | `16838032/243` |
| `D4 T3 K` | `1105759232/6561` | `0` |
| u | `1327717/4 + (568896/5)sqrt(5)` | `3029657/20 + (145120/3)sqrt(5)` |
| `P10(K) K` | `1951691/3 − (568896/5)sqrt(5)` | `2292404/15 − (145120/3)sqrt(5)` |

En las dos memorias se ha incorporado el factor ocho de la norma de `sqrt(8)`; no se comparan sus versiones racionalizadas como si fueran energías originales.

Para las cuatro filas racionales se obtiene

\[
\begin{array}{c|c|c}
v&w(v)&s(v)\\\hline
K&10684363/12753771&224866857/4251257\\
\Pi K&3512283/11789915&776369003/11789915\\
D_3K&1052377/2890011&61904585/963337\\
D_4T_3K&0&73.
\end{array}
\tag{4}
\]

En las dos filas cuadráticas, la tabla de a y b constituye una expresión exacta en `Q(sqrt(5))` de ambas respuestas, sin redondeo. Sus evaluaciones decimales, sólo para lectura, son:

| Objeto v | w(v), aproximado | s(v), aproximado |
|---|---:|---:|
| K | 0.8377414805393636 | 52.89420446705527 |
| `Pi K` | 0.2979057100920575 | 65.85026295779062 |
| `D3 K` | 0.3641429046463837 | 64.26057028848679 |
| `D4 T3 K` | 0 | 73 |
| u | 0.4428244530591254 | 62.37221312658099 |
| `P10(K) K` | 0.1127385160275117 | 70.29427561533972 |

**El valor 73 de la segunda memoria está forzado.** La identidad `P0(U-I)=0` da

\[
 P_0D_4T_3K=0.
\tag{5}
\]

Su norma positiva en la tabla garantiza que es un vector no nulo. Por (2), su razón s es exactamente 73. Esto no depende de seleccionar una aproximación decimal.

## 3. Recorrido del registro completo: terminal y ambas memorias

La composición estudiada archiva los dos complementos por separado y conserva el terminal

\[
 t=T_4T_3K,\qquad V_2K=(t,m_0,m_1).
\]

Su identidad previa es `V2*V2=I`. Los tres operadores de canal `T4T3`, `D3`, `D4T3` son polinomios en S. Por tanto conmutan con U, P0 y L, y

\[
 V_2P_0=(P_0\oplus P_0\oplus P_0)V_2,
 \qquad V_2L=(L\oplus L\oplus L)V_2.
\tag{6}
\]

**Proposición 2.** Para todo v, incluidos K, k, u y q, se conservan exactamente

\[
 \|v\|^2=\|T_4T_3v\|^2+\|D_3v\|^2+\|D_4T_3v\|^2,
\]

\[
 \|P_0v\|^2=\|P_0T_4T_3v\|^2+\|P_0D_3v\|^2,
\]

\[
 \|Lv\|^2=\|LT_4T_3v\|^2+\|LD_3v\|^2+\|LD_4T_3v\|^2.
\tag{7}
\]

**Prueba.** Aplicar la isometría a v, P0v y Lv, y utilizar (6). La contribución de P0 en el segundo complemento es cero por (5), para todo v. No se necesita que v sea eigenvector de los lectores, ni que P3 conmute con ellos.

Así el peso del registro completo, calculado con el proyector transportado de (6), es

\[
 w(V_2v)=
 \frac{\sum_a\|v_a\|^2 w(v_a)}{\sum_a\|v_a\|^2}=w(v),
 \qquad s(V_2v)=s(v),
\tag{8}
\]

omitiendo de la expresión los canales nulos. Los valores de canales aislados se combinan con sus normas, no por una media aritmética sin pesos.

Para K, el terminal efectivo tiene

\[
 \|t\|^2=\frac{25538253193}{6561},\qquad
 \|P_0t\|^2=\frac{848595371}{243},
\]

\[
 w(t)=\frac{22912075017}{25538253193},\qquad
 s(t)=\frac{1314402682681}{25538253193}
 \simeq51.46799480558349.
\tag{9}
\]

La suma de las tres normas es `4251257`. La suma de las normas fijas es

\[
 \frac{848595371+16838032}{243}
 =\frac{10684363}{3}.
\]

Por ello la lectura completa vuelve a `s(K)=52.89420446705527...`, aunque el segundo complemento por separado dé 73. En la entrada centrada, las memorias no cambian porque ambas anulan el modo uniforme. Cambia el terminal a `T4T3 Pi K`, con

\[
 \|T_4T_3\Pi K\|^2=\frac{16367568169}{26244},\qquad
 \|P_0T_4T_3\Pi K\|^2=\frac{217142795}{972},
\]

y las sumas recuperan exactamente `11789915/12` y `1170761/4`. De nuevo, el registro completo conserva `s(Pi K)`.

La prueba se prolonga a una sucesión de lectores que conmutan con U y a la isometría completa de su límite, incluyendo el terminal positivo `A_infty^(1/2)`. Si los lectores no conmutan, el operador transportado es `V P0 V*` sobre la imagen; no se sustituye automáticamente por la suma diagonal de copias de P0.

## 4. Comparación posterior con la salida alfa

La [normalización completa de alfa](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/alpha.tex:265>) conserva el prefijo compatible

\[
 (007,297,352,569,283,800,997,285,105,472,380,662,999,\ldots).
\]

Se distingue de la ventana de frontera cero, que termina en 663. Del prefijo de la sección completa, usando que los bloques posteriores pertenecen a `0,...,999`, se obtiene el intervalo heredado

\[
 \frac{7297352569283800997285105472380662}{10^{36}}
 <\alpha_A<
 \frac{7297352569283800997285105472380663}{10^{36}}.
\tag{10}
\]

La desigualdad inferior es estricta por el siguiente bloque 999; la superior es estricta por la convención canónica que excluye una cola finalmente constante 999. No se emplea la raíz de un truncamiento como si fuera alfa completa.

Entonces

\[
 72.97352569283800997285105472380662
 <10^4\alpha_A<
 72.97352569283800997285105472380663.
\tag{11}
\]

La condición para que el lector fijo (3) coincidiera con ese valor sería

\[
 w(v)=\frac{73-10^4\alpha_A}{24},
\tag{12}
\]

cuyo intervalo está entre

\[
 0.0011030961317495844645393865080570833333\ldots
 \quad\text{y}\quad
 0.0011030961317495844645393865080575.
\]

Se usa (12) únicamente como criterio de comparación **después** de calcular los seis objetos. No se construyó un vector que lo satisficiera ni se varió ninguna mezcla.

**Dictamen focal exacto.** Los cinco objetos K, `Pi K`, `D3 K`, u y `P10(K)K` tienen `w>1/24`, por sustitución racional o signo exacto en `Q(sqrt5)`. Por ello sus respuestas cumplen `s<72`, mientras que `10^4 alpha_A>72`. El sexto objeto, `D4T3K`, tiene `w=0` y `s=73`, mientras que `10^4 alpha_A<73`. **Ninguna de las seis lecturas coincide con `10^4 alpha_A`.** La lectura conjunta con toda la memoria mantiene los pesos iniciales, por (7)–(8); seleccionar solamente la segunda memoria produce 73, no el valor intermedio de (11).

Este dictamen concierne a L, U, la carta y los seis objetos especificados. No es una negación de otras relaciones HMT entre alfa, el registro, la escala, las incidencias o el índice 73. El resultado positivo operativo es la separación exacta entre el índice ternario, el peso fijo del estado y el balance de memoria completa.

## 5. Reproducción y procedencia

El cálculo exacto empleó `Fraction` y las operaciones de `Q(sqrt5)` de [variacional.py:306](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/IV_MOONSHINE_DUALIDAD_TEORIA_M/antecedentes/controles_articulo_I/propietarios_k_moonshine/variacional.py:306>), cargado con `runpy.run_path(...,run_name='read_only_ternary')`; su función principal de escritura no se ejecutó. La matriz P3 se deriva de su suma finita de carácter, no se recibe aproximada.

Procedimiento reproducible exacto:

1. Construir S con `S[i,j]=1` si `j=(i+1) mod12`, U=S⁴, P0=(I+U+U²)/3 y L=8I−U.
2. Construir Pi, P3, K, u=P3 Pi K y q=Pi K−u.
3. Construir T3,T4 y los lectores racionalizados `Z3=(S³−I)/9`, `Z4=(S⁴−I)/9`.
4. Evaluar `a=dot(v,v)`, `b=dot(P0 v,P0 v)` para K,k,u,q,t. Para las memorias, usar `v=Z3 K` o `v=Z4 T3 K` y multiplicar a,b por ocho.
5. Comprobar exactamente `dot(Lv,Lv)=73a−24b`, antes de la racionalización de memorias o usando coherentemente el mismo factor ocho.
6. Para v=K,k,u,q, comprobar las tres sumas (7) usando I,P0,L. Los cuatro objetos dieron igualdad exacta en los tres balances.
7. Calcular w=b/a y s=73−24w por inversión racional cuadrática. La evaluación decimal se realiza al final con cuarenta cifras de trabajo.

Los propietarios inmediatos de Tj,Dj, la inversa y el balance son [nuclear/10.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/10.tex:140>) y [nuclear/11.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/11.tex:1>). K y P3 permanecen como resultados antecedentes. El lector `8I−S⁴` y estas seis evaluaciones constituyen una formalización focal añadida a la exploración, sin cambio de parámetros, fuentes selladas ni PDF.
