# Aritmética genealógica de los números primos y estructura espectral de la función zeta

Responsable editorial: tarea «Aclarar la tarea». Esta sucesora conserva el contenido
del manuscrito anterior y modifica únicamente su presentación pública. Como
antecedente de planificación, el título y la numeración de aquel encargo eran
provisionales; el Artículo VII, sobre gravitación, torsión y dinámica cosmológica,
permanecía a cargo de «Ley 9 puertas». El radión no se incorpora como artículo
independiente en este encargo.

## Entrega actual: PDF y fuentes

El PDF está en [Aritmética genealógica de los números primos y estructura espectral de la función zeta](output/pdf/ARITMETICA_GENEALOGICA_PRIMOS_Y_ESTRUCTURA_ESPECTRAL_ZETA.pdf).
El [paquete completo de esta presentación](../ARITMETICA_GENEALOGICA_PRIMOS_PRESENTACION_20260911_0d5bd4fdd195.zip)
reúne ese PDF, fuentes, pruebas, antecedentes y recibos. Su
[comprobación de extracción e integridad](../ARITMETICA_GENEALOGICA_PRIMOS_PRESENTACION_20260911_0d5bd4fdd195_INTEGRIDAD.json)
corresponde a esta misma versión; el ZIP anterior permanece como antecedente.
Reúne el núcleo común, los cinco capítulos y los antecedentes demostrativos
seleccionados en apéndices. El manuscrito no se presenta como una demostración
cerrada de la hipótesis de Riemann. El título no anuncia esa resolución.
La procedencia privada queda documentada en este paquete, separada de las pruebas
que se han reunido dentro del PDF.

El avance de esta entrega está en las secciones 14–15 del capítulo 03:
coercividad de la forma completa para cualquier función del dominio soportada
en nueve intervalos, control uniforme de sus refinamientos, y coercividad de
los detalles de media nula en cualquier ventana fijada, con umbral explícito.
La positividad global de Weil no se da por demostrada.

Para leer, basta el PDF. Para reproducir, descomprimir el ZIP completo y mantener
su estructura de carpetas. No se necesitan las carpetas de otros artículos:
los propietarios usados por el ensamblador están copiados en `antecedentes/`.

Requisitos: Python 3.9 o posterior y `mpmath` (los controles se ejecutaron con
1.3.0); LuaLaTeX con TeX Live, `fontspec`, `unicode-math`, TikZ y las familias
STIX Two Text/STIX Two Math para recompilar. Los scripts no instalan dependencias.

```sh
python3 gestion/reproducir_lote_reanudacion.py
python3 gestion/construir_lectura.py --compile --passes 3
```

El primer comando ejecuta seis controles en modo normal y optimizado. El segundo
convierte sin resumir los cinco capítulos y compila el PDF. El control de fórmulas
se efectúa antes de dos cambios puramente tipográficos de intervalos largos.
Los recibos documentales no reemplazan las demostraciones analíticas del texto.
Las herramientas históricas que incluyen rutas absolutas del corpus se conservan
para procedencia: no forman parte de esos dos comandos portables.

El comando de compilación utiliza `main_lectura.tex` y `preambulo_lectura.tex`
de esta carpeta; no los regenera. Conserva el título temático, los autores, la
identificación HMT–MD y el alcance matemático, y publica el nombre de PDF indicado
arriba, sin reintroducir los rótulos retirados de portada, cabecera y metadatos.
Los nombres técnicos heredados de los scripts y recibos se mantienen para no
alterar las instrucciones de reproducción.

El [análisis focal posterior sobre la recuperación generativa de Weil](gestion/RECUPERACION_GENERATIVA_WEIL_20260911.md)
se conserva como documento separado. No se ha incorporado al PDF ni modifica
el contenido o las delimitaciones matemáticas de esta entrega.

## Qué contiene esta carpeta

- `manuscrito/01_CONSTRUCCION_ARITMETICA.md`: primera redacción matemática propia del artículo, con definiciones, operaciones y pruebas del sector de formas normales.
- `manuscrito/02_ORDEN_ESPECTRAL_Y_MOMENTOS.md`: enlace demostrativo con los relojes, la factorización, los momentos y las dos realizaciones circulares; distingue los dominios de cada operación.
- `manuscrito/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.md`: forma completada, transformada de Mellin, columnas, consecuencias de los dos momentos, doble círculo, pesos cilíndricos, memoria y aproximación espectral. Las secciones 12–15 reúnen el conector gamma global, su norma, la factorización basal, el pliegue previo, el control de nueve ventanas, el ensamblaje de nueve intervalos y los detalles de media nula. Contiene veinticuatro resultados numerados con sus pruebas y condiciones.
- `manuscrito/04_PARTES_FINITAS_Y_LECTORES_RESIDUALES.md`: partes finitas, Euler–Mascheroni, Apéry, Stieltjes, clases residuales y evaluación regularizada de −1/12, con cotas explícitas y productor racional.
- `manuscrito/05_CONSTRUCCION_CORRELATIVA_DEL_CONTINUO.md`: árbol común, cociclo, medida de historias, transporte por hojas, balance, incidencia, complejo de memoria y ensamblaje terminal, con sus pruebas locales.
- `sections/01_*.tex` a `sections/05_*.tex`: conversión tipográfica de los cinco capítulos; el recibo conserva las ecuaciones en bloque literalmente. No constituye una compilación.
- `gestion/CONTINUIDAD_TRAS_RECARGA.md`: avances de esta reanudación, composición espectral delimitada y reparto confirmado con la otra tarea.
- `gestion/INTEGRACION_CAPITULO_03_Y_ALCANCE.md`: propietarios leídos, incorporaciones, correcciones de multiplicidad y contracción, y dependencias todavía no reunidas.
- `gestion/RECUPERACION_COLA_GAMMA_Y_ENSAMBLE.md`: continuación que actualiza aquel alcance. La acción global entre las dos columnas está recuperada; la contractividad global sobre su imagen efectiva se mantiene separada del resultado basal y del Gram finito de nueve ventanas.
- `gestion/PROYECTO_EDITORIAL.md`: jerarquía del artículo completo, destinos y límites temáticos.
- `gestion/REUNIR_FUENTES.py`: copia conservativa de propietarios y del núcleo común, con huellas y procedencia.
- `antecedentes/`: copias literales de los propietarios; su conservación no equivale a incorporación al manuscrito ni a verificación de todos sus teoremas.
- `fuente/pruebas/python/`: productor nativo y comprobadores conservados, más los nuevos evaluadores racionales y controles locales, identificados por sus nombres y recibos.
- `fuente/certificados/`: resultados de la ejecución realizada en esta carpeta, separados de los recibos heredados.

