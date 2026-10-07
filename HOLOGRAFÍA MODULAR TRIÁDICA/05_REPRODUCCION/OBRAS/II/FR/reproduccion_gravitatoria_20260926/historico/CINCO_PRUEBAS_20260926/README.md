# Reproducción focal de la composición gravitatoria

Esta carpeta contiene cinco verificadores, sus entradas efectivas y las demostraciones que acompañan los cálculos. Su ámbito es la composición longitudinal, métrica y angular de la realización examinada. Los artículos II y VII se conservan fuera de esta carpeta.

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

Los indicadores de alcance emitidos por cada programa se conservan tal como estaban en las fuentes. En particular, un indicador negativo en el verificador de sustitución delimita **lo que esa sustitución comprueba por sí misma**; no es un dictamen sobre todos los resultados contenidos en las demás demostraciones.

`datos/` incluye las tres expansiones regionales archivadas de mil decimales y `EVALUACION_VACIO.json`. El registro K se lee de este último archivo. `propietarios/` contiene la fuente de la ecuación del contraángulo. `demostraciones/` conserva íntegramente los cuatro desarrollos focales. Ningún archivo Lean forma parte de esta reproducción; no se declara aquí una certificación Lean ni una regeneración integral del TPK.

## Procedencia y conservación

`procedencia/ORIGENES.json` identifica las fuentes de cada copia. `procedencia/PROCEDENCIA_SHA256.json` registra la huella de la fuente, la de la copia y la adaptación realizada. `procedencia/originales_scripts/` conserva los cinco programas anteriores a la adaptación. Sólo dos programas han cambiado: sus rutas de lectura apuntan a esta carpeta; sus fórmulas, filtros, aserciones y estatutos permanecen intactos. Los otros tres programas, los datos y los textos son copias exactas.

`MANIFIESTO_LOCAL.json` permite comprobar la integridad de todos los archivos necesarios. Los informes regenerables de `resultados/` quedan fuera del manifiesto. Las rutas originales citadas en la procedencia y en las demostraciones son localizadores documentales, no dependencias de ejecución. La opción `--registrar-procedencia` se reserva al mantenimiento de esta copia en el ordenador de origen; la ejecución ordinaria no la necesita ni consulta esas rutas.

La suma de comprobación SHA-256 identifica los bytes conservados y detecta una modificación accidental. No sustituye una demostración matemática ni certifica por sí misma el origen generativo de los datos.
