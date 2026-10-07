# Guía de reproducción de la edición integrada

Esta guía corresponde a `ARITMETICA_PRIMOS_DOBLE_CIRCULO_INTEGRADA_20260911`.
Los comandos se ejecutan desde la raíz de la carpeta descomprimida, que contiene
`main_lectura.tex`, `technical/`, `ampliacion/` y `nucleo_comun/`. Mantener juntos
esos archivos. Las rutas siguientes son relativas y no requieren el directorio
personal del equipo de edición.

El orden de esta guía gobierna la reproducción de la **integración actual**.
Los README, recibos y ensambladores heredados se conservan como antecedentes de
sus propios cortes; no se deben ejecutar indiscriminadamente para regenerar esta
edición. En particular, recompilar el LaTeX integrado es distinto de volver a
convertir los Markdown anteriores, que no contienen por sí solos todas las
incorporaciones.

## 1. Orden causal y lectura previa

La dependencia es:

`rectas 0–10/0–9 → APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo → publicaciones y lectores → reconocimiento posterior`.

Se lee primero el núcleo formal incluido en el manuscrito; después, la construcción
aritmética y los lectores; finalmente, el expediente de doble círculo, centro,
frontera, memoria y vacancias. Las cinco construcciones del continuo permanecen
conjuntas. La fase retorna sin reiniciar la historia.

El catálogo y sus estados preceden a los lectores de firmas. La densidad de
vacancia procede de comparar los bloques `3^6=729` y `10^3=1000`; no recibe una
constante objetivo. El certificado de Schur recibe una publicación HMT previa de
π y autentica sus antecedentes locales: es un uso posterior, no una nueva
generación de π ni una entrada metrológica que seleccione el estado.

## 2. Entorno y carpeta de resultados

Se necesitan Python 3.9 o posterior y `mpmath==1.3.0` para el certificado intervalar
de Schur. Los demás controles de esta guía utilizan la biblioteca estándar.
LuaLaTeX sólo se necesita para producir el PDF.

Si el entorno disponible no contiene `mpmath`, puede prepararse uno local. Estos
comandos son instrucciones para el receptor, no constancia de una instalación
realizada al escribir esta guía:

```sh
python3 -m venv .venv-reproduccion
.venv-reproduccion/bin/python -m pip install -r ampliacion/expediente/requirements_schur.txt
```

En los comandos siguientes, `python3` debe ser el intérprete que contiene esa
biblioteca. Si se usa el entorno anterior, sustituirlo por
`.venv-reproduccion/bin/python` —en Windows, `.venv-reproduccion/Scripts/python.exe`—.

Crear una carpeta nueva para no sobrescribir recibos de la entrega:

```sh
mkdir RESULTADOS_NUEVOS
```

Si ese nombre ya existe, elegir otro y sustituirlo en todos los comandos. La
subcarpeta `doble_circulo` del paso siguiente **no debe existir**: el reproductor
comprueba esa condición y no mezcla resultados de ejecuciones diferentes.

## 3. Controles del expediente: doble círculo y centro–frontera

```sh
python3 ampliacion/expediente/reproducir_controles.py --centro-borde --output RESULTADOS_NUEVOS/doble_circulo
```

El programa ejecuta cinco familias en modo normal y optimizado, guarda sus JSON
y registros de ejecución, y escribe `RECIBO_CONJUNTO.json`. El resultado esperado
es `PASS_CONTROLES_FOCALES_DOBLE_CIRCULO`, con diez ejecuciones satisfactorias.
No añadir `-S` a este comando: Schur necesita cargar `mpmath`. El reproductor
aplica por sí mismo `-I -S` a los controles independientes de esa biblioteca.

| Familia | Controles por modo | Alcance del certificado |
|---|---:|---|
| Costura | 210 | Identidades finitas de compresión, complemento y conservación de memoria. |
| Momentos de memoria | 1.046 | Identidades algebraicas finitas de los modelos de memoria; no todos los momentos aritméticos globales. |
| Expectativa | 25 | Acciones sobre modos y productos cruzados en las cartas especificadas. |
| Schur | 21 | Cotas intervalares de la prueba funcional para la ventana de longitud `1/9`; no todas las ventanas. |
| Centro–frontera | 11.430 | Cartas, levantamientos, vacancias locales y costura; el censo regional recibido no se vuelve a generar aquí. |

Los 25.464 controles de las diez ejecuciones son comprobaciones focales. Las
demostraciones sobre dominios infinitos son las pruebas escritas del manuscrito
y del expediente, no una extrapolación de ese conteo. El ensayo
`explorar_schur_ventana_con_primo.py` queda fuera de esta cadena certificada.

