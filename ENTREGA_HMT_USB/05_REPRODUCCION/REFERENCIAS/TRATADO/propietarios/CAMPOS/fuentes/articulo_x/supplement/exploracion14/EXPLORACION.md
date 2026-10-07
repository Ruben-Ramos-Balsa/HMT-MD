# Función aritmética, incidencia y capacidad de reconstrucción del registro generado

Fecha: 14 de septiembre de 2026. Desarrollo para ponderación e integración posterior
en *Conservación estructural y dinámica de la memoria*. El PDF de 326 páginas y sus
fuentes permanecen intactos. La denominación científica del objeto queda abierta.

## 0. Dirección autoral y objetivo conservado

Rubén pide explorar el significado físico-matemático generalizable del objeto
llamado provisionalmente K, su vínculo con pi, phi, e, alfa e incidencia
excepcional, sin desplazar el eje conservación–memoria–realización del artículo.
Se conserva literalmente la precisión terminológica recibida:

> Cuando digo universal nueva me refiero a esa universalidad de generalización del significado. y explórala. Yo creo que la hay que llevar al límite, porque es la clave de enganche con Pi, Fi, E alfa y simetrías excepcionales y eso también atañe al PDF que vas a hacer.

La pregunta concreta es qué reconstrucciones permite el mismo objeto generado,
qué estructura conserva al cambiar de representación y qué observables de sus
realizaciones quedan determinados. El nombre será posterior a esa función.

## 1. Antecedentes efectivos y orden causal

Los dos ejes nonádicos producen mediante APP las hojas aditiva y multiplicativa,
con residuo y cociente. TRIT conserva orientación, régimen y memoria local. Las
operaciones de selección, transporte y actualización del TPK producen el estado
enriquecido, su prolongación y la estructura discreta conjunta del continuo. Se
mantienen juntas las cinco construcciones y la doble lectura de cilindros e
incidencia; esta nota estudia lectores posteriores de uno de sus registros.

La procedencia de los antecedentes está dentro del manuscrito existente:

`../PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/`.

- `sections/nucleo.tex`, `trit_desarrollo.tex`, `tpk_desarrollo_integrado.tex`:
  núcleo común, operaciones, orientación, extensión y memoria.
- `sections/registro_k.tex`, ecuaciones `k-lector-firmado`, `k-bloques-firmados`,
  `k-u-firmado`, `k-vector`, `k-diferencia-kappas`: registro de eventos,
  extracción de canales, transformación de Hadamard y lecturas de fase.
- `sections/registro_imagen_integral.tex`, teorema `img09:imagen`:
  imagen integral y reconstrucción única desde canales y carga.
- `sections/alpha.tex`, ecuación `alpha-identidad-completa`: clausura de la vía A.
- `sections/k_reversibilidad.tex`: inversión posicional y cambio de fase.
- `sections/revision_k.tex`, `excepcional.tex`: selección incidencial y bandera.
- `sections/k_direccion_dimensional.tex`: proyector tridimensional, dirección y
  complemento transversal, con sus cartas y transformaciones.
- `nuclear/10.tex`: acoplamiento reversible y recuperación no estacionaria.
- `nuclear/11.tex`: dos memorias, estabilidad, transporte exterior y descriptor.

El registro utilizado como testigo publicado es

\[
k=(234,543,140,729,659,824,621,58,914,794,146,601).
\]

Se recibe como salida del registro firmado producido en el manuscrito, no como
entrada primaria de APP ni como valor metrológico. El programa de esta nota
comprueba sus lectores posteriores; no anuncia haber reejecutado el productor
completo desde las semillas. El orden heredado es

\[
x_{\rm term}\longmapsto(P,E,\Phi),\qquad
x_{\rm term}\longmapsto U^{\rm sgn}_{12}\longleftrightarrow k,
\qquad(P,E,\Phi,k,\text{acarreo})\longmapsto\alpha_A.
\]

La rueda de 108 posiciones organiza doce ventanas nonádicas. Su extensión
cíclica conserva la diferencia entre retorno de fase y actualización del estado.
La letra S empleada abajo designa exclusivamente el desplazamiento de las doce
coordenadas de esa carta; la historia completa tiene sus transportes propios.

## 2. Recuperación conjunta desde la clausura aritmética

Sean B=1000, D=B^12−1 y

\[
N(k)=\sum_{j=1}^{12} k_j B^{12-j},\qquad
\kappa(k)=\frac{N(k)}D,\qquad
a=\pi_{\rm HMT}+e_{\rm HMT}-\varphi_{\rm HMT}-4.
\]

