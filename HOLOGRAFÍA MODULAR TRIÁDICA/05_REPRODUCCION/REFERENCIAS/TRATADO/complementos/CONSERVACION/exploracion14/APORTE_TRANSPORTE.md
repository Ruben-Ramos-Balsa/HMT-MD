# Transporte de la dirección dodecafásica por la conservación completa de memoria

Fecha: 14 de septiembre de 2026. Desarrollo focal autónomo; fuentes del manuscrito fundacional conservadas sin modificación.

## 1. Resultado y procedencia

La isometría completa de memoria transporta el vector seleccionado por el registro, su recta y su complemento transversal. La recuperación tiene inversa de norma uno. La selección de la dirección utiliza el registro generado y la representación de incidencia ya declarada; no añade un ángulo, una escala ni una orientación ajustada. La proporción cuadrática `eta_K` se conserva como lectura del estado **y de los proyectores transportados conjuntamente**.

Este resultado compone antecedentes existentes. La selección `u_K`, el proyector `P10(K)`, su recuperación desde dos memorias y `eta_K` ya están escritos y demostrados. El transporte de observables por una isometría, la conservación exterior y la acción cotangente también tienen propietarios. La presente nota reúne su aplicación a la dirección de K, añade cotas focales para el registro completo y formula una carga variacional concreta. Estatuto: **formalización añadida de arquitectura autoral preexistente**, con novedad limitada a esta composición en el expediente, sin declaración de prioridad mundial.

Fuentes leídas directamente:

1. [Dirección seleccionada por K](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/k_direccion_dimensional.tex:1>): representación de `A5/C5`, carácter, `P3`, `P11`, norma positiva de `u_K`, definición de `P10` y covariancia.
2. [Registro dodecafásico](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_k.tex:181>): lectura del estado terminal, canales orientados, inversión de Hadamard y evaluación de K.
3. [Reconstrucción incidencial y covariancia](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/05.tex:1>): isometría incidencial F, transporte de operadores, recuperación por complementos, refinamiento con marcos locales y distinción entre covariancia y conmutación en carta fija.
4. [Acoplamiento reversible y transporte no estacionario](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/10.tex:140>): identidad telescópica, terminal positivo, isometría completa y adjunto inversor.
5. [Reconstrucción dimensional y conservación exterior](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/11.tex:1>): dos memorias, `||L||=9/4`, `P10`, `eta_K`, grados exteriores y acción cotangente de soporte finito; proposición `nuc11:noether`.
6. [Antecedente de investigación](</Users/ruben/Documents/New project/output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911/RECONSTRUCCION_DIMENSIONAL_DESDE_MEMORIA_Y_LEY_EXTERIOR_20260912.md:198>): primera exposición local del descriptor y su procedencia limitada. El certificado antecedente también contiene `P10 k=k-u` y el balance cuadrático; esos dos hechos se recuperan aquí, no se presentan como descubrimientos.

El resolutor global consultado sigue devolviendo el testigo de 2.084 páginas. No se modificó ese puntero: el propietario focal autorizado es el manuscrito fundacional citado, posterior a la selección integral de 2.249 páginas de la serie.

## 2. Corte causal y estructura de partida

Se conserva la composición APP–TRIT–TPK del manuscrito: las hojas aditiva y multiplicativa mantienen residuo y cociente; TRIT conserva régimen y orientación; la selección, el transporte y la actualización TPK conservan acarreo, ruta, frontera, incidencias y memoria del mismo estado enriquecido y de su estructura discreta conjunta del continuo. En el corte utilizado aquí, el registro de canales del estado terminal produce el vector firmado U y la inversión orbital de Hadamard produce K. Las realizaciones lineales y los caracteres de incidencia actúan después sobre ese registro. Ninguna constante convencional selecciona sus componentes.

