# Compresión nonádica, espejo espectral y reconstrucción de K

Nota interna de investigación. Consulta de propietarios existentes; ningún artículo anterior ha sido editado. La fuente numérica primaria sigue siendo APP–TRIT–TPK. Los operadores de esta nota actúan sobre publicaciones ya construidas del mismo estado enriquecido. No se utilizan alturas de ceros, valores metrológicos ni una geometría objetivo para seleccionar K.

## Fuentes y localizadores

Raíz VIII:
`/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/08_PRIMOS_Y_ZETA_ES/documentacion_original/payload/spanish_source`

Raíz X:
`/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/source`

- VIII, `sections/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.tex:347–461`: representación de la forma de Weil positiva, traslaciones, generador autoadjunto, representación espectral y Cayley canónico.
- VIII, `sections/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.tex:465–610`: árbol de historias, pesos, cociclo de memoria, refinamiento isométrico, retorno nonádico, calendario y compresión.
- VIII, `ampliacion/transporte_y_momentos.tex:55–101`: compresión para C acotado y balance con defecto de costura.
- VIII, `ampliacion/transporte_y_momentos.tex:105–176`: registro de pérdidas, memoria bilateral, balance de la forma aritmética y círculo comprimido.
- VIII, `ampliacion/transporte_y_momentos.tex:425–497`: Cayley auxiliar sobre pruebas exponenciales y conservación conjunta de gamma, primo y polar.
- VIII, `antecedentes/integral/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex:203–242`: transformación de Möbius y espejo recíproco.
- X, `nuclear/01.tex:34–94`: masa de cilindros, pullback isométrico y unital, esperanza condicional.
- X, `nuclear/02.tex:39–153`: compresión, balance de observables, telescopía, sector fijo y cambio unitario de carta.
- X, `nuclear/02.tex:172–204`: realización excepcional de orden tres sin vectores fijos; factor cuadrático 19/27, con dominio propio.
- X, `nuclear/11.tex:7–177`: lectores S³/S⁴, dos memorias, inversa exacta, núcleo y estabilidad.
- X, `nuclear/11.tex:188–225`: registros numéricos de memoria, reconstrucción del K publicado.
- X, `nuclear/11.tex:234–307`: composición efectiva memoria→u_K→P_10(K).
- X, `sections/01_hilbert_nonadico.tex:222–279`: conservación de unidad y traza normalizada al mantener toda la fibra; reducción de traza por nueve al seleccionar una esquina.
- X, `nuclear/12.tex:529–577`: realización simpléctica/gaussiana, covarianza W=(8I+HHᵀ)/9 y sus valores simplécticos; objeto distinto de una compresión euclídea unitaria.

## 1. El espejo r→1/r y el operador C tienen tipos diferentes

**Resultado recuperado.** La carta espectral es τ(z)=(z−1)/z, z≠0. Para el espejo z♯=1−conj(z), y restringiendo a z∉{0,1} cuando ambas expresiones se escriben en la carta finita,

τ(z♯)=1/conj(τ(z)).

Si τ(z)=r exp(iθ), r>0, el espejo conserva θ y transforma r en 1/r. Para z=σ+it,

r²=((σ−1)²+t²)/(σ²+t²),

de donde r=1 equivale a σ=1/2. El conjunto fijo del espejo es la circunferencia unidad. Esta identidad algebraica determina una equivalencia entre cartas; por sí sola no selecciona las posiciones de los ceros. La conjugación z→conj(z) es otra involución: sobre la recta crítica cambia t por −t e invierte la orientación angular. No se la identifica con el espejo anterior.

El C de VIII, sección espectral, es

C=(H+iI/2)(H−iI/2)^{-1}: H_W→H_W,

donde H es el generador autoadjunto de las traslaciones en la realización hilbertiana de la forma de Weil. Por cálculo funcional, C es unitario y su multiplicador en la coordenada espectral γ es (γ+i/2)/(γ−i/2). Su construcción en ese propietario aparece después del antecedente de positividad global que permite el cociente hilbertiano. No es una involución ni una permutación finita ni un operador de orden tres por esa definición.

El artículo VIII conserva además una realización auxiliar anterior a ese cociente. Para a>b>1/2, sea E_b el espacio de funciones suaves cuyas derivadas decrecen al menos como exp(−b|x|). Entonces

C_a f(x)=f(x)−2a∫₀∞exp(−at)f(x+t)dt,
C_a^{-1}f(x)=f(x)−2a∫₀∞exp(−at)f(x−t)dt.

