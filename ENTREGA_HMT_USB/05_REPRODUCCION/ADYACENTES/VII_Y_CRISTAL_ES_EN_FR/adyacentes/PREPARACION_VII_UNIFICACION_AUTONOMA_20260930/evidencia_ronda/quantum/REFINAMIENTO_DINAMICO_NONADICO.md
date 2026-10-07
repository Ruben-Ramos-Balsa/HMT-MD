# Refinamiento nonádico de una evolución acoplada: norma temporal y límite

## 1. Objeto recibido y construcción añadida

Se conserva APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. Las holonomías de las fibras, sus hojas, orientación y archivo son salidas de esa cadena. La escala de acción positiva ℏ y la velocidad constitutiva c se reciben de sus lectores anteriores, no de valores metrológicos. Los transportes internos pueden actuar conjuntamente sobre los índices geométricos, de color y electrodébiles ya construidos.

Esta nota añade una realización dinámica de ruta. El reconocimiento convencional posterior es un operador autoadjunto sobre un intervalo, obtenido como límite de sus subdivisiones nonádicas. No identifica un intervalo con el espacio-tiempo completo ni sustituye las ecuaciones gravitatorias por una red arbitraria.

El antecedente efectivo es la diferencia de corona `D₉f(a)=f(t(a))−Uₐf(s(a))`, su energía `D₉*WD₉` y la conservación de memoria por Schur, en:

- `VIII_ES/fuentes_conservadas/02_dinamica_tres_hojas.tex`, secciones «Corona nonádica y energía torsional» y «Reducción de Feshbach–Schur»;
- `II_ES/sections/gravedad_rigidez_20260926.tex`, secciones «Memoria dinámica y norma temporal inducida» y «Refinamiento, dominios espectrales y alcance»;
- la composición completa 8:1 en `VII_ES/manuscrito/desarrollos/restitucion_operatoria.tex`.

Las tres rutas anteriores pertenecen a `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`. Las pruebas nuevas de esta nota no se atribuyen literalmente a esos propietarios.

## 2. Energía y norma sobre el mismo refinamiento

Sea una ruta con N=9^m subtramos y transportes unitarios U₁,…,U_N sobre una fibra finita E. Se conserva su producto ordenado T=U_N⋯U₁. Escribimos P₀=I, P_j=U_j⋯U₁ y v_j=P_j* f_j. Esta descomposición usa los transportes completos; no borra los registros que los produjeron. El refinamiento sustituye conjuntamente cada tramo por sus nueve subtramos, con producto igual al transporte anterior.

En la coordenada de ruta s∈[0,1], la energía es

\[
 q_N(f)=N\sum_{j=1}^{N}\|f_j-U_jf_{j-1}\|^2
       =N\sum_{j=1}^{N}\|v_j-v_{j-1}\|^2.
\]

Para incorporar la evolución, se declara explícitamente la realización temporal: cada v se interpola linealmente en los subtramos, y se utiliza su norma L² exacta. Resulta

\[
 m_N(v)=\frac1{3N}\sum_{j=1}^{N}
 \bigl(\|v_{j-1}\|^2+\|v_j\|^2+
       \operatorname{Re}\langle v_{j-1},v_j\rangle\bigr).
 \tag{1}
\]

El bloque local de la matriz de norma es `(1/(6N)) [[2I,I],[I,2I]]`. No se usa la suma no normalizada de las normas nodales como si fuera la misma magnitud. La integración uniforme de esta coordenada es una regla explícita de esta realización; no se identifica con la medida areal–volumétrica de Parry ni con una consecuencia automática del mero cardinal nueve.

**Proposición 1.** La inclusión J_N que representa la misma función lineal por tramos en la malla de 9N subtramos (9N+1 nodos) conserva exactamente energía y norma:

\[
 J_N^*L_{9N}J_N=L_N,\qquad J_N^*M_{9N}J_N=M_N.
 \tag{2}
\]

**Prueba.** En cada tramo original la derivada de la función interpolada es constante; sumar las nueve integrales de su norma cuadrada reproduce la integral anterior. Lo mismo ocurre con la integral exacta de la norma cuadrada de la función. Las identidades se obtienen por polarización. ∎

La evolución finita se escribe `iℏ M_N ∂t v=E₀ L_N v`, con E₀>0 recibido de la sección dimensional. En el producto M_N, el generador es autoadjunto; en coordenadas ortonormales es `E₀ M_N^{-1/2} L_N M_N^{-1/2}`. Esto no afirma que los generadores finitos se entrelacen exactamente por J_N: (2) conserva formas y normas, y el paso a la evolución se demuestra mediante resolventes en §4.

## 3. Memoria temporal exacta de la frontera

Fijemos f₀=a, f_N=b. La extensión de mínima energía, en el marco transportado, es

