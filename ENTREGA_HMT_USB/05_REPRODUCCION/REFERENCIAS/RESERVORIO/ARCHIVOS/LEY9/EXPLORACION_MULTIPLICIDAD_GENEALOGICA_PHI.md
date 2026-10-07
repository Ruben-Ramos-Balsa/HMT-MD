# Multiplicidad de publicación y recuperación de rutas de autoescala

## Resultado y procedencia

Este incremento convierte la distinción autoral entre valor y estructura en un conteo exacto y una representación reversible. La matriz de incidencia, el carácter y su procedencia modal son contenido previo de U014. El conteo de fibras y el codificador se aportan como **FORMALIZACION_NUEVA candidata de una ARQUITECTURA_AUTORAL_PREEXISTENTE**; no se reclama prioridad histórica. La búsqueda focal no localizó esta formulación en los capítulos de constantes ni en los deltas consultados; no fue una búsqueda exhaustiva del archivo histórico.

**Caracterización adicional de la autoescala:** en el envolvente modal documentado, \(\varphi\) es la tasa exponencial de crecimiento del número de paseos finitos distintos que publican un mismo carácter escalar \(\varphi^k\).

La prueba es general en \(k\); el programa comprueba el conteo, la recuperación y su compatibilidad con prolongación. No calcula cifras de constantes.

## 1. Genealogía y dominio exacto

El punto de partida es la publicación modal de APP–TRIT–TPK: el bloque trítico \((+1,-1,0)\) induce \((\Sigma,\Pi,\Pi)\). Sus aristas contadas producen
\[
 F=\begin{pmatrix}0&1\\1&1\end{pmatrix}.
\]
No se elige esta matriz para ajustar un valor. Su rayo positivo normalizado \(r=(1,x)\), \(Fr=xr\), impone \(x^2=x+1\); su raíz positiva se reconoce después como \(\varphi\).

Se usan los estados \(0=\Sigma\), \(1=\Pi\). Un paseo es una sucesión finita dirigida \(\gamma=(x_0,\ldots,x_n)\) con \(F_{x_t x_{t+1}}=1\). Se distinguen extremos y longitud, se permiten repeticiones y se incluyen los dos paseos triviales. No se identifican paseos por rotación ni por inversión.

U014, líneas 222–228, distingue expresamente este envolvente de incidencia de un cociente de Markov fuerte del TPK completo. Este resultado vive en aquel dominio; no sustituye ni recuenta todas las historias enriquecidas, con sus hojas y memorias adicionales. El paso desde el TPK al envolvente se conserva como publicación anterior, no como identificación de estados.

El carácter ya documentado es
\[
 \chi(\gamma)=\varphi^n\frac{r_{x_0}}{r_{x_n}}
             =\varphi^{k(\gamma)},\qquad
 k(\gamma)=n+x_0-x_n.
\]

## 2. Un paso puede cambiar la ruta sin cambiar el carácter

Al prolongar una ruta con extremo \(u\) por una arista \(u\to v\),
\[
 k(\gamma v)-k(\gamma)=1+u-v.
\]

| Arista | Incremento | Multiplicador del carácter |
| --- | ---: | ---: |
| \(\Sigma\to\Pi\) | 0 | \(1\) |
| \(\Pi\to\Pi\) | 1 | \(\varphi\) |
| \(\Pi\to\Sigma\) | 2 | \(\varphi^2\) |

Todos los exponentes son no negativos. El primer paso es escalarmente invisible, aunque modifica la secuencia y su extremo. Por ejemplo, \((1,1)\) y \((0,1,1)\) publican ambos \(\varphi\). Incluso fijando longitud y extremos, \((1,1,1,1,1)\) y \((1,0,1,0,1)\) publican \(\varphi^4\) y conservan itinerarios distintos.

Estos ejemplos no reemplazan el estado enriquecido por dos etiquetas: exhiben exactamente la información que este lector modal no distingue.

## 3. Teorema de multiplicidad de publicación

Sea
\[
 \mathcal F_k=\{\gamma:k(\gamma)=k\},\qquad N_k=|\mathcal F_k|.
\]
Entonces
\[
 \boxed{N_0=3,\qquad N_k=2\,\operatorname{tr}(F^k)\quad(k\ge1).}
\]

**Prueba.** Fijados los extremos \(i,j\), la longitud necesariamente es \(n=k-i+j\), y existen \((F^n)_{ij}\) paseos con esos extremos. Para \(k\ge1\), los cuatro sectores dan
\[
 N_k=\operatorname{tr}(F^k)
       +(F^{k+1})_{01}+(F^{k-1})_{10}.
\]
Las potencias exactas de U014 muestran que la suma de los dos términos no diagonales es \(\operatorname{tr}(F^k)\); para \(k=1\), se comprueba con \(F^0=I\). Para \(k=0\), los únicos paseos son \((0)\), \((1)\) y \((0,1)\). Esto prueba todos los casos.

