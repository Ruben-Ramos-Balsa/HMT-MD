# Moonshine, dualidad T y teoría M desde la estructura discreta del continuo

Oumar Haidara Fall · Rubén Ramos Balsa

Integración y recopilación documental generadas por ChatGPT Astra.

Esta sucesora del 11 de septiembre de 2026 conserva el desarrollo de REV02 y
añade la construcción correlativa local del continuo, antes de las publicaciones
coinductivas y excepcionales. Reúne el manuscrito LaTeX, las figuras, las fuentes
de procedencia y los controles ejecutables incluidos en esta edición.

## PDF activo y estado de entrega

El PDF nuevo es exclusivamente:

`output/pdf/MOONSHINE_DUALIDAD_T_TEORIA_M_CONTINUO.pdf`

Tiene **134 páginas**, 764.603 bytes y SHA-256
`5649278f225c5b1d935fb85ebb41eb9443ea55eda3a2e09039a456660c7a0467`.
Se compiló en tres pasadas después de superar el preflight canónico del corte
actual. No hay referencias, citas o glifos ausentes, etiquetas duplicadas ni
desbordamientos; se registran dos avisos `underfull hbox`.

**Estado: compilado y revisión visual focal satisfactoria; entrega de fuentes
preparada para empaquetado verificable.** Raíz inspeccionó directamente 25
páginas del PDF final, incluido el capítulo conjunto completo, la portada,
el índice y las remisiones corregidas. No encontró defectos críticos en esas
páginas. El recibo es `technical/QA_VISUAL_FINAL_20260911.json`; no equivale
a inspección visual integral de las 134 páginas.

El cierre del ZIP exige ese recibo y el de compilación del mismo PDF. Conserva
el manifiesto de REV02 en `technical/historial_manifiestos/` antes de generar
el `MANIFIESTO_ENTREGA.json` propio de esta ampliación. El reproductor exige
coincidencia real con el manifiesto; se detiene ante hashes desactualizados.
El ZIP de esta edición se denomina
`MOONSHINE_DUALIDAD_T_TEORIA_M_CONTINUO_20260911.zip` y contiene la carpeta
completa de entrega, incluidos el PDF activo, las fuentes y estos recibos.

El PDF `ARTICULO_IV_MOONSHINE_DUALIDAD_TEORIA_M_REV02.pdf`, de 124 páginas,
que pueda permanecer en la carpeta es **el antecesor conservado**, no el nuevo
resultado. Su SHA-256 es
`f170b4cf2ece666b666581dec2828cca567f177efd481c4d43c228506333db7e`.
El README anterior se preserva íntegro en
`technical/antecedentes_editoriales/README_REV02.md`.

## 1. Orden de lectura y dependencia matemática

El orden de inclusión efectivo se encuentra en `main.tex`. Las secciones han de
leerse atendiendo a sus definiciones y demostraciones, no como un catálogo de
valores independientes:

1. **Resumen e introducción.** Objeto, tesis expositiva y alcance de las dos
   realizaciones del estado.
2. **Núcleo formal HMT.** Construcción de APP, firma orientada TRIT y operaciones
   del Topological Phase Kernel (TPK). Se conservan hojas, residuos, cocientes,
   orientación, frontera y memoria pertinentes.
3. **Desarrollo del núcleo formal.** Condiciones iniciales, transporte,
   refinamiento, calendario y geometría operativa.
4. **Construcción correlativa del continuo.** Historias levantadas con hoja
   activa y prefijo conservado, memoria afín, medida de historias, transporte
   isométrico, balance orientado, incidencia rectangular, complejo de memoria,
   ensamblaje de caminos terminales y líneas determinantes. Las pruebas de
   naturalidad mantienen unidos estos objetos; el terminal se conserva hasta
   demostrar su extinción en el dominio pertinente. Comienza en la página
   impresa 37, antes de la generación coinductiva.
5. **Generación coinductiva.** Regiones y publicaciones de π, φ y e; compatibilidad
   de cilindros y retorno de fase con avance de memoria.
6. **Registro dodecafásico K.** Registro de canales, transformación firmada,
   reconstrucción entera y evaluación racional. La evaluación no sustituye su
   cadena de procedencia.
7. **Constante de estructura fina.** Clausura entera, lector analítico de
   vacancias y estatuto preciso de su identificación a toda profundidad.
8. **Prolongación excepcional.** Incidencia de K y α, código ternario, Witt,
   Niemeier, Leech y álgebra de operadores de vértice; construcciones de
   Moonshine de órdenes 2 y 3 y sus teoremas externos identificados.
9. **Realización hilbertiana.** Representación de Weyl, elevaciones, conservación
   de la unidad, cierre inductivo y realización tracial.
