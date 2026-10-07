# Suplemento de evaluación conjunta portable — copia de control

Este suplemento añade el evaluador conjunto de la composición radial a una copia
de control del paquete focal. No modifica los cinco verificadores originales ni
su manifiesto. No constituye todavía la distribución final de las monografías.

Ejecutar desde cualquier directorio, con Python 3.9 o posterior:

```text
python3 -I -B -S /ruta/COMUN_REPRODUCCION/suplemento/verificar_suplemento.py
```

El evaluador recibe las coordenadas regionales y el registro K conservados en el
paquete. Reproduce la composición de longitud, acción retornada, respuesta radial,
coeficientes constitutivos, parámetro de Barbero, electrón y escala energética del
reloj térmico. Comprueba nueve identidades y estabilidad de 71 cifras significativas
al comparar cálculos de 100 y 140 cifras de trabajo. Esa estabilidad describe el
cálculo, no la precisión de una medición física.

`gravedad_estructural.py` conserva todas las fórmulas, condiciones y aserciones del
original. La única adaptación es la ruta `UPSTREAM`, que ahora resuelve el
verificador local. `originales/` conserva la fuente previa; el cotejo AST elimina
únicamente esa asignación antes de comparar el resto del programa. El diff exacto
está en `ADAPTACION_RUTAS.diff` y la traza en `PROCEDENCIA_ADAPTACION.json`.

`referencia/EVALUACION_CONJUNTA_ORIGEN.json` conserva el resultado anterior para
cotejar todos los valores y las nueve identidades. Sus rutas históricas son
procedencia documental, no dependencias de ejecución. El informe reproducido
registra las seis huellas efectivamente utilizadas dentro de esta copia.

`MANIFIESTO_SUPLEMENTARIO.json` sella sólo este suplemento y enlaza la huella del
manifiesto base sin sobrescribirlo. Los informes regenerables quedan en
`resultados/`. La comprobación también verifica la integridad completa de los
archivos que el manifiesto base enumera.

El éxito acredita reproducción focal con entradas archivadas y conservación de
las fórmulas. No vuelve a ejecutar APP–TRIT–TPK ni la selección de K, no contiene
una comprobación Lean, no compila PDFs y no transforma por sí solo una identidad
de la realización declarada en validación experimental.
