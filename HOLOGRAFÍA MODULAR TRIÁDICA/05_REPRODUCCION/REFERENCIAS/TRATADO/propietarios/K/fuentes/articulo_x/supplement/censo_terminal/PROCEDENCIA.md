# Procedencia y alcance del censo terminal recuperado

## Resultado y corte operativo

El resultado incorporado es el censo finito de tres catálogos de frontera,
su reducción mediante un perfil declarado y la selección por la recta de
orientación. Su estatuto es **RESULTADO_RECUPERADO**, con un
**CERTIFICADO_NUEVO** portátil escrito con la biblioteca estándar de Python.
Está demostrado con estructura de partida explícita: cilindros regionales
ya publicados, orden de canales, seis posiciones ternarias, perfil del
lector y orientación.

No se presenta como resultado nuevo la arquitectura del selector, ni se
afirma que el programa demuestre el origen causal universal del perfil.
La matriz visible tampoco sustituye al registro firmado ni a sus canales.

## Entradas activas: exclusivamente salidas HMT ya incluidas

La raíz de los tres archivos es:

`supplement/alpha_completa/certificados/ley_nueve_puertas_2026-07-30/salidas/`

| Archivo | SHA-256 |
|---|---|
| pi_1000_decimales.txt | e898fea26734a6d3af5396b9f4c60ae5dcc88fc40944d835911a9ee8a672ea1b |
| e_1000_decimales.txt | b6d580142ddcf16920e195bc52cbc68c50a8e5b6cf93c69e8e5d17d798e7e78e |
| phi_1000_decimales.txt | 61a95781320c3b7219ca83ca52ba251fef4ab3b55928d593d2c3aa2c2ab63408 |

El programa lee estos cilindros como publicaciones posteriores a la
construcción regional. Exige igualdad exacta de las cotas del piso para
los multiplicadores `3^30`, `1000^171` y `3^1080`, en cada canal.
Los dos primeros determinan el catálogo; el tercero se usa únicamente
para el cotejo posterior de la frontera seleccionada. No existe una
lectura de N38, de `x0` ni de `ACT` en el programa activo.

La reducción de cada catálogo a los seis últimos trits es inyectiva
porque sus longitudes son menores que 729. Los catálogos completos
se obtienen por intersección de cilindros semiabiertos; no se construyen
a partir de las dos matrices finales.

## Propietarios históricos consultados, no usados como entradas activas

Directorio histórico:

`/Users/ruben/Documents/HMT2/corpus/HMT_BIBLIOTECA_MAESTRA_2026-07-18/HMT_BIBLIOTECA_MAESTRA_HMT/02_COLECCIONES/C00_ARCHIVO_ORIGINAL/02_LECTURA/paquetes_descomprimidos/F081_archivador-Feigenbaum-perme/archivador-Feigenbaum-perme`

1. `hmt_lift_celda08_terminal_boundary_selector.py`.
   SHA-256: `8d7a1948b1ee95b987c88fb67417ef6636740976dd30b99ee5539a2288bc1e18`.
   Se leyó completo, sin ejecutarlo. Sus funciones `candidates`,
   `matrix_features`, la asignación `ACT`, el bucle de conteos
   progresivos y el refinamiento de columnas contienen el precedente
   material del procedimiento y de sus límites.
2. `__extraido__/HMT_N38_HENSEL_LIFT_FLOW_PACK/n38_lift_data.json`.
   SHA-256: `15bce180654fa68172fc5918035ce5b300c1481cc254686054e62b13335a98c1`.
   Se leyó completo. La advertencia del campo `notes.warning` se conserva
   literalmente debajo. No se incluyó el JSON como entrada activa.
3. `__extraido__/HMT_N38_HENSEL_LIFT_FLOW_PACK/hmt_n38_hensel_lift_flow.py`.
   SHA-256: `a533386a7668f4bf1530b5469e1058468b2db85286ae15469f4562b539472930`.
   Se leyó completo para precisar la recurrencia y la función documental
   de sus datos; no se ejecutó ni se incorporó como generador.

Advertencia íntegra de N38:

> x0_mod_3^T here are the encoder states that reproduce the first 6*T ternary digits of the corresponding constant's fractional part (pi-3, e-2, phi-1) when used in the 3-adic transducer with matrix A. This uses the constant as an oracle; it is NOT yet a derivation from APP/TPK.

En el propietario histórico, `actual_blocks` procede de la emisión
de `x0_mod_3^180`, y `ACT=matrix_features(actual_blocks)`.
Ese hecho impide presentar allí la obtención de la firma como una
derivación causal independiente del estado que se desea reconocer.
La comparación retrospectiva confirma que los prefijos de treinta trits
y las 171 tríadas coinciden con las salidas HMT incluidas; esta coincidencia
no atribuye a los codificadores históricos una genealogía que su propio
archivo niega.

## Dependencias científicas y decisiones conservadas

| Campo | Objeto o decisión |
|---|---|
| APP | La genealogía upstream de las regiones procede del núcleo y de `source/sections/generacion.tex`; este censo recibe sus publicaciones y no vuelve a seleccionar semillas. |
| TRIT | Se conservan las palabras ternarias, el orden de canales y la orientación `(1,1,-1)`; los cálculos de Gram, rango y sumas son sobre el cuerpo de tres elementos. |
| TPK | La prolongación regional conserva prefijo y memoria. El corte censal usa prefijo30, cola1050 y longitud1080; no reemplaza la dinámica enriquecida por la reducción módulo729. |
| Coeficientes | 30 y1080 fijan el corte histórico; 171 es su capacidad decimal. Los valores del perfil son datos explícitos del lector, no números deducidos de una ley universal por este programa. |
| Conservación | Intersección de cilindros completos, extremos semiabiertos, cola, prefijo, orden, coordenadas y orientación. Se demuestra la inyectividad de la reducción de frontera sólo sobre estos catálogos. |
| Estado enriquecido | Las salidas regionales y el registro proceden de su construcción previa; el censo es una lectura posterior y no identifica la frontera visible con el estado completo. |
| Salida | Catálogos196/197/196,331 ternas de firma local,18 con pesos de columna,2 con sumas,1 tras orientación. |
| Comparación y falsador | El entero de1080trits extraído después permite cotejar la frontera; cualquier desigualdad de pisos, conteo o filtro aborta. Ninguna prueba aquí certifica alfa, CH o una interpretación física. |
| Propietarios | `generacion.tex`, `registro_k.tex`, los tres archivos de salida anteriores y el propietario histórico LIFT-CELDA-08, con estatutos separados. |

La fuerza del enunciado de conteo se conserva sin reducirla a un resumen:
los catálogos se parametrizan íntegramente; el TeX define las sumas finitas
de indicadores y sus matrices de transferencia; el suplemento conserva las
cuatro contribuciones por cada rango del canal pi y las 331 ternas. La
enumeración se evalúa sobre todo el dominio, no sobre una muestra.

## Archivos nuevos y comprobación efectuada

- `source/sections/censo_terminal_completo.tex`: subsección autónoma con
  demostraciones y localizadores `censo:*`.
  SHA-256 del corte entregado:
  `f58cbf1344d3d4f8627e70f6a1b94cf637335547d29c04dcaedf1e38224d7454`.
- `supplement/censo_terminal/verificar_censo.py`: verificador entero.
  SHA-256:
  `5b57a0756c11885bb91495c324df6c1bfd0f3a4af7685aa56d3391b0bb8270be`.
- `supplement/censo_terminal/resultados.json`: salida de la ejecución.
  SHA-256:
  `f526e26b36c8c4121394a77331d118f5b707076b3d4e39a0e43b188351e15777`.
- `supplement/censo_terminal/README.md` y esta nota.

Las ejecuciones `python3 -I -S` y `python3 -I -S -O` terminan con
código cero y salida idéntica byte a byte: **2703 controles exactos**,
incluidos **726 casos** de las fórmulas de extremos semiabiertos.
No se utilizaron punto flotante, NumPy, ReportLab, valores de alfa ni datos
metrológicos. No se modificaron `registro_k.tex`, `main.tex`, las salidas
regionales, los originales históricos o los recibos existentes. No se
compiló ni se emitió una aprobación matemática global.

Las huellas anteriores identifican los archivos; no sustituyen las pruebas
ni acreditan el origen universal del perfil.
