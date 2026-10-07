# Materia interactuante y memoria a profundidad arbitraria

Formalización reunida y extensión focal, 29 de septiembre de 2026. Esta nota
continúa la composición de cuatro interacciones; no cambia ninguna fuente
publicada ni sustituye sus dominios por la sola enumeración de constantes.

## 1. Procedencia efectiva

La cadena es APP → TRIT → TPK → estado enriquecido → estructura discreta
conjunta del continuo → lectores de masa, canales, acción y transporte. Se
conservan las cinco construcciones del mismo continuo. Los valores de los
lectores son salidas, nunca objetivos introducidos para elegir historias.

Los propietarios, bajo
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`, son:

- `VI_ES/sections/05_registro_operador_masa.tex`: extractor de eventos de
  108 pasos, carácter refinado, convergencia de torres y operador positivo
  de masa por congruencia.
- `VI_ES/sections/05b_electron_estados_ley_masas_20260927.tex`: ecuaciones
  `vi:eq:ley-masas-trayectoria`, `vi:eq:balance-conservacion-masa` y prueba
  del criterio exacto de transporte a masa fija. Conserva por separado
  celda `(5,5)`, frontera `111111`, emisión `555555` y orientación.
- `VI_ES/sections/13_fock_pauli_composicion.tex`, desde
  `vi:subsec:fock-refinamiento`: naturalidad de Fock y dominio de dΓ.
- `VI_ES/sections/15_aritmetica_historias.tex`: restricciones de estados,
  memoria de acarreos, álgebra de rutas y prolongación contravariante de
  observables.
- `XII_ES/nuclear/09.tex`: dominio de historias completas X, transporte
  reversible C, archivo infinito isométrico, inversa, precisión 729^(-n),
  conservación de productos y conmutadores y memoria `C*DC=D+I`.
- `XII_ES/ampliacion_20260922.tex`, «Levantamiento dodecafásico y
  amplificación compatible»: caso explícito `J_m v=v⊗u_9` y
  `H_(m+1)J_m=J_mH_m` para el lector allí construido.
- `X_ES/sections/ym_complete.tex`, «Refinamiento nonádico y persistencia
  en el límite»: entrelazamiento fuerte del generador Yang–Mills y cierre
  de su forma por la descomposición de Hoeffding.
- `VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex`: eliminación
  de contorsión de la acción espinorial y coeficiente de la corriente total.

Se reutilizan las pruebas de esta carpeta en
`HAMILTONIANO_FINITO_HIGGS_FOCK.md` y `EVOLUCION_ACOPLADA_Y_LIMITE.md`.
La novedad de esta nota es pasar del registro geométrico finito a las
historias completas, componer su transporte con la interacción y demostrar
la convergencia de las lecturas de masa y de su evolución. La profundidad
de la memoria, la precisión de un lector, el número de ocupaciones y el
refinamiento espacial son índices distintos: no se identifican.

## 2. La masa conserva una lectura concreta de la historia

Para una ruta γ, el propietario construye σγ y las torres ηγ antes de
evaluar el carácter. Con `s_h=q_-^h-q_+^h`, `0<q_+<q_-<1`, su coordenada
relativa es

\[
\Lambda_\gamma=\log(m_\gamma^\beta/m_e^\beta)
=\delta n_Ax+\frac{\delta s_C}{6}y
+\delta k_\Delta\Delta_4+\delta b_\zeta\zeta_{270}
+\sum_h\delta N_hs_h+\delta\kappa\log R_{\rm act},
\quad N_h=\eta_h+b_{120}\mathbf1_{h=120}.
\tag{1}
\]

Las diferencias son con respecto a la misma sección electrónica y se
toman una sola vez. Las dos composiciones de altura 360, las hojas y el
orden de la ruta no se identifican porque el lector produzca un mismo
escalar. Tampoco se identifica la torsión ζ270 con el término de torre s270.

En el dominio de torres del propietario,
`Σ_h |δN_h s_h|<∞`. Si Λγ,N conserva las alturas h≤N y

\[
\epsilon_{\gamma,N}=\sum_{h>N}|\delta N_hs_h|,
\]

entonces

\[
|\Lambda_\gamma-\Lambda_{\gamma,N}|\le\epsilon_{\gamma,N},\qquad
\left|\frac{m_{\gamma,N}^\beta}{m_\gamma^\beta}-1\right|
\le e^{\epsilon_{\gamma,N}}-1\longrightarrow0.\tag{2}
\]

La prueba es la desigualdad triangular y la monotonía de la exponencial.
No presupone igualdad de la masa en todos los prefijos. Para cualquier
fibra finita de rutas, el máximo de sus ε tiende a cero, por lo que el
operador diagonal de masa converge en norma. Esta conclusión no exige
reemplazar las rutas por números ni escoger coeficientes a partir de una
masa objetivo. Las coordenadas infinitas se reciben del lector de la ruta.

En la forma general no diagonal, `Mβ=C_R M0 C_R`, con
`C_R=R_act^(B/2)`, se conserva la congruencia positiva. En una fibra finita,
si `B_N→B`, `R_N→R>0` y `M0_N→M0`, la continuidad del cálculo funcional
da `Mβ_N→Mβ`. Ésta es la prolongación operatoria del mismo lector.

La relación con el movimiento es exacta. Para el transporte TPK biyectivo
F de un dominio estable, `V_F eγ=eFγ`,

\[
[M^\beta,V_F]e_\gamma
=m_e^\beta(e^{\Lambda_{F\gamma}}-e^{\Lambda_\gamma})e_{F\gamma}.
\tag{3}
\]

La masa se conserva precisamente cuando el balance completo de (1) tiene
incremento cero. Los eventos y la memoria pueden cambiar manteniendo ese
balance; no se afirma que todo transporte conserve todas las masas.

## 3. Retirar el corte de memoria del espacio interactuante

Sea X el dominio de historias completas del propietario XII/09, en un
sector reversible estable donde están definidos los lectores utilizados
y se cumplen las condiciones de sus torres. La existencia de X y sus
prolongaciones procede de APP–TRIT–TPK; esta nota no las crea escribiendo
un límite inverso. Sobre X se utiliza la representación atómica del
propietario. No hace falta elegir una nueva probabilidad de historias:
cada vector de ℓ²(X) tiene soporte a lo sumo numerable.

Para cada x, sea h_x el operador asociado a la forma de la nota
`EVOLUCION_ACOPLADA_Y_LIMITE.md`, excluido únicamente el término que
transporta x a otra historia. En esa fibra permanecen conjuntamente

\[
 h_x=\hbar cK_{{\rm gauge},x}
+d\Gamma(D_{T,x}^*W_xD_{T,x})
+H_{H,\rm cin,x}+V_{H,x}+H_{Y,x}+H_{{\rm tor},x}.\tag{4}
\]

La celularización espacial y el número de modos fermiónicos de la carta
siguen fijados. Las amplitudes H∈C² no están cortadas. Los coeficientes son
los lectores de x y cada forma conserva su dominio, positividad del
cuártico, cinética positiva y pesos de volumen positivos. No se requiere
que sus cotas inferiores sean uniformes en todo X para el teorema siguiente.

El bloque Yukawa usa las mismas masas y base de mezcla:

\[
Y_u(x)=\sqrt2D_u(x)/v(x),\quad
Y_d(x)=\sqrt2V(x)D_d(x)V(x)^*/v(x),
\quad \mathsf Y_x(H)=[\widetilde H\otimes Y_u(x),H\otimes Y_d(x)]\otimes I_c.
\tag{5}
\]

El adjunto se incluye en `H_Y`; no se duplica la rotación CKM. Los bloques
leptónicos se componen con sus lectores y representaciones ya declarados.
La torsión se calcula con la corriente de todas las especies antes del
cuadrado:

\[
 Q_{{\rm tot},x}=\sum_{a=1}^4s_a
 \{d\Gamma(\widetilde M_{a,x})^2-d\Gamma(\widetilde M_{a,x}^2)\},
 \quad s=(-1,-1,-1,+1),
\]
\[
H_{{\rm tor},x}=-\sum_v\frac{N_v(x)cC_\gamma(x)}{\mathcal V_v(x)}Q_{{\rm tot},v,x},
\quad C_\gamma=\frac{3\kappa_{\rm grav}c\hbar^2}{16}\frac{\gamma^2}{1+\gamma^2}.
\tag{6}
\]

Así se conservan los términos entre especies. Se trabaja en la misma
carta efectiva reducida de la eliminación espinorial: no se retiene a la
vez como variable independiente la contorsión que ya produjo (6).

**Teorema 1 (interacción sobre todas las historias).** El operador

\[
 H_{\rm loc}=\bigoplus_{x\in X}h_x,\quad
 \operatorname{Dom}H_{\rm loc}=
 \{\Psi:\Psi_x\in\operatorname{Dom}h_x,
              \sum_x\|h_x\Psi_x\|^2<\infty\}
\tag{7}
\]

es autoadjunto y genera una evolución unitaria para todo tiempo. Conserva
el subespacio gauge físico. Este resultado no necesita que haya finitas
historias ni un máximo de profundidad de memoria.

**Prueba.** Para `Im z≠0`, `(h_x−z)^−1` existe y su norma es a lo sumo
`1/|Im z|`, uniformemente en x aunque las cotas inferiores varíen. Su
suma directa es acotada y es la inversa de `H_loc−z` en el dominio (7).
La simetría y la existencia de las inversas para z=±i prueban
autoadjunción. El cálculo espectral da la evolución. En cada fibra, las
formas recibidas son gauge invariantes; sus proyectores físicos reducen
h_x y por suma directa reducen H_loc. ∎

Las geometrías de volumen pequeño no quedan excluidas por una cota
uniforme inventada. Si el coeficiente de (6) crece sobre X, el dominio (7)
registra ese crecimiento. Sin una cota inferior uniforme no se infiere
estabilidad global inferior, vacío mínimo ni una traza térmica finita.

## 4. Evolución del estado completo: interacción y retorno no se separan

El propietario proporciona una biyección reversible d de historias completas
y `Cδ_x=δ_(dx)`. En su subsección «Covariancia del operador de memoria bajo
retorno» restringe expresamente al sector `X_rev,grad` y toma `d=Γ9`, con
`q_mem(dx)=q_mem(x)+1`. Usamos d para el teorema general; la especialización
nonádica se hace sólo en ese sector. Un paso de C significa un retorno d
completo, no una microtransición del calendario. δτ debe ser su lectura
de tiempo correspondiente. Si las fibras gauge tienen medidas μ_x
diferentes, se usa la identificación probada

\[
A_x:L^2(\mu_0)\longrightarrow L^2(\mu_x),\qquad
A_xf=\sqrt{Z_x}e^{S_x/2}f.
\]

Junto al transporte unitario de hoja/espín recibido, esto da un operador
unitario `T_x:𝓗_x→𝓗_dx`, que conserva el cuadrado de la representación
gauge. Su adjunto es el adjunto entre esos espacios, no la transpuesta
euclídea de muestras con pesos distintos. Definimos

\[
 (C_\mu\Psi)_{dx}=T_x\Psi_x,\qquad
 \mathbb U_{\delta\tau}=C_\mu e^{-i\delta\tau H_{\rm loc}/\hbar},\tag{8}
\]

donde δτ es el intervalo de la lectura de reloj recibida. Esta operación
significa primero evolución material en la historia y después transporte
del estado completo por el retorno; su orden queda declarado. No se
postula que (8) sea el exponencial de la suma de dos generadores continuos
sin comprobar los dominios de esa suma.

**Teorema 2 (propagación interactuante a todos los retornos).** (8) es
unitario, preserva Gauss y está definido a toda profundidad de memoria.
Para n≥1, sobre una fibra inicial x,

\[
 \mathbb U^n|_{\mathcal H_x}
=T_{d^{n-1}x}E_{d^{n-1}x}\cdots T_{dx}E_{dx}T_xE_x,
 \qquad E_x=e^{-i\delta\tau h_x/\hbar}.\tag{9}
\]

**Prueba.** La biyección d y la unitariedad de cada T_x prueban que C_μ
es unitario. El teorema 1 prueba la del otro factor. Sus inversos dan
también la propagación hacia atrás. Cada factor entrelaza las
representaciones gauge, luego el producto lo hace. La inducción sobre n
prueba (9), sin conmutar ni promediar los factores. ∎

Ésta no es una evolución con memoria decorativa: h_x cambia con los
lectores de la historia. En la especialización graduada `d=Γ9`, incluso
cuando el lector de fase vuelve, el grado de memoria satisface
`D(dx)=D(x)+1`. Si el observable de masa es
M_x, su transporte es

\[
 (\mathbb U^*M\mathbb U)|_x
=E_x^*T_x^*M_{dx}T_xE_x.\tag{10}
\]

En la lectura escalar de una sola ruta se recupera (3); en el espacio
material completo se conservan además sus conmutadores con Yukawa y con
los transportes de mezcla. Igualdad de una masa parcial no identifica dos
historias ni sus operadores. La continuidad temporal de `H_clk+H_loc`
se prueba adicionalmente cuando el reloj recibido es acotado o satisface
un control relativo suficiente; no se escoge un logaritmo de C para
inventar esa conclusión.

## 5. Convergencia de la masa, Yukawa y torsión en la evolución

Conservemos el espacio completo X y aproximemos los lectores de masa y de
los coeficientes torsionales por sus truncaciones, no cortando las historias
mismas. En este teorema se mantienen exactamente fijos μ_x, su identificación
A_x, la cinética escalar, los pesos de volumen, el potencial Higgs, los
transportes y el bloque gauge. No se cambia de medida con N ni se afirma
convergencia de una cinética variable por la mera convergencia puntual de
sus coeficientes. Para variar también una cinética A_x(u) sería necesario
su control uniforme en u en la norma de forma; no se usa esa ampliación aquí.
Para cada x, (2) y la continuidad de (5) hacen converger las matrices
Yukawa. Se conserva v>0 exacto; R_act se conserva o se aproxima dentro del
mismo lector de masa con límite positivo. Los coeficientes escalares que
se aproximen en (6), sobre los volúmenes exactos, tienen límite finito.
La continuidad de `γ²/(1+γ²)` da convergencia del correspondiente factor.
Son matrices de dimensión finita en cada fibra, independientes de u y H;
por ello esta convergencia es en norma. Se conserva el operador cuártico total,
no sólo las contribuciones diagonales de cada especie.

**Teorema 3 (paso al límite interactuante).** Sean h_x,N las formas
recibidas con sólo los lectores de masa/Yukawa y torsión truncados como
acaba de precisarse. En cada fibra sus matrices convergen en norma; la
cinética positiva y el cuártico positivo permanecen fijos. Entonces h_x,N converge a h_x
en resolvente; las sumas directas convergen en resolvente fuerte y

\[
 e^{-itH_{{\rm loc},N}/\hbar}\Psi\longrightarrow
 e^{-itH_{\rm loc}/\hbar}\Psi,\qquad
 \mathbb U_N^n\Psi\longrightarrow\mathbb U^n\Psi\quad(n\in\mathbb Z)
\tag{11}
\]

para todo vector y todo t,n fijos.

**Prueba.** Fijado x, las formas tienen dominio común
`Q_x={Ψ:∇_HΨ∈L², |H|²Ψ∈L²}` de la nota de evolución, sobre la misma
medida μ_x. La diferencia de matrices finitas tiende a cero. Los términos lineales Yukawa
se controlan por `a|H|≤ε|H|⁴+C(a,ε)`; los cuadráticos por la misma
cota de forma y la torsión por su norma matricial. Por tanto
`|(q_x,N−q_x)(u,v)|≤ε_x,N ||u||Q_x ||v||Q_x`, con ε_x,N→0.
La coercividad común para N grande y la resta de las ecuaciones
variacionales dan convergencia en norma de resolventes en esa fibra.
No es necesario uniformarla en x: la cota universal `1/|Im z|` permite
convergencia dominada sobre el soporte numerable de cada Ψ en la suma
directa. La convergencia resolvente fuerte de operadores autoadjuntos da
convergencia fuerte de sus grupos unitarios para t fijo. Multiplicar por
el mismo C_μ conserva la convergencia; la telescopía de potencias de
unitarios demuestra (11) para n≥0 y sus adjuntos para n<0. ∎

Este límite no supone el entrelazamiento falso `h_(N+1)J_N=J_Nh_N`
para aproximaciones con diferente precisión. El error de masa de (2)
tiende a cero y aparece en la prueba. En cambio, para observables
heredados exactamente mediante precomposición, los cuadrados de
refinamiento sí se conservan exactamente, como se demuestra en el
propietario de aritmética de historias.

## 6. Archivo infinito del operador completo, con cola residual

Sobre la misma representación de historias completas, sea C el transporte
unitario ya recibido, `T=(8I+C)/9`, y η su defecto nonádico del propietario:

\[
I-T^*T=\eta^*\eta=\frac8{81}(I-C)^*(I-C).
\]

La versión de N registros que no pierde información es

\[
V_Nv=(T^Nv,\eta v,\eta Tv,\ldots,\eta T^{N-1}v).\tag{12}
\]

**Teorema 4 (archivo interactuante y profundidad).** V_N es una isometría.
La prolongación que divide el residuo, sin borrar los bloques anteriores,

\[
J_N(r,m_0,\ldots,m_{N-1})=(Tr,m_0,\ldots,m_{N-1},\eta r)
\tag{13}
\]

es isométrica y `J_NV_N=V_(N+1)`. Sobre las imágenes compatibles, todo
operador H recibido, con su dominio si no es acotado, tiene la realización

\[
H_N^{\rm arch}=V_N H V_N^*,\qquad
J_NH_N^{\rm arch}=H_{N+1}^{\rm arch}J_N.\tag{14}
\]

En particular, (14) transporta conjuntamente H_loc, U, las masas, Yukawa,
la corriente total y sus relaciones; no los convierte en operadores que
conmutan si no conmutaban. El archivo infinito es

\[
 Vv=(Pv,\eta v,\eta Tv,\ldots),\quad
 v=Pv+\sum_{j\ge0}T^{*j}\eta^*(\eta T^jv),\tag{15}
\]

donde `P=proj ker(I−C)`. Es una isometría sobre su imagen y la serie de
reconstrucción converge en norma.

**Prueba.** La suma telescópica
`||T^Nv||²+Σ_(j<N)||ηT^jv||²=||v||²` prueba (12).
La identidad de defecto aplicada a r prueba (13); sustituir (12) da su
cuadrado. La isometría implica `V_N*J_N*=V_(N+1)*` y, sobre las imágenes,
`V_(N+1)*J_N=V_N*`. Éstas prueban (14), incluyendo el transporte del
dominio. El teorema espectral para T, que es una función del unitario C,
da `T^N→P` fuertemente. Pasar al límite en la telescopía demuestra (15)
y su inversa. Para un H no acotado, `Dom(VHV*)=V DomH` sobre la imagen;
es equivalencia unitaria con ese dominio, no una compresión arbitraria. ∎

En el sector graduado con `C*DC=D+I`, todas las órbitas completas son
infinitas y P=0 en la representación de conteo del propietario. La cola
residual desaparece fuertemente al llevar N a infinito, pero no se puede
borrar antes a profundidad finita. Suprimir `T^Nv` en (12) pierde
exactamente esa norma y ya no conserva los operadores.

El refinamiento tensorial explícito de XII y el funtor Γ de VI son
compatibles: para un entrelazador isométrico J que satisfaga ambos
cuadrados de Yukawa, `Y'J_R=J_LY` y `Y'^*J_L=J_RY*`, la segunda
cuantización conserva H_Y y los polinomios de corrientes. No basta el
primer cuadrado: el adjunto puede acoplar un modo nuevo al antiguo.
El archivo (12) evita esa pérdida conservando la cola; no declara
automáticamente esos cuadrados para un refinamiento espacial distinto.

## 7. Resultado alcanzado y alcance de la composición

Se obtiene una evolución cuántica interactuante sobre historias completas
con profundidad arbitraria de memoria, masas leídas desde esas historias,
Yukawa con las mismas matrices y torsión de corriente total. La retirada
del corte de lector tiene una prueba resolvente; el archivo nonádico
conserva el operador, no sólo la evaluación; los retornos se componen
unitariamente sin reiniciar el estado.

La celularización espacial sigue fijada en los teoremas 1–3. La construcción
Yang–Mills del propietario ya posee su propio límite espacial, mientras
el bloque de respuesta geométrica posee la reducción Schur con memoria
de la nota compañera. Componer esos límites con una realización quiral
espacial requiere conservar los cuadrados y dominios del mismo operador;
no se deduce de aumentar únicamente N en (12). Esta distinción identifica
los índices exactos que ya se han eliminado y no rebaja ni reinicia la
generación APP–TRIT–TPK recibida.

`verificar_limite_materia_memoria.py` comprueba el defecto, el archivo con
cola, el entrelazamiento, productos/conmutadores, una evolución ordenada
con el cuártico espinorial y falsadores de borrar la cola, alterar el orden
o sustituir el balance de masa por un histograma. Los números de prueba
son fixtures declarados, no constantes HMT recalibradas. El comprobador
no sustituye las pruebas de dominios y convergencia de esta nota.
