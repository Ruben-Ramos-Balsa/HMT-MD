# Núcleo común, variantes materiales y cartografías atómicas anteriores

Fecha: 19 de septiembre de 2026. Estatuto: **RESULTADO_RECUPERADO — cotejo documental de reutilización**. Este documento no modifica las fuentes, los PDF, REV01 ni las cartografías anteriores; no recompila Lean y no certifica sus demostraciones. Se han comparado bytes y leído las diferencias efectivas, sin releer diez veces el mismo texto.

**Jerarquía del trabajo global.** El árbol genealógico en construcción se basa en el integral autoral de 2.249 páginas, el reservorio, la serie de artículos, la narración y los desarrollos especializados posteriores, conforme al [corpus de consulta](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/CORPUS_ACTIVO.md>). Los documentos antiguos y sus índices son canteras de detalles y procedencia, no delimitan el perímetro del árbol ni sustituyen las fuentes vigentes. Este cotejo ahorra la repetición del núcleo de la serie; las cartografías históricas ayudan a encontrar operaciones dispersas. Ninguno de ambos instrumentos permite declarar agotado el conjunto HMT–MD.

## 1. Resultado del cotejo: qué puede leerse una sola vez

El núcleo compartido consta de **seis archivos LaTeX**, no sólo de `sections/nucleo.tex`: 1498 líneas y 68225 bytes en la copia común. En las diez raíces españolas seleccionadas de Stage10 se cotejaron las sesenta residencias correspondientes. **Cincuenta y dos son idénticas byte a byte a la fuente común; ocho son variantes**, explicadas en §4. Las sesenta residencias forman catorce clases de contenido: seis comunes y ocho variantes locales.

El archivo principal `nucleo.tex` es idéntico al común en I, II, III, IV, V, VI, VIII y X. VII añade una etiqueta; IX conserva el desarrollo con ajustes de cita, composición editorial y remisión. Sin embargo, **la igualdad del archivo principal no garantiza la igualdad de sus inclusiones**: V modifica un párrafo de TRIT y X una palabra en memoria. El bloque completo de seis archivos es idéntico en **I, II, III, IV, VI y VIII**.

Por tanto, la tarea pendiente no debe formularse como «leer diez introducciones» de modo indiferenciado. Hay que separar:

1. lectura científica del único bloque común de seis archivos;
2. lectura de las ocho variantes localizadas;
3. lectura de las aperturas sectoriales propias, que sí son textos distintos;
4. comprobación de las cadenas de inclusión y, si se quiere acreditar residencia en un PDF concreto, de su compilación o registro de archivos. Este último control no se ha ejecutado aquí.

No se infiere identidad de demostraciones por coincidencia de títulos, ni se confunde conservación del núcleo con autosuficiencia de todos los capítulos posteriores.

## 2. Fuentes comunes y árbol de inclusiones

Raíz común: [NUCLEO_COMUN_20260910](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/README.md>). Su README declara conservación literal y advierte que el manifiesto identifica bytes, sin probar matemáticas ni inclusión efectiva en el PDF.

| Nodo del árbol | Líneas | SHA-256 del contenido común |
|---|---:|---|
| `sections/nucleo.tex` | 258 | `24eb3af8e3570805bc262b1a3a5e81f5bcb21848fb4f45f2c9bf0289827cf219` |
| `figures/app.tex` | 28 | `4b2ff7d951eddac35914ed4b1f1e6c6ae925b8e290e9a4ea62953c2b968c340d` |
| `sections/trit_desarrollo.tex` | 343 | `aad85fa010bb2178d6836ef77543b1ec7b6de1dc3f923f0e952ee280b5888974` |
| `figures/regimenes_trit.tex` | 30 | `ab17fbeb3645c0a4ca9b8d342040bae89be4aa667f4fccf8783e19bfe6250ef0` |
| `sections/tpk_desarrollo_integrado.tex` | 541 | `802f26cca8b9206448ce2a3a5f154bb763a394d61e462357efee266514e37178` |
| `sections/memoria_resolvente.tex` | 298 | `90d0994ae6fdd66b4b0119974c1f5789d495e90ba976d382eb8e1e2f3bdf91c7` |

