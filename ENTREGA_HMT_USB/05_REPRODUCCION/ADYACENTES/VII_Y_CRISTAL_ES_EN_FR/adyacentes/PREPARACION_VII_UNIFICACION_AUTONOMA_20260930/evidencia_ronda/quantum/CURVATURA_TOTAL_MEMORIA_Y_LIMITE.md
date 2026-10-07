# Curvatura de deformaciones, memoria completa y límite compatible

Desarrollo del 29 de septiembre de 2026. Continúa el cálculo espacial anterior;
no sustituye los manuscritos, sus pruebas ni las diecisiete notas conservadas.
La identidad objetivo es la solicitada por el autor, no una hipótesis añadida.

## 1. Antecedente efectivo y alcance del cálculo

APP produce las dos hojas y sus datos de residuo, cociente y acarreo. TRIT
conserva orientación y régimen. TPK transporta y actualiza el estado enriquecido
con ruta, memoria y supervivencia. La estructura discreta conjunta del continuo
conserva sus cinco construcciones consustanciales. La prolongación
w6 → w12 → w18 → w24 → w30 → R36 → G9 conserva el prefijo; en
U_t → Γ9 → K_ph, el retorno de fase avanza memoria, no reinicia el estado.
Los coeficientes de acción son salidas HMT anteriores. Se fija una sección
positiva de esa acción, denotada por ℏ, antes del cálculo siguiente.

La operación focal que se compone aquí es precisamente la conservación de la
memoria durante una lectura: no se identifica el generador completo con su
bloque visible. La doble proyección se mantiene como lectura del mismo estado,
no como sustitución de las identidades entre operadores por igualdad de valores.
El reconocimiento convencional posterior usa conexiones y cálculo de bloques
para expresar esa composición ya tipada.

Propietarios materiales:

1. `VII_ES/manuscrito/desarrollos/restitucion_operatoria.tex`, §dilatación:
   lectura 8:1 más complemento y composición exacta de la dilatación.
2. `VIII_ES/manuscrito/30b_variacion_energia_memoria.tex`, ecuaciones
   `vii:eq:variacion-completa-memoria` y
   `vii:eq:variacion-transporte-compuesto`: se varían conjuntamente campo,
   transporte y peso; la regla del producto conserva la posición en la ruta.
3. `X_ES/supplement/00_MEMORIA_Y_FORMA.md`: reconstrucción de K, forma positiva,
   refinamiento energético y complemento reconstructible.
4. `II_ES/ampliacion_20260922.tex`, teorema del generador diferenciable:
   término de conexión del transporte de la elipse y distinción entre cambio
   de marco y deformación física.
5. `XII_ES/sections/aritmetica_historias.tex`: cociclo torcido de rutas y
   memoria que distingue historias con la misma publicación observable.

