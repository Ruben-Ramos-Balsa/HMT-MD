# Revisión metrológica focal — antecedentes y ampliación REV08

## Corrección REV08 — 25 de septiembre de 2026

Se conserva el dossier REV07 y se modifica únicamente el cuadro térmico-gravitatorio de la página 15. Se incorpora ℏ_geom = √(H5 η_ret) × 10⁻³⁴ J s = 1,054571817280596765… × 10⁻³⁴ J s, frente a h_SI/(2π) = 1,054571817646156391… × 10⁻³⁴ J s. La diferencia es −3,65560 × 10⁻⁴⁴ J s; la relativa, −3,46643 × 10⁻¹⁰.

Boltzmann muestra la realización SI documentada 1,380649 × 10⁻²³ J/K frente a la definición SI. G muestra la evaluación del lector declarado 10⁻¹¹(6 + 674/10³ + 30/10⁵) = 6,67430 × 10⁻¹¹ frente a CODATA 2022, 6,67430(15) × 10⁻¹¹ m³ kg⁻¹ s⁻². Sus diferencias numéricas nulas se identifican expresamente como coincidencias de una definición o de cifras declaradas, no como predicciones independientes. La relación térmica interna y la función de la normalización permanecen visibles.

La comprobación reproducible y las huellas de las fuentes recuperadas se registran en revision/COMPROBACION_NUMERICA_REV08.json del directorio superior trilingüe. No se modifica ni se vuelve a ejecutar el generador científico. Los párrafos siguientes conservan el historial de correcciones anteriores.

Fecha: 22 de septiembre de 2026. Fuente editorial: selección de obras vigente en `REV01/metadata/FUENTES_DOCUMENTALES.json`; artículos I, II y III del núcleo integrado de 21 de septiembre. El archivo `metrologia.json` contiene coordenadas, referencias, diferencias, unidades y localizadores. Esta revisión transcribe y compara; no ejecuta de nuevo el generador ni modifica las obras fuente.

## 1. α y electrón: conservar el contraste de ambas ediciones

La sección corregida del electrón es εₑᵝ = 0,5109989506900008086082571648…; se realiza mediante Eₑᵝ = εₑᵝ u_E y mₑᵝ = Eₑᵝ/c², con u_E = 1 MeV. No usar la evaluación basal anterior como si fuese la vigente. El artículo I ya conserva tanto CODATA 2018 como CODATA 2022:

| Observable y referencia | Diferencia HMT − referencia | Diferencia / u de referencia |
|---|---:|---:|
| α, CODATA 2018, recíproco del centro de α⁻¹ | −5,68408 × 10⁻³⁷ | −5,08289 × 10⁻²⁵ |
| α, CODATA 2018, valor directo redondeado | −1,61990 × 10⁻¹⁴ | −0,0147264 |
| α, CODATA 2022 | +4,98380 × 10⁻¹² | +4,53073 |
| mₑᵝ, CODATA 2022 | +8,08608 × 10⁻¹⁶ MeV/c² | +0,00000505380 |
| mₑᵝ, CODATA 2018 | +6,90001 × 10⁻¹⁰ MeV/c² | +4,60001 |

REV03 recupera la comparación que REV02 omitía: r = 1/137,035999084. Frente a ese centro recíproco, la lectura prolongada presenta una diferencia relativa −7,7892411359 × 10⁻³⁵, inferior a 10⁻³⁴ en valor absoluto. La incertidumbre propagada es 1,11827844493 × 10⁻¹². La ventana finita 0,007297352569283800997285105472380663 tiene diferencia relativa −7,7832687308 × 10⁻³⁵; no se identifica con la prolongación, que incorpora el acarreo remoto. El registro `ACTUALIZACION_NUCLEO_SERIE_20260921/EVIDENCIA_K_PORTATIL/03_PAPER/HMT_MACROPAPER_V3/CURRENT.json`, líneas 286–290, consigna explícitamente `floor(10^36/137.035999084)/10^36` como reconocimiento externo, no predicción independiente. La relación de reconocimiento no demuestra por sí sola ni calibración del generador ni independencia causal. Las dos filas 2018 usan la misma referencia con representaciones redondeadas diferentes, no dos mediciones.

