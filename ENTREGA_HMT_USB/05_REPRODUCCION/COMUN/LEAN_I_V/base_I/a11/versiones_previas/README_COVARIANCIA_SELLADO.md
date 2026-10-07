# Artículo I — continuación de campos y simetrías reticulares

Entrada única reproducible:

```sh
python3 -I -S reproducir_covariancia.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

Requiere Python3, Lean4.21.0 y Mathlib commit
`308445d7985027f538e281e18df29ca16ede2ba3`.
Esta carpeta y su ZIP contienen la clausura de fuentes HMT. No requieren
otra carpeta privada HMT. El ejecutor coteja las huellas, comprueba imports,
reutiliza objetos sólo tras verificar su procedencia y compila los cambios.
Consulta además los axiomas de las declaraciones registradas. El manifiesto
y los recibos distinguen compilación, conservación documental y alcance.

## Continuidad matemática

Se conserva la cadena APP → TRIT → TPK → estado enriquecido → publicaciones
regionales → registro seleccionado → incidencia → retículo → cociclo y
álgebra torcida → Fock → campos. Se conserva el contenido preciso de las
publicaciones anteriores de acción y electrón, incluidos sus parámetros,
dominios y condiciones. No se reinicia K ni se introduce un coeficiente de
Moonshine como dato generador.

Los módulos nuevos prolongan esos mismos operadores:

- Covarianza de carga de todos los coeficientes del campo reticular.
- Conjugación de los campos por la involución de orden dos, y estabilidad
  de la parte fija bajo las combinaciones simétricas de campos.
- Derivación de traslación de osciladores y su extensión cargada, con
  vacío anulado y conmutador energético de peso uno. La identidad diferencial
  de creación sobre el vacío se demuestra para todos los coeficientes.
- Conmutador mixto de los aniquiladores con el exponencial de creación,
  cuyo coeficiente es el emparejamiento integral del retículo ya construido.
- Conmutación de aniquiladores con los coeficientes exponenciales de
  aniquilación y conservación del corte efectivo después de aniquilar.
- Corrección de fase cuadrática para elevar el Coxeter a la misma álgebra
  torcida; su compatibilidad multiplicativa y su cubo identidad se prueban.
  Este levantamiento no se identifica aquí con una acción del orbifold ni
  con el centralizador de la involución no corregida.

La entrada conjunta está en `deltas/covariancia/SelectedCovariantFields.lean`.
Los enunciados de los módulos, y no el número de archivos, fijan qué queda
formalmente demostrado. La construcción de campos, sus conmutadores y las
simetrías anteriores no se declaran por sí solas una demostración de Jacobi,
de una representación completa de Virasoro, del producto del sector torcido,
del orbifold de FLM o de su grupo de automorfismos Monstruo.

El LaTeX aplica el teorema clásico de Frenkel–Lepowsky–Meurman después de
construir y reconocer el retículo. Aquí no se ha introducido ese teorema como
axioma Lean. Su prueba formal completa y la de Moonshine no se certifican en
esta continuación. Tampoco se modificaron los PDFs.

Todos los archivos anteriores están conservados byte por byte; el README
anterior se encuentra en `versiones_previas/README_CAMPOS_SELLADO.md`.
La consulta heredada a `Lean.ofReduceBool` se mantiene identificada; las
nuevas pruebas generales de operadores sólo usan los axiomas estándar.
El recibo de compilación conjunta es
`recibos/covariancia/LEAN_CONJUNTO.json`.
