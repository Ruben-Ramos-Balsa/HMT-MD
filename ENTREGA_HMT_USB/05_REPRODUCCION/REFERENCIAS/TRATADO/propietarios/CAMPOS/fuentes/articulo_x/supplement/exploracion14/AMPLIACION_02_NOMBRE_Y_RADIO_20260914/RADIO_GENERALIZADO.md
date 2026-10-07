# Radio exacto de dos memorias: familia algebraica y caso nonádico

Nota aditiva del 14 de septiembre de 2026. Se conservan intactos el paper de 326 páginas, sus fuentes, los desarrollos anteriores y sus recibos. El objetivo es explicar el origen del radio y probar su generalización; no renombrar K ni sustituir la generación HMT por un parámetro ajustado.

## 1. Corte causal, procedencia y resultado

El registro entero es una publicación previa de la cadena APP–TRIT–TPK. La realización lineal y el lector actúan después sobre ese registro. El caso canónico conserva la partición nonádica 8+1 y su denominador 9. La familia de esta nota introduce explícitamente un **parámetro algebraico posterior** a>0 para estudiar el lector; no afirma que cada valor de a proceda del mismo generador HMT ni que a deba determinarse por una magnitud física.

Fuentes efectivamente utilizadas:

- [Registro generado e integralidad](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_k.tex:213>), líneas 213–296 y 322–375: extracción tipada, canales anteriores a K, Hadamard, subred integral y registro canónico.
- [Extractor, carga y memoria de eventos](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_imagen_integral.tex:17>), líneas 17–85, 149–199 y 203–263: imagen entera, inversa, carga, covariancia y acumulación prospectiva.
- [Lector de dos memorias](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/11.tex:7>), líneas 7–44: dominio, lectores 3/4 y origen nonádico de 8+1; 118–183: Gram, inversa de mínimos cuadrados y estabilidad. Las líneas 48–74 proporcionan además una inversa de T₃ específica del caso a=8; no se extrapola esa inversión a a=1.
- [Distancias enteras del caso a=8](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/APORTE_INCIDENCIA.md:33>), §§2–6: cortes, paridad, corrección de errores, umbral 729 e isometría incidencial.
- [Exploración antecedente](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/EXPLORACION.md>), §6.1: algoritmo finito de carga conocida en el caso canónico. El verificador asociado implementa ese caso, no la familia completa de esta nota.

La ampliación paramétrica y sus pruebas se clasifican como **FORMALIZACION_NUEVA en esta exploración**. Los lectores, la reconstrucción, la genealogía de K y el caso a=8 ya desarrollado conservan su procedencia anterior. No se formula una pretensión de prioridad mundial.

El resultado principal es

\[
\boxed{
d_0(a)^2=\frac{4a(a^2+a+1)}{(a+1)^4},\qquad
d_q(a)^2=\frac{8a(a^2+a+1)}{(a+1)^4}
\quad(a>0),}
\tag{1}
\]

donde d₀ es la distancia mínima entre clases enteras módulo la dirección uniforme, y d_q la distancia mínima con carga entera fijada. En particular,

\[
\boxed{r_q(a)=\frac{d_q(a)}2
=\frac{\sqrt{2a(a^2+a+1)}}{(a+1)^2},\qquad
r_q(8)=\frac{4\sqrt{73}}{81}.}
\tag{2}
\]

### Genealogía por resultado y límites del corte

1. APP conserva sus hojas y los residuos/cocientes de las posiciones; no recibe este radio como dato.
2. TRIT conserva régimen, orientación y acarreo de los eventos generadores.
3. TPK proporciona el estado enriquecido, las ventanas ordenadas y la extracción hacia el registro firmado y K, según los propietarios citados.
4. El lector canónico usa 8+1 y 9 por su partición nonádica. El símbolo a parametriza aquí una familia posterior declarada; los coeficientes del Gram y sus radios se deducen de ella, sin usar K objetivo, α ni datos metrológicos.
5. La aplicación conserva la información centrada y distingue el canal de carga. Los errores de lectura no se interpretan como nuevos eventos o historias admisibles.
6. El punto de corte es la publicación entera de doce ventanas, con su realización lineal. No se reconstruye toda la historia enriquecida desde ese corte finito.
7. La salida adicional es una familia de garantías exactas de reconstrucción y un decodificador acotado. Su aplicación posterior restituye los lectores incidenciales y dimensionales ya construidos.
8. La terminología de redes, distancias y decodificación describe esa realización posterior. No introduce unidades físicas, una constante universal o un ajuste a α.
9. Las fuentes anteriores localizan los antecedentes; las pruebas contiguas de §§2–6 justifican la nueva composición. Los controles finitos de §8 se mantienen separados de la demostración general.

