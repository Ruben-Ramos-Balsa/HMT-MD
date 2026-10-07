# Procedencia y autonomía: Fock graduado, Pauli y composición

Fecha: 10 de septiembre de 2026.
Archivo propio: `sections/13_fock_pauli_composicion.tex`.
Destino: Artículo VI, sin modificación de las demás fuentes y sin compilación.

## Operación realizada

Se reúnen las definiciones y pruebas finitas que necesita VI para utilizar
Fock, CAR/CCR, Pauli y los proyectores de intercambio. La construcción
empieza en los canales APP–TRIT–TPK ya realizados, conserva las etiquetas
y declara el carácter de paridad y su regla de intercambio. No introduce
un Hamiltoniano o una energía convencional como generador de la ocupación.

La redacción despliega las pruebas que los propietarios presentan de forma
breve: promedios de permutación, base de ocupación normalizada, signos de
inserción exterior, factores de creación simétrica, dominios y transporte.
No se reclama una nueva teoría de estadística. Las construcciones matrices
y el control de frontera del corte bosónico son explicitaciones
matemáticas; no se les atribuye prioridad conceptual HMT nueva.

## Propietarios leídos completos

Raíces de procedencia:

- **M** = `/Users/ruben/Documents/New project/PUBLICACION_HMT/TEORIA_HOLOGRAFICA_INTEGRAL_MASA_HMT_MD_REV2_2026-08-20`.
- **F** = `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente`.
- **V** = `/Users/ruben/Documents/New project/output/ARTICULO_V_ESTADISTICA_CUANTICA_RADIACION_20260910`.

1. `M/fuente/modulos/11_ontologia_cuantica_de_la_particula.md`, completo,
   518 líneas. Especialmente «Espín y cierre de orientación», «Estadística
   y ocupación», «Compuesto», «Majorana» y «Anyón». Conserva la diferencia
   entre signo de retorno, grado de espín, representación y estadística.
2. `F/manuscrito/sections/md/delta_127/04b_completaciones_cuanticas.tex`,
   completo, 334 líneas. Núcleo propietario de espacio de canales,
   cociente tensorial graduado, CAR, exclusión, 2π/4π y censos de ocupación.
3. `F/manuscrito/integracion_83/parte_iv/body/B015_ch56_pauli_completacion_fermionica_7549b83967f5_04d_ocupacion_estadistica.tex`,
   completo, 48 líneas. Prueba de idempotencia una vez dadas las CAR.
   La nueva sección conserva esa prueba pero construye antes las CAR.
4. `F/manuscrito/sucesor_102/deltas_masas/realizacion_equivariante_especies_operadores_masicos_publico.tex`,
   completo en la tarea previa de este mismo agente; reutilizado sin
   cambio. El cuerpo de Fock reside en líneas 856–906: morfismos
   contractivos, functorialidad, CAR/CCR y límite de la identificación
   relativista. La composición se sitúa en líneas 786–825.
5. `V/manuscrito/sections/20_completaciones_cuanticas.tex`, completo,
   354 líneas; recuperación del propietario delta_127 con etiquetas de V.
6. `V/manuscrito/sections/30_fock_gibbs.tex`, completo, 90 líneas;
   recuperación de Fock y Gibbs del propietario de realización.
7. `V/manuscrito/sections/40_exclusion_pauli.tex`, completo, 55 líneas;
   recuperación de la prueba de ocupación.

Coordinación local leída para evitar duplicaciones:

- VI `sections/10_sectores_topologicos.tex`, completo, 234 líneas.
  Se conserva su prueba de generadores reales de CAR y no se reproduce
  en 13 la discusión de Majorana/Clifford/Ising.
- VI `sections/03_conjugacion_mobius.tex`, redactada y leída por este
  agente en la tarea anterior; sus retornos y su representación
  espinorial son antecedentes, no se reescriben.
- VI `sections/08_familias_y_compuestos.tex`, redactada y verificada en
  la tarea anterior; la gramática, el cociclo, los singletes y Feshbach
  permanecen allí. 13 añade únicamente la compatibilidad estadística.