La identidad heredada es \(\alpha_A=a-\kappa(k)\), con normalización y
frontera compatibles. La lectura periódica y la lectura finita N/B^12
conservan usos distintos. Se trabaja aquí con la primera.

**Proposición 1.** En el dominio de palabras de doce bloques, con B, longitud,
origen y orientación fijados, el par exacto (a, alfa_A) determina el registro
entero y todas sus funciones incidenciales y lineales ya definidas.

**Prueba.** Se obtiene N=D(a−alfa_A). La división euclídea iterada por B,
con doce posiciones conservadas, recupera k. Se compone después con cada lector
del manuscrito, por ejemplo k↦(D3k,D4k,Q(k)), k↦B_k y k↦P10(k).
La prueba invierte una salida previamente generada: no utiliza alfa para
seleccionar el registro causal inicial. Tampoco identifica el registro de doce
posiciones con la totalidad de una historia de profundidad ilimitada. □

**Precisión suficiente.** Si una aproximación de a−alfa_A tiene error menor
que 1/(2D), redondear D veces esa aproximación al entero más próximo recupera N
exactamente. El radio estricto es

\[
\frac1{2(1000^{12}-1)}.
\]

Es una garantía para la carta entera completa: valores vecinos N y N+1 distan
1/D. No afirma que todo vecino sea generado por el perfil HMT. Si a y alfa_A
se aproximan separadamente, basta que la suma de sus cotas de error sea menor
que ese radio. La recuperabilidad exacta no equivale a disponibilidad metrológica
de semejante precisión; ambas cuestiones tienen especificaciones distintas.

## 3. Completitud cíclica del registro publicado

Trabajamos en la realización lineal posterior V=R^12, con el producto interior
de la carta. Definimos (Sx)_i=x_(i+1), índices módulo doce, y

\[
O_k=(k,Sk,\ldots,S^{11}k).
\]

**Teorema 2.** Las doce columnas de O_k forman una base de V. Para cualquier
coeficiente c se cumplen las cotas óptimas

\[
589609\,\|c\|^2\le\|O_kc\|^2\le39225169\,\|c\|^2.
\tag{1}
\]

Por tanto \(\|O_k^{-1}\|=1/\sqrt{589609}\) y su número de condición es
\(6263/\sqrt{589609}\), aproximadamente 8,16. La órbita del registro centrado
abarca exactamente las once dimensiones ortogonales al modo uniforme.

**Prueba.** El Gram es circulante. Sus autocorrelaciones, en el orden j=0,…,11,
son

\[
(4251257,2999323,3163385,3287920,3216553,3344743,
2950064,3344743,3216553,3287920,3163385,2999323).
\]

Diagonalizando mediante los doce caracteres de la carta cíclica, sus valores
propios, con multiplicidades, son

\[
\begin{array}{c|c}
\lambda&\text{multiplicidad}\\\hline
39225169&1\\
1248025-345420\sqrt3&2\\
589609&2\\
1407529&2\\
1053157&2\\
1248025+345420\sqrt3&2\\
697225&1.
\end{array}
\]

El menor es 589609: para la única comparación no inmediata,
658416>345420√3 se verifica elevando al cuadrado ambos miembros positivos.
El mayor es 6263²; la suma positiva de las coordenadas alcanza esa amplitud en
el carácter trivial y acota todas las demás por desigualdad triangular.
El teorema espectral da (1). Restar la media elimina únicamente el carácter
trivial y deja positivos los otros once valores. □

El certificado entero independiente da

\[
\det O_k=5483119259214020183850397930008283625\ne0.
\]

`RESULTADOS_EXACTOS.json` conserva además la matriz entera J y el denominador
d tales que O_k J=dI; el programa comprueba las dos inversas con fracciones
exactas. El cálculo verifica las constantes de la prueba, no sustituye el
argumento de diagonalización.

**Contenido.** La distinción de las doce fases, ya conocida, se refuerza aquí:
las doce lecturas rotadas son linealmente independientes. La sola ausencia de
un período propio no basta para esa independencia; lo decisivo es que ningún
modo de la realización cíclica se anula en este registro.

## 4. Identificación de operadores a partir de sus respuestas

**Teorema 3.** Sea H:V→V lineal. Conocidas las doce respuestas H S^j k, H queda
determinado por