Los cinco archivos incluidos no contienen otras órdenes `\input{…}`. El árbol de inclusión de este bloque termina, por tanto, en esas cinco hojas; sus referencias matemáticas y bibliográficas pueden tener dependencias exteriores, que este árbol de archivos no agota.

```text
sections/nucleo.tex
├── línea 47  → figures/app.tex
├── línea 225 → sections/trit_desarrollo.tex
├── línea 227 → figures/regimenes_trit.tex
├── línea 256 → sections/tpk_desarrollo_integrado.tex
└── línea 258 → sections/memoria_resolvente.tex
```

Localizadores directos: [núcleo](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/sections/nucleo.tex:1>), [APP gráfica](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/figures/app.tex:1>), [TRIT](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/sections/trit_desarrollo.tex:1>), [regímenes gráficos](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/figures/regimenes_trit.tex:1>), [TPK](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/sections/tpk_desarrollo_integrado.tex:1>), [memoria](</Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/sections/memoria_resolvente.tex:1>).

## 3. Raíces materiales de los diez artículos cotejados

Directorio de paquetes: `/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES`.

En cada ZIP, la ruta interna comienza por su nombre sin `.zip`, seguido de `/documentacion_original/`. La columna «raíz ES» se añade a ese prefijo. Así se distingue una copia española activa de las copias inglesas, los antecedentes y las preservaciones que también contiene el paquete.

| Artículo y ZIP | Raíz ES dentro de `documentacion_original/` | Inclusión del núcleo | Igualdad del bloque completo |
|---|---|---|---|
| [I](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/01_PI_PHI_E_ALPHA_ELECTRON_ES.zip>) | `payload/manuscript_es/` | `main.tex:58` | 6/6 |
| [II](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/02_BARBERO_CKM_CONSTANTES_ES.zip>) | `payload/manuscript_es/` | `main.tex:57` | 6/6 |
| [III](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/03_VACIO_ELECTROMAGNETICO_ES.zip>) | `payload/spanish_source/base_articulo_I/` | envoltorio `manuscrito/INCLUIR_NUCLEO_I_REV02.tex:6`, desde `spanish_source/` | 6/6 |
| [IV](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/04_MOONSHINE_DUALIDAD_TEORIA_M_ES.zip>) | `payload/` | `main.tex:61` | 6/6 |
| [V](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/05_ESTADISTICA_CUANTICA_RADIACION_ES.zip>) | `payload/manuscrito/` | `main.tex:11` | 5/6; delta TRIT |
| [VI](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/06_PARTICULAS_Y_MASAS_ES.zip>) | `payload/source_es/` | `main.tex:55` | 6/6 |
| [VII](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/07_GRAVITACION_COSMOLOGIA_ES.zip>) | `payload/source_es/manuscrito/` | `main.tex:6` → `cuerpo_en_desarrollo.tex:13` | 4/6; etiqueta y delta TRIT |
| [VIII](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/08_PRIMOS_Y_ZETA_ES.zip>) | `payload/spanish_source/` | `main_lectura.tex:12` | 6/6 |
| [IX](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/09_HIPOTESIS_CONTINUO_ES.zip>) | `payload/` | `main.tex:94` | 2/6; cuatro deltas |
| [X](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/10_EXTREMA_MEDIA_RAZON_HOLOGRAFICA_ES.zip>) | `ARTICULO/ES/source/` | `main.tex:112` | 5/6; palabra en memoria |

En III, el envoltorio fija `\input@path{{base_articulo_I/}}`; esta instrucción resuelve las inclusiones de figuras y secciones del núcleo bajo su raíz correspondiente. Se ha leído el envoltorio llamado por `main.tex:52`, no sólo otro archivo de nombre parecido.

