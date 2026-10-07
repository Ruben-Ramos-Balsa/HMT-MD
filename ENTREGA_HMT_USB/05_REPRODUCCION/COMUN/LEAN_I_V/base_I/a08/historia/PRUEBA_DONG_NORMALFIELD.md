# Localidad del producto normal: prueba y puerto exacto de formalización

## Alcance y procedencia

Esta nota trabaja sobre los campos ya construidos del mismo portador reticular
seleccionado. No modifica APP–TRIT–TPK, el registro seleccionado, el retículo ni
sus representaciones. Reutiliza la genealogía material del paquete de 279
módulos y la construcción posterior del mapa estado–campo. Las operaciones
convencionales que aparecen aquí son el lenguaje de prueba de esos objetos,
no selectores ni entradas de su generación.

Estatuto: **FORMALIZACIÓN NUEVA de una clausura clásica necesaria para la
construcción ya recuperada**. No es una nueva definición de HMT ni una
afirmación de que FLM o el orbifold estén formalizados íntegramente.

La prueba matemática siguiente es completa como argumento algebraico
coeficiente a coeficiente. Su traslado a Lean se divide en identidades de los
núcleos, el paso binomial de tres variables y su ensamblaje con las sumas
localmente finitas de los campos reales. Sólo los recibos individuales
certifican qué partes de ese traslado han compilado. Esta nota no sustituye
el teorema Lean de clausura de localidad.

## Convención y enunciado

Escribimos los coeficientes por exponentes de Laurent:

\[
H(t)=\sum_{k\in\mathbb Z}H_k t^k,\qquad
B(z)=\sum_{k\in\mathbb Z}B_k z^k,\qquad
C(w)=\sum_{l\in\mathbb Z}C_l w^l.
\]

Para el campo de Heisenberg construido, `H_k = hmode (-k-1)`.
Sean `p,q,s` órdenes de localidad efectivos tales que

\[
(t-w)^p[H(t),C(w)]=0,\quad
(z-w)^q[B(z),C(w)]=0,\quad
(t-z)^s[H(t),B(z)]=0.
\]

Para cada natural `n`, el campo `normalField o i n B` es local con `C`, con
orden suficiente

\[
\boxed{N=p+q+s+n.}
\]

No se exige que `p,q,s` sean mínimos. No se duplica el coste de la derivada:
el incremento de la cota es `n`, no `2n`.

## Los dos núcleos y el producto existente

Definimos las dos expansiones formales del mismo núcleo:

\[
K_n^+(t,z)=\sum_{a\ge0}\binom{a+n}{n}t^{-n-1-a}z^a,
\]
\[
K_n^-(t,z)=(-1)^{n+1}\sum_{a\ge0}\binom{a+n}{n}t^a z^{-n-1-a}.
\]

Son precisamente `leftExpansion (-n-1)` y `rightExpansion (-n-1)`;
`LatticeDongKernel.negative_contraction_binomial` demuestra la fórmula de
todos los coeficientes desde la recurrencia de contracción ya construida.
El signo exterior del residuo es importante:

\[
D(z)=\operatorname {Res}_t\left(K_n^+H(t)B(z)-K_n^-B(z)H(t)\right).
\]

Su coeficiente de exponente `k` es

\[
D_k=\sum_{a\ge0}\binom{a+n}{n}H_{a+n}B_{k-a}
 +(-1)^n\sum_{a\ge0}\binom{a+n}{n}B_{k+a+n+1}H_{-a-1}.
\]

Por tanto, coincide exactamente con `normalCoefficient o i n B k`:
el primer sumando es `creationTerm`, y el segundo `annihilationTerm`.
`LatticeNormalProductDerivativeBridge` ya identifica ambas partes con la
derivada dividida por `n!`, sin cambiar signos, índices ni normalización.
`LatticeResidueProducts.heisenberg_residueField` es el puerto de igualdad
de campos, no sólo una igualdad de unos pocos coeficientes.

## Finitud antes de reorganizar

Todas las expresiones se interpretan sobre un vector fijo `v` y unos
exponentes de salida fijos. No se postula convergencia analítica.

En el primer sumando, `B_(k-a) v` se anula para `a` suficientemente grande,
por el límite inferior de Laurent de `B` sobre `v`. En el segundo,
`H_(-a-1) v` se anula para `a` suficientemente grande. En una composición
con `C_l`, el mismo argumento se aplica al vector fijo `C_l v`. Cuando
`C_l` está a la izquierda, se aplica después de una suma de soporte finito.

Multiplicar por cualquiera de los polinomios usados abajo sólo produce
finitas traslaciones de los índices. Una unión finita de esos soportes
sigue siendo finita. Así están justificadas la distribución de los
polinomios, la extracción de residuos, la aplicación de un operador lineal
a la suma y la reagrupación de términos.

No se afirma que un producto arbitrario de distribuciones formales
multivariables exista. Sólo se utilizan las expansiones ordenadas para
las que acaba de darse el argumento puntual de soporte finito.

## Dos anuladores del mismo integrando

Introduzcamos el integrando del conmutador

\[
F(t,z,w)=
K_n^+\bigl(HBC-CHB\bigr)
-K_n^-\bigl(BHC-CBH\bigr),
\]

donde el orden de las letras indica composición, con variables `t,z,w`
respectivamente. Su residuo en `t` es `[D(z),C(w)]`.

Pongamos `F_q=(z-w)^q F`. Hay dos anuladores efectivos.

