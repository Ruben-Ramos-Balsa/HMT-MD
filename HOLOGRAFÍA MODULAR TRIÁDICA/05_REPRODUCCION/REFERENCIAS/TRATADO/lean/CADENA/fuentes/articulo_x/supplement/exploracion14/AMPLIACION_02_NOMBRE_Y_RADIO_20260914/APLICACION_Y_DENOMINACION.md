# Función computacional y denominación del registro estructural

14 de septiembre de 2026. Nota focal para la investigación de la función del objeto denominado provisionalmente K. Conserva el manuscrito y los archivos sellados.

## 1. Propuesta de definición y nombre

**Nombre recomendado: constante de enlace estructural.**

Definición propuesta: *la constante de enlace estructural es el objeto finito ordenado producido por el registro orientado de la construcción, cuya lectura posicional es reversible y cuyas realizaciones declaradas coordinan la clausura aritmética, la incidencia y la dirección geométrica; su órbita de fase completa permite reconstruir los operadores del portador cíclico en los dominios de identificación demostrados*.

La definición conserva el orden **objeto generado → representaciones → funciones de lectura**. Su carácter fundamental se expresa por esa función de enlace, no por introducir una nueva entrada primaria ni por afirmar que un único escalar contenga toda la historia enriquecida. La normalización, la orientación y el origen de fase forman parte del objeto declarado. Una actualización con nuevos eventos y un cambio de carta son operaciones distintas.

Se propone reservar el símbolo K para el objeto ordenado y κ para su lectura racional periódica. Ambos pueden convertirse uno en otro en la carta fijada, pero no poseen el mismo tipo matemático. El primero permite aplicar directamente incidencia, desplazamiento y proyección; el segundo conserva la codificación numérica exacta.

**Segunda opción: constante de referencia correlativa.** Expresa que el objeto sirve de referencia común a lectores diferentes y, por su órbita, a la identificación de operadores. Tiene una ventaja: evita sugerir que K sea un coeficiente de interacción física. Su desventaja es que «referencia» describe menos directamente su intervención en la clausura aritmética.

No propongo «constante de reconstrucción universal»: el adjetivo ocultaría las hipótesis de conmutación, el portador y la información disponible. Los dos nombres anteriores son propuestas funcionales; no se les atribuye prioridad terminológica mundial. Tampoco se modifica la denominación del manuscrito existente en esta nota.

## 2. Representación exacta utilizable en informática

La salida del registro APP–TRIT–TPK del manuscrito precede a esta codificación. Fijados `B=1000`, doce posiciones, origen y orientación,

\[
 N(K)=\sum_{j=1}^{12}K_jB^{12-j},\qquad
 D=B^{12}-1,\qquad \kappa(K)=N(K)/D.
\tag{1}
\]

El procedimiento exacto es:

1. recibir K como salida del productor tipado;
2. construir N por `N←BN+K_j`;
3. conservar N y el esquema de lectura —base, longitud y carta—;
4. recuperar las doce componentes mediante doce divisiones euclídeas sucesivas por B;
5. aplicar al objeto recuperado los lectores de incidencia y los proyectores ya definidos.

Si se recibe κ como una fracción reducida `p/q`, se calcula `N=Dp/q` y se comprueba su integralidad y el dominio `0≤N≤D`; la misma división recupera K. El denominador reducido por sí solo no sustituye los metadatos de longitud y base.

El dominio de todas las palabras de doce bloques tiene `1000^12=10^36` elementos. Una representación binaria de longitud fija necesita

\[
 \lceil\log_2(10^{36})\rceil=120
\]

bits para el entero N. Ésta es una cifra de capacidad del código, no un resultado de compresión del corpus: los doce bloques almacenados individualmente en diez bits también ocupan 120 bits. La etiqueta de carta y las reglas de incidencia conservan su propia representación. K no se reduce a sus dígitos sin dichas reglas si se pretende aplicar sus funciones estructurales.

**Recuperación desde datos aproximados.** La inversión entera de κ es garantizada cuando

\[
 |\widetilde\kappa-\kappa|<\frac1{2D}.
\tag{2}
\]

