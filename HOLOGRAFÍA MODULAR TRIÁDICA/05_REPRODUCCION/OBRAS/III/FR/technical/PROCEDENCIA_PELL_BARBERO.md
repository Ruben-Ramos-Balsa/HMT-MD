# Procedencia y comprobaciones de la sección Catalán–Pell–Barbero

## Entrega y alcance

Se crea exclusivamente `manuscrito/sections/06_pell_barbero.tex`, con etiqueta
`iii:sec:pell-barbero`, y esta nota. No se han modificado las secciones03–05,
las fuentes I/II, el archivo principal ni ningún PDF. La sección tiene 427 líneas
y 1803 unidades separadas por espacios según `wc -w`; esta última cifra no es un
recuento editorial de palabras, pues incluye TeX.

La intervención reúne resultados existentes y amplía la exposición de sus
pruebas. Su estatuto general es **RESULTADO_RECUPERADO**, con desarrollo
demostrativo explícito del límite de Abel y de la normalización de la traza.
No se reivindican una nueva constante, una nueva derivación primaria de las
constantes HMT ni prioridad histórica de las identidades analíticas.

## Fuentes materiales leídas

Raíz de la nota especializada:

`/Users/ruben/Documents/New project/output/ARTICULO_ACCION_BARBERO_HMT_20260907_BORRADOR_02`.

1. `04_DESARROLLO/CONFLUENCIA_ESPECTRAL_Y_JERARQUIA_20260907.md`, completo.
   - §2, líneas 49–119: cociente determinantal, resolvente orientado, momento de
     profundidad, identidad Catalán–Pell y distinción entre rho y los canales.
   - §3, líneas 123–188: funcional de Barbero, función H, inversa cúbica,
     factorización, traza y coordenadas normalizadas del vacío.
2. `01_FUENTES/D07/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md`, §9 completo,
   líneas 247–359: representación en profundidad, integral del momento, prueba
   por caracteres de la evaluación de Pell, orientación y composición.
3. `01_FUENTES/B06/c51_barbero_area_informacion.tex`, completo.
   - líneas 13–43: incidencia 6→8, cardinales 90/120 y series de retorno.
   - líneas 45–78: cadena dodecafásica y generación de los pesos 12:-1.
   - líneas 80–148: funcional de Barbero y demostración del coeficiente singular.
4. Propietario integral de la realización de Pell, leído completo:

   `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/espirales/cap46_tornillo_espectral_pell.tex`.

   Las líneas 7–31 reciben la ley `V^{-1} S V=(2+sqrt3)i S` y desarrollan
   su órbita; las líneas 48–58 contienen la inversión contractiva. La sección 06
   no vuelve a presentar ese enunciado recibido como una prueba autónoma de la
   existencia de los operadores V y S. Demuestra íntegramente la evaluación
   del momento en la unidad correspondiente.
5. Propietario integral de la compatibilidad electromagnética, leído completo:

   `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/espirales/cap63_realizacion_electromagnetica.tex`.

   Sus líneas 100–115 establecen una condición de invariancia de fase para el
   tornillo de Pell. No establecen `s_+=rho` ni `s_-=rho`; por ello no se ha
   incorporado ninguna de esas identificaciones.
6. Secciones 03, 04 y 05 del artículo III, completas. Sus etiquetas se reutilizan
   sin modificar sus archivos. El núcleo común y las dependencias angulares
   se integran por el editor principal desde los propietarios I/II.

## Correspondencias de contenido

| Resultado conservado | Fuente | Destino en06 | Desarrollo añadido a la exposición |
|---|---|---|---|
| Momento orientado e integral | D07 §9; sección05 | `iii:eq:pell-moment-integral` | Condiciones en cero y continuidad del integrando |
| Integral de log(tan) | D07 §9 | `iii:lem:log-tangent` | Regularización de Abel escrita, serie uniformemente convergente antes de integrar y dominación integrable al retirar el parámetro |
| Evaluación Catalán–Pell | D07 §9 | `iii:thm:catalan-pell` | Tabla completa de las seis clases impares módulo12 y origen de2/3 |
| Derivadas en rho | D07 §9 | `iii:eq:catalan-pell-derivatives` | Reconocimiento angular y reciprocidad rho+rho^{-1}=4 |
| Retorno de fase y profundidad | D07 §9 | `iii:eq:pell-depth-composition` | Dominio del operador y acción diagonal en cada profundidad |
| Pesos12:-1 | B06, cadena fundamental | `iii:eq:barbero-cycle`–`iii:eq:barbero-weights` | Definición sobre generadores del módulo libre antes de evaluar el polo |
| Coeficiente1/24 | B06 | `iii:prop:barbero-pole` | Factorización finita de1−q^{3m}; distinción entre coeficiente de(1−q)^{-1} y residuo enq−1 |
| Factorización de gamma | Confluencia §3 | `iii:thm:barbero-factorization` | Conversión explícita grados/radianes y diferencia de cuadrados que fija1/(20pi) |
| Traza orientada | Confluencia §3 | `iii:eq:barbero-trace` | Se especifica Tr ordinaria; la variante normalizada lleva factor2 |
| Amplificación | Sección04, cálculo funcional; identidad de traza | `iii:eq:barbero-amplification` | Se explicita la normalización por9^m, consecuencia del tensor con la identidad |
| Reconstrucción mediante Z,c | Confluencia §3; sección04 | `iii:eq:barbero-zc` | Dominio positivo, orden de los canales y cambio de signo bajo conjugación |