## 2. Familia de lectores, conservación y Gram

Sea V=R¹², con norma euclídea, y sea S la permutación (Sx)_i=x_(i+1), con índices módulo 12. Para a>0 y j=3,4 definimos

\[
T_{j,a}=\frac{aI+S^j}{a+1},\qquad
D_{j,a}=\frac{\sqrt a}{a+1}(S^j-I),\qquad
M_a k=(D_{3,a}k,D_{4,a}T_{3,a}k).
\tag{3}
\]

Las dos memorias se archivan por separado: la segunda actúa sobre la compresión producida en la primera etapa. No se identifica este protocolo con la evolución que reinyecta el primer complemento.

**Proposición 1.** Para todo a>0,

\[
T_{j,a}^*T_{j,a}+D_{j,a}^*D_{j,a}=I,
\qquad
G_a:=M_a^*M_a=I-(T_{4,a}T_{3,a})^*(T_{4,a}T_{3,a}).
\tag{4}
\]

**Prueba.** La unitariedad de S da

\[
T_{j,a}^*T_{j,a}
=\frac{(a^2+1)I+a(S^j+S^{-j})}{(a+1)^2},\qquad
D_{j,a}^*D_{j,a}
=\frac{a(2I-S^j-S^{-j})}{(a+1)^2}.
\]

Su suma es I. Aplicando la identidad a las dos etapas se obtiene (4), por cancelación del término intermedio T₃* T₃. ∎

Escribamos

\[
p(a)=a^2+a+1,\qquad A(a)=a(a^2+1),\qquad B(a)=a^2.
\]

La expansión de (4) produce

\[
\boxed{
(a+1)^4G_a=4a p(a)I
-A(a)(S^3+S^4+S^8+S^9)
-B(a)(S+S^5+S^7+S^{11}).}
\tag{5}
\]

En efecto, el término diagonal antes de restar es (a²+1)² y

\[
(a+1)^4-(a^2+1)^2=4a(a^2+a+1).
\]

Los términos simples pesan a(a²+1) y los cruzados a². Por tanto, para h real,

\[
\begin{aligned}
(a+1)^4\|M_a h\|^2={}&
A(a)\sum_i\bigl((h_i-h_{i+3})^2+(h_i-h_{i+4})^2\bigr)\\
&+B(a)\sum_i\bigl((h_i-h_{i+1})^2+(h_i-h_{i+5})^2\bigr).
\end{aligned}
\tag{6}
\]

Cada arista no orientada aparece una sola vez. El grado ponderado es 4A+4B=4ap(a). Los pesos son positivos para todo a>0.

## 3. Núcleo, espectro y una inversa que incluye a=1

Sean \(P=I-\mathbf1\mathbf1^*/12\) y \(P_u=I-P\). Si M_a h=0, la primera memoria implica S³h=h, luego T₃,ₐh=h. La segunda implica S⁴h=h. Como S=S⁴(S³)⁻¹, h es uniforme. Recíprocamente, ambas memorias anulan el modo uniforme. Así,

\[
\ker M_a=\mathbb R\mathbf1\quad(a>0).
\tag{7}
\]

La diagonalización del circulante (5) da la tabla siguiente. Los índices m son los modos duodécimos de S; el uso de caracteres es un cálculo posterior del lector, no un generador de K.

| Modos m | Valor propio de G_a | Multiplicidad |
|---|---:|---:|
| 0 | 0 | 1 |
| 3,9 | \(2a/(a+1)^2\) | 2 |
| 4,8 | \(3a/(a+1)^2\) | 2 |
| 6 | \(4a/(a+1)^2\) | 1 |
| 1,5,7,11 | \(a(5a^2+4a+5)/(a+1)^4\) | 4 |
| 2,10 | \(a(7a^2+2a+7)/(a+1)^4\) | 2 |