La nota comienza en esta salida tipada y compone lectores posteriores. No reconstruye K a partir del descriptor ni pretende que doce coordenadas sustituyan la historia enriquecida completa. Tampoco modifica la generación correlacionada de las coordenadas regionales y de alfa ni sus dos vías internas.

En la realización lineal posterior `H=R^12`, sea `e=(1,...,1)`,

\[
 \Pi=I-\frac{ee^*}{12},\qquad
 P=P_3=\frac3{60}\sum_{g\in A_5}\chi_3(g^{-1})\rho(g).
\]

La carta y el carácter son exactamente los de la fuente 1. Se tienen `P=P*=P²`, `rank P=3`, `P e=0` y `P Pi=Pi P=P`. Ponemos

\[
 k=\Pi K,\qquad u=Pk,\qquad
 E_u=\frac{uu^*}{\|u\|^2},\qquad Q_K=\Pi-E_u=P_{10}(K).
\]

Para el registro ya generado,

\[
 K=(234,543,140,729,659,824,621,58,914,794,146,601),
\]

\[
 \|k\|^2=\frac{11789915}{12},\qquad
 \|u\|^2=\frac{6638585+2275584\sqrt5}{20}>0.
\]

La no nulidad fija la recta sin parámetro suplementario. El descriptor antecedente es

\[
 \eta_K=\frac{\|u\|^2}{\|k\|^2}
 =\frac{3(6638585+2275584\sqrt5)}{5\cdot11789915}
 \simeq0.5967954228259091.
\]

Como `P` es ortogonal, `u* k=||u||²`; por tanto

\[
 E_uk=u,\qquad Q_Kk=k-u,\qquad
 \boxed{k=u+Q_Kk,\quad u\perp Q_Kk.}
\tag{1}
\]

En consecuencia `eta_K` y `1-eta_K` son los pesos cuadráticos exactos de la recta seleccionada y de su complemento en este estado. Esta igualdad sobre k no identifica los operadores `E_u` y `P3`: el segundo tiene rango tres y el primero rango uno. En particular, `Q_K` conserva las dos direcciones de `im P3` ortogonales a u.

## 3. Isometría de memoria y proyector transportado

Se toma la composición de lectores no estacionarios ya construida. Para unitarios `C_n` en H,

\[
 T_n=(8I+C_n)/9,\qquad D_n=\sqrt8(C_n-I)/9,
 \qquad R_0=I,\quad R_{n+1}=T_nR_n.
\]

La notación `R_n` reemplaza aquí al `P_n` del capítulo 10 para distinguirlo de los proyectores de incidencia. Los coeficientes proceden de la partición colectiva `8+1` entre las nueve posiciones, como demuestra ese capítulo.

La identidad local `T_n*T_n+D_n*D_n=I` da, por telescopía,

\[
 I=R_N^*R_N+\sum_{n<N}R_n^*D_n^*D_nR_n.
\tag{2}
\]

Los operadores positivos `R_N*R_N` decrecen fuertemente a `A_infty`. La aplicación completa es

\[
 Vx=\bigl(A_\infty^{1/2}x,(D_nR_nx)_{n\ge0}\bigr),
 \qquad V^*V=I,
\tag{3}
\]

con codominio de trabajo `M=im V`, cerrado. Su inversa sobre M es V*, de norma uno. Para una profundidad finita se usa

\[
 V_Nx=(R_Nx,D_0x,\ldots,D_{N-1}R_{N-1}x)
\]

y se obtiene la misma propiedad. No se exige que el terminal vectorial `R_Nx` converja; la componente terminal de (3) procede del límite de Gram.

**Teorema de transporte de la dirección.** En M, defínanse

\[
 K^V=VK,\quad \Pi^V=V\Pi V^*,\quad P^V=VPV^*,\quad
 k^V=\Pi^VK^V,\quad u^V=P^Vk^V.
\]

Entonces

\[
 \boxed{u^V=Vu,\qquad
 Q_K^V=VQ_KV^*
 =\Pi^V-\frac{u^V(u^V)^*}{\|u^V\|^2}.}
\tag{4}
\]