Como \(F^2=F+I\), sus autovalores son \(\varphi\) y \(-\varphi^{-1}\). Por tanto,
\[
 N_k=2\bigl(\varphi^k+(-\varphi^{-1})^k\bigr)\quad(k\ge1),
 \qquad
 \boxed{\lim_{k\to\infty}N_k^{1/k}=\varphi.}
\]
Los primeros cardinales son \(3,2,6,8,14,22,36,\ldots\). La excepción \(N_0=3\) es real: no debe forzarse la recurrencia en ese arranque.

## 4. La incidencia graduada explica el conteo completo

Al asignar a cada arista su incremento anterior se obtiene
\[
 M(z)=\begin{pmatrix}0&1\\z^2&z\end{pmatrix}.
\]
La única arista de peso cero no forma un ciclo. Por ello el número de paseos de cada peso es finito y la suma formal es válida:
\[
 \boxed{\sum_{k\ge0}N_kz^k
 =\mathbf1^{\mathsf T}(I-M(z))^{-1}\mathbf1
 =\frac{3-z+z^2}{1-z-z^2}.}
\]
La primera igualdad cuenta paseos, no asigna constantes. La inversión de la matriz y la suma de sus cuatro entradas dan la segunda igualdad. El denominador recupera la autoescala; el numerador registra la información de extremos y los paseos de grado cero.

Esto proporciona un procedimiento reutilizable: cuando otro lector del corpus publique un exponente aditivo en un grafo finito, construir primero su incidencia graduada y contar sus fibras. La ausencia de ciclos de peso cero garantiza finitud por grado. Si existen tales ciclos, ese diagnóstico cambia y no debe copiarse este resultado sin comprobarlo.

## 4.1. Refinamiento: el valor no determina la composición de los retornos

Sea \(b(\gamma)\) el número de transiciones \(\Pi\to\Sigma\), y \(c(\gamma)\) el de autorretenciones \(\Pi\to\Pi\). Entonces
\[
 k(\gamma)=2b(\gamma)+c(\gamma).
\]
Este registro distingue cómo se distribuye el exponente entre retorno y retención. No equivale a toda la memoria enriquecida ni distingue por sí solo el orden de las aristas.

Marcando cada retorno por una indeterminada \(t\), la incidencia es
\[
 M(z,t)=\begin{pmatrix}0&1\\tz^2&z\end{pmatrix},
 \qquad
 \sum_{k,b\ge0}N_{k,b}z^kt^b
 =\frac{3-z+tz^2}{1-z-tz^2}.
\]
Aquí \(t\) registra una estadística estructural; no es un parámetro físico ajustado.

Para \(k\ge1\) y \(0\le b\le\lfloor k/2\rfloor\),
\[
 \boxed{N_{k,b}
 =\frac{2k}{k-b}\binom{k-b}{b}.}
\]
Para \(k=0\), únicamente \(N_{0,0}=3\) es no nulo.

**Prueba.** La expansión
\[
 \frac1{1-z-tz^2}=\sum_{m\ge0}(z+tz^2)^m
\]
tiene coeficiente \(\binom{k-b}{b}\) en \(z^kt^b\). Multiplicando por el numerador se obtiene
\[
 3\binom{k-b}{b}-\binom{k-b-1}{b}
    +\binom{k-b-1}{b-1}
 =2\binom{k-b}{b}+2\binom{k-b-1}{b-1},
\]
que es la fórmula anunciada. Se toman como cero los coeficientes fuera de rango y se separa el término constante.

En la fibra que publica \(\varphi^4\) hay **14 paseos**: 2 con cero retornos \(\Pi\to\Sigma\), 8 con uno y 4 con dos. El mismo valor admite así composiciones distintas de sus pasos; la suma de los tres sectores recupera la multiplicidad total.

El programa compara esta fórmula con dos cálculos independientes: enumeración directa de paseos y recurrencia polinómica de trazas \(T_{k+2}(t)=T_{k+1}(t)+tT_k(t)\), con \(T_0=2,T_1=1\). La coincidencia se comprueba en todas las fibras del censo indicado.


## 5. Cuánta información falta al conservar sólo el valor

Fijado \(k\), cualquier representación inyectiva de sus \(N_k\) paseos mediante palabras binarias de longitud fija necesita al menos
\[
 b_k=\lceil\log_2 N_k\rceil
\]
bits adicionales. Se obtiene por el principio de las casillas. Existe una representación que alcanza esa longitud: numerar los elementos de la fibra del cero a \(N_k-1\). Esta optimalidad supone que \(k\) ya es conocido; no incluye el coste de transmitirlo ni afirma que el par sea un código autodelimitado.