**Verificación analítica.** En el modo m, sustituir en (4)

\[
\lambda_m(G_a)=1-
\frac{[a^2+1+2a\cos(\pi m/2)]
[a^2+1+2a\cos(2\pi m/3)]}{(a+1)^4}.
\]

Los doce valores de esos dos cosenos producen exactamente la tabla. Respecto de 2a/(a+1)², la diferencia del penúltimo valor es

\[
\frac{3a(a^2+1)}{(a+1)^4}>0,
\]

y la del último es

\[
\frac{a(5a^2-2a+5)}{(a+1)^4}>0.
\]

Los otros valores no nulos son múltiplos estrictamente mayores. Se concluye

\[
\lambda_{\min}(G_a|_{\mathbf1^\perp})
=\frac{2a}{(a+1)^2},\qquad
L_a=(G_a+P_u)^{-1}M_a^*,\qquad
L_aM_a=P,\qquad
\|L_a\|=\frac{a+1}{\sqrt{2a}}.
\tag{8}
\]

G_a+P_u es invertible: vale 1 sobre la dirección uniforme y tiene el espectro positivo anterior en su complemento. Esta fórmula, a diferencia de un procedimiento basado en T₃,ₐ⁻¹, sigue siendo válida en **a=1**, donde T₃,₁=(I+S³)/2 es singular. La pérdida de invertibilidad de una compresión individual no supone pérdida de la reconstrucción mediante sus dos memorias.

## 4. Distancias enteras: pruebas válidas para todo a>0

Se consideran los dominios algebraicos

\[
\mathcal C_0(a)=M_a\mathbb Z^{12},\qquad
\Lambda_q=\{k\in\mathbb Z^{12}:\mathbf1^*k=q\},\qquad
\mathcal C_q(a)=M_a\Lambda_q,\quad q\in\mathbb Z.
\tag{9}
\]

La primera imagen se identifica con la red PZ¹² mediante M_a. Estos conjuntos contienen las publicaciones enteras a las que se aplica el lector; no se afirma que todos sus candidatos sean historias HMT generadas.

### Teorema 2. Distancia sin carga

Para todo a>0,

\[
\min_{h\in\mathbb Z^{12}\setminus\mathbb Z\mathbf1}
\|M_a h\|^2=\frac{4a p(a)}{(a+1)^4}.
\tag{10}
\]

**Prueba.** Usamos los cortes del grafo (6). Para cualquier subconjunto propio no vacío de las doce posiciones, cada uno de los pasos 1 y 5, que forma un ciclo conexo de longitud doce, aporta al menos dos aristas de corte. Por tanto hay al menos cuatro aristas de peso B.

Para los pasos 3 y 4:

- Si el conjunto no es invariante por ninguno de esos dos pasos, cada familia aporta al menos dos aristas: hay al menos cuatro de peso A.
- Si es invariante por el paso 3, es unión de clases módulo 3. Cada uno de los cuatro triángulos del paso 4 cruza el conjunto dos veces: hay ocho aristas de peso A.
- Si es invariante por el paso 4, es unión de clases módulo 4. Cada uno de los tres ciclos de longitud cuatro del paso 3 cruza al menos dos veces: hay al menos seis aristas de peso A.

La invariancia simultánea obligaría a invariancia por S y no corresponde a un subconjunto propio no vacío. Todo corte no trivial pesa, por ello, al menos 4A+4B=4ap(a); el corte de una posición alcanza la igualdad.

Para un h entero no constante se usa (h_i−h_j)²≥|h_i−h_j| y la descomposición de las diferencias absolutas en los cortes de nivel {i:h_i>t}. Hay al menos un nivel no trivial. El miembro derecho de (6) es al menos 4ap(a); h=e_i lo alcanza. Esto prueba (10) para todos los enteros y todos los a>0, no sólo para una muestra finita. ∎

### Teorema 3. Distancia con carga y clasificación de los minimizadores

