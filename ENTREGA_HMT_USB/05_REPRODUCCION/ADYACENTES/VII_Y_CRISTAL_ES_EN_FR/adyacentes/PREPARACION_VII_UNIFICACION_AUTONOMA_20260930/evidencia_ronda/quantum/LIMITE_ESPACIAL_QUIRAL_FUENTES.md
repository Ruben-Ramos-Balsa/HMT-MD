# Refinamiento espacial, quiralidad y álgebra de deformaciones

Lectura focal y pruebas de composición, 29 de septiembre de 2026. No se
modifican propietarios ni se repite el cierre de memoria y suspensión del
reloj. Se distingue el límite espacial del límite de precisión y del
archivo de historias completas, ya demostrados en sus notas propias.

## 1. Procedencia y resultados materiales recibidos

APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del
continuo es el origen de los transportes, incidencias, registros y lectores
utilizados. Las cinco construcciones del continuo permanecen conjuntas.
Los grupos, espacios de Hilbert y operadores de esta nota son realizaciones
de esos objetos; no seleccionan retroactivamente semillas ni constantes.

Las rutas siguientes son relativas a
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`.

### 1.1. Entrelazamiento fuerte del propietario Yang–Mills

`X_ES/sections/ym_complete.tex`, ecuaciones
`eq:pdf2-ym-owner-refined-generator`,
`eq:pdf2-ym-owner-physical-reduction`,
`eq:pdf2-ym-g-dynamics` y `eq:pdf2-ym-owner-intertwining`, demuestra:

\[
\Gamma_mJ_m f=f\otimes1_{\rm det},\qquad
H_{m+1}=\Gamma_m^*(H_m\otimes I+I\otimes H^{\rm det}_{m+1})\Gamma_m,
\quad H^{\rm det}_{m+1}1_{\rm det}=0,\tag{1}
\]
\[
H_{m+1}J_m=J_mH_m,\qquad
P^{\rm phys}_{m+1}J_m=J_mP^{\rm phys}_m.\tag{2}
\]

El primer cuadrado sale de (1), no de una compresión de energía. La
construcción con acoplamiento transporta conjuntamente medidas, expectativas,
generadores, proyecciones e inclusiones. El cociclo de la acción
`S_(m+1)=S_m+S_det` da consistencia de las medidas; los transportes
triangulares de Gibbs conservan productos y las coordenadas ancestrales.
Las identidades de Ward y Schwinger–Dyson se prueban sobre cilindros y
pasan al estado cofinal porque cada cilindro reside en un nivel.

En las líneas 796–836, la forma límite se cierra mediante Hoeffding:

\[
\mathcal E_\infty(f)=3\kappa_{\rm av}
\sum_{S\Subset\mathcal I_\infty}|S|\,\|f_S\|^2.\tag{3}
\]

Las truncaciones constituyen un núcleo de forma y Fatou da la
semicontinuidad inferior. Éste es un límite espacial/operatorio real del
propietario, no sólo una ampliación de la memoria decimal.

### 1.2. Refinamiento de la respuesta y de su corriente

`VIII_ES/manuscrito/30b_variacion_energia_memoria.tex`, desde la línea
254, prueba para una familia compatible C¹:

\[
D'J=KD,\quad K^*W'K=W
\quad\Longrightarrow\quad J^*(D'^*W'D')J=D^*WD.\tag{4}
\]

También transporta el diferencial respecto de los transportes y pesos.
`30c_composicion_corriente_conexion.tex`, desde la línea 239, deduce

\[
s_m=P_m^{\mathsf T}s_{m+1},\qquad
M_m\sigma_m=P_m^{\mathsf T}M_{m+1}\sigma_{m+1}.\tag{5}
\]

Son identidades de formas y covectores sobre las variaciones enlazadas.
En esos enunciados no se sustituye (4) por el entrelazamiento fuerte (2).
La dependencia de J respecto de una deformación exige conservar además
sus derivadas, según advierte la continuación del mismo propietario.

`30d_realizacion_geometrica.tex`, líneas 18–59, transporta la soldadura
`e_m=J_scr,m β_m` y exige la igualdad de holonomías sobre las rutas,
conservando identidad, concatenación, inversión y subdivisión. Las
líneas 97–123 prueban las identidades de Bianchi de la realización.

`81_propagacion_bidireccional.tex`, desde la línea 475, da un criterio
fuerte adicional: una proyección absorbente se prolonga si se transportan
tanto su núcleo como su complemento ortogonal. Conserva así los dominios,
en lugar de inferir una proyección límite de una sola inclusión.

### 1.3. Fibra espinorial y completación de Fock

`VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex`, líneas
55–118, contiene las matrices de Clifford g^I, la conexión
`Ω=ω^{IJ}[g_I,g_J]/8` y la acción de Dirac con la masa, acción y
velocidad leídas previamente. No se usa el nombre de la especie para
elegir esos valores.

`VI_ES/sections/13_fock_pauli_composicion.tex`, desde la línea 413,
demuestra la compatibilidad de los proyectores graduados y Γ(J) para
entrelazadores contractivos que conservan el grado. El grado fermiónico
que controla la exclusión no debe confundirse con la quiralidad.

`VI_ES/sections/03_conjugacion_mobius.tex`, línea 409, distingue
explícitamente la helicidad direccional de la graduación relativista.
Ese pasaje no identifica un helicity projector con un regulador Dirac.

## 2. Quiralidad transportada sin eliminar las masas

En la fibra de Clifford del propietario, definamos

\[
\Gamma_5=i g^0g^1g^2g^3,\quad
\Gamma_5^*=\Gamma_5,\quad\Gamma_5^2=I,\quad
\Gamma_5g^I=-g^I\Gamma_5.\tag{6}
\]

Las relaciones se obtienen de la firma −+++ y de la anticomutación de
los generadores. En particular,

\[
[\Gamma_5,[g_I,g_J]]=0,\qquad [\Gamma_5,\Omega]=0.\tag{7}
\]

Por la ecuación del transporte espinorial, (7) implica el cuadrado
`Γ_(5,t)T_a=T_aΓ_(5,s)` en cambios de marco orientados con su
levantamiento de espín. El transporte interno actúa sobre su propio
factor y conserva el mismo cuadrado. No se identifica SU(2) de espín
con SU(2) débil.

Para el diferencial covariante de la composición conjunta,

\[
(D_Tf)_a=f_{t(a)}-T_af_{s(a)},
\quad D_T\Gamma_{5,V}=\Gamma_{5,E}D_T.\tag{8}
\]

Si el peso W transportado es par, `WΓ_(5,E)=Γ_(5,E)W`, entonces

\[
[D_T^*WD_T,\Gamma_{5,V}]=0.\tag{9}
\]

**Prueba.** Sustituir el cuadrado de transporte en cada arista prueba
(8). Tomar adjuntos y componer con W prueba (9). Los pesos escalares
en espín, incluidos los pesos globales entre incidencias con transporte
de marco correspondiente, satisfacen esa condición. ∎

Esto se refiere al bloque covariante de segundo orden realmente
construido. No lo renombra operador de Weyl de primer orden. En la
representación espinorial completa, el operador principal covariante
de Dirac invierte la quiralidad espinorial; en una representación gauge
quiral cada Weyl conserva además su propia fibra de carga en el
codominio. No se identifican las fibras internas E_L y E_R para
forzar un único tensor cuando son distintas.

El bloque Yukawa de la composición anterior tiene forma
`h_Y=[[0,Y],[Y*,0]]` sobre E_L⊕E_R y es impar respecto de la
graduación `diag(I_L,−I_R)`. La corriente espinorial total y su
cuártico son pares. Por ello la condición correcta de continuidad es
transportar la graduación y el tipo de cada bloque. Exigir que todo
H, incluida la masa, conmute con la graduación borraría el acoplamiento
L/R que precisamente se quiere conservar.

## 3. Teorema de prolongación espacial de la estructura graduada

Sean `J_m:𝓗_m→𝓗_(m+1)` las inclusiones isométricas de la realización
espacial recibida. Sean χ_m involuciones autoadjuntas con

\[
\chi_{m+1}J_m=J_m\chi_m.\tag{10}
\]

**Proposición 1.** Existe una única involución autoadjunta χ∞ sobre
el límite Hilbert que satisface `χ∞J_(m,∞)=J_(m,∞)χ_m`. Sus
proyectores `(I±χ∞)/2` son los límites compatibles de los proyectores
quirales. La completación fermiónica satisface

\[
\mathcal F_-(\mathscr H_\infty)
=\overline{\bigcup_m\Gamma(J_{m,\infty})\mathcal F_-(\mathscr H_m)}.
\tag{11}
\]

**Prueba.** (10) define χ∞ en la unión algebraica sin depender del
representante. Su norma es uno; las identidades de adjunto e involución
pasan por continuidad. Para (11), los vectores de número finito de
partículas y las combinaciones de tensores simples son densos. Se
aproxima cada uno de sus finitísimos factores a un nivel común; el
producto exterior y su proyector son continuos. La conservación de
normas de J prueba la isometría de cada Γ(J). ∎

Así, una vez dados los entrelazadores espaciales graduados, no permanece
un corte de número de modos ni de ocupaciones en la **álgebra CAR**.
Las identidades de creación y aniquilación se prolongan por su
naturalidad y acotación. Esto no determina por sí solo la suma de
interacciones sobre todas las celdas: su dominio y convergencia son
una cuestión operatoria adicional, no un defecto de CAR.

**Proposición 2 (palabras operatorias y defectos).** Sobre núcleos
invariantes compatibles 𝓓_m, supongamos que los operadores A_m^a
realmente satisfacen

\[
A_{m+1}^aJ_m=J_mA_m^a.\tag{12}
\]

Entonces todo producto ordenado finito y todo conmutador de esos
operadores se prolonga al núcleo algebraico 𝓓∞. Si
`χ_m A_m^a=ε_a A_m^aχ_m`, con ε_a∈{±1}, el mismo tipo se conserva
en el límite. Para cualquier polinomio no conmutativo R,

\[
R(A_\infty)J_{m,\infty}f
=J_{m,\infty}R(A_m)f,\qquad f\in\mathcal D_m.\tag{13}
\]

**Prueba.** Se aplica (12) a cada factor, manteniendo su orden. La
invariancia de 𝓓_m permite cada producto. La linealidad da la
afirmación polinómica y (10) transporta la paridad. ∎

La proposición no introduce el cierre de un álgebra de restricciones
como premisa oculta. Permite **calcular y transportar su residuo**.
Si el residuo finito de una identidad es no nulo en f, entonces

\[
\|R(A_\infty)J_{m,\infty}f\|=\|R(A_m)f\|>0.\tag{14}
\]

El refinamiento isométrico no puede borrar ese residuo. Cuando el
residuo se demuestra cero en las fuentes, (13) sí lo conserva.

Para operadores acotados uniformemente, la prolongación es acotada.
Para operadores no acotados, la proposición declara el núcleo y los
productos; no infiere esencial autoadjunción. El propietario Yang–Mills
añade precisamente el control de formas (3) que determina su cierre.

## 4. Componer la quiralidad con el límite Yang–Mills ya construido

Hay una consecuencia inmediata que sí utiliza íntegramente (1)–(3).
Tensorizar sus inclusiones con la fibra espinorial y las representaciones
internas ya realizadas da

\[
\mathsf J_m=J_m^{\rm YM}\otimes I_{\rm sp,int},\quad
\chi_m=I\otimes\Gamma_5,
\quad \mathsf D_m=D_m^{\rm YM}\otimes I_{\rm sp,int}.\tag{15}
\]

Se verifican (10), (12) para 𝔇_m y el cuadrado de Gauss. La forma
de Hoeffding tensorizada es cerrada con el mismo dominio ponderado
por |S|; χ∞ y Gauss la reducen. La realización conserva ambas
componentes quirales con sus etiquetas y sus cargas internas. Si se
trabaja directamente con E_L/E_R, se toma la suma de los dos
productos, sin igualar sus representaciones.

(15) completa el transporte de la **fibra quiral** junto a la dinámica
gauge en todos los niveles. No asegura por sí solo que un operador
espacial de primer orden sobre los nuevos modos fermiónicos tenga una
sola especie por quiralidad. Ésa es una propiedad de su símbolo,
dominio y realización, no una propiedad del proyector χ∞ aislado.

## 5. Defecto exacto entre compresión y álgebra

Se reutiliza la identidad ya demostrada en
`MEMORIA_DOMINIO_Y_ALGEBRA.md`, §2, y su verificador
`verificar_memoria_dominio_algebra.py`. La aportación aquí es su
aplicación al refinamiento de la fuente 30b, el falsador que conserva
la quiralidad y el enlace con el límite espacial; no otra prueba
presentada como hallazgo independiente.

Sean J una isometría, P=JJ*, A′,B′ autoadjuntos y
`A=J*A′J`, `B=J*B′J`. En dimensión finita, o sobre un dominio
común que permita estas operaciones, se cumple

\[
\boxed{J^*[A',B']J-[A,B]
=X_A^*X_B-X_B^*X_A,\quad
X_A=(I-P)A'J,\quad X_B=(I-P)B'J.}\tag{16}
\]

**Prueba.** Insertar `I=P+(I−P)` entre A′ y B′ separa el producto
grueso del que entra en los modos nuevos. Restar el producto inverso
da (16), y la autoadjunción identifica los adjuntos de X_A,X_B. ∎

El miembro derecho contiene la excursión a los grados de detalle y
su regreso. Es precisamente información que la compresión de energía
(4) no contiene por sí sola. Si se dispone de (12), ambos X son cero.
Si no, el resolvente de Schur debe conservar esos canales, como ya
se hizo en la nota de respuesta geométrica.

**Falsador incluso con quiralidad conservada.** En C⁴, tome
`χ′=diag(1,1,−1,−1)`, `A′=σ_x⊕σ_x`, `B′=σ_y⊕σ_y`, y J que
incluye las coordenadas primera y tercera. Entonces `χ′J=J diag(1,−1)`
y ambos A′,B′ son pares. Pero A=B=0 mientras

\[
J^*[A',B']J=2iI_2\ne0.\tag{17}
\]

Por tanto, entrelazar los proyectores quirales y conservar las
compresiones no basta para entrelazar el álgebra de restricciones.
No se está atribuyendo (17) al regulador HMT: se refuta la inferencia
general que omitiría X_A,X_B.

Otro control surge del propio generador producto. Si sus expectativas
E_ι conmutan y se ponderan por un lapso escalar externo en la celda,

\[
\mathcal C_m(N)=3\kappa_{\rm av}\sum_\iota
N(\operatorname{cell}\iota)(I-E_\iota),
\quad [\mathcal C_m(N),\mathcal C_m(M)]=0.\tag{18}
\]

(18) no es el álgebra general de deformaciones normales de una
hipersuperficie con métrica dinámica. No se debe renombrar ese
generador gauge como restricción gravitatoria. Las identidades Ward
del propietario son gauge, y su transporte euclídeo de pantallas
conserva el relabelado; no identifica por ese solo hecho todos los
generadores normales espaciales de PCH.

## 6. Un control específico del refinamiento nonádico impar

Se verifica una posible inferencia que no debe usarse: «una malla de
9^m puntos evita por sí misma la duplicación quiral». Para el operador
centrado de diagnóstico sobre un círculo de longitud L,

\[
D_N(p)=\frac1a\sin p,\quad a=L/N,\quad
p_k=2\pi k/N,\quad N=9^m,
\]

la malla impar no contiene exactamente p=π. Sin embargo, en
`k=(N−1)/2` se tiene

\[
D_N(p_k)=\frac NL\sin(\pi/N)\longrightarrow\frac\pi L.\tag{19}
\]

La cota `0≤π−N sin(π/N)≤π³/(6N²)` demuestra el límite. Es una
sucesión de modos de frecuencia espacial cercana al borde de la
malla cuya energía permanece finita; una mera inspección del núcleo
exacto en cada malla impar no detectaría esa rama. La misma
anticomutación formal con una matriz quiral puede conservarse.

Este ejemplo no afirma que el operador HMT sea el centrado ni que
posea esa rama. Muestra qué propiedad espectral tiene que calcularse
para su operador efectivo antes de deducir ausencia de duplicación
del número nueve o de la quiralidad algebraica. Las construcciones
de CAR, la cancelación de anomalías de cargas y el archivo de memoria
no equivalen a ese cálculo.

## 7. Aplicación a deformaciones espaciales arbitrarias

Para las etiquetas de deformación que ya tengan transporte tipado
entre niveles, (13) da la prolongación algebraica exacta. Si las
restricciones contienen coeficientes métricos operatorios, éstos
también forman parte de la palabra ordenada; no se los sustituye
por valores escalares después de calcular el conmutador.

La ampliación de etiquetas cilíndricas a lapsos suaves arbitrarios
necesita continuidad en una topología que controle sus derivadas y
los dominios de los productos. Para el operador espinorial de primer
orden esta composición ya se ha realizado en las dos notas compañeras
`CONMUTADOR_ESPACIAL_ESPINORIAL.md` y
`DEFORMACIONES_ESPACIALES_Y_QUIRALIDAD.md`, leídas en esta intervención.
Con `H=−ia α^j∇_j+B`, `a=ℏ_int c_int`, B hermítico y
`{B,α(ξ)}=0`, definen `A_N=(NH+HN)/2` y demuestran

\[
[A_N,A_M]=-a^2\left(\nabla_v+
\tfrac12\operatorname{div}v+
\tfrac14[\alpha(dN),\alpha(dM)]\right),
\quad v=g^{-1}(N\,dM-M\,dN).\tag{20}
\]

Es una igualdad para lapsos suaves arbitrarios sobre el núcleo suave,
con cancelación demostrada del término másico/Yukawa de ese tipo; no
se deduce de suponer que el álgebra debe cerrar. La segunda nota
construye `P_R=1_[0,R²](D²)` sobre una hoja compacta suave sin borde,
con D el cinético recibido, y prueba que los productos comprimidos
convergen sobre H² al producto sin corte. En particular, el defecto
(16) tiende fuertemente a cero sobre ese núcleo. El corte cotransporta
espín, métrica y quiralidad: `P'_R U_φ=U_φ P_R`. No se confunden sus
identidades con el entrelazamiento fuerte (2) en cada corte finito.

