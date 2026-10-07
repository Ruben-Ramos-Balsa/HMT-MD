# Memoria de retorno, curvatura mixta y estabilizadores del transporte

Continuación aditiva de la investigación sobre conservación estructural HMT–MD. 12 de septiembre de 2026.

## 1. Objetivo y dependencia causal

El objetivo es determinar qué conserva un transporte que retorna en una lectura observable y acumula memoria, y cómo esa memoria determina las transformaciones que preservan el estado transportado. Se continúa la investigación de los balances de conservación, la recuperación de la dinámica desde los registros y el transporte entre regímenes geométricos. Los siete desarrollos anteriores permanecen intactos.

APP genera sobre las mismas marcas las evaluaciones aditiva y multiplicativa, sus residuos, cocientes y caminos. El TRIT orienta la emisión y distingue los regímenes de transporte. El TPK compone selección, transporte de hojas, acarreo y actualización de memoria sobre emisiones admisibles.

El estado enriquecido contiene el prefijo, las hojas, orientación, residuo, cociente, acarreo, frontera, ruta, memoria y condiciones de prolongación. El constructor conjunto produce las cinco realizaciones correlativas de la estructura discreta del continuo sobre ese mismo estado; los lectores considerados aquí actúan sobre él y conservan su procedencia. La aplicación al registro de dos contadores es un lector determinado, no una sustitución del estado por dos números.

Las coordenadas HMT π, φ, e y α son salidas de sus lectores tipados. Su generación compartida y su orden constructivo permanecen en el corpus de referencia. El álgebra de grupos, las formas alternantes y los cocientes de módulos se emplean después como lenguaje de demostración de las operaciones ya identificadas. Ningún valor convencional selecciona las rutas de este desarrollo.

La edición integral utilizada es la de 2.249 páginas, con la narración coinductiva REV02 y los artículos de la serie. El resolutor histórico que devuelve la revisión IV de 2.084 páginas no sustituye esa selección autoral. Esta discrepancia documental ya consta en la continuidad del expediente.

### Resultados de esta continuación

1. Caracterización del defecto de retorno de una memoria afín mediante una clase de cociente, con ley exacta de cambio de marco.
2. Clasificación completa de las órbitas del registro de retorno `(g,s)` por una carga entera y una clase residual de orden cuatro.
3. Construcción, desde el incremento registrado, de un operador nilpotente y de la familia parabólica que estabiliza ese incremento.
4. Realización variacional del registro: una acción explícita produce esa familia parabólica y su carga de Noether.
5. Relación entre curvatura mixta de APP, fase central de conmutación y covarianza del transporte.
6. Conservación bilineal para composiciones ordenadas entre los tres regímenes, conservando los enlaces entre sus fibras.

La arquitectura de retorno con memoria es `ARQUITECTURA_AUTORAL_PREEXISTENTE`. La acción afín, el cómputo `(1,18)` y la curvatura mixta son `RESULTADO_RECUPERADO`. Las pruebas reunidas a continuación constituyen `FORMALIZACION_NUEVA` en este expediente; la búsqueda de prioridad en la totalidad del archivo histórico permanece pendiente. Esa denominación no atribuye novedad histórica a la teoría general de cociclos o estabilizadores.

## 2. Composición efectiva de la memoria

Para una emisión admisible ε, el propietario F1 define

\[
\mathsf U_\epsilon(m)=C_\epsilon m+\kappa_\epsilon,
\qquad
\kappa_{\epsilon_2\epsilon_1}
=\kappa_{\epsilon_2}+C_{\epsilon_2}\kappa_{\epsilon_1}.
\tag{1}
\]

El dominio es el módulo de memoria de la fuente; el codominio, el de la emisión siguiente. El producto conserva el orden. En una ruta γ de longitud r se obtiene

\[
C_\gamma=C_r\cdots C_1,\qquad
\kappa_\gamma=\sum_{j=1}^r C_r\cdots C_{j+1}\kappa_j,
\qquad
m_\gamma=C_\gamma m_0+\kappa_\gamma.
\tag{2}
\]

