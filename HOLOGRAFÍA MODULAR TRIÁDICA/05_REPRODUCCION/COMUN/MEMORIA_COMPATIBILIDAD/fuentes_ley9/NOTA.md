# Memoria cronológica, balance y respuesta de vacancias

Nota de desarrollo — 22 de septiembre de 2026. No modifica las publicaciones.

## Procedencia y alcance

Se reúnen consecuencias del calendario de vacancias ya definido en HMT y de
sus lectores. La arquitectura APP–TRIT–TPK, las regiones, el retorno nonádico,
el registro K y la interpretación autoral son preexistentes. Las pruebas que
siguen son una elaboración matemática focal; no se reivindica prioridad
histórica para los teoremas generales sobre palabras mecánicas o información.
La búsqueda de procedencia ha sido focal, no una auditoría de todo el corpus.

El punto de corte de esta nota es el factor simbólico de capacidad. Se recibe
la razón interna 3^6/10^3=729/1000 y su calendario ya construido; se estudia
qué conserva y qué pierde una lectura posterior. No se vuelve a generar ni
a seleccionar pi, phi, e o alfa mediante logaritmos o constantes externas.
El alcance no se extiende automáticamente al estado TPK completo.

Propietarios consultados:

- `output/DOBLE_PROYECCION_HOLOGRAFICA_CRISTAL_TEMPORAL_APERIODICO_MONOGRAFIA_AUTOSUFICIENTE/manuscrito/generated/cristal_relojes_sincronizacion.tex`,
  secciones de capacidad, reloj inducido (línea 931), levantamiento (813)
  y memoria integrada (2253).
- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/03/ES/source/manuscrito/sections/03b_vacancias_prefactor.tex`,
  palabra mecánica, polarización, corriente y modo trítico.
- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/01/ES/source/sections/electron.tex`,
  plano principal y álgebra electrónica local (267).
- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/10/ES/source/libro/01_acoplamiento.tex`,
  referencia cíclica de K e identificación de operadores (197–350).
- `output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/10/ES/source/antecedentes_vii/sections/v_transduccion_termica.tex`,
  recuperación de fibra, actualización reversible y borrado (1–125).

## 1. Objeto, medida y dos lectores

Sea δ=log_10(10/9), pendiente del calendario de capacidad, y sea θ una fase
uniformemente distribuida en [0,1). Esta medida describe incertidumbre sobre
el origen de lectura, no aleatoriedad del mecanismo. Definimos

    z_j(θ)=floor((j+1)δ+θ)−floor(jδ+θ),
    W_n(θ)=(z_0(θ),…,z_{n−1}(θ)),
    B_n(θ)=sum z_j(θ).

W_n conserva la cronología y B_n conserva sólo el balance. Para una fase
exacta conocida y una regla exacta conocida, ambos objetos son deterministas;
las entropías aquí se refieren expresamente al conjunto de fases posibles.

La telescopía da B_n=floor(nδ+θ). Por tanto, B_n sólo admite floor(nδ)
y ceil(nδ). Los puntos {−jδ}, j=0,…,n, dividen el círculo en n+1 intervalos
de fase. Cada intervalo porta una palabra distinta de longitud n. En efecto,
los prefijos acumulados floor(kδ+θ), k=1,…,n, son monótonos en θ, y cada
frontera cambia uno; la palabra reconstruye todos esos prefijos.

Los extremos tienen medida cero; elegir convención semiabierta resuelve
su asignación sin alterar las entropías.

## 2. Información creciente con tasa entrópica nula

Sean ℓ_0,…,ℓ_n las longitudes de los intervalos de fase y

    H_n = −sum ℓ_j log_2 ℓ_j.

**Proposición.** Se cumplen simultáneamente

    H_n → ∞,             H_n/n → 0.

**Demostración.** La cota superior es H_n≤log_2(n+1). Si
ℓ_max(n)=max ℓ_j, entonces H_n≥−log_2 ℓ_max(n). La pendiente δ es irracional:
si δ=p/q, con q>0, entonces (10/9)^q=10^p, imposible por la valuación
del primo 3. Por irracionalidad de δ,
los puntos de la órbita son densos. Sus particiones sucesivas tienen malla
máxima tendente a cero: para cada ε>0 existe un tramo finito ε-denso,
y los tramos posteriores sólo subdividen. Por tanto la cota inferior
diverge. La cota superior dividida por n tiende a cero. QED.

No se ha demostrado H_n=log_2(n+1): las palabras no son equiprobables.
Tampoco se ha afirmado una ley asintótica logarítmica exacta sin condiciones
diofánticas adicionales.

La entropía topológica del factor es igualmente cero porque
log(n+1)/n→0. La información del bloque y su tasa son cantidades diferentes.
El crecimiento del archivo de una trayectoria conocida no equivale por sí
solo a creación de información estadística independiente.

## 3. Información cronológica invisible al balance

**Corolario.** Para el mismo conjunto de fases,

    H(W_n | B_n) = H_n − H(B_n) ≥ H_n − 1 → ∞.

**Demostración.** B_n es función de W_n, por lo que la regla de la cadena
da la igualdad. Su soporte tiene dos elementos, así que H(B_n)≤1 bit.
Se aplica la proposición anterior. QED.

La afirmación no dice que cada balance concreto tenga la misma incertidumbre,
sino que la entropía condicional promedio diverge. Tampoco dice que esa
información quede oculta al estado enriquecido completo: si la memoria
retenida recupera W_n, entonces H(W_n|B_n,M_n)=0.

Además, por cardinalidad, al menos una de las dos fibras de B_n contiene
al menos ceil((n+1)/2) palabras. Es una cota combinatoria distinta de la cota entrópica.

Este resultado concreta la distinción entre valor y genealogía en este lector:
dos balances posibles no agotan las historias temporales compatibles.

## 4. Corriente centrada: balance acotado y actividad persistente

Se conserva el lector ya definido en el artículo III:

    J_j = z_j − δ,           sum_{j=0}^{n−1} J_j = B_n−nδ.

En consecuencia, |sum J_j|<1 para toda ventana. A la vez,

    lim (1/n) sum J_j = 0,
    lim (1/n) sum J_j² = δ(1−δ) > 0.

**Prueba.** z_j²=z_j y B_n/n→δ por la cota de discrepancia. Se expande
(z_j−δ)²=z_j(1−2δ)+δ². La sustitución da la segunda identidad.
Es válida para cualquier fase y no exige un promedio aleatorio. QED.

Así, balance acumulado acotado, actividad cuadrática positiva y tasa de
entropía cero son compatibles. Ninguna de estas identidades supone energía
gratuita ni carga elemental igual a los dos valores centrados de J.

Si una realización dimensional ya establecida toma I_j=(u_Q/t_0)J_j,
se obtiene I_rms²=(u_Q/t_0)² δ(1−δ). Si cada I_j se mantiene durante
un intervalo de duración t_0, este promedio discreto coincide con el promedio
temporal. Como prueba física posterior, una carga resistiva ideal R>0 tendría potencia media
R(u_Q/t_0)² δ(1−δ)>0. Es una predicción del modelo compuesto con esa carga,
no una derivación de R ni del dispositivo desde el calendario.

## 5. Espectro de la corriente y orientación

La función de observación es f(θ)=1_[1−δ,1)(θ)−δ y
J_j=f(θ+jδ). Sus coeficientes de Fourier, para m≠0, son

    a_m=(exp(2π i mδ)−1)/(2π i m),
    |a_m|²=sin²(πmδ)/(π²m²),       a_0=0.

Se obtiene integrando la indicatriz sobre su intervalo. Parseval da
sum_{m≠0}|a_m|²=δ(1−δ), coherente con la actividad cuadrática.
Las frecuencias temporales son mδ módulo 1. La correlación estacionaria
con fase uniforme queda determinada por esas intensidades; éstas no
contienen la fase inicial. Una traslación multiplica a_m por una fase
unitaria y la inversión temporal intercambia las frecuencias opuestas.

Por ello, medir únicamente potencia espectral tampoco recupera la orientación
ni el origen temporal. Se necesita una lectura sensible a fase o una
referencia marcada. Esta deducción no identifica automáticamente tal
referencia con K ni identifica los ritmos simbólicos con un experimento.

### 5.1. K distingue transportes de igual intensidad espectral

La propiedad cíclica ya demostrada del registro K permite una consecuencia
finita independiente del espectro anterior. En V=R^12, sea S el desplazamiento
(Sx)_i=x_{i+1} y O_K=(K,SK,…,S^11K), invertible por el teorema de referencia
cíclica del manuscrito. Para cualquier H real que conmuta con S, pongamos
y_+=HK e y_−=HᵀK.

**Proposición.** Las doce intensidades de Fourier de y_+ e y_− coinciden.
Sin embargo, y_+=y_− si y sólo si H=Hᵀ. Cada respuesta vectorial completa,
junto con K y la orientación de S, recupera su operador.

**Prueba.** H es circulante; sus multiplicadores de Fourier son λ_m y los
de Hᵀ son sus conjugados. Por ello ambas respuestas tienen intensidades
|λ_m|²|K̂_m|². Si sus vectores coinciden, (H−Hᵀ)K=0. La conmutación implica
que H−Hᵀ anula también S^jK para todo j. Esos vectores forman una base,
así que H−Hᵀ=0. La recuperación es H=O_{y_+}O_K^−1, y análogamente para
Hᵀ. QED.

En particular, los desplazamientos S y S^−1 dan respuestas de igual espectro
de potencia, pero distintas. Las autocorrelaciones exactas publicadas dan

    ||SK−S^−1K||² = 2(||K||²−<K,S²K>) = 2175744 > 0.

El script recupera de ambas respuestas los coeficientes e_1 y e_11,
respectivamente, por inversión racional de O_K. K se usa aquí después de
su generación, como referencia marcada, nunca como entrada retrospectiva.
Una intensidad espectral o un balance escalar no sustituye esa respuesta
vectorial. Este corolario describe el portador cíclico de doce componentes;
no identifica S con la dinámica enriquecida completa ni convierte por sí
solo S↔S^−1 en conjugación física de carga. Para H general, la transposición
tampoco significa inversión temporal; en el caso S sí coincide con S^−1.

## 6. Enlace operatorio electrónico ya presente

La incidencia entre las fibras suma/producto de APP sobre D9³ define C.
Su vector m_ph=(1,−1,0)^3 satisface

    C m_ph = Cᵀ m_ph = −m_ph/2.

El calendario inducido recorre los regímenes del mismo selector trítico;
la incidencia selecciona el plano principal de singularidad 1/2. En él,

    P=diag(1,0),
    Q=[[1/4,√3/4],[√3/4,3/4]],
    J=(4/√3)[P,Q],        J²=−I.

Se recupera así una relación efectiva entre organización temporal y bloque
electrónico, conservando el selector, sus etiquetas y la incidencia. La
identidad no equivale a asignar directamente ±carga elemental a z−δ.
La representación de carga y la realización dimensional conservan sus
operadores propios.

## 7. Información y energía: composición correcta

El desarrollo térmico del corpus ya establece

    H(X|q(X),M(X))=0

cuando el lector enriquecido tiene inversa, y conserva H(X) bajo una
actualización biyectiva. Por tanto, la posibilidad anterior de H_n creciente
y tasa cero no contradice ese desarrollo ni las identidades de Shannon.

El trabajo de borrado depende de la información accesible que se retiene.
En el régimen ideal isotermo de memorias lógicas degeneradas y en el límite
asintótico apropiado, el coste por copia con información lateral es
k_B T ln(2) H(X|M). Si X se recupera desde M, la contribución lógica ideal
puede ser cero. El transporte físico, la lectura, el control y el ciclo
completo necesitan balances propios; h_top=0 no los hace gratuitos.

La composición de interés es concreta: cronología → registro de frontera →
lector de corriente/estado → memoria retenida → balance térmico. La presente
nota desarrolla los dos primeros lectores y sus consecuencias informacionales;
no certifica un dispositivo físico completo ni modifica la tesis de las
constantes.

## 8. Comprobación reproducible y falsadores

`python3 verificar_conteo.py --output resultados.json` calcula las particiones
para n=9,108,1000,10000 con 70 y 100 cifras de trabajo para las particiones.
Las entropías se evalúan en doble precisión; la concordancia no certifica
70 cifras de H_n. Verifica las cotas entrópicas y la telescopía, y enumera las palabras completas para
n≤108. También reconstruye exactamente las incidencias de los 729 triples
APP, comprueba los dos modos C m_ph y Cᵀ m_ph, los nueve autovectores del Gram,
la norma al cuadrado del conmutador, ||[P,Q]||²=3/16, y J²=−I.
El cuadrado del propio conmutador en ese plano es −3I/16. No comprueba por ello
la masa o la carga físicas. El análisis de fases es numérico posterior,
no prueba del límite infinito.

La comprobación cíclica recibe el K ya publicado, verifica su determinante
y las autocorrelaciones con aritmética entera/racional, y recupera los dos
desplazamientos desde sus respuestas. Su alcance es la observación posterior
del registro, no una nueva generación de sus doce coordenadas.

Falsadores locales: una tercera posibilidad de balance; una colisión de
palabras en intervalos distintos; fallo de telescopía; H_n superior a
log_2(n+1); confusión del factor simbólico con todo TPK; atribuir coste
térmico cero sin fijar memoria lateral y realización.

## Referencias externas de contraste

- C. E. Shannon, *A Mathematical Theory of Communication* (1948).
  https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
- C. H. Bennett, *Logical Reversibility of Computation* (1973).
  https://doi.org/10.1147/rd.176.0525
- L. del Rio et al., *The thermodynamic meaning of negative entropy*,
  arXiv:1009.1630, especialmente apéndice E.
  https://arxiv.org/abs/1009.1630

Las referencias externas identifican resultados generales de comparación.
No se usan como entradas numéricas para generar las constantes HMT.
