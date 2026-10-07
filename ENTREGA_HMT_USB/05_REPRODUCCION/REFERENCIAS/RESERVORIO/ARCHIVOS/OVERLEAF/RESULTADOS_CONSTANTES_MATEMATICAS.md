# Constantes matemáticas: resultados reunidos para la integración coordinada

Fecha: 6 de septiembre de 2026. Responsable de este bloque: **Preparar paper en Overleaf**. Integración: **Aclarar la tarea**.

## Resultado y alcance

Se han reunido los pasajes demostrativos y las comprobaciones existentes de los **19 apartados matemáticos asignados**. El resultado incluye familias infinitas definidas en el texto, identidades exactas y cálculos finitos con su alcance expresado separadamente. Los apartados se corresponden con el inventario de trabajo: **no son 19 constantes independientes**. Apéry pertenece a los valores impares de zeta; Glaisher–Kinkelin pertenece a Bendersky–Glaisher.

Esta entrega recupera resultados del corpus y concilia sus evaluadores. No modifica el manuscrito, ningún PDF ni los certificados compartidos. No vuelve a calcular el intervalo racional de Catalán, el producto de primos gemelos, las cien millones de posiciones de vacancia ni las ocho bifurcaciones almacenadas.

La edición fijada por la coordinación es el [integral de 2.249 páginas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/02_PDF/INTEGRAL/main_paquete_union_demostrativa_20260904.pdf>), SHA-256:

`958d252f301763ff8901f775d8ec0b02b6ae4f9f7c57dc04ea917f747dccbf24`.

El bloque de π, φ, e, i y α corresponde a Ley 9 puertas; masas, electrón, Planck, gravedad, Barbero y mezclas corresponden a MASAS; electromagnetismo y termodinámica corresponden a Aclarar la tarea. No se ha duplicado su trabajo.

## 1. Construcciones presentes y sus resultados

Los localizadores F18 y C33–C39 se resuelven a archivos absolutos en la sección 5. Los números tras dos puntos son líneas de fuente.