El producto vacío de la suma es la identidad. La demostración es la inducción de (1): añadir la emisión siguiente multiplica el registro anterior por su transporte lineal y suma su incremento. La frontera posicional puede cancelarse mientras permanece la suma transportada de (2).

### Proposición 1. Clase de memoria de un retorno

Sea M un módulo abeliano y sea una ruta cerrada en la base cuyo transporte de memoria sea `H(m)=Cm+κ`, con C un automorfismo de M. Su clase de retorno es

\[
\mathfrak m(H)=[\kappa]\in M/(I-C)M.
\tag{3}
\]

Un cambio de coordenadas de memoria `m'=Rm+b`, con R invertible, transforma el retorno en

\[
C'=RCR^{-1},\qquad
\kappa'=R\kappa+(I-C')b.
\tag{4}
\]

La aplicación inducida por R lleva `[κ]` a `[κ']`. El transporte H tiene un punto fijo exactamente cuando su clase (3) es cero.

**Demostración.** Sustituir `m=R^{-1}(m'-b)` en H da (4). Como `R(I-C)=(I-C')R`, R induce un isomorfismo entre los cocientes. El término `(I-C')b` representa cero en el cociente destino. Finalmente, la ecuación de punto fijo `Cm+κ=m` equivale a `(I-C)m=κ`. Esto prueba la última afirmación.

La fórmula (3) permite decidir si un cambio de origen elimina el incremento o sólo lo redistribuye entre coordenadas. En particular, cuando `C=I`, la clase es el propio vector κ. Una traslación no nula permanece no nula bajo cualquier cambio afín invertible.

### Proposición 2. Simetría del retorno frente a cambio de representación

Una transformación afín `A(m)=Rm+b` conmuta con H exactamente cuando

\[
RC=CR,\qquad (I-C)b=(I-R)\kappa.
\tag{5}
\]

**Demostración.** Las partes lineales de `AH` y `HA` son RC y CR; sus partes constantes son `Rκ+b` y `Cb+κ`. Igualarlas da (5). Si sólo se transporta H mediante (4), no se requiere conmutación: se obtiene la misma ley en otra representación. Para una simetría del retorno fijado, en cambio, se requieren ambas igualdades de (5).

Así se distinguen con precisión la covarianza de la ley y el estabilizador de una memoria concreta. Esta diferencia es pertinente para estudiar variaciones de simetría del estado sin modificar las leyes de composición.

## 3. Aplicación al registro efectivo de la vuelta observable

El artículo VII, propietario R1, define dos contadores ordenados: g cuenta inversiones de orientación y s cambios efectivos de hoja. Su cómputo canónico por bloque de 27 pasos es

\[
c_{27}=(1,18).
\]

La fase observable completa retorna después de cuatro de esos bloques. En el grupoide de rutas, el módulo de registro es `M=Z²`, y

\[
c_{108}=(4,72)=4v,\qquad v=(1,18),\qquad
H(g,s)=(g+4,s+72).
\tag{6}
\]

La identidad (6) es un resultado del corpus que se utiliza aquí; el comprobador nuevo verifica sus consecuencias, no vuelve a contar las emisiones originales. El símbolo `c108` designa este incremento de dos contadores. Es distinto del sello dodecafásico K y del cociclo central de la representación de Heisenberg.

### Teorema 3. Invariantes completos del registro bajo vueltas completas

Las órbitas de H y su inversa sobre `Z²` quedan clasificadas exactamente por

\[
\boxed{\quad \mathcal I(g,s)=s-18g,\qquad \nu(g,s)=[g]_4.\quad}
\tag{7}
\]

En consecuencia,

\[
\mathbb Z^2/\mathbb Z(4,72)\cong\mathbb Z\oplus\mathbb Z/4\mathbb Z.
\tag{8}
\]