Es legítimo destacar las referencias solicitadas —2018 para α, 2022 para electrón— si los contrastes cruzados siguen visibles. Las ediciones no son pruebas independientes, y esos cocientes no incorporan una incertidumbre teórica HMT que la tabla no proporciona. Las cifras posteriores a la precisión experimental describen la evaluación de la expresión, no nuevas mediciones.

Localizadores: I, `sections/comparacion.tex`, líneas 4–47; `sections/electron.tex`, líneas 925–950 y 984–995. Referencias externas verificadas: [CODATA 2018, pp. 1–2](https://physics.nist.gov/cuu/pdf/all_2018.pdf) y [tabla NIST CODATA 2022](https://physics.nist.gov/cuu/Constants/Table/allascii.txt).

## 2. Planck: fórmula propia y comparación con una definición exacta

Las dos secciones conservan h_pre = 2πH₅ × 10⁻³⁴ J s y h_ret = 2πη_ret × 10⁻³⁴ J s. Con los coeficientes completos de `III/technical/EVALUACION_VACIO.json`:

| Sección | Valor en J s | Diferencia relativa respecto de h_SI |
|---|---:|---:|
| h_pre | 6,626070149999987926… × 10⁻³⁴ | −1,82 × 10⁻¹⁵ |
| h_ret | 6,626070145406254334… × 10⁻³⁴ | −6,93284 × 10⁻¹⁰ |

h_SI = 6,62607015 × 10⁻³⁴ J s es exacto por definición. No hay residuo en unidades de incertidumbre experimental; no debe dividirse por cero. Para ℏ, la referencia exacta es h_SI/(2π), no el decimal corto 1,054571817 × 10⁻³⁴ tratado como exacto. La fórmula de H₅ ya incluida en el cuadro 2 debe conservarse completa.

Detalle de precisión: II imprime −1,822221 × 10⁻¹⁵ para la sección anterior al retorno; el recálculo a partir del H₅ completo da −1,82219605532702 × 10⁻¹⁵. La presentación −1,82 × 10⁻¹⁵ evita una falsa precisión común; queda registrada la pequeña discrepancia de últimas cifras para el editor de II. No se modifica esa fuente.

Localizador: II, `sections/18_comparacion_cuantitativa_II.tex`, líneas 36–76. Referencia: [constantes definitorias del SI, BIPM](https://www.bipm.org/en/measurement-units/si-defining-constants).

## 3. CKM: comparación homogénea, no cambio de observable

La fuente vigente compara sin θ₁₂, sin θ₂₃, sin θ₁₃, δ en radianes y J. Los residuos marginales recalculados son, respectivamente, −0,00381653; +0,0148823; +0,0289018; −0,0282515 y −0,00856389. Para una diferencia positiva se usa la incertidumbre superior; para una negativa, la inferior. Las ecuaciones angulares pueden conservarse en grados, pero la conversión a radianes se efectúa una sola vez al evaluar senos y fase.

No confundir sin θ₁₂ con |V_us| = sin θ₁₂ cos θ₁₃, ni sin θ₂₃ con |V_cb| = sin θ₂₃ cos θ₁₃. No sumar los residuos al cuadrado para fabricar un ajuste global sin las covarianzas del comparador. El valor de J se compara con el mismo factor de escala en valor e incertidumbre.

Localizador: II, `sections/18_comparacion_cuantitativa_II.tex`, líneas 154–220; referencia [PDG 2025, CKM, p. 13, ecuaciones 12.27–12.28 y J contiguo](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf).

## 4. G: relación determinada y coordenada de carta

La fórmula vigente es G_a = (54/π)² c_int⁵ t₀²/ℏ_a, equivalente a G_a = c_int³ R₁₀₈²/ℏ_a con R₁₀₈ = (54/π)ℓ₀ y ℓ₀ = c_int t₀. El selector adimensional es 295,4525715010569…; se conservan la reciprocidad G_pre/G_ret = R_act⁻¹ y la identidad G_aℏ_a/c_int³ = R₁₀₈².

II consigna 6,67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² en la carta utilizada. La misma sección identifica explícitamente esta coordenada como referencia de carta y no calcula un residuo predictivo. Por tanto, el dossier puede mostrar el número con esa denominación, junto a CODATA 2022, 6,67430(15) × 10⁻¹¹, pero no convertir la coincidencia de escritura en una predicción independiente de residuo cero. Para un contraste independiente falta, en las fuentes focales examinadas, la evaluación numérica de t₀ en una carta de tiempo fijada sin G objetivo, además de explicitar c_int, orientación y sección de acción. La fórmula y las identidades sí están disponibles y no deben omitirse.

Localizador: II, `sections/18_comparacion_cuantitativa_II.tex`, líneas 264–308 y `sections/definicion_gravedad_rev06.tex`. Referencia: [CODATA 2022, NIST](https://physics.nist.gov/cuu/Constants/Table/allascii.txt).

## 5. Vacío: las cuatro coordenadas existen; no son todavía cifras SI

III construye una respuesta común V = (I − T⁹⁰)(I − T¹²⁰)⁻¹. Sus dos autovalores r_± determinan ε̂ = r₊², μ̂ = r₋², Ẑ = r₋/r₊ y ĉ = 1/(r₊r₋). Las coordenadas vigentes son:

| Coordenada interna | Evaluación | Realización dimensional |
|---|---:|---|
| ε̂ | 0,999999257096636702760… | ε = ε̂ u_Q²/(u_S u_C) |
| μ̂ | 0,999448350479326935089… | μ = μ̂ u_S/(u_C u_Q²) |
| Ẑ | 0,999724508538937215455… | Z = Ẑ u_S/u_Q² |
| ĉ | 1,000276310486157526106… | c = ĉ u_C |

No faltan las relaciones constitutivas: με = c⁻² y μ/ε = Z² se conservan exactamente en la realización. Lo que III declara necesario para comparar cifras SI es una carta numérica independiente para u_S, u_Q y u_C. El dossier debe exhibir coordenadas y fórmulas, sin rellenar su columna HMT–SI con las cifras de referencia. Si se fija c = c_SI, la sección sería u_C = c_SI/ĉ; identificar u_C directamente con c_SI introduciría un factor incorrecto, y ajustar la sección mediante c objetivo sería una calibración explícita.

Las referencias CODATA 2022 para una futura comparación, ya recogidas en el JSON, son ε₀ = 8,8541878188(14) × 10⁻¹² F/m; μ₀ = 1,25663706127(20) × 10⁻⁶ N/A²; Z₀ = 376,730313412(59) Ω; c = 299792458 m/s exacto. No se presentan como cuatro observaciones independientes.

Localizadores: III, `manuscrito/sections/04_respuesta_constitutiva.tex`, líneas 12–83 y 193–199; `08_evaluacion_y_realizacion.tex`, líneas 49–83 y 116–123; `technical/EVALUACION_VACIO.json`, campo `values`. Referencia: [CODATA 2022, NIST](https://physics.nist.gov/cuu/Constants/Table/allascii.txt).

## 6. Filas complementarias que deben conservar su significado

La fila de mezcla débil ya presente en REV01 corresponde al esquema on-shell de la narrativa de 314 páginas: 0,224870880752843569… frente a 0,22342 ± 0,00009; el residuo marginal es +16,1209. No sustituir ese comparador por MS-bar o por el ángulo efectivo leptónico. Referencia: [PDG 2025, interacción electrodébil, tabla 10.2](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf). Es una fila documental complementaria, no una atribución nueva a I–III.

k_B = 1,380649 × 10⁻²³ J/K es exacto en el SI. La relación interna k_B Θ_clk,a log 3 = h_a/(108t₀) realiza el enlace térmico; la identificación dimensional fija la escala de temperatura. Barbero–Immirzi se compara con otra construcción teórica, no con una medición ni una incertidumbre experimental.

## Estado de la revisión

El antecedente REV02 registró una divergencia de hash de AGENTS.md en su arranque. En REV03, el núcleo formal, la autocomprobación de constantes y `trunkctl check` han pasado. El contraste α se reproduce a 120 cifras en `herramientas/verificar_alpha_2018.py`; su alcance es aritmético y documental, no una nueva prueba del generador ni validación física externa. Las fuentes y los PDF de referencia permanecen intactos. Las comprobaciones de precompilación y composición de la entrega se registran separadamente en metadata.
