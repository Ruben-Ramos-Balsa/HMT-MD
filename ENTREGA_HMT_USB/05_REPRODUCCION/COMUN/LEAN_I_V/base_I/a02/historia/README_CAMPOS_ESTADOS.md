# Artículo I: campos de estados en la prolongación reticular torcida

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
9. Los estados pares actúan ahora sobre los dos sectores de la suma directa
   mediante campos concretos en z. Se demuestran vacío, creación, inyectividad,
   las dos inclusiones y la coincidencia conforme con sus modos de Virasoro
   de carga central 24. En el ensamblaje posterior, ET ya queda fijado por
   esta construcción: sólo los productos con fuente torcida TE y TT siguen
   siendo argumentos del adaptador, sin sustituirlos por cero.

La fuente `LatticeTwistedStateField.lean` reúne la asignación corregida;
`LatticeTwistedPositiveStateDescent.lean` reúne su restricción y descenso;
`LatticeTwistedStateConformal.lean` demuestra el enlace conforme. Las fuentes
de sus dependencias y los recibos de compilación se conservan junto a ellas.
`LatticeOrbifoldEvenAction.lean` y `LatticeOrbifoldEvenConformal.lean` consumen
estos campos en la suma directa y prueban las compatibilidades indicadas.

## Qué comprueba Lean y qué conserva la entrega

La reproducción sigue las dependencias existentes: campos exponenciales →
normalización → productos normales y corrección → campos de todos los estados →
involución, descenso y campo conforme. No se reinicia la construcción de K.
Cada recibo identifica fuentes, importaciones, objetos compilados y la consulta
de axiomas de todas las declaraciones públicas nuevas. Los únicos axiomas
admitidos en estas nuevas declaraciones son `propext`, `Classical.choice` y
`Quot.sound`; no se añaden axiomas de FLM, de localidad o de Moonshine.

El antecedente se conserva una sola vez, sin editar sus fuentes ni sus PDF.
La compilación incremental reutiliza sus objetos autenticados. La carpeta
desplegada y el ZIP contienen los mismos archivos; el README de reproducción
indica la orden explícita y el runtime requerido. No hay ejecución automática
al conectar un USB. El control de conservación de archivos, la revisión por
lectura y la comprobación de Lean son evidencias diferentes.

## Relación exacta con la prolongación hasta Moonshine

No se atribuye una nueva prioridad al álgebra de operadores de vértice ni a la
construcción clásica de Frenkel–Lepowsky–Meurman. Aquí se materializa su familia
de campos torcidos sobre el portador reticular heredado, incluidos todos sus
estados oscilatorios, la corrección y la compatibilidad conforme.

Este resultado no se rotula como una prueba Lean de la identidad de Jacobi
torcida completa, de todos los productos entre los dos sectores del orbifold,
ni de `Aut(V♮)=Monster` o del teorema de Moonshine. El LaTeX que compone los
teoremas clásicos conserva su contenido; esa composición documental no es un
teorema importado en Lean. Las identidades que aquí sí están demostradas se
conservan íntegramente y no se vuelven a tratar como ausentes.

## Continuidad para la siguiente ejecución

Se empieza por los recibos compilados y el grafo de importaciones, no por una
nueva auditoría de K, Hadamard, Witt, Golay o Leech. No se repiten las pruebas
selladas. Cualquier ampliación consume estas asignaciones concretas; no debe
volver a pedir como dato la corrección, el descenso o la igualdad conforme que
ya están construidos. El siguiente producto que se incorpore ha de conservar
sus dominios y codominios y demostrar sus identidades, sin introducirlas como
hipótesis bajo un nombre nuevo.
