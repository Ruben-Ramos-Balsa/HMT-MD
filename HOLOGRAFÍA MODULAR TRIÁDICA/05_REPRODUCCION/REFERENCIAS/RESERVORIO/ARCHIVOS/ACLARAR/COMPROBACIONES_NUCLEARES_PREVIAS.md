# Comprobaciones nucleares conservadas para la integración

Este documento reúne resultados comprobados en Aclarar la tarea antes del reparto. Su finalidad es conservar las pruebas positivas y permitir que los responsables de cada bloque continúen desde ellas, sin repetir la generación numérica ni confundir un resultado local con toda su prolongación.

## 1. π, φ y e

La ejecución del certificado nonádico ha reproducido 1.000 decimales por canal y ha superado su contraste independiente. Se ha leído la prueba verificable, que especifica los lectores y sus normalizaciones: selección de las cinco regiones y clausura angular para π; carácter de propagación normalizado para e; incidencia de autoescala y rayo positivo para φ. La enumeración y las cotas racionales constituyen evidencia reproducible. La prueba de prolongación pertenece a los lectores y a sus cotas, no al mero hecho de haber obtenido mil cifras.

El certificado conserva las distinciones entre 104.976 estados-semilla, 468 emisiones decimales, 243 palabras visibles y el ambiente de 729 palabras. Registra 396 niveles, 43 vueltas y 387 comparaciones entre niveles separados por nueve pasos por canal. Se mantiene la distinción entre retorno de fase y retorno del estado.

Fuentes: [prueba verificable](</Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/PRUEBA_VERIFICABLE.md>) y [generador del certificado](</Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py>). El examen final de los antecedentes y la prolongación queda reunido por Ley 9 puertas.

## 2. Centro electrónico y vacancias

Sobre \(D_9^2=\{1,\ldots,9\}^2\), la inversión \((a,b)\mapsto(10-a,10-b)\) tiene un único punto fijo: \((5,5)\). Es una afirmación comprobada exhaustivamente sobre las 81 celdas.

Se conserva la evaluación completa

\[
\mathcal A(a,b)=\bigl((\rho_9(a+b),q_+),(\rho_9(ab),q_\times)\bigr),
\quad n=\rho_9(n)+9q,
\quad \rho_9(n)=1+(n-1)\bmod9.
\]

En la fibra aditiva \(a+b=10\), el centro tiene evaluaciones \(((1,1),(7,2))\). Las únicas celdas cuyo residuo multiplicativo sigue siendo siete y cuyo cociente multiplicativo disminuye exactamente en uno son \((8,2)\) y \((2,8)\), ambas con evaluaciones \(((1,1),(7,1))\). Todas sus coordenadas pertenecen a la clase residual dos módulo tres, correspondiente al régimen TRIT de esta fibra.

La prueba no requiere sólo enumeración: escribiendo \((a,b)=(5+t,5-t)\), el producto es \(25-t^2\). Conservar el residuo producto exige \(t^2\equiv0\pmod9\). Para \(|t|\le4\), las posibilidades son \(t=0,\pm3\); las dos no centrales reducen el producto en nueve y, por tanto, eliminan exactamente un acarreo. Se obtiene una vacancia mínima bidireccional bajo conservación de la hoja aditiva, del residuo producto y del régimen trítico.

## 3. Conmutador electrónico y álgebra local

Se ha reconstruido la tabla conjunta de las dos particiones, suma y producto reducidos, sobre las 729 ternas de \(D_9^3\). Si \(M\) es la tabla de incidencias y \(D_r,D_c\) sus marginales, el operador de solapamiento \(K=D_r^{-1}MD_c^{-1}M^T\) es semejante a uno positivo. Su polinomio característico, calculado mediante aritmética racional, es

\[
\chi_K(t)=t^4(t-1)(t-\tfrac14)(t-\tfrac1{18})^2(t-\tfrac7{132}).
\]

No se ha supuesto que sólo existan tres autovalores. El espectro completo da

\[
\max_{\lambda\in\sigma(K)}\lambda(1-\lambda)=\frac3{16},
\qquad \|[P_\Sigma,P_\Pi]\|=\frac{\sqrt3}{4}.
\]

En el bloque principal correspondiente a \(\lambda=1/4\), se verifican exactamente

\[
S^2=I,\quad J^2=-I,\quad SJ=-JS,
\]