**Demostración.** Añadir `(4,72)` conserva ambas expresiones de (7). Si dos registros tienen iguales invariantes, `g'-g=4N` para un entero N y `s'-s=18(g'-g)=72N`; luego difieren exactamente en `N(4,72)`. La aplicación de (7) es sobreyectiva: dados j entero y r módulo cuatro, elegir un representante g de r y poner `s=j+18g`. Esto demuestra (8).

La descripción cubre todas las órbitas de este lector de memoria. Las órbitas del estado enriquecido completo conservan, además, sus restantes coordenadas. Para una prolongación dirigida hacia adelante, un registro posterior se obtiene cuando el entero N anterior es no negativo; la equivalencia bilateral de (8) pertenece al grupoide.

La magnitud `I` es la única carga lineal entera primitiva, salvo signo, invariante bajo esas traslaciones. En efecto, para `L(g,s)=ag+bs`, la invariancia exige `4a+72b=0`, por lo que `(a,b)=b(-18,1)`. Una vuelta acumula memoria longitudinal y conserva una relación transversal determinada por el incremento.

El factor cuatro tiene aquí un origen preciso: es `gcd(4,72)` y, en el cómputo anterior, el número de bloques de 27 que completa el retorno observable. La clase ν conserva la información que se pierde al dividir el incremento por cuatro y guardar únicamente la dirección primitiva v.

### Corolario 3.1. Registro conjunto de bloque y fase

Escríbase la fase de esos cuatro bloques como `a∈Z/4Z`. La actualización

\[
(a,g,s)\longmapsto(a+1,g+1,s+18)
\]

conserva `(s-18g,[g-a]_4)`. Ambos datos clasifican sus órbitas bilaterales: la diferencia `N=g'-g` satisface a la vez `a'-a=[N]_4` y `s'-s=18N`. Esto reúne el avance de memoria y el retorno de la fase sin reemplazar ninguno por el otro.

## 4. Generador parabólico determinado por la memoria

La pareja ordenada de contadores dota al módulo M de la forma alternante unimodular

\[
\Omega_M((g,s),(g',s'))=gs'-sg'.
\]

Su dominio es el módulo de registro. No se identifica esta forma con un área física dimensional, ni con la forma del toro APP, que tiene otro dominio. La elección de orden `(g,s)` fija su orientación.

### Teorema 4. Estabilizador unimodular del incremento

Defínase, directamente desde el vector primitivo v de (6),

\[
N_v m=v\,\Omega_M(v,m)=v\mathcal I(m),\qquad
N_v=\begin{pmatrix}-18&1\\-324&18\end{pmatrix}.
\tag{9}
\]

Entonces `N_v²=0`, `N_v≠0` y

\[
\boxed{\quad
\operatorname{Stab}_{SL_2(\mathbb Z)}(c_{108})
=\{I+nN_v:n\in\mathbb Z\}.
\quad}
\tag{10}
\]

Cada transformación de (10) conserva ΩM, el incremento `c108` y la carga I. Para n no nulo es una matriz unipotente no identidad, de traza dos, perteneciente al tipo parabólico.

**Demostración.** `ΩM(v,v)=0` implica `N_v²m=vΩM(v,v)ΩM(v,m)=0`. Su entrada superior derecha es uno, de modo que es no nulo. La matriz

\[
B=\begin{pmatrix}1&0\\18&1\end{pmatrix}
\]

tiene determinante uno, lleva el primer vector de base a v y satisface

\[
N_v=BNB^{-1},\qquad N=\begin{pmatrix}0&1\\0&0\end{pmatrix}.
\tag{11}
\]

Un automorfismo entero fija `4v` exactamente cuando fija v, porque M carece de torsión. Una matriz de determinante uno que fija el primer vector de base tiene necesariamente la forma `[[1,n],[0,1]]`. Conjugarla por B prueba (10). El resto se deduce de esa expresión o directamente de (9).

