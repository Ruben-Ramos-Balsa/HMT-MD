# Artículo I: campos de estados y producto TE en la prolongación reticular torcida

Esta entrega continúa la formalización existente sobre el mismo retículo
seleccionado. Conserva la genealogía APP–TRIT–TPK → estado enriquecido →
estructura discreta conjunta del continuo. No vuelve a elegir K, no sustituye
sus lectores y no introduce un retículo independiente. La selección regional,
la incidencia excepcional, el cociclo, los portadores y sus graduaciones se
reciben de las fuentes verificadas que permanecen en `antecedente/`.

La generación correlacionada de π, φ, e y α y la lectura excepcional pertenecen
al antecedente común; no se ejecuta otra generación numérica en este incremento.
La construcción actual está situada después de esa publicación reticular:
formaliza campos sobre sus espacios lineales concretos. Los operadores de
campo no se renombran como operadores TPK. Ningún valor de comparación ni
grupo de automorfismos actúa como entrada del selector HMT.

## Construcciones efectivas añadidas

1. Se normaliza el campo de una carga con el factor reticular y el desplazamiento
   de exponente de la fórmula torcida. Se prueban truncación, identidad de carga
   cero y covarianza energética. La covarianza por sí sola no se presenta como
   una prueba de unicidad de la normalización.
2. Se demuestra la reordenación operatoria completa de cada par de coeficientes
   exponenciales, con los coeficientes del factor de contracción ya construido.
   No se sustituye esa igualdad de operadores por una coincidencia escalar.
3. Se construyen los productos normales de todas las derivadas divididas de los
   campos semienteros. La variable es `z=t²`: la derivación se hace respecto de
   z, no de t. Se prueba la finitud puntual antes de intercambiar sumas.
4. Se define el campo sin corregir sobre toda la base de estados del retículo
   y se extiende linealmente. La conmutación de los productos normales demuestra
   su independencia de la palabra que representa cada ocupación y su recursión
   sobre todo el portador, no sólo sobre unos ejemplos.
5. Se construye el operador de corrección Δ a partir del núcleo bivariado y de
   la matriz de Gram inversa heredada. Se prueban su descenso de energía,
   compatibilidad con la involución y finitud sobre cada estado. Su exponencial
   y su inversa se construyen y se demuestra su composición identidad.
6. La asignación corregida es efectivamente `W(exp(Δ)u)`, definida coeficiente a
   coeficiente. Es lineal, está truncada sobre cada vector y conserva los campos
   de vacío y de carga. No se recibe esa asignación como un parámetro final.
7. Se demuestra la covarianza de la asignación completa bajo la involución. Para
   todo estado par, los coeficientes impares se anulan; por eso el descenso de
   t a z no descarta información no nula. La restricción al sector torcido
   positivo conmuta con ese descenso y recupera exactamente los campos de carga
   normalizados anteriores.
8. La evaluación de Δ sobre el estado conforme produce el término
   `(rango/16) z⁻² Id`. El coeficiente de índice `−2m−4` del campo corregido en
   t coincide con el modo conforme ya construido. El desplazamiento procede
   de esa evaluación, no de introducir la igualdad conforme como hipótesis.
9. Los estados pares actúan sobre los dos sectores de la suma directa mediante
   campos concretos en z. Se demuestran vacío, creación, inyectividad, las dos
   inclusiones y la coincidencia conforme con sus modos de Virasoro de carga
   central 24. Los bloques EE y ET quedan fijados por estas construcciones.
10. El bloque TE también se construye sobre los espacios existentes:
    `twistedEvenField : positiveSector → campos(evenSpace, positiveSector)`.
    Usa la asignación ET descendida y `D=positiveConformalMode (-1)` mediante
    la transformación formal `exp(zD) ET(u,-z)v`. Su coeficiente de grado k es
    `∑_{n≥0} (1/n!) Dⁿ((-1)^(k−n) ET(u)_(k−n)v)`. La suma es finita para cada
    coeficiente y cada par de vectores por la truncación Laurent de ET; no se
    supone que D sea localmente nilpotente. Se prueban linealidad, cota Laurent,
    coeficientes de Taylor sobre el vacío, creación e inyectividad. El ensamblaje
    `stateFieldWithTT` fija EE, ET y TE y conserva sólo TT como argumento
    explícito. Para todo ese argumento prueba vacío, creación, truncación sobre
    el vacío, inyectividad, las fórmulas de los bloques y compatibilidad conforme.
11. Sobre el factor finito efectivo `FiniteSpace o`, un espacio complejo, se
    obtiene una dualidad bilineal no degenerada e invariante para la
    representación heredada. La dimensión uno
    del espacio de morfismos equivariantes hacia la representación dual permite
    elegir un morfismo no nulo; irreducibilidad y dimensión finita lo convierten
    en un isomorfismo. La forma resultante conserva la acción del grupo y de los
    operadores reticulares. Su escala no está normalizada y aquí no se demuestra
    ni se presupone su simetría.