Así existe una realización positiva del paso a lapsos suaves, del
conmutador (20) y de su límite, no sólo la condición abstracta siguiente.
Para extender el mismo razonamiento a otros generadores se requiere
una estimación uniforme de un núcleo común del tipo

\[
\|\mathcal C_m(N_m)\psi_m\|
\le c\,\|N\|_{C^r}\|\psi\|_{\mathcal D},\tag{21}
\]

junto con controles correspondientes para los productos, permitiría
aproximar N y pasar la identidad al límite. Aquí (21) se muestra
como condición concreta de promoción, no como resultado que se
supone satisfecho por cualquier Hamiltoniano finito. Tampoco se
identifica una reparametrización del reloj, aun siendo exacta, con
todas las deformaciones normales locales de una pantalla espacial.

La lectura focal ha recuperado (1)–(7) con los propietarios citados.
Las proposiciones 1–2 y las aplicaciones (8)–(19) reúnen la composición
y los controles de esta nota, reutilizando en (16) la identidad ya
publicada en `MEMORIA_DOMINIO_Y_ALGEBRA.md`; (20) es la prueba nueva
de las notas compañeras.
El rastreo realizado se limita a esas fuentes
activas y sus antecedentes espinoriales; no es una declaración de
inexistencia en el corpus completo. En este conjunto de pruebas,
la flecha más fuerte que no se deduce todavía es identificar el
residuo de los generadores normales **totales** de la geometría
dinámica con cero, no el conmutador material (20), ya calculado,
conservando simultáneamente el operador quiral espacial y sus
dominios de límite. Ni la suspensión continua ni la autoadjunción
por sí solas sustituyen esa identidad.

## 8. Resultado de esta intervención

Se han reunido el límite espacial Yang–Mills y su Gauss, demostrado
su composición con la fibra quiral, extendido la estructura graduada
y CAR al límite inductivo y aplicado el término ya calculado que
se pierde al promover una compresión a un conmutador. Los defectos
son transportables y comprobables; no se ocultan detrás de una
declaración genérica de «compatibilidad».

Esto permite trabajar sobre una ecuación operatoria concreta en la
siguiente composición geométrica: transportar los generadores y
sus cruces de detalle, no reconstruir el núcleo HMT ni volver a
seleccionar sus constantes.

El verificador focal `verificar_limite_espacial_quiral.py` comprueba
mediante matrices exactas el entrelazamiento graduado, la naturalidad
de CAR/Fock, el transporte de conmutadores y el defecto (16), con su
falsador quiral. La sucesión de (19) tiene además controles numéricos
de su cota; la prueba del límite es la desigualdad analítica escrita.
Los fixtures son instancias de las identidades, no nuevos selectores
de estados ni valores físicos HMT.
