# Recuperación focal de masas REV.2 para la corriente gravitatoria de VII

## Actualización de integración — revisión 06

Los antecedentes recuperados en esta búsqueda ya se han utilizado en el
manuscrito autónomo. La composición espinorial está escrita con sus pruebas
en `../manuscrito/33_corriente_espinorial_y_densidad.tex`; determina el
funcional material s0[rho,Vc] por variación, con sector positivo conservado.
Las fuentes 32, 50 y 51 incorporan, respectivamente, la eliminación no
lineal diferenciada, el rebote y la solución homogénea explícita.
El informe siguiente conserva el recorrido de búsqueda y sus estados
intermedios como procedencia; no sustituye el estado actual de integración.

## Informe de búsqueda conservado

Fecha: 10 de septiembre de 2026. Alcance: memoria y representación espinorial,
acción de pantalla y corriente, evaluación cuadrática y amplitud de referencia.
Este informe es un desarrollo separado. No modifica manuscritos ni PDFs y no
declara la autonomía del artículo VII.

## 1. Identidad material y lecturas efectuadas

Raíz de la monografía, denominada **MAS** en los localizadores siguientes:

`/Users/ruben/Documents/New project/PUBLICACION_HMT/TEORIA_HOLOGRAFICA_INTEGRAL_MASA_HMT_MD_REV2_2026-08-20`

- PDF: `MAS/output/pdf/TEORIA_HOLOGRAFICA_INTEGRAL_DE_LA_MASA_HMT_MD_REV2_2026-08-20.pdf`.
- SHA-256 comprobado: `b56bb38d10b9a4f4d0de47b7da8010fb31a6e8e8684a3bfd4237e37d7a3dddfa`.
- Certificado leído completo: `MAS/gestion/CERTIFICADO_ENTREGA_PDF_REV2.json`;
  registra 479 páginas físicas.
- Fuente: `MAS/fuente/TEORIA_HOLOGRAFICA_INTEGRAL_DE_LA_MASA_HMT_MD_REV2.md`.
- SHA-256 comprobado de la fuente: `64d667148764a2bc40c2f6bef18b03035667edcc4797419f52d1c8e24251d42a`;
  coincide con el certificado.

Se leyeron completos los módulos `10_fundamento_y_ley_general.md` (597 líneas),
`11_ontologia_cuantica_de_la_particula.md` (518),
`14_topologia_exoticos_y_gravedad.md` (634),
`18_cuantica_estadistica_y_termodinamica.md` (472) y
`19b_corredor_excepcional_cuerdas_y_masas.md` (304). Se leyó además la sección
8 completa del ensamblado, líneas 1025–1216, sobre acoplamiento espectral.
La búsqueda textual de corriente, torsión, acción y espín se efectuó sobre el
ensamblado completo; la lectura matemática detallada fue la delimitada aquí,
no una auditoría de todas las filas del catálogo.

Se siguieron las remisiones de los módulos 14 y 18 y se leyeron íntegramente:

- `/Users/ruben/Documents/New project/HMT_OBRAS/OBRA_II/chapters/04_particula_rutas_feynman.tex` (183 líneas).
- `/Users/ruben/Documents/New project/HMT_OBRAS/OBRA_II/chapters/05_cinematica_cuantica.tex` (245).
- `/Users/ruben/Documents/New project/HMT_OBRAS/OBRA_II/chapters/11_cartan_bianchi_cosmologia.tex` (246).
- `/Users/ruben/Documents/New project/PUBLICACION_HMT/HMT_MD_GRANDES_PREGUNTAS_FISICA_2026-07-29_REV_3/manuscrito/capitulos/06_gravedad_mach.tex` (626).

Estas fuentes anteriores se utilizan por remisión concreta de la monografía;
no sustituyen la selección integral de 2249 páginas de la serie. Se mantuvieron
los antecedentes ya reunidos en VII y se leyó su sección `50_dilucion_y_rebote.tex`
completa antes de componer la amplitud.

