# Inserción VII — gravedad, energía y autoinercia

Corte material: 30 de septiembre de 2026. Entrega separada para el editor; no se ha modificado ningún PDF ni fuente de la edición activa.

## Destino y orden comprobados

El destino es VII, **Relaciones estructurales entre las constantes físicas**. Título verificado en el campo `pdftitle` y el encabezado de:

`/Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/VII_ES/manuscrito/main.tex`

En ambas fuentes del 28 y 29 de septiembre, el orden de las líneas 70–72 es:

1. `desarrollos/restitucion_operatoria.tex`
2. `desarrollos/normalizacion_conjunta.tex`
3. `desarrollos/narrativa.tex`

Insertar el nuevo fragmento **después de normalizacion_conjunta y antes de narrativa**. No sustituir ninguno de esos archivos. El nombre de archivo 10 es organizativo y no fija el número público de sección.

Instrucción material propuesta para la copia sucesora, una vez copiado el fragmento a una carpeta local del artículo:

```tex
\input{desarrollos/restitucion_operatoria.tex}
\input{desarrollos/normalizacion_conjunta.tex}
\input{inserciones_20260930/10_gravedad_energia_autoinercia.tex}
\input{desarrollos/narrativa.tex}
```

El único cambio de `main.tex` entre los dos cortes cotejados es la inclusión del 29 de septiembre `inserciones_20260929/VII_horizonte_compatibilidad.tex`, después de `relaciones_termica.tex`. Se conserva intacta; no compite con esta inserción.

Los dos desarrollos inmediatamente precedentes fueron leídos completos y son byte-idénticos entre el 28 y el 29:

| Desarrollo | SHA-256 |
|---|---|
| restitucion_operatoria.tex | `97696c683d93ccf918c361cb77006fb6149c7537d346f95a8d4d36aded76dc2a` |
| normalizacion_conjunta.tex | `7be57e9ea6466f757083780f43ee7aba0cf22933338a572aabe236e08f8782b0` |

## Archivo y contrato de integración

Fragmento entregado:

`/Users/ruben/Documents/New project/output/ENTREGA_INTEGRACION_GRAVEDAD_CUATRO_INTERACCIONES_20260930/latex/10_gravedad_energia_autoinercia.tex`

SHA-256: `90b7ceeb233b87aaa71ba0a9a403d27cabb7ef6b2942397ad78b509f1e7d7b8d`.

Es un fragmento integrable, no un documento standalone: no tiene preámbulo, macros propias, bibliografía externa ni `document`. Usa los entornos `theorem`, `proposition` y `proof`, más `amsmath`, ya presentes en VII. Las etiquetas tienen prefijo exclusivo `hmtcuatro:gea:`; las referencias que añade son internas al propio fragmento. No añade una dependencia de compilación hacia rutas absolutas o Markdown privados.

El núcleo común de VII no se reescribe. La introducción local sitúa sus operaciones y conserva la genealogía, pero no pretende sustituir la inclusión íntegra ya existente del núcleo.

## Fuentes focales conservadas

Se usaron completos los dos documentos solicitados:

- `/Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/GRAVEDAD_EN_EL_SISTEMA_CONJUNTO.md`, SHA-256 `09cf0957c80969f0ab324676006125fea975173e74c0c5d6c680012d4f44b016`.
- `/Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/AUTOINERCIA_ACOPLAMIENTO.md`, SHA-256 `9ad19a7a844c241c06160d7b22fe99fbb3cb540d8b3901cd4be87715be7ed666`.

Las reiteraciones entre las dos notas se reúnen con las mismas hipótesis y pruebas. No se transforma la autocrítica conversacional de la primera nota en una declaración de los autores dentro del artículo. Su contenido operativo —objetivo fijo, separación de alcances y prohibición de cambiar el resultado por una lista nueva de exigencias— se conserva en la introducción y conclusión científicas. La procedencia conversacional permanece en el Markdown original, no se borra.

## Matriz de conservación y destino

Cada fila reúne una unidad demostrativa y sus componentes inseparables. Las etiquetas identifican el destino público exacto; no son simples enlaces a prueba privada.