**Primer anulador.** La localidad B–C permite intercambiar `B` y `C`
después del factor `(z-w)^q`. La expresión restante se reorganiza en
`K_n^+ [H,C]B - K_n^- B[H,C]`, con ese factor conservado. Por localidad
H–C,

\[
(t-w)^p F_q=0.
\]

**Segundo anulador.** Las identidades de núcleo ya compiladas dan

\[
(t-z)^{s+n+1}K_n^+=(t-z)^s
=(t-z)^{s+n+1}K_n^-.
\]

Tras ese factor, las dos expresiones se reúnen exactamente en
`(z-w)^q (t-z)^s [[H,B],C]`, que se anula por localidad H–B. Por tanto,

\[
(t-z)^{s+n+1}F_q=0.
\]

La identidad no presupone que los dos núcleos sean iguales antes de
limpiar el polo. Su diferencia antes de ese paso es precisamente lo que
el cálculo conserva.

## Paso binomial y orden final

En el espacio de coeficientes triples sean `X`, `Y`, `Z` las operaciones
de multiplicación por `t-w`, `t-z`, `z-w`, respectivamente. Son
endomorfismos lineales de desplazamiento; `X` e `Y` conmutan y `Z=X-Y`.

Si `X^p u=0` y `Y^m u=0`, la expansión binomial prueba

\[
(X-Y)^{p+m-1}u=0.
\]

En efecto, en cada término `X^j (-Y)^(p+m-1-j) u`, o bien `j≥p`, o bien
`p+m-1-j≥m`. La conmutación permite aplicar el anulador pertinente al
mismo vector `u`. No se exige nilpotencia global de `X` o de `Y`.

Aplicando esto a `u=F_q` y `m=s+n+1` obtenemos

\[
(z-w)^{p+s+n}F_q=0,
\qquad
(z-w)^{p+q+s+n}F=0.
\]

Extraer el coeficiente `t^-1` conmuta con los desplazamientos en `z,w`.
Luego

\[
(z-w)^{p+q+s+n}[D(z),C(w)]=0,
\]

que es el enunciado.

## Correspondencia exacta con los módulos Lean

`LatticeDongKernel.lean` prueba siete declaraciones sobre los núcleos:
coeficientes de ambos dominios, signo, limpieza del polo reteniendo el
factor de localidad y separación de los órdenes. Su recibo es
`kernel_build/VERIFICATION.json`.

`LatticeDongBinomial.lean` realiza los endomorfismos `firstThird`,
`firstSecond`, `secondThird` sobre `ℤ → ℤ → ℤ → V`, el residuo como
extracción en `-1` y el paso binomial sobre un vector. Su declaración
`dong_residue_bound` requiere las dos anulaciones del **mismo** integrando
y concluye el orden `p+q+s+n`. Esas hipótesis son el lugar preciso donde
se insertan las tres localidades de los campos reales; no se presentan
como si ya estuviesen descargadas por ese lema.

En el corte inicial, el ensamblaje restante para un teorema Lean de clausura
consiste en construir `F` a partir de las expansiones ordenadas, identificar
su residuo con el conmutador de `residueField`, y probar sus dos anuladores
usando las localizaciones efectivas. No requiere un nuevo registro, un
nuevo retículo, ni una hipótesis de Jacobi o FLM.

La parte algebraica de ambos anuladores está ahora compilada en
`LatticeTripleLocality.lean`: `rawLeft_annihilated` y
`rawRight_annihilated` utilizan sólo las localidades A–C y B–C;
`rawDifference_annihilated` utiliza sólo la localidad A–B y la identidad
explícita con el doble conmutador. Sus versiones vectoriales conmutan la
evaluación con las potencias de los tres desplazamientos. El recibo
`triple_build/VERIFICATION.json` verifica 16 declaraciones. La composición
con las convoluciones ordenadas de los núcleos es un paso separado: no se
confunde la finitud puntual en cada vector con un soporte finito uniforme
de todos los endomorfismos.

## Ensamblaje completado — 21 de septiembre de 2026

La continuación descarga ya las dos anulaciones sobre el integrando real.
`LatticeDongIntegrand.integrand_residue_locality` compone los campos y sus
cotas unilaterales; `LatticeResidueConvolution.residue_convolution_commutator`
identifica el residuo con el conmutador efectivo. El resultado
`LatticeDongLocality.residueField_localAt` sólo recibe las tres localidades
originales, y `normalField_localAt` lo transporta mediante la igualdad
`heisenberg_residueField`. No recibe la conclusión como hipótesis.

La inducción de `LatticeDescendantLocality` y la extensión lineal prueban
`stateField_local` sobre todo el portador. El adaptador
`SelectedDescendantLocality.selected_fields_local` usa literalmente el
origen y el mapa Y anteriores. El recibo integrado
`../locality_closed_results/VERIFICATION.json`, de SHA-256
`867e422b5b95948f1ec34de21f73f61bb213f059c0ea521e9b9f7f133d60d05d`,
confirma las 160 declaraciones públicas del cierre. La lectura independiente
de los once módulos coincidió con las fuentes y los objetos del recibo.

## Referencia posterior

La cota coincide con el lema 27 de Michael Tuite, *Vertex Algebras According
to Isaac Newton*, pp. 13–14: para producto residual de índice `r`, el orden
suficiente es la suma de los tres órdenes menos `r+1`. Aquí `r=-n-1`.
Esta referencia documenta procedencia clásica; no es un axioma del código:
<https://arxiv.org/pdf/1702.02902>.
