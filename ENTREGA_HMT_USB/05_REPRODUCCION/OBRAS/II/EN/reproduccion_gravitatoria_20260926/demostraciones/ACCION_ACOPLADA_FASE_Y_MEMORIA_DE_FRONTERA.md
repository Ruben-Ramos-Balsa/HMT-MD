# Acción acoplada, fase y memoria de frontera

25 de septiembre de 2026. Investigación y formalización focal. No se modifican manuscritos, PDF, paquetes ni Lean. Esta nota continúa las pruebas de retorno de vacancias y reciprocidad radial; conserva sus resultados y explicita las hipótesis de cada composición.

## 1. Base HMT y objetivo delimitado

La base heredada es APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. APP conserva hojas suma–producto, residuo, cociente y acarreo. TRIT determina régimen y orientación. El TPK selecciona, transporta y actualiza; el retorno de fase conserva el avance de memoria. Se mantienen conjuntamente las cinco construcciones consustanciales del continuo, sin convertir sus lectores en generadores independientes.

El orden es U_t → Γ₉ → K_ph y la prolongación w6 → w12 → w18 → w24 → w30 → R36 → G9. Los objetos focales son salidas posteriores: rutas, transportes de fibra, diferencias covariantes, respuesta energética y sección de acción. El reconocimiento convencional es posterior. Los valores experimentales de G no eligen un operador ni un coeficiente.

El propietario VII, `30b_variacion_energia_memoria.tex`, define la energía del transporte con un peso global positivo que puede acoplar aristas diferentes. La reducción anterior de esta investigación trataba pesos independientes. Esta nota extiende aquella prueba al dominio completo declarado por el propietario y enlaza la reducción estática con la dinámica de memoria de `02_dinamica_tres_hojas.tex`.

La pregunta precisa es qué conserva la eliminación de variables cuando el transporte, sus acoplamientos y la fase pertenecen a una misma realización. El resultado radial previo G=c³L²/ℏ permanece con sus premisas; no se condiciona a demostrar otra acción completa de Cartan–Holst.

## 2. Eliminación con un peso global acoplado

Considérese una ruta finita de N incidencias con fibras H_j y transportes invertibles U_j:H_{j−1}→H_j. La realización unitaria del propietario está incluida. Sean

\[
r_j=f_j-U_jf_{j-1},\qquad
\mathcal K=\bigoplus_{j=1}^{N}H_j,\qquad
W=W^*>0\quad\text{en }\mathcal K.
\]

La acción declarada es S=𝔞 r*Wr, con 𝔞>0 y extremos f₀=a, f_N=b. El factor 𝔞 conserva las unidades y la normalización de la acción fuente; aquí no se selecciona por ajuste. Se define

\[
U_\gamma=U_N\cdots U_1,\quad B_j=U_N\cdots U_{j+1},\quad B_N=I,
\quad B=[B_1\ \cdots\ B_N],\quad z=b-U_\gamma a.
\]

La recurrencia de los campos equivale a Br=z. Como B_N=I, B es sobreyectiva. Por tanto,

\[
\boxed{R=BW^{-1}B^*>0.}
\tag{1}
\]

**Teorema 1.** La extensión minimizante y la acción de frontera son

\[
y=R^{-1}z,\qquad r_{\min}=W^{-1}B^*y,\qquad
\boxed{S_{\rm ef}=\mathfrak a\,z^*R^{-1}z.}
\tag{2}
\]

**Prueba.** Br_min=RR⁻¹z=z. Cualquier otra extensión es r_min+k, Bk=0. Se tiene k*Wr_min=k*B*y=0, por lo que

\[
(r_{\min}+k)^*W(r_{\min}+k)=z^*R^{-1}z+k^*Wk.
\]

La positividad estricta da la unicidad. La reconstrucción f_j=U_jf_{j−1}+r_j recupera cada estado intermedio. ∎

Los bloques fuera de la diagonal de W⁻¹ conservan las correlaciones entre incidencias. En particular,

\[
R=\sum_{j,k}B_j(W^{-1})_{jk}B_k^*.
\tag{3}
\]

La suma con j=k solamente es exacta cuando los bloques cruzados pertinentes se anulan. No es una abreviatura inocua en el caso acoplado.

## 3. Concatenación que conserva las correlaciones

Divídase la ruta en dos tramos. Sean B₁ y B₂ sus aplicaciones de defecto a sus respectivas fibras finales, U₂ el transporte completo del segundo tramo y C_ij los bloques de W⁻¹ relativos a esa partición. Defínase

\[
R_{ij}=B_iC_{ij}B_j^*.
\]

