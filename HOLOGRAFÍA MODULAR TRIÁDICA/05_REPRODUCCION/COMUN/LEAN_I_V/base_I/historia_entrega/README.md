# Artículo I: enganche HMT y aplicación de FLM

## Resultado de esta entrega

La entrada `lean/ArticleIExceptionalInterface.lean` reúne el enganche propio
de HMT con el retículo al que se aplica la construcción clásica de
Frenkel–Lepowsky–Meurman (FLM). No se vuelve a seleccionar K, ni se proporciona
una igualdad de K como hipótesis del teorema final.

`article_I_exceptional_interface` conserva conjuntamente:

- la bandera y el punto marcado procedentes de las incidencias regionales;
- la incidencia concreta cuatro más uno y la octada transversal;
- el mismo vecino reticular, positivo, par, integral, autodual, de rango24,
  con norma mínima4 y, por tanto, sin raíces de norma2;
- la igualdad entre el defecto residual suma–producto, la norma radial54 y
  las lecturas operatorias APP/Fock ya construidas;
- el cociclo, los osciladores, los modos cero y la paridad sobre ese origen.

Los resultados se obtienen por composición de las pruebas conservadas, no
mediante campos de un certificado que presupongan la conclusión.
El defecto de cociente129 permanece separado y conservado: la identidad
completa es `2025−810 = 54+9·129`. La igualdad con54 no sustituye las pruebas
reticulares ni equivale por sí sola a la identidad de Jacobi de una VOA.

## Aplicación del resultado clásico

El manuscrito identifica el vecino construido con Leech mediante las
propiedades anteriores. Después aplica la construcción FLM estándar sobre
ese retículo, obteniendo el álgebra Moonshine y su grupo de automorfismos.
La nota `APLICACION_CLASICA.md` explicita esta composición y sus referencias.

Este es el alcance de cierre solicitado por los autores: demostrar el
enganche propio y usar, por referencia, la matemática clásica posterior.
No se exige reproducir en Lean toda la prueba clásica de FLM. Tampoco se
afirma falsamente que el núcleo de Lean haya comprobado esa prueba externa.
No hay axioma FLM, axioma Monster ni `sorry` en la nueva fuente.

## Orden de lectura y reproducción

1. Leer este README y `APLICACION_CLASICA.md`.
2. Abrir el teorema terminal en `lean/ArticleIExceptionalInterface.lean`.
3. Seguir sus importaciones registradas en `REGISTRO_REPRODUCCION.json`.
   `antecedente/` conserva íntegra, una sola vez, la entrega anterior de477
   módulos y sus fuentes, datos, Python, LaTeX, PDFs y recibos.
4. Ejecutar explícitamente el reproductor desde esta carpeta:

```text
python3 -I -S reproducir.py --report-dir /ruta/nueva/resultados \
  --lean /ruta/lean-4.21.0/bin/lean --mathlib-root /ruta/mathlib4
```

`--verify-only` comprueba la integridad sin compilar. La ejecución normal
autentica el compilador, Mathlib y las dependencias, y compila únicamente la
entrada terminal nueva. No recompila los477 módulos anteriores. Requiere
Lean4.21.0 y Mathlib `308445d7985027f538e281e18df29ca16ede2ba3`.
Los objetos entregados y el recibo corresponden a macOS arm64; otras
plataformas necesitan reconstruir los antecedentes desde sus fuentes.
No se autoejecuta nada al conectar un USB.

La cadena causal heredada es APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo → publicaciones aritmética e
incidencial → retículo → reconocimiento clásico. π, φ, e y α conservan sus
lectores y orden interno; no se inyectan valores metrológicos como entradas.
Los límites de cada módulo antecedente permanecen en sus fuentes y recibos;
esta entrega no modifica retroactivamente sus enunciados.

La política de axiomas registra `propext`, `Classical.choice`, `Quot.sound`
y `Lean.ofReduceBool` heredado del selector finito. La nueva fuente no usa
`native_decide`. Esa dependencia computacional no se oculta como prueba
exclusivamente reducida por el núcleo.

## Conservación

Los PDF y LaTeX científicos no se modifican. Los desarrollos adicionales
sobre campos torcidos y normalización permanecen conservados como suplementos
en sus carpetas de trabajo. No se convierten en requisitos nuevos para la
aplicación bibliográfica de FLM ni en una segunda demostración atribuida a HMT.
