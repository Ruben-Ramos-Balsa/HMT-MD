# Eliminación coerciva de los detalles y residuo finito de una ventana

11 de septiembre de 2026. Desarrollo focal para integración por el editor único.
No modifica los manuscritos I–VIII ni sus PDF.

## 1. Base, dominio y resultado obtenido

Se utilizan las columnas completas ya construidas desde la aritmética nativa
de APP, el estado orientado TRIT, las operaciones y la memoria TPK, y la
estructura conjunta del continuo. El producto nativo publica irreducibles y
potencias; sus longitudes y pesos alimentan después los lectores primo,
gamma y polar. La coordenada interna de π y el lector racional de la parte
finita de Euler–Mascheroni intervienen después de esa publicación. Ningún
cero, valor buscado del funcional o constante metrológica selecciona estas
operaciones.

Esta nota toma como antecedentes el capítulo 03 del VIII, §§2–3 y §§12–15.
Los §§12–15 se han leído íntegramente para esta tarea; la identidad de las
columnas y sus dominios se ha cotejado en §§2–3. La construcción conjunta
del continuo permanece como antecedente común: no se sustituye por esta
descomposición funcional, ni sus cinco construcciones por cinco módulos.

La operación nueva aquí reunida es la eliminación exacta del espacio
infinito de detalles mediante su forma coerciva. Produce una matriz finita
con todas las correcciones de acoplamiento, no solamente una matriz de
medias. Además se cierra un caso concreto:

> Para toda función del cierre de
> \(C_c^\infty((-1/18,1/18))\) en la norma conjunta de los lectores,
> \[
> \mathscr W(f,f)\geq\frac12\|f\|_2^2.
> \]
> La misma afirmación vale en cualquier intervalo trasladado de longitud
> \(1/9\), y en todos sus refinamientos interiores nonádicos.

La ventana completa tiene longitud \(1/9>0.085626\ldots\), el extremo
del criterio basal anterior. No contiene una traslación prima activa,
pues \(1/9<\log2\). Ese límite del ejemplo se mantiene explícito.

**Procedencia.** Arquitectura autoral y lectores: preexistentes. Coercividad
de detalles: resultado recuperado del teorema 23, conservando una estimación
intermedia más fuerte que su cota logarítmica abreviada. Ensamblaje de Schur,
certificación residual y prueba del intervalo \(1/9\): formalización y
certificado añadidos en esta nota; no se atribuye novedad histórica global.

## 2. Partición, medias celulares y detalles

Fíjese \(R>0\), \(I_R=(-R/2,R/2)\) y \(H_R=L^2(I_R)\), con extensión
por cero. Sea \(V_R\) el dominio cerrado conjunto de los lectores del
capítulo 03. Equivalentemente, su norma puede tomarse como
\[
\|f\|_{V_R}^2=\|f\|_2^2+Q_\Gamma(f),\qquad
Q_\Gamma(f)=\int_0^\infty\mu(a)\|(I-T_a)f\|_2^2\,da,
\quad \mu(a)=\frac{e^{-a/2}}{1-e^{-2a}}.
\]
Los canales primos y polares son acotados en cada ventana fijada.
La forma gamma es cerrada: es la forma de un multiplicador positivo
en Fourier, restringida al subespacio de funciones soportadas en la
ventana; equivalentemente se verifica por convergencia en la integral
directa de diferencias. La forma completa es una perturbación acotada
de ella y define un operador autoadjunto semiacotado \(L_R\).

Particiónese \(I_R\) en intervalos contiguos \(I_j=(\ell_j,r_j)\), con
longitudes \(h_j\leq h\), y póngase
\[
u_j=h_j^{-1/2}\mathbf1_{I_j},\qquad
Ua=\sum_{j=1}^M a_j u_j,\qquad P=UU^*,\quad Q=I-P.
\]
En la última suma, \(a=(a_1,\ldots,a_M)\) es el vector de coeficientes;
los extremos \(\ell_j,r_j\) sólo se emplean al definir \(I_j\).

