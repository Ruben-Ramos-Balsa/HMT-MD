# Aritmética trítica: normalización, transporte y reconstrucción

Ampliación acumulativa REV03. Desarrolla TRIT-001 y la parte algebraica de TRIT-002; mantiene las dependencias APP-004–APP-011 y la conexión con TPK-001. No reemplaza las fichas anteriores. Procedencia: `RESULTADO_RECUPERADO`; el desglose expositivo y los ejemplos focales de esta revisión no se presentan como nuevos resultados matemáticos.

## Fuente y corte de la construcción

La fuente leída íntegramente es [división balanceada, operaciones y realizaciones del TRIT](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/trit_desarrollo.tex:1>). Los rótulos LaTeX se conservan junto a cada grupo de pasos. La residencia en el núcleo común se registra en REV02; esta revisión usa la fuente de la edición especializada posterior, no una fórmula externa en sustitución del generador.

El dato inicial de esta sección es una evaluación entera ya obtenida de una hoja de APP. Aquí se descompone esa evaluación y se transportan sus operaciones. La selección del régimen sobre el reloj del TPK usa la misma sección residual, pero es otra aplicación: su entrada es una posición de fase, no una evaluación de la hoja. La generación de las constantes continúa después por el emisor, las semillas, las elevaciones y la prolongación nonádica. Ninguna constante objetivo entra en los ejemplos siguientes.

La prueba aritmética recupera la evaluación. El registro de ruta, orientación, hoja, frontera y memoria se conserva en el estado enriquecido que la contiene; no se afirma que la pareja residuo–cociente reconstruya por sí sola una trayectoria que nunca recibió.

## TRIT-001.01 — Construcción del cociente balanceado

**Entrada:** un entero \(n\), obtenido por evaluación de la hoja declarada. **Salida:** dos enteros \(r,c\), con \(r\in\{-1,0,1\}\). **Propietario:** `trit-ampl-def-coordenadas`.

1. TRIT-001.01.01. Se traslada el dividendo una unidad: \(n+1\). Ese desplazamiento fija la sección centrada; no es un acarreo añadido al estado.
2. TRIT-001.01.02. Se calcula \(c=\lfloor(n+1)/3\rfloor\). El suelo se toma también para enteros negativos; truncar hacia cero produciría otra operación.
3. TRIT-001.01.03. Se define \(r=n-3c\).
4. TRIT-001.01.04. De \(3c\le n+1<3c+3\) se deduce \(-1\le r<2\).
5. TRIT-001.01.05. Como \(r\) es entero, sólo puede valer \(-1,0,1\).
6. TRIT-001.01.06. La evaluación se reconstruye sin aproximación: \(n=r+3c\).

La notación que se conservará es

\[
\mathcal B(n)=(r_3(n),q_3(n)),\qquad
q_3(n)=\left\lfloor\frac{n+1}{3}\right\rfloor,\quad
r_3(n)=n-3q_3(n),\qquad
\mathcal L(r,c)=r+3c.
\]

## TRIT-001.02 — Unicidad e inversión exacta

**Dependencia:** TRIT-001.01. **Propietario:** párrafo de unicidad posterior a `trit-ampl-def-coordenadas`.

1. TRIT-001.02.01. Supóngase \(r+3c=s+3d\), con ambos residuos balanceados.
2. TRIT-001.02.02. Se resta: \(r-s=3(d-c)\).
3. TRIT-001.02.03. El miembro izquierdo está entre \(-2\) y \(2\); el derecho es múltiplo de \(3\).
4. TRIT-001.02.04. Por tanto, ambos son cero: \(r=s\) y \(c=d\).
5. TRIT-001.02.05. Para cualquier pareja admisible, la representación de \(\mathcal L(r,c)\) es precisamente \((r,c)\); esto prueba \(\mathcal B\circ\mathcal L=\mathrm{id}\).
6. TRIT-001.02.06. La igualdad del paso 01.06 prueba \(\mathcal L\circ\mathcal B=\mathrm{id}\). Las dos direcciones quedan escritas; no se sustituye una por la palabra «reversible».

