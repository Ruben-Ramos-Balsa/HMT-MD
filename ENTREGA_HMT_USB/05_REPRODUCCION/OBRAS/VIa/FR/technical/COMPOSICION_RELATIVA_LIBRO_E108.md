# Cierre relativo de la evaluación incidencial

Fecha: 2026-09-10. Alcance: composición efectiva desde un libro declarado hasta las 25 coordenadas y el sello. **No es otra búsqueda nominal, ni una certificación de autonomía global.**

Se conserva el resultado de la consulta previa en `BUSQUEDA_FOCAL_PRODUCTOR_E108_20260910.md`. Esta nota desarrolla la parte matemática que allí quedaba recuperada: no modifica su conclusión de procedencia ni vuelve a inspeccionar todo el corpus.

## Dictamen operativo

**Sí hay un resultado relativo completo y demostrable:** para todo libro finito de visitas APP y trazas orientadas con los datos declarados, sus recuentos producen unívocamente 12 bloques; sus diferencias de pasos 3 y 4 y su suma producen las 25 coordenadas; el operador armónico y la inversa de Hadamard recuperan exactamente esos bloques. Las condiciones integrales de la imagen se deducen del mapa directo. No se escogen después para obtener K.

El pasaje completo está en `COMPOSICION_RELATIVA_LIBRO_E108.tex`, con seis etiquetas propias `vi:lib:*`, pruebas completas y ninguna remisión externa obligatoria. No se ha insertado automáticamente en `main.tex`, ni se ha editado la sección09 estable. El coordinador puede integrar su definición y prueba donde corresponda, evitando duplicar las pruebas que09 ya contiene.

**El alcance numérico canónico no se obtiene por ese cambio de formulación.** La identidad `E_cnt = E108` sobre un estado concreto requiere el libro seleccionado por el TPK para ese estado. Declarar un libro como argumento permite cerrar la evaluación relativa; no demuestra que el generador canónico lo haya seleccionado. Tampoco permite anunciar que el K numérico publicado se ha generado desde las semillas si sólo se han recibido sus diferencias o sus recuentos.

La fuente de II declara expresamente esta misma distinción en `registro_incidencias.tex:67`. Conservarla no altera la tesis de la fuente. Presentar una evaluación relativa como prueba de la selección numérica sí alteraría su alcance.

## 1. Datos de partida y salidas efectivamente calculadas

| Objeto | Papel en la composición recuperada | Qué calcula el código existente |
|---|---|---|
| Tabla APP y operaciones de hoja | Estructura de partida; suma, producto y convención de umbral | Calcula `n`, raíz positiva `r` y cociente `q9` desde posición y hoja. No recibe el residuo como entrada independiente. |
| TRIT en cada visita | Etiqueta del estado de la ruta, producida por la dinámica cuando su procedencia está acreditada | Comprueba pertenencia a `{-1,0,1}` y calcula el signo de la suma sobre cada traza. No comprueba por sí mismo la evolución TPK de la etiqueta ni su compatibilidad con la hoja. |
| Origen de fase y ventanas de 9 instantes | Carta temporal fija, 12 ventanas sobre 108 instantes | Agrupa visitas por instante; conserva el origen de cada traza. |
| Familia de rutas e historial | Dato incidencial suministrado; la selección dinámica pertenece al tramo anterior | Comprueba identificadores, coordenadas APP y cobertura de 108 instantes por ruta. No ejecuta un selector canónico de familias. |
| Multiplicidades y clase de frontera del representante 9 | Datos del libro que deben proceder del transporte y del operador de frontera | Los valida y usa en los recuentos; no los infiere del valor de K ni los genera desde la semilla. |
| Familia de trazas y unidad de longitud reducida | Datos del lector incidencial; deben venir con regla de enumeración y cobertura | Comprueba consecutividad, ruta única, canal no nulo y longitud `120(1+3j)`. El campo de procedencia de cobertura no equivale a una prueba ejecutada de exhaustividad. |
| A,C,V | Salidas enteras de las incidencias declaradas | Sumas finitas con orientación y multiplicidad. |
| 36 residuos y 36 cocientes de división por 10 | Salidas de A,C,V | División euclídea, válida también para recuentos negativos. |
| 12 bloques z y 25 coordenadas D3z,D4z,Q | Salidas del lector | Composición directa, sin K, U, alfa ni coordenadas objetivo. |
| U yK | Publicaciones posteriores de ese mismo libro | ΠH seguido de H12/4; se demuestra K=z. |

Los datos del libro no se proponen como nuevas constantes físicas ni como parámetros ajustables. El teorema fija el dominio donde su evaluación tiene sentido. La afirmación de que esos datos ya están seleccionados por un protocolo concreto exige conservar ese protocolo con la afirmación; no se acredita por el formato JSON.

## 2. Prueba reunida y consecuencias exactas

La composición escrita y probada es:

