# Ley bilateral de conservación, refinamiento de la unidad y transducción

14 de septiembre de 2026. Ampliación aditiva de la investigación fundacional. Se conserva íntegramente AMPLIACION_02_NOMBRE_Y_RADIO_20260914, incluidos sus recibos, así como el paper de 326 páginas y sus fuentes. Esta nota integra las aportaciones siguientes del autor y explicita una ley independiente de la dimensión del portador.

## 1. Denominación y objetivo conservado

El autor ha aprobado **constante holográfica de acoplamiento aritmético-geométrico** como denominación del objeto anteriormente indicado por K. Se conserva K para el registro ordenado y \(\kappa\) para su lectura posicional racional reversible en base 1000 y longitud doce.

La denominación expresa el enlace entre sus funciones aritméticas, incidenciales y geométricas. El operador de órbita \(O_K\), los transportes que actúan sobre el registro y el índice 73 conservan sus propios tipos; no se identifican todos ellos con K.

El objetivo de esta ampliación es obtener una ley explícita de conservación y recuperación, explicar su conexión con la normalización de la unidad y componerla con los lectores del registro. Las coordenadas \(\pi,\varphi,e,\alpha\), K y la incidencia se reciben de la genealogía previa APP–TRIT–TPK → estado enriquecido → estructura discreta conjunta del continuo; la nueva ley actúa sobre sus realizaciones y no sustituye sus productores.

## 2. Del centro documentado a la completación

El manuscrito contiene el bloque central
\[
B_c=\begin{pmatrix}7&2\\2&7\end{pmatrix}.
\]
Sus concatenaciones decimales cumplen
\[
72+27=77+22=99.
\]
La fuente diferencia esas concatenaciones de los autovalores 9 y 5, de la posición central y del registro electrónico.

Se añade ahora la composición aritmética exacta
\[
\boxed{
(72,27)\xrightarrow{+(1,0)}(73,27)
\xrightarrow{\,10(\cdot)+(-1,+1)\,}(729,271).}
\tag{1}
\]
Las sumas son 99, 100 y 1000. La última transición redistribuye una unidad entre dos componentes, conservando la suma después del cambio de escala:
\[
\frac{729}{1000}=\frac{73}{100}-\frac1{1000},\qquad
\frac{271}{1000}=\frac{27}{100}+\frac1{1000}.
\tag{2}
\]

La fuente de EMRH da además la partición concreta
\[
1000=729+243+27+1,\qquad 271=243+27+1.
\]
El último uno tiene residencia combinatoria en el ápice añadido. El nuevo mapa (1) reúne esas identidades con el índice ternario; su igualdad aritmética no identifica por sí sola todos los lectores físicos o las expansiones de constantes que utilizan números de esos bloques.

La familia algebraica posterior lo expresa sin depender de una concatenación accidental. Para \(b\ge3\), \(B=b+1\) y \(p_b=b^2-b+1\), las dos concatenaciones en base B de \((b-2,2)\) y \((2,b-2)\) son
\[
B(b-2)+2=b(b-1)=p_b-1,\qquad
2B+(b-2)=3b.
\]
Suman \(B^2-1\); restituir una unidad en la primera da \((p_b,3b)\), de suma \(B^2\). Entonces
\[
\boxed{Bp_b-1=b^3,\qquad B(3b)+1=B^3-b^3.}
\tag{3}
\]
El caso b=9 es el documentado. La generalización es una familia aritmética explícita, no la afirmación de que todos los b sean nuevos generadores de APP.

El transporte general con acarreo
\[
L_c(x,y)=(Bx-c,By+c)
\]
y su iteración con memoria, inversa y límites se desarrollan en REFINAMIENTO_CONSERVATIVO.md. El primer acarreo 1 de (1) no impone acarreos iguales en todos los pasos posteriores.

## 3. Ley bilateral para dos transportes isométricos

Sean H y H' espacios de Hilbert de realizaciones posteriores ya construidas, y sean \(B,C:H\to H'\) isometrías lineales:
\[
B^*B=C^*C=I.
\]
La letra B denota aquí un transporte y no la base posicional de §2. Para \(a>0\), se definen
\[
p=a^2+a+1=a(a+1)+1,\qquad
N=(2a+1)p=(a+1)^3+a^3,
\]
\[
Q_-=aB-C,\qquad Q_+=(a+1)B+C.
\]

