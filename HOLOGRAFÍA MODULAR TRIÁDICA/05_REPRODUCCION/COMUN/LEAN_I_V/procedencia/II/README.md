# Instancia sectorial de área e información del artículo II

Se formaliza el desarrollo ya escrito en `09_area.tex` y
`09c_entropia_sectorial.tex`, conservando sus dos sectores de dieciocho
enlaces y sus espacios tríticos. Es una formalización añadida del resultado
preexistente, no una selección nueva de constantes.

`SectorialAreaInformation.lean` importa `IncidenceChain` del antecedente
compilado y `Mathlib`. Las etiquetas 90 y 120 se recuperan de los cardinales
ya demostrados de los espacios de banderas; su papel es posterior a la
incidencia TPK. Los índices de borde se realizan explícitamente como las
36 aristas orientadas del bloque 9 por 9 dentro del toro de orden 27.
`boundaryEdge_injective` demuestra que no se identifican aristas distintas.

La recuperación de ambos sectores a partir de N y D, su unicidad y la
involución de ocupaciones quedan probadas. La distribución `probability`
es el producto concreto de los pesos tríticos normalizados sobre las
3^36 configuraciones. Se prueban su positividad y normalización sin
enumerar esas configuraciones, mediante el teorema estándar del producto
de sumas. Se construye la purificación diagonal en coordenadas reales,
incluidas canónicamente en el espacio complejo de Schmidt; se prueba su
norma unitaria y su reducción diagonal exacta.

El empalme informacional se hace sobre ese mismo estado, mediante:

- `negative_log_probability`: −log p(Δ,v) = log Z(Δ) + Δ D(v).
- `entropy_state_equation`: s(Δ) = log Z(Δ) + Δ ⟨D⟩.
- `modular_area_of_reduced_state`: el logaritmo negativo del estado
  reducido coincide con la constante de normalización más las dos áreas
  sectoriales con sus coeficientes respectivos.

Estos hechos proporcionan la instancia positiva, normalizada y de rango
completo necesaria para aplicar los resultados clásicos de entropía de
Schmidt y de la primera ley modular que el manuscrito expone. No se afirma
haber reformalizado en este módulo la teoría general de entropía relativa,
sus desigualdades o sus derivadas. Tampoco se convierte este cierre focal
en cierre de todo el artículo II.

El módulo sectorial formula su identidad para gamma y a0 no nulos.
El consumidor `SelectedAreaInformation.lean` descarga ambas hipótesis:
gamma procede del funcional ya construido y a0 se obtiene del carácter
angular y del ángulo conjugado generados. Sólo delta queda como parámetro
de la familia reducida.

## Reproducción

Desde `/Users/ruben/Documents/New project`, con los antecedentes ya
compilados e inalterados:

```sh
task_mathlib='/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'
task_imports="$PWD/output/ARTICLE_I_PUBLICACION_PRINCIPAL_20260922/reproduction/exceptional/build:$task_mathlib/.lake/build/lib/lean"
for task_dep in "$task_mathlib"/.lake/packages/*/.lake/build/lib/lean; do task_imports="$task_imports:$task_dep"; done
LEAN_PATH="$task_imports" /Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean -DwarningAsError=true -o output/CIERRE_ACUMULATIVO_II_V_20260922/II/SectorialAreaInformation.olean output/CIERRE_ACUMULATIVO_II_V_20260922/II/SectorialAreaInformation.lean
```

La compilación ejecutada termina con código 0. Sus terminales utilizan
únicamente `propext`, `Classical.choice` y `Quot.sound`; no se añadieron
axiomas ni se usó `sorry`. El recibo causal y la verificación de huellas
se conservan separados en esta misma carpeta. No se recompilaron Mathlib
ni los antecedentes y no se alteraron los manuscritos ni paquetes sellados.

## Especialización al registro regional seleccionado

`SelectedAreaInformation.lean` realiza el empalme adicional solicitado:
gamma es exactamente `barbero SelectedPublication.angles.channels`, donde
la cámara angular procede de la instancia seleccionada del artículo I.
La positividad de gamma es conclusión, no premisa.

La prueba reorganiza la serie de retornos ya demostrada como suma de
`12*u^3-u^4`, con `u=q^(30+90*j)`. La monotonía de este polinomio en
(0,1), junto con el orden de los dos canales y la positividad angular,
demuestra `barbero_pos`. La derivación no consulta el valor decimal del
parámetro. Después se reutilizan las recuperaciones constitutivas y las
identidades de traza existentes, incluida la amplificación nonádica.

La escala areal se determina mediante
chi10 = (1 + 2 cos(pi_HMT/18))/3, thetaClock = angles.y/6 y
a0 = chi10 thetaClock, conforme a `09_area.tex:151–164`.
`thetaClock_from_degrees` demuestra su equivalencia con
(C*/6) pi_HMT/180 mediante la carta en grados ya construida.
Se prueban chi10 > 0, thetaClock > 0, a0 > 0 y gamma a0 > 0.
El reconocimiento previo de pi_HMT como pi se utiliza exclusivamente para
aplicar la positividad clásica del coseno; no selecciona ningún dato.

El terminal `selected_generated_area_information delta` aplica la
identidad modular y la ecuación entrópica a esas dos magnitudes generadas.
No recibe gamma, a0, su positividad ni su no nulidad como hipótesis.
El auxiliar `selected_area_information` se conserva como composición
intermedia general; el terminal seleccionado usa `a0_pos` para descargarla.

Para reproducir este segundo módulo, anteponer a `task_imports` los
directorios `output/CIERRE_ACUMULATIVO_II_V_20260922/II` y
`output/CIERRE_ACUMULATIVO_II_V_20260922/III`, y sustituir en la orden
de compilación `SectorialAreaInformation` por `SelectedAreaInformation`.
Se requiere el objeto compilado de `SelectedConstitutivePublication`
cuya huella registra `VERIFICATION_SELECTED.json`.

La compilación termina con código 0 y advertencias tratadas como errores.
La dependencia `Lean.ofReduceBool` procede de la construcción seleccionada
heredada; este incremento no incorpora `native_decide`, axiomas ni `sorry`.