Los puntos 1–3 se leen bajo
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`;
4–5 bajo
`/Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/`.
Las notas previas `MEMORIA_DOMINIO_Y_ALGEBRA.md` y
`DIMENSION_DENSIDAD_ENTRELAZAMIENTO.md` demostraron la compresión fija y el
transporte temporal. Aquí se calculan **dos variaciones y su curvatura**, incluido
el movimiento de la inclusión y el complemento de memoria.

## 2. Qué representa exactamente la fórmula solicitada

Sea B un dominio de realizaciones admitidas del mismo estado enriquecido y sea
E → B su campo de espacios hermíticos. En una trivialización local unitaria,
δ_N actúa sobre los coeficientes y cumple
[δ_N,δ_M] = δ_[N,M]. La notación [N,M] designa el corchete de las
**deformaciones efectivas**, no el producto de dos funciones de lapse. Si las
deformaciones dependen del estado, incluye su variación mutua.

En un núcleo común invariante se define

\[
 \nabla_N=\delta_N+A_N,\qquad A_N=\frac{i}{\hbar}H_N.
\]

Una expansión de los cuatro productos, conservando la regla de Leibniz, da

\[
 [\nabla_N,\nabla_M]-\nabla_{[N,M]}
 =\frac{i}{\hbar}\mathcal F_{N,M},
\]
\[
 \boxed{\mathcal F_{N,M}=\delta_NH_M-\delta_MH_N-H_{[N,M]}
                  +\frac{i}{\hbar}[H_N,H_M].}\tag{1}
\]

Esto fija signos y dominios. En dimensión finita basta regularidad C²; para
operadores no acotados las igualdades se interpretan en un núcleo estable por
H_N, H_M, sus productos y las derivadas. La convergencia de resolventes aislada
no permite sustituir ese requisito cuando se toman conmutadores.

Si ℏ cambia físicamente con la realización, la curvatura de δ+iH/ℏ incluye
además

\[
 -(\delta_N\log\hbar)H_M+(\delta_M\log\hbar)H_N.\tag{2}
\]

La fórmula (1) corresponde a la sección fija declarada, o a una conexión que
transporte también la unidad de acción. No se elimina (2) por llamar a ℏ una
constante si en ese mismo cálculo se la ha hecho depender de B.

## 3. Cambio completo de marco: todos los términos quedan determinados

Sea W(q) unitario de clase C², preservando los núcleos implicados. De
∇' = W*∇W se obtiene, sin escoger un nuevo Hamiltoniano físico,

\[
 H'_N=W^*H_NW-i\hbar W^*\delta_NW.\tag{3}
\]

**Teorema 1.** La curvatura de (3) es

\[
 \boxed{\mathcal F'_{N,M}=W^*\mathcal F_{N,M}W.}\tag{4}
\]

**Prueba.** Para una sección ψ, ∇'_Nψ=W*∇_N(Wψ).
Insertar WW*=I entre las dos derivadas demuestra
[∇'_N,∇'_M]ψ=W*[∇_N,∇_M]Wψ. Restar ∇'_[N,M]
y aplicar (1). La prueba incluye las derivadas de W; omitirlas cambiaría el
operador. ∎

El término −iℏW*δ_NW es el análogo de dos parámetros del término mixto
de la elipse de acción. Es una consecuencia del transporte, no un corrector
ajustado para imponer la conclusión. (4) prueba también que un cambio de
marco no puede eliminar una curvatura genuina: conserva el operador completo.

## 4. Lectura móvil y memoria: cálculo exacto de la curvatura aparente

Sea J(q):E₀ → E una isometría C² y P=JJ*. Su conexión inducida es
J*∇J. El generador leído y la fuga al complemento son

\[
 h_N=J^*H_NJ-i\hbar J^*\delta_NJ,
 \qquad
 B_N=(I-P)\left(\delta_NJ+\frac{i}{\hbar}H_NJ\right).
\tag{5}
\]

B_N no es una constante ni una masa; es la componente de la derivada covariante
que sale del espacio leído y queda en la memoria. Para una isometría fija,
se reduce a (i/ℏ)(I−P)H_NJ.

Para H no acotado se exige que J, sus derivadas y la completación de marco
transporten los núcleos y normas de grafo utilizados en los productos. Si
no se ha probado el dominio de B_N*B_M, (6)–(7) se leen como identidades
de formas sesquilineales mediante ⟨B_Nu,B_Mv⟩ en el núcleo común; no se
afirma por notación la existencia de un producto de adjuntos en todo E₀.

**Teorema 2.** La curvatura calculada sólo con los h_N satisface

\[
 \boxed{\mathcal F^{\rm leida}_{N,M}
  =J^*\mathcal F_{N,M}J
       -i\hbar(B_N^*B_M-B_M^*B_N).}\tag{6}
\]

**Prueba.** Completar localmente J a una unitaria W=(J,R). La conexión
completa en ese marco tiene bloques

\[
 A'_N=\begin{pmatrix}a_N&-b_N^*\\b_N&d_N\end{pmatrix},
 \qquad a_N=\frac{i}{\hbar}h_N,\quad b_N=R^*B_N.
\]

El bloque superior de dA'+A'∧A' es

\[
 \delta_Na_M-\delta_Ma_N-a_{[N,M]}+[a_N,a_M]
                      -b_N^*b_M+b_M^*b_N.
\]

Por (4) es (i/ℏ)J*F_NMJ. Como RR*=I−P sobre el complemento,
b_N*b_M=B_N*B_M. Despejar da (6). Esta prueba es local; la fórmula no
depende de la elección de R y por ello vale globalmente donde existe J. ∎

Así queda identificado el término que faltaría al **cálculo comprimido**:

\[
 \boxed{\mathcal F^{\rm leida}_{N,M}
       +i\hbar(B_N^*B_M-B_M^*B_N)=J^*\mathcal F_{N,M}J.}\tag{7}
\]

Restaurar la memoria cancela exactamente ese defecto, tanto para cambios de
marco como para generadores no conmutativos. No significa que todo B sea cero,
ni que la curvatura situada a la derecha se anule por definición.

### 4.1. Aplicación literal a la lectura nonádica 8:1

La dilatación ya publicada utiliza el proyector constante

\[
 P_w=\frac19\begin{pmatrix}1&\sqrt8\\\sqrt8&8\end{pmatrix},
 \quad P_w^2=P_w,
 \qquad \widehat H_N=P_w\otimes H_N.
\]

El homomorfismo conserva derivadas y productos, de modo que

\[
 \widehat{\mathcal F}_{N,M}=P_w\otimes\mathcal F_{N,M}.
\tag{8}
\]

La lectura de la primera coordenada, sin el complemento, da h_N=H_N/9,
y por sustitución **directa** en (1),

\[
 \boxed{\mathcal F^{\rm visible}_{N,M}
    =\frac19\mathcal F_{N,M}
       -\frac{8i}{81\hbar}[H_N,H_M].}\tag{9}
\]

El complemento es B_N=i√8 H_N/(9ℏ); su contribución en (7) es
8i[H_N,H_M]/(81ℏ). Por tanto

\[
 \boxed{\mathcal F^{\rm visible}_{N,M}
        +\mathcal F^{\rm memoria}_{N,M}
          =\frac19\mathcal F_{N,M}.}\tag{10}
\]

Esto utiliza el coeficiente nonádico del propietario, no una dilatación
numérica inventada. Si el transporte original es plano, el visible aislado
puede no serlo; el estado completo restaura exactamente la identidad. Si el
original tiene curvatura de calibre, la conserva con el mismo tipo y sus
restricciones. No se confunde preservar una identidad con crearla.

## 5. El operador total: dónde entran las relaciones entre interacciones

La suma de generadores no autoriza sumar sólo sus curvaturas. Si
H_N=Σ_a H_N^(a), con el mismo ℏ, la misma δ y el mismo corchete,

\[
 \boxed{\mathcal F_{N,M}^{\rm tot}
 =\sum_a\mathcal F_{N,M}^{(a)}
 +\frac{i}{\hbar}\sum_{a<b}
 ([H_N^{(a)},H_M^{(b)}]+[H_N^{(b)},H_M^{(a)}]).}\tag{11}
\]

Cada F^(a) incluye la variación de los campos y lectores compartidos por ese
sector. (11) se prueba expandiendo el único conmutador total, sin cambiar la
base de variación entre sumandos. En particular, tratar la geometría como fija
en uno y variable en otro no calcula (11). Los términos de Yukawa, la corriente
total y su interacción torsional mantienen las dependencias de la misma acción.

(6)–(10) se aplican a H^tot sin eliminar ninguno de esos términos. Restaurar
memoria conserva también los productos cruzados de (11); no permite
descartarlos por separado. Para cotransporte unitario del operador total hay
una cancelación adicional exacta desarrollada en `COCICLO_ACCION_Y_CURVATURA.md`.
Para deformaciones de hipersuperficies del operador de Dirac derivado de la
acción, el cálculo de δ_NH_M se da en `CURVATURA_DEFORMACIONES_PCH.md`.

## 6. Restricciones de calibre: condición exacta de descenso

Sea P_phys un proyector físico ortogonal, preservado por la conexión completa.
Esto significa ∇_N(P_physψ)=P_phys∇_Nψ, no solamente [H_N,P_phys]=0
si P_phys depende de la realización. Si

\[
 \mathcal F_{N,M}=\sum_a f_{N,M}^aG_a,
 \qquad G_a\psi=0\quad(\psi\in\mathscr D_{\rm phys}),\tag{12}
\]

y los productos tienen el orden/domino escrito, entonces la conexión física
es plana sobre ese núcleo. El transporte de (12) por (3) transforma también
G_a y P_phys; la inclusión física horizontal hace B_N=0 y (6) conserva la
anulación. Este descenso es una prueba operatoria concreta de qué significa
«reducción a restricciones de calibre».

Una curvatura central f_NMI no satisface (12) en vectores no nulos si
f_NM≠0. Puede dar planitud **proyectiva**: el conmutador inducido sobre
observables es cero porque [fI,O]=0. No equivale a F=0 como operador ni
permite anular la memoria de un lazo. Si se añade una línea compensadora,
debe derivarse su curvatura opuesta; no basta llamarla «fase». El cociclo TPK y
su realización de Weyl se examinan con ese alcance en la nota citada.

## 7. Límite conjunto: un criterio que sí transporta la identidad completa

El índice λ puede incluir simultáneamente profundidad, refinamiento espacial
y corte de modos. No se identifican esos índices. Sean E_λ campos hermíticos
con inclusiones C² isométricas J_μλ que satisfagan composición exacta. La
condición de compatibilidad dinámica para una inclusión **móvil** es

\[
 \boxed{\delta_NJ_{\mu\lambda}
       +\frac{i}{\hbar}H_N^\mu J_{\mu\lambda}
       -\frac{i}{\hbar}J_{\mu\lambda}H_N^\lambda=0.}\tag{13}
\]

No se sustituye (13) por una igualdad de energías comprimidas. Es
∇_N^μJ_μλ=J_μλ∇_N^λ como operadores sobre secciones.

**Teorema 3.** Si (13) vale sobre núcleos compatibles invariantes, entonces

\[
 \mathcal F_{N,M}^{\mu}J_{\mu\lambda}
       =J_{\mu\lambda}\mathcal F_{N,M}^{\lambda}.\tag{14}
\]

Existe una conexión sobre el núcleo cilíndrico del límite inductivo, y si
F^λ_NM=G^λ(χ_NM), con inclusiones que también entrelazan G y los
proyectores físicos, entonces

\[
 \mathcal F^\infty_{N,M}=G^\infty(\chi_{N,M}),
 \qquad \mathcal F^\infty_{N,M}\psi=0
 \quad(\psi\in\mathscr D^\infty_{\rm phys}).\tag{15}
\]

**Prueba.** Aplicar dos veces (13), restar el intercambio N↔M y la
identidad correspondiente a [N,M]; así se obtiene (14). Definir
∇^∞_N(I_λψ)=I_λ∇^λ_Nψ: (13) demuestra que no depende del representante.
Repetir para productos prueba (15) en la unión de núcleos, densa por definición
del límite. La igualdad de clausuras requiere además que esa unión sea núcleo
para las clausuras que se comparan; para declarar igualdad de operadores
autoadjuntos hay que conservar sus dominios. ∎

Si Γ_λ son graduaciones quirales autoadjuntas con Γ_λ²=I y
J_μλΓ_λ=Γ_μJ_μλ, definen una graduación acotada Γ_∞ en el mismo límite.
Si las restricciones preservan esa graduación, también lo hace (15). No se
impone [H^tot,Γ]=0: la dinámica de masa/Yukawa puede mezclar las dos
subfibras sin borrar sus etiquetas. «Límite quiral» no significa suprimir esos
términos del operador total.

### 7.1. Inclusiones aproximadamente compatibles

Sea
E_N=∇_N^μJ−J∇_N^λ el defecto de (13). La identidad exacta es

\[
 (\mathcal R^\mu_{N,M}J-J\mathcal R^\lambda_{N,M})
 =\nabla_N^{\rm Hom}E_M-\nabla_M^{\rm Hom}E_N-E_{[N,M]},
 \quad \mathcal R=\frac{i}{\hbar}\mathcal F.\tag{16}
\]

Aquí ∇_N^Hom E_M=∇_N^μ∘E_M−E_M∘∇_N^λ. La expansión cancela los
términos intermedios y demuestra (16). Para pasar F al límite basta controlar
los tres términos derechos en el núcleo correspondiente, además de los
operadores que realizan el límite. E_N→0 sin control de sus derivadas no
lo implica. Si la aproximación se formula mediante holonomías de rectángulos,
el error debe ser o(st) al dividir por su área st.

## 8. Resultado que produce esta composición

Se ha calculado exactamente la contribución de la memoria y del cambio de
marco a (1), incluyendo el coeficiente 8/81 específico de la lectura nonádica.
También se ha demostrado cómo transportarla, sin pérdida, a un límite
conjunto que cumpla (13), y cómo desciende si la curvatura es una restricción
de calibre verdadera. No es una nueva auditoría de K ni de sus lectores.

Estas identidades permiten comprobar una propuesta de cierre total sin
fragmentarla: se calculan en el mismo estado los términos de (11), se restaura
el complemento mediante (7), y se aplica (13)–(16). Las cancelaciones efectivas
de las otras dos notas se conservan con sus dominios. No se declara una
anulación del operador cuántico gravitatorio total a partir únicamente de la
conservación de memoria, de una supercarga cuyo cuadrado es H, ni de la llegada
del corredor excepcional a una realización de teoría M.
