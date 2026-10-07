# Primera revisión individual: primos y zeta

Fecha: 11 de septiembre de 2026. Entrada: REV03, 153 páginas, SHA-256
`7ce8c01ad7349dc83591a6618784f4d1777eb0754e916736e4b62cc7aeb56d1f`.

## Evaluación editorial

El artículo contiene más desarrollo del que deja ver su apertura. Su problema
de jerarquía no es falta de material: la aritmética, el centro, las vacancias,
el calendario y los lectores compiten en el anuncio con el objetivo espectral.
La pregunta rectora debe ser la positividad de la forma completa de Weil y la
función que cumple cada construcción para llegar a ella.

La prueba funcional de Schur sí trata un espacio infinito de detalles. No debe
presentarse como una comprobación de unas cuantas funciones ni, en sentido
contrario, como una demostración de positividad global. El propio manuscrito
recibido distingue estos alcances y declara que no concluye RH. He conservado
esa declaración; no la he añadido como una rebaja nueva del artículo.

## Cambios aplicados en la copia LaTeX

1. **Introducción centrada en la pregunta y el resultado.** Los primeros dos
   párrafos anuncian la reducción exacta de Schur, la ventana completa de
   longitud 1/9, los transportes y el requisito de identificación global.
   La demostración conserva su orden genealógico.
   [Introducción revisada](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_SERIE_HMT_20260911/PRIMERA_ENTREGA/PRIMOS_Y_ZETA/gestion/lectura_introduccion.tex:1>).

2. **Un mapa en lugar de otro resumen extenso.** Cinco niveles diferencian
   construcción común, aritmética y funcional, reconstrucción y transporte,
   signo, y criterio global. Cada nivel remite a pruebas incluidas. Se
   conservan centro, vacancias, 555555, tres hojas y calendarios como
   instrumentos del argumento, no como resultados espectrales intercambiables.
   [Mapa de resultados](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_SERIE_HMT_20260911/PRIMERA_ENTREGA/PRIMOS_Y_ZETA/gestion/lectura_resumen.tex:1>).
   Su ajuste visual queda pendiente de compilación.

3. **Conclusiones en orden de importancia.** Primero aparece el resultado de
   positividad y su dominio; después, los antecedentes aritméticos y los
   mecanismos de reconstrucción; al final, la condición global. No se han
   eliminado los resultados singulares de las conclusiones anteriores.
   [Conclusiones revisadas](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_SERIE_HMT_20260911/PRIMERA_ENTREGA/PRIMOS_Y_ZETA/gestion/lectura_conclusiones.tex:1>).

4. **Remisiones y lenguaje temporal.** Se sustituyeron once remisiones
   manuales o relativas del capítulo espectral por etiquetas; se retiraron
   anuncios de «primera redacción» y de capítulos que ya están integrados.
   Se corrigió el anuncio de que faltaba incorporar gamma y concordancias
   como «el álgebra» y «el límite inverso».