La habilidad `verify-hmt-mass-law`, leída con su referencia canónica, terminó
en `PASS_SKILL_HMT_MASS_LAW`. El resolutor que envuelve aún presenta el integral
histórico de 2084 páginas: esa salida no cambia la selección vigente de la serie.
Se aplicó asimismo `preserve-hmt-continuity`: recuperar primero la composición,
distinguir tipos y conservar condiciones. Este PASS focal no certifica por sí
solo la corriente material ni la densidad cosmológica de VII.

## 2. Qué se recupera del material de masas

| Antecedente | Resultado material recuperado | Localizador |
| --- | --- | --- |
| Ruta, registro y carácter | La masa, la carga, la holonomía y la ocupación son lectores del mismo estado enriquecido; sus dominios se conservan al componerlos. | MAS, módulo 10 completo; módulo 11:3–74; módulo 18:3–22. |
| Holonomía y representación | Retornos fermiónicos de signo y representación de Clifford real con cuatro matrices explícitas; la representación permite derivar generadores infinitesimales. | Módulo 11:150–197; módulo 18:104–181; propietario `05_cinematica_cuantica.tex:178–223`. |
| Estado material | Núcleo positivo de acoplamiento, filtros de representación y persistencia, compresión espectral y normalización; un estado positivo normalizado evalúa el operador. | Ensamblado MAS:1025–1216; módulo 11:267–286; módulo 18:382–404 y 419–436. |
| Acción y torsión | Acción Palatini–Cartan–Holst con término material y ecuación de conexión; coincide con el tipo de corriente e inversas ya desarrolladas en VII/31. | Módulo 14:459–517; propietario `11_cartan_bianchi_cosmologia.tex:43–112`; VII/31:96–176 y 180–347. |
| Momento cuadrático y cosmología | Un medio no polarizado puede tener media de espín nula y cuadrado no nulo. Para número conservado, el término de fluido de espín se presenta como \(\xi_\gamma n^2\), con dilución \(a^{-6}\). | Propietario `11_cartan_bianchi_cosmologia.tex:205–230`. |

El corredor excepcional del módulo 19b:94–145 conserva una clasificación conjunta
de fibra de masa e incidencia excepcional y una escalarización por conmutación
en bloques irreducibles. Eso es pertinente para representar el estado; la dimensión
de un bloque no es por sí sola un número de fermiones por volumen.

## 3. Composición efectiva: Clifford → derivada de transporte → corriente

### 3.1 Generadores calculables desde las matrices recuperadas

El módulo 18:135–169 da

\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
R=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Z=\operatorname{diag}(1,-1),
\]
\[
\gamma_0=J\otimes I,\quad \gamma_1=R\otimes I,\quad
\gamma_2=Z\otimes R,\quad \gamma_3=Z\otimes Z,
\qquad \{\gamma_I,\gamma_J\}=2\eta_{IJ}I_4,
\quad \eta=\operatorname{diag}(-1,1,1,1).
\]

De estos operadores, sin fijar una masa ni una corriente por su valor objetivo,
se construye

\[
\mathbb B_{IJ}=\frac14[\gamma_I,\gamma_J].
\]

La anticomutación permite mover \(\gamma_K\) a través de los dos factores,
y da, por cancelación de los términos cúbicos,

\[
[\mathbb B_{IJ},\gamma_K]
=\eta_{JK}\gamma_I-\eta_{IK}\gamma_J.
\]

Aplicando esta derivación a \([\gamma_K,\gamma_L]/4\) se obtiene

\[
[\mathbb B_{IJ},\mathbb B_{KL}]
=\eta_{JK}\mathbb B_{IL}-\eta_{IK}\mathbb B_{JL}
-\eta_{JL}\mathbb B_{IK}+\eta_{IL}\mathbb B_{JK}.
\]