**Teorema 1. Conservación bilateral independiente de la dimensión.**
\[
\boxed{(a+1)Q_-^*Q_-+aQ_+^*Q_+=NI.}
\tag{4}
\]

**Demostración.** Escribiendo \(X=B^*C+C^*B\),
\[
Q_-^*Q_-=(a^2+1)I-aX,\qquad
Q_+^*Q_+=((a+1)^2+1)I+(a+1)X.
\]
Los términos de X se cancelan al ponderar por a+1 y a. La suma de los términos escalares es
\[
(a+1)(a^2+1)+a((a+1)^2+1)
=2a^3+3a^2+3a+1=N.
\]
Esto prueba (4). No se ha usado conmutación entre B y C ni una relación de orden finito. ∎

En el caso nonádico a=8,
\[
\boxed{9\|Q_-v\|^2+8\|Q_+v\|^2
=(9^3+8^3)\|v\|^2
=17\cdot73\,\|v\|^2.}
\tag{5}
\]

La normalización 73 procede de \(8\cdot9+1=72+1\). En el ciclo ternario aparece además como determinante y norma de semejanza; esos significados específicos coexisten con el balance más general.

### Factorización explícita de la conservación

Definamos
\[
E_av=\frac1{\sqrt p}
\binom{\sqrt{a(a+1)}\,Bv}{Cv},\qquad
R_a=\frac1{\sqrt{2a+1}}
\begin{pmatrix}\sqrt a&-\sqrt{a+1}\\
\sqrt{a+1}&\sqrt a\end{pmatrix}.
\]
Entonces \(E_a^*E_a=I\), \(R_a^*R_a=I\), y
\[
\boxed{W_av:=R_aE_av
=\frac1{\sqrt N}
\binom{\sqrt{a+1}\,Q_-v}{\sqrt a\,Q_+v}.}
\tag{6}
\]
En a=8, el primer reparto tiene pesos \(72/73\) y \(1/73\); el segundo es una rotación entre canales. Ésta es la operación que da significado al 72+1 en la norma completa, antes de cualquier interpretación numérica adicional.

### Recuperación y compatibilidad

Para \(x=Q_-v\), \(y=Q_+v\),
\[
Bv=\frac{x+y}{2a+1},\qquad
Cv=\frac{ay-(a+1)x}{2a+1}.
\tag{7}
\]
Como B es isométrico,
\[
v=B^*\frac{x+y}{2a+1}.
\]
La reconstrucción estable desde los canales normalizados es
\[
v=W_a^*W_av,\qquad \|W_a^*\|=1.
\tag{8}
\]
La cota significa que el inversor no amplifica el error aditivo medido en la norma de esos canales.

Para B y C arbitrarios entre espacios, la compatibilidad de un par se expresa como pertenencia a \(\operatorname{im}W_a\), cuyo proyector ortogonal explícito es \(W_aW_a^*\). Cuando B=I y C=U es unitario, los Q conmutan y la condición se simplifica a
\[
Q_+x=Q_-y.
\tag{9}
\]
La condición simple (9) no se extrapola a transportes no conmutativos distintos sin componer sus dominios.

### Transporte de lectores y criterio exacto de conservación

Sea F un operador acotado autoadjunto sobre H'. El mismo lector actúa en ambos canales como diag(F,F). Entonces
\[
\boxed{
W_a^*\operatorname{diag}(F,F)W_a
=\frac{a(a+1)B^*FB+C^*FC}{a(a+1)+1}.}
\tag{9a}
\]

**Demostración.** En las expansiones de Q_-*FQ_- y Q_+*FQ_+ los términos cruzados B*FC+C*FB se cancelan con las ponderaciones a+1 y a. El coeficiente de B*FB es a(a+1)(2a+1) y el de C*FC es 2a+1. Dividir por N prueba la igualdad. ∎

La norma corresponde al lector F=I. Para otro lector, (9a) establece su transformación exacta y no presupone su conservación. Si B*FB=C*FC=G, el valor de G se conserva en todos los estados. Así se obtiene un criterio de compatibilidad entre ambos transportes y el observable conservado.