Se redondea `D κ_tilde` al entero más próximo y se decodifica. La prueba es que el intervalo de error tiene radio menor que media unidad en la escala entera. Este requisito es mucho más estricto que conservar unas pocas cifras significativas: para un intercambio reproducible se prefiere el entero o la fracción exacta. El código no acredita por sí solo procedencia, integridad frente a alteraciones ni autenticación.

## 3. Identificación de filtros cíclicos mediante una respuesta vectorial

En la realización lineal posterior, sea `Sx_i=x_(i+1)` y

\[
 O_K=(K,SK,\ldots,S^{11}K).
\]

El teorema cíclico del desarrollo prueba

\[
 \lambda_-I\le O_K^*O_K\le\lambda_+I,
 \quad\lambda_-=589609,\quad\lambda_+=39225169=6263^2.
\tag{3}
\]

Un operador lineal H que conmuta con S tiene una escritura única

\[
 H=\sum_{j=0}^{11}h_jS^j.
\]

En efecto, la conmutación determina todas sus columnas desde una de ellas; las doce potencias de S generan exactamente ese espacio de operadores. Una respuesta completa `y=HK`, de doce componentes, da

\[
 y=O_Kh,\qquad
 \boxed{h=O_K^{-1}y,\quad H=O_yO_K^{-1}.}
\tag{4}
\]

Por tanto el registro puede utilizarse como referencia determinante de un filtro de convolución cíclica. Se precomputa la inversa exacta de O_K, se aplica una vez el filtro al registro y se resuelve (4). «Una respuesta» no significa una medición escalar: se necesita el vector y completo y la conmutación debe formar parte de la especificación del sistema.

Para ruido aditivo `||δy||≤ε`,

\[
 \|\widehat h-h\|\le\frac\epsilon{\sqrt{589609}},
 \qquad
 \|\widehat H-H\|\le\sqrt{\frac{12}{589609}}\,\epsilon.
\tag{5}
\]

La primera cota usa directamente `||O_K^-1||`. Para la segunda, la matriz `O_(δy)` tiene doce columnas de norma `||δy||`; su norma operatoria está acotada por su norma de Frobenius, `sqrt(12)||δy||`. Los factores son aproximadamente `0.00130232` y `0.00451137` respectivamente.

Las cotas absolutas anteriores incluyen la amplitud concreta de K. Su condicionamiento es `6263/sqrt(589609)≈8.15643`. Si se normaliza K a norma uno, los límites del Gram son `589609/4251257` y `39225169/4251257`. Por tanto no debe atribuirse a la magnitud de sus coordenadas una mejora intrínseca frente a cualquier referencia de igual norma.

Un control sencillo fija el alcance: el vector de impulso e₀ tiene una órbita que es una base ortonormal y también identifica todo filtro cíclico mediante una respuesta. Así, la identificación de filtros no es por sí sola una capacidad exclusiva ni una novedad histórica. El resultado específico obtenido aquí es que **el mismo K ya producido por la construcción y usado en clausura e incidencia satisface además la condición de referencia cíclica completa**, con espectro y cotas exactas. No fue elegido de nuevo para optimizar el ensayo del filtro.

Para un operador general sin conmutación se requieren las doce respuestas `HS^jK`:

\[
 H=(HK,HSK,\ldots,HS^{11}K)O_K^{-1}.
\]

El operador no nulo con primera fila `(543,-234,0,...,0)` y restantes filas cero anula K; demuestra que una respuesta aislada no identifica un operador arbitrario.

### Aplicación a holonomía relativa

El acoplamiento del manuscrito da

\[
 D_\gamma=\frac{\sqrt8}{9}(H_C-H_B),\qquad
 H_B^{-1}H_C=I+\frac9{\sqrt8}H_B^{-1}D_\gamma.
\]

Si `H_B` es conocido e invertible y `D_gamma` conmuta con S —en particular, si lo hacen `H_B,H_C`—, una respuesta `y=D_gamma K` determina

\[
 \boxed{H_B^{-1}H_C
 =I+\frac9{\sqrt8}H_B^{-1}O_yO_K^{-1}.}
\tag{6}
\]

