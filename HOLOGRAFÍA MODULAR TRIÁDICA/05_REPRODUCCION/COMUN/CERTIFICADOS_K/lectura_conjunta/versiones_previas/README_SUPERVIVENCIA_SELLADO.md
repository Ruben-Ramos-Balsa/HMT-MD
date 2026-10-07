# Artículo I — cadena Lean de supervivencia, registros y campos

Esta carpeta contiene la cadena anterior de 251 módulos y seis módulos
adicionales enlazados con ella. Conserva todas las fuentes manifestadas del
paquete anterior. Su README anterior permanece en `versiones_previas`.

El recorrido científico del manuscrito se conserva:
APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del
continuo → publicaciones internas → reconocimiento convencional posterior.
La coordenada real no reemplaza el estado enriquecido completo.

## Qué se incorpora

Las desigualdades de compatibilidad de cilindros definen la supervivencia,
sin incluir como premisa la igualdad al bloque que se pretende obtener.
Se demuestra que seleccionan una única historia; la historia produce los
registros regionales, las elevaciones `L0,L1` y la firma ya verificadas.
La observación a profundidades cofinales es suficiente. Toda historia que
difiere de la seleccionada presenta un rechazo a profundidad finita.

La recurrencia residual posterior a R36 usa el residuo actual y conserva
el balance de prefijo y residuo. Su compatibilidad con los cilindros es una
conclusión demostrada, no una hipótesis añadida. Sus hijos satisfacen el
mismo criterio de supervivencia y producen la misma firma regional.

Las fuentes nuevas se encuentran en `deltas/supervivencia`. La exposición
completa de su alcance y procedencia está en
`procedencia/supervivencia/README_SUPERVIVENCIA_INTEGRADA.md`.

## Una entrada de reproducción

Requisitos: Python 3, Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`, con sus dependencias compiladas.
El paquete incluye todas las fuentes HMT de la cadena; Lean y Mathlib son
dependencias externas declaradas, no archivos científicos omitidos.

```sh
python3 -I -S reproducir_supervivencia.py --plan
python3 -I -S reproducir_supervivencia.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

El primer comando comprueba el manifiesto y el orden de dependencias. El
segundo comprueba los datos de incidencia y ejecuta la cadena Lean. En una
máquina nueva compila las fuentes. Sólo reutiliza una compilación local
cuando coinciden las huellas de fuente, dependencias, compilador y objeto.
Los resultados de ejecución se escriben en `resultados/lean_unificado`;
los recibos de la entrega permanecen en `recibos/supervivencia`.

Los seis módulos añadidos han pasado 48 consultas de axiomas; únicamente
utilizan `propext`, `Classical.choice` y `Quot.sound`. La cadena heredada
conserva la dependencia `Lean.ofReduceBool` de su selector finito; no se
oculta ni se presenta como un axioma añadido por este desarrollo.

## Alcance exacto

Este sucesor conecta supervivencia, historia, registros y realización
residual. No presenta la coordenada real posterior a R36 como la ejecución
histórica de nueve pasos sobre todas las fibras anteriores a R36. Tampoco
certifica la construcción íntegra de FLM y Moonshine ni el artículo íntegro.
Esos enunciados no se deducen del número de archivos ni de la compilación
de resultados con alcance menor.

El estado enriquecido sigue siendo parte del objetivo formal: no se ha
retirado del manuscrito ni sustituido por una tabla. Los PDF no han sido
modificados. Los controles de procedencia y causalidad son metadatos; las
pruebas matemáticas son los términos Lean comprobados.