El Artículo V figura en `CORPUS_ACTIVO.md` como borrador integrado de 142
páginas. Se consultaron sus fuentes, no se infirió contenido sólo de su
PDF o de la paginación del índice.

## Cierre de dependencias incorporado

| Resultado | Construcción y prueba en 13 | Procedencia y alcance |
|---|---|---|
| Espacio de canales | Suma finita de multiplicidades de representación, base ortonormal | Delta_127 y REV2 11; los canales ya están producidos, no son masas seleccionadas |
| Graduación | Carácter aditivo `p`, involución `J_p`, proyectores `(I±J_p)/2` | Delta_127; la realización del carácter es dato explícito |
| Intercambio | Signo `(-1)^(p(v)p(w))` y relaciones de Coxeter | Despliegue de la simetría graduada del propietario |
| Simetrización | Promedios sobre `S_n`, autoadjunción e idempotencia | Construcción finita explícita de Sym/Exterior |
| Fock graduado | Cociente tensorial y base de monomios; suma por grados | Delta_127/V20, explicitado |
| CAR | Fórmulas de inserción/retirada con signo de orden y prueba en cada subconjunto | Propietario exterior; sin postular CAR como dato nuevo |
| Pauli | `N_j^2=N_j`, espectro 0/1 | Propietario Pauli y REV2, con CAR previamente construidas |
| CCR | Creación/aniquilación con raíces de ocupación sobre `D_fin` | Completación simétrica del propietario, dominio explicitado |
| Corte finito bosónico | `I−(N+1)|N><N|` en el conmutador truncado | Control negativo exacto; no modifica CCR en Fock completo |
| Modo completo | Norma Gram de `u∧v`; etiquetas y hojas preservadas | Explicitación de las multiplicidades del corpus |
| Censos | Binomios exterior/simétrico por bases | Delta_127/V20, con demostración combinatoria |
| Refinamiento | Potencias tensoriales, promedios y `Γ(T)` | Propietario integral 856–906; contractividad conservada |
| Composición estadística | Descenso por entrelazador de interfaz y promedios finitos | Composición del corpus; el cuadrado se afirma bajo su covariancia explícita |
| Pauli bariónico | Signo cromático por signo de la parte espín/sabor/orbital/hoja | Consecuencia del singlete de 08, no nueva definición del barión |
| Observable material | `dΓ_n(B)` y dominio de suma directa | Aplicación de un operador ya construido, no ley de masa ligada por suma |

## Delimitaciones conservadas en el cuerpo

1. Una monodromía de signo no basta por sí sola para deducir CAR:
   se declaran espacio graduado y cociente de intercambio y se prueban
   las CAR de esa completación. La compatibilidad con rotaciones y el
   teorema relativista de espín–estadística conservan sus condiciones.
2. Hoja suma/producto no se sustituye verbalmente por bosón/fermión.
   La regla emplea el carácter de paridad de transporte realizado.
3. El vacío de Fock de grado cero no se identifica con una vacancia
   TPK ni con la estructura constitutiva del vacío electromagnético.
4. Una masa, una celda o una firma reducida común no identifican el modo
   completo. Dos componentes ortogonales de espín/hoja pueden ocuparse
   simultáneamente sin violar Pauli.
5. Una suma de ocupaciones degeneradas no es un proyector, aunque cada
   ocupación elemental sí lo sea.
6. CCR exactas viven sobre un dominio denso de Fock; un corte matricial
   duro conserva un defecto terminal explícito. No se expide un PASS
   falso de CCR sin ese término de frontera.
7. Contractividad basta para la segunda cuantización acotada; en el
   exterior finito es innecesaria porque hay un número finito de grados.
   En bosones, `T=2I` da un ejemplo no acotado.
8. La creación es natural para aplicaciones lineales graduadas en
   partículas finitas; el entrelazamiento de la aniquilación con la
   misma norma requiere isometría. No se confunde contracción con unitario.
9. El producto de proyectores físicos representa la intersección cuando
   conmutan. Sin esa condición se construye el subespacio común o el
   orden físico de las operaciones.
