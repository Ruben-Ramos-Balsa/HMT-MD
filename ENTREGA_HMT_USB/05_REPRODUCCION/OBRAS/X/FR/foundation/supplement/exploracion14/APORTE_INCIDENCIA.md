# Memoria entera, decodificación exacta y estabilidad de la incidencia

Desarrollo focal del 14 de septiembre de 2026. Se mantienen intactos el PDF de 326 páginas, sus fuentes y las notas previas. No se propone cambiar el eje conservación/memoria ni decidir una denominación nueva para K.

## 1. Resultado y base material

El lector de dos memorias ya construido induce una red discreta de salidas. Su distancia mínima puede calcularse exactamente, sin recibir el registro objetivo. De aquí resulta una franja de error dentro de la cual se recuperan **exactamente**, no sólo aproximadamente, el registro centrado y su proyector dimensional. Si se conserva además la carga entera, se recupera K íntegro y su selección incidencial, incluso cuando una componente está exactamente sobre el umbral 729.

Fuentes utilizadas, con localizadores del manuscrito conservado:

- **R1 — Genealogía e integralidad.** [registro_k.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_k.tex:213>), líneas 213–296: extracción tipada y canales anteriores a K; 322–375: Hadamard, subred integral, inversión y registro canónico.
- **R2 — Imagen, carga y eventos.** [registro_imagen_integral.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_imagen_integral.tex:17>), líneas 17–85: extractor e inversa; 149–199: dominios, covariancia y límites de la sola compatibilidad; 203–263: acumulación prospectiva y concatenación.
- **R3 — Lector de memoria.** [nuclear/11.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/11.tex:7>), líneas 7–44: M; 48–183: inversa, Gram, espectro y norma 9/4; 187–225: aplicación al registro publicado; 234–387: proyector dimensional y descriptor escalar.
- **R4 — Selección incidencial.** [excepcional.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/excepcional.tex:236>), líneas 236–260: lectura de bloque alto y umbral; 278–329: bandera, unicidad y origen marcado.
- **R5 — Dirección y marco.** [k_direccion_dimensional.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/k_direccion_dimensional.tex:12>), líneas 12–99: carta de A5/C5, proyector y no nulidad; 101–161: reducción y covariancia.
- **R6 — Pantalla isométrica.** [nuclear/05.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/05.tex:3>), líneas 3–58: isometría completa F, imagen, inversa y levantamiento covariante.
- **N1 — Antecedente de la composición.** [Reconstrucción dimensional desde memoria](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/RECONSTRUCCION_DIMENSIONAL_DESDE_MEMORIA_Y_LEY_EXTERIOR_20260912.md:17>), §§2–3, líneas 17–217: lectura, reconstrucción, ruido y proyector; [continuación excepcional](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/EXCEPCIONAL_CONTINUACION_20260912.md:22>), §§2–3: transporte isométrico hacia incidencia.

R1–R6 son antecedentes, no resultados redescubiertos aquí. La nueva composición es la separación discreta de la imagen de M y su uso para corregir errores de lectura antes de aplicar los selectores. En la búsqueda focal de los archivos anteriores y las notas del expediente no se localizó este teorema de distancia mínima. Se clasifica como **FORMALIZACION_NUEVA / consecuencia adicional en este expediente**, sin afirmación de prioridad mundial.

### 1.1. Genealogía y corte de la aplicación

1. APP aporta las dos hojas sobre las mismas posiciones, con residuos y cocientes, no valores objetivo externos.
2. TRIT conserva régimen, orientación y acarreo de los eventos.
3. TPK compone selección, transporte y actualización; el registro de doce ventanas conserva los eventos y sus marcas. R1 fija la extracción hacia los canales y el estado firmado antes de K.
4. La inversión H/4 procede de H²=4I y actúa sobre la subred integral; los coeficientes 8, 1 y 9 del lector posterior proceden de la partición nonádica. Las constantes de separación calculadas abajo proceden de ese mismo lector, no del vector canónico.
5. Se conservan carga, orden de ventanas y datos de orientación/incidencia requeridos. Una perturbación de lectura no se declara evento, ruta ni historia admisible.
6. El estado enriquecido y la construcción conjunta del continuo son el antecedente común. El corte de este resultado es su publicación entera dodecafásica y su realización lineal; no se pretende reconstruir toda la historia desde doce coordenadas.
7. La salida nueva es un decodificador de memorias y sus radios exactos, seguido de los lectores incidenciales y dimensionales ya construidos.
8. La terminología de red discreta, distancia mínima y corrección de errores describe esa realización posterior. No se introduce aquí una unidad física ni una interpretación experimental de la norma de ruido.
9. R1–R6 localizan las flechas usadas. El teorema siguiente proporciona las pruebas nuevas; los controles finitos del §8 son comprobaciones separadas.

