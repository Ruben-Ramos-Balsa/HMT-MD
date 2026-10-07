# Entrada única de la composición formal del artículo I

Abrir `deltas/base_compartida/SharedArticleIBase.lean`. El teorema
`HMT.Shared.ArticleI.shared_action_electron_incidence` reúne las ramas de
acción–electrón e incidencia–retículo sobre el mismo registro seleccionado.
Reutiliza sus pruebas por importación; no las vuelve a copiar ni recibe K
mediante una igualdad asumida.

## Reproducción

```sh
python3 -I -S reproducir.py --check --n69
python3 -I -S reproducir_base_compartida.py --plan
python3 -I -S reproducir_base_compartida.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

Lean 4.21.0 y Mathlib `308445d7985027f538e281e18df29ca16ede2ba3` son
requisitos externos de ejecución. Todas las fuentes HMT importadas por
esta entrada están incluidas. `--plan` no compila. El tercer comando
compila y consulta los axiomas; sólo reutiliza objetos con huellas
verificadas de fuente, dependencias y compilador. El resultado efectivo
queda en `resultados/lean_unificado/VERIFICATION.json`.

El registro común conserva la secuencia regional, calendario, N69,
descriptor, selección terminal, publicaciones de alfa a toda profundidad,
soportes, origen marcado y retículo. La rama de acción–electrón conserva
sus unidades positivas, lectores y refinamiento explícitos.

## Alcance exacto

El selector finito conserva como entrada explícita el repertorio no
ordenado de ocho continuaciones S8. Estos módulos no prueban su selección
prospectiva desde el estado inicial. Tampoco formalizan la construcción
FLM completa ni el teorema de Moonshine. Esta delimitación afecta a los
archivos Lean reunidos, no declara inexistencia de esos desarrollos en
el corpus. El cálculo finito hereda `Lean.ofReduceBool`; no se lo presenta
como reducción exclusiva del núcleo. No se han añadido axiomas de HMT,
`sorry` ni `admit` para suplir pruebas.

## Conservación

Los 422 archivos del paquete anterior se conservan sin cambiar un byte.
Sus recibos distinguen la compilación transitiva base de 74 módulos y
las ampliaciones incrementales posteriores. La entrada compartida
conserva su recibo incremental propio; una ejecución completa posterior
tiene un recibo distinto. Las fuentes íntegras y el suplemento del
artículo X permanecen como material de continuidad. Los PDF no cambian.

Los scripts `reproducir.py --lean` y `reproducir_deltas.py` anteriores
se conservan para reproducir sus alcances originales. Para el conjunto
actual se utiliza `reproducir_base_compartida.py`.
