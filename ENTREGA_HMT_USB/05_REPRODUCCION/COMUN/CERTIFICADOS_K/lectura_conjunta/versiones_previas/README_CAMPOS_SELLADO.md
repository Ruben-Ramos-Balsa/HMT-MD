# Continuación Lean del artículo I: energía y campos reticulares

Esta carpeta sucede al corte de traza graduada. Conserva sus fuentes y sus
pruebas; el README anterior está íntegro en
`versiones_previas/README_TRAZA_SELLADO.md`. No se reinicia la selección de K.

## Una entrada reproducible

```sh
python3 -I -S reproducir_campos.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

Dependencias declaradas: Python3, Lean4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`. Las fuentes HMT de la clausura
están en esta carpeta y en su ZIP; no se necesita otro directorio privado HMT.
El ejecutor comprueba los hashes y el cierre de imports, reutiliza objetos
sólo con claves verificadas, compila los módulos cambiados y consulta los
axiomas de los teoremas principales registrados. No reconstruye Mathlib.

Entrada matemática conjunta: `deltas/campos/SelectedEnergyInput.lean`.
Teorema: `HMT.I.SelectedEnergyInput.shared_action_electron_energy_and_fields`.

## Cadena conservada y continuación efectiva

`APP → TRIT → TPK → estado enriquecido → publicaciones regionales → registro
seleccionado → incidencia → retículo → cociclo y álgebra torcida → osciladores
→ campos de Heisenberg → energía y operadores exponenciales reticulares`.

Se conservan los objetos, parámetros y condiciones de la publicación previa
de acción y electrón. Ningún coeficiente del carácter de Moonshine se usa
como entrada de estas nuevas operaciones. Los resultados precedentes se
importan; no se sustituyen por duplicados o por una tabla de valores.

La continuación incluye:

- El operador de energía sobre el mismo portador. Sus espacios propios son
  exactamente las piezas finitas de peso utilizadas en la traza.
- Su construcción operatoria: derivación de Euler de los osciladores más
  semínorma de la carga reticular. La identidad no se supone.
- Los conmutadores con los modos enteros reales de Heisenberg y con los
  desplazamientos de carga del álgebra torcida.
- La línea del vacío como espacio propio de energía cero. En peso uno,
  la parte par del sector **no torcido** es nula, utilizando la ausencia
  de raíces ya demostrada para el mismo retículo.
- Los coeficientes exponenciales de creación y aniquilación, construidos
  para cualquier grado, con sus controles de finitud y de peso.
- Los campos reticulares sobre el portador ya construido: la aniquilación
  termina en cada estado por una cota demostrada de su soporte monomial;
  la fórmula no depende de ampliar el corte por encima de esa cota. Se
  comprueban truncación de Laurent, vacío y campo identidad de carga cero.
- La compatibilidad entre energía y cada coeficiente del campo cargado.
- El levantamiento de la isometría reticular de orden tres al Fock real,
  con orden exactamente tres, vacío conservado y creación covariante.

La graduación y las operaciones anteriores son objetos algebraicos
efectivamente construidos. La acción de orden tres en Fock no se identifica
sin prueba con la carta matricial de seis bloques C y seis bloques C inverso:
el retículo utiliza su carta de Witt. Tampoco se confunde esa acción con la
involución de orden dos utilizada en la traza.

## Frontera exacta respecto de FLM

El LaTeX conservado aplica la construcción clásica de
Frenkel–Lepowsky–Meurman al retículo construido y reconocido como Leech.
Esta entrega amplía su implementación algebraica; no introduce ese teorema
como un axioma de Lean. Construir los campos lineales truncados no sustituye
la prueba de la identidad de Jacobi o de la reconstrucción de VOA. Tampoco
declara verificados el producto completo del
orbifold torcido, su grupo de automorfismos Monstruo ni el teorema de
Moonshine de Borcherds. Tampoco identifica el operador de energía con una
representación completa de Virasoro sin construir esa representación.

La existencia de fuentes Lean y una compilación correcta no acreditan por
sí solas todo el manuscrito: el resultado comprobado es el enunciado preciso
de cada declaración registrada. No se han modificado los PDFs.

No se añaden `sorry`, `admit` ni axiomas HMT. El uso heredado de
`Lean.ofReduceBool` en el selector finito permanece identificado. Los nuevos
lemas operatorios generales sólo usan los axiomas estándar de Mathlib.

El recibo conjunto congelado está en `recibos/campos/LEAN_CONJUNTO.json`.
Una nueva ejecución escribe `resultados/lean_unificado/VERIFICATION.json`.
El manifiesto conserva las huellas y permite comprobar el predecesor sin
alterarlo.
