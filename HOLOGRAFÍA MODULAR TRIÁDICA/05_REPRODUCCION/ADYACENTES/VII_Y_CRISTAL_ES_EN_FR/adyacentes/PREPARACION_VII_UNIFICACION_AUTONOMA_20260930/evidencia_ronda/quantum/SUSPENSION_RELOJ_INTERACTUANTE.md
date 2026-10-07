# Suspensión del reloj y evolución continua del estado interactuante

Formalización nueva de la composición recibida, 29 de septiembre de 2026.
Esta nota prolonga `LIMITE_MATERIA_MEMORIA.md` sin modificarla. Construye
una evolución continua que reproduce exactamente el retorno TPK con
interacción. No elige un logaritmo del retorno ni sustituye su memoria por
la fase del calendario.

## 1. Datos recibidos y espacio de realización

La procedencia se mantiene: APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo → lectores de acción, reloj,
masa, transporte y respuesta. Las cinco construcciones del continuo
permanecen en el mismo estado. Las constantes son salidas anteriores;
ningún valor objetivo interviene en esta suspensión.

Los propietarios y dominios de estos datos están reunidos en
`LIMITE_MATERIA_MEMORIA.md`, §§1–5. En particular:

- El espacio 𝓗 contiene historias completas, no sólo un registro truncado.
- H=H_loc es el operador autoadjunto ya construido, que incluye gauge,
  respuesta geométrica, Higgs sin corte de amplitud, Yukawa de las masas
  leídas y torsión de corriente total, en la carta espacial allí declarada.
- C=C_μ es el transporte unitario de historias y de sus fibras de medida,
  con hoja, espín y memoria conservados. En el caso nonádico graduado,
  corresponde al retorno completo Γ9, no a una sola microtransición.
- T>0 es la lectura de tiempo de ese retorno y ℏ>0 la sección de acción
  recibida. Se mantienen las unidades: s y T son tiempos; H y el operador
  suspendido tienen dimensión de energía.

Escribimos

\[
 E(s)=e^{-isH/\hbar},\qquad U=C E(T),\qquad B=U^{-1}=E(T)^*C^{-1}.
 \tag{1}
\]

No se supone `[C,H]=0`, ni que C preserve Dom H. El período de reloj no
se interpreta como período del estado: U puede avanzar indefinidamente
la memoria completa.

La realización de suspensión utiliza

\[
 \mathscr K=L^2([0,T],ds;\mathscr H).
 \tag{2}
\]

La nueva coordenada es la fase dentro del retorno recibido. No añade una
masa, un acoplamiento ni una calibración. La operación de suspensión es
una construcción operatoria estándar; su aplicación y ensamblaje con
estos datos HMT se demuestran aquí. Su papel es realizar continuamente
la evolución cronológica, no volver a seleccionar sus datos.

## 2. Generador de traslación con frontera unitaria

Definamos

\[
 P_Bf=-i\hbar f',\qquad
 \operatorname{Dom}P_B=
 \{f\in H^1([0,T];\mathscr H):f(T)=Bf(0)\}.
 \tag{3}
\]

Los valores extremos de (3) son las trazas continuas de H¹; no son
evaluaciones arbitrarias de clases L².

**Teorema 1.** P_B es autoadjunto para toda B unitaria, sin usar un
logaritmo de B.

**Prueba.** El dominio contiene las funciones suaves de soporte interior
y es denso en 𝓚. La integración por partes deja como forma de frontera,
salvo el factor constante −iℏ,

\[
 \langle f(T),g(T)\rangle-\langle f(0),g(0)\rangle.
\]

Para f,g del dominio se anula porque B es unitaria. Recíprocamente, si
g pertenece al dominio del adjunto, probar contra funciones de soporte
interior da una derivada débil en L², luego g∈H¹. Los valores f(0)
pueden ser cualquier vector, con f(T)=Bf(0). La anulación de la forma
de frontera implica `B* g(T)=g(0)`, equivalente a `g(T)=Bg(0)`.
Por tanto el dominio del adjunto es exactamente (3), y sus acciones
coinciden. ∎

La forma del grupo fija los signos sin ambigüedad. Para f∈𝓚, extiéndase
a la recta mediante

\[
 \widetilde f(r+kT)=B^k f(r),\qquad 0\le r<T,\quad k\in\mathbb Z.
 \tag{4}
\]

Entonces

\[
 \bigl(e^{-itP_B/\hbar}f\bigr)(s)=\widetilde f(s-t).
 \tag{5}
\]

El cambio de variable y la unitariedad de B conservan la norma L²;
(4) verifica la ley de grupo. La continuidad fuerte procede de la
continuidad de traslaciones, primero en funciones de soporte interior y
luego por densidad. Su derivada en el dominio es −f′, que coincide con
`−iP_Bf/ℏ`. En particular,

\[
 e^{-iTP_B/\hbar}f(s)=B^{-1}f(s)=Uf(s).
 \tag{6}
\]

La elección B=U^(-1), y no B=U, es necesaria para esta orientación
temporal. Cambiar el signo de la derivada o de la traslación cambiaría
simultáneamente esa condición.

