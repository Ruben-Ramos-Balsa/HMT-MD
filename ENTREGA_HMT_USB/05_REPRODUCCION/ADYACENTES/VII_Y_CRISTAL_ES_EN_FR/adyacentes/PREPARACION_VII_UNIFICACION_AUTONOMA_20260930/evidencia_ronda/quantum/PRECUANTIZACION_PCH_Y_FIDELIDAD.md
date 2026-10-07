# Conexión precuántica PCH total y fidelidad de su realización

Composición focal del 29 de septiembre de 2026. No modifica las fuentes
ni identifica representaciones distintas por compartir un álgebra.

## 1. Flechas recibidas que se utilizan

Se conserva APP → TRIT → TPK → estado enriquecido → estructura discreta
conjunta del continuo, con memoria, orientación, ruta, hojas y frontera,
según el [recibo vigente](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/RECIBO_GENEALOGIA.json>).
La acción y su sección ℏ son realizaciones posteriores de esos datos,
no objetos convencionales utilizados para seleccionar el generador.

La acción PCH con materia y su Legendre ya están reunidas en
[RETROACCION_PCH_Y_RESTRICCIONES_VARIACIONALES.md](</Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/RETROACCION_PCH_Y_RESTRICCIONES_VARIACIONALES.md>).
Se usan su potencial canónico reducido Θ, su forma Ω=−dΘ, la eliminación
de la contorsión una sola vez y las restricciones **totales**, con
retroacción y sin congelar la métrica. El dominio es la carta regular
del reducido y los parámetros de soporte interior de esa nota; los
cargos de borde no se convierten en restricciones cero.

El propietario [11p](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex>)
declara la realización de Einstein–Schrödinger mediante
(H_sec,𝒟,𝒬), ordenamiento y restricciones. El propietario
[04ab](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/04ab_postulados_cuanticos_genealogicos_rev2.tex>)
precisa el tipo de 𝒬:

- líneas 43–60: funtor de rutas preparadas a espacios reales complejizados;
- líneas 106–120: cociclo proyectivo y representación de la memoria;
- líneas 178–207: evolución unitaria, continuidad fuerte y generador;
- líneas 339–382: teorema de reconstrucción hilbertiana con sus hipótesis.

El [11d del reloj](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11d_regimenes_cuadraticos_lector_temporal.tex>)
proporciona la realización exacta de C_108 y su Lagrangiano de Schrödinger;
no se utiliza ese calendario finito como sustituto del estado con memoria
ni como definición del operador de restricciones PCH.

## 2. Construcción exacta desde el potencial de la acción total

En la carta canónica exacta del reducido, definamos la conexión de línea

\[
 \nabla=d-\frac{i}{\hbar}\Theta,
 \qquad R^\nabla=\frac{i}{\hbar}\Omega.
 \tag{1}
\]

Para un funcional f con campo Hamiltoniano definido por
\(\iota_{X_f}\Omega=df\), sea

\[
 \mathcal P_f=-i\hbar\nabla_{X_f}+f
 =-i\hbar X_f+f-\Theta(X_f).
 \tag{2}
\]

La conexión de (1) se obtiene del potencial de la misma acción; no se
elige después un Hamiltoniano plano arbitrario. En la convención
canónica \(\{q,p\}=1\), se tiene
\([X_f,X_g]=-X_{\{f,g\}}\), y el cálculo con (1) da

\[
 \boxed{[\mathcal P_f,\mathcal P_g]
             =i\hbar\mathcal P_{\{f,g\}}.}
 \tag{3}
\]

Es una igualdad sobre secciones suaves donde están definidos sus
productos. Conserva Jacobi y no necesita que las restricciones sean
polinomios cuadráticos ni que q⁻¹ sea constante.

### Funciones de estructura: término que debe conservarse

La aplicación (2) es lineal y preserva el corchete, pero no es un
homomorfismo del producto de funciones. La regla exacta es

\[
 \mathcal P_{fg}=f\mathcal P_g+g\mathcal P_f-fg.
 \tag{4}
\]

Por tanto, cuando \(\{C_A,C_B\}=f_{AB}{}^C C_C\),

\[
 [\mathcal P_{C_A},\mathcal P_{C_B}]
 =i\hbar\sum_C\left[
 f_{AB}{}^C\mathcal P_{C_C}
 +C_C\bigl(\mathcal P_{f_{AB}{}^C}-f_{AB}{}^C\bigr)\right].
 \tag{5}
\]

El segundo término no puede borrarse fuera de la superficie de
restricciones. En particular, las funciones métricas q⁻¹ del álgebra
de hipersuperficies no son constantes en el espacio canónico total.

## 3. Planitud parcial en la superficie total de restricciones