Cuando B es unitario y C=BR, con R unitario en el dominio, escribiendo G=B*FB se obtiene
\[
W_a^*\operatorname{diag}(F,F)W_a
=\frac{a(a+1)G+R^*GR}{a(a+1)+1}.
\tag{9b}
\]
Por tanto el lector G se conserva exactamente si y sólo si R*GR=G, equivalentemente GR=RG. Para a=8, los pesos son 72/73 y 1/73. La ley relaciona de manera explícita el reparto bilateral, los lectores y la simetría relativa de los transportes. Se trata de un resultado operatorio sobre las realizaciones especificadas; su identificación con una ley dinámica física conserva los operadores e hipótesis de la aplicación correspondiente.

## 4. Evolución reversible con memoria entrante

En un mismo espacio, sean B=I y C=U unitario. Escribamos
\[
A=\sqrt{a+1}\,Q_-/\sqrt N,\qquad
D=\sqrt a\,Q_+/\sqrt N.
\]
Son operadores normales que conmutan, al ser polinomios de U. La matriz de actualización
\[
\boxed{\mathscr R_a=
\begin{pmatrix}A&-D^*\\D&A^*\end{pmatrix}}
\tag{10}
\]
es unitaria.

**Demostración.** \(A^*A+D^*D=I\) por (4). La normalidad da también \(AA^*+DD^*=I\). Las entradas no diagonales de \(\mathscr R_a^*\mathscr R_a\) se anulan por conmutación. El mismo cálculo en el orden inverso da la identidad. ∎

Sobre \((v,0)\), la primera columna es W; sobre \((v,m)\), (10) conserva \(\|v\|^2+\|m\|^2\) y es invertible por el adjunto. Así la extensión admite memoria entrante, no sólo un archivo de salidas.

Para dos datos normalizados \(z=(z_1,z_2)\), la transformación inversa proporciona
\[
v_{\rm rec}=A^*z_1+D^*z_2,\qquad
m_{\rm rec}=-Dz_1+Az_2.
\tag{11}
\]
Una entrada de memoria nula exige \(m_{\rm rec}=0\). Con perturbación e de los datos,
\[
\|e\|^2=\|e_{\rm rec}\|^2+\|e_{\rm mem}\|^2.
\tag{12}
\]
El segundo término detecta la parte del error incompatible con memoria entrante nula. Un error contenido en la imagen W no se detecta por ese residuo solo; la recuperación entera de K utiliza además el código y los radios ya demostrados.

## 5. Archivo de profundidad arbitraria con agotamiento uniforme del terminal

En cada etapa n se permiten espacios H_n y dos isometrías \(B_n,C_n:H_n\to H_{n+1}\). Manteniendo a>0 fijo, sean \(A_n,D_n\) los dos bloques normalizados de (6). Se continúa por A_n y se archiva D_n:
\[
P_0=I,\quad P_{n+1}=A_nP_n,\quad m_n=D_nP_nv.
\]
Esta política es distinta de reintroducir m_n en la siguiente aplicación unitaria (10); ambas están definidas, pero no son el mismo procedimiento.

La desigualdad triangular da
\[
\|Q_{-,n}\|\le a+1,\qquad
\boxed{\|A_n\|^2\le r_a:=
\frac{(a+1)^3}{(a+1)^3+a^3}<1.}
\tag{13}
\]
Por tanto \(\|P_n\|^2\le r_a^n\), uniformemente en la dimensión y en la secuencia de transportes.

**Teorema 2. Recuperación desde la memoria completa.**
\[
\boxed{
\|v\|^2=\sum_{n\ge0}\|m_n\|^2,\qquad
v=\sum_{n\ge0}P_n^*D_n^*m_n.}
\tag{14}
\]
La aplicación \(v\mapsto(m_n)_{n\ge0}\) es isométrica; su adjunto tiene norma 1.

**Demostración.** La telescopía de \(A_n^*A_n+D_n^*D_n=I\) da
\[
I=P_N^*P_N+\sum_{n<N}P_n^*D_n^*D_nP_n.
\]
La norma del terminal está acotada por \(r_a^N\), así que tiende a cero en norma operatoria. La identidad límite prueba la isometría. Su adjunto proporciona la serie convergente de (14). ∎

Con sólo N registros,
\[
v-\sum_{n<N}P_n^*D_n^*m_n=P_N^*P_Nv,\qquad
\left\|v-\sum_{n<N}P_n^*D_n^*m_n\right\|\le r_a^N\|v\|.
\tag{15}
\]
Para a=8, \(r_a=729/1241\). En el caso específico U=S⁴, el espectro de A*A da la cota mejorada \(r_a=9/17\). Estas tasas pertenecen a la política explícita anterior; no se atribuyen a cualquier trayectoria del TPK sin esa selección.