Es, por tanto, una representación explícita del álgebra de Lorentz. Para
\(i,j\in\{1,2,3\}\), \(\mathbb B_{ij}\) es antihermítico, mientras
\(\mathbb B_{0i}\) es hermítico respecto del producto positivo de la fibra.
La respuesta completa de VII/30c conserva ambas clases de variaciones; el
representante antihermítico aislado de VII/30b sólo representa la restricción
unitaria. Éste es un enlace concreto obtenido de la monografía.

Para una realización de conexión ya especificada, la matriz
\(\Omega_a=\tfrac12\omega_a^{IJ}\mathbb B_{IJ}\), con suma sobre ambos
órdenes de índices, proporciona el transporte espinorial local
\(U_a=\exp\Omega_a\). Su diferencial es calculable sin introducir una
matriz de corriente independiente:

\[
\partial_j U_a=
\int_0^1 e^{(1-t)\Omega_a}(\partial_j\Omega_a)e^{t\Omega_a}\,dt.
\]

La identidad se demuestra derivando la serie convergente de la exponencial;
la integral reproduce los factores factoriales de la suma de todas las
posiciones de la variación. En particular, en \(\Omega_a=0\) la derivada
es exactamente \(\partial_j\Omega_a\). Los productos sobre rutas se
diferencian por la regla ya impresa en VII/30e,
`vii:eq:derivada-incidencia-rutas`.

Esta composición especifica el cálculo una vez suministrada la conexión que
realiza la ruta y su levantamiento espinorial. La representación de Clifford
por sí sola no escoge el levantamiento global de todos los ciclos. Se conservan
las holonomías de signo y la identificación de fibras de esa realización.

### 3.2 Inserción en la incidencia y acción mínima de VII

Tomando la fibra \(\mathcal K=\mathbb C^4\) en la incidencia transportada
de VII/30e y los transportes anteriores, se obtiene una matriz efectiva
\(\mathsf C(\omega)\). En el dominio de rango fila completo,

\[
\mathsf L=\mathsf C\mathsf C^*,\qquad
y=\mathsf L^{-1}b,\qquad f_{\min}=\mathsf C^*y,
\quad E=\chi\langle b,y\rangle,\quad
\chi=\frac{112}{81\ell_m^2}.
\]

La extensión y el peso son los del problema mínimo recuperado de pantalla.
Sus derivadas de conexión reciben las matrices \(\mathbb B_{IJ}\) mediante
la fórmula precedente, manteniendo el orden de los transportes. La acción
\(S_{\min}=\mathfrak a_mE\) determina

\[
s_j=4\mathfrak a_m\chi\operatorname{Re}
 \langle y,(\partial_j\mathsf C)f_{\min}-\partial_jb\rangle
-2\mathfrak a_m(\partial_j\chi)\langle b,y\rangle
-2(\partial_j\mathfrak a_m)E,
\qquad
\sigma=\mathsf M_{\rm cel}^{-1}s.
\]

Se conservan el dato de frontera, su dependencia de conexión, la normalización
de acción, la escala y el emparejamiento celular. La matriz de incidencia
\(\mathsf C\) no es la matriz de emparejamiento \(\mathsf M_{\rm cel}\).
La fórmula es una composición operatoria, no una inferencia desde una masa
numérica o desde el nombre «espín».

La fuente de masas facilita una representación de la fibra y el formalismo de
preparación/acoplamiento; el problema mínimo de VII selecciona la extensión
para cada frontera. Son aportaciones complementarias. La identificación del
protocolo de preparación de masas con un dato concreto \(b\) de la pantalla
gravitatoria debe conservar el mapa y el estado correspondientes; normalizar
la traza de un núcleo de preparación no equivale a fijar una densidad espacial.

### 3.3 De corriente a respuesta de Cartan

La corriente anterior se inserta en la convención de VII/31,

\[
D_\omega(P_\gamma\Sigma)=\kappa c\,\sigma,
\qquad
P_\gamma^{-1}=
\frac{\gamma^2}{1+\gamma^2}(-\star+\gamma^{-1}I).
\]