La aplicación final es [U₂B₁, B₂] y, por multiplicación,

\[
\boxed{R=U_2R_{11}U_2^*+U_2R_{12}+R_{21}U_2^*+R_{22}.}
\tag{4}
\]

Eliminar primero dentro de cada tramo conserva la matriz completa (R_ij), no sólo sus dos bloques diagonales. Su inversa es el peso efectivo de los dos defectos intermedios. La segunda eliminación produce exactamente (4).

**Prueba de independencia de la agrupación.** Sea A la aplicación por bloques que produce los defectos de los tramos, y T su composición hacia la frontera final. Como B=TA,

\[
BW^{-1}B^*=T(AW^{-1}A^*)T^*.
\tag{5}
\]

La fórmula vale para cualquier agrupación finita sobreyectiva. Conserva tanto la acción como los términos cruzados; no presupone un límite continuo. ∎

## 4. Inversión de ruta y diferencial completo

La inversión define una aplicación invertible J entre las sumas de fibras de residuos:

\[
(Jr)_{N+1-j}=-U_j^{-1}r_j.
\]

El peso inverso correcto, incluidos los acoplamientos, es

\[
W_{\rm inv}=J^{-*}WJ^{-1}.
\tag{6}
\]

Se verifica r_inv*W_inv r_inv=r*Wr. Como z_inv=−U_γ⁻¹z y B_inv J=−U_γ⁻¹B,

\[
R_{\rm inv}=U_\gamma^{-1}R\,U_\gamma^{-*},\qquad
S_{{\rm ef},{\rm inv}}=S_{\rm ef}.
\tag{7}
\]

Si J depende de la variación, también varía W_inv. Esta contribución forma parte de la identidad y no puede omitirse al comparar ida y vuelta.

Para una familia diferenciable de transportes, pesos y extremos,

\[
\dot R=\dot BW^{-1}B^*+BW^{-1}\dot B^*
-BW^{-1}\dot WW^{-1}B^*,
\]

\[
\boxed{\dot S_{\rm ef}=\dot{\mathfrak a}\,z^*y
+\mathfrak a\bigl(2\operatorname{Re}(y^*\dot z)-y^*\dot Ry\bigr).}
\tag{8}
\]

Es una identidad para todas las direcciones de la familia, incluidas las no conmutativas; se restringe después a las variaciones admitidas por la realización HMT.

**Prueba.** Derivar RR⁻¹=I da (R⁻¹)·=−R⁻¹R·R⁻¹. La regla del producto produce (8). Alternativamente, q=Wr_min=B*y. Si U·_j=A_jU_j, la parte de conexión obtenida antes de eliminar es

\[
-2\mathfrak a\operatorname{Re}\sum_jq_j^*A_jU_jf_{j-1}.
\tag{9}
\]

Las variaciones de los campos interiores se cancelan por estacionariedad. Las contribuciones de extremo, peso y prefactor reproducen (8). ∎

Por tanto, está demostrada la igualdad variacional entre esta acción de memoria y su acción efectiva para el peso acoplado completo. No se limita a una dilatación. La igualdad concierne a la misma acción antes y después de eliminar; identificarla con otra acción exige utilizar el mapa de realización de esa otra acción.

## 5. Transferencia de la normalización desde el generador de fase

El propietario nativo escribe H=H_clk+D*WD. El propietario de acción de caminos, bajo su cláusula local, escribe S_int=ℏ𝒜*, con 𝒜*=n_g+λ*n_s, y conserva además el transporte ordenado de fibra. Ambos objetos tienen tipos distintos: el contador de una ruta y la forma energética de un campo no son intercambiables sin la realización que los compone.

Puede precisarse exactamente cómo una dinámica completa fija esa forma energética.

**Teorema 2.** Sean ℏ y H_clk fijados, y una familia de evolución sobre el espacio completo, incluida la memoria,

\[
P(t)=\exp(-itH/\hbar).
\]

Su primer jet determina H=iℏP′(0). Es suficiente conocer una familia coherente P(t_n) con t_n→0 y este generador acotado, pues

\[
H=i\hbar\lim_{n\to\infty}\frac{P(t_n)-I}{t_n}.
\tag{10}
\]

En una ruta puesta a tierra en f₀=0, el operador D₀:(f₁,…,f_N)↦r es triangular invertible. Si la realización identifica H−H_clk con D₀*WD₀, entonces

\[
\boxed{W=D_0^{-*}(H-H_{\rm clk})D_0^{-1}.}
\tag{11}
\]

La positividad de W equivale a la positividad de H−H_clk en este dominio. La congruencia es única y transmite a (1)–(2) su normalización absoluta.