\[
 v_j=(1-j/N)a+(j/N)T^*b.
\]

La energía y la norma de esa misma extensión dan

\[
 K_0=\begin{pmatrix}I&-T^*\\-T&I\end{pmatrix},\qquad
 Z=\begin{pmatrix}\frac13I&\frac16T^*\\
                   \frac16T&\frac13I\end{pmatrix}.
 \tag{3}
\]

**Prueba.** La energía de la extensión es `∥T*b−a∥²`. Para la norma, integrar `∥(1−s)a+sT*b∥²`: las integrales de `(1−s)²` y `s²` son 1/3, y la de `s(1−s)` es 1/6. La interpolación representa exactamente esta función para cada N, por lo que el resultado no depende del nivel. ∎

La eliminación dinámica se hace sobre `L_N−z M_N`, no sólo sobre L_N. Su complemento de Schur de frontera satisface

\[
 K_N(z)=K_0-zZ+O(z^2).
 \tag{4}
\]

La derivada respecto de z de la forma estacionaria es menos la norma de su extensión estática; las derivadas de la extensión se cancelan por estacionariedad. Ésta es la prueba de (4). Los términos superiores conservan la memoria dinámica de los tramos interiores.

Para comparar con una lectura nodal distinta, la suma sin normalizar de todas las normas nodales da, en N=9, diagonales 95/27 y términos cruzados 40/27. Esos números son correctos para esa lectura, pero no son los coeficientes de (1). Con cuadratura trapecial normalizada se obtiene en cambio

\[
 Z_N^{trap}=\begin{pmatrix}
 (\frac13+\frac1{6N^2})I&(\frac16-\frac1{6N^2})T^*\\
 (\frac16-\frac1{6N^2})T&(\frac13+\frac1{6N^2})I
 \end{pmatrix}\longrightarrow Z.
\]

La norma exacta (1) conserva ya Z en todos los niveles. Declarar la norma utilizada evita confundir tres realizaciones temporales diferentes.

## 4. Límite dinámico construido

El caso sin potencial permite escribir el límite sin invocar una analogía. Para z=−κ², κ>0, y N>κ/√6, sean

\[
 a_N=N-\frac{\kappa^2}{6N},\qquad
 \cosh\eta_N=\frac{N+\kappa^2/(3N)}{N-\kappa^2/(6N)}.
\]

La ecuación interior de `L_N+κ²M_N` es

\[
 -a_N v_{j-1}+2a_N\cosh\eta_N\,v_j-a_N v_{j+1}=0.
\]

Con las dos condiciones de frontera, la solución es

\[
 v_j=\frac{\sinh((N-j)\eta_N)}{\sinh(N\eta_N)}a
      +\frac{\sinh(j\eta_N)}{\sinh(N\eta_N)}T^*b.
\]

Sustituirla en las filas de frontera da el complemento dinámico exacto

\[
 K_N(-\kappa^2)=\frac{a_N\sinh\eta_N}{\sinh(N\eta_N)}
 \begin{pmatrix}\cosh(N\eta_N)I&-T^*\\-T&\cosh(N\eta_N)I\end{pmatrix}.
 \tag{5}
\]

Puesto que `cosh η_N=1+κ²/(2N²)+O(N^{-4})`, se tiene `Nη_N→κ` y `a_N sinh η_N→κ`. Por tanto, en norma matricial,

\[
 \boxed{K_N(-\kappa^2)\longrightarrow
 \frac{\kappa}{\sinh\kappa}
 \begin{pmatrix}\cosh\kappa I&-T^*\\-T&\cosh\kappa I\end{pmatrix}.}
 \tag{6}
\]

El lado derecho es la respuesta de frontera del operador covariante `−D_s²+κ²` de la misma ruta. Su desarrollo en κ² conserva exactamente los dos primeros coeficientes (3). No se ha deducido el límite a partir de un número finito de verificaciones: (5) y la expansión de cosh lo demuestran para toda la sucesión nonádica.

### Potenciales y pesos matriciales acoplados

La prueba se extiende a una clase precisa. Sobre una ruta, o un grafo métrico finito con condiciones de vértice fijadas, sea

\[
 q(u,v)=\langle D_su,W D_sv\rangle_{L^2}
              +\langle u,Vv\rangle_{L^2},
 \qquad w_-I\le W\le w_+I,\quad V=V^*,\quad\|V\|<\infty,
 \tag{7}
\]

