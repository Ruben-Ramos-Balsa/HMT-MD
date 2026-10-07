# Una entrada: origen seleccionado, incidencia concreta y campos reticulares

Entrada Lean: `deltas/union/SelectedExceptionalChain.lean`.

La reproducción empieza por las fuentes conservadas APP–TRIT–TPK, el registro
seleccionado y sus lectores. No se recibe K como nuevo dato ni se repite su
inversión. Se conservan la generación regional, las dos lecturas de alfa y la
composición previa de acción y electrón con sus condiciones explícitas.

## Resultado de esta integración

La misma selección tiene ahora una carta concreta entre las 132 hexadas
generadas y el diseño residual binario, el paso hexada–octada y la incidencia
4+1. El espacio reticular ya construido recibe generación desde el vacío,
conmutadores de traslación, orden normal exacto a todos los grados y
cancelación polinómica de polos. La igualdad APP–Witt se demuestra para los
operadores de su carta racional, no por una coincidencia escalar de 54.

Se conservan además las pruebas recuperadas del retorno espinorial, el álgebra
de Weyl y la dualidad T en su realización hilbertiana, con el radio obtenido
del lector angular anterior. Son desarrollos posteriores: no seleccionan K.

El teorema `shared_action_electron_exceptional_chain` reúne la publicación
anterior con la incidencia concreta sin borrar sus parámetros ni hipótesis.
La composición no afirma que se haya formalizado el orbifold de FLM, su
identificación con el Monstruo o la totalidad del manuscrito. El carácter
reflejado reticular conservado no se renombra como J.

## Ejecutar

Con Python 3, Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`:

```sh
python3 -I -S reproducir_cadena.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

`--plan` comprueba primero la clausura de fuentes sin compilar. La ejecución
compila los módulos necesarios en orden de dependencias. Si existe una caché
verificada, sólo reutiliza objetos cuya fuente, compilador y dependencias
coinciden. Una copia sin caché recompila desde las mismas fuentes. Mathlib es
una dependencia externa fijada; no se reconstruye durante este comando.

Se rechazan `sorry`, `admit` y axiomas locales. El cálculo finito heredado usa
`native_decide`; la dependencia `Lean.ofReduceBool` se declara expresamente.
Las hipótesis de cada teorema siguen formando parte de su enunciado.

## Reutilización comprobada

La entrega precedente verificó conjuntamente 188 módulos y 534 consultas.
El revisor comprobó los 11 módulos de Golay–Steiner, espín y dualidad mediante
160 consultas, también después de extraer su ZIP. La unión conserva ambas
evidencias. Sus objetos se adoptan sólo tras cotejar fuentes, objetos,
dependencias, versión de Lean, registros de axiomas y huellas del compilador.
Esta adopción se registra como reutilización, no como tercera recompilación.

El control conjunto vuelve a leer todas las fuentes, comprueba cada informe
de axiomas y compila la nueva entrada. El recibo distingue qué se compiló y
qué se reutilizó. No se usa un recuento de archivos como prueba de cobertura.

Los archivos anteriores permanecen íntegros; el README anterior se conserva
en `versiones_previas`. No se ha modificado ningún PDF ni paquete sellado.