10. Fock no reemplaza al registro de ligadura. `dΓ(B)` es el observable
    aditivo de canales independientes, no una prueba de que una masa
    compuesta sea suma de masas aisladas.
11. Los sectores trenzados no reducibles a permutaciones conservan su
    codominio en 10; no se fuerzan dentro de Sym/Exterior.

## Posición sugerida en VI y referencias

El nombre de archivo 13 responde al reparto de tareas, no impone el orden
lógico del artículo. Conviene incluir esta sección después de los canales,
el transporte y el operador de una partícula (03–05), antes de las
aplicaciones de Pauli en familias/compuestos y de los generadores reales de
10. Algunas referencias a las aplicaciones posteriores serán prospectivas
y permanecerán como referencias internas ordinarias.

Entrada principal: `vi:sec:fock-pauli`.
Resultados principales:

- `vi:thm:fock-graduado`;
- `vi:thm:car-construidas` y `vi:cor:pauli-ocupacion`;
- `vi:thm:ccr-construidas` y `vi:prop:corte-bosonico`;
- `vi:prop:pauli-gram`, `vi:prop:censo-fock`;
- `vi:thm:fock-naturalidad`;
- `vi:prop:composicion-estadistica`.

Dependencias citadas por etiquetas existentes:
`vi:sec:conjugacion`, `vi:prop:car-real`, `vi:sec:topologia`,
`vi:subsec:composicion-registro`, `vi:prop:singlete-barion`,
`vi:sec:familias-compuestos`, `vi:subsec:resonancias-familias`.

No se han introducido claves bibliográficas nuevas. El historial de
Pauli/Dirac está en el propietario, pero esta sección no formula una
afirmación de prioridad histórica ni necesita una cita para reemplazar
las pruebas contenidas. El ensamblador conserva la bibliografía común.

## Controles finitos reproducibles

El verificador materializado y vigente es
`technical/verificar_fock_pauli.py`; su recibo de ejecución es
`technical/RECIBO_FOCK_PAULI.json`. Se ejecuta con Python estándar, sin
paquetes, metrología ni valores objetivo. Los límites finitos figuran en
el código y en el recibo. Las pruebas generales residen en LaTeX; el
programa comprueba realizaciones finitas y controles negativos.

El código abreviado que sigue se conserva únicamente como antecedente de
la primera ejecución. El archivo materializado lo sustituye para la
reproducción de la entrega: utiliza comprobaciones explícitas, rechaza
`-O` y `-OO` y registra las huellas de su fuente y de la sección 13.