Esta carpeta contiene el **PDF y sus fuentes**, no una prueba global cerrada.
No se han modificado ni sustituido los artículos I–VI. Tampoco se declara aquí
reproducida la totalidad de la demostración terminal de Riemann–Weil por haber
ejecutado controles finitos del producto nativo.

## Orden de lectura y ejecución

1. Leer `gestion/PROYECTO_EDITORIAL.md`.
2. Consultar el núcleo común y después `05_CONSTRUCCION_CORRELATIVA_DEL_CONTINUO.md`, antes del sector aritmético. La numeración del archivo conserva su orden de redacción, no fija aún su posición en el índice del PDF.
3. Leer el capítulo de construcción aritmética y `fuente/pruebas/python/a9_native.py`.
4. Ejecutar, desde esta carpeta:

   ```sh
   python3 -S fuente/pruebas/python/generar_certificado_producto_nativo.py
   python3 -S fuente/pruebas/python/auditar_producto_nativo.py --write
   ```

5. Leer el capítulo espectral. La generación del conjunto de irreducibles precede a
   los cálculos sobre ese conjunto. Una criba convencional sólo puede actuar como
   comprobación posterior, nunca como sustituto del productor nativo.
6. Para el bloque de Riemann–Weil, leer el capítulo 03, que reúne la forma y sus
   lectores; los propietarios de capítulos 96 y 97 se conservan como antecedentes
   de procedencia. Una identidad de contracción no sustituye la identificación de
   la forma aritmética completa con el operador de frontera.
7. Leer las partes finitas después de los modos enteros. Ejecutar
   `python3 gestion/reproducir_lote_reanudacion.py` para los controles nuevos,
   sus variantes optimizadas y la conversión literal a LaTeX. Este conjunto
   requiere `mpmath` en el comprobador posterior de valores y en la evaluación
   intervalar del Gram completo. El productor nativo usa enteros; las cotas de
   partes finitas usan fracciones de la biblioteca estándar. El Gram consume
   esas cotas y la publicación nonádica de pi, conservada con su huella:
   `mpmath` evalúa las operaciones posteriores, no selecciona los irreducibles
   ni aporta un valor objetivo para la forma.

8. Leer las secciones 12–13 del capítulo 03 en su orden: inversión de cola,
   norma, dominio basal, pliegue, Gram completo y detalles de refinamiento.
   `verificar_cola_y_pliegue.py` comprueba identidades finitas exactas;
   `verificar_gram_nueve_ventanas.py` comprueba el Gram completo de las
   nueve ventanas declaradas. Ninguno sustituye la estimación uniforme
   sobre todas las ventanas y todos sus refinamientos.

9. Leer las secciones 14–15. `verificar_nueve_intervalos_coercividad.py`
   evalúa las cotas demostradas de interacción para los nueve intervalos;
   no infiere una afirmación infinito-dimensional de un muestreo de funciones.
   El teorema de detalles de media nula se demuestra analíticamente mediante
   primitivas por celdas y una suma gamma positiva. Su constante escalar
   `mathfrak c_R` es distinta del conector `mathcal C_R`.

10. Los apéndices del PDF contienen las reglas y pruebas del núcleo heredado
    que se han reunido para la lectura. `MANIFIESTO_ANTECEDENTES_LECTURA.json`
    registra los nueve archivos propietarios íntegros, los fragmentos incorporados
    y las sustituciones editoriales. Un censo conservado no se confunde con una
    nueva certificación matemática global.

El script de reproducción no acepta valores objetivo ni una tabla metrológica
como argumentos de los productores. Tampoco certifica la positividad de Weil:
los resultados finitos y el alcance de cada prueba permanecen separados.

Los programas ejecutan una prueba computacional finita. Sus recibos incluyen su
alcance exacto y mantienen las distinciones del corpus entre formas normales,
historias completas y realización espectral.

## Regla de continuidad

La cadena es: rectas de partida → APP → TRIT → TPK → estado con sus coordenadas
genealógicas → estructura discreta conjunta del continuo → salida HMT–MD →
reconocimiento posterior. Las cinco construcciones del continuo permanecen unidas.
Los seis archivos del núcleo común se copian literalmente; cualquier desarrollo
específico de este manuscrito se sitúa fuera de esos archivos.

La procedencia de esta primera redacción es `RESULTADO_RECUPERADO`: reúne y explica
construcciones ya presentes en el corpus. Las demostraciones elementales desarrolladas
en los capítulos no se atribuyen como descubrimientos nuevos.
