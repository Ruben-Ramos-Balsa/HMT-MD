# Correcciones conservadas para después del Artículo VI

Recibido el 10 de septiembre de 2026 por el coordinador de la tarea, como extracto operativo del mensaje de «Ley 9 puertas». No es una transcripción íntegra: el mensaje completo permanece en la conversación de raíz. **Estado: preservado, pendiente; no implementado por esta nota.** El objetivo actual sigue siendo VI. Otro editor atiende II y V. Rubén reserva el radión: no iniciar un artículo específico.

## Artículo I

- «Actualizar resumen y conclusiones. Todavía describen principalmente la composición escalar del electrón. Añadiría una frase que anuncie la representación de espín 1/2, su descomposición direccional y el retorno espinorial».
- «Precisar una denominación en p. 114: donde dice proyector regional P3, pondría proyector isótipo tridimensional».

## Artículo III

- Diferenciar `P3 ico` de `P3 cíc`.
- «Precisar qué velocidad transmite III a V. III escribe c_vac=ĉu_C; V utiliza c=c_int en la dispersión radiativa. Hay que declarar la identificación y su normalización, o explicar que son lecturas diferentes».

## Artículo IV

- «Especializar el radio utilizando el desarrollo ya existente en II. Actualmente R0>0 funciona como parámetro. II contiene R0=((A−C*)/(A+C*))^(1/4). Incorporaría su construcción con los antecedentes necesarios de acción, par angular y elipse».
- Consolidar pantallas/dualidad de las pp. 97–99 y 104–110.
- Depurar el duplicado del integral y añadir números de teoremas externos de Moonshine.
- Conservar el alcance del teorema 11.4: transporte de la identidad de supercarga bajo sus condiciones.

## Regla de continuidad de este registro

Esta nota conserva propuestas recibidas, no certifica que las discrepancias ya estén corregidas ni que se haya revisado nuevamente cada artículo. Cada integración posterior exige consultar el corte vigente del artículo y sus dependencias. No se han editado I, II, III, IV, V, sus fuentes, punteros o gates.

## Actualización recibida: enlace de velocidad III–V

Recibida posteriormente el 10 de septiembre de 2026. **Estado: enlace recuperado por Ley9 y conservado aquí para incorporación posterior; no implementado por este registro.** Esta actualización precisa el punto de velocidad de III indicado arriba, sin borrar la observación histórica.

Según la comunicación del coordinador, Ley9 recuperó las identidades

\[
 c_{\mathrm{int}}=\exp(-E)u_C,\qquad
 E=\log(r_+r_-),\qquad
 c_{\mathrm{vac}}=(r_+r_-)^{-1}u_C.
\]

Las dos velocidades son la misma sección en la misma carta. El propietario señalado es `10b_funtor_dimensional.tex`, en las etiquetas `eq:cZ-internos` y `eq:longitud-ruta`. Para `t_0=u_T`, la longitud correspondiente es

\[
 \ell_0=\widehat c\,u_L,
\]

no `u_L` sin ese factor. El cambio de carta comunicado es

\[
 u_C'=d\,u_C,\qquad \widehat c'=\widehat c/d,\qquad
 u_T'=\eta u_T,\qquad \tau_0'=\tau_0/\eta,\qquad
 u_L'=d\eta u_L.
\]

Conserva `ℓ0`; la carta adaptada utiliza `d=ĉ`. Deben trasladarse juntas la identificación de la velocidad y esta normalización de longitud, conservando las variables y unidades declaradas en el propietario.

El fragmento, su prueba y el control de 271 casos —en ejecución normal y con `-O`, según el mensaje recibido— se encuentran en:

`/Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/colaboracion_velocidad_III_V_20260910/`.

Está disponible para III el archivo `69_enlace_constitutivo_velocidad.tex`. Este registro conserva la localización y el resultado comunicado; no declara haber releído el fragmento ni repetido esos controles.

El coordinador informa además: VI principal compilado con 117 páginas y catálogo de 570; II REV10 compilado con 206 páginas, bajo revisión de otro editor para II/V. Son estados recibidos, no nuevas verificaciones efectuadas por esta nota. Se mantiene la prioridad de cerrar la revisión visual y entrega de VI: no se modifica su manuscrito, ni se abre una nueva tarea.
