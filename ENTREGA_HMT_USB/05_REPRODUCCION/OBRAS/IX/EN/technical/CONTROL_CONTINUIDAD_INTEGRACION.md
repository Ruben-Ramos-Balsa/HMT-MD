# Continuidad material de la ampliación de primos

Identidad binaria de fuentes, preservación de cuerpos y grafo de inclusión; no certificación de completitud matemática global, de positividad de Weil ni de RH.

## Corte de comparación

- OLD: `/Users/ruben/Documents/New project/output/PRESENTACION_ACADEMICA_SERIE_20260911/PRIMOS_Y_FUNCION_ZETA`.
- NEW: `/Users/ruben/Documents/New project/output/ARITMETICA_PRIMOS_DOBLE_CIRCULO_INTEGRADA_20260911`.
- Expediente: `/Users/ruben/Documents/New project/output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911`.

## Resultado de identidad binaria

| Grupo | Coincidencias | Total |
|---|---:|---:|
| nucleo_comun_activo | 6 | 6 |
| nucleo_comun_copia_archivada | 6 | 6 |
| cuerpos_tex_generados | 5 | 5 |
| apendices_tex | 9 | 9 |
| manuscritos_cinco | 5 | 5 |
| propietarios_archivados_apendices | 9 | 9 |
| cinco_desarrollos_expediente | 5 | 5 |
| soporte_antecedentes | 4 | 4 |

Todos los archivos de los grupos anteriores son byteidénticos.

El JSON conserva las dos rutas y sus SHA-256 por cada archivo. En las seis fuentes comunes se contrasta además la huella del manifiesto del núcleo.

## Cambios separados de los cuerpos

- `main_lectura.tex`: Portada y orden de inclusión; título y autores conservados; añade ampliaciones sin retirar inputs anteriores.
- `preambulo_lectura.tex`: Cambios de comentario/metadata y protección de inicio de entornos; conserva fuentes tipográficas y macros comunes.
- `gestion/lectura_resumen.tex`: Añade resultados de la ampliación y palabras clave; conserva párrafos anteriores y alcance global.
- `gestion/lectura_introduccion.tex`: Amplía organización y narrativa centro–frontera; mantiene delimitación de alcance.
- `gestion/lectura_conclusiones.tex`: Amplía resultados de reconstrucción, memoria y coercividad; conserva advertencia de positividad global no demostrada.
- `gestion/lectura_bibliografia.tex`: Ampliación autorizada de tres referencias internas; separada de la comparación byteidéntica de cuerpos y apéndices.

Inputs previos retirados del maestro: 0. Los cinco cuerpos generados, los nueve fragmentos de apéndice y sus propietarios archivados se comprueban por separado.

## Inclusión estática y compilación

- nucleo_comun_activo: 6/6 accesibles por inclusión desde el maestro.
- cuerpos_tex_generados: 5/5 accesibles por inclusión desde el maestro.
- apendices_tex: 9/9 accesibles por inclusión desde el maestro.
- FLS final `build_integrada/main_lectura.fls`, directorio de trabajo NEW y log terminado: 150 páginas. Se acredita inclusión material de las seis fuentes comunes, cinco cuerpos y nueve fragmentos de apéndice; el FLS de OLD permanece identificado sólo como antecedente.
- Los 9 archivos TeX de ampliación, incluida `figura_compresion_circular.tex`, figuran en el FLS final. Sus huellas actuales se conservan en el JSON.
- PDF final: SHA-256 `d96733bdc47c4f37903202ba823c228911cc779c1d3c143aef360836900418c0`; copia de entrega byteidéntica al PDF de `build_integrada`.
- Log final: overfull=0, missing_glyph=0, undefined_references=0, multiply_defined_labels=0. Este control no reemplaza la inspección visual.

## Alcance y conservación

Este control no modifica manuscritos, macros, PDF, índices ni fuentes concurrentes. La identidad de archivos y la presencia en el grafo de inclusión son controles documentales distintos de la suficiencia de las demostraciones. Los cambios de apertura y cierre se documentan mediante diffs completos en el JSON; no se interpretan como modificación de los cuerpos preservados.