Los indicadores pertenecen a \(V_R\): su energía gamma se controla por
\(\|(I-T_a)u_j\|_2^2=2\min(|a|/h_j,1)\). Por ello \(P\) actúa
continuamente en \(V_R\), y todo \(f\in V_R\) tiene descomposición única
\[
f=Ua+d,\qquad a_j=\langle f,u_j\rangle,\qquad
d\in V_D:=V_R\cap QH_R.
\]
Aquí \(d\) tiene integral nula en cada celda. El espacio \(V_D\) es
cerrado en la norma de forma y denso en \(QH_R\).

El teorema 23 da una cota \(\mathscr W_R(d,d)\geq\eta\|d\|_2^2\)
si se elige una partición suficientemente fina. Se puede emplear su
umbral logarítmico publicado, o conservar la estimación intermedia exacta
\[
\eta_N(h,R)=4\sum_{n=0}^N\frac1{4n+1}
-\frac{h^2(N+1)(2N+1)}{\pi^2}
+c_\Gamma-2\sum_{k\log p\leq R}(\log p)p^{-k/2}-\beta_R,
\quad \beta_R=2\sinh(R/2)-R. \tag{S1}
\]
La prueba de esa estimación consta en el propietario: se retienen
\(N+1\) energías gamma positivas y se aplica Dirichlet a la primitiva
celular. No hace falta sustituir la suma armónica por su integral inferior.
Para el uso numérico de esta nota se comprueba además
\((2N+1/2)h<\pi\), de modo que cada cota gamma retenida es no negativa.

## 3. El complemento de Schur exacto tiene tamaño finito

Sea \(D\) el operador asociado a la restricción de la forma a \(V_D\).
Si \(\eta>0\), entonces \(D\geq\eta I\) sobre \(QH_R\),
\(D^{-1}\) existe y \(\|D^{-1}\|\leq\eta^{-1}\).
No se presume que \(L_R\) conserve el espacio de detalles.

Los indicadores pertenecen también al dominio operatorio de \(L_R\).
La expresión de su imagen gamma se da en la sección siguiente: sólo
tiene singularidades logarítmicas, que pertenecen a \(L^2(I_R)\).
Esto permite definir, sin extender indebidamente un funcional de forma,
\[
A=U^*L_RU,\qquad B=QL_RU:\mathbb C^M\longrightarrow QH_R.
\]
El producto interior es lineal en la primera variable, como en el
manuscrito. Las matrices se escriben de modo que
\(\mathscr W_R(Ua,Ua)=a^*Aa\). La identidad de bloques es
\[
\mathscr W_R(Ua+d,Ua+d)
=a^*Aa+2\operatorname{Re}\langle Ba,d\rangle
+\mathfrak d[d,d],
\]
donde \(\mathfrak d\) es la forma cerrada de \(D\).

**Teorema S1.** La matriz
\[
S=A-B^*D^{-1}B \tag{S2}
\]
satisface la identidad exacta
\[
\boxed{\mathscr W_R(Ua+d,Ua+d)
=a^*Sa+
\mathfrak d[d+D^{-1}Ba,d+D^{-1}Ba].} \tag{S3}
\]
En particular, \(\mathscr W_R\geq0\) sobre \(V_R\) si y sólo si
\(S\succeq0\). Su índice negativo coincide con el de \(S\).

**Prueba.** Para \(z=D^{-1}Ba\in\operatorname{Dom}D\),
\(\mathfrak d[z,d]=\langle Ba,d\rangle\). Expandir el segundo término
de (S3) y usar \(\mathfrak d[z,z]=a^*B^*D^{-1}Ba\) da la igualdad.
La suficiencia es inmediata. Para la necesidad se elige
\(d=-D^{-1}Ba\). El cambio triangular \((a,d)\mapsto(a,d+D^{-1}Ba)\)
es invertible en \(\mathbb C^M\oplus V_D\). La segunda forma resultante
es positiva definida; las direcciones negativas son exactamente las de
la matriz finita. ∎

Este teorema convierte el índice finito del corolario 24 en una matriz
exacta. La matriz todavía contiene \(D^{-1}\): finitud de su tamaño no
significa que sus entradas ya estén calculadas. La sección siguiente
da una forma de encerrarlas con residuos controlados.

## 4. Imágenes explícitas y cotas certificables de las correcciones