Las inversas impresas determinan la torsión y la contorsión desde esa
corriente y la cotétrada. Para materia afín en la contorsión, el propietario
reunido en VII/31 prueba

\[
\mathcal L_{\rm spin}^{\rm eff}
=-\frac14K_*^{IJ}\wedge\sigma_{IJ}.
\]

Para la acción de transporte exponencial, \(\sigma\) depende en general
de la conexión. Se mantiene entonces esa dependencia en la ecuación de
Cartan; la eliminación cuadrática afín no puede aplicarse retirando dicha
condición. El obstáculo preciso no es «no hay representación» ni «no hay
corriente calculable»: es justificar el tipo de dependencia material de la
acción efectivamente elegida antes de aplicar esa particular eliminación.

## 4. Espín, segundo momento y amplitud cosmológica

### 4.1 Un control que la monografía hace necesario

Con orientación cíclica, definamos

\[
T_1=-\tfrac12\gamma_2\gamma_3,\quad
T_2=-\tfrac12\gamma_3\gamma_1,\quad
T_3=-\tfrac12\gamma_1\gamma_2,
\qquad S_i=i\hbar_{\rm int}T_i.
\]

Se tiene \(T_i^*=-T_i\), \(T_i^2=-I/4\) y
\([T_i,T_j]=\epsilon_{ijk}T_k\). Luego

\[
[S_i,S_j]=i\hbar_{\rm int}\epsilon_{ijk}S_k,
\qquad \sum_iS_i^2=\frac34\hbar_{\rm int}^2I_4.
\]

Además, \(e^{2\pi T_i}=-I\), \(e^{4\pi T_i}=I\), por la fórmula
\(e^{\theta T_i}=\cos(\theta/2)I+2\sin(\theta/2)T_i\).
Así se reúnen la representación recuperada y los retornos de signo sin
usar la masa para seleccionar el espín.

Para el estado de prueba no polarizado \(\varrho=I_4/4\),

\[
\operatorname{Tr}(\varrho S_i)=0,
\qquad
\sum_i\operatorname{Tr}(\varrho S_i^2)
=\frac34\hbar_{\rm int}^2>0.
\]

La prueba procede de las trazas nulas de los generadores y de su Casimir.
El estado anterior es un testigo de la distinción entre primer y segundo
momento, no la elección del estado cosmológico. Coincide con la distinción
explícita del propietario `11_cartan_bianchi_cosmologia.tex:205–219`.
Al formar una densidad cuadrática, sustituir el segundo momento por el
cuadrado de la media borraría una contribución que la fuente conserva.

Se comprobaron por multiplicación racional exacta 92 identidades: 16 de
Clifford, 24 de acción sobre vectores, 36 de cierre de Lorentz, seis de
transposición, tres cuadrados, tres conmutadores cíclicos, tres trazas y el
Casimir. Es una comprobación finita posterior de las matrices recuperadas,
sin evaluación de constantes ni de \(s_0\). No constituye una auditoría
global ni sustituye las pruebas algebraicas anteriores.

### 4.2 Identidad concreta que enlaza con VII/50

El propietario citado por la monografía presenta

\[
H^2+\frac{k}{a^2}
=\frac{8\pi G}{3}(\rho-\xi_\gamma n^2)+\frac\Lambda3,
\]

y conserva expresamente la normalización del transductor de espín en
\(\xi_\gamma\) (`11_cartan_bianchi_cosmologia.tex:218–229`).
Para \(N\) conservado, volumen comóvil \(V_c\) y \(a\) adimensional,
\(V(a)=a^3V_c\) da

\[
n(a)=\frac{N}{V_c}a^{-3},\qquad
\rho_{\rm s}(a)=\xi_\gamma\left(\frac{N}{V_c}\right)^2a^{-6},
\qquad
s_0=\xi_\gamma\left(\frac{N}{V_c}\right)^2.
\]