Para todo a>0 y q entero,

\[
\min_{k\ne k'\in\Lambda_q}\|M_a(k-k')\|^2
=\frac{8a p(a)}{(a+1)^4}.
\tag{11}
\]

Las diferencias que alcanzan el mínimo son exactamente h=e_i−e_j con j−i≡2,6,10 módulo 12. **El dominio paramétrico de esta clasificación es toda la semirrecta a>0.**

**Prueba.** Si h es entero, no nulo y de suma cero, su norma cuadrada es un entero par: Σh_i²≡Σh_i≡0 módulo 2. Si ||h||²≥4, (8) implica

\[
\|M_a h\|^2\ge\frac{8a}{(a+1)^2}
>\frac{8a p(a)}{(a+1)^4},
\tag{12}
\]

porque (a+1)²−p(a)=a>0. Sólo quedan los vectores de norma cuadrada 2, que son e_i−e_j. Su energía es 2[(G_a)_{ii}−(G_a)_{ij}]. Según (5), las entradas fuera de la diagonal son:

- cero en separaciones 2,6,10;
- −B/(a+1)⁴ en separaciones 1,5,7,11;
- −A/(a+1)⁴ en separaciones 3,4,8,9.

Como A,B>0, las primeras dan exactamente el mínimo 8ap(a)/(a+1)⁴ y las otras dan valores mayores. Toda diferencia e_i−e_j puede realizarse dentro de cada clase de carga q. ∎

## 5. Radios óptimos y origen exacto del factor 73

Si y=M_a k+e, se mide ε=||e|| en V⊕V con la normalización de (3). Las imágenes (9) son discretas porque PZ¹²⊂(1/12)Z¹² es discreta y (8) acota M_a inferiormente sobre el complemento uniforme. Sus puntos más cercanos existen.

La desigualdad triangular demuestra que una palabra a distancia mínima d de las demás es el único vecino más cercano cuando ε<d/2. Por (10)–(11),

\[
\boxed{
r_0(a)=\frac{\sqrt{a p(a)}}{(a+1)^2},\qquad
r_q(a)=\frac{\sqrt{2a p(a)}}{(a+1)^2}
=\sqrt2\,r_0(a).}
\tag{13}
\]

Bajo ε<r₀ se recupera Pk; bajo ε<r_q y con q exacto se recupera k completo. Los radios son óptimos como garantías uniformes adversariales en los dominios algebraicos declarados: el punto medio entre dos palabras mínimas está a d/2 de ambas. No se concluye optimalidad sobre un subconjunto adicional de historias admisibles.

En el caso canónico,

\[
\begin{aligned}
a&=8,& a+1&=9,& p(8)&=8^2+8+1=73,\\
4ap(a)&=4\cdot8\cdot73=2336,&
8ap(a)&=8\cdot8\cdot73=4672.
\end{aligned}
\]

El radio con carga es la mitad de la raíz cuadrada de la distancia mínima:

\[
r_q(8)=\frac12\sqrt{\frac{4672}{9^4}}
=\frac{\sqrt{64\cdot73}}{2\cdot81}
=\boxed{\frac{4\sqrt{73}}{81}}.
\tag{14}
\]

Así, **73 es el valor exacto del polinomio a²+a+1 en a=8**. Aparece al restar los términos diagonales de las dos compresiones y calcular la separación de los registros enteros. No es el reemplazo, el truncamiento ni el redondeo de un número vinculado a α. La identidad algebraica p(a)=Φ₃(a)=(a³−1)/(a−1), para a≠1, y p(1)=3 es exacta; la prueba del radio no necesita asignarle una interpretación física adicional.

No hay una entrada α en (3)–(14). Una relación adicional entre este factor y un lector HMT de α debe mantener sus flechas y sus tipos propios; sustituir 73 por una aproximación numérica destruiría las igualdades exactas de esta nota.

## 6. Decodificación finita y aplicaciones computacionales delimitadas

### 6.1. Carga conocida: hasta 4096 candidatos

Para q exacto y y=M_a k+e, se calcula

\[
\widetilde k=\frac q{12}\mathbf1+L_a y.
\]

Bajo ε<r_q(a), (8) y (13) dan

