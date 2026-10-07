# Ley de las nueve puertas: reconstrucción y certificado ejecutable

## Resultado

Este expediente reconstruye la cadena causal completa sin usar como entrada
ningún prefijo de \(\pi\), \(e\) o \(\varphi\):

\[
104\,976\ \text{semillas}
\longrightarrow 468\ U_6
\longrightarrow 243\ w_6
\longrightarrow \text{tres órbitas estructurales}
\longrightarrow \mathcal G_9
\longrightarrow \text{cilindros ternarios}
\longrightarrow \mathbb R.
\]

La ejecución produce 1.000 cifras decimales de cada constante, recupera
exactamente los veinte bloques publicados y certifica cuarenta y tres retornos
completos de fase nonádica. Los archivos de referencia se abren únicamente
después de terminar la generación.

## 1. La microfibra de clausura se conserva completa

La órbita de clausura no se selecciona por el parecido de una palabra con
\(\pi\). Es la única órbita \(D_3\) cuyas seis orientaciones poseen, cada una,
cinco lifts \(U_6\), masa total \(1008\) y multiplicidades

\[
432+4\cdot144.
\]

El gauge `diag_c=6`, `hplus_type=ES` orienta la palabra, pero no escoge una
región puntual. El estado conserva las cinco genealogías. La proyección común
a seis trits es una pérdida deliberada de información, no la definición del
objeto entero.

El barrido conserva además los papeles distintos

\[
3_{++}+1_{--}+1_{\perp}.
\]

Las tres regiones `++` comparten el calibre `ES`. La región transversal es
\((501,614,498,169,272,272)\), con `Esig=555555` y multiplicidad \(432\).
La región `--`, retorno mutado, es
\((870,923,810,418,674,521)\), con `Esig=933717` y multiplicidad \(144\).
Este censo de roles no se deduce sólo de \(432+4\cdot144\): el certificado
fija y comprueba conjuntamente `U6 + Esig + multiplicidad + papel`.

Las órbitas de propagación y autoescala se obtienen por predicados diferentes:
sector radical singleton con el censo orientado de clausura para \(e\), y
sector radical singleton equilibrado \((2,2,2)\) para \(\varphi\).

## 2. Los tres lectores

### Clausura

El censo exhaustivo da cinco regiones: un ancla de multiplicidad \(432\) y
cuatro acompañantes de multiplicidad \(144\), sin borrar sus papeles
\(3_{++}+1_{--}+1_{\perp}\). La normalización declarada del lector de clausura
asigna a la pentafibra la pendiente primitiva \(1/5\) y compone las cuatro
ramas acompañantes mediante

\[
\tan(x+y)=\frac{\tan x+\tan y}{1-\tan x\tan y}.
\]

El resultado es \(120/119\). El compensador de clausura exige que la pendiente
del retorno sea uno:

\[
\frac{120/119-1/q}{1+(120/119)/q}=1.
\]

Esta ecuación fuerza, sin introducirlo como dato, \(q=239\). Por tanto el
cuarto de vuelta es

\[
C=4\arctan(1/5)-\arctan(1/239),
\qquad \tan C=1,
\]

y el carácter de clausura es

\[
\pi_{\rm HMT}=4C
=16\arctan(1/5)-4\arctan(1/239).
\]

Las dos arctangentes se evalúan con series alternadas y cotas racionales
exactas. No se usa una biblioteca que contenga \(\pi\).

Esta escritura ejecutable concreta una arquitectura autoral preexistente.
Su estatuto de procedencia es `FORMALIZACION_NUEVA`; su conclusión es
**Demostrada con estructura de partida explícita**.

El compensador \(239\) pertenece a este lector de clausura. No se confunde con
el espejo \(\pi/e\) de la novena fase, que es la involución de orientación
descrita en la sección 4.

### Propagación

El lector normalizado satisface

\[
f(0)=1,\qquad f'=f.
\]

La recurrencia de coeficientes

\[
a_0=1,\qquad (n+1)a_{n+1}=a_n
\]