Equivalente en una referencia cualquiera:
\(s_0=\xi_\gamma n_{\rm ref}^2a_{\rm ref}^6\).
La prueba es la sustitución de la ley de volumen y conservación del número.
La identificación con la memoria de VII/50 conserva su igualdad independiente
\(M_n=\varphi^{-2n}=(a_n/a_{\rm ref})^{-6}\).

Más generalmente, si la acción efectiva y el estado material ya determinan
\(U^{\rm phys,spin}\), la comparación con el signo de VII/50 exige

\[
s_0=-a_{\rm ref}^6\,
 \langle U^{\rm phys,spin}_{\mu\nu}u^\mu u^\nu\rangle_{\rm ref},
\qquad g(u,u)=-1,
\]

en una realización homogénea donde esa contribución sea negativa. La
esperanza significa la evaluación clásica, de conjunto o cuántica que
especifique la acción material; sus dominios no se intercambian. La positividad
de \(s_0\) exige comprobar el signo de esa contracción. La corriente de espín,
su respuesta cuadrática y su variación métrica son etapas sucesivas; el
Casimir positivo por sí solo no fija el signo gravitatorio ni su coeficiente.

Ésta es la identidad objetivo precisa: evaluar la contracción de la acción
efectiva en el estado de referencia, o equivalentemente \(\xi_\gamma\) y
\(N/V_c\) en la realización de fluido de espín que usa esa misma acción.
Una vez evaluada, VII/50 ya propaga la amplitud y determina el umbral
\(a_b^{3(1-w)}=s_0/\rho_0\) bajo sus hipótesis conservadas.

## 5. Alcance positivo y siguiente operación concreta

La monografía sí aporta operadores que hacen avanzar VII: la representación
matricial de espín, el clasificador conjunto de la sección, el formalismo
de estado/preparación y la conexión explícita entre cuadrado de espín y
dilución cosmológica. Los propietarios citados contienen además acción
gravitatoria, variación y fluido de espín. No corresponde describir ese
material como una lista de masas desprovista de estructura.

En las fuentes completas seguidas aquí, la acción gravitatoria conserva el
término material \(S_m\) con su corriente variacional; la ecuación de Dirac
declara la representación y el operador covariante. No se encontró en esos
propietarios una evaluación contigua del bilineal axial o de la acción de
pantalla para un estado cosmológico especificado que produjera el valor de
\(\xi_\gamma(N/V_c)^2\). Esta observación delimita esta búsqueda, no declara
ausencia en todo el corpus ni invalida la representación recuperada.

La continuación operativa consiste en componer los generadores anteriores
con la realización de conexión de VII, evaluar \(b\) y su preparación en
la incidencia de 30e, y diferenciar esa misma acción respecto de conexión
y métrica. Si la realización elegida es fermiónica afín, se conserva su
bilineal y su segundo momento antes de aplicar 31. Si es una acción de
holonomía no afín, se resuelve su ecuación de contorsión conservando la
dependencia. Ninguna de las dos vías selecciona el estado para imponer
un rebote.

Los números de celdas (81), rutas (324), familias (56), multisecciones (13),
masas catalogadas (471) y modos de una pantalla microcanónica no son un
número físico de fermiones por volumen. Tampoco el \(s_0=0\) del módulo
10, en la recurrencia de trazas armónicas, es la amplitud torsional de VII:
allí designa el término de índice cero de \(q_-^n-q_+^n\).

Procedencia: matrices, representaciones, acción gravitatoria y fluido de
espín son **RESULTADO_RECUPERADO**; las derivadas y la composición aquí
reunidas son **FORMALIZACION_NUEVA** con sus premisas explícitas. El control
de 92 identidades es **CERTIFICADO_NUEVO** focal. Ninguno de estos estatutos
declara una amplitud física evaluada, ni cambia los alcances de los
propietarios previos.