La ampliación tensorial es una consecuencia elemental de la construcción
ya presente, no un resultado de nueva física. El relato conserva la familia
C2(s), su evaluación extrema de Catalán y su evaluación de Pell como objetos
distintos. La relación con Barbero utiliza C2 a través del operador f y de los
argumentos angulares s±, no mediante la sustitución de toda la familia por G_Cat.

## Recibo genealógico focal para la integración

Este registro semántico acompaña la sección; el recibo JSON de incorporación
del artículo corresponde al editor principal y debe incorporar estas fuentes.

1. **APP:** el soporte bidimensional y las hojas aditiva/multiplicativa son los
   del núcleo común del artículo. No se añaden alfabetos ni valores objetivo.
2. **TRIT:** se conservan la orientación de hoja y los regímenes de la
   representación; el plano de cuarto de giro está construido en la sección05.
3. **TPK:** el ciclo dodecafásico actúa en R12; P3, P4 y el plano Q de la
   sección 05 determinan f(s) y k4(s). El registro de profundidad determina
   N y el carácter U4. La incidencia 6→8 determina 90/120; la cadena fundamental
   determina los pesos 12:-1. El transporte angular anterior determina q±.
4. **Coeficientes:** 2/3 procede de la descomposición del carácter módulo 12;
   pi/12 del argumento angular de rho; 12:-1 de la cadena; 30 de la escala
   común de90/120; 1/(20pi) de la diferencia de cuadrados tras cambiar a s=q30.
5. **Información conservada:** índice de profundidad, carácter módulo 4,
   orientación de hoja, etiquetas de canal, incidencia y retorno trítico.
   La cuarta potencia de B(s,1) conserva s^{4N}, no restituye la identidad.
6. **Residencia:** son composiciones posteriores de los operadores y salidas
   ya construidos desde el núcleo común; no se redefine el continuo ni se
   introducen cinco construcciones independientes.
7. **Salidas:** evaluación C2(rho), derivadas, imagen del retorno12S90−S120 y
   funcional gamma como diferencia H(s−)−H(s+).
8. **Reconocimiento y comprobación:** las fórmulas analíticas y las pruebas
   numéricas son posteriores; no se usan medidas físicas, CODATA ni valores
   objetivo de gamma para seleccionar argumentos o coeficientes.
9. **Localizadores:** fuentes y destinos de las dos tablas anteriores, junto a
   `iii:eq:trace-det`, `iii:eq:quarter-intertwiner`, `iii:eq:catalan-vacuum`,
   `iii:eq:cubic`, `iii:eq:rchannels` e `iii:eq:four-identities` de03–05.

## Precisión corregida

La nota de confluencia usa `tr_2` sin fijar allí si es ordinaria o normalizada.
En dimensión 2:

`gamma = -Tr[R H(psi(V))]`.

Si `tau_2=Tr/2`, la expresión equivalente es `gamma=-2 tau_2[...]`.
Omitir ese 2 mientras se declara la traza normalizada dividiría gamma por 2.
La sección 06 fija ambas convenciones y conserva la fórmula escalar.
No se han cambiado los coeficientes del funcional ni la evaluación de Catalán.

## Comprobación propia ejecutada

Se ejecutaron controles en memoria, sin modificar archivos de datos ni crear
un generador alternativo. Python 3 y mpmath 1.3.0, con 90 decimales de trabajo.
Los controles numéricos son comprobaciones posteriores de identidades cuya
prueba está escrita en el TeX; no son cotas de intervalos certificadas.

- Residuo observado de la identidad Catalán–Pell: `-6.1363668e-92`.
- Las seis clases impares de la identidad de caracteres satisfacen la
  comparación numérica con tolerancia 1e-85; la tabla entera prueba la identidad.
- Cuatro pares angulares racionales de prueba: `(10,1)`, `(7,2)`, `(3,1)` y
  `(1,1/4)`, expresados en grados. Son puntos de control del dominio, no valores
  físicos ni selecciones del TPK. La diferencia entre la fórmula inicial de
  gamma y H(s−)−H(s+) fue, respectivamente,
  `3.9886384e-91`, `-1.2272734e-91`, `-1.2272734e-91`, `-4.9090935e-91`.
