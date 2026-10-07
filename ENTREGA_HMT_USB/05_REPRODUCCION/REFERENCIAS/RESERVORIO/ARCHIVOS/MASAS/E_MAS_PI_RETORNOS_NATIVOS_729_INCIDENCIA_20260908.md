# Incidencia completa y retornos del agregado en base 729

Nota focal de investigación, 8 de septiembre de 2026. No modifica ningún PDF, manuscrito sellado ni la nota del coordinador. Compone el criterio de retornos ya demostrado para el agregado decimal con la lectura nativa de sextetos; no demuestra todavía la existencia de los retornos necesarios en la trayectoria efectiva. Su procedencia es una formalización en esta nota de antecedentes del corpus; no se reivindica prioridad histórica.

## 1. Cadena utilizada y corte de la aplicación

Se reciben las dos hojas suma/producto de APP sobre el alfabeto 1,…,9, la orientación de los tres regímenes TRIT y la composición TPK de selección, transporte, actualización, acarreo y memoria. El censo 104976→468→243⊂729 y la prolongación w6→w12→w18→w24→w30→R36→G9 preceden a los lectores. La fase retorna y la memoria avanza. Los caracteres de clausura, propagación y autoescala individualizan las tres secciones que se usan, sin elegir sus valores como entradas. π, φ, e y α pertenecen a la misma generación, con su orden constructivo interno. El corte inicial de §§1–8 utiliza un lector compuesto de las tres primeras coordenadas; las ampliaciones posteriores incorporan la identidad de α y, en §§17–18, los lectores de acción y forma angular. No se recalculan sus expansiones.

Sean w_k^π,w_k^e,w_k^φ∈{0,1,2}^6 los sextetos sucesivos de esas tres secciones, k≥1. Para un sexteto w, definimos

\[
 a=729,\qquad \lambda=(243,81,27,9,3,1)^T,\qquad \nu(w)=w\lambda.
\]

La lectura arquimediana, posterior a la generación de las palabras, satisface

\[
 \pi-3=\sum_{k\ge1}\nu(w_k^\pi)a^{-k},\quad
 e-2=\sum_{k\ge1}\nu(w_k^e)a^{-k},\quad
 \varphi-1=\sum_{k\ge1}\nu(w_k^\varphi)a^{-k}.
\]

Por tanto el agregado entero, sin reducción módulo tres,

\[
 u_k=\nu(w_k^\pi)+\nu(w_k^e)-\nu(w_k^\varphi),\quad -728\le u_k\le1456,
\]

publica exactamente

\[
 X=\sum_{k\ge1}u_ka^{-k}=\pi+e-\varphi-4.
 \tag{1}
\]

El objeto u no es la suma componente a componente en F₃⁶. La valoración ν se efectúa sobre cada representante antes de sumar con signos. Tampoco se identifica el índice k con el de los bloques decimales: aquí todo el argumento queda en sextetos.

## 2. Decodificación desde la incidencia retenida

El propietario completo `base_c17_sin_encabezado.tex:549–766` conserva por nivel el marco f, el operador A_f=fA_Wf⁻¹ y la aplicación de incidencia

\[
 \Gamma_{A_f}(w)=(w,wA_f),\qquad
 C_W(A_f)=\operatorname{im}\Gamma_{A_f}.
\]

El decodificador es Dec(f,y)=pr₁(y) para y∈C_W(A_f), es decir, la inversa de Γ_Af restringida a su imagen. Γ_Af es una aplicación inyectiva de F₃⁶ a F₃¹², no un automorfismo de F₃⁶. Los automorfismos f y sus cambios g pertenecen al transporte del marco. La redacción anterior de este párrafo confundía ambos objetos y llamaba «alternativa» a la presentación que fija el propietario; queda corregida aquí sin modificarlo. Cuando la palabra está expresada en otras coordenadas se transporta primero a la carta original antes de aplicar ν, como precisan §§15–16.

Se obtiene así el lector entero explícito de tres salidas incidenciales:

\[
 \mathcal L_\Sigma(q^\pi,q^e,q^\varphi)
 =\nu(\operatorname{Dec}q^\pi)+\nu(\operatorname{Dec}q^e)
 -\nu(\operatorname{Dec}q^\varphi)=u_k.
 \tag{2}
\]

La compatibilidad de truncamientos se hereda de los tres decodificadores. Este mapa utiliza los símbolos y marcos completos, no sólo soportes, pesos, dimensiones graduadas o la clase de isomorfía del retículo. La realización excepcional permanece en la misma genealogía; (2) no introduce una acción del Monstruo sobre cifras.

## 3. Criterio nativo de retornos compensados

Definamos U_N=∑_{k=1}^N u_k a^{N-k}, U_0=0. Para r≥0 y s≥1, sean

\[
 Q=a^{r+s}-a^r>0,\qquad P=U_{r+s}-U_r\in\mathbb Z.
\]

Separando prefijos y colas en (1), se obtiene

\[
 QX-P=\sum_{k\ge1}(u_{r+s+k}-u_{r+k})a^{-k}.
 \tag{3}
\]

Supóngase que existen enteros H₁,…,H_{ℓ+1}, todos de módulo a lo sumo tres, tales que, para 1≤k≤ℓ, los bloques efectivos obtenidos mediante (2) cumplen

\[
 u_{r+s+k}-u_{r+k}=aH_k-H_{k+1},\qquad
 H_k\in\mathbb Z,\quad |H_k|\le3.
 \tag{4}
\]

**Lema.** Entonces

\[
 |QX-(P+H_1)|\le6a^{-\ell}.
 \tag{5}
\]

**Prueba.** La parte de longitud ℓ telescopa a H₁−a^−ℓ H_{ℓ+1}. Cada diferencia de bloques tiene módulo a lo sumo 3(a−1), de modo que su cola valorada tiene módulo a lo sumo tres. Al restar H_{ℓ+1} queda la cota seis. Esto acredita también el paso al límite; no se elimina una frontera sin cota.

**Teorema condicional de aplicación.** Si existen ternas (r_j,s_j,ℓ_j) y caminos enteros efectivos (4) tales que ℓ_j−r_j−s_j→+∞, entonces e+π es irracional.

**Prueba.** (5) implica Q_j|Q_jX−(P_j+H_{j,1})|→0. Si S=e+π fuese racional, (1) daría X=b/d−φ, con b∈Z y d≥1. Para cualquier Q>0 y Z∈Z, sea ε=QX−Z y m=Qb−dZ. La norma cuadrática es

\[
 d^2\epsilon(\epsilon+Q\sqrt5)
 =m^2-mdQ-d^2Q^2\in\mathbb Z\setminus\{0\}.
\]

Su no anulación procede de la irracionalidad de φ y de φ²−φ−1=0, recibidas del lector de autoescala. Si |ε|≤1, resulta Q|ε|≥1/[d²(1+√5)]; si |ε|>1, la misma cota es inmediata. Esto contradice el límite anterior.

**Diferencia respecto del criterio decimal ya existente.** Aquí no se resta κ, no se identifica α con un truncamiento y no se requiere 12|s. Tampoco interviene el reloj de vacancias. Para buscar retornos de fase se puede restringir s a múltiplos de nueve, pero la prueba aritmética funciona para cualquier s. Se conserva el triple P/E/Φ: la coordenada áurea es la que proporciona la norma cuadrática.