10. **Acción y publicación angular.** Cociente local, norma, valoración, carácter
   y renovación normalizada; secciones positivas, cartas en grados/radianes,
   conservación de acción e inversión de los canales.
11. **Elipse y determinación del radio.** Semiejes, prueba de pertenencia a la
    carta, ley areal, orientación simpléctica, radio positivo único y matriz
    reticular. La familia conserva las dos fibras recíprocas.
12. **Dualidad T.** Dominio entero, intercambio de coordenadas, radio,
   Hamiltoniano, clases residuales y equivalencia unitaria.
13. **Pantallas dimensionales.** Perforación de código, dirección producida por K,
    reducción de rango y cociente reticular, con sus respectivos núcleos.
14. **Acción y realización undecadimensional.** Descenso de observables,
    composición de trayectorias, supercarga y condiciones de compactificación.
15. **Conclusiones y referencias.** Resultados, condiciones y procedencia.

La cadena causal de referencia es:

`rectas 0–10/0–9 → APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo → salidas y realizaciones HMT–MD → reconocimiento convencional posterior`.

La prolongación `w6 → w12 → w18 → w24 → w30 → R36 → G9` conserva sus tipos y
sus operadores. Las coordenadas internas de π, φ y e pueden publicarse antes
de alimentar el cierre de α: una dependencia interna posterior no las convierte
en entradas convencionales. CODATA, valores objetivo o fórmulas convencionales
de evaluación no actúan como selectores del generador en esa lectura.

Una revisión asistida por IA debe seguir esta dependencia y comprobar cada
operación con su fuente, dominio y alcance. No debe sustituir un productor por
la cifra que reconoce al final, ni interpretar esta guía como autorización para
ignorar discrepancias concretas. El orden documental facilita una comprobación
reproducible; no puede garantizar el comportamiento de un sistema externo.

## 2. Qué contiene cada carpeta

- `main.tex`: entrada del manuscrito y configuración tipográfica.
- `sections/`: cuerpos incluidos o conservados durante el ensamblaje. Las cuatro
  secciones propias de este desarrollo son `01_hilbert_nonadico.tex`,
  `02_dualidad_t.tex`, `03_pantallas_coordinadas.tex` y
  `04_accion_realizacion.tex`. Los cuerpos heredados del Artículo I y las
  incorporaciones de la serie conservan sus funciones y referencias. Esta
  sucesora añade `continuo_conjunto.tex` y la portada `iv_portada.tex`. Estar en la
  carpeta no significa necesariamente estar incluido: lo determina `main.tex`
  y la cadena de sus instrucciones `\input`.
- `figures/`: figuras vectoriales LaTeX/TikZ; no se requiere una imagen externa
  para sustituir sus construcciones.
- `technical/antecedentes/`: seis propietarios íntegros del integral, conservados
  como procedencia. No son versiones nuevas de los cuerpos activos.
- `technical/REGISTRO_PROCEDENCIA.json`: relaciones de procedencia, localizadores,
  hashes explícitos y alcance del desarrollo focal.
- `technical/MAPA_ENSAMBLE_20260910.md`: dependencias y decisiones de ensamblaje.
- `technical/MAPA_DE_FUSIONES_REV02.md`: residencia de las pruebas reunidas,
  incorporación desde II y conservación de condiciones y etiquetas.
- `technical/INTEGRACION_CONTINUO_20260911.md`: delta de esta sucesora,
  procedencia, dominios y estado real de compilación y revisión visual.
- `technical/LECTURAS_EFECTUADAS_20260911.json` y
  `technical/TRAZA_INTEGRAL_WEIL_20260911.md`: lectura efectivamente realizada
  y localizadores del contraste focal; no declaran leído el corpus entero.
- `technical/IMPLICACION_ESTRUCTURAL_WEIL_20260911.md`: conserva la propuesta
  autoral de implicación estructural y el punto de investigación exacto.
  `technical/antecedentes_editoriales/RECUPERACION_GENERATIVA_WEIL_20260911.md`
  preserva íntegra su nota matemática antecedente. Ambas quedan fuera del
  argumento demostrado del PDF; no cambian su alcance.
- `technical/QA_VISUAL_FINAL_20260911.json`: resultado de la inspección visual
  focal de 25 páginas sobre el PDF final identificado por SHA-256.
- `technical/verificar_radio_elipse.py`: identidad polinómica del radio,
  cotas racionales, transportes y pruebas de rechazo fuera del dominio.
- `technical/verificar_focal.py`: control de las cuatro secciones propias y seis
  antecedentes, más pruebas finitas de identidades concretas.
