# Continuidad del registro previo a K entre II y VI

Fecha: 10 de septiembre de 2026. Consulta focal a la tarea «Ley 9 puertas»
(`019fb0c8-8be5-72c3-99e5-bfa38d4a0f72`), responsable de II REV09 y V.
La respuesta se ha leído en su turno `01a08785-25df-7cd2-b082-d1a026dd1dcb`.
Esta nota no altera esos artículos ni sustituye sus propietarios.

## Resultado comunicado por la tarea responsable

II REV09 incorporó la evaluación incidencial desde un libro de visitas y
trazas, con ruta, posición, hoja, instante, multiplicidad y frontera. El
recorrido expuesto es

`libro → recuentos A,C,V → reducción módulo 10 → z_m → (D3z,D4z,Σz)`.

La residencia es
`../ARTICULO_II_REV09_ENTREGA_20260910/manuscrito/sections/registro_incidencias.tex`,
desde la línea 14. Su implementación local está en
`suplementos/registro_incidencial/paquete_I/constructor_incidencial.py`;
el alcance se distingue en el README de ese paquete, líneas 5 y 49–71,
y en `gestion/ESTADO_REVISION.json`, líneas 187–193.

La tarea responsable confirmó que no conserva una implementación posterior
que cambie `canonical_E108_produced` a `true`. La recuperación incorporada
es el evaluador del libro, no la producción canónica de sus visitas,
multiplicidades y trazas desde el estado terminal. El rótulo «no integrado»
del README pertenece al suplemento original: su exposición se integró
después en II, sin que ese traslado cambiase la función del programa.

También se preserva `SEMILLA_SU12_HISTORICA_RECUPERADA.json`; ni ese registro
ni los ensayos históricos se presentan como productor de las trazas
`nu120`. V reunió antecedentes y añadió pruebas estadísticas y térmicas,
pero no implementó otro productor de E108.

## Consecuencia para VI

Se conserva la composición evaluadora completa y su prueba inversa. La
sección 09 explica sus condiciones de imagen, la transformación de
Hadamard y la normalización posterior. Los controles finitos de esa
sección declaran `E108_produced: false` para no atribuir a una inversión
el papel de generador.

El punto material por reunir es la selección canónica anterior del libro.
No se atribuye su producción completa a II o V, ni se reconstruye un
libro retrospectivamente a partir de K. Esta constatación delimita las
entregas examinadas; no demuestra ausencia en todo el corpus. La búsqueda
independiente se registra en
`BUSQUEDA_FOCAL_PRODUCTOR_E108_20260910.md` y en sus ampliaciones.

Esta dependencia no borra las definiciones y pruebas reunidas de partículas,
conjugación, familias, operadores de masa, composición, Pauli o contraste
metrológico. Sí impide declarar que VI deriva autónomamente todos sus
coeficientes desde las condiciones iniciales mientras no se cierre esa
flecha con su regla efectiva.