`L → (A,C,V) → z → (D3z,D4z,Q) → ΠH → U → H12 U/4 = z`.

Para `b=D3z,c=D4z,q=Q(z)`, se define `w_i=c_i−b_(i+1)=z_i−z_(i+1)`. Se deducen:

- `sum(w)=0`;
- `b_i=w_i+w_(i+1)+w_(i+2)`;
- `q+sum_i sum_(j<i) w_j=12z_0`.

La fórmula inversa reconstruye z sin ambigüedad. Las sumas por órbitas y diferencias producen ΠH y se prueba por sustitución que coincide con H12z. La identidad H12²=4I da la última inversión. El mapa lineal D:Z12→Z25 tiene rango 12; las 25 coordenadas no son 25 datos libres.

Para dos matrices de recuentos, la igualdad de las salidas equivale exactamente a la igualdad de sus 36 residuos módulo 10. Esto describe **fibras de una aplicación de conjuntos**. La codificación decimal con representantes no es un homomorfismo aditivo a Z25; llamar a esa afirmación un «núcleo lineal» sin especificar la estructura sería impreciso.

La identidad no recupera toda la historia: diferentes libros pueden tener los mismos recuentos módulo 10. Se preservan explícitamente en el libro los cocientes, rutas, hojas, orientación, frontera y multiplicidades. No se presenta la reversibilidad del sello como reversibilidad automática de todo el estado enriquecido.

## 3. Composición con la dinámica y límite exacto

La notación de enlace usada en el pasaje es `B(R12(x))`, donde B designa **la regla efectiva que selecciona y enumera el libro**, no un operador nuevo dado por la mera introducción de una letra. Si B se explicita, el resultado probado se aplica directamente a ese libro y se obtiene la evaluación del estado. La notación permite localizar el tramo; no lo suplanta.

El calendario y las reglas locales de suma/producto bastan para calcular cada visita una vez producida. No bastan por sí solos para determinar cuántas rutas cuenta el lector, sus multiplicidades, qué incidencias de 9 clasifica como corona o interior y qué trazas orientadas de longitud reducida 120 enumera. La selección de estos datos no se infiere de que la salida publicada satisfaga las congruencias transversales.

Tampoco se identifica el vector elemental de doce eventos de una ruta con el registro de bloques. El control anterior `|e_m|≤9`, diferencias≤18 y suma≤108 sigue delimitando ese tipo distinto; no limita el libro enriquecido, que puede reunir multiplicidades y familias.

**Conclusión para el cierre editorial:** este pasaje puede cerrar la proposición de evaluación incidencial con estructura de partida explícita. No autoriza por sí solo marcar verdadero `canonical_E108_produced` ni `autonomia_global`. La producción del libro canónico es una dependencia de la afirmación numérica concreta, no de la prueba algebraica general que acaba de quedar reunida.

## 4. Fuentes completas releídas en este corte

Raíz de II:

`/Users/ruben/Documents/New project/output/ARTICULO_II_AUTONOMIA_20260910_REVISION_09_NUCLEO_COMUN/`.

- `manuscrito/sections/registro_incidencias.tex` (156 líneas): dominio y recuentos 13–42, composición 44–70, información necesaria 72–97, conjugación y memoria 99–156. SHA256: `b20bd06c5807a55d7f850c8ae863af89e9260b9adc885b9043434ecfc8e13bad`.
- `suplementos/registro_incidencial/paquete_I/constructor_incidencial.py` (297 líneas): recuentos→canales 56–81; libro 92–196; inversión posterior 199–209; controles 212–279. SHA256: `fa26779735017d1737f5a8ff89afe0906be30686961f35aba92f7b028de8a502`.

También se releyó íntegra la nota focal de E108 y el tramo estable de 09 que contiene recuentos, imagen integral, ΠH, Hadamard y normalización de alfa. Las fuentes primarias del integral ya leídas y sus localizadores permanecen en la nota focal; este trabajo no los confunde con una nueva lectura integral.

## 5. Control material de este pasaje

Se ejecutó el `self_test()` del constructor conservado: `PASS_TESTS_COMPILATEUR_INCIDENCIEL`. Además se comprobaron con enteros 97 matrices de recuentos firmados distintas: condiciones de imagen, fórmula inversa, integralidad de ΠH e identidad de Hadamard. Las pruebas generales son las escritas en LaTeX; estos controles finitos protegen sus fórmulas, no sustituyen la demostración ni producen el libro canónico.

La fuente nueva tiene seis etiquetas distintas, tres remisiones internas resueltas y entornos correctamente anidados. No se compiló un PDF. Su huella al terminar este control es `0eb05dfd2ccaf487a7e644cee61bc97d56600be8ee289189aa882e9d0c905f98`.

No se editaron main, 09, gate editorial, manifiestos ni artículos anteriores. La nota `PENDIENTES_LEY9_I_III_IV_DESPUES_VI_20260910.md` conserva separadamente las propuestas recibidas para después de VI.
