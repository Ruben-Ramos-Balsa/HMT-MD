# La suma de las coordenadas exponencial y circular: clasificación aritmética y normalización del acarreo

Inicio: 6 de septiembre de 2026. Ampliaciones matemáticas: 7 y 8 de septiembre de 2026. Documento de investigación editable, conservado para eventual composición en LaTeX. Las secciones 10–14 desarrollan la obstrucción al acarreo periódico, su aplicación a las orientaciones efectivas y el intento analítico mediante la segunda vía de \(\alpha\). Las secciones 15–19 componen los transportes cilíndrico e incidencial y demuestran criterios de complejidad relativa y de retorno mediante norma cuadrática. Las secciones 21–22 construyen el transporte del agregado con su acarreo y amplían el criterio a retornos compensados, que no exigen igualdad de los bloques sin normalizar. Las secciones 24–25 construyen controles exactos del transporte de aperiodicidad y de cobordes; la sección 26 sustituye la hipótesis racional en las dos vías completas y determina el efecto aritmético de cambios racionales del registro. La irracionalidad de la suma permanece sin demostrar en este desarrollo.

## 1. Sistema de partida y procedencia

**APP.** Se recibe del capítulo 27 la doble realización posicional y aritmética de las nueve marcas. Sus hojas aditiva y multiplicativa conservan residuo, cociente y acarreo. El dominio de los dos cursores es \(\Omega_{\rm seed}=(I_9^2\times D)_+\times(I_9^2\times D)_\times\), con \(I_9=\{0,\ldots,8\}\), \(D=\{N,E,S,O\}\) y \(104\,976\) estados. La aplicación de 54 pasos produce los 468 sextetos; la reducción trítica produce 243 palabras dentro del ambiente de 729.

**TRIT.** El selector \(M_{\rm ph}\) asigna a cada marca su orientación local en \(\{+1,-1,0\}\). La acción se efectúa sobre el estado y la hoja; el vector de valores de ese selector y el propio operador de selección permanecen diferenciados.

**TPK.** La transición recibida es
\[
\mathcal U_t=\operatorname{Rec}_t\circ\operatorname{Mem}_t
\circ\operatorname{Lift}(T_{d(t)})
\circ\operatorname{Sel}_t\bigl(\,\cdot\,,M_{\rm ph}(g(t))\bigr).
\]
Las prolongaciones
\(w_6\to w_{12}\to w_{18}\to w_{24}\to w_{30}\to R_{36}\to G_9\)
conservan sus tipos. La holonomía nonádica retorna la fase y actualiza el cociente y la memoria; el operador de memoria reducida es posterior a esa dinámica.

**Estado enriquecido.** Se conservan hoja, orientación, residuo, cociente, acarreo, ruta, frontera, memoria y supervivencia en los estados truncados. La relación de prolongación y los truncamientos satisfacen
\[
(x_r,x_{r+6})\in\operatorname{Ext}_{r+6,r}
\ \Longrightarrow\ \operatorname{tr}_{r+6,r}(x_{r+6})=x_r.
\]
La selección forward individualizada por el carácter R36 determina la sección compatible. La historia completa se retiene junto a cualquier valoración posterior.

**Estructura discreta conjunta del continuo.** El sistema compatible y sus realizaciones se reciben como construcción común del corpus. Esta investigación compone sus lectores exponencial y circular y el registro dodecafásico sobre el mismo estado; las cinco construcciones consustanciales del continuo permanecen en su antecedente común. Aquí se estudia una consecuencia aritmética de esos lectores, y no se reproduce ni se vuelve a certificar el tratado completo.

**Salidas HMT.** Las secciones regionales producen \(\pi_{\rm HMT},e_{\rm HMT},\varphi_{\rm HMT}\). El registro firmado y el sello dodecafásico actúan con esas secciones en la vía A de \(\alpha\). El orden constructivo de las operaciones conserva la genealogía común. Todos los coeficientes del cálculo que sigue proceden de la base de agrupación, del sello publicado y de esas salidas.

**Realización aritmética posterior.** En las identidades siguientes se escribe \(\pi,e,\varphi\) para las realizaciones ya identificadas de las tres coordenadas. Se usa \(\alpha_A\) para la sección infinita de la vía A con el sello periódicamente prolongado que define la fuente. Así queda separado este objeto tanto de la ventana racional de doce tríadas como de la raíz de una ecuación truncada. La identificación posterior permite utilizar las operaciones del cuerpo generado y la ecuación \(\varphi^2-\varphi-1=0\).

La observación autoral que motiva el estudio es la relación entre \(e+\pi\), el cierre dodecafásico y la profundidad de \(\alpha\). La identidad de la sección 2 es un **RESULTADO_RECUPERADO** de los propietarios indicados al final. Las secciones 3–6 reúnen deducciones y pruebas para esta pregunta; se clasifican como **FORMALIZACION_NUEVA** respecto de esta nota, sin reivindicación de novedad histórica de los lemas algebraicos generales.

## 2. Identidad exacta del sello periódico

Sea \(B=1000\), base utilizada para agrupar tres cifras decimales. Sean
\[
\pi-3=\sum_{k\ge1}P_kB^{-k},\quad
e-2=\sum_{k\ge1}E_kB^{-k},\quad
\varphi-1=\sum_{k\ge1}\Phi_kB^{-k}.
\]
Las tres sucesiones son las expansiones de las salidas previamente construidas.

La fuente fija
\[
(K_1,\ldots,K_{12})
=(234,543,140,729,659,824,621,058,914,794,146,601)
\]
y prolonga \(K_k=K_{1+((k-1)\bmod12)}\). Por suma geométrica,
\[
\kappa:=\sum_{k\ge1}K_kB^{-k}
=\frac{M_K}{B^{12}-1},\qquad
M_K=\sum_{j=1}^{12}K_jB^{12-j}
=234543140729659824621058914794146601.
\tag{1}
\]
En particular, \(\kappa\in\mathbb Q\). Esta racionalidad corresponde al sello periódico valorado; no determina la clase aritmética de \(\alpha_A\).

Definamos
\[
D_k=P_k+E_k-\Phi_k-K_k.
\]
La normalización de la vía A es
\[
A_k=D_k+c_{k+1}-Bc_k,\qquad
c_k=\left\lfloor\frac{D_k+c_{k+1}}{B}\right\rfloor,\qquad
0\le A_k<B.
\tag{2}
\]
Como \(-1998\le D_k\le1998\), el conjunto de acarreos
\(\{-2,-1,0,1,2\}\) es estable bajo esa división euclídea.

**Proposición 1.** Para cada horizonte \(N\),
\[
c_1+\sum_{k=1}^{N}A_kB^{-k}
=\sum_{k=1}^{N}D_kB^{-k}+c_{N+1}B^{-N}.
\tag{3}
\]

**Demostración.** Se multiplica (2) por \(B^{-k}\) y se suma. Los términos de acarreo intermedios se cancelan: la diferencia de las dos sumas de acarreos es \(c_{N+1}B^{-N}-c_1\). Esto da (3). La cota del acarreo terminal implica que su contribución tiende a cero. Dos condiciones terminales en el conjunto admitido producen valores completos que difieren a lo sumo en \(4B^{-N}\). \(\square\)

El valor límite es independiente de la condición terminal acotada. La coincidencia de prefijos canónicos exige además atender a los extremos con doble expansión; por eso el ejecutable conservado publica el prefijo común de todos los terminales admitidos.

En la sección efectiva de la fuente, \(c_1=0\). Por (3),
\[
\alpha_A=(\pi-3)+(e-2)-(\varphi-1)-\kappa,
\]
de donde resulta
\[
\boxed{S:=e+\pi=4+\varphi+\kappa+\alpha_A.}
\tag{4}
\]
Esta es una igualdad de valores límite, no una comparación de aproximaciones decimales.

## 3. Transferencia exacta de la clasificación aritmética

Escribamos \(r=4+\kappa\in\mathbb Q\), \(K_5=\mathbb Q(\varphi)=\mathbb Q(\sqrt5)\) y \(\overline{\mathbb Q}\) para el cuerpo de los números algebraicos.

**Teorema 2.** En la sección definida en la sección 2 se cumplen:
\[
\begin{aligned}
S\in\mathbb Q
&\iff \alpha_A+\varphi\in\mathbb Q
\iff \alpha_A\in\mathbb Q-\varphi, \tag{5}\\
S\in\overline{\mathbb Q}
&\iff \alpha_A\in\overline{\mathbb Q}, \tag{6}\\
S\text{ es trascendente}
&\iff \alpha_A\text{ es trascendente}. \tag{7}
\end{aligned}
\]
Además,
\[
\mathbb Q(\varphi,S)=\mathbb Q(\varphi,\alpha_A).
\tag{8}
\]
Si \(\alpha_A=a+b\varphi\) con \(a,b\in\mathbb Q\), entonces
\[
S\in\mathbb Q\iff b=-1.
\tag{9}
\]

**Demostración.** Por (4), \(S=r+\varphi+\alpha_A\). Restar el racional \(r\) da (5). La suma y la diferencia de algebraicos son algebraicas; como \(r+\varphi\) es algebraico, se obtiene (6) en ambos sentidos. Su complemento da (7). Cada uno de \(S,\alpha_A\) se expresa a partir del otro y de \(r,\varphi\), lo que prueba (8). Finalmente,
\(S=r+a+(b+1)\varphi\); la independencia lineal de \(1,\varphi\) sobre \(\mathbb Q\) da (9). \(\square\)

**Corolario 3.** Cualquiera de las condiciones siguientes basta para demostrar la irracionalidad de \(S\):

- \(\alpha_A\notin K_5\);
- \(\alpha_A\in\mathbb Q\), en cuyo caso \(S\) tiene grado exactamente dos sobre \(\mathbb Q\);
- \(\alpha_A=a+b\varphi\), con \(a,b\in\mathbb Q\) y \(b\ne-1\);
- \(\alpha_A\) trascendente, en cuyo caso también \(S\) es trascendente.

**Demostración.** Si \(S\) fuera racional, (5) impondría \(\alpha_A\in\mathbb Q-\varphi\subset K_5\). Los dos casos siguientes se deducen de (9), y el último de (7). \(\square\)

La exclusión exacta que decide la pregunta es, por tanto, \(\alpha_A\notin\mathbb Q-\varphi\). La sola irracionalidad de \(\alpha_A\) deja abierta la posibilidad precisa \(q-\varphi\), que también es irracional. La profundidad infinita del refinamiento y la clasificación aritmética son propiedades distintas. Por ejemplo, las dos cantidades generadas a partir de \(\varphi\), \(\varphi-1\) y \(2-\varphi\), son irracionales con expansiones no eventualmente periódicas, mientras que su suma es exactamente uno. Este ejemplo comprueba la insuficiencia de esa inferencia general; no atribuye racionalidad a \(e+\pi\).

La transferencia del teorema 2 reorganiza la cuestión, pero no aporta por sí sola una prueba independiente de la clase aritmética. Una demostración de trascendencia de \(\alpha_A\) que utilizara previamente la trascendencia de \(e+\pi\) no permitiría aplicar (7) para demostrar esta última sin circularidad. La información adicional tendría que proceder de una propiedad probada de la dinámica normalizada o de la segunda vía completa que no presuponga la conclusión investigada.

## 4. Núcleo de la valoración y ecuación del acarreo

El siguiente lema identifica exactamente qué información de una sucesión entera puede cancelarse al valorar una expansión. Permite formular la cuestión sobre el acarreo completo, conservando la distinción entre historia y valor.

**Lema 4.** Sea \(B\ge2\) entero y sea \((d_k)_{k\ge1}\) una sucesión entera acotada, con \(M=\sup_k|d_k|\). Entonces
\[
\sum_{k\ge1}d_kB^{-k}=0
\]
si y sólo si existe una sucesión entera acotada \((c_k)_{k\ge1}\), con \(c_1=0\), tal que
\[
d_k=Bc_k-c_{k+1}\qquad(k\ge1).
\tag{10}
\]
Esta sucesión es única y satisface \(|c_k|\le M/(B-1)\).

**Demostración.** Supóngase que la suma es cero. Para \(n\ge0\), se define
\[
c_{n+1}=B^n\sum_{k>n}d_kB^{-k}
=-\sum_{k=1}^{n}d_kB^{n-k}.
\tag{11}
\]
La segunda expresión prueba la integridad y \(c_1=0\). La primera proporciona la cota geométrica \(M/(B-1)\). Al restar colas consecutivas se obtiene (10). Recíprocamente, (10) implica
\[
\sum_{k=1}^{N}d_kB^{-k}
=c_1-c_{N+1}B^{-N}\longrightarrow0.
\]
Si dos soluciones acotadas existieran, su diferencia cumpliría \(h_{k+1}=Bh_k\); la acotación fuerza \(h_k=0\). \(\square\)

En consecuencia, dos sucesiones enteras acotadas representan el mismo valor y la misma parte entera exactamente cuando su diferencia es de la forma (10). El operador \(c\mapsto(Bc_k-c_{k+1})_k\) describe este núcleo. Se trata de la normalización de la lectura numérica; la historia enriquecida que la produjo permanece como antecedente separado.

## 5. Aplicación al lector de la suma

Sea
\[
x=\pi-3,\qquad y=e-2,\qquad
u_k=\{B^{k-1}x\},\quad v_k=\{B^{k-1}y\},
\]
y defínase el acarreo binario \(C_k=\lfloor u_k+v_k\rfloor\in\{0,1\}\).
La parte fraccionaria del valor transportado es
\(T_k=u_k+v_k-C_k=\{B^{k-1}(x+y)\}\). Por división euclídea,
\[
BT_k=
\underbrace{P_k+E_k+C_{k+1}-BC_k}_{s_k}+T_{k+1},
\qquad 0\le T_{k+1}<1.
\]
Por tanto,
\[
s_k=P_k+E_k+C_{k+1}-BC_k\in\{0,\ldots,B-1\}
\tag{12}
\]
son las cifras canónicas de la suma, y
\[
x+y=C_1+\sum_{k\ge1}s_kB^{-k}.
\tag{13}
\]
En la sección estudiada \(x+y<1\), de modo que \(C_1=0\). Las fórmulas conservan ese término para evitar perder una unidad en otras sumas.

**Proposición 5.** La irracionalidad de \(S=e+\pi\) equivale a la inexistencia de una expansión eventualmente periódica \((r_k)\) en base \(B\), un entero \(q_0\) y una sucesión entera acotada \((c_k)\), con \(c_1=q_0\), tales que
\[
P_k+E_k-r_k=Bc_k-c_{k+1}\qquad(k\ge1).
\tag{14}
\]

**Demostración.** Si (14) se cumple, la telescopía da
\(x+y=q_0+\sum_{k\ge1}r_kB^{-k}\), que es racional por periodicidad eventual. Recíprocamente, si \(x+y\) es racional, se toma su expansión canónica eventualmente periódica y su parte entera \(q_0\). La misma construcción de colas del lema 4, ahora con suma \(q_0\), proporciona el acarreo entero acotado; en (11) la segunda expresión se sustituye por
\(B^nq_0-\sum_{k=1}^n d_kB^{n-k}\). \(\square\)

El criterio de separación de colas del corpus resulta pertinente precisamente para \((s_k)\), después de (12). Hay que probar que la dinámica efectiva de la suma excluye (14), incluidos el prefijo transitorio y cualquier período posterior. La aperiodicidad de las dos secciones por separado, el avance de memoria enriquecida o el retorno de la fase en nueve pasos no sustituyen esa exclusión.

El invariante ejecutable \((a_j+b_j)\bmod3\), denominado «\(\pi+e\) fijo» en una comprobación residual, conserva información local anterior a esta valoración. La suma real exige adicionalmente los acarreos de (12). No se ha usado aquel invariante como una prueba de (14).

## 6. La segunda vía y la ecuación truncada

El propietario del capítulo 31 distingue la sección completa de la raíz \(\xi_9\) de una ecuación finita. Su parte de grado seis es
\[
2\pi z-\frac74z^2+\frac{z^3}{2\pi}
+\frac{z^4}{20}-\frac{2z^5}{21}-\frac{z^6}{46}
=\log_{10}(10/9);
\]
el tramo de grados siete a nueve añade
\[
-\frac{z^7}{120}+\frac{z^8}{45}+\frac{2z^9}{495}.
\]
Los coeficientes pertenecen al cuerpo
\(\mathbb Q(\pi,\log_{10}(10/9))\). La prueba de existencia y unicidad de la raíz pequeña es una prueba analítica sobre ese dominio. Esa propiedad, por sí sola, no excluye que la sección completa pertenezca a \(\mathbb Q-\varphi\).

Para usar la vía B en la clasificación de \(S\), debe actuar la ecuación completa sobre su sección completa. Reemplazar \(\alpha_A\) por \(\xi_9\) o por la ventana racional de doce tríadas modificaría el objeto de (4). No se ha realizado tal sustitución. La identidad límite de las dos vías, afirmada en el corpus, y la clasificación aritmética de su valor son enunciados distintos.

## 7. Resultado obtenido y continuación matemática delimitada

Quedan demostrados aquí:

1. La valoración racional exacta del sello periódico y la identidad (4), recuperadas del corpus.
2. Las equivalencias de racionalidad, algebraicidad y trascendencia (5)–(9).
3. La caracterización completa del núcleo de valoración por acarreos enteros acotados.
4. El criterio de racionalidad de la suma mediante una expansión eventualmente periódica y la ecuación (14).
5. La caracterización de cada período mediante un autómata de tres estados y nueve transiciones; véase el teorema 6.
6. La reducción a períodos múltiplos de una longitud fijada y la cancelación exacta del sello periódico en la ecuación de diferencias; sección 11.
7. La trascendencia de \(\log_{10}(10/9)\), como resultado auxiliar de la vía analítica; proposición 8. Su traslado a la clasificación de \(\alpha_A\) requiere una inferencia adicional y no se da por demostrado.

La cuestión principal se ha reducido exactamente a dos formulaciones equivalentes y utilizables: excluir \(\alpha_A\in\mathbb Q-\varphi\), o excluir la solución periódica normalizada de (14). Esta nota no contiene esa exclusión. No presenta una demostración de irracionalidad ni de trascendencia de \(e+\pi\).

La revisión focal comprendió los propietarios de las dos vías de \(\alpha\), el teorema de prolongación arbitraria, la taxonomía aritmética, el capítulo de compuestos y los ejecutables de acarreo. El alcance de esta constatación es ese conjunto de fuentes; no se declara ausencia en todo el corpus. Tampoco se infiere una limitación de la generación de \(\pi,e,\varphi\) a una cantidad finita de cifras.

## 8. Inserción editorial puntual

El lugar natural de (4) y del teorema 2 es el primer artículo en preparación por **Aclarar la tarea**, inmediatamente después de la construcción completa de \(\alpha\). La identidad enlaza exactamente sus cuatro coordenadas y permite formular una cuestión aritmética verificable. Se propone incorporar únicamente la identidad demostrada y las equivalencias probadas; la afirmación de irracionalidad requiere la exclusión indicada en la sección 7.

El artículo de **Ley nueve puertas**, dedicado a acción y Barbero, mantiene su objeto propio. Esta investigación no exige introducir allí la clasificación de \(e+\pi\), ni ampliar ahora ninguno de los dos manuscritos con todo el catálogo de constantes. No se han modificado esos trabajos ni se han enviado mensajes de coordinación.

## 9. Fuentes y control de procedencia

Corte científico empleado: fuente editable del integral de 2.249 páginas de 5 de septiembre de 2026, cuyo PDF tiene SHA-256
`958d252f301763ff8901f775d8ec0b02b6ae4f9f7c57dc04ea917f747dccbf24`.
El registro común puede conservar referencias históricas de menor extensión; no se ha sustituido este corte de trabajo por ellas.