5. **Diccionario Mellin–Fourier incorporado.** Se desarrolla la biyección de
   pruebas compactas, su inversa y las identidades de transformadas y
   conjugación. Así no queda oculta la normalización del reconocimiento
   clásico. La fórmula explícita y la dirección difícil del criterio siguen
   atribuidas a su antecedente, no a ese cambio de variables.
   [Desarrollo incorporado](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_SERIE_HMT_20260911/PRIMERA_ENTREGA/PRIMOS_Y_ZETA/gestion/lectura_generada/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.tex:403>).
   Procedencia: [monografía terminal, cambio de pruebas](</Users/ruben/Documents/HMT2/PDF_2_RESOLUCIONES_EXTENSAS_RH_NS_YM_HODGE_BSD_2026-08-19/manuscrito/secciones/02_riemann_weil.tex:771>).
   Se añadió la entrada bibliográfica de Bombieri; título, volumen y páginas
   se cotejaron con la [publicación original](https://www.bdim.eu/item?id=RLIN_2000_9_11_3_183_0).

6. **Guías históricas identificadas como tales.** Dos entradas seguían
   anunciando 107 páginas y una modificación exclusiva de portada. Ahora
   advierten que sus constructores pueden regenerar fuentes anteriores.
   La entrada de esta propuesta es
   [LEER_REVISION_EDITORIAL](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_SERIE_HMT_20260911/PRIMERA_ENTREGA/PRIMOS_Y_ZETA/LEER_REVISION_EDITORIAL.md>).

## Corrección matemática puntual: regularidad y representación límite

La sección de momentos construye primero un desplazamiento bilateral regular
S. Más adelante propone identificar los momentos aritméticos mediante ese
mismo símbolo, aunque ya ha distinguido el límite débil atómico del límite
vectorial regular. La notación debía corregirse.

Para S sobre ℓ²(Z;K), una ecuación Sx=λx, |λ|=1, obliga a que todas las
coordenadas tengan la misma norma. La sumabilidad fuerza x=0. En consecuencia,
una representación con un vector propio no nulo no puede entrelazarse
isométricamente con S. El GNS aritmético atómico, si se satisfacen las
hipótesis globales que lo construyen, tiene esos vectores.

La propuesta distingue por ello un espacio límite K_lim y una vuelta unitaria
U_mem, cuya construcción desde las historias sigue formando parte del enlace
prospectivo. Se conservan íntegros S, los momentos q^|n|, su factorización y
las pruebas de convergencia de estados. **No se afirma haber construido
K_lim ni el lector global.**
[Precisión y prueba breve](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_SERIE_HMT_20260911/PRIMERA_ENTREGA/PRIMOS_Y_ZETA/ampliacion/transporte_y_momentos.tex:587>).

El cotejo no se limitó a una búsqueda nominal: el capítulo espectral del
integral y la monografía de cinco problemas se contrastaron en los operadores
pertinentes. La monografía recibe las dos identidades de Gram del lector
estructural y la recurrencia del residual; su anulación es válida con esos
datos. Esos enunciados no construyen, por sí solos, la identificación del
nuevo lector regular. Recuperarlos exige conservar ese tipo de lector, no
traspasar automáticamente su conclusión.
[Dos momentos del antecedente](</Users/ruben/Documents/HMT2/PDF_2_RESOLUCIONES_EXTENSAS_RH_NS_YM_HODGE_BSD_2026-08-19/manuscrito/secciones/02_riemann_weil.tex:269>).

## Fuerza de los resultados conservados

| Resultado | Qué establece | Qué no sustituye |
|---|---|---|
| Cola gamma | Reconstrucción mediante un conector acotado | Contractividad automática de ese conector |
| Momentos de memoria | Grams positivos para toda dimensión y terminal explícito | Identidad de los momentos aritméticos completos |
| Reducción de Schur | Signo de una ventana mediante su acoplamiento finito exacto | Eliminar sin control el espacio infinito de detalles |
| Ventana 1/9 | W(f,f) ≥ 1/2 ||f||² para todo el dominio indicado | Positividad de todas las combinaciones entre ventanas |
| Cayley integral | Conservación de los tres canales sobre el dominio exponencial | Estabilidad del dominio compacto bajo ese operador |
| Reconocimiento de Weil | Criterio global con todas las pruebas y multiplicidades | Probar la premisa global con una muestra finita |

Residencia principal: [Schur y coercividad](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_SERIE_HMT_20260911/PRIMERA_ENTREGA/PRIMOS_Y_ZETA/ampliacion/schur_y_coercividad.tex:210>).
La condición de prolongación global ya estaba impresa en el original; si
la intención autoral es que este artículo publique una resolución de RH,
la tarea científica prioritaria es incorporar la identificación completa
con su cobertura, no cambiar sólo el resumen o el título.

## Comprobaciones de esta entrega

El equipo recorrió las inclusiones matemáticas activas, no sólo el resumen.
Se reprodujeron, sin escribir sobre los originales:

- Schur normal y optimizado: 21/21 en cada modo.
  η > 1, A > 0,97 y ||B||² < 0,2; cota funcional 1/2.
- Momentos racionales de memoria: 1.046/1.046 en cada modo;
  819 entradas LDL, 13 determinantes, 210 correlaciones truncadas y cuatro
  identidades de factores polares.
- Expectativas de modos: 25/25.

El inventario local recorre 37 archivos activos: 161 marcadores de enunciado
o prueba, sin etiquetas eliminadas, duplicadas ni remisiones sin destino.
Los 719 bloques matemáticos separados originales pasan a 723: se sustituye
una expresión prospectiva S→U_mem y se añaden cuatro identidades del
diccionario. No se han eliminado teoremas. Este conteo es documental,
no una verificación formal de las pruebas.

## Pendientes para una edición publicable

- Revisar visualmente la tabla, los cortes de página y las remisiones al
  compilar el corte sucesor.
- Unificar la numeración de enunciados manuales y automáticos sin perder
  correspondencia con antecedentes.
- Corregir transversalmente el anuncio del «capítulo electrónico» en el
  TRIT compartido: en este artículo no existe ese capítulo posterior.
  No he modificado aisladamente los seis archivos comunes.
- Para cerrar RH dentro de este manuscrito, incorporar la prueba del enlace
  global descrito, con su representación límite y todos los productos mixtos.

Los cambios son una propuesta materializada, no una nueva edición PDF
certificada. Originales, resultados anteriores y recibos históricos
permanecen intactos.

