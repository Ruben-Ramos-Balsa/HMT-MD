# Refinamiento conservativo de la unidad y memoria de acarreos

14 de septiembre de 2026. Nota nueva de la tercera ampliación. No modifica la segunda ampliación sellada, el paper de 326 páginas, sus fuentes o sus recibos. Formaliza un transporte afín posterior, su memoria exacta y su límite; no identifica por coincidencia de cifras una generación de α.

## 1. Procedencia y punto de corte

La completación 1000=729+271 y su descomposición 1000=729+243+27+1 pertenecen a la arquitectura autoral preexistente, conservada en el [contrato operativo](</Users/ruben/Documents/New project/AGENTS.md:475>) y en su [columna vertebral](</Users/ruben/Documents/New project/AGENTS.md:599>). No se presentan como hallazgos de esta nota.

La ampliación anterior reunió la identidad y su lectura operatoria

\[
73=9^2-9+1=\frac{9^3+1}{9+1}=\frac{729+1}{10},
\]

en [CONSTANTE_Y_NORMA_TRITICA.md](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_02_NOMBRE_Y_RADIO_20260914/CONSTANTE_Y_NORMA_TRITICA.md:142>), líneas 142–166: factor fijo 10, índice ternario 73 y Gram 73I+27P₀ del socio 9I+U.

El bloque central y sus concatenaciones están construidos en [centro_electronico_registros.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/centro_electronico_registros.tex:36>), líneas 36–48: B_c=[[7,2],[2,7]]=9P₊+5P₋ y 72+27=77+22=99. El propietario completo distingue posición central, autovalores, cocientes APP, orientación y firma regional. Aquí se compone exclusivamente su lectura matricial; no se vuelve a identificar esos objetos por coincidencia numérica.

El principio de conservar contribuciones de eventos, carga, prefijos y cociclos afines tiene como propietario [registro_imagen_integral.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_imagen_integral.tex:203>), líneas 203–263. Ese propietario exige reglas prospectivas sobre eventos antes de evaluar su salida; la independencia de una partición no autoriza escoger contribuciones a partir del resultado esperado.

El corte de esta nota es preciso: se reciben objetos producidos por APP–TRIT–TPK y sus publicaciones de norma/completación; se estudia después una familia afín explícita sobre parejas enteras. La ley de acarreo que una historia HMT particular aporte debe conservar su procedencia. La aritmética siguiente no declara que cada sucesión acotada sea esa historia ni que el primer acarreo 1 se repita por necesidad.

Estatuto: las completaciones y la relación de 73 con la norma ternaria conservan su procedencia; el transporte afín reunido, su inversa por residuos, la codificación finita y el teorema de cilindros se presentan como **FORMALIZACION_NUEVA en esta exploración**. No se reclama prioridad mundial para la aritmética posicional o las series geométricas que intervienen como métodos de prueba posteriores.

## 2. El paso exacto entre la norma cuadrática y la completación cúbica

Sea b un entero ≥1 y B=b+1≥2. Definimos

\[
p_b=b^2-b+1,\qquad q_b=B^2-p_b=3b.
\tag{1}
\]

**Proposición 1.** Se tiene

\[
Bp_b=b^3+1,\qquad
Bq_b+1=3b^2+3b+1=B^3-b^3.
\]

En consecuencia,

\[
\boxed{(p_b,B^2-p_b)
\longmapsto(Bp_b-1,B(B^2-p_b)+1)
=(b^3,B^3-b^3).}
\tag{2}
\]

**Prueba.** La factorización b³+1=(b+1)(b²−b+1) da la primera igualdad; la segunda es la expansión de (b+1)³−b³. La suma de la pareja inicial es B² y la de la pareja final es B³. ∎

Para b=9, B=10,

\[
p_9=73,\quad q_9=100-73=27,\qquad
\boxed{(73,27)\longmapsto(10\cdot73-1,10\cdot27+1)
=(729,271).}
\tag{3}
\]

El complemento 271 conserva sus tres contribuciones: 243+27+1. La corrección (−1,+1) tiene suma cero. No conserva la suma entera sin reescala: la multiplicación por B la lleva de B² a B³. Lo conservado exactamente es la unidad normalizada,

\[
\frac{p_b}{B^2}+\frac{q_b}{B^2}=1,
\qquad
\frac{b^3}{B^3}+\frac{B^3-b^3}{B^3}=1.
\]

El transporte entre las dos parejas normalizadas es