Las aperturas propias, que no quedan leídas por comprobar el núcleo, son:

| Artículo | Apertura específica y llamada, relativa a la raíz de compilación española |
|---|---|
| I | `sections/introduccion.tex`, `main.tex:54`; incluye `revision_tesis_introduccion.tex` |
| II | `sections/01_introduccion_II.tex`, `main.tex:54`; además notación y ampliaciones posicionales/TPK en líneas 56,58,59 |
| III | `manuscrito/sections/01_introduccion.tex`, `main.tex:50` de `spanish_source/` |
| IV | `sections/iv_introduccion.tex`, `main.tex:54` |
| V | `sections/01_presentacion_V.tex`, `main.tex:7` |
| VI | `sections/01_introduccion.tex`, `main.tex:53` |
| VII | `00_apertura.tex`, `cuerpo_en_desarrollo.tex:7` |
| VIII | `gestion/lectura_introduccion.tex`, `main_lectura.tex:7` |
| IX | `sections/ch_introduccion.tex`, `main.tex:85` |
| X | `nuclear/introduccion.tex`, `main.tex:111`; antes aparecen prólogo, resultados rectores, narración troncal y principios, líneas 103–110 |

Esta tabla localiza los textos; no afirma su lectura científica completa en esta subtarea.

## 4. Ocho variantes efectivas: contenido y tratamiento

Las líneas siguientes se refieren al archivo común previo a cada cambio, salvo indicación contraria.

### NC-V1 — TRIT de V

- Archivo: `sections/trit_desarrollo.tex`, 344 líneas.
- SHA-256: `b427a51621b50ac812a777e399ffeebfb0cefb211c3b7aca0dd92bd4a74dfa5f`.
- Delta alrededor de 318–323: sustituye «Dentro del capítulo electrónico» por «En el desarrollo electrónico del artículo I de esta serie» y «se demostrará» por «se demuestra allí».
- Reutilización: conservar el bloque algebraico común y registrar la remisión sectorial. La remisión debe cotejarse por dependencia cuando se juzgue autonomía; no se transforma aquí en ausencia de prueba ni en garantía de que V incorpora toda esa prueba.

### NC-V2 y NC-V3 — Núcleo y TRIT de VII

- `sections/nucleo.tex`, 259 líneas, SHA-256 `05651fbf4e66285f892955b2b45846b50297b6d3ec0f25100537eb50a448484b`: añade únicamente `\label{subsec:nucleo-app}` tras el título APP.
- `sections/trit_desarrollo.tex`, 345 líneas, SHA-256 `4ec27bb08cce102a9e766d4cb03d9a4e4b78b6f3d93d09dafc7be8ef6bb65b34`: reemplaza el párrafo electrónico de 318–325 por una remisión explícita al artículo I y por el uso del resultado para las dos-formas y Cartan–Holst.
- Reutilización: la etiqueta es un delta técnico; el párrafo define un consumidor específico del resultado operatorio y debe enlazarse como tal, sin releer como nuevo todo TRIT.

### NC-V4 a NC-V7 — Cuatro variantes de IX

