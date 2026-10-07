# Plegado, memoria y cardinalidad: desarrollo focal desde APP–TRIT–TPK

Fecha: 10 de septiembre de 2026. Investigación separada; no modifica ningún PDF.
Encargo: desarrollar, de manera independiente, la conexión holográfica propuesta
entre cilindros, memoria, cardinalidad y ordinalidad, y comprobar su alcance para CH.

## 1. Punto de partida y corte causal

APP conserva suma y producto, posiciones, residuo y cociente. La reconstrucción
positiva n = 9q + r, con 1 ≤ r ≤ 9, distingue la fase visible del cociente.
TRIT selecciona régimen y orientación sin borrar el acarreo.
TPK compone selección, transporte, actualización de memoria y prolongación.
El retorno de fase no reinicia el estado enriquecido.

El sistema compatible del continuo conserva esos datos en las historias completas.
Se hereda la construcción conjunta del corpus, incluidas sus cinco operaciones
consustanciales; no se sustituyen por cinco dominios independientes ni se vuelve
a demostrar globalmente esa construcción en esta nota. El corte investigado es
posterior: los cilindros de historias, su peso, el plegado y sus lectores.
Los grados de emisión se leen del emisor, no se eligen para obtener un cardinal.

La fuente especializada aportada por Rubén, §3 del artículo nuclear, define
Em(x), d(x) = #Em(x), el peso local 1/d(x), los enlaces de restricción y la
medida proyectiva. Éstos son los antecedentes concretos de los resultados
de las secciones 2–4. Las constantes generadas del corpus no se reintroducen
como valores convencionales ni como parámetros para seleccionar estos grados.
La cuatrirrelación conserva su procedencia común; aquí no se recalculan sus cifras.

El material histórico se utiliza como orientación para la actualización,
no como objeto de un dictamen. El desarrollo siguiente conserva el problema
cardinal y reúne las operaciones necesarias para abordarlo.

## 2. Dualidad exacta entre peso y magnificación de un cilindro

Fijemos un estado enriquecido inicial y su árbol de prolongaciones admisibles.
Para cada prefijo x, el conjunto Em(x) es finito y no vacío. Los sucesores
retienen su etiqueta de emisión y su predecesor: que dos lecturas visibles
coincidan no identifica las historias.

Sea x_0 → x_1 → … una historia y d_n = d(x_n). Definimos dos operaciones
distintas, ambas calculadas a partir de los grados producidos:

```text
w_0 = 1                    M_0 = 1
w_(n+1) = w_n / d_n         M_(n+1) = d_n M_n.
```

w_n es el peso condicional del cilindro respecto del estado inicial;
M_n es el factor entero acumulado de subdivisión. No se define M_n como
el inverso de una medición de w_n: se obtiene multiplicando los grados.

**Proposición 1.** En todo nivel finito,

\[
 w_n M_n=1,\qquad
 \sum_{y\in\operatorname{Em}(x_n)} w([x_n y])=w([x_n]).
\]

**Demostración.** En el nivel cero ambas identidades son inmediatas.
Si w_n M_n = 1, entonces
(w_n/d_n)(d_n M_n) = 1. Cada una de las d_n prolongaciones tiene
peso w_n/d_n; su suma es w_n. La inducción prueba las identidades
a toda profundidad finita, sin fijar un límite de cálculo. ∎

Al sumar por los prefijos de un nivel se obtiene masa total uno. Los pesos
son compatibles con la restricción. En el espacio compacto de historias
finitamente ramificado, definen la medida de cilindros de la fuente:
la continuidad desde arriba en el álgebra de cilindros se obtiene por
compacidad; su extensión boreliana queda determinada por esa álgebra.
No se requiere que todos los estados tengan el mismo grado.

Si un estado no admite ninguna prolongación, este argumento se aplica al
árbol de estados supervivientes declarado por el corpus, no a un supuesto
grado cero al que se asignara 1/0.

### 2.1 Dirección entera, contracción y conservación del código

Elijamos el orden efectivo de las emisiones de cada prefijo; si el corpus
no fija ese orden, la afirmación vale para cualquier orden declarado y no
pretende seleccionar una orientación física. Sea a_(n+1) el índice,
entre 0 y d_n−1, de la emisión seguida. Se construyen

\[
 q_0=0,\qquad q_{n+1}=d_nq_n+a_{n+1},
 \qquad I_n=\left[\frac{q_n}{M_n},\frac{q_n+1}{M_n}\right].
\]

Las prolongaciones subdividen I_n en d_n intervalos de igual longitud.
Sus interiores son disjuntos y su unión es I_n. Pueden hacerse semiabiertos,
exceptuando el extremo final, para evitar contar dos veces los bordes;
para la prueba de intersección se utilizan sus clausuras.

La identidad se comprueba directamente:

\[
 \frac{q_{n+1}}{M_{n+1}}
 =\frac{q_n}{M_n}+\frac{a_{n+1}}{d_nM_n}.
\]

Además, la división euclídea recupera
q_n = ⌊q_(n+1)/d_n⌋ y a_(n+1) = q_(n+1) mod d_n.
Esta recuperación utiliza el grado y el estado previo registrados.
No permite recuperar una historia arbitraria a partir de un escalar visible.

**Proposición 2.** Los intervalos se contraen a un punto si y sólo si
M_n tiende a infinito. Como d_n son enteros positivos, esto equivale
a que haya infinitas etapas con d_n ≥ 2.

**Demostración.** La longitud es 1/M_n. M_n es no decreciente.
Si sólo hay finitas etapas con d_n ≥ 2, M_n acaba siendo constante;
si hay infinitas, M_n ≥ 2^k tras k de ellas. La intersección de
intervalos cerrados anidados tiene longitud límite 1/lim M_n. ∎

Esta es una parametrización por grados. Su identificación con un lector
arquimediano concreto del corpus exige que coincidan las subdivisiones y
las convenciones de frontera de ese lector; no se impone por nomenclatura.

La profundidad n no es M_n. En un refinamiento ternario uniforme,
M_n = 3^n, no n. El ambiente de 729 palabras del censo tampoco se convierte
automáticamente en grado 729 de cada extensión TPK.

### 2.2 Qué permite afirmar sobre la fórmula de la captura

La captura define cardinalidad holográfica mediante una suma de pesos
angulares normalizada por π, y ordinalidad holográfica como longitud
de una ruta dividida por tres. La Proposición 1 no cambia esas definiciones.

Para identificar exactamente aquellas dos cantidades con w_n y M_n hay
que comprobar, con el peso y la ruta que realmente usa la captura,

\[
 \sum \rho_b=\pi_{\rm HMT} w_n,
 \qquad |\gamma_n|=3M_n.
\]

Si esas identidades se cumplen, su producto es uno por la Proposición 1.
No se las da por demostradas al definir M_n: son las dos ecuaciones
de identificación concretas que deben satisfacer los lectores históricos.
En particular, si |γ_n| designase sólo tres veces la profundidad n,
el producto sería n/3^n en el modelo ternario, no uno.

El límite de productos w_n M_n es uno. Cuando w_n → 0 y M_n → ∞,
eso NO autoriza la expresión aritmética “0 × ∞ = 1”.

**Procedencia:** el peso proyectivo es RESULTADO_RECUPERADO. La presentación
pareada w/M y su código mixto es FORMALIZACION_NUEVA en este expediente;
no se reclama prioridad sobre la identidad elemental ni novedad de la
intuición autoral de crecimiento interior/exterior.

## 3. Plegar conservando memoria no equivale a reducir los valores a 729

Sea P: Ω → B una lectura de bloque y m: Ω → Mem la memoria conservada.
Supongamos que existe un decodificador efectivo sobre la imagen conjunta:

\[
 D(P(x),m(x))=x.
\]

**Proposición 3.** La aplicación x ↦ (P(x),m(x)) es inyectiva.

**Demostración.** Si las dos coordenadas coinciden para x e y, aplicar D
da x = y. ∎

La hipótesis no se obtiene conservando x como una coordenada tautológica:
en una aplicación física o TPK debe proceder del transporte y su inversa,
como en el desarrollo previo de reconstrucción citado en las referencias.

Si B tiene 729 elementos y el lector de valor factoriza como Val = f ∘ P,
entonces su imagen contiene a lo sumo 729 valores. Por tanto, si el lector
produce siquiera 730 valores distintos, no puede factorizar de esa manera.
Para conservar todos los valores debe utilizar también la memoria o una
estructura interna que el rótulo de bloque no contiene.

Esta conclusión es compatible con la tesis autoral: importa dónde, por qué
ruta y con qué memoria se publica un valor. No se puede usar primero esa
memoria para conservar el continuo y después descartarla al contar sus valores.

La inyectividad de (P,m) tampoco implica la de Val: historias diferentes
pueden tener el mismo valor publicado. El objeto pertinente para CH es
Ω/~Val, no el conjunto de bloques ni la colección de prefijos finitos.

## 4. Compatibilidad con Mecánica Dimensional

La realización dimensional de la fuente es posterior a la genealogía.
Sea F una realización compatible de los registros y ν = F_*μ.
La definición de empuje da ν(A) = μ(F^−1(A)).
La conservación de peso se transporta sobre las imágenes de cilindros
cuando esas imágenes forman la partición correspondiente; si se fusionan,
sus pesos se suman. No se asigna a cada imagen fusionada el peso de
uno solo de sus antecedentes.

Si la realización conserva un código dimensional conjunto E y una
inversa D_MD con D_MD E = id, se aplica la Proposición 3. Si además E y
D_MD conmutan con las restricciones de nivel, sus límites satisfacen
D_MD,∞ E_∞ = id componente a componente.