Su multiplicador Fourier es c_a(ξ)=(ξ−ia)/(ξ+ia). Es unitario en L² y conserva E_b. La forma aritmética completa satisface W(C_a f,C_a g)=W(f,g), incluyendo los términos polares cruzados. El propietario distingue expresamente esta conservación de una forma hermítica de una prueba de su signo. La elección a>1/2 protege la convergencia término a término de los lectores polares; no reemplaza silenciosamente al Cayley canónico a=1/2.

La memoria entera tiene, a su vez, C=S sobre ℓ²(Z), Se_n=e_{n+1}, unitario de orden infinito. En X, sobre R¹², aparecen C=S³ y C=S⁴, con (Sx)_i=x_{i+1}; sus órdenes son cuatro y tres respectivamente. El operador excepcional g_c de X actúa en otra realización y cumple g_c³=I y ker(I−g_c)=0. Compartir la forma de compresión no identifica estos operadores.

La diferencia de sectores fijos tiene un efecto numérico preciso: para S⁴, P_fix=(I+S⁴+S⁸)/3 tiene rango cuatro y T₄*T₄=P_fix+(19/27)(I−P_fix). Para g_c, el proyector fijo es cero y el factor 19/27 actúa en todo su dominio. El orden tres, sin el dato de los vectores fijos, no autoriza el segundo resultado.

## 2. Conservación de compresión, complemento y memoria

**Resultado recuperado.** Para C acotado en H, sobre H⁹ se definen

S_C(v₀,…,v₈)=(Cv₈,v₀,…,v₇),  Jv=(v,…,v)/3,
T=J* S_C J=(8I+C)/9,
η=(I−JJ*)S_CJ.

La fórmula explícita es ηv=(8(C−I)v,−(C−I)v,…,−(C−I)v)/27. Por expansión,

η*η=(8/81)(I−C)*(I−C),
I−T*T=η*η+(I−C*C)/9.

Si C es unitario, T*T+η*η=I. Para todo observable acotado autoadjunto A que satisface C*AC=A, la misma expansión da

A=T*AT+(8/81)(I−C)*A(I−C).

La compresión N veces conserva el balance de todos los productos cruzados:

A=T*ᴺATᴺ+Σ_{j=0}^{N−1} T*ʲη*(I₉⊗A)ηTʲ.

El transporte completo cumple S_C⁹=I₉⊗C, mientras Tᴺ describe compresiones sucesivas con almacenamiento de sus complementos. Son operaciones distintas. Para C unitario, Tᴺ tiende fuertemente a P_fix, proyector sobre ker(I−C), y el límite mantiene dicho sector fijo. La memoria bilateral tiene P_fix=0; un ciclo finito conserva su dirección uniforme. La extinción fuerte no impone una contracción uniforme: en la realización bilateral puede ocurrir ||Tᴺ||=1 para todo N.

**Corolario algebraico reunido para este desarrollo.** Con D=√8(I−C)/9, el par (T,D) es una isometría H→H⊕H. Sobre operadores de clase traza X,

Q_C(X)=TXT*+DXD*=(8X+CXC*)/9.

Para C unitario, esta aplicación conserva la traza y la unidad; su completa positividad sigue de la expresión con dos operadores. La fórmula conserva las coherencias internas de X en ambos términos. No se identifica esta reducción de registro con un Hamiltoniano físico ni con la forma de Weil. La búsqueda focal en nuclear/10–12 y en las fuentes X por Kraus/unital/canal no localizó esta identidad escrita en esta forma; la consecuencia algebraica procede del balance recuperado.

El otro dueño de unidad y traza es la prolongación de álgebras a→a⊗I₉: conserva la traza normalizada. La esquina a→a⊗p_j la divide por nueve. En el árbol completo, μ(hε)=μ(h)/d(h) conserva Σ_hijos μ=μ(h); el pullback Rf(hε)=f(h) satisface R*R=I y R1=1. Estos balances tienen dominios distintos y son compatibles al conservar explícitamente sus mapas.

## 3. Dos memorias reconstruyen K y su dirección geométrica

**Resultado recuperado, no analogía.** En V=R¹², sean S el desplazamiento cíclico anterior,

T_j=(8I+S^j)/9,  D_j=√8(S^j−I)/9,  j=3,4,
m₀=D₃K,  m₁=D₄T₃K,  q=Σ_i K_i.