- `technical/CONTROL_FOCAL*.json`: recibos antecedentes de comprobación.
  Los resultados del lote actual están en
  `technical/CONTROL_REPRODUCCION_LOCAL_FINAL_20260911.json`;
  una reproducción posterior se guarda en `reproduction/`.
- `technical/preflight_20260911/`: contrato y preflight de la sucesora;
  `CORTE_ACTUAL.json` identifica el corte vigente `8f03f52de977edb5` bajo `runs/`.
  La aprobación programática autoral y la revisión técnica del delta se registran
  separadamente; ninguna de ellas se presenta como validación matemática global.
- `technical/preflight_rev02/`: expediente histórico de REV02, conservado sin
  utilizarlo para autorizar las fuentes modificadas de esta sucesora.
- `technical/preflight_20260910/`: constancia histórica de la edición anterior,
  conservada sin utilizarla para autorizar la compilación nueva. Puede conservar rutas
  absolutas del entorno de origen. No es necesario disponer de ese entorno para
  ejecutar el reproductor portable.
- `technical/reproducir_controles_continuo.py`: suite actual de **doce ejecuciones**,
  normales y optimizadas, de seis programas: control focal, radio, siete
  antecedentes de II, identidades conjuntas locales, naturalidad de puertos y
  grafo fuente/preflight. El programa de REV02 permanece como antecedente.
- `technical/verificar_identidades_continuo.py`: 43.503 comprobaciones exactas
  por modo de cociclos, retorno, balance, incidencia, complejo, Gram, homología
  local, publicaciones y terminal.
- `technical/verificar_naturalidad_puertos.py`: 9.072 comprobaciones exactas por
  modo de las identidades de puertos marcados, prefijos y reducción modular.
- `technical/recepcion_20260911/`: fuente compuesta y recibos genealógico y
  causal del corte; su resultado propio es la construcción local incorporada,
  no un certificado del corpus completo ni de la positividad global de Weil.
- `technical/compilar_continuo.py`: controlador actual; consume el preflight
  auténtico y comprueba las fuentes antes de cada pasada. No emite su aprobación.
- `technical/empaquetar_continuo.py`: prepara inventario en modo de sólo lectura;
  `--seal` requiere el recibo de compilación y el de revisión visual del PDF
  actual. No debe sustituirse por el empaquetador antiguo de REV02.
- `output/pdf/`: PDF preparado para la lectura, cuando la entrega esté montada.
- `reproducir.py`: entrada portable de comprobación y recompilación.
- `MANIFIESTO_ENTREGA.json`: lista final `files`, con `path` relativo y `sha256`.
  Se verifica; este programa nunca lo genera ni lo actualiza automáticamente.

Los scripts de ensamblaje y precompilación conservados en `technical/` documentan
el proceso editorial original. No se presentan como reproductores portables de
todo el corpus. Para esta entrega, la entrada pública es `reproducir.py`.

## 3. Comprobación sin compilar

Requisitos: Python 3.9 o posterior y su biblioteca estándar. No se instalan
dependencias ni se requiere conexión de red.

Descomprima la entrega manteniendo sus carpetas. Desde ese directorio ejecute:

```bash
python3 -I -S reproducir.py
```

También puede invocar el programa mediante su ruta completa desde otro
directorio. El programa localiza las fuentes junto a su propio archivo.

La ejecución comprueba primero todos los hashes enumerados en el manifiesto y
la presencia de los archivos mínimos del control focal. Rechaza rutas que salgan
de la entrega, duplicados, archivos ausentes y contenidos modificados. Después
ejecuta los seis programas locales tanto en modo normal como con `-O`
(doce ejecuciones) y exige igualdad de sus resultados matemáticos, separando
el metadato que registra el modo de optimización. Se escriben:

```text
reproduction/RECIBO_REPRODUCCION.json
reproduction/CONTROL_PORTABLE_CONTINUO.json
reproduction/verificacion_focal.log
```

El control focal examina los cuerpos propios y sus referencias dentro del
ensamblado activo. Comprueba seis copias contra
sus SHA-256 registrados, identidades racionales de dualidad, invariancia por
representantes, minimización entera, recuentos de código y cociclo de
concatenación. Sus 605 muestras racionales son pruebas finitas, no una
demostración automatizada de todos los enunciados. El control del enlace
elíptico añade la identidad polinómica, las cotas de pertenencia y los casos
negativos; las pruebas generales están en las tres secciones incorporadas.

Los dos controles nuevos añaden 43.503 y 9.072 comprobaciones exactas por modo,
respectivamente. Trabajan con enteros y fracciones racionales, y las condiciones
de comprobación no desaparecen con `-O`. Su éxito acredita esas instancias
finitas; las demostraciones generales y sus condiciones están en el capítulo
conjunto del continuo.

