# Conciliación documental focal — 21 de septiembre de 2026

La discrepancia del certificado de arranque corresponde exactamente a una actualización editorial autoral de `AGENTS.md`: la lista de referencias pasa a reproducirse a petición expresa. No altera ninguna definición, fuente Lean ni construcción matemática.

El resultado histórico se conserva literalmente: `FAIL_ARRANQUE_HMT: hash divergente: AGENTS.md` (código 1, observado por la tarea principal). Este recibo no lo convierte en un PASS global y no se ha vuelto a ejecutar la puerta de arranque para emitirlo.

## Comparación exacta, no aplicada

- SHA esperado por `CERTIFICADO_ARRANQUE_HMT.json`, `operating_contract`, líneas 230–232: `40d16e6e94b5699910e82ffc46f580133fdba2ea53d903e45d541a1a690aacf3`.
- SHA actual de `AGENTS.md`: `cd897d28c593e5f46a37706c48e8ef973d795787c1aaa976f7e97d23ad1342bf`.
- Se eliminaron **sólo en memoria** las líneas actuales 3–15 (13 líneas) y se sustituyó el rótulo actual de la línea 16, «Antecedente conservado: accesos en cada respuesta — 11 de septiembre de 2026», por el rótulo histórico «Accesos obligatorios en cada respuesta — mandato del 11 de septiembre de 2026».
- Con todos los demás bytes idénticos, el resultado reproduce exactamente el SHA esperado. No se ha escrito esa transformación ni modificado el contrato vigente.

Las 13 líneas añadidas, conservadas literalmente en el JSON contiguo, contienen el mandato del 21 de septiembre: referencias únicamente a petición, selección vigente por idioma, comprobación conjunta de PDF/fuentes/paquete/revisión y distinción entre incorporación documental e incorporación matemática. Lo corroboran `PUBLICACION_HMT/SERIE_ARTICULOS_HMT/CRITERIO_EDITORIAL.md:3–9`, `ENLACES_RESPUESTAS.md:1–3` y `output/ACTUALIZACION_CATALOGO_REUNITIVO_20260921/ACTUALIZACION.json`. Sus huellas están registradas en el JSON.

## Continuidad del corte formal 371

Se comprobó la huella `f3fc574feea5f73d2e7234e7386d651af5e81075a368044361b1b65e3634a095` del recibo `orbifold_input/orbifold_closed_results/VERIFICATION.json`. Coinciden sus 17 fuentes nuevas con sus snapshots y sus objetos compilados, los 17 códigos de salida son cero, y coinciden las ocho huellas de recibos antecedentes. El recibo registra 154 declaraciones públicas y 126 teoremas en este incremento sobre 354 módulos anteriores.

No se recompiló Lean, no se reconstruyó Mathlib, no se reauditaron los PDF ni se reseñó o reselló ningún antecedente. La comprobación focal no extiende el alcance matemático del recibo ni atribuye una formalización íntegra de FLM al corte conservado.

La excepción aprobada por la tarea principal se limita al contrato editorial histórico: se conserva su FAIL, se documenta su causa exacta y se reutilizan los testigos formales inalterados. Los archivos originales, certificados y verificadores quedan intactos.