12. La acción conforme efectiva sobre `positiveSector o` demuestra que L₁ baja
    el peso en uno. La graduación positiva ya construida implica que `(L₁)^d`
    anula un vector de peso d y que L₁ es localmente nilpotente sobre cada
    vector. Por tanto los coeficientes `(1/n!) (L₁)^n` tienen soporte finito
    puntual y término constante identidad. Es la parte exponencial necesaria
    para la inversión contragrediente, no una afirmación de nilpotencia de L₋₁
    ni una construcción del producto TT. Estos dos precursores no sustituyen las
    identidades que deba demostrar ese producto.
13. Sobre ese mismo sector se construyen las series formales `exp(zL₁)` y
    `exp(−zL₁)` y se demuestra que son inversas por ambos lados. Se identifica
    el coeficiente de cada grado con `(1/n!) (±L₁)^n` y se prueba que ambas
    series tienen soporte finito al aplicarse a cada vector. Esta unidad formal
    no usa un corte global ni supone nilpotencia de la traslación L₋₁; tampoco
    constituye por sí sola todo el cambio contragrediente de coordenadas.
14. El signo de coordenada se construye sobre el sector positivo existente a
    partir de su descomposición en pesos conformes enteros: en peso d actúa por
    `(−1)^d`. Es involutivo, conmuta con L₀ y anticomuta con L₁. Su
    conjugación lleva `exp(zL₁)` a `exp(−zL₁)` y viceversa; el producto
    `exp(zL₁) C(signo)` tiene cuadrado identidad como serie formal. No se
    recibe el signo final como hipótesis ni se cambia de portador. Este signo
    por peso no se confunde con la involución que define el sector fijo.
15. Sobre la base monomial heredada se construye primero una forma factorial
    auxiliar, simétrica y no degenerada. El transporte de Gram utiliza la
    matriz marcada existente, el factor `−(n+1/2)` y su inverso explícito,
    sin cambiar a una base ortonormal. Resulta una forma bilineal compleja no
    degenerada en el Fock semientero, separante por ambos lados, para la cual
    el adjunto bilineal de un creador es menos el aniquilador correspondiente.
    No se afirma aquí la simetría de esta forma transportada.
16. El producto tensorial de esa forma y la dualidad finita invariante da una
    forma sobre el `Carrier` efectivo, no degenerada y separante por ambos
    lados. Conserva la adjunción semientera y es invariante bajo la aplicación
    simultánea del operador de carga a sus dos argumentos. No se presupone
    simetría del factor finito ni invariancia completa bajo campos de vértice.
17. El transporte de Gram no mezcla pesos distintos. La forma tensorial anula
    parejas de pesos diferentes y el proyector al sector fijo es autoadjunto
    respecto de ella. Su restricción a `positiveSector` es no degenerada;
    también lo son sus restricciones homogéneas, donde se construyen
    equivalencias con los duales finitos. En `weightSpace d`, d denota el peso
    oscilatorio duplicado y el peso conforme es `(d+3)/2`;
    `positiveWeightSpace d` usa directamente el peso conforme entero d. No se
    identifica el Fock infinito con todo su dual algebraico.
18. La misma construcción factorial y de Gram se aplica al Fock de frecuencias
    enteras `n+1`, sobre el mismo retículo marcado. Se construye otra forma
    bilineal no degenerada y separante por ambos lados y se demuestra de
    nuevo creador adjunto igual a menos aniquilador. No se introduce otro
    retículo ni se deduce de estas formas el producto TT.
19. Se construyen coeficientes contragredientes efectivos con valores en el
    dual algebraico del sector par. Si v tiene peso conforme d, su evaluación
    sobre w del sector positivo y a del sector par es
    `(−1)^d ∑_{0≤j<d} B₊(w, TE((L₁)^j v/j!)_(j−2d−k) a)`.
    La suma conserva su valor con cualquier corte N≥d porque los términos
    posteriores se anulan. La descomposición interna por pesos extiende esta
    fórmula linealmente al portador completo. El codominio demostrado es
    `Module.Dual ℂ (evenSpace o)`: no se afirma representabilidad por un
    vector de `evenSpace`, truncación Laurent de un campo TT ni Jacobi para TT.

Todas estas formas son bilineales complejas, no productos hermíticos ni
formas positivas definidas. «Sector positivo» significa aquí sector fijo de
la involución. La simetría de la forma factorial auxiliar no se promueve a
simetría de las formas finita, tensorial o restringida; tampoco se afirma en
estos ingredientes la adjunción de todos los modos conformes.

