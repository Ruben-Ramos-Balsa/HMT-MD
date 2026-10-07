# Reproducción focal de la composición gravitatoria

Esta carpeta contiene siete verificadores, sus entradas efectivas y las demostraciones que acompañan los cálculos. Su ámbito es la composición longitudinal, métrica, angular y dinámica de la realización examinada. Los artículos II y VIII —este último conservado en el directorio técnico VII— se encuentran fuera de esta carpeta.

## Ejecución

Se requiere Python 3.9 o posterior, con su biblioteca estándar. Desde cualquier directorio:

```text
python /ruta/a/COMUN_REPRODUCCION/verificar_reproduccion.py
```

En Windows puede utilizarse `py -3` en lugar de `python`; las rutas con espacios se escriben entre comillas. En macOS suele emplearse `python3`. El verificador general comprueba las huellas del inventario, los imports declarados y las dependencias locales; ejecuta cada prueba en un directorio temporal ajeno al paquete, con las aserciones activadas. Conserva los resultados en `resultados/`. La comprobación de portabilidad es de rutas y ejecución Python: no equivale a una ejecución nativa de Windows cuando se realiza en macOS.

## Contenido y alcance demostrativo

| Verificador | Comprobación reproducida | Delimitación |
| --- | --- | --- |
| `verificar_transporte_radial_polar.py` | Archivo complementario, normalización polar del lector definido, transporte radial y distinción entre polarización y compresión anticipada. | Comprobaciones exactas con matrices racionales; las reglas del lector permanecen explícitas. |
| `verificar_composicion_metrica.py` | Mínimo con métrica global acoplada, transporte del lector, conservación de la respuesta variacional y reducción de Schur. | La transformación de la métrica debe acompañarse de la transformación del lector. |
| `verificar_rigidez_simultanea.py` | Compatibilidad simultánea de las reglas R1–R8, estabilidad ante cambios de representación y defectos de las renormalizaciones examinadas. | La rigidez se refiere al sistema completo de condiciones declarado en la demostración; las pruebas finitas acompañan ese argumento y no sustituyen su cuantificación general. |
| `verificar_sustitucion_estructural.py` | Composición desde las coordenadas regionales archivadas y K, evaluación de alfa, acción, electrón, velocidad constitutiva, longitud, acoplamiento y G; estabilidad decimal y equivalencia de fórmulas. | Reutiliza salidas HMT anteriores. No reejecuta el generador APP–TRIT–TPK ni el selector de K; la sustitución numérica sola no demuestra la selección física del lector. |
| `verificar_sustitucion_contraangulo.py` | Sustitución del contraángulo por su ecuación, recuperación de la acción y coincidencia de las expresiones angular, estructural y constitutiva de G. | Conserva explícitas las bases dimensionales; no convierte la equivalencia de expresiones en una derivación independiente del selector. |
| `verificar_accion_acoplada_y_fase.py` | 65 controles racionales: peso positivo global, términos cruzados, inversión, variación matricial, congruencia del generador, primer jet de fase, resolvente y transporte dual de la longitud. | La normalización procede del generador completo fijado en el teorema. Las matrices de ensayo comprueban sus identidades; su ejecución no selecciona un generador gravitatorio físico. |
| `verificar_rigidez_conjunta.py` | 202 controles racionales: dos productos normalizados, covarianza por congruencias duales, unidades, incidencia marcada y restitución constitutiva mediante el momento de Catalán. Incluye el control de fibra nula. | La unicidad del coeficiente se refiere a fibras no nulas y a los lectores positivos con secciones fijadas. La convención de radio reducido permanece explícita. La extensión a operadores no acotados exige las condiciones de dominio y límite de la demostración. |