Esta prueba incluye la realización dimensional sin convertir las unidades
SI, una masa o una constante física en selectores de ramas. No demuestra
la existencia de E para un aparato particular; transporta la reconstrucción
allí donde el mapa y su inversa están efectivamente construidos.
Ni un cambio de unidad ni esta identidad añaden un buen orden de los valores.

## 5. Actualización constructiva: plegado fiel y familias de valores

El material histórico sirve como orientación. La actualización no identifica
una diagonal con una fila ni usa el número de bloques como cardinal de los
valores. El objeto se organiza mediante tres mapas explícitos:

\[
 \widehat\Omega
 \xrightarrow{\ (P,m)\ }E(\widehat\Omega)
 \xrightarrow{\ D\ }\widehat\Omega
 \xrightarrow{\operatorname{Val}}Q_{\rm HMT},
 \qquad D(P(x),m(x))=x.
\]

El primer mapa publica bloque y memoria; el segundo reconstruye; el tercero
publica el valor. Las incidencias de la otra proyección siguen en el estado
completo. No se cambian por un nombre de valor ni se usan como un selector
externo del árbol.

La equivalencia de valores queda definida por la igualdad de Val.
La equivalencia de registros fieles queda definida por igualdad de (P,m).
No son la misma relación. Ambas quedan escritas para evitar que una
simplificación de borde modifique el conjunto que se está contando.

### 5.1 Familias admisibles por prolongación con testigos

Trabajamos primero en una carta compacta del continuo generado.
Sea Ω_m su espacio de historias, con los cilindros del corpus y su lector
continuo Val. Un testigo z es una sucesión de códigos naturales que
registra las decisiones auxiliares de admisibilidad; no contiene el
valor real que se desea obtener.

Una regla de compatibilidad de prefijos determina un árbol T de pares
de prefijos (u,v), donde u corresponde a una historia y v al testigo.
El árbol es cerrado por restricción. Su conjunto de ramas [T] es cerrado
en Ω_m × N^N. La familia publicada es

\[
 A_T=\{\operatorname{Val}(x):\exists z,\ (x,z)\in[T]\}.
\]

Este mecanismo incluye sistemas cerrados de historias y proyecciones con
testigos. Un nodo del árbol retiene el estado completo pertinente,
no sólo su rótulo escalar. Aquí se prueba un resultado para cualquier
árbol así producido; el criterio de admisibilidad concreto sigue siendo
el que entregue el constructor HMT, no uno seleccionado por el resultado.

### 5.2 Lema de separación de valores no numerables

Sea S un conjunto no numerable de valores en una carta real.
Un punto de S es de condensación si todo entorno suyo contiene una
cantidad no numerable de puntos de S.

Los puntos de S que no son de condensación forman un conjunto numerable:
para cada uno hay un intervalo de extremos racionales cuyo corte con S
es numerable; sólo hay numerablemente muchos intervalos de ese tipo.
La unión de sus cortes numerables es numerable.

Por ello S posee al menos dos puntos de condensación diferentes.
Podemos rodearlos mediante dos intervalos abiertos con clausuras
disjuntas y diámetros tan pequeños como se requiera.
Cada intervalo contiene una parte no numerable de S. Pueden escogerse
intervalos abiertos V_i con clausuras dentro de esos entornos y con
S∩V_i no numerable: se utiliza de nuevo un entorno de un punto de condensación.

Esta prueba usa los valores como lectura posterior para discriminar
familias que el árbol ya produce. No calcula nuevas semillas desde
intervalos objetivo. La distinción es importante: es una selección
demostrativa de una subfamilia, no el algoritmo generador del TPK.

### 5.3 Teorema de dicotomía mediante fusión de cilindros completos

**Teorema 4.** Si A_T no es numerable, contiene una copia continua e
inyectiva de {0,1}^N. En consecuencia su cardinal es el del continuo.

**Demostración.** Para un nodo p de T, sea A_p el conjunto de valores
de las ramas de [T] que extienden p. Partimos de un nodo con A_p
no numerable; si es necesario, se obtiene de una cubierta numerable
por nodos iniciales.

Construimos, para cada palabra binaria finita s, un nodo p_s del árbol
de historias y testigos y un intervalo cerrado J_s, de manera que:

1. A_(p_s) es no numerable y está contenido en J_s.
2. p_(s0) y p_(s1) extienden p_s.
3. las dos coordenadas de los prefijos crecen al menos un lugar
   en cada etapa;
4. J_(s0) y J_(s1) tienen clausuras disjuntas dentro de J_s;
5. el diámetro de J_s es a lo sumo 2^(-|s|), salvo la normalización inicial.

