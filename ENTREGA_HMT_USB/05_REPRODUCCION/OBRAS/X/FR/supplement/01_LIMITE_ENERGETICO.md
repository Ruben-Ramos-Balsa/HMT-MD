# Realización analítica de las energías compatibles

El registro positivo y sus refinamientos determinan, después de su construcción HMT, una familia de particiones de un intervalo. La conclusión siguiente concierne a este lector energético unidimensional. Su demostración precisa el paso desde las identidades finitas de subdivisión hasta una realización analítica; el continuo conjunto del corpus conserva su genealogía anterior y sus demás lectores.

Fijemos una partición inicial \(P_0\) de \([0,1]\) con longitudes \(d_j=K_j/\sum_iK_i>0\), y particiones finitas anidadas \(P_n\), cada una obtenida subdividiendo los intervalos anteriores. Supondremos que su malla máxima tiende a cero. Un refinamiento reiterado con un número fijo de hijos iguales satisface esta hipótesis; para otras reglas, la contracción de la malla es una condición que se comprueba en el lector correspondiente. Conservamos las etiquetas de los hijos y sus datos de acarreo como información del refinamiento.

Denotemos por \(V_n\) el espacio de funciones continuas afines en cada intervalo de \(P_n\). En este espacio la energía de la red es exactamente

\[
E_n(f)=\sum_{[a,b]\in P_n}\frac{|f(b)-f(a)|^2}{b-a}
=\int_0^1|f'(x)|^2\,dx.
\]

La segunda expresión reconoce analíticamente la suma ya construida. Para \(f\in V_n\), su extensión afín a cualquier subdivisión pertenece a \(V_{n+1}\) y conserva la energía. La inclusión \(V_n\subset V_{n+1}\), acompañada por el valor \(f(0)\), es por tanto isométrica para la norma \(|f(0)|^2+E_n(f)\).

**Teorema de reconstrucción energética.** Sea \(f_n\in V_n\) una familia compatible por restricción a los nodos antiguos: \(f_{n+1}(a)=f_n(a)\) para todo nodo \(a\) de \(P_n\). Si \(\sup_n E_n(f_n)<\infty\), existe una única función \(f\in H^1([0,1])\) cuyos valores en todos esos nodos son los prescritos. Además, \(f_n\to f\) uniformemente y en \(H^1\), y

\[
\int_0^1|f'(x)|^2\,dx=\lim_{n\to\infty}E_n(f_n).
\]

Recíprocamente, toda función de \(H^1([0,1])\), tomada en su representante continuo, produce mediante interpolación nodal una familia de esta clase.

Para demostrar la primera dirección, escribamos \(g_n=f_n'\). La compatibilidad en los extremos de cada intervalo de \(P_n\) implica, para \(m\ge n\),

\[
\frac1{b-a}\int_a^b g_m(x)\,dx
=\frac{f_n(b)-f_n(a)}{b-a}=g_n|_{(a,b)}.
\]

En consecuencia, \(g_n\) es la proyección ortogonal de \(g_m\) sobre las funciones constantes en cada intervalo de \(P_n\). Se obtiene la identidad

\[
\|g_m-g_n\|_{L^2}^2=E_m(f_m)-E_n(f_n).
\]

Las energías son crecientes y acotadas. Por ello \((g_n)\) es de Cauchy y converge en \(L^2\) a una función \(g\). Definamos \(f(x)=f_0(0)+\int_0^xg(t)\,dt\). Entonces

\[
\sup_{x\in[0,1]}|f_n(x)-f(x)|\le\|g_n-g\|_{L^2}\longrightarrow0.
\]

Esta estimación prueba convergencia uniforme, conserva los valores nodales y, junto con la convergencia de las derivadas, prueba convergencia en \(H^1\). Las normas de las derivadas dan la identidad energética. La unión de los nodos es densa porque la malla tiende a cero; dos representantes continuos con esos mismos valores coinciden, lo que prueba unicidad.

Para la recíproca, sea \(g=f'\in L^2\). La derivada de la interpolación nodal es el promedio de \(g\) sobre cada intervalo de la partición. Estos promedios son proyecciones ortogonales contractivas en \(L^2\). Para una función continua, su error frente a los promedios está acotado uniformemente por su módulo de continuidad evaluado en la malla máxima, que tiende a cero. La densidad de las funciones continuas en \(L^2\), junto con la contractividad, extiende la convergencia a \(g\). Se siguen las convergencias de funciones y energías, con los mismos argumentos anteriores.

La reconstrucción admite una descomposición de memoria por escalas. Sea \(H_n\) la extensión afín de los valores de \(P_n\) a \(P_{n+1}\), y

\[
z_{n+1}=f_{n+1}-H_nf_n.
\]

El detalle \(z_{n+1}\) se anula en todos los nodos de \(P_n\). Su derivada es ortogonal a todas las funciones constantes en los intervalos antiguos. Por ello los detalles de niveles diferentes son ortogonales en energía y, para toda profundidad finita \(N\),

\[
E_N(f_N)=E_0(f_0)+\sum_{n=0}^{N-1}E_{n+1}(z_{n+1}).
\]

En el límite, la misma suma converge exactamente a \(\int|f'|^2\). Los datos \(f_0\) y todos los detalles recuperan la familia completa. La eliminación de los nodos interiores corresponde a escoger el detalle nulo; su archivo permite recuperar cualquier configuración de energía finita. Así queda exhibida, para este lector, la distinción entre publicación efectiva y conservación de la información de refinamiento.

El flujo determinado por \(u=P_3P_{11}K\) transporta esta construcción. En cada intervalo inicial sea

\[
a_j(s)=\frac{d_j(s)}{d_j(0)}>0,
\qquad d_j(s)=\frac{K_je^{su_j}}{\sum_lK_le^{su_l}}.
\]

La aplicación \(F_s\) que envía los nodos iniciales a sus posiciones nuevas y es afín entre ellos tiene pendiente \(a_j(s)\). Si cada subdivisión hereda las fracciones y la dirección de su intervalo padre, todos sus nodos se transportan por el mismo \(F_s\). Para \(s\) en un compacto, los doce factores \(a_j(s)\) tienen cota superior finita y cota inferior positiva. La condición de malla decreciente y las normas energéticas se conservan por equivalencia: para \(U_sf=f\circ F_s^{-1}\),

\[
\int_0^1|(U_sf)'(y)|^2\,dy
=\sum_j\frac1{a_j(s)}\int_{t_{j-1}(0)}^{t_j(0)}|f'(x)|^2\,dx.
\]

Esta es la ley exacta de transporte de la energía; expresa una equivalencia de normas y explicita los factores métricos. Los espacios completados se transportan coherentemente, y la minimización de los detalles conmuta con la evolución, como en cada nivel finito.

El resultado proporciona una realización analítica completa del lector de energía del artículo: las configuraciones de energía finita se reconstruyen de su refinamiento y de su memoria. Su relación con las formas canónicas conserva el dominio ya probado: ambas construcciones son compatibles con subdivisiones de dominio fijo, mediante suma de formas en un caso y eliminación energética con detalle archivado en el otro. La fórmula de energía no identifica por sí sola una forma canónica amplituhedral de rango superior, ni altera las condiciones de cobertura y residuos que correspondan a esa promoción.