## 6. Extensión a formas geométricas y precisión de alcance

Si b y b' son formas no degeneradas, simétricas o alternantes, y
\(B^*b'B=C^*b'C=b\), el mismo cálculo algebraico produce
\[
(a+1)Q_-^*b'Q_-+aQ_+^*b'Q_+=Nb.
\tag{16}
\]
Se conservan así la forma y sus transportes en las realizaciones declaradas. La fuente nuclear ya distingue métrica positiva, forma lorentziana y área orientada; esta ampliación mantiene esa distinción.

La convergencia contractiva y las cotas de ruido de §5 utilizan normas de Hilbert positivas. La identidad de forma (16) también vale para una forma indefinida o alternante, pero no implica esas desigualdades positivas. Esta separación permite aplicar los tres regímenes operatorios conservando sus hipótesis, en vez de identificarlos por compartir matrices de orden dos.

## 7. La prueba inversa de alfa dentro del balance general

Para v no nulo se define la correlación de los dos transportes
\[
\chi(v)=\frac{\operatorname{Re}\langle Bv,Cv\rangle}{\|v\|^2},
\qquad -1\le\chi(v)\le1.
\]
Las lecturas individuales son
\[
s_-=a^2+1-2a\chi,\qquad
s_+=(a+1)^2+1+2(a+1)\chi.
\tag{17}
\]
Con a=8,
\[
s_-=65-16\chi,\quad s_+=82+18\chi,\quad
9s_-+8s_+=1241.
\tag{18}
\]

Por tanto, usar \(s_-=10^4\alpha_A\) como ensayo inverso determina también
\[
\boxed{s_+=73+\frac98(73-10^4\alpha_A).}
\tag{19}
\]
La corrección en una lectura tiene una respuesta complementaria necesaria. En el ensayo, el valor aproximado es \(s_+\simeq73.029783595557\). La normalización conjunta permanece exactamente 73 después de dividir el balance por 17.

Éste es un resultado adicional al ensayo de fase: un cambio de fase unitario puede alterar las lecturas individuales y conservar la ley bilateral general, aunque cambie el orden ternario. (19) es una consecuencia de la hipótesis del ensayo, no una nueva derivación independiente de alfa ni una identificación de ese segundo valor con otra constante física del corpus.

## 8. Articulación con K y los lectores

La nota TRANSDUCCION_Y_RECUPERACION.md compone W, el archivo infinito de §5, el marco invertible O_K, la lectura posicional de \(\kappa\) y los lectores incidenciales. El contenido operativo es la inversión efectiva de los datos mediante operadores de norma controlada, antes de aplicar los lectores; no la generación retrospectiva de un estado que se haya empaquetado como primera coordenada.

K conserva su procedencia APP–TRIT–TPK, su orden y orientación. Su órbita permite una reconstrucción cíclica específica; la ley de conservación bilateral vale para más transportes que esa órbita particular. Esa diferencia de alcance distingue la constante generada, su función de transducción y una ley matemática aplicable a sus realizaciones.

## 9. Fuentes, clasificación y conservación editorial

Fuentes leídas para esta ampliación:

- [Núcleo: emisión, bloque central, curvatura y completación](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/extension.tex>).
- [Centro y concatenaciones 72/27 y 77/22](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/centro_electronico_registros.tex>).
- [EMRH: estratos, ápice y compatibilidad dimensional de la unidad](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/revision_emrh.tex>).
- [Acoplamiento, reentrada, terminal positivo y memoria ilimitada](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/10.tex>).
- [Ampliación precedente: norma ternaria, radio y ensayo inverso](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_02_NOMBRE_Y_RADIO_20260914/CONSTANTE_Y_NORMA_TRITICA.md>).

Las identidades centrales y la completación son antecedentes del corpus. La composición (1)–(3), la ley general (4), su factorización (6), la extensión (10) y la política contractiva de §5 constituyen formalizaciones añadidas en esta exploración. Se apoyan en la construcción anterior de transportes y memoria y no se presentan como demostraciones de prioridad histórica o como sustitución de los productores físicos.

La comprobación focal de continuidad de masas se ejecutó exclusivamente para la lectura del propietario central y terminó en PASS_SKILL_HMT_MASS_LAW. Su índice histórico sigue remitiendo a 2084 páginas; conforme al mandato de la serie, ese resultado no sustituye la selección activa de 2249 páginas. No se abrió una investigación nueva de masas ni se cambió la autoridad editorial.