`Q_K^V` es el proyector ortogonal de rango diez sobre `V(im Q_K)` y

\[
 V^*u^V=u,\quad V^*Q_K^VV=Q_K,\quad
 \|u^V\|=\|u\|,\quad \eta_K^V=\eta_K.
\tag{5}
\]

**Prueba.** Insertar `V*V=I` en cada composición da `k^V=Vk` y `u^V=Vu`. La misma identidad prueba conservación de productos y adjuntos. La igualdad de normas permite transportar el cociente de rango uno exactamente como en (4). La idempotencia, autoadjunción y rango se conservan por el isomorfismo isométrico `V:H→M`. El cociente de las normas de `u^V` y `k^V` prueba la invariancia de eta. Las composiciones con V* dan las dos fórmulas inversas. Esto demuestra todas las afirmaciones.

La identidad sobre M es `VV*`, no la identidad de la suma de Hilbert ambiente. La extensión por cero de `Q_K^V` al complemento de M es canónica como operador `VQ_KV*`, pero sus ceros adicionales no representan nuevas direcciones físicas ni nuevo contenido del registro.

### Observables conservados

Para cualquier operador acotado A en H, sea `A^V=VAV*|M`. Para `x,y∈H`,

\[
 \langle Vx,A^VVy\rangle=\langle x,Ay\rangle.
\tag{6}
\]

La correspondencia conserva productos, adjuntos, norma, espectro en M, trazas de operadores de rango finito y medidas espectrales. Aplicada a (1), conserva la dirección, el complemento, sus ángulos, los dos pesos `eta_K`, `1-eta_K`, y todas sus correlaciones con otros observables transportados. Para cada grado exterior finito, `Lambda^p V` conserva los determinantes de Gram, incluidos los términos que mezclan lectura terminal y memorias. Es la aplicación del teorema exterior antecedente a estos sectores concretos.

No se introduce un postulado probabilístico al llamar pesos a estas razones de normas. Su lectura como probabilidades de una medida cuántica requeriría la preparación normalizada y el observable de esa realización.

## 4. Aplicación operativa: estabilidad sin amplificación y coherencia entre memorias

Con el registro completo perturbado `y=VK+delta`, `||delta||≤epsilon`, la reconstrucción

\[
 \widehat K=V^*y,\qquad
 \widehat k=\Pi\widehat K,\qquad
 \widehat u=P\widehat k
\]

satisface

\[
 \|\widehat K-K\|\le\epsilon,\qquad
 \|\widehat k-k\|\le\epsilon,\qquad
 \|\widehat u-u\|\le\epsilon.
\tag{7}
\]

Esta reconstrucción es válida aunque y no pertenezca a M. La componente de ruido ortogonal a M es anulada por V*. Si `epsilon<||u||`, el proyector reconstruido está definido y

\[
 \boxed{\|Q_{\widehat K}-Q_K\|\le\epsilon/\|u\|.}
\tag{8}
\]

La prueba es la distancia entre las rectas de u y `u_hat`: su seno angular es `dist(u,span(u_hat))/||u||≤||u-u_hat||/||u||`. Los proyectores de rango uno tienen exactamente esa distancia operatoria. Frente a la cota antecedente `9 epsilon/(4||u||)` para dos memorias solas, (8) elimina el factor `9/4` al conservar el registro completo con su terminal. Para el K documentado, `||u||≈765.733`; el factor de (8) es aproximadamente `0.00130594`, frente a `0.00293836` del lector de dos memorias. Son modelos de datos diferentes: la mejora utiliza los canales adicionales, no declara mejor información con idénticas observaciones.

Si `epsilon<||k||`, también

\[
\boxed{|\eta_{\widehat K}-\eta_K|\le\epsilon/\|k\|.}
\tag{9}
\]

