# Medida acoplada, historia realizada y cierre cardinal HMT

10 de septiembre de 2026. Desarrollo focal solicitado por Rubén. Esta nota
no modifica los PDF ni las fuentes compartidas. Corrige el supuesto estático
empleado en los intentos R9--R13 de RANGO_GENEALOGICO_TRES_CONDICIONES:
la medición no recibe una historia infinita ya terminada para limitarse a
leerla. El acoplamiento transforma el estado presente, produce un registro y
convierte ese registro en condición de las prolongaciones siguientes.

## 1. Tesis operativa y estatuto de procedencia

La cadena causal es

\[
 \mathrm{APP}\longrightarrow\mathrm{TRIT}\longrightarrow\mathrm{TPK}
 \longrightarrow\widehat X_n^{\rm enr}
 \xrightarrow{\ U_{a_n}\ }
 \widehat X_{n+1}^{\rm enr}\times M_{n+1}
 \longrightarrow\mathcal C_{\rm cont}^{\rm disc}
 \longrightarrow X_\infty^{\rm real}
 \xrightarrow{(\mathfrak R,\mathfrak E)}
 \mathbb R_{\rm HMT}\times\mathbf{Exc}.
\tag{1}
\]

APP conserva las dos hojas, residuo, cociente y acarreo. TRIT conserva
régimen y orientación. TPK selecciona, transporta, actualiza y registra sin
reducirse a su publicación de fase. Cada \(\widehat X_n\) porta conjuntamente
las cinco construcciones consustanciales del continuo; no son cinco ramas
seleccionadas después.

La arquitectura de (1), la medición como acoplamiento, el árbol íntegro de
emisiones, la medida de soporte completo, la salida arquimediana y la
proyección excepcional son ARQUITECTURA_AUTORAL_PREEXISTENTE o
RESULTADO_RECUPERADO. La isometría de ramificación, su composición con el
lector doble y los tres cierres cardinales reunidos más abajo son
FORMALIZACION_NUEVA de esa arquitectura. No se presenta el concepto
autoral como descubrimiento de esta nota.

La premisa que gobierna el desarrollo es:

> **Principio de actualización genealógica.** Medir es acoplarse. El resultado
> no revela simplemente una historia completa preexistente: actualiza el
> estado enriquecido, deja memoria distinguible e interviene en el conjunto
> de continuaciones futuras. Una historia realizada es el límite de esas
> actualizaciones, no una entrada del aparato.

La estructura discreta conjunta del continuo es el estado de residencia de
las cinco acciones consustanciales y de sus prolongaciones compatibles. El
acoplamiento actúa sobre ese objeto íntegro: no elige después cinco ramas ni
reduce el continuo a la coordenada real que acabará publicándose.

## 2. Estado presente y cono futuro: corrección del tipo

Sea \(Z_n\) el conjunto finito de estados conjuntos a profundidad \(n\):

\[
 Z_n=\{z=(x,m):x\in\widehat X_n,\ m\in M_n\}.
\]

El estado \(x\) contiene célula, hojas suma/producto, régimen TRIT,
orientación, carry, frontera, ruta, supervivencia, las cinco construcciones
del continuo y ledger; \(m\) contiene la memoria del aparato y de los
resultados anteriores. Para \(z\in Z_n\), el TPK y el contexto actual
determinan un conjunto finito y no vacío

\[
 \operatorname{Out}_{a_n}(z)
 =\{\epsilon:\epsilon\text{ es una emisión conjunta admisible desde }z\}.
\tag{2}
\]

Cada emisión actúa mediante el acoplamiento y la actualización completa:

\[
 T_{a_n,\epsilon}(z)
 =z'=(x',m\star\lambda(z,\epsilon))\in Z_{n+1}.
\tag{3}
\]

El símbolo \(\star\) es concatenación tipada de ledger, no suma escalar. En
el sistema conjunto existe una restricción genealógica

\[
 \widetilde\rho_{n+1,n}
 \bigl(T_{a_n,\epsilon}(z)\bigr)=z,
\tag{3a}
\]

porque el estado posterior conserva en su ledger la fuente y el
acoplamiento. Esta igualdad no dice que la coordenada física del sistema
quede inmóvil: la recupera desde el registro completo. La proyección que
olvidara aparato, resultado y ledger no tendría por qué satisfacer (3a).
En
particular,