\[
H=(Hk,HS k,\ldots,HS^{11}k)O_k^{-1}.
\tag{2}
\]

Si además HS=SH, basta una respuesta completa y=Hk:

\[
H=O_yO_k^{-1}.
\tag{3}
\]

**Prueba.** La matriz de respuestas es HO_k y se aplica la inversa del teorema
2. La conmutación transforma cada respuesta HS^jk en S^jy. □

Para una perturbación E de la matriz de respuestas,
\(\|\delta H\|\le\|E\|/\sqrt{589609}\). En (3), si la respuesta y tiene
error δy, \(\|O_{\delta y}\|\le\sqrt{12}\|\delta y\|\), luego

\[
\|\delta H\|\le\sqrt{12/589609}\,\|\delta y\|.
\]

Los transportes polinómicos en S, incluidos los lectores T3,T4 y sus
complementos, pertenecen a este dominio de conmutación. Otros operadores
requieren sus doce respuestas o una estructura adicional probada. No se
atribuye esta conmutación a todo el TPK, a cualquier Hamiltoniano ni al grupo
Monstruo.

**Falsador de generalización.** El operador cuya primera fila es
(543,−234,0,…,0) y cuyas restantes filas son nulas es distinto de cero y
anula k. Por tanto, una respuesta aislada al registro no identifica un operador
arbitrario. Ese operador no conmuta con S. La hipótesis de (3) es efectiva.

### 4.1. Aplicación: reconstrucción de la holonomía relativa

El propietario `nuclear/11.tex`, ecuación `nuc11:eq:25`, relaciona dos
transportes invertibles H_B,H_C sobre un lazo con su complemento de memoria:

\[
D_\gamma=\frac{\sqrt8}{9}(H_C-H_B),\qquad
H_B^{-1}H_C=I+\frac9{\sqrt8}H_B^{-1}D_\gamma.
\]

El manuscrito recupera esta igualdad de operadores conociendo las respuestas
del complemento sobre una base. El teorema 2 identifica ahora una base
construida por las fases del propio registro: k,Sk,…,S^11k. Si H_B y H_C
conmutan con S, también lo hace D_gamma, y una respuesta vectorial completa
y=D_gamma k determina

\[
\boxed{H_B^{-1}H_C
=I+\frac9{\sqrt8}H_B^{-1}O_yO_k^{-1}.}
\tag{3a}
\]

Se conocen el transporte de referencia H_B y la carta S. La respuesta y
consta de doce componentes; no es una única medición escalar. Para error δy,
el error de la holonomía recuperada está acotado por

\[
\frac9{\sqrt8}\|H_B^{-1}\|
\sqrt{\frac{12}{589609}}\,\|\delta y\|.
\]

Para transportes de referencia unitarios, el factor ||H_B^-1|| es uno. La
fórmula es covariante al transportar simultáneamente registro, carta y
transportes. Si la conmutación no pertenece a la realización, se usan las
doce respuestas sobre la base del registro y se aplica (2).

**Ejemplo exacto.** Tomando H_B=S³, H_C=S⁴ en el dominio unitario del
acoplamiento ya definido, el programa recibe la respuesta
z=D_gamma k/√8=(S⁴−S³)k/9 y H_B. Reconstruye mediante (3a) la holonomía
relativa S, sin recibir H_C en el procedimiento inversor. Ésta es una
instancia algebraica del protocolo del manuscrito, no una identificación
experimental de un lazo físico. La conclusión general es que la memoria
puede determinar la diferencia completa entre los dos transportes, utilizando
el registro como referencia de sus respuestas.

## 5. Conservación de esta capacidad a profundidad arbitraria

El resultado rector del manuscrito proporciona, para sus compresiones T_n y
complementos D_n, P_0=I, P_(n+1)=T_nP_n y

\[
\mathcal V_Nx=(P_Nx,D_0x,D_1P_1x,\ldots,D_{N-1}P_{N-1}x),
\qquad\mathcal V_N^*\mathcal V_N=I.
\]

Para el límite no estacionario, A_∞=s-lim P_N*P_N y

\[
\mathcal V_\infty x=(A_\infty^{1/2}x,(D_nP_nx)_{n\ge0}),
\qquad\mathcal V_\infty^*\mathcal V_\infty=I.
\]

Se conserva el terminal positivo completo; no se reemplaza A_∞ por un
proyector salvo que se haya probado esa propiedad en la realización concreta.

**Teorema 4.** Para toda profundidad finita y para el límite anterior,