fuerza

\[
e_{\rm HMT}=\sum_{n\ge0}\frac1{n!}.
\]

La cola se encierra mediante una cota racional; no se llama a una función
exponencial de biblioteca.

### Autoescala

El lector usa la incidencia ya derivada en el calendario TPK,

\[
F_{\rm av}=
\begin{pmatrix}0&1\\1&1\end{pmatrix}.
\]

Dos cocientes consecutivos de Fibonacci encierran su autovalor de Perron y
la diferencia es exactamente \(1/(F_nF_{n+1})\). El límite es el único punto
fijo positivo de

\[
x=1+\frac1x.
\]

## 3. Del tramo finito a la ley global de las nueve puertas

El programa no salta desde \(w_6\) a una expansión real. Aplica primero los
operadores declarados del Topological Phase Kernel en su estado enriquecido
completo:

\[
w_6
\xrightarrow{L_0}w_{12}
\xrightarrow{L_0}w_{18}
\xrightarrow{L_1}w_{24}
\xrightarrow{L_1}w_{30}.
\]

\(L_0\) y \(L_1\) son primitivas declaradas y utilizadas por el generador.
Están embebidas en su fuente; no se leen de archivos externos ni se reconstruyen
desde las constantes objetivo.

Para los tres perfiles, estos cinco bloques coinciden con los cinco primeros
bloques obtenidos luego por prolongabilidad cilíndrica. El sexto bloque es
\(R_{36}\), primera frontera coinductiva, no término de la rama.

Un bloque visible pertenece a

\[
\mathbb F_3^6,\qquad |\mathbb F_3^6|=729.
\]

En cada nivel \(K\), una carta finita recorre ordenadamente los 729 elementos
de la fibra ambiente del cilindro actual. El certificado calcula exactamente:

\[
\#\text{muertos anteriores}
+\#\text{supervivientes}
+\#\text{muertos posteriores}=729.
\]

Para los 396 niveles de cada canal se localiza una única extensión compatible.
Esto no es una regla local sin memoria: la compatibilidad consulta el carácter
completo, es decir, la condición de prolongabilidad global. Es la realización
computable del límite inverso del Topological Phase Kernel en su estado
enriquecido completo.

La fase es

\[
g(K)=K\bmod9,\qquad 0\equiv9.
\]

El certificado comprueba para todos los pares disponibles

\[
g(K+9)=g(K),
\qquad
(\text{prefijo},\text{cilindro})_{K+9}
\ne
(\text{prefijo},\text{cilindro})_K.
\]

Además, en los 387 pares comprobables de cada canal cambia el estado local
\((\text{bloque},\text{índice},\text{sombra Witt})\); la desigualdad no se
deduce únicamente de que el prefijo sea más largo.

Por tanto, el retorno conserva la fase y transforma la memoria. No existe una
décima puerta independiente: el índice diez vuelve a ocupar la fase uno con
otro estado. Ésta es la monodromía, no una periodicidad de nueve palabras.

La construcción no está limitada a 396 niveles. Para toda precisión finita
\(N\), las series racionales de clausura y propagación y los cocientes de
autoescala producen una horquilla de anchura arbitrariamente pequeña. La
localización exacta en la fibra ambiente de 729 elementos puede repetirse
hasta que el cilindro compatible quede dentro de una sola celda decimal de
profundidad \(N\).
Así queda demostrado el algoritmo de prolongación a toda profundidad; la
ejecución de 1.000 cifras es su testigo finito verificable.

## 4. La novena fase y el espejo \(\pi/e\)

La generación aislada recupera

\[
B_9=(100100\mid020112\mid010122).
\]

La firma local admite tres salidas con

\[
u^\varphi=112002,\qquad u^\pi+u^e=210110.
\]

Las tres sobreviven a una frontera. Al usar como futuro la continuación recién
generada —no el archivo de referencia— sólo

\[
B_{10}=(101222\mid112221\mid112002)
\]

