# Contrato estable del fundamento compartido HMT

Este suplemento añade pruebas de regresión a la biblioteca existente. No
copia sus demostraciones ni altera los manuscritos. Su función es impedir
que una integración posterior cambie silenciosamente los objetos, pierda
memoria o sustituya una conclusión universal por una comprobación finita.

## Base exacta

Se utiliza `PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA`, cuyo ZIP
tiene SHA-256
`535c3e706d9b62b7772f96ad0b2fc3ab1261c012e7b84292bf12c7ec88befdf3`.
El recibo de partida es `recibos/base_compartida/LEAN_CONJUNTO.json`:
122 módulos en la clausura de fuentes, con 48 compilados y 74 objetos
reutilizados después de comprobar sus huellas. No son 122 pruebas nuevas.

`FOUNDATION_BASELINE.json` fija qué variante de cada módulo está activa.
No se debe regenerar automáticamente para aceptar un cambio. Un cambio
legítimo requiere conservar el contrato, comprobarlo y registrar una nueva
línea de base con su procedencia. La conservación de las versiones anteriores
continúa a cargo del registro histórico y del control de preservación.

## Qué exige Lean

`FoundationRegression.lean` contiene tipos explícitos, no solamente consultas
de nombres. Reutiliza las pruebas ya construidas y exige:

1. Reconstrucción de las dos evaluaciones APP mediante TRIT en toda visita.
2. Unicidad de las semillas regionales y coincidencia de su lista compartida.
3. Ecuaciones y unicidad de L₀/L₁ sobre sus registros de transición, junto con
   compatibilidad por truncación de las historias de elevación.
4. Conservación de longitud y prefijo del historial registrado; ausencia de
   reinicio después de un número positivo de pasos, incluidos nueve pasos.
5. Retorno de la fase nonádica con avance de su coordenada de memoria y
   reconstrucción de la profundidad a partir de ambas lecturas.
6. Publicación conjunta de las tres regiones a cualquier escala positiva,
   publicaciones a toda profundidad y compatibilidad de todos sus prefijos.
   El reconocimiento como π, e y φ viene después de los lectores construidos.
7. Identidad definicional del registro compartido, la coordenada alfa, el
   soporte alto y el preacarreo. No basta con que coincidan unos decimales.
8. Publicación de alfa para **todo** `n : Nat`, con salida de acarreo nula y
   los dígitos de longitud `12*n`, sin ocultar el cuantificador en un alias.
9. Composición de acción y electrón con las unidades, positividad y lectores
   explícitos de la prueba existente; se mantiene la conclusión de orden −34.
10. Bandera de incidencia, norma radial, rango 24, paridad, integralidad,
    autodualidad y mínimo del vecino reticular seleccionado, con el tipo
    desplegado y compatible con la entrada común `SharedArticleIBase`.

Dos controles negativos de Lean rechazan usar una publicación de profundidad
cero como prueba a toda profundidad, o una igualdad de fase como igualdad de
estados registrados. Los controles Python rechazan cambios de fuentes,
variantes activas y objetos compilados frente a la línea de base fija.

## Continuidad y alcance

La conexión nonádica conjunta del corpus no se reduce al calendario finito
6→12→18→24→30, a una tabla de cifras, al reloj observable ni a nueve filtros
independientes. Se conserva la prolongación w₆→w₁₂→w₁₈→w₂₄→w₃₀→R₃₆→G₉,
el retorno de fase con memoria y la distinción entre estado enriquecido,
holonomía y publicación reducida. El [mapa de fuentes](GENEALOGIA_FUENTES.md)
mantiene también la continuación excepcional, geométrica y de dualidades.

Los tipos de este suplemento precisan qué partes verifica este control:
`HistoryLift` es el modelo registrado de transporte; las funciones
`nonadicPhase` y `nonadicMemory` son lecturas de profundidad. No se las
identifica con todo el estado enriquecido. La expansión finita de `TPKLifts`
no se presenta como el teorema de publicación a toda profundidad.

Las interfaces X/Y de reconstrucción y S8 del selector se heredan sin
alteración. Los axiomas consultados se registran por declaración; se admiten
los axiomas estándar de Lean y la dependencia computacional `Lean.ofReduceBool`
que ya pertenece al selector finito. No se admite `sorryAx` ni un axioma nuevo.

El mapa conserva los desarrollos de Moonshine, dualidad T y teoría M del
manuscrito; un localizador documental no se cuenta como formalización Lean.
Este suplemento no añade ni proclama un teorema completo de FLM/Moonshine o
de teoría M. Tampoco cambia el alcance de los resultados del manuscrito.

## Reproducción sin duplicar la biblioteca

Requisitos: Python 3, Lean 4.21.0, el paquete base ya desplegado y Mathlib
local compatible (commit `308445d7985027f538e281e18df29ca16ede2ba3`).
No se descargan dependencias ni se reconstruye Mathlib.

Este control incremental exige también la huella del compilador y de los
objetos aceptados. No promete reutilizar binarios de otra plataforma: en un
entorno distinto corresponde reproducir primero la base desde sus fuentes
y registrar una línea de base de ese entorno, sin cambiar los contratos.

```sh
python3 verify_foundation_contract.py --self-test
python3 verify_foundation_contract.py \
  --package "/ruta/PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA" \
  --lean "/ruta/lean4-4.21.0/bin/lean" \
  --mathlib "/ruta/mathlib4" \
  --output "/ruta/salida-nueva"
```

El ejecutor comprueba la línea de base y los objetos existentes, compila
solamente el contrato y registra sus axiomas. La salida identifica por
separado lo compilado en esta ejecución y lo reutilizado. La carpeta de
salida debe ser nueva para no confundir recibos de ejecuciones distintas.

## Regla para los artículos siguientes

Importar `SharedArticleIBase`; no copiar ni reemplazar su registro. Añadir
solamente los desarrollos propios del artículo y conservar sus mapas de
entrada. Ejecutar este contrato antes de integrar un sucesor. Si falla, se
identifica el tipo, archivo o dependencia que cambió; no se reinicia toda la
construcción ni se exige al autor que vuelva a explicar la genealogía.

Los PDF, LaTeX, Python científicos y archivos históricos quedan intactos.
Este ZIP es un suplemento de control y reutilización; necesita el paquete
base señalado y no pretende sustituir una entrega autónoma de los artículos.

## Recibos de esta entrega

- `resultados/contrato_05/VERIFICATION.json`: comprobación incremental final.
- `resultados/contrato_05/FoundationRegression.log`: salida de Lean y
  dependencias axiomáticas por declaración.
- `RUNNER_SELF_TESTS.json`: controles positivos y negativos del ejecutor.
- `FOUNDATION_CAUSAL_RECEIPT.json`: procedencia y alcance del suplemento;
  no sustituye el recibo de compilación.

Las pruebas de implementación anteriores se conservan en la carpeta de
trabajo; el ZIP incluye solamente la ejecución final indicada.