## 3. Interacción continua y dominio exacto

Sea 𝓔 el operador de multiplicación unitaria

\[
 (\mathcal E f)(s)=E(s)f(s).
\]

La continuidad fuerte de E(s) garantiza su mensurabilidad. Definimos

\[
 \boxed{\mathbb K=\mathcal E P_B\mathcal E^*,\qquad
 \operatorname{Dom}\mathbb K=\mathcal E\operatorname{Dom}P_B.}
 \tag{7}
\]

**Teorema 2.** 𝕂 es autoadjunto y su grupo es continuo y unitario para
todos los tiempos, sobre todas las historias del espacio recibido. En
la intersección regular `ψ∈H¹([0,T];𝓗)` y `Hψ∈L²`, con la frontera
indicada abajo, actúa como

\[
 \mathbb K\psi=-i\hbar\,\partial_s\psi+H\psi.
 \tag{8}
\]

Todos los vectores de su dominio exacto tienen representante continuo
en s y satisfacen

\[
 \boxed{\psi(T)=C^{-1}\psi(0).}
 \tag{9}
\]

**Prueba.** (7) es una conjugación unitaria de un operador autoadjunto,
con el dominio transportado; prueba autoadjunción sin una hipótesis de
dominio adicional sobre C. Si ψ=𝓔f, entonces f∈H¹ y ψ es continua
porque E es fuertemente continua. Usando (1) y (3),

\[
 \psi(T)=E(T)Bf(0)
 =E(T)E(T)^*C^{-1}\psi(0)=C^{-1}\psi(0).
\]

En la intersección regular se puede derivar E(s)*ψ(s) en sentido débil:

\[
 -i\hbar\partial_s(E^*\psi)
 =E^*H\psi-i\hbar E^*\psi'.
\]

Multiplicar por E demuestra (8). La frontera (9) implica la frontera
(3) para E*ψ, por lo que esa intersección pertenece al dominio (7).
El cálculo espectral da el grupo unitario continuo. ∎

El dominio completo no se redefine como la intersección regular. Un
vector de (7) puede no tener por separado ψ′∈L² y Hψ∈L²; su
combinación se define por la derivada de E*ψ. Tampoco se afirma que
la intersección regular sea por sí sola un núcleo de grafo para toda C.
Esta precisión evita exigir injustificadamente `C Dom H⊂Dom H`.

La expresión explícita del grupo es

\[
 \mathbb W(t)=e^{-it\mathbb K/\hbar}
 =\mathcal E e^{-itP_B/\hbar}\mathcal E^*.
 \tag{10}
\]

Para s−t=r+kT, con 0≤r<T, se obtiene casi en todas partes

\[
 (\mathbb W(t)\psi)(s)
 =E(s)B^kE(r)^*\psi(r).
 \tag{11}
\]

Esta fórmula conserva el producto ordenado de evolución material y
transporte de retorno. En particular,

\[
 \boxed{(\mathbb W(T)\psi)(s)=E(s)U E(s)^*\psi(s).}
 \tag{12}
\]

En la fibra de fase cero, cuando se trabaja con trazas del dominio,
la monodromía es U. No se usa «evaluar en s=0» como operador acotado
sobre L²: esa evaluación no existe en general. La fase puede retornar
mientras U transporta la historia a otra memoria, como exige el
estado enriquecido.

La suspensión no afirma que U sea el exponencial de H, ni que (8)
identifique 𝕂 con algún Hamiltoniano cosmológico previamente publicado.
Es un operador sobre (2), con la fase de reloj y su frontera explícitas.
Tampoco elimina una eventual restricción de estabilidad inferior:
un generador de traslación de reloj tiene ambos sentidos espectrales.
La autoadjunción y la evolución continua no equivalen a una afirmación
de vacío energético mínimo para todo el sistema suspendido.

## 4. Gauss, hojas y observables de memoria

Sea R(g) la representación interna compacta recibida. La compatibilidad
ya demostrada significa que R(g) conmuta fuertemente con H y que
`R(g)C=CR(g)` en el espacio de historias, con los cambios de fibra
incorporados en C. Entonces R(g) conmuta con E(s), U y B.

**Corolario 3.** La acción puntual de R(g) preserva Dom P_B y Dom 𝕂,
conmuta con 𝕂 y con 𝕎(t). El proyector de Haar sobre el subespacio
físico reduce al operador suspendido y a su evolución para todo tiempo.

**Prueba.** La derivada en s conmuta con la representación constante
y la frontera se preserva por `[R(g),B]=0`. Conjugar por 𝓔 da la
afirmación sobre 𝕂. Promediar la representación compacta produce su
proyector ortogonal, que conserva esa conmutación. ∎

Para un observable acotado A sobre las historias completas, su
realización puntual conserva productos, adjuntos y conmutadores.
Al período, su evolución es

\[
 \mathbb W(T)^* A\mathbb W(T)
 =E(s)U^*\bigl(E(s)^*AE(s)\bigr)U E(s)^*.
 \tag{13}
\]