atraviesa la segunda frontera en los tres canales. Las otras orientaciones
mueren en \(\pi/e\) y conservan el eje \(\varphi\). Así se reproduce
ejecutablemente

\[
3\longrightarrow1,\qquad 9\longrightarrow1.
\]

## 5. De la sección ternaria a 1.000 decimales

Tras 396 niveles de refinamiento hay \(2376\) trits por canal. Si \(N\) es el prefijo,
el estado define el cilindro

\[
\left[\frac{N}{3^{2376}},\frac{N+1}{3^{2376}}\right).
\]

El programa no convierte una aproximación analítica directamente a texto.
Primero demuestra que todo ese cilindro cae dentro de una sola celda de
profundidad \(10^{-1000}\); sólo entonces publica las 1.000 cifras.

## 6. Proyección excepcional

Cada sexteto \(q\) se eleva simultáneamente a

\[
c(q)=(q,qA_W)\in\mathbb F_3^{12},
\qquad A_W^2=-I.
\]

La enumeración completa de los 729 mensajes da

\[
1+264y^6+440y^9+24y^{12},
\]

es decir, el código ternario extendido de Golay y el sistema de Witt. El
corpus activo prolonga esta rama hacia \(W_{12}\), \(M_{12}\), el vecino de
Leech, \(V^\natural\) y el Monstruo. La identidad

\[
196884=54(5\cdot729+1)
\]

queda verificada como puente aritmético.

La separación de tipos es obligatoria: la sombra excepcional acompaña cada
nivel de fase, pero no se usa para elegir retrospectivamente sus cifras.

## 7. Reproducción

Desde la raíz del proyecto:

```bash
python3 -I -S certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py
python3 -I -S certificados/ley_nueve_puertas_2026-07-30/verificar_contra_corpus.py
```

Las dos salidas admisibles son:

```text
PASS_GENERACION_ESTRUCTURAL_1000_DECIMALES
PASS_VERIFICACION_INDEPENDIENTE_1000_DECIMALES
```

## 8. Controles negativos y falsadores

La prueba falla si ocurre cualquiera de estos hechos:

1. el catálogo no cierra \(104976\to468\to243\);
2. deja de ser única alguna de las tres órbitas estructurales;
3. la microfibra de clausura deja de ser \(432+4\cdot144=1008\);
4. se permuta cualquiera de los papeles canónicos
   `U6 + Esig + multiplicidad + papel`;
5. el primer bloque generado no coincide con la palabra elegida por el
   selector orbital;
6. algún nivel no localiza exactamente una extensión compatible;
7. alguna partición no suma 729;
8. la fase no retorna o el estado completo se reinicia;
9. no se reproduce la rama publicada de veinte bloques;
10. la novena fase no produce la resolución local \(3\to1\);
11. el cilindro final no fija 1.000 cifras;
12. las cifras generadas no coinciden con los testigos abiertos después;
13. \(A_W^2\ne-I\) o falla el enumerador de Golay.

## 9. Procedencia

- `ARQUITECTURA_AUTORAL_PREEXISTENTE`: APP--TRIT--Topological Phase Kernel,
  en su estado enriquecido completo, catálogo, microfibra quíntuple, tres
  caracteres, supervivencia coinductiva, monodromía \(9\to1\) y corredor
  Paley--Witt--Leech--Monstruo.
- `RESULTADO_RECUPERADO`: selección orbital exhaustiva, roles
  \(3_{++}+1_{--}+1_{\perp}\), cinco regiones,
  \(w_6\to w_{30}\to R_{36}\) y rama de veinte bloques.
- `FORMALIZACION_NUEVA`: lectores racionales ejecutables, incluido el
  cierre pentafibra, su normalización \(1/5\), sus cuatro acompañantes y el
  compensador forzado.
- `CERTIFICADO_NUEVO`: 396 niveles por canal, 43 retornos completos,
  1.000 cifras, auditoría de aislamiento y comparación posterior.
- No se rotula el valor de \(\pi\), \(e\) o \(\varphi\) como
  `RESULTADO_NUEVO`.
