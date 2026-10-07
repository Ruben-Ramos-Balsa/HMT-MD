# Procedencia y cierre focal de los cuerpos de partícula, conjugación y órbita

Fecha: 10 de septiembre de 2026. Documento de trabajo para el ensamblador de VI.
No sustituye las demostraciones incluidas en el cuerpo. No modifica I–V, el
integral ni la monografía de masas.

## Alcance de la intervención

Se redactan tres cuerpos nuevos de exposición, con resultados recuperados de
los propietarios indicados. No se presentan como descubrimientos del agente:

- `sections/02_particula_persistencia.tex`: extensión, historia, sección,
  equivalencia material, multisección y selector equivariante.
- `sections/03_conjugacion_mobius.tex`: conjugación de registro y antisección,
  covariancia de masa, línea de signo, retículo bidireccional y representación
  espinorial electrónica con helicidad.
- `sections/06_kepler_sommerfeld.tex`: flujo, realización central, leyes
  orbitales, cubierta y fase semiclásica.

La organización es definición → operación → prueba → significado. La
formalización de las pruebas de equivalencia, paridad y transporte desarrolla
las operaciones de los propietarios sin atribuirles un resultado físico más
fuerte. No se introduce un catálogo de masas, un espectro atómico ni una nueva
identificación de la antipartícula. No se cambia el título de VI.

## Raíces de procedencia