Supongamos construido p_s. El lema anterior proporciona dos intervalos abiertos V_0,V_1 cuyas
clausuras son disjuntas, están dentro del interior de J_s y tienen diámetro
suficientemente pequeño, con A_(p_s)∩V_i no numerable. Los dos extremos
de J_s no pueden contener por sí solos esa parte no numerable.
Para cada rama cuyo valor esté en V_i, la continuidad
de Val proporciona un prefijo de historia que fuerza a todas sus
prolongaciones a tener valor dentro de ese intervalo.
Prolongamos también el prefijo testigo y la longitud de ambos códigos.

Hay sólo numerablemente muchos pares de prefijos así elegibles.
Sus conjuntos de valores cubren la parte no numerable que se considera.
Por tanto, al menos uno de esos pares tiene una publicación no numerable.
Se elige uno en cada intervalo. Esos son p_(s0) y p_(s1); fijamos
J_(si)=clausura(V_i), que contiene A_(p_(si)).
Al inicio se puede pasar a un intervalo compacto acotado con parte
no numerable; a lo largo de la construcción se dejan márgenes para
que las clausuras siguientes queden en el intervalo precedente.

Para cada sucesión binaria b, los nodos
p_(b|1), p_(b|2), … determinan por unión una historia completa x_b
y un testigo completo z_b. El crecimiento de las dos longitudes
garantiza que no se deja ninguna coordenada sin determinar.
Cada prefijo pertenece a T y [T] es cerrado, de modo que
(x_b,z_b) pertenece a [T].

Definamos f(b)=Val(x_b). Sus valores están en los J_(b|n).
Si b y c se separan en una etapa, sus valores pertenecen a intervalos
disjuntos y son diferentes. Luego f es inyectiva.
Si comparten n decisiones, sus valores están en un intervalo de
diámetro a lo sumo 2^(-n); luego f es continua.

Así {0,1}^N se inyecta en A_T, mientras A_T ya es una familia de
valores reales. Ambas cotas dan |A_T|=2^ℵ0. ∎

La cifra 2 usada en la prueba cuenta las dos elecciones de la subfamilia
separada. No modifica el alfabeto APP ni el refinamiento TRIT ni sustituye
el árbol TPK por un emisor binario.

La selección de un nodo con publicación no numerable es una selección
matemática en la demostración. No se presenta como un test decidible
por Python. El código adjunto comprueba las identidades finitas y una
instancia explícita de la fusión; no certifica por cálculo esa selección
para todos los árboles.

### 5.4 Transporte del resultado al registro de borde y a MD

En cada nivel se aplica E=(P,m) al prefijo completo y se conserva el testigo.
Si E y su inversa D conmutan con las restricciones, el árbol transportado
es isomorfo al original sobre su imagen. Sus ramas corresponden una a una.

El lector sobre el registro es Val_B=Val∘D. Por tanto,

\[
 \{\operatorname{Val}_B(E(x)):\exists z,\ (x,z)\in[T]\}=A_T.
\]

Las divisiones del argumento anterior pueden hacerse antes o después
de ese transporte: se obtienen los mismos valores, no sólo el mismo
número de rótulos. Ésta es la igualdad que se necesitaba para aplicar
el plegado sin perder el problema cardinal.

Una realización MD que conserve ese registro mediante un par de
mapas inversos compatibles conserva asimismo la familia de valores.
Si únicamente conserva una magnitud y fusiona genealogías, la igualdad
se formula para esa magnitud específica y su relación de equivalencia;
no se la identifica con el conjunto completo de números.

### 5.5 Qué queda actualizado

La dependencia matemática reunida es:

\[
 \text{emisiones APP–TRIT–TPK}
 \longrightarrow\text{prefijos enriquecidos compatibles}
 \longrightarrow\text{árbol con testigos}
 \longrightarrow\text{ramas completas}
 \longrightarrow\text{valores publicados}.
\]

Sobre esa misma cadena se han dado dos pruebas diferentes y compatibles:

- una identidad exacta de peso y refinamiento, w_n M_n=1;
- una dicotomía cardinal para las familias A_T: numerables o del
  cardinal completo del continuo.

El plegado fiel y su realización dimensional transportan ambas sin
confundir memoria con valor. No se utiliza la repetición de una fase
como prueba de que se repita la historia completa.

**Procedencia:** arquitectura de cilindros, memoria y doble proyección,
ARQUITECTURA_AUTORAL_PREEXISTENTE; medida y dicotomía, RESULTADO_RECUPERADO
de la fuente nuclear; prueba de fusión aquí desplegada y transporte
del árbol al registro, FORMALIZACION_REUNIDA. No se reclama novedad
del teorema del conjunto perfecto.

## 6. Paso a todos los subconjuntos: potencia, rango y universo