Los tres primeros programas ejecutan respectivamente 82, 125 y 160 controles exactos. Las dos sustituciones verifican estabilidad a 71 cifras significativas; la sustitución estructural añade nueve casos radiales exactos y la del contraángulo comprueba ocho identidades en cada precisión de trabajo. El ejecutor exige los recuentos 82, 125, 160, 65 y 202, y conserva los informes completos de las siete pruebas. Las composiciones longitudinal y métrica R4/R5 se presentan como formalizaciones añadidas con sus condiciones explícitas; sus antecedentes no se convierten retrospectivamente en una prueba de esas composiciones.

El ejecutor realiza además el suplemento de `suplemento/`: reproduce 23 valores y nueve identidades del evaluador conjunto, con 71 cifras significativas estables y comparación exacta con el informe de procedencia. Este suplemento conserva el enlace entre longitud, acción retornada, velocidad constitutiva, Barbero, electrón y reloj térmico. Se registra separadamente de las siete pruebas anteriores. `gravedad_estructural.py` utiliza el verificador estructural local; el cotejo sintáctico con su original permite únicamente la adaptación de la ruta `UPSTREAM`.

Los indicadores de alcance emitidos por cada programa se conservan tal como estaban en las fuentes. En particular, un indicador negativo en el verificador de sustitución delimita **lo que esa sustitución comprueba por sí misma**; no es un dictamen sobre todos los resultados contenidos en las demás demostraciones.

`datos/` incluye las tres expansiones regionales archivadas de mil decimales y `EVALUACION_VACIO.json`. El registro K se lee de este último archivo. `propietarios/` contiene la fuente de la ecuación del contraángulo. `demostraciones/` conserva íntegramente los seis desarrollos focales. Ningún archivo Lean forma parte de esta reproducción; no se declara aquí una certificación Lean ni una regeneración integral del TPK. Las siete pruebas y sus importaciones locales utilizan únicamente las dependencias enumeradas en `LOCAL_DEPENDENCIES` del ejecutor. Las dos incorporaciones son independientes de `basereal/gravedad_estructural.py`; ese archivo pertenece a otros cálculos y no constituye una dependencia efectiva de estas pruebas.

## Procedencia y conservación

`procedencia/ORIGENES.json` identifica las fuentes de cada copia. `procedencia/PROCEDENCIA_SHA256.json` registra la huella de la fuente, la de la copia y la adaptación realizada. `procedencia/originales_scripts/` conserva los siete programas anteriores a la adaptación. Sólo tres programas han cambiado: sus rutas de lectura apuntan a esta carpeta; sus fórmulas, filtros, aserciones y estatutos permanecen intactos. Los otros cuatro programas, los datos y los textos son copias exactas. La prueba de rigidez conjunta corresponde a la revisión de 202 controles, que incluye la degeneración del espacio cero y formula la unicidad escalar sobre una fibra no nula.

`MANIFIESTO_LOCAL.json` permite comprobar la integridad de todos los archivos necesarios. Los informes regenerables de `resultados/` quedan fuera del manifiesto. Las rutas originales citadas en la procedencia y en las demostraciones son localizadores documentales, no dependencias de ejecución. La opción `--registrar-procedencia` se reserva al mantenimiento de esta copia en el ordenador de origen; la ejecución ordinaria no la necesita ni consulta esas rutas.

La revisión anterior de cinco pruebas se conserva completa en `historico/CINCO_PRUEBAS_20260926/`, con su manifiesto de 23 entradas, guía e informes originales. El suplemento recibido se conserva en `historico/SUPLEMENTO_GEMMA_20260926/`. Los nuevos resultados llevan la revisión `SIETE_PRUEBAS_Y_SUPLEMENTO_20260926`; no sustituyen documentalmente los informes históricos. El manifiesto actual incluye ambas copias históricas y excluye sólo los resultados regenerables actuales de la raíz y del suplemento, además de las cachés de Python.

La suma de comprobación SHA-256 identifica los bytes conservados y detecta una modificación accidental. No sustituye una demostración matemática ni certifica por sí misma el origen generativo de los datos.