**F, integral activo de la serie (2.249 páginas):**

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/`

**M, masas REV.2 (479 páginas):**

`/Users/ruben/Documents/New project/PUBLICACION_HMT/TEORIA_HOLOGRAFICA_INTEGRAL_MASA_HMT_MD_REV2_2026-08-20/`

**I, delta electrónico de helicidad:**

`/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910/`

Las páginas que siguen son las impresas según los índices de compilación de
las ediciones consultadas, no una nueva revisión visual de esos PDFs.

## Matriz de propietarios y disposición

| ID | Resultado/estructura conservada | Propietario y localizador | Destino VI y disposición |
|---|---|---|---|
| P1 | Sistema inverso, sombra de ruta, sección compatible | `F/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex`, líneas 1–52; integral §94.4.1, pp. 1565–1571 | 02, `vi:subsec:extension-persistente`; conservación y prueba desplegada de naturalidad |
| P2 | Identidad por equivalencia eventual de simetrías compatibles | `F/manuscrito/integracion_83/masas_p0/tex/fragmentos/75_rev2_ontologia_particula.tex`, líneas 14–56; §94.5.1.2, pp. 1572–1573 | 02, `vi:subsec:identidad-material`; definición y prueba explícita de equivalencia |
| P3 | Diferencia estado/historia/realización | `M/fuente/modulos/11_ontologia_cuantica_de_la_particula.md`, líneas 3–74; §§2.2.1–2.2.2, pp. 55–56 | 02, entrada y definición de partícula; explicación ampliada |
| P4 | Multisecciones, mapa celular, centro fijo y obstrucción al selector | `F/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex`, líneas 54–158 | 02, `vi:subsec:especie-fibra`; prueba del selector incluida; censo completo en dependencia atlas |
| P5 | Estratificación extensión/ruta/registro/firma/carácter/torres | Mismo propietario, líneas 199–240; `M/fuente/modulos/11_ontologia_cuantica_de_la_particula.md`, secciones Partícula y Medición | 02, `vi:subsec:particula-observable`; exposición, sin sustituir las fórmulas del operador másico que reúne el editor |
| C1 | C_M, funcionales lineales impares y memoria cuadrática par | `F/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex`, líneas 242–255 | 03, `vi:prop:paridad-registro`; prueba por cambio de índices |
| C2 | Levantamiento a secciones y preservación de restricciones | Mismo propietario, líneas 258–267; `M/fuente/modulos/11_ontologia_cuantica_de_la_particula.md`, líneas 76–119 | 03, `vi:prop:antiseccion-persistente`; declaración del dominio estable y de las simetrías transportadas |
| C3 | Igualdad de masa por covariancia, no por paridad aislada | `M/fuente/modulos/11_ontologia_cuantica_de_la_particula.md`, líneas 93–102; `F/manuscrito/integracion_83/masas_p0/tex/fragmentos/75_rev2_ontologia_particula.tex`, líneas 59–89 | 03, `vi:prop:masa-conjugada` y `vi:eq:banda-paridad`; dominio autoadjunto y transporte explícitos |
| C4 | Lazo, carácter de signo, banda de Möbius y retorno de memoria | `F/manuscrito/sections/md/21_persistencia_ruta_mobius_familias_actualizada.tex`, líneas 269–304; `M/fuente/modulos/18_cuantica_estadistica_y_termodinamica.md`, desde línea 104, §2.12.5, p. 100 | 03, `vi:thm:retorno-mobius`; prueba del signo y explicación condicionada 108/216 |
| C5 | Descomposición par/impar y cero de una sección de la línea real | Propietario 21, líneas 306–338 | 03, `vi:prop:observables-paridad`; prueba por transición y valor intermedio |
| C6 | Retículo W_±, índice 12 y conjugación de canales | Propietario 21, líneas 294–302 y 403–435 | 03, `vi:prop:indice-bidireccional` y `vi:eq:conjugacion-canales`; inversión entera y dominio a>|b| incluidos |
| C7 | Álgebra electrónica P,Q,S,J | `I/sections/electron.tex`, apartado Álgebra del bloque electrónico local, líneas 267–298; construcción precedente del prefactor, líneas 136–266 | 03, `vi:eq:bloque-electronico`; antecedente APP tridimensional debe incorporarse materialmente por main |
| C8 | Terna hermítica, representación de espín 1/2, helicidad y tipos de inversión | `I/sections/helicidad_electron.tex`, líneas 1–186; I §7.3, pp. 85–87 | 03, `vi:prop:spin`, `vi:prop:helicidad`; pruebas esenciales completas y narración conservada |
| K1 | Gauss finito y conteo de enlaces cúbicos | `F/manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/09_sommerfeld_kepler.tex`, líneas 14–70; integral §67.1.1, p. 1181 | 06, `vi:thm:gauss`; dominio, orientación e isotropía separados |
| K2 | Lagrangiano, cónica y leyes de área/periodo | Mismo propietario, líneas 72–155; §§67.1.2, pp. 1182–1183 | 06, `vi:prop:conica`, `vi:prop:ley-areal`; Binet y eliminación de semiejes desarrolladas |
| K3 | Cubierta q=z² frente a banda orbital | Mismo propietario, líneas 157–204; §67.1.3, p. 1183 | 06, `vi:subsec:cubierta-orbital`; tipos de fibra y ley de transporte conservados |
| K4 | Fase de Sommerfeld y desplazamiento semientero | Mismo propietario, líneas 206–270; §67.1.4, pp. 1183–1184 | 06, `vi:thm:sommerfeld`; condición semiclásica, holonomía y observación Maslov conservadas |

Los propietarios 21, 75_rev2, 09_sommerfeld, el delta I de helicidad y los
módulos 11 y 18 de M se leyeron completos. La residencia de P,Q en
`I/sections/electron.tex` se consultó focalmente; su construcción previa
completa corresponde a la dependencia material que debe reunir el editor.

## Dependencias que el ensamblaje debe incorporar dentro de VI

1. **Núcleo formal común:** APP, TRIT y TPK; dominio admisible; prolongación;
   memoria; restricciones; conexión/holonomía nonádica. Se conserva la fuente
   común idéntica de la serie. Nuestros tres cuerpos la reciben como
   construcción precedente, no la reemplazan por las fórmulas de límite.
2. **Atlas completo y registro de rutas:** lector celular pi_81, funciones de
   familia y nivel, estabilidad bajo rho_c, censo 81/56/13/324 y asignación
   central. Los números mencionados en 02 orientan la ontología, pero no son
   una prueba nueva del censo. Propietarios: el ensamblador
   `F/manuscrito/integracion_83/parte_iv/chapters/75_definicion_particula.tex`
   y sus inputs; el desarrollo de atlas de la monografía M.
3. **Lectores K_D/K_Ω y operador de masa:** el cuerpo dedicado a masa debe
   conservar sus fórmulas, dominios, compresión, torres y condiciones de
   escalaridad. Propietario de ensamblaje:
   `F/manuscrito/integracion_83/parte_iv/chapters/73_lectores_bidireccionales_masa.tex`.
   La proposición de covariancia de 03 transmite un operador ya construido;
   no selecciona una especie ni reemplaza el operador.
4. **P,Q desde APP tridimensional:** incluir la construcción de las esperanzas
   condicionales, sus fibras, matriz de incidencia, modo trítico y plano
   principal que anteceden al bloque de `I/sections/electron.tex`. Mostrar
   únicamente las matrices P,Q no satisface esa dependencia. La sección 03
   sí contiene, después, las multiplicaciones y pruebas espinoriales.
5. **Constantes internas y par angular:** las regiones y lecturas de pi, phi,
   e, alfa; registro dodecafásico; A y C*; q_± y su normalización. Estos son
   antecedentes internos de la realización, nunca objetivos de entrada.
6. **Constante reducida de Planck y carta de acción:** recuperar las
   construcciones del Artículo II vigente, REV09. En 06, hbar_int es un dato
   posterior de esa salida, expresado en la recta de la acción del ciclo.
   El teorema de Sommerfeld no se ofrece como otra derivación de hbar.
7. **Realización orbital particular:** antes de identificar una fuerza o un
   espectro físico, deben estar fijados el mapa de la ruta a la carta
   métrica, la isotropía del lector, la masa reducida y el acoplamiento
   dimensional, el lagrangiano central y la línea de fase. El propietario
   09_sommerfeld establece sus resultados con estos datos explícitos. El
   texto de 06 conserva ese alcance; no declara que Gauss determine por sí
   solo el potencial o que la holonomía seleccione el Hamiltoniano.

No se proponen aquí nuevas ausencias matemáticas. Se enumeran residencias
que deben quedar materialmente incluidas o desarrolladas por el ensamblador
para que las dependencias del artículo sean públicas y autónomas.

## Labels e integración

Entradas: `vi:sec:particula`, `vi:sec:conjugacion`, `vi:sec:kepler`.
Todas las etiquetas introducidas llevan `vi:`. Los tres archivos sólo
contienen cruces entre sus etiquetas propias; no presuponen nombres de
etiquetas que otro editor todavía no haya fijado. Las dependencias
anteriores se nombran en prosa y en este documento para su inclusión por
main. El texto requiere `amsmath`, `amssymb` y entornos de teorema, definición,
proposición y demostración ya utilizados por los artículos anteriores.
No incorpora paquetes, macros globales ni cambios de estilos.

En el montaje pueden existir pruebas duplicadas de la terna y la helicidad
si se incluye literalmente todo el capítulo electrónico I. La decisión
editorial debe conservar la derivación APP de P,Q y una residencia completa
de la prueba de helicidad; no eliminar ninguna dependencia para suprimir
una mera repetición. No se han editado las fuentes I.

## Diferencias de representación que se preservan

- Ruta observable ≠ clase de sección persistente; el lector puede perder
  información y su reversibilidad no se supone.
- Inversión celular rho_c ≠ conjugación dodecafásica C_M ≠ levantamiento a
  antisección; se exige el mapa pertinente para componerlas.
- Palabra electrónica fija bajo C_M ≠ carga nula; el estado conserva el
  factor de hoja y la representación de carga.
- Paridad de un funcional ≠ invariancia de la masa completa; esta última
  usa covariancia del operador y de su dominio.
- Banda real de Möbius ≠ cubierta q=z² ≠ representación espinorial. Comparten
  algunos órdenes de retorno con tipos y acciones distintos.
- Cierre de orientación ≠ reinicio de la memoria nonádica.
- Elipse de configuración de Kepler ≠ elipse de acción; su comparación
  conserva el mapa de realización.
- Condición semiclásica de cierre ≠ espectro atómico exacto. Se mantienen
  Hamiltoniano, ciclos, normalizaciones e índices de Maslov cuando proceden.

## Estado de los controles

El núcleo formal permanente y la autocomprobación del control de constantes
devuelven PASS en esta intervención. No se reutiliza ese resultado como
certificación matemática de VI. El gate global de arranque conserva la
discrepancia de huella del índice humano ya comunicada al editor; no se ha
alterado ese índice ni ningún manifiesto sellado.

Este aporte es fuente de trabajo: no hay compilación, PDF ni revisión visual
de VI realizada por este agente. El editor único completa la integración,
los recibos causales del artículo y las verificaciones de la entrega.

### Controles focales ejecutados

- 72 etiquetas `vi:` y 38 referencias internas: ninguna etiqueta duplicada ni
  referencia interna sin destino; entornos LaTeX equilibrados. Hay 16 pruebas
  explícitas (3 en 02, 8 en 03, 5 en 06).
- Involutividad de C_M, paridad lineal simétrica y correlación cuadrática
  cíclica: comprobadas sobre las 531.441 palabras del **ambiente** trítico
  de longitud 12. Este ambiente no se declara igual al dominio admisible.
- Inversa del retículo W_±: 201 puntos de imagen en el cuadrado [-24,24]^2.
- Productos de las tres matrices de Pauli: comprobación exacta.
- Identidades de energía elíptica y periodo: 24 casos racionales exactos.

Estos controles son locales y complementan las pruebas escritas. No
certifican el selector de especies, un transductor físico o todo el artículo.
No usan valores físicos objetivo.

El script material `technical/verificar_particula_mobius_kepler.py` añade
11 controles negativos o de dominio y se ha ejecutado en modo completo.
Su recibo `technical/RECIBO_PARTICULA_MOBIUS_KEPLER.json` conserva el modo,
los censos comprobados, las huellas de los tres cuerpos y del propio
script, y el alcance no comprobado. Su estado es
`PASS_FOCAL_PARTICULA_MOBIUS_KEPLER`; no es un artefacto sellado ni un
recibo causal global de VI.

Comando reproducible desde cualquier directorio:

```bash
python3 -I -S "/Users/ruben/Documents/New project/output/ARTICULO_VI_PARTICULAS_Y_MASAS_20260910/technical/verificar_particula_mobius_kepler.py" --receipt "/Users/ruben/Documents/New project/output/ARTICULO_VI_PARTICULAS_Y_MASAS_20260910/technical/RECIBO_PARTICULA_MOBIUS_KEPLER.json"
```

`--quick` ejecuta sólo 16 palabras de prueba para la parte C_M y lo
declara como `QUICK_SAMPLE`; no debe presentarse como la enumeración
completa. Los restantes controles conservan su dominio declarado.

Código de reproducción de las identidades (Python 3 estándar, sin instalar
bibliotecas ni producir archivos):

```python
from itertools import product
from fractions import Fraction as F