Su error está acotado por `9/sqrt(8) · ||H_B^-1|| · sqrt(12/589609) ε`. En una referencia unitaria, el factor es aproximadamente `0.01435510`. La aplicación es concreta: para `H_B=S³`, `H_C=S⁴`, la respuesta del complemento permite reconstruir la holonomía relativa S sin proporcionar `H_C` al inversor. La selección de un lazo físico y su representación seguirán siendo las de su operador generador; (6) no las reemplaza.

## 4. Memoria completa y sistemas complejos

Sea V la isometría de terminal y complementos de memoria del manuscrito, con `V*V=I`. La referencia transportada conserva exactamente

\[
 (VO_K)^*(VO_K)=O_K^*O_K.
\]

Si se recibe la respuesta almacenada `z=Vy+δz`, la estimación

\[
 \widehat h=O_K^{-1}V^*z
\tag{7}
\]

mantiene la primera cota de (5), con `ε=||δz||`, porque `||V*||=1`. La profundidad del archivo de memoria no empeora esa constante cuando se conserva la isometría completa y su terminal. Una selección parcial de canales posee otro Gram y debe usar sus cotas propias; en el lector de dos memorias del manuscrito aparece precisamente la amplificación `9/4`.

En sistemas con interacciones cíclicas, esta construcción proporciona un ensayo lineal reproducible: aplicar la misma referencia en los nodos tipados, conservar las respuestas con sus posiciones y reconstruir el acoplamiento cíclico. Si existen campos de lectores transportados, el mismo procedimiento se efectúa en las imágenes isométricas, con `S^V=VSV*` y `H^V=VHV*`. No presupone que el desplazamiento ambiente del almacenamiento coincida con `S^V`.

La generalización matemática es un criterio explícito: para un portador de n posiciones y cualquier vector generado g, la aplicación `H↦Hg` identifica los operadores que conmutan con el ciclo **si y sólo si** `O_g=(g,Sg,...,S^(n-1)g)` es invertible. La prueba es (4); si O_g es singular, existe un polinomio no nulo de grado menor que n que anula g, y el operador correspondiente es no nulo porque las n potencias del ciclo son independientes. Para otros tamaños no se presume esta condición: se comprueba en el objeto realmente producido.

El lenguaje «sistemas complejos» designa aquí una aplicación a componentes lineales tipadas o a una linealización que se haya definido y justificado. No se concluye identificación de una dinámica no lineal, reconstrucción de toda una red con observaciones escalares, ni recuperación de estados ocultos arbitrarios. La reducción de parámetros de n² a n proviene de la simetría cíclica comprobada, no de una propiedad inexplicada del registro.

## 5. Conclusión de denominación y alcance

La universalidad defendible es **la generalización de la función de enlace y reconstrucción mediante mapas explícitos**, no la fijación del mismo vector numérico como referencia necesaria de cualquier sistema. El perfil canónico fija el objeto; sus realizaciones explican qué representa y qué conserva; los teoremas determinan dónde sirve de referencia computacional completa.

«Constante de enlace estructural» expresa conjuntamente esa participación en clausura, incidencia, dirección y reconstrucción. Para una formulación más conservadora respecto de una futura lectura física, «constante de referencia correlativa» describe el mismo objeto sin anticipar que opere como coeficiente dinámico. En ambos casos, la función precede al nombre.

### Fuentes y controles focales

- [Desarrollo de la exploración, §§2–5](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/EXPLORACION.md:78>): codificación reversible, teorema cíclico, identificación y holonomía.
- [Verificador exacto de la exploración](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/verificar_exploracion.py>): espectro, inversa, filtros, radio de redondeo y controles negativos; ejecución focal normal y optimizada revisada previamente.
- [Transporte de dirección y cargas](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/APORTE_TRANSPORTE.md>): transporte de P10 y eta, recuperación de norma uno, coherencia entre bloques y carga cotangente.
- [Registro y sus propietarios](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_k.tex:181>): producción del registro antes de sus lectores computacionales.

En esta intervención se recalcularon las cifras de capacidad y las cotas numéricas con biblioteca estándar, sin modificar los productores ni los sellos. La identificación de filtros y la representación racional son consecuencias matemáticas explícitas; no se anuncian como nuevas técnicas generales de informática. No se atribuyen autenticación criptográfica, ganancia cuántica, predicción física ni prioridad terminológica por analogía.
