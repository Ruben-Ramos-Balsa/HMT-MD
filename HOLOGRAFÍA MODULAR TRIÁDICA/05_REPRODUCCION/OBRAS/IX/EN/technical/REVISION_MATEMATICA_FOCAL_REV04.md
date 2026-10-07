# Revisión focal del delta analítico

## Corte y autorización

Esta revisión integra las propuestas que el autor ha solicitado aplicar desde
`REVISION_SERIE_HMT_20260911`. La entrada congelada es el PDF REV03 de
153 páginas, SHA-256
`7ce8c01ad7349dc83591a6618784f4d1777eb0754e916736e4b62cc7aeb56d1f`.
No se atribuye al autor una aprobación de huellas que aún no existían.

Las demostraciones y los dominios del núcleo APP–TRIT–TPK se conservan.
La revisión no añade una selección de constantes, ceros ni datos físicos.
Actúa sobre los lectores analíticos posteriores y su exposición.

## Diccionario Mellin–Fourier

Residencia: `gestion/lectura_generada/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.tex`,
etiqueta `rz:mellin-fourier`.

Procedencia: RESULTADO_RECUPERADO. El propietario es
`/Users/ruben/Documents/HMT2/PDF_2_RESOLUCIONES_EXTENSAS_RH_NS_YM_HODGE_BSD_2026-08-19/manuscrito/secciones/02_riemann_weil.tex`,
ecuaciones `eq:pdf2-rh-cambio-mellin` a `eq:pdf2-rh-mellin-involucion`.

La prueba incluida establece lo siguiente:

1. El cambio exponencial transporta cada soporte compacto de la recta a un
   compacto de la semirrecta positiva, separado de cero. Su inversa logarítmica
   tiene la misma propiedad en sentido contrario.
2. Los factores `x^(-1/2)` y `exp(t/2)` se cancelan exactamente en ambas
   composiciones. La aplicación es una biyección entre las clases completas
   de pruebas suaves compactas, no entre muestras seleccionadas.
3. Al sustituir `x=exp(t)`, el exponente de Mellin queda `s-1/2`.
   Con Fourier definido por `exp(-i z t)`, el argumento correcto es
   `i(s-1/2)`. Sobre la recta crítica es `-gamma`.
4. La conjugación en `1-s` produce `conj(Phi_g(1-conj(s)))`.
5. Integración por partes en una banda vertical compacta da decaimiento
   arbitrario en altura. Junto con el recuento `O(T log T)` de ceros,
   justifica la convergencia absoluta del sumando bilineal.

El cambio de variables prueba el transporte del dominio y su normalización.
La fórmula explícita y el criterio global mantienen su atribución a la fuente
externa citada. No se presenta este diccionario como prueba de positividad.

## Representación regular y representación límite

Residencia: `ampliacion/transporte_y_momentos.tex`, etiqueta `tm-add-m7`.
Procedencia: FORMALIZACION_NUEVA de una distinción necesaria en el lector
prospectivo de la edición recibida. No se atribuye novedad al hecho clásico
sobre el desplazamiento bilateral.

El desplazamiento `S` sobre `l2(Z;K)` es unitario. Si tuviera un vector propio
no nulo, su autovalor tendría módulo uno; la recurrencia de coordenadas
impondría norma constante a todas las componentes. Su sumabilidad cuadrática
fuerza que todas sean cero. En consecuencia, una representación con un vector
propio no nulo no tiene un entrelazador isométrico hacia ese desplazamiento.

Esta observación no invalida el límite débil de estados: un límite débil de
estados no es necesariamente un vector del espacio regular de partida. La
representación que recibe aquel límite debe especificarse en su propio tipo.

La ecuación prospectiva usa por ello `U_mem` sobre `K_lim`, en lugar de
identificarlo de antemano con `S`. La energía de momento cero y el
entrelazamiento producen los momentos positivos; la invariancia del dominio
y la inversa de Cayley proporcionan los negativos. La energía de momento
cero sigue siendo una igualdad por establecer para esa identificación global.

## Alcance de los controles

Un cotejo independiente y una lectura del editor han encontrado concordancia
de las fórmulas anteriores, sus signos y sus dominios. Se conservan por
separado los controles ejecutables de Schur, de las matrices racionales de
memoria y de las expectativas nonádicas. Sus resultados verifican los objetos
que declaran; no sustituyen las pruebas generales del diccionario o del
desplazamiento, ni certifican positividad global de Weil.

La corrección del espacio de representación se registra como sustitución
tipada de una fórmula prospectiva, no como eliminación de las identidades
anteriores sobre memoria. El estado científico del alcance global de REV03
se conserva. La revisión no dicta una ausencia del resultado en todo el corpus.
