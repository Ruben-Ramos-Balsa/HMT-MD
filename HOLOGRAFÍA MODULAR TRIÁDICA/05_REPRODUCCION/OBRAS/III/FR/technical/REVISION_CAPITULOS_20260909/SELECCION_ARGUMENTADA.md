# Selección argumentada de los capítulos propuestos

## Alcance de esta lectura

Fecha: 9 de septiembre de 2026. Se han contrastado los cuerpos pertinentes del integral de 2.249 páginas con el artículo I de 117 páginas, la revisión de trabajo 05 del artículo II de 182 páginas y el artículo III de 140 páginas. La revisión 05 de II se consulta como testigo de trabajo, sin sustituir silenciosamente la revisión 04 del índice público de la serie.

Los materiales aquí identificados son resultados recuperados y conexiones expositivas entre desarrollos existentes. Esta selección no acredita prioridad histórica, no vuelve a certificar todas sus pruebas y no constituye una nueva edición de los PDFs. Las condiciones de los teoremas citados se conservan como figuran en sus fuentes.

El envío a «Ley 9 puertas» permanece suspendido por indicación expresa del autor. No se ha realizado ninguna comunicación con esa tarea ni se han modificado sus archivos.

Las páginas del integral son las impresas; en el archivo PDF su posición es una unidad mayor. Los localizadores de fuente que siguen se resuelven desde:

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/`

## 1. Prioridades concretas para el artículo III

### 1.1. De la distribución de vacancias a una polarización discreta

El §58.4.2, p.1055 del integral, define, para la fase \(\theta\) y la pendiente \(\delta_{\rm vac}\),

\[
z_n(\theta)=
\lceil(n+1)\delta_{\rm vac}+\theta\rceil
-\lceil n\delta_{\rm vac}+\theta\rceil,
\]

\[
P_N(\theta)=
\sum_{n=0}^{N-1}(z_n(\theta)-\delta_{\rm vac})
=\lceil N\delta_{\rm vac}+\theta\rceil-\lceil\theta\rceil-N\delta_{\rm vac},
\qquad |P_N(\theta)|<1,
\]

\[
J_N(\theta)=P_{N+1}(\theta)-P_N(\theta)
=z_N(\theta)-\delta_{\rm vac}.
\]

La importancia para III es precisa: el calendario de vacancias no proporciona únicamente una frecuencia; también determina un funcional acumulado acotado y su diferencia temporal. El artículo puede pasar así de la distribución simbólica a una descripción explícita del transporte.

La discrepancia acotada ya aparece en I, p.58, y en III, p.58 impresa. La mejora no consiste en volver a demostrar esa cota, sino en reunir su formulación como polarización y corriente aritméticas antes de los capítulos de respuesta constitutiva.

La realización electromagnética debe escribir la escala de carga y la escala temporal que emplea. La denominación de corriente no sustituye el mapa entre este funcional escalar, los canales orientados y los observables dimensionales. Este enlace debe exponerse antes de afirmar que ambos operadores son equivalentes.

**Destino propuesto:** inicio del §15 de III, conservando la prueba de vacancias en su lugar anterior y remitiendo a ella con un localizador interno.

**Fuente:** `manuscrito/sections/md/06l_vacancias_corriente_rev11.tex:106–136`.

### 1.2. Modo trítico, prefactor electrónico e incidencia \(90/120\)

El §58.5.2, p.1056, presenta

\[
m_{\rm ph}=(1,-1,0)^3,\qquad
C^{(3)}m_{\rm ph}=(C^{(3)})^*m_{\rm ph}
=-\frac12m_{\rm ph}.
\]

Con \(s=1/2\),

\[
1-s^2=\frac34=\frac{90}{120},\qquad
\|[P_{\Sigma,3},P_{\Pi,3}]\|=\frac{\sqrt3}{4}.
\]

I, pp.83–84, ya contiene el espectro y el modo trítico. III desarrolla la respuesta
\[
F(T)=(I-T^{90})(I-T^{120})^{-1}
\]
y sus valores propios en el intervalo \((3/4,1)\).

El refuerzo pertinente es reconstruir la relación entre el modo de APP–TRIT, el defecto espectral y el calendario de las dos longitudes. No debe reducirse a que dos fracciones coinciden: los espacios, las acciones y los mapas conservados deben permanecer visibles. Tampoco debe identificarse la norma del conmutador con el operador constitutivo completo.

**Destino propuesto:** articulación entre los antecedentes del núcleo y la definición del operador constitutivo de III. La demostración del prefactor electrónico conserva su residencia principal en I.

**Fuente:** `manuscrito/sucesor_102/espirales/cap58_electron_lector_helicoidal.tex:20–42`.

### 1.3. Un antecedente angular, dos evaluaciones funcionales

El §49, pp.884–887, distingue la respuesta constitutiva del determinante:

\[
T=q_+P_++q_-P_-,
\qquad q_\pm=e^{-(A_{\rm rad}\pm C^*_{\rm rad})},
\]

\[
F(T)^2,\qquad
F(z)=\frac{1-z^{90}}{1-z^{120}},
\qquad
D_A=\det T=q_+q_-=e^{-2A_{\rm rad}}.
\]

En III, \(\mathcal V\) denomina \(F(T)\), mientras que sus respuestas cuadráticas proporcionan las coordenadas constitutivas. Esta diferencia de notación debe declararse al incorporar el pasaje; no se deben confundir \(F(T)\) y \(F(T)^2\).

La involución \(C^*\mapsto-C^*\) intercambia los canales. El determinante permanece invariante, las dos respuestas cuadráticas se intercambian y la impedancia normalizada se invierte. Es una relación más informativa que reunir constantes en una tabla: especifica qué transformaciones distingue cada evaluación del mismo operador.

El capítulo electrodébil continúa con las firmas angulares \((94,-1)\) y \((95,-1)\), de donde obtiene, en la sección de escala y refinamiento común declarada,

\[
\frac{m_W^\angle}{m_Z^\angle}=e^{-A_{\rm rad}},
\qquad
\sin^2\theta_W^{\rm OS}=1-D_A.
\]

**Decisión editorial propuesta:** incorporar en III la relación funcional y su comportamiento bajo conjugación. La derivación completa de Weinberg requiere presentar también la procedencia de las firmas, la cancelación de refinamientos y el reconocimiento gauge. No debe añadirse como una fórmula aislada ni convertir III en un tratado electrodébil por acumulación. Si se decide incluir esa consecuencia completa, sus dependencias pasarán al mismo artículo; en otro caso, su residencia será el trabajo electrodébil o de masas.

**Fuentes:** `colaboracion/parte_iii/source/public_final/constantes/c41_electrodebil_body.tex:3–118` y `colaboracion/parte_iii/source/public_final/constantes/c41_determinante_vacio.tex:1–26`.

## 2. Contenido ya incorporado que debe conservarse

### 2.1. Clausura entre los sectores nulo y material

El §58.3, p.1053, relaciona el modo uniforme del calendario y la sección electrónica mediante un mapa de rango uno. I, p.94, ya incorpora ese mapa, ecuación `el-rango-uno`. La amplitud electrónica sigue procediendo de su construcción y no del mero hecho de representarla sobre el modo uniforme.

No se propone añadir otra derivación del electrón al III. Sí conviene citar internamente esta distinción al explicar por qué una respuesta del vacío y una sección material pueden compartir soporte sin ser el mismo objeto.

**Fuente:** `manuscrito/sections/md/06ka_clausura_nulo_material_electron_rev3.tex:13–106`.

### 2.2. Producto \(G\hbar\) y escala de área

II, §16.1–16.2, p.130, ya desarrolla

\[
G_a\hbar_a=\vartheta^\circ_{108}c_{\rm int}^{5}t_0^2,
\qquad
\ell_P^2=\vartheta^\circ_{108}\ell_0^2,
\]

junto con la transformación contragrediente de \(G_a\) y \(\hbar_a\). El selector \(\vartheta^\circ_{108}=(54/\pi)^2\) utiliza el radio gravitatorio reducido de la fuente. La convención con un factor \(2\) no se intercambia silenciosamente.

Este desarrollo conserva su residencia en II. III puede explicar qué escala recibe cuando evalúa un operador de área, sin duplicar toda la construcción gravitatoria.

**Fuentes:** capítulos50–51; II `manuscrito/sections/10_gravedad.tex:24–66`.

### 2.3. Área, capacidad e incidencia de Barbero

II, §15, pp.122–129, ya distingue el corte de81 trits, la capacidad \(81\log3\) para el estado declarado y los dos sectores colectivos90/120. En particular,

\[
N=N_{90}+N_{120},\qquad D=90N_{90}+120N_{120},
\]

\[
N_{90}=4N-\frac D{30},\qquad
N_{120}=\frac D{30}-3N.
\]

III, §18, pp.121–125 impresas, recupera el funcional de Barbero a partir de los canales constitutivos. La conexión entre ambos artículos debe hacer visible que recuperación de canales, ocupaciones sectoriales y lectura de área son etapas distintas de una misma composición.

No se propone reproducir íntegramente en III las pruebas que II ya dedica al área. Si un teorema de III utiliza una de ellas como antecedente indispensable, se incorporará su dependencia exacta para mantener la autonomía.

**Fuentes:** `constantes/c43_area_incidencia.tex`, `barbero/c43_operador_area.tex`; II `manuscrito/sections/09_area.tex:45–232`.

### 2.4. Reducción \(11\to3\to1\), orientación y transporte hacia Witt

II, §14, pp.115–124, ya contiene selección variacional, orientación, recalibración y descomposición polar. El integral las desarrolla en §§20.1.5–20.1.10, pp.537–542.

No debe presentarse como un resultado ausente de II ni añadirse una tercera explicación equivalente a III. Su función es sostener el paso desde la información angular al espacio de incidencia. La futura ampliación excepcional debe conservar ese antecedente.

**Fuentes:** `manuscrito/sections/hmt/delta_297/16c_entrelazador_dodecafase_witt.tex`; II `manuscrito/sections/08j_enlace_angular_witt.tex`.

### 2.5. Unidad imaginaria y defecto \(-1/12\)

La familia de regímenes \(J^2=-I\) ya está expuesta en el núcleo de I. III, p.118, añade el entrelazamiento \(CW=WJ\), y en esa misma página conserva

\[
\frac1{12}\operatorname{Tr}(P_3-P_4)=-\frac1{12}.
\]

La recuperación de esos valores no justifica añadir todas sus representaciones históricas en cada artículo. Deben incorporarse las que intervengan efectivamente en el argumento.

## 3. Ampliación excepcional de especial interés

El integral, §§22.1 y22.3.2, pp.585–595, contiene una segunda presentación de Moonshine mediante un orbifold de orden3:

\[
V_{(3)}=\operatorname{Orb}_{\mathbb Z/3}
(V_{N_v},\widehat g_c)\cong V^\natural.
\]

La construcción conserva el vecino de Leech, la acción de orden3, los datos del levantamiento y su tipo. El teorema22.13 compara esta presentación con la de orden2:

\[
\Phi_{23}=\phi_2^{-1}\phi_3:
V_{(3)}\longrightarrow V_{(2)}.
\]

La comparación conserva producto de vértice, gradación y trazas; depende de los isomorfismos elegidos. La vía de orden2 ya aparece en I p.107, II p.156 y III p.89 impresa. En los cuerpos cotejados no está desarrollada esta comparación de ambas presentaciones.

Su relevancia es concreta: permite seguir la estructura ternaria hasta la presentación excepcional y comparar el resultado con la construcción de orden2. También da un lugar natural al cociente de funciones eta de nivel3 y a \(t_3\), sin introducir otra lista de coincidencias numéricas.

**Destino propuesto:** ampliación focal del corredor excepcional de I o artículo excepcional autónomo. II y III conservarán los antecedentes necesarios para sus propios teoremas; no se triplicará por defecto toda la prueba.

**Fuente:** `colaboracion/partes_i_ii/source/public/residencias/capitulo_22_voa_leech_moonshine.tex:1–127`.

## 4. Dimensión11: continuidad ya identificada para un artículo posterior

El capítulo89, pp.1338–1343, debe leerse junto con §25.13, pp.638–640. Este último no ofrece únicamente un cotejo de dimensiones: presenta el morfismo algebraico y la prueba de la equivalencia cocientada.

El registro \(K\) interviene mediante

\[
u_K=P_3P_{11}K,\qquad \ell_K=\mathbb Ru_K,
\qquad
P_{10}=P_{11}-\frac{u_Ku_K^{\mathsf T}}{\|u_K\|^2}.
\]

Así, los pasos \(12\to11\to10\) tienen operaciones determinadas: retirar el modo uniforme y la dirección polarizada por \(K\). El cociente reticular

\[
e_+^\perp/\mathbb Ze_+\cong\Lambda_{24}
\]

tiene otra fuente y otra categoría. Ambos se coordinan, con el intercambio momento–enrollamiento, en \(\mathcal R_M^{\rm alg}\).

La revisión05 de II ya desarrolla la dualidadT desde la elipse y su carta dimensional, incluidas la conjugación unitaria y la memoria del cambio de sección. Sus conclusiones reservan explícitamente teoríaM a un trabajo posterior. Por tanto, no es necesario reconstruir allí ese antecedente.

**Propuesta de articulación posterior:**

1. núcleo común APP–TRIT–TPK, con todas las dependencias empleadas;
2. incidencia marcada por \(K\) y construcción de las reducciones;
3. retículo de Leech, plano hiperbólico y cociente isotrópico;
4. elipse, radio normalizado y dualidad momento–enrollamiento;
5. persistencia extendida y superficies o volúmenes de mundo;
6. terna espectral, supercarga, campos y realización undecadimensional.

El texto distingue el isomorfismo algebraico demostrado del reconocimiento físico mediante \(\Xi_M\), cuyas condiciones declara expresamente. Conservar esta distinción es parte de reproducir fielmente el alcance de la fuente, no una eliminación de su construcción. La lectura de estos capítulos no autoriza a declarar por sí sola completada toda la dinámica física.

**Fuentes:** `colaboracion/partes_i_ii/source/public/residencias/capitulo_25_pantallas_teoria_m.tex:1–216`; `manuscrito/incorporaciones/parte_iv_ampliaciones_20260824/sources/editor_ready/21_cuerdas_branas_teoria_m.tex`, `22_interfaz_teoria_m.tex` y `24_terna_supercarga_teoria_m.tex`.

## 5. Material conservado para otras continuaciones

### 5.1. Dinámica temporal y formulación variacional

El integral contiene el Hamiltoniano108 y su propagador en pp.1094–1095; el forzamiento de Floquet en pp.1100–1101. El resultado finito y su control perturbativo deben exponerse junto a su dominio de validez. La suspensión simbólica aperiódica que ya contienen I/III no se identifica automáticamente con ese sistema forzado.

La aplicación de la reducción de Feshbach–Schur a las tres hojas, pp.1097–1098, aporta una articulación variacional concreta:

\[
\Sigma_0(z)=V(z-H_{\rm ext})^{-1}V^*.
\]

La reducción algebraica ya está en I/III; lo recuperable para II o un trabajo dinámico es su aplicación a la acción efectiva y a los tres regímenes, no otra demostración genérica del complemento de Schur.

### 5.2. Masa y correlación entre los dos lectores

El §92.24.11, pp.1545–1546, conserva la correlación de los lectores mediante

\[
\nu_M=\frac1{|M|}
\sum_{\Gamma\in M}
\delta_{(m_D(\Gamma),m_\Omega(\Gamma))}.
\]

Su soporte registra qué dos valores proceden de una misma ruta. Sustituirlo por el producto de los espectros marginales pierde esa correspondencia. Este desarrollo es especialmente pertinente para el futuro artículo de masas y para enlazarlo con CKM–PMNS; no pertenece al centro argumental de III.

**Fuente:** `manuscrito/sucesor_102/deltas_masas/10j_prueba_ley_general_masas_propietario_20260903.tex:888–1032`.

### 5.3. Geometría de Hopf, Möbius y Villarceau

El §32.1, pp.773–774, añade una realización geométrica más específica que el cuarto de giro ya incluido en el núcleo. Conserva grados, orientación y familias. Su interpretación toroidal del espectro \(\{7,3\}\) se formula mediante una interfaz declarada. La reservaría para una exposición geométrica del electrón y del retorno; no constituye una reparación necesaria de III.

**Fuente:** `colaboracion/parte_iii/source/public_final/base_83/c26_body.tex:64–198`.

## 6. Decisión resultante de la lectura

- Prioridad para III: polarización discreta de vacancias; articulación del modo trítico con90/120; evaluaciones constitutiva y determinantal del mismo operador.
- Conservación sin duplicación: clausura nulo–material en I; área, \(G\hbar\), transporte haciaWitt y dualidadT en II; cuarto de giro y defecto de traza en III.
- Ampliación excepcional prioritaria: orbifold de orden3 y comparación con la presentación de orden2.
- Continuaciones separadas: correlación de lectores de masa; dinámica temporal/variacional; realización dimensional11.
- No se ha editado ni recompilado ningún PDF en esta lectura.
- La selección y los mensajes originales quedan pendientes de compartir cuando el autor lo indique.