- La sustitución de cada s+ en la ecuación cúbica de su r+ tuvo residuos
  observados menores que 1.2e-91 en valor absoluto.
- La traza ordinaria se contrastó con la diferencia escalar en esos cuatro
  puntos. La equivalencia general se prueba mediante los proyectores de rango 1.
- Se comprobaron con `fractions.Fraction` los cardinales, el índice−1/12,
  el coeficiente1/24, el peso2/3 y `4/(36*20)=1/180` en el término logarítmico.

Código reproducible de los controles principales (lectura y cálculo en memoria):

```python
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 90
rho, lam = 2-mp.sqrt(3), 2+mp.sqrt(3)
integrand = lambda t: mp.atan(t)/t if t else mp.mpf(1)
C2 = lambda s: mp.quad(integrand, [0, s])
G = C2(1)
error = C2(rho) - (mp.mpf(2)*G/3 - mp.pi*mp.log(lam)/12)
if abs(error) > mp.mpf('1e-85'):
    raise RuntimeError('Catalan-Pell')

for n in range(1, 12, 2):
    chi = lambda j: 1 if j % 4 == 1 else -1
    rhs = chi(n) + (3*chi(n//3) if n % 3 == 0 else 0)
    if abs(2*mp.sin(n*mp.pi/6)-rhs) > mp.mpf('1e-85'):
        raise RuntimeError('character')

if Fraction(12, 270)-Fraction(1, 360) != Fraction(1, 24):
    raise RuntimeError('pole')
if Fraction(1, 2)+Fraction(3, 2)*Fraction(1, 9) != Fraction(2, 3):
    raise RuntimeError('Catalan coefficient')
if Fraction(4, 6*6*20) != Fraction(1, 180):
    raise RuntimeError('angular coefficient')

f = lambda s: (1+s+s*s)/(1+s+s*s+s**3)
H = lambda s: 12*s**3/(1-s**9)-s**4/(1-s**12)-mp.log(s)**2/(20*mp.pi)
Sm = lambda q, m: q**m/(1-q**(3*m))
for A, C in [(10, 1), (7, 2), (3, 1), (1, mp.mpf('0.25'))]:
    qp, qm = mp.exp(-mp.pi*(A+C)/180), mp.exp(-mp.pi*(A-C)/180)
    sp, sm = qp**30, qm**30
    rp, rm = f(sp), f(sm)
    gamma = (mp.pi*A*C/180
             + 12*(Sm(qm, 90)-Sm(qp, 90))
             - (Sm(qm, 120)-Sm(qp, 120)))
    if abs(gamma-(H(sm)-H(sp))) > mp.mpf('1e-80'):
        raise RuntimeError('Barbero factorization')
    if abs(rp*sp**3+(rp-1)*(1+sp+sp**2)) > mp.mpf('1e-85'):
        raise RuntimeError('inverse cubic')
    if abs(gamma-(-(H(sp)-H(sm)))) > mp.mpf('1e-80'):
        raise RuntimeError('ordinary trace')
print('CHECKS_PASS')
```

## Continuidad y estado de integración

El primer intento del arranque falló por la huella de AGENTS.md. El editor
principal comunicó su reconciliación documental autorizada. Tras ella se
repitió `tools/verificar_arranque_hmt.py` y devolvió
`PASS_ARRANQUE_HMT_2026_07_23`. También se obtuvieron
`PASS_NUCLEO_FORMAL_HMT_PERMANENTE`,
`PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY` en la autocomprobación y
`PASS_PAQUETE_RECTOR_MASAS_HMT_MD_2026_08_06` en el verificador focal directo.
Esas salidas no se denominan certificación matemática del artículo nuevo.

La comprobación estructural del TeX verificó 28 etiquetas distintas, todas con
prefijo `iii:`, 20 referencias locales resueltas en las secciones del artículo y
el cierre ordenado de todos los entornos. No equivale a una compilación.

No se ha compilado ni inspeccionado visualmente la sección 06. El preámbulo final
debe definir el entorno `lemma`, además de `theorem`, `proposition` y `proof`.
La prueba tipográfica parcial anterior sólo definía los dos primeros entornos
de enunciado y no incluía 06. El editor puede enlazar el último párrafo de 05 con
`\ref{iii:sec:pell-barbero}`: ya existe el desarrollo al que antes se remitía
como unidad de integración.

Huella de la sección al terminar la redacción:
`4b044ead8824dd15aecfb86cd111f9639412a0e5da996c1597b8c0fab7388693`.

Huellas de fuentes:

- Confluencia: `41c65faaf8ce3b686c7a9480922c682ecfad577d638a4e60c877d3654624e81e`.
- D07: `bf9069556e20d47215ef3604fdda78dd23f32ff2ed0def07a9481ea2a42db409`.
- B06: `fdeb5535396b18d9ad02adca65ab13052b87fc6e21b59da6d447a48f225122c9`.