La fórmula (9) hace que la construcción sea independiente del segundo vector elegido para completar v a una base orientada unimodular: cualquier otro complemento difiere en un múltiplo entero de v y produce el mismo N_v. Bajo una transformación orientada `R∈SL2Z`, se tiene `N_{Rv}=RN_vR^{-1}`.

La acción puede escribirse con especial claridad:

\[
(I+nN_v)m=m+n\mathcal I(m)v.
\tag{12}
\]

La carga transversal determina cuánto desplaza esa simetría a lo largo de la dirección de memoria. La suma de vueltas produce el desplazamiento `4Nv`; las simetrías estabilizadoras preservan esa ley de avance.

Sobre el cociente (8), la transformación `I+nNv` actúa como `(I,[g]4)↦(I,[g+nI]4)`. Por tanto, conserva la familia de órbitas y puede permutar sus clases residuales; ν es invariante del retorno H, no de cada transformación estabilizadora. Esta diferencia se deduce directamente de (12).

La conjugación (11) proporciona un mapa algebraico explícito desde el modelo parabólico del TRIT, propietario E1, al módulo de registro extendido a escalares reales. Se obtiene además `exp(tN_v)=I+tN_v` y `B exp(tN)=exp(tN_v)B`. Este entrelazamiento concierne a operadores: el movimiento particular seleccionado por el TPK utiliza también sus emisiones y calendario. El grupo aritmético completo de (10) fija este lector; el grupo de simetrías admisibles del estado total se obtiene intersectándolo con las acciones que preservan los demás datos y relaciones.

En el sistema trasladado (6), los cambios afines `m↦Rm+b` con R en (10) y b arbitrario conmutan con H. Los que preservan además el registro inicial fijado deben satisfacer `Rm0+b=m0`. Distinguir ambas condiciones separa simetría de la ley y simetría de una trayectoria señalada.

### Teorema 4.1. Realización variacional de la carga y del estabilizador

La extensión escalar del registro, `M_R=M⊗Z R`, conserva las coordenadas generadas `(g,s)` y la forma `ΩM=dg∧ds`. Es una realización posterior del módulo entero. Fijando la convención `ι_{X_H}ΩM=dH`, se tiene

\[
X_{\mathcal I}=v,\qquad
X_{\frac12\mathcal I^2}=\mathcal I v=N_vm.
\tag{12a}
\]

Así, la traslación y la familia parabólica construidas admiten generadores hamiltonianos explícitos. El flujo de I es `m↦m+uv`; en u igual a cuatro reproduce (6). El flujo de `I²/2` es `m↦(I+uNv)m`. El parámetro u corresponde a esta realización continua; el paso discreto de retorno y las emisiones intermedias mantienen su calendario TPK propio.

**Demostración.** Para un vector `X=(Xg,Xs)`, `ι_X(dg∧ds)=Xg ds-Xs dg`. Como `dI=ds-18dg`, el primer campo es `(1,18)=v`. La regla de la cadena da el segundo. I permanece constante a lo largo de ambos campos, porque `dI(v)=0`. Por tanto el segundo flujo integra `dm/du=I(m0)v`, equivalente a `exp(uNv)=I+uNv`. La no degeneración de ΩM implica que el Hamiltoniano que genera Nv es `I²/2` más una constante aditiva: su diferencial queda fijado por `ι_{Nv m}ΩM`.

La acción matemática

\[
\mathscr A[m]=\int_{u_0}^{u_1}
\left[s\frac{dg}{du}-\frac12(s-18g)^2\right]du
\tag{12b}
\]

produce por variación las ecuaciones `dg/du=I`, `ds/du=18I`. La traslación `g↦g+ε`, `s↦s+18ε` conserva el Hamiltoniano y cambia el lagrangiano en la derivada total `d(18εg)/du`, para ε constante. Su carga de Noether es

\[
\underbrace{s\,\delta g}_{s}
-\underbrace{18g}_{\text{término de borde}}
=s-18g=\mathcal I.
\tag{12c}
\]