| Apartado | Construcción y resultado presentes | Evidencia matemática y material |
|---|---|---|
| 1. Catalán | El levantamiento unitario de orden cuatro determina \(Q_4=(U_4-U_4^\ast)/(2i)\); la traza \(\operatorname{Tr}(N^{-2}Q_4)\) da \(\sum_{n\ge0}(-1)^n/(2n+1)^2\). | C33:93–158 demuestra la identificación y la convergencia absoluta. El cálculo racional ya ejecutado por Aclarar da un intervalo de anchura \(\le2^{-150}\), sin emplear un decimal objetivo. |
| 2. Apéry | Evaluación del funcional espectral en \(s=3\): \(\mathcal Z_3(3)=\zeta(3)\). | F18:815–838 contiene \(S_N+[2(N+1)^2]^{-1}<\zeta(3)<S_N+(2N^2)^{-1}\). El cálculo existente con \(N=10^6\) está acompañado de estos límites analíticos. |
| 3. Euler–Mascheroni | Parte finita del polo espectral: \(\gamma=C_0+C_1+C_2\). | F18:684–813 deriva la recomposición de los tres residuos. La evaluación compartida da \(0.577215664901532860606512090082402431\ldots\). |
| 4. Familia de Stieltjes | Los coeficientes de Laurent de las tres clases residuales producen \(\gamma_n=(-1)^n n!(c_{0,n}+c_{1,n}+c_{2,n})\). | F18:684–753 prueba la relación para todo \(n\ge0\). C33:246–273 proporciona la representación theta–Mellin. El control numérico existente cubre \(n=0,\ldots,6\); la generalidad procede de la identidad de series, no de esos siete ensayos. |
| 5. Glaisher–Kinkelin | \(A_1=\exp(1/12-\mathcal Z_3'(-1))\), con la normalización del hiperfactorial explicitada. | F18:843–864 y C35:1–49. Valor compartido \(1.282427129100622636875342568869791\ldots\). |
| 6. Bendersky–Glaisher | \(A_k=\exp(H_kB_{k+1}/(k+1)-\mathcal Z_3'(-k))\), \(k\ge0\), con \(H_0=0\), \(B_1=-1/2\). | C35:1–65 construye la familia y su relación con los valores impares. Se han reutilizado las evaluaciones \(A_0,\ldots,A_6\). |
| 7. Euler–Kronecker | Parte finita normalizada de la zeta de los cuerpos cuadráticos tratados: \(\gamma_K=\gamma+L'(1,\chi)/L(1,\chi)\). | F18:866–906 para \(\mathbb Q(\sqrt{-3})\); C34:1–46 para \(\mathbb Q(\sqrt3)\). Valores concordantes \(0.94549728087168070324\ldots\) y \(1.05396560824848258004\ldots\). Se ha conciliado una discrepancia entre comprobadores, detallada abajo. |
| 8. Meissel–Mertens | \(B_1=\gamma+\sum_p[\log(1-1/p)+1/p]\), mediante los modos irreducibles de la factorización espectral. | F18:952–999; C34:48–63. La prueba controla la convergencia de la corrección por primos. La evaluación compartida incluye suma truncada y cota de cola; sus decimales deben conservar el alcance de redondeo del evaluador. |
| 9. Constante de los primos gemelos | \(C_2=\prod_{p>2}p(p-2)/(p-1)^2\). | F18:908–950 demuestra la convergencia y acota la cola por el producto telescópico sobre enteros. El replay con corte \(2\,000\,000\) da el intervalo exterior \(0.66016150712258952<C_2<0.66016183720350813\). Esto es una constante de producto, distinta de afirmar infinitud de pares de primos gemelos. |
| 10. Khinchin | Media logarítmica del dígito de fracción continua respecto de \(d\mu_G=dx/[(1+x)\log2]\); \(K=\exp\int\log a_1\,d\mu_G\). | C36:38–106 fija medida, distribución y convergencia del producto. Valor compartido \(2.68545200106530644531\ldots\). El teorema ergódico es casi seguro respecto de esa medida; no afirma la misma media para cada historia individual. |
| 11. Lévy | \(L=-\int_0^1\log x\,d\mu_G=\pi^2/(12\log2)\). | C36:38–106. Valor compartido \(1.18656911041562545282\ldots\). La entropía de la transformación es \(2L\), no una constante independiente sin relación. |
| 12. Lochs y bases | \(\Lambda_b=6\log2\,\log b/\pi^2\), para base entera \(b\ge2\). | C36:108–145. Se recuperan \(\Lambda_{10}=0.97027011439203392574\ldots\) y \(\Lambda_{729}=2.77761896637430577771\ldots\). El parámetro \(b\) especifica la representación; no es un valor ajustado de la constante. |
| 13. Gauss–Kuzmin–Wirsing | Operador de transferencia \((\mathcal Lf)(x)=\sum_{n\ge1}(n+x)^{-2}f(1/(n+x))\), con su problema espectral subdominante. | C36:147–193 contiene el operador, la normalización y el valor de referencia \(\lambda_2\simeq-0.3036630028987326586\). La constante positiva habitualmente tabulada es su módulo. El aislamiento espectral certificado se distingue expresamente de la referencia decimal. |
| 14. Feigenbaum \(\delta_F,\alpha_F\) | Las doce fases del TPK fijan un perfil par y una familia unimodal, de la que se calculan parámetros superestables y razones de escala. | F37:10–277 y el certificado conservado contienen la construcción finita sin usar \(\delta_F\) ni \(\alpha_F\) como valores objetivo. Hay ocho niveles almacenados; su contenido y la cuestión del límite se separan en la sección 3. |
| 15. Valores impares de zeta | \(\zeta(2n+1)=(-1)^{n+1}2(2\pi)^{2n}\log A_{2n}/(2n)!\), \(n\ge1\). | C35:21–29 y 54–65 demuestra la identidad a partir de la ecuación funcional y \(B_{2n+1}=0\). Se reutilizan los valores de \(\zeta(3),\zeta(5),\zeta(7),\zeta(9)\), sin reducir la familia a estos ejemplos. |
| 16. Valores de funciones \(L\) individualizados | Caracteres de los levantamientos de órdenes tres, cuatro y doce; en particular \(L(1,\chi_{-3})=\pi/(3\sqrt3)\), \(L(1,\chi_{12})=\log(2+\sqrt3)/\sqrt3\), \(L(2,\chi_{12})=\pi^2/(6\sqrt3)\). | C33:23–244; F18:761–813. Para \(\chi_{12}\), los residuos \(1,5,7,11\) tienen signos \(+,-,-,+\). Valores compartidos \(0.60459978807807261686\ldots\), \(0.76034599630094634753\ldots\), \(0.94970312629400939526\ldots\). |
| 17. Constantes regularizadas de vacancia | La palabra mecánica \(z_n=\lfloor(n+1)\delta\rfloor-\lfloor n\delta\rfloor\) produce una discrepancia acotada y la familia \(\gamma_{\rm vac,j}^{+}=\delta\gamma_j+\sum_{n\ge1}(z_n-\delta)(\log n)^j/n\), con la convención impresa. | C39:26–143 prueba convergencia mediante sumación por partes para cada \(j\ge0\). El certificado preexistente registra \(10^8\) posiciones y \(4\,575\,749\) eventos. Para \(j=0\), su intervalo conservador está contenido en \((-0.112071086058764,-0.112071064058763)\). |
| 18. Valor \(-1/12\) | Se encuentran realizaciones diferenciadas: continuación meromorfa \(\mathcal Z_3(-1)\), defecto de incidencia \((90-120)/(24\binom62)\), pseudoinversa orientada y exponente del cociente eta. | C27:96–159; B43:28–43. Son identidades con dominios y normalizaciones propios. La suma ordinaria de enteros positivos y la continuación meromorfa son operaciones distintas; la igualdad del escalar tampoco identifica por sí sola sus operadores. |
| 19. Valor \(1/24\) | El funcional de Lambert de pesos \(12:-1\) da \(12/270-1/360=1/24\), coeficiente de \((1-q)^{-1}\). | B43:60–144 y la precedencia dodecafásica conservan los pesos antes de evaluar el polo. El residuo complejo en la variable \(q\), en \(q=1\), es \(-1/24\). El control racional exacto estaba ya ejecutado. |

Los logaritmos usados en normalizaciones, las bases de representación y los índices de una familia se muestran como tales. No se suman al inventario como nuevas constantes independientes.

### Unidades algebraicas complementarias

El corpus conserva \(3+2\sqrt2\), \(2+\sqrt3\) y \(30+\sqrt{899}\). C38 demuestra para \(3+2r\), \(r^2=2\), norma uno y orden \(4\cdot3^{k-1}\) en la reducción trítica, con el límite correspondiente. El modo de F38 utiliza la matriz
\[
\begin{pmatrix}30&899\\1&30\end{pmatrix},
\qquad \det=1,
\]
cuyos autovalores son \(30\pm\sqrt{899}\). Los tres valores fueron evaluados en el fichero compartido. Su tipado permanece separado: la igualdad de forma «unidad de Pell» no identifica las tres dinámicas.

## 2. Dependencias y normalizaciones verificadas en los pasajes

La lectura preserva la precedencia del corpus APP → TRIT → TPK → estado enriquecido → realizaciones espectrales y aritméticas. El objeto principal de este bloque es la evaluación de los funcionales ya construidos. La verificación completa de la generación nonádica de π, φ, e, i y α corresponde al bloque coordinado de Ley 9 puertas; este informe no la sustituye por llamadas a funciones numéricas.

En F18:510–611 se define el operador discreto sobre \(C_m=\mathbb Z/3^m\mathbb Z\), con normalización
\[
D_m^2=\frac{3^{2m}}{4\pi}\Delta_m.
\]
La fuente utiliza aquí la coordenada π del sector arquimediano previamente construido: es una dependencia posterior, no un decimal externo destinado a seleccionar el generador. La traza positiva elimina el modo cero y cuenta una sola vez cada pareja \(n,-n\). El límite de calor se prueba por convergencia dominada, con una cota gaussiana sumable uniforme. Su transformada de Mellin normalizada identifica \(\mathcal Z_3(s)\) y fundamenta las evaluaciones de las filas 2–8 y 15.

C33 construye el levantamiento unitario que determina el carácter para Catalán y los caracteres compuestos. La aparición de \(i\) en este lector es una realización posterior del levantamiento, no una nueva entrada numérica de APP. C36 especifica la medida invariante y el lector de fracciones continuas sobre los valores; la casi seguridad tiene una medida explícita. C39 fija el inicio \(n=1\), la orientación y la pendiente de vacancia; cambiar cualquiera de estos datos cambia la parte finita.

Esta separación permite informar tanto el resultado positivo como las condiciones efectivas bajo las cuales se obtiene. El texto, las identidades exactas y los evaluadores cumplen funciones distintas.

### 2.1. Procedencia ejecutable: generación, evaluación y comprobación

Esta precisión se incorpora por la indicación de Rubén: los evaluadores empleados en esta auditoría son operaciones posteriores; su alcance no define ni sustituye el del generador del corpus.

La [demostración de profundidad arbitraria del capítulo 27](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex:553>) establece el orden caracteres exactos → evaluación arquimediana → prefijos compatibles. El [recibo causal del paquete](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/04_RECIBOS/RECIBO_CAUSAL_GENERACION_ANTES_PUBLICACION_ARQUIMEDIANA_20260905.json>) enumera las hojas APP, el orientador TRIT, los operadores TPK y las cuatro salidas correlacionadas. Es un contrato de procedencia: conserva expresamente el estado `STAGING_UNTIL_EXT_GLOBAL_SECTION_AND_PACKAGE_ADMISSION_PASS`; no se confunde con un recibo de ejecución.

El ejecutable sucesor examinado es [verificar_generacion_infinita_nonadica.py](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/verificar_generacion_infinita_nonadica.py:2248>), SHA-256 `0a5b0b8cee4ec477e5a255c4ba30ff6155a4b5cc28588ead3cebff652416c579`. Su función `run` ordena las operaciones siguientes:

| Etapa | Funciones y operación efectiva |
|---|---|
| Catálogo APP–TRIT ya producido → órbitas | `select_structural_orbits` lee `TPK_U_catalog_468.json`, comprueba multiplicidades y acción trítica, y selecciona los representantes de clausura, propagación y autoescala. En esta función el catálogo se consume como antecedente serializado; no se vuelve a generar desde las parejas iniciales. |
| Transporte y frontera | `reconstruct_lifts_and_calendar` reconstruye elevaciones respecto del registro explícito; `finite_chain` aplica las elevaciones; `generate_target_free_r36` construye candidatos mediante margen, acarreo, ocupación y condición de Witt, y los discrimina por energía del semigrupo. `verify_typed_r36_aw_bridge` verifica el cambio de representación de incidencia. |
| Caracteres antes de las cifras | `generate_structural_characters` reúne los datos de clausura, la recurrencia normalizada de propagación y la incidencia de autoescala, junto con sus fuentes y controles. Incluye la descripción del carácter firmado de α; esta función no calcula su expansión. |
| Evaluación posterior | `evaluate_generated_characters` entrega los caracteres a `closure_bounds`, `propagation_bounds` y `autoscale_bounds`. La sucesora valida la normalización/recurrencia de e y la incidencia/polinomio de φ antes de aplicarlos. |
| Representación de los valores | `publish_archimedean_blocks` obtiene bloques de las cotas racionales. `run` contrasta sus primeros bloques con las palabras y la frontera R36 anteriores, además de comprobar compatibilidad de prefijos y contadores de fase/memoria. Esta publicación se ejecuta después de los caracteres. |

La [documentación portable](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/README_VALIDACION_CARACTERES.md>) identifica las nueve dependencias locales y diferencia dos ejecuciones ya conservadas: siete pruebas de la interfaz e/φ, y una ejecución de integración de `run` solicitando ocho cifras con 396 niveles heredados. El [recibo de esas ejecuciones](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS/RECIBO_VALIDACION_CARACTERES.json>) enlaza los tres archivos de `SMOKE_8`. En esta corrección se comprobaron las siete huellas de fuente, fixture, prueba y salidas que registra: todas coinciden. No se repitieron esas ejecuciones. Su existencia acredita el recorrido del programa; no transforma declaraciones de metadatos sobre profundidad arbitraria en una prueba obtenida de una corrida finita.

**Qué hizo nuestra reevaluación compartida.** [`comprobar_valores_corpus.py:build`](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_valores_corpus.py:74>) llamó a la selección de órbitas y al lector de clausura. Para e y φ volvió a escribir los caracteres normalizados y llamó directamente a sus evaluadores; no llamó a `run` ni a `generate_structural_characters`. Después contrastó doce tríadas con las serializadas para el cierre dodecafásico. Ése es el alcance efectivo de esta comprobación parcial. Los antecedentes TPK de los caracteres se documentan en los propietarios anteriores y en el bloque de Ley 9; no quedan sustituidos por esta reevaluación.

**Lugar exacto de Chudnovsky y del cierre de α.** En [`verificar_alpha_dos_vias.py`](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_alpha_dos_vias.py:67>), `k_from_hadamard` y `k_from_differences` reconstruyen el sello a partir de los registros publicados; `alpha_by_carry` aplica el acarreo a las tríadas publicadas. La función `pi_chudnovsky` es llamada por `vacancy_root`, un control analítico posterior de un polinomio de vacancias fijado. No interviene en esas dos reconstrucciones del sello ni en el acarreo. Tampoco es llamada por la reevaluación compartida: ésta utiliza sus propias cotas de π para evaluar los jets. Por tanto, encontrar Chudnovsky en ese control no permite atribuirle la generación APP–TRIT–TPK de π, φ, e o α. A su vez, reconstruir el sello desde registros publicados no equivale a haber reejecutado en ese comprobador la producción de dichos registros.

La distinción anterior conserva simultáneamente el contenido matemático documentado, las dependencias realmente ejecutadas y el alcance limitado de nuestros controles. No introduce cifras nuevas ni modifica el generador.

La [traza estructural ampliada](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/PROCEDENCIA_ESTRUCTURAL_MATEMATICAS_Y_COSMOLOGIA.md>) reúne las entradas, operaciones, salidas y controles posteriores de los 19 apartados. Incorpora además el producto nativo y su selector de irreducibles como antecedentes de los funcionales sobre primos, sin sustituirlos por las cribas usadas en los replays.

## 3. Construcción finita de Feigenbaum conservada

Las doce marcas \(3m-1\) dan exactamente
\[
\sum_{m=1}^{12}(3m-1)^2=5394=6\cdot899,
\qquad
\sum_{m=1}^{12}(3m-1)^4=4294614.
\]
La normalización produce
\[
u_0(x)=1-\frac1{12}\sum_{m=1}^{12}
\cos\!\left(\frac{2(3m-1)x}{\sqrt{899}}\right)
=x^2-\frac{715769}{2424603}x^4+O(x^6).
\]
El factor π se cancela al normalizar las fases. Ni \(\delta_F\) ni \(\alpha_F\) seleccionan los coeficientes del perfil. La forma trigonométrica cerrada se demuestra en F37:83–144; la paridad, criticidad cuadrática y propiedades unimodales se tratan en F37:146–202.

El código conservado define \(f_\lambda=1-\lambda u_0\), busca el retorno superestable y comprueba numéricamente los retornos de períodos menores. El certificado registra:
\[
\lambda_8=1.8740277441544506728970075735950924\ldots,
\]
\[
\delta_8=4.6692121891502041545560962158896639\ldots,\qquad
\alpha_8=2.5029684798804640158584204408267322\ldots.
\]
Los residuos numéricos de raíces llegan aproximadamente a \(3.6\cdot10^{-50}\). El programa emplea precisión múltiple y bisección; estos registros no son intervalos de raíces obtenidos con aritmética dirigida. Las filas posteriores que el texto presenta como provisionales no se cuentan como ocho nuevos niveles reproducidos.

Hay, por tanto, un perfil generado y una sucesión finita calculada que deben incorporarse positivamente al inventario. La demostración de convergencia al límite universal exige las condiciones de renormalización, transversalidad y control global explicitadas en F37:279–343. Este control concreto no ejecutó ese certificado de límite. No se traslada esta reserva a las identidades del perfil ni a las ocho aproximaciones efectivamente almacenadas.

## 4. Conciliación y alcance de las comprobaciones

### Corrección concreta de un evaluador: Euler–Kronecker de \(\mathbb Q(\sqrt3)\)

Un replay había guardado \(1.05396560814669664149\ldots\) dentro de un bloque marcado globalmente como aprobado. El evaluador Euler–Maclaurin compartido daba \(1.05396560824848258004\ldots\).

Se ejecutó **una sola comprobación focal adicional**, reutilizando la biblioteca local, sin instalación ni red. Para \(\chi_{12}\) se empleó el coeficiente de Laurent:
\[
L'(1,\chi_{12})=-\log12\,L(1,\chi_{12})
-\frac1{12}\sum_{r\in\{1,5,7,11\}}\chi_{12}(r)\gamma_1(r/12).
\]
Las evaluaciones a 60 y 90 dígitos concuerdan hasta un error observado de \(4.49\cdot10^{-50}\). La evaluación de mayor precisión da
\[
\gamma_{\mathbb Q(\sqrt3)}
=1.0539656082484825800360884791800748691347934450903\ldots,
\]
y difiere de Euler–Maclaurin en aproximadamente \(1.47\cdot10^{-45}\). El escalar antiguo difiere en \(1.02\cdot10^{-10}\).

**Para la integración se utiliza el valor concordante; se descarta ese único escalar del replay.** La discrepancia corresponde a los comprobadores posteriores. No se atribuye sin prueba a una incorrección de la fórmula del tratado. Tampoco se convierte concordancia a dos precisiones en una cota rigurosa de redondeo.

- [Control conciliado](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/CONTROL_EULER_KRONECKER.json>).
- [Programa focal reproducible](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/resolver_discrepancia_ek.py>).

### Límites precisos del bloque, después de los resultados

1. **Gauss–Kuzmin–Wirsing:** están el operador, su interpretación y el decimal de referencia. En el pasaje examinado, el aislamiento certificado del autovalor se formula como una obligación específica. Este bloque no acredita haber ejecutado ese aislamiento.
2. **Feigenbaum:** están la construcción exacta del perfil y ocho niveles finitos calculados. El certificado del límite universal es una obligación distinta, delimitada en la sección anterior.
3. **Redondeo:** la diferencia máxima entre dos resoluciones del evaluador espectral compartido es aproximadamente \(1.38\cdot10^{-56}\). Es evidencia de estabilidad numérica, no una cota uniforme de todo error posible. Los intervalos racionales o con redondeo dirigido se distinguen de las sumas decimales acompañadas únicamente de una cola analítica.
4. **Procedencia:** las fórmulas, familias y pruebas recuperadas pertenecen al corpus. El trabajo nuevo aquí consiste en reunir su localización y conciliar un escalar de control. No se atribuye al presente informe un descubrimiento matemático ni una nueva prueba de todo el corpus.
5. **Cobertura:** este documento termina la partición asignada, no el dictamen del catálogo físico ni el de π, φ, e, i y α. El estado global lo consolida Aclarar la tarea con las otras entregas.

## 5. Fuentes y cálculos reutilizados

### Fuente matemática

- **F18:** [Funcionales espectrales triádicos](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/18_funcionales_espectrales_triadicos.tex:510>).
- **C33:** [Catalán, Apéry, Euler y caracteres](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c33_catalan_apery_euler.tex:23>).
- **C34:** [Euler–Kronecker y constantes de primos](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c34_euler_kronecker_primos.tex:1>).
- **C35:** [Bendersky–Glaisher](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c35_bendersky_glaisher.tex:1>).
- **C36:** [Gauss, Khinchin, Lévy, Lochs y Wirsing](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c36_gauss_kuzmin.tex:3>).
- **C38:** [Unidad de Pell y reducciones tríticas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c38_pell.tex:1>).
- **C39:** [Familia de vacancias](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c39_vacancias.tex:26>).
- **F37:** [Perfil y sucesión de Feigenbaum](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/feigenbaum/c37_feigenbaum.tex:10>).
- **F38:** [Modo de Pell \(30+\sqrt{899}\)](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/feigenbaum/c38_modo_30.tex:1>).
- **C27:** [Realizaciones diferenciadas de \(-1/12\)](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/base_83/c27_body.tex:96>).
- **B43:** [Incidencia y coeficiente de polo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/barbero/c43_funcional_barbero.tex:28>).
- [Precedencia de los pesos dodecafásicos](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/barbero/c43_precedencia_dodecafasica_20260905.tex:1>).

### Resultados compartidos, conservados sin modificación

- [Evaluación espectral Euler–Maclaurin](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/VALORES_ESPECTRALES_RECALCULADOS.json>) y [su código](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_valores_espectrales.py>).
- [Replay de comprobaciones](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/RECOMPROBACION_CONSTANTES/REPLAY_RESULTADOS.json>) y [su código](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_constantes_corpus.py>). La excepción de Euler–Kronecker queda identificada arriba.
- [Intervalo racional de Catalán y otros controles prioritarios de Aclarar](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COMPROBACIONES_RESULTADOS_PRIORITARIOS.json>) y [su código](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_resultados_prioritarios.py>).
- [Certificado conservado de vacancias y criticidad](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/certificados/vacancias_criticidad.json>) y [su código original](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_vacancias_criticidad.py>). No se reejecutó su procedimiento masivo ni se sobrescribió el certificado.

El único cálculo nuevo de este cierre fue la conciliación focal indicada; el resto se obtuvo leyendo las fuentes y reutilizando controles ya efectuados. Esta es una entrega de evidencia para el trabajo conjunto, no otra edición del PDF.