\[
\left(\frac{p_b}{B^2},\frac{q_b}{B^2}\right)
\longmapsto
\left(\frac{p_b}{B^2}-\frac1{B^3},
\frac{q_b}{B^2}+\frac1{B^3}\right).
\tag{4}
\]

Este paso no implica por sí solo conservación de una norma cuadrática, una energía física o un observable de todos los estados. La conservación demostrada aquí es la suma, con su cambio explícito de unidad.

### 2.1. Enlace con las concatenaciones del bloque central

Para esta extensión tomamos b≥2, de modo que b−2 y 2 sean dígitos válidos en base B=b+1. Consideramos la familia algebraica posterior

\[
B_c^{(b)}=\begin{pmatrix}b-2&2\\2&b-2\end{pmatrix}.
\]

El caso b=9 es exactamente el bloque del propietario; no se afirma que todas las matrices de esta familia sean evaluaciones centrales del atlas HMT. Con el lector de concatenación C_B(u,v)=Bu+v, sus dos filas producen

\[
\begin{aligned}
C_B(b-2,2)&=B(b-2)+2=b(b-1)=p_b-1,\\
C_B(2,b-2)&=2B+(b-2)=3b=q_b.
\end{aligned}
\tag{4a}
\]

La suma es p_b−1+q_b=B²−1. Añadir la unidad complementaria a la primera lectura da (p_b,q_b), de suma B², y el paso L₁ de (2) proporciona la completación cúbica. Así se obtiene la composición exacta

\[
\boxed{(p_b-1,3b)
\xrightarrow{\ +(1,0)\ }(p_b,3b)
\xrightarrow{\ L_1\ }(b^3,B^3-b^3).}
\tag{4b}
\]

En b=9 la cadena es

\[
\boxed{(72,27)\longmapsto(73,27)\longmapsto(729,271).}
\tag{4c}
\]

La primera flecha y la segunda tienen funciones diferentes. La primera restaura la unidad complementaria de B²−1; incrementa la suma de la pareja en 1. La segunda multiplica la escala por B y transfiere una unidad con corrección de suma cero. No se las presenta como una única conservación cerrada de la pareja sin registrar esa aportación.

Si se quiere mantener explícita la unidad antes de integrarla, el registro de tres componentes (p_b−1,3b,1) ya suma B², y la aplicación declarada (x,y,r)↦(x+r,y,0) conserva esa suma. Para invertir esta integración se debe conservar que r=1; sobre triples arbitrarios el mapa no es inyectivo. Esta escritura es contabilidad matemática de la restauración, no una afirmación de que se haya demostrado aquí una reserva física adicional.

El bloque y sus concatenaciones son antecedentes; reunirlos con la restauración unitaria y el acarreo L₁ es la formalización adicional. La composición no prueba por igualdad escalar que un estado físico sea el mismo observado desde otra perspectiva. Tampoco decide c₂,c₃,…: sólo determina el acarreo 1 del paso (4b).

## 3. Transporte afín, inversa y dominio de positividad

Para B entero ≥2 y un acarreo c entero definimos

\[
\boxed{L_c(x,y)=(Bx-c,By+c).}
\tag{5}
\]

El signo de c especifica una transferencia entre las dos coordenadas. Si c es positivo, la primera disminuye respecto de Bx y la segunda aumenta en la misma cantidad.

**Proposición 2.** Sobre R², con B y c conocidos,

\[
L_c^{-1}(X,Y)=\left(\frac{X+c}{B},\frac{Y-c}{B}\right),
\qquad X+Y=B(x+y).
\tag{6}
\]

Sobre Z², esta inversa es entera exactamente cuando X+c e Y−c son divisibles por B. Si se parte de x,y≥0, la salida sigue siendo no negativa exactamente cuando

\[
-By\le c\le Bx.
\tag{7}
\]

Las igualdades se comprueban por sustitución. La condición (7) mantiene separado el dominio de parejas no negativas del dominio algebraico entero general.

Para los acarreos canónicos c∈{0,…,B−1}, todas las ramas son admisibles si x≥1 e y≥0. Si x=0, sólo c=0 conserva la no negatividad. No se omite este caso de frontera.

## 4. El residuo recupera la última operación

**Teorema 3. Inversa canónica por residuo.** Sea M≥1 entero y sea (X,Y) una pareja entera no negativa con X+Y=BM. Existe una única terna admisible (x,y,c) tal que

\[
x+y=M,\quad c\in\{0,\ldots,B-1\},\quad L_c(x,y)=(X,Y).
\]

Se obtiene mediante

\[
\boxed{c=Y\bmod B=(-X)\bmod B,\qquad
y=\frac{Y-c}{B},\qquad x=\frac{X+c}{B}.}
\tag{8}
\]