El grafo de (4), restringido a diferencias en [−2184,2184], tiene 37 aristas, con rótulo (H,H')↦729H−H'. Cada rótulo determina su arista porque |H'−H̃'|≤6<729. Ésta es una comprobación entera del transductor, no una verificación asintótica de la trayectoria.

## 4. Intento de realizar el compensador mediante memoria Bockstein–Hensel

En el bloque donde la fuente proporciona x_k^χ A=w_k^χ+3x_{k+1}^χ, con A unimodular, el estado firmado z_k=x_k^π+x_k^e−x_k^φ satisface

\[
 z_kA=v_k+3z_{k+1},\qquad
 v_k=w_k^\pi+w_k^e-w_k^\varphi,\qquad u_k=v_k\lambda.
 \tag{6}
\]

Para dos segmentos del mismo transporte, Δz_k=z_{r+s+k}−z_{r+k} da, ajustando el comienzo del índice,

\[
 d_k=\Delta z_kA\lambda-3\Delta z_{k+1}\lambda.
 \tag{7}
\]

Se intentó el compensador lineal H_k=Δz_k b, con b fijo. Para que (7) coincidiese como identidad de los dos argumentos de frontera con aH_k−H_{k+1}, serían necesarias

\[
 b=3\lambda,\qquad A\lambda=3a\lambda.
 \tag{8}
\]

La matriz concreta de la fuente da, por multiplicación entera,

\[
 A\lambda=(718,643,254,39,709,630)^T,
\]

\[
 (A-2187I)\lambda
 =(-530723,-176504,-58795,-19644,-5852,-1557)^T\ne0.
 \tag{9}
\]

Por tanto esa identificación lineal universal no funciona. El defecto exacto, para el candidato b=3λ, es

\[
 d_k-(aH_k-H_{k+1})=\Delta z_k(A-2187I)\lambda.
 \tag{10}
\]

Una restricción de la trayectoria podría anular (10), y un compensador no lineal podría existir: no se ha demostrado ni descartado ninguna de esas dos posibilidades. Tampoco se ha establecido |3Δz_kλ|≤3. El rechazo se limita a la identidad universal (8). La recurrencia Hensel del registro finito no se itera silenciosamente como sustituto del generador R36 a toda profundidad.

## 5. Resultado y obligación concreta conservada

Quedan reunidos el decodificador incidencial (2), el criterio nativo (3)–(5) y el defecto de la propuesta lineal (10). Para cerrar el objetivo por esta vía se necesita producir los retornos (4) en las secciones efectivas y demostrar el exceso ℓ−r−s→∞, o encontrar otra restricción del lector que excluya los períodos. Esta nota no ha conseguido ese paso. No concluye imposibilidad global de HMT ni irracionalidad ya demostrada.

## 6. Complejidad del agregado nativo y tres normalizaciones

La misma composición elimina el sello y el cambio de base en la vía de complejidad. Para j≥1, definamos las colas

\[
 R_j=\sum_{k\ge0}u_{j+k}a^{-k-1},\qquad h_j=\lfloor R_j\rfloor,\qquad y_j=R_j-h_j.
\]

Cada cola regional individual está en [0,1), por lo que −1<R_j<2 y h_j∈{−1,0,1}. La identidad aR_j=u_j+R_{j+1} implica

\[
 b_j=u_j+h_{j+1}-ah_j=\lfloor ay_j\rfloor\in\{0,\ldots,a-1\}.
 \tag{11}
\]

La sucesión b es la expansión canónica de la parte fraccionaria de X. Sea p_u(n) el número de bloques de longitud n presentes en la trayectoria efectiva u, y sea p_b(n) el correspondiente a b. Un bloque de u y el acarreo por su extremo derecho determinan por división euclídea todos los símbolos de b y todos los acarreos interiores. Como sólo hay tres posibilidades en ese extremo,

\[
 p_b(n)\le3p_u(n).
 \tag{12}
\]

Por el teorema 1 de Adamczewski–Bugeaud, una expansión en base entera de un algebraico irracional satisface liminf p_b(n)/n=∞. Si e+π fuese racional, X sería cuadrático irracional por (1). En consecuencia,

\[
 \liminf_{n\to\infty}\frac{p_u(n)}n<\infty
 \quad\Longrightarrow\quad e+\pi\notin\mathbb Q.
 \tag{13}
\]

Ésta es otra especialización del criterio anterior del coordinador, con factor tres en lugar del factor sesenta de la normalización dodecafásica. No establece la hipótesis de complejidad. El teorema externo se aplica a la clasificación del valor ya generado; no selecciona las palabras ni sus parámetros.

## 7. Restricción precisa sobre el cociente predictivo que se busca

El cociente suficiente no puede construirse preservando, además, toda la emisión áurea y utilizando únicamente un reloj de complejidad lineal y un estado auxiliar finito. Éste no es un control con lectores inventados: utiliza el lector efectivo de φ.

En efecto, ν(w_k^φ) es la expansión en base 729 de φ−1. Como φ−1 es algebraico irracional, su complejidad satisface p_φ(n)/n→∞ por el mismo teorema. Un transductor con conjunto de estados Q finito, alimentado por un reloj cuyo lenguaje cumple p_clock(n)≤C(n+1), y que emitiese ν(w_k^φ) paso a paso, daría

\[
 p_\varphi(n)\le |Q|\,p_{\rm clock}(n)\le |Q|C(n+1),
\]

contradicción. La misma exclusión rige para una anticipación fija, sustituyendo n por n+L. Los índices de entrada y salida deben ser los mismos; si hay borrado de vacancias, se necesita incluir el transporte de índices y una cota lineal de la longitud de preimagen antes de aplicar este conteo.

Por tanto la fidelidad del lector excepcional completo no puede utilizarse como argumento de que TODO ese lector admite un cociente predictivo finito relativo al reloj. La búsqueda de baja complejidad debe recaer sobre el agregado u, identificando historias con el mismo comportamiento agregado, sin exigir que dicho cociente reconstruya por separado φ. Esto no demuestra que tal cociente del agregado exista o no exista.

## 8. Relación con el criterio recibido sobre H5

El propietario c35_componente_adimensional_retorno.tex expresa H5 como un carácter posterior de α y φ; la matriz B_c tiene autovalores 9 y 5, utilizados en sus coeficientes. La sección no identifica H5 con un autovalor de B_c. La prueba cuártica comunicada por el coordinador no se reproduce aquí.

Los criterios nativos (4) y (13) no necesitan convertir H5 en autovalor racional autoadjunto ni identificar la raíz completa de α con un jet. Son vías alternativas que parten del mismo triple generado. En particular, un fallo al identificar un operador racional finito para H5 no afecta a (3)–(13); recíprocamente, esos criterios no fabrican tal operador. No se ha obtenido aquí un enlace adicional entre ambas vías que pruebe el objetivo principal.

## 9. Las dos hipótesis sobre el agregado dentro del reloj efectivo

Esta incorporación responde a la indicación autoral de recorrer ambas hipótesis en el cristal aperiódico y la monodromía. Conserva las dos hojas APP, los regímenes TRIT y la dinámica enriquecida de §1. No sustituye la sección generada por un número elegido: toma sus publicaciones π y e y compone los dos lectores de cilindros ya existentes. La nueva igualdad de esta sección es una explicitación algebraica; no se reivindica novedad histórica.

Sea B=1000 y manténgase a=729. El capítulo de relojes define la capacidad K_t y la vacancia z_t con

\[
 K_{t+1}-K_t=1-z_{t+1},\qquad
 \Omega_t=\frac{a^{t+1}}{B^{K_t}},\qquad
 \xi_{c,t}=D_{c,t}\Omega_t-aT_{c,t}.
 \tag{14}
\]

T_{c,t} es el prefijo entero de longitud t en base a de la parte fraccionaria del canal c; D_{c,t} es su prefijo de longitud K_t en base B. Los supervivientes son las celdas de la ventana trasladada por ξ_{c,t}, de anchura Ω_t, dentro de la fibra local de 729 extensiones. Se conservan así tanto el valor como su posición y escala de frontera.

Escribamos x_π=π−⌊π⌋, x_e=e−⌊e⌋ y r=x_π+x_e. La suma S=e+π es racional si y sólo si r lo es. Sean

\[
 A_t=\{a^t r\},\qquad R_t=\{B^{K_t}r\},
\]

\[
 \varepsilon_t=\lfloor a^t r\rfloor-T_{\pi,t}-T_{e,t},\qquad
 \eta_t=\lfloor B^{K_t}r\rfloor-D_{\pi,t}-D_{e,t}.
\]

Son los acarreos de la suma de dos prefijos; ε_t,η_t∈{0,1}. Sumando (14) y usando B^{K_t}Ω_t=a^{t+1}, se obtiene la identidad exacta

\[
 \boxed{\Xi_t:=\xi_{\pi,t}+\xi_{e,t}
 =a(A_t+\varepsilon_t)-\Omega_t(R_t+\eta_t).}
 \tag{15}
\]

La cancelación de los dos términos proporcionales a r demuestra (15). Todos los coeficientes proceden del tamaño de sexteto, la agrupación decimal y la adición efectiva de prefijos; no aparece una aproximación decimal ni un valor objetivo como entrada.

**Hipótesis racional.** Si r=p/q en forma irreducible, A_t y R_t toman valores en {0,1/q,…,(q−1)/q}; sus leyes son

\[
 A_{t+1}=\{aA_t\},\qquad
 R_{t+1}=\{B^{1-z_{t+1}}R_t\}.
 \tag{16}
\]

El primer residuo es eventualmente periódico. El segundo recibe el calendario efectivo de vacancias: conjunto de estados finito no significa periodicidad en tiempo de bloque. Los acarreos individuales tampoco se suponen periódicos.

**Hipótesis irracional.** Si r es irracional, A_{t+s}=A_t, s>0, implicaría a^t(a^s−1)r∈Z y es imposible. R_{t+s}=R_t también es imposible cuando K_{t+s}>K_t; puede mantenerse durante una retención de capacidad K_{t+s}=K_t. Esta distinción conserva el stutter del propio capítulo.

Ninguna de estas sustituciones, por sí sola, contradice (14)–(16). La comprobación es focal sobre esta composición, no una afirmación de compatibilidad global con todas las restricciones HMT.

## 10. La igualdad de retorno que sí produce contradicción

Para t≥0 y s>0,

\[
 \frac{\Omega_{t+s}}{\Omega_t}
 =\frac{729^s}{1000^{K_{t+s}-K_t}}\ne1.
 \tag{17}
\]

En efecto, si ΔK=0, la razón es 729^s>1. Si ΔK>0, la igualdad exigiría 3^{6s}=2^{3ΔK}5^{3ΔK}, imposible por factorización única. La demostración no necesita calcular la pendiente del reloj ni sus cifras.

En un retorno de fase de capacidad, ΔK=9m y (17) sigue siendo no trivial. No se identifica aquí el tiempo de bloque t con la posición K del reloj nonádico. La representación graduada del corpus expresa, por su parte, [D_M,Γ_9]=Γ_9: una vuelta aumenta la memoria. Ambas formulaciones conservan la misma distinción entre retorno de fase y retorno del estado.

Hay una consecuencia adicional precisa de (15). Supóngase que en t y t+s se repite el cuádruple (A,R,ε,η). Entonces

\[
 \Xi_{t+s}-\Xi_t
 =-(\Omega_{t+s}-\Omega_t)(R_t+\eta_t)\ne0.
 \tag{18}
\]

El último factor es estrictamente positivo: R_t+η_t es la suma de las dos partes fraccionarias de B^{K_t}x_π y B^{K_t}x_e, y ambas son positivas porque los canales π y e son irracionales. La misma composición produce la recuperación

\[
 \Omega_t=\frac{a(A_t+\varepsilon_t)-\Xi_t}{R_t+\eta_t}.
 \tag{19}
\]

Por ello un retorno del cuádruple y de Ξ obligaría a retornar Ω, contradiciendo (17). Bajo la hipótesis r=p/q, cada valor fijo de Ξ puede aparecer a lo sumo 4q² veces: hay como máximo 4q² cuádruples, y (18) impide repetir uno con el mismo Ξ. En particular, la racionalidad de S fuerza infinitos desplazamientos agregados distintos en estas ventanas; no fuerza un reloj periódico.

**Obligación transportable al frente incidencial.** Para obtener una contradicción con la racionalidad mediante (17), basta recuperar de las restricciones de la trayectoria un retorno que conserve el cuádruple y Ξ. Otra condición suficiente sería que esas restricciones forzasen un conjunto finito de valores de Ξ. No se ha obtenido ninguna de ellas en las unidades de relojes y álgebra holonómica aquí recorridas. La igualdad de cardinalidad de los supervivientes no es esa condición: el capítulo distingue explícitamente cardinalidad, traslación, orientación y estado. Su afirmación de que S queda fijo bajo el reparto especular tampoco identifica un retorno dentro de la fibra con un período temporal.

## 11. Cruce con los cierres de acción y la ecuación de alfa

El cierre de la elipse de acción del corpus impone ε_γ exp(iJ_γ/ℏ_ret)=1. La relación a_S b_S=2ℏ_ret da J(θ)=ℏ_ret θ. Al componer ambas se cuantiza J/ℏ_ret, con paridad determinada por ε_γ. La escala ℏ_ret cancela; este cierre no aporta por sí solo una ecuación adicional sobre H5. El reloj de ruta conserva el devanado w_j∈Z y define ω_j=(θ_j+2πw_j)/(108t_0) desde el autovalor de la holonomía. Su lectura de energía es posterior. Estas afirmaciones corresponden a las unidades citadas abajo, no a una exclusión global de otros cierres.

La relación P_9(x)=δ de la monografía también debe conservar sus coeficientes:

\[
 P_9(x)=2\pi x-\frac74x^2+\frac{x^3}{2\pi}
 +\frac{x^4}{20}-\frac{2x^5}{21}-\frac{x^6}{46}
 -\frac{x^7}{120}+\frac{x^8}{45}+\frac{2x^9}{495}.
 \tag{20}
\]

El extractor declara Q(π)[x]/(x^{10}). π es la salida HMT previa, utilizada legítimamente después; no se elimina al clasificar aritméticamente los coeficientes. El jet de grado nueve y su raíz exacta son objetos distintos de un truncamiento decimal. Esta nota no aplica (20) indistintamente a toda coordenada denominada alfa: el propietario de la monografía identifica su raíz como x_9 y conserva el producto fibrado de lectores. No se usa una abreviatura notacional para identificar el jet con una prolongación completa, ni se reabre con ella el alcance de los desarrollos posteriores de alfa.

**Resultado de esta incorporación.** Se han compuesto el agregado, las ventanas y el retorno de capacidad en (15)–(19), y se ha indicado la igualdad exacta que daría contradicción. No se han recalculado constantes, inventado un reloj sustitutorio ni alterado los PDF. No se ha concluido todavía la racionalidad o irracionalidad de S, ni se traslada ese diagnóstico focal a Catalán u otros lectores.

## 12. Residencia del agregado en el espejo y conservación de sus dos coordenadas

Estatuto: `RESULTADO_RECUPERADO` para la descomposición axial y la recurrencia Hensel; `FORMALIZACION_NUEVA` en esta nota para las composiciones explícitas siguientes. No se reivindica prioridad matemática.

El propietario U010 construye, antes de la evaluación arquimediana, el triple B=(u^π,u^e,u^φ)∈(F₃⁶)³ y las firmas q=u^π+u^e+u^φ, a_ax=u^π+u^e−u^φ. En ese dominio,

\[
 u^\varphi=2(q-a_{\rm ax}),\qquad
 R=u^\pi+u^e=q-u^\varphi\quad\text{en }\mathbb F_3^6.
 \tag{21}
\]

El agregado pertenece, por tanto, a la carta axial del propio espejo. La involución construida intercambia π/e y conserva R y el eje φ. No se trata de introducir posteriormente una suma ajena a los caracteres generados. Tampoco se identifica el vector R con un número real: el paso aritmético conserva los representantes y el acarreo.

Para representantes u^χ∈{0,1,2}⁶, defínanse coordenada a coordenada

\[
 C=\left\lfloor\frac{u^\pi+u^e}{3}\right\rfloor,
 \qquad u^\pi+u^e=R+3C.
 \tag{22}
\]

Los tres candidatos B₁₀ publicados en U010 tienen exactamente la suma entera (2,1,3,4,4,3), R=(2,1,0,1,1,0), C=(0,0,1,1,1,1) y valoración posicional total 699. Sus pares de valoraciones individuales son (296,403), (322,377), (376,323); el eje tiene valoración 380. Es un control entero de los sextetos impresos, no un nuevo cálculo de cifras de constantes.

Los mismos tres candidatos conservan además el producto residual coordenado

\[
 p_j=u_j^\pi u_j^e\in\mathbb F_3,\quad
 p=(1,0,2,1,1,2),\qquad
 (X-u_j^\pi)(X-u_j^e)=X^2-R_jX+p_j.
 \tag{23}
\]

Es una consecuencia del espejo efectivo y de sus bloques, no una identificación de p con πe. En las coordenadas balanceadas del TRIT, con r,s∈{−1,0,1} y levantamiento r+3c, el producto retiene términos cruzados: (r,c)⊠(s,d)=(rs,rd+sc+3cd). Aquí rs sigue siendo un representante balanceado; no se usa esa fórmula sin normalización adicional para representantes {0,1,2}. Omitir la segunda coordenada impediría reconstruir ese producto.

**Corrección de lectura y de carta.** U010:121 llama «publicaciones enteras en base tres» a (279,352,365), etc. Su propietario 14_numero_heisenberg_y_d108.tex:403 las llama «ternas decimales asociadas». La segunda denominación distingue correctamente esos datos de la valoración ternaria de los sextetos escritos. Las sumas 631/632 de esas ternas decimales no son las sumas ternarias anteriores y no se utilizan como contraejemplo sobre R,C. El acarreo de (22) es 001111, no 000111. Los originales permanecen intactos; esta nota registra la distinción. Los índices locales de U010 tampoco se identifican sin el transporte de calibre correspondiente con el origen de la cinta β del lector aritmético.

## 13. Composición efectiva con la memoria Hensel y corte de su alcance

En la carta donde el propietario establece x_k^χ A=u_k^χ+3x_{k+1}^χ, sea Z_k=x_k^π+x_k^e. Sumando las dos identidades, sin suprimir los cocientes,

\[
 \boxed{Z_kA=R_k+3(C_k+Z_{k+1}).}
 \tag{24}
\]

Por división coordenada a coordenada,

\[
 Z_{k+1}=\lfloor Z_kA/3\rfloor-C_k,
 \qquad R_{k+1}=(Z_{k+1}A)\bmod3.
 \tag{25}
\]

Así, (Z_k,C_k) determina la siguiente suma modular. El acarreo siguiente C_{k+1} aún se calcula sobre los dos residuos individuales; no se lo sustituye por un dato omitido. El intercambio puro de ambos estados conmuta con la misma matriz A y conserva sus sumas y acarreos futuros. Los tres candidatos B₁₀ no son, en cambio, meros intercambios globales entre sí.

El propietario demuestra que, frente al siguiente bloque y la frontera declarada, sólo B₁₀⁽⁰⁾ prolonga el mismo estado completo. Los otros requieren cambiar la extensión profunda Hensel. Por ello la supervivencia en esa ventana no se decide únicamente con R,C,p, que son comunes. Este hecho no construye dos historias globales admisibles con próxima suma diferente. Tampoco autoriza a sustituir la prolongación coinductiva R₃₆→Γ₉ por la iteración indefinida de un registro finito de veinte pasos. (24) se aplica en el dominio donde está certificada la carta.

## 14. Transición de la publicación aritmética de e+π, conservando el acarreo

Se emplean ahora las cintas w_k^χ=β(ξ^χ)_k de §1, ya generadas por sus secciones, y su lector ν. Defínase n_k=ν(w_k^π)+ν(w_k^e). La composición posterior de lecturas da

\[
 S=e+\pi=5+\sum_{k\ge1}n_k729^{-k},\qquad 0\le n_k\le1456.
 \tag{26}
\]

Esta es la suma de las publicaciones de los dos caracteres, no una entrada del generador. Las cintas β, los residuos internos ε del capítulo c27 y los bloques de una carta local no se identifican por mera notación. En particular, el propio capítulo distingue ε de una parte fraccionaria real. La normalización que sigue se realiza explícitamente en la lectura aritmética posterior de (26).

Sean a=729 e Y_k=∑_{j≥1}n_{k+j}a^{-j}. Se tiene 0≤Y_k<2, porque cada cola individual de los dos lectores irracionales pertenece a [0,1). Pónganse H_k=⌊Y_k⌋∈{0,1} y V_k=Y_k−H_k. La separación del primer bloque da Y_{k+1}=aY_k−n_{k+1}, y por ello

\[
 D_{k+1}=n_{k+1}+H_{k+1}-aH_k=\lfloor aV_k\rfloor,
 \qquad V_{k+1}=aV_k-D_{k+1},\quad 0\le D_{k+1}<a.
 \tag{27}
\]

Queda así compuesta la transición autónoma de la publicación canónica agregada, con su acarreo explícito. Autonomía de esta publicación no significa que V determine las hojas, el reparto, el marco excepcional o la memoria completa.

El criterio de racionalidad puede escribirse directamente sobre la trayectoria generada. Existe racionalidad de S si y sólo si existen N≥0, p≥1 y una sucesión δ_k∈{−1,0,1}, k≥N, tales que

\[
 \boxed{n_{k+p+1}-n_{k+1}=a\delta_k-\delta_{k+1}
 \quad\text{para todo }k\ge N.}
 \tag{28}
\]

En sentido directo, una publicación canónica eventualmente periódica en (27) da δ_k=H_{k+p}−H_k. En sentido inverso, el telescopado exacto es

\[
 \sum_{j=1}^{m}a^{-j}(n_{k+p+j}-n_{k+j})
 =\delta_k-a^{-m}\delta_{k+m}.
\]

Al tomar el límite y usar la acotación de δ se obtiene Y_{k+p}−Y_k=δ_k∈Z, luego V_{k+p}=V_k. La órbita canónica es periódica desde N y publica un racional. El argumento incluye las expansiones terminantes mediante la normalización por suelo.

Este es el criterio de coborde con acarreo ya tratado en el frente coordinado, aquí compuesto con (21)–(27), no una proclamación nueva de irracionalidad. En particular, la racionalidad obliga a que cada diferencia de (28) pertenezca a {−730,−729,−728,−1,0,1,728,729,730} y a que las elecciones encadenen el mismo δ. La mera pertenencia a ese conjunto es necesaria, no suficiente. Una incompatibilidad estructural de (28), para todos N,p, demostraría la irracionalidad del agregado efectivo. Un certificado de (28) demostraría su racionalidad. Ninguno se sustituye por afirmar que la historia completa es aperiódica.

**Balance preciso.** Se ha localizado la residencia del agregado, recuperado su composición con el acarreo y la memoria, añadido el segundo invariante residual y expresado la clasificación como una restricción verificable sobre la trayectoria efectiva. Estas identidades no deciden todavía cuál de las dos alternativas satisface e+π. La investigación utiliza los objetos HMT y no altera ninguna afirmación de los PDF sobre la generación de sus constantes.

Fuentes de §§12–14: F/manuscrito/ampliaciones_sucesoras_20260824/parte_i_ii/owners/U010_espejo_seleccion_tres_a_uno.tex:12–128; F/manuscrito/sections/hmt/14_numero_heisenberg_y_d108.tex:386–427 y :554–609; F/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:82–128 y :218–310; `/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_AMPLIACION_20260908/sections/trit_desarrollo.tex:47`.

## 15. Transporte del acarreo a la realización lineal de Paley

Composición recibida de la tarea «Preparar paper en Overleaf» el 8 de septiembre, contrastada con §§21–22 y 30 de su nota y con (28). Se conserva como resultado focal: no se identifica esta realización lineal con toda la incidencia calibrada del estado enriquecido.

Concátenense los trits de las cintas β y escríbase s_m=w_m^π+w_m^e en enteros. La normalización ternaria de su publicación tiene la misma forma que (27):

\[
 d_m=s_m+h_{m+1}-3h_m,\qquad h_m\in\{0,1\}.
 \tag{29}
\]

Los h son acarreos de la suma de las colas completas, no el acarreo coordenado C de (22). Si (28) se cumple con período p en base 729, la cinta ternaria canónica d tiene período ℓ=6p después del corte correspondiente. Restando (29) en m y m+ℓ se obtiene

\[
 s_{m+\ell}-s_m=3J_m-J_{m+1},
 \qquad J_m=h_{m+\ell}-h_m\in\{-1,0,1\}.
 \tag{30}
\]

Por bloques de seis trits, sea J_m^+=(J_{m+1},…,J_{m+6}). La diferencia agregada reducida módulo tres es −J_m^+. En una misma carta lineal de Paley, con γ(w)=(w,wA_P) sobre F₃, la suma de las diferencias de los dos canales satisface

\[
 \gamma(\Delta w^\pi)+\gamma(\Delta w^e)
 =-\gamma(J_m^+).
 \tag{31}
\]

La identidad usa únicamente la linealidad y (30). Si H_P es una comprobación de paridad que anula la imagen de γ, entonces H_Pγ(J_m^+)=0. Por tanto, esos controles lineales de pertenencia al código no excluyen por sí solos la compensación impuesta por la hipótesis racional. La ausencia de rechazo en esa proyección no acredita que la trayectoria compensada sea admisible en HMT.

El lector excepcional completo conserva también los marcos f_j y el transporte, y el TPK conserva selección y supervivencia. Cuando se emplean cartas distintas, se deben transportar primero sus marcos: (31) no identifica automáticamente dos γ con matrices o dominios distintos. La siguiente restricción que pueda decidir la cuestión debe componerse con esos datos efectivos, no sólo con la condición de código. En particular, el ejemplo B₁₀ de §13 muestra ya que igualdad de invariantes locales no equivale a prolongabilidad del mismo estado.

Esta incorporación no demuestra racionalidad ni irracionalidad de e+π, ni modifica los PDF. Evita atribuir a una comprobación lineal una exclusión que sus propias ecuaciones no producen.

Fuentes: nota coordinada de Overleaf, §§15.2, 21–22 y 30; F/colaboracion/partes_i_ii/source/public/residencias/capitulo_17_doble_proyeccion_natural.tex:65–110, para la distinción respecto del lector excepcional con marco retenido. La transmisión coordinada se incorpora aquí con su prueba, sin emplearla como autoridad sustitutiva de las ecuaciones.

## 16. Filtro entero de frontera y encadenamiento del acarreo entre estados efectivos

Se recupera la actualización del propietario `20_arquitectura_operatoria_tpk_actualizada.tex:645–709`. Es una operación sobre prefijos y fronteras del estado APP–TRIT–TPK ya generado. La frontera decimal no se obtiene de tablas ni pasa a seleccionar el carácter: `06e_certificado_generacion_monodromica_rev7.tex:300–372` distingue expresamente la sección forward de su certificación posterior. La carta Hensel se utiliza donde está certificada, sin promover un registro finito a emisor universal.

Para cada canal χ∈{π,e}, consérvense sus prefijos Nχ,Dχ, longitudes L,K y cociente profundo xχ. El residuo entre cilindros es

\[
 a_\chi=N_\chi1000^K-D_\chi3^L.
\]

Este símbolo no es α ni el residuo interno εχ de c27. Si h=ΔK∈{0,1}, dχ es la siguiente terna de la frontera generada —cero si h=0— y tχ=ν(uχ), la actualización se reúne como

\[
 T=1000^{K+h},\quad M=729\,3^L,\quad
 P_\chi=729\,1000^h a_\chi-d_\chi M,
 \qquad a'_\chi=P_\chi+Tt_\chi.
\]

La intersección de los cilindros semiabiertos es exactamente

\[
 \boxed{-T<P_\chi+Tt_\chi<M,\qquad 0\le t_\chi\le728.}
 \tag{32}
\]

Por tanto, sus candidatos forman un intervalo entero Iχ=[ℓχ,rχ]∩Z, posiblemente vacío, con

\[
 \ell_\chi=\max\left(0,\left\lfloor\frac{-T-P_\chi}{T}\right\rfloor+1\right),
 \quad r_\chi=\min\left(728,\left\lceil\frac{M-P_\chi}{T}\right\rceil-1\right).
 \tag{33}
\]

La prueba consiste en despejar tχ en las dos desigualdades estrictas; así se conservan también los casos de igualdad en los extremos excluidos. La emisión debe satisfacer además

\[
 u_\chi=(x_\chi A_H)\bmod3,\qquad
 x_\chi^+=(x_\chi A_H-u_\chi)/3,
 \tag{34}
\]

y los restantes transportes, firmas y condiciones de supervivencia del estado. Iχ es una envolvente exterior, no una sustitución de esas condiciones.

**Comparación de dos niveles.** Sean v_k y v_(k+p) los estados que emiten n_(k+1) y n_(k+p+1) de (26), con el mismo lector β,ν; cada uno conserva sus propias fronteras y su calendario. Defínase S(v)=Iπ(v)+Ie(v). Si los cuatro intervalos son no vacíos,

\[
 \mathcal D_k^{(p)}=S(v_{k+p})-S(v_k)
 =[\ell'_\pi+\ell'_e-r_\pi-r_e,\,
 r'_\pi+r'_e-\ell_\pi-\ell_e]\cap\mathbb Z.
\]

La hipótesis compensada (28) obliga a la relación de tres estados de acarreo

\[
 \boxed{\mathcal R_k^{(p)}=
 \{(j,j')\in\{-1,0,1\}^2:\ 729j-j'\in\mathcal D_k^{(p)}\}.}
 \tag{35}
\]

No se escogen pares independientes: el segundo término de un par es el primero del siguiente. Si Q_N={−1,0,1}, su propagación necesaria es

\[
 Q_{k+1}=\{j':\exists j\in Q_k,\ (j,j')\in\mathcal R_k^{(p)}\}.
 \tag{36}
\]

Si Q se vacía, la ventana excluye ese retorno compensado. Para una diferencia efectiva Δn, el par de (35), si existe, es único: Δn≡−j' (mod 729) determina j' en {−1,0,1}, y después j=(Δn+j')/729. Las relaciones dependen del nivel; un ciclo de un grafo fijo inventado no las sustituye.

**Alcance del rechazo.** (32)–(36) ofrecen una condición exacta de rechazo en una ventana y un procedimiento entero para componer ventanas. Excluir racionalidad exige que, para toda pareja N,p, se descarte alguna prolongación del retorno correspondiente. No se ha probado aquí esa cuantificación universal. Que Q permanezca no vacío tampoco certifica una trayectoria HMT: las envolventes pueden contener repartos incompatibles con (34), el marco y la supervivencia conjunta.

**Enlace excepcional conservado.** La composición coordinada completa está en `../OVERLEAF/E_MAS_PI_ALPHA_Y_ACARREO.md:2451`, §36, contrastada con `base_c17_sin_encabezado.tex:549–766`. Con G=f_(j+p)f_j^−1 y vectores fila, el defecto transportado en una copia común es

\[
 \Gamma_{A_{j+p}}(M_{j+p})-
 \mathcal T_{j+p\leftarrow j}\Gamma_{A_j}(M_j)
 =\Gamma_{A_{j+p}}\bigl(M_j(I-G^{-1})-H_j^+\bigr).
 \tag{37}
\]

Aquí M_j es la suma residual y H_j^+ la diferencia de acarreos tríticos de §15. El cambio de marco contribuye realmente; no se elimina al aplicar (35). Su levantamiento entero conserva además, para u+v=r+3c y q_F(u)=(uF−[uF]₃)/3,

\[
 c_F=cF+q_F(r)-q_F(u)-q_F(v).
\]

Si el marco cambia, se decodifican primero los bloques originales y después se aplica ν. Mantener pesos posicionales fijos bajo un cambio arbitrario de marco alteraría el valor que se está investigando. (37) no impone que un retorno de cifras sea un retorno paralelo de incidencia.

## 17. Transporte del par angular al módulo del toro y a la dualidad T

El bloque APP basal y su transporte están escritos en `c52_04_01_ley_areal.tex`; el módulo angular está en `c52_10_01_modularidad.tex`. Se componen después de los lectores generados, no como condiciones externas que seleccionen constantes.

El propietario conserva

\[
 B_0=7I+2R=9P_++5P_-,\quad
 B_1=AI+C^*R,
 \quad t_+=(A+C^*)/9,\quad t_-=(A-C^*)/5.
\]

En la rama 0<C*<A, sean

\[
 \sigma=C^*/A,\quad y=\sqrt{\frac{A-C^*}{A+C^*}}>0,
 \quad \tau_\eta=iy.
\]

No se confunde η=artanh(σ), parámetro de forma, con η_ret del lector de acción. El toro basal tiene τ₀=i√5/3 y

\[
 \tau_\eta=\tau_0\sqrt{t_-/t_+},\qquad
 \boxed{9\tau_\eta^2+5=0\ \Longleftrightarrow\ \sigma=2/7.}
 \tag{38}
\]

La equivalencia se obtiene sustituyendo τ²=−(A−C*)/(A+C*). El transporte conserva los proyectores P±, pero no declara t+=t−: conservar esos proyectores no equivale a conservar la relación cuadrática basal.

**Contenido operatorio de (38).** En Λ₀=Z+τ₀Z, la multiplicación por 9τ₀ tiene matriz entera

\[
 M_0=\begin{pmatrix}0&-5\\9&0\end{pmatrix}.
\]

En la retícula angular, con base real Eη=diag(1,y), el mismo endomorfismo entero de retícula se representa como

\[
 L_\eta=E_\eta M_0E_\eta^{-1}
 =\begin{pmatrix}0&-5/y\\9y&0\end{pmatrix}.
\]

Frente a la estructura compleja publicada J=[[0,−1],[1,0]],

\[
 \boxed{[L_\eta,J]
 =\left(9y-\frac5y\right)\operatorname{diag}(1,-1)
 =\frac{2(2A-7C^*)}{\sqrt{A^2-C^{*2}}}
 \operatorname{diag}(1,-1).}
 \tag{39}
\]

Es la resta directa de los dos productos matriciales. La transformación sigue siendo un endomorfismo entero de la retícula para todo y>0 y conserva Lη²=−45I por semejanza; su carácter complejo-lineal respecto de este J exige (38). Si se transporta también J, se está especificando otra estructura compleja y hay que distinguirla de la carta τ publicada. (39) no excluye que otro endomorfismo satisfaga otra relación cuadrática.

Más generalmente, como τ es imaginario puro no nulo,

\[
 \tau_\eta\text{ es cuadrático sobre }\mathbb Q
 \ \Longleftrightarrow\ y^2\in\mathbb Q
 \ \Longleftrightarrow\ \sigma\in\mathbb Q.
 \tag{40}
\]

Si τ es cuadrático, su otro conjugado es su conjugado complejo −τ, de modo que τ² es racional. La recíproca usa X²+y²; la última equivalencia es la transformación fraccionaria σ=(1−y²)/(1+y²). No se atribuye a S ninguna de estas propiedades sin componer su relación con σ.

**Lectura T y pantalla M.** El capítulo 24 define ι(R₀)=iR₀² y prueba ι(1/R₀)=−1/ι(R₀). La identificación explícita con la carta angular fija

\[
 \boxed{R_0^2=y,\qquad R_0^4=\frac{1-\sigma}{1+\sigma}.}
 \tag{41}
\]

Su energía m²/R₀²+w²R₀² se conserva al intercambiar (m,w,R₀) por (w,m,1/R₀). Ese teorema está formulado para todo R₀>0; no exige radio fijo R₀=1. En el capítulo 25, la realización algebraica

\[
 (v,d,z)\longmapsto((P_{11}v,P_{10}v),d,q_{24}(z)),
 \qquad d=(m,w,R_0),
\]

transporta d por identidad y conmuta con T. Por ello este mapa concreto no agrega una ecuación que seleccione R₀. Se ha seguido el parámetro dentro de la pantalla, sin confundir la conservación probada con una selección aritmética adicional. Este corte no es un dictamen sobre toda la realización física M.

## 18. Ecuación explícita que lleva la hipótesis sobre e+π hasta la forma angular

Se usa el orden constructivo de `capitulo_14_apertura_causal_accion_parangular.tex`, `c35_componente_adimensional_retorno.tex` y `c52_01_02_independencia_prospectiva.tex`. Para aligerar sólo esta prueba, a=α_HMT, p=π_HMT, h=H₅. Son salidas del mismo estado, con su orden interno, y no parámetros convencionales introducidos. El retorno regional aporta

\[
 D_A=\exp(-100pa/9),\qquad
 \mathscr C_p=169a^6+\frac{D_Aa^7}{1-D_Aa},
 \quad \eta_{\rm ret}=h-\frac{90}{p}\mathscr C_p.
\]

En la rama canónica sin reducción por 360,

\[
 A=1000a,\qquad C^*=2(\eta_{\rm ret}+a),\qquad
 \eta_{\rm ret}=500a\sigma-a.
\]

Se define únicamente como abreviatura algebraica

\[
 B_\sigma=\frac p{90}(h+a-500a\sigma)-169a^6.
\]

Sustituir el retorno da Bσ=D_A a⁷/(1−D_A a). Por multiplicación y despeje,

\[
 \boxed{\exp(-100pa/9)
 =\frac{B_\sigma}{a^7+aB_\sigma},\qquad
 \sigma=\frac{1-R_0^4}{1+R_0^4}.}
 \tag{42}
\]

El dominio mantiene a>0 y 1−D_A a>0. En él Bσ>0 y a⁷+aBσ>0, por lo que el despeje no introduce raíces ni divide por cero. En otras cartas angulares deben retenerse los enteros del levantamiento por 360 antes de utilizar esta fórmula; no se extiende silenciosamente la rama canónica.

Ahora entra la pregunta de Rubén. La identidad ya recogida de los dos lectores es

\[
 S=e+\pi=4+\kappa+\varphi+a.
\]

Con κ racional en el registro declarado, la hipótesis S∈Q impone a=q−φ, q=S−4−κ∈Q. El lector de acción obliga a

\[
 h=f(a)+\sqrt{250a/\varphi},\qquad
 f(a)=-a+\frac9{16}a^2-\frac59a^3+\frac7{48}a^4-\frac1{54}a^5.
\]

Por la prueba coordinada de Overleaf §27, este h tiene grado exactamente cuatro sobre Q, con dos conjugados reales y dos no reales. Sustituyéndolo en (42) se obtiene una restricción explícita sobre el radio y la estructura compleja de (38)–(41). Así se ha compuesto, sin saltar desde una coincidencia numérica,

\[
 \text{estado APP–TRIT–TPK}\longrightarrow(S,a,h,D_A)
 \longrightarrow(A,C^*)\longrightarrow(R_0,\tau_\eta)
 \longrightarrow\text{transporte T y pantalla M}.
\]

**Lo que demuestra esta composición.** La clasificación de S condiciona efectivamente otras lecturas del mismo estado. En particular, la hipótesis racional impone simultáneamente el coborde (28), su transporte de frontera y marco (32)–(37), la consecuencia cuártica de h y la ecuación angular (42). No se ha encontrado en las identidades compuestas una contradicción que las descarte conjuntamente. Tampoco se ha demostrado que puedan realizarse conjuntamente en la sección forward: cumplir condiciones necesarias por separado no construye esa sección. No se declara clasificado S ni se reduce el alcance de los teoremas de generación ya publicados.

**Procedencia y comprobación.** Las operaciones de cilindros, el transporte de forma, el retorno, la dualidad T y el mapa de pantalla son `RESULTADO_RECUPERADO`. Los despejes (33), el encadenamiento (35)–(36), el conmutador (39) y la composición (42) son formalización focal sobre arquitectura autoral preexistente, con prioridad global pendiente de auditoría. Sus pruebas están aquí. El archivo `verificar_filtros_y_modulo_e_mas_pi_20260908.py` comprueba implementación y casos racionales exactos de esas identidades; no calcula cifras de constantes, no prueba una cuantificación infinita y no certifica la racionalidad ni la irracionalidad de S. Ningún PDF o fuente rectora ha sido modificado.

Fuentes de §§16–18: F/manuscrito/sections/hmt/20_arquitectura_operatoria_tpk_actualizada.tex:645; F/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex:300; F/colaboracion/partes_i_ii/source/base_residencias/base_c17_sin_encabezado.tex:549; F/manuscrito/sucesor_102/radion_52/snippets/c52_04_01_ley_areal.tex; F/manuscrito/sucesor_102/radion_52/snippets/c52_10_01_modularidad.tex; F/colaboracion/partes_i_ii/source/public/residencias/capitulo_24_dualidad_t.tex; F/colaboracion/partes_i_ii/source/public/residencias/capitulo_25_pantallas_teoria_m.tex; F/manuscrito/sucesor_102/residencias/capitulo_14_apertura_causal_accion_parangular.tex; F/manuscrito/sucesor_102/deltas_ley9/c35_componente_adimensional_retorno.tex; F/manuscrito/sucesor_102/radion_52/snippets/c52_01_02_independencia_prospectiva.tex. Las unidades correspondientes fueron leídas completas; el análisis aquí es focal y no se presenta como nueva auditoría integral.

## 19. Memoria entera de una ventana y conservación de sus solapamientos

Se incorpora la composición de `../OVERLEAF/E_MAS_PI_ALPHA_Y_ACARREO.md:2683`, §38, leída y contrastada con la carta del propietario `14_numero_heisenberg_y_d108.tex:552–609`. Su dominio es una ventana donde se cumple efectivamente x_jA_H=u_j+3x_(j+1). No se itera esa igualdad en lugar de actualizaciones que tengan correcciones adicionales.

Como A=A_H es unimodular, para residuos canónicos u_j∈{0,1,2}⁶ se define un entero por coordenada

\[
 E_m(u)=\sum_{j=0}^{m-1}3^ju_jA^{-(j+1)}.
\]

Sustituir sucesivamente x_j=(u_j+3x_(j+1))A⁻¹ da

\[
 x_0=E_m(u)+3^m x_mA^{-m}.
\]

En consecuencia, con x₀ fijado, los residuos son los de esa ventana si y sólo si

\[
 \boxed{x_0\equiv E_m(u)\pmod{3^m\mathbb Z^6},\qquad
 x_m=3^{-m}(x_0-E_m(u))A^m.}
 \tag{43}
\]

La suficiencia se prueba reconstruyendo hacia atrás los estados enteros desde el x_m de (43). La condición de que cada u_j sea el representante canónico garantiza entonces las divisiones euclídeas prescritas. Al comparar dos posiciones separadas por p, se conserva una ventana de longitud p+m por canal: el estado de la segunda posición lo transportan los p pasos iniciales. Los símbolos solapados no se eligen otra vez. Deben cumplirse las dos congruencias individuales de π y e; su suma sola puede ocultar dos residuos incompatibles.

La corrección del marco también permanece en la congruencia. Si v_j=[u_jF_j]₃ y H_j representa la inversa residual de F_j,

\[
 u_j=v_jH_j-3q_{H_j}(v_j),\qquad
 q_H(v)=(vH-[vH]_3)/3.
\]

Al sustituir en E_m, el término de corrección de la posición j pesa 3^(j+1)A^−(j+1). Sólo el último desaparece automáticamente módulo 3^m. Omitir los anteriores altera la memoria inicial que se pretende conservar.

Finalmente, para Z_j=x_j^π+x_j^e y ΔZ_j=Z_(p+j)−Z_j de esa misma ventana, el criterio posicional es

\[
 \boxed{(\Delta Z_jA-3\Delta Z_{j+1})\lambda
 =729\delta_j-\delta_{j+1},\qquad
 \delta_0,\ldots,\delta_m\in\{-1,0,1\}.}
 \tag{44}
\]

Se obtiene sumando las identidades de ambos canales, restando las posiciones comparadas y aplicando λ. Así se reúnen la memoria individual (43), el acarreo posicional (44), los intervalos (32) y el marco (37) sobre una sola ventana. Esto fortalece el test finito; no demuestra su incompatibilidad para todos los N,p de la sección global. La separación residuo–cociente es `RESULTADO_RECUPERADO`; la composición focal por ventanas conserva la procedencia coordinada de §38, sin atribuir novedad a la arquitectura HMT.

## 20. Continuación del 9 de septiembre: holonomía de acción y degeneración del espectro dual

Se continúa desde §§17–19, sin recalcular expansiones ni modificar los PDF. El objeto de partida sigue siendo el estado conjunto APP–TRIT–TPK y sus publicaciones generadas. La pregunta es qué restricciones de las realizaciones posteriores actúan realmente sobre la forma angular que aparece en (42). No se introduce un radio desde fuera ni se supone un autovalor para obtener la respuesta.

### 20.1. La condición orbital conserva hoja y acción; su forma escrita no selecciona la excentricidad

Los propietarios c52_10_02_orbitas_caminos.tex:43–53 y 06_03c_elipse_accion_holonomia_rev8.tex:25–64 conservan

\[
 \varepsilon_\gamma\exp(iJ_\gamma/\hbar_{\rm ret})=1,\qquad
 a_Sb_S=2\hbar_{\rm ret}.
\]

La sustitución de la ley areal da, en el ciclo cilíndrico,
\(J_\gamma/\hbar_{\rm ret}=2\pi\), \(\varepsilon_\gamma=1\); y en la vuelta visible de Möbius, \(J_\gamma/\hbar_{\rm ret}=\pi\), \(\varepsilon_\gamma=-1\). Ambos productos valen uno. La razón de semiejes no interviene en ese producto: \(a_S=\sqrt{2\hbar_{\rm ret}e^\eta}\) y \(b_S=\sqrt{2\hbar_{\rm ret}e^{-\eta}}\) la cancelan.

Esto comprueba el efecto de **esta condición concreta**. No afirma que todas las holonomías del TPK pierdan la forma, ni que el módulo generado sea un parámetro libre. El módulo ya está fijado por \(A,C^*\); el cierre orbital examinado no proporciona una segunda ecuación que lo seleccione.

Análogamente, el propietario completo capitulo_24_dualidad_t.tex:168–235 conserva la condición
\[
 N_L-N_R=a_L-a_R-mw.
\]
El radio no aparece en ella. La igualdad T-dual de energías compara radios recíprocos; no exige que la salida angular esté en el radio autodual.

### 20.2. Un criterio aritmético exacto sobre el espectro que sí distingue la forma

En el dominio estable que construye el capítulo 24,
\[
 E_{R_0}(m,w)=m^2/R_0^2+w^2R_0^2,\qquad (m,w)\in\mathbb Z^2,
\]
llamaremos degeneración distinta del cambio de signos a una igualdad de energías entre dos pares para los que \((m^2,w^2)\ne(m'^2,w'^2)\).

**Proposición.** En ese dominio completo,
\[
 \boxed{\exists\ \text{degeneración distinta del cambio de signos}
 \quad\Longleftrightarrow\quad R_0^4\in\mathbb Q_{>0}.}
 \tag{45}
\]

**Prueba.** Multiplicar una igualdad de energías por \(R_0^2\) da
\[
 m^2-m'^2+(w^2-w'^2)R_0^4=0.
\]
Si \(w^2=w'^2\), también \(m^2=m'^2\), caso excluido. Por tanto,
\[
 R_0^4=\frac{m'^2-m^2}{w^2-w'^2}\in\mathbb Q_{>0}.
\]
Recíprocamente, si \(R_0^4=a/b\), con enteros positivos \(a,b\), los pares
\[
 (m,w)=(a+1,b-1),\qquad (m',w')=(a-1,b+1)
\]
tienen diferencias de cuadrados \(4a\) y \(-4b\). Su diferencia energética multiplicada por \(R_0^2\) es \(4a-4bR_0^4=0\). Son pares distintos incluso cuando \(a=1\) o \(b=1\). Esto prueba ambas direcciones sin un barrido numérico.

Componiendo **la carta concreta de (40)–(41)**, se obtiene
\[
 \boxed{
 \text{degeneración de (45)}
 \Longleftrightarrow \sigma=C^*/A\in\mathbb Q
 \Longleftrightarrow \tau_\eta\text{ es cuadrático sobre }\mathbb Q.}
 \tag{46}
\]
La proposición se refiere al dominio \(\mathbb Z^2\) entero del núcleo dual. Si una realización física ulterior restringe los modos, su dirección suficiente requiere verificar que los dos pares construidos pertenecen a ese sector; no se omite esa pertenencia.

### 20.3. Enlace preciso con la investigación sobre la suma

(45) no atribuye al corpus una degeneración que aún no se haya localizado. Distingue una condición espectral a **radio fijo** de la igualdad
\[
 E_{R_0}(m,w)=E_{R_0^{-1}}(w,m),
\]
que compara dos cartas y vale para todo radio. Tampoco identifica racionalidad de \(\sigma\) con racionalidad de \(S=e+\pi\): entre ambas permanece la composición efectiva (42), con \(\alpha=q-\varphi\) bajo la hipótesis racional de \(S\).

Las fuentes examinadas proporcionan el núcleo dual, el transporte del módulo y los cierres orbitales. En esos cuerpos no se ha localizado una condición de degeneración de tipo (45) exigida sobre el módulo angular generado, ni una contradicción universal de (42) para todo \(q\in\mathbb Q\) admisible. El examen es focal, no una nueva auditoría del corpus entero. Esta comprobación no clasifica todavía \(S\) ni modifica los teoremas de generación usados como antecedentes.

**Procedencia.** Holonomía, área, forma angular y núcleo dual: RESULTADO_RECUPERADO. El criterio espectral (45)–(46) y su colocación en esta cadena constituyen formalización focal, sin reivindicación de novedad histórica. La prueba es el despeje y la construcción entera expuestos, no un certificado de cifras ni una instrucción de skill.

**Fuentes leídas en sus cuerpos completos para esta continuación:** F/manuscrito/sucesor_102/radion_52/snippets/c52_10_02_orbitas_caminos.tex; F/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/06_03c_elipse_accion_holonomia_rev8.tex; F/colaboracion/partes_i_ii/source/public/residencias/capitulo_24_dualidad_t.tex. Se conservan los anclajes del módulo y del par angular citados en §§17–18.

## 21. Continuación del 10 de septiembre: sello prolongado y restricción exacta sobre la suma

Se conserva íntegro el desarrollo precedente. Esta sección explicita la semántica de frontera utilizada en §§17–20 y no sustituye ninguna demostración de los PDF. El objeto sigue siendo la misma sección generada por APP–TRIT–TPK: no se introducen valores convencionales ni se permite variar libremente sus coordenadas.

El propietario `F/colaboracion/partes_i_ii/source/base_residencias/base_c10_sin_encabezado.tex:1006–1047` y el segundo propietario `F/colaboracion/parte_iii/source/public_final/alpha/08a_alpha_dos_vias_t1_rev8_body.tex:168–183` fijan explícitamente

\[
 B=1000,\qquad K_j^{\rm per}=K_{1+((j-1)\bmod12)}.
\]

Si \(M_K=\sum_{j=1}^{12}K_jB^{12-j}\), la valoración de la prolongación es

\[
 \kappa_{\rm per}=\sum_{j\ge1}K_j^{\rm per}B^{-j}
 =\frac{M_K}{B^{12}-1}\in\mathbb Q.
 \tag{47}
\]

No se reemplaza por la valoración de una ventana, \(\kappa_{36}=M_K/B^{12}\). Para \(N=12m\), la valoración truncada es \(\kappa_N=\kappa_{\rm per}(1-B^{-N})\). La periodicidad pertenece al sello leído, no a los canales completos ni a la memoria del estado enriquecido.

La recurrencia de la vía A da, antes de tomar ningún límite,

\[
 P_j+E_j-\Phi_j-K_j^{\rm per}-A_j=Bc_j-c_{j+1}.
\]

Multiplicar por \(B^{-j}\) y sumar de 1 a \(N\) conserva exactamente la frontera:

\[
 p_N+e_N-f_N-\kappa_N-a_N=c_1-B^{-N}c_{N+1},
 \tag{48}
\]

donde las letras minúsculas denotan las valoraciones de los respectivos prefijos fraccionarios. Los propietarios fijan \(c_1=0\) y los acarreos en \(\{-2,-1,0,1,2\}\). En consecuencia, el último término tiende a cero con cota \(2B^{-N}\). Las secciones estabilizadas publican \(\pi-3,e-2,\varphi-1,\alpha_A\), respectivamente, y resulta

\[
 \boxed{S:=e+\pi=4+\varphi+\kappa_{\rm per}+\alpha_A.}
 \tag{49}
\]

Así, sobre esta sección concreta,

\[
 \boxed{S\in\mathbb Q
 \quad\Longleftrightarrow\quad
 \alpha_A=q-\varphi\text{ para algún }q\in\mathbb Q.}
 \tag{50}
\]

La equivalencia es una consecuencia exacta de la recurrencia, no una comparación decimal. Utilizar el nombre \(\alpha_A\) identifica el lector efectivamente sumado; esta prueba no necesita resolver otra vez la identificación de sus dos vías. Bajo (50), \(\alpha_A\) es cuadrática e irracional y satisface

\[
 \alpha_A^2+(1-2q)\alpha_A+q^2-q-1=0,
 \tag{51}
\]

obtenida sustituyendo \(\varphi=q-\alpha_A\) en \(\varphi^2-\varphi-1=0\). El discriminante vale 5. Ésta es una restricción aritmética precisa que la hipótesis racional impone a la salida dodecafásica; no una afirmación de que esa hipótesis se realice. La hipótesis irracional excluye exactamente la pertenencia \(\alpha_A\in\mathbb Q-\varphi\), sin decidir por sí sola si \(\alpha_A\) tiene otro grado algebraico o es trascendente.

**Procedencia:** sello y recurrencia, RESULTADO_RECUPERADO; telescopaje y composición (49)–(51), FORMALIZACION_REUNIDA de las relaciones previas. No se reivindica novedad histórica.

## 22. Restricción conjunta de complejidad en los canales nativos

Volvemos a la base nativa \(a=729\), sin mezclar los índices de sextetos con los de tríadas decimales. Sean

\[
 P_i=\nu(w_i^\pi),\quad E_i=\nu(w_i^e),\qquad
 0\le P_i,E_i<a.
\]

Sean \(D_i\) los dígitos normalizados de la suma de sus partes fraccionarias, con representación que no termina en una cola constante \(a-1\). El lector aditivo con su memoria de acarreo cumple

\[
 D_i=P_i+E_i+H_i-aH_{i-1},\qquad H_i\in\{0,1\}.
 \tag{52}
\]

El acarreo entero inicial se conserva por separado. Esta normalización es posterior a los dos canales generados; no modifica su dinámica ni el marco incidencial que los decodifica en §2.

**Proposición.** Supóngase \(S\in\mathbb Q\), y elíjase \(N\) después del preperíodo de \(D\), con período \(p\ge1\). Denotemos por \(p_P^{(N)}(n)\) y \(p_E^{(N)}(n)\) el número de bloques distintos de longitud \(n\) que aparecen en cada canal en posiciones iniciales mayores o iguales a \(N\). Entonces, para todo \(n\ge1\),

\[
 \boxed{
 p_E^{(N)}(n)\le2p\,p_P^{(N)}(n),\qquad
 p_P^{(N)}(n)\le2p\,p_E^{(N)}(n).}
 \tag{53}
\]

**Prueba.** Fijemos un bloque de \(P\), su posición módulo \(p\) dentro de \(D\), y el acarreo en su extremo derecho. Hay a lo sumo \(p\) posiciones y dos acarreos. Recorriendo el bloque de derecha a izquierda, la división euclídea obliga a

\[
 \begin{aligned}
 E_i&=\operatorname{rem}_a(D_i-P_i-H_i),\\
 H_{i-1}&=(E_i-D_i+P_i+H_i)/a.
 \end{aligned}
 \tag{54}
\]

Cada combinación produce como máximo un bloque de \(E\). La cota \(0\le D_i,P_i<a\) y \(H_i\in\{0,1\}\) asegura que el cociente reconstruido pertenece a \(\{0,1\}\). No es preciso afirmar que cada combinación ocurra en la trayectoria HMT: basta contar las que efectivamente ocurren. Se obtiene la primera desigualdad; intercambiar \(P,E\) da la segunda. Una suma con expansión terminante se trata con la cola de ceros, de período uno; la representación alternativa no produce una excepción al argumento.

En particular,

\[
 \left|\log p_P^{(N)}(n)-\log p_E^{(N)}(n)\right|
 \le\log(2p).
 \tag{55}
\]

Por tanto, la diferencia de sus tasas logarítmicas divididas por \(n\) tiende a cero. Esto se refiere al crecimiento del lenguaje de bloques de las dos trayectorias, no a la entropía termodinámica, al principio de Landauer ni a una pérdida de la memoria HMT.

La aplicación matemática es concreta: si las relaciones genealógicas obligasen a que el cociente entre esas complejidades fuera no acotado, la hipótesis racional quedaría contradicha. Esta sección prueba (53), pero no ha establecido esa separación para las dos trayectorias efectivas. No convierte una condición necesaria en una clasificación ya concluida.

**Comprobación complementaria ya ejecutada:** la identidad local (54), el rango del acarreo y la inversión de los canales se verificaron para las bases 2, 3, 9 y 729, en 1.063.070 combinaciones de \((P_i,D_i,H_i)\), además de la composición de dos tramos en base 3. No se calcularon cifras de ninguna constante. La prueba para todos los índices es la división euclídea anterior; el barrido finito sólo contrasta la implementación de esa identidad local.

**Procedencia:** FORMALIZACION_REUNIDA a partir del lector de §14 y de los canales previamente generados; no se atribuye novedad al generador ni prioridad histórica a la cota.

## 23. Composición con la forma angular y alcance de las realizaciones posteriores

En esta sección, \(\rho=\pi/e\) significa el cociente de valores publicados, no el nombre del reparto especular de canales residuales. Sobre el mismo estado,

\[
 \pi=\frac{S\rho}{1+\rho},\qquad e=\frac{S}{1+\rho}.
 \tag{56}
\]

No se ha introducido una familia nueva de estados ni una libertad para escoger \(S,\rho\). Son identidades entre salidas ya determinadas. Si \(S\) fuera racional y no nulo, \(\rho\) tendría que ser trascendente: si fuese algebraico, la segunda igualdad haría algebraico a \(e\). Asimismo, \(\pi e\) tendría que ser trascendente, pues de ser algebraico la ecuación \(e^2-Se+\pi e=0\) haría algebraico a \(e\). Se utiliza aquí el reconocimiento posterior de la coordenada \(e\); estas deducciones no seleccionan el generador. Ninguna de las dos necesidades produce una contradicción por sí misma.

El propietario del par angular compone, sobre la carta declarada,

\[
 \begin{aligned}
 \eta_{\rm ret}
 &=H_5(\alpha,\varphi)-\frac{90}{\pi}
   \left(169\alpha^6+\frac{D(\alpha)\alpha^7}{1-D(\alpha)\alpha}\right),\\
 D(\alpha)&=\exp(-100\pi\alpha/9),\\
 A&=1000\alpha,\qquad C^*=2(\eta_{\rm ret}+\alpha),\\
 \sigma&=C^*/A,\qquad R_0^4=(1-\sigma)/(1+\sigma).
 \end{aligned}
 \tag{57}
\]

Al usar la identificación de la vía A con la coordenada \(\alpha\) declarada por el corpus, (50) entra efectivamente en (57). El radio conserva también la dependencia de \(\pi\) separadamente; no es una función de \(S\) sola. Esto exhibe el vínculo solicitado con el desarrollo ulterior, sin borrar las coordenadas que ese desarrollo utiliza.

El capítulo 25 transporta \(d=(m,w,R_0)\) por identidad en el morfismo de pantallas, mientras que sus proyectores dependen del vector completo \(K\). La igualdad T-dual del capítulo 24 vale para radios recíprocos; no impone que \(R_0=R_0^{-1}\). Así, estas dos flechas conservan relaciones determinadas por la salida HMT, pero no agregan por sí mismas una segunda ecuación aritmética para \(S\). El examen no demuestra la existencia de un estado HMT alternativo con suma racional.

**Estado de esta continuación:** (49)–(55) son consecuencias demostradas de los lectores y de las fronteras indicados; (56)–(57) localizan cómo la hipótesis se transmite a otras salidas. No se ha obtenido todavía una contradicción de \(S\in\mathbb Q\) ni una prueba de \(S\in\mathbb Q\). La investigación no queda certificada como resuelta por cerrar esta nota. No se modifica ningún PDF, TeX, índice sellado ni prueba anterior.

Fuentes adicionales de §§21–23:

- F/colaboracion/partes_i_ii/source/base_residencias/base_c10_sin_encabezado.tex:1006–1161: periodicidad del sello, recurrencia y frontera remota.
- F/colaboracion/parte_iii/source/public_final/alpha/08a_alpha_dos_vias_t1_rev8_body.tex:168–183: repetición explícita del sello en la prolongación; :145–157: identificación de las secciones límite declarada por el propietario.
- F/manuscrito/sucesor_102/residencias/capitulo_14_apertura_causal_accion_parangular.tex:14–106: H5, retorno y cartas angulares.
- F/manuscrito/sucesor_102/radion_52/snippets/c52_10_01_modularidad.tex:70: cadena del carácter de forma.
- F/colaboracion/partes_i_ii/source/public/residencias/capitulo_25_pantallas_teoria_m.tex:33–146: dependencia de K y transporte de d por identidad.

## Fuentes exactas

Raíz integral F: `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente`.

- F/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:8–163: dinámica conjunta, caracteres, división interna y secciones forward; :218–310: valoración de sextetos y doble proyección.
- F/colaboracion/partes_i_ii/source/public/residencias/capitulo_17_doble_proyeccion_natural.tex:65–110: decodificación de la incidencia calibrada.
- F/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex:14–159: calendario finito; :193–254: inversión, carácter circular, propagación y autoescala.
- F/manuscrito/sections/hmt/14_numero_heisenberg_y_d108.tex:552–609: matriz A, división por tres y memoria Bockstein–Hensel.
- `/Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/E_MAS_PI_ALPHA_Y_ACARREO.md`, §§15–26, en particular §§19 y 22: criterios anteriores de retorno y norma cuadrática.
- F/manuscrito/sucesor_102/deltas_ley9/c35_componente_adimensional_retorno.tex:5–20: B_c, sus autovalores y el carácter H5; no se identifica éste con un autovalor de B_c.
- Adamczewski y Bugeaud, *On the complexity of algebraic numbers I. Expansions in integer bases*, Annals of Mathematics 165 (2007), teorema 1, p. 549: https://annals.math.princeton.edu/wp-content/uploads/annals-v165-n2-p04.pdf. Fuente primaria consultada directamente para (13) y §7.

Control realizado: multiplicación entera de Aλ y (A−2187I)λ, y censo de las 37 aristas. No se recalcularon expansiones de constantes. Las pruebas son las identidades y la norma expuestas; ningún recibo causal las sustituye.

Fuentes de §§9–11, leídas en sus unidades completas por la investigación coordinada:

- M = `/Users/ruben/Documents/New project/output/DOBLE_PROYECCION_HOLOGRAFICA_CRISTAL_TEMPORAL_APERIODICO_MONOGRAFIA_AUTOSUFICIENTE/manuscrito`.
- M/generated/cristal_relojes_sincronizacion.tex:1–137: capacidad, vacancias y dos tiempos; :608–613: invariancia de S bajo reparto especular; :1602–1670: ventanas; :1910–2050: extractor y coeficientes de P9. El capítulo completo tiene 2362 líneas.
- M/generated/algebra_holonomica.tex:791–899: observables de fase, avance de memoria y distinción entre representación simbólica y realización física del cristal temporal. Se leyó el cuerpo completo.
- M/generated/semillas_proyeccion_constantes.tex:2439–2452: coordenadas del producto fibrado de lectores de alfa.
- F/manuscrito/integracion_83/masas_p0/corpus/source/demostraciones_primarias/06_03c_elipse_accion_holonomia_rev8.tex:1–73: elipse de acción y cierre cilíndrico/Möbius.
- F/manuscrito/integracion_83/masas_p0/tex/fragmentos/73_rev2_electron_lectores_torres_publicacion.tex:582–615: reloj de ruta, devanado y lectura de energía.
- F/manuscrito/integracion_83/parte_iv/body/B002_ch48_electron_primera_realizacion_5326d609ca60_06k_electron_two_way_rev11.tex:1: igualdad componente a componente K_D=K_Ω=(80,54,6), anterior a la evaluación de κ_e.
