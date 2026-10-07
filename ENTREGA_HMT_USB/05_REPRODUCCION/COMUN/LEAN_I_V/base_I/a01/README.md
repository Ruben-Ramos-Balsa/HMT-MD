# Artículo I: cuatro productos de estados construidos

Esta entrega prolonga la misma genealogía APP–TRIT–TPK → estado enriquecido →
estructura discreta conjunta del continuo. Reutiliza el retículo marcado, su
cociclo, los portadores y la selección ya construidos; no vuelve a elegir K ni
introduce otro retículo. La generación correlacionada de π, φ, e y α pertenece
al antecedente común; no se ejecuta una nueva generación numérica en este delta.
Los campos y las formas bilineales son realizaciones posteriores sobre esa
estructura heredada, no nuevos nombres para los operadores del TPK.

## 1. Forma del sector par y representación por pesos

Cinco módulos construyen la forma bilineal compleja sobre el portador
reticular no torcido y su restricción al sector par efectivo. Demuestran no
degeneración, ortogonalidad de pesos distintos y representación única de
funcionales en los espacios homogéneos finitos. Se conserva la matriz de Gram
y el cociclo anteriores; no se supone una forma final ni se declara positiva
definida o hermítica por llamar «par» o «positivo» a un sector.

Propietarios: `GradedPairingRepresentability`, `LatticeChargePairing`,
`LatticeIntegerPairingWeights`, `LatticeUntwistedPairing` y
`LatticeEvenPairingRepresentability`.

## 2. Reconstrucción en el dual restringido

`LatticeEvenRestrictedDual` representa en `evenSpace` los funcionales que se
anulan a partir de algún peso. La suma de representantes homogéneos es
independiente del corte, única y lineal. Las identidades inversas prueban una
equivalencia lineal entre el sector par existente y ese dual de soporte
acotado. No se identifica el portador infinito con todo su dual algebraico.

## 3. Soporte homogéneo de los coeficientes contragredientes

Siete módulos demuestran la covarianza energética efectiva de productos
normales, campos crudos, corrección, descenso positivo y bloque TE, junto con
la compatibilidad energética de la forma. De ahí obtienen el soporte en un
único peso de los coeficientes contragredientes. Las covarianzas utilizadas
son conclusiones de la cadena, no hipótesis nuevas del resultado terminal.

Propietarios: `LatticeTwistedNormalEnergy`, `LatticeTwistedRawEnergy`,
`LatticeTwistedCorrectedEnergy`, `SkewFieldEnergy`,
`LatticeTwistedPairingEnergy`, `LatticeTwistedFullEnergy` y
`LatticeContragredientWeightSupport`.

## 4. Producto torcido–torcido efectivo

`LatticeTwistedPairProduct` aplica ese soporte a estados arbitrarios mediante
su descomposición finita por pesos. Demuestra que los coeficientes pertenecen
al dual restringido y construye sus representantes únicos en el sector par.
También demuestra truncación Laurent para todo par de estados torcidos. Así
define el campo TT concreto, bilineal en los estados: ya no es un argumento
libre, ni sólo un funcional con valores en el dual, ni una representabilidad
recibida como hipótesis.

## 5. Asignación concreta de los cuatro bloques

`LatticeOrbifoldFullStateFields` reúne EE, ET, TE y TT sobre la suma de los
dos sectores existentes. Prueba sus fórmulas de coeficientes, vacío, creación,
anulación de coeficientes negativos sobre el vacío e inyectividad. El campo
del estado conforme coincide con los modos ya construidos, y sus coeficientes
satisfacen Virasoro con carga central 24 para todos los índices enteros.

La construcción completa de los cuatro productos se afirma en este sentido
preciso de asignación lineal por campos Laurent sobre los portadores efectivos.
No se usa esa expresión como sustituto de las identidades globales de localidad
o Jacobi mixto.

## 6. Especialización a la selección heredada

`SelectedOrbifoldStateFields` instancia los resultados en el mismo
`selectedOrigin`. Sus seis declaraciones públicas reúnen el portador, la
asignación, los cuatro productos, vacío y creación, el enlace conforme y los
pesos bajos ya probados. No ejecuta otra selección regional.

Esta especialización tiene un recibo separado: además de `propext`,
`Classical.choice` y `Quot.sound`, registra explícitamente `Lean.ofReduceBool`
heredado de `SelectedConformalVertex`, cuya fuente y objeto se fijan por SHA.
No contiene `native_decide` ni añade un axioma. Esta política no se extiende
a las quince nuevas fuentes generales, cuyas consultas admiten sólo los tres
axiomas ordinarios.

## Conservación y reproducción

La entrega de 461 módulos se conserva íntegra una sola vez en `antecedente/`,
con su manifiesto, PDFs, fuentes, objetos, recibos y testimonios históricos
sin editar. El incremento general contiene 15 módulos: 5 + 1 + 7 + 1 + 1.
El corte principal es 476; la especialización seleccionada se conserva aparte
y lleva el total de fuentes registradas a 477. Las reservas de los README
anteriores conservan su contexto histórico y no sustituyen estos resultados.

El verificador portable autentica fuentes, objetos, logs, consultas públicas
y huellas de los recibos. `--plan` sólo autentica. Una ejecución explícita
recompila los 15 módulos nuevos contra los objetos anteriores; nunca recompila
los 461. La especialización se reproduce por una ejecución separada y explícita
con su propia política de axiomas. Se requiere el runtime Lean/Mathlib
autenticado indicado por la ayuda; no hay autoejecución al conectar un USB.

La verificación de conservación de archivos, la consulta de axiomas y la prueba
de cada identidad son controles diferentes. La carpeta desplegada y el ZIP
conservan los mismos archivos, con CRC y SHA verificados por entrada. Las
ampliaciones futuras no se añaden silenciosamente a este inventario cerrado.

## Alcance que esta entrega no afirma

No se atribuye una nueva prioridad al álgebra de operadores de vértice ni a la
construcción clásica de Frenkel–Lepowsky–Meurman. Este corte no afirma la
localidad global entre todos los bloques ni la identidad de Jacobi mixta
completa; tampoco FLM completo, `Aut(V♮)=Monster` o el teorema de Moonshine.
No declara cerrado el artículo I entero. Estas exclusiones no rebajan a
hipótesis el TT efectivo, los otros tres productos, la reconstrucción o las
compatibilidades concretas que sí se han demostrado.
