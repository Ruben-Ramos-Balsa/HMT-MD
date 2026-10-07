# Refinamiento ternario y cambio de carta decimal: derivación elemental y contratos de compatibilidad

REV03 — bloque 22 — 19 de septiembre de 2026.

## 1. Lugar de este desarrollo en el árbol global

Este bloque desarrolla CG-010, no sustituye el inventario previo. Su fuente inmediata es el artículo X sucesor; sus propietarios anteriores se localizan en el integral de 2.249 páginas y en ejecutables del reservorio. La V2 antigua de estructura discreta no delimita esta investigación.

La operación pertenece a la cadena APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo → lecturas. Recibe un bloque ternario ya producido por la prolongación y transporta la relación entre sus prefijos en dos cartas. No escoge la ruta mediante un valor conocido. La cuadrirrelación coinductiva (π,φ,e,α), su incidencia y las demás publicaciones permanecen salidas de la genealogía común; este bloque no vuelve a derivarlas ni las introduce como datos de ensayo.

**Procedencia:** las dos recurrencias son RESULTADO_RECUPERADO. Su desglose algebraico y los contratos de intervalo reúnen dependencias ya escritas en las fuentes. El nuevo script es CERTIFICADO_NUEVO focal, con ejemplos de carta declarados; no certifica por sí solo la selección global de una constante ni la admisibilidad de una historia en todos los campos TPK.

Concordancias:

- APP-004/005: representante, residuo y cociente; APP-008: conservación de ambas hojas; APP-022: base 1000.
- CG-001/002: división nonádica y balanceada; CG-008: prefijo y prolongación; CG-010: residuo de conversión; CG-016: recuperación con profundidad.
- LRG.10.4: recuperación del prefijo; LRG.10.6: índice de un sexteto; LRG.11.3–11.4: subcilindros y condiciones de borde; LRG.12: capacidad de emisión y vacancias.
- EDC-164/165/168–173: números, acarreo, lector y actualización del registro conjunto; EDC-190–206: compatibilidad y recuperación al límite.

El árbol expositivo y el grafo de dependencias siguen diferenciados. El mismo registro de extensión conserva hojas, orientación, acarreo, frontera, incidencia y memoria, aunque este bloque despliegue sólo sus coordenadas de cambio de carta. No convierte los cinco aspectos consustanciales del continuo en teorías independientes.

## 2. Contrato de entrada: N, L, D, r, A y B

### RC-001 — Prefijo ternario y longitud

Se fija una palabra posicional \(a_1\cdots a_L\), con \(a_i\in\{0,1,2\}\):

\[
N=\sum_{i=1}^{L}a_i3^{L-i}.
\]

En la carta de la unidad, \(L\in\mathbb N\) y \(0\le N<3^L\). Si \(L=0\), la palabra vacía tiene \(N=0\). La pareja \((N,L)\), no sólo N, representa el prefijo: los ceros iniciales son parte de la profundidad.

Los trits topológicos orientados y los dígitos posicionales tienen tipos distintos. El ejecutable de ensayo utiliza la carta \(0\mapsto0,+1\mapsto1,-1\mapsto2\). Es la reducción representativa en \(\mathbb F_3\), no una suma ternaria balanceada que permita omitir acarreos. Se conserva la carta utilizada.

### RC-002 — Prefijo decimal por tríadas

Para \(\delta_1,\ldots,\delta_r\in\{0,\ldots,999\}\),

\[
D=\sum_{j=1}^{r}\delta_j1000^{r-j}.
\]

En la carta de la unidad, \(0\le D<1000^r\); si \(r=0\), \(D=0\). La pareja \((D,r)\) conserva bloques iniciales nulos: \(D=7,r=1\) y \(D=7,r=2\) representan extremos distintos.

Aquí r es número de tríadas, no el residuo de una división ni un radio. A es residuo de conversión, no el ángulo homónimo. B es el segundo residuo de extremo, no el bloque visible conjunto.