La suite pública utiliza exclusivamente las copias locales y declara
`SOLO_HASHES_DECLARADOS`, con cero originales externos cotejados. El verificador
focal individual permite además un cotejo con originales cuando se ejecuta
separadamente en un entorno que los conserve. La comprobación de hashes depende de la integridad del propio
manifiesto y registro; no es una autenticación independiente de su autoría.

## 4. Recompilación opcional del PDF

Además de Python, se necesitan LuaLaTeX y `kpsewhich` de TeX Live o MiKTeX, los
paquetes LaTeX usados en `main.tex` y las fuentes **STIX Two**. En TeX Live, éstas
corresponden al paquete `stix2-otf`, incluidos los estilos de texto y la fuente
matemática. Son dependencias del entorno de compilación, separadas del corpus.

```bash
python3 -I -S reproducir.py --compile
```

Si LuaLaTeX no está en la ruta de ejecutables:

```bash
python3 -I -S reproducir.py --compile --lualatex /ruta/al/ejecutable/lualatex
```

El reproductor verifica primero el manifiesto y la suite local. Copia únicamente
los miembros inventariados a `reproduction/compilacion_<identificador>/`.
Dentro de esa copia consume el recibo vigente de preflight y comprueba sus
vínculos locales y el grafo de fuentes. Las autoridades externas quedan como
constancia de la ejecución editorial original, sin simular una reejecución.
Después realiza **tres pases LuaLaTeX**, con ejecución de órdenes externas
desactivada y caché tipográfica local. Dentro de la copia aparecen:

```text
output/pdf/MOONSHINE_DUALIDAD_T_TEORIA_M_CONTINUO.pdf
tmp/build/<ejecución>/main.log
tmp/build/<ejecución>/main.fls
tmp/build/<ejecución>/pass-1.txt  (y pass-2.txt, pass-3.txt)
tmp/texcache/
technical/compilacion/<ejecución>/RECIBO_COMPILACION.json
technical/compilacion/<ejecución>/MANIFIESTO_COMPILACION.json
```

No sobrescribe el PDF entregado, los recibos previos ni las fuentes. El nuevo
recibo registra el comando, el motor utilizado, los avisos de cada pasada,
las huellas de las fuentes propias y las dependencias leídas según el recorder.
Distintas versiones de TeX o metadatos pueden producir PDFs binariamente
distintos. Compilar sin errores no sustituye la comprobación de referencias,
la inspección visual ni la validación matemática.

## 5. Alcance matemático y condiciones conservadas

Este paquete no afirma ejecutar todos los productores Python del integral ni
incluye una formalización Lean de sus resultados. No se simulan archivos Lean,
certificados inexistentes ni controles de productores no ejecutados. Los hashes
protegen identidad documental; las demostraciones se leen en sus cuerpos y las
referencias a teoremas externos mantienen su atribución.

La ampliación del continuo conserva conjuntamente operaciones sobre las mismas
historias, con sus pruebas locales, condiciones de especialización y mapas de
compatibilidad. No transforma una isometría interna en una identificación
automática con las columnas completas de Weil. Ni las doce ejecuciones finitas,
ni los recibos documentales, ni el nuevo capítulo se presentan como prueba de
positividad global de Weil o de RH. La lectura del integral y de otros propietarios
fue focal y está registrada; no se afirma que se haya leído íntegramente el corpus.

La sección de α conserva por separado la normalización posicional, el
resolvente finito y la identificación de límites compatibles. Su proposición de
igualdad usa la pertenencia de ambas vías a los mismos cilindros, cuyos
diámetros tienden a cero. La nota de alcance del manuscrito declara qué
operaciones se han recuperado explícitamente y qué compatibilidad analítica a
toda profundidad no ha quedado reconstruida de forma autónoma en este
borrador. Ni la compilación ni el control focal convierten esa proposición
condicional en una identidad demostrada sin esas premisas.

De igual modo, las pantallas y la equivalencia unitaria del Hamiltoniano
compacto conservan sus dominios. La identificación física undecadimensional
mantiene las condiciones de campos, tensión, osciladores, amplitudes, anomalías
y límite de baja energía expresadas en el manuscrito. El transporte de
supercarga exige sus operadores y entrelazamientos. La coincidencia de rangos
no sustituye esos mapas. El Monstruo actúa en `V^natural`; no se postula una
flecha universal que identifique por sí sola Moonshine con toda la teoría M.

La selección, reutilización y ampliación de fuentes se rige por continuidad
documental, procedencia y clausura de las dependencias pertinentes. Este README
orienta la lectura y reproducción de la entrega concreta; no sustituye el
contenido demostrativo del artículo.
