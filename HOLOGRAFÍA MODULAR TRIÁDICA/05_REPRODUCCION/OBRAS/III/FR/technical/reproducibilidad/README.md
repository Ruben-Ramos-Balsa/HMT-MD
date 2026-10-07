# Reproducción técnica focal del artículo III

## Contenido efectivo

Este directorio conserva 24 archivos originales con identidad binaria y procedencia SHA-256, un ejecutor portable y un certificado finito adicional. Los originales incluyen:

- el programa de confluencia espectral del borrador 02 y los diez archivos que ese programa identifica mediante huellas, contando el propio programa;
- el propietario adicional B01 de la precedencia dodecafásica;
- D07 y B06 de la revisión de trabajo 05 del artículo II;
- dos secciones y dos notas de alcance del artículo I de 117 páginas;
- los propietarios 06e, U008 y U016 del núcleo;
- el catálogo de 468 emisiones, el catálogo de rutas y dos verificadores históricos de esos datos.

El PDF dentro de `originales/BORRADOR_02/output/pdf/` es un **antecedente histórico conservado porque el programa original calcula su huella**. No es el artículo III. El manuscrito III y sus fuentes I/II están en el árbol superior de esta entrega. El archivo `MANIFIESTO_ORIGINALES.json` discrimina cada fuente, destino, función y huella.

## Dependencia matemática y orden de lectura

La exposición parte de APP–TRIT–TPK. Las publicaciones regionales y el registro dodecafásico anteceden a la acción, al par angular, a los canales contractivos y a sus lectores constitutivos. Las constantes convencionales o metrológicas no se emplean para seleccionar los estados de los controles aquí ejecutados.

El orden de lectura es:

1. Núcleo, recurrencia de emisión y generación regional del artículo I copiado en `base_articulo_I`.
2. Registro de transiciones y reconstrucción de los levantamientos, registro firmado y construcción de K; conservar las dependencias y los límites de exposición declarados en esas secciones.
3. Propietarios de la acción, par angular y canales del artículo II copiados en `base_articulo_II`.
4. Propietarios A07, B01, B03, B04 y B06: precedencia de acción y ángulos, pesos dodecafásicos, operador de área y lectura modular.
5. D06 y D07: inversión de las coordenadas del vacío, orientación y momentos de profundidad. D07 es una fuente extensa de procedencia; su inclusión íntegra no convierte cada una de sus secciones en resultado anunciado por el artículo III.
6. `originales/BORRADOR_02/04_DESARROLLO/CONFLUENCIA_ESPECTRAL_Y_JERARQUIA_20260907.md`, que compone esos lectores y diferencia sus dominios.
7. Demostraciones propias del cuerpo del artículo III y su apéndice de enumeración finita.

El orden de ejecución siguiente organiza **comprobaciones de alcance distinto**. No afirma que ejecutar el censo produzca por sí solo las matrices regionales o que el programa de confluencia genere las constantes primarias. Esa distinción es parte del resultado que debe conservar cualquier revisión humana o asistida.

## Ejecución portable

Requisito: Python 3.9 o posterior, sólo biblioteca estándar. No se requieren acceso a red, paquetes numéricos, valores metrológicos, TeX ni rutas privadas. Desde este directorio:

```sh
python3 -I -S reproducir.py --integrity-only
python3 -I -S reproducir.py
```

El ejecutor realiza, sin omitir etapas:

1. Verificación de `SELLADO.json` y de los 24 originales conservados. También comprueba que D07/B06 de B02 e II son idénticos.
2. Enumeración de las condiciones iniciales desde la recurrencia declarada, seguida de la comparación con el catálogo preservado. El catálogo se carga **después** de construir las emisiones. Se comprueban 324 condiciones por cursor, 104976 parejas, 18 y 26 firmas, 468 emisiones y 243 palabras ternarias.
3. Reconstrucción exacta de L0/L1 desde las cuatro matrices de transiciones impresas en 06e. La eliminación se realiza sobre F3. Se enumeran los 16 calendarios binarios y las 144 modificaciones unitarias. Este control recibe el registro de transiciones, no construye su antecedente mediante selección, transporte y actualización.
4. Ejecución sin modificación del programa original de confluencia: 44 comprobaciones algebraicas y regresiones racionales separadas.
5. Escritura de salidas auténticas, huellas de programas y recibo agregado en `ejecuciones/`.