\[
(\mathcal V O_k)^*(\mathcal V O_k)=O_k^*O_k.
\tag{4}
\]

La órbita transportada conserva exactamente las cotas (1) y es base de su
imagen de dimensión doce. Todo resultado de reconstrucción de los teoremas
2–3 se transporta a esa imagen mediante la inversa \(\mathcal V^*\).

**Prueba.** Insertar \(\mathcal V^*\mathcal V=I\) en el producto. Para el
límite, la existencia e isometría proceden del balance no estacionario citado;
la polarización conserva también los productos cruzados de las doce columnas.
Como sólo se transportan doce columnas, el Gram finito queda idéntico en el
sistema ampliado, aunque su componente de memoria tenga longitud ilimitada. □

En la imagen de V, los operadores transportados son
\(\widehat S=\mathcal V S\mathcal V^*\) y
\(\widehat H=\mathcal V H\mathcal V^*\).
Se cumple \(\widehat S^j\mathcal V=\mathcal V S^j\), y la conmutación
HS=SH equivale allí a la conmutación de sus transportados. Así se define la
órbita después del almacenamiento: no se identifica con un desplazamiento
arbitrario de las componentes del espacio ambiente ampliado.

La afirmación conserva doce modos del registro en una representación de memoria
posiblemente infinita. No limita a doce la dimensión del estado enriquecido
global ni supone periodicidad de su evolución. La dimensión algebraica de este
lector y las dimensiones de las realizaciones físicas conservan sus mapas propios.

## 6. Articulación con incidencia y selección dimensional

La extracción B_k={j:k_j≥729} produce {4,6,9,10}. El manuscrito enlaza esta
tétrada con los códigos regionales y el soporte firmado de la clausura para
construir la bandera excepcional. El mismo k fija

\[
x=P_{11}k,\quad u=P_3x\ne0,\quad
E_u=uu^*/\|u\|^2,\quad P_{10}=P_{11}-E_u.
\]

El carácter tridimensional, la carta de incidencia y la norma usados aquí son
los del propietario `k_direccion_dimensional.tex`, posteriores a la generación
del registro. Su geometría no selecciona retroactivamente sus coordenadas.

Por las proposiciones 1 y 3, estas funciones del registro pueden reconstruirse
desde la clausura exacta, o desde las respuestas completas recuperadas mediante
memoria. Por (4), su transporte conserva el producto interior necesario para
reconstruir u, E_u y P10. Las pruebas cuantitativas complementarias se reúnen en
`APORTE_INCIDENCIA.md` y `APORTE_TRANSPORTE.md`.

La reducción 12→11→10 tiene causas distintas: eliminación del modo uniforme y
selección de una dirección no nula por el registro. Los mapas hacia la pantalla
reticular, dualidad y realizaciones posteriores permanecen como en el manuscrito.
El presente resultado fortalece la recuperabilidad de sus antecedentes; no añade
por conteo de coordenadas una identificación física distinta.

### 6.1. Protección exacta de la incidencia mediante las memorias enteras

El lector antecedente usa

\[
T_j=(8I+S^j)/9,\quad D_j=\sqrt8(S^j-I)/9,
\qquad Mk=(D_3k,D_4T_3k).
\]

Su núcleo es la dirección uniforme. La nota `APORTE_INCIDENCIA.md`, §§2–4,
demuestra mediante cortes ponderados y paridad las separaciones exactas

\[
\min_{h\in\mathbb Z^{12}\setminus\mathbb Z\mathbf1}\|Mh\|^2
=\frac{2336}{6561},\qquad
\min_{h\in\mathbb Z^{12}\setminus\{0\},\,\sum h_i=0}
\|Mh\|^2=\frac{4672}{6561}.
\]

El primer mínimo permite recuperar exactamente la clase centrada sin carga;
el segundo permite recuperar k completo con q=Σk_i conocido. El radio estricto
de corrección en este segundo caso es

\[
r_q=\frac{4\sqrt{73}}{81}\simeq0.421926.
\tag{5}
\]

La norma es la norma euclídea conjunta de las dos memorias M, no una incertidumbre
en unidades físicas. Las constantes de separación se deducen del lector y de
la red entera, independientemente del registro canónico. El teorema vale sobre
su dominio algebraico; no selecciona nuevas historias enriquecidas.