**Prueba.** (10) se obtiene derivando la exponencial en cero; no selecciona por separado ramas de logaritmos finitos. Multiplicar la identidad cuadrática a izquierda y derecha por los inversos de D₀ prueba (11). ∎

Una reescala del coste que cambie H−H_clk cambia P′(0); no conserva la misma dinámica completa. En un grafo general, D puede tener núcleo: entonces el generador fija la forma sobre Ran D, no un peso arbitrario sobre todo el espacio de aristas. Esa distinción no afecta a la acción de los campos admisibles.

El teorema es un procedimiento de composición y de unicidad; no afirma que se haya evaluado aquí un nuevo H gravitatorio. El ejemplo racional del certificado comprueba la congruencia, su reducción y el primer jet, no selecciona la dinámica física por sus matrices de ensayo.

## 6. La memoria interviene también en el coeficiente temporal

El propietario `02_dinamica_tres_hojas.tex` ya conserva el resolvente de Feshbach–Schur. Este antecedente permite evitar otro recorte: usar únicamente un mínimo estático para representar una fase dinámica.

Sea H, en una carta fija y con las variables de memoria conservadas,

\[
H=\begin{pmatrix}H_{bb}&V\\V^*&H_{ii}\end{pmatrix},\qquad H_{ii}>0.
\]

En el dominio resolvente de H_ii, la eliminación dinámica exacta es

\[
\boxed{K_b(\omega)=H_{bb}-\hbar\omega I
-V(H_{ii}-\hbar\omega I)^{-1}V^*.}
\tag{12}
\]

La compresión de (H−ℏωI)⁻¹ a la frontera es K_b(ω)⁻¹, cuando ambos inversos existen. Para |ℏω|<λ_min(H_ii), la serie convergente da

\[
K_b(\omega)=H_{\rm est}-\hbar\omega Z
-(\hbar\omega)^2VH_{ii}^{-3}V^*-\cdots,
\]

\[
H_{\rm est}=H_{bb}-VH_{ii}^{-1}V^*,\qquad
\boxed{Z=I+VH_{ii}^{-2}V^*\geq I.}
\tag{13}
\]

La desigualdad es exacta porque Z−I=(H_ii⁻¹V*)*(H_ii⁻¹V*). Este término coincide con la norma adicional que conserva la extensión estática de mínima energía (b,−H_ii⁻¹V*b): su norma cuadrada es b*Zb. La energía y la norma temporal de la misma extensión quedan así coordinadas.

Al primer orden temporal, la coordenada canónica ψ=Z¹ᐟ²b transforma la pareja (H_est,Z) en (Z⁻¹ᐟ²H_est Z⁻¹ᐟ²,I). Esto no cambia ℏ. Restituye la normalización de estado que se perdería leyendo sólo H_est. Si los parámetros dependen del tiempo, la transformación incorpora además su derivada; la expresión (12) conserva la respuesta dinámica completa en la carta estacionaria.

Esta consecuencia procede de la reducción de memoria ya presente en el corpus. No es una nueva ley física ni un nuevo valor de G. Explica por qué conservar el mínimo y desechar la memoria temporal puede conservar una cifra energética y alterar la evolución que esa cifra debe representar.

## 7. Vacancias, normalización media y cierre radial

El retorno de capacidad conserva el cociclo de borde previamente demostrado:

\[
N(k,C)=(\rho^{-1}-1)C+\varepsilon(k+C)-\varepsilon(k),
\quad \rho=\log_{10}9.
\]

En la realización homogénea W_j=I/d_j y transportes unitarios, R=CI. La respuesta total es R⁻¹=I/C; la inversa de la respuesta media por incidencia es (R/N)⁻¹=(N/C)I. Así se recupera 35/729 para la ventana nativa concreta de 35 incidencias y capacidad 729. El mismo cociclo admite ventanas de 34 incidencias para esa capacidad. No se reinicia la memoria para imponer 35 en cada retorno.

En el caso acoplado, (1) reemplaza al cociente escalar. La identificación con la pantalla pentádica debe transportar sus espacios y su norma, junto con la fase, para que una igualdad escalar sea la lectura de una composición real. Los operadores (1), (8) y (12) dejan reunidas las cantidades que necesita esa composición.

El cierre radial recuperado conserva otra conclusión ya establecida: para los lectores M=ℏX/(cL), R_g=LX y λ̄=LX⁻¹, la realización R_g=(G/c²)M determina G=c³L²/ℏ. La composición aquí demostrada no modifica ese teorema ni convierte la comparación con Cartan–Holst en su condición previa.

