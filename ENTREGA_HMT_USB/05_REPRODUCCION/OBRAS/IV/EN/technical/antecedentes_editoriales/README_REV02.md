# Artículo IV — Moonshine, dualidad T y teoría M — Revisión 02

**Moonshine, dualidad T y teoría M desde la estructura discreta del continuo**

Oumar Haidara Fall · Rubén Ramos Balsa

Borrador de trabajo para revisión académica. Este directorio reúne el manuscrito
LaTeX, las figuras, las fuentes de procedencia y los controles ejecutables
incluidos en esta edición. La distribución final se identifica mediante
`MANIFIESTO_ENTREGA.json`, preparado después de la revisión editorial y visual.
La existencia de fuentes compilables no equivale por sí sola a una entrega
cerrada. Si todavía no existe ese manifiesto, `reproducir.py` se detiene antes
de ejecutar los controles o la compilación.

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
4. **Generación coinductiva.** Regiones y publicaciones de π, φ y e; compatibilidad
   de cilindros y retorno de fase con avance de memoria.
5. **Registro dodecafásico K.** Registro de canales, transformación firmada,
   reconstrucción entera y evaluación racional. La evaluación no sustituye su
   cadena de procedencia.
6. **Constante de estructura fina.** Clausura entera, lector analítico de
   vacancias y estatuto preciso de su identificación a toda profundidad.
7. **Prolongación excepcional.** Incidencia de K y α, código ternario, Witt,
   Niemeier, Leech y álgebra de operadores de vértice; construcciones de
   Moonshine de órdenes 2 y 3 y sus teoremas externos identificados.
8. **Realización hilbertiana.** Representación de Weyl, elevaciones, conservación
   de la unidad, cierre inductivo y realización tracial.
9. **Acción y publicación angular.** Cociente local, norma, valoración, carácter
   y renovación normalizada; secciones positivas, cartas en grados/radianes,
   conservación de acción e inversión de los canales.
10. **Elipse y determinación del radio.** Semiejes, prueba de pertenencia a la
    carta, ley areal, orientación simpléctica, radio positivo único y matriz
    reticular. La familia conserva las dos fibras recíprocas.
11. **Dualidad T.** Dominio entero, intercambio de coordenadas, radio,
   Hamiltoniano, clases residuales y equivalencia unitaria.
12. **Pantallas dimensionales.** Perforación de código, dirección producida por K,
    reducción de rango y cociente reticular, con sus respectivos núcleos.
13. **Acción y realización undecadimensional.** Descenso de observables,
    composición de trayectorias, supercarga y condiciones de compactificación.
14. **Conclusiones y referencias.** Resultados, condiciones y procedencia.

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
  incorporaciones de la serie conservan sus funciones y referencias. Estar en la
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
- `technical/verificar_radio_elipse.py`: identidad polinómica del radio,
  cotas racionales, transportes y pruebas de rechazo fuera del dominio.
- `technical/verificar_focal.py`: control de las cuatro secciones propias y seis
  antecedentes, más pruebas finitas de identidades concretas.
- `technical/CONTROL_FOCAL*.json`: recibos históricos de comprobación de esta
  edición. Los recibos de una nueva ejecución se guardan en `reproduction/`.
- `technical/preflight_rev02/`: contrato y preflight de esta revisión;
  `CORTE_ACTUAL.json` identifica el corte vigente bajo `runs/`.
- `technical/preflight_20260910/`: constancia histórica de la edición anterior,
  conservada sin utilizarla para autorizar la compilación nueva. Puede conservar rutas
  absolutas del entorno de origen. No es necesario disponer de ese entorno para
  ejecutar el reproductor portable.
- `technical/reproducir_controles_rev02.py`: suite de ocho ejecuciones, normal y
  optimizada, de controles focales, radio, siete antecedentes de II y grafo fuente.
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
ejecuta los cuatro controles locales tanto en modo normal como con `-O`
(ocho ejecuciones) y exige igualdad de sus resultados. Se escriben:

```text
reproduction/RECIBO_REPRODUCCION.json
reproduction/CONTROL_PORTABLE_REV02.json
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
output/pdf/ARTICULO_IV_MOONSHINE_DUALIDAD_TEORIA_M_REV02.pdf
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
