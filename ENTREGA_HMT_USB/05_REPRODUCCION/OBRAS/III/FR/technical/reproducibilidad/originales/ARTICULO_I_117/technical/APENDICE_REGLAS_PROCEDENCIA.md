# Localización de las reglas de transporte y de extracción terminal

## Objeto y decisión de integración

La lectura focal solicitada concierne a dos dependencias del artículo: la producción del registro de transiciones que determina los operadores `L0,L1`, y la acción coordenada del extractor `E108^{90,120}` que produce doce coordenadas de cada canal y una carga total. No constituye una auditoría general del corpus, una nueva campaña numérica ni una decisión sobre la compatibilidad completa de las dos vías de alfa.

**Resultado de la búsqueda acotada:** se han recuperado completamente la reconstrucción de `L0,L1` a partir de las transiciones publicadas y la transformación de los 25 enteros de canal hacia el registro firmado y `K`. No se ha recuperado, en las fuentes y las implementaciones concretas enumeradas a continuación, una especificación coordenada ejecutable de las dos operaciones anteriores que produce esos datos. Por tanto, no se ha creado `sections/apendice_reglas_generativas.tex`: un apéndice que copiase las tablas e inversiones posteriores no satisfaría la clausura generativa solicitada.

Este límite se refiere a la recuperación material efectuada y a la autonomía de la exposición disponible. No equivale a una demostración de inexistencia de una construcción en cualquier otro documento del corpus.

## Fuentes consultadas

Raíz de la cantera (`C`):

`/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906`