La búsqueda de la promoción universal se ha separado en tres vías.
Se han leído completos los propietarios de los capítulos 18 y 19 del
integral vigente, el capítulo Gödel–Cohen de ese mismo ensamblado y el
propietario de potencia genealógica. La vía de rango no se reemplaza por
otra discusión sobre cifras decimales.

### 6.1 Vía A: transporte de la potencia plena mediante registro fiel

Ésta corrige el planteamiento de exigir una descripción analítica para
cada subconjunto. Sean Q el cociente por valores de historias completas
y Q_B el cociente por valores de registros plegados con memoria.
La reconstrucción produce una biyección

\[
 \bar E:Q\longrightarrow Q_B,\qquad \bar D\bar E=\mathrm{id}_Q,
 \quad \bar E\bar D=\mathrm{id}_{Q_B}.
\]

Para cualquier subconjunto A⊆Q, sin hipótesis topológicas o descriptivas,
se construye

\[
 \mathcal P(\bar E)(A)=\bar E[A].
\]

**Teorema 5.** La aplicación anterior es una biyección de P(Q) en P(Q_B).
Su inversa es la imagen directa por \bar D. Conserva inclusiones,
uniones arbitrarias, intersecciones arbitrarias y complementos.

**Demostración.** Para cualquier q, pertenecer a
\bar D[\bar E[A]] equivale a pertenecer a A, porque \bar D\bar E es
la identidad. El argumento inverso es idéntico.
La imagen directa conserva cualquier unión por definición.
La inyectividad implica que un elemento que pertenece a todas las
imágenes tiene el mismo antecedente en todos los conjuntos, lo que
prueba la conservación de intersecciones.
Finalmente, \bar E[Q\A]=Q_B\bar E[A] por biyectividad. ∎

Así se conserva el cuantificador “todo subconjunto” durante el plegado.
No se lo reemplaza por “todo subconjunto cerrado” ni “todo subconjunto
con testigo numerable”. La pertenencia a A se transporta; no se afirma
que el TPK reciba A como entrada para generar sus números.

La consecuencia adicional es exacta: si se produce una inyección
j:Q_B→ω1, entonces j∘\bar E inyecta TODOS los valores de Q en ω1.
El Teorema 5 conserva después cualquiera de sus subconjuntos.
Éste es el enlace adecuado con CH, sin reclamar una codificación
analítica universal de la potencia.

### 6.2 Vía B: rango genealógico del universo fijado por el corpus

El capítulo 19 define h como el código del lenguaje, tablas, transiciones
y lectores producidos, y fija M=L[h]. Aquí se recupera ese alcance y se
despliega la construcción de su rango. No se presenta la introducción
de L[h] como una identidad obtenida sólo de multiplicar grados finitos.

La jerarquía relevante es

\[
 L_0[h]=\varnothing,\qquad
 L_{\beta+1}[h]=\operatorname{Def}_h(L_\beta[h]),\qquad
 L_\lambda[h]=\bigcup_{\beta<\lambda}L_\beta[h].
\]

Def_h conserva el predicado h en el lenguaje de definición.
Para h⊆ω, el lema de condensación relativizado utilizado por el corpus
sitúa cada real de M en un nivel L_β[h] con β<ω1^M.
Esta dependencia es conjuntista y está declarada: el bucle Python
de profundidades finitas no sustituye el lema.

Para precisar ese uso: dentro de M se toma un nivel L_θ[h] suficientemente
grande que contenga el real r, y un submodelo elemental numerable
que contenga r, h y todos los naturales. Su colapso transitivo fija r
y h; por condensación es un nivel L_β[h] de altura numerable en M.
Por tanto r aparece antes de ω1^M. Los niveles de altura numerable son
numerables en M: en cada sucesor hay numerablemente muchas fórmulas
y tuplas finitas de parámetros, y en un límite numerable se unen
numerablemente muchos niveles numerables.

Sea β(r) la menor etapa sucesora en la que aparece r.
En cada nivel se toma la enumeración numerable escogida por el buen
orden constructible de M y se restringe a los reales cuya primera
aparición es esa etapa. Su índice j_β(r) es natural. Así,

\[
 R(r)=(\beta(r),j_{\beta(r)}(r))
\]

es una inyección de R^M en ω1^M×ω. La pareja conserva la etapa y
el índice local; la etapa sola podría identificar muchos reales.
Ordenamos la imagen D de R lexicográficamente, primero β y luego j.

**Teorema 6.** D tiene tipo de orden ω1^M, y produce una biyección

\[
 b_h:\omega_1^M\longrightarrow\mathbb R^M.
\]

**Demostración.** El orden de ω1^M×ω por bloques tiene tipo
ω·ω1^M=ω1^M. Todo subconjunto suyo tiene tipo a lo sumo ω1^M.
D no es numerable en M, porque es biyectivo con R^M; por tanto su tipo
no es un ordinal menor que ω1^M. Es exactamente ω1^M.
Componer el isomorfismo de orden ω1^M→D con la inversa de R da b_h. ∎