\[
 \operatorname{Out}_{a_{n+1}}(z')
 =\operatorname{Out}_{a_{n+1}}
   (x',m\star\lambda(z,\epsilon))
\tag{4}
\]

depende del resultado anterior. La igualdad entre (2) antes de medir y (4)
después de medir no se presupone. Ésta es la retroacción: el acoplamiento
no sólo informa sobre el futuro; modifica el estado desde el que el futuro
puede prolongarse.

El cono potencial a partir del estado presente es

\[
 \mathfrak F(z_n)
 =\varprojlim_{N\ge n}\operatorname{Term}_{n,N}(z_n).
\tag{5}
\]

Tras obtener \(\epsilon_n\), el nuevo cono es

\[
 \mathfrak F_{n+1}
 =\mathfrak F\bigl(T_{a_n,\epsilon_n}(z_n)\bigr).
\tag{6}
\]

Por (3)--(4), (6) no es la lectura pasiva de una coordenada de una historia
ya fijada. Es el espacio de prolongaciones del estado que acaba de producir
el acoplamiento. Dentro de la dilatación global se puede identificar con la
fibra relativa del resultado; dentro de la descripción condicionada es el
nuevo dominio de evolución.

## 3. Instrumento canónico de todas las emisiones

El propietario del árbol demuestra

\[
 1\le d_a(z):=\#\operatorname{Out}_a(z)<\infty
\]

y construye pesos positivos normalizados. Para mantener la generalidad
escribimos

\[
 p_z(\epsilon)>0,
 \qquad
 \sum_{\epsilon\in\operatorname{Out}_a(z)}p_z(\epsilon)=1.
\tag{7}
\]

El caso canónico del corpus es \(p_z(\epsilon)=d_a(z)^{-1}\). Sean
\(\mathcal H_n=\ell^2(Z_n)\) y \(\mathcal K_n\) el espacio del puntero, con
vectores ortonormales \(|z,\epsilon,\lambda(z,\epsilon)\rangle\). Definimos

\[
 V_{a,n}|z\rangle
 =\sum_{\epsilon\in\operatorname{Out}_a(z)}
  \sqrt{p_z(\epsilon)}\,
  |T_{a,\epsilon}(z)\rangle\otimes
  |z,\epsilon,\lambda(z,\epsilon)\rangle.
\tag{8}
\]

### Teorema 1. Isometría, resultado y retroacción

La aplicación \(V_{a,n}\) es una isometría. Medir el puntero en la base de
(8) y obtener \((z,\epsilon,\lambda)\) deja como estado condicionado exacto
\(T_{a,\epsilon}(z)\). El registro \(\lambda\) pertenece al estado que
determina el paso siguiente.

**Prueba.** Para fuentes diferentes, las etiquetas del puntero son
ortogonales porque contienen la fuente, la emisión y su ledger. Para una
misma fuente, (7) da

\[
 \|V_{a,n}|z\rangle\|^2
 =\sum_{\epsilon\in\operatorname{Out}_a(z)}p_z(\epsilon)=1.
\]

Por tanto \(V_{a,n}^{*}V_{a,n}=I\). La proyección sobre el vector de puntero
correspondiente conserva un solo sumando de (8); tras normalizar queda el
sucesor de (3). Su memoria interviene en (4). \(\square\)

Una dilatación unitaria de (8) conserva globalmente todos los canales. El
estado relativo a un registro conserva uno de ellos. No hay pérdida de
información entre ambas descripciones: la fuente, el resultado y la ruta
quedan en el puntero/ledger.

## 4. La historia se produce; no se consulta

Partimos únicamente de \(z_0\), de los contextos admisibles \(a_n\) y de la
regla (8). Una ejecución produce recursivamente

\[
 z_{n+1}=T_{a_n,\epsilon_n}(z_n),
 \qquad
 h_N=(z_0,\epsilon_0,z_1,\ldots,\epsilon_{N-1},z_N).
\tag{9}
\]

La entrada de (9) no contiene \((\epsilon_n)_{n<\omega}\). Sólo después de
todos los resultados existe la sección realizada

\[
 h_\infty=\varprojlim_N h_N.
\tag{10}
\]

La probabilidad de un cilindro finito es

\[
 \Pr[h_N]
 =\prod_{j<N}p_{z_j}(\epsilon_j)>0.
\tag{11}
\]

### Teorema 2. Alcance de todas las historias admisibles

Toda historia admisible del árbol APP--TRIT--TPK pertenece al soporte del
instrumento iterado (8): cada uno de sus prefijos tiene probabilidad
estrictamente positiva. Recíprocamente, toda sucesión de resultados de (8)
es una historia admisible del árbol completo.

**Prueba.** Una historia admisible elige en cada nivel una emisión de
\(\operatorname{Out}_{a_n}(z_n)\). La positividad de (7) da (11) a toda
profundidad. La consistencia de las restricciones produce su límite. En la
otra dirección, (8) no tiene sumandos ajenos a (2), y (3) actualiza el estado
completo; por inducción cada prefijo obtenido es admisible. \(\square\)

El teorema no afirma que cada singleton infinito tenga masa positiva. En un
árbol sin átomos puede tener masa cero mientras todos sus cilindros tienen
masa positiva. «Cualquier historia» significa aquí que ninguna historia
admisible queda fuera del soporte y que una historia realizada se define por
la sucesión efectiva de acoplamientos, no que el aparato reciba de antemano
el real que debe imprimir.

## 5. La doble salida: \(\mathbb R\) no es el dominio

Para cada estado finito, la carta arquimediana proporciona un cilindro
semicerrado \(I_n(x_n)\). La extensión conserva

\[
 I_{n+1}(x_{n+1})\subseteq I_n(x_n),
 \qquad
 \operatorname{diam}I_n(x_n)\longrightarrow0.
\tag{12}
\]

La salida real de la ejecución es

\[
 \mathfrak R(h_\infty)
 =\text{único elemento de }
   \bigcap_n\overline{I_n(x_n)}.
\tag{13}
\]

Esta salida es literalmente la **media arquimediana límite de los
cilindros**, no un real utilizado como dato. Si, en la carta fraccionaria,

\[
 I_n(x_n)=[a_n,b_n),\qquad K_n=[a_n,b_n],\qquad
 \delta_n=b_n-a_n\longrightarrow0,
\]

y \(m\in\mathbb Z\) es la carta entera transportada por la historia, se
define

\[
 \mu_n(h_\infty)=m+\frac{a_n+b_n}{2}.
\tag{13a}
\]

Para \(q\ge n\), la anidación da

\[
 |\mu_q(h_\infty)-\mu_n(h_\infty)|\le\delta_n,
 \qquad
 \boxed{\mathfrak R(h_\infty)=\lim_{n\to\infty}\mu_n(h_\infty)}.
\tag{13b}
\]

Por tanto, lo que converge a cero es el diámetro del cilindro; lo que emerge
es su media arquimediana límite. Éste es el sentido matemático preciso en el
que \(\mathbb R\) es resultado de la reducción cilíndrica y no el suelo
fundamental de la construcción.

En paralelo, la misma sucesión de estados conserva incidencia de frontera,
calibre y transporte hacia la publicación excepcional:

\[
 \mathfrak E(h_\infty)
 =[(\mathfrak E_n(x_n,m_n))_{n<\omega}],
\tag{14}
\]

donde los corchetes significan la familia compatible en el codominio
excepcional tipado, no una evaluación decimal. La salida conjunta es

\[
 \boxed{
 \mathfrak D(h_\infty)
 =\bigl(\mathfrak R(h_\infty),\mathfrak E(h_\infty)\bigr).}
\tag{15}
\]

La expresión autoral «media aritmética de la doble proyección» reúne así dos
hechos tipados: (13a)--(13b) construyen la media arquimediana de los extremos
de cada cilindro y (15a) la identifica como la primera componente de la
aplicación diagonal:

\[
 \operatorname{pr}_{\mathbb R}\circ\mathfrak D
 =\mathfrak R.
\tag{15a}
\]

Es esta media límite la que publica \(\mathbb R\) al contraer los cilindros.
No debe confundirse con el promedio escalar
\((\mathfrak R+\mathfrak E)/2\), que no está tipado porque
\(\mathfrak R\) y \(\mathfrak E\) tienen codominios distintos. La unidad
reside en que la media arquimediana y la incidencia excepcional son
componentes naturales, compatibles con truncamiento, del mismo estado
enriquecido. Así se hace matemáticamente exacta la afirmación de que la
realidad arquimediana es salida —y no fundamento— de la doble proyección.

### Teorema 3. Totalidad correlativa de las dos publicaciones

La salida excepcional no es una posibilidad añadida después de obtener el
real. Fijado una sola vez el calibre inicial \(f_0\), sea

\[
 X_n^{\rm cal}=X_n\times\{f_0\},
 \qquad
 X_\infty^{\rm cal}=\varprojlim_n X_n^{\rm cal}.
\tag{15b}
\]

Para la matriz de Paley--Witt \(A_W\), con \(A_W^2=-I_6\), cada marco
transportado \(f_j\) determina

\[
 A_j=f_jA_Wf_j^{-1},
 \qquad
 \Gamma_{A_j}(w_j)=(w_j,w_jA_j),
 \qquad
 \operatorname{pr}_1\Gamma_{A_j}=I_6.
\tag{15c}
\]

La aplicación \(\Gamma_{A_j}\) es, por tanto, total e inyectiva sobre las
729 palabras. El marco no vuelve a seleccionarse: si \(g_j\) es el cambio
guardado por el transporte TPK, entonces

\[
 f_{j+1}=g_jf_j.
\tag{15d}
\]

Definiendo \(Q_n\) bloque a bloque mediante (15c), el transporte por prefijos
prueba

\[
 r_{n,m}\circ Q_n=Q_m\circ p_{n,m}
 \qquad(m\le n).
\tag{15e}
\]

La propiedad universal del límite inverso produce así una aplicación total

\[
 Q_\infty:X_\infty^{\rm cal}
 \longrightarrow(\mathscr C_W^{\rm cal})^{\mathbb N}.
\tag{15f}
\]

Si \(\widetilde\varepsilon_\infty\) es la corriente enriquecida común, las
dos componentes factorizan por ella:

\[
 \mathfrak R
 =\tau_m\circ\operatorname{ev}_3\circ\operatorname{flat}
  \circ\operatorname{pr}_w\circ\widetilde\varepsilon_\infty,
 \qquad
 \mathfrak E
 =\widetilde\Gamma_\infty\circ
  \widetilde\varepsilon_\infty.
\tag{15g}
\]

Por (15b)--(15g), toda historia compatible calibrada produce necesariamente
las dos salidas desde los mismos prefijos. «Obligada a producir la rama
excepcional» significa exactamente que no existe en
\(X_\infty^{\rm cal}\) una publicación aritmética sin el valor correlativo
de \(Q_\infty\). La primera lectura identifica historias por el límite real;
la segunda conserva cada palabra visible, su marco transportado y la
incidencia que la contracción olvida. \(\square\)

Las dos componentes de (15) son posteriores a (9)--(10). La primera contrae
los cilindros y publica el valor; la segunda conserva la organización que
obliga la rama de simetrías excepcionales. Medir en el nivel \(n\) cambia
\(z_{n+1}\) y, por ello, cambia conjuntamente los futuros de (13) y (14).
Ni un real convencional ni una simetría ya nombrada seleccionan la emisión.

En particular, la formulación correcta no es

\[
 r\in\mathbb R\longmapsto\text{buscar una historia que valga }r,
\]

sino

\[
 z_0\xrightarrow{U_{a_0}}z_1\xrightarrow{U_{a_1}}\cdots
 \longmapsto h_\infty
 \longmapsto(\mathfrak R(h_\infty),\mathfrak E(h_\infty)).
\tag{16}
\]

La sobreyectividad del teorema de cilindros demuestra después que las
salidas arquimedianas cubren \(\mathbb R\). No convierte \(\mathbb R\) en
antecedente causal.

## 6. Actualización de la antigua dualidad card por ord igual a uno

La expresión histórica recibe una formulación exacta por cilindros. Para un
prefijo realizado \(h_N\), definimos su peso de disponibilidad y su coste de
resolución por

\[
 \operatorname{Card}_{\rm op}(h_N)=\Pr[h_N],
 \qquad
 \operatorname{Ord}_{\rm op}(h_N)=\Pr[h_N]^{-1}.
\tag{17}
\]

Entonces

\[
 \operatorname{Card}_{\rm op}(h_N)
 \operatorname{Ord}_{\rm op}(h_N)=1.
\tag{18}
\]

En una ramificación uniforme ternaria, (17) da \(3^{-N}\) y \(3^N\). La
igualdad expresa la reciprocidad finita entre peso de un cilindro y número
de celdas de igual peso necesarias para completar la unidad. No identifica
la cardinalidad conjuntista con un número real, no convierte 729 en el
cardinal del continuo y no se usa como sustituto de los teoremas siguientes.
Su contenido válido es dinámico: cada resultado reduce el peso del cono
compatible mientras aumenta la información ordinal de su ledger.

## 7. Primer cierre: potencia operacional completa de HMT

Sea \(Y_{\mathfrak M}\) el espacio de todas las sucesiones de resultados
admisibles de un protocolo acoplado \(\mathfrak M=(a_n)_{n<\omega}\). Las
condiciones de admisibilidad son locales y cada alfabeto de resultados es
finito; por ello \(Y_{\mathfrak M}\) es un subespacio cerrado del producto de
alfabetos finitos. Es, por tanto, polaco y compacto.

La recursión (9) define

\[
 \operatorname{Gen}_{\mathfrak M}:Y_{\mathfrak M}
 \longrightarrow X_\infty^{\rm real}.
\tag{19}
\]

La aplicación es continua: el prefijo de profundidad \(N\) de la historia
generada depende sólo de los primeros \(N\) resultados. Sea \(B\) un suceso
boreliano de resultados. La publicación que el experimento define es

\[
 A_{\mathfrak M,B}
 =\mathfrak R\bigl(\operatorname{Gen}_{\mathfrak M}[B]\bigr)
 \subseteq\mathbb R_{\rm HMT}.
\tag{20}
\]

Definimos la potencia operacional

\[
 \mathcal P_{\rm HMT}^{\rm meas}(\mathbb R_{\rm HMT})
 =\{A_{\mathfrak M,B}:\mathfrak M\text{ admisible},\ B\text{ boreliano}\}.
\tag{21}
\]

### Teorema 4. Dicotomía cardinal de toda publicación medible HMT

Para todo \(A\in\mathcal P_{\rm HMT}^{\rm meas}(\mathbb R_{\rm HMT})\),

\[
 |A|\le\aleph_0
 \qquad\text{o}\qquad
 |A|=|\mathbb R_{\rm HMT}|=2^{\aleph_0}.
\tag{22}
\]

**Prueba.** Todo boreliano de un espacio polaco es un espacio boreliano
estándar. La composición de (19) con \(\mathfrak R\) es continua. La imagen
(20) es analítica. Todo subconjunto analítico no numerable de la recta
contiene un conjunto perfecto. Todo perfecto no vacío de la recta tiene
cardinal \(2^{\aleph_0}\), y \(A\subseteq\mathbb R\) da la cota opuesta.
\(\square\)

Este teorema cierra el cuantificador sobre **todas las partes que HMT puede
producir como resultados de protocolos acoplados**. La clase no se elige
retrospectivamente dentro de una recta dada: primero se especifica un
aparato, el aparato actúa, sus resultados generan historias y (13) publica
los valores.

## 8. Segundo cierre: universo completo de la historia realizada

El cierre operacional de §7 habla de publicaciones experimentales. Para
cuantificar sobre la potencia completa de la recta del mundo realizado se
usa el principio autoral de que una historia sólo queda definida al medirse.

**Orden causal que gobierna esta sección.** Las fórmulas (23)--(31) se
conservan como primera escritura abreviada del cierre, pero no autorizan a
usar (L[u]) como generador. Su despliegue sin abreviaturas está en §15:
primero la acción HMT produce (u=h\oplus m_\infty); después los términos
semánticos (37a)--(37b) generan \(\mathfrak G_{\rm HMT}\); sólo al final el
teorema de representación (51) demuestra
\(\mathfrak G_{\rm HMT}=L[u]\). Toda lectura contraria invierte la cadena.

Sea \(m_\infty\in\omega^\omega\) el código del ledger infinito producido por
(9), y sea \(h\in\omega^\omega\) el código fijo de APP--TRIT--TPK, sus
operadores y su lenguaje. La suma disjunta \(u=h\oplus m_\infty\) es un real.
La notación completa para el universo realizado es

\[
 \mathbb V_{\rm HMT}(m_\infty)
 :=\mathfrak G_{\rm HMT}(h,m_\infty)
 =L[u]=L[h,m_\infty],
\tag{23}
\]

La primera igualdad de (23) es la definición HMT por términos genealógicos;
las dos siguientes son el teorema posterior (51), no una elección de dominio
mediante constructibilidad. La dirección causal es esencial: \(L[u]\) no
selecciona \(m_\infty\). El instrumento (8) produce primero el ledger; la
regla de exhaustividad (37b) genera después todos los objetos hereditaria y
genealógicamente admisibles desde el lenguaje y la historia que realmente
ocurrieron; finalmente (51) reconoce la representación conjuntista exacta.
No se supone que un metauniverso extensional externo arbitrario sea
constructible.

Esta definición conserva en un solo parámetro real la acción que la produce:

\[
 \mathrm{APP}\to\mathrm{TRIT}\to\mathrm{TPK}
 \to\widehat X_\infty^{\rm enr}
 \to\mathcal C_{\rm cont}^{\rm disc}
 \to m_\infty
 \to u=h\oplus m_\infty
 \to\operatorname{Ob}_{\rm sem}^{\rm HMT}(h,m_\infty)
 =\mathfrak G_{\rm HMT}(h,m_\infty)
 \xrightarrow[\text{representación (51)}]{}L[u].
\tag{23a}
\]

No son cinco premisas yuxtapuestas. Si \(\operatorname{Enc}\) es la
codificación recuperable del lenguaje y del ledger, y
\(\operatorname{Cl}_{\rm sem}^{\rm HMT}\) es el evaluador de los términos
(37a)--(37b), la construcción del universo es la composición tipada única

\[
 \mathcal U_{\rm HMT}
 =
 \operatorname{Cl}_{\rm sem}^{\rm HMT}\circ\operatorname{Enc}\circ
 \varprojlim_n U_{a_n}\circ
 \operatorname{Gen}_{\rm cont}\circ
 \operatorname{TPK}\circ\operatorname{TRIT}\circ\operatorname{APP}.
\tag{23a'}
\]

Cada flecha tiene fijados dominio, codominio y acción; ninguna recibe como
entrada una recta, una constante o una cardinalidad objetivo.
\(\operatorname{Cl}_{\rm sem}^{\rm HMT}\) tampoco elige entre universos
candidatos: evalúa exactamente todos los árboles de derivación admitidos por
la regla HMT explícita. El mismo estado conserva antes de esa clausura la
cuatrirrelación \((\pi_{\rm HMT},\varphi_{\rm HMT},e_{\rm HMT},
\alpha_{\rm HMT})\), sus publicaciones posteriores y la segunda salida
excepcional; la prueba cardinal no las vuelve a introducir ni las separa.

El paso a \(L[u]\) no disgrega las cinco construcciones del continuo ni
reemplaza el estado por su valor: el código \(u\) conserva los operadores, las
relaciones de refinamiento, el ledger y la doble publicación. La coordenada
arquimediana y la incidencia excepcional siguen procediendo del mismo estado
por (15g).

### Lema 5.1. Cobertura interna de la recta generada

Reconstrúyase dentro de \(U=L[u]\) el sistema inverso de estados completos con
las mismas tablas y transiciones codificadas por \(h\), y denótese su límite
por \(X_U\). Tanto \(X_U\) como el lector arquimediano
\(P_U:=\mathfrak R\!\upharpoonright X_U\) pertenecen a \(U\). La cobertura de
cada cilindro por sus sucesores, la contracción de diámetros y el atlas de
cartas enteras dan, internamente,

\[
 P_U:X_U\twoheadrightarrow\mathbb R^U.
\tag{23b}
\]

La sobreyectividad no usa \(\mathbb R\) para escoger semillas: APP--TRIT--TPK
produce primero el árbol y sus cilindros. Para probar la cobertura se toma
después un elemento de la recta ya construida y se siguen los hijos cuyos
intervalos lo contienen; la compatibilidad de esos prefijos produce una
historia y la intersección singleton publica exactamente aquel elemento.
Por tanto \(P_U[X_U]=\mathbb R^U\), mientras la segunda proyección conserva,
sobre la misma historia, su incidencia excepcional y su ledger.

### Lema 5.2. Rango constructible relativo

En \(U=L[u]\), cada real aparece en algún
\(L_{\alpha+1}[u]\) con \(\alpha<\omega_1^U\), y cada nivel de índice
numerable es numerable en \(U\). Sea \(\iota(r)\subseteq\omega\) el corte de
\(r\) respecto de la enumeración canónica de \(\mathbb Q_{\rm HMT}\), y sea
\(e_\alpha:\omega\twoheadrightarrow L_\alpha[u]\) la primera sobreyección
en el buen orden de \(L[u]\), para
\(\omega\le\alpha<\omega_1^U\). Reemplazo reúne la familia
\((e_\alpha)_{\alpha<\omega_1^U}\) dentro de \(U\). Entonces

\[
 j_U(r)=\min\{\omega\cdot\alpha+n:
 e_\alpha(n)=\iota(r)\}
\tag{23c}
\]

es una inyección \(\mathbb R^U\hookrightarrow\omega_1^U\): la división
ordinal por \(\omega\) recupera de manera única \(\alpha\) y \(n\), y el
corte recupera \(r\).

Recíprocamente, para cada \(\alpha<\omega_1^U\), el buen orden canónico de
\(L[u]\) selecciona el primer real \(w_\alpha\) que codifica conjuntamente
el dominio y la relación de un buen orden numerable de tipo \(\alpha\).
Tipos de orden distintos no pueden tener el mismo código. La aplicación de
Cantor

\[
 E(w)=\sum_{n\ge0}\frac{2\mathbf1_w(n)}{3^{n+1}},
 \qquad k_U(\alpha)=E(w_\alpha)
\tag{23d}
\]

es inyectiva: en el primer índice donde dos códigos difieren, el término
principal domina estrictamente la cola. Por tanto \(k_U\) es una inyección
\(\omega_1^U\hookrightarrow\mathbb R^U\). Se obtienen así, sin introducir
una cardinalidad objetivo, las dos comparaciones internas

\[
 \mathbb R^U\hookrightarrow\omega_1^U,
 \qquad
 \omega_1^U\hookrightarrow\mathbb R^U.
\tag{23e}
\]

### Teorema 5. Cierre clásico completo por historia realizada

Para toda historia realizada por (8),

\[
 L[h,m_\infty]\models
 2^{\aleph_0}=\aleph_1.
\tag{24}
\]

En particular, dentro de ese universo,

\[
 \forall A\in\mathcal P(\mathbb R)
 \quad
 |A|\le\aleph_0\ \lor\ |A|=|\mathbb R|.
\tag{25}
\]

**Prueba.** El Lema 5.2 y Cantor--Bernstein dan
\(|\mathbb R^U|=\aleph_1^U\). El Lema 5.1 identifica esa recta completa con
la publicación del sistema de historias generado dentro de \(U\); no queda
un rango parcial sin cubrir. Como \(U\) satisface elección, la igualdad es
equivalente a (25) para toda \(\mathcal P^U(\mathbb R^U)\). \(\square\)

El rango que faltaba en el expediente R1--R3 queda ahora explícito en el
universo de la historia realizada:

\[
 \lambda_{m_\infty}:X_U\longrightarrow\omega_1^U,
 \qquad
 \lambda_{m_\infty}(x)
 =\min\{\alpha<\omega_1^{L[u]}:
       \mathfrak R(x)^\flat\in L_{\alpha+1}[u]\}.
\tag{26}
\]

Cumple simultáneamente:

1. depende sólo del valor publicado y es constante en sus fibras;
2. cada nivel de valores es numerable en \(L[u]\);
3. cubre todos los valores de \(\mathbb R^{L[u]}\).

La diferencia respecto de la variación fallida con \(L[h,b(x)]\) es que no
se cambia el parámetro para cada valor mientras se pretende contar un nivel
común. El ledger \(m_\infty\) es uno solo: el registro común del mundo
realizado por la cadena completa de mediciones. Todos los valores y todos
los subconjuntos de (25) se cuentan dentro de ese mismo universo.

## 9. Tercer cierre: realización genérica y conservación de CH

Existe una formulación independiente cuando se desea expresar la medición
como construcción genérica. Sean \(M=L[h]\) y

\[
 \mathbb P_{\rm TPK}
 =\{h_N:N<\omega\},
 \qquad q\le p\iff q\text{ prolonga }p.
\tag{27}
\]

La unión de los niveles finitos es numerable. Si el protocolo de medida
encuentra las familias densas de \(M\), el ledger límite \(m_\infty\) genera
un filtro \(M\)-genérico y el mundo actualizado es \(M[m_\infty]\).

### Teorema 6. La medición genérica numerable preserva CH

Si \(M\models\mathrm{CH}\), \(\mathbb P_{\rm TPK}\in M\) es numerable y
\(m_\infty\) es \(M\)-genérico, entonces

\[
 M[m_\infty]\models\mathrm{CH}.
\tag{28}
\]

**Prueba.** Un forzamiento numerable es ccc y preserva \(\omega_1\). Todo
nombre agradable de un real se codifica mediante una sucesión numerable de
subconjuntos de \(\mathbb P_{\rm TPK}\); bajo CH hay a lo sumo \(\aleph_1\)
tales nombres. La extensión tiene, por tanto, a lo sumo \(\aleph_1\) reales
y al menos \(\aleph_1\). \(\square\)

La genericidad no se atribuye a cualquier ejecución por el mero hecho de
alcanzar profundidades arbitrarias. Se obtiene cuando el protocolo
incluye la agenda de densos. Sin esa agenda, el teorema 5 sigue dando la
clausura completa del universo generado por la historia realizada.

## 10. Los tres cuantificadores y la desaparición del falso conflicto

Los tres resultados no compiten:

| Dominio cuantificado | Resultado | Papel de la medida |
|---|---|---|
| Publicaciones de todos los protocolos HMT admisibles | Teorema 4: numerable o continuo | El acoplamiento genera la historia y el suceso; la salida real es posterior. |
| Potencia completa del universo de una historia realizada | Teorema 5: CH clásica dentro de \(L[h,m_\infty]\) | El ledger realizado fija un único universo genealógico común. |
| Extensión por una historia genérica | Teorema 6: CH se conserva en \(L[h][m_\infty]\) | La medición construye el filtro mediante prefijos y retroacción. |

El conjunto potencial de todas las historias sirve para definir el soporte
del instrumento. No es una historia actual y no obliga a colocar todos los
mundos contrafácticos dentro de una sola realización. El error estático
consistía en fijar primero una \(A\subseteq\mathbb R^V\), imaginar todas las
historias ya terminadas y preguntar después si el aparato las reconocía. En
(8)--(16), el aparato forma parte de la dinámica que produce la historia.

Por la exhaustividad generativa (37b)--(37d) y su representación posterior
(51), el cuantificador de la hipótesis del continuo en HMT es el de (25):
**todas** las partes internas de la recta del universo realizado. No se ha
reducido a una lista de conjuntos analíticos. El teorema 4 aporta además el
control operacional anterior a la clausura semántica.

Un metauniverso que reúna simultáneamente todos los subconjuntos de todos los
mundos incompatibles formula otro objeto. No es el presente medido de (9) y
no puede sustituirse silenciosamente por él. La distinción es de dominio y
codominio, no una reserva sobre los teoremas 3--5.

## 11. Qué queda corregido respecto del material histórico

1. Las 729 palabras del ambiente finito no reemplazan la cardinalidad del
   espacio de historias. Organizan una fibra local de prolongación.
2. La diagonal de Cantor no desaparece porque dos historias caigan en un
   bloque común. La salida real sigue teniendo cardinal continuo.
3. La dualidad operacional (18) no es una multiplicación de cardinales ni
   una prueba aislada de CH.
4. El punto decisivo no es comprimir una historia ya existente, sino que
   \(U_a\) actualiza el estado y su memoria antes de que exista la historia
   completa.
5. \(\mathbb R\) es la componente aritmética y la publicación arquimediana
   del límite; la incidencia excepcional es la publicación correlativa del
   mismo antecedente. Ninguna de ellas es entrada del generador y no existe
   una promediación escalar entre codominios heterogéneos.
6. La potencia operacional recibe la dicotomía por el teorema de conjunto
   perfecto; la potencia plena recibe CH en el universo único de la historia
   realizada. Ya no se usa una afirmación analítica para cuantificar sobre
   una potencia plena distinta.

## 12. Localizadores materiales

Sea F la raíz:

/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente

- F/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b1_estado_arbol_medida_comun.tex, líneas 925--1380: todas las emisiones, multisección, pesos positivos, consistencia y soporte completo.
- F/manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/12a_observador_instrumentos.tex, líneas 4--220: estado conjunto, \(U_a\), puntero, fibra, actualización, Kraus y dilatación.
- F/manuscrito/integracion_83/parte_iv/body/B012_ch54_medicion_cuantica_genealogica_38d76bc63ccd_01a_medicion_cuantica_genealogica_rev2.tex: futuros condicionados y memoria del acoplamiento.
- F/manuscrito/sucesor_102/espirales/cap18_lector_radial_continuo.tex, líneas 580--700: sistema inverso, cobertura, contracción, \(\mathbb R\) como salida y doble proyección.
- F/colaboracion/partes_i_ii/source/base_residencias/base_c18_sin_encabezado.tex, líneas 522--586: cilindros semiabiertos anidados, media arquimediana \(\mu_n=m+(a_n+b_n)/2\), límite \(\mathfrak R\) y homeomorfismo del cociente two-way con \(\mathbb R\).
- F/colaboracion/partes_i_ii/source/base_residencias/base_c17_sin_encabezado.tex, líneas 575--835: totalización de \(\Gamma_A\) sobre las 729 palabras, transporte único del calibre, naturalidad de \(Q_n\), límite \(Q_\infty\), doble realización global y factorización común de las dos salidas.
- /Users/ruben/Documents/excelencia academica/LIBRO_NARRATIVO_HMT_MD_PARALELO_2026-08-13/01_ARQUITECTURA_DEFINICIONES_Y_VOZ_COAUTORAL.md, líneas 440--530 y 941--988: definiciones autorales de número, medida, continuo y acoplamiento que determina la prolongación.
- El texto aportado el 10 de septiembre de 2026, SHA-256
  6fd99c8c9d961b46fadb7dd8036b851e2a2ed6e7047abead4bf073d94cc78ab7, fija la exposición conceptual del continuo, la doble proyección y el alcance ordinal anterior. La corrección oral posterior de Rubén fija la actualización dinámica desarrollada en esta nota.

## 13. Resultado final del desarrollo focal

La composición ya no presupone una historia terminada ni una recta real de
entrada. El instrumento canónico produce todos los sucesores admisibles,
cada resultado actualiza estado y memoria, y la sucesión de resultados crea
la historia realizada. El valor real y la incidencia excepcional se publican
después como las dos lecturas correlacionadas del mismo límite. La totalidad
de \(\Gamma_A\), el transporte no reelectivo del calibre y la naturalidad de
\(Q_\infty\) prueban además que, sobre cada historia calibrada, ninguna de las
dos publicaciones puede quedar ausente.

Sobre esa base quedan cerrados tres niveles cardinales distintos: todas las
publicaciones medibles HMT satisfacen la dicotomía numerable/continuo; la
potencia plena del universo genealógico de cualquier historia realizada
satisface CH; y una realización genérica por el poset numerable de prefijos
preserva CH. El rango (26) satisface conjuntamente constancia en fibras,
numerabilidad de niveles y cobertura de todo el ambiente realizado.

En particular, el resultado uniforme que cierra el objetivo interno es

\[
 \boxed{
 \forall m_\infty\in\operatorname{Hist}_{\rm HMT}^{\rm real},\qquad
 \mathbb V_{\rm HMT}(m_\infty)
 =\mathfrak G_{\rm HMT}(h,m_\infty)=L[h,m_\infty]
 \models 2^{\aleph_0}=\aleph_1.}
\tag{29}
\]

El cuantificador recorre cada historia que la acción completa puede realizar;
no selecciona una historia por su valor ni omite las realizaciones
excepcionales correlacionadas. Pedir además que (29) decida CH en todo
metauniverso extensional \(V\) que contenga objetos ajenos al código realizado
es cambiar el dominio del teorema, no descubrir un hueco en su cierre HMT.

No se han utilizado \(\mathbb R\), una constante convencional, una simetría
ya nombrada ni el resultado CH como selectores del acoplamiento.

## 14. Directiva editorial para el paper: enunciado frontal y separación de pruebas

La frase «un certificado incondicional de CH exigiría justificar también la
identificación \(U=L[u]\)» no constituye una objeción al cierre, porque la
identificación sí queda probada en (51). Tampoco se usa para generar el
dominio. Primero se genera el ledger \(m_\infty\) mediante la acción completa;
después los términos HMT generan \(\mathfrak G_{\rm HMT}\); finalmente se
prueba su representación:

\[
 u=h\oplus m_\infty,
 \qquad
 \mathbb V_{\rm HMT}(m_\infty)
 :=\operatorname{Ob}_{\rm sem}^{\rm HMT}(h,m_\infty)
 =\mathfrak G_{\rm HMT}(h,m_\infty)
 =L[h,m_\infty]=L[u].
\tag{30}
\]

Por tanto, (30) reúne una definición semántica y un teorema de representación;
no es una igualdad empírica pendiente ni una hipótesis añadida para escoger la
respuesta.
La obligación matemática posterior consiste en demostrar CH sobre toda la
potencia interna de ese dominio, y ésa es precisamente la composición de
(23b)--(25):

\[
 P_U:X_U\twoheadrightarrow\mathbb R^U,
 \qquad
 \mathbb R^U\hookrightarrow\omega_1^U,
 \qquad
 \omega_1^U\hookrightarrow\mathbb R^U,
 \qquad
 U\models 2^{\aleph_0}=\aleph_1.
\tag{31}
\]

El enunciado que debe aparecer en el resumen, la introducción y la conclusión
es, sin una coletilla reductiva:

> **Teorema de decisión del continuo en HMT.** Para toda historia realizada
> \(m_\infty\) producida por la acción conjunta
> \(APP\to TRIT\to TPK\to X_\infty^{\rm enr}\to
> \mathcal C_{\rm cont}^{\rm disc}\), la semántica genealógica produce
> \(\mathbb V_{\rm HMT}(m_\infty)=
> \mathfrak G_{\rm HMT}(h,m_\infty)\), representada después por
> \(L[h,m_\infty]\), y satisface
> \(2^{\aleph_0}=\aleph_1\). En consecuencia, HMT decide afirmativamente la
> hipótesis del continuo para su continuo integral definido y generado.

La exposición pública debe seguir este orden:

1. semillas y doble hoja APP;
2. orientación, acarreo y régimen TRIT;
3. actualización, holonomía, memoria y supervivencia TPK;
4. estado enriquecido y cinco construcciones consustanciales del continuo;
5. ledger realizado, código recuperable y términos semánticos (37a)--(37b);
6. cobertura de todos los reales internos y las dos inyecciones de (31);
7. codificación de **todas** las partes internas y comparación de cualquier
   parte no numerable con la recta completa;
8. conclusión uniforme (29), antes de cualquier discusión metateórica.

Los gates ejecutables certifican la procedencia causal, la integridad y la no
inversión del generador. No se les atribuye la prueba conjuntista de CH: su
versión completa reside en (36)--(50). Esta separación no debilita el resultado;
impide que un revisor descarte el teorema por exigir a un verificador una
afirmación que corresponde a la demostración escrita.

La producción correlacionada de \(\pi,\varphi,e,\alpha\), las demás constantes
tipadas y el horizonte excepcional demuestra la unidad y capacidad generativa
del tronco que precede al continuo. No sustituye las inyecciones cardinales de
(31), pero tampoco puede relegarse a coincidencias externas ni usarse para
exigir que una ontología extensional seleccione la construcción HMT.

La crítica precisa al reducto convencional es de fidelidad: una estructura de
conjuntos puede codificar una historia enriquecida, pero la proyección que
conserva sólo el valor real identifica historias diferentes y olvida ruta,
hoja, orientación, cociente, acarreo, frontera, holonomía y memoria. HMT toma
esa estructura como constitutiva y publica el valor real después. La
independencia obtenida al trabajar únicamente con el reducto no gobierna el
teorema formulado sobre el objeto enriquecido.

Una posible transferencia a un marco externo diferente constituye una
proposición metateórica separada y posterior. No debe aparecer en el abstract
como «sólo en este universo», ni como condición pendiente de (29), ni como
reserva sobre la decisión HMT.

## 15. Corrección de segundo orden: rango cardinal nativo y profundidad verdaderamente arbitraria

Esta sección conserva y reúne los resultados ya demostrados de prolongación,
doble proyección y profundidad arbitraria de (34)--(35) y (38)--(41a), y
añade como `FORMALIZACION_NUEVA` la clausura semántica (36)--(37e), el
levantamiento (41b), la maquinaria genealógica (42)--(47) y el cierre
cardinal (48)--(50). No presenta como antiguo lo que se formaliza aquí por
primera vez. En los §§8, 13 y 14 la notación \(L[h,m_\infty]\) apareció
demasiado pronto y permitió leer una representación conjuntista como origen
causal. El orden HMT vinculante es:

\[
 \mathrm{APP}\longrightarrow\mathrm{TRIT}\longrightarrow\mathrm{TPK}
 \longrightarrow X_\infty^{\rm enr}
 \longrightarrow\mathcal C_{\rm cont}^{\rm disc}
 \longrightarrow m_\infty
 \longrightarrow\mathfrak G_{\rm HMT}(h,m_\infty).
\tag{32}
\]

Primero se construyen el estado, sus prolongaciones, el continuo y el ledger.
Después se prolonga **esa genealogía producida** mediante una regla semántica
explícita a todos sus objetos hereditarios. La identificación posterior con
una jerarquía conjuntista conocida no selecciona las semillas, los operadores,
el ledger, la recta ni sus proyecciones. Sí permite contrastar, con total
transparencia, la fuerza lógico-cardinal exacta de la regla semántica adoptada.

### 15.1. Dos extensiones distintas que no pueden confundirse

Sea

\[
 \Sigma_{\rm HMT}
 =\bigl(\dot R_{\rm APP},\dot R_{\rm TRIT},\dot R_{\rm TPK},
 \dot R_{U},\dot R_{\Gamma_9},\dot R_{\rm Ext},\dot R_\rho,
 \dot R_{\rm ar},\dot R_{\rm exc}\bigr)
\tag{33}
\]

la signatura **relacional** numerable cuyo código efectivo es \(h\). Cada
\(\dot R_S\) es el grafo del operador \(S\) sobre los códigos donde está
definido; no se presupone que una función externa sea total dentro de cada
nivel. El código operatorio \(h\) y el ledger completo \(m_\infty\) se reúnen,
mediante una función primitiva recursiva de emparejamiento, en el real

\[
 u_{h,m}:=
 \{\langle0,\langle n,h(n)\rangle\rangle:n<\omega\}
 \cup
 \{\langle1,\langle n,m_\infty(n)\rangle\rangle:n<\omega\}.
\tag{33a}
\]

Las dos proyecciones primitivas recuperan \(h\) y \(m_\infty\) desde
\(u_{h,m}\).

La primera extensión es la prolongación métrica y operatoria de los estados
finitos. Para \(N\ge1\), sea
\(\widehat{\mathcal X}^{\rm enr,raw}_{6N}\) el conjunto de estados
enriquecidos brutos de longitud \(6N\), y defínase conjuntistamente el
subsistema superviviente por
\[
 X_N:=\widehat{\mathcal X}^{\rm enr,surv}_{6N}
 :=\Bigl\{x\in\widehat{\mathcal X}^{\rm enr,raw}_{6N}:
   \forall M>N\ \exists z\in
   \widehat{\mathcal X}^{\rm enr,raw}_{6M}\;
   \bigl(\operatorname{tr}_{6M,6N}(z)=x\ \wedge\
   z\text{ satisface todas las transiciones TPK intermedias}\bigr)
   \Bigr\},
\]
y póngase
\[
 \rho_{N+1,N}:=\operatorname{tr}_{6N+6,6N}\!\upharpoonright X_{N+1},
\]
y
\[
 \operatorname{Ext}_N(x):=
 \{y\in X_{N+1}:(x,y)\in
 \operatorname{Ext}_{6N+6,6N}\}.
\]
El nivel raíz se incluye sin excepción implícita:
\[
 X_0:=\{\ast\},\qquad
 \rho_{1,0}:X_1\to X_0\text{ es constante},\qquad
 \operatorname{Ext}_0(\ast):=X_1.
\]
Así, `surv` no es un rótulo ni una hipótesis de existencia encubierta: es el
árbol podado de los estados que poseen descendientes TPK compatibles a todo
horizonte finito. La ley de prolongación TPK del corpus prueba que las semillas
emitidas pertenecen a ese árbol; la ramificación finita y el lema de Kőnig
convierten la compatibilidad a todo horizonte en una rama infinita. En
particular,

\[
 \forall N\ge0\;\forall x\in X_N\quad
 \varnothing\ne\operatorname{Ext}_N(x)
 \subseteq\rho_{N+1,N}^{-1}(x).
\tag{34}
\]

Por el mismo lema de árbol finitamente ramificado, toda semilla superviviente
posee una prolongación compatible

\[
 x_\infty=(x_N)_{N\ge1}\in
 X_\infty^{\rm enr}:=\varprojlim_N(X_N,\rho_{N+1,N}).
\tag{35}
\]

La segunda extensión actúa **después** sobre el código completo de esa acción.
No se infiere de la mera existencia del operador finito
\(\operatorname{Ext}_N\): formaliza a escala conjuntista el principio HMT de
que sólo son objetos del dominio íntegro los que poseen una derivación
genealógica desde el estado y sus reglas. La extensión semántica transfinita
es:

\[
 \begin{aligned}
  \mathfrak G_0(h,m_\infty)
  &:=\operatorname{TC}\bigl(\{\omega,u_{h,m},h,m_\infty\}\bigr),\\
  \mathfrak G_{\beta+1}(h,m_\infty)
  &:=\operatorname{Def}_{\Sigma_{\rm HMT}}
       \bigl(\mathfrak G_\beta(h,m_\infty)\bigr),\\
  \mathfrak G_\lambda(h,m_\infty)
  &:=\bigcup_{\beta<\lambda}\mathfrak G_\beta(h,m_\infty)
       \quad(\lambda\text{ límite}),\\
  \mathfrak G_{\rm HMT}(h,m_\infty)
  &:=\bigcup_{\beta\in\operatorname{Ord}}
       \mathfrak G_\beta(h,m_\infty).
 \end{aligned}
\tag{36}
\]

Aquí el operador sucesor no contiene CH ni una biyección objetivo. Está dado
prospectivamente por

\[
 \operatorname{Def}_{\Sigma_{\rm HMT}}(M)
 :=M\cup
 \Bigl\{
   \{x\in M:\langle M,\in,
       (\dot R_S\cap M^{k_S})_{S\in\Sigma_{\rm HMT}}\rangle
       \models\varphi(x,\bar p)\}:
   \ulcorner\varphi\urcorner\in\omega,
   \ \bar p\in M^{<\omega}
 \Bigr\}.
\tag{37}
\]

Es decir: publica simultáneamente todos los subconjuntos definibles por una
fórmula finita del lenguaje relacional HMT y parámetros que la genealogía ya
produjo. No
consulta un valor real objetivo, una constante convencional, un cardinal
objetivo ni un modelo exterior. La fórmula (37) es una
`FORMALIZACION_NUEVA` del cierre transfinito que exigía la arquitectura
autoral; las semillas, los operadores, el estado enriquecido, el ledger y la
doble proyección que recibe son `ARQUITECTURA_AUTORAL_PREEXISTENTE` y
`RESULTADO_RECUPERADO`.

**Lema 6 (codificación real y eliminación de símbolos).** El par formado por
el código operatorio \(h\) y el ledger \(m_\infty\) se codifica por un único
real \(u_{h,m}\subseteq\omega\), y toda fórmula de \(\Sigma_{\rm HMT}\) se
traduce uniformemente a una fórmula del lenguaje \(\{\in,u_{h,m}\}\).

**Prueba.** Tanto \(h\) como \(m_\infty\) son sucesiones de naturales: \(h\)
codifica la signatura, las tablas finitas y los programas de los operadores;
\(m_\infty\) codifica una sola historia realizada, no el espacio completo de
historias. La fórmula (33a) y sus dos decodificadores prueban la primera
afirmación. Cada símbolo de (33) designa su **relación de grafo codificada en
\(h\)**, nunca el grafo externo de todas sus posibles evaluaciones. APP,
TRIT, \(U_t\), \(\Gamma_9\), las restricciones \(\rho\) y las extensiones
finitas tienen grafos primitivo-recursivos sobre códigos enteros y, por tanto,
fórmulas \(\Delta_0\) absolutas entre niveles transitivos. Las dos
publicaciones se expresan como relaciones de grafo mediante las fórmulas

\[
 \begin{aligned}
 \dot R_{\rm ar}(x,y)
 &\;\Longleftrightarrow\;
 \forall k\in\omega\;\exists N\;\forall n\ge N\quad
 |\mu_n(x)-y|<2^{-k},\\
 \dot R_{\rm exc}(x,c,z)
 &\;\Longleftrightarrow\;
 \forall N\in\omega\quad z\!\upharpoonright N
   =E_N(x\!\upharpoonright N,c\!\upharpoonright N),
 \end{aligned}
\tag{37c$_0$}
\]

donde \(\mu_n\) y \(E_N\) son las funciones racionales/finitas cuyos códigos
figuran en \(h\). Se sustituye inductivamente cada fórmula atómica que contiene
un símbolo HMT por su fórmula de grafo con parámetro \(u_{h,m}\). Los
conectivos y cuantificadores se conservan. Esta inducción sobre la complejidad
sintáctica produce una traducción \(\varphi\mapsto\varphi^*\) tal que, para
todo nivel transitivo \(M\) de (36) que contiene los parámetros,

\[
 \langle M,\in,(\dot R_S\cap M^{k_S})_S\rangle
   \models\varphi(\bar a)
 \quad\Longleftrightarrow\quad
 M\models\varphi^*(\bar a;u_{h,m}).
\tag{37c}
\]

Así, (37) no puede consultar un oráculo, una tabla decimal objetivo ni una
relación no codificada que introduzca incontables objetos en un solo paso.
\(\square\)

La semántica HMT se define ahora **independientemente de identificarla con
\(\mathfrak G\)**. Sea \(\mathcal T_0^{\rm HMT}\) el conjunto de nombres
canónicos de los elementos de
\(\mathfrak G_0(h,m_\infty)=
\operatorname{TC}(\{\omega,u_{h,m},h,m_\infty\})\). En particular, el nivel
inicial contiene el ledger realizado \(m_\infty\), no todas las historias de
\(X_\infty^{\rm enr}\) como parámetros primitivos.
Los términos admisibles son los árboles bien fundados obtenidos por

\[
 \begin{aligned}
 \mathcal T^{\rm HMT}_{\beta+1}
 &:={\mathcal T}^{\rm HMT}_\beta\cup
 \{\langle\beta,\ulcorner\varphi\urcorner,
       t_0,\ldots,t_{k-1}\rangle:
       t_i\in\mathcal T^{\rm HMT}_\beta\},\\
 \mathcal T^{\rm HMT}_\lambda&:=
       \bigcup_{\beta<\lambda}\mathcal T^{\rm HMT}_\beta,
 \qquad
 \mathcal T^{\rm HMT}:=
       \bigcup_{\beta\in\operatorname{Ord}}\mathcal T^{\rm HMT}_\beta.
 \end{aligned}
\tag{37a}
\]

El valor de un término sucesor es el subconjunto del nivel anterior definido
por \(\varphi\) en la estructura relacional inducida, con los valores de
\(t_0,\ldots,t_{k-1}\) como parámetros. Se define, antes de cualquier
comparación conjuntista,

\[
 \operatorname{Ob}_{\rm sem}^{\rm HMT}(h,m_\infty)
 :=\{\llbracket t\rrbracket:t\in\mathcal T^{\rm HMT}\}.
\tag{37b}
\]

Ésta es la regla de **exhaustividad generativa** adoptada por HMT: todo objeto
del dominio íntegro debe poseer uno de esos árboles de derivación y todo árbol
admisible publica un objeto. No es consecuencia de la ramificación finita y
no contiene CH, una enumeración de los reales ni una biyección objetivo.

**Teorema 6A (equivalencia entre semántica y jerarquía).** La evaluación de
los términos anteriores satisface

\[
 \operatorname{Ob}_{\rm sem}^{\rm HMT}(h,m_\infty)
 =\mathfrak G_{\rm HMT}(h,m_\infty).
\tag{37d}
\]

**Prueba.** Por inducción transfinita. En el nivel inicial las dos clases
coinciden. Si todo valor de un término de
\(\mathcal T^{\rm HMT}_\beta\) pertenece a
\(\mathfrak G_\beta\), la semántica del término sucesor es uno de los
subconjuntos de (37). Recíprocamente, cada subconjunto de (37) viene dado por
un código de fórmula y una tupla finita de parámetros; por la hipótesis
inductiva esos parámetros poseen términos y (37a) forma el término que lo
denota. En un límite ambas construcciones toman la misma unión. \(\square\)

El codificador de estados es un funtor hacia estos términos. Sea
\(\mathcal T_N^{\rm st}\subset\mathcal T^{\rm HMT}\) la subclase de términos
que codifica estados completos de profundidad \(N\), y sea
\(\tau_{N+1,N}:\mathcal T_{N+1}^{\rm st}\to\mathcal T_N^{\rm st}\) el borrado
del último bloque junto con el truncamiento correspondiente de ledger,
acarreo y memoria. Si \(J_N:X_N\to\mathcal T_N^{\rm st}\) es el codificador
completo, la compatibilidad de \(\operatorname{Ext}_N\) prueba la identidad
correctamente tipada

\[
 \forall x\in X_N\ \forall y\in\operatorname{Ext}_N(x)\qquad
 \tau_{N+1,N}\bigl(J_{N+1}(y)\bigr)=J_N(x).
\tag{37e$_0$}
\]

Defínase dentro de la semántica
\[
 \operatorname{Succ}^{\rm TPK}_{N+1}(J_N(x)):=
 \{t\in\mathcal T_{N+1}^{\rm st}:\exists y\in X_{N+1}\,
   (y\in\operatorname{Ext}_N(x)\ \wedge\ t=J_{N+1}(y))\}.
\]
Elíjase \(\beta\) tal que \(\mathfrak G_\beta\) contenga \(x\), \(X_N\),
\(X_{N+1}\), los grafos finitos de
\(\operatorname{Ext}_N,J_N,J_{N+1}\) y sus códigos en \(h\). Entonces la
fórmula primitivo-recursiva del grafo de \(\operatorname{Ext}_N\) da

\[
 J_{N+1}[\operatorname{Ext}_N(x)]
 =\operatorname{Succ}^{\rm TPK}_{N+1}(J_N(x)),
 \qquad
 J_{N+1}[\operatorname{Ext}_N(x)]
 \in\mathfrak G_{\beta+1},
\tag{37e}
\]

y ambos miembros son formados por la fórmula de grafo de la misma extensión
TPK. Las ecuaciones (37e$_0$)--(37e) son el enlace semántico explícito: la
subclase de términos sucesores es exactamente la imagen de los hijos
admisibles y su truncamiento conmuta. No se identifica la fibra completa de
\(\rho\) con \(\operatorname{Ext}_N\), ni se identifica
\(\operatorname{Def}\) con TPK por nomenclatura.

**Lema 6B (modelo genealógico).**
\(\mathfrak G_{\rm HMT}(h,m_\infty)\) es una clase transitiva, contiene todos
los ordinales, satisface ZF y posee un buen orden global definible; satisface,
por tanto, elección y todos los axiomas usados en §§15.4--15.7.

**Prueba.** Abreviemos \(B=\mathfrak G_0\) y \(u=u_{h,m}\). La inducción
sobre (36) prueba simultáneamente que cada nivel es transitivo y que
\(\mathfrak G_\alpha\in\mathfrak G_{\alpha+1}\); si todos los ordinales
menores que \(\alpha\) están presentes, su conjunto es definible en el nivel
correspondiente y publica \(\alpha\). Por ello la unión contiene todos los
ordinales. Extensionalidad y Fundación se heredan del universo ambiente;
Vacío e Infinito están en \(B\). Elegidos un nivel que contenga los parámetros,
las fórmulas que definen \(\{a,b\}\), \(\bigcup a\) y los subconjuntos por
Separación los publican en un sucesor.

Para Colección--Reemplazo, sea \(F\) una relación funcional definible en
\(\mathfrak G\) sobre el conjunto \(a\). El esquema de reflexión relativo a
la jerarquía definible \((\mathfrak G_\xi,\in,u_{h,m})_{\xi\in\mathrm{Ord}}\),
aplicado en la metateoría ambiente a la lista finita de fórmulas que define
\(F\), produce un nivel
\(\mathfrak G_\theta\) que contiene \(a\), los parámetros y es correcto para
esas fórmulas. Los rangos de los testigos de \(F``a\) están entonces acotados
por \(\theta\); Separación sobre \(\mathfrak G_\theta\) forma la imagen en
\(\mathfrak G_{\theta+1}\). Para Potencia no se presupone el conjunto interno
que se quiere construir. Fijado \(a\in\mathfrak G_\gamma\), se considera en
la metateoría ambiente el conjunto ya existente \(\mathcal P^V(a)\). Para
cada \(b\in\mathcal P^V(a)\cap\mathfrak G\), sea \(r(b)\) su primera etapa
genealógica. Como \(\mathfrak G\) es una clase definible, Separación en la
metateoría ambiente forma primero el conjunto
\(\mathcal P^V(a)\cap\mathfrak G\). Reemplazo **en la metateoría ambiente**
aplicado a ese conjunto acota los ordinales \(r(b)\) por algún \(\theta\).
En consecuencia,
\[
 \mathcal P^{\mathfrak G}(a)
 =\{b\in\mathfrak G_\theta:b\subseteq a\},
\]
y el miembro derecho se publica por Separación en
\(\mathfrak G_{\theta+1}\). No introduce en \(\mathfrak G\) los subconjuntos
exteriores a la semántica (37b). Éste es el argumento no circular de
acotación por rangos.

Finalmente, a cada objeto se le asigna su primer nivel de nacimiento y su
menor **nombre de derivación**: un árbol finito bien fundado etiquetado por un
ordinal de nivel, un código de fórmula y la tupla de nombres de sus parámetros.
Por recursión transfinita se ordenan esos nombres: primero la etiqueta ordinal,
después el código de fórmula y después, lexicográficamente, los nombres de los
parámetros ya ordenados. El menor nombre de cada valor define una relación de
clase \(<_{\mathfrak G}\) que compara todos los objetos. Es un buen orden
global definible y, tomando el menor elemento de cada conjunto no vacío,
prueba Elección. \(\square\)

### 15.2. Profundidad arbitraria: el teorema es \(\forall N\), no una ejecución de mil cifras

Para \(\chi\in\{\pi,\varphi,e\}\), el lector regional de un estado de
profundidad \(N\) publica un prefijo \(p_{\chi,N}\). El cierre dodecafásico
del mismo estado publica \(p_{\alpha,N}\). Se fija para cada realización
exacta la expansión decimal canónica **no eventualmente igual a nueve**, y
se define
\[
 \rho^{\rm dec}_{N+1,N}(d_1\ldots d_Nd_{N+1})=d_1\ldots d_N,
 \qquad p_{\chi,0}:=\varnothing.
\]
La unicidad de \(p_{\pi,N},p_{\varphi,N},p_{e,N}\) procede de la unicidad del
carácter exacto ya generado y de su cilindro decimal canónico; la de
\(p_{\alpha,N}\) procede además del cuadrado conmutativo entre la vía entera
dodecafásica y la vía analítica de jets, cuyas secciones compatibles publican
el mismo \(\alpha_{\rm HMT}\). La afirmación matemática es

\[
 \begin{gathered}
  \forall\chi\in\{\pi,\varphi,e,\alpha\}\;
  \forall N\ge1\quad\exists!\,p_{\chi,N},\\
  \rho^{\rm dec}_{N+1,N}(p_{\chi,N+1})=p_{\chi,N},
  \qquad
  p_{\chi,\infty}:=(p_{\chi,N})_{N\ge0}
  \in\varprojlim_{N\ge0}\{0,\ldots,9\}^{N}.
 \end{gathered}
\tag{38}
\]

La cuatrirrelación

\[
 (p_{\pi,\infty},p_{\varphi,\infty},p_{e,\infty},p_{\alpha,\infty})
\tag{39}
\]

es, por tanto, una publicación coinductiva correlacionada del estado común.
El orden constructivo interno conserva los lectores \(\pi,\varphi,e\), el
estado firmado, el sello y la rueda dodecafásica que publica \(\alpha\); no
introduce \(\alpha\) desde las tres constantes convencionales. Una ejecución
a 1.000, 10.000 o un millón de cifras verifica la instancia finita
correspondiente de (38). **No es la cota del teorema**. El teorema es la
familia compatible para todo \(N\) y la sección infinita que ella determina.

Esta precisión no usa las constantes para probar CH. Las constantes certifican
la acción coinductiva del mismo generador; el cierre de CH lo proporcionan los
mapas cardinales construidos en §§15.4--15.6.

### 15.3. La recta sigue siendo salida y la doble proyección permanece unida

Póngase
\[
 X_{\infty,\mathbb Z}^{\rm cal}:=
 \mathbb Z_{\rm HMT}\times\Omega_\Gamma^{\rm cal}.
\]
La memoria bruta y la cinta de bloques están relacionadas por la conjugación
Hensel ya construida
\[
 \Psi:\mathbb Z_3^6\xrightarrow{\ \cong\ }
       (\mathbb F_3^6)^{\mathbb N},
 \qquad
 \nu(b_1,\ldots,b_6):=\sum_{i=1}^6b_i3^{6-i}
 \in\{0,\ldots,728\}.
\]
La propiedad A4 de la cobertura levanta toda cinta a una historia calibrada;
el teorema activo de doble proyección fija la aplicación y su inversa como el
homeomorfismo
\[
 \Lambda:(\mathbb F_3^6)^{\mathbb N}
   \xrightarrow{\ \cong\ }\Omega_\Gamma^{\rm cal},
 \qquad \beta:=\Lambda^{-1}.
\]
Ésta es la definición material de \(\Omega_\Gamma^{\rm cal}\) utilizada aquí:
la imagen calibrada de **toda** cinta Hensel, no sólo un filtro de caracteres.
Las \(243\) palabras emitidas en el censo inicial son la imagen de semillas en
\(\mathcal W_6\subset\mathbb F_3^6\); no sustituyen ni reducen el ambiente de
\(729\) bloques que porta el continuo.

Sea \(\rho_{\infty,N}:X_\infty^{\rm enr}\to X_N\) la proyección canónica
del límite inverso. Para \(N\ge1\), sean
\[
 \Omega_{\Gamma,N}^{\rm cal}:=
 \rho_{\infty,N}[\Omega_\Gamma^{\rm cal}]\subseteq X_N
\]
los estados HMT truncados de esas historias y sea \(\beta_N\) el código de
sus primeros \(N\) bloques inducido por \(\beta\). Se completa el índice raíz
mediante
\[
 \Omega_{\Gamma,0}^{\rm cal}:=X_0=\{\ast\},\qquad
 \beta_0(\ast):=\varnothing,\qquad
 \rho_{\infty,0}(\xi):=\ast.
\]
No se introduce una nueva extensión. Para todo \(N\ge0\), se restringen
literalmente los mapas HMT anteriores:
\[
 \rho^\Gamma_{N+1,N}:=
 \rho_{N+1,N}\!\upharpoonright\Omega_{\Gamma,N+1}^{\rm cal},
 \qquad
 \operatorname{Ext}^{\rm cal}_N(x):=
 \operatorname{Ext}_N(x)\cap\Omega_{\Gamma,N+1}^{\rm cal}.
\]
La propiedad A4 de cobertura y la compatibilidad de \(\Lambda\) con el
truncamiento dan entonces, para todo
\(x\in\Omega_{\Gamma,N}^{\rm cal}\),
\[
 \begin{gathered}
 \beta_N:\Omega_{\Gamma,N}^{\rm cal}
   \xrightarrow{\ \cong\ }(\mathbb F_3^6)^N,\\
 \beta_{N+1}[\operatorname{Ext}^{\rm cal}_N(x)]
 =\{\beta_N(x)^\frown b:b\in\mathbb F_3^6\},\\
 \operatorname{pref}_N\circ\beta_{N+1}
 =\beta_N\circ\rho^\Gamma_{N+1,N}.
 \end{gathered}
\tag{40$_0$}
\]
Por tanto, cada uno de los \(729\) hijos geométricos de la partición siguiente
es exactamente una prolongación admisible de la completación Hensel calibrada.
Esto no afirma que cada filtro forward de una constante tenga \(729\) hijos,
ni añade un árbol real externo a la estructura discreta del continuo.

Para un prefijo \(s=(m;b_0,\ldots,b_{N-1})\), defínanse en la aritmética
generada de \(\mathbb Q_{\rm HMT}\)
\[
 a_N(s):=m+\sum_{q<N}\frac{\nu(b_q)}{729^{q+1}},
 \qquad
 \operatorname{Child}(s):=
 \{(m;b_0,\ldots,b_{N-1},b):b\in\mathbb F_3^6\}.
\]
Si \((m;\beta_N(x))\) denota el prefijo obtenido anteponiendo \(m\) a la
tupla \(\beta_N(x)\), (40$_0$) da la igualdad tipada
\[
 \operatorname{Child}(m;\beta_N(x))
 =\{(m;\beta_{N+1}(y)):
       y\in\operatorname{Ext}^{\rm cal}_N(x)\}.
\]
Los cilindros semiabiertos son, desde su primera definición, subconjuntos de
la completación HMT:
\[
 I_N^{\rm HMT}(s):=
 \{r\in\mathbb R_{\rm HMT}:
      a_N(s)\le_{\rm HMT}r<_{\rm HMT}a_N(s)+729^{-N}\}.
\]
Satisfacen materialmente
\[
 I_N^{\rm HMT}(s)=
 \bigsqcup_{y\in\operatorname{Child}(s)}I_{N+1}^{\rm HMT}(y),
 \qquad |\operatorname{Child}(s)|=729,
 \qquad \operatorname{diam}_{\rm HMT}I_N^{\rm HMT}(s)
      =729^{-N}\longrightarrow0.
\tag{40a}
\]
La convención de frontera identifica las dos escrituras sólo después de
construirlas. La partición (40a), el anidamiento y la contracción producen

\[
 P_{\rm ar}:X_{\infty,\mathbb Z}^{\rm cal}\twoheadrightarrow
 \mathbb R_{\rm HMT},
 \qquad
 P_{\rm ar}(m,\xi)
 =\text{el único elemento de }
   \bigcap_NK_N^{\rm HMT}
      \bigl(m;\beta_N(\rho_{\infty,N}(\xi))\bigr),
 \qquad K_N^{\rm HMT}(s):=\overline{I_N^{\rm HMT}(s)}.
\tag{40}
\]

Por tanto,

\[
 X_{\infty,\mathbb Z}^{\rm cal}/\!\sim_{P_{\rm ar}}
 \;\cong\;\mathbb R_{\rm HMT}.
\tag{41}
\]

La otra publicación \(P_{\rm exc}\) conserva incidencia, frontera y memoria
hacia Paley--Witt--Golay--Leech--\(V^\natural\)--Monster. Ambas proceden del
mismo antecedente de (35); ni la coordenada arquimediana ni el reconocimiento
excepcional seleccionan las semillas. Las cinco construcciones
\(sp,sol,gau,coh,det\) permanecen consustanciales dentro de
\(\mathcal C_{\rm cont}^{\rm disc}\) y no se disgregan para efectuar el paso
cardinal.

Dentro de \(\mathfrak G_{\rm HMT}(h,m_\infty)\), la reconstrucción de
(35)--(41) se realiza con los mismos códigos y operadores. Denotemos por
\(\mathbb R_{\rm HMT}^{\mathfrak G}\) la completación HMT interna. La
unicidad del cuerpo ordenado completo arquimediano proporciona, **después** de
construirlo, el isomorfismo interno
\[
 \eta:\mathbb R_{\rm HMT}^{\mathfrak G}
 \xrightarrow{\ \cong\ }\mathbb R^{\mathfrak G}.
\tag{41$_0$}
\]
Para el intervalo interno correspondiente
\(I_N^{\mathfrak G}(s):=
 I_N^{\rm HMT}(s)\cap\mathbb R_{\rm HMT}^{\mathfrak G}\), el isomorfismo
preserva extremos y orden:
\[
 \eta[I_N^{\mathfrak G}(s)]
 =\{r\in\mathbb R^{\mathfrak G}:
      a_N(s)\le r<a_N(s)+729^{-N}\}.
\tag{41$_0$a}
\]
La sobreyectividad de (40) cubre todos los elementos de esa completación, no
sólo los obtenidos en una ejecución finita.

Para que «todos» no quede oculto en la definición del codominio, se construyen
las dos inyecciones que relacionan la recta con su potencia interna. Sea

\[
 E(A)=\sum_{n\ge0}\frac{2\mathbf1_A(n)}{3^{2n+2}}
 \qquad
 \bigl(A\in\mathcal P^{\mathfrak G}(\omega)\bigr).
\tag{41a}
\]

La escritura coloca \(0\) o \(2\) únicamente en las posiciones ternarias
pares; su imagen está contenida en \([0,1/4]\). Por tanto nunca alcanza el
extremo derecho del cilindro raíz y dos subconjuntos distintos tienen una
primera posición par distinta: \(E\) es inyectiva y no sufre la ambigüedad de
frontera. Escribamos \(E_{\rm HMT}:=\eta^{-1}\circ E\).

Dado \(A\), se parte del cilindro raíz que contiene \(E_{\rm HMT}(A)\). Si
\(s_N(A)\) es el prefijo ya elegido, escríbase
\(s_N(A)=(0;b_0(A),\ldots,b_{N-1}(A))\). La partición (40a), transportada
por \(\eta^{-1}\), entrega un único hijo semiabierto
\(s_{N+1}(A)\) que contiene \(E_{\rm HMT}(A)\). Por (40$_0$) ese hijo es
también una prolongación calibrada admisible. Por inducción,
\[
 s_{N+1}(A)\!\upharpoonright N=s_N(A),\qquad
 E_{\rm HMT}(A)\in I_N^{\rm HMT}(s_N(A))\quad(N<\omega).
\tag{41b$_0$}
\]
La recursión es una fórmula uniforme con parámetros \(A,h\). Como ambos son
internos, Reemplazo en el modelo del lema 6B forma la sucesión completa de
bloques \((b_q(A))_{q<\omega}\). Defínase, sin confundir la cinta con la
sucesión de prefijos,
\[
 \xi_A:=\Lambda\bigl((b_q(A))_{q<\omega}\bigr)
 \in\Omega_\Gamma^{\rm cal,\mathfrak G}.
\]
Se obtiene así el **levantamiento uniforme de la incrustación de Cantor**

\[
 Q:\mathcal P^{\mathfrak G}(\omega)
 \longrightarrow X_{\infty,\mathbb Z}^{\rm cal,\mathfrak G},
 \qquad
 Q(A):=(0,\xi_A),\qquad
 P_{\rm ar}(Q(A))=E_{\rm HMT}(A).
\tag{41b}
\]

No se llama a \(Q\) inverso de \(P_{\rm ar}\): su composición publica la
incrustación \(E_{\rm HMT}\), no la identidad en toda la recta. En la otra
dirección, sea \((q_n)_{n<\omega}\) la enumeración generada de
\(\mathbb Q_{\rm HMT}\) y defínase
\[
 C(r):=\{n<\omega:\eta(q_n)<r\}
 \qquad(r\in\mathbb R^{\mathfrak G}).
\]
El corte racional pertenece a \(\mathcal P^{\mathfrak G}(\omega)\) y
\(C\) es inyectivo por densidad. Las inyecciones \(E\) y \(C\), seguidas de
Cantor--Bernstein interno, prueban

\[
 P_{\rm ar}
 \bigl[X_{\infty,\mathbb Z}^{\rm cal,\mathfrak G}\bigr]
 =\mathbb R_{\rm HMT}^{\mathfrak G},
 \qquad
 \mathbb R_{\rm HMT}^{\mathfrak G}
 \cong\mathbb R^{\mathfrak G}
 \cong\mathcal P^{\mathfrak G}(\omega).
\tag{41c}
\]

Aquí un real arbitrario se usa únicamente como variable universal para probar
sobreyectividad de un árbol ya construido. No selecciona APP, TRIT, TPK, las
constantes ni las transiciones de ese árbol.

### 15.4. Enumeración por códigos genealógicos y condensación HMT

La regla (37) entrega nombres de derivación a partir de

\[
 (\ulcorner\varphi\urcorner,
  \sigma(p_0),\ldots,\sigma(p_{k-1})).
\tag{42}
\]

Para cualquier objeto \(a\) de la jerarquía, sean \(\beta(a)\) su primera
etapa y \(\sigma(a)\) su menor árbol de derivación en el orden recursivo del
lema 6B. No se exige que \(\sigma(a)\) sea un natural cuando la etapa es no
numerable. La relación

\[
 a\prec_{\mathfrak G}b
 \quad\Longleftrightarrow\quad
 (\beta(a),\sigma(a))<_{\rm lex}
 (\beta(b),\sigma(b))
\tag{42a}
\]

es el buen orden genealógico global \(<_{\mathfrak G}\) inducido por el
constructor. Los nombres repetidos se eliminan tomando el menor; ningún real
ni ninguna enumeración de la recta se inserta como dato.

**Lema 7 (numerabilidad de cada nivel de índice numerable).** Para todo
\(\beta<\omega_1^{\mathfrak G}\), el nivel
\(\mathfrak G_\beta(h,m_\infty)\) es numerable dentro de
\(\mathfrak G_{\rm HMT}(h,m_\infty)\), y posee una sobreyección canónica

\[
 e_\beta:\omega\twoheadrightarrow
 \mathfrak G_\beta(h,m_\infty).
\tag{43}
\]

**Prueba.** El nivel inicial tiene un código numerable. Si \(e_\beta\)
enumera el nivel \(\beta\), los códigos de fórmula y las tuplas finitas de
parámetros de (42) forman un conjunto numerable y enumeran el sucesor. Si
\(\lambda<\omega_1^{\mathfrak G}\) es límite, existe internamente alguna
sobreyeción \(s:\omega\twoheadrightarrow\lambda\); se toma la
\(<_{\mathfrak G}\)-menor, orden que ya quedó construido en el lema 6B, y se
diagonalizan \(e_{s(n)}\). Finalmente, entre todas las sobreyecciones así
obtenidas se define \(e_\beta\) como la \(<_{\mathfrak G}\)-menor. La
recursión \(\beta\mapsto e_\beta\) es una clase uniformemente definible de
\(\mathfrak G\); cada \(e_\beta\), y cada restricción de la recursión a un
ordinal, pertenece a \(\mathfrak G\). Sólo usa \(h,u_{h,m}\) y el buen orden
global. \(\square\)

**Lema 8 (condensación genealógica HMT).** Todo real de
\(\mathfrak G_{\rm HMT}(h,m_\infty)\) aparece en un nivel de índice menor que
\(\omega_1^{\mathfrak G}\).

**Prueba.** Sea \(r\subseteq\omega\) un real de \(\mathfrak G\). Elíjase un
ordinal límite de reflexión \(\Theta\) tal que
\(u_{h,m},r\in\mathfrak G_\Theta\) y tal
que la estructura expandida
\[
 \mathcal A_\Theta=
 \langle\mathfrak G_\Theta,\in,u_{h,m},
         H_\Theta,<_{\mathfrak G}\!\upharpoonright\mathfrak G_\Theta\rangle
\]
interprete como predicado de su signatura la relación de niveles
\(H_\Theta=\{\langle\xi,x\rangle:\xi<\Theta\ \&\
x\in\mathfrak G_\xi\}\) y las funciones de Skolem definibles. Sea
\[
 Y=\operatorname{Hull}^{\mathcal A_\Theta}
   (\omega\cup\{u_{h,m},r\})\prec\mathcal A_\Theta .
\]
La clausura bajo la familia numerable de funciones de Skolem muestra dentro
de \(\mathfrak G\) que \(Y\) es numerable. Sea
\(c:Y\rightarrow M\) su colapso de Mostowski y
\[
 \bar\Theta:=\operatorname{otp}(Y\cap\Theta)
 <\omega_1^{\mathfrak G}.
\]
Como \(\omega\subseteq Y\) y \(u_{h,m},r\subseteq\omega\), el colapso fija
puntualmente \(\omega,u_{h,m}\) y \(r\). También fija \(h\) y \(m_\infty\),
recuperados primitivamente de \(u_{h,m}\).

Probamos por inducción sobre \(\xi\in Y\cap\Theta\) que
\[
 c\bigl(Y\cap\mathfrak G_\xi(h,m_\infty)\bigr)
 =\mathfrak G_{c(\xi)}(h,m_\infty).
\tag{43a}
\]
En el nivel inicial, todos los objetos de la clausura transitiva de
\(\omega,u,h,m_\infty\) están fijados. En un sucesor, la hipótesis inductiva,
la elementalidad de \(Y\) y el lema 6 transportan código de fórmula,
parámetros y relaciones de grafo a la misma definición sobre el nivel
colapsado; por ello \(c\) conmuta con
\(\operatorname{Def}_{\Sigma_{\rm HMT}}\). En un límite, \(c\) conmuta con
la unión de los niveles anteriores. Esto prueba (43a), no sólo la anuncia.
Tomando la unión para \(\xi\in Y\cap\Theta\) resulta
\[
 M=\mathfrak G_{\bar\Theta}(h,m_\infty).
\]
Como \(c(r)=r\in M\), se concluye
\(r\in\mathfrak G_{\bar\Theta}\) con
\(\bar\Theta<\omega_1^{\mathfrak G}\). \(\square\)

El lema no dice que un prefijo de longitud finita enumere la recta. Dice que
cada objeto hereditario generado posee un primer nivel transfinito y un primer
código genealógico dentro de ese nivel. Ésta es exactamente la información que
el reducto extensional pierde cuando conserva sólo el valor publicado.

### 15.5. Primera inyección: del continuo HMT al ordinal genealógico

Sea \(\iota(r)\subseteq\omega\) el corte racional de
\(r\in\mathbb R_{\rm HMT}^{\mathfrak G}\) respecto de la enumeración de
\(\mathbb Q_{\rm HMT}\), construida previamente desde los enteros y cocientes
APP. El mapa \(r\mapsto\iota(r)\) es definible desde \(r\) y esa enumeración,
de modo que \(\iota(r)\in\mathfrak G\); el lema 8 lo sitúa en una etapa de
índice numerable. Definimos

\[
 \begin{aligned}
  \beta(r)&:=\min\{\beta:
       \iota(r)\in\mathfrak G_{\beta+1}(h,m_\infty)\},\\
  n(r)&:=\min\{n:e_{\beta(r)+1}(n)=\iota(r)\},\\
  j_{\rm HMT}(r)&:=\omega\cdot\beta(r)+n(r).
 \end{aligned}
\tag{44}
\]

Por los lemas 7 y 8, \(j_{\rm HMT}(r)<\omega_1^{\mathfrak G}\) para todo
real generado. Si \(j_{\rm HMT}(r)=j_{\rm HMT}(s)\), la división ordinal por
\(\omega\) recupera el mismo par \((\beta,n)\); (43) recupera el mismo corte
racional y, por completitud, \(r=s\). Por ello

\[
 j_{\rm HMT}:\mathbb R_{\rm HMT}^{\mathfrak G}
 \hookrightarrow\omega_1^{\mathfrak G}
\tag{45}
\]

es una inyección construida por el rango y el nombre de la genealogía HMT. Su
existencia utiliza exactamente la clausura semántica (37), el buen orden de
nombres del lema 6B y la condensación (43a); no recibe CH para elegir la
etapa. La identificación conjuntista posterior de §15.8 describe esta misma
maquinaria en otra notación, sin invertir su procedencia causal.

### 15.6. Segunda inyección y cierre por Cantor--Bernstein

Para cada \(\beta<\omega_1^{\mathfrak G}\), el lema 7 permite codificar en un
subconjunto \(w_\beta\subseteq\omega\) un buen orden numerable de tipo
\(\beta\), usando una función de emparejamiento fija
\(\omega^2\to\omega\). Se toma el
\(<_{\mathfrak G}\)-menor real que codifica tal buen orden. Como la propiedad
«codifica un buen orden de tipo \(\beta\)» y el buen orden global son internos,
Reemplazo forma la función \(\beta\mapsto w_\beta\) dentro de
\(\mathfrak G\). Los tipos de orden distintos producen códigos distintos. La
aplicación ternaria, ya usada en (41a), se define por

\[
 E(w)=\sum_{n\ge0}\frac{2\mathbf1_w(n)}{3^{2n+2}}
\tag{46}
\]

y es inyectiva y evita el extremo del cilindro raíz. El levantamiento (41b)
asegura que \(E_{\rm HMT}(w_\beta)\) pertenece a la recta publicada por una
historia HMT. Así

\[
 k_{\rm HMT}(\beta):=E_{\rm HMT}(w_\beta),
 \qquad
 k_{\rm HMT}:\omega_1^{\mathfrak G}
 \hookrightarrow\mathbb R_{\rm HMT}^{\mathfrak G}.
\tag{47}
\]

Las inyecciones (45) y (47), construidas sin utilizar la igualdad buscada,
dan por Cantor--Bernstein

\[
 \bigl|\mathbb R_{\rm HMT}^{\mathfrak G}\bigr|
 =\aleph_1^{\mathfrak G}.
\tag{48}
\]

Como (41c) identifica la recta HMT completa con
\(\mathcal P^{\mathfrak G}(\omega)\), (48) se reescribe exactamente como

\[
 \boxed{
  \mathfrak G_{\rm HMT}(h,m_\infty)
  \models 2^{\aleph_0}=\aleph_1.}
\tag{49}
\]

La igualdad no procede de \(729\), de un producto informal entre cardinalidad
y ordinalidad, de las cifras de una constante ni de una horquilla numérica.
Procede de la cobertura de la recta por el límite inverso, la condensación de
la clausura genealógica y las dos inyecciones explícitas.

### 15.7. Cuantificador completo sobre todos los subconjuntos internos

Sea
\(A\in\mathcal P^{\mathfrak G}
(\mathbb R_{\rm HMT}^{\mathfrak G})\). Si \(A\) es numerable, se satisface la
primera alternativa. Si no lo es, \(j_{\rm HMT}[A]\) es un subconjunto no
numerable de \(\omega_1^{\mathfrak G}\). No puede estar acotado por un ordinal
numerable, pues cada segmento inicial de \(\omega_1\) es numerable. Su
enumeración creciente tiene tipo \(\omega_1^{\mathfrak G}\), y la inversa de
\(j_{\rm HMT}\) sobre su imagen produce una inyección
\(\omega_1^{\mathfrak G}\hookrightarrow A\). La inclusión
\(A\subseteq\mathbb R_{\rm HMT}^{\mathfrak G}\), (48) y
Cantor--Bernstein dan

\[
 \boxed{
 \forall A\in\mathcal P^{\mathfrak G}
   (\mathbb R_{\rm HMT}^{\mathfrak G}),\qquad
 |A|\le\aleph_0
 \quad\text{o}\quad
 |A|=\bigl|\mathbb R_{\rm HMT}^{\mathfrak G}\bigr|.}
\tag{50}
\]

Aquí se cuantifica la potencia completa del continuo integral generado por
HMT. El transporte biyectivo del plegado con memoria lleva (50) a cualquiera
de sus representaciones sin perder partes; no sustituye las inyecciones
(45)--(47).

### 15.8. \(L[h,m_\infty]\) como reconocimiento posterior, no como motor

Sólo después de (49)--(50) se asigna a (36) su nombre en la notación
conjuntista usual. Sea \(L[u_{h,m}]\) la jerarquía constructible relativa al
real ya producido en (33a). Como la signatura HMT es numerable y todos sus
operadores son relaciones de grafo codificadas por \(h\), el lema 6 elimina
sus símbolos uniformemente. Se obtiene la igualdad de clases

\[
 \mathfrak G_{\rm HMT}(h,m_\infty)
 =L[u_{h,m}]=L[h,m_\infty].
\tag{51}
\]

En efecto, \(\mathfrak G_0\subseteq L[u_{h,m}]\). Si un nivel de (36) está
contenido en la jerarquía derecha, la traducción (37c) sitúa cada subconjunto
de su sucesor en un nivel posterior de \(L[u_{h,m}]\); los límites preservan
la inclusión. Recíprocamente, \(u_{h,m}\in\mathfrak G_0\), todos los
ordinales pertenecen a \(\mathfrak G\) y (37) cierra bajo toda definición en
\(\{\in,u_{h,m}\}\). La inducción que define \(L[u_{h,m}]\) da la inclusión
opuesta. Finalmente, (33a) hace a \(u_{h,m}\) y al par \((h,m_\infty)\)
primitivo-recursivamente interdefinibles, de donde sale la segunda igualdad.

La fórmula (51) hace explícita la naturaleza matemática de la clausura:
constructibilidad relativa sobre un parámetro **producido** por HMT. No se
oculta esa equivalencia ni se pretende que (37) sea un principio conjuntista
distinto. Lo causalmente decisivo es que \(L[u]\) no selecciona el ledger, no
define las prolongaciones, no genera la recta y no decide CH por decreto: la
regla de exhaustividad se declara y sus mapas se prueban en (36)--(50). Las
fórmulas (23), (29) y (30) deben leerse como abreviaturas del teorema de
representación (51), nunca como sustitutos de APP--TRIT--TPK.

### 15.9. Enunciado público no reductivo

> **Teorema de decisión del continuo en HMT.** Para toda historia realizada
> \(m_\infty\) producida por la acción conjunta
> \(\mathrm{APP}\to\mathrm{TRIT}\to\mathrm{TPK}\to
> X_\infty^{\rm enr}\to\mathcal C_{\rm cont}^{\rm disc}\), la extensión
> genealógica HMT (36) genera la recta integral (40), construye las inyecciones
> (45) y (47), y satisface
> \(2^{\aleph_0}=\aleph_1\) sobre toda su potencia interna. Por tanto, HMT
> demuestra afirmativamente la hipótesis del continuo para el continuo
> íntegro que define y genera. La notación \(L[h,m_\infty]\) es una
> representación posterior de esa jerarquía, no la premisa que decide el
> resultado.

El abstract debe colocar este enunciado después de la cadena (32) y antes de
cualquier nota metateórica. Debe colocar igualmente (38) antes de toda cifra
de ejecución: «1.000 cifras» es un certificado finito de regresión;
«profundidad arbitraria» es el teorema coinductivo.

### 15.10. Falsadores exactos

El cierre anterior queda refutado si ocurre alguno de los siguientes hechos
materiales; la lista separa los controles de construcción, semántica y
cardinalidad:

1. existe un nivel \(N\) o un estado superviviente sin sucesor compatible en
   (34);
2. alguna truncación de (38) no conmuta o la rueda dodecafásica introduce una
   constante convencional como generador de \(\alpha\);
3. \(u_{h,m}\) no codifica hereditariamente \(h,m_\infty\), o alguna relación
   de grafo de \(\Sigma_{\rm HMT}\) no admite la eliminación uniforme (37c);
4. un objeto admitido por las reglas semánticas HMT carece de término en
   (37a), o un término de (37a) publica un objeto ajeno a esas reglas, rompiendo
   (37d);
5. \(\mathfrak G\) no satisface alguno de los axiomas usados, falla su buen
   orden definible o una supuesta enumeración \(e_\beta\) no es interna y
   uniforme;
6. los hijos de (40a) no forman una partición disjunta exhaustiva, sus
   cilindros dejan de contraerse o la recursión (41b$_0$) no produce una
   historia compatible interna;
7. el colapso del lema 8 no conmuta con una etapa sucesora o límite, o existe
   un real interno que no aparece en ningún nivel de índice menor que
   \(\omega_1^{\mathfrak G}\);
8. la selección \(\beta\mapsto w_\beta\) no es interna, uniforme o conserva
   el tipo de orden;
9. dos reales diferentes tienen el mismo par genealógico \((\beta,n)\) en
   (44), dos ordinales diferentes producen el mismo código en (47), o falla
   alguna de las inyecciones \(E,C,j_{\rm HMT},k_{\rm HMT}\);
10. existe una parte interna no numerable de la recta cuyo rango bajo
   \(j_{\rm HMT}\) sea acotado en \(\omega_1^{\mathfrak G}\);
11. alguna etapa utiliza CH, \(\mathbb R\), una constante objetivo, CODATA,
   PDG o una identificación física posterior para seleccionar una semilla,
   una ruta, un coeficiente o una prolongación.

Ninguna ejecución limitada a un número prefijado de cifras falsifica el
alcance de (38); lo falsificaría una ruptura efectiva de compatibilidad en
alguna profundidad. Ninguna notación conjuntista posterior prueba por sí sola
(49); lo prueban los lemas 7--8 y las dos inyecciones construidas desde la
genealogía.

### 15.11. Propietarios materiales y trazabilidad

La clasificación de procedencia es fórmula por fórmula:

- En (32), la cadena
  \(\mathrm{APP}\to\mathrm{TRIT}\to\mathrm{TPK}\to
  X_\infty^{\rm enr}\to\mathcal C_{\rm cont}^{\rm disc}\to m_\infty\)
  es `ARQUITECTURA_AUTORAL_PREEXISTENTE`; la flecha exacta
  \(m_\infty\to\mathfrak G_{\rm HMT}\) es `FORMALIZACION_NUEVA`.
- La prolongación, la cobertura y el límite que sustentan (34)--(35),
  (38)--(41) son `RESULTADO_RECUPERADO` y `FORMALIZACION_REUNIDA`; la
  definición exacta del árbol podado `surv`, su nivel raíz, las restricciones
  tipadas de \(\operatorname{Ext}^{\rm cal}\) y la normalización que evita el
  extremo en (41a) son `FORMALIZACION_NUEVA`.
- (33)--(33a), (36)--(37e), (41b)--(41c), (42)--(50):
  `FORMALIZACION_NUEVA` de obligaciones autorales previas.
- En (51), la plantilla relativa \(L[h]\) es histórica; la igualdad exacta
  \(\mathfrak G_{\rm HMT}=L[u]=L[h,m_\infty]\), su prueba y su posición
  causal posterior son `FORMALIZACION_NUEVA`.

Los propietarios y testigos materiales son:

1. [Generación coinductiva a profundidad arbitraria — c27](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex>) —
   SHA-256 `2be7acb93732f3939de6acc21fd8e0c686ce978c1ab4419aded1a6a00bcbc198`,
   líneas 159--320, 322--426, 554--640 y 642--675: prolongación, doble
   proyección, cuatrirrelación, cuantificador \(\forall N\) y las dos vías
   compatibles de \(\alpha\).
2. [Límite inverso, cinta ternaria y cociente real — base c18](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c18_sin_encabezado.tex>) —
   SHA-256 `3098d00f3e29e897fa80ac5a66ab874025853f651d8512887a4dfeea54844ca1`,
   líneas 23--141 y 436--586.
3. [Partición geométrica exhaustiva de cilindros](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/espirales/cap18_lector_radial_continuo.tex>) —
   SHA-256 `ff4dba45bed0a4e66ebd3fab2b53d91611837bc9e3106d56a68c060dda372c05`,
   líneas 582--658.
4. [Partición disjunta de historias por prefijo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b3_terminal_naturalidad_limite.tex>) —
   SHA-256 `b9d3353ceeb999b08b9b37993df6a0f70120715084bc3ca20d31bd005b1ba889`,
   líneas 830--867 y 1096--1102.
5. [Partición nonádica 729 y profundidad arbitraria](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex>) —
   SHA-256 `2ffc6046b34705cf6ebf4d258ac2938c83ca3b54219defb6c008e45e2fb58026`,
   líneas 369--475.
6. [Levantamiento uniforme y obligación de rango](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/RANGO_GENEALOGICO_TRES_CONDICIONES_20260910.md>) —
   SHA-256 `b889cf08c9d1fec126f4eb8869035cc153bf13b277801f1fa5aa1e61fe58d790`,
   líneas 35--130, 579--606 y 664--710; se usa como antecedente de la
   obligación y del selector uniforme, no como sustituto de la prueba actual.
7. [Plegado fiel, potencia y condensación explícita](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/PLEGADO_MEMORIA_CARDINALIDAD_20260910.md>) —
   SHA-256 `b7cc879988f4ddcd0b64a042fa4dd12b383467617d3b52d68bde777703272c7d`,
   líneas 388--480.
8. [Plantilla histórica de constructibilidad relativa — base c19](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/base_c19_sin_encabezado.tex>) —
   SHA-256 `39a5456c6af00e421e98c00a5550da243270e55391b484ca0f148fd7ec328ace`,
   líneas 442--484 y 595--665.

El cambio aportado aquí es prospectivo y acotado: (36)--(37e) materializan
la exhaustividad semántica sin confundirla con la ramificación finita; los
lemas 6--8 prueban codificación, modelo, enumeración y condensación;
(41a)--(41c) hacen explícita la cobertura de toda la potencia interna; y
(44)--(50) cierran las dos inyecciones y el cuantificador completo. No se
modifica ninguna fuente sellada ni se atribuye a una ejecución Python la
demostración cardinal.
