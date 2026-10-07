# Selección orbital terminal y composición con alfa

Esta ampliación formaliza el selector finito publicado: se enumeran todas las
ordenaciones de ocho palabras ternarias, se intersecan sus cilindros con el
panel funcional y se selecciona el registro mediante incidencia temporal de
dos lectores y la cara excepcional. El valor de K no entra en el algoritmo
de selección: aparece en la conclusión que Lean comprueba.

## Resultado comprobado

- 40.320 ordenaciones; 21.902 incidencias de cilindros.
- 19.446 candidatos distintos y 79 candidatos en la cara excepcional.
- La cara se calcula a partir de los dos lectores regionales y la matriz de
  Witt, y resulta ser {4,6,9,10}; no se obtiene de K.
- Un único superviviente: (234,543,140,729,659,824,621,058,914,794,146,601).
- Su registro se compone con las pruebas existentes: recuperación exacta y
  raíz analítica única correlacionada con las publicaciones dodecafásicas de
  alfa, para cualquier profundidad de publicación.

No se crea una población ficticia de visitas ni se obtiene una historia
terminal invirtiendo las cifras deseadas de K.

## Entradas y alcance

El selector finito admite W24, el repertorio no ordenado S8, las nueve
posiciones del panel funcional y las cien filas del calendario N69. No
recibe como hipótesis la igualdad del resultado con K.

La composición `SelectedFromRegionalInputs.lean` elimina el panel y N69
como entradas independientes: ambos se evalúan desde las publicaciones
regionales de 600 trits por canal y se demuestra su correspondencia con
las tablas que usaba el cálculo finito. Las tablas sirven de certificados
de igualdad; no son consultadas por sus productores regionales.

W24 también se calcula mediante el descriptor regional orientado: primera
pausa del reloj, retorno de nueve fases y los operadores de defecto y lectura
de fase de la fuente. **S8 sigue siendo la interfaz explícita no regenerada
en esta ampliación.** Tampoco se sustituye el estado pleno por la fase del
reloj ni por el registro reducido de 108 eventos.

## Archivos

1. `TerminalReaders.lean`: lectores comparativo y afín, atlas temporal,
   residuo orientado y condición de cambio de tipo en las aristas 4→8→12.
2. `TerminalInputs.lean`: transcripción íntegra de las entradas necesarias.
3. `TerminalOrbitalSelection.lean`: enumeración, filtración y unicidad.
4. `SelectedTerminalAlpha.lean`: composición con la biblioteca de alfa ya
   existente, sin repetir sus demostraciones.
5. `RegionalPanelBridge.lean`: producción de las nueve posiciones del
   panel desde las publicaciones regionales.
6. `SelectedFromRegionalInputs.lean`: composición de panel y N69 generados
   con el selector, la raíz única y las publicaciones de alfa.

`regional/` conserva copias íntegras de los cuatro módulos coordinados que
producen los 600 trits, sus firmas, las cien filas y W24. Sus demostraciones se
reutilizan; no se vuelve a escribir una segunda construcción regional.

El atlas se cotejó independientemente con el Python original: 14.849 pares
palabra–residuo, cero diferencias; las cien filas coinciden exactamente.
Los tiempos son distintos (0–99), por lo que unir por fila y unir por tiempo
son aquí la misma operación. `CheckReaders.lean` permite exportar ese cotejo.

## Reproducción y confianza

Lean 4.21.0, con la misma revisión de Mathlib que utiliza la entrega del
artículo I. `verify.py --help` describe la compilación desde fuentes y la
reutilización de dependencias sin reconstruir Mathlib.

La evaluación finita usa `native_decide`; por tanto, además del núcleo de
Lean, interviene su evaluación nativa y aparece `Lean.ofReduceBool` en el
informe de axiomas. No se presenta como una comprobación exclusivamente por
reducción del núcleo. La composición analítica reutiliza también los axiomas
lógicos de la biblioteca (`propext`, `Quot.sound`, `Classical.choice`). No hay
`sorry`, `sorryAx` ni axiomas matemáticos locales añadidos.

`VERIFICATION_INCREMENTAL.json` registra la compilación incremental realizada
y el cotejo independiente; `REGIONAL_COMPOSITION_VERIFICATION.json` registra
la composición con los antecedentes regionales. No se confunden con una
compilación limpia de toda la biblioteca. `verify.py` permite esta comprobación de dependencias
locales cuando se requiere. Este directorio es una ampliación de la entrega
del artículo I, no un sustituto del paquete autónomo completo.

## Propietarios

Directorio fuente: `16_CIERRE_GLOBAL_HMT_MD_2026-07-22/15_SELECTOR_GLOBAL_DOBLE_LECTURA`.

- `verificar_selector_orbital_etiquetado.py`.
- `verificar_cierre_afin_monodromico_terminal.py`.
- `TEOREMA_CIERRE_AFIN_MONODROMICO_TERMINAL.md`.
- `DICTAMEN_PROCEDENCIA_SUPERVIVENCIA_S8.md`.

Los PDF, LaTeX y datos originales no se han modificado.
