# Estado conforme del mismo portador reticular

Este desarrollo continúa el mapa estado–campo ya construido desde el retículo
marcado del artículo I. Reutiliza literalmente sus objetos, el selector terminal,
el cociclo, la base integral, la energía, la traslación y la involución. No vuelve
a seleccionar K ni recibe una función modular como dato generador.

## Orden de las demostraciones

1. `LatticeGramDual` deriva la no degeneración del emparejamiento positivo y
   construye su inversa matricial. `LatticeGramSymmetry` prueba la simetría.
2. `LatticeConformalState` construye
   `ω = (1/2) Σᵢⱼ (G⁻¹)ᵢⱼ aᵢ(-1)aⱼ(-1)1`
   en el portador existente. Su campo es la correspondiente suma de productos
   normales y su energía es dos. `LatticeConformalCoefficient` conserva el
   lector de coeficientes: `Lₘ = coeff(Yω)(-m-2)`.
3. Las contracciones de Gram, las cotas de aniquilación sobre cada vector y la
   evaluación sobre la base prueban `L₀ = E` en `LatticeConformalEnergy`.
   La comparación de conmutadores con todos los creadores y de cargas puras
   prueba `L₋₁ = T` en `LatticeConformalTranslation`. Ninguna de las dos
   identidades se presupone al definir los modos.
4. `LatticeNormalEnergy` y `LatticeStateFieldEnergy` prueban
   `[E,Y(u)ₖ] = Y(Eu)ₖ + kY(u)ₖ` para todo estado, extendiendo la identidad
   cargada por productos normales y linealidad. `LatticeCreationTaylor`
   obtiene `Y(u)ₙ1 = Tⁿu/n!` para cada entero natural n.
5. `LatticeConformalCovariance`, `LatticeConformalLowModes` y
   `LatticeConformalCentralCoefficient` calculan los modos propios de ω.
   En particular `L₁ω=0`, `L₂ω=(rank(G)/2)1` y `Lₘω=0` para `m>2`.
   El término central se evalúa mediante `Σᵢⱼ(G⁻¹)ᵢⱼGⱼᵢ`, no se inserta
   como coeficiente objetivo. `LatticeConformalFoundation` reúne esas
   identidades y las tres relaciones de Möbius.
6. `LatticeEvenTranslation` usa la involución ya comprobada de todos los
   campos para restringir T y Y al subespacio fijo. Prueba además que ω es
   par y que sus modos conservan ese subespacio.
7. `LatticeConformalHeisenberg` demuestra `[L_m,h_i(n)]=-n h_i(m+n)`.
   `LatticeConformalCentralizer` deriva que la diferencia entre el conmutador
   conforme y `(m-n)L_(m+n)` conmuta con todos los modos. Su recurrencia en
   `LatticeVirasoroDefect` y `LatticeVirasoroPolynomial` determina el factor
   cúbico. `LatticeConformalCentralCharge` calcula el valor restante sobre
   todas las cargas puras y lo extiende por creadores.
   `LatticeVirasoroRelations` prueba así Virasoro para todos los índices
   enteros; la carga central 24 procede del rango reticular ya demostrado.
8. `LatticeResidueCreation`, `LatticeResidueTranslation` y
   `LatticeDongAllIndices` prueban creatividad, covarianza y localidad de los
   productos residuales para todo índice entero. La unicidad ya demostrada
   identifica esos productos con `Y(u_p v)` en `LatticeStateFieldProducts`.
   Se conservan ambas regiones de expansión y sus sumas puntualmente finitas.
9. `LatticeConformalGrading` identifica la graduación conforme con los espacios
   de peso finitos anteriores y demuestra el peso de los productos. La entrada
   `SelectedConformalVertex.selected_local_conformal_publication` reúne estas
   propiedades sobre `selectedOrigin`, sin recibir otro retículo o registro.

## Reproducción sin reiniciar la cadena

`verify_vertex_extension.py` autentica los 323 módulos antecedentes y sus
objetos compilados: base 279, coherencia de campos 17, localidad de generadores
2, localidad de todos los estados 11, traslación 12 e involución 2. Compila
únicamente el cierre de las fuentes solicitadas. Consulta todas sus
declaraciones públicas y rechaza axiomas nuevos o pruebas incompletas.

Desde esta carpeta, con los antecedentes conservados en sus rutas de trabajo:

```sh
python3 -I -S verify_vertex_extension.py \
  --modules LatticeCreationTaylor LatticeConformalFoundation LatticeEvenTranslation \
  --report-dir resultados_nuevos
```

El directorio de resultados debe ser nuevo. Los argumentos `--base`, los
distintos `--*-root`, `--*-report-dir`, `--lean` y `--mathlib` permiten indicar
las ubicaciones al trasladar la entrega. `--plan` verifica procedencia y
resolución de importaciones sin compilar: no equivale a un recibo de prueba.

El primer corte ya tiene recibo `conformal_closed_results/VERIFICATION.json`:
17 módulos, 117 declaraciones públicas y 105 teoremas, con SHA-256
`d77a961bb9fed30a971654096d311de8f94d3058ad017a8e8397a3b091bcac43`.
El sucesor `verify_vertex_products.py` reutiliza esos 17 módulos y los 323
anteriores. Sólo compila el cierre nuevo solicitado; su recibo de ejecución
integrada, y no el plan, certifica el nuevo corte. La integración conjunta ha
terminado con `PASS_VERTEX_PRODUCTS_DELTA`: 14 módulos nuevos, 119 declaraciones
públicas y 111 teoremas, sobre 340 antecedentes autenticados sin recompilación.
El recibo `products_closed_results/VERIFICATION.json` tiene SHA-256
`0bea29292112ad21de3c261e8ada14e39642f9e6dcc0d0e85e0deb91f4f98dd0`.
Sólo tres declaraciones de `SelectedConformalVertex` heredan
`Lean.ofReduceBool` del selector anterior; no se introduce allí una nueva
prueba nativa. Los demás sondeos usan únicamente los axiomas ordinarios
declarados en el recibo. Ninguna fuente congelada del primer corte ha cambiado.

Los antecedentes sellados nunca se sobrescriben. El recibo enumera los
enunciados efectivamente comprobados. El sector torcido y el producto orbifold
no se atribuyen automáticamente al álgebra reticular y a su parte fija.

## Procedencia

La arquitectura reticular y la aplicación posterior de FLM están expuestas
en el LaTeX del artículo. Estas fuentes son formalizaciones y certificados
de esa construcción anterior, no una declaración de descubrimiento del
estado conforme clásico. Tampoco redefinen el alcance escrito del artículo:
documentan qué composición está comprobada por el núcleo de Lean. La cadena
escrita del LaTeX no es un resultado desconocido: construye el retículo,
identifica Leech y aplica posteriormente el teorema clásico de FLM. La
formalización de sus operadores internos conserva esa cadena; no convierte
una referencia bibliográfica al teorema clásico en una prueba Lean del
sector torcido ni del grupo completo de automorfismos.