con `0<w_-≤w_+<∞`. Los operadores pueden actuar en la misma fibra de índices geométricos e internos; W puede ser un operador acotado positivo sobre el espacio de residuos, conservando sus términos cruzados. Se fija un transporte unitario que identifica D_s con la derivada en cada arista. El dominio es el H¹ covariante definido en ese marco transportado. Las condiciones de vértice son relaciones lineales cerradas entre las trazas de los extremos, y los subespacios lineales por tramos son conformes a esas relaciones. No se imponen condiciones arbitrarias sobre derivadas puntuales en un dominio H¹. No se introduce una conexión no unitaria como si preservase ese producto positivo.

**Teorema 2.** La forma (7) es cerrada y acotada inferiormente. Sus restricciones a los espacios lineales por tramos de mallas N=9^m, con norma L² exacta, determinan generadores autoadjuntos. Sus resolventes de Galerkin convergen fuertemente al del generador de (7).

**Prueba.** Elegir λ>∥V∥ hace `q+λ⟨·,·⟩` coerciva y continua en H¹; su norma es equivalente a la de H¹, luego la forma es cerrada. Para f∈L², la ecuación variacional

`q(u,v)+λ⟨u,v⟩=⟨f,v⟩`

tiene solución única. Su solución u_N en el subespacio refinado cumple ortogonalidad de Galerkin. Continuidad y coercividad dan

`∥u−u_N∥_{H¹} ≤ (C/c) inf_{v_N}∥u−v_N∥_{H¹}`.

Las funciones lineales por tramos en las mallas anidadas son densas en ese dominio H¹: primero se aproxima por funciones suaves compatibles con las trazas y después se interpola conservando sus valores de extremo. El término derecho tiende a cero. Así, `(H_N+λ)^{-1}P_N f→(H+λ)^{-1}f` en L², donde P_N es la proyección L². Extendiendo H_N por cero sobre el complemento de su subespacio, P_N→I y la convergencia anterior dan convergencia fuerte de resolventes en el espacio común. De ella resulta `exp(−itH_N)P_N f→exp(−itH)f`, uniformemente para t en compactos. No se postula un entrelazamiento finito que (2) no demuestra. ∎

Este teorema trata una realización de ruta o grafo métrico con fibra y condiciones fijadas. Para incluir campos cuánticos con ocupación sin corte, geometría arbitraria o el espacio-tiempo completo, sus formas y cotas uniformes deben entrar efectivamente en (7) o en una extensión demostrada; no quedan incorporados por renombrar W o V.

## 5. Relación con la lectura gravitatoria y las constantes

En el sector positivo de un carácter conjunto X, el propietario de rigidez ya fija

\[
 Y=\mathsf U X\mathsf U^*,\quad
 L=\frac{5759}{23040}\alpha^{16}L_*,\quad
 E_L=\frac{\hbar c}{L},\quad
 H_X=E_LY,\quad R_X=LY,\quad\Lambda_X=LY^{-1}.
\]

La sustitución da una relación **operatoria**, no sólo una coincidencia numérica:

\[
 R_X=\frac{L^2}{\hbar c}H_X=\frac{G}{c^4}H_X,\qquad
 H_X\Lambda_X=\hbar cI,\qquad G=\frac{c^3L^2}{\hbar}.
\]

Si H_X se realiza mediante la forma acoplada anterior, su respuesta radial recibe todos los términos de ese mismo operador. Para `R_X=χH_X`, el Schur dinámico conserva `K_R(χz)=χK_H(z)`: hay que escalar también el parámetro espectral. La identidad inversa, en un sector donde H_X tenga inverso acotado, se transmite como `H_eff (J*Λ_XJ)=ℏcI`, comprimiendo Λ_X y tomando el Schur estático de H_X. No se aplica Schur independientemente a los dos inversos. Por ejemplo, H=[[2,1],[1,2]] tiene Schur 3/2, mientras Schur(H^-1)=1/2; su producto no es uno. La compresión de H^-1 es 2/3 y sí da la identidad. Para un inverso no acotado se conserva su dominio espectral y no se extiende la fórmula a vectores ajenos a él. Esta composición no demuestra que una realización arbitraria de (7) sea el carácter seleccionado por HMT, ni identifica el radio reducido con el tensor de Einstein. Son mapas de tipos distintos y la prueba no los intercambia.

## 6. Comprobación y resultado

`verificar_refinamiento_dinamico.py` comprueba las identidades exactas de energía y norma bajo la inclusión nonádica, los coeficientes de memoria, (5) en matrices pequeñas y la convergencia numérica de (6). Las pruebas generales están en el texto; el cálculo no las sustituye.

El resultado añadido es un paso al límite dinámico efectivo para la clase (7), con conservación explícita de la norma y de la memoria de frontera. No se presenta como la prueba de una teoría cuántica completa de las cuatro interacciones. Su aportación a esa tarea es reemplazar una inferencia incorrecta —«se conserva la energía, luego se conserva la evolución»— por un resolvente construido y una prueba de convergencia.