## 2. El lector conservado y su Gram explícito

Sea V=R¹² la realización del registro, con producto euclídeo, y sea (Sx)_i=x_(i+1), con índices módulo 12. Para j=3,4 se conservan las definiciones de R3:

\[
T_j=\frac{8I+S^j}{9},\qquad D_j=\frac{\sqrt8}{9}(S^j-I),
\qquad Mk=(D_3k,D_4T_3k)\in V\oplus V.
\tag{1}
\]

El segundo complemento se registra después de la primera compresión; no se reinyecta el primero en este protocolo. Sean \(P=I-\mathbf1\mathbf1^*/12\), \(G=M^*M\) y L la inversa de mínimos cuadrados de R3. Se tienen

\[
\ker M=\mathbb R\mathbf1,\qquad LM=P,\qquad
G|_{\mathbf1^\perp}\ge\frac{16}{81}I.
\tag{2}
\]

La expansión del Gram da la forma útil para esta continuación:

\[
\boxed{6561G=2336I
-520(S^3+S^4+S^8+S^9)
-64(S+S^5+S^7+S^{11}).}
\tag{3}
\]

**Demostración.** Por el balance de R3,

\[
G=I-(T_4T_3)^*(T_4T_3),\qquad
T_j^*T_j=\frac{65I+8(S^j+S^{-j})}{81}.
\]

Todos estos operadores son polinomios de S y conmutan. El producto produce 65²I, los cuatro términos de coeficiente 65·8=520 y los cuatro términos cruzados de coeficiente 8²=64. Como 81²−65²=2336, resulta (3). No se ha utilizado K. ∎

Equivalentemente, para h real,

\[
6561\|Mh\|^2=
520\sum_i\bigl((h_i-h_{i+3})^2+(h_i-h_{i+4})^2\bigr)
+64\sum_i\bigl((h_i-h_{i+1})^2+(h_i-h_{i+5})^2\bigr).
\tag{4}
\]

Cada suma corresponde a aristas no orientadas contadas una vez. La diagonal 2336 es el grado ponderado 4·520+4·64.

## 3. Dos distancias mínimas exactas

El dominio de decodificación sin carga es Z¹²/Z·1, o equivalentemente la red proyectada Λ=PZ¹² en 1⊥. Su imagen es C₀=MZ¹². Con carga entera q se usa

\[
\Lambda_q=\{k\in\mathbb Z^{12}:\mathbf1^*k=q\},\qquad
\mathcal C_q=M\Lambda_q.
\tag{5}
\]

Estos dominios algebraicos contienen las publicaciones enteras a las que se aplica el lector. No se afirma que todo elemento suyo sea la publicación de una historia HMT; no son un nuevo generador de historias.

### Teorema 1 — Separación sin carga

\[
\boxed{\min_{h\in\mathbb Z^{12}\setminus\mathbb Z\mathbf1}
\|Mh\|^2=\frac{2336}{6561}.}
\tag{6}
\]

**Demostración.** En el grafo de (4), llamemos pesadas a las aristas de pasos 3 y 4 y ligeras a las de pasos 1 y 5. Para todo subconjunto propio no vacío A de las doce posiciones:

- Cada uno de los pasos 1 y 5 forma un ciclo conexo de longitud doce. Cada ciclo cruza A al menos dos veces; hay al menos cuatro aristas ligeras en el corte.
- Si A no es invariante por S³ ni por S⁴, cada una de esas dos familias tiene al menos dos aristas de corte, luego hay al menos cuatro pesadas.
- Si A es invariante por S³, es unión de sus órbitas, que son las tres clases módulo 3. Como A es propio no vacío, cada uno de los cuatro triángulos de S⁴ corta A dos veces: hay ocho aristas pesadas.
- Si A es invariante por S⁴, es unión de clases módulo 4. Cada uno de los tres ciclos de longitud cuatro de S³ contiene dentro y fuera de A, luego hay al menos seis aristas pesadas. La invariancia por ambos pasos obligaría a invariancia por S y no es posible para A propio no vacío.