**Prueba de (9).** Sean x e y las normalizaciones de k y `k_hat`. La diferencia `xx*-yy*` tiene, sobre su plano, valores propios `+sin(theta)` y `-sin(theta)`. Para `0≤P≤I`, su emparejamiento de traza con P tiene módulo a lo sumo `sin(theta)`. Por otro lado, `sin(theta)=dist(k,span(k_hat))/||k||≤epsilon/||k||`. Las razones de Rayleigh de P son precisamente los dos valores de eta. La desigualdad permanece válida en el caso colineal, donde la diferencia es cero.

### La conservación requiere las correlaciones entre bloques

Escribamos `Vx=(W_a x)_a`, incluyendo el terminal. El bloque `(a,b)` del observable transportado es

\[
 (Q_K^V)_{ab}=W_aQ_KW_b^*.
\tag{10}
\]

Así la respuesta exacta a un registro y es la de este operador completo. Su forma cuadrática se entiende como el límite de truncaciones por bloques:

\[
 \langle y,Q_K^Vy\rangle
 =\lim_{F\uparrow\mathcal A}
 \sum_{a,b\in F}\langle y_a,W_aQ_KW_b^*y_b\rangle.
\tag{11}
\]

La convergencia procede de la acotación de `Q_K^V` y de la convergencia fuerte de las proyecciones de truncación; no se presupone convergencia absoluta de una doble serie arbitraria. Descartar sus bloques fuera de la diagonal cambia en general el observable.

Un ejemplo mínimo del mismo balance lo muestra. Para `H=R`, `C=-I`, `T=7/9`, `D=-2 sqrt(8)/9` y `Vx=(Tx,Dx)`, sea `A=I`. La lectura completa da `||x||²`. Retener sólo la diagonal de `VAV*` y evaluarla sobre Vx da

\[
 (T^4+D^4)|x|^2=\frac{3425}{6561}|x|^2,
\]

mientras que los dos términos cruzados aportan `3136/6561 |x|²`. La suma vuelve a ser uno. Es un control algebraico del acoplamiento, no una trayectoria física seleccionada. Establece que conservar únicamente magnitudes de cada memoria no equivale a conservar la forma observable que liga dirección e incidencia.

## 5. Covariancia de marco y refinamiento

Para un isomorfismo ortogonal `G:H→H'`, transportamos

\[
 K'=GK,\quad \Pi'=G\Pi G^*,\quad P'=GPG^*.
\]

Se obtiene `u'=Gu`, `Q_K'=GQ_KG*` y `eta'=eta`. La transformación afín `K↦aK+b e`, `a≠0`, conserva el proyector y el descriptor en la carta fija; la nota antecedente ya lo demuestra. Esta invariancia de la realización lineal no declara que cada transformación afín sea una historia TPK admitida.

Los marcos locales del capítulo 5 dan una aplicación de refinamiento efectiva:

\[
 \mathscr R_n(e_z\otimes x)
 =\sum_{\tau z'=z}\sqrt{\mu(z')/\mu(z)}
   e_{z'}\otimes G_{z'}G_z^*x.
\]

Defínanse en cada fibra `Q_z=G_zQ_KG_z*`, y de igual manera `Pi_z,P_z,u_z`. Entonces

\[
 \boxed{\mathscr Q_{n+1}\mathscr R_n
 =\mathscr R_n\mathscr Q_n,\qquad
 \mathscr R_n^*\mathscr Q_{n+1}\mathscr R_n=\mathscr Q_n.}
\tag{12}
\]

**Prueba.** En cada descendiente,
`Q_z' G_z' G_z*=G_z' Q_K G_z*=G_z'G_z* Q_z`.
La suma conserva los pesos; su suma cuadrática es uno. Se obtienen el entrelazamiento y la compresión. La composición a varias profundidades y la extensión al límite inductivo proceden de las isometrías compatibles, exactamente como en el propietario. Aplicar el mismo argumento a `E_u` conserva el otro sector. Tensorizar con una fibra ya construida y transportar la forma mantiene la identidad; el rango resultante es el rango tensorial correspondiente, no una identificación con una dimensión física por coincidencia numérica.