**Prueba.** Toda preimagen satisface Y≡c módulo B. El representante en {0,…,B−1} es único. La divisibilidad de X+c se sigue de X+Y≡0. La división euclídea de Y da y≥0, y X+c≥0 da x≥0. Si c>0, x no puede ser cero porque ello exigiría X=−c<0. La suma de las preimágenes es M. Finalmente, (6) verifica la imagen. ∎

Así, el acarreo no tiene que conservarse como una etiqueta externa separada **cuando** pertenece al alfabeto canónico y se conserva la pareja entera con su escala: su residuo lo contiene. El resultado es una biyección entre las ternas admisibles de entrada y las parejas de suma BM, no una mera inclusión nominal.

Como control de cardinalidad, hay M+1 entradas en la rama c=0 y M en cada una de las B−1 ramas restantes, en total BM+1, que coincide con el número de parejas no negativas de suma BM.

Para un acarreo entero no canónico, el residuo sólo recupera c módulo B. Escribiendo

\[
c=r+B\ell,\qquad r\in\{0,\ldots,B-1\},
\]

se debe conservar además la elevación entera ℓ para reconstruir

\[
y=\frac{Y-r}{B}-\ell,\qquad
x=\frac{X+r}{B}+\ell.
\tag{9}
\]

Este dato no se obtiene del residuo por sí solo.

## 5. Iteración variable y memoria finita completa

Fijemos B y una pareja inicial entera (x₀,y₀), de suma M₀>0. Los acarreos c₁,c₂,… se reciben como una secuencia de operaciones, no se eligen por un valor objetivo. Sea

\[
(x_n,y_n)=L_{c_n}\cdots L_{c_1}(x_0,y_0),\qquad
C_n=\sum_{j=1}^n c_jB^{n-j},\quad C_0=0.
\]

**Teorema 4. Registro acumulado exacto.** Para todo n≥0,

\[
\boxed{
x_n=B^n x_0-C_n,\qquad
y_n=B^n y_0+C_n,\qquad
x_n+y_n=B^nM_0,}
\tag{10}
\]

y el registro satisface Cₙ₊₁=BCₙ+cₙ₊₁.

**Prueba.** La fórmula es inmediata en n=0. Sustituirla en (5) añade el término cₙ₊₁ y multiplica los anteriores por B, lo que da la recurrencia y el paso inductivo. ∎

Si los acarreos son canónicos,

\[
0\le C_n\le B^n-1.
\tag{11}
\]

En particular, x₀≥1 e y₀≥0 garantizan positividad en todos los pasos: xₙ≥Bⁿ(x₀−1)+1 e yₙ≥0.

### Reconstrucción de toda la historia finita

Con B, n y la pareja entera final se recuperan

\[
\boxed{
C_n=y_n\bmod B^n,\quad
y_0=\left\lfloor\frac{y_n}{B^n}\right\rfloor,\quad
x_0=\frac{x_n+C_n}{B^n},}
\tag{12}
\]

y después

\[
\boxed{c_j=
\left\lfloor\frac{C_n}{B^{n-j}}\right\rfloor\bmod B,
\qquad 1\le j\le n.}
\tag{13}
\]

Equivalentemente se aplica (8) n veces, desde el último paso. La pareja final y la profundidad conservan tanto la entrada como la palabra finita completa de operaciones canónicas. Las divisiones euclídeas constituyen la prueba de recuperabilidad; no se ha retenido la entrada como una coordenada independiente por definición.

La profundidad importa: los ceros iniciales de una palabra forman parte de su registro aunque no cambien el entero Cₙ. Si M₀ se conserva en lugar de n, puede recuperarse n de la igualdad exacta (xₙ+yₙ)/M₀=Bⁿ. Al normalizar ambas coordenadas para que sumen 1 se pierde ese contador de escala si no se lo guarda por separado.

### Composición de bloques y cambio de partición

Un bloque de n pasos con acumulado C actúa como

\[
L^{[n]}_C(x,y)=(B^nx-C,B^ny+C).
\]

Para dos bloques consecutivos,

\[
\boxed{L^{[m]}_D\circ L^{[n]}_C
=L^{[n+m]}_{B^m C+D}.}
\tag{14}
\]

La ley (n,C),(m,D)↦(n+m,BᵐC+D) es asociativa por composición de aplicaciones. El factor Bᵐ transporta la contribución del primer bloque a la escala del segundo. Conserva el resultado al reagrupar los mismos eventos; no afirma que añadir eventos nuevos deje fija la pareja.

