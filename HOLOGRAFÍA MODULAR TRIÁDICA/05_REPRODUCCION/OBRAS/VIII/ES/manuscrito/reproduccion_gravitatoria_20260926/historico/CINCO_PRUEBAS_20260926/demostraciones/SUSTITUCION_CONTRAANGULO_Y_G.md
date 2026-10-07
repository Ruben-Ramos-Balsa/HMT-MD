# Sustitución de la acción en el contraángulo y en G

25 de septiembre de 2026. Incorporación del añadido autoral sin cambiar el
objetivo de la revisión conjunta. Conserva la construcción y las pruebas
anteriores; no modifica PDF ni Lean.

## 1. Identidad recuperada, no entrada adicional

El documento de relaciones entre constantes conserva en
`ES/manuscrito/desarrollos/composicion.tex:8–47` la identidad exacta

    A_deg = 1000 α,
    C*_deg = sqrt(1000 α/φ) + 2 B(α),

con

    B(α) = 9α²/16 − 5α³/9 + 7α⁴/48 − α⁵/54 − 90 Cπ(α)/π,
    Cπ(α) = 169α⁶ + D_A α⁷/(1−D_A α),
    D_A = exp(−100πα/9).

La sección de acción retornada se expresa mediante

    η(α) = (1/2)sqrt(1000α/φ) − α + B(α),
    ℏ_ret = η(α) S_*,       S_* = 10^−34 J s

en la realización SI usada por los evaluadores. De ahí
C*=2(η+α). El término −α de η se cancela con el +α al construir C*.

Esto es precisamente la sustitución señalada por Rubén: no hay que leer
ℏ, α y C* como tres datos físicos independientes. π y φ se mantienen como
coordenadas previamente generadas por el mismo núcleo. La notación B(α)
fija esas coordenadas; no afirma que se hayan eliminado algebraicamente π
y φ ni que el decimal aislado de α sustituya al estado completo.

El mismo manuscrito recupera también

    η = C*/2 − α = α(500 ξ−1),       ξ=C*/A.

Aquí ξ es la razón angular del propietario, no un factor gravitatorio libre.
Para evitar la colisión con otros usos de ξ se designará ξ_ang en la síntesis.

## 2. Composición cerrada de la expresión radial

Sea r_N=5759/23040 y L=r_N α^16 L_* la longitud construida en la realización
del expediente conjunto. El resultado radial da

    G = c³ L²/ℏ_ret
      = (c³ L_*²/S_*) r_N² α^32/η(α)
      = (2c³ L_*²/S_*) r_N² α^32/(C*−2α)
      = (c³ L_*²/S_*) r_N² α^31/(500 ξ_ang−1).

Las cuatro escrituras son la misma función compuesta. La tercera muestra
directamente la participación del contraángulo; la segunda elimina ℏ como
argumento independiente. Ninguna utiliza G observado para despejar L ni η.

Esta composición no vuelve a generar las constantes ni selecciona una
realización por proximidad metrológica: sustituye salidas ya construidas en
la expresión de G. Conserva el lector longitudinal y la identificación radial
explicitados en `COMPOSICION_Y_CRITERIO_FIJO.md`.

## 3. Inserción constitutiva y sentido de las unidades

El par angular determina

    x=π A/180,     y=π C*/180,
    q_±=exp(−x∓y),
    r_±=(1−q_±^90)/(1−q_±^120),
    c_hat=(r_+r_−)^−1.

Por tanto, en una base de velocidad c_* común,

    G = (c_*³ L_*²/S_*)
        [r_N² α^32 c_hat³/η(α)].

El corchete reúne sólo las salidas adimensionales de la composición. Las
bases dimensionales permanecen a la vista. En la evaluación SI c_* se
transporta para que c_* c_hat sea la sección c=299792458 m/s que utiliza
el evaluador publicado; no se vuelve a multiplicar esa sección SI por c_hat.

La sustitución de c=(με)^−1/2, con μ y ε en la misma realización,
da también G=L²/[ℏ_ret(με)^(3/2)]. Esto enlaza la respuesta constitutiva
con la expresión gravitatoria sin confundir coeficientes normalizados y
valores dimensionales.

## 4. Alcance y procedencia

La prueba es sustitución exacta en las ecuaciones indicadas. Los controles
numéricos independientes que acompañan esta nota comparan la fórmula
expandida de C*, la recuperación de η y las cuatro formas de G a dos
precisiones de trabajo. La precisión decimal no es precisión experimental.

La causalidad conservada es APP → TRIT → TPK-full → estado enriquecido →
estructura discreta conjunta del continuo → coordenadas generadas → acción,
par angular, respuesta constitutiva y longitud → coeficiente radial.
La comparación experimental, si se solicita, va después.

Propietario principal:
`/Users/ruben/Documents/New project/output/RELACIONES_ESTRUCTURALES_CONSTANTES_ES_EN_20260923/ES/manuscrito/desarrollos/composicion.tex`.
Evaluador reutilizado:
`/Users/ruben/Documents/New project/output/SELECCION_LONGITUD_GRAVITATORIA_HMT_20260925/verificar_sustitucion_estructural.py`.