La carpeta local `ampliacion/expediente/dependencias_viii/` contiene los antecedentes
necesarios para Schur. Debe conservarse completa: no sustituir sus archivos ni
volver a copiarlos desde otra edición para resolver un fallo de huella.

## 4. Firma producto `555555` y memoria de transporte

```sh
python3 -I -S ampliacion/verificar_memoria_555555.py --receipt RESULTADOS_NUEVOS/MEMORIA_555555_NORMAL.json
python3 -O -I -S ampliacion/verificar_memoria_555555.py --receipt RESULTADOS_NUEVOS/MEMORIA_555555_OPTIMIZADO.json
```

Resultado esperado: `PASS_MEMORIA_555555_324_RUTAS`. Enumera las 324 posiciones
orientadas, las 26 firmas producto y su refinamiento estable `26→28→28`. La fibra
de `555555`, de 24 representantes, se descompone en tres hojas de ocho bajo avance
y media vuelta. Se comprueban también las órbitas de tamaños `1,9,9,9`.

Este certificado conserva el tipo de la firma regional y su memoria finita. Su
relación con la celda electrónica `(5,5)` se expone mediante los mapas del
manuscrito; el control no identifica ambos objetos ni sustituye la historia
enriquecida completa por una firma de seis cifras.

## 5. Vacancias `21/22` y retornos inducidos `6/7`

```sh
python3 -I -S ampliacion/verificar_vacancias.py --receipt RESULTADOS_NUEVOS/VACANCIAS_NORMAL.json
python3 -O -I -S ampliacion/verificar_vacancias.py --receipt RESULTADOS_NUEVOS/VACANCIAS_OPTIMIZADO.json
```

Resultado esperado: `PASS_VACANCIAS_RACIONALES_21_22_6_7`, con 48.614 controles por
modo en la configuración predeterminada. Utiliza fracciones racionales, series
de logaritmos y cotas explícitas de resto; sólo acepta una parte entera cuando
los dos extremos de su horquilla dan el mismo entero. Reproduce 512 vacancias
hasta el bloque 11.189 y 64 separaciones secundarias, además de los balances,
mesetas y cambios de escala.

Los teoremas universales están en `ampliacion/vacancias_21_22_6_7.tex`. Distinguen
las separaciones primarias en bloques, los índices de los intervalos cortos,
el selector TRIT y los relojes cronológico y de capacidad. Los valores `6/7`
no significan alternancia estricta. Para un rango mayor pueden usarse
`--events`, `--short-events` y `--series-order`; si la horquilla no decide una
parte entera, el programa falla y debe aumentarse su orden, sin redondear.

## 6. Compilar el LaTeX integrado, sin regenerar sus fuentes

Requisitos tipográficos: LuaLaTeX/TeX Live, STIX Two Text, STIX Two Math y los
paquetes declarados en `preambulo_lectura.tex` —entre ellos `fontspec`,
`unicode-math`, TikZ y `cleveref`—. El compilador no instala dependencias.

```sh
python3 technical/compilar.py . --main main_lectura.tex --pdf-name PRIMOS_DOBLE_CIRCULO_REPRODUCIDO.pdf --build-dir build_reproduccion --receipt RESULTADOS_NUEVOS/COMPILACION.json
```

Elegir nombres nuevos si `build_reproduccion` o el PDF de reproducción ya existen.
Si LuaLaTeX no está en `PATH`, añadir `--lualatex /ruta/al/ejecutable/lualatex`.
El programa realiza tres pasadas y escribe el PDF reproducido en `output/pdf/`,
junto con una huella y el recuento de advertencias en el recibo indicado. No altera
las fuentes ni regenera capítulos a partir de los antecedentes Markdown.

## 7. Interpretación y conservación de los recibos

Una compilación satisfactoria certifica composición tipográfica, no los teoremas.
Las advertencias y las páginas deben revisarse visualmente; la presencia de un
PDF no sustituye esa lectura. Los controles documentales de continuidad tampoco
equivalen a completitud demostrativa.

Conservar por separado los recibos recibidos y los recién producidos. Ante un
fallo, guardar el registro y localizar la operación afectada; no modificar una
huella, un resultado esperado o una prueba para convertirlo en `PASS`. Ninguno
de los controles de esta guía certifica por sí solo la positividad global de
Weil o el cierre de RH. Su alcance está registrado por familia y permanece
separado del contenido demostrativo del manuscrito integrado.