Cada proceso debe terminar correctamente; un error de integridad o una comprobación fallida detienen el ejecutor. No se sustituye el resultado por un indicador manual. El recibo conserva el alcance de cada prueba y los hashes de sus salidas.

Para comprobar además las 58 copias que figuran en los tres manifiestos I/II de la entrega completa:

```sh
python3 -I -S reproducir.py --check-article-copies
```

Esta opción requiere el árbol III completo. El modo predeterminado sólo requiere este directorio de reproducción. En la máquina donde siguen presentes los propietarios originales puede añadirse `--check-sources`; esa opción es un contraste local de procedencia y **no** un requisito portable.

## Alcance de los resultados

`verificar_nucleo_finito.py` genera las emisiones desde el soporte y la ley de emisión explícitos, conserva las 44 clases con todas sus preimágenes y reconstruye los levantamientos desde el registro publicado. El fichero `NUCLEO_FINITO.json` contiene las 468 emisiones, su reducción ternaria, las cuatro matrices, las dos soluciones, las tres sucesiones, los 16 calendarios y las 144 perturbaciones. Su justificación científica se desarrolla en `manuscrito/sections/11_nucleo_finito.tex`; el código permite reproducir los censos, no reemplaza el argumento de inyectividad ni el de unicidad matricial.

El programa de confluencia comprueba identidades polinómicas generales con coeficientes racionales, el residuo dodecafásico, la inversión de la matriz de incidencias y cuatro pares racionales de regresión. No ejecuta la generación primaria de pi, phi, e o alfa, no evalúa CODATA y no formaliza por software los límites analíticos ni el cálculo funcional. Las identidades logarítmicas y los dominios de inversión se justifican en el texto. La salida original mantiene literalmente esa delimitación.

Los dos verificadores históricos bajo `originales/CENSO_REGIONAL/pruebas/python/` se conservan como antecedentes íntegros y **no son llamados por el ejecutor**. En particular, `verificar_dinamica_cociente_468.py` contiene controles posteriores de lecturas y evaluaciones que exceden el censo aquí aislado. No se presenta su presencia en la carpeta como ejecución de esos controles ni como una nueva generación primaria.

No se incluye una formalización Lean nueva. Tampoco se emite una certificación global de autonomía, de equivalencia a toda profundidad entre las vías de alfa, de interpretación física o de publicabilidad. La compilación del artículo es otra operación, dirigida por su constructor editorial, y no forma parte de este ejecutor.

## Preparación y conservación

`preparar_paquete.py` es el colector mecánico **local**: conserva rutas absolutas para localizar los antecedentes al preparar esta edición. Esas rutas no participan en `reproducir.py` salvo que se solicite explícitamente `--check-sources`. El colector no se debe ejecutar en la máquina receptora para reproducir las pruebas; las fuentes ya están incluidas.

`python3 -I -S reproducir.py --seal` crea el sellado técnico al preparar una edición. Rechaza reemplazar un sellado existente por otro contenido. Para modificar las fuentes se debe crear una revisión y conservar la anterior. Un hash verifica identidad, no es una firma institucional ni demuestra la veracidad matemática del archivo.

Los recibos generados quedan fuera del sellado para permitir nuevas ejecuciones. Se incluye una ejecución de referencia real. No puede certificarse que una IA obedezca un texto; sí se puede exigir que cualquier afirmación de reproducción venga acompañada de los comandos, estados y recibos verificables correspondientes, manteniendo los dominios y las dependencias indicados.
