# Semillas, dualidad de lectura y espacios de módulos

La conexión con los espacios de módulos se estudia conservando los datos que cambian y las transformaciones que identifican sus realizaciones. En HMT, el punto de partida es la composición APP–TRIT–TPK: el estado retiene residuo, cociente, orientación, acarreo y memoria antes de su representación geométrica. Una misma lectura numérica puede así tener distintas realizaciones y una misma realización puede admitir diferentes cartas. Para reunir esta estructura importa especificar qué información conserva cada mapa.

## Del dato aritmético a la dualidad

Sobre las posiciones \(1\leq i,j\leq9\), la APP levantada conserva las cuatro matrices de suma y producto:
\[
i+j=9Q^+_{ij}+R^+_{ij},\qquad
ij=9Q^\times_{ij}+R^\times_{ij}.
\]
Los residuos positivos \(R^+\) y \(R^\times\) toman representantes entre uno y nueve; los cocientes conservan los cruces de frontera. Por tanto,
\[
ij-(i+j)
=(R^\times_{ij}-R^+_{ij})
+9(Q^\times_{ij}-Q^+_{ij}).
\]
La diferencia visible no agota la diferencia del estado.

Para un entero positivo \(n\), las coordenadas
\[
r=1+((n-1)\bmod9),\qquad Q=(n-r)/9
\]
satisfacen \(n=9Q+r\). El intercambio de sus papeles se realiza sobre un dominio estable más amplio,
\[
\mathscr D_0=\mathbb Z^2\times\mathbb R_{>0},
\]
pues el cociente no está limitado al intervalo de representantes residuales. Con coordenadas \((m,w,R_0)\), la forma y su dualidad son
\[
E_{R_0}(m,w)=m^2/R_0^2+w^2R_0^2,
\qquad
\mathsf T_0(m,w,R_0)=(w,m,R_0^{-1}).
\]
Por sustitución,
\[
\mathsf T_0^2=\mathrm{id},\qquad
E_{R_0^{-1}}(w,m)=E_{R_0}(m,w).
\]
El paso a momento y enrollamiento pertenece a la realización física posterior. La igualdad anterior conserva un sector reticular completo, no sólo un valor numérico.

Cambiar de representantes también exige conservar el acarreo. El mapa escrito en el corpus es
\[
C(r,Q)=\bigl(\bar r,Q+\mathbf1_{\{r=9\}}\bigr),
\]
donde \(\bar r=r\) para \(r<9\) y \(\bar r=0\) para \(r=9\). Conserva el entero, pero no la forma cuadrática sin corregir. El texto reúne ambas cartas mediante
\[
L_9=\mathbb Z(9,-1),\qquad
\mathcal E_R^{L_9}([x])=\min_{\ell\in L_9}q_R(x+\ell),
\quad
q_R(x_1,x_2)=x_1^2/R^2+x_2^2R^2.
\]
El mínimo existe porque la restricción a \(x+k(9,-1)\) es una cuadrática coerciva en el entero \(k\). Es independiente del representante porque trasladarlo permuta los elementos del mismo coset. Para \(S(x_1,x_2)=(x_2,x_1)\),
\[
\mathcal E_{R^{-1}}^{SL_9}([Sx])
=\mathcal E_R^{L_9}([x]).
\]
De esta manera, cambiar de carta no borra la diferencia entre valor, representante y memoria. Este mapa \(C\) y la dualidad \(\mathsf T_0\) tienen definiciones distintas.

## El estado determina una dirección, no sólo una dimensión

La representación icosaédrica de doce coordenadas se descompone como
\[
V_{12}=V_1\oplus V_3\oplus V_{3'}\oplus V_5.
\]
La componente uniforme \(V_1\) se elimina mediante
\[
P_{11}=I_{12}-\frac1{12}J_{12},
\]
siendo \(J_{12}\) la matriz de unos. El vector dodecafásico \(K\) se expresa en la correspondencia de posiciones e icosaedro declarada por el corpus. Con el proyector \(P_{\mathrm{ico},3}\) sobre el sumando tridimensional,
\[
u_K=P_{\mathrm{ico},3}P_{11}K,\qquad
\ell_K=\mathbb Ru_K.
\]
La fuente calcula una norma estrictamente positiva para su \(K\), por lo que la recta existe. Entonces
\[
P_{10}(K)=P_{11}
-\frac{u_Ku_K^{\mathsf T}}{\|u_K\|^2}.
\]
La reducción elimina primero el modo uniforme y después la dirección marcada por el estado. La información estructural está en esa dirección y en la correspondencia de coordenadas, no únicamente en escribir \(12\to11\to10\). El segundo paso depende de \(K\); no se presenta como una recta invariante de toda la representación sin marcar.

## El espacio de módulos y su compatibilidad

Un módulo de representación, una operación módulo nueve y un espacio de módulos son objetos diferentes. El último organiza clases de realizaciones mediante una equivalencia especificada. En la interfaz del corpus, una compactificación candidata se escribe
\[
(x_\infty,\kappa,\mathcal U),
\qquad
\kappa:\mathcal X_{\mathrm{HMT}}^{\mathrm{enr}}
\dashrightarrow\mathcal M.
\]
La sección \(x_\infty\) conserva una prolongación compatible; \(\mathcal M\) es el espacio de módulos declarado; \(\mathcal U\) transporta métrica, orientación, registro y frontera. La compatibilidad con la dualidad exige
\[
\kappa(\mathsf T_{\mathrm{HMT}}x_\infty)
=\mathsf T_{\mathcal M}(\kappa(x_\infty))
\]
donde ambos miembros estén definidos, junto con el descenso espectral y la conservación de los tipos de observables.

Esto precisa cómo investigar la indicación sobre las semillas: seguir qué estado produce cada configuración, qué cambios de carta preservan su clase y qué operaciones se transportan al cociente. La proyección \(P_{10}(K)\) es una dependencia explícita recuperada; no sustituye por sí sola todo el mapa \(\kappa\). El criterio de admisibilidad tampoco se confunde con un ejemplo completo de compactificación.

La lectura conjunta debe conservar ambos niveles. Los mapas y equivalencias algebraicas se recuperan con sus pruebas; la realización en teoría M conserva además métrica, tres-forma, gravitino, acción y transformaciones de supersimetría. Reunir la red significa componer esos mapas efectivos, no inferir la conclusión por coincidencia de rangos ni declarar ausentes las conexiones que aún no se han recorrido.