N = 0
w = tuple(min(j, 11-j) for j in range(12))
for tau in product((-1, 0, 1), repeat=12):
    cm = tuple(-t for t in tau[::-1])
    assert tuple(-t for t in cm[::-1]) == tau
    assert sum(a*t for a, t in zip(w, cm)) == -sum(a*t for a, t in zip(w, tau))
    assert sum(cm[j]*cm[(j+1)%12] for j in range(12)) == sum(
        tau[j]*tau[(j+1)%12] for j in range(12))
    N += 1
tau_e = (1,1,1,-1,-1,-1,1,1,1,-1,-1,-1)
assert tuple(-t for t in tau_e[::-1]) == tau_e

L = 0
for a, b in product(range(-24, 25), repeat=2):
    if (a+b) % 12 == 0:
        n, s = F(a+b, 12), F(a-b, 2)
        assert n.denominator == s.denominator == 1
        assert (6*n+s, 6*n-s) == (a,b)
        L += 1

def mul(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))
def scale(z, A):
    return tuple(tuple(z*t for t in row) for row in A)
I = ((1,0),(0,1))
sig = (((0,1),(1,0)), ((0,-1j),(1j,0)), ((1,0),(0,-1)))
for A in sig:
    assert mul(A,A) == I
for a,b,c in ((0,1,2),(1,2,0),(2,0,1)):
    assert mul(sig[a],sig[b]) == scale(1j,sig[c])
    assert mul(sig[b],sig[a]) == scale(-1j,sig[c])

O = 0
for mu,K,a,e in product((F(1),F(2)), (F(1),F(3)),
                         (F(1),F(5)), (F(0),F(1,3),F(2,3)):
    p = a*(1-e*e)
    ell2 = K*p/mu
    b2 = a*a*(1-e*e)
    assert a*a*b2/ell2 == mu*a**3/K
    assert K*(e*e-1)/(2*p) == -K/(2*a)
    O += 1
print("PASS_FOCAL_IDENTITIES", N, L, O)
```
