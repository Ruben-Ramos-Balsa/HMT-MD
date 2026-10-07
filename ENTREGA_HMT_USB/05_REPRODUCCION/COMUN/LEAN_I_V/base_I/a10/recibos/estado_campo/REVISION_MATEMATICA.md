# Revisión focal de la correspondencia estado–campo

Revisión independiente de las fórmulas y de los enunciados de
`LatticeNormalOrderedField.lean`, `LatticeDescendantFields.lean` y
`LatticeStateFieldMap.lean`. No modifica sus fuentes ni sustituye la
compilación conjunta y su inventario de axiomas.

## Índices y signos

Con la convención `h(z)=Σ_m h_m z^(-m-1)`, el término creador
`h_(-r-1) z^r`, después de aplicar la derivada dividida de orden `n`, aporta
`choose(r,n) z^(r-n)`. Al escribir `r=a+n`, el exponente es `a`, y el
coeficiente del producto normal en grado `k` utiliza `B[k-a]`.

Para `m=a≥0`, la derivada dividida de `z^(-a-1)` es
`(-1)^n choose(a+n,n) z^(-a-n-1)`; el segundo término del producto normal
utiliza por tanto `B[k+a+n+1] h_a`. Las dos expresiones implementadas
conservan el orden de composición correcto: creadores a la izquierda,
modos no negativos a la derecha. No se detectó un desplazamiento ni un
signo incorrectos en estas fórmulas.

## Finitud y truncación

La suma creadora es finita sobre cada vector porque los coeficientes
`B[k-a]v` se anulan cuando `a` supera el límite inferior de Laurent de
`Bv`. La suma restante es finita porque sólo intervienen finitos modos
no negativos del vector de entrada. El modo cero se mantiene dentro de
ese conjunto finito; no se lo trata incorrectamente como un aniquilador
nulo sobre cualquier carga.

El límite inferior común del producto normal se obtiene después mediante
un mínimo sobre esos finitos modos. Es una cota para cada pareja campo–
vector, exactamente el tipo exigido por `VertexOperator.of_coeff`.
No constituye un límite uniforme de frecuencias para todo el portador y
no reduce el espacio a una ventana finita.

## Creación y vacío

`normalField_creates` no presupone su conclusión: usa la propiedad
previamente comprobada del campo de entrada. En grado negativo todos
los términos sobre el vacío desaparecen; en grado cero la suma creadora
se reduce al término `a=0`, mientras la suma de modos no negativos se
anula. El resultado es precisamente la acción del creador existente.

La inducción `descendantField_creates` comienza en el campo cargado
concreto y aplica ese resultado. Después `Basis.constr` extiende los
campos de la base a todos los estados. La recuperación en el vacío y la
inyectividad se deducen de esa extensión y de las identidades ya
demostradas; no se incorporan como campos axiomáticos de una estructura.

El campo del vacío se identifica por sus coeficientes con la identidad
mediante el resultado anterior de carga cero. La coincidencia en los
estados de un oscilador usa el puente probado con el campo de Heisenberg
derivado, no una segunda definición independiente de los generadores.

## Elección de palabras y alcance exacto

`wordForOccupation a = a.toMultiset.toList` proporciona una lista concreta
con exactamente las multiplicidades de `a`. Se demuestra que sus
creadores producen el vector correspondiente de la base existente. Para
dos palabras con la misma ocupación se demuestra la igualdad de los
**estados** producidos.

La definición de `stateField` es por ello una asignación lineal válida
sobre una base auténtica. Sin embargo, la igualdad

`stateField (descendantState x w) = descendantField x w`

para **toda** palabra `w` no se obtiene solamente de la creatividad o de
la inyectividad del mapa. Los campos pueden tener el mismo coeficiente
constante sobre el vacío sin que esa observación determine su acción
completa. En estos archivos no se afirma esa inferencia.

Un avance acotado posterior consiste en demostrar la conmutación de las
dos operaciones de producto normal de Heisenberg sobre cualquier campo
del mismo portador. Al desarrollar ambas composiciones, los términos
mixtos se emparejan y los otros utilizan la conmutación de los creadores
y de los modos no negativos. Esa demostración exige justificar los
intercambios de sumas localmente finitas. Permitiría pasar a invariancia
por permutaciones de la palabra y demostrar la igualdad anterior para
cualquier representante, sin postular FLM ni otro teorema externo.

## Resultado de esta revisión

No se detectó un error matemático concreto en los tres módulos revisados.
Sus enunciados no afirman localidad mutua de todos los descendientes,
Jacobi, la construcción del sector torcido o el producto orbifold, ni
identifican por axioma su grupo de automorfismos con el Monstruo. La
construcción escrita en el manuscrito y el alcance de esta comprobación
Lean permanecen distinguidos.

Fuentes revisadas, SHA-256:

- `LatticeNormalOrderedField.lean`: `e6ee1ce2fa8e0573b9f2cc4070d2d14cf8266223bb3d70f279a3cb9a8c24d171`.
- `LatticeDescendantFields.lean`: `86a41de81135ccd645cb4a86c320d554fd41058cd707bf935d1ade3fe7a08492`.
- `LatticeStateFieldMap.lean`: `4d517f865de1ba62ce1ee45c3b7361b46567f6453a70d37b4bbdcfdf5e944b80`.