La inversión de signo es igualmente exacta: \(-n=(-r)+3(-c)\), y \(-r\) sigue siendo balanceado. La unicidad da \(\mathcal B(-n)=(-r_3(n),-q_3(n))\).

| Evaluación \(n\) | \(q_3(n)\) | \(r_3(n)\) | Reconstrucción |
|---:|---:|---:|---|
| \(-3\) | \(-1\) | \(0\) | \(0+3(-1)\) |
| \(-2\) | \(-1\) | \(1\) | \(1+3(-1)\) |
| \(-1\) | \(0\) | \(-1\) | \(-1+3(0)\) |
| \(0\) | \(0\) | \(0\) | \(0+3(0)\) |
| \(1\) | \(0\) | \(1\) | \(1+3(0)\) |
| \(2\) | \(1\) | \(-1\) | \(-1+3(1)\) |
| \(3\) | \(1\) | \(0\) | \(0+3(1)\) |
| \(4\) | \(1\) | \(1\) | \(1+3(1)\) |

## TRIT-001.03 — Acarreo de la suma: todos los casos residuales

**Entrada:** \(n=r+3c\), \(m=s+3d\). **Dependencias:** TRIT-001.01–02. **Propietario:** `trit-ampl-prop-aritmetica`, ecuación `trit-ampl-eq-suma`.