\[
\|\widetilde k-k\|
<\|L_a\|r_q(a)
=\frac{\sqrt{a^2+a+1}}{a+1}<1.
\tag{15}
\]

Por ello cada entero k_i pertenece al par suelo/techo de la correspondiente coordenada de k tilde; si ésta es entera, el par tiene un solo elemento. El algoritmo consiste en:

1. Enumerar los productos de esos doce pares: como máximo 2¹²=4096 candidatos.
2. Conservar los candidatos h de suma q.
3. Elegir el que minimiza ||M_a h−y||².

El candidato verdadero está incluido, y la separación (11) garantiza que es el ganador único. No se recibe el registro objetivo ni una tabla de historias. Fuera del radio declarado, esta búsqueda local no se presenta como un decodificador universal.

Si se dispone de una carga observada q_obs con |q_obs−q|<1/2, el redondeo al entero más cercano restituye primero q. Se mantiene separado este canal y su condición de error.

### 6.2. Sin carga: doce residuos, hasta 49152 candidatos

La recuperación centrada también admite una búsqueda finita explícita. Cada clase de Z¹²/Z·1 tiene un representante entero único cuya suma ρ pertenece a {0,…,11}: para un k de carga q, escribir q=12t+ρ y tomar h=k−t1. Su memoria es la misma que la de k.

Para cada ρ=0,…,11 se forma

\[
\widetilde h_\rho=L_a y+\frac\rho{12}\mathbf1.
\]

En la clase residual verdadera, bajo ε<r₀(a),

\[
\|\widetilde h_\rho-h\|
<\frac{\sqrt{a^2+a+1}}{\sqrt2\,(a+1)}<1.
\tag{16}
\]

Se enumeran los pares suelo/techo para cada ρ, se exige suma ρ y se minimiza el residuo de memoria entre todos los candidatos. Hay a lo sumo 12·2¹²=49152 candidatos antes del filtro. Representantes de dos residuos distintos no pueden diferir en una traslación uniforme entera, por lo que no duplican la misma clase. La separación (10) garantiza la clase única correcta y se devuelve Ph=Pk. No se deduce de ello la carga perdida.

### 6.3. Aritmética exacta, a=1 y normalización

Para a racional positivo conviene almacenar

\[
R_a=M_a/\sqrt a,\qquad z=y/\sqrt a.
\]

Los coeficientes de R_a son racionales. Si los datos observados z son racionales, la inversa

\[
(R_a^*R_a+P_u)^{-1}R_a^*z
\]

es exactamente L_a y; los candidatos y sus residuos cuadrados pueden calcularse mediante fracciones, sin comparar aproximaciones de raíces cuadradas. La cota de ruido se traduce a

\[
\|\delta z\|<\frac{r_q(a)}{\sqrt a}
=\frac{\sqrt{2p(a)}}{(a+1)^2}
\]

y análogamente para r₀. Se puede comprobar por cuadrados cuando el error es conocido en un ensayo. La inversión del Gram sigue disponible en a=1, aunque T₃ sea singular. Para a real arbitrario las pruebas mantienen su sentido exacto, pero una implementación numérica debe controlar también los errores de representación de a y de sus operadores; no quedan incluidos automáticamente en un modelo que sólo perturba y.

La aplicación computacional concreta es una corrección de errores en un registro estructurado de dimensión fija, seguida de lectura exacta de incidencias o proyectores. No se ha probado una complejidad favorable cuando aumenta el número de ventanas: 4096 y 49152 son cotas finitas para doce coordenadas, no un algoritmo polinómico general de vecino más cercano.

## 7. Dualidad del parámetro y comparación de lectores

Las tres funciones normalizadas que aparecen en (5) son invariantes bajo a↦1/a. Por tanto,

\[
G_{1/a}=G_a,\qquad
r_0(1/a)=r_0(a),\qquad r_q(1/a)=r_q(a),\qquad
\|L_{1/a}\|=\|L_a\|.
\tag{17}
\]