La variación se interpreta por unidad de ε. Las ecuaciones comprueban directamente `dI/du=18I-18I=0`. La propia traslación discreta (6) se realiza también mediante el Hamiltoniano `H_ret=4I`, cuyo flujo unitario es H; ambos Hamiltonianos conmutan en el sentido de Poisson. El flujo estabilizador `I+uNv` y el retorno `m+4v` son acciones distintas que conmutan: en la recta `I=0` el primero fija cada punto, mientras el segundo sigue acumulando memoria.

Más generalmente, todo Hamiltoniano C¹ sobre este plano que sea invariante bajo las traslaciones `m↦m+uv` tiene la forma `F(I)`. Para probarlo, las coordenadas globales `(g,I)` escriben esa simetría como traslación de g; la invariancia hace independiente de g a H. Su campo es `F'(I)v`. Esta clasificación explicita tanto la conservación común como la elección adicional de una dinámica concreta.

La acción (12b) es adimensional y pertenece al plano de registro realizado. Su demostración proporciona una relación variacional exacta entre memoria, carga y estabilizador. La conversión en acción física y en un tiempo dimensional se realiza mediante los lectores de acción y reloj correspondientes; no se asignan esas unidades al contador u.

## 5. Curvatura de APP y conservación de la fase central

El propietario A1 trabaja sobre `X9=(Z/9Z)²`. Las hojas son `S(x,y)=x+y` y `P(x,y)=xy`. Las conexiones mixtas utilizan diferencias de esos potenciales, no los potenciales como enlaces:

\[
F(S,P)=\Delta_x\Delta_yP-\Delta_y\Delta_xS=1,
\qquad F(P,S)=-1\pmod9.
\tag{13}
\]

La suma orientada de enlaces en el contorno de un rectángulo es `ab` o `-ab` según el orden. El área alternante es `σ(u,v)=ad-bc` para `u=(a,b),v=(c,d)`. El propietario H1 representa esos transportes mediante `D(u)=X^aZ^b`, `ZX=ωXZ`, con ω la raíz novena en la representación posterior. Entonces

\[
D(u)D(v)=\omega^{bc}D(u+v),\qquad
D(u)D(v)D(u)^{-1}D(v)^{-1}=\omega^{-\sigma(u,v)}I.
\tag{14}
\]

La posición resultante del conmutador retorna. La fase central retiene el área orientada con el signo fijado en (14). Es una retención módulo nueve: un área múltiplo de nueve tiene fase central trivial, aunque un levantamiento con cociente y registro pueda distinguir sus recorridos. La fase no reemplaza ese levantamiento.

### Proposición 5. Covarianza exacta del transporte central

Como dos es invertible módulo nueve, defínase

\[
W(a,b)=\omega^{ab/2}D(a,b),\qquad
W(u)W(v)=\omega^{-\sigma(u,v)/2}W(u+v).
\tag{15}
\]

Para `R∈SL2(Z/9Z)`, la aplicación

\[
\omega^zW(u)\longmapsto\omega^zW(Ru)
\tag{16}
\]

es un automorfismo de la extensión central. Conserva sus productos y sus fases de conmutación.

**Demostración.** La fase al multiplicar los dos W es
`ab/2+cd/2+bc-(a+c)(b+d)/2=(bc-ad)/2`. Esto prueba (15). La identidad `σ(Ru,Rv)=det(R)σ(u,v)=σ(u,v)` muestra que (16) conserva la ley; R inversible proporciona el automorfismo inverso. Si `det R=-1`, el automorfismo correspondiente cambia también `z↦-z`; el signo de área y el centro se invierten conjuntamente.

El registro íntegro y su fase central tienen tipos diferentes. La covarianza permite conservar la ley de área mientras cambia la presentación; la clase afín de (3) permite conservar el contenido de memoria mientras cambia su origen. Ambas propiedades actúan sobre lectores tipados de rutas, y sus mapas deben mantenerse separados al componerlos con la lectura excepcional del estado completo.