Sea \(\mathcal C\) la superficie regular de las restricciones
totales PCH–materia, después de la reducción de segunda clase. Por
primera clase es coisótropa. Los campos \(X_{C_A}\) son tangentes a
ella y generan su distribución característica. La primera clase
significa aquí la identidad de la acción total ya probada, no una
suposición acerca de conmutadores cuánticos.

**Teorema.** La restricción de (1) a la distribución característica
de \(\mathcal C\) es una conexión parcial plana. Para campos
característicos X,Y,

\[
 \boxed{[\nabla_X,\nabla_Y]-\nabla_{[X,Y]}=0
                     \quad\text{sobre }\mathcal C.}
 \tag{6}
\]

**Prueba.** Por coisotropía,
\(\Omega(X_{C_A},X_{C_B})=\{C_A,C_B\}=0\) en \(\mathcal C\).
La misma igualdad vale para combinaciones con coeficientes variables
porque la curvatura de una conexión es tensorial. (1) da (6).
Además, allí \(\mathcal P_{C_A}=-i\hbar\nabla_{X_{C_A}}\), y los
términos proporcionales a C_C de (5) se anulan. Así se conserva el
álgebra con sus funciones de estructura sin congelar la geometría. ∎

La identidad (6) es un cierre exacto para la conexión precuántica de
las restricciones **totales** en este dominio. Si se elige una sección
horizontal respecto del calibre, se expresa módulo la acción vertical
correspondiente. No es sólo el sector Dirac en un fondo fijo.

La planitud parcial es local y no elimina por sí sola la holonomía
global de una hoja gauge. Una conexión plana puede tener monodromía
no trivial. Tampoco identifica rutas TPK diferentes por tener los
mismos extremos: la memoria y el cociclo declarados en 04ab se
conservan hasta probar la relación de rutas pertinente.

## 4. Qué cuadrado realiza y cuál no identifica por su solo enunciado

La construcción demuestra el cuadrado

\[
 (S_{\rm PCH+materia},\Theta,\{\ ,\ \}_D)
 \longrightarrow (\mathcal P_f,\nabla)
 \longrightarrow R^\nabla|_{\mathrm{característica}}=0.
 \tag{7}
\]

Para identificarlo con una realización concreta ya usada, el cuadrado
operatorio es una afirmación adicional bien tipada. Si I transporta
las secciones precuánticas admisibles a la realización 𝒬 de 11p,
la igualdad que identifica **el mismo operador** es

\[
 \widehat C_N^{\mathcal Q}I=I\mathcal P_{C_N},
 \qquad
 \widehat{fC}^{\mathcal Q}I=I\mathcal P_{fC},
 \tag{8}
\]

con producto, dominio y restricciones de representación conservados.
Una coincidencia de nombres o una isomorfía abstracta de espacios de
Hilbert no prueba (8). 04ab permite transportar una relación probada
de rutas mediante su funtor; no convierte la sola igualdad de extremos
de dos rutas en una relación de igualdad.

Este límite de identificación puede falsarse de modo concreto. Para
\(\Theta=p\,dq\),

\[
 \mathcal P_q=i\hbar\partial_p+q,\quad
 \mathcal P_p=-i\hbar\partial_q,\quad
 \mathcal P_{p^2/2}=-i\hbar p\partial_q-p^2/2.
 \tag{9}
\]

Los dos primeros descienden a funciones independientes de p. El
tercero no preserva ese subespacio: no es, por mera restricción,
el operador Schrödinger \(-\hbar^2\partial_q^2/2\). Su obtención
en otra cuantización necesita el mapa de realización correspondiente.
Para momentos lineales, el lift cotangente y la corrección de
semidensidad sí producen los generadores ya calculados; no se
extrapola ese hecho a todas las restricciones no lineales.

En dimensión canónica finita, con medida de Liouville y flujos completos,
(2) se realiza como generador autoadjunto de transporte con fase en
L². Sobre una fase de campos infinita, (1)–(6) siguen siendo identidades
de la conexión y de sus funcionales donde el cálculo canónico está
definido; no proporcionan por sí solas una medida de Liouville
infinito-dimensional ni el dominio autoadjunto de la realización
hilbertiana concreta. No se sustituye el espacio de historias completo
por un L² de fase sin declarar y demostrar ese transporte.

## 5. Conclusión focal

Se obtiene una realización precuántica exacta del álgebra variacional
total y una conexión parcial plana sobre su superficie de restricciones,
con estructura métrica variable y calibre conservados. La prueba nace
del potencial de la acción PCH–materia recuperada.

El resultado no afirma que la representación precuántica sea idéntica
al Hamiltoniano de reloj, al operador de respuesta de pantalla o a
un ordenamiento concreto de Einstein–Schrödinger. (8) nombra el
cuadrado exacto para esa identificación; el control (9) prueba que
no es una identidad automática de toda cuantización. Esto describe
el alcance de la composición efectuada, no una ausencia global del
resultado en el corpus.