Es una igualdad de Gram, métricas y radios. No identifica por ello Mₐ con M₁/ₐ. De hecho, Dⱼ,₁/ₐ=Dⱼ,ₐ, mientras Tⱼ,₁/ₐ=SʲTⱼ,ₐ*; la segunda memoria puede ser distinta. Si se intercambia el parámetro, el decodificador debe usar el lector correspondiente.

Sea t=a/(a+1)². Para a>0, 0<t≤1/4 y la igualdad se alcanza sólo en a=1. Como

\[
r_q(a)^2=2t(1-t),\qquad r_0(a)^2=t(1-t),
\]

y estas funciones son crecientes en ese intervalo,

\[
\boxed{r_q(a)\le\frac{\sqrt6}{4},\qquad
r_0(a)\le\frac{\sqrt3}{4},}
\tag{18}
\]

con igualdad sólo en a=1. El caso a=8 tiene el mismo Gram y radio que a=1/8. Los radios tienden a cero cuando a tiende a cero o a infinito; los extremos no se añaden al dominio del teorema.

Esta comparación sirve para diseñar un **lector posterior distinto** cuando tal elección forme parte del problema computacional. No convierte a=1 en el parámetro generado por la partición nonádica: el canon sigue siendo a=8. Además, (18) compara la norma de las memorias Mₐ tal como fue fijada en (3). Reescalar los datos a Rₐ cambia la unidad de error; no permite anunciar una ganancia sin conservar esa normalización.

## 8. Restitución estructural, falsadores y controles

Bajo el radio sin carga, se recupera exactamente Pk; por composición se recuperan u_k=P₃Pk, su dirección y P₁₀=P−u_ku_k*/||u_k||² cuando u_k≠0. También se recupera η_k=||P₃Pk||²/||Pk||² cuando Pk≠0. Se mantienen las condiciones y el proyector P₃ del propietario; no se infieren dimensiones físicas por contar coordenadas.

Bajo el radio con carga, se recupera k completo. Por tanto se conserva el selector {i:k_i≥729}, incluso para el registro canónico con k₄=729 exactamente sobre el umbral. Los restantes datos marcados deben conservarse o transportarse según sus leyes para restituir la misma bandera excepcional. Las isometrías de la pantalla incidencial conservan distancias y radios al transportar simultáneamente lector, imagen y métrica, como en el antecedente.

El testigo k'=k−e₄+e₆ mantiene carga y tiene separación cíclica 2. Por el teorema 3 alcanza d_q(a) para **todo a>0**; en el registro canónico cambia la selección al disminuir 729 a 728. El punto medio de sus memorias prueba la frontera del radio. No se atribuye al candidato k' una historia generadora HMT.

Falsadores y exclusiones precisos:

- En ε=r_q(a), el punto medio anterior ya es ambiguo: la desigualdad debe ser estricta.
- Sin carga, Mₐ(k+1)=Mₐk; no se puede recuperar un selector absoluto que cambie bajo ese desplazamiento.
- En a=1 no puede usarse una fórmula que requiera T₃,₁⁻¹; sí puede usarse (8).
- Al cambiar a hay que cambiar el lector en la reconstrucción; igualdad de Gram no significa igualdad de las memorias.
- No se puede conservar un radio de Mₐ después de dividir las memorias por √a sin reescalarlo.
- Perturbar a, S o las marcas geométricas no es el mismo modelo que añadir ruido e a las memorias de un lector fijo.
- Los dominios enteros de búsqueda no generan retrospectivamente historias ni fijan α o unidades físicas.

Como control separado se calcularon, mediante Python estándar en modo -I -S y fracciones exactas, los casos racionales a=1/100, 1/8, 1/2, 1, 2, 8 y 100. Se verificaron 1008 entradas de Gram, 84 modos espectrales, 28658 cortes no triviales, 924 raíces orientadas y 21 desigualdades/identidades paramétricas auxiliares. Todos los casos reprodujeron (5), (8), (10) y (11); las raíces mínimas tuvieron siempre separaciones 2,6,10. No se creó ni modificó un verificador anterior. Estos controles no sustituyen las pruebas analíticas para todos los a>0 y todos los vectores enteros.

La nota es una ampliación de investigación para revisión e integración por el editor principal. No actualiza el paper, sus fuentes, los registros globales o los recibos sellados previos.
