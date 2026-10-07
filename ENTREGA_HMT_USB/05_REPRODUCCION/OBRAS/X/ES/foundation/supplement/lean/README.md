# Formalización Lean focal del balance bilateral

`BalanceBilateral.lean` demuestra siete proposiciones universales en Lean4.21.0,
usando exclusivamente su biblioteca `Std`. El archivo contiene términos de
prueba comprobables por Lean; no es una enumeración de valores de prueba.

## Objeto y alcance

Para coordenadas enteras `x,y`, define los dos lectores mediante las expresiones
`8x-y` y `9x+y`. La identidad formalizada es

\[
9(8x-y)^2+8(9x+y)^2=17(72x^2+y^2).
\]

Sumando las primeras `n` coordenadas de funciones `Nat -> Int`, la identidad se
demuestra para todo `n`, incluidos cero y doce. Si ambas entradas tienen la misma
suma de cuadrados, el resultado es `17 * 73` veces esa suma. Esta hipótesis es
explícita: el archivo no presupone ni demuestra que todo transporte la satisfaga.
El par de lectores también determina exactamente ambas entradas enteras:

\[
(8x-y)+(9x+y)=17x,\qquad
8(9x+y)-9(8x-y)=17y.
\]

La inyectividad se demuestra sobre `Int`; las fórmulas de recuperación se dejan
sin división para conservar exactamente ese dominio.

El antecedente matemático es el balance bilateral de la nota archivada
`../exploracion14/AMPLIACION_03_REFINAMIENTO_UNIDAD_Y_TRANSDUCCION_20260914/LEY_BILATERAL_UNIDAD_Y_TRANSDUCCION.md`,
§3. Esta formalización es una especialización entera posterior de esa ley. La
producción de los operadores por APP--TRIT--TPK, los espacios de Hilbert generales,
las constantes, la física y los restantes resultados del libro conservan sus
demostraciones textuales y controles propios; este archivo no les atribuye una
verificación Lean.

## Declaraciones comprobadas

- `HMT.Bilateral.balance_polynomial`: identidad escalar universal sobre enteros.
- `HMT.Bilateral.scalar_norm_preserving`: balance escalar con igualdad de cuadrados.
- `HMT.Bilateral.finite_balance`: suma de la identidad en dimensión finita arbitraria.
- `HMT.Bilateral.finite_norm_preserving`: balance con igualdad de sumas de cuadrados.
- `HMT.Bilateral.recovery_x`: recuperación entera de `17x`.
- `HMT.Bilateral.recovery_y`: recuperación entera de `17y`.
- `HMT.Bilateral.readers_injective`: inyectividad del par completo de lectores.

## Reproducción

Se necesita Lean4.21.0 ya instalado. No se necesita Mathlib ni un proyecto Lake.
Desde esta carpeta:

```sh
lean -DwarningAsError=true BalanceBilateral.lean
python3 verificar_lean.py --lean-bin /ruta/a/lean
```

`--lean-bin` es opcional cuando `lean` está en `PATH`. El comprobador no instala
herramientas ni ejecuta comandos de descarga. Para una ejecución estrictamente
local, puede indicarse directamente el binario del toolchain instalado en lugar
de un gestor que seleccione o descargue versiones.

El programa escribe `RESULTADO_LEAN.json` con versión, comando, código de salida,
huella de fuente y ejecutable y axiomas utilizados por las siete declaraciones.
Se puede escoger otro destino mediante `--output`. Un error produce código de
salida distinto de cero y se registra como fallo, nunca como comprobación pasada.

Las pruebas no contienen `sorry`, `admit` ni axiomas propios. La salida de
`#print axioms` registra las dependencias estándar `propext`, `Quot.sound` y, en la
prueba de inyectividad, `Classical.choice`. Esa información permanece visible;
no se afirma ausencia de los fundamentos lógicos de Lean.

El resultado JSON es un registro de ejecución, no una prueba independiente. La
prueba formal reside en los términos elaborados a partir de la fuente `.lean` y
aceptados por el núcleo de Lean. El programa Python y los controles científicos
anteriores cumplen funciones distintas.