Póngase \(M(x)=\int_x^\infty\mu(a)\,da\), para \(x>0\).
Para un indicador \(u=h^{-1/2}\mathbf1_{(a,b)}\), su imagen gamma,
restringida a \(I_R\), es casi en todas partes
\[
(L_\Gamma u)(x)=h^{-1/2}
\begin{cases}
M(x-a)+M(b-x),&a<x<b,\\
-M(a-x)+M(b-x),&x<a,\\
-M(x-b)+M(x-a),&x>b.
\end{cases} \tag{S4}
\]
La igualdad se obtiene integrando las dos traslaciones: dentro de la
celda queda una cola por cada extremo, y fuera queda la integral del
único intervalo de traslaciones que toca la celda. Puede probarse primero
con el regulador \(a_{\rm traslado}\geq\epsilon\); la convergencia en
\(L^2(I_R)\) de la expresión logarítmica justifica su límite débil de
forma. Las otras partes son
\[
L_{\rm primo}u=-\sum_{k\log p\leq R}w_{p,k}
M_R(T_{k\log p}+T_{-k\log p})u,
\]
\[
L_{\rm polar}u(x)=2\int_a^b h^{-1/2}\cosh((x-y)/2)\,dy,
\qquad L_Ru=L_\Gamma u+c_\Gamma u+L_{\rm primo}u+L_{\rm polar}u. \tag{S5}
\]
Todas las discontinuidades y singularidades de (S4)–(S5) están en una
lista finita de extremos y extremos trasladados por relojes publicados.
Así, \(A_{ij}\) y
\[
G_B=B^*B,\qquad (G_B)_{ij}=\langle Be_j,Be_i\rangle
\]
se calculan por integrales unidimensionales explícitas. En esta última
fórmula \(e_j\) denota el vector coordenado estándar de
\(\mathbb C^M\), no el indicador en \(H_R\).
La cota inicial es
\[
 A-\eta^{-1}G_B\preceq S\preceq A. \tag{S6}
\]
Es una desigualdad operatoria con los cruces conservados, no una
sustitución de \(G_B\) por sus entradas diagonales.

**Teorema S2. Certificación por residual.** Para cualquier operador
finito de aproximación \(Z:\mathbb C^M\to\operatorname{Dom}D\), defínanse
\[
E=B-DZ,\qquad C_Z=Z^*B+B^*Z-Z^*DZ.
\]
Entonces
\[
B^*D^{-1}B=C_Z+E^*D^{-1}E,
\]
y por tanto
\[
\boxed{A-C_Z-\eta^{-1}E^*E\preceq S\preceq A-C_Z.} \tag{S7}
\]
**Prueba.** Sustituir \(B=DZ+E\) y expandir el producto. Todos los
términos están definidos porque las columnas de \(Z\) pertenecen a
\(\operatorname{Dom}D\). La cota usa \(0<D^{-1}\leq\eta^{-1}I\). ∎

Una elección efectiva de \(Z\) consiste en resolver el sistema de
Galerkin sobre detalles escalonados de un refinamiento nonádico. Sus
columnas son combinaciones finitas de indicadores y tienen imágenes
(S4)–(S5), por lo que \(E\) y su Gram son integrables explícitos. El
sistema de Galerkin no se declara solución exacta: el término
\(\eta^{-1}E^*E\) conserva su error sobre el complemento infinito.