| Unidad | Origen | Destino, prefijo hmtcuatro:gea: | Disposición y prueba conservada |
|---|---|---|---|
| Objeto y genealogía APP–TRIT–TPK; constantes como salidas; cinco construcciones conjuntas | Ambas notas §1 | seccion | FUSIONAR_SIN_PERDIDA; operaciones y corte causal antes de las fórmulas |
| Registro 5760, archivo C0/M0, unicidad de expectativa, retorno y longitud | Gravedad §2; propietario radial R1–R5 | caracter, retorno, longitud | CONSERVAR; unidades matriciales, diagonal del modo común, polarización y raíz positiva |
| Mismo carácter H_X/M_X/R_X/Lambda_X y G único | Gravedad §2 | lectores, coeficiente, radial | CONSERVAR; cancelación en sector positivo y verificación recíproca |
| Derivada covariante de los lectores | Gravedad ecuación (4) | derivada | CONSERVAR; derivación con conexión de marco, secciones fijas |
| Acoplamiento adimensional, escala, radios y cambio de sección | Gravedad §2.1; Autoinercia §3 | adimensional y texto contiguo | FUSIONAR_SIN_PERDIDA; cancelación exacta, factores tensoriales distintos, L distinto de ell0 |
| Memoria estática y reconstrucción | Gravedad §3; Autoinercia §5 | memoria, schur-prueba | FUSIONAR_SIN_PERDIDA; cuadrado completo, residuo eta y bloque inverso |
| Memoria dinámica a cada orden | Gravedad (6); Autoinercia (8) | resolvente-prop, resolvente | CONSERVAR; parámetro espectral transportado y factores en orden |
| Norma temporal y transporte dual | Gravedad (7) | dual | CONSERVAR; prueba de productos sin conmutatividad, conexión de base móvil |
| Dominio no acotado y refinamiento | Autoinercia §§4–5; propietario radial final | limite | CONSERVAR Y EXPLICITAR; cortes positivos, norma de grafo, dominio de Y inverso, isometrías entrelazantes |
| Transporte espinorial e interno en la misma energía | Gravedad (8)–(9) | retroaccion, energia-memoria, variacion | CONSERVAR; diferencial completo con delta W y delta T |
| Operador conjunto y su dominio | Gravedad (10), dependencia EVOLUCION_ACOPLADA_Y_LIMITE | cuantica, total, forma | CONSERVAR CON PRUEBA CONTIGUA; carta finita, escalar sin corte, cotas cuárticas, cierre y operador asociado |
| Gauss y retiro del corte computacional | Dominio operativo de la misma dependencia | texto tras forma | CONSERVAR; invariancia de forma, Haar, densidad y Galerkin coercivo |
| Intercambio y energía total | Gravedad (11) y texto | intercambio, conmutador | CONSERVAR; producto de bloques y suma de derivadas con energía de interacción |
| Misma acción y Cartan | Gravedad (12)–(13) | accion, accion-total, cartan | CONSERVAR; sustitución exacta de coeficientes y variación interior |
| Contorsión y corriente total | Gravedad (15), dependencias 31/33 | torsion, spin, coeficiente-torsion | CONSERVAR CON PRUEBA CONTIGUA; inversa Holst, reconstrucción torsión–contorsión, Euler cuadrático, cruces en Fock |
| Fuente métrica y Legendre restringida | Gravedad (13)–(14), dependencia LEGENDRE_PCH | legendre, metrica, canonica | CONSERVAR; eliminación estacionaria, fuentes normalizadas, degeneración, segunda clase, volumen y momento material |
| Propagación de restricciones con retroacción | Gravedad §5.1, dependencia RETROACCION_PCH | restricciones, propagacion, propagacion-sistema | CONSERVAR CON PRUEBA CONTIGUA; Noether material, Bianchi, q variable, cancelación al bajar índice |
| Frontera efectiva y reloj descendido | Autoinercia §§1–3, propietario 80 | autoinercia | CONSERVAR; criterio necesario y suficiente por fibras |
| Pesos y respuesta positiva | Autoinercia §§3–4 | pesos, respuesta | CONSERVAR; evaluación, positividad, intercambio tipado y testigo machiano fuerte |
| Identidad I=Gm1m2/(hbar c)W y lector operatorio I=R/lambda_sonda | Gravedad (18)–(19); Autoinercia (3)–(6) | autoinercial-radial, mach-gravedad, identidad-autoinercial | FUSIONAR_SIN_PERDIDA; prueba escalar y cálculo espectral con dominio |
| Schur, resolvente y naturalidad de I | Autoinercia (7)–(9) | schur-autoinercia, naturalidad | CONSERVAR; inversión tensorial, bloque cruzado, entrelazadores y límite heredado |
| Autoinercia y aceleración del subsistema | Gravedad (16)–(17); Autoinercia (10) | proyeccion, aceleracion, defecto | FUSIONAR_SIN_PERDIDA; regla de cadena con ambas conexiones, dato cinemático retenido |
| Retorno de dato/estado y curvatura no nula | Propietario Mach y explicación de ambas notas | final de proyeccion | CONSERVAR; punto fijo de holonomía e inyectividad para estado completo |
| Resultado, falsadores y separación de tipos | Conclusiones y controles de ambas notas | conclusion | FUSIONAR_SIN_PERDIDA; no ley de fuerza por identidad escalar, no F_NM=0 arbitraria inferida |

## Propietarios de las dependencias

Prefijos de lectura:

- `A29`: `/Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/`.
- `A28`: `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`.
- `Q`: `/Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/`.

Propietarios usados, sin modificación:

