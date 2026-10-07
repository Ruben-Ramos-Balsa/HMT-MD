# Memoria, compresión y conservación del álgebra operatoria

Formalización focal del 29 de septiembre de 2026. No modifica manuscritos ni
certifica por sí sola el cierre conjunto de las cuatro interacciones.

## 1. Procedencia y punto de corte

Se conserva la genealogía APP → TRIT → TPK → estado enriquecido → estructura
discreta conjunta del continuo, documentada en
[`RECIBO_GENEALOGIA.json`](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/RECIBO_GENEALOGIA.json>). Las operaciones focales
son el transporte completo de fibra, la conservación de memoria y su lectura
posterior. APP conserva hojas, residuos, cocientes y acarreos; TRIT fija régimen
y orientación; TPK compone transportes sin reiniciar memoria al retornar la fase.
No se reconstruye retrospectivamente el generador a partir de matrices de prueba.
La escala positiva de acción que aparece abajo es una salida ya publicada; no se
introduce un valor experimental ni un valor objetivo.

Propietarios efectivos de la composición:

1. `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VII_ES/manuscrito/desarrollos/restitucion_operatoria.tex`, líneas 146–207: dilatación completa de la lectura 8:1, composición exacta y términos cruzados de memoria.
2. `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/fuentes_conservadas/02_dinamica_tres_hojas.tex`, sección «Corona nonádica y energía torsional»: diferencia covariante, forma positiva y cuadrados de refinamiento; sección «Reducción de Feshbach–Schur»: memoria en el resolvente completo.
3. `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/81_propagacion_bidireccional.tex`, líneas 111–145: autoadjunción, dominio y estructura compleja de la evolución.
4. `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/X_ES/sections/ym_complete.tex`, líneas 313–344, 415–425 y 796–836: forma cerrada, reducción física compatible y entrelazamiento del generador Yang–Mills en el límite inductivo.

Los lemas de §§2–4 son la formalización reunida aquí. Los propietarios aportan
las operaciones; las pruebas siguientes explicitan qué conserva su composición.
No afirman que cualquier familia abstracta de operadores sea ya la familia de
restricciones Einstein–Schrödinger del corpus. No se divide globalmente el conjunto
en una parte «clásica» y otra «cuántica»: se examina la compatibilidad de operadores
cuánticos sobre la misma realización enriquecida.

## 2. Identidad exacta del defecto de compresión

Sean \(J:\mathcal H\to\widehat{\mathcal H}\) una isometría,
\(P=JJ^*\), \(E=I-P\) y \(\Phi(A)=J^*AJ\). Para operadores acotados
\(A,B\),

\[
\boxed{[\Phi(A),\Phi(B)]-\Phi([A,B])
=-J^*AEBJ+J^*BEAJ.}\tag{1}
\]

**Prueba.** Insertar \(JJ^*=I-E\) entre los dos factores:
\(\Phi(A)\Phi(B)=J^*ABJ-J^*AEBJ\), y restar la igualdad con
\(A,B\) intercambiados. No se supone conmutatividad. ∎

Para operadores no acotados, (1) se interpreta en un núcleo común donde todos
los productos escritos están definidos: por ejemplo, un subespacio denso
\(\widehat{\mathscr D}\) invariante por \(A,B,P\), con
\(J\mathscr D\subset\widehat{\mathscr D}\). Esta cláusula no puede
reemplazarse por manipulación formal de dominios.

Los dos términos del lado derecho son exactamente los recorridos que salen
del subespacio leído y retornan a él. La identidad no es una afirmación sobre
anomalías quirales ni sobre regularización de determinantes fermiónicos. Es
un defecto de composición de una lectura comprimida. Si
\(EAJ=EBJ=0\), desaparece. Si no desaparece, conservar ambos términos
restaura la lectura del conmutador completo, sin probar por ello cuál es el
álgebra de restricciones del sistema físico.

### Formas compatibles no equivalen a generadores entrelazados

Las identidades de refinamiento

\[
D'J=KD,\qquad K^*W'K=W
\]

dan

\[
\langle D'Ju,W'D'Jv\rangle=\langle Du,WDv\rangle.
\]