Raíz de la fuente integral activa consultada (`S`):

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente`

Artículo sucesor (`A`):

`C/ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909`

Fuentes principales:

1. `C/fuentes/integral/manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex`, en particular líneas 45–154.
2. `C/fuentes/integral/manuscrito/propietarios_exactos/tpk/U016_registro_dodecafasico_hadamard_k.tex`, leído completo. Su copia en `S/manuscrito/propietarios_exactos/tpk/` es idéntica byte a byte en la comparación efectuada.
3. `S/manuscrito/ampliaciones_sucesoras_20260824/parte_i_ii/owners/U008_orbitas_elevacion_r36.tex`, leído completo.
4. `C/fuentes/integral/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex`, contraste del pasaje de reconstrucción de levantamientos, líneas 536–549.
5. `S/colaboracion/parte_iii/source/public_final/base_83/c25_body.tex`, contraste del pasaje del lector firmado, líneas 307–400.
6. `/Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py`, declaración inicial, matrices de las líneas 68–86 y funciones de aplicación de las líneas 544–567.
7. `/Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/ACTUALIZACION_TPK_ETA_Y_DETERMINANTE.md`, leído completo para distinguir la actualización del censo de eventos de la extracción terminal de los canales.

También se efectuaron búsquedas focales de los nombres del extractor y de sus coordenadas en los programas de `C/fuentes/investigacion`, en los programas de `S` y en el directorio de coordinación citado. Las búsquedas por sí solas no se toman como prueba de ausencia; la decisión se basa en los pasajes efectivamente leídos y en el inicio exacto de sus reglas coordenadas.

## 1. Reconstrucción finita de los operadores de transporte

### Material recuperado

`06e`, líneas 45–97, define los registros mediante los bloques de las tres sucesiones regionales. Para el primer operador, las filas de `X0` son `b0,b1` de cada sucesión y las de `Y0` son `b1,b2`; para el segundo, se usan las transiciones `b2→b3` y `b3→b4`. Las cuatro matrices se imprimen íntegramente. El mismo pasaje da la composición

\[
x_{j+1}^{\chi}=\mathcal U_{9j+9}\circ\cdots\circ\mathcal U_{9j+1}(x_j^{\chi}),
\qquad b_j^{\chi}=\Pi_6(x_j^{\chi}),
\qquad\mathcal U_t=\mathsf{Upd}_t\circ\mathsf{Tra}_t\circ\mathsf{Sel}_t.
\]

`06e`, líneas 99–123, establece la reconstrucción sobre `F3`:

\[
\det X_0=1,\quad\det X_1=-1,\quad X_aL_a=Y_a,
\qquad L_a=X_a^{-1}Y_a.
\]

El texto declara además el examen de los 16 calendarios binarios y de las 144 modificaciones unitarias de entradas. Las tres sucesiones completas y el calendario `0011` se encuentran en las líneas 127–149. Estos datos permiten formular una comprobación finita autónoma de la reconstrucción y del calendario, con las transiciones impresas como punto de partida.

### Límite de esa reconstrucción

La fórmula de composición de `U_t` y `Pi6` en este pasaje no despliega la acción coordenada de sus factores sobre los estados regionales que produce las cuatro matrices impresas. El paso de inversión matricial determina `L_a` una vez producido el registro; no produce por sí mismo ese registro anterior.

El ejecutable citado declara expresamente, en sus primeras líneas, que utiliza `L0,L1` como primitivas. Las matrices están incorporadas en las líneas 68–85, y `FINITE_CALENDAR` se fija en la línea 86. `finite_w30_from_tpk_lifts`, líneas 558–567, aplica esas matrices a las palabras seleccionadas. Este algoritmo reproduce las sucesiones a partir de los operadores; no aporta una construcción independiente de sus coeficientes a partir de los tres factores anteriores de `U_t`.

La elevación con residuos y cocientes de `U008`, líneas 381–407, sí es una regla completa:

\[
y_k=x_kA,\qquad u_k=y_k\bmod3,\qquad
x_{k+1}=(y_k-u_k)/3,\qquad
x_k=(u_k+3x_{k+1})A^{-1}.
\]

Su entrada incluye el levantamiento entero `A` de un operador ya fijado. Conserva y recupera la información del transporte; no sustituye el origen de los coeficientes de ese operador.

**Dependencia exacta por recuperar para el apéndice solicitado:** las reglas de selección, transporte, actualización y proyección sobre los estados regionales que permiten obtener `X0,Y0,X1,Y1` antes de usar `L0,L1` o sus sucesiones resultantes. Se requiere su acción sobre las coordenadas pertinentes, no sólo el nombre de la composición.

## 2. Extracción terminal de los 25 enteros

### Material recuperado

`U016`, líneas 256–298, define el estado terminal mediante 108 actualizaciones y presenta

\[
\mathcal E_{108}^{90,120}\bigl(\mathcal R_{12}(x_{\rm term})\bigr)
=(b^{90},b^{120},Q_{\rm TPK}).
\]

En ese mismo pasaje aparecen las dos listas completas de doce enteros y `Q=6263`. El texto las identifica como salidas del registro previo y excluye `U` y `K` de su dominio generador.

Las reglas coordenadas completas se encuentran inmediatamente después, en las líneas 298–326, para `Pi_H`. Son las sumas orbitales de `b120`, la determinación de tres sumas integrales mediante `Q`, y las combinaciones de `b90` que forman los bloques del registro firmado. El resto de `U016` desarrolla la transformación integral de Hadamard y las diferencias cíclicas. Este tramo puede exponerse de forma autónoma desde los 25 enteros indicados.

El cuadrado de naturalidad de `U016`, líneas 356–380, expresa que la prolongación no reescribe las coordenadas del registro ya fijado. Es una propiedad de compatibilidad del lector; no enumera los pesos o las operaciones coordenadas que producen sus 25 valores.

### Límite de la extracción localizada

No se ha recuperado en los pasajes anteriores la acción de `E108^{90,120}` sobre cada entrada pertinente del registro de eventos: las fórmulas que, aplicadas al registro y a sus datos de orientación, hojas, residuos, cocientes y transporte, produzcan cada componente de `b90`, cada componente de `b120` y `Q`. Las copias contrastadas de `c25` y del propietario `U016` coinciden en este inicio de la especificación explícita en `Pi_H`.

Las identidades posteriores `D3 K=b90`, `D4 K=b120` y `Q(K)=6263` verifican la compatibilidad del resultado reconstruido. Usarlas para definir los canales anteriores desde `K` invertiría el orden de la derivación que se pretende exponer.

La nota incremental sobre `eta` define explícitamente un censo de eventos por ventanas y su actualización en un marco móvil. Distingue esa evaluación del estado íntegro. Por ello no se identifica ese censo, sin una regla adicional, con los 25 enteros de `E108^{90,120}`.

**Dependencia exacta por recuperar para el apéndice solicitado:** una especificación de `E108^{90,120}` por coordenadas o por su acción en generadores del registro, junto con las reglas que producen el registro usado en esta evaluación. El mero tipo de la aplicación y la lista de sus valores no suministran esa especificación.

## 3. Consecuencia editorial acotada

Los dos tramos algebraicos posteriores están disponibles y preservados en `A/sections/generacion.tex` y `A/sections/registro_k.tex`. No se modificaron esas fuentes. La copia de otro apéndice con las mismas tablas e inversiones aumentaría la extensión sin resolver las dos dependencias precisas descritas.

La presente nota conserva los resultados recuperados y señala el punto material exacto donde comienza cada construcción reproducible. No reclasifica las constantes como entradas convencionales, no introduce valores objetivo y no infiere de este examen ningún resultado sobre la compatibilidad analítica completa de alfa.

No se ejecutaron nuevas campañas de cálculo, no se recompiló el artículo y no se modificó ningún PDF. Se aplicaron las instrucciones de continuidad documental, genealogía de constantes generadas y verificación de la conexión nonádica para separar productor, registro, reconstrucción y evaluación posterior. No se emite un certificado nuevo de clausura pública.