- [Capítulo 27: sistema inicial y prolongación completa](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:8>); proposición `prop:c27-alpha-prolongacion-completa`, desde la línea 642.
- [Vía A y periodicidad del sello](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/alpha/08a_alpha_dos_vias_t1_rev8_body.tex:173>); fórmula del acarreo desde la línea 177.
- [Sección larga y prefijo común](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/alpha/08b_alpha_t1_10000_rev9.tex:1>).
- [Capítulo 31: dos vías y truncación analítica](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c31_dos_vias_alpha_y_prolongacion_nonadica.tex:1>).
- [Taxonomía: separación de colas y periodicidad](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/dependencies/14c_taxonomia_monodromia_nonadica_body.tex:49>).
- [Capítulo 44: construcción de compuestos y clasificación](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/base_83/c44_body.tex:800>).
- [Generador T1 conservado](</Users/ruben/Documents/excelencia academica/DERIVACION_CONSTANTE_ESTRUCTURA_FINA_HMT_2026-08-18/evidencia_reproducible/conexion_nonadica_10000/generar_alpha_T1_10000.py:94>).
- [Invariante residual ternario](</Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/verificar_contra_corpus.py:278>).

Como contexto bibliográfico posterior, la presentación de Michel Waldschmidt de 2012 enumera la pregunta por la irracionalidad de \(e+\pi\): [Number Theory: Challenges of the Twenty-First Century](https://webusers.imj-prg.fr/~michel.waldschmidt/articles/pdf/NTchallengesVI.pdf). El trabajo de F. M. S. Lima de 2013 recuerda esa cuestión y prueba restricciones conjuntas sobre suma y producto: [Some transcendence results from a harmless irrationality theorem](https://arxiv.org/abs/1310.7289). Estas fuentes sitúan históricamente el problema; no sustituyen las pruebas de esta nota ni certifican por sí solas su estado bibliográfico en 2026.

Verificación realizada: lectura de los propietarios citados y revisión algebraica independiente de (3), (5)–(10) y (14). Los controles documentales de continuidad y causalidad distinguen las salidas generadas de sus realizaciones posteriores; no constituyen certificados de irracionalidad. Los originales, los artículos en preparación y sus PDFs no se han modificado.

## 10. Obstrucción a la periodicidad mediante tres estados de acarreo

Se trabaja sobre las secciones circular y exponencial recibidas en la sección 1 y sobre sus valores posteriores \(x=\pi-3\), \(y=e-2\). El argumento vale para cualquier base entera \(B\ge3\); la aplicación decimal utiliza \(B=1000\), y la lectura de sextetos tríticos utiliza \(B=3^6=729\).

Sean
\[
u_k=\{B^{k-1}x\},\qquad v_k=\{B^{k-1}y\},\qquad
z_k=u_k+v_k\in[0,2),
\]
donde \(\{\,\cdot\,\}\) denota la parte fraccionaria. Escribamos
\[
P_k^{(B)}=\lfloor Bu_k\rfloor,\qquad
E_k^{(B)}=\lfloor Bv_k\rfloor.
\]
En esta sección se abrevian estas cifras por \(P_k,E_k\) para la base elegida. Coinciden con los bloques de las secciones anteriores cuando \(B=1000\). Definamos
\[
t_k=P_k+E_k,\quad C_k=\lfloor z_k\rfloor\in\{0,1\},
\quad T_k=z_k-C_k.
\]
Las identidades de desplazamiento son
\[
Bz_k=t_k+z_{k+1},\qquad
BT_k=s_k+T_{k+1},\qquad
s_k=t_k+C_{k+1}-BC_k.
\tag{15}
\]
En particular, \(s_k=\lfloor BT_k\rfloor\) son las cifras canónicas de la suma fraccionaria.

**Teorema 6.** Fijados \(N\ge1\) y \(p\ge1\), las condiciones siguientes son equivalentes:

1. \(s_{k+p}=s_k\) para cada \(k\ge N\).
2. \(T_{N+p}=T_N\).
3. Existe una sucesión \(h_k\in\{-1,0,1\}\), \(k\ge N\), tal que
   \[
   d_k^{(p)}:=t_{k+p}-t_k=Bh_k-h_{k+1}.
   \tag{16}
   \]

Cuando existe, la sucesión de estados es única y satisface
\[
h_k=z_{k+p}-z_k=C_{k+p}-C_k.
\tag{17}
\]

**Demostración.** Las condiciones 1 y 2 son equivalentes por unicidad de la expansión canónica y por la dinámica \(T_{k+1}=\{BT_k\}\). Bajo la condición 2 se tiene \(T_{k+p}=T_k\) para cada \(k\ge N\). Por tanto, \(z_{k+p}-z_k=C_{k+p}-C_k\) pertenece a \(\{-1,0,1\}\). La diferencia de las dos identidades \(Bz=t+\operatorname{shift}(z)\) proporciona (16).

Recíprocamente, sea \(D_k=z_{k+p}-z_k\). Esta sucesión acotada satisface
\[
BD_k=d_k^{(p)}+D_{k+1}.
\]
Si \(h\) satisface (16), entonces
\[
(D-h)_{k+1}=B(D-h)_k.
\]
La acotación y \(B>1\) obligan a \(D_k=h_k\) para cada \(k\ge N\). En consecuencia, \(z_{k+p}-z_k\) es entero, sus partes fraccionarias coinciden y se obtiene 2. El mismo argumento aplicado a dos soluciones acotadas prueba la unicidad. \(\square\)

El conjunto de transiciones del autómata es
\[
\mathcal E_B=\{(h,Bh-h',h'):h,h'\in\{-1,0,1\}\}.
\]
Para \(B\ge3\), cada etiqueta determina un único par ordenado de estados: de \(Bh-h'=B\widetilde h-\widetilde h'\) se sigue
\(B(h-\widetilde h)=h'-\widetilde h'\), cuyo segundo miembro tiene módulo a lo sumo \(2\). Así \(h=\widetilde h\) y \(h'=\widetilde h'\).

En base mil, la tabla completa es:

| Estado inicial \(h\) / estado final \(h'\) | \(-1\) | \(0\) | \(1\) |
|---|---:|---:|---:|
| \(-1\) | \(-999\) | \(-1000\) | \(-1001\) |
| \(0\) | \(1\) | \(0\) | \(-1\) |
| \(1\) | \(1001\) | \(1000\) | \(999\) |

Una sucesión de diferencias queda excluida cuando aparece una etiqueta ajena a la tabla o cuando dos etiquetas consecutivas exigen estados incompatibles. Por ejemplo, la pareja de etiquetas \((1,1)\) es incompatible: ambas representan la transición \(0\to-1\).

**Corolario 7.** La irracionalidad de \(e+\pi\) equivale a que, para cada \(N\ge1\) y cada \(p\ge1\), la sucesión
\[
\bigl(t_{k+p}-t_k\bigr)_{k\ge N}
\]
contenga una etiqueta inadmisible o una concatenación de dos etiquetas incompatible.

**Demostración.** Una sucesión infinita cuyas etiquetas son admisibles y cuyas transiciones consecutivas concatenan define una única trayectoria infinita del autómata. El teorema 6 identifica esa trayectoria con un período de la suma normalizada. La caracterización de los racionales por periodicidad eventual completa la equivalencia. \(\square\)

Este criterio elimina la búsqueda de una expansión racional completa: cada período candidato se contrasta mediante diferencias de los dos lectores efectivos y tres estados de acarreo. El cuantificador sobre \(N,p\) permanece íntegro.

### 10.1. Comprobación exacta del criterio

El archivo acompañante [verificar_obstruccion_periodica_suma.py](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/verificar_obstruccion_periodica_suma.py>) utiliza exclusivamente aritmética entera y racional de la biblioteca estándar.

Se han comprobado:

- las transiciones y todas sus concatenaciones de longitud dos en bases \(3,10,729,1000\);
- las trayectorias de cinco estados en esas bases;
- 264 casos racionales exactos de entradas puramente periódicas en base tres, incluyendo el cierre del ciclo;
- el rechazo explícito de aplicar la equivalencia infinita a un prefijo arbitrario.

La precondición del último grupo es material: se verifica \(\{B^\ell x\}=x\), \(\{B^\ell y\}=y\), junto con una longitud de inspección que cubre el ciclo y su concatenación final. Una aceptación finita sin esa precondición no prueba periodicidad.

Se han leído asimismo los prefijos de mil cifras ya conservados, sin generar cifras nuevas: 333 bloques completos por canal. Los períodos \(1,\ldots,108\) quedan rechazados desde \(N=1\) en esa ventana. Por ejemplo, las diferencias iniciales de los períodos \(1,2,9,12,108\) son, respectivamente, \(14,622,-228,95,244\), ajenas a la tabla. Este resultado excluye esos períodos **desde el inicio indicado**; no excluye un prefijo transitorio arbitrario ni períodos mayores.

## 11. Compatibilidad con el período dodecafásico y la normalización de \(\alpha\)

Para cualquier entero fijo \(L\ge1\), basta demostrar el corolario 7 para los períodos \(p=Lm\), \(m\ge1\). En efecto, una expansión de período eventual \(p_0\) admite también el período \(Lp_0\).

En base mil se puede elegir \(L=12\). La identidad del acarreo de la sección 2 proporciona
\[
t_k=A_k+\Phi_k+K_k+Bc_k-c_{k+1}.
\]
Para \(p=12m\), defínase \(\Delta_p f_k=f_{k+p}-f_k\) y
\(b_k=c_{k+p}-c_k\). La periodicidad del sello implica
\[
\Delta_p t_k
=\Delta_p(A+\Phi)_k+Bb_k-b_{k+1}.
\tag{18}
\]
Por tanto, si \(h\) fuese una trayectoria compatible con (16), \(g_k=h_k-b_k\) satisfaría
\[
\Delta_p(A+\Phi)_k=Bg_k-g_{k+1}.
\tag{19}
\]
Recíprocamente, una solución entera acotada de (19) produce una solución entera acotada de (16); la demostración del teorema 6 obliga entonces a que esta última tome sus valores en \(\{-1,0,1\}\).

La periodicidad del sello desaparece exactamente de la ecuación de diferencias. La obstrucción buscada reside en la suma normalizada de las secciones \(\alpha_A\) y \(\varphi\). La mera profundidad de \(\alpha_A\) no decide (19): un valor \(q-\varphi\) tiene expansión infinita aperiódica y, al sumarle \(\varphi\), produce el racional \(q\).

En base \(729\), el retorno de fase permite examinar períodos múltiplos de \(9\). El índice de un sexteto trítico y el índice de un bloque decimal no se identifican: el cambio de base se realiza mediante los cilindros de valoración. Por ello, la cancelación dodecafásica de (18) y la alineación nonádica son dos formulaciones coordinadas, no una igualdad entre sus índices.

## 12. Aplicación a las orientaciones nonádicas y cancelación local

El propietario [06e, desde la línea 547](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex:547>) presenta las tres orientaciones
\[
\begin{aligned}
&(101222\mid112221\mid112002),\\
&(102221\mid111222\mid112002),\\
&(111221\mid102222\mid112002).
\end{aligned}
\]
Sus dos primeros sextetos, valorados como enteros en base tres, son
\[
(296,403),\quad(322,377),\quad(376,323).
\]
Los tres pares suman exactamente
\[
699=(221220)_3.
\tag{20}
\]
La transición entre los dos primeros pares cambia los valores en \(+26\) y \(-26\); la suma cancela ese cambio antes de cualquier acarreo.

El agregado residual \(210110\) del propietario pertenece a la suma componente a componente módulo tres. El valor entero de (20) utiliza la suma posicional con sus acarreos. Ambos agregados coinciden entre las orientaciones respectivas, pero no son el mismo objeto.

La frontera siguiente selecciona la primera orientación: el censo pasa de tres supervivientes a uno. Esta selección determina la continuación efectiva indicada por la fuente. La igualdad (20) muestra que la lectura escalar de la suma no separa las tres orientaciones en la primera frontera. No demuestra que sus colas completas coincidan ni constituye un contraejemplo a la irracionalidad de las coordenadas efectivas.

### 12.1. Delimitación exacta del argumento por memoria y unicidad

Puede comprobarse algebraicamente por qué el avance de memoria, la selección única posterior y la aperiodicidad individual deben vincularse al carácter efectivo para resolver la suma.

Sea \(\theta=\varphi_{\rm HMT}-1\) y
\[
b_n=\lfloor n\theta\rfloor-\lfloor(n-1)\theta\rfloor.
\]
Su promedio converge a \(\theta\), irracional; por tanto \(b_n\) es aperiódica. Construyamos únicamente para esta comprobación los canales auxiliares
\[
p_n=296+26b_n,\qquad e_n=403-26b_n,
\]
cuyos pares utilizan dos de las orientaciones de (20). Ambos son aperiódicos, pero sus valoraciones en base \(729\) satisfacen
\[
X+Y=\sum_{n\ge1}\frac{p_n+e_n}{729^n}
=\frac{699}{728}\in\mathbb Q.
\tag{21}
\]
Un estado que retenga \(n\), su fase módulo nueve y \(b_n\) determina la elección única en cada paso y conserva memoria creciente.

Estos canales auxiliares **no son** \(\pi_{\rm HMT}\) y \(e_{\rm HMT}\): no se les atribuyen sus caracteres R36 ni sus lectores específicos. La construcción sólo refuta la inferencia que utilizaría las tres propiedades abstractas indicadas como sustituto de la acción de esos caracteres. Para aplicar el corolario 7 a la pareja efectiva, la compensación de (21) tiene que quedar excluida por sus operaciones propias.

## 13. Intento de exclusión mediante el lector analítico de \(\alpha\)

### 13.1. Clasificación de la constante regularizada de vacancia

**Proposición 8.** El valor regularizado
\[
\varepsilon_v=\log_{10}(10/9)
\]
es trascendente.

**Demostración.** Si \(\varepsilon_v=m/n\), con \(m,n\) enteros y \(n>0\), entonces \(10^m=(10/9)^n\). La valoración en el primo tres es cero en el primer miembro y \(-2n\) en el segundo, contradicción. Si \(\varepsilon_v\) fuese algebraica irracional, el teorema de Gelfond–Schneider haría trascendente \(10^{\varepsilon_v}\), mientras que ese valor es el racional \(10/9\). Se excluyen así las dos clases de números algebraicos. \(\square\)

La identidad de \(\varepsilon_v\) se recibe del propietario de vacancias, después de su construcción. El teorema de trascendencia se utiliza como reconocimiento aritmético posterior, no como selector de una salida HMT. Su formulación puede consultarse en [Michel Waldschmidt, *Introduction to Diophantine methods: irrationality and transcendence*](https://webusers.imj-prg.fr/~michel.waldschmidt/coursHCMUNS2007.html).

### 13.2. Sustitución cuadrática efectuada

Escribamos
\[
P_9(z)=2\pi z+\frac{z^3}{2\pi}+R_9(z),\quad
R_9(z)=-\frac74z^2+\frac{z^4}{20}
-\frac{2z^5}{21}-\frac{z^6}{46}
-\frac{z^7}{120}+\frac{z^8}{45}+\frac{2z^9}{495}.
\tag{22}
\]
Para \(q\in\mathbb Q\), la reducción
\((q-\varphi)^n=u_n+v_n\varphi\) está determinada por
\[
(u_0,v_0)=(1,0),\qquad
u_{n+1}=qu_n-v_n,\quad
v_{n+1}=-u_n+(q-1)v_n.
\tag{23}
\]
Se deduce
\[
P_9(q-\varphi)=A(q;\pi)+B(q;\pi)\varphi,\qquad
A,B\in\mathbb Q(\pi).
\]
Una igualdad \(P_9(q-\varphi)=\varepsilon_v\) exigiría
\[
(\varepsilon_v-A)^2-B(\varepsilon_v-A)-B^2=0.
\tag{24}
\]
La ecuación se obtiene eliminando \(\varphi\) mediante \(\varphi^2-\varphi-1=0\). Sus coeficientes pertenecen a \(\mathbb Q(\pi)\); la trascendencia de \(\varepsilon_v\) sobre \(\mathbb Q\) no la contradice. Haría falta excluir la relación correspondiente sobre ese cuerpo, o emplear una restricción más fuerte del transporte.

Además, \(P_9\) define la raíz \(\xi_9\) del cociente finito, no la sección completa \(\alpha_A\). La cuenta anterior examina una posible estrategia de exclusión; no sustituye \(\alpha_A\) por \(\xi_9\).

### 13.3. Coeficientes graduados y prolongación posicional

La acción expuesta para los grados siete a nueve es
\[
Ne_7=-\frac83e_8,\quad Ne_8=\frac2{11}e_9,\quad
Ne_9=0,\qquad v_7=-\frac1{120}e_7.
\]
Como \(N^3=0\),
\[
\operatorname{ev}(I-N)^{-1}v_7
=-\frac{z^7}{120}+\frac{z^8}{45}+\frac{2z^9}{495}.
\tag{25}
\]
La prolongación al grado diez requiere la acción efectiva sobre el siguiente componente graduado. En efecto, las extensiones
\[
\widehat N_\lambda e_9=\lambda e_{10},\qquad
\widehat N_\lambda e_{10}=0
\]
con \(\lambda\in\mathbb Q\), las mismas acciones sobre \(e_7,e_8\) y la misma semilla \(v_7\), conservan (25) al truncar y añaden \((2\lambda/495)z^{10}\). La compatibilidad con el cociente anterior no selecciona por sí sola \(\lambda\).

Se han seguido las remisiones del capítulo 31, su propietario exacto enlazado y el ejecutable del integral. Allí se recupera la actualización posicional
\[
d_k=\operatorname{Dig}_{729}(\epsilon_k),\quad
\epsilon_{k+1}=729\epsilon_k-d_k,\quad
N_{k+1}=729N_k+d_k,\quad \chi_{k+1}=\chi_k,
\tag{26}
\]
con el carácter \(\chi\) previamente construido. Véase [el ejecutable, desde la línea 1569](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:1569>).

La cifra \(d_{10}\) de (26) y el coeficiente de \(z^{10}\) de la ecuación analítica pertenecen a tipos diferentes. Para un candidato \(a=q-\varphi\in(0,1)\), la actualización residual tiene la realización exacta
\[
N_n=\lfloor729^na\rfloor,\qquad
\epsilon_n=729^na-N_n\in\mathbb Q(\varphi)\cap(0,1).
\tag{27}
\]
Aquí \(n\ge0\), \(N_0=0\), \(\epsilon_0=a\) y \(\operatorname{Dig}_{729}(t)=\lfloor729t\rfloor\) para \(0\le t<1\). Se cumple \(d_n=N_{n+1}-729N_n\). Sus cilindros son compatibles, contienen \(a\) y tienen diámetro \(729^{-n}\). Esto verifica que la regla residual por sí sola admite el candidato; no prueba que el selector R36 lo produzca. La acción que distingue ese carácter de los candidatos debe conservarse explícitamente al componer la vía analítica.

El conjunto de remisiones seguido no ha proporcionado aquí una regla evaluable para el coeficiente de grado diez o su familia completa. Esta constatación está circunscrita a esas remisiones y no se convierte en una afirmación de inexistencia en el corpus.

### 13.4. Contraste de la alternativa angular

Existe un criterio de exclusión particularmente corto: una identidad demostrada
\[
\lambda=\exp(2\pi i\alpha_A),\qquad
\lambda\in\overline{\mathbb Q},
\tag{28}
\]
excluiría \(\alpha_A=q-\varphi\). En efecto, \(2(q-\varphi)\) es algebraico irracional y el miembro derecho sería un valor de
\((-1)^{2(q-\varphi)}\), trascendente por Gelfond–Schneider. El mismo argumento excluye cualquier valor algebraico irracional de \(\alpha_A\). Si además \(\lambda\) no fuese raíz de la unidad, (28) excluiría también \(\alpha_A\in\mathbb Q\) y probaría su trascendencia.

Se ha buscado (28) en los operadores angulares concretos, sin identificar objetos de tipos diferentes:

- la carta \(A_{\rm deg}=1000\alpha\) es una evaluación angular posterior; no demuestra la algebraicidad de su exponencial;
- la rotación regular de \(C_{12}\) tiene espectro ciclotómico; \(A_{34}\) transporta racionalmente sus sectores de órdenes tres y cuatro. El texto consultado no identifica un argumento espectral con \(\alpha_A\);
- el resolvente del capítulo 27 es hiperbólico:
  \(T_\pm=\alpha e^{\pm\xi}\), \(T_+T_-=\alpha^2\);
  \(\alpha\) es allí la media geométrica de dos valores positivos, no el argumento de un autovalor unitario;
- la holonomía \(\exp(2\pi ik\varepsilon_v)\) utiliza \(\varepsilon_v\), no \(\alpha_A\).

Por ello, (28) queda formulado como un criterio exacto que requeriría una identidad operatoria adicional; no se lo incorpora como dato al generador.

## 14. Balance probatorio de la ampliación

La ampliación desarrolla dos intentos efectivos sobre los objetos de la fuente:

1. Compone las emisiones circular y exponencial con su acarreo, demuestra el teorema de tres estados y reduce los períodos a una familia cofinal alineable con el calendario. La exclusión universal exige una incompatibilidad producida por el transporte efectivo para cada cola y período; los prefijos inspeccionados y la selección local \(3\to1\) no cubren ese cuantificador.
2. Sustituye exactamente la clase \(q-\varphi\) en la vía analítica, elimina \(\varphi\), prueba la trascendencia de \(\varepsilon_v\) y distingue la prolongación de cifras de la de coeficientes. La relación obtenida sobre \(\mathbb Q(\pi)\) no produce todavía una contradicción; los operadores angulares leídos tampoco proporcionan la identidad (28).

Los teoremas auxiliares y sus pruebas quedan conservados. El objetivo principal —demostrar \(e+\pi\notin\mathbb Q\)— continúa sin una demostración en este archivo. Ningún resultado finito, prueba de compilación, recibo causal o clasificación editorial sustituye ese enunciado.

La procedencia de los objetos HMT sigue siendo la de la sección 1. Los argumentos de las secciones 10–13 son formalizaciones incorporadas en esta ampliación; no se reivindica originalidad histórica para el teorema de Gelfond–Schneider, la normalización posicional ni los criterios generales de periodicidad. El programa acompañante verifica el criterio local y ejemplos racionales: no declara solucionado el problema de \(e+\pi\).

## 15. Composición del transporte cilíndrico con el reloj y la incidencia

Ampliación del 8 de septiembre de 2026. Se recibe la misma trayectoria regional
APP–TRIT–TPK, con sus tres canales, cocientes, marcos, memoria e incidencia.
La lectura del integral se realiza sobre su PDF de 2.249 páginas, no sobre el
testigo de 2.084. Se incorpora además la monografía del cristal temporal
aperiódico de 775 páginas, capítulo 7, y la revisión de constantes y electrón
del 8 de septiembre, páginas 39–47 y 62–75 del corte de 81 páginas, SHA-256
`10de8e3fff9b8af99feb7224703149d643dfeb56e175d50ebf496bf4478e414b`.
Las páginas aquí indicadas son las posiciones físicas de los respectivos PDF.
El archivo de compilación especializado cambió después a 88 páginas; estas
citas corresponden al corte leído y a sus secciones 6 y 8, no a una supuesta
paginación definitiva del archivo vivo.

La notación de esta sección separa dos índices: \(t\) cuenta extensiones por
sextetos tríticos; \(k\) cuenta bloques decimales efectivamente emitidos.
Los mapas se aplican a la trayectoria conjunta seleccionada. No se reemplaza
su dominio por el producto de los tres conjuntos de continuaciones marginales.

### 15.1. Desplazamientos de las ventanas y actualización agregada

Sean \(B=1000\), \(a=3^6=729\) y
\[
\rho=\log_B a,\qquad K_t=\lfloor(t+1)\rho\rfloor,\qquad
\Delta_t=K_{t+1}-K_t\in\{0,1\}.
\]
El calendario es la realización posterior de la comparación de capacidades
ternaria y decimal. Para cada canal \(c\in\{\pi,e,\varphi\}\), sean \(T_{c,t}\)
el entero de su prefijo de \(6t\) trits y \(D_{c,t}\) el entero de su prefijo
de \(K_t\) bloques decimales. La monografía define
\[
\Omega_t=\frac{a^{t+1}}{B^{K_t}},\qquad
\xi_{c,t}=D_{c,t}\Omega_t-aT_{c,t}.
\tag{29}
\]
La ventana de extensiones que intersectan ambos cilindros es exactamente
\[
I_{c,t}=
[\lfloor\xi_{c,t}\rfloor,\,
 \lceil\xi_{c,t}+\Omega_t\rceil-1]_{\mathbb Z}
\cap\{0,\ldots,a-1\}.
\tag{30}
\]
El origen es la intersección de intervalos semiabiertos, con desigualdades
estrictas en los extremos opuestos. La anchura \(\Omega_t\) es común; los
desplazamientos \(\xi_{c,t}\) retienen los prefijos de cada canal.

Escribamos \(u_{c,t}\in\{0,\ldots,a-1\}\) para la extensión trítica elegida y
\(d_{c,t}\) para el nuevo bloque decimal cuando \(\Delta_t=1\); fijemos
\(d_{c,t}=0\) cuando \(\Delta_t=0\). Las actualizaciones son
\[
T_{c,t+1}=aT_{c,t}+u_{c,t},\qquad
D_{c,t+1}=B^{\Delta_t}D_{c,t}+d_{c,t},\qquad
\Omega_{t+1}=aB^{-\Delta_t}\Omega_t.
\]
Sustituirlas en (29) da la identidad exacta
\[
\boxed{\xi_{c,t+1}
 =a\xi_{c,t}+\Omega_{t+1}d_{c,t}-a u_{c,t}.}
\tag{31}
\]
En efecto,
\[
(B^{\Delta_t}D_{c,t}+d_{c,t})
 aB^{-\Delta_t}\Omega_t-a(aT_{c,t}+u_{c,t})
 =a(D_{c,t}\Omega_t-aT_{c,t})
  +\Omega_{t+1}d_{c,t}-a u_{c,t}.
\]
Por tanto, para la combinación orientada
\(\xi_{\Sigma,t}=\xi_{\pi,t}+\xi_{e,t}-\xi_{\varphi,t}\), y análogamente
\(u_{\Sigma,t}\) y \(d_{\Sigma,t}\),
\[
\boxed{\xi_{\Sigma,t+1}
 =729\xi_{\Sigma,t}+\Omega_{t+1}d_{\Sigma,t}
   -729u_{\Sigma,t}.}
\tag{32}
\]
En una emisión, \(d_{\Sigma,t}=P_k+E_k-\Phi_k\), con \(k=K_{t+1}\).
En una vacancia de capacidad, ese término es cero y la extensión trítica
y el desplazamiento siguen evolucionando.

Las fórmulas (31)–(32) son identidades de la trayectoria ya seleccionada,
no una afirmación de que \(\xi_\Sigma\) determine por sí sola la siguiente
extensión. Conservan el agregado de los residuos sin descartar las
restricciones regionales ni la incidencia conjunta.

### 15.2. Información conservada por la prolongación excepcional

El integral y la revisión especializada construyen, sobre el mismo prefijo,
\[
Q_n(x)=
\bigl(f_j,\gamma_{f_jA_Wf_j^{-1}}(w_j)\bigr)_{j<n},
\qquad
\gamma_A(w)=(w,wA),
\]
con marcos transportados causalmente y
\(r_{n,m}Q_n=Q_mp_{n,m}\). El gráfico conserva la palabra visible mediante
su primera proyección. En una carta fija, la codificación símbolo a símbolo
\(w\mapsto(w,wA_W)\) induce una biyección entre sus lenguajes de bloques,
de modo que
\[
p_{\gamma(w)}(n)=p_w(n).
\tag{33}
\]
Con marcos variables retenidos se conserva al menos la recuperación del
bloque visible desde el bloque codificado correspondiente.

La transformación integral reversible del registro firmado produce \(K\);
los soportes regionales y el signo anterior al acarreo determinan la bandera
marcada de Witt. La selección de componente, el pegado ternario y el vecino
reticular conducen después a Leech y a la realización de \(V^\natural\).
Estas operaciones conservan dominios distintos: el valor \(\alpha_A\), el
registro \(K\), el soporte negativo y el vector reticular no se identifican.

En el argumento siguiente, la incidencia interviene en la admisibilidad de
la trayectoria completa. Se cuentan sólo las palabras agregadas que esa
trayectoria realiza, con todos sus transportes conservados. La igualdad
(33) explica por qué una codificación reversible de incidencia conserva
complejidad visible; la reducción de complejidad que se busca concierne
específicamente al agregado \(P+E-\Phi\).

### 15.3. Acoplamiento del cociclo de memoria con la graduación excepcional

El integral, páginas físicas 1714–1715, sección 97.3.2, compone el transporte
entre niveles cilíndricos con la representación espectral del cociclo. Para
un descendiente enriquecido \(z'\) de \(z\), \(\tau z'=z\), la aplicación es
\[
\widetilde U_k(e_z\otimes v)=
\sum_{\tau z'=z}
\sqrt{\frac{\mu_{k+1}(z')}{\mu_k(z)}}\,
e_{z'}\otimes C_W^{q_{\rm mem}(z')-q_{\rm mem}(z)}v.
\]
Aquí \(\mu_k\) son los pesos proyectivos del transporte construido,
\(q_{\rm mem}\) es el cociclo entero de memoria y \(C_W\) es su realización
unitaria espectral. Para
\(G_k(e_z\otimes v)=e_z\otimes C_W^{q_{\rm mem}(z)}v\), se verifica
\[
\widetilde U_k=G_{k+1}(U_k\otimes I)G_k^*.
\]
La identidad conserva el soporte de descendientes de peso positivo y
transporta su memoria; no identifica los estados de una misma fase.

Sobre la realización graduada del mismo desarrollo, el integral, páginas
1729–1730, sección 97.7, define el proyector
\[
\Pi_{\chi_{\rm exc}}=
\sum_{n\ge0}|n\rangle\langle n|\otimes I_{\mathcal H_W}
\otimes P_n^\natural.
\]
Su acción sobre memoria \(n\) y grado excepcional \(r\) es
\(\delta_{nr}\). Por tanto, el acoplamiento conserva un índice común entre
memoria y graduación de \(V^\natural\); las dos realizaciones no se
reemplazan por un producto independiente. Para un grado admitido, la fórmula
del proyector no distingue los bloques decimales de los descendientes.

El apéndice O, página 2231, expresa la compatibilidad como equivariancia:
\[
P_{\rm rad}^{\rm enr}(\Gamma_9\gamma)
=\widehat\Gamma_{9,\rm rad}P_{\rm rad}^{\rm enr}(\gamma).
\]
La página 2228 conserva simultáneamente
\(q_9(N+9)=q_9(N)+1\). En consecuencia, el análisis de repeticiones del
lector agregado debe mantener el operador inducido
\(\widehat\Gamma_{9,\rm rad}\); sustituirlo por la identidad eliminaría el
incremento de memoria. Las cotas siguientes se refieren a las emisiones de
esta trayectoria conjunta, sin identificar retorno de fase con retorno de
estado ni con igualdad de palabras agregadas.

## 16. Criterio de complejidad relativa al reloj sobre la trayectoria conjunta

Esta sección contiene una implicación demostrada. La cota que figura como
hipótesis del teorema 9 no se da por establecida para la trayectoria HMT.

Fijemos \(q\ge2\) y el reloj
\[
g_t=K_t\bmod q,\qquad \zeta_t=(g_t,\Delta_t).
\]
La representación rotacional demostrada en el capítulo 7 de la monografía
del cristal da
\[
p_\zeta(m)=q(m+1).
\tag{34}
\]
También se obtiene desde \(p_g(m)=qm\): como
\(g_{t+1}=g_t+\Delta_t\bmod q\) y \(\Delta_t\in\{0,1\}\), una palabra
de longitud \(m\) en \(\zeta\) equivale a una de longitud \(m+1\) en \(g\).
La irracionalidad de \(\rho\) asegura la distinción de los extremos de la
partición rotacional. La fórmula cuenta el reloj, no el estado completo.

Decórese cada paso con
\[
v_t=
\begin{cases}
d_{\Sigma,t},&\Delta_t=1,\\
\bot,&\Delta_t=0,
\end{cases}
\]
donde \(\bot\) es un símbolo distinto del entero cero. Eliminar los símbolos
\(\bot\) de esta sucesión produce
\[
t_k=P_k+E_k-\Phi_k.
\]
Para una palabra \(U\) de longitud \(m\) del reloj, definamos
\[
N_m(U)=
\#\{V:\ \exists j\ge0,\ 
 \zeta_{j:j+m-1}=U,\ v_{j:j+m-1}=V\},
\]
y su multiplicidad media
\[
\overline M(m)=
\frac{1}{q(m+1)}
\sum_{U\in\mathcal L_m(\zeta)}N_m(U).
\tag{35}
\]
El cuantificador recorre posiciones de la trayectoria regional completa,
no elecciones independientes de los canales ni todas las palabras del
ambiente ternario. Distintas historias que dan el mismo bloque agregado
se cuentan una sola vez en \(N_m(U)\).

**Lema 9.1 (Borrado de vacancias).** Para todo \(n\ge1\),
\[
\boxed{p_t(n)\le q(2n+1)\overline M(2n).}
\tag{36}
\]

**Demostración.** Como \(\rho>1/2\),
\[
K_{j+2n}-K_j\ge\lfloor2n\rho\rfloor\ge n.
\]
Todo intervalo de \(2n\) pasos contiene, por tanto, al menos \(n\) emisiones.
Cada bloque de \(n\) letras de \(t\) comienza en un paso de emisión y se
recupera borrando \(\bot\) de la palabra decorada de longitud \(2n\) que
comienza allí, y tomando sus primeras \(n\) letras restantes. Esta operación
es determinista. El número de palabras decoradas con su reloj es exactamente
\(\sum_U N_{2n}(U)=q(2n+1)\overline M(2n)\), que da la cota. \(\square\)

**Lema 9.2 (Normalización dodecafásica).** Sea \(A\) la expansión canónica de
\(\alpha_A\). Entonces
\[
p_A(n)\le60p_t(n).
\tag{37}
\]

**Demostración.** Un bloque de \(t\), una de las doce fases de \(K\) y el
acarreo entrante por su extremo derecho determinan, de derecha a izquierda,
el bloque \(A\) mediante división euclídea. El acarreo pertenece al conjunto
de cinco elementos \(\{-2,-1,0,1,2\}\), establecido para la normalización
completa. Cada bloque real de \(A\) procede de uno de esos datos; algunos
datos pueden no realizarse, lo que sólo reduce el conteo. Por ello hay a lo
sumo \(12\cdot5=60\) bloques normalizados por bloque de \(t\). \(\square\)

**Teorema 9 (Criterio de multiplicidad media).** Si la trayectoria conjunta
satisface
\[
\boxed{\liminf_{n\to\infty}\overline M(2n)<\infty,}
\tag{38}
\]
entonces \(e+\pi\) es irracional.

**Demostración.** (36)–(38) implican
\(\liminf_{n\to\infty}p_A(n)/n<\infty\). Por otra parte, la identidad completa
del lector es
\[
e+\pi=4+\varphi+\kappa_{\rm per}+\alpha_A,\qquad
\kappa_{\rm per}\in\mathbb Q.
\]
Si \(e+\pi\) fuese racional, \(\alpha_A\) pertenecería a
\(\mathbb Q-\varphi\) y sería algebraico irracional de grado dos. El
teorema 1 de Adamczewski–Bugeaud exige que su complejidad en base \(1000\)
satisfaga \(\liminf p_A(n)/n=+\infty\), contradicción. \(\square\)

Fuente primaria del resultado aritmético empleado después de la construcción:
[Adamczewski–Bugeaud, *On the complexity of algebraic numbers I. Expansions
in integer bases*, Annals of Mathematics 165 (2007), teorema 1](https://annals.math.princeton.edu/wp-content/uploads/annals-v165-n2-p04.pdf).

La condición (38) es más débil que exigir un máximo uniforme de \(N_m(U)\)
para toda palabra y toda longitud. Permite multiplicidades grandes en
algunas fibras siempre que su media permanezca acotada en una sucesión
cofinal de longitudes pares. La entropía nula del reloj y el retorno de
fase constituyen antecedentes de (34); no se han utilizado como sustitutos
de (38).

## 17. Alcance preciso de esta ampliación

Las fórmulas (31)–(32) y los lemas 9.1–9.2 se han deducido explícitamente.
El teorema 9 transfiere una cota de multiplicidad de la trayectoria conjunta
a la irracionalidad; la demostración de esa cota para los tres lectores
regionales permanece pendiente en este trabajo.

La lectura de la revisión del 8 de septiembre confirma la definición de
\(\alpha_A\) y la diferencia entre su sección infinita y la ventana racional
de 36 cifras. Las construcciones de Hadamard, Witt, Leech y \(V^\natural\)
se mantienen en el dominio genealógico; no se introduce una acción del
Monstruo sobre cifras como sustituto de los mapas impresos.

Procedencia: las ventanas, el reloj y las construcciones de incidencia son
**RESULTADO_RECUPERADO** de las fuentes indicadas. Su composición en
(31)–(38) es **FORMALIZACION_NUEVA** dentro de esta nota; no se reivindica
prioridad histórica para identidades de cambio de base, conteo de factores
o el teorema externo de complejidad. No se ha obtenido aquí una prueba
consumada de irracionalidad de \(e+\pi\).

## 18. Realización suficiente mediante un cociente predictivo finito

Sea \(X\) el dominio de estados enriquecidos efectivamente recorridos por la
trayectoria conjunta y sus desplazamientos, \(F:X\to X\) su sucesor,
\(a:X\to\mathcal A\) el símbolo del reloj de la sección 16 y
\(b:X\to\mathcal B\cup\{\bot\}\) la emisión agregada decorada. El símbolo
del reloj incluye la indicación de emisión \(\Delta(a)\).

**Proposición 10.** Supóngase construido un conjunto finito \(Q\), una
aplicación \(q:X\to Q\) y funciones \(\delta,o\) tales que, sobre todos los
pares alcanzables,
\[
q(Fx)=\delta(q(x),a(x)),\qquad b(x)=o(q(x),a(x)),
\qquad o(q,a)=\bot\ \Longleftrightarrow\ \Delta(a)=0.
\tag{39}
\]
Entonces \(N_m(U)\le|Q|\) para toda longitud \(m\) y palabra de reloj
\(U\). En particular, se cumple la hipótesis del teorema 9.

**Demostración.** Fijados \(U=a_0\cdots a_{m-1}\) y un estado inicial
\(q_0\in Q\), las recurrencias
\(q_{j+1}=\delta(q_j,a_j)\) y \(b_j=o(q_j,a_j)\) determinan una sola
palabra agregada decorada. Las elecciones no realizables se descartan;
las que producen la misma palabra se cuentan una sola vez. Existen como
máximo \(|Q|\) palabras. \(\square\)

Para una aplicación \(q\) propuesta, (39) equivale a comprobar
\[
q(x)=q(x'),\ a(x)=a(x')
\quad\Longrightarrow\quad
b(x)=b(x'),\quad q(Fx)=q(Fx').
\tag{40}
\]
Esto define un cociente para el comportamiento del lector agregado, no una
identificación de las genealogías completas.

Una construcción por niveles finitos es suficiente si dispone de cocientes
\(q_n:X_n\to Q_n\), mapas inducidos \(\sigma_{n,m}\) y transductores
\(\delta_n,o_n\), compatibles con truncamientos \(r_{n,m}\), con el
mismo paso temporal y con las etiquetas de reloj:
\[
q_mr_{n,m}=\sigma_{n,m}q_n,
\qquad
\sigma_{n,m}\delta_n(z,a)=\delta_m(\sigma_{n,m}z,a),
\qquad o_n(z,a)=o_m(\sigma_{n,m}z,a).
\tag{41}
\]
Si además \(\sup_n|Q_n|\le M<\infty\), entonces
\(|\varprojlim Q_n|\le M\): de existir \(M+1\) elementos distintos del
límite, algún nivel común distinguiría los \(M+1\), contradicción. Así se
obtiene (39) y la cota \(N_m(U)\le M\).

La naturalidad de los mapas de incidencia recuperados en la sección 15
aporta compatibilidad de los datos conservados. Para aplicar esta proposición
se requieren además (40) y el control uniforme del número de estados
predictivos. La construcción de ese cociente para el agregado HMT no está
establecida en esta nota; tampoco se identifica con los cocientes finitos
de fase de la monografía del cristal.

## 19. Criterio elemental mediante retornos cuantificados y norma cuadrática

Este criterio utiliza directamente la recurrencia de acarreo y la ecuación
de la coordenada áurea ya construida. Sean
\[
T_N=\sum_{k=1}^N t_kB^{N-k},\qquad T_0=0,\qquad
x=\sum_{k\ge1}t_kB^{-k}.
\]
La identidad (3) y la acotación del acarreo dan
\(\alpha_A=x-\kappa-c_1\). Para \(r\ge0\), \(s\ge1\) y \(12\mid s\),
definamos
\[
Q=B^{r+s}-B^r,\qquad
P=T_{r+s}-T_r-Q(\kappa+c_1).
\]
Se tiene \(Q>0\) y \(P\in\mathbb Z\), porque
\(\kappa=M_K/(B^{12}-1)\) y \(B^{12}-1\mid B^s-1\). Separar el prefijo
de la cola de \(x\) en los dos índices produce exactamente
\[
Q\alpha_A-P
=\sum_{k\ge1}(t_{r+s+k}-t_{r+k})B^{-k}.
\tag{42}
\]
Puesto que \(-999\le t_k\le1998\), la coincidencia de ambas colas
durante \(\ell\) posiciones implica
\[
|Q\alpha_A-P|\le3B^{-\ell}.
\tag{43}
\]

**Teorema 11.** Si existen \((r_j,s_j,\ell_j)\), con \(12\mid s_j\),
tales que
\[
t_{r_j+s_j+k}=t_{r_j+k}\quad(1\le k\le\ell_j),
\qquad \ell_j-(r_j+s_j)\longrightarrow+\infty,
\tag{44}
\]
entonces \(e+\pi\) es irracional.

**Demostración.** (43) y \(Q_j<B^{r_j+s_j}\) implican
\(Q_j|Q_j\alpha_A-P_j|\to0\). Supóngase \(S=e+\pi\in\mathbb Q\).
Por (4), \(\alpha_A=a/d-\varphi\), con \(a\in\mathbb Z\),
\(d\ge1\). Para enteros \(P,Q\), \(Q>0\), sean
\(\epsilon=Q\alpha_A-P\) y \(m=Qa-dP\). La ecuación
\(\varphi^2-\varphi-1=0\) da la norma entera no nula
\[
N(m-dQ\varphi)=m^2-mdQ-d^2Q^2\in\mathbb Z\setminus\{0\}.
\]
El conjugado de \(\epsilon\) es \(\epsilon+Q\sqrt5\); por tanto
\[
|\epsilon|\,|\epsilon+Q\sqrt5|\ge d^{-2}.
\]
Si \(|\epsilon|\le1\), se deduce
\(Q|\epsilon|\ge[d^2(1+\sqrt5)]^{-1}\). Si
\(|\epsilon|>1\), la misma cota vale inmediatamente. Esta cota positiva
uniforme contradice el límite anterior. \(\square\)

Un retorno exacto de ambas colas infinitas es también suficiente: (42)
da \(\alpha_A=P/Q\in\mathbb Q\), y (4) hace entonces a \(S\)
cuadrático irracional.

El teorema 11 no utiliza un teorema de trascendencia ni una hipótesis sobre
la complejidad de todos los bloques. Requiere el régimen cuantificado (44),
que no se ha deducido aquí de la holonomía nonádica. El retorno de fase y
la conservación de memoria recuperados en 15.3 permanecen diferenciados
de la coincidencia del observable exigida en (44). Estos criterios no
constituyen una prueba consumada de la irracionalidad de \(e+\pi\).

## 20. Definición HMT de número y cociente de futuros del lector de la suma

La lectura directa de las páginas físicas 972–1002 del integral de 2.249
páginas recupera las definiciones y pruebas del capítulo 53 hasta el cierre
genealógico y su enlace con el atlas. Las páginas físicas 354–355 recuperan,
además, el teorema 8.44 y la definición de número de 8.5.7. Los localizadores
que siguen emplean la **paginación impresa**, una unidad menor que la física.

### 20.1. Clasificación recibida del tratado

Las definiciones 53.15, 53.19 y 53.22 fijan un número HMT como una sección
compatible \(\boldsymbol x\) del sistema inverso de estados supervivientes.
El par \((\boldsymbol x,L)\) es su presentación y
\(\operatorname{Val}_L(\boldsymbol x)\) su evaluación. La definición
conserva la genealogía antes de efectuar el cociente por igualdad de valor.

La tabla 53.1, p. 987, y los apartados 53.14 y 53.16.4 distinguen:

- entero: representación ternaria balanceada finita, con signo y magnitud;
- racional periódico: expansión canónica finalmente periódica;
- racional monodrómico: valor racional con evolución adicional de la fibra
  enriquecida, invisible para ese lector;
- irracional coinductivo: cilindros compatibles que determinan un valor cuya
  expansión canónica es no finalmente periódica;
- algebraico: evaluación que anula un polinomio entero no nulo;
- trascendente: evaluación para la que se excluye todo polinomio entero no
  nulo mediante la demostración correspondiente;
- distinguido HMT: sección seleccionada por un predicado estructural de
  fibra, frontera, supervivencia, simetría o cierre. Este atributo es
  transversal a las clases aritméticas.

El teorema 53.17 y el corolario 53.18, p. 984, prueban la implicación desde
una órbita no eventualmente periódica hacia una lectura irracional cuando
el lector separa sus colas. El apartado 53.16.4, p. 996, aplica expresamente
la definición de objeto compuesto a \(e+\pi\) y conserva las dos
genealogías de sus operandos. Estos resultados se reciben completos, con la
condición de observabilidad que contienen sus demostraciones.

### 20.2. Clasificación exacta por futuros de la suma normalizada

En el estado conjunto ya construido sean \(P_k,E_k\) los bloques de los
dos lectores regionales y \(w_k=P_k+E_k\). Definamos, después de generar
ambas secciones,
\[
z_k=\sum_{j\ge0}w_{k+j}B^{-j-1},\qquad
h_k=\lfloor z_k\rfloor,\qquad r_k=z_k-h_k.
\]
Cada cola canónica de un operando pertenece a \([0,1)\); por tanto
\(0\le z_k<2\), \(h_k\in\{0,1\}\) y \(r_k\in[0,1)\). La identidad
\(Bz_k=w_k+z_{k+1}\) proporciona
\[
b_k:=w_k+h_{k+1}-Bh_k=Br_k-r_{k+1}
=\lfloor Br_k\rfloor\in\{0,\ldots,B-1\}.
\tag{45}
\]
Así \((b_k)\) es la expansión canónica de la parte fraccionaria de la
suma. La construcción conserva \(P,E,h\) en el estado fuente y aplica
después el lector escalar (45); la segunda proyección sigue definida sobre
esa misma genealogía.

Sean \(\sigma\) el desplazamiento de palabras y
\[
\mathcal Q_\Sigma=
\{\sigma^n(b_1b_2\cdots):n\ge0\}.
\tag{46}
\]
Equivalentemente, dos ocurrencias temporales de la historia conjunta efectiva se
identifican en este cociente cuando el lector de la suma publica el mismo
futuro completo. El desplazamiento induce una transición determinista en
\(\mathcal Q_\Sigma\). Esta construcción generaliza a la órbita efectiva
la equivalencia de futuros del teorema 8.44, **sin presuponer que su conjunto
de clases es finito ni que estabiliza a una profundidad finita**.

**Proposición 12.** Para el lector (45),
\[
e+\pi\in\mathbb Q
\quad\Longleftrightarrow\quad
|\mathcal Q_\Sigma|<\infty.
\tag{47}
\]

**Demostración.** Si el conjunto de futuros es finito, existen
\(n<m\) con \(\sigma^n b=\sigma^m b\); de ahí
\(b_{k+m-n}=b_k\) para todo \(k\ge n+1\). El teorema 53.7 da la
racionalidad. Recíprocamente, una expansión con prefijo de longitud \(n\)
y período de longitud \(p\) tiene a lo sumo \(n+p\) futuros distintos.
El mismo teorema completa la equivalencia. \(\square\)

La proposición sitúa el criterio en la información que el lector de la
suma distingue a través de sus continuaciones. Conserva íntegramente el
estado HMT, pero permite identificar, para este observable, historias que
producen el mismo futuro. Por ello no exige demostrar que una sola lectura
escalar recupera toda la incidencia excepcional o toda la memoria de origen.

### 20.3. Conexión con los criterios ya desarrollados

Fijados un inicio \(N\ge1\) y un período candidato \(p\ge1\), la
igualdad de futuros desde esos índices equivale a la compatibilidad de
acarreo demostrada en la sección 10: para todo \(k\ge N\),
\[
w_{k+p}-w_k=B(h_{k+p}-h_k)-(h_{k+p+1}-h_{k+1}).
\tag{48}
\]
Los tres estados de diferencias, las nueve etiquetas y la obstrucción de
concatenación de aquella sección son, por tanto, una realización explícita
del criterio de clasificación HMT para el lector compuesto. No se
presentan de nuevo como un resultado descubierto en esta lectura.

El cociente **autónomo** \(\mathcal Q_\Sigma\) de (46) tampoco es el
transductor **relativo a un reloj aperiódico** de la sección 18. El primero
describe todos los futuros de la suma normalizada; el segundo describe las
salidas del residuo \(P+E-\Phi\) condicionadas a una palabra de reloj.
Un transductor relativo finito puede recibir infinitos futuros distintos
del reloj. Ambas afirmaciones preservan sus objetos y sus cuantificadores.

La clasificación se incorpora como criterio efectivo de la preparación del
artículo. Para asignar la clase «irracional coinductivo» a la suma concreta
se debe establecer la infinitud de (46), por ejemplo excluyendo (48) para
toda cola y período, o aplicar el criterio suficiente de la sección 19.
La definición general y sus ejemplos no asignan por sí solos esa clase a
la trayectoria seleccionada. Tampoco la clase «distinguido HMT» implica
trascendencia.

**Procedencia.** Definiciones y clasificación: **RESULTADO_RECUPERADO** del
capítulo 53; cociente predictivo: **RESULTADO_RECUPERADO** de 8.5.6. La
especialización explícita (45)–(47) reúne estos antecedentes para el lector
de la suma. La ecuación (48) recupera la sección 10 de esta misma nota. Se
conservan los criterios anteriores y su alcance; esta incorporación no
declara demostrada la irracionalidad de \(e+\pi\).

## 21. Composición efectiva del agregado: reducción trítica, acarreo y residuo decimal

Se compone el funcional firmado \((1,1,-1)\) sobre las tres secciones
regionales de la misma trayectoria. El intercambio especular de los dos
primeros canales queda eliminado porque
\((1,1,-1)\cdot(1,-1,0)=0\). La componente diagonal permanece, pues
\((1,1,-1)\cdot(1,1,1)=1\). Esta cancelación particular conserva la
dependencia respecto de la coordenada áurea y de la memoria conjunta.

### 21.1. Transporte entero de las extensiones tríticas

En el calendario finito \(L_0,L_0,L_1,L_1\), sean
\(w_\chi\in\{0,1,2\}^6\) los representantes de los tres canales y
\[
v=w_\pi+w_e-w_\varphi=S+3c,\qquad S=[v]_3,
\qquad c\in\{-1,0,1\}^6.
\]
Para la matriz activa \(L\), la reducción individual escribe
\[
w'_\chi=w_\chi L-3q_\chi,\qquad
q_\chi=\left\lfloor\frac{w_\chi L}{3}\right\rfloor,
\]
con piso componente a componente. Sustituyendo las tres ecuaciones,
\[
\boxed{
S'=[SL]_3,\qquad
c'=cL+\left\lfloor\frac{SL}{3}\right\rfloor
 -(q_\pi+q_e-q_\varphi).
}
\tag{49}
\]
La primera componente tiene 729 valores posibles. La segunda conserva
la diferencia entre reducción modular y agregado entero; su último término
procede de las tres reducciones efectivas.

Para \(\nu(a)=\sum_{i=1}^6a_i3^{6-i}\),
\[
u_\Sigma=\nu(v)=\nu(S)+3\nu(c).
\tag{50}
\]
En los cinco bloques de la trayectoria finita publicada,
\[
\begin{aligned}
u_\Sigma&=(176,220,-34,126,551),\\
\nu(S)&=(419,211,209,42,542),\\
3\nu(c)&=(-243,9,-243,84,9).
\end{aligned}
\]
Estas igualdades evalúan conjuntamente las tres filas regionales; no toman
continuaciones independientes. La fuente es
[generacion.tex, transporte finito](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_AMPLIACION_20260908/sections/generacion.tex:46>).
El calendario indicado termina en \(w_{30}\). Su continuación efectiva
se recibe de \(R_{36}\); repetir indefinidamente aquellas cuatro matrices
cambiaría el generador.

### 21.2. Residuo escalar y acarreo trivalente

Escribamos \(x_\pi=\pi-3\), \(x_e=e-2\), \(x_\varphi=\varphi-1\)
para las valoraciones ya producidas por los lectores. Para \(k\ge0\),
\[
R_k=\{B^kx_\pi\}+\{B^kx_e\}-\{B^kx_\varphi\},
\qquad -1<R_k<2.
\]
La división euclídea de cada canal, sumada con signos \(+,+,-\), da
\[
\boxed{t_{k+1}=BR_k-R_{k+1}.}
\tag{51}
\]
Sean \(h_k=\lfloor R_k\rfloor\in\{-1,0,1\}\) e
\(y_k=R_k-h_k\). El lector normalizado satisface exactamente
\[
\boxed{
b_{k+1}=t_{k+1}+h_{k+1}-Bh_k=\lfloor By_k\rfloor,
\qquad y_{k+1}=\{By_k\}.
}
\tag{52}
\]
**Prueba.** Sustituir \(R_k=h_k+y_k\) en (51) produce
\(By_k=t_{k+1}+h_{k+1}-Bh_k+y_{k+1}\), con
\(0\le y_{k+1}<1\). La división euclídea determina (52). \(\square\)

Se han reducido las tres valoraciones a un residuo escalar y un acarreo
trivalente. Esta reducción es posterior al estado enriquecido: la historia y
la incidencia de los tres canales se conservan en el antecedente de ambos
lectores. La ecuación escalar multiplica por \(B\) en cada intervalo de
continuidad; no incorpora por sí misma una contracción del residuo.

Para dos ocurrencias con desplazamiento \(s\),
\(E_i=R_{r+s+i}-R_{r+i}\) satisface
\[
t_{r+s+i+1}-t_{r+i+1}=BE_i-E_{i+1}\in\mathbb Z.
\tag{53}
\]
Por tanto,
\[
\max_{0\le i\le L}|E_i|<\frac1{B+1}
\quad\Longrightarrow\quad
t_{r+s+k}=t_{r+k}\quad(1\le k\le L).
\tag{54}
\]
En efecto, el entero de (53) tiene módulo estrictamente menor que uno.
En sentido inverso, si coinciden esos \(L\) símbolos, (53) implica
\(E_L=B^LE_0\), y la cota \(|E_L|<3\) da
\(|E_0|<3B^{-L}\).

### 21.3. Composición con el reloj de vacancias

Sea \(K_j\) el número de emisiones decimales acumuladas en la frontera
\(j\). La palabra \(\Delta_j=K_{j+1}-K_j\) determina los instantes de
emisión. Se mantiene la decoración de la sección 16: \(v_j=\bot\)
si \(\Delta_j=0\), y \(v_j=t_{K_{j+1}}\) en una emisión. Eliminar
\(\bot\) produce exactamente \(t\).

Dos ventanas iguales de \(v\), de longitud \(L\), comienzos \(j\)
y \(j+d\), producen un retorno de \(t\) con
\[
r=K_j,\qquad s=K_{j+d}-K_j,\qquad
\ell=K_{j+L}-K_j.
\tag{55}
\]
La igualdad de la palabra de vacancias asegura que ambas ventanas contienen
las mismas posiciones de emisión. La igualdad de los contenidos en esas
posiciones da la coincidencia de los \(\ell\) términos de \(t\).
La repetición adicional de \(K_j\bmod12\) asegura \(12\mid s\).
La cantidad de la sección 19 queda convertida sin pérdida en
\[
\ell-r-s=K_{j+L}-K_j-K_{j+d}.
\tag{56}
\]

La composición se ha aplicado al prefijo ya certificado. En los pasos
\(j=0\) y \(j=12\), el reloj \((K_j\bmod12,\Delta_j)\) vale
\((0,1)\), mientras los contenidos emitidos son respectivamente
\(t_1=241\) y \(t_{13}=234\). Este par descarta que el contenido sea
función sólo de ese estado instantáneo del reloj. No descarta una reducción
que conserve más memoria, ni un régimen de retornos a otras longitudes.

## 22. Retornos compensados por acarreo y aplicación del transductor

La composición permite debilitar la coincidencia cruda exigida por (44).
Se conserva la identidad (42), pero se admite que sus diferencias sean
compensadas por una trayectoria de acarreo entera y acotada. Esta
especialización reúne el núcleo de valoración de la sección 4 con el
criterio de retorno de la sección 19; no se atribuye novedad histórica al
lema general de telescopía.

Para \(12\mid s\), sean \(Q,P\) los enteros de la sección 19 y
\[
d_k=t_{r+s+k}-t_{r+k},\qquad |d_k|\le3(B-1).
\]
Supongamos que durante \(\ell\) posiciones existe un **acarreo
compensador** \(H_1,\ldots,H_{\ell+1}\in\{-3,-2,-1,0,1,2,3\}\)
tal que
\[
d_k=BH_k-H_{k+1}\quad(1\le k\le\ell).
\tag{57}
\]
Se distingue \(H\) tanto del acarreo original \(c\) de \(\alpha_A\)
como del acarreo \(h\) de (52).

**Proposición 13.** La condición (57) implica
\[
\boxed{|Q\alpha_A-(P+H_1)|\le6B^{-\ell}.}
\tag{58}
\]
En consecuencia, una sucesión de tales caminos efectivos con
\(\ell-r-s\to+\infty\) demuestra la irracionalidad de \(e+\pi\).

**Demostración.** La parte finita de (42) telescopa:
\[
\sum_{k=1}^{\ell}d_kB^{-k}=H_1-H_{\ell+1}B^{-\ell}.
\]
De ello se deduce
\[
Q\alpha_A-(P+H_1)
=B^{-\ell}\left(
\sum_{j\ge1}d_{\ell+j}B^{-j}-H_{\ell+1}\right).
\]
La suma entre paréntesis tiene módulo a lo sumo seis. Como
\(P+H_1\in\mathbb Z\) y \(Q<B^{r+s}\),
\[
Q|Q\alpha_A-(P+H_1)|<6B^{r+s-\ell}\longrightarrow0.
\]
La norma cuadrática del teorema 11 excluye que \(e+\pi\) sea racional.
\(\square\)

Las coincidencias de (44) se recuperan con \(H_k=0\). Se admiten ahora
también diferencias no nulas: por ejemplo, las etiquetas alternadas
\(B+1,-B-1\) corresponden al ciclo \(1,-1,1\). El nuevo criterio
no presupone igualdad de los bloques antes del acarreo.

En base mil, las aristas \((H,H')\mapsto1000H-H'\), restringidas a
\(|d|\le2997\), son exactamente 37. Las cinco fuentes
\(-2,-1,0,1,2\) admiten siete destinos; las fuentes \(-3\) y \(3\)
admiten sólo el destino idéntico. Cada etiqueta determina unívocamente su
arista: de \(B(H-\widetilde H)=H'-\widetilde H'\) y
\(|H'-\widetilde H'|\le6<B\) se sigue igualdad de ambas fuentes y
destinos. La composición se comprueba mediante concatenación de aristas,
no por una búsqueda sobre valores racionales objetivo.

El ejecutable existente `verificar_obstruccion_periodica_suma.py`, con
`--aggregate-returns`, comprueba 4687 trayectorias de cinco estados, sus
identidades racionales de telescopía y 27 ternas racionales para (51)–(52).
Conserva además los 264 casos anteriores. Sobre los 333 bloques completos
ya certificados por canal, se han examinado 4455 pares de comienzo y
desplazamiento decimal positivo múltiplo de doce. Hay 24 coincidencias
compensadas no vacías; el mayor exceso observado es \(-40\), para
\((r,s,\ell)=(5,36,1)\). La coincidencia cruda con mayor exceso en
esa ventana tiene \((112,60,1)\) y exceso \(-171\).

Estos controles aplican el transductor a la trayectoria disponible y
verifican la ampliación del criterio sin generar nuevas cifras. No prueban
ni refutan su régimen asintótico. Quedan construidos (49)–(58), la
normalización del agregado, el transporte de índices y el algoritmo de
retornos compensados. La existencia de una sucesión de esos retornos con
exceso divergente no se ha demostrado para la trayectoria HMT completa.

**Procedencia.** Matrices, regiones, reloj y lectores:
**RESULTADO_RECUPERADO** de los propietarios indicados. Transporte explícito
del acarreo firmado y composición de (49)–(58): **FORMALIZACION_NUEVA**
en esta nota. La prueba reutiliza los lemas de las secciones 4 y 19.
Verificaciones exactas añadidas al ejecutable anterior:
**CERTIFICADO_NUEVO**, de alcance algebraico y finito, no certificado de
irracionalidad.

## 23. Composición directa de los intervalos regionales y altura de sus extremos

Se ha examinado también una aplicación que prescinde de coincidencias de
palabras. Los tres lectores exactos del generador producen intervalos
racionales de anchura menor que \(T^{-1}\). Su composición correcta es
\[
L_\alpha=L_\pi+L_e-U_\varphi-4-\kappa,
\qquad U_\alpha=U_\pi+U_e-L_\varphi-4-\kappa,
\tag{59}
\]
con \(L_\alpha<\alpha_A<U_\alpha\) y anchura menor que \(3/T\).
El signo negativo del canal áureo invierte sus extremos. Por ello
\[
\alpha_A-L_\alpha=(\pi-L_\pi)+(e-L_e)+(U_\varphi-\varphi)
\tag{60}
\]
es una suma de tres errores positivos. La composición conserva todos los
canales, pero en estos extremos concretos sus errores no se cancelan.

Puede determinarse rigurosamente una familia de extremos cuya altura
impide aplicar directamente la norma cuadrática de la sección 19. Se
recibe \(q=239\) de la compensación angular producida por las cinco
regiones; no se elige a partir de una aproximación objetivo. Para \(N\)
par, definamos
\[
A_p(N)=\sum_{j=0}^{N-1}\frac{(-1)^j}{(2j+1)p^{2j+1}},\qquad
a_p(N)=\frac1{(2N+1)p^{2N+1}}.
\]
El lector circular implementado en
[generar_desde_estructura.py](</Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py:427>)
proporciona
\[
L_\pi(N)=16A_5(N)-4(A_q(N)+a_q(N)),\qquad
W_N=U_\pi(N)-L_\pi(N)=16a_5(N)+4a_q(N).
\]
Tomemos \(N=2q^h\) y
\(T_N=\lfloor(2W_N)^{-1}\rfloor\). Para \(h\) suficientemente grande,
\[
\frac1{4W_N}\le T_N\le\frac1{2W_N},\qquad
W_NT_N<1<W_{N-2}T_N.
\]
La última desigualdad usa \(W_{N-2}/W_N>5^4\). Por tanto, el
lector se detiene exactamente en \(N\), y
\(T_N\asymp N5^{2N}\).

**Proposición 14.** Si el extremo inferior compuesto se escribe reducido
como \(L_\alpha(T_N)=P_N/Q_N\), entonces
\[
Q_N|Q_N\alpha_A-P_N|\longrightarrow+\infty
\tag{61}
\]
sobre esta subsecuencia de precisiones.

**Demostración.** En \(A_q(N)+a_q(N)\), el último denominador posee
valoración \(q\)-ádica \(2N+1\), porque \(2N+1=4q^h+1\).
Es el máximo único. En efecto, un denominador anterior tiene la forma
\(m q^m\), \(m=2N+1-2d\), \(d\ge1\). Como
\(m<q^{h+1}\), se cumple \(v_q(m)\le h\). Si \(2d>h\),
se obtiene \(v_q(m)<2d\); si \(2d\le h\),
\(v_q(m)=v_q(2d-1)<2d\). En ambos casos
\(m+v_q(m)<2N+1\). La contribución de \(A_5(N)\) tiene
valoración denominadora \(q\)-ádica de orden \(O(\log N)\).
En consecuencia,
\[
v_q(L_\pi(N))=-(2N+1).
\]
El lector exponencial de precisión \(T_N\) se detiene en un índice
\(M\le N\) para \(N\) grande, pues \(25^N/N!\to0\).
Sus denominadores dividen \((M+1)^2M!\) y tienen valoración
\(q\)-ádica a lo sumo \(N/(q-1)+2\log_q(N+1)<N\).
Para el lector áureo, la primera parada satisface
\(F_{J-2}F_{J-1}\le T_N\). Usando \(F_{j+1}\le2F_j\),
\[
F_J\le2\sqrt{2T_N}\le C\sqrt N\,5^N<q^N
\]
para \(N\) grande. Sus dos denominadores también tienen valoración
\(q\)-ádica menor que \(N\). El denominador de \(\kappa\) es fijo.
Ninguno de estos sumandos cancela la valoración extrema circular, de modo
que \(v_q(Q_N)=2N+1\) y \(Q_N\ge q^{2N+1}\).

El resto alternado primario satisface
\[
\arctan(1/5)-A_5(N)\ge a_5(N)-a_5(N+1)
\ge\frac{24}{25}a_5(N).
\]
La contribución espejo a \(\pi-L_\pi\) es no negativa. Por (60),
\[
\alpha_A-L_\alpha
\ge\frac{384}{25(2N+1)5^{2N+1}}.
\]
Se obtiene finalmente
\[
Q_N^2(\alpha_A-L_\alpha)
\ge\frac{384}{25}\,
\frac{239^{4N+2}}{(2N+1)5^{2N+1}}\longrightarrow+\infty.
\]
\(\square\)

La proposición identifica una obstrucción de altura para esta receta de
extremos y esta subsecuencia. No excluye otras aproximaciones, ni otras
subsecuencias, ni decide la clase aritmética de la suma. Su utilidad en
la composición es precisa: convergencia certificada de cilindros y calidad
diofántica relativa al denominador son estimaciones diferentes, y aquí
ambas se han calculado desde los lectores efectivos.

**Procedencia.** Los lectores y la identidad de \(\alpha_A\) se reciben
del corpus. La estimación \(239\)-ádica se incorpora como deducción de
trabajo; su procedencia histórica permanece pendiente de auditoría.

## 24. Control exacto de la aperiodicidad bajo normalización del acarreo

El objetivo de esta sección es comprobar una implicación particular que
interviene en la aplicación: si la aperiodicidad, la complejidad lineal y
la recurrencia del reloj se conservan en dos lectores, ¿su suma normalizada
es necesariamente irracional? La respuesta a esa implicación general se
obtiene mediante una construcción exacta sobre el reloj inducido del corpus.
Los lectores auxiliares que siguen **no son** los lectores regionales de
clausura y propagación; no se modifica su definición ni se presenta el
control como modelo del conjunto de axiomas HMT.

### 24.1. Palabra inducida en los instantes de emisión

Se recibe del propietario `sections/vacancias_capacidad.tex` de la ampliación
del 8 de septiembre la capacidad
\(\mathcal C_j=\lfloor(j+1)\rho\rfloor\), con
\(\rho=\log_{10}9\), y su inverso
\[
\mathcal T(k)=\left\lceil\frac{k}{\rho}\right\rceil-1,
\qquad k\ge1.
\]
Se define exclusivamente para este control
\[
b_k=\mathcal T(k+1)-\mathcal T(k)-1,
\qquad \sigma=\rho^{-1}-1.
\tag{62}
\]
La letra \(b_k\) de esta sección no es la cifra normalizada de (45).
Como \(\rho\) es irracional y \(2/3<\rho<1\), se tiene
\(0<\sigma<1/2\), \(\sigma\notin\mathbb Q\), y
\[
b_k=\lceil(k+1)\sigma\rceil-\lceil k\sigma\rceil
=\lfloor(k+1)\sigma\rfloor-\lfloor k\sigma\rfloor\in\{0,1\}.
\]
En particular \(b_1=0\). Esta palabra mecánica es aperiódica,
uniformemente recurrente y de complejidad \(p_b(n)=n+1\). Su densidad
es \(\sigma\); la irracionalidad de esa densidad basta para excluir
periodicidad eventual. Las propiedades se obtienen de la misma partición
rotacional que se utiliza para las vacancias, ahora en el índice de emisión.

### 24.2. Dos lectores trascendentes y una suma racional

Fijada la base ya presente \(B=1000\), sean
\[
Z=\sum_{k\ge1}b_kB^{-k},\qquad
P_k^*=499+500b_k,\qquad
E_k^*=499+500b_k-b_{k+1}.
\tag{63}
\]
Los coeficientes son \(499=(B-2)/2\) y \(500=B/2\), escogidos
para este control algebraico; no son coeficientes inferidos del generador
regional HMT. Se cumple
\[
P_k^*\in\{499,999\},\qquad
E_k^*\in\{498,499,998,999\}.
\]
Sean \(X=\sum P_k^*B^{-k}\), \(Y=\sum E_k^*B^{-k}\).

**Proposición 15.** Ambos números \(X,Y\) son trascendentes. Su agregado
sin normalizar es aperiódico, de complejidad lineal, y satisface
\[
\boxed{X+Y=\frac{998}{999}.}
\tag{64}
\]

**Demostración.** La palabra de cifras de \(Z\) es la palabra mecánica
aperiódica \(b\). Por tanto \(Z\) es irracional y
\(p_Z(n)=n+1\). El teorema 1 de Adamczewski–Bugeaud, aplicado a esta
salida ya construida, da su trascendencia. La suma convergente se calcula
sin truncación:
\[
X=\frac{499}{999}+500Z,\qquad
Y=\frac{499}{999}-500Z+b_1.
\]
Son transformaciones afines racionales no constantes de \(Z\), de modo
que ambos números son trascendentes. Como \(b_1=0\), resulta (64).

La cancelación tiene una expresión de acarreo exacta. Para
\(w_k^*=P_k^*+E_k^*\),
\[
w_k^*=998+1000b_k-b_{k+1},\qquad
w_k^*+b_{k+1}-1000b_k=998.
\tag{65}
\]
El acarreo es el entero \(b_k\), conservado en el estado; la palabra
normalizada consta exclusivamente del bloque \(998\). El agregado crudo
toma los valores \(997,998,1997,1998\). Sus valores menores y mayores
que \(1000\) recuperan \(b_k\), y después la misma ecuación recupera
\(b_{k+1}\). Por ello una palabra de longitud \(n\) de \(w^*\)
equivale a una palabra de longitud \(n+1\) de \(b\), y
\(p_{w^*}(n)=n+2\). La pareja \((P^*,E^*)\) también tiene
complejidad \(n+2\). En particular, el agregado es aperiódico y la
normalización es periódica. \(\square\)

La identidad finita que acredita el paso al límite es, para todo \(N\),
\[
\sum_{k=1}^Nw_k^*B^{-k}
=\frac{B-2}{B-1}(1-B^{-N})+b_1-b_{N+1}B^{-N}.
\tag{66}
\]
El último término tiende a cero porque \(b_{N+1}\in\{0,1\}\).
No se infiere (64) de una muestra decimal: se deduce de (66) para todos
los índices.

### 24.3. Compatibilidad con el reloj cronológico

Esta construcción distingue el índice \(j\) del refinamiento y el índice
\(k\) de las emisiones. El par \((P_k^*,E_k^*)\) se publica en
\(j=\mathcal T(k)\); en las vacancias se publica \(\bot\).
Cada intervalo entre emisiones tiene longitud uno o dos. Al observar
hasta las dos emisiones siguientes se recuperan \(b_k,b_{k+1}\), usando
como máximo cuatro pasos futuros. La decoración es, por tanto, un código
local con anticipación finita del reloj de capacidad, no una identificación
de sus dos índices.

Si se conserva además la fase de capacidad módulo doce, una ventana
decorada de longitud \(m\) está determinada por una ventana de longitud
\(m+4\) del reloj \(\zeta\) de (34). En consecuencia,
\[
p_{\rm decorado}(m)\le12(m+5),
\tag{67}
\]
y su entropía topológica es cero. Registrar el índice, la fase y el
acarreo mantiene la historia y el avance de memoria. El control no requiere
reiniciar el estado cuando se repite una observación finita.

### 24.4. Aplicación y alcance del control

Queda refutada la inferencia general que deduce irracionalidad de una suma
únicamente de: generación conjunta de dos valores trascendentes, reloj
aperiódico de complejidad lineal, agregado aperiódico y conservación del
acarreo. Todas esas condiciones se cumplen en (62)–(67), pero la suma es
racional.

Esta conclusión no refuta \(e+\pi\notin\mathbb Q\), ni prueba que esa
afirmación sea independiente del corpus HMT. Para obtener una refutación
del enunciado concreto sería necesario conservar los lectores regionales
efectivos de \(\pi\) y \(e\), que no son (63). El control localiza la
obligación de la aplicación precisamente en esas identidades regionales.

También distingue por qué el teorema 9 trata \(P+E-\Phi\), y no sólo
\(P+E\). En el control, si se conserva la coordenada áurea generada y el
sello \(\kappa\), y se añaden las partes enteras \(3\) y \(2\),
\[
\alpha^*=1+\frac{998}{999}-\varphi-\kappa
\in\mathbb Q-\varphi.
\]
Se tiene \(0<\alpha^*<1\), usando
\(0<\kappa<1/4\) y \(3/2<\varphi<5/3\). Su expansión canónica es
cuadrática irracional y tiene complejidad superlineal por el mismo teorema
de Adamczewski–Bugeaud. Por (37), el agregado auxiliar
\(P^*+E^*-\Phi\) tampoco puede satisfacer la cota lineal requerida.
La baja complejidad de la pareja (63) no se traslada a ese agregado por
la sola existencia del origen común.

**Procedencia.** Reloj de capacidad e inversión: **RESULTADO_RECUPERADO**,
`ARTICULO_AMPLIACION_20260908/sections/vacancias_capacidad.tex`, apartado
«Índice de capacidad, vacancias e inducción del régimen trítico». (63)–(67):
**FORMALIZACION_NUEVA** en esta nota, especialización del núcleo de valoración
de la sección 4; no se reivindica novedad histórica. A diferencia de
§12.1, el agregado crudo no es constante. El verificador existente comprueba
(65)–(66) para todas las palabras binarias de hasta diez posiciones, con
su símbolo siguiente, en bases \(4,10,1000\): \(12\,276\) casos exactos.
La prueba infinita es la anterior; la enumeración sólo comprueba su identidad
local. La fuente externa de clasificación es el teorema 1 de
[Adamczewski–Bugeaud (2007)](https://annals.math.princeton.edu/wp-content/uploads/annals-v165-n2-p04.pdf).

## 25. Coborde aditivo y acarreo ponderado: composición y distinción exactas

El propietario
`cristal_relojes_sincronizacion.tex`, líneas 737–763, demuestra que
\(z_j-\delta\) es un coborde aditivo acotado. Una forma entera puede
obtenerse para cualquier desplazamiento \(s\ge1\). Sean
\[
J_k=\sum_{i=k+1}^{k+s}z_i-\lfloor s\delta\rfloor\in\{0,1\}.
\]
El balance de la palabra mecánica da la pertenencia indicada y
\[
d_k:=z_{k+s}-z_k=J_k-J_{k-1}.
\tag{68}
\]
Así, las diferencias desplazadas poseen una primitiva aditiva entera de
altura acotada. Se puede comprobar directamente si esta primitiva aporta
el acarreo de (57).

**Proposición 16.** Para \(B=1000\), un camino de longitud
\(\ell\ge2\) que satisface
\[
d_k=BH_k-H_{k+1},\quad |H_k|\le3,\quad |d_k|\le1
\]
debe satisfacer \(d_k=0\) para \(1\le k<\ell\).

**Demostración.** Cada ecuación da
\(B|H_k|\le|d_k|+|H_{k+1}|\le4\); como \(H_k\) es entero,
\(H_k=0\). Para \(k<\ell\), la ecuación siguiente también da
\(H_{k+1}=0\), y por tanto \(d_k=0\). \(\square\)

Para un desplazamiento fijo, la aperiodicidad de \(z\) asegura diferencias
no nulas arbitrariamente lejos. Por consiguiente, la primitiva (68) no
produce por sí sola un camino infinito de acarreo ponderado. Los factores
\(1\) y \(B\) pertenecen a identidades distintas. Esto refuta sólo la
promoción automática de ese coborde al acarreo de (57), no las identidades
del cristal ni la posibilidad de retornos cuantificados del agregado
regional efectivo.

## 26. Sustitución de la hipótesis racional en las dos vías completas de alfa

Esta vía utiliza las identidades de los lectores regionales efectivos, no
los lectores auxiliares de la sección 24. Se recibe del propietario integral
`manuscrito/sucesor_102/deltas_ley9/c31_dos_vias_alpha_y_prolongacion_nonadica.tex`
la compatibilidad completa
\[
\alpha_A=\alpha_B,\qquad
E_{21/22}=\varprojlim_m E_{21/22}^{(6+3m)},\qquad
E_{21/22}(\alpha_A)=0.
\]
Se mantiene la distinción del propietario entre este valor y la raíz
\(\xi_9\) del jet. La aplicación combina esa igualdad recibida con la
identidad de la sección 2.

### 26.1. Ecuación exacta bajo la hipótesis de racionalidad

Supóngase \(S=e+\pi\in\mathbb Q\) y defínase
\[
r=S-4-\kappa\in\mathbb Q,\qquad a=r-\varphi=\alpha_A.
\]
La hipótesis conduce exactamente a
\[
\boxed{E_{21/22}(r-\varphi)=0,\qquad 0<r-\varphi<10^{-2}.}
\tag{69}
\]
Esta sustitución conserva la vía analítica completa. Para explicitar lo
que ya determina el jet, sean \(\delta=\log_{10}(10/9)\),
\(G=E_{21/22}+\delta\) en su dominio real, y
\[
R_9(z)=-\frac74z^2+\frac{z^4}{20}-\frac{2z^5}{21}
-\frac{z^6}{46}-\frac{z^7}{120}+\frac{z^8}{45}
+\frac{2z^9}{495}.
\]
Para \(z\in I_\alpha\), se escribe
\(H_{\rm TPK}(z)=(G(z)-P_9(z))/z^{10}\). Esta notación es el
resto efectivo del lector, no una cola elegida para imponer una raíz;
al restringirse a \(z>0\), no presupone una extensión analítica a cero.
Entonces (69) equivale a
\[
\delta=2\pi a+\frac{a^3}{2\pi}+R_9(a)+a^{10}H_{\rm TPK}(a),
\qquad a=r-\varphi.
\tag{70}
\]
El carácter algebraico de \(a\) bajo esta hipótesis no vuelve algebraicos
los términos \(2\pi a\), \(a^3/(2\pi)\) ni el valor del resto. La
trascendencia de \(\delta\) sobre \(\mathbb Q\) no contradice, por sí
sola, (70), que incluye coeficientes y valores fuera de ese cuerpo.

Para excluir un candidato \(r\), un certificado evaluativo suficiente
consiste en un nivel \(m\) y una cota demostrada que satisfagan
\[
\left|E_{21/22}(r-\varphi)
       -E_{21/22}^{(6+3m)}(r-\varphi)\right|
<\left|E_{21/22}^{(6+3m)}(r-\varphi)\right|.
\tag{71}
\]
La desigualdad triangular inversa daría
\(E_{21/22}(r-\varphi)\ne0\). El cierre por esta vía requiere producir
tal exclusión para cada \(r\in\mathbb Q\) del intervalo pertinente,
o un teorema uniforme equivalente. Esta sección compone (69)–(70), pero
no establece (71) para todos esos candidatos. La nota técnica
`ARTICULO_AMPLIACION_20260908/technical/procedencia_alpha.md`, §5, conserva
el teorema de compatibilidad y delimita expresamente la transcripción de
los coeficientes de grados al menos diez y de una mayorante de su cola.
Ese límite expositivo de las fuentes focales no se convierte aquí en una
afirmación de inexistencia matemática dentro del corpus completo.

### 26.2. Invariancia de la condición aritmética al cambiar el registro racional

Sean \(K,K'\) dos registros de componentes racionales, y sean sus
lecturas periódicas \(\kappa(K),\kappa(K')\in\mathbb Q\). Manteniendo
los mismos lectores regionales, definamos
\[
\alpha(K)=S-4-\varphi-\kappa(K).
\]
Se obtiene por sustracción
\[
\alpha(K')-\alpha(K)=\kappa(K)-\kappa(K')\in\mathbb Q,
\]
y, por tanto,
\[
\boxed{\alpha(K')+\varphi\in\mathbb Q
\ \Longleftrightarrow\ \alpha(K)+\varphi\in\mathbb Q.}
\tag{72}
\]
Las reconstrucciones racionales finitas de Hadamard y las permutaciones
del registro conservan esa condición. La afirmación no supone que todo
registro racional sea un estado HMT admisible, ni que cambiar el registro
preserve la raíz del mismo lector analítico. Describe exactamente el
efecto aritmético de esa operación en la identidad de la suma. El espejo
que intercambia las dos coordenadas regionales conserva \(S\) también
de manera exacta.

**Resultado de esta aplicación.** Las ecuaciones (69)–(72) incorporan la
segunda vía completa y el registro firmado a la hipótesis de racionalidad.
No se ha derivado una contradicción. Tampoco se ha demostrado que sea
imposible deducirla del corpus; ese enunciado de imposibilidad sería otro
resultado y exigiría una prueba propia. Las identidades de la suma,
los criterios de las secciones 16 y 19 y los controles de las secciones
24–25 conservan sus alcances respectivos.

**Procedencia.** Identidad de las dos vías, jet y registros:
**RESULTADO_RECUPERADO** de los propietarios citados. Sustitución y
transformación racional: **FORMALIZACION_NUEVA** en esta nota, sin
reivindicación de novedad histórica. No se ha compilado un PDF ni
modificado las publicaciones de referencia.

## 27. Consecuencia cuártica en el lector de acción bajo la hipótesis racional

El propietario integral
`manuscrito/sucesor_102/deltas_ley9/c35_componente_adimensional_retorno.tex`
define el carácter escalar
\[
H_5=f(\alpha)+\sqrt{250\alpha/\varphi},\qquad
f(z)=-z+\frac9{16}z^2-\frac59z^3+\frac7{48}z^4-\frac1{54}z^5.
\tag{73}
\]
La residencia causal del capítulo 14 y
`ARTICULO_AMPLIACION_20260908/sections/electron.tex` conservan esta fórmula.
Se utiliza después de la generación conjunta de las coordenadas regionales
y de alfa; ni el valor SI de Planck ni un valor objetivo intervienen como
coeficientes generadores. La matriz celular de autovalores 9 y 5 aporta
coeficientes a (73); su espectro no se identifica con el valor de (73).

**Proposición.** La conjunción de las identidades de esta nota con
\(S=e+\pi\in\mathbb Q\) implica que \(H_5\) es algebraico de grado
exactamente cuatro, con dos conjugados reales y dos no reales.

**Demostración.** Sean
\[
r=S-4-\kappa\in\mathbb Q,\quad a=r-\varphi=\alpha>0,\quad
F=\mathbb Q(\sqrt5),\quad u=250a/\varphi.
\]
La inmersión no trivial de \(F\) envía
\(\varphi\) a \(\varphi'=1-\varphi<0\) y \(a\) a
\(a'=a+\sqrt5>0\). En consecuencia,
\[
u>0,\qquad u'=250a'/\varphi'<0.
\]
Un cuadrado de \(F\) tiene imágenes no negativas en ambas inmersiones
reales. Por tanto, \(u\notin F^2\), y
\(L=F(\sqrt u)\) tiene grado cuatro sobre \(\mathbb Q\) y firma
\((2,1)\). Las cuatro imágenes de \(H_5\) son
\[
f(a)\pm\sqrt u,\qquad f(a')\pm i\sqrt{-u'}.
\]
Son distintas: las dos primeras son reales y diferentes; las otras tienen
partes imaginarias no nulas y opuestas. Por ello,
\(\mathbb Q(H_5)=L\), y su polinomio mínimo mónico es
\[
\boxed{
\bigl((X-f(a))^2-u\bigr)
\bigl((X-f(a'))^2-u'\bigr)\in\mathbb Q[X].
}
\tag{74}
\]
\(\square\)

Esto produce una condición aritmética adicional sobre una salida de la
misma genealogía. En particular, una construcción independiente de ese
mismo \(H_5\) como autovalor de una matriz finita, racional y autoadjunta
contradiría (74): su polinomio mínimo dividiría un polinomio característico
con todas sus raíces reales. Los propietarios focales consultados definen
\(H_5\) como carácter escalar, sin tal identificación espectral. La
positividad de su valor seleccionado, la positividad de acción y la
autoadjunción sin la condición aritmética y finita no implican que todos
sus conjugados algebraicos sean reales. La conjugación de \(F\) tampoco
se identifica automáticamente con la involución de rutas del TPK.

La consecuencia paralela
\[
N_{F/\mathbb Q}(\Sigma_H)=-(r^2-r-1)^{16},\qquad
\Sigma_H=\varphi a^{16},
\]
ya está demostrada en
`ARTICULO_REVISION_ARGUMENTAL_20260907/REVISION_SUSTANTIVA_20260907/CONSECUENCIAS_RACIONALIDAD_SUMATORIA.md`.
Se conserva como **RESULTADO_RECUPERADO**, no como resultado nuevo.
La proposición cuártica se demuestra aquí explícitamente; su procedencia
global permanece pendiente de auditoría. Ninguna de ambas consecuencias
constituye por sí sola una contradicción con la construcción publicada.

## 28. Transporte graduado y evaluación cuadrática de la segunda vía

La consulta alcanzó el propietario exacto enlazado por
`03_PRUEBAS/verificar_generacion_infinita_nonadica.py`, además del c31
integral:
`output/INTEGRAL_SUCESOR_AISLADO_REFUERZOS_ADMITIDOS_20260904/fuente/manuscrito/sucesor_fuente_nivel_20260904/overrides/parte_iii/c31_dos_vias_alpha_rectificacion_20260904.tex`.
Su familia compatible se conserva como dato teoremático recibido. El
transporte finito impreso satisface
\[
Ne_7=-\frac83e_8,\quad Ne_8=\frac2{11}e_9,\quad Ne_9=0,
\quad v=-\frac1{120}e_7.
\]
Para \(R=(I-N)^{-1}\), el cálculo finito da
\[
R^m=I+mN+\binom{m+1}{2}N^2,\qquad
R^mv=-\frac1{120}e_7+\frac m{45}e_8+
\frac{m(m+1)}{495}e_9.
\tag{75}
\]
Así, la prolongación completa incluye la actualización del estado y de la
graduación: elevar este resolvente a potencias mantiene los grados 7–9 y
altera coeficientes anteriores. No genera los grados posteriores.

Escribiendo \(E_m=E_{21/22}^{(6+3m)}\), la compatibilidad de truncamiento
organiza las salidas efectivas en triples:
\[
E_{m+1}(z)-E_m(z)=z^{7+3m}(a_m+b_mz+c_mz^2),
\qquad (a_0,b_0,c_0)=(-1/120,1/45,2/495).
\tag{76}
\]
Esta identidad organiza coeficientes producidos; no prescribe los triples
siguientes. Tampoco atribuye convergencia analítica a un límite formal.

Para evaluar cada salida polinómica en el candidato racional del §26,
escríbase \(r=p/q\), \(a=r-\varphi\) y \(a^n=u_n+v_n\varphi\).
La relación \(\varphi^2=\varphi+1\) da el transporte exacto
\[
\binom{u_{n+1}}{v_{n+1}}
=\begin{pmatrix}r&-1\\-1&r-1\end{pmatrix}
\binom{u_n}{v_n},\qquad (u_0,v_0)=(1,0).
\tag{77}
\]
En particular, \((u_n,v_n)\in q^{-n}\mathbb Z^2\), y
\[
v_n=\frac{a^n-(a+\sqrt5)^n}{\sqrt5}.
\]
Estas coordenadas racionales describen las potencias de \(a\). Si los
coeficientes de \(E_m\) pertenecen a \(\mathbb Q(\pi)\), la evaluación
polinómica completa pertenece a \(\mathbb Q(\pi,\sqrt5)\), no por ello
a \(\mathbb Q(\sqrt5)\).
Aunque \(0<a<10^{-2}\), la segunda cantidad propia es mayor que dos.
La pequeñez de \(a^n\) coexiste con crecimiento de las coordenadas
cuadráticas que se cancelan. Por ello, la evaluación convergente en
\(a\) no autoriza a separar y sumar las dos coordenadas ni a transportar
la evaluación al conjugado: ese paso necesita control de convergencia
adicional. La ecuación (70) conserva su carácter completo y su dependencia
de los coeficientes del lector efectivo. Las identidades (75)–(77) no
reemplazan esa dependencia por una prolongación elegida.

## 29. Composición firmada de las aproximaciones regionales

Las recurrencias de
`certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py`,
líneas 397–499, realizan los lectores seleccionados por la construcción
regional. Se transportan sus restos exactos con signo, a diferencia de
las anchuras positivas del §23. Sean
\[
A_d(n)=\sum_{j=0}^{n-1}\frac{(-1)^j}{(2j+1)d^{2j+1}},\qquad
E_m=\sum_{j=0}^{m}\frac1{j!},
\]
y sea \(Q\) el mínimo común múltiplo de \(m!\) y de **todos los
denominadores individuales** de los términos de \(A_5(n)\) y
\(A_{239}(\ell)\). Entonces
\(P=Q(E_m+16A_5(n)-4A_{239}(\ell))\) es entero.
Para el lector de propagación \(f'=f,\ f(0)=1\), defínanse
\[
F_m=\frac1{m!}\int_0^1 f(t)(1-t)^m\,dt,\qquad
I_d(n)=\int_0^{1/d}\frac{t^{2n}}{1+t^2}\,dt.
\]
Las identidades de resto dan
\[
\boxed{Q(e+\pi)-P
=Q\bigl(F_m+16(-1)^n I_5(n)-4(-1)^\ell I_{239}(\ell)\bigr).}
\tag{78}
\]
Con \(m=n=\ell\),
\[
I_5(n)\ge\frac{25}{26(2n+1)5^{2n+1}},\qquad
F_n<\frac{n+2}{(n+1)^2n!},\qquad
\frac{I_{239}(n)}{I_5(n)}
\le\frac{26}{25}(5/239)^{2n+1}.
\]
Por consiguiente, \(F_n/I_5(n)\to0\) y
\(I_{239}(n)/I_5(n)\to0\). Para ambas paridades y todo \(n\)
suficientemente grande, el valor absoluto del resto entre paréntesis
en (78) es al menos \(8I_5(n)\). Como el \(Q\) construido contiene
el denominador individual \((2n-1)239^{2n-1}\),
\[
|Q(e+\pi)-P|\ge
\frac{200}{26}\frac{239^{2n-1}}{(2n+1)5^{2n+1}}
\longrightarrow+\infty.
\tag{79}
\]
Esta familia concreta tampoco produce formas lineales que tiendan a cero.
La afirmación concierne al entero común explícitamente elegido y a estas
profundidades iguales; no cuantifica sobre todos los denominadores posibles,
todas las sincronizaciones ni todas las composiciones del TPK.

**Estado conjunto de §§27–29.** Se han deducido una consecuencia cuártica,
un transporte exacto de la evaluación cuadrática y una obstrucción para
una familia firmada concreta. Ninguno demuestra la racionalidad o la
irracionalidad de \(e+\pi\), ni la imposibilidad de resolverlas desde HMT.
Las pruebas escritas conservan sus fuentes; no se han modificado los
manuscritos científicos activos ni se ha compilado otro PDF.

## 30. Composición recibida de MASAS: incidencia y base 729

La tarea MASAS fue contactada expresamente por petición de Rubén. Su
respuesta desarrollada se leyó íntegramente en
`../MASAS/E_MAS_PI_RETORNOS_NATIVOS_729_INCIDENCIA_20260908.md`.
Se conserva ese desarrollo en su archivo, sin copiarlo ni modificarlo.

Su agregado efectivo es
\[
u_k=\nu(w_k^\pi)+\nu(w_k^e)-\nu(w_k^\varphi),\qquad
\nu(w)=w(243,81,27,9,3,1)^T,
\]
con valoración \(X=\sum u_k729^{-k}=e+\pi-\varphi-4\).
El decodificador de la incidencia calibrada se compone antes de \(\nu\);
la fuente y el dominio de ese mapa quedan explícitos en su §2.
La prueba de retornos funciona directamente para \(X\), sin restar
\(\kappa\) ni imponer un período múltiplo de doce. La norma cuadrática
que excluye el caso racional de la suma se conserva, ahora aplicada a
\(X=q-\varphi\).

La normalización canónica satisface
\[
b_k=u_k+h_{k+1}-729h_k,\qquad h_k\in\{-1,0,1\}.
\]
Fijados un bloque de \(u\) y su acarreo derecho, la división euclídea
determina el bloque normalizado completo. Por tanto,
\[
p_b(n)\le3p_u(n).
\tag{80}
\]
El factor tres sustituye al factor sesenta de la vía dodecafásica previa;
es una mejora de esa composición, no la demostración de la cota lineal
para el agregado efectivo.

MASAS intentó además realizar el acarreo a partir de la memoria
\(z_kA=v_k+3z_{k+1}\). Para el candidato lineal
\(H_k=3\Delta z_k\lambda\), \(\lambda=(243,81,27,9,3,1)^T\),
obtuvo el defecto exacto
\[
d_k-(729H_k-H_{k+1})=\Delta z_k(A-2187I)\lambda.
\tag{81}
\]
La columna del segundo miembro no es nula para la matriz impresa. Esto
descarta su identificación universal con el acarreo; la anulación sobre
una trayectoria restringida y los compensadores no lineales quedan fuera
de ese descarte. El cálculo tampoco proporciona una cota uniforme para
\(H_k\). Se ha comprobado la deducción formal de (80) y (81) en el
desarrollo recibido; la multiplicación numérica de la matriz consta allí.

**Balance de la colaboración.** La composición nativa, la normalización
de tres estados y la consecuencia cuártica de §27 están escritas con sus
pruebas. No se ha construido un régimen efectivo de retornos con exceso
arbitrario, ni una cota de complejidad suficiente, ni una contradicción
por el carácter de acción. El estudio coordinado no ha resuelto la
irracionalidad de la suma y tampoco ha demostrado su imposibilidad.

## 31. Correspondencia algebraica entre la suma, la coordenada alfa y H5

Esta ampliación responde a la petición de Rubén del 8 de septiembre: incorporar
§27 a los desarrollos especializados y componer su consecuencia aritmética con
la estructura discreta común, su incidencia excepcional y sus realizaciones
posteriores. Se conserva el antecedente APP–TRIT–TPK y las dos vías de alfa de
§26. Las operaciones siguientes actúan sobre las salidas ya generadas; ningún
valor convencional selecciona sus coeficientes.

Escribimos \(a=\alpha_{\rm HMT}\), \(h=H_5\) y
\[
f(X)=-X+\frac9{16}X^2-\frac59X^3+\frac7{48}X^4-\frac1{54}X^5.
\]
El propietario `c35_componente_adimensional_retorno.tex`, ecuación
`eq:l9s102:h5`, proporciona
\[
h=f(a)+\sqrt{250a/\varphi}.
\]
Su subíndice cinco y el grado cinco del término polinómico describen ese lector;
son distintos del grado del polinomio mínimo de su valor sobre \(\mathbb Q\).

### 31.1. Equivalencia de algebraicidad, sin hipótesis racional sobre la suma

Al eliminar la raíz y después \(\varphi\), se obtiene la identidad exacta
\[
\boxed{\mathcal P(a,h):=(h-f(a))^4
+250a(h-f(a))^2-62500a^2=0.}
\tag{82}
\]
En efecto, \(B=(h-f(a))^2=250a/\varphi\), y
\((1/\varphi)^2+1/\varphi-1=0\), de donde
\(B^2+250aB-62500a^2=0\).

El polinomio \(\mathcal P(X,Y)\in\mathbb Q[X,Y]\) es mónico de grado
cuatro en \(Y\). Su grado en \(X\) es veinte, con coeficiente principal
\(54^{-4}\), independiente de \(Y\) y no nulo. Por ello, si \(a\) es
algebraico, también lo es \(h\); si \(h\) es algebraico, (82) hace
algebraico a \(a\). La identidad dodecafásica recibida
\(S=e+\pi=4+\varphi+\kappa+a\), con \(\kappa\in\mathbb Q\), da
\[
\boxed{S\in\overline{\mathbb Q}
\iff a\in\overline{\mathbb Q}
\iff h\in\overline{\mathbb Q}.}
\tag{83}
\]
En particular, \(e+\pi\) es trascendente si y sólo si \(H_5\) lo es.
Cuando los valores son algebraicos, sus grados satisfacen
\[
[\mathbb Q(h):\mathbb Q]\le4[\mathbb Q(a):\mathbb Q],\qquad
[\mathbb Q(a):\mathbb Q]\le20[\mathbb Q(h):\mathbb Q].
\tag{84}
\]
La primera cota usa el grado en \(Y\) de (82); la segunda, su grado en
\(X\), y ambas se obtienen por la fórmula de la torre. La ecuación eliminada
es una consecuencia de la rama positiva seleccionada, no una sustitución del
lector por todas las ramas de su ecuación algebraica. (83) transporta la
clasificación; no asigna por sí sola una de las dos clases a los valores.

### 31.2. Clausura normal bajo la hipótesis racional de la suma

Se retoman las variables de §27:
\[
r=S-4-\kappa\in\mathbb Q,\quad F=\mathbb Q(\sqrt5),\quad
a=r-\varphi>0,\quad a'=r-\varphi'=a+\sqrt5,
\]
\[
u=250a/\varphi>0,\qquad u'=250a'/\varphi'<0,
\qquad D=uu'=-62500(r^2-r-1)<0.
\]
Aquí el primo indica la conjugación no trivial de \(F\). Según §27,
\(L=\mathbb Q(h)=F(\sqrt u)\subset\mathbb R\) es de grado cuatro y
firma \((2,1)\). Sean \(x=\sqrt u\) e \(y=\sqrt{u'}\). El cuerpo
\(N=F(x,y)=L(\sqrt D)\) satisface \([N:L]=2\): \(L\) es real e
\(y\) es imaginario no nulo. Es el cuerpo de descomposición de
\[
(T^2-u)(T^2-u')
=T^4+250(r+2)T^2-62500(r^2-r-1).
\tag{85}
\]
Los automorfismos de \(N\) permutan los pares \(\{x,-x\}\) y
\(\{y,-y\}\). Ese grupo de permutaciones signadas tiene orden ocho;
como \([N:\mathbb Q]=8\), la acción fiel lo identifica con
\[
\boxed{\operatorname{Gal}(N/\mathbb Q)\simeq D_4,
\qquad |D_4|=8.}
\tag{86}
\]
El cuerpo \(L\) es no normal: contiene \(x\) y no contiene su conjugado
\(y\). Por consiguiente, bajo esta hipótesis racional:

- \(h\) no pertenece a ninguna extensión abeliana de \(\mathbb Q\),
  porque los subcampos de una extensión abeliana son normales;
- en particular, \(h\) no pertenece a ningún campo ciclotómico;
- \(h\) tampoco pertenece a un campo CM: un elemento real de un campo CM
  pertenece a su subcampo totalmente real, mientras que \(h\) tiene dos
  conjugados no reales.

La parte real \(N\cap\mathbb R=L\) es distinta de un campo totalmente
real. El mayor subcampo totalmente real de \(N\) es precisamente \(F\):
la conjugación compleja fija \(x\) y cambia el signo de \(y\); su conjugada
por un automorfismo que intercambia ambos pares cambia el signo de \(x\).
Estas dos involuciones generan \(\operatorname{Gal}(N/F)\), que debe fijar
todo subcampo totalmente real. En cambio, \(F(\sqrt D)\subset N\) sí es
un subcampo CM. La presencia de una subestructura CM es así compatible con
que el campo total y el lector \(h\) tengan la firma anterior.

## 32. Representación racional de H5 sobre la incidencia de Paley

El propietario `10h_prueba_corredor_excepcional_rectificacion_probatoria_20260903.tex`,
ecuaciones `eq:exc-calibre-proyectivo` y `eq:exc-matriz-paley`, fija el calibre
\(\mathcal U_9\to\mathbb P^1(\mathbb F_5)\) y la matriz simétrica
\(C_P\in M_6(\mathbb Z)\), con
\(C_P^2=5I_6\) y \(\operatorname{Tr}C_P=0\). Por ello
\(\mathbb Q(\sqrt5)\to\mathbb Q[C_P]\), \(\sqrt5\mapsto C_P\),
es un isomorfismo de \(\mathbb Q\)-álgebras. Esta representación relaciona
dos realizaciones posteriores; conserva la generación previa de \(\varphi\).

Defínanse, bajo la hipótesis racional de §31.2,
\[
\Phi_P=\frac{I_6+C_P}{2},\quad A_P=rI_6-\Phi_P,\quad
U=250A_P\Phi_P^{-1},\quad F_P=f(A_P).
\tag{87}
\]
Se cumple \(\Phi_P^2-\Phi_P-I_6=0\), luego
\(\Phi_P^{-1}=\Phi_P-I_6\). Las matrices de (87) son racionales,
simétricas y conmutan. En los autoespacios \(C_P=\pm\sqrt5 I\), ambos
de dimensión tres, \(U\) tiene valores \(u>0\) y \(u'<0\).

La composición explícita
\[
\boxed{T_h=\begin{pmatrix}F_P&U\\ I_6&F_P\end{pmatrix}
\in M_{12}(\mathbb Q)}
\tag{88}
\]
tiene los cuatro autovalores
\(f(a)\pm\sqrt u\) y \(f(a')\pm\sqrt{u'}\), cada uno con
multiplicidad tres. Su polinomio característico es el cubo del polinomio
mínimo de \(h\) escrito en §27. Ésta es una realización finita y racional
del lector cuártico usando la matriz de incidencia publicada.

Para la forma hiperbólica
\[
J=\begin{pmatrix}0&I_6\\ I_6&0\end{pmatrix},\qquad
JT_h=T_h^{\mathsf T}J
=\begin{pmatrix}I_6&F_P\\F_P&U\end{pmatrix},
\tag{89}
\]
la firma de **\(J\)** es \((6,6)\). Así, la autoadjunción respecto de una
forma indefinida admite esos conjugados no reales. En el autoespacio
\(C_P=\sqrt5 I\), el bloque \(\begin{pmatrix}f(a)&u\\1&f(a)\end{pmatrix}\)
es autoadjunto respecto de \(\operatorname{diag}(1,u)\), que es positiva.
En el autoespacio conjugado la forma \(\operatorname{diag}(1,u')\) es
indefinida. La positividad seleccionada y la firma aritmética mixta son
compatibles en esta construcción concreta.

El operador racional completo \(T_h\) no admite una forma definida positiva
respecto de la cual sea autoadjunto, pues tiene autovalores no reales. Tampoco
\(U\) admite una raíz cuadrada real simétrica: el cuadrado de una matriz
real simétrica es semidefinido positivo y \(U\) tiene firma \((3,3)\).
Seleccionar sólo el autoespacio positivo requiere aquí el proyector
\((I_6+C_P/\sqrt5)/2\), cuyos coeficientes ya pertenecen a \(F\).

### 32.1. Conjugación cuadrática realizada por una permutación signada

En la base publicada \((\infty,0,1,2,3,4)\), sea
\[
S_Pe_\infty=-e_\infty,\qquad S_Pe_x=e_{2x\bmod5}
\quad(x\in\mathbb F_5).
\]
La matriz \(S_P\) es racional ortogonal y cumple
\[
S_P^4=I_6,\qquad S_PC_PS_P^{-1}=-C_P,\qquad
S_P\Phi_PS_P^{-1}=I_6-\Phi_P.
\tag{90}
\]
La segunda igualdad sigue de \(\chi(2)=-1\) sobre las entradas finitas de
Paley y del signo en \(\infty\) sobre las restantes. \(S_P\) tiene orden
cuatro; su conjugación restringida a \(\mathbb Q[C_P]\) tiene orden dos y
realiza exactamente \(\sqrt5\mapsto-\sqrt5\).

Esto proporciona un operador aritmético explícito en la incidencia, distinto
del intercambio hiperbólico \(J\). Para
\(N_V=\begin{pmatrix}0&V\\I_6&0\end{pmatrix}\), se cumple
\(N_U=T_h-\operatorname{diag}(F_P,F_P)\) y
\[
JT_hJ=\begin{pmatrix}F_P&I_6\\U&F_P\end{pmatrix},\qquad
JN_UJ=\operatorname{diag}(U,U)N_{U^{-1}}.
\tag{91}
\]
La inversión de un autovalor real no cambia su signo; la conjugación
cuadrática intercambia los autoespacios que llevan \(u>0\) y \(u'<0\).
La operación (90) realiza la segunda transformación en la representación
matricial. No extiende esa conjugación a un automorfismo del campo real
cuártico \(L\), cuya no normalidad quedó probada en §31.2.

## 33. Transporte por la doble proyección y alcance de las realizaciones posteriores

### 33.1. Recuperación del lector desde la incidencia calibrada

El capítulo `capitulo_17_doble_proyeccion_natural.tex` construye
\[
(w_j,f_j)\longmapsto(f_j,y_j),\qquad
y_j=\Gamma_{f_jA_Wf_j^{-1}}(w_j),
\]
y su inversa sobre la imagen mediante
\(w_j=\Gamma_{f_jA_Wf_j^{-1}}^{-1}(y_j)\). Los truncamientos compatibles
proporcionan el decodificador \(\operatorname{Dec}_\infty\) de la historia
calibrada. Sean \(a(x),\varphi(x)\) los lectores ya generados de esa
historia. Sobre la imagen excepcional y el dominio donde ambos son positivos,
se compone efectivamente
\[
h_{\rm exc}(y)=
f\bigl(a(\operatorname{Dec}_\infty y)\bigr)
+\sqrt{\frac{250a(\operatorname{Dec}_\infty y)}
{\varphi(\operatorname{Dec}_\infty y)}}.
\tag{92}
\]
Entonces \(h_{\rm exc}\circ\mathfrak E_{\infty,\chi_{\rm exc}}=h\)
en ese dominio. La composición conserva el registro, el calibre y la
profundidad, pues decodifica la historia completa antes de aplicar el lector.
En cada dominio compacto donde esos lectores sean continuos y
\(\varphi\) esté separada de cero, (92) es un funcional continuo. Así
puede incorporarse al sistema de operadores común del capítulo mediante
composición de funciones.

Este transporte muestra cómo el lector de acción se recupera desde la
incidencia de la misma estructura discreta. Su codominio es una función de
historias, no un valor de carácter de una representación finita. No requiere
que su polinomio mínimo tenga todos los conjugados reales.

### 33.2. Caracteres finitos y trazas graduadas del corredor excepcional

Si \(g\) es un elemento de orden \(m\) en una representación compleja
finita, sus autovalores son raíces \(m\)-ésimas de la unidad. Por ello
\(\operatorname{Tr}(g)\in\mathbb Q(\zeta_m)\). Lo mismo vale para
normalizaciones y combinaciones racionales de tales trazas, tomando un
múltiplo común de los órdenes. En consecuencia, §31.2 demuestra:
\[
\boxed{S\in\mathbb Q\ \Longrightarrow\
h\text{ no es un valor de carácter ordinario de un grupo finito}.}
\tag{93}
\]
El lector \(H_5\), llamado «carácter regional» en su propietario, se define
por la fórmula analítica de §31. Esa nomenclatura y la igualdad funcional
(92) no lo identifican con la traza finita de (93).

Los propietarios `capitulo_22_voa_leech_moonshine.tex` y
`15d_voa_moonshine_orden_dos_rev11.tex` transportan la incidencia hacia
Leech, sus orbifold y \(V^\natural\), con
\[
T_g(q)=\sum_n\operatorname{Tr}(g\mid V_n^\natural)q^{n-1}.
\]
Cada coeficiente finito satisface la restricción ciclotómica anterior. La
evaluación de esta serie convergente es una operación adicional sobre todos
los grados. La convergencia de elementos de un campo numérico no conserva
necesariamente la pertenencia a ese campo: ni siquiera \(\mathbb Q\) es
cerrado en \(\mathbb R\). Por tanto, (93) se aplica a los coeficientes y
lectores finitos indicados, no automáticamente a toda evaluación de una traza
graduada o al funcional (92).

### 33.3. Acción, área, dualidad de radio y realización supersimétrica

El transporte publicado conserva la secuencia
\(h\to\eta_{\rm ret}\to y_*\to q_\pm\to\gamma_{\rm HMT}\), con
\[
\eta_{\rm ret}=h-\frac{90}{\pi}\mathscr C_\pi,\qquad
y_*=\frac\pi{90}(h+a)-\mathscr C_\pi.
\]
En `c51_barbero_area_informacion.tex`, ecuaciones
`eq:l9s102:area-operador` y `eq:l9s102:area-numero-spectrum`,
\[
\widehat{\mathcal A}_{\rm phys}/\ell_P^2
=\gamma_{\rm HMT}a_0N,\qquad
\operatorname{Spec}N=\{0,\ldots,72\},
\tag{94}
\]
sobre los treinta y seis enlaces qutrit. La normalización por
\(\gamma_{\rm HMT}a_0\) recupera \(N\) y elimina ese escalar. Así,
el espectro entero del operador normalizado no impone algebraicidad ni
realidad total a \(h\), que interviene antes en el coeficiente. La rama
positiva física y todos los conjugados aritméticos son objetos diferentes.

La dualidad de radio de `21_cuerdas_branas_teoria_m.tex` actúa en
\(\ell^2(\mathbb Z^2)\):
\[
U_T|m,w\rangle=|w,m\rangle,\qquad
U_TH(R)U_T^{-1}=H(R^{-1}),\quad
E_R(m,w)=m^2/R^2+w^2R^2.
\tag{95}
\]
En (95) se intercambian los enteros y el radio; los coeficientes generados
permanecen fijos. Las transformaciones (90), (91) y (95) tienen dominios y
acciones explícitos diferentes. La existencia de cada una queda preservada;
su identificación requeriría un entrelazamiento entre esos dominios y no se
infiere del uso común de una inversión.

El propietario `24_terna_supercarga_teoria_m.tex` formula
\(W\widehat H=HW\), \(W\widehat Q=QW\), \(\widehat Q^2=\widehat H\)
en sus espacios de Hilbert y dominios comunes. Tales identidades espectrales
preservan autoadjunción y graduación en la realización indicada. Una
realización de \(h\) como autovalor de un operador finito definido sobre un
campo totalmente real y autoadjunto respecto de una forma positiva bajo
todas sus inmersiones proporcionaría la realidad de **todos los conjugados
algebraicos** de \(h\). Ésta es una condición suficiente, no una condición
necesaria ni la única vía probatoria. Esa conclusión
aritmética no está contenida en la sola identidad \(Q^2=H\).

El resultado positivo de esta composición es específico: la firma cuártica
de §27 posee la realización (88)–(90) en el Paley del corpus, y la
recuperación (92) conserva la historia común. Esto acredita compatibilidad
con esos mapas concretos; no constituye un modelo global de todos los
axiomas HMT bajo la hipótesis racional ni una prueba de independencia.

## 34. Catalán: reducción ternaria, momento de profundidad y escala de Pell

El propietario `c33_catalan_apery_euler.tex`, secciones de construcción
residual y estructura compleja, establece la cadena posterior
\[
C_P\longmapsto J_3=C_P\bmod3,\qquad J_3^2=-I_6,
\qquad U_4e_n=i^ne_n,
\]
\[
Q_4=(U_4-U_4^*)/(2i),\quad Ne_n=ne_n,\quad
G_{\rm Cat}=\operatorname{Tr}(N^{-2}Q_4).
\tag{96}
\]
Se conserva así el antecedente APP–TRIT–TPK que selecciona la orientación
antes de evaluar el momento. La representación de \(F\) por Paley en §32
aporta un vínculo algebraico adicional: sobre el orden
\(\mathbb Z[1/2,\sqrt5]\), la reducción módulo tres lleva
\(\sqrt5\mapsto J_3\) y \(\varphi\mapsto(I_6+J_3)/2\), porque
\(X^2-5\equiv X^2+1\pmod3\). Este homomorfismo finito no identifica
los cuerpos \(\mathbb F_9\) y \(\mathbb C\), ni conmuta automáticamente
con una suma real infinita.

La subsecuencia de términos de (96) con \(n=3^k\) es
\((-1)^k/3^{2k}\). Su norma 3-ádica es \(3^{2k}\), de modo que los
términos no tienden a cero en esa topología. La traza real convergente no
define por esa serie una suma 3-ádica reducible módulo tres, aun bajo la
hipótesis de que su valor real fuese racional.

### 34.1. El momento y su operador espectral

El operador compacto autoadjunto \(T=N^{-2}Q_4\) tiene
\[
\operatorname{Spec}T=\{0\}\cup
\left\{\frac1{(4k+1)^2},-\frac1{(4k+3)^2}:k\ge0\right\}.
\]
La serie alternante prueba \(8/9<G_{\rm Cat}<1\). Ese intervalo carece
de autovalores de \(T\). Por tanto, Catalán es aquí su **traza**, no un
autovalor de ese mismo operador. Esta distinción se prueba a partir del
lector exacto, sin una clasificación aritmética asumida de la constante.

El entrelazador y la base del plano de cuarto de giro, ya construidos en
`../TRAZA_GENERATIVA_COORDINADA.md`, líneas 1739–1783, dan
\[
Cu=v,\quad Cv=-u,\qquad
\langle v,(I-sC)^{-1}u\rangle=\frac{s}{1+s^2}.
\]
Dos integraciones logarítmicas con condiciones nulas en cero producen
\[
F_2(s)=\int_0^s\frac{dt}{t}\int_0^t\frac{d\xi}{\xi}
\langle v,(I-\xi C)^{-1}u\rangle,
\qquad D^2F_2(s)=\frac{s}{1+s^2},\quad D=s\partial_s.
\tag{97}
\]
La finitud del plano controla el carácter de los coeficientes; el peso
\(n^{-2}\) y la profundidad ilimitada proceden de las integraciones.

### 34.2. Transporte exacto de la hipótesis racional por el tornillo de Pell

La confluencia del corpus proporciona \(\lambda=2+\sqrt3\) y
\(\rho=\lambda^{-1}\). La prueba contigua en
`RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md`, desde la línea 270, establece
\[
F_2(\rho)=\frac23G_{\rm Cat}-\frac\pi{12}\log\lambda,
\qquad DF_2(\rho)=\frac\pi{12},\qquad D^2F_2(\rho)=\frac14.
\tag{98}
\]
Así, \(G_{\rm Cat}=q\in\mathbb Q\) obliga exactamente a
\[
\boxed{F_2(2-\sqrt3)+\frac\pi{12}\log(2+\sqrt3)=\frac{2q}{3}.}
\tag{99}
\]
Ésta es una relación entre el momento amortiguado, la escala de Pell y la
coordenada circular generada. No exige que cada sumando sea algebraico.
La conjugación \(\rho\mapsto\lambda>1\) transforma los términos de
\(\sum_{k\ge0}(-1)^k\rho^{2k+1}/(2k+1)^2\) en términos que no
tienden a cero. Por ello, la evaluación mediante continuación de la integral
en \(\lambda\) es distinta de conjugar término a término esa serie.

La proposición cuártica de \(H_5\) usa \(a=r-\varphi\) con
\(r\in\mathbb Q\), una consecuencia específica de \(S\in\mathbb Q\).
La hipótesis \(G_{\rm Cat}\in\mathbb Q\) proporciona (99), no esa
sustitución de \(a\). Las construcciones conservan su raíz común y el
enlace efectivo Paley–cuarto de giro–profundidad–Pell; sus condiciones
aritméticas deben transportarse por las operaciones que efectivamente las
relacionan.

## 35. Resultado del estudio estructural y procedencia

Se incorporan como pruebas de esta ampliación:

1. La correspondencia algebraica (82) y la equivalencia exacta de
   trascendencia entre \(e+\pi\), \(\alpha\) y \(H_5\).
2. La clausura normal dihedral de orden ocho bajo la hipótesis racional,
   y sus consecuencias abeliana, ciclotómica, CM y representacional.
3. La representación racional de dimensión doce construida con el Paley
   publicado, su forma hiperbólica y el operador signado de conjugación.
4. La composición del lector \(H_5\) con el decodificador de incidencia
   calibrada y la discriminación de sus realizaciones finitas e infinitas.
5. El enlace de Catalán con la reducción ternaria de ese Paley, junto con
   la prueba de que la traza no es autovalor de su operador. La evaluación
   de Pell (98) se recupera del desarrollo previo, sin atribuirle novedad.

La referencia de §27 quedó añadida al índice común como séptimo enlace del
bloque especializado de esta investigación. Se amplía este mismo Markdown;
los PDFs científicos y sus fuentes selladas permanecen intactos.

El núcleo, los lectores y las identidades publicadas tienen estatuto
`RESULTADO_RECUPERADO`. Las pruebas (82)–(93) y las discriminaciones
operatorias adicionales son formalizaciones de esta revisión sobre la
arquitectura autoral preexistente; su procedencia global queda pendiente
de auditoría y no se reivindica prioridad histórica. Se revisaron
independientemente la eliminación algebraica, el grado cuártico, la clausura
dihedral y las composiciones matriciales. Se comprobaron además con
aritmética racional exacta la matriz Paley, la permutación signada y las
identidades de adjunción; el control de implementación de \(T_h\) empleó
un parámetro racional de prueba y no sustituye la demostración para todo
\(r>\varphi\).

**Alcance aritmético.** El estudio demuestra las consecuencias y equivalencias
anteriores. La representación Paley efectivamente compuesta admite la firma
cuártica; las trazas y normalizaciones examinadas no la contradicen. No se
deduce de este resultado la racionalidad ni la irracionalidad de \(e+\pi\)
o de Catalán. Tampoco demuestra que su clasificación no pueda deducirse del
resto de la estructura HMT. La información obtenida permite contrastar un
lector preciso y sus propiedades aritméticas, conservando su genealogía,
en lugar de identificar por nomenclatura una dualidad, una traza y una
conjugación de cuerpos.

## 36. Transporte de marcos y conservación entera del acarreo

Se recibe la composición de MASAS, §§12–15, en
`../MASAS/E_MAS_PI_RETORNOS_NATIVOS_729_INCIDENCIA_20260908.md`.
El propietario material del transporte excepcional es
`F/colaboracion/partes_i_ii/source/base_residencias/base_c17_sin_encabezado.tex`,
líneas 549–766, donde F es la raíz integral de 2.249 páginas registrada en §30.
La residencia pública `capitulo_17_doble_proyeccion_natural.tex`, líneas
65–102, conserva la decodificación; el propietario extenso precisa su acción.
Las matrices y los cambios de marco se reciben de la historia APP–TRIT–TPK.
Las operaciones siguientes actúan después sobre sus emisiones y acarreos.

### 36.1. Transporte entre dos niveles de una historia calibrada

Con vectores fila, el propietario define
\[
\Gamma_A(w)=(w,wA),\quad C_W(A)=\operatorname{im}\Gamma_A,
\quad \Gamma_A^{-1}|_{C_W(A)}=\operatorname{pr}_1.
\]
La historia conserva los cambios \(g_j\) y determina
\[
f_{j+1}=g_jf_j,\qquad A_j=f_jA_Wf_j^{-1}.
\]
Fijados \(j\ge0\) y \(p\ge1\), sea
\[
G=G_{j,p}=g_{j+p-1}\cdots g_j=f_{j+p}f_j^{-1}.
\]
La covarianza escrita por el propietario produce
\[
\boxed{\mathcal T_{j+p\leftarrow j}(z)
=z(G^{-1}\oplus G^{-1}),\qquad
\mathcal T_{j+p\leftarrow j}:C_W(A_j)\longrightarrow C_W(A_{j+p}).}
\tag{100}
\]
En efecto, \(A_{j+p}=GA_jG^{-1}\), y
\(\Gamma_{A_{j+p}}(wG^{-1})=\Gamma_{A_j}(w)(G^{-1}\oplus G^{-1})\).
Si se concatenan dos transportes, sus matrices se multiplican en el orden
de la historia: \(G_{j,p+q}=G_{j+p,q}G_{j,p}\). Esto prueba la composición
de (100) y conserva el calibre inicial.

Para \(z_j=\Gamma_{A_j}(w_j)\), la identidad de diferencia es
\[
\boxed{z_{j+p}-\mathcal T_{j+p\leftarrow j}z_j
=\Gamma_{A_{j+p}}(w_{j+p}-w_jG^{-1}).}
\tag{101}
\]
La fórmula compara emisiones reales en sus copias calibradas. La condición
de que esa diferencia sea cero es una condición adicional sobre la emisión,
no una consecuencia del solo transporte del marco.

### 36.2. Composición con la diferencia compensada de las cintas aritméticas

Se utilizan las cintas beta del lector aritmético, con su identificación
en el producto fibrado de c27:218–310. Cuando se trabaja en una carta local
U010, se conserva por separado el transporte que la identifica con esas
cintas; no se igualan sus índices por notación.

Sea \(M_j=[w_j^\pi+w_j^e]_3\). El coborde posicional de MASAS (28),
al normalizar los trits, implica
\(M_{j+p}-M_j=-H_j^+\) en \(\mathbb F_3^6\), donde \(H_j^+\)
reúne las seis diferencias de acarreos por los extremos derechos de los
trits. Si los dos canales están expresados en una misma copia calibrada
y comparten el transporte G, (101) da
\[
\boxed{\Gamma_{A_{j+p}}(M_{j+p})
-\mathcal T_{j+p\leftarrow j}\Gamma_{A_j}(M_j)
=\Gamma_{A_{j+p}}\bigl(M_j(I-G^{-1})-H_j^+\bigr).}
\tag{102}
\]
El término \(M_j(I-G^{-1})\) conserva el cambio de marco; el término
\(-H_j^+\) conserva la compensación posicional. Para \(G=I\) se recupera
el cálculo de la copia fija. La deducción es sustituir
\(M_{j+p}=M_j-H_j^+\) en (101).

Si los transportes son \(G_\pi,G_e\), se trabaja por canal. Los defectos
visibles \(\eta_\chi=w_{j+p}^\chi-w_j^\chi G_\chi^{-1}\) satisfacen
\[
\eta_\pi+\eta_e=-H_j^+
+w_j^\pi(I-G_\pi^{-1})+w_j^e(I-G_e^{-1}).
\tag{103}
\]
Sus imágenes de código se reúnen sólo en una copia común explícitamente
transportada. Tampoco se supone que un retorno de las cifras normalizadas
sea un retorno paralelo de incidencia: para una palabra b repetida, este
último exige además \(bG^{-1}=b\), por la inyectividad de \(\Gamma\).

### 36.3. El acarreo entero bajo un cambio de coordenadas

Para una matriz entera F que represente un cambio lineal residual, sea
\([uF]_3\) el representante en \(\{0,1,2\}^6\) y defínase
\[
q_F(u)=\frac{uF-[uF]_3}{3}\in\mathbb Z^6.
\]
Para \(u,v\in\{0,1,2\}^6\), escribamos \(u+v=r+3c\), con
\(r=[u+v]_3\) y \(c\in\{0,1\}^6\). Entonces
\[
\boxed{r_F=[rF]_3,\qquad
c_F=cF+q_F(r)-q_F(u)-q_F(v),}
\qquad [uF]_3+[vF]_3=r_F+3c_F.
\tag{104}
\]
**Prueba.** Se sustituye \([uF]_3=uF-3q_F(u)\), y análogamente para v,
en la suma. A continuación se sustituye \(u+v=r+3c\) y
\(rF=[rF]_3+3q_F(r)\). La suma de dos representantes canónicos muestra
además que \(c_F\in\{0,1\}^6\). La identidad vale incluso para matrices
con entradas negativas. La invertibilidad sólo interviene al reconstruir.

Para dos matrices enteras F y G, la composición conserva exactamente
\[
\boxed{q_{FG}(u)=q_F(u)G+q_G([uF]_3).}
\tag{105}
\]
En efecto, \(uFG=[uF]_3G+3q_F(u)G\), y el último sumando es divisible
por tres. Si \(FH=I+3M\), con H representante entero de la inversa residual,
\[
[[uF]_3H]_3=u,\qquad
q_F(u)H+q_H([uF]_3)=uM.
\tag{106}
\]
La pareja recuperada tiene de nuevo acarreo c. El término \(uM\) conserva
la diferencia entre inversa residual e inversa entera. Así queda probado
el transporte afín completo del acarreo de los representantes.

El acarreo de (104) pertenece al cambio de marco; el de MASAS (28)
pertenece a la valoración posicional de una cola. Un cambio arbitrario de
marco puede alterar la lectura \(\nu\) si se mantienen sus pesos fijos.
Para conservar el valor original se aplica primero el inverso de (106)
a cada bloque y después \(\nu\). De esta forma la compensación posicional
se comprueba sobre la misma salida HMT y no sobre otra lectura.

### 36.4. Dominio de supervivencia y resultado de esta composición

El resultado recuperado (100) transporta los marcos suministrados por la
historia; (102)–(106) conservan las contribuciones residuales y enteras que
deben acompañarlo. La pertenencia al código recibe ahora su transporte
correcto, en lugar de comparar copias etiquetadas distintas.

La supervivencia permanece en el estado fuente. c27:82–163 define las
secciones forward seleccionadas por su carácter; U010:169–195 fija el
segundo horizonte local sobre ese estado. Para contrastar un candidato de
coborde se mantienen esas condiciones junto con (102) y (104). El marco
se transporta usando sus g_j efectivos y los cocientes siguen formando
parte de la historia. U010 es el testigo del segundo horizonte allí fijado;
sus bloques B11 y su frontera concreta no se repiten como una regla global.
Estas identidades no autorizan reemplazar la selección
de caracteres por la sola pertenencia al código.

**Procedencia.** Matrices, covarianza y marcos por prefijos:
`RESULTADO_RECUPERADO`. Composición de defectos y transporte afín del
acarreo: formalización focal de esta revisión sobre arquitectura autoral
preexistente, con prioridad global pendiente de auditoría. Las identidades
se probaron simbólicamente y fueron revisadas independientemente; no se
generaron nuevas cifras. Su alcance es el transporte exacto. La exclusión
de todos los cobordes en la sección conjunta seleccionada sigue sin quedar
demostrada por estas identidades. Los PDF y las fuentes rectoras permanecen
intactos.

## 37. Filtro entero de dos estados para la compensación posicional

La arquitectura operatoria del TPK, `F/manuscrito/sections/hmt/20_arquitectura_operatoria_tpk_actualizada.tex:645–703`,
proporciona el test de cilindros y la división Hensel. Se compone aquí el
filtro comunicado por MASAS con el criterio (28) de su desarrollo, conservando
los estados en las dos posiciones que se comparan. Las fronteras decimales
se reciben ya generadas por esos estados y no se eligen para imponer un valor.

### 37.1. Extremos enteros exactos

Para un canal, sea A el residuo entero del cilindro anterior, sea h el
número de tríadas decimales anexadas y sea d su entero concatenado. Escribamos
\[
T=1000^{K+h},\qquad M=729\,3^L,\qquad
P=729\,1000^h A-dM.
\]
Tras anexar el bloque ternario de valoración t, las condiciones de
intersección son \(-T<P+Tt<M\), con \(0\le t\le728\). Por tanto,
\[
\boxed{L_*\le t\le U_*,\quad
L_*:=\max\{0,\lfloor-P/T\rfloor\},\quad
U_*:=\min\{728,\lfloor(M-P-1)/T\rfloor\}.}
\tag{107}
\]
Si \(L_*>U_*\), el filtro es vacío. Para probar (107), la primera
desigualdad estricta da \(t\ge\lfloor(-T-P)/T\rfloor+1
=\lfloor-P/T\rfloor\). La segunda, sobre enteros, equivale a
\(Tt\le M-P-1\). Así se conservan exactamente las fronteras semiabiertas,
también cuando P es negativo.

### 37.2. Composición de los dos horizontes con las aristas de acarreo

Para los dos canales, sean \([L_\pi,U_\pi]\) y \([L_e,U_e]\) los filtros
del primer estado, y los intervalos primados los del segundo. Se consideran
los casos en que los cuatro intervalos son no vacíos. Defínanse
\(L_\Sigma=L_\pi+L_e\), \(U_\Sigma=U_\pi+U_e\), y sus versiones primadas.
Entonces toda pareja realmente superviviente satisface
\[
\boxed{L'_\Sigma-U_\Sigma\le n'-n\le U'_\Sigma-L_\Sigma.}
\tag{108}
\]
Esta inclusión procede de sumar y restar los extremos; no presupone
independencia de los canales ni declara realizable toda combinación interior.

En el contraste del comienzo N y período p del criterio MASAS (28), se usan
en cada k las ventanas que producen \(n_{k+1}\) y \(n_{k+p+1}\). Sus estados
y cartas se conservan, conforme a §36. La compensación sólo puede recorrer
las aristas
\[
\boxed{\mathcal A_k=
\{(b,b')\in\{-1,0,1\}^2:
L'_\Sigma-U_\Sigma\le729b-b'\le U'_\Sigma-L_\Sigma\}.}
\tag{109}
\]
La prueba sustituye \(n'-n=729\delta_k-\delta_{k+1}\) en (108).
Si se inicia \(R_N=\{-1,0,1\}\) y se propaga
\[
R_{k+1}=\{b':\exists b\in R_k,\ (b,b')\in\mathcal A_k\},
\]
un conjunto vacío en cualquier horizonte excluye ese comienzo y período.
Por inducción, todo acarreo efectivo compatible pertenece a R en cada nivel;
por ello no puede atravesar un conjunto vacío.

Este es un filtro necesario de la trayectoria, deliberadamente exterior a la
intersección adicional con Hensel, los caracteres, los cocientes y la
supervivencia completa. Un camino que atraviesa todos sus intervalos no
acredita por sí solo esa intersección. El teorema de exclusión por vaciedad
es exacto para cada par N,p; no se afirma aquí que se haya producido tal
vaciedad para todos los pares de la trayectoria HMT. No se han utilizado
prefijos objetivo ni generado nuevas cifras.

**Procedencia.** Test entero y actualización de cilindros: resultados
recuperados del propietario citado. Filtro de MASAS y su composición
(107)–(109): formalización focal conjunta; se conserva la distinción entre
la prueba simbólica del filtro y su aplicación a una familia de períodos.

## 38. Compatibilidad de ventanas con la memoria entera fijada

El siguiente paso utiliza la separación residuo–cociente del TPK y no añade
un selector de valores. El propietario es
`F/manuscrito/sections/hmt/14_numero_heisenberg_y_d108.tex:552–609`, con la
misma matriz de `20_arquitectura_operatoria_tpk_actualizada.tex:682–709`.
La proposición se aplica en una ventana donde está acreditada la carta
entera \(x_jA_H=u_j+3x_{j+1}\). Conserva las dos secciones individualizadas
por sus caracteres y sus estados iniciales; no identifica esta carta con
toda la actualización forward de c27.

### 38.1. Reconstrucción exacta y condición de congruencia

Sea \(A=A_H\in\operatorname{GL}_6(\mathbb Z)\), y sean
\(u_0,\ldots,u_{m-1}\in\{0,1,2\}^6\). Para vectores fila, defínase
\[
E_m(u):=\sum_{j=0}^{m-1}3^j u_jA^{-(j+1)}\in\mathbb Z^6.
\]
La composición de las m divisiones euclídeas es
\[
\boxed{x_0=E_m(u)+3^m x_mA^{-m}.}
\tag{110}
\]
Por tanto, para un estado inicial entero fijado, la ventana tiene exactamente
los residuos prescritos si y sólo si
\[
\boxed{x_0\equiv E_m(u)\pmod{3^m\mathbb Z^6}.}
\tag{111}
\]
En ese caso, su estado final está determinado por
\[
x_m=3^{-m}\bigl(x_0-E_m(u)\bigr)A^m.
\tag{112}
\]

**Prueba.** Se despeja \(x_j=(u_j+3x_{j+1})A^{-1}\) y se sustituye
sucesivamente. Esto da (110) y la necesidad de (111). Recíprocamente,
(111) hace entero el vector (112). Se reconstruyen todos los estados
intermedios hacia atrás mediante el mismo despeje, que conserva integridad
porque \(A^{-1}\) es entera. El estado reconstruido al comienzo coincide
con el x0 fijado por (110). Como cada u_j está en el alfabeto canónico,
la división euclídea de x_j A tiene precisamente residuo u_j y cociente
x_(j+1). Así se obtiene también la suficiencia y la unicidad.

La prolongación conserva
\[
E_{m+1}(u)\equiv E_m(u)\pmod{3^m\mathbb Z^6}.
\tag{113}
\]
Al concatenar ventanas se transporta el estado (112); no se escoge otro
representante de la clase inicial. Esta condición es la contribución de la
memoria de cociente que el intervalo escalar de §37, por sí solo, no retiene.

### 38.2. Comparación de dos posiciones sin perder el tramo intermedio

Para contrastar un comienzo N, un desplazamiento p y m emisiones comparadas,
se conservan, por cada canal \(\chi\in\{\pi,e\}\), la ventana completa
\(u_0^\chi,\ldots,u_{p+m-1}^\chi\) y el estado inicial
\(x_N^\chi\). Se aplican las dos congruencias (111) con longitud p+m.
Si las ventanas se solapan, los símbolos comunes son los mismos; si están
separadas, los p pasos iniciales transportan el estado hasta la segunda.
En particular, el estado allí obtenido es el de (112) para el prefijo p:
no constituye una nueva variable independiente.

Sobre estas mismas emisiones, decodificadas en su carta original conforme
a §36, se forma \(n_j=\nu(u_j^\pi)+\nu(u_j^e)\). El test de período
exige además
\[
n_{p+j}-n_j=729\delta_j-\delta_{j+1},\qquad
\delta_0,\ldots,\delta_m\in\{-1,0,1\},\quad 0\le j<m.
\tag{114}
\]
Las cotas de cilindros (107) y las condiciones de carácter, marco,
orientación, frontera y supervivencia se comprueban sobre esa misma
prolongación. (111) verifica exactamente su componente Hensel; (114)
verifica la compensación escalar finita. Ninguna se reemplaza por la otra.

**Control de pérdida de información.** Sumar las dos congruencias no basta.
En la carta local de prueba, tómense dos estados iniciales nulos y una ventana
de longitud uno con residuos candidatos
\(u=(1,0,0,0,0,0)\), \(v=(2,0,0,0,0,0)\). Entonces
\((u+v)A^{-1}\equiv0\pmod3\), por lo que pasa la congruencia agregada.
Sin embargo, \(uA^{-1}\) y \(vA^{-1}\) son ambos no nulos módulo tres,
pues A es invertible: fallan las dos congruencias individuales. Los estados
nulos emiten necesariamente dos residuos nulos. Este control prueba la
necesidad de conservar los estados separados; no propone sustituir las
secciones de las constantes por esos estados de prueba.

### 38.3. Correcciones enteras del marco dentro de la ventana

Si el bloque se entrega como \(v_j=[u_jF_j]_3\), sea H_j una matriz
entera que represente la inversa residual de F_j. La reconstrucción de §36
da \(u_j=[v_jH_j]_3=v_jH_j-3q_{H_j}(v_j)\). Sustituyéndola en (111),
\[
\boxed{x_0\equiv
\sum_{j=0}^{m-1}3^j
\bigl(v_jH_j-3q_{H_j}(v_j)\bigr)A^{-(j+1)}
\pmod{3^m\mathbb Z^6}.}
\tag{115}
\]
La contribución del acarreo de marco j tiene factor \(3^{j+1}\).
Sólo en la última posición desaparece automáticamente módulo \(3^m\);
las contribuciones anteriores deben conservarse. Cambiar el representante
entero a \(H_j+3K_j\) aumenta \(q_{H_j}(v_j)\) en \(v_jK_j\),
de modo que ambos cambios se cancelan exactamente en (115).

Por otro lado, sean \(Z_j=x_j^\pi+x_j^e\) y
\(\Delta Z_j=Z_{p+j}-Z_j\) en la ventana entera reconstruida. Con
\(\lambda=(243,81,27,9,3,1)^{\mathsf T}\), (114) equivale a
\[
\boxed{\bigl(\Delta Z_jA-3\Delta Z_{j+1}\bigr)\lambda
=729\delta_j-\delta_{j+1}.}
\tag{116}
\]
La prueba suma las dos identidades Hensel, resta los horizontes y aplica
\(\nu(u)=u\lambda\). Así los residuos, el marco y los estados profundos
participan en el mismo test; los \(\Delta Z_j\) están fijados por (112),
y el acarreo posicional delta sigue siendo distinto del acarreo trítico
de la suma y del acarreo producido por el cambio de marco.

**Aplicación y alcance.** Se ha construido la intersección finita de memoria
entera, comparación de ventanas y acarreo sobre el mismo trayecto, incluyendo
el tramo intermedio. Las ecuaciones (110)–(116) no eliminan por sí solas
todos los pares N,p de la trayectoria seleccionada. Tampoco se prolonga
silenciosamente una carta finita: si una actualización efectiva incluye
correcciones adicionales de segundo orden, éstas se conservan y se compone
esa actualización completa en lugar de iterar la ecuación homogénea.

**Procedencia y control reproducible.** La separación de memoria y residuo
es arquitectura autoral preexistente y resultado recuperado. La composición
por ventanas es formalización focal, con prioridad global pendiente de
auditoría. Su prueba fue revisada independientemente. La opción
`--hensel-window` del comprobador existente verifica 32 ventanas enteras,
rechaza 192 alteraciones de sus símbolos y detecta el falso positivo de la
congruencia agregada. Esos son controles sintéticos exactos, no nuevos dígitos
de constantes ni certificados de supervivencia global. Los PDF y las fuentes
rectoras permanecen inalterados; no se declara clasificada la suma.