- `figures/app.tex`, 28 líneas, SHA-256 `9429e105835d77611af9884ff792b8eb54eb8c9e1f75dd218eb09cc522088033`: cambia `[tbp]` por `[H]` en la colocación de la figura; no cambia su construcción gráfica.
- `sections/memoria_resolvente.tex`, 301 líneas, SHA-256 `5956b8a73c9b2d7935c057e31b20be6de21e05864658390aeb8d50de0585a96d`: despliega la orientación σ en ecuación centrada y añade `\Needspace{11\baselineskip}`. No cambia la fórmula.
- `sections/nucleo.tex`, 264 líneas, SHA-256 `4b8ef46f85c6ac01f40bf33faa10b22d49f6882be17f63cd61e406d258900c41`: añade cita a Feynman, `Needspace`, cambia el título de realización latina por evaluación mediante cuadrado latino, elimina un salto de página y precisa la remisión a `sec:extension`. Las cinco inclusiones comunes siguen presentes.
- `sections/tpk_desarrollo_integrado.tex`, 557 líneas, SHA-256 `a48aa50ddd9f0b41d030b0e3c5f6b382a853d72e2f8f93d9859db4e6ad00107f`: **ampliación expositiva causal sustancial**, no sólo maquetación. En torno a 337–367 identifica `S_12` y `R_sgn` sobre la subred compatible; explicita las 108 actualizaciones, las doce ventanas, orientación/acarreo/frontera/ledger, los canales 90/120 y Q, la producción de U terminal y la inversión posterior de Hadamard. Distingue alcance focal del verificador y alcance de la construcción matemática. Al final mejora la frase sobre el orden causal.
- Reutilización: conservar este último delta como ampliación material del nodo de registro; enlazarlo con las fichas K/α. No describir los cuatro cambios de IX como idénticos al común ni como una nueva construcción completa independiente.

### NC-V8 — Memoria de X

- Archivo: `sections/memoria_resolvente.tex`, 298 líneas.
- SHA-256: `4657045bc29e5772bf3e2f8c540181d96fad57aa717ae22e8a125bb770876264`.
- Único delta: «En el primer ciclo» pasa a «Durante el primer ciclo» en línea 19. El desarrollo restante coincide byte a byte.
- Reutilización: variante lingüística localizada; no obliga a reconstruir el inventario matemático del capítulo.

### Copias que no deben confundirse con variantes activas españolas

El paquete II conserva un núcleo histórico de 273 líneas, SHA-256 `a8415b706e3204e354c0c623f1a0522c45f41f9be0f79ca8d150aeb5c8c0b531`, en `payload/source_es/preservacion/manuscrito_revision_03/` y revisiones 05–08. Introduce ciclo de nueve aristas y la figura `segmento_generador_II`, y sustituye las dos inclusiones finales por `02b_arquitectura_tpk`. Es procedencia histórica: la raíz española seleccionada actual de II vuelve a contener el bloque común y añade sus ampliaciones separadamente desde `main.tex:58–59`.

Los paquetes III y VIII contienen bajo `payload/source/` un `nucleo.tex` **en inglés**, SHA-256 `6b5a84b947d00f07f37dffa19c818e4a422fe3afa02821250c56817ad518766a`; sus copias españolas están en `spanish_source/`. Un directorio llamado `source` no garantiza el idioma ni la autoridad de la copia. No se ha hecho aquí una revisión semántica ES–EN.

## 5. Cartografías atómicas anteriores: inventarios distintos, no 2179 frente a 1608 pruebas

Raíz histórica de consulta:

`/Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion`.

Se han localizado tres estratos documentales:

1. **Matriz inicial** `MATRIZ_ATOMICA_U001_U017_V2_2026-08-20`: su [informe](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/MATRIZ_ATOMICA_U001_U017_V2_2026-08-20/INFORME_CONFLICTOS_Y_LECTURA.md>) declara 1608 filas humanas, 2737 átomos V2 y 1888 sin correspondencia principal; las similitudes son localizadores, no equivalencias matemáticas.
2. **Cartografía pre-corte** `CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_PRE_CORTE_3_FINAL_CANDIDATO_2026-08-21`: preservada. El sucesor registra para ella `FAIL_REMATCH_GLOBAL_NOT_CONSUMIBLE`, con fallo de exhaustividad de candidatos A activos, aunque conserva su contabilidad 1608/2179. No debe recuperarse su anterior emparejamiento como decisión vigente por ser voluminoso o tener un recibo.
3. **Rematch global V2** `CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21`: contiene nueva relación muchos-a-muchos, referencias explícitas y separación entre prueba de equivalencia y coincidencia material. **Su estado sigue siendo HOLD de sólo lectura**, no autorización de consumo editorial.