## 6. Límite con acarreos acotados y cota de error

Normalicemos por Mₙ=BⁿM₀:

\[
f_n=\frac{x_n}{M_n},\qquad g_n=\frac{y_n}{M_n},\qquad
\theta_n=\frac{C_n}{B^n}=\sum_{j=1}^n\frac{c_j}{B^j}.
\]

Entonces

\[
\boxed{f_n=\frac{x_0}{M_0}-\frac{\theta_n}{M_0},\qquad
g_n=\frac{y_0}{M_0}+\frac{\theta_n}{M_0},\qquad
f_n+g_n=1.}
\tag{15}
\]

**Teorema 5. Convergencia para acarreos acotados.** Si |c_j|≤C para todo j, la serie

\[
\theta=\sum_{j\ge1}\frac{c_j}{B^j}
\]

converge absolutamente y define límites f y g de suma 1. Además,

\[
\boxed{|f-f_n|=|g-g_n|
\le\frac{C}{M_0(B-1)B^n}.}
\tag{16}
\]

**Prueba.** El valor absoluto de la cola de θ es como máximo

\[
C\sum_{j=n+1}^{\infty}B^{-j}
=\frac{C}{(B-1)B^n}.
\]

La sustitución en (15) prueba la cota y la conservación del total en el límite. ∎

La convergencia no implica por sí sola positividad. Si se permiten acarreos con ambos signos, una condición suficiente para conservarla en todas las etapas es x₀,y₀≥C/(B−1). Para el alfabeto canónico, basta la condición más débil x₀≥1,y₀≥0 ya demostrada.

En el caso canónico c_j∈{0,…,B−1}, se tiene 0≤θ≤1, fₙ es no creciente y gₙ no decreciente. La cota se simplifica a

\[
0\le f_n-f=g-g_n\le\frac1{M_0B^n}.
\tag{17}
\]

Lo conservado es la suma normalizada, la transferencia acumulada y —si se retiene el registro entero con escala— la historia canónica finita. Las proporciones individuales fₙ y gₙ pueden cambiar en cada paso.

## 7. Consecuencia adicional: cilindros compatibles, fronteras y memoria

En esta sección se considera el alfabeto canónico completo, sin una selección adicional de historias. Todas sus prolongaciones conservan la no negatividad cuando x₀≥1,y₀≥0, como ocurre para (p_b,q_b). En ese dominio, un prefijo de n acarreos, con acumulado Cₙ, permite exactamente las prolongaciones cuyos límites θ pertenecen al intervalo

\[
\boxed{I_n(C_n)=
\left[\frac{C_n}{B^n},\frac{C_n+1}{B^n}\right].}
\tag{18}
\]

**Teorema 6. Cilindros anidados y clasificación de la pérdida de memoria.**

1. Si se añade el acarreo c, el cilindro hijo Iₙ₊₁(BCₙ+c) está contenido en Iₙ(Cₙ). Los B hijos cubren el padre y sólo se solapan en sus extremos.
2. Los cilindros de una historia infinita tienen diámetro B⁻ⁿ y una única intersección. Su imagen para la fracción f tiene diámetro 1/(M₀Bⁿ), coincidente con (17).
3. Dos historias canónicas distintas producen el mismo θ únicamente mediante la ambigüedad de una frontera: en la primera posición distinta sus dígitos difieren en 1; después, la historia de dígito menor tiene todos los acarreos B−1 y la otra todos 0.

**Prueba.** La fórmula de los extremos después de añadir c demuestra la inclusión y la partición en B subintervalos. La cola de la serie recorre todo [0,B⁻ⁿ], por lo que (18) describe exactamente las prolongaciones; la elección sucesiva de subintervalos prueba su realización. La compacidad y los diámetros decrecientes prueban la intersección única.

Para el punto 3, sea k la primera posición distinta y supóngase d_k>c_k. Si ambos límites fueran iguales,

\[
\frac{d_k-c_k}{B^k}
=\sum_{j>k}\frac{c_j-d_j}{B^j}
\le\sum_{j>k}\frac{B-1}{B^j}=\frac1{B^k}.
\]

Como la diferencia de dígitos es un entero positivo, debe valer 1. Alcanzar la igualdad en la cota exige c_j=B−1 y d_j=0 para todo j>k. La recíproca es la misma suma geométrica. ∎

Así, la lectura arquimediana del límite es única para cada historia, pero un valor aislado de frontera puede corresponder a dos historias. Por ejemplo,

\[
(1,0,0,\ldots),\qquad(0,B-1,B-1,\ldots)
\]