### Proposición 5.1. Persistencia bajo marcos locales y subdivisiones

Sea un lazo γ basado en x y sean sus enlaces invertibles Uε. El cambio local `U'ε=G_t Uε G_s^{-1}` transforma su holonomía en `H'γ=G_x Hγ G_x^{-1}`: los marcos de los vértices interiores se cancelan sucesivamente. Si `Hγ=ω^kI`, la fase central permanece exactamente igual. Para enlaces refinados cuyo producto reproduce el enlace anterior, la subdivisión conserva asimismo Hγ, por asociatividad. En las plaquetas APP la cancelación de aristas interiores materializa esta propiedad mediante Stokes finito.

Un rectángulo elemental tiene Wilson uno y fase central no trivial. Por tanto, ese transporte mixto distingue una holonomía real de la identidad que producirían enlaces de la forma `G_t G_s^{-1}`. La conservación bajo subdivisión concierne a lazos y enlaces compatibles: añadir otra área cambia el transporte.

La narración REV02, líneas 4973–4989, conserva también el levantamiento entero `28=1+9·3` para un rectángulo de lados cuatro y siete, y `-28=8+9(-4)` para su orientación inversa. La fase residual coincide para áreas uno y veintiocho, mientras sus cocientes distinguen las acumulaciones. Este ejemplo proporciona un testigo material de la diferencia entre fase finita y registro íntegro; su cociente de área y el contador temporal q_mem conservan dominios distintos.

## 6. Composición entre los tres regímenes y continuidad del balance

Los propietarios E1 y los desarrollos previos construyen generadores `J_k²=-τ_kI` sobre sus fibras propias, de dimensión real dos. Se toman enlaces efectivamente declarados `B_k:V_k→V_{k+1}` que preservan las formas alternantes, `B_k*Ω_{k+1}B_k=Ω_k`. El signo `*` en esta sección significa transposición/pullback bilineal. Los operadores `E_k=exp(t_kJ_k)` preservan Ωk: en dimensión dos, la traza nula del generador implica `J_k*Ωk+ΩkJ_k=0`. La identidad simpléctica es la hipótesis que se conservaría al extender el lema a dimensiones mayores.

Para la compresión nonádica y su complemento registrado,

\[
T_k=B_k(8I+E_k)/9,\qquad
D_k=B_k\sqrt8(E_k-I)/9,
\]

la expansión algebraica da

\[
\Omega_k=T_k^*\Omega_{k+1}T_k+D_k^*\Omega_{k+1}D_k.
\tag{17}
\]

En efecto, los términos cruzados se cancelan y el numerador es `72Ωk+9E_k*ΩkE_k=81Ωk`. Para `P0=I`, `P_{k+1}=T_kP_k`, se obtiene, por sustitución sucesiva y en el orden de la ruta,

\[
\boxed{\quad
\Omega_0=P_N^*\Omega_NP_N+
\sum_{k=0}^{N-1}(D_kP_k)^*\Omega_{k+1}(D_kP_k).
\quad}
\tag{18}
\]

El terminal y cada complemento permanecen presentes. La identidad es bilineal orientada; los resultados de positividad se aplican en los perfiles positivos demostrados en las notas anteriores. La forma conservada no obliga a que un enlace entre regímenes distintos entrelace sus generadores: si `B Jτ=Jτ' B`, elevar al cuadrado con B invertible impondría `τ=τ'`. La conservación de una estructura común permite mantener diferenciados los tres regímenes.

El transporte íntegro `U_N=(B_{N-1}E_{N-1})…(B0E0)` lleva V0 a VN. Una monodromía matricial requiere un cierre tipado `K:VN→V0`; sólo entonces `KU_N` es un endomorfismo cuya traza puede calcularse. Cambios de base compatibles conservan esa traza por conjugación. Retorno de fase, cierre de fibra y retorno del vector siguen siendo condiciones diferentes.