Este resultado transporta una dirección ya seleccionada en las fibras y conserva sus etiquetas. Una actualización del registro por nuevos eventos puede cambiar K. Determinar esa actualización utiliza el operador de eventos del corpus; (12) no impone artificialmente que el registro escalar permanezca constante durante cualquier evolución enriquecida.

### Control exacto contra una invariancia indebidamente universal

Con `Sx_i=x_(i+1)` y el P3 de la carta publicada, se recalculó en `Q(sqrt5)`:

\[
 \|P_3S^3K\|^2=\frac{369035}{4}-\frac{281861}{10}\sqrt5,
\]

\[
 \|P_3S^4K\|^2=\frac{1327717}{4}+\frac{694618}{5}\sqrt5.
\tag{13}
\]

Son distintos de `||P3K||²=1327717/4+568896 sqrt5/5`; además los conmutadores `[P3,S³]` y `[P3,S⁴]` son no nulos. El cálculo utiliza la suma de sesenta términos de `projector_three()` en el propietario `variacional.py`, cargada en lectura sin ejecutar su función de escritura. Por tanto eta en una carta mantenida fija no es constante bajo esos cambios aislados de K. En cambio, al transportar también P3 mediante `S^j P3 S^(-j)`, (4)–(5) conservan exactamente eta. Este control no contradice la conservación: identifica qué objetos deben viajar conjuntamente.

El propietario exacto es [variacional.py, función projector_three](</Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/IV_MOONSHINE_DUALIDAD_TEORIA_M/antecedentes/controles_articulo_I/propietarios_k_moonshine/variacional.py:306>); `q5_text`, `dot` y `matrix_vector` se definen en las líneas 132, 215 y 230. El bloque `if __name__ == "__main__"` de la línea 822 protege la ejecución que escribe el certificado. Este control reproducible usa otro nombre de ejecución y no crea archivos:

```bash
python3 -I -S - <<'PY'
from fractions import Fraction as F
import runpy
p = '/Users/ruben/Documents/New project/output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/IV_MOONSHINE_DUALIDAD_TEORIA_M/antecedentes/controles_articulo_I/propietarios_k_moonshine/variacional.py'
r = runpy.run_path(p, run_name='hmt_direction_read_only')
P = r['projector_three']()
K = [(F(x), F(0)) for x in (234,543,140,729,659,824,621,58,914,794,146,601)]
expected = {0: (F(1327717,4), F(568896,5)),
            3: (F(369035,4), F(-281861,10)),
            4: (F(1327717,4), F(694618,5))}
for j, target in expected.items():
    x = K[j:] + K[:j]
    actual = r['dot'](x, r['matrix_vector'](P,x))
    if actual != target:
        raise ArithmeticError(('norma cuadrática', j, actual, target))
    S = [[r['ONE'] if c == (i+j)%12 else r['ZERO'] for c in range(12)] for i in range(12)]
    commutes = r['matmul'](S,P) == r['matmul'](P,S)
    if commutes != (j == 0):
        raise ArithmeticError(('conmutador', j, commutes))
    print(j, r['q5_text'](actual), 'conmuta=', commutes)
print('CONTROL_Q5_DIRECCION_COMPLETADO')
PY
```

## 6. Carga de Noether concreta en la acción de transporte

Se usa la acción auxiliar ya definida en `nuc11:accion-local`; no se la rebautiza como acción física del corpus. Sean `U_n:E_n→E_(n+1)` los transportes completos invertibles y

\[
 L_n=p_{n+1}^*(q_{n+1}-U_nq_n).
\]

