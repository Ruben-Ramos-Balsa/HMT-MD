# Generación regional reunida en VI

La sección `14_generacion_regional.tex` reúne material de I que necesita VI
antes de usar las coordenadas regionales. No modifica la edición de I.

## Propietarios leídos

Raíz: `/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910`.

- `sections/extension.tex`: dominio completo, dos cursores, calendario,
  emisor, firmas, multiplicidades y extensión cíclica108.
- `sections/generacion.tex`: selección de órbitas, condiciones diagonales,
  representantes regionales y representación lineal de transiciones.
- `sections/revision_monodromia.tex`, subsección «Simetría especular de las
  regiones y doble realización»: involución del bloque regional y su
  reconstrucción en F3. Esta subsección se leyó completa; la incorporación
  no pretende reproducir aquí todo su desarrollo excepcional.

## Contenido y procedencia

- `RESULTADO_RECUPERADO`: censo104976→468→243,43órbitas, selección de regiones,
  multiplicidades y calendario108.
- `FORMALIZACION_REUNIDA`: fórmula de posiciones `p_k=p+f(k)nu_d` que explicita
  la recurrencia temporal previamente dada. La comparación con el bucle
  temporal independiente se realiza para las648 condiciones de hoja.
- `CERTIFICADO_NUEVO`: generador finito independiente
  `generar_catalogo_regional.py`, que recibe sólo reglas y condiciones
  iniciales, y genera las tablas completas de18y26firmas y43órbitas.

Los 468registros se forman como producto de los catálogos de un cursor.
Cada registro JSON conserva las condiciones iniciales de ambas hojas;
su producto cartesiano enumera íntegramente sus semillas sin duplicar
innecesariamente104976bloques narrativos en el cuerpo del artículo.

## Alcance exacto del control

El programa verifica el emisor finito, su factorización y la selección
regional. No es el productor cronológico del libro canónico E108 ni una
prueba autónoma de todos los pasos de la prolongación infinita.
Las matrices X/Y de la representación de transiciones conservan la
procedencia de I; su inversión única no se promueve a generación de X/Y.

Las tablas impresas en el apéndice proporcionan todos los datos del censo
finito utilizados en las pruebas del cuerpo. El certificado añade la
enumeración de los cursores y permite reproducirlas sin un catálogo de
decimales de constantes como entrada.

## Ejecución

`python3 -I -S technical/generar_catalogo_regional.py`

Resultado observado: `PASS_CENSO_REGIONAL_FINITO_VI` con104976condiciones,
468emisiones,243palabras y43órbitas; representantes010211,201101,121200.
El programa rechaza la ejecución con `-O`, que desactivaría sus comprobaciones.
Los archivos de datos y las tablas se generan mecánicamente desde esa
misma ejecución; no se editan a mano.