### RC-003 — Cilindros semiabiertos

\[
C_3(N,L)=
\left[\frac N{3^L},\frac{N+1}{3^L}\right),\qquad
C_{1000}(D,r)=
\left[\frac D{1000^r},\frac{D+1}{1000^r}\right).
\]

Sus anchuras son \(3^{-L}\) y \(1000^{-r}\). Los extremos son racionales de carta: no se presupone un real externo para construirlos.

### RC-004 — Residuos de los extremos

Con denominador común positivo,

\[
\frac N{3^L}-\frac D{1000^r}
=\frac{1000^rN-D3^L}{3^L1000^r}.
\]

Por tanto,

\[
\boxed{A=1000^rN-D3^L},\qquad
\boxed{B=(N+1)1000^r-D3^L=A+1000^r}.
\]

A compara los extremos inferiores; B compara el extremo superior ternario con el inferior decimal. Ninguno sustituye toda la memoria de la historia.

### RC-005 — Inicialización vacía o en un prefijo generado

La inicialización de carta es

\[
(N,L,D,r,A,B)=(0,0,0,0,0,1).
\]

Ambos cilindros son \([0,1)\). Este estado inicial del convertidor no reemplaza las semillas APP, cursores u orientación que alimentan al productor de bloques.

También puede iniciarse en una profundidad ya generada. Se reciben \((N,L,D,r)\), se recalculan A,B y se comprueba el contrato de intervalo aplicable. No se añade un prefijo decimal conocido como selector de una constante.

## 3. El cociente contribuye al módulo

### RC-006 — División por 1000

Si \(n=1000q+s\), \(0\le s<1000\),

\[
n-q-s=(1000-1)q=999q=9\cdot111q.
\]

Por tanto \(n\equiv q+s\pmod9\), y también módulo tres. El cociente se suma al residuo porque \(1000\equiv1\).

Como control, 0 y 1000 tienen igual residuo módulo 1000, pero diferentes clases módulo nueve y tres. Conservar sólo ese residuo pierde información para reconstruir la clase del entero.

## 4. Seis símbolos adicionales

### RC-007 — Índice del sexteto

Para \((b_1,\ldots,b_6)\in\{0,1,2\}^6\),

\[
\nu=\sum_{j=1}^6b_j3^{6-j},\qquad0\le\nu<3^6=729.
\]

729 procede de la capacidad de un sexteto. No afirma que las 729 palabras sean semillas del catálogo inicial de 243, ni que todas sean admisibles en cualquier estado TPK.

### RC-008 — Concatenación ternaria

Los L dígitos previos se desplazan seis posiciones:

\[
\begin{aligned}
N'
&=\sum_{i=1}^{L}a_i3^{L+6-i}
+\sum_{j=1}^{6}b_j3^{6-j}\\
&=3^6\sum_{i=1}^{L}a_i3^{L-i}+\nu\\
&=\boxed{729N+\nu},
\qquad
\boxed{L'=L+6}.
\end{aligned}
\]

La determinación del sexteto por los operadores anteriores es otra operación con su propietario; esta igualdad expresa su concatenación.

### RC-009 — Subdivisión del cilindro

\[
C_{3,\nu}=
\left[
\frac{729N+\nu}{3^{L+6}},
\frac{729N+\nu+1}{3^{L+6}}
\right).
\]

Como \(0\le\nu<729\), sus extremos están entre \(N/3^L\) y \((N+1)/3^L\). Los 729 subcilindros son consecutivos, disjuntos en la convención semiabierta y su unión es el cilindro previo. La partición posicional no realiza por sí sola el filtro de admisibilidad TPK.

### RC-010 — Prefijo decimal fijo: primera recurrencia

Si no se publica una tríada, \(D'=D,r'=r\). Entonces

\[
\begin{aligned}
A'
&=1000^rN'-D3^{L'}\\
&=1000^r(729N+\nu)-D3^{L+6}\\
&=729\,1000^rN+\nu1000^r-729D3^L\\
&=729(1000^rN-D3^L)+\nu1000^r\\
&=\boxed{729A+\nu1000^r}.
\end{aligned}
\]

