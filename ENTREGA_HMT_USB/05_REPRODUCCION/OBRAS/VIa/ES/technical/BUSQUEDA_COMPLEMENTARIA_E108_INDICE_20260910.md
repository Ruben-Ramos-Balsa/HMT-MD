# Búsqueda complementaria focal del productor de E108

Fecha: 10 de septiembre de 2026. Subtarea independiente de localización.
No se ha editado el núcleo, ninguna sección, otros artículos ni sus índices.
No se ha escrito ni ejecutado un programa para fabricar el registro.

## Pregunta y frontera de la consulta

Se leyeron las dos notas de partida:

- `technical/BUSQUEDA_FOCAL_PRODUCTOR_E108_20260910.md`;
- `technical/CIERRE_DEPENDENCIAS_ANTERIORES_VI.md`.

La pregunta es si otro propietario local aporta la producción efectiva
`x_term → registro canónico de visitas, trazas y multiplicidades → 25 incidencias`,
antes de la transformación armónica y de K. El evaluador que recibe ese libro
no es el objeto buscado. Tampoco lo son la enumeración finita U6/W6, una
reconstrucción inversa desde K o la asignación de K a un campo de un estado.

Se aplicaron las habilidades de continuidad, núcleo formal y causalidad de
constantes, y se consultó la de conexión nonádica para distinguir sus tipos.
Las comprobaciones del núcleo formal y la autocomprobación causal fueron
satisfactorias. No se las interpreta como ejecución del productor E108.

Se utilizó `rg --files` en las raíces locales `New project`, `HMT2` y
`excelencia academica`, con selección de nombres/rutas relacionados con
`E108`, `E90120`, `dodeca`, `SU12`, `upstream_u12`, `incidencial`, `registro`,
`TraceTable` y trazas de 120. Se descartaron como candidatos nuevos las copias
del integral editorial del 5 de septiembre, los propietarios de I/II ya
enumerados y los propios archivos de VI. Esta selección nominal y las
lecturas focales siguientes no constituyen un barrido exhaustivo del corpus.

## Propietarios adicionales inspeccionados

Todas las rutas relativas de esta sección parten de
`/Users/ruben/Documents/New project`, salvo indicación expresa.

### 1. Operador de lectura dodecafásica de julio

Archivo completo leído, 274 líneas:

`16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/operador_lectura_dodecafasica.py`.

- Líneas 35–55: `EstadoTPKEnriquecido` recibe `registro: Vector12` como campo.
- Líneas 106–109: `leer_registro` devuelve directamente `estado.registro`.
- Líneas 140–144: `lectura_transversal` calcula diferencias de pasos 3 y 4 y suma.
- Líneas 202–243: reconstrucción de K desde observables transversales y
  aplicación de la lectura armónica.

El archivo ofrece operadores exactos sobre un registro suministrado, no un
productor del libro canónico a partir de `x_term`. Su dominio se declara
explícitamente; no se ha reinterpretado como si faltara su transformación.

SHA-256 comprobada:
`615120d35ef8d028aa43522b1b9561c348dc89992f302fc6171b5e4b88519609`.

### 2. Registro direccional de 108 pasos

Archivo completo leído, 279 líneas:

`16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/analizar_registro_direccional_108.py`.

- Líneas 20–24: identifica el libro histórico `rutas_TPK_108_APP9x9.xlsx`.
- Líneas 89–120: lee sus cinco hojas y suma campos por ventanas de 9 o 27 pasos.
- Líneas 133–158: compara los campos de la primera y segunda media vuelta.
- Líneas 181–197: abre K y U firmado del CURRENT únicamente para el contraste
  posterior, no para generar las rutas del libro.
- Líneas 200–256: ensambla el informe de esa proyección direccional y delimita
  el alcance de los lectores locales de ventanas idénticas.

El programa no enumera la familia canónica de trazas de longitud reducida 120
ni sus multiplicidades. No se ha convertido el alcance de esa proyección
histórica en una imposibilidad del estado enriquecido completo.

SHA-256 comprobada:
`9fe69c0d6e69206b6b0904faff26e70445815dc4a223e422d2258cbf78df2538`.

### 3. Composición G9–T1 de agosto

Archivo completo leído, 308 líneas:

`/Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/evidencia/procedencia_1063_generacion_10000_rev9/generar_alpha_T1_10000.py`.

