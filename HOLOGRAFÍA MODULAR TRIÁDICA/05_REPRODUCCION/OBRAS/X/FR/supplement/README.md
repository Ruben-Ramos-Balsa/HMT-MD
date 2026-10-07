# Continuación del artículo: memoria, forma y dualidad

Este paquete amplía la investigación del artículo `ARTICULO_MULTIMORFOLOGIA_K_20260918`, cuyo PDF de 25 páginas y archivo sellado se conservan sin cambios. Contiene demostraciones y fuentes para una integración posterior en ese mismo artículo; no crea otro PDF ni modifica la serie de diez publicaciones.

## Lectura

1. `00_MEMORIA_Y_FORMA.md`: composición de la reconstrucción de K ya publicada con la red positiva, el cono de memorias y su estabilidad.
2. `energy/energia_refinamiento.tex`: demostración matricial completa del lector energético, su complemento, la interpolación y la reducción de Schur.
3. `01_LIMITE_ENERGETICO.md`: demostración del límite analítico de las familias intervalares de energía acotada y de su archivo por escalas.
4. `nonadic/PROCEDENCIA_Y_COMPOSICION.md`: propietarios de las compresiones, distinción de sus dominios, reconstrucción exacta de K y covariancia con métrica transportada.
5. `leech/LEECH_K_DEFORMACION_THETA.md`: flujo sobre los doce planos marcados, dualidad euclídea, identidad theta, testigo de pérdida de integralidad euclídea y realización integral partida.

## Alcance matemático y procedencia

La reconstrucción mediante dos memorias y la dirección `u=P3L(m)` son **resultados recuperados** del artículo X, no nuevos descubrimientos de esta investigación. El espejo espectral y el balance de la compresión también tienen propietarios anteriores en VIII/X. La formalización del cono de memorias, su aplicación a la geometría positiva, el lector de energía intervalar y la composición del flujo con los planos marcados son desarrollos añadidos sobre esas premisas. Los principios de Schur, interpolación afín, completación energética y dualidad reticular se prueban aquí en sus dominios; no se reivindica novedad histórica de esos principios generales. La búsqueda focal de procedencia se documenta en las notas y no se presenta como búsqueda exhaustiva de todo el corpus.

Las demostraciones finitas y el límite de energía no sustituyen la construcción conjunta del continuo HMT ni sus certificados. El límite de esta ampliación es una realización analítica unidimensional posterior, con hipótesis explícitas de compatibilidad, malla decreciente y energía acotada. La realización positiva conserva el alcance del artículo previo: red de rango dos y amplituedro de rango uno en los dominios allí demostrados.

La deformación reticular preserva covolumen uno y la simetría de orden tres especificada. Su dual euclídeo corresponde al parámetro opuesto. Un vector explícito demuestra que la integralidad euclídea se pierde para parámetros no nulos suficientemente pequeños. La realización duplicada conserva, en cambio, una forma integral, par y autodual de signatura (24,24). Estas afirmaciones utilizan productos bilineales diferentes, declarados en la prueba.

## Continuidad material

Se mantiene la selección vigente de la serie: integral de 2.249 páginas y desarrollos especializados posteriores declarados en `CORPUS_ACTIVO.md`. El resolver global consultado todavía informa del testigo histórico de 2.084 páginas; su resultado se registra como desfase documental y no desplaza la selección vigente. No se ha modificado el localizador global ni ningún manifiesto sellado compartido.

Los propietarios especializados efectivos de esta ampliación son las versiones materiales de los artículos IV, VIII y X especificadas en `provenance/sources.json`, junto con el artículo de 25 páginas ya conservado. `provenance/owners/` contiene copias de los archivos seleccionados para facilitar la comprobación. Las fuentes de los pasos fundacionales heredados conservan sus rutas y huellas en el recibo genealógico.

## Comprobación

`python3 -I -S build_evidence.py` ejecuta los cuatro verificadores locales en modo normal, optimizado y aislado, registra sus resultados y aplica las puertas de genealogía y constantes al cuerpo reunido. Los cálculos exactos comprueban instancias, matrices y testigos; las pruebas cuantificadas y el paso al límite están escritos en los documentos. El resultado de una puerta documental no sustituye esas pruebas.

`python3 -I -S seal_package.py` produce el manifiesto y un archivo ZIP sin sobrescribir un archivo sellado previo. No hay compilación LaTeX ni generación de figuras en esta ampliación.