Todo corte no trivial pesa, por tanto, al menos 4·520+4·64=2336. Para h entero no constante, usar (h_i−h_j)²≥|h_i−h_j| y descomponer |h_i−h_j| en los cortes de los conjuntos de nivel A_t={i:h_i>t}. Hay al menos un nivel no trivial. La suma ponderada de cuadrados es al menos 2336. Para h=e_i, el valor es precisamente 2336, por ser el corte de un punto. Dividiendo por 6561 se obtiene (6). ∎

### Teorema 2 — Separación con carga

Para cualquier q entero,

\[
\boxed{\min_{k\ne k'\in\Lambda_q}\|Mk-Mk'\|^2
=\frac{4672}{6561}.}
\tag{7}
\]

**Demostración.** La diferencia h=k−k' es entera, no nula y de suma cero. Su norma cuadrada es un entero par, pues h_i²≡h_i módulo 2. Si ||h||²≥4, (2) da

\[
\|Mh\|^2\ge\frac{64}{81}=
\frac{5184}{6561}>\frac{4672}{6561}.
\]

Sólo queda ||h||²=2, es decir h=e_i−e_j. Por (3), su energía es 2(G_ii−G_ij). Los términos fuera de la diagonal son cero para j−i=2,6,10; −64/6561 para 1,5,7,11; y −520/6561 para 3,4,8,9. El mínimo es 2·2336/6561 y se alcanza exactamente entre las raíces con separaciones 2,6,10. Tales diferencias pertenecen a toda clase de carga. ∎

## 4. Decodificación prospectiva y radios de corrección

Se observa y=MK+e, con ε=||e|| en la norma conjunta de las dos memorias de (1). Se fija el lector M antes de observar K o y.

Sin carga, se selecciona el punto de C₀ más cercano a y y se devuelve su única preimagen centrada. Con carga q, se selecciona el punto de C_q más cercano y se devuelve su única preimagen de carga q. Las imágenes son discretas: Λ⊂(1/12)Z¹² es discreta y M está acotado inferiormente sobre 1⊥ por (2). Hay, por tanto, mínimos de distancia y sólo un número finito de candidatos dentro de cualquier radio acotado. En C₀ se identifican desde el principio k y k+t1; no se intenta decidir entre preimágenes uniformemente desplazadas.

Este decodificador utiliza la integralidad, la carga cuando se suministra y el lector M; no recibe el vector terminal como tabla objetivo. No presupone una lista de historias admisibles ni sustituye su generación.

### Teorema 3 — Corrección exacta

1. Si

   \[
   \boxed{\varepsilon<r_0:=\frac{2\sqrt{146}}{81}
   \approx0{,}298346814162829,}
   \tag{8}
   \]

   la decodificación sin carga recupera exactamente PK.

2. Si q=ΣK_i se conoce exactamente y

   \[
   \boxed{\varepsilon<r_q:=\frac{4\sqrt{73}}{81}
   \approx0{,}421926110879878,}
   \tag{9}
   \]

   la decodificación con carga recupera exactamente K.

3. Si sólo se observa una carga real q_obs con |q_obs−q|<1/2, su redondeo al entero más cercano recupera primero q; entonces se aplica el punto 2. Este canal de carga es distinto de las memorias.

**Demostración.** Para un punto de código incorrecto c', la desigualdad triangular da ||y−c'||≥d−ε>ε=||y−MK|| cuando ε<d/2. Los teoremas 1 y 2 dan respectivamente d=√2336/81 y d=√4672/81. La preimagen es única en el dominio de cada decodificador. El último punto usa la separación unitaria entre enteros. ∎

Los radios son óptimos como garantías uniformes contra ruido adversarial en **estos dominios algebraicos**: el punto medio de dos palabras a distancia mínima está a d/2 de ambas. Ningún decodificador puede decidir siempre correctamente a cuál pertenecía la entrada a partir de ese mismo dato. Esto no afirma optimalidad sobre un subconjunto desconocido de publicaciones físicamente admisibles; restringir el dominio puede aumentar la separación.

Las memorias racionales almacenadas en N1 son z=m/√8. Si el error se mide en z, los radios correspondientes son r₀/√8=√73/81 y r_q/√8=√146/81. No deben aplicarse los números de (8)–(9) sin conservar esta normalización.

### Consecuencia dimensional sin carga ni terminal

R5 fija P₃ y R3 demuestra u_K=P₃PK, P₁₀(K)=P−u_Ku_K*/||u_K||². Si P₃PK≠0, bajo (8) el registro centrado decodificado determina **exactamente** u_K, su recta y la matriz completa P₁₀(K). Para PK≠0 recupera también η_K=||P₃PK||²/||PK||². No se utiliza la carga ni T₄T₃K.

La diferencia respecto de la cota continua de R3 es precisa: allí el error del proyector se controla por 9ε/(4||u_K||); aquí la decodificación entera devuelve primero PK sin error, dentro de un radio uniforme. La composición no requiere dividir por una aproximación a u_K. Si u_K=0, no se define el proyector de rango diez mediante esa fórmula: el teorema de corrección no borra esa condición.

## 5. El umbral 729: margen continuo nulo y restitución discreta

En la carta de R4,

\[
K=(234,543,140,729,659,824,621,58,914,794,146,601),
\qquad B_K=\{i:K_i\ge729\}=\{4,6,9,10\}.
\tag{10}
\]

Se usan aquí posiciones 1–12, como en la fuente.

### Proposición 4 — El selector continuo directo no tiene radio positivo

Considérese la reconstrucción lineal sin cuantización, con q exacto. Para t>0 sea

\[
e_t=-tM(Pe_4),\qquad
\widetilde K_t=\frac q{12}\mathbf1+L(MK+e_t)
=K-tPe_4.
\tag{11}
\]

Entonces ||e_t||→0, pero la cuarta coordenada vale 729−11t/12<729. Para t positivo suficientemente pequeño, sólo cambia la pertenencia de esa posición a B. Por tanto no existe un radio euclídeo positivo de estabilidad del selector directo alrededor de MK, aun conservando q. Estos datos perturbados son errores de lectura en su realización lineal, no nuevas historias HMT.

### Corolario 5 — La integralidad restituye exactamente la selección

Aplicando antes el decodificador de carga de (9), cualquier error menor que r_q devuelve K exacto y, después, B_K exacto con el **mismo umbral 729**. No se desplaza el umbral para adaptarlo al vector observado.

Si los demás datos marcados P_π, H_e, H_φ y H_APP de R4 se conservan exactos —o se transportan simultáneamente mediante su ley—, la unicidad allí demostrada devuelve también la misma bandera B_K⊂H⁻_α y el mismo origen marcado o_*. La corrección de K no presume corregir automáticamente errores independientes en esos otros datos.

La frontera del radio con carga posee un testigo concreto que cambia la incidencia:

\[
K'=K-e_4+e_6,
\qquad Q(K')=Q(K)=6263,\qquad
B_{K'}=\{6,9,10\}.
\tag{12}
\]

Ambos vectores están en {0,…,999}¹² y ||MK'−MK||²=4672/6561. Su punto medio de memorias está exactamente a r_q de cada uno. El testigo demuestra el límite de la garantía uniforme en Λ_q; no atribuye a K' una genealogía terminal HMT.

Sin carga, M(K−1)=MK y B_(K−1)≠B_K. Por ello las dos memorias solas pueden recuperar el proyector dimensional, que ignora la media, pero no este selector absoluto de bloques. No es una contradicción: los dos lectores conservan información diferente.

## 6. Transporte a incidencia y covariancia

R6 construye la isometría sobreyectiva

\[
F:V\to Y=\mathbb R\oplus E_{\rm inc},\qquad
Fk=(\mu(k),\mathcal I Pk/6),
\qquad \|Fk\|_Y=\|k\|,
\tag{13}
\]

con producto \(12\mu\nu+\langle y,z\rangle\) y \(E_{\rm inc}=\mathcal I(\mathbf1^\perp)\), no todo R¹³². La lectura incidencial de las dos memorias es

\[
M_{\rm inc}=(F\oplus F)M.
\tag{14}
\]

**Corolario 6.** Las dos distancias mínimas y los radios (8)–(9) son idénticos para M_inc en Y⊕Y. Los decodificadores conjugados recuperan los mismos registros, selecciones y proyectores.

**Demostración.** F⊕F conserva exactamente todas las distancias entre palabras de código y las normas de ruido. Su inversa convierte el problema de vecino más cercano en el ya probado. ∎

Para una permutación R de las posiciones, se transportan S'=RSR⁻¹, K'=RK y M'=(R⊕R)MR⁻¹. Entonces M'R=(R⊕R)M. La red entera, la carga y las distancias se conservan; en el régimen de unicidad, el decodificador transforma su salida por R, y los proyectores por conjugación, transportando P₃ como en R5. Fuera de ese régimen, se transporta el conjunto de minimizadores, sin imponer una elección arbitraria entre empates. No se exige [R,S]=0. Bajo un cambio ortogonal general hay que transportar también la red RZ¹² y la dirección uniforme R1: redondear respecto de Z¹² en una carta arbitraria no es covariante. La isometría hacia incidencia no añade una acción del Monstruo sobre K.

## 7. Refinamiento, función generalizable y alcance

Los radios se han calculado para el lector fijo de doce posiciones, sobre todos los registros enteros de su realización, no ajustándolos a (10). Por ello se aplican a cualquier publicación HMT entera dentro de ese tipo cuando se usa este mismo protocolo. Para un prefijo fijado, R2 conserva su evaluación bajo prolongaciones y particiones compatibles: el decodificador recupera esa misma publicación si el error de lectura satisface el radio. Si nuevos eventos cambian K, se corrige el registro nuevo a partir de sus memorias nuevas; no se afirma constancia temporal de K.

La consecuencia funcional es una **protección discreta de la información estructural**: la separación de las memorias permite restituir relaciones de incidencia y una dirección dimensional, pese a errores de lectura inferiores a un umbral demostrado. Es una propiedad del sistema generación entera → lector de memoria → decodificador → incidencia/dirección. No reduce K a doce parámetros sin relaciones ni cambia la dimensión algebraica por una afirmación sobre dimensiones físicas.

El resultado es finito y uniforme en el registro para este lector. No requiere un límite analítico adicional. No se extrapola a un número distinto de ventanas, a otro operador de memoria, a otra métrica de ruido o a una dinámica física no especificada.

## 8. Controles realizados, falsadores y estado documental

Se efectuaron controles de sólo lectura con Python estándar en modo -I -S y aritmética Fraction. No se crearon ni modificaron scripts previos. Los controles calcularon la primera fila de G, verificaron los 4094 subconjuntos propios no vacíos y las 132 raíces orientadas e_i−e_j. Resultados:

- Primera fila de 6561G: (2336,−64,0,−520,−520,−64,0,−64,−520,−520,0,−64).
- Mínimos de cortes pesado, ligero y ponderado: 4, 4 y 2336.
- Mínimo sobre raíces de carga cero: 4672/6561, en separaciones 2,6,10.
- El testigo (12) conserva la carga, cambia B y alcanza esa distancia.
- La exclusión espectral de ||h||²≥4 da 64/81>4672/6561.

Estos cálculos corroboran las pruebas; la cobertura de todos los vectores enteros procede del argumento por niveles del teorema 1 y del argumento espectral/paritario del teorema 2, no de una enumeración de 4094 casos.

Falsadores de la composición:

1. Aplicar directamente el umbral a la reconstrucción real: (11) produce errores arbitrariamente pequeños que alteran B.
2. Suprimir q y anunciar recuperación del selector absoluto: K y K−1 tienen memorias iguales y distintos soportes altos.
3. Usar radios no estrictos: los puntos medios entre palabras mínimas son ambiguos.
4. Cambiar el lector o normalizar m a z sin reescalar el error: cambia la métrica en la que se formularon los radios.
5. Cuantizar en Z¹² después de un marco ortogonal general sin transportar la red: se cambia el objeto decodificado.
6. Confundir el dominio algebraico de candidatos con historias admisibles, o atribuir al testigo K' una procedencia no construida.
7. Recuperar P₁₀ sin la condición P₃PK≠0, o extender la corrección de K a perturbaciones independientes del diseño y sus marcas.

Se han aplicado las habilidades de continuidad, núcleo formal y construcción desde primeros principios para conservar las fuentes y componer el lector existente; no se ha reiniciado el corpus ni alterado su causalidad. Los controles de arranque no se presentan como pruebas de este desarrollo. El resolutor global consultado sigue identificando el testigo histórico de 2084 páginas; la selección material de esta exploración es el paper de 326 páginas expresamente autorizado, con el integral2249 y la serie como sus antecedentes, sin modificar punteros globales.

Este archivo es una aportación de investigación con prueba focal para revisión del editor principal, no una integración en el paper ni una actualización de registros globales, recibos de publicación o estatutos físicos. Las fuentes, el PDF y las notas anteriores permanecen intactos.