producen ambas θ=1/B, aunque sus prefijos y sus estados enteros finitos sean distintos. Una convención canónica de expansiones, o una marca de frontera conservada, distingue esas dos procedencias. Si se excluyen las colas finalmente constantes B−1 para θ<1, se obtiene la expansión usual única; el extremo θ=1 requiere conservarse aparte, pues dentro de este alfabeto fraccionario corresponde a la cola constante B−1.

Este resultado separa tres objetos: la historia de operaciones, el sistema de cilindros compatibles y el número límite. Su vínculo está probado por las flechas explícitas, no por identificarlos nominalmente.

### Acarreos con signo: la convergencia no basta para reconstruirlos

Incluso a profundidad finita, permitir acarreos fuera del alfabeto canónico destruye la unicidad sin sus elevaciones. Sobre la misma pareja inicial y en dos pasos,

\[
(c_1,c_2)=(1,-1),\qquad(d_1,d_2)=(0,B-1)
\]

producen C₂=B−1 y, por tanto, la misma pareja final. Ambas secuencias son acotadas por B−1; pueden mantener positividad, por ejemplo desde (73,27) en B=10. La memoria adicional ℓ de (9), o la palabra de acarreos firmados, es necesaria para distinguirlas. El teorema de convergencia sigue siendo válido, pero no convierte el residuo en un lector de un dato que éste sólo conserva módulo B.

## 8. Qué fija realmente el primer paso nonádico

La identidad (3) fija c₁=1 para esa transición entre las dos parejas. No fija c₂,c₃,… ni su ley generadora. Si se impusiera el valor 1 en todos los pasos como una hipótesis adicional, entonces

\[
\theta_n=\frac{1-B^{-n}}{B-1},\qquad
\theta=\frac1{B-1}.
\tag{19}
\]

Para B=10, x₀=73,y₀=27, la sucesión comienza

\[
(73,27)\to(729,271)\to(7289,2711)
\to(72889,27111),
\]

y la primera fracción converge a

\[
\frac{73}{100}-\frac1{900}
=\frac{164}{225}=0.728888\ldots.
\]

Esto es una consecuencia de la regla adicional «todos los acarreos valen 1», no la lectura de una historia HMT que se haya demostrado aquí.

Más generalmente, si sólo se fija c₁=1 y los restantes acarreos son canónicos no negativos, el cilindro resultante obliga a

\[
\boxed{\frac{b^3-1}{B^3}\le f\le\frac{b^3}{B^3}.}
\tag{20}
\]

En B=10 es el intervalo [0.728,0.729]. Las fracciones posteriores no pueden superar el valor 0.729 de ese primer paso bajo las hipótesis declaradas. Esta restricción permite contrastar cualquier lectura propuesta sin elegir libremente nuevos acarreos. Si se cambia el signo o el alfabeto, se cambia la familia y debe conservarse su memoria adicional.

Ni la aparición de 729 en (3) ni la familia completa de (15) derivan por sí solas los decimales de α. En esta nota no se obtiene una secuencia de acarreos de un valor esperado ni se identifica la realización límite con otro lector por compartir cifras. La completación autoral y la unidad normalizada quedan conservadas; la regla prospectiva que produzca c_j permanece como parte del dato operatorio de cada aplicación específica.

## 9. Aplicación operativa y límites de alcance

La composición proporciona un procedimiento exacto de refinamiento con memoria:

- Actualización: multiplicar por B y transferir c entre dos coordenadas sin cambiar su suma reescalada.
- Comprobación local: recuperar c por residuo cuando se usa el alfabeto canónico.
- Reconstrucción: conservar la escala/profundidad y deshacer todas las etapas mediante divisiones euclídeas.
- Lectura límite: usar cilindros de diámetro conocido para controlar el error sin borrar las marcas de frontera.
- Reagrupación: combinar segmentos mediante (14), conservando su orden y el transporte de escala de cada contribución.

No se identifica esta conservación lineal de la unidad con la isometría de los lectores de memoria del paper: L_c no conserva en general una norma cuadrática. Para las fracciones de (15), una transferencia δ=c/(BM) produce

\[
(f-\delta)^2+(g+\delta)^2-(f^2+g^2)
=2\delta(g-f)+2\delta^2,
\]

que no es cero en general. Un enlace con un balance de forma o una realización física debe conservar su operador y su métrica propios.

La nota añade una prueba de recuperación, un cociclo explícito y un límite controlado. No administra recibos, no modifica estatutos de otros artefactos y no convierte secuencias enteras arbitrarias en historias enriquecidas producidas por HMT.
