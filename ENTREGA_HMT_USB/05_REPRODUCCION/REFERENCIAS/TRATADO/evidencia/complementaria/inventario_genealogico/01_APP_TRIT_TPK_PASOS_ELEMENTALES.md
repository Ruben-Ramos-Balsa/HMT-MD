# Construcción elemental de APP, orientación TRIT y transición TPK

Primera lectura desglosada. Fuente principal leída íntegramente: `/Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/sections/nucleo.tex`, 258 líneas. Las inclusiones de otras fuentes se identifican al final: leer el archivo principal no equivale a haber leído automáticamente sus inclusiones.

Procedencia de las fichas: **RESULTADO_RECUPERADO**, salvo los cálculos ilustrativos indicados como ejemplos desarrollados para este inventario. No se reclama novedad matemática. El estatuto de prueba citado es textual; este documento no anuncia una nueva compilación Lean ni una reproducción de todo el núcleo.

## APP-001 — Alfabeto posicional y recta de referencia

- **Objeto:** las nueve marcas interiores \(D_9=\{1,\ldots,9\}\) de la recta graduada entre cero y diez.
- **Acción:** fijar posiciones discretas antes de toda expansión de una constante.
- **Origen de coeficientes:** nueve marcas y dos extremos de referencia; los diez intervalos unitarios no son nueve intervalos.
- **Conservación:** identidad de cada marca, orden y orientación de lectura.
- **Fuente:** núcleo común, líneas 8–15.
- **Consumidor:** producto de posiciones APP-002.
- **Subinventario requerido:** representar gráficamente marcas, extremos e intervalos; distinguir alfabeto, carta y valor final sin comenzar por una expansión real conocida.

## APP-002 — Producto de dos ejes

- **Dominio:** \(D_9\times D_9\).
- **Acción:** formar una celda por cada pareja ordenada; hay \(9^2=81\) celdas.
- **Salida:** soporte bidimensional anterior a sus evaluaciones.
- **Conservación:** coordenada de fila y de columna por separado; intercambiarlas es una operación, no un olvido.
- **Fuente:** líneas 13–19.
- **Consumidores:** las dos hojas aritméticas y las rutas cardinales.
- **Subinventario:** tabla completa de coordenadas; convención gráfica de fila/columna; diferencia entre soporte y matriz de valores.

## APP-003 — Identificación cíclica

- **Mapa:** identificación de posiciones módulo nueve, con soporte \(X_9=(\mathbb Z/9\mathbb Z)^2\).
- **Salida:** soporte cíclico en ambas direcciones.
- **Dato imprescindible:** carta de representantes positivos; el símbolo nueve representa la clase nula.
- **Fuente:** líneas 16–27.
- **Consumidores:** traslaciones, composición de rutas y evaluación residual.
- **Subinventario:** cruce explícito del borde en cada eje y distinción entre posición residual y desplazamiento entero.

## APP-004 — Residuo positivo y raíz digital

- **Dominio de la fórmula escrita:** enteros positivos.
- **Regla:** \(\rho_9(n)=1+((n-1)\bmod9)\).
- **Salida:** representante en \(D_9\), no el resto usual en {0,…,8}.
- **Fuente:** líneas 20–27; fórmula `eq:residuo-cociente`.
- **Ejemplo desarrollado:** \(\rho_9(9)=9\), mientras el resto usual de 9 módulo 9 es 0. La clase es la misma; el representante escrito cambia.
- **Subinventario:** prueba de concordancia con la suma iterada de cifras para enteros positivos, tratamiento separado de cero y extensión a enteros si se utiliza después.

## APP-005 — Cociente exacto de la lectura nonádica

- **Regla:** \(q_9(n)=(n-\rho_9(n))/9\), con \(n=\rho_9(n)+9q_9(n)\).
- **Conservación:** el par residuo–cociente recupera el entero; el residuo solo no lo recupera.
- **Prueba:** identidad por sustitución, líneas 20–27 y 49–54.
- **Ejemplo de fuente:** 10 y 19 comparten residuo 1 y tienen cocientes 1 y 2.
- **Consumidores:** hojas levantadas, acarreo de transporte y registro enriquecido.
- **Subinventario:** tabla con valor bruto, residuo, cociente y reconstrucción para cada entrada APP; no sólo la tabla coloreada residual.

## APP-006 — Hoja aditiva anterior al cociente

- **Mapa:** \(S:D_9^2\to\mathbb Z\), \(S(i,j)=i+j\).
- **Salida:** tabla de sumas enteras antes de aplicar raíz digital.
- **Fuente:** líneas 29–34.
- **Conservación:** celda de origen y valores de ambos ejes.
- **Consumidor:** \(\Sigma=\rho_9\circ S\), con su cociente \(q^+\).
- **Subinventario:** mostrar las 81 evaluaciones y cómo se agrupan por suma; no identificar todavía sus clases residuales.