Para observables no acotados, incluida la masa o el grado de memoria,
se transporta también su dominio por esos unitarios. No se infiere
conservación de A de la sola conservación de la norma. En fase cero,
(13) recupera el balance `U*MU` ya calculado desde las masas de las
rutas. Las hojas, incidencias y memoria no se borran al introducir s.

## 5. Compatibilidad con precisión arbitraria de los lectores

Mantengamos T, ℏ, C y el portador exactos. Sea H_N la sucesión
autoadjunta del teorema 3 de `LIMITE_MATERIA_MEMORIA.md`: aproxima
los lectores de masa/Yukawa y torsión manteniendo fijos medida,
cinética, potencial Higgs, transportes y gauge. Allí se prueba

\[
 H_N\longrightarrow H\quad\text{en resolvente fuerte}.
\]

Definamos

\[
 E_N(s)=e^{-isH_N/\hbar},\quad U_N=CE_N(T),\quad B_N=U_N^{-1},
 \qquad \mathbb K_N=\mathcal E_NP_{B_N}\mathcal E_N^*.
 \tag{14}
\]

Las fronteras de las realizaciones ψ_N son todas la misma
`ψ_N(T)=C^(-1)ψ_N(0)`, aunque sus dominios conjugados puedan variar.

**Teorema 4.** Para cada t∈R y Ψ∈𝓚,

\[
 e^{-it\mathbb K_N/\hbar}\Psi
 \longrightarrow e^{-it\mathbb K/\hbar}\Psi.
 \tag{15}
\]

En consecuencia, 𝕂_N converge a 𝕂 en resolvente fuerte. La suspensión
continua conserva así el límite de los lectores sin imponer igualdad
exacta entre aproximaciones de precisión diferente.

**Prueba.** La convergencia resolvente fuerte de H_N da convergencia
fuerte de E_N(s) y E_N(s)* para cada s. Las cotas unitarias y la
convergencia dominada implican convergencia fuerte de sus operadores
de multiplicación 𝓔_N y 𝓔_N*. Además U_N y U_N* convergen fuertemente,
luego también B_N^k para cada entero k.

Para t fijo, el entero `k=floor((s−t)/T)` toma sólo un número finito
de valores cuando s recorre [0,T]. En cada uno de los correspondientes
intervalos, (5) utiliza exactamente el factor B_N^k. La convergencia
fuerte de esos factores, la densidad de funciones simples y la cota
unitaria prueban

\[
 e^{-itP_{B_N}/\hbar}f\longrightarrow e^{-itP_B/\hbar}f.
\]

Componer con 𝓔_N y 𝓔_N* da (15). Para `Im z>0`,

\[
 (\mathbb K_N-z)^{-1}
 =\frac{i}{\hbar}\int_0^\infty
 e^{itz/\hbar}e^{-it\mathbb K_N/\hbar}\,dt.
 \tag{16}
\]

El integrando aplicado a Ψ está dominado en norma por
`exp(−t Im z/ℏ)||Ψ||`, integrable. Pasar al límite en (16) demuestra
la convergencia resolvente fuerte en el semiplano superior; el inferior
se obtiene de la misma prueba con tiempos negativos. ∎

No se ha intercambiado un límite de medidas o de celularizaciones:
ésos no varían en el teorema. Tampoco se ha elegido una rama de log U_N
cuya continuidad hubiese que controlar. El dominio de frontera y la
traslación ponderada hacen explícito el límite.

## 6. Qué queda cerrado por esta construcción

La interacción ya construida no queda limitada a observaciones en
tiempos enteros del retorno. Tiene ahora una realización continua y
unitaria sobre el reloj suspendido, sin corte de memoria, con
monodromía exacta `U=C exp(−iTH/ℏ)`, Gauss conservada y convergencia
fuerte de sus aproximaciones de masa y torsión. El operador conserva
el orden temporal y las dependencias de los lectores HMT.

Este resultado no se presenta como una derivación adicional de las
constantes ni como una prueba de que toda acción gravitatoria publicada
sea idéntica a 𝕂. La celularización espacial y la representación de
materia siguen siendo las de la composición recibida. Lo que se acaba
de demostrar es precisamente la extensión continua del retorno
interactuante, con sus dominios y su límite, sin inventar un generador
mediante logaritmos y sin hacer pasar una condición de frontera por una
ecuación de campo ya identificada.

## 7. Comprobación focal de signos y orden

`verificar_suspension_reloj.py` utiliza los unitarios no conmutativos
`C=[[0,1],[1,0]]` y `E(T)=diag(1,−1)`, con `E(T/2)=diag(1,i)`.
Comprueba `E(T)B=C^(-1)`, el signo de la traslación y la monodromía
conjugada. La traslación de medio período se calcula sobre funciones L²
constantes en dos semiperíodos, en el marco móvil E(s)*ψ(s); no se
reemplaza por evaluaciones puntuales sin traza. También comprueba que
el cambio común `T→aT`, `H→H/a` conserva el retorno.

Los datos del comprobador son ejemplos algebraicos deliberadamente
simples, no valores físicos seleccionados ni una sustitución de los
lectores HMT. La prueba de autoadjunción y del límite infinito está en
los teoremas anteriores, no en el número de ejemplos calculados.