Se utilizó \(3^{L+6}=3^6\,3^L=729\,3^L\). No aparece un ajuste adicional.

### RC-011 — Segundo extremo

\[
B'=A'+1000^r.
\]

El incremento es \(1000^r\), no \(729\,1000^r\), porque el nuevo numerador superior es \(N'+1\). La contracción ya está en el denominador \(3^{L+6}\).

## 5. Actualización conjunta con una tríada decimal

### RC-012 — Concatenación decimal

Si se publica \(\delta\in\{0,\ldots,999\}\),

\[
D'=1000D+\delta,\qquad r'=r+1.
\]

δ procede del lector o del predicado de publicación aplicable al estado. No se obtiene simplemente por escribir la identidad siguiente.

### RC-013 — Sustitución completa

\[
A'=1000^{r+1}(729N+\nu)-(1000D+\delta)3^{L+6}.
\]

Expandiendo ambos productos,

\[
A'=729\,1000^{r+1}N+\nu1000^{r+1}
-1000D\,729\,3^L-\delta729\,3^L.
\]

### RC-014 — Factor común: segunda recurrencia

\[
729\,1000^{r+1}N-1000D\,729\,3^L
=729000(1000^rN-D3^L).
\]

Luego

\[
\boxed{A'=729000A+\nu1000^{r+1}-729\delta3^L}.
\]

\(729000=3^6\,10^3\) expresa la composición de ambos cambios de posición. Sustituirlo por 729 elimina el avance decimal.

### RC-015 — Segundo extremo después de publicar

\[
B'=A'+1000^{r+1}.
\]

Ambos tipos de transición conservan así el mismo formato de datos.

### RC-016 — Fórmula uniforme y dato de opción

Sea \(e_{\rm pub}\in\{0,1\}\). Cuando vale cero, fijamos \(\delta=0\) sólo como notación auxiliar, no como bloque publicado. Entonces

\[
\begin{aligned}
L'&=L+6,&N'&=729N+\nu,\\
r'&=r+e_{\rm pub},&
D'&=1000^{e_{\rm pub}}D+e_{\rm pub}\delta,\\
A'&=729\,1000^{e_{\rm pub}}A+\nu1000^{r+e_{\rm pub}}
-729e_{\rm pub}\delta3^L.
\end{aligned}
\]

El registro distingue \(\bot\), «sin publicación», de \(\delta=0\), «publicación de 000». Borrar esta diferencia pierde profundidad decimal.

## 6. Intersección, inclusión y publicación única

### RC-017 — Intersección de cilindros

\([a,b)\cap[c,d)\ne\varnothing\) equivale a \(a<d\) y \(c<b\). Por tanto,

\[
\frac N{3^L}<\frac{D+1}{1000^r}\iff A<3^L,
\qquad
\frac D{1000^r}<\frac{N+1}{3^L}\iff B>0.
\]

Se obtiene

\[
\boxed{C_3(N,L)\cap C_{1000}(D,r)\ne\varnothing
\iff A<3^L\ \land\ B>0}.
\]

Las desigualdades son estrictas: el contacto por un extremo excluido no produce intersección.

### RC-018 — Inclusión completa

\(C_3(N,L)\subseteq C_{1000}(D,r)\) equivale a

\[
\frac D{1000^r}\le\frac N{3^L},
\qquad
\frac{N+1}{3^L}\le\frac{D+1}{1000^r}.
\]

Es decir,

\[
\boxed{A\ge0,\qquad B\le3^L}.
\]

Aquí compartir el extremo superior excluido sí es compatible con inclusión. Esta condición es más fuerte que la intersección.

### RC-019 — Celdas candidatas de una profundidad

Fijados \(N',L'\), sean \(T=3^{L'}\), \(S=1000^{r+1}\). Los índices de celdas decimales que intersectan el cilindro van desde

\[
j_{\min}=\left\lfloor\frac{SN'}T\right\rfloor
\]

hasta

\[
j_{\max}
=\left\lceil\frac{S(N'+1)}T\right\rceil-1
=\left\lfloor\frac{S(N'+1)-1}T\right\rfloor.
\]

La última igualdad utiliza enteros. El −1 conserva la frontera semiabierta.

### RC-020 — Publicación determinada por inclusión

Si \(j_{\min}=j_{\max}=j\), todo el cilindro está en una celda. Si además

\[
\left\lfloor j/1000\right\rfloor=D,
\]

ésta prolonga el prefijo anterior. Entonces

\[
\delta=j\bmod1000,\qquad D'=j.
\]

El criterio está implementado en el propietario Python localizado. Determina publicación de prefijos; no es la regla que produjo ν.

### RC-021 — Varias celdas candidatas

Si \(j_{\min}<j_{\max}\), la inclusión del cilindro no determina una tríada única. La implementación localizada registra \(\bot\), conserva D,r y actualiza N,L,A,B.

Otros datos de frontera del estado completo pueden intervenir mediante su lector declarado; este contrato delimita únicamente el criterio de inclusión ejecutado. No se sustituye el lector global por este subprograma.

### RC-022 — Compatibilidad global

El integral distingue:

1. la transición entera fijado un par admisible \((\nu,\delta)\);
2. la filtración conjunta por cilindros y retorno nonádico;
3. la prolongación de estado profundo, firma, hojas, orientación y registro.

La primera no consulta un valor objetivo. Tampoco demuestra por sí sola que cualquier par sea admisible en la tercera. El propietario común actualiza Hensel, palabra, cociclos, firma y sombra de Witt junto al cilindro. Sus operaciones permanecen enlazadas al árbol general.

## 7. Recuperación de prefijos y profundidad

### RC-023 — Inversa ternaria

Dado N′ y sabiendo que se añadió un sexteto,

\[
N=\lfloor N'/729\rfloor,\quad
\nu=N'\bmod729,\quad L=L'-6.
\]

La unicidad procede de \(0\le\nu<729\). Seis divisiones sucesivas por tres recuperan sus seis dígitos, incluidos los ceros iniciales.

### RC-024 — Inversa decimal

Si hubo publicación,

\[
D=\lfloor D'/1000\rfloor,\quad
\delta=D'\bmod1000,\quad r=r'-1.
\]

Si hubo \(\bot\), D y r no cambian. Sin el indicador registrado no se debe borrar una tríada que nunca se añadió.

### RC-025 — Inversa del residuo sin publicación

\[
A=\frac{A'-\nu1000^r}{729}.
\]

La divisibilidad del numerador por 729 es condición de pertenencia a la imagen de esta transición.

### RC-026 — Inversa del residuo con publicación

\[
A=\frac{A'-\nu1000^{r+1}+729\delta3^L}{729000}.
\]

Se utilizan las profundidades anteriores recuperadas en RC-023/024. La divisibilidad es exacta en la imagen.

### RC-027 — Conmutación con truncación registrada

Aplicar las divisiones anteriores y borrar la última entrada devuelve exactamente los prefijos y profundidades previos. La iteración recupera la secuencia de coordenadas del cambio de carta.

La tupla \((N,L,D,r,A,B)\) no es todo el estado enriquecido. Orientación, hojas, firma e incidencia se recuperan por sus actualizaciones y registros propietarios. El integral conserva explícitamente las sucesiones completas y las trunca conjuntamente.

### RC-028 — Profundidad indispensable

\((N,L)=(1,6)\) y \((1,12)\) tienen igual numerador pero extremos \(1/729\) y \(1/531441\), distintos. Un bloque decimal inicial 000 cambia r sin cambiar D.

Además, N=D=0 da A=0 a cualquier profundidad. El residuo aislado no recupera profundidad ni historia completa.

## 8. Ejemplo racional exacto sin constante objetivo

### RC-029 — Datos y estatuto del ejemplo

Se eligen explícitamente índices de sexteto

\[
(\nu_1,\nu_2,\nu_3)=(100,200,300).
\]

Es un ejemplo posicional, no una afirmación de que la palabra sea seleccionada por un productor de constantes o constituya una trayectoria global TPK. Los trits de carta y todos los campos se conservan en el JSON.

El racional final se obtiene después de concatenar:

\[
x_{\rm ej}=\frac{53\,290\,200}{3^{18}}
=\frac{17\,763\,400}{129\,140\,163}.
\]

No se introduce como objetivo del convertidor; describe el extremo construido por el ejemplo.

### RC-030 — Primer sexteto: espera de publicación

\[
N_1=100,\quad L_1=6,\quad A_1=100,\quad B_1=101.
\]

Para el cilindro \([100/729,101/729)\),

\[
j_{\min}=\lfloor100000/729\rfloor=137,\qquad
j_{\max}=\lfloor(101000-1)/729\rfloor=138.
\]

Hay dos celdas candidatas. Se conserva \(D_1=0,r_1=0\), con \(\bot\).

### RC-031 — Segundo sexteto: tríada 137

\[
N_2=729\cdot100+200=73\,100,\quad L_2=12.
\]

Ambos índices de celda son 137. Se publica \(\delta_2=137\), \(D_2=137,r_2=1\).

\[
\begin{aligned}
A_2
&=729000\cdot100+200\cdot1000-729\cdot137\cdot729\\
&=72\,900\,000+200\,000-72\,807\,417\\
&=292\,583\\
&=1000\cdot73\,100-137\cdot531\,441.
\end{aligned}
\]

\(B_2=293583\). Como \(0\le A_2\) y \(B_2\le531441\), el cilindro completo está en \([137/1000,138/1000)\).

### RC-032 — Tercer sexteto: tríada 551

\[
N_3=729\cdot73\,100+300=53\,290\,200,\quad L_3=18.
\]

La única celda decimal de profundidad dos tiene índice 137551 y prolonga 137:

\[
\delta_3=551,\quad D_3=137551,\quad r_3=2.
\]

\[
\begin{aligned}
A_3
&=729000\cdot292583+300\cdot1000^2
-729\cdot551\cdot3^{12}\\
&=124\,317\,561\\
&=10^6\cdot53\,290\,200-137551\cdot387\,420\,489.
\end{aligned}
\]

\(B_3=125317561<3^{18}=387420489\), con \(A_3\ge0\); se prueba la inclusión decimal.

### RC-033 — Recuperación de la etapa anterior

\[
53\,290\,200=729\cdot73\,100+300,\qquad
137551=1000\cdot137+551.
\]

Se recuperan \(N_2,\nu_3,D_2,\delta_3,L_2=12,r_2=1\). La fórmula inversa devuelve \(A_2=292583\). Reiterar conserva la marca \(\bot\) inicial.

| Etapa | ν | L | N | Publicación | r | D | A | B |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Inicial | — | 0 | 0 | — | 0 | 0 | 0 | 1 |
| 1 | 100 | 6 | 100 | ⊥ | 0 | 0 | 100 | 101 |
| 2 | 200 | 12 | 73100 | 137 | 1 | 137 | 292583 | 293583 |
| 3 | 300 | 18 | 53290200 | 551 | 2 | 137551 | 124317561 | 125317561 |

## 9. Frontera y límite

### RC-034 — Frontera decimal exacta

El criterio de inclusión es más estrecho que una decisión simbólica completa. Como control racional del criterio, la palabra ternaria infinita de dígitos 1 tiene

\[
N_L=\frac{3^L-1}{2},\quad
C_3(N_L,L)=
\left[\frac12-\frac1{2\cdot3^L},
      \frac12+\frac1{2\cdot3^L}\right).
\]

Su límite es \(1/2\), frontera entre las celdas 499 y 500 de la primera tríada. Para \(L=6,12,\ldots\), el cilindro tiene puntos a ambos lados:

\[
j_{\min}=499,\qquad j_{\max}=500.
\]

Ningún prefijo finito satisface la inclusión en una sola celda. El script comprueba doce etapas y la fórmula prueba la afirmación para toda longitud múltiplo de seis.

Esto no refuta el lector TPK ni declara ausente su dato de frontera. Delimita el subprograma localizado: para decidir una frontera exacta necesita el testigo adicional o la convención canónica aplicable a su interfaz. El residuo transporta la ambigüedad; una identidad algebraica no la resuelve.

### RC-035 — Profundidad fija fuera de la frontera

Si una historia compatible tiene límite x estrictamente interior a una celda decimal de profundidad r, su distancia a los dos extremos es positiva. Cuando el diámetro del cilindro ternario que contiene x es menor que esa distancia, todo el cilindro está en esa celda.

El argumento explica la determinación eventual del prefijo fuera de las fronteras. Usa contracción y pertenencia, no sólo la identidad del residuo.

### RC-036 — Cilindros y clausuras

La convención semiabierta separa las celdas finitas. Para el límite se conservan las condiciones de frontera y, cuando corresponde, las clausuras.

Una sucesión de cilindros con extremo superior 1 puede tener clausuras cuya intersección sea {1}, aunque 1 no pertenezca a ninguno de los cilindros abiertos por ese extremo. No se identifica automáticamente la intersección de clausuras con pertenencia al mismo representante semiabierto. El extremo de unidad conserva su carta o convención.

### RC-037 — Tres alcances distintos

- **Identidad algebraica:** las fórmulas de A valen por sustitución para los enteros y profundidades declarados.
- **Publicación local:** un predicado de intervalo o un lector con datos de frontera decide δ o \(\bot\). El ejecutable localizado usa inclusión.
- **Compatibilidad global:** la extensión conserva Hensel, firmas conjuntas, incidencia, orientación, hojas, reloj y memoria. Sus propietarios pertenecen al árbol general.

Aquí queda desarrollado el álgebra y el contrato del convertidor focal, no una formalización nueva de todos los operadores del continuo.

## 10. Implementaciones y comprobación

### RC-038 — Comprobadores previos

Se localizaron y leyeron dos bloques:

1. El comprobador de representaciones modulares recorre longitudes 6/12, numeradores de borde, profundidades decimales, \(\nu\in\{0,1,728\}\) y dígitos de ensayo. Su comentario distingue álgebra de admisibilidad.
2. El comprobador de memoria de una entrega posterior ejecuta las recurrencias en *test_states*, junto a controles de Hensel y calendario ajenos al presente alcance.

No se volvieron a ejecutar esos programas completos. Su presencia no equivale a una formalización Lean de las identidades.

### RC-039 — Convertidor material

*Cylinder.append_trit* inicializa \(N=L=D=r=A=0,B=1\), acumula seis trits, calcula ν, aplica la recurrencia sin publicación y determina candidatos por división entera. Si hay una celda única que prolonga D, publica δ y usa la segunda recurrencia; si no, conserva D,r.

El propietario declara su instancia prospectiva como FORMALIZACION_NUEVA y la distingue de la sección terminal histórica. Se aprovecha el convertidor sin promover todo el programa a identificación demostrada con cualquier trayectoria.

### RC-040 — Comprobación focal REV03

El nuevo script:

1. prueba las dos identidades e inversas en 17.496 casos enteros;
2. comprueba 225 casos de intersección, inclusión y candidatos con fracciones exactas;
3. extrae por AST sólo las definiciones *require*, *encode_trits* y *Cylinder* del propietario, sin importar el programa completo;
4. reproduce el ejemplo con todas sus coordenadas;
5. comprueba la frontera \(1/2\) durante doce sextetos 364;
6. usa un control negativo: cambiar 729000 por 729 produce −72534517 en vez de 292583 en la segunda etapa.

Resultado: PASS_FOCAL_REFINAMIENTO_CAMBIO_CARTA.

El PASS se limita a esos controles. La prueba universal está en RC-008–016; el ensayo finito no la sustituye. No se produjo una nueva formalización Lean ni se certificó el selector de constantes.

## 11. Lectura y conservación

Se leyó completo el archivo del artículo X sobre geometría modular; del integral, el propietario de sistemas inversos en líneas 1–150, arquitectura TPK en 560–705 y el estado/lector común en 515–695. De los programas se leyeron los bloques de recurrencia y convertidor citados. Se reutilizaron CG-010 y las concordancias LRG; no se declara releído el integral ni toda la biblioteca Python/Lean.

REV01, REV02, los PDF y sus fuentes permanecen intactos. Este desarrollo se enlaza al productor de sextetos y a la conservación conjunta de campos, manteniendo contratos distintos. Su continuación pertinente es desplegar el lector global de frontera en su propietario vigente, sin volver a presentar estas identidades recuperadas como resultados nuevos.

## 12. Localizadores materiales directos

- [X sucesor: módulos y recurrencias](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/geometria_modular.tex:99>).
- [Integral: carta de estado](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/14_numero_heisenberg_y_d108.tex:20>); [intersección y transición](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/14_numero_heisenberg_y_d108.tex:73>).
- [Integral: estado enriquecido](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/20_arquitectura_operatoria_tpk_actualizada.tex:589>); [operador de cilindros](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/20_arquitectura_operatoria_tpk_actualizada.tex:647>).
- [Integral: lector compacto](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:515>); [Hensel e índice](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:572>); [opción, recurrencias y registro](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:612>); [truncación completa](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex:680>).
- [Comprobador previo de representaciones](</Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_TRABAJO_STIX_20260906/REVISION_CONCEPTUAL_20260907/verificar_representaciones_modulares.py:110>).
- [Comprobador de memoria de entrega](</Users/ruben/Documents/New project/output/REPARACION_ENTREGA_MULTIPLATAFORMA_20260916/ENTREGA/ES/PAQUETES/02_BARBERO_CKM_CONSTANTES_ES/payload/source_es/suplementos/memoria/paquete_I/python/verificar_memoria.py:276>).
- [Convertidor: alcance](</Users/ruben/Documents/New project/output/INVESTIGACION_XTERM_S12_TARGET_FREE_20260914/construir_libro_pleno.py:1>); [carta de trits](</Users/ruben/Documents/New project/output/INVESTIGACION_XTERM_S12_TARGET_FREE_20260914/construir_libro_pleno.py:65>); [inicialización Cylinder](</Users/ruben/Documents/New project/output/INVESTIGACION_XTERM_S12_TARGET_FREE_20260914/construir_libro_pleno.py:117>); [candidatos y publicación](</Users/ruben/Documents/New project/output/INVESTIGACION_XTERM_S12_TARGET_FREE_20260914/construir_libro_pleno.py:148>).
- [Script focal](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/22_verificar_refinamiento_cambio_carta.py:1>).
- [Resultados exactos](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/22_RESULTADOS_REFINAMIENTO_CAMBIO_CARTA.json:1>).
- [CG-010](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/03_COINDUCCION_GEOMETRIAS.md:227>).
- [LRG: prolongación y subcilindros](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV02_ARBOL/12_LECTURA_RAPIDA_Y_GENERACION.md:249>).
- [EDC: registro conjunto](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV02_ARBOL/13_ESTRUCTURA_DISCRETA_ARBOL.md:1>).