La memoria m₁ lee el resultado de la primera compresión. La inversa exacta es

T₃^{-1}=(512I−64S³+8S⁶−S⁹)/455.

Por tanto b=−9m₀/√8=(I−S³)K y c=−9T₃^{-1}m₁/√8=(I−S⁴)K. Definiendo w_i=c_i−b_{i+1} y B_i=Σ_{j<i}w_j, se tiene

w_i=K_i−K_{i+1},  B_i=K₀−K_i,
K_i=(q+Σ_jB_j)/12−B_i.

Anular ambas memorias equivale a S³K=K y S⁴K=K, luego SK=S⁴(S³)^{-1}K=K. Su núcleo común es exactamente la recta uniforme. La aplicación M:K→(m₀,m₁) tiene rango once y

M*M=I−(T₄T₃)*(T₄T₃).

El propietario obtiene la inversa centrada L con LM=P₁₁ y norma 9/4. De ahí la composición ya escrita en X:

u_K=P₃L(m₀,m₁),
P₁₀(K)=P₁₁−P₃L(m)[P₃L(m)]*/||P₃L(m)||².

El flujo geométrico dirigido por u_K recibe así una dirección recuperable de memorias efectivas, no un coeficiente añadido por coincidencia formal. La carga q hace recuperable también el registro completo y sus pesos positivos d_i=K_i/q. No se afirma por ello que cada vector del espacio ambiente V sea una historia TPK admisible.

Testigo exacto reproducido por `verify_nonadic_k.py`, usando como entrada las memorias publicadas z_i=m_i/√8:

9z₀=(495,116,684,−108,−601,90,173,88,−313,−560,397,−461),
81z₁=(2729,2503,3818,−5843,2583,−920,−4051,4338,−5312,−1583,233,1505),
q=6263.

Su inversa produce K=(234,543,140,729,659,824,621,58,914,794,146,601), exactamente. El script verifica además rango once, norma por suma de Grams, inversa T₃ y reconstrucción con q=0 del centrado.

## 4. Composición con el flujo geométrico: igualdad efectiva y frontera de tipo

La dirección u_K define, después de su construcción, un flujo diagonal g(s)=exp(sA_K) en V, con A_K diagonal proporcional a u_K. Como Σ_i(u_K)_i=0, det g(s)=1. Sus componentes positivas permiten actuar sobre coordenadas positivas, pero g(s) no es en general unitario euclídeo. Sustituir C por g(s) en el balance general produce

T*T+D*D=(8I+g(s)*g(s))/9,

que no es I en general. El testigo racional g=diag(2,1/2) tiene determinante uno pero T=diag(10/9,17/18), de modo que una coordenada se expande. La propiedad simpléctica de un levantamiento cotangente tampoco implica unitariedad euclídea.

**Formalización nueva acotada: covariancia con métrica transportada.** Sobre el mismo V, partiendo de uno de los lectores unitarios C₀=S³ o S⁴, se define

C_s=g(s)C₀g(s)^{-1},  G_s=g(s)^{-*}g(s)^{-1}.

Entonces C_s*G_sC_s=G_s, T_s=g(s)T₀g(s)^{-1}, y

T_s*G_sT_s+(8/81)(I−C_s)*G_s(I−C_s)=G_s.

La demostración consiste en cancelar las g(s) inversas en cada producto. La fórmula de η da simultáneamente η_sg(s)=g(s)^{⊕9}η₀. La memoria y la compresión se transportan por un cuadrado conmutativo real, con una métrica indicada, sin exigir que g(s) conmute con C₀ en una carta fija. Esta extensión no compone por sí sola un operador en H_W con un flujo en V: tales dominios siguen separados hasta proporcionar la aplicación entre ellos.

El espejo g(−s)=g(s)^{-1} y el espejo r→1/r son recíprocos en sus respectivas cartas. La identidad del tipo de involución no suministra por sí sola un mapa entre V y el plano espectral. La composición firme recuperada es memoria→K→u_K/P₁₀; el transporte métrico anterior es una consecuencia nueva verificable de esa realización finita.

## Comprobación material

`verify_nonadic_k.py` usa únicamente `fractions` y `json`, no escribe archivos, no consulta red y no contiene `assert`. Los modos ordinario, `-O` y `-I -S` deben terminar en `PASS_NONADIC_K_EXACT`. El recibo corresponde a controles algebraicos finitos y no sustituye los enunciados generales ni convierte los distintos C del corpus en un único operador.