Para certificar esos integrales sin perder los extremos singulares,
se separa
\[
M(x)=-\tfrac12\log x+\log2+\tfrac\pi4+r(x),
\qquad r(0)=0,\quad r'(x)=\tfrac1{2x}-\mu(x). \tag{S8}
\]
En \(0<x\leq R\),
\[
-\tfrac14 e^{R/2}\leq r'(x)\leq\tfrac14,
\qquad |r'(x)|\leq\tfrac14e^{R/2}.
\]
En efecto, \(\mu(x)=e^{x/2}/(2\sinh x)\) y
\(x\leq\sinh x\leq xe^x\) dan
\(e^{-x/2}/(2x)\leq\mu(x)\leq e^{x/2}/(2x)\).
Las desigualdades \(1-e^{-y}\leq y\) y \(e^y-1\leq ye^y\)
prueban las cotas. No se afirma que \(r'\) tenga signo constante
en una ventana arbitrariamente grande.
Se integran analíticamente \(\log x\) y \(\log^2x\) en los pequeños
tramos de extremo; el resto \(r\) se acota por su constante de Lipschitz.
Fuera de los extremos se usan cuadraturas intervalares subdivididas y
la serie exponencial de \(M\). Por ejemplo,
\[
\int_0^\delta\log^2x\,dx
=\delta[(\log\delta)^2-2\log\delta+2].
\]
Los productos de dos singularidades en puntos distintos se tratan
separando sus vecindades; para un extremo compartido se usa la misma
integral cuadrática. Los intervalos resultantes se insertan en (S7) y
se verifica positividad mediante una descomposición \(LDL^*\) con
pivotes intervalares estrictamente positivos o una cota de perturbación
de una matriz racional. Queda así especificado un certificado finito
con control del complemento infinito; no se usa una malla sin cota de cola.

## 5. Certificado cerrado en la ventana completa de longitud 1/9

Tómese \(R=h=1/9\), una sola celda y \(u=R^{-1/2}\mathbf1_{I_R}\).
Es un intervalo completo, no nueve intervalos con huecos. La sección
de detalles es todo \(V_R\cap\{u\}^{\perp}\).

### 5.1. Margen del bloque infinito

En (S1) se toma \(N=13\). No hay términos primos porque
\(R<\log2\). Se obtiene
\[
\eta=4\sum_{n=0}^{13}\frac1{4n+1}
-\frac{(1/9)^2\,14\cdot27}{\pi^2}+c_\Gamma-\beta_{1/9}>1.
\tag{S9}
\]
El certificado intervalar da
\(1.00363976543713133046<\eta<1.00363976543713133048\).
La condición \((53/2)/9<\pi\) garantiza además la positividad de
cada cota gamma retenida. La suma se conserva; sustituirla por la
cota \(\log(1+4/h)-2/3\) perdería aquí el margen necesario.

### 5.2. Bloque de media

Dentro de la ventana, escribiendo \(x=R(t-1/2)\),
\[
L_Ru(x)=R^{-1/2}g(t),\quad
g(t)=c_\Gamma+M(Rt)+M(R(1-t))
+8\sinh(R/4)\cosh(R(t-1/2)/2).
\]
Por ello \(A=\int_0^1g(t)\,dt\) y \(\|B\|^2\) es la varianza
de \(g\) en el intervalo unidad. Tonelli aplicado a \(M\) da
\[
A=c_\Gamma+\frac2R\sum_{n=0}^\infty
\frac{1-e^{-(2n+1/2)R}}{(2n+1/2)^2}
+\frac{32}R\sinh^2(R/4). \tag{S10}
\]
Si se retienen los primeros \(L\) términos, la cola positiva es a lo
sumo \(\lambda_L^{-2}+(2\lambda_L)^{-1}\), con
\(\lambda_L=2L+1/2\). Se separa el primer término de la cola y se
acota el resto por la integral de una función decreciente. Para
\(L=1024\), el certificado produce
\[
0.9723307136651774<A<0.9767284617331572,
\qquad A>97/100. \tag{S11}
\]
No se necesita una aproximación más ajustada para la prueba.

### 5.3. Todo el acoplamiento media–detalle

En \(0<x\leq1/9\), la estimación de (S8) se mejora a
\[
-9/10\leq r'(x)\leq0.
\]
En efecto, para \(0<x\leq1/9\),
\[
\frac{\sinh x}{x}
=\sum_{k\geq0}\frac{x^{2k}}{(2k+1)!}
\leq\frac1{1-x^2}\leq1+\frac x2\leq e^{x/2}.
\]
La desigualdad intermedia equivale a \(1-2x-x^2\geq0\),
que vale en ese intervalo. Así \(\mu(x)\geq1/(2x)\).
Por otro lado,
\[
\mu(x)-\frac1{2x}\leq\frac{e^{x/2}-1}{2x}
\leq\frac14 e^{x/2}
\leq\frac1{4(1-1/18)}=\frac9{34}<\frac9{10}.
\]
Se conserva la cota \(9/10\), menos ajustada, usada por el certificado.
La función \(q(t)=r(Rt)+r(R(1-t))\) es simétrica respecto de
\(1/2\) y su constante de Lipschitz es a lo sumo \(9R/10\).
Su oscilación es a lo sumo \(9R/20=1/20\); por tanto su desviación
típica es a lo sumo \(1/40\). Esta última afirmación sigue de
\(\operatorname{Var}(X)\leq(\sup X-\inf X)^2/4\): restar el
punto medio del rango y usar que la media minimiza el error cuadrático.

La parte singular \(v(t)=-\tfrac12\log(t(1-t))\) tiene media 1 y
varianza \(1-\pi^2/12\). Para comprobarlo, se integran
\(\log t\), \(\log^2t\) y la serie positiva de
\(\log t\log(1-t)\), que da
\(\int_0^1\log t\log(1-t)\,dt=2-\sum_{n\geq1}n^{-2}\).
La identidad \(\sum n^{-2}=\pi^2/6\) puede obtenerse por Parseval
aplicado a la serie de senos de \(x\) en \((-\pi,\pi)\): sus
coeficientes son \(2(-1)^{n+1}/n\) y
\((1/\pi)\int_{-\pi}^{\pi}x^2dx=2\pi^2/3\). Es un reconocimiento
funcional posterior de la misma π, no una selección de su generador.

La parte polar tiene oscilación
\(8\sinh(R/4)[\cosh(R/4)-1]\), y desviación típica a lo sumo
la mitad. La desigualdad triangular en el espacio de funciones
centradas da, para el acoplamiento completo,
\[
\boxed{\|B\|^2\leq
\left[\sqrt{1-\pi^2/12}+\frac1{40}
+4\sinh(R/4)(\cosh(R/4)-1)\right]^2<\frac15.} \tag{S12}
\]
El término escalar y todas las constantes independientes de \(t\)
se eliminan al centrar, no mediante una supuesta desaparición de los
cruces. La evaluación intervalar del miembro acotante es
\(0.19926357337268538427\ldots<1/5\).

### 5.4. Schur positivo y coercividad de toda la forma

De (S6), (S9), (S11) y (S12),
\[
S=A-B^*D^{-1}B>\frac{97}{100}-\frac15=\frac{77}{100}>0.
\]
Además, para \(f=au+d\),
\[
\mathscr W_R(f,f)-\tfrac12\|f\|_2^2
\geq(A-\tfrac12)|a|^2
-2\|B\||a|\|d\|_2+(\eta-\tfrac12)\|d\|_2^2.
\]
La matriz escalar del segundo miembro tiene diagonal positiva y
determinante estrictamente mayor que
\(\tfrac{47}{100}\cdot\tfrac12-\tfrac15=\tfrac7{200}>0\).
Así queda probado \(\mathscr W_R(f,f)\geq\tfrac12\|f\|_2^2\)
para todo \(f\in V_R\). El argumento controla todos los detalles
infinitos; no los sustituye por indicadores finitos. ∎

## 6. Refinamiento, doble círculo y los dos momentos

Cada subdivisión en nueve conserva exactamente
\(u_{\rm padre}=\tfrac13\sum_{r=0}^8u_r\), y la recomposición de
funciones ocurre antes de aplicar \(J_+\) y \(J_-\). Por tanto,
los Grams de todos los indicadores nonádicos dentro de la ventana
cumplen \(G_n\geq\tfrac12 I\) y
\(V_n^*G_{n+1}V_n=G_n\). Se conservan los ocho detalles por padre y
todos sus cruces. Es uniformidad en profundidad sobre esta ventana,
no un resultado uniforme al aumentar \(R\).

Para una partición general, la matriz Schur exacta no obedece sin más
la misma compresión que el Gram bruto. Si se refina y se expresa el
Schur fino en coordenadas media antigua/nuevo detalle, el Schur
antiguo se obtiene eliminando también ese nuevo detalle. Esto es
asociatividad de la minimización en (S3). Afirmar
\(S_{\rm padre}=V^*S_{\rm hijos}V\) omitiría esa segunda corrección.

En la ventana certificada, el conector ya construido
\(\mathcal C_R=J_{-,R}L_R^{\rm cola}\) satisface
\(\mathcal C_RJ_{+,R}=J_{-,R}\). Su restricción al cierre de la
imagen efectiva \(\mathcal M_{+,R}\) es contractiva, porque
\[
\|J_{-,R}f\|^2\leq\|J_{+,R}f\|^2.
\]
La contracción se demuestra ahora mediante Schur; no se define a
partir de un Gram presuntamente positivo. Después se toma su defecto
\(\Delta_R=(I-\mathcal C_R^*\mathcal C_R)^{1/2}\) en ese espacio
efectivo y se construye
\[
\Xi_Rf=J_{-,R}f\oplus\Delta_RJ_{+,R}f.
\]
Si \(P_-\) es la proyección al primer sumando,
\[
\Xi_R^*\Xi_R=J_{+,R}^*J_{+,R},\qquad
\Xi_R^*P_-\Xi_R=J_{-,R}^*J_{-,R}.
\]
Son igualdades de formas en el dominio conjunto, no productos de
operadores no acotados sobre todo \(L^2\). Dan los dos momentos en
el codominio de dilatación. Una identificación adicional con un
\(T_N\) concreto del doble círculo necesita el entrelazamiento
con ese operador: no se identifica una proyección arbitraria con
\(T_N\) sólo por disponer de los dos momentos.

## 7. Reproducción, falsadores y siguiente extensión precisa

El programa [verificar_schur_ventana_nonadica.py](verificar_schur_ventana_nonadica.py)
certifica las constantes con aritmética intervalar y cotas explícitas
de cola. Usa el prefijo interno de π con sus huellas y el productor
racional ya conservado de γ y \(\log2\). No usa `mpmath.pi`,
`mpmath.euler`, tablas de ceros ni argumentos flotantes como entradas.

```text
python3 verificar_schur_ventana_nonadica.py --receipt CERTIFICADO_SCHUR_R_UN_NOVENO.json
python3 -O verificar_schur_ventana_nonadica.py --receipt CERTIFICADO_SCHUR_R_UN_NOVENO_OPTIMIZADO.json
```

Ambas ejecuciones: `PASS_SCHUR_FIXED_WINDOW_ONE_NINTH`, 21 controles.
Los recibos conservan extremos racionales exactos, precisión, versión
de biblioteca, procedencia y huellas. El control adversarial
\(\begin{pmatrix}1&2\\2&1\end{pmatrix}\) tiene ambos bloques
diagonales positivos y Schur \(-3\): rechaza usar sólo sus signos.

Falsadores sustantivos: omitir el negativo polar; intercambiar media
de celda con muestreo puntual; perder una traslación prima en una
ventana mayor; sustituir el Schur por \(A\); aceptar Galerkin sin
\(E^*E/\eta\); o confundir todos los refinamientos interiores con
todas las ventanas. Ninguno forma parte de este certificado.

La siguiente extensión concreta es una ventana \(R>\log2\), con
una partición nonádica cuyo bloque de detalles sea coercivo. Allí
debe evaluarse (S7), incluyendo al menos el reloj \(\log2\).
El resultado presente no afirma ese nuevo signo, ni la positividad
global de Weil, ni RH. Tampoco extrae una negación del corpus a partir
de ese alcance local: entrega una eliminación exacta, un procedimiento
certificable y un primer caso cerrado que amplía el anterior basal.

## Localizadores materiales

- `output/ARTICULO_VIII_PRIMOS_ESTRUCTURA_ESPECTRAL_20260910/manuscrito/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.md`: §§2–3, líneas 120–260; §12, 1000–1244; §13, 1245–1514; §14, 1515–1739; §15, 1740–1896.
- Mismo paquete, `fuente/pruebas/python/verificar_gram_nueve_ventanas.py`: publicación autenticada de π, forma intervalar y cola gamma.
- Mismo paquete, `fuente/pruebas/python/partes_finitas_exactas.py`: productores racionales de γ y logaritmos.
- Mismo paquete, `fuente/pruebas/python/verificar_nueve_intervalos_coercividad.py`: estimación completa previa en soportes desconectados.
- Mismo paquete, `gestion/recibo_gamma/RECIBO_CONSTANTES_GAMMA.json` y `RECIBO_GENEALOGIA_GAMMA.json`: procedencia heredada; esta nota no cambia su estado ni pretende estar ya incorporada en esos recibos.
- Serie activa: integral de 2.249 páginas y desarrollo estructural común. El gate global de primera aplicación sigue devolviendo el testigo de 2.084 páginas; conforme a continuidad, no desplaza la selección autoral de la serie ni este delta focal.