```python
from itertools import product, combinations, combinations_with_replacement
from math import comb

def op(mask, j, creation):
    present = bool(mask & (1 << j))
    if present == creation:
        return None
    sign = -1 if bin(mask & ((1 << j) - 1)).count('1') % 2 else 1
    return mask ^ (1 << j), sign

def compose(mask, first_j, first_creation, second_j, second_creation):
    a = op(mask, first_j, first_creation)
    if a is None:
        return {}
    b = op(a[0], second_j, second_creation)
    if b is None:
        return {}
    return {b[0]: a[1] * b[1]}

def add(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, 0) + v
    return {k: v for k, v in c.items() if v}

car_checks = 0
for d in range(1, 8):
    for mask in range(1 << d):
        for i in range(d):
            for j in range(d):
                for left_creation, right_creation in product([False, True], repeat=2):
                    # a_i a_j^* + a_j^* a_i, and the three companion cases.
                    a = compose(mask, j, right_creation, i, left_creation)
                    b = compose(mask, i, left_creation, j, right_creation)
                    expected = {mask: 1} if i == j and left_creation != right_creation else {}
                    assert add(a, b) == expected
                    car_checks += 1
            number = compose(mask, i, False, i, True)
            assert number == ({mask: 1} if mask & (1 << i) else {})

coxeter_checks = 0
def swap(state, i):
    terms, sign = state
    a, b = terms[i], terms[i+1]
    result = list(terms)
    result[i], result[i+1] = b, a
    return tuple(result), sign * (-1 if a[1] * b[1] else 1)

for parity in product([0, 1], repeat=3):
    state = (tuple(enumerate(parity)), 1)
    assert swap(swap(state, 0), 0) == state
    left = swap(swap(swap(state, 0), 1), 0)
    right = swap(swap(swap(state, 1), 0), 1)
    assert left == right
    coxeter_checks += 2

census_checks = 0
for d in range(1, 7):
    for n in range(0, 8):
        fermion = sum(1 for _ in combinations(range(d), n))
        boson = sum(1 for _ in combinations_with_replacement(range(d), n))
        assert fermion == (comb(d, n) if n <= d else 0)
        assert boson == comb(d+n-1, n)
        census_checks += 2

# The products of square-root coefficients in the normalized basis are
# integers m+1 and m, so the commutator can be tested exactly with integers.
boundary_checks = 0
for N in range(0, 33):
    diagonal = []
    for m in range(N+1):
        creation_then_annihilation = (m+1) if m < N else 0
        annihilation_then_creation = m
        result = creation_then_annihilation - annihilation_then_creation
        assert result == 1 - ((N+1) if m == N else 0)
        diagonal.append(result)
        boundary_checks += 1
    assert sum(diagonal) == 0  # Trace of a finite commutator.
    assert diagonal[-1] != 1  # Negative control: exact CCR cannot hold at the cut.

print({
    'CAR_on_1_to_7_modes': car_checks,
    'graded_Coxeter_checks': coxeter_checks,
    'dimension_checks': census_checks,
    'bosonic_boundary_checks': boundary_checks,
    'result': 'PASS_FINITE_FOCK_PAULI_NOT_PHYSICAL_CERTIFICATION',
})
```

El programa verifica CAR y la acción de número sobre todas las ocupaciones
de 1 a 7 modos, las relaciones graduadas de tres factores, los censos
hasta 6 modos/7 partículas y el defecto del corte bosónico hasta N=32.
No certifica un límite dinámico, la localidad relativista o la selección
física de una representación a partir de un nombre de partícula.

### Ejecución conservada

Comando vigente de reproducción desde la raíz de VI:

```bash
python3 -I -S technical/verificar_fock_pauli.py --receipt technical/RECIBO_FOCK_PAULI.json
```

La ejecución del archivo materializado produjo 44.249 controles satisfactorios:

```text
CAR: 38888
Coxeter: 16
numero_fermionico: 1538
Pauli_idempotencia: 1538
Pauli_doble_creacion: 1538
censos: 96
frontera_bosonica: 561
traza_conmutador_finito: 33
negativo_CCR_sin_frontera: 33
negativo_omision_signo_exterior: 1
negativo_numero_degenerado_no_proyector: 1
dominios_rechazados: 5
negativo_Python_O: 1
PASS_FINITE_FOCK_PAULI_NOT_PHYSICAL_CERTIFICATION
```

La prueba de optimización se ejecuta en un subproceso aislado y exige
salida 2 con `RECHAZADO_OPTIMIZACION`, sin publicar un PASS. El producto
de las dos amplitudes bosónicas se calcula mediante sus cuadrados
enteros iguales; no se usan raíces aproximadas. El recibo conserva los
límites comprobados y excluye expresamente una certificación de
localidad, límite dinámico o identificación física.

La errata de la línea 185 (`quad` sin barra) se corrigió a `\quad`.
Se revisó asimismo completo el cierre de la sección: dominio de suma
directa de `dΓ(B)`, distinción entre observables aditivos y operadores
de compuestos ligados, y condiciones de la realización espín–estadística.
No se alteraron los enunciados ni sus condiciones.

Control estático adicional del archivo LaTeX: 642 líneas, 3175 palabras
por separación de espacios, 30 etiquetas propias únicas, 11 pruebas y
20 referencias resueltas en las fuentes locales de VI. Los entornos están
equilibrados y no hay colisión de etiquetas con las demás secciones.
No se ha compilado ni modificado el PDF o el archivo maestro.
