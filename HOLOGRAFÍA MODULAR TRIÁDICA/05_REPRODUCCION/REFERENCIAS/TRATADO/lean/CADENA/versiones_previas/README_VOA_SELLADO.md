# Entrada vigente del paquete Lean del artículo I

Este README gobierna la ejecución de esta continuación. Los textos de inicio
heredados (`INICIO_AQUI.md`, `LEEME_PRIMERO.md` y las entregas previas) se
conservan íntegros como antecedentes; no sustituyen esta entrada.

## Un único recorrido

`APP → TRIT → TPK → estado enriquecido → publicaciones regionales → registro
seleccionado → incidencia y retículo → álgebra torcida → osciladores y campos`.
Los supuestos y dominios exactos de cada flecha son los de sus teoremas Lean.
Los valores de llegada no se añaden como entradas nuevas de esta continuación.
No reiniciar la inversión de K ni sus lectores: se reutilizan sus fuentes y
sus pruebas dentro de la misma clausura.

Ejecutar desde esta carpeta:

```sh
python3 -I -S reproducir_voa.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

Lean debe ser 4.21.0. El commit de Mathlib está declarado en `README_VOA.md`.
El ejecutor verifica las huellas, resuelve los imports, compila o reutiliza
objetos sólo si coinciden sus fuentes y dependencias y consulta los axiomas
de las declaraciones explícitas. No reconstruye Mathlib. El entorno de Lean
y la biblioteca Mathlib son dependencias externas, no archivos ocultos del
proyecto. El ZIP incluye las fuentes HMT de toda la clausura declarada.

La entrada matemática es `deltas/voa/SelectedHeisenbergInput.lean`; conserva
la composición acción/electrón/incidencia y agrega los campos construidos.
`RESULTADO_CONTINUACION_VOA.md` explica los resultados y su límite exacto.
`recibos/voa/LEAN_CONJUNTO.json` conserva la ejecución conjunta sellada;
las ejecuciones futuras escriben `resultados/lean_unificado/VERIFICATION.json`.

La localidad de los campos de Heisenberg está demostrada. Este paquete no
declara formalizados el sistema completo de campos exponenciales, el módulo
torcido, el orbifold de FLM ni su identificación con el Monstruo. La presencia
de la fuente LaTeX de esos resultados conserva su procedencia; no los convierte
automáticamente en teoremas Lean. No se ha añadido un axioma para suplirlos.