## 8. Composición con el par radial y la norma temporal

CORPUS ha reunido en `CORPUS_COMPOSICION_MEMORIA_RADIO_20260925.md` la identidad del inverso comprimido y la conservación del residuo. Gemma ha compuesto en `CIERRE_CONJUNTO_CUATRO/COMPOSICION_Y_CRITERIO_FIJO.md`, §5.4, la respuesta dinámica: si R=κH sobre el mismo portador, entonces Schur(R−κzI)=κ Schur(H−zI). Se transporta también el parámetro espectral; κ=L²/(ℏc) convierte energía en longitud. Esta identidad conserva los órdenes de memoria de (12).

La normalización temporal de (13) admite una composición adicional precisa. Supóngase que la misma reducción ha producido R_eff=κH_eff y R_effΛ_b=L²I. Para una coordenada canónica ψ=Tb, con T invertible y T*T=Z, las formas de energía y radio se transportan por congruencia:

\[
H_{\rm can}=T^{-*}H_{\rm eff}T^{-1},\qquad
R_{\rm can}=T^{-*}R_{\rm eff}T^{-1}.
\]

La longitud recíproca, como operador dual, debe transformarse en

\[
\Lambda_{\rm can}=T\Lambda_bT^*.
\]

Entonces

\[
\boxed{R_{\rm can}=\kappa H_{\rm can},\qquad
R_{\rm can}\Lambda_{\rm can}=L^2I.}
\tag{14}
\]

**Prueba.** La primera igualdad es lineal. Para la segunda,
T⁻*R_effT⁻¹TΛ_bT*=T⁻*(L²I)T*=L²I. No se presupone que T conmute con R_eff. ∎

Ésta es la compatibilidad concreta entre el radio, la acción y la memoria temporal: la normalización inducida no agrega un factor independiente a G si se transportan las dos lecturas y su dual sobre el mismo portador. Aplicar la misma congruencia a Λ_b, en lugar de la congruencia dual, rompería el producto y produciría una discrepancia artificial. La identificación constitutiva de partida permanece explícita; la prueba demuestra su conservación bajo esta operación.

## 9. Conclusión y alcance de esta entrega

Se ha completado la reducción exacta del funcional acoplado que admite VII30b: mínimo, correlaciones entre tramos, inversión, diferencial en cualquier dirección admisible y transferencia de una normalización fijada por el generador completo. La eliminación dinámica conserva además el factor temporal Z y el resolvente dependiente de frecuencia; reducirla al mínimo estático descarta parte de la memoria.

La aportación focal no es anunciar de nuevo G ni escoger su valor mediante una fracción. Es reunir la respuesta de energía, su corriente y su fase sin tratarlas como lecturas independientes. La evaluación física de (11) requiere el generador concreto y su separación H_clk establecidos por la realización correspondiente. Esta nota no sustituye esos objetos por matrices de prueba ni declara evaluada esa composición gravitatoria.

`verificar_accion_acoplada_y_fase.py` ejecuta 65 comprobaciones racionales exactas. Comprueba pesos positivos acoplados, transportes no conmutativos, reducción por etapas, inversión, las 12 direcciones matriciales de conexión y las 21 direcciones simétricas del peso, congruencia del generador, primer jet de fase, resolvente y transporte dual de la longitud recíproca. Las demostraciones generales están en §§2–6 y §8; los ejemplos son falsadores focales.

## 10. Propietarios y continuidad

- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/07/ES/source/manuscrito/30b_variacion_energia_memoria.tex`: funcional con W global, variación, inversión y refinamiento.
- En la misma fuente, `fuentes_conservadas/02_dinamica_tres_hojas.tex`: H_clk+D*WD, hoja nilpotente y reducción de memoria por resolvente.
- En la misma fuente, `fuentes_conservadas/18_clausura_energetica.tex`: respuesta de pantalla, norma del defecto y extensión mínima.
- Integral, `incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/07_integral_genealogica_caminos.tex`: acción de rutas, fase y transporte completo de fibra.
- En esta carpeta, `RETORNO_DE_VACANCIAS_Y_ACCION_EFECTIVA.md`: retorno con cociclo de borde y reducción previa para pesos independientes.
- En esta carpeta, `RECIPROCIDAD_NATIVA_Y_ALCANCE_DEL_CIERRE_G.md`: reciprocidad anterior a G y coeficiente radial dentro de la realización declarada.

Procedencia: antecedentes recuperados; generalización acoplada y composición con la reducción dinámica formalizadas aquí; certificado focal nuevo. Las puertas de trazabilidad no sustituyen las demostraciones ni certifican, por sí solas, la selección física de G.