La composición causal con la evaluación y el registro es ahora explícita:

\[
 \rho_h=b_h^{-1}\circ\operatorname{Val}_h,\qquad
 \rho_{B,h}=b_h^{-1}\circ\operatorname{Val}_h\circ D.
\]

Por inyectividad de b_h^{-1},

\[
 \rho_h(x)=\rho_h(y)
 \Longleftrightarrow
 \operatorname{Val}_h(x)=\operatorname{Val}_h(y).
\]

El registro completo no se destruye al añadir ese rango; éste es otro
lector. Su valor ordinal no contiene por sí solo toda la genealogía.

**Corolario 7, con cuantificador completo en M.**
Para todo A∈M con A⊆R^M, A es numerable en M o existe en M una
biyección entre A y R^M. No se exige que A sea analítico.

**Demostración.** Sea B=b_h^{-1}[A]⊆ω1^M.
Si B es numerable, también A. Si no lo es, B con el orden heredado
tiene tipo exactamente ω1^M: tiene tipo a lo sumo ω1^M y no puede
tener tipo menor, porque todos los ordinales menores son numerables.
Su enumeración creciente ω1^M→B, seguida de b_h, enumera A.
Componer con b_h^{-1}:R^M→ω1^M da la biyección requerida. ∎

Éste no es un resultado limitado a conjuntos analíticos.
Es CH para todos los subconjuntos del modelo que fija el capítulo 19.
Su estatuto es RESULTADO_RECUPERADO, con la composición y el
cuantificador desarrollados explícitamente.

### 6.3 Vía C: condición suficiente de promoción al dominio ambiente

Fijemos ahora un universo ambiente V en el que se interpretan los
conjuntos y M=L[h] como su modelo interno. La frase “todos” debe
conservar el mismo dominio antes y después del argumento.

**Teorema 8.** Si R^V=R^M, la biyección anterior demuestra CH en V,
incluso para subconjuntos de R^V que no pertenezcan a M.

**Demostración.** La función b_h pertenece a M y por tanto a V.
La igualdad de reales hace que siga siendo sobreyectiva sobre R^V.
Todo ordinal numerable en M lo sigue siendo en V, porque se conserva
su enumeración; luego ω1^M≤ω1^V.
Si ω1^M fuera numerable en V, b_h enumeraría R^V con un conjunto
numerable, contradiciendo su no numerabilidad.
Así ω1^M=ω1^V y b_h es en V una biyección ω1^V→R^V.
Para cualquier A⊆R^V existente en V se repite allí la prueba del
Corolario 7, sin exigir A∈M. ∎

La igualdad R^V=R^M no se obtiene del hecho de compartir h.
En efecto, el código del árbol contiene sus reglas y nodos finitos;
una historia completa es una sucesión que satisface esas reglas.
Es necesario comprobar también en qué universo se toman todas esas
sucesiones, no sólo que coincidan los prefijos.

Bajo las coberturas y el lector absoluto del capítulo 18, esa igualdad
se puede comprobar mediante la clausura de las historias completas:

\[
 \widehat\Omega_h^V=\widehat\Omega_h^M
 \quad\Longleftrightarrow\quad
 \mathbb R^V=\mathbb R^M.
\]

La dirección de izquierda a derecha aplica el mismo lector a las
mismas historias y usa la cobertura en ambos dominios.
Para la otra dirección se codifica una historia y su memoria mediante
una sucesión numerable de enteros, es decir, mediante un real.
Si todos esos códigos ya pertenecen a M, la reconstrucción finitaria
definida por h pertenece a M y devuelve la misma historia. Las
condiciones locales de compatibilidad son las mismas.

Esta equivalencia explicita qué tendría que proporcionar la extensión
del argumento: clausura de TODOS los códigos completos de memoria en M,
no sólo conservación de cada código que ya se haya producido allí.

### 6.4 Vía D: ampliación del rango sin exigir ausencia de reales nuevos

La condición de la sección 6.3 es suficiente, pero no es necesaria
para una ampliación del rango. El propietario nuclear sucesor lo
advierte expresamente: el separador ambiente puede requerir una
reindexación, en lugar de una prolongación que conserve literalmente
cada etiqueta ordinal anterior.

Trabajamos en V, con M=L[h] como antes. Escribamos

\[
 N_h=\mathbb R^V\setminus\mathbb R^M.
\]

Esto separa valores nuevos, no historias nuevas: una historia de V
que no pertenezca a M puede publicar un valor que sí pertenezca a M.
Esa historia debe recibir la misma etiqueta que cualquier otra de su
fibra, sin que se descarte su memoria.

**Teorema 9.** Existe un separador de todas las fibras de Val en V
con valores en ω1^V si y sólo si existe una inyección
κ:N_h→ω1^V. Cuando existe κ, el separador se obtiene mediante una
reindexación explícita del separador heredado.