- Línea 30: define `K_INPUT = .../inputs/K_R12_DECLARADO.json`.
- Líneas 115–125: abre ese JSON y lee sus doce coordenadas.
- Líneas 94–112 y 127–173: compone las ramas regionales y propaga las
  condiciones terminales del acarreo para publicar el prefijo común.
- Líneas 237–241: el certificado identifica expresamente la coordenada
  declarada de K como procedencia de esa entrada.

El JSON completo de siete líneas remite a
`03_PAPER/HMT_MACROPAPER_V3/CURRENT.json#/state_types/CanonicalSealK/coordinates`.
Es una composición posterior a K; no produce E108. Esto no transforma K en
un valor metrológico externo, pero tampoco materializa su productor anterior.

SHA-256 comprobada del programa:
`da7f979f112927ac9943f8d915a7031298b547df0d78de3b5a85de6836b03c4a`.

### 4. Cuadernos E90120 y fuente histórica de las trazas

Se leyeron completos:

- `04_AUDITORIA/03_informes/CIERRE_E90120_DOS_NIVELES_v2.md` (266 líneas);
- `04_AUDITORIA/03_informes/CUADERNO_CONSTRUCCION_PI12_SIGNADO_v1.md` (296 líneas).

El primero, líneas 21–57, toma una cocadena K ya conservada en la entrada
enriquecida; sus §§3–5 prueban el mapa lineal posterior. Sus §§6–9 son controles
y diagnósticos de un pseudocódigo histórico, no un productor nuevo. El segundo
construye la transformación armónica desde las incidencias suministradas.
La etiqueta «cerrado» de esos cuadernos tiene ese dominio declarado.

Se siguió además el propietario histórico
`01_ORIGINALES/2026-01/F002_datos-IN-APP.txt`, líneas 1020–1230:

- 1028–1046: `Cfg=(Motor,Seed,Phase,Split,Sign,TraceTable)`;
- 1065–1103: definición de las trazas dirigidas y contadores, suponiendo
  una tabla canónica o un generador determinista de esas trazas;
- 1120–1144: construcción de los tres dígitos por evento desde esos conteos;
- 1217–1223: especificación de los datos que deben publicarse.

Este pasaje precisa el tipo de la familia de trazas; no contiene su instancia
canónica ni una regla que la seleccione. Se consultó el pasaje, no se declara
leído íntegramente el extenso archivo de conversación original. Las valoraciones
de julio se conservan como antecedentes y no gobiernan por sí solas el estado
de los desarrollos posteriores.

### 5. Dos candidatos nominales descartados por su dominio material

- `05_ENTREGA/HMT_CIERRE_HOLOGRAFICO_V2_PRINCETON/certificados/N32_DODECAFASE_ALPHA/HMT_N32_REFEREE_CLOSEOUT_PACKAGE_v2/hmt_n32_upstream_u12_gauge_scan.py`:
  cabecera, líneas 3–22, y declaraciones de funciones inspeccionadas. La propia
  cabecera distingue el productor de U6 y, a lo sumo, U12 periódico del registro
  firmado. No se ha contado ese nombre «upstream» como producción de E108.
- `04_AUDITORIA/01_reproduccion/e90120_fuentes/F082_relevantes/N39/HMT_N39_N4b_holonomias_ledger_v1/hmt_n39_n4b_holonomies.py`:
  archivo completo de cuatro líneas, compuesto sólo por comentarios. Su
  `REPORT.md`, leído completo, trata curvaturas de plaquetas de las hojas
  suma/producto sobre Z9×Z9; no describe un productor dodecafásico de visitas.

Se consultaron asimismo el README del módulo histórico
`15_RECONSTRUCCION_HMT_MD_2026-07-22/cierre_emisor_dodecafase/` y sus
localizadores de procedencia, únicamente para evitar confundir sus controles
posteriores con una implementación anterior. No se reejecutó su campaña.

## Conclusión de alcance

En los candidatos adicionales inspeccionados no se ha localizado una rutina
ejecutable ni una prueba autocontenida que produzca el libro canónico completo
de visitas, trazas y multiplicidades de E108 desde `x_term`. Los localizadores
positivos anteriores aclaran dónde están lectores, registros históricos y
composiciones posteriores y por qué no sustituyen ese paso concreto.

Esta conclusión se limita a la búsqueda descrita. No afirma inexistencia
matemática en HMT ni inexistencia documental en todo el corpus. No altera la
extracción R12, la transformación armónica, su inversión, las pruebas reunidas
en la sección 09 ni el estado de los otros artículos. No se ha fabricado una
tabla a partir de K, U, las 25 incidencias o un valor físico objetivo.