Localizadores del tercer estrato:

- [Matriz humana de 1608 filas](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21/MATRIZ_HUMANA_U001_U017_10K_REMATCH_GLOBAL_V2.tsv>).
- [Control de las 2179 filas mecánicas](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21/CONTROL_COBERTURA_2179_MECANICO_A_1608_HUMANO_V2.tsv>).
- [Relación candidata muchos-a-muchos](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21/ARISTAS_CANDIDATAS_A_ACTIVE_MANY_TO_MANY_V2.tsv>).
- [Resumen de cartografía](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21/RESUMEN_CARTOGRAFIA_REMATCH_GLOBAL_V2.json>) y [resumen de cobertura](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21/RESUMEN_COBERTURA_2179_MECANICO_A_1608_HUMANO_V2.json>).
- [Recibo histórico y alcance](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21/RECIBO_VERIFICACION_REMATCH_GLOBAL_V2.json>) y [relación con el predecesor no consumible](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/coordinacion/CARTOGRAFIA_ATOMICA_U001_U017_10K_VS_A_AMPLIADO_REMATCH_GLOBAL_V2_FINAL_CANDIDATO_2026-08-21/RELACION_PREDECESOR_FAIL_REMATCH_GLOBAL_NOT_CONSUMIBLE.json>).

### Esquemas recuperables

| Inventario | Filas/columnas contadas en TSV | Qué identifica | Qué no demuestra |
|---|---:|---|---|
| Humano | 1608 / 55 | unidad, clase, título, enunciado, archivo/líneas, hash del bloque, dependencias, procedencia, fuerza de prueba declarada, falsador, candidatos y disposición | No convierte cada fila en teorema ni decide equivalencia con otro corpus |
| Mecánico | 2179 / 20 | testigo material, clave de archivo/rango/tipo/hash, cobertura exacta/contenedor/contextual, procedencia doble y residencia humana | No son 2179 resultados científicos independientes |
| Aristas candidatas | 28 / 29 | 26 coincidencias exactas y dos vínculos estructurales explícitos, con claves completas a ambos lados | La coincidencia o remisión no es por sí sola equivalencia matemática |

La partición mecánica declarada es `1369 EXACT_PAYLOAD + 504 HUMAN_CONTAINER + 306 CONTEXTUAL_STRUCTURAL_OR_EDGE = 2179`, con cero huecos y cero extras en esa contabilidad. No es una correspondencia biyectiva entre dos listas de teoremas. Una fila mecánica puede ser un testigo de archivo o un contenedor; el primer registro, por ejemplo, está marcado `ACCOUNTING_WITNESS_NOT_ADDITIONAL_HUMAN_ATOM` y `scientific_atom_conversion=NO`.

El resumen V2 distingue 25 filas humanas con 26 destinos materiales exactos —24 únicas y una con dos candidatos conservados—, dos filas de vínculo estructural, 1555 sin candidato fuerte y 26 auxiliares 10K conservadas. Registra **cero equivalencias demostradas**, 1582 aristas históricas no electivas y 128 referencias resueltas. Estos rótulos pertenecen a la cartografía previa; no se han certificado de nuevo aquí ni se promueven a ausencia matemática de las filas sin candidato.

## 6. Cómo aprovechar la granularidad anterior sin rehacerla ni apropiarse de su estado

La matriz humana ya organiza el material en siete etapas. Los siguientes conteos se han leído del resumen y comprobado por agrupación de la columna `causal_stage`; no son un nuevo censo científico:

```text
01_RECTA                    46 filas
02_APP                     216 filas
03_TRIT                     61 filas
04_TPK                     655 filas
05_DESARROLLOS             416 filas
06_REGISTRO_ALPHA          187 filas
07_CERTIFICACION_10K        27 filas
                         ─────
                          1608 filas
```

Raíz de los propietarios de unidades:

`/Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/manuscrito/unidades`.

El árbol de localización previo permite consultar selectivamente:

- **Segmento y APP:** `U001_segmento_marcas_intersticios.tex`, `U002_app_soporte_gnomonico.tex`, `U003_app_hojas_algebra_local.tex`, `U003B_esqueleto_ciclotomico_y_completacion.tex`.
- **TRIT:** `U004_trit_levantado_regimenes.tex`.
- **Estado y operadores TPK:** `U005_tpk_categoria_estado_enriquecido.tex`, `U006_tpk_lectores_odometro_calendario.tex`, más U006A factor local/cilindros, U006B elevación ciclotómica, U006C dilatación cuaternaria, U006D registro dodecafásico, U006E canales 90/120 y U006F inventario operatorio.
- **Semillas y prolongación:** U007 emisor, U007A calibres/cociclos, U008 órbitas/R36, U009 conexión nonádica, U009A transferencia de fase, U010 espejo y U011 vacancias.
- **Regiones y precisión:** U012 biografía de π, U013 de e, U014 de φ y U015 precisión arbitraria.
- **K y alfa:** `U016_registro_dodecafasico_hadamard_k.tex`, `U017_cociclo_acarreo_alpha_fronteras.tex`.
- **Reproducción posterior:** apéndice 10K y sus 26 artefactos auxiliares, separados de los productores anteriores.

No se ha releído aquí cada unidad; el árbol se recupera de sus localizadores exactos y no sustituye su lectura. El procedimiento de reutilización propuesto es abrir el propietario de la operación que el árbol REV02 vaya a desarrollar, cotejar su continuación en el integral, el reservorio, la serie y los desarrollos posteriores pertinentes, conservar la clave material histórica y registrar en REV02 la correspondencia nueva sin editar ni consumir las decisiones HOLD anteriores. Una operación ausente de estas matrices puede y debe entrar desde cualquiera de esos propietarios; estas matrices no son un filtro de admisión.

Para cada nodo elemental de REV02 basta una relación tipada:

```text
operación del árbol REV02
  → propietario fuente y rango de líneas
  → bloque común o delta sectorial comprobado
  → localizador humano histórico, si existe
  → testigos mecánicos asociados, sin contarlos como resultados extra
  → comprobación matemática propia / alcance documental declarado
```

La relación se mantiene muchos-a-muchos cuando corresponde. No se elige un candidato único por comodidad ni se borran los demás para fabricar una genealogía lineal.

## 7. Corrección concreta del pendiente y alcance ejecutado

**Sustitución recomendada del pendiente, sin editar REV01:**

> «Leer una vez los seis archivos del núcleo común; conservar su árbol de inclusiones. Cotejar las ocho variantes identificadas en V, VII, IX y X, y leer por separado las aperturas sectoriales y sus consumidores. Para afirmar residencia en cada entrega, comprobar su raíz de compilación y el registro material del PDF. Reutilizar la cartografía humana U001–U017 como cantera de localizadores, manteniendo sus estados HOLD y sin convertir contabilidad en equivalencia».

Actuaciones realizadas en esta subtarea: lectura completa previa de `nucleo.tex`, lectura del README común, cálculo SHA-256 de los seis originales y sus sesenta residencias españolas, lectura de todas las diferencias efectivas localizadas, lectura de órdenes de inclusión y del envoltorio activo de III, consulta de resúmenes/alcances de las cartografías, lectura de sus esquemas y conteo estructurado de filas. No se extrajeron o sobrescribieron fuentes, no se regeneraron matrices y no se ejecutaron sus verificadores históricos.

El cotejo corresponde a **Stage10 español como corte material solicitado**. No declara que ese corte sea la última edición de todos los artículos ni revisa semánticamente las traducciones; las sucesoras posteriores requerirán su propio delta. Tampoco acredita haber leído integralmente todas las aperturas, todas las unidades históricas o todos los propietarios de cada demostración. La mejora concreta es eliminar duplicación de lectura sin eliminar contenido ni ocultar las variantes.