## APP-007 — Hoja multiplicativa anterior al cociente

- **Mapa:** \(P:D_9^2\to\mathbb Z\), \(P(i,j)=ij\).
- **Fuente:** líneas 29–34, incluida la acumulación repetida que describe el producto.
- **Conservación:** factores, posición y posterior cociente multiplicativo.
- **Consumidor:** \(\Pi=\rho_9\circ P\).
- **Subinventario:** tabla de productos enteros, simetría de factores, multiplicidades y comparación casilla a casilla con la hoja aditiva.

## APP-008 — Evaluación levantada de las dos hojas

- **Mapa:** \(\mathcal A(i,j)=((\rho_9(i+j),q_9(i+j)),(\rho_9(ij),q_9(ij)))\).
- **Tipo:** un soporte con dos evaluaciones; no dos APP independientes.
- **Prueba y fuente:** definición y proposición, líneas 36–54.
- **Conservación:** residuo y cociente de cada hoja, sin intercambiar sus papeles.
- **Ejemplo de fuente:** \(5,5\) y \(8,2\) tienen suma 10 y producto residual 7; sus productos enteros son 25 y 16 y sus cocientes multiplicativos difieren.
- **Subinventario:** desarrollar por completo este ejemplo y registrar qué datos siguen distinguiendo posiciones que una proyección identifica.

## APP-009 — Intercambio de ejes

- **Involución:** \((i,j)\mapsto(j,i)\).
- **Invariantes:** las dos evaluaciones enteras y sus residuos/cocientes.
- **Fuente:** línea 34 y definiciones anteriores.
- **Límite de la afirmación:** la simetría del valor no borra una ruta orientada; la acción sobre rutas requiere su propio transporte.
- **Subinventario:** celdas fijas y parejas no fijas, distinguiendo invariancia aritmética de identidad de posición.

## APP-010 — Cuatro traslaciones cardinales

- **Reglas:** \(\nu_N=(-1,0)\), \(\nu_E=(0,1)\), \(\nu_S=(1,0)\), \(\nu_O=(0,-1)\); \(T_d(x)=x+\nu_d\) en \(X_9\).
- **Convención:** fila aumenta al sur; columna al este.
- **Fuente:** líneas 56–67.
- **Conservación:** origen y dirección de cada paso; el transporte no selecciona por sí solo la hoja.
- **Subinventario:** un ejemplo interior y un ejemplo de cruce de borde para cada dirección; inversas norte/sur y este/oeste.

## APP-011 — Grafo de Cayley y soporte toroidal

- **Objeto:** grafo aditivo de \(X_9\) con los cuatro generadores cardinales.
- **Censo:** 81 vértices y cuatro aristas orientadas salientes por vértice.
- **Fuente:** líneas 63–67.
- **Distinción indispensable:** esta estructura de grupo es aditiva; las filas multiplicativas no son todas permutaciones porque existen divisores de cero.
- **Subinventario:** separar el grafo finito, la identificación de bordes y cualquier realización continua del toro; conservar el mapa entre las representaciones.

## APP-012 — Palabra de transporte y censo de rutas

- **Datos:** origen \(x_0\) y palabra \(d_1\cdots d_r\).
- **Acción:** \(x_k=x_0+\sum_{j=1}^k\nu_{d_j}\pmod9\).
- **Censo:** \(81\cdot4^r\), con retornos y retrocesos permitidos.
- **Fuente:** líneas 69–73.
- **Subinventario:** justificar el producto combinatorio; diferenciar rutas de extremos alcanzados y rutas admitidas por restricciones posteriores del TPK.

## APP-013 — Enrollamiento de una ruta cerrada