Esto resuelve una dificultad operativa específica. Como k_4=729, un error
continuo arbitrariamente pequeño hacia abajo puede alterar el selector de
bloques altos. La decodificación entera previa, dentro de (5), recupera 729
exactamente y mantiene B_k={4,6,9,10}. Con los restantes datos marcados de la
construcción excepcional conservados, queda restituida la misma bandera. La
recuperación de k no corrige por sí sola errores independientes en esas marcas.

**Algoritmo finito con garantía.** Para y=Mk+e y carga q exacta, sea L la
inversa de mínimos cuadrados sobre el complemento uniforme. El antecedente
da ||L||=9/4. Entonces

\[
\widetilde k=(q/12)\mathbf1+Ly,\qquad
\|\widetilde k-k\|<\frac94r_q=\frac{\sqrt{73}}9<1.
\]

Cada coordenada entera de k pertenece al par formado por el suelo y el techo
de la correspondiente coordenada de k tilde. Basta enumerar esos pares,
conservar los candidatos de suma q y minimizar ||Mh−y||. Son a lo sumo
2^12 candidatos; el teorema de separación garantiza el ganador único. En una
coordenada entera de k tilde, suelo y techo coinciden. La garantía utiliza
\(\|e\|<r_q\); fuera de ese régimen esta búsqueda acotada no se presenta
como decodificador universal.

**Ejemplo ejecutado.** El programa forma z=Mk/√8, añade 1/10 únicamente a la
primera coordenada de z y entrega esas memorias perturbadas y q=6263 al
decodificador, sin entregar k. El error en unidades de M tiene norma
√8/10≈0.282843, menor que (5). El algoritmo examina 924 candidatos de carga
correcta y devuelve los doce bloques originales, incluida la selección
{4,6,9,10}. `RESULTADOS_EXACTOS.json` conserva la salida. Este ejemplo
ejecuta una reconstrucción con ruido; la prueba de cobertura del radio es la
demostración anterior, no la sola recuperación de ese caso.

### 6.2. Conservación de la selección geométrica y su carga variacional

La nota `APORTE_TRANSPORTE.md` demuestra la composición

\[
P_{10}^{\mathcal V}
=\mathcal V P_{10}(k)\mathcal V^*
=\mathcal V P_{11}\mathcal V^*
-\frac{(\mathcal V u)(\mathcal V u)^*}{\|u\|^2}.
\tag{6}
\]

En la imagen de la isometría se conservan la dirección, el complemento,
los productos interiores y las correlaciones entre bloques de memoria.
El descriptor η=||u||²/||P11k||² es el peso cuadrático exacto del sector
seleccionado; su complemento tiene peso 1−η. Ambos se conservan bajo el
transporte conjunto del registro y del lector.

La distinción entre ese transporte y cambiar sólo k es verificable: en la carta
P3 fija, los desplazamientos S³k y S⁴k cambian η. La nota proporciona las
evaluaciones exactas en Q(√5). Por tanto el resultado es covariante y precisa
los objetos que deben transportarse conjuntamente; no impone invariancia de
una lectura fija bajo cualquier cambio del registro.

El enlace variacional utiliza la acción de transporte ya escrita en el artículo,
con sus covariables. Si A_n es el proyector transportado y las ecuaciones dan
q_(n+1)=U_nq_n, p_n=U_n* p_(n+1), entonces

\[
A_{n+1}U_n=U_nA_n
\quad\Longrightarrow\quad
J_n=p_n^*A_nq_n=J_0.
\tag{7}
\]

La simetría y la prueba por variaciones están explicitadas en la nota; no se
identifica esta acción auxiliar con cualquier acción física del corpus. En la
realización ortogonal y con p_n=q_n, J_n es la norma cuadrada del sector
transportado. Así se conecta selección estructural, memoria y cantidad conservada
mediante una cadena concreta de operadores.

## 7. Qué significa la universalidad que se está investigando

El contenido preciso obtenido es una capacidad de referencia estructural:
el objeto generado participa en la clausura aritmética, determina incidencia y
dirección, y su órbita distingue todos los modos de la carta de fase. La ley de
conservación transporta íntegramente esa capacidad mediante lectura y memoria.
Es una función generalizable de reconstrucción, no sólo la fijación de una lista.

Tres nociones permanecen separadas:

1. **Objeto determinado:** el registro de la construcción canónica, con su
   origen, orientación, canales y carga generados.
2. **Invariantes de representación:** clases, normas y proyectores bajo las
   transformaciones que transportan simultáneamente el objeto y sus lectores.
