# Composición seleccionada HMT de los artículos I–V

Este suplemento reúne las entradas Lean de las cadenas principales y sus aplicaciones tipadas seleccionadas. Conserva íntegramente la entrega del primer artículo y añade los consumidores de II, III, IV y V sobre sus mismas coordenadas regionales. No modifica los PDF ni sustituye sus paquetes LaTeX editoriales.

## Orden de lectura y ejecución

La cadena comienza en APP–TRIT–TPK, el estado enriquecido y la estructura discreta conjunta del continuo. Las publicaciones regionales y el registro seleccionado se conservan como resultados anteriores. Las coordenadas de acción y los lectores posteriores los consumen; no se introduce retrospectivamente una cifra física para construir el registro.

| Artículo | Entrada seleccionada | Resultado reunido |
| --- | --- | --- |
| I | `ArticleIPrincipalPublication` | Publicaciones regionales a toda profundidad, alfa, acción, composición electrónica, plano APP, espín/helicidad y condiciones del enganche excepcional. |
| II | `SelectedCKMPublication`, `SelectedActionGravityThermal`, `SelectedAreaInformation`, `SelectedPentadicTensor` | CKM sectorial, acción y transducción circular/térmica, estado de frontera y representación tensorial sobre las coordenadas ya seleccionadas. |
| III | `SelectedConstitutivePublication` | Respuesta constitutiva positiva y única, inversión angular, refinamiento y relaciones eléctricas sobre la misma acción. |
| IV | `ArticleIVSelectedScreens` | Dirección seleccionada por K, proyección dimensional y pantallas, con radio elíptico y dualidad en la realización especificada. |
| V | `SelectedThermalPublication`, `SelectedBoltzmannRadiation` | Modos fermiónicos y bosónicos, ocupaciones, límite termodinámico y radiación usando acción, velocidad y transductor térmico seleccionados. |

Cada archivo contiene el enunciado exacto y sus parámetros. Las bases dimensionales positivas, los estados térmicos y las representaciones posteriores permanecen explícitos cuando intervienen. La igualdad del registro final no se añade como nueva premisa de estos consumidores.

La conservación conjunta no convierte cinco aspectos del continuo en cinco generadores independientes. La organización por artículos es una organización de consumidores del núcleo preservado.

## Contenido

- `base_I/`: entrega anterior completa e inalterada, con fuentes, objetos, recibos y aplicación clásica documentada.
- `lean/` y `objects/`: fuentes adicionales y sus objetos compilados.
- `REGISTRO_UNIFICADO.json`: correspondencia de fuentes, objetos, dependencias, hashes y entradas por artículo.
- `procedencia/`: recibos y fuentes auxiliares de las intervenciones; los scripts históricos con rutas locales se conservan como antecedente, no son el punto de entrada portátil.
- `reproducir.py`: entrada portátil de comprobación y reproducción.
- `MANIFIESTO.json`: inventario exacto de la entrega.

No hay que buscar módulos ni ordenar carpetas manualmente. El reproductor lee el registro y determina el orden de importación.

## Uso

Comprobación de integridad, sin compilar ni modificar la entrega:

```text
python3 -I -S reproducir.py --verify-only --report-dir /ruta/nueva/integridad
```

Reproducción de los consumidores de todos los artículos, reutilizando los objetos comprobados de sus antecedentes:

```text
python3 -I -S reproducir.py --article all --lean /ruta/lean --mathlib-root /ruta/mathlib4 --report-dir /ruta/nueva/resultados
```

Para un solo artículo, sustituir `all` por `I`, `II`, `III`, `IV` o `V`. El programa incluye también los consumidores anteriores que ese artículo importa. La carpeta de resultados debe ser nueva y estar fuera de la entrega.

Herramientas fijadas: Lean 4.21.0 y Mathlib `308445d7985027f538e281e18df29ca16ede2ba3`. Los objetos entregados corresponden a macOS ARM64; el modo normal exige el mismo binario registrado. Para reconstruir la clausura completa desde las fuentes en otra plataforma se usa `--from-sources --portable-toolchain`, con esa versión de Lean y ese commit de Mathlib. El programa no descarga herramientas ni inicia procesos al insertar un USB.

## Alcance de la comprobación

El recibo de ejecución distingue fuentes recompiladas, objetos reutilizados y declaraciones cuyo conjunto de axiomas se imprimió. Compilar estas entradas acredita sus enunciados exactos; no convierte automáticamente cualquier frase narrativa o identificación física del manuscrito en un teorema Lean.

La aplicación de los resultados clásicos de Leech, Frenkel–Lepowsky–Meurman y Moonshine se documenta en `base_I/APLICACION_CLASICA.md`, una vez comprobadas las condiciones propias del enganche. No se exige volver a demostrar esa matemática clásica, ni se la disfraza de axioma Lean nuevo.

Se conserva el uso heredado y declarado de `Lean.ofReduceBool` en el selector regional, junto con los axiomas ordinarios indicados en los recibos. El dominio y las interfaces del selector siguen siendo los de las fuentes del primer artículo; esta composición no los sustituye por una selección retrospectiva.

El fallo histórico de huella de `AGENTS.md` se conserva con su conciliación editorial. No se transforma en un PASS global ni se modifica un certificado anterior para ocultarlo.