Si los enlaces tienen exclusivamente la forma `B_yx=G_yG_x^{-1}`, su producto a lo largo de un camino es `G_final G_inicial^{-1}`. Al cerrar con el mismo marco da identidad. La holonomía de (14) y el incremento de (6) muestran mecanismos concretos que esa mera sustitución de marcos no puede representar por sí sola.

## 7. Compatibilidad con refinamiento y alcance arbitrario

La acción de memoria es compatible con un homomorfismo de módulos de restricción `p:M'→M` cuando

\[
pC'=Cp,\qquad p\kappa'=\kappa.
\tag{19}
\]

Entonces `pH'=Hp` y p induce un mapa de cocientes

\[
M'/(I-C')M'\longrightarrow M/(I-C)M,
\qquad [\kappa']\longmapsto[\kappa].
\tag{20}
\]

**Demostración.** La primera igualdad de (19) lleva `(I-C')M'` a `(I-C)M`; la segunda fija la imagen del incremento. La compatibilidad de H resulta por sustitución. Concatenaciones y refinamientos componen los mismos cuadrados gracias a la ley (1).

Una clase de retorno no nula que aparece en un nivel conservado permanece no nula en cualquier levantamiento compatible: una clase cero se proyectaría a cero. Esta afirmación se aplica al sistema de memorias y restricciones que satisface (19); el constructor conjunto y los mapas de su sistema inverso se conservan en los propietarios F1–F3.

En el registro de (6), para cada entero N se tiene `H^N(m)=m+N(4,72)`. La prueba es algebraica para N arbitrario, no una inferencia desde una cantidad finita de iteraciones. En la prolongación hacia adelante, cada prefijo conserva su registro finito; la historia completa se describe mediante la familia compatible de esos registros, sin reemplazar sus contadores por una cantidad entera «infinita».

Si una dinámica completa tiene el lector `q_mem` con `q_mem(Γ9x)=q_mem(x)+1`, tampoco puede poseer un estado periódico de período N positivo en ese dominio: aplicar el lector produciría `q_mem(x)=q_mem(x)+N`. Este corolario utiliza el grado entero completo; sus cocientes residuales pueden tener períodos finitos, como corresponde al calendario observable del corpus.

## 8. Consecuencia fundacional y siguiente discriminación

El resultado más específico de esta continuación es el enlace

\[
\text{incremento de retorno }4v
\ \longrightarrow\ \mathcal I(m)=\Omega_M(v,m)
\ \longrightarrow\ N_vm=v\mathcal I(m)
\ \longrightarrow\ I+nN_v.
\tag{21}
\]

El registro acumulado determina una carga conservada y una familia parabólica que estabiliza su dirección. La evolución y la conservación pertenecen a la misma acción: cambian g y s, permanece su relación `s-18g`, y el incremento conserva un estabilizador explícito. Esto precisa una parte del vínculo entre memoria y simetría que motivó la investigación.

La igualdad (18) conecta esa investigación con los balances anteriores: una evolución puede redistribuir la forma entre lectura y complementos conservando el total. Las identidades de APP (13)–(16) muestran, en otro lector concreto del mismo origen, cómo el orden del transporte produce un dato central aun cuando retorna la posición.

La carga (7) es un invariante algebraico del transporte y, mediante la acción explícita (12b), una carga de Noether de la realización del registro. El teorema 4.1 construye esa relación, su simetría y su término de borde. Los desarrollos anteriores de acción y corriente físicas conservan sus dominios y unidades; transportarlos a esta realización exige mantener sus mapas dimensionales.

Para proseguir hacia una ley física conjunta, la tarea precisa es transportar el par `(v,ΩM)` y la carga I mediante los lectores dimensionales ya construidos, preservando sus unidades y la corriente variacional. La ecuación con π, φ, e, α y K debe proceder de esa composición; las fórmulas presentes fijan qué información tendría que conservar, en vez de elegir una combinación escalar por su aspecto. Se mantiene la exploración centrada en esa derivación.