**Demostración.** En ω1^V definimos dos columnas ordinales disjuntas:

\[
 j_0(\xi)=\omega\cdot\xi,\qquad
 j_1(\xi)=\omega\cdot\xi+1.
\]

Para cada ordinal numerable ξ, ambos valores son numerables.
Cada columna es inyectiva y las dos imágenes son disjuntas.
La multiplicación es ordinal, con ω a la izquierda.
Puesto que ω1^M≤ω1^V, la primera columna también admite las
etiquetas antiguas. Definimos sobre cada historia completa x de V:

\[
 \rho_V(x)=
 \begin{cases}
 j_0\bigl(b_h^{-1}(\operatorname{Val}(x))\bigr),
    &\operatorname{Val}(x)\in\mathbb R^M,\\
 j_1\bigl(\kappa(\operatorname{Val}(x))\bigr),
    &\operatorname{Val}(x)\in N_h.
 \end{cases}
\]

En cada caso, la inyectividad de b_h^{-1} o de κ hace que
ρ_V(x)=ρ_V(y) equivalga a Val(x)=Val(y). Entre casos distintos,
las etiquetas no coinciden porque las columnas son disjuntas.
Sobre las historias de M, la función coincide con j_0∘ρ_h.
No se ha modificado ninguna historia ni operación APP–TRIT–TPK:
se ha construido una publicación ordinal posterior.

Recíprocamente, un separador de fibras induce una función
r↦ρ_V(x), con Val(x)=r, independiente del representante x.
La cobertura garantiza su definición para cada r∈R^V, y la
separación de fibras garantiza su inyectividad. Su restricción a N_h
es la inyección κ requerida. ∎

El teorema evita una exigencia excesiva: no hay que demostrar que
N_h sea vacío. Hay que construir su índice κ, o una estructura que
lo produzca. Reindexar deja espacio para etiquetas nuevas, pero no
asigna por sí solo una etiqueta a cada valor nuevo. κ figura
explícitamente como hipótesis del teorema, no como salida acreditada
del generador.

### 6.5 Construcción suficiente mediante niveles de valores completos

La búsqueda anterior se puede convertir en un constructor preciso.
No necesita que cada subconjunto de la recta sea analítico, ni que
cada fibra de historias sea numerable.

**Teorema 10.** Supongamos construida en V una familia
(Γ_ξ)_{ξ<ω1^V} de historias completas admisibles, junto con

\[
 C_\xi=\operatorname{Val}[\Gamma_\xi]\cap N_h,
 \qquad e_\xi:C_\xi\hookrightarrow\omega,
 \qquad N_h=\bigcup_{\xi<\omega_1^V}C_\xi.
\]

Entonces los niveles producen κ y, por el Teorema 9, un separador
de todas las fibras del continuo ambiente.

**Demostración.** Para cada r∈N_h existe un primer nivel

\[
 \xi(r)=\min\{\xi:r\in C_\xi\}.
\]

Definimos

\[
 \kappa(r)=\omega\cdot\xi(r)+e_{\xi(r)}(r)<\omega_1^V.
\]

Los intervalos ordinales [ω·ξ,ω·ξ+ω) son disjuntos para
índices distintos. Dentro de un mismo intervalo, e_ξ es inyectiva.
Así κ es inyectiva. Si sólo se proporciona la numerabilidad de
cada C_ξ, la elección de la familia e_ξ utiliza elección en V;
no se presenta como un algoritmo finitario ni como una selección
ya producida por el TPK. ∎

Para aplicar este constructor desde HMT se requieren tres pruebas
materiales, en este orden:

1. Dar Γ_ξ a partir de las operaciones existentes, con historias
   completas y memoria conservada; no definirla retrospectivamente
   como la fibra de una supuesta solución ordinal.
2. Construir e_ξ o demostrar que la imagen C_ξ es numerable.
   La imagen de un nivel de prefijos no es la imagen del conjunto
   de sus prolongaciones completas.
3. Demostrar que para cada historia completa x de V cuyo valor
   no esté en M existe ξ con Val(x)∈C_ξ. Basta cubrir las fibras
   por sus valores: no es necesario que cada representante x
   pertenezca personalmente a algún Γ_ξ.

La tercera condición es deliberadamente más débil que exigir
Γ_ξ exhaustivas como conjuntos de historias enriquecidas. El
separador puede actuar sobre la fibra completa conservada, aunque
el constructor utilice un representante para indexar su valor.
El transporte E,D de las secciones anteriores permite publicar
el mismo rango en la frontera sin eliminar esa información.

