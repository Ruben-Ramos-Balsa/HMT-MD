# Incorporación focal: período de K y conjugación incidencial

Fecha editorial: 10 de septiembre de 2026. Estatuto: **RESULTADO_RECUPERADO**.
Se añaden dos desarrollos a `sections/09_dependencias_anteriores.tex`, conservando
el resto del archivo. No se modifican el núcleo común, los artículos anteriores,
las puertas de aceptación ni la selección del libro terminal. No se compila en
esta subtarea.

## 1. Período mínimo de la coordenada racional

Fuente leída íntegramente en el cotejo previo:

`/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910/sections/registro_k.tex`

Localizador: líneas 486–514, `prop:k-periodo` y su demostración. Se recupera
la prueba de período mínimo de doce bloques y treinta y seis cifras, después
de la definición de la publicación racional en VI. La prueba emplea el
registro ya construido, sus doce componentes distintos y la agrupación de
cifras de tres en tres. No atribuye ese período a la salida completa de alfa.

Destino: `vi:dep:periodo-minimo-k`. La igualdad entre las lecturas finita y
periódica no se afirma: su diferencia exacta ya estaba preservada en VI.

## 2. Conjugación de recuentos y frontera de una ruta

Fuente leída íntegramente:

`/Users/ruben/Documents/New project/output/ARTICULO_V_REV02_EDICION_INTEGRADA_20260910/manuscrito/sections/registro_incidencias.tex`

Localizador: líneas 99–133, `subsec:registro-conjugacion-incidencial` y
`eq:registro-conjugacion-decimal`. Se conserva la conjugación declarada:
reversión de ventanas, conservación de clase aritmética y etiqueta de frontera,
intercambio de canales. Se explicitan las biyecciones y multiplicidades que
permiten transportar las sumas. No se identifica esa conjugación con cualquier
involución de rutas sin comprobar su acción sobre el libro.

Se conserva la fórmula de reducción decimal. Para no confundir la coordenada
con los cocientes de normalización de alfa, `[C_m]_10` se denomina `u_m` en
esta incorporación. La demostración explicita asimismo el cociente de la
división euclídea de `-C`. La identidad de frontera se demuestra por cambio
de índices y se aplica antes de la reducción decimal. Las trazas que cruzan
una unión remiten a la partición ya demostrada en
`vi:dep:libro-actualizacion`.

Destinos: `vi:dep:conjugacion-incidencial`, `vi:dep:conjugacion-recuentos`,
`vi:dep:conjugacion-bloque`, `vi:dep:conjugacion-frontera`.

## 3. Control y alcance

`technical/verificar_periodo_conjugacion_k_vi_rev02.py` lee el testigo de K
de la fuente activa; comprueba su período por desplazamiento de bloques,
de cifras y por congruencias sobre el denominador racional reducido. Además
comprueba las fórmulas de residuo/cociente/bloque conjugados sobre 6300 ternas,
la involutividad del registro de doce ventanas y la identidad de frontera
sobre 1092 secuencias finitas, con controles negativos de lectura finita y de
omisión de extremos. Usa comprobaciones explícitas que siguen activas con `-O`.

El control es un **CERTIFICADO_NUEVO** de estas identidades focales. No se
presenta como productor del libro terminal ni como prueba de autosuficiencia
científica global. La construcción de K ya demostrada en VI no se reclasifica
como pendiente; la procedencia de la selección del libro conserva su ámbito
propio, anterior a las reconstrucciones integrales.

Comandos ejecutables desde la raíz de VI_REV02:

```sh
python3 -I -S technical/verificar_periodo_conjugacion_k_vi_rev02.py --receipt technical/CONTROL_PERIODO_CONJUGACION_K_VI_REV02.json
python3 -O -I -S technical/verificar_periodo_conjugacion_k_vi_rev02.py --receipt technical/CONTROL_PERIODO_CONJUGACION_K_VI_REV02_OPT.json
```

La continuidad del contenido se verifica por el carácter exclusivamente
aditivo del parche de la sección 09; este registro no sustituye la posterior
compaginación ni el control conjunto de la entrega. Skills aplicadas:
`preserve-hmt-continuity`, `hmt-formal-kernel` y
`enforce-hmt-generated-constants`.