Las variaciones de soporte finito dan `q_(n+1)=U_nq_n` y `p_n=U_n* p_(n+1)`. Fijemos en el nivel inicial el proyector Q_K en el portador correspondiente, o `diag(Q_K,Q_K)` cuando se use el acoplamiento de lectura y memoria. Con `G_0=I`, `G_(n+1)=U_nG_n`, definimos

\[
 A_n=G_n A_0G_n^{-1}.
\]

El entrelazamiento `A_(n+1)U_n=U_nA_n` es exacto. La proposición variacional del manuscrito da

\[
 \boxed{J_n=p_n^*A_nq_n=J_0.}
\tag{14}
\]

**Prueba directa.** Sustituir las dos ecuaciones de evolución y el entrelazamiento en `J_(n+1)` produce `p_n* A_n q_n`. La simetría que genera esta carga es `q_n↦exp(t A_n)q_n`, `p_n↦exp(-t A_n*)p_n`. La acción queda invariante porque la exponencial entrelaza U_n. Esto es una simetría del espacio cotangente aun cuando A_n sea un proyector simétrico, no un generador antisimétrico.

Si U_n es ortogonal para las métricas declaradas, A_n sigue siendo proyector ortogonal y la elección `p_n=q_n` es compatible con las ecuaciones. Entonces (14) se convierte en

\[
 J_n=\|A_nq_n\|^2,
\]

la magnitud cuadrática del sector transversal transportado. La carga de su complemento se conserva igualmente. Para transportes que preservan una forma alternante pero no la norma positiva, (14) conserva el emparejamiento cotangente; no se transforma sin más en una energía positiva.

Finalmente, si `V_n:E_n→M_n` son isometrías completas de registro, defínanse sobre sus imágenes

\[
 \widehat U_n=V_{n+1}U_nV_n^*,\quad
 \widehat A_n=V_nA_nV_n^*,\quad
 \widehat q_n=V_nq_n,
\]

y la covariable `p_hat_n(y)=p_n(V_n* y)`. Se cumple

\[
 \widehat A_{n+1}\widehat U_n
 =\widehat U_n\widehat A_n,\qquad
 \widehat p_n(\widehat A_n\widehat q_n)=p_n(A_nq_n).
\tag{15}
\]

La acción y su carga se transportan exactamente al registro completo, con todos los dominios e inversas restringidos a sus imágenes. Esto responde a la pregunta de observabilidad: la misma carga puede evaluarse antes o después del almacenamiento de memoria, sin añadir un parámetro a K.

## 7. Alcance y siguiente aplicación permitida

La función demostrada del registro en esta composición es doble: selecciona una polarización en su representación de incidencia y permite conservarla y reconstruirla a través de la memoria. El descriptor mide la distribución cuadrática entre los sectores seleccionados; el proyector conserva una información geométrica más rica que ese escalar. Las fórmulas (4), (8), (12) y (15) forman una cadena operativa: selección, transporte, recuperación estable y evaluación de carga.

La extensión a una realización física concreta utilizará su operador de acoplamiento y su mapa de observables ya tipados. Las dimensiones diez y once aquí son rangos de proyectores sobre el portador declarado; no se identifica por ese solo hecho una compactificación ni una equivalencia con teoría M. Tampoco se identifica el descriptor con alfa ni con una constante universal: el resultado caracteriza el registro y los lectores efectivamente usados.

### Registro de comprobación de esta nota

Se reprodujeron el control del núcleo formal, el arranque local y la autocomprobación de causalidad de constantes, con sus salidas positivas. Se ejecutó el protocolo operativo HMT en modo de lectura y se registró su puntero histórico, sin modificarlo. Las identidades (13) se evaluaron con aritmética racional cuadrática exacta y sin escrituras del propietario. Las pruebas (1)–(15) están escritas aquí; los controles finitos no sustituyen las demostraciones de isometría, límite o naturalidad. Los recibos del manuscrito mantienen su alcance antecedente y no se presentan como certificados automáticos de una incorporación nueva. Esta nota no compila, modifica ni entrega otro PDF.
