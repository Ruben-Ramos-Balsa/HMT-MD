# Transporte TPK, segunda variación y curvatura conservada por refinamiento

Desarrollo focal del 29 de septiembre de 2026. Se reutilizan los resultados
anteriores y no se modifican fuentes selladas. Esta nota calcula tres
operaciones diferentes: comparar dos rutas completas, diferenciar dos veces
la energía de memoria y retirar el corte conservando el defecto de bucle.

## 1. Base HMT usada y propietarios

La construcción parte de APP → TRIT → TPK → estado enriquecido → estructura
discreta conjunta del continuo. La ruta conserva hojas, orientación, carry,
incidencia y memoria. La realización matricial no reemplaza esos datos;
las constantes, incluidos los lectores de acción, se reciben como salidas
anteriores. Las cinco construcciones del continuo permanecen conjuntas.

Se han leído directamente estos propietarios bajo
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`:

- `VIII_ES/manuscrito/nucleo_ampliado/continuo_conjunto.tex`, desde línea 32:
  actualización afín `U_ε(m)=C_εm+κ_ε` y cociclo de concatenación.
- `VIII_ES/manuscrito/29_retorno_y_memoria_traslacional.tex`, §§ cociclo y
  representación: `c_27=(1,18)`, `c_108=(4,72)`, representación semidirecta
  de espín y traslación, inversión y memoria de vueltas completas.
- `VIII_ES/manuscrito/30b_variacion_energia_memoria.tex`, líneas 23–124,
  134–170 y 261–309: energía global `D*WD`, diferencial completo,
  diferenciación de productos de transportes y refinamiento variable.
- `VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex`, líneas
  239–282: transporte del covector de conexión y conservación de su
  dependencia respecto de la conexión actual.
- `VIII_ES/manuscrito/30d_realizacion_geometrica.tex`, líneas 18–168:
  igualdad de holonomías, curvatura/torsión de Cartan, Bianchi y tres
  realizaciones TRIT.
- `X_ES/sections/ym_complete.tex`, ecuaciones de Gibbs global,
  superficie–Bianchi y Ward, líneas 600–728: composición ordenada de
  colores, naturalidad grueso/detalle y Ward en el estado cofinal.
- `XII_ES/nuclear/09.tex`, ecuaciones `nuc09:lecturas`,
  `nuc09:transporte-recuperado`, `nuc09:error-producto`, `nuc09:memoria`:
  conjugación del transporte completo, archivo unitario y precisión de
  productos ordenados. El índice de precisión no se confunde con el
  número de retornos ni con el refinamiento espacial.

## 2. Dos rutas: el cociclo conserva el bucle, no lo borra

Para dos rutas admisibles componibles γ₁ y γ₂, realizadas en cartas de
memoria reversibles, el propietario da

\[
 U_\gamma(m)=C_\gamma m+\kappa_\gamma,\qquad
 U_{\gamma_2\gamma_1}=U_{\gamma_2}U_{\gamma_1},
 \quad \kappa_{\gamma_2\gamma_1}
 =C_{\gamma_2}\kappa_{\gamma_1}+\kappa_{\gamma_2}.
 \tag{1}
\]

Sean ahora α y β dos rutas paralelas, con los mismos extremos. La
comparación completa en la fibra inicial es

\[
 U_\beta^{-1}U_\alpha(m)=
 C_\beta^{-1}C_\alpha m+
 C_\beta^{-1}(\kappa_\alpha-\kappa_\beta).
 \tag{2}
\]

Por tanto, dos realizaciones coinciden sobre toda esa carta precisamente
cuando coinciden su parte lineal y su traslación. La coincidencia de un
lector parcial no sustituye esas dos igualdades. (2) resulta de invertir
la aplicación afín de β y sustituir; no usa valores físicos objetivo.

En una carta donde dos actualizaciones sean automorfismos A y B, con
pares `(C_A,κ_A)` y `(C_B,κ_B)`, el bucle ordenado `A⁻¹B⁻¹AB` tiene

\[
 C_\square=C_A^{-1}C_B^{-1}C_AC_B,
\]
\[
 \kappa_\square=C_A^{-1}C_B^{-1}
 \bigl((C_A-I)\kappa_B-(C_B-I)\kappa_A\bigr).
 \tag{3}
\]

La fórmula sólo compara composiciones con ese dominio común; en un
grupoide con fibras distintas se emplea (2) sobre los dos caminos del
cuadrado. La memoria no se sustituye por una suma sin transporte.

El resultado material `ρ_C(γ_108)=(I,72ℓ_0u)` ya ofrece un caso concreto:
retorna la fase y persiste una traslación. No es una anomalía del
transporte. Es la información que la realización afín debe conservar.
Una subdivisión de una misma ruta conserva su producto por (1); cambiar
de ruta conserva el bucle (2), que puede ser no trivial.

Sobre las historias completas X, cualquier transporte reversible d se
representa por `C_d δ_x=δ_(dx)`. Si se acompaña de una fase de acción
leída, la forma tipada es

\[
 T_\gamma\delta_x=e^{-i a_\gamma(x)}\delta_{d_\gamma x},
 \quad
 a_{\beta\alpha}(x)=a_\alpha(x)+a_\beta(d_\alpha x)
 \pmod {2\pi}.
 \tag{4}
\]

Aquí `a_γ` es la lectura adimensional de acción correspondiente a la
ruta, no una constante convencional usada para escogerla. (4) demuestra
la multiplicatividad si el lector satisface ese cociclo; no afirma que
cualquier función añadida sea el lector HMT. El archivo isométrico V de
XII/09 conserva el bucle exactamente:

\[
 \widehat T_\beta^{-1}\widehat T_\alpha
 =\mathcal V(T_\beta^{-1}T_\alpha)\mathcal V^{-1}.
 \tag{5}
\]

Así la recuperación de memoria conserva también cualquier defecto entre
los dos recorridos. No fuerza que ese defecto sea la identidad.

## 3. Segunda variación completa de la energía recibida

Trabajamos en un nivel finito sobre el funcional del propietario

\[
 r(q)=D(q)f(q),\qquad E(q)=\langle r(q),W(q)r(q)\rangle,
 \quad W(q)^*=W(q)>0,
 \tag{6}
\]

en una familia C² de realizaciones admisibles. El producto hermítico es
antilineal en la primera variable. Para campos de variación N,M se
escribe `r_N=δ_Nr`, `W_N=δ_NW` y `r_NM=δ_Nδ_Mr`. La regla del
producto calcula

\[
\begin{split}
 \delta_N\delta_M E
 ={}&2\operatorname{Re}\langle r_N,W r_M\rangle\cr
 &+2\operatorname{Re}\langle r,
       W_Nr_M+W_Mr_N+W r_{NM}\rangle
   +\langle r,W_{NM}r\rangle.
\end{split}
\tag{7}
\]

**Prueba.** Se diferencia
`δ_ME=2Re⟨r,Wr_M⟩+⟨r,W_Mr⟩`. Se reúnen los términos adjuntos
usando que W y W_M son hermíticos. No se fija f, U, W ni una inclusión
dependiente de q durante esa derivación. ∎

Al antisimetrizar, los primeros términos se cancelan y quedan

\[
 (\delta_N\delta_M-\delta_M\delta_N-\delta_{[N,M]})E=0.
 \tag{8}
\]

Para una familia de campos efectiva (8) es una igualdad de segunda
variación, no una condición de planitud. La versión covariante explica
por qué. Si ∇ es métrica, con curvatura `R_NM`, actúa sobre los pesos
mediante el conmutador. Las contribuciones aparentes a (8) son

\[
 2\operatorname{Re}\langle r,W R_{NM}r\rangle
 +\langle r,[R_{NM},W]r\rangle=0.
 \tag{9}
\]

**Prueba.** `R_NM* = −R_NM`. El primer sumando es
`⟨r,(WR_NM−R_NMW)r⟩`, el opuesto del segundo. ∎

Esta cancelación usa precisamente el peso transportado que acompaña la
memoria. Eliminar `δW` puede crear una incompatibilidad artificial;
conservarlo prueba consistencia de la acción, pero no permite inferir
`R_NM=0`. El verificador incluye un caso con curvatura no nula en que
los dos términos de (9) son respectivamente 4 y −4.

### Derivadas de una ruta completa

Con `U_γ=U_k⋯U_1`, la fórmula del propietario
`δ_NU_γ U_γ⁻¹=Σ_j B_j(δ_NU_j U_j⁻¹)B_j⁻¹` conserva la posición de
cada incidencia. Al diferenciar otra vez, también se diferencian los
factores B_j. Para cualquier familia unitaria U(q),
`X_N=(δ_NU)U⁻¹` satisface

\[
 \delta_NX_M-\delta_MX_N-X_{[N,M]}-[X_N,X_M]=0.
 \tag{10}
\]

Se obtiene expandiendo el conmutador de derivadas aplicado a U.
Es la identidad del cambio de marco `−dU U⁻¹`. No se la identifica con
la curvatura de una conexión física independiente: elegir una sección
de caminos para escribir U(q) no borra las holonomías de otros caminos.

## 4. Refinamiento variable y operador total

La fuente 30b prueba la naturalidad del diferencial y conserva el término
adicional con `δJ` cuando la inclusión depende de la deformación.
La segunda variación (7) conserva además `δ_Nδ_MJ` y los cruces de
primeras derivadas. No deben suprimirse al pasar de energía a conexión.

La nota coordinada `CURVATURA_TOTAL_MEMORIA_Y_LIMITE.md` desarrolla la
curvatura de la conexión inducida por una inclusión isométrica variable.
Se remite allí para la identidad de segunda forma, sin reproducirla como
hallazgo nuevo. En particular, la compresión de H recibe el término de
conexión `−iℏ J*δ_NJ`; no equivale a conservar únicamente `J*H_NJ`.

En una trivialización y núcleo comunes, escribamos el operador completo
como suma de sus contribuciones realmente realizadas, `H_N=Σ_a H_N^a`.
Cada sumando retiene la dependencia en campos, marco, memoria y lectores
que utiliza. La curvatura solicitada es

\[
 \mathcal F_{NM}=\delta_NH_M-\delta_MH_N-H_{[N,M]}
                  +\frac{i}{\hbar}[H_N,H_M].
 \tag{11}
\]

Definiendo `F^a` por la misma expresión para cada sumando, la identidad
exacta es

\[
 \mathcal F_{NM}=\sum_a\mathcal F^a_{NM}
 +\frac{i}{\hbar}\sum_{a<b}
 \left([H_N^a,H_M^b]+[H_N^b,H_M^a]\right).
 \tag{12}
\]

No basta sumar curvaturas sectoriales. La igualdad (12) sale expandiendo
el conmutador sin alterar su orden; las derivadas ya incluyen la variación
de todos los coeficientes de cada contribución. En los acoplamientos
construidos, los operadores comparten materia, conexión y geometría:
no se supone que actúen siempre sobre factores independientes. La nota de
conmutador espacial calcula uno de estos bloques sobre su núcleo; la
presente identidad conserva los otros cruces en el mismo operador.

## 5. Holonomía, Bianchi y una transformación gauge genuina

La realización Cartan recibida tiene
`F_C=[[F_ω,T/ℓ_0],[0,0]]`, y en las hojas extremas incorpora el término
`−τ e∧e/ℓ²`. Las identidades Bianchi transportan esta curvatura; no la
anulan. En X/YM, el producto orientado y transportado de plaquetas sobre
la frontera de una celda es la identidad. Es cancelación de la frontera
de una frontera, no identidad de cada plaqueta. La prueba preserva la
acción, el clover y los productos, incluidos los no conmutativos.

Hay un criterio preciso que sí reduce el bucle sobre estados físicos.
En el grupo gauge y representación ya recibidos, si el operador de
comparación completo satisface

\[
 T_\beta^{-1}T_\alpha=R(g),\qquad
 P_{\rm phys}R(g)=R(g)P_{\rm phys}=P_{\rm phys},
 \tag{13}
\]

entonces ambas rutas coinciden sobre `Ran P_phys`. Si una familia
diferenciable de estos bucles tiene generador de curvatura igual a una
combinación de las restricciones Gauss efectivas, su curvatura se anula
en el núcleo físico que ellas aniquilan. (13) requiere una transformación
gauge de toda la configuración y sus fibras, o la representación bloque
a bloque expresamente declarada; no sólo una matriz con valores en G.

**Falsador exacto.** En una plaqueta Z₂ con cuatro enlaces, la holonomía
`w=u₀u₁u₂u₃` es gauge-invariante. La media gauge P conserva tanto la
función 1 como w, pero la multiplicación por w satisface
`P M_w P 1=w≠1`. Ward vale para la medida uniforme y sin embargo la
holonomía no desaparece. Este modelo prueba la distinción lógica entre
ser gauge-invariante, tomar valores en el grupo y ser una restricción
que aniquila estados físicos. No sustituye el grupo HMT por Z₂.

En el propietario X, Ward es `∫δ_εF dμ=0`, por invariancia del estado y
de su acción. Se transporta al límite para cilindros. Eso autoriza usar
las transformaciones gauge demostradas; no identifica por sí solo una
evolución normal multitiempo con (13). La búsqueda focal de esas fuentes
recupera conmutación de collares disjuntos y Bianchi, no una regla que
permita intercambiar todas las capas de colores o toda deformación normal.

## 6. Límite: conservar bucles finitos y extraer su curvatura

Para una familia de inclusiones naturales que entrelace los transportes
de cada tramo, el entrelazamiento de cualquier bucle finito se prueba
componiendo los cuadrados en su orden. En una trivialización compatible,
si cada transporte e inverso converge fuertemente y es unitario, todo
producto de longitud finita converge fuertemente. XII/09 preserva además
estos productos y conmutadores por la isometría de archivo V.

Extraer el generador infinitesimal exige un control más fino. Sea
`L(ε)=I+ε² R_NM+o(ε²)` sobre un núcleo común, para la orientación
de bucle escogida. Si `L_n(ε)` es su realización refinada, basta

\[
 \|(L_n(\varepsilon)-L(\varepsilon))\psi\|
       \le\eta_n(\varepsilon)\|\psi\|_{\mathcal D},
 \qquad
 \eta_{n(\varepsilon)}(\varepsilon)=o(\varepsilon^2).
 \tag{14}
\]

Restar I y dividir por ε² prueba la convergencia de la curvatura
sobre ese núcleo. Para dos tamaños diferentes, ε² se reemplaza por el
área orientada absoluta del rectángulo, y se mantiene el signo en R.

La cota concreta de XII/09, `r·729^(−n)`, controla productos de
contracciones con r lectores numéricos reemplazados, dejando exactos
el transporte y la incidencia. Si el bucle está realizado en esa clase,
una elección explícita es

\[
 \varepsilon_m=9^{-m},\qquad n(m)=m,
 \quad \frac{r\,729^{-m}}{\varepsilon_m^2}=r\,9^{-m}\longrightarrow0.
 \tag{15}
\]

También un factor `exp(−iθM_ξ)` tiene error de norma a lo sumo
`|θ|729^(−n)` por la identidad integral de Duhamel para multiplicadores
autoadjuntos acotados. La suma de esos errores controla el producto.
Esto no extiende automáticamente (15) a Hamiltonianos espaciales no
acotados: allí se requiere la cota de núcleo de (14), o convergencia
de las dos derivadas de forma. Los índices de precisión, corte espacial
y archivo pueden elegirse conjuntamente, pero no se identifican por su
nombre ni por tener todos una base nonádica.

**Falsador de intercambio de límites.** Con Z hermítica involutiva y
`t_n(ε)=ε²/(1+nε²)`, defina

\[
 L_n(\varepsilon)=(I+i t_nZ)(I-i t_nZ)^{-1}.
 \tag{16}
\]

Para ε fijo, `L_n→I`; de hecho `|t_n|≤1/n` da convergencia uniforme
de los bucles. Pero para cada n fijo,
`(L_n(ε)−I)/ε²→2iZ`. La convergencia de holonomías sin la tasa
o(área) no conmuta necesariamente con la extracción de curvatura.

Para la reducción física, si además las proyecciones Gauss convergen
fuertemente, permanecen entrelazadas por el refinamiento y los bucles
satisfacen (13), su identidad sobre estados físicos pasa al límite.
Cuando se trabaja con generadores no acotados, se requiere además la
convergencia de (14) en un núcleo físico común. No se reemplaza ese
control por una identidad sólo de expectativas del estado.

## 7. Resultado, procedencia y control reproducible

Se conservan los cociclos y la memoria ya demostrados; se calcula su
comparación de dos caminos, se desarrolla la segunda variación completa
de D*WD y se prueba su cancelación covariante sin borrar curvatura. Se
escriben los cruces obligatorios de la curvatura total y se distingue la
reducción Gauss efectiva de una holonomía gauge-invariante. La precisión
nonádica recibida permite una diagonal explícita que conserva curvatura
cuando el bucle tiene la clase y cota indicadas en (14)–(15).

El archivo `verificar_curvatura_tpk_refinamiento.py` ejecuta controles
exactos de cociclos, memoria del retorno, Hessiano, cancelación (9),
cruces de (12), reducción gauge y falsador de Ward, además de las cotas
racionales de (15)–(16). Son controles de estas pruebas, no certificados
de una identidad total no calculada. La condición operativa para el
cierre pedido queda expresada sobre el operador completo (11), con
sus derivadas, Gauss y cruces, sin reabrir APP–TRIT–TPK ni borrar el
transporte ya construido.