- **Dominio:** rutas cuyo extremo residual coincide con el origen.
- **Lector:** \(\operatorname{wind}(w)=((\#S-\#N),(\#E-\#O))/9\in\mathbb Z^2\).
- **Fuente:** líneas 73–78.
- **Conservación:** desplazamiento entero previo a la reducción; invertir la ruta cambia su signo.
- **Subinventario:** comparar una vuelta de nueve pasos hacia el este con un retroceso local; ambos pueden cerrar la posición, pero no tienen el mismo enrollamiento.

## APP-014 — Cociclo de acarreo del transporte

- **Dato:** sección positiva \(s_9:\mathbb Z/9\mathbb Z\to D_9\).
- **Regla:** \(c_9(a,b)=(s_9(a)+s_9(b)-s_9(a+b))/9\).
- **Fuente:** líneas 80–100.
- **Prueba:** la suma de dos acarreos por cualquiera de las asociaciones de tres términos tiene el mismo numerador.
- **Invariante:** compatibilidad del registro de acarreo con concatenación/asociatividad.
- **Subinventario:** expandir ambas asociaciones paso a paso y conservar todos los términos de sección, no sólo enunciar «hay memoria».

## APP-015 — Cambio de sección y normalización del cociclo

- **Hecho:** con representantes positivos, \(c_9(0,a)=1\).
- **Cambio:** sección \(s_0\) en {0,…,8}; \(c_9=c_0+\mathbf1_{a=0}+\mathbf1_{b=0}-\mathbf1_{a+b=0}\).
- **Fuente:** líneas 102–107.
- **Salida:** mismo contenido composicional en coordenadas diferentes.
- **Subinventario:** casos con y sin clase nula; explicar qué se normaliza y por qué no debe perderse el término de corrección.

## APP-016 — Totales de las tablas antes y después del cociente

- **Valores de fuente:** ∑S=810, ∑P=2025, ∑Σ=405, ∑Π=459; ∑q⁺=45, ∑q×=174.
- **Fuente:** líneas 109–120.
- **Dependencias:** APP-005 a APP-008.
- **Subinventario:** seis cómputos individualizados, cada uno con suma por filas y total; la mera presencia de las seis cifras no reemplaza el cálculo.

## APP-017 — Descomposición exacta de la diferencia suma–producto

- **Identidad:** \(2025-810=(459-405)+9(174-45)=54+9\cdot129\).
- **Fuente:** líneas 116–121.
- **Conservación:** defecto visible 54 y defecto de cociente 129, ambos procedentes de la misma evaluación levantada.
- **Subinventario:** enlazar la identidad global con la identidad casilla a casilla; no atribuir al 54 por sí solo todo el contenido aritmético.

## APP-018 — Unidades y sector no invertible

- **Objeto:** anillo \(R=\mathbb Z/9\mathbb Z\).
- **Clases:** unidades {1,2,4,5,7,8} e ideal {0,3,6}.
- **Fuente:** líneas 123–129.
- **Efecto:** toda fila aditiva es una permutación; una fila multiplicativa lo es exactamente para índices invertibles.
- **Subinventario:** determinar inversas de las seis unidades; mostrar las filas 3, 6 y 9 y sus multiplicidades.

## APP-019 — Nilpotencia y dos lecturas de 3/6/9

- **Mapa:** \(x\mapsto3x\), cuyo núcleo e imagen coinciden con {0,3,6}; el cuadrado del ideal es cero.
- **Mapa inducido:** \(R/\mathfrak m\to\mathfrak m\) como espacios sobre \(\mathbb F_3\), no como anillos.
- **Fuente:** líneas 125–135.
- **Distinción:** reducción directa módulo tres de 3,6,9 da 0,0,0; la lectura interna \([3k]_9\mapsto[k]_3\), que extrae el factor tres antes de reducir, da 1,2,0.
- **Subinventario:** escribir ambos recorridos completos y sus dominios. No llamar a ambos «módulo tres» sin explicar la operación adicional.

## APP-020 — Realización operatoria de la hoja aditiva

- **Construcción:** base \(e_r\) de \(\mathbb C^9\); \(v_{ab}=e_{a+b}\); \(P_{ab}=v_{ab}v_{ab}^*\).
- **Resultado:** proyectores de rango uno con sumas de fila y columna iguales a identidad.
- **Fuente y prueba:** líneas 137–154; la traslación permuta los nueve residuos.
- **Orden causal:** primero hoja aditiva, después representación en espacio con producto interno.
- **Subinventario:** definir base, producto interno, proyector y suma, exhibiendo un ejemplo completo. El nombre «Hilbert» no reemplaza este mapa.

## APP-021 — Multiplicidad operatoria de la hoja multiplicativa

- **Caso:** \(a=3\), con \(e_{3b}\) repitiendo 0,3,6.
- **Identidad:** suma de proyectores igual a tres veces la suma sobre esos tres vectores.
- **Fuente:** líneas 155–166.
- **Salida:** operador que retiene multiplicidad, distinto de la resolución de identidad aditiva.
- **Subinventario:** rango, soporte y multiplicidades; comparación con APP-020 sin identificar las dos hojas por su mismo tamaño.

## TRIT-001 — Firma balanceada y acarreo ternario

- **Regla:** 0→0, 1→+1, 2→−1; conservación \(n=r+3c\).
- **Fuente:** líneas 168–178.
- **Distinción:** firma, trayectoria y acarreo son datos diferentes. Igual residuo nulo admite distintos acarreos.
- **Subinventario:** ejemplos positivos y negativos; prueba de unicidad con representantes balanceados; relación con la reducción de emisiones posterior.

## TRIT-002 — Tres realizaciones cuadráticas

- **Objeto posterior a la firma:** \(\mathbb A_\tau=\mathbb R[X]/(X^2+\tau)\), \(J_\tau^2=-\tau I\).
- **Tipos:** elíptico \(+1\), parabólico \(0\), hiperbólico \(−1\).
- **Fuente:** líneas 180–187.
- **Subinventario:** definir cada álgebra, multiplicación y representación; no identificar automáticamente tipo algebraico con toda una geometría física.

## TRIT-003 — Exponenciación y conservación cuadrática

- **Regla:** separación de potencias pares e impares de \(\exp(tJ_\tau)\).
- **Prueba:** líneas 189–224, incluyendo \(C_\tau^2+\tau S_\tau^2=1\).
- **Distinción:** la exponencial realiza los tres regímenes; no es por sí misma el productor regional de la constante e.
- **Subinventario:** tres derivaciones particulares, convergencia o lectura formal pertinente, inversión \(t\mapsto-t\) y coordenadas que conservan la unidad.

## TRIT-004 — Direcciones hiperbólicas y lectura temporal

- **Operadores:** \(P_\pm=(I\pm J_{-1})/2\); expansión \(e^tP_++e^{-t}P_-\).
- **Fuente:** líneas 217–224.
- **Convención temporal HMT:** +1 retorno/memoria; 0 umbral; −1 apertura bidireccional.
- **Subinventario:** complementariedad de proyectores, signo de orientación y orden de parametrización; separación entre convención temporal y demostración algebraica.

## TPK-001 — Selector trítico de fase operativa

- **Función:** \(M_{\rm ph}\) vale +1 en {1,4,7}, −1 en {2,5,8} y 0 en {3,6,9}.
- **Fuente:** líneas 230–241.
- **Efecto:** selecciona evaluación o umbral; no desplaza el cursor.
- **Subinventario:** nueve evaluaciones; función frente a vector de valores; relación con modo activo y hojas.

## TPK-002 — Campos del estado enriquecido

- **Objeto:** posiciones/direcciones de cursores, modo, firma TRIT, fase, residuos, cocientes, acarreos, prefijo y frontera; el cilindro se añade cuando se introduce refinamiento.
- **Fuente:** líneas 241–243 y grafo tipado OP12.
- **Subinventario:** ficha por campo con tipo, inicialización, regla de actualización, operador que lo consume y proyección que lo olvida. Una lista de nombres no cumple este desarrollo.

## TPK-003 — Composición de selección, transporte y actualización

- **Regla:** \(\mathcal U_t=\mathsf{Mem}_t\circ\mathsf{Tra}_t\circ\mathsf{Sel}_t\); el grafo permanente usa `Upd_t` para la actualización conjunta.
- **Fuente:** líneas 245–257; grafo dinámico SEL_T, TRA_T, UPD_T y U_T.
- **Orden:** seleccionar modo, transportar, actualizar registros. La composición nominal remite a reglas finitas que se inventariarán aparte.
- **Subinventario:** un paso calculado completo con todos los campos antes/después y reglas para campos invariantes; después, composición de varios pasos y retorno.

## APP-022 — Carta base 1000: localizador distinto de la tabla residual

- **Definición registrada:** división euclídea en cociente y resto \(0\le r<1000\), OP04_IOTA1000 del grafo permanente.
- **Dependencias a reunir:** carta cruzada ternaria/base1000 OP14, emisión decimal SR y calendario de conversión CG.
- **Estado documental:** la definición está localizada; esta ficha todavía no reúne todas sus realizaciones y pruebas propietarias.
- **Subinventario exigido por el añadido autoral:** tabla bruta, carta base1000 y raíz digital se mostrarán como operaciones diferentes, con ejemplos. No se afirmará que «sólo cambia una ruta» sin localizar y calcular el mapa de esa ruta.

## Lectura material y ampliaciones pendientes de este bloque

Leído íntegramente: el archivo principal `sections/nucleo.tex` y el grafo tipado permanente. La copia JSON íntegra del grafo queda en el censo; su transcripción no equivale a nueva verificación de todos sus propietarios.

Inclusiones que necesitan su propia ficha y lectura: `figures/app.tex`, `sections/trit_desarrollo.tex`, `figures/regimenes_trit.tex`, `sections/tpk_desarrollo_integrado.tex`, `sections/memoria_resolvente.tex`. Debe cotejarse la misma materia en las introducciones de I–X y en el integral, la síntesis, la cadena compacta y el reservorio; no se declara esa concordancia terminada.

Este bloque contiene 29 fichas, incluida la ficha de enlace base1000: el desarrollo posterior debe subdividirlas, no usarlas como excusa para sustituir tablas, pruebas o ejemplos por una lista breve.
