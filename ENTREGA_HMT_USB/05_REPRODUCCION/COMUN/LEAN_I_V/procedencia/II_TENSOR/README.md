# Portador tensorial pentádico del artículo II

Esta ampliación formaliza la instancia matricial finita del manuscrito y compone su realización con `HMT.I.SelectedAction.phi`, procedente del paquete principal del artículo I. No modifica aquel paquete ni recompila sus módulos.

`PentadicTensorCarrier.lean` construye el reloj cociente de 108 posiciones, la tabla de seis ejes orientados y doce posiciones, la involución antipodal y el proyector racional `P5`. Demuestra simetría, idempotencia, traza cinco y anulación de la componente constante. Los tensores son matrices reales de tamaño tres, simétricas y de traza nula. Su carta de cinco coordenadas se demuestra exhaustiva; por tanto, el dominio tensorial no es una tupla arbitraria de cinco escalares.

La realización concreta de los seis ejes proporciona `Qsix`, y la tabla de posiciones proporciona `Qposition`. Sus productos de Frobenius dan exactamente `(8/5)P5`. Se demuestran las identidades `Gamma0 Gamma0Adj = (8/5)I`, `Gamma5 Gamma5Adj = I` y `Gamma5Adj Gamma5 = P5`, con la normalización `sqrt(5/8)` del manuscrito. La raíz radical de la carta geométrica se mantiene como reconocimiento posterior.

`SelectedPentadicTensor.lean` importa `SelectedActionDomain` desde el paquete sellado de I. Su coordenada `phi` está definida por el límite de la sucesión modal y se reconoce mediante `AlphaCarryLimit.autoscale_recognition`. El módulo demuestra las condiciones algebraicas de esa coordenada, especializa las identidades del marco tensorial y construye `selectedTensorEquivalence : V5 ≃ STF`, con pruebas de pertenencia y ambas inversas. La importación conserva los objetos compilados y recibos anteriores.

La reducción transversal se formaliza en el marco cuyo eje es el tercer vector coordenado. Se demuestran idempotencia, autoadjunción de Frobenius, anulación de la componente longitudinal y descripción exacta de la imagen por dos parámetros matriciales. El resultado es el proyector transversal de esa carta; no declara derivadas ecuaciones de propagación gravitatoria.

## Reproducción

Ejecutar `bash reproducir.sh` desde este directorio o desde la raíz del proyecto. El guion usa Lean 4.21.0 y los directorios de objetos declarados en `REGISTRO_REPRODUCCION.json` del paquete principal de I. Compila únicamente los dos archivos nuevos con `-DwarningAsError=true`; genera sus dos objetos y sus dos registros de compilación. Los enunciados terminales imprimen sus dependencias axiomáticas.

## Alcance exacto

La tabla incidencial y los seis ejes concretos son los del manuscrito. Esta ampliación prueba sus identidades matriciales y consume la coordenada seleccionada en I. No formaliza nuevamente la derivación de la tabla desde todas las rutas enriquecidas del TPK, ni añade una prueba de equivariancia global bajo la acción de `A5`. El reloj es una proyección finita del estado enriquecido: su período 108 no expresa reinicio de la memoria. La reducción transversal se prueba para un eje coordinado; la covariancia para un eje unitario arbitrario no forma parte de este incremento. La equivalencia se entrega como `Equiv` con identidades del marco; no se declara empaquetada como `LinearIsometryEquiv`.

## Propietarios del manuscrito

- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/02/ES/source/sections/representacion_dodecafasica_rev08.tex`: reloj, posición, tabla de vértices firmados, tensores y normalización.
- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/02/ES/source/sections/10d_portador_pentadico_rev06.tex`: portador pentádico, producto de Frobenius, equivalencia tensorial y reducción transversal.
- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/02/ES/source/sections/incidencia_icosaedrica_rev07.tex`: incidencia y marco real de seis ejes.
- `SelectedActionDomain.lean`, `AlphaCarryLimit.lean` y `AutoscaleLimit.lean`, con localización material fijada en el registro de reproducción del paquete principal de I: coordenada seleccionada, límite generado y reconocimiento posterior.

No se ha editado el tratado, la fuente central, los certificados previos ni ningún archivo ZIP.