Este esquema no se cuenta como una prueba adicional de CH: es
una implicación cuyo dato decisivo es la cobertura numerable por
ω1 niveles. El corpus consultado proporciona esa cobertura para
los niveles de L[h]; no se ha derivado aquí una familia Γ_ξ que
cubra las fibras restantes de V. Atribuirle esa cobertura por
definición introduciría precisamente el cuantificador que se está
intentando demostrar.

### 6.6 Estado matemático del desarrollo

Ya están reunidos cinco resultados distintos:

1. Plegar con memoria transporta la potencia plena, no únicamente
   sus subconjuntos regulares.
2. El rango de L[h] cierra el cuantificador sobre todos sus
   subconjuntos; no se reduce a la dicotomía analítica.
3. La igualdad de reales o de historias completas transportaría
   ese cierre al universo ambiente y a todos sus subconjuntos.
4. Esa igualdad no es necesaria para extender el rango: se puede
   reindexar el rango heredado y añadir una columna para valores nuevos,
   siempre que se construya su índice κ.
5. Una familia de niveles con imágenes numerables que cubra esos
   valores produciría κ mediante la fórmula explícita del Teorema 10.

El tercer resultado es una implicación demostrada, no una prueba
de su antecedente. En la lectura de los propietarios de cobertura
y rango no se ha producido una demostración de ese antecedente para
un universo ambiente arbitrario. La cobertura del capítulo 18 permite
reconstruir una historia a partir de cada real del dominio en que se
ejecuta; no convierte esa historia automáticamente en un elemento
del modelo interno L[h].

El objetivo de CH ambiente sigue abierto en este expediente.
No se renombra CH ambiente como CH en M para declarar terminado
el encargo. Tampoco se descarta el rango ya construido en M:
se conserva y se identifican dos vías suficientes distintas de
promoción: ausencia de valores nuevos, o indexación de los valores
nuevos mediante niveles de imágenes numerables. Ninguno de esos
antecedentes se declara probado para V en este expediente.


## 7. Alcance de los controles y conservación

El programa adjunto usa sólo enteros, fracciones exactas y biblioteca estándar.
Comprueba subdivisiones de árboles de control, las identidades de las
secciones 2–3 y una instancia de la fusión de cilindros construida en la sección 5.
Las demostraciones generales están escritas arriba: ejecutar un
número finito de casos no sustituye la inducción, la fusión ni el
lema de condensación utilizado por el propietario del rango.

El programa NO ejecuta el censo completo ni certifica que cada árbol de
control coincida con Ext del TPK. Lo identifica explícitamente como control.
No calcula miles de cifras de constantes. No declara resuelta CH.
Los recibos causales y hashes verifican trazabilidad, no la conclusión de CH.

No se han modificado PDFs, manuscritos compartidos, índices, skills ni
manifiestos sellados. El fallo conocido del arranque editorial por divergencia
del índice de referencias no se repara manipulando sus hashes: este
expediente separado no se presenta como edición global certificada.

## 8. Fuentes materiales

- [Clausura cardinal vigente: capítulos 18 y 19](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c19_sin_encabezado.tex:595>).
- [Fuente nuclear: medida, cilindros y alcance cardinal](</Users/ruben/Documents/EXTRA/PAPER_NUCLEAR_HMT_CONTINUO_AUTONOMO_2026-09-02/source/sections/03_continuo.tex:130>), con §3.7 desde línea 498.
- [Sucesor nuclear: rango constructible y reindexación](</Users/ruben/Documents/EXTRA/PAPER_NUCLEAR_HMT_CONTINUO_AUTONOMO_2026-09-02/SUCESOR_ACADEMICO_AUTONOMO_20260902/source/sections/05_estatuto_cardinal_zfc.tex:489>), con la reindexación desde línea 553.
- [Formulación nuclear: cociente y fase](</Users/ruben/Documents/EXTRA/PAPER_NUCLEAR_HMT_CONTINUO_AUTONOMO_2026-09-02/source/sections/01_formulacion.tex:74>).
- [HTT/CANTOR–LATTICE histórico](</Users/ruben/Desktop/GTP+/20-2025/EULER-GODEL.txt:4039>), especialmente líneas 4100–4180.
- [Arquitectura narrativa: número, medida e historia](</Users/ruben/Documents/excelencia academica/LIBRO_NARRATIVO_HMT_MD_PARALELO_2026-08-13/01_ARQUITECTURA_DEFINICIONES_Y_VOZ_COAUTORAL.md:410>).
- [Desarrollo previo: acoplamiento y reconstrucción](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/ACOPLAMIENTO_PRESENTE_Y_RECONSTRUCCION_20260910.md>).
- [Integral vigente, conservado: 2.249 páginas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/02_PDF/INTEGRAL/main_paquete_union_demostrativa_20260904.pdf>).
- [Corpus activo y desarrollos adyacentes](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/CORPUS_ACTIVO.md>).

La lectura de esta investigación es focal. La presencia del último enlace
no implica una nueva lectura integral de las 2.249 páginas.