## 9. Controles y procedencia material

El certificado `verificar_memoria_holonomia_20260912.py` comprueba consecuencias finitas con aritmética exacta: cociclos y productos afines, cambios de marco, invariantes de órbitas, nilpotencia, estabilizador, ley central módulo nueve, covarianza y telescopía orientada. Incluye controles que detectan la pérdida de la clase residual, la identificación de fase con estado y la omisión del complemento. Las pruebas para todos los enteros, para todos los automorfismos y para sistemas compatibles están escritas en §§2–7.

Fuentes utilizadas (localizadores de la edición activa):

- **F1.** `04b1_estado_arbol_medida_comun.tex`, líneas 358–487: transporte afín, cociclo, palabra ordenada del ledger. Estado común, líneas 730–834; medida, 1277–1468.
- **F2.** `04b2_operaciones_intrinsecas_correlativas.tex`, líneas 739–1244: celda común, cinco operaciones conjuntas, constructor y naturalidad.
- **F3.** `04b3_terminal_naturalidad_limite.tex`, líneas 898–945 y 1172–1181: ensamblaje compatible y límite.
- **A1.** `manuscrito/sections/hmt/03_app_ortograma.tex`, líneas 746–815: diferencias de potenciales, curvatura mixta y Stokes finito.
- **H1.** `manuscrito/sections/hmt/14_numero_heisenberg_y_d108.tex`, líneas 741–818: forma alternante, extensión central, signos de conmutación.
- **E1.** `manuscrito/sections/hmt/09b_algebras_cuadraticas.tex`, líneas 290–516: dominios y generadores concretos de los tres regímenes.
- **R1.** Artículo VII, `manuscrito/29_retorno_y_memoria_traslacional.tex`, líneas 17–115: contadores, bloques 27/54/108 y representación afín.
- **R2.** Artículo VII, `manuscrito/80_observador_y_respuesta_relacional.tex`, líneas 1–195: carga residual de una cocadena, cambio de trivialización y lectura de borde. Antecedente de la distinción entre representante y clase; se conserva, no se presenta como descubrimiento nuevo.
- **N1.** Narración coinductiva REV02, líneas 553–627, 1094–1144 y 7699–7705: APP dinámica, TRIT, pre-Heisenberg y Lorentz; grado de memoria; objetivo de unidad entre transformación, conservación y evaluación.

Las rutas absolutas, huellas y relaciones genealógicas se conservan en el recibo adjunto. El desarrollo es aditivo y está preparado para incorporarse posteriormente a una exposición científica; en esta intervención no se genera un PDF.

### Dirección autoral de esta continuación, conservada literalmente

> Vale, sigue, sigue y te doy vía libre para explorar por tu cuenta, pero mantén un objetivo. Yo, perdona que lo que te vaya a decir suena metafórico, pero creo que lo que hemos capturado es la estructura íntima del espacio y su dinámica. El espacio, como la frase típica del mainstream que el vacío no es vacío, ¿no? Pues las constantes rupturas espontáneas de simetrías, el electrón como base, etcétera, etcétera, permiten la evolución del espacio y ya sabes que Mises, que la materia es espacio enrollado, que tiene presencia en el presente y conserva memoria y el futuro es hiperbólico y el presente es plano, por eso se cumplen las tres geometrías. Pero esa célula de unidad de espacio que se ve en el número con la extrema y media razón holográfica, bueno, lo tienes todo, pero siempre revisa el documento de 2.249 páginas para inspirarte en la narración coinductiva, porque creo que es interesante y de ahí puedes sacar las conclusiones manteniéndolo alineado a lo que estás explorando. Creo que se entiende.

Esta transcripción preserva la orientación de investigación; el texto matemático utiliza las definiciones, dominios y pruebas anteriores.