Es compatibilidad de formas. Si los operadores asociados están definidos en
los vectores implicados, expresa \(J^*H'J=H\). Para concluir
\(H'J=JH\) debe verificarse también que no sale componente al complemento:
\((I-JJ^*)H'J=0\). En dimensión finita esta equivalencia es inmediata;
para operadores no acotados incluye la pertenencia a sus dominios. Una
reducción espectral del subespacio leído asegura además el entrelazamiento de
resolventes y grupos unitarios.

**Control negativo positivo-semidefinido.** Sean

\[
H'=\begin{pmatrix}1&1\\1&1\end{pmatrix}=I+\sigma_x\succeq0,
\quad Jz=(z,0),\quad H=1.
\]

Entonces \(J^*H'J=H\), pero \(H'J-JH=(0,1)^\mathsf T\ne0\),
\(J^*(H')^2J=2\ne H^2=1\), y

\[
J^*e^{-itH'}J=\frac{1+e^{-2it}}2\ne e^{-itH}.
\]

Se ha utilizado una coordenada temporal adimensional en este ejemplo algebraico;
no se ha fijado el valor de ninguna constante física. La positividad por sí
sola no elimina la fuga de memoria.

## 3. Generador autoadjunto de la dilatación 8:1

Sea \(h=h^*\) sobre \(\mathcal H\), con dominio denso \(D(h)\), y
\(C(t)=\exp(-it h/\hbar)\), donde \(\hbar>0\) es la escala de acción
ya publicada en la realización. Definimos

\[
R=\frac13\begin{pmatrix}\sqrt8 I&I\\-I&\sqrt8 I\end{pmatrix},
\qquad
P_w=\frac19\begin{pmatrix}1&\sqrt8\\\sqrt8&8\end{pmatrix}.
\]

Se comprueba \(R^*R=I\), \(P_w=P_w^*=P_w^2\), y la dilatación del
propietario es

\[
\mathcal U_C=R\begin{pmatrix}I&0\\0&C\end{pmatrix}R^*
=\frac19\begin{pmatrix}8I+C&\sqrt8(C-I)\\
\sqrt8(C-I)&I+8C\end{pmatrix}.\tag{2}
\]

Por tanto \(\mathcal U_{C_2}\mathcal U_{C_1}=\mathcal U_{C_2C_1}\).
En particular, \(t\mapsto\mathcal U_{C(t)}\) es un grupo unitario
fuertemente continuo con generador autoadjunto

\[
\boxed{\widehat h=R(0\oplus h)R^*,\qquad
D(\widehat h)=R(\mathcal H\oplus D(h)).}\tag{3}
\]

Equivalentemente,

\[
D(\widehat h)=\{(x,y):x+\sqrt8y\in D(h)\},\quad
\widehat h(x,y)=\frac19\bigl(h(x+\sqrt8y),\sqrt8h(x+\sqrt8y)\bigr).
\]

En \(D(h)\oplus D(h)\), que es un núcleo de \(\widehat h\), se escribe
\(\widehat h=P_w\otimes h\); la clausura tiene el dominio (3).
No se impone indebidamente \(D(h)\oplus D(h)\) como dominio máximo.

**Prueba.** \(0\oplus h\) es autoadjunto sobre
\(\mathcal H\oplus D(h)\); la conjugación por la unitaria acotada \(R\)
transporta dominio, cálculo espectral y exponencial. El núcleo se obtiene
aproximando la primera coordenada libre por vectores de \(D(h)\). ∎

Con \(Jx=(x,0)\), la lectura del generador es \(J^*\widehat hJ=h/9\).
Sin embargo,

\[
J^*\mathcal U_{C(t)}J=\frac{8I+C(t)}9
\]

no es en general \(\exp(-it h/(9\hbar))\). La dilatación conserva el grupo;
la lectura visible aislada no constituye ese mismo grupo de evolución.

### Unidad activa y complemento pasivo

La aplicación \(j(A)=P_w\otimes A\) es un *-homomorfismo, pero **no es
unital en el espacio completo**: \(j(I)=P_w\otimes I=:P_{\rm act}\ne I\).
Su unidad es la del sector activo. El complemento
\(Q_{\rm pas}=I-P_{\rm act}\) tiene generador cero y evolución identidad:

\[
e^{-itj(h)/\hbar}=Q_{\rm pas}+j(e^{-ith/\hbar}).\tag{3a}
\]

Por ello una relación central \([A,B]=i\hbar I\), cuando sus dominios
permiten escribirla, se transporta a
\([j(A),j(B)]=i\hbar P_{\rm act}\), no a \(i\hbar I\) en todo el
espacio dilatado. En el sector activo sí conserva su unidad propia.
La dilatación añade un complemento trivial; no convierte por sí sola una
realización en una teoría cuántica completa de todos los sectores físicos.

## 4. Conservación exacta del álgebra y control Pauli

Sean \(h_a=h_a^*\) con un núcleo común denso \(\mathscr D\), invariante
por todos los \(h_a\), y supongamos que en él

\[
[h_a,h_b]=i\hbar\sum_c f_{ab}^{\ c}h_c,\tag{4}
\]

donde los \(f_{ab}^{\ c}\) son escalares y la suma indicada es finita.
Las dilataciones (3) satisfacen, sobre
\(\widehat{\mathscr D}=\mathscr D\oplus\mathscr D\),

\[
[\widehat h_a,\widehat h_b]
=P_w\otimes[h_a,h_b]
=i\hbar\sum_c f_{ab}^{\ c}\widehat h_c.\tag{5}
\]

**Prueba.** El núcleo es invariante y \(P_w^2=P_w\); multiplicar los
operadores en él prueba (5). No se obtiene el cierre inicial (4) de la mera
existencia de \(P_w\): se demuestra que la dilatación conserva un cierre
previamente demostrado. ∎

La diferencia entre ambos órdenes de lectura es exactamente

\[
[J^*\widehat h_aJ,J^*\widehat h_bJ]=\frac1{81}[h_a,h_b],\quad
J^*[\widehat h_a,\widehat h_b]J=\frac19[h_a,h_b].
\]

Por ello el defecto de (1) vale
\(-\frac8{81}[h_a,h_b]\); los recorridos de memoria restituyen
\(+\frac8{81}[h_a,h_b]\) al pasar del conmutador visible a la lectura
del conmutador completo. No hay contradicción de signos: son los dos órdenes
de restar la misma identidad.

Para \(h_a=\hbar\sigma_a/2\),
\([h_a,h_b]=i\hbar\epsilon_{ab}^{\ \ c}h_c\). Las dilatadas conservan
esta relación con el mismo coeficiente. En cambio,

\[
[h_x/9,h_y/9]=i\hbar h_z/81
\ne i\hbar(h_z/9).
\]

Este control negativo detecta precisamente una compresión que se hubiera
presentado falsamente como entrelazamiento del álgebra original. No identifica
el álgebra Pauli con todas las restricciones gravitatorias ni con una anomalía
quiral. Para coeficientes operatorios, productos ordenados o restricciones con
funciones de estructura, hay que transportar también esos coeficientes y sus
dominios; (4) no demuestra por sí sola ese caso distinto.

## 5. Verificación focal y alcance

`verificar_memoria_dominio_algebra.py` comprueba con aritmética exacta en
\(\mathbb Q(i,\sqrt2)\) las identidades de compresión, los proyectores y la
unitaria, la composición 8:1, el álgebra Pauli completa y su defecto visible,
así como el contraejemplo positivo de compatibilidad de formas sin
entrelazamiento. Las matrices de prueba son falsadores de estas identidades,
no datos de entrada de un generador HMT ni selección de una dinámica física.

La autoadjunción y los dominios infinitodimensionales quedan demostrados en
§3 por conjugación unitaria; no se atribuye esa prueba a una batería finita.
La aplicación de (5) a una realización concreta requiere sus propios
operadores \(h_a\), su núcleo común y la relación (4). La fuente Yang–Mills
citada sí proporciona su forma, reducción física y entrelazamientos
concretos. La composición presente conserva esos resultados sin sustituir
por un teorema genérico las identificaciones adicionales del problema conjunto.
