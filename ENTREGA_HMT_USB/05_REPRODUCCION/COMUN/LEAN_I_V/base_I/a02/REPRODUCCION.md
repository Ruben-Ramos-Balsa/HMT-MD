# Reproducción de campos y descendientes

Esta carpeta y el ZIP contienen los mismos archivos. Descomprima una sola vez
si recibe el ZIP. Conectar un USB no ejecuta nada. Desde esta carpeta:

```sh
python3 -I -S reproducir.py --plan --report-dir plan_nuevo
python3 -I -S reproducir.py --report-dir resultados_nuevos
```

El plan sólo autentica; no compila. La segunda orden reutiliza los 418 módulos
anteriores y compila únicamente los 21 del último
incremento, consultando sus 201 declaraciones
públicas. Los recibos originales no se sobreescriben.

Los dos incrementos intermedios se pueden reproducir separadamente:

```sh
python3 -I -S reproducir_normalizacion.py --report-dir normalizacion_nueva
python3 -I -S reproducir_continuacion.py --report-dir continuacion_nueva
```

La normalización consulta 19 declaraciones.
La continuación compila 11 módulos y consulta
171 declaraciones; reutiliza la normalización
sellada. Los nuevos resultados no reemplazan automáticamente los recibos sellados.

`antecedente/` contiene íntegra y una sola vez la entrega de 406 módulos.
`lean/normalization/`, `lean/continuation/` y `lean/descendants/` separan las
fuentes de los tres incrementos. `recibos/` conserva sus snapshots, objetos,
logs y consultas de axiomas. Los Python de reproducción están en la raíz.

Se requiere el runtime externo exacto Lean 4.21.0 y Mathlib registrado en los
recibos, con sus rutas disponibles. Se comprueba la relocalización de los
archivos del paquete; no se afirma que objetos compilados de una plataforma
sean portables a otra ni se instala o descarga software automáticamente.

`README.md` explica el alcance matemático. El plan, el control causal y los
hashes son comprobaciones distintas de Lean. Ninguna cifra de módulos o archivos
equivale por sí sola a la formalización íntegra de FLM o Moonshine.

## Consumidores terminales incluidos

Después de los campos generales, `lean/terminal/` conserva 22
módulos con 244 declaraciones públicas. Se reproducen sin
recompilar los 439 módulos que consumen:

```sh
python3 -I -S reproducir_terminal.py --plan --report-dir plan_terminal_nuevo
python3 -I -S reproducir_terminal.py --report-dir resultados_terminales_nuevos
```

El recibo terminal es `recibos/terminal/VERIFICATION.json`. «Terminal» designa
el consumidor de este incremento, no el cierre de todos los teoremas de Moonshine.