El estudio inverso usa alfa ya generada como dato posterior declarado, con conservación de su genealogía. No se han cambiado fuentes selladas, PDFs anteriores, registros globales ni trabajos de otras tareas.

## 10. Orientación del artículo troncal propuesta durante esta ampliación

El autor propone reunir la extrema y media razón holográfica, la constante holográfica de acoplamiento aritmético-geométrico y la conservación evolutiva de la unidad dimensional por doble proyección. Se conserva esa orientación para el paper fundacional en curso, sin sustituirlo por un segundo proyecto ni alterar su PDF vigente.

La estructura expositiva se organiza mediante dependencias, con cuatro funciones explícitas:

1. La arquitectura APP–TRIT–TPK produce el estado enriquecido, sus transportes, la unidad y sus realizaciones correlacionadas.
2. La extrema y media razón holográfica proporciona los antecedentes de completación y compatibilidad dimensional; el refinamiento afín de esta nota formaliza una transferencia con memoria y unidad normalizada conservada.
3. El registro K y sus lectores relacionan datos aritméticos e incidenciales. La nueva denominación expresa esa función y conserva el orden y la orientación necesarios para evaluarla.
4. La ley bilateral conserva una forma cuadrática; su normalización positiva permite distribución reversible, archivo de profundidad arbitraria y reconstrucción con cotas explícitas. Los lectores del registro se componen después con esa recuperación.

La cohesión científica procede de los mapas que enlazan esas funciones. La conservación de una suma, la conservación de una forma y la recuperabilidad del registro tienen cantidades conservadas y dominios propios. Una presentación reunida debe mostrar su composición efectiva; compartir el número 73 no las convierte automáticamente en una misma aplicación.

Para realizar una primera composición explícita, puede codificarse la palabra finita de acarreos en sus coordenadas enteras finales y su profundidad, como demuestra REFINAMIENTO_CONSERVATIVO.md. Su representación lineal posterior puede transportarse por W o por el archivo isométrico, recuperarse mediante el adjunto y deshacerse después por divisiones euclídeas. Esta composición conserva los acarreos canónicos finitos y el control de ruido del transporte. La unidad normalizada del refinamiento sigue siendo la suma de sus dos componentes; la norma del archivo corresponde a su representación lineal. La realización física y los lectores específicos conservan además sus estructuras antecedentes.

El levantamiento más preciso de LEVANTAMIENTO_UNITARIO_REFINAMIENTO.md emplea como base las ternas admisibles (x,y,c), y envía cada una a la pareja final (Bx−c,By+c). La inversa por residuos demuestra una biyección de bases y, por tanto, una unitaria entre sus espacios de amplitudes. Para B=10 y x+y=100, ambos espacios tienen dimensión 1001. Este operador permite aplicar (4) y (9a) al refinamiento mismo, conservando la diferencia entre amplitudes sobre estados y las dos coordenadas aritméticas de cada etiqueta. El registro K conserva su espacio de doce componentes y su aplicación bilateral propia; las 1001 etiquetas de ese ejemplo no se identifican con sus doce posiciones.

La propuesta troncal permite dar unidad al paper actual: generación, compatibilidad dimensional, transducción, conservación y recuperación. La extracción de un artículo especializado y su eventual título se decidirán sobre esa exposición ya compuesta, preservando el desarrollo acumulado.

## 11. Controles ejecutables de esta ampliación

El programa verificar_ley_bilateral.py utiliza aritmética racional exacta y testigos finitos de las identidades, incluyendo transportes no conmutativos, transportes rectangulares, formas alternante y lorentziana, recuperación entera y archivo. Mantiene sus comprobaciones bajo optimización de Python. El programa recibe K de su propietario antecedente; no reproduce la generación HMT de ese registro ni certifica mediante iteración finita los teoremas generales de dimensión y profundidad arbitrarias, cuyas demostraciones están escritas arriba.

Los resultados normal y optimizado se conservan en RESULTADOS_LEY_BILATERAL.json y RESULTADOS_LEY_BILATERAL_OPT.json. Los recibos focales de genealogía y constantes describen la procedencia y el alcance de esta ampliación; son controles de trazabilidad, separados de las pruebas matemáticas.