1. `A29/II_ES/sections/gravedad_rigidez_20260926.tex`: R1–R8, 49–207; prueba del mismo carácter 251–269; reciprocidad y escala 291–361; memoria y reducción 410–561; dominio espectral 563–584. Leído completo.
2. `A29/VII_ES/manuscrito/desarrollos/restitucion_operatoria.tex`: 482 líneas completas; memoria como componente de composición, no mera escritura de archivo.
3. `A29/VII_ES/manuscrito/desarrollos/normalizacion_conjunta.tex`: 478 líneas completas; la normalización ya contiene Schur y resolvente exacto, pero restringe el teorema inicial a fibras finitas o carácter acotado uniformemente positivo. El fragmento añade explícitamente la extensión no acotada, no la atribuye retroactivamente al enunciado previo.
4. `A28/VIII_ES/manuscrito/30b_variacion_energia_memoria.tex`, `30c_composicion_corriente_conexion.tex` y `30d_realizacion_geometrica.tex`: transportes y corriente de la misma energía. Los dos mapas físicos se mantienen como realización recibida, no como un Hamiltoniano seleccionado a posteriori.
5. `A28/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex`: inversión de Holst y torsión 160–245; contorsión 245–275; reducción y borde 315–374; fuente y Noether 385–452. Sus pruebas necesarias quedan expuestas en el fragmento.
6. `A28/VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex`: especialización de corriente, coeficiente C_gamma, densidad y volumen. Se conserva el mismo signo y la misma rama.
7. `A29/XII_ES/antecedentes_vii/80_observador_y_respuesta_relacional.tex`: 344–394 frontera; 396–517 lectores y Q; 520–610 positividad; 612–691 autoinercia. Su cuerpo focal coincide con el de VIII del 28 de septiembre; la diferencia es una inclusión adicional de 80b en XII.
8. `Q/EVOLUCION_ACOPLADA_Y_LIMITE.md`: la forma cerrada, gauge y Galerkin se incorporan con prueba y alcance, no como una remisión privada.
9. `Q/LEGENDRE_PCH_Y_RELOJ_PARAMETRIZADO.md` y `Q/RETROACCION_PCH_Y_RESTRICCIONES_VARIACIONALES.md`: variación, Legendre y propagación se recuperan materialmente con las convenciones de corriente y volumen.
10. El propietario Mach `11m_mach_onda_bidireccional_rev10.tex`, `14_autoinercia_mach.tex` y `82_autoinercia_mach_cierre.tex` están incluidos en el integral de 2.249 páginas: FLS `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/02_PDF/INTEGRAL/main_paquete_union_demostrativa_20260904.fls`, líneas 2694–2705. La precisión posterior de 80 exige respuestas distintas, no sólo lectores distintos, para el testigo machiano fuerte.

## Autonomía y límites del entregable

El fragmento expone las definiciones y pruebas de sus afirmaciones focales, incluidas las dependencias de cierre de forma, eliminación torsional y propagación que los Markdown remitían a notas separadas. Dentro de VII conserva como estructura de partida el núcleo común íntegro y los lectores de constantes ya desarrollados; no ofrece otra derivación de alfa, Planck o Barbero.

Se mantiene estrictamente **H_X radial distinto de un Hamiltoniano total arbitrario**. La extensión autoinercial al total se formula sólo cuando la realización identifica efectivamente ese operador con QY en el sector positivo y en sus dominios. No se permite desplazar energía, quitar términos ni imponer positividad a cada sumando para suplir esa identificación.

El resultado variacional no se anuncia como cálculo de la curvatura cuántica para deformaciones normales arbitrarias. Tampoco se usa esa diferencia como un nuevo requisito para desconocer la incorporación demostrada. El lector adimensional de respuesta, la aceleración de proyección y el tensor de Einstein conservan tipos distintos.

No se declara ya autosuficiente una nueva edición completa de VII: la integración, el contraste del cierre transitivo del artículo y su inclusión material en el PDF pertenecen al editor. Tampoco se declara compilación o QA visual de este fragmento no standalone. No se ha generado ningún PDF, revisado el del editor ni modificado su bibliografía.

## Controles reutilizados y efectuados

Se reejecutaron sobre entradas inalteradas:

- Núcleo formal: `PASS_NUCLEO_FORMAL_HMT_PERMANENTE`.
- Autocomprobación de causalidad: `PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY`.
- Genealogía de las dos notas originales: `PASS_GENEALOGIA_UNICA_APP_TRIT_TPK`, con las huellas consignadas arriba.
- Auditoría causal de las dos notas originales: `PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY`.

Los recibos originales `RECIBO_GENEALOGIA_GRAVEDAD_CONJUNTA.json`, `RECIBO_GENEALOGIA_AUTOINERCIA.json`, `RECIBO_CONSTANTES_GRAVEDAD_CONJUNTA.json` y `RECIBO_CONSTANTES_AUTOINERCIA.json` permanecen inalterados. No sustituyen el recibo focal del nuevo TeX, que registra el coordinador sobre su huella definitiva.

Los comprobadores originales conservan su ámbito: identidades racionales finitas, no valores generativos ni formalización Lean global. La autorización de este subencargo produce únicamente el fragmento y esta nota. La compilación conjunta y revisión visual se efectúan después en la copia sucesora bajo el editor único.