1. TRIT-001.03.01. Se suman los residuos como enteros: \(u=r+s\).
2. TRIT-001.03.02. Se normaliza ese entero, no cada sumando de nuevo: \(u=r_3(u)+3q_3(u)\).
3. TRIT-001.03.03. Se denomina \(\chi(r,s)=q_3(r+s)=(r+s-r_3(r+s))/3\).
4. TRIT-001.03.04. Los cocientes anteriores y el acarreo nuevo se suman: \(c'=c+d+\chi(r,s)\).
5. TRIT-001.03.05. La salida es \((r_3(r+s),c')\).
6. TRIT-001.03.06. Su reconstrucción es \(r+s+3(c+d)=n+m\); la unicidad identifica la salida con \(\mathcal B(n+m)\).

| \(r\) | \(s\) | \(r+s\) | Residuo normalizado | Acarreo \(\chi(r,s)\) |
|---:|---:|---:|---:|---:|
| \(-1\) | \(-1\) | \(-2\) | \(1\) | \(-1\) |
| \(-1\) | \(0\) | \(-1\) | \(-1\) | \(0\) |
| \(-1\) | \(1\) | \(0\) | \(0\) | \(0\) |
| \(0\) | \(-1\) | \(-1\) | \(-1\) | \(0\) |
| \(0\) | \(0\) | \(0\) | \(0\) | \(0\) |
| \(0\) | \(1\) | \(1\) | \(1\) | \(0\) |
| \(1\) | \(-1\) | \(0\) | \(0\) | \(0\) |
| \(1\) | \(0\) | \(1\) | \(1\) | \(0\) |
| \(1\) | \(1\) | \(2\) | \(-1\) | \(1\) |

El acarreo no es siempre positivo. En el extremo \((-1)+(-1)\) se prolonga con \(-1\); en \(1+1\), con \(+1\). Las dos correcciones son parte de una misma normalización balanceada.

## TRIT-001.04 — Producto: procedencia de cada término

**Misma entrada**, pero otra operación. **Propietario:** `trit-ampl-eq-producto`.

1. TRIT-001.04.01. Se distribuye \((r+3c)(s+3d)\).
2. TRIT-001.04.02. Se conserva el término residual \(rs\).
3. TRIT-001.04.03. El término \(r\cdot3d\) aporta \(rd\) al cociente.
4. TRIT-001.04.04. El término \(3c\cdot s\) aporta \(sc\) al cociente.
5. TRIT-001.04.05. El término \(3c\cdot3d=9cd\) aporta \(3cd\) al cociente.
6. TRIT-001.04.06. El producto \(rs\) pertenece ya a \(\{-1,0,1\}\), por lo que no aparece otro acarreo residual.
7. TRIT-001.04.07. La salida es \((rs,rd+sc+3cd)\), cuya reconstrucción es exactamente \(nm\).

Ejemplo de la fuente, desarrollado: \(2=(-1)+3(1)\), \(4=1+3(1)\).

\[
\begin{aligned}
\mathcal B(2+4)&=(r_3(0),1+1+0)=(0,2),&\mathcal L(0,2)&=6,\\
\mathcal B(2\cdot4)&=(-1,(-1)1+1(1)+3(1)(1))=(-1,3),&\mathcal L(-1,3)&=8.
\end{aligned}
\]

Aquí las evaluaciones, residuos y cocientes permanecen diferenciados. Usar la misma pareja como entrada de suma y producto permite ver en qué paso se separan ambas operaciones.

## TRIT-001.05 — Asociatividad y contabilidad del acarreo

**Entrada:** tres residuos \(r,s,t\), con sus cocientes cuando proceda. **Propietario:** identidad del cociclo tras `trit-ampl-eq-producto`.

1. TRIT-001.05.01. Se escribe \(r\oplus s=r_3(r+s)\).
2. TRIT-001.05.02. La asociación izquierda da
   \(r+s+t=r_3((r\oplus s)+t)+3[\chi(r,s)+\chi(r\oplus s,t)]\).
3. TRIT-001.05.03. La asociación derecha da
   \(r+s+t=r_3(r+(s\oplus t))+3[\chi(s,t)+\chi(r,s\oplus t)]\).
4. TRIT-001.05.04. Ambas expresiones son descomposiciones balanceadas del mismo entero. Por unicidad coinciden tanto sus residuos como sus cocientes.
5. TRIT-001.05.05. Se obtiene
   \(\chi(r,s)+\chi(r\oplus s,t)=\chi(s,t)+\chi(r,s\oplus t)\).
6. TRIT-001.05.06. Añadir los cocientes originales aporta \(c+d+e\) a ambos lados; la asociación no altera la evaluación reconstruida.

Ejemplo que desplaza el lugar del acarreo: para \((1,1,-1)\), la asociación izquierda acumula \(+1\) y después \(-1\); la derecha acumula \(0\) y \(0\). Los totales son iguales, pero los registros ordenados \((1,-1)\) y \((0,0)\) son distintos. La igualdad de evaluaciones no identifica esos registros de operaciones. Éste es un ejemplo aritmético de contabilidad ordenada; su elevación a rutas TPK requiere además los datos de transporte.

## TRIT-001.06 — Segundo nivel ternario y módulo nueve

**Entrada:** un residuo balanceado \(r\) y una clase \(\bar c\in\mathbb Z/3\mathbb Z\). **Salida:** una clase módulo nueve. **Propietario:** aplicación \(\beta\) en la misma fuente.

1. TRIT-001.06.01. Se define \(\beta(r,\bar c)=r+3c\pmod9\).
2. TRIT-001.06.02. Sustituir \(c\) por \(c+3k\) cambia la expresión en \(9k\); la clase de salida no depende del representante.
3. TRIT-001.06.03. Si dos imágenes coinciden, la reducción módulo tres iguala los residuos balanceados.
4. TRIT-001.06.04. Tras cancelar esos residuos, \(3(c-d)\) es múltiplo de nueve; por tanto \(\bar c=\bar d\).
5. TRIT-001.06.05. Para cualquier clase módulo nueve, se elige un representante entero \(n\) y se calcula \((r_3(n),q_3(n)\bmod3)\). La reconstrucción devuelve esa clase.
6. TRIT-001.06.06. Cambiar \(n\) por \(n+9k\) mantiene \(r_3(n)\) y añade \(3k\) al cociente. La inversa tampoco depende del representante.

| Clase \(n\bmod9\) | Residuo \(r\) | Clase del cociente \(\bar c\) |
|---:|---:|---:|
| \(0\) | \(0\) | \(0\) |
| \(1\) | \(1\) | \(0\) |
| \(2\) | \(-1\) | \(1\) |
| \(3\) | \(0\) | \(1\) |
| \(4\) | \(1\) | \(1\) |
| \(5\) | \(-1\) | \(2\) |
| \(6\) | \(0\) | \(2\) |
| \(7\) | \(1\) | \(2\) |
| \(8\) | \(-1\) | \(0\) |

La suma de parejas incluye \(\chi\) en el segundo componente, ahora reducido módulo tres. La pareja \((1,0)\) sumada consigo misma da \((-1,1)\), clase dos, no \((-1,0)\), clase ocho. Por eso esta codificación de nueve posiciones no es la suma componente a componente de dos coordenadas ternarias independientes.

En la tabla APP con representantes positivos, el nueve representa la clase cero. No se cambia la celda nueve por una ausencia de celda. La información del representante y la del cociente de la división entera deben conservarse cuando el objeto es el estado completo, no solamente una clase.

## TRIT-001.07 — Fibra nula, iteración y profundidad

**Propietarios:** `trit-ampl-inversion` y definición inicial.

1. TRIT-001.07.01. La condición \(r_3(n)=0\) equivale a \(n=3c\).
2. TRIT-001.07.02. Su fibra entera es \(\{(0,c):c\in\mathbb Z\}\), no sólo tres pares.
3. TRIT-001.07.03. Si otra operación restringe el cociente a \(-1,0,1\), la fibra restringida tiene tres casos. Esa restricción pertenece a dicha operación y debe declararse.
4. TRIT-001.07.04. Para iterar, se fija \(n_0=n\), \(n_{j+1}=q_3(n_j)\), \(r_j=r_3(n_j)\).
5. TRIT-001.07.05. La sustitución de \(n_j=r_j+3n_{j+1}\), repetida \(k\) veces, da
   \(n=\sum_{j=0}^{k-1}r_j3^j+3^kn_k\).
6. TRIT-001.07.06. La inducción empieza en \(k=1\). En el paso siguiente se sustituye \(n_k=r_k+3n_{k+1}\); se agrega el término \(r_k3^k\) y el nuevo resto es \(3^{k+1}n_{k+1}\).
7. TRIT-001.07.07. Cada profundidad conserva prefijo y cociente terminal. No se descarta \(n_k\) por haber escrito más trits.

Por ejemplo, \(8=-1+3(3)\), \(3=0+3(1)\), \(1=1+3(0)\), de modo que los trits sucesivos son \((-1,0,1)\) y \(8=-1+0\cdot3+1\cdot9\). Se ha desarrollado la representación de un entero; ésta no debe confundirse con la prueba de generación coinductiva de un valor real, que usa su propio refinamiento y sus cilindros.

## TRIT-001.08 — Firma de evaluación y selector de fase

**Entradas diferentes:** \(F(p,q)\), con \(F\) la evaluación de una hoja APP; y una posición \(t\) del reloj operativo. **Dependencias:** APP y TRIT-001.01. **Salida:** en ambos casos un símbolo trítico, con destino diferente.

1. TRIT-001.08.01. La firma de la evaluación es \(r_3(F(p,q))\).
2. TRIT-001.08.02. La sección aplicada a las posiciones \(1,\ldots,9\) produce \((1,-1,0,1,-1,0,1,-1,0)\).
3. TRIT-001.08.03. En el selector \(M_{\rm ph}\), las posiciones \(1,4,7\) activan el modo positivo; \(2,5,8\), el negativo; \(3,6,9\), el neutro.
4. TRIT-001.08.04. El operador de transporte recibe ese modo junto con cursor, dirección y memoria. La acción concreta se desarrolla en la traza del emisor, sin deducirla de la firma de otra evaluación.
5. TRIT-001.08.05. Coincidir en el símbolo no identifica entradas ni salidas completas. El libro deberá declarar siempre «firma de esta hoja» o «selector de esta fase» en la primera aplicación de cada mapa.

## TRIT-001.09 — Reversión orientada de una palabra

**Entrada:** \((\tau_1,\ldots,\tau_n)\). **Propietario:** `trit-ampl-inversion`.

1. TRIT-001.09.01. Se invierte el orden de las posiciones.
2. TRIT-001.09.02. Se cambia el signo de cada símbolo.
3. TRIT-001.09.03. Se obtiene \(C_{\rm rev}(\tau)_j=-\tau_{n+1-j}\).
4. TRIT-001.09.04. Al repetir la operación, el índice es \(n+1-(n+1-j)=j\) y el signo es \(-(-\tau_j)=\tau_j\); por tanto \(C_{\rm rev}^2=\mathrm{id}\).
5. TRIT-001.09.05. La longitud y el número de ceros se conservan. La posición de un cero se refleja; no se afirma que permanezca en la misma casilla.
6. TRIT-001.09.06. Para el estado TPK completo se empleará su involución tipada sobre los demás campos. Esta fórmula sola no especifica el transporte de una hoja o un registro que no figure en la palabra.

Ejemplo: \((1,0,-1,1)\mapsto(-1,1,0,-1)\mapsto(1,0,-1,1)\).

## TRIT-002.01 — Realización cuadrática del régimen seleccionado

**Corte:** después de seleccionar el tipo \(\tau\in\{-1,0,1\}\), se estudia su realización algebraica. Las coordenadas \(a,b\) de esta realización no sustituyen los residuos y cocientes enteros anteriores. **Propietario:** `trit-ampl-norma`.

El campo de esta realización es \(\mathbb R\): se trabaja en \(\mathbb A_\tau=\mathbb R[J]/(J^2+\tau)\), con \(a,b,c,d\in\mathbb R\). La equivalencia entre norma no nula e invertibilidad se afirma en esta álgebra real; no se traslada sin más a una presentación sobre los enteros.

1. TRIT-002.01.01. El generador de la realización satisface \(J_\tau^2=-\tau I\).
2. TRIT-002.01.02. Se escriben dos elementos \(z=aI+bJ_\tau\), \(w=cI+dJ_\tau\).
3. TRIT-002.01.03. Al distribuir su producto aparecen \(acI\), \(adJ_\tau\), \(bcJ_\tau\) y \(bdJ_\tau^2\).
4. TRIT-002.01.04. Se sustituye exclusivamente el último término por \(-\tau bdI\).
5. TRIT-002.01.05. Se reúnen las dos componentes: \(zw=(ac-\tau bd)I+(ad+bc)J_\tau\).
6. TRIT-002.01.06. La conjugación \(\bar z=aI-bJ_\tau\) mantiene \(\tau\); no es la reversión orientada que puede intercambiar signos del tipo.
7. TRIT-002.01.07. El producto \(z\bar z=(a^2+\tau b^2)I\) define la norma algebraica \(N_\tau(z)\).
8. TRIT-002.01.08. La conjugación es multiplicativa. Por conmutatividad, \((zw)\overline{zw}=(z\bar z)(w\bar w)\); de ahí \(N_\tau(zw)=N_\tau(z)N_\tau(w)\).
9. TRIT-002.01.09. Si \(N_\tau(z)\ne0\), \(z^{-1}=\bar z/N_\tau(z)\) da producto uno.
10. TRIT-002.01.10. Si existe inversa \(w\), \(N_\tau(z)N_\tau(w)=1\), luego \(N_\tau(z)\ne0\). Quedan escritas necesidad y suficiencia.

## TRIT-002.02 — Casos degenerados y representación matricial

La representación es \(z\mapsto\begin{pmatrix}a&-\tau b\\b&a\end{pmatrix}\). La entrada superior izquierda y la inferior izquierda recuperan \(a,b\), por lo que es fiel. Su multiplicación reproduce el producto anterior, y su determinante es \(a^2+\tau b^2\).

- TRIT-002.02.01. Para \(\tau=1\), la norma es \(a^2+b^2\); se anula sólo en el elemento cero.
- TRIT-002.02.02. Para \(\tau=0\), \(J_0\ne0\), pero \(J_0^2=0\) y \(N_0(J_0)=0\). El símbolo de tipo cero no identifica al generador con el elemento cero.
- TRIT-002.02.03. Para \(\tau=-1\), \(N_{-1}(I+J)=N_{-1}(I-J)=0\), aunque ambos elementos son no nulos.
- TRIT-002.02.04. Su producto es \(I-J^2=0\). Esta anulación es algebraica y se conserva al pasar a matrices.
- TRIT-002.02.05. Para \(I+uJ_\tau\) e \(I+vJ_\tau\), el producto completo es \((1-\tau uv)I+(u+v)J_\tau\).
- TRIT-002.02.06. Sólo si \(1-\tau uv\ne0\) se obtiene la coordenada afín \((u+v)/(1-\tau uv)\); el factor escalar dividido debe conservarse si interesa el elemento completo.
- TRIT-002.02.07. Con \(\tau=1,u=v=1\), el producto es \(2J\): la carta escalar deja de servir, pero el elemento es no nulo.
- TRIT-002.02.08. Con \(\tau=-1,u=1,v=-1\), el producto es cero: en este caso no existe dirección que se recupere cambiando de carta. Los dos bordes no son equivalentes.

La lectura lorentziana de la forma escindida, las exponenciales, su conservación cuadrática y las realizaciones operatorias del estado siguen vinculadas a TRIT-003–004 y a CG. Esta revisión no los elimina ni los da por desarrollados por haber explicitado el producto. Su extensión debe conservar tipo, representación, campo, escala y operador de transporte.

## Puente hacia los siguientes desarrollos

1. TPK-001 recibe el selector de fase de TRIT-001.08, no una constante clásica elegida como entrada.
2. El emisor recibe la evaluación APP y su estado de cursor; la reducción de sus seis emisiones tiene dominio y fibras propios. La traza completa se conserva en el documento 21.
3. La prolongación en base tres y la publicación en bloques decimales se desarrollan en el documento 22. La inversión de una evaluación no debe usarse como prueba automática de publicación de un cilindro.
4. El documento 23 identifica implementaciones existentes y contratos pendientes de conexión. Una identidad probada aquí en lenguaje matemático no se anunciará como formalizada en Lean hasta identificar y ejecutar su prueba correspondiente.

## Comprobación focal de esta revisión

[Programa reproducible](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/tools/comprobar_trit_rev03.py>) y [datos completos del control](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/20_TRIT_COMPROBACION.json>).

El control enumera los nueve pares residuales, las veintisiete ternas del cociclo y las ochenta y una operaciones en las nueve clases; comprueba además suma, producto, inversión y descomposición iterada en un intervalo entero declarado. Conserva las tablas de los dominios residuales completos y las trazas de ejemplo. Los argumentos universales son las pruebas algebraicas escritas arriba: el muestreo entero y las comprobaciones de matrices no sustituyen esos argumentos ni certifican el conjunto del corpus.

## Localizadores y revisión independiente

En la fuente citada: coordenadas y unicidad, líneas 13–40; operaciones, 43–84; cociclo, 86–98; segundo nivel módulo nueve, 100–125; inversión y memoria, 128–149; reversión de palabras, 150–167; producto, conjugación y norma, 170–233; carta afín y bordes, 277–304. Los rótulos LaTeX conservados permiten remontar estas residencias aunque cambie la paginación.

La revisión matemática independiente de este desglose comprobó las operaciones y pidió explicitar el campo real en TRIT-002.01; la precisión se ha incorporado. La localización formal posterior encontró los teoremas de TRITCore para reconstrucción, unicidad, suma, producto y cociclo. Sus rutas y contratos figuran en CF-005/006 del documento 23. Esa correspondencia no se presenta como una nueva compilación Lean de REV03.