3. **Ley de conservación:** isometría completa, que conserva todas las
   correlaciones incluso cuando la lectura visible cambia.

Ningún nombre nuevo sustituye estas pruebas. La elección de nombre debe expresar
la función que finalmente reúna el artículo, no el acrónimo del marco o solamente
el número de posiciones.

**Control de suficiencia de un descriptor único.** El cociente η del manuscrito
retiene el peso relativo de un sector. En la realización lineal, k y k+1 tienen
la misma componente centrada, dirección, proyector y η, pero

\[
\kappa(k+\mathbf1)-\kappa(k)=1/999.
\]

Manteniendo las regiones, cambia en −1/999 la fórmula de clausura. Esto prueba
que un descriptor geométrico que olvida la carga no sustituye el objeto completo.
Es una prueba del dominio algebraico de los lectores; no declara ambos registros
estados terminales del mismo perfil generador ni una variación física admisible.

## 8. Procedencia, comprobaciones y decisión editorial

La idea de vincular registro, constantes, espacio e incidencia es arquitectura
autoral preexistente. La inversión racional, los lectores transversales, la
bandera, P10 y la isometría de memoria son resultados recuperados del manuscrito.
La composición de recuperación desde alfa es una formalización reunida.

La completitud cíclica con espectro exacto, la identificación de operadores y
su conservación por la isometría constituyen desarrollos añadidos en esta nota.
Se buscaron antecedentes por `cíclico`, `circulante`, `Bézout`, `observabilidad`,
`resultante` y expresiones afines en las fuentes del paper y las doce notas de
investigación. No se localizó allí este teorema concreto. No se afirma prioridad
mundial ni ausencia en los 300 GB del corpus: la procedencia global queda abierta.

`verificar_exploracion.py` ejecuta aritmética entera y racional, sin librerías
externas, y conserva espectro, inversa, redondeo, leyes de fase y falsadores.
Se ejecutó en modo normal y con `-O`, con resultados idénticos. El código usa
excepciones explícitas para que los controles no desaparezcan al optimizar.

La exploración mantiene el eje del artículo: conservación estructural,
reconstrucción desde memoria, incidencia y consecuencias de realización. La
ponderación editorial propuesta es incorporar el teorema cíclico después de la
reconstrucción del registro, y su conservación después de la isometría general.
Se preservan las derivaciones anteriores. No se ha compilado una nueva edición.

## 9. Balance de la exploración y tesis que se conserva para el artículo

Las aplicaciones se han reunido sin sustituir el eje del manuscrito. Su contenido
central se precisa así: **la conservación de memoria preserva la capacidad de
reconstruir estructura y respuesta, además de conservar la norma**.

La cadena efectiva de esta exploración reúne cuatro resultados:

1. La clausura aritmética, con las regiones y su normalización fijadas, permite
   recuperar el registro que participa en ella y sus lecturas incidenciales.
2. La órbita del registro publicado abarca su espacio de doce modos: sus
   respuestas identifican operadores del dominio declarado y reconstruyen
   la holonomía relativa desde el complemento de memoria del manuscrito.
3. La memoria completa conserva exactamente esa capacidad a cualquier
   profundidad; las dos memorias parciales también permiten recuperación
   entera estable, con el canal de carga cuando se necesita la selección absoluta.
4. La dirección geométrica seleccionada viaja con los lectores y conserva una
   carga en la acción de transporte especificada.

La afirmación de centralidad se apoya en estas composiciones, no en renombrar K.
La lectura racional periódica es una representación escalar reversible del
registro con base, longitud y origen fijados. El objeto registrado contiene sus
canales, carga, orden y mapas; un único descriptor de forma como η conserva
menos información. Esta distinción ayuda a decidir qué entidad y qué función
debe nombrar una eventual denominación científica.

El teorema de base cíclica es una aplicación de álgebra lineal a este registro
generado; el teorema general vale para todo vector cíclico. La aportación focal
es demostrar que el registro publicado satisface la condición, determinar sus
cotas exactas y componerlas con el transporte de memoria e incidencia existente.
No se atribuye a esa herramienta algebraica una novedad universal ni se deduce
una magnitud física adicional del solo hecho de obtener un escalar.

Queda preparada la integración científica: añadir estas pruebas y su ejemplo
operativo, conservar los antecedentes y decidir el nombre por la función reunida.
El alcance de esta entrega es la exploración escrita y ejecutable. El manuscrito
y el PDF existentes no han sido alterados.