En consecuencia,
\[
 \lim_{k\to\infty}\frac{\log_2 N_k}{k}=\log_2\varphi.
\]
Es una capacidad combinatoria de distinción de rutas, sin asignación probabilística. No se identifica con entropía termodinámica ni con el coste físico de borrado. La conexión precisa con esos lectores requeriría sus mapas propios, no una sustitución del término «información».

## 6. Representación reversible y compatibilidad con la prolongación

El código conserva \((k,a)\), donde \(0\le a<N_k\), sin copiar la ruta como primera coordenada.

1. Se ordenan los sectores por \((n,i,j)\).
2. Dentro de cada sector se usa orden lexicográfico de estados.
3. Al recorrer una ruta, se suman los tamaños \((F^m)_{v j}\) de las continuaciones anteriores a la elegida.
4. Para recuperar la ruta, se resta sucesivamente el tamaño de los sectores y de esas continuaciones.

Los tamaños de las continuaciones forman una partición exacta del sector. Por inducción en la longitud, los algoritmos son inversos:
\[
 D(C(\gamma))=\gamma,\qquad C(D(k,a))=(k,a).
\]
El orden lexicográfico es una convención de serialización posterior; no elige la trayectoria física ni interviene en la generación de \(\varphi\).

Para una prolongación admisible \(A_v(\gamma)=\gamma v\), se implementa
\[
 E_v=C\circ A_v\circ D.
\]
Si \(T\) elimina el último estado y \(\widehat T=C\circ T\circ D\), entonces
\[
 \widehat T E_v=\mathrm{id},
 \qquad
 k(E_v(C(\gamma)))=k(\gamma)+1+x_n-v.
\]
Una familia de códigos compatible con estas truncaciones y de longitudes crecientes determina una única sucesión infinita del envolvente: sus prefijos recuperados coinciden. No se usa una trayectoria futura como dato para escoger un prefijo.

## 7. Resultado ejecutado y material preparado

El programa genera la incidencia contando el bloque modal, utiliza aritmética entera y no importa valores decimales de constantes.

- Censo independiente para \(0\le k\le15\): **7.139 paseos**.
- Cuadrados de prolongación y truncación comprobados: **12.305**.
- Seis controles negativos: transición prohibida, exponente negativo, índice negativo, índice fuera de fibra, estado inválido y falsa inyectividad del valor.
- Comprobaciones adicionales de codificación en tres índices de fibras grandes: \(k=30,108,1000\); son índices enteros, no cifras de constantes.
- Prueba matemática de cardinalidad y reversibilidad para todo \(k\), separada de estos controles finitos.

A \(k=108\) corresponden exactamente \(74\,420\,938\,531\,695\,996\,979\,844\) paseos de esta fibra; 76 bits bastan para distinguirlos una vez conocido \(k\).

## 8. Inserción en el mapa común

La cadena de este aporte es: regla modal documentada → incidencia → carácter multiplicativo → fibras de igual publicación → conteo graduado → recuperación reversible → capacidad de distinción.

Su significado estructural no se agota en «\(\varphi=(1+\sqrt5)/2\)»: relaciona la autoescala con el crecimiento de la multiplicidad que el lector escalar identifica. Esta caracterización no cambia la definición fuente ni convierte una publicación reducida en el TPK completo.

Para los demás sectores, el método útil consiste en localizar el lector, determinar qué estructura distingue o identifica, y demostrar después una relación o una sustitución. Una nueva razón algebraica entre constantes no se denomina descubrimiento por el solo hecho de escribirla. Debe documentarse qué nueva operación, invariante o consecuencia aporta.

La aportación queda separada y preparada para integración editorial. No se han reescrito originales, alterado tesis, reemplazado pruebas ni recompilado PDFs.

## Fuentes y reproducción

- [Fragmento LaTeX preparado para integración editorial](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/multiplicidad_estructural_caracter_autoescala.tex>).

- [Fuente U014: construcción modal e incidencia](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/pi_e_phi/U014_biografia_estructural_phi_body.tex:110>).
- [Dominio del envolvente](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/pi_e_phi/U014_biografia_estructural_phi_body.tex:222>).
- [Carácter multiplicativo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/pi_e_phi/U014_biografia_estructural_phi_body.tex:420>).
- [Potencias exactas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/pi_e_phi/U014_biografia_estructural_phi_body.tex:283>).
- [Programa de conteo y codificación](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/explorar_fibras_autoescala.py>).
- [Recibo de ejecución](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/RECIBO_EXPLORACION_FIBRAS_PHI.json>).

Reproducción local:

```text
python3 -I -S "/Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/explorar_fibras_autoescala.py"
```