con \(S=\operatorname{diag}(1,-1)\) y \(J=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)\). Es la presentación local de \(\mathrm{Cl}_{1,1}\cong M_2(\mathbb R)\), y no una identificación de todo el estado HMT con una sola matriz. Para la palabra dodecafásica \((+++---)^2\), se han vuelto a comprobar los lectores \(\Omega=80\) y \(P_6=6\).

Fuente leída: capítulo 58, páginas físicas 1041–1053 del integral fijo. El desarrollo retrospectivo y el código de la aritmética local están conservados en [verificador del estado holonómico](</Users/ruben/Documents/New project/output/INVESTIGACION_HOLONOMIA_NONADICA_CRISTAL_APERIODICO_20260903/verificar_aritmetica_estado_holonomico.py>).

## 4. Raíz de −1 y Catalán

La matriz de conferencia integral \(C\) satisface \(C^2=5I\); su reducción módulo tres satisface \(\overline C^2=-I\). La comprobación se ha ejecutado con entradas enteras. Esta realización finita conserva su característica; no se identifica el cuerpo finito con \(\mathbb C\). La realización real de la extensión integral \(\mathbb Z[u]/(u^2+1)\) y el bloque matricial precedente proporcionan el otro ámbito explícito del operador de cuadrado −I.

El carácter de cuarto de giro determina el operador diagonal \(Q_4\) con valores \(0,1,0,-1\). Para \(N e_n=n e_n\), la serie de la traza

\[
\operatorname{Tr}(N^{-2}Q_4)
=\sum_{n\ge0}\frac{(-1)^n}{(2n+1)^2}
=L(2,\chi_{-4})
\]

converge absolutamente y determina Catalán. Se ha leído la construcción del carácter y la prueba de esta identificación, y se ha calculado de nuevo un intervalo racional mediante 150 términos de la transformación de Euler. Su anchura es a lo sumo \(2^{-150}\), sin proporcionar al algoritmo un decimal objetivo. La evaluación coincide en las cifras garantizadas con

\[
G_{\rm Cat}=0,915965594177219015054603514932384110774149374\ldots
\]

Fuente: [Catalán, Apéry y caracteres residuales](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c33_catalan_apery_euler.tex>).

## 5. Comprobaciones de α y del funcional de Barbero

Se ha reconstruido exactamente el mismo vector \(K\) mediante las cartas de Hadamard y de diferencias. Reutilizando las primeras doce tríadas de π, e y φ generadas por el certificado, el acarreo terminal con \(c_{13}=0\) produce

\[
(7,297,352,569,283,800,997,285,105,472,380,663).
\]

La telescopía del acarreo se comprueba con enteros. Para las ecuaciones de los aproximantes polinómicos de órdenes seis y nueve se han comprobado signos opuestos en los extremos, derivada positiva y sendos intervalos racionales de anchura inferior a \(8\times10^{-45}\) para sus raíces. La ventana finita, cada aproximante y la prolongación infinita conservan sus denominaciones: la igualdad de límites es objeto del informe de Ley 9 puertas, no una consecuencia inferida de la proximidad decimal.

En el funcional de Barbero se han comprobado las incidencias 90 y 120, los doce sectores y la costura orientada que dan

\[
F(q)=12\frac{q^{90}}{1-q^{270}}-\frac{q^{120}}{1-q^{360}},\qquad
\lim_{q\to1^-}(1-q)F(q)=\frac1{24}.
\]

El residuo complejo en uno es, por tanto, \(-1/24\). La evaluación angular completa y la realización de área se integran desde MASAS; no se confunde este coeficiente de polo con todo el parámetro.

## Evidencia ejecutable y límites de atribución

Todo lo anterior se conserva en [comprobar_resultados_prioritarios.py](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_resultados_prioritarios.py>) y [su resultado ejecutado](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COMPROBACIONES_RESULTADOS_PRIORITARIOS.json>). El archivo separa pruebas exactas, evaluaciones acotadas y antecedentes recuperados.

La estructura electrónica, su realización física, su expresión energética y el contraste experimental son afirmaciones relacionadas, pero sus comprobaciones no se sustituyen entre sí. El contraste de masas y la continuación de los antecedentes se reúnen en el bloque MASAS. Del mismo modo, una prueba local no se atribuye como demostración retrospectiva de todas las afirmaciones del tratado. Estas distinciones permiten conservar resultados positivos precisos sin perder sus hipótesis ni atribuir como nuevo lo que ya estaba construido.