La fuente `LatticeTwistedStateField.lean` reúne la asignación corregida;
`LatticeTwistedPositiveStateDescent.lean` reúne su restricción y descenso;
`LatticeTwistedStateConformal.lean` demuestra el enlace conforme. Las fuentes
de sus dependencias y los recibos de compilación se conservan junto a ellas.
`LatticeOrbifoldEvenAction.lean` y `LatticeOrbifoldEvenConformal.lean` consumen
estos campos en la suma directa y prueban las compatibilidades indicadas.
`SkewFieldTransform.lean` demuestra la transformación formal con finitud puntual;
`LatticeTwistedEvenProduct.lean` la aplica al ET efectivo, construye TE y reúne
el ensamblaje cuyo único bloque todavía parametrizado es TT.
`LatticeFiniteInvariantPairing.lean` contiene la dualidad del factor finito;
`LatticeTwistedContragredientTruncation.lean` demuestra la nilpotencia local del
L₁ efectivo y la finitud puntual de sus coeficientes exponenciales.
`LatticeTwistedCoordinateExponential.lean` reúne las exponenciales de ambos
signos, su inversión bilateral y su finitud puntual.
`CoordinateWeightSign.lean`, `LatticeTwistedWeightSignLaws.lean`,
`LatticeTwistedCoordinateSign.lean` y `LatticeTwistedCoordinateConjugation.lean`
construyen el signo efectivo y sus leyes, incluida la conjugación exponencial.
`WeightedBasisPairing.lean`, `LatticeFactorialPairing.lean`,
`LatticeHalfGramTransport.lean` y `LatticeHalfFockPairing.lean` construyen la
forma semientera desde la base y la matriz de Gram heredadas;
`LatticeTwistedTensorPairing.lean` la lleva al tensor efectivo.
`LatticeHalfGramWeight.lean` y `LatticeTwistedPairingGrading.lean` demuestran
las propiedades de peso y las restricciones no degeneradas.
`LatticeIntegerFockPairing.lean` realiza la construcción de frecuencia entera.
`LatticeTwistedContragredientCoefficients.lean` construye los coeficientes con
valores en el dual y demuestra la estabilidad del corte y la extensión lineal.

## Qué comprueba Lean y qué conserva la entrega

La reproducción sigue las dependencias existentes: campos exponenciales →
normalización → productos normales y corrección → campos de todos los estados →
involución, descenso y campo conforme → producto TE. No se reinicia la
construcción de K. Cada recibo identifica fuentes, importaciones, objetos
compilados y la consulta de axiomas de todas las declaraciones públicas nuevas.
Los únicos axiomas admitidos en estas nuevas declaraciones son `propext`,
`Classical.choice` y `Quot.sound`; no se añaden axiomas de FLM, de localidad o
de Moonshine.

El antecedente se conserva una sola vez, sin editar sus fuentes ni sus PDF.
La compilación incremental reutiliza sus objetos autenticados. La carpeta
desplegada y el ZIP contienen los mismos archivos; el README de reproducción
indica la orden explícita y el runtime requerido. No hay ejecución automática
al conectar un USB. El control de conservación de archivos, la revisión por
lectura y la comprobación de Lean son evidencias diferentes. El README anterior
se conserva; este sucesor actualiza el alcance de TE y de los ingredientes
contragredientes expresamente descritos.

El corte anterior de 443 módulos permanece sellado e intacto. Este sucesor
reutiliza la base de 406 módulos y los mismos recibos de normalización,
continuación y descendientes; el recibo terminal TE reúne los cuatro módulos
terminales anteriores, los dos propietarios de TE y los dos precursores de TT
con sus ingredientes adicionales descritos aquí. El recibo terminal de los
443 módulos y su README se conservan como historia, junto con todas las fuentes
demostrativas. Esta continuidad no declara cerrado el artículo I completo.

## Relación exacta con la prolongación hasta Moonshine

No se atribuye una nueva prioridad al álgebra de operadores de vértice ni a la
construcción clásica de Frenkel–Lepowsky–Meurman. Aquí se materializa su familia
de campos torcidos sobre el portador reticular heredado, incluidos todos sus
estados oscilatorios, la corrección, la compatibilidad conforme y el producto TE.

Este resultado no se rotula como una prueba Lean de la identidad de Jacobi
torcida completa ni de las compatibilidades mixtas completas. TT permanece
como argumento del ensamblaje, no como un producto construido ni sustituido
por cero. Tampoco se afirma `Aut(V♮)=Monster` ni el teorema de Moonshine. El
LaTeX que compone los teoremas clásicos conserva su contenido; esa composición
documental no es un teorema importado en Lean. Las identidades que aquí sí están
demostradas se conservan íntegramente y no se vuelven a tratar como ausentes.

## Continuidad para la siguiente ejecución

Se empieza por los recibos compilados y el grafo de importaciones, no por una
nueva auditoría de K, Hadamard, Witt, Golay o Leech. No se repiten las pruebas
selladas. Cualquier ampliación consume estas asignaciones concretas; no debe
volver a pedir como dato la corrección, el descenso, la igualdad conforme o el
bloque TE que ya están construidos. El siguiente producto que se incorpore ha
de conservar sus dominios y codominios y demostrar sus identidades, sin
introducirlas como hipótesis bajo un nombre nuevo.
