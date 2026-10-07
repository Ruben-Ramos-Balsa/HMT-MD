# Deformaciones espaciales del operador espinorial: identidad local completa

Fecha: 29 de septiembre de 2026. Desarrollo añadido al acumulado, sin modificar
ningún manuscrito sellado. Procedencia: formalización reunida de la realización
espinorial recibida; no nueva generación de sus constantes ni del módulo de
Clifford.

## 1. Antecedente y objeto que se calcula

La cadena permanece APP → TRIT → TPK → estado enriquecido → estructura discreta
conjunta del continuo. APP aporta las rutas y sus hojas; TRIT conserva régimen
y orientación; TPK transporta la ruta, el marco, la memoria y su elevación de
espín. La doble proyección se conserva antes de la realización: ni la carta
real ni el módulo espinorial reemplazan el estado enriquecido. Las constantes
son salidas HMT anteriores, recibidas por esta realización. El reconocimiento
convencional posterior es el cálculo de un operador de Dirac en una hoja
espacial, no una selección retrospectiva de las semillas.

Propietarios leídos en
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`:

- `VIII_ES/manuscrito/30d_realizacion_geometrica.tex`, §§ pantalla y conexión:
  `e_m=J_scr,m beta_m`, igualdad de holonomías, conservación del levantamiento
  de espín que la representación vectorial no distingue y realización suave
  con cotétrada no degenerada.
- `VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex`, líneas 50–119:
  módulo de Clifford explícito, conexión en esa representación y acción
  espinorial afín. Las líneas 171–221 y 229–315 separan la eliminación
  torsional y el operador cuártico de corriente.
- `INTEGRACION_MATEMATICA.md`, §5.1, y
  `HAMILTONIANO_FINITO_HIGGS_FOCK.md`: mapa Yukawa entre las dos
  representaciones quirales, con su adjunto y equivariancia.

Se trabaja en una hoja espacial suave orientada, con métrica positiva `g`,
módulo espinorial recibido y conexión unitaria Clifford-compatible. La
conexión intrínseca usada en la fórmula de Dirac es la de Levi–Civita más
la conexión interna; cualquier contorsión remanente se declara como término
adicional y no se elimina dos veces. Tomamos una hoja compacta sin borde; la
identidad diferencial también vale para secciones de soporte compacto en una
hoja abierta. No se introducen condiciones de borde implícitas.

En la convención del propietario, sean

\[
 \alpha^j=-g^0g^j,\qquad \beta=-i g^0,\qquad
 \Gamma_5=i g^0g^1g^2g^3.
\]

Las matrices satisfacen

\[
 \{\alpha^i,\alpha^j\}=2\delta^{ij},\quad
 \{\beta,\alpha^j\}=0,\quad
 [\Gamma_5,\alpha^j]=0,\quad
 \{\Gamma_5,\beta\}=0.
\tag{1}
\]

En un marco general se escribe `α(ξ)` para la multiplicación Clifford de
una covector espacial, de modo que
`{α(ξ),α(η)}=2g^{-1}(ξ,η)I`. El coeficiente `a=ℏ_int c_int` se recibe de
la construcción anterior. El operador es

\[
 H=-ia\alpha^j\nabla_j+B,\qquad
 B^*=B,\qquad \{B,\alpha(\xi)\}=0.
\tag{2}
\]

El término másico `B=βmc²` cumple esta condición, incluso con masa suave
dependiente de la posición. También la cumple el bloque Yukawa espinorial
escalar con su adjunto, siempre que se conserven ambos espacios quirales.
La matriz de sabor puede ser no diagonal. No se presupone `[H,Γ5]=0` en
presencia de masa: conservar la estructura quiral no significa borrar su
acoplamiento.

## 2. Teorema: dos lapsos espaciales arbitrarios

Para cualesquiera funciones reales suaves `N,M`, sean

\[
 H_N=\tfrac12(NH+HN),\qquad
 v=N\operatorname{grad}M-M\operatorname{grad}N.
\tag{3}
\]

En el núcleo común de secciones suaves se cumple la identidad exacta

\[
 \boxed{[H_N,H_M]
 =-a^2\left(
 \nabla_v+\tfrac12\operatorname{div}v
 +\tfrac14[\alpha(dN),\alpha(dM)]\right).}
\tag{4}
\]

No se exige que los lapsos sean constantes, homogéneos ni positivos. El
primer término es transporte tangencial con su corrección de densidad; el
segundo sumando matricial es una rotación espinorial local. Es un conmutador
de operadores diferenciales sobre un núcleo común, no una afirmación sobre
el producto de cualesquiera extensiones autoadjuntas.

### Demostración

Escribamos `d_N=[H,N]=−ia α(dN)`. Como `N,M` son multiplicadores escalares,
conmutan con `d_N,d_M`. La expansión de (3) da, sin usar todavía Clifford,

\[
 [H_N,H_M]
 =\tfrac12N\{H,d_M\}-\tfrac12M\{H,d_N\}
   +\tfrac14[d_N,d_M].
\tag{5}
\]

La compatibilidad de la conexión y la simetría del Hessiano implican

\[
 \{H,d_M\}
 =-a^2\bigl(2\nabla_{\operatorname{grad}M}+\Delta M\bigr).
\tag{6}
\]

En efecto, al aplicar el anticomutador a una sección, los términos con una
derivada de la sección se contraen mediante
`α^j α^k+α^k α^j=2g^{jk}I`. El término sin derivada es la contracción del
Hessiano de `M`; su parte antisimétrica se anula. La contribución de `B`
es `−ia{B,α(dM)}=0`. No aparece una derivada de `B`, pues `d_M` ya es un
operador de orden cero.

Al sustituir (6) en (5), se usa

\[
 \operatorname{div}v=N\Delta M-M\Delta N,
 \qquad [d_N,d_M]=-a^2[\alpha(dN),\alpha(dM)],
\]

y se obtiene (4). Esto prueba el enunciado para cada pareja de lapsos
suaves, sin expansión perturbativa de su amplitud. ∎

## 3. Qué conserva la composición de las dos quiralidades

En la parte cinética `D=−ia α^j∇_j`, la conexión y `α` conservan `Γ5`,
de modo que `[D,Γ5]=0`. Por tanto (4) se restringe a cada sector quiral
cuando `B=0`. Si `B` mezcla las dos quiralidades, el espacio correcto es
su suma con el mapa `B` completo. El conmutador (4) conserva la graduación
aunque los factores `H_N` no la conserven por separado: la cancelación de
los términos másicos se ha demostrado en (5)–(6), no supuesto.

La corriente de torsión es un operador cuártico después de la eliminación
de la contorsión. No es un nuevo `B` lineal de (2). Su tratamiento en Fock
no se obtiene llamándolo «masa efectiva» dentro de esta prueba.

## 4. Elevación a Fock algebraico y su alcance

Sea `F_fin(D)` el espacio de vectores con número finito de partículas y
componentes en productos antisimetrizados del núcleo suave `D`. Para un
operador `A` que conserva `D`, `dΓ(A)` actúa como la suma de `A` en cada
factor. En ese núcleo se demuestra directamente

\[
 [d\Gamma(A),d\Gamma(B)]=d\Gamma([A,B]).
\tag{7}
\]

Los términos que actúan sobre factores diferentes conmutan; los que actúan
sobre el mismo factor dan el conmutador de un cuerpo. Así (4) pasa a este
Fock sin término central. Esto utiliza la representación de Fock indicada,
con vacío de partículas y núcleo algebraico. No cambia silenciosamente a
una representación de mar de Dirac, un determinante fermiónico o un vacío
interactuante renormalizado. (7) tampoco trata por sí sola una interacción
local cuártica sin regulador.

## 5. Falsador y operación que no se puede omitir

Si se añade un término `V` que no anticomuta con Clifford, la identidad
tiene el término adicional exacto

\[
 \mathcal E_V(N,M)
 =-\frac{ia}{2}\left(
 N\{V,\alpha(dM)\}-M\{V,\alpha(dN)\}\right).
\tag{8}
\]

Para `V=v_0 I`, se reduce a
`−ia v_0 α(NdM−MdN)`, generalmente no nulo. Este caso impide suprimir el
término gauge temporal o una interacción incompatible mientras se invoca
(4). Su compensación, si procede, debe venir de la restricción y conexión
correspondientes de la misma acción, no de una igualdad entre constantes.

El verificador `verificar_conmutador_espacial.py` utiliza las matrices
explícitas (1), jets polinómicos en tres coordenadas, masas variables y
lapsos no homogéneos. Comprueba (4), (8), la cancelación másica y la paridad
quiral mediante aritmética racional compleja. La prueba para funciones
suaves arbitrarias es (5)–(6); los ejemplos exactos son controles negativos
y de implementación, no su sustituto.

## 6. Relación con la exigencia global

Esta identidad permite calcular un componente real del álgebra espacial:
no reemplaza `N(x)` por el lapso de un único reloj. La nota compañera
`DEFORMACIONES_ESPACIALES_Y_QUIRALIDAD.md` trata su naturalidad y el límite
de cortes espaciales sobre el núcleo suave. El resultado se apoya en la
realización espinorial ya documentada, con su cotétrada y sus coeficientes
recibidos.

La identidad (4) no demuestra que este operador de materia sea, por sí
solo, la restricción Hamiltoniana total de la geometría dinámica. Esa
restricción contiene también la parte geométrica, las restricciones de
Gauss y las interacciones. Se conservan (4) y su límite como resultados
positivos precisos; no se los denomina una prueba del cierre conjunto de
las cuatro interacciones.
