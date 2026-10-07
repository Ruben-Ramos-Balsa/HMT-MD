# Positividad generada, publicación de momentos y compatibilidad coinductiva

## Encargo y conservación

Esta nota responde a la indicación de recuperar la positividad desde la estructura
discreta conjunta APP–TRIT–TPK, antes de su reconocimiento mediante Weil. No sustituye
el continuo por un problema analítico independiente. Conserva el manuscrito previo,
sus pruebas locales, sus seis fuentes comunes y el PDF entregado de 107 páginas.
La corrección pública paralela afecta únicamente a los rótulos rechazados por el autor.
Esta nota técnica no se presenta como una demostración global de la hipótesis de Riemann.

## 1. Construcción positiva que sí se recupera

El registro común conserva emisiones APP, las dos hojas, orientación TRIT, cociente,
acarreo, transporte TPK, frontera, ruta y memoria. Las prolongaciones de una historia
se distinguen por su etiqueta, aun cuando tengan la misma lectura terminal.
La medida proyectiva de historias produce el transporte ponderado

\[
U_ke_x=\sum_{\rho_k(y)=x}\sqrt{p(y\mid x)}\,e_y,
\qquad \sum_{\rho_k(y)=x}p(y\mid x)=1.
\]

Los conjuntos de hijos de padres distintos son disjuntos. Por tanto
\(U_k^*U_k=I\). La evaluación ponderada en todas las continuaciones conserva
esta isometría sin seleccionar una historia privilegiada. Esta es una construcción
anterior a cualquier columna analítica de Weil.

Sea \(P\) una proyección ortogonal del espacio generado y \(\Xi\) un lector
con dominio declarado. La publicación de frontera es

\[
B_{\mathrm{int}}=\Xi^*(I-P)\Xi,
\qquad B_{\mathrm{int}}(f,f)=\|(I-P)\Xi f\|^2\geq0.
\]

La positividad es intrínseca a esta construcción. Ni un cero de zeta ni una
desigualdad sobre la forma de Weil intervienen en esta identidad.

En la hoja antiespecular, el propietario utiliza \(q=5/9\),
\(A=P_++qP_-\), \(D=\sqrt{1-q^2}P_-\). Si \(P_-E=E\), entonces

\[
E^*E=\sum_{n=0}^{N-1}(DA^nE)^*(DA^nE)+(A^NE)^*(A^NE),
\qquad (A^NE)^*(A^NE)=q^{2N}E^*E.
\]

Así se conserva y se extingue el terminal. Esta prueba es válida para el
complemento construido, sin utilizar una identificación con Weil.

Los aspectos espectral, solenoidal, gauge, cohomológico y determinantal siguen
siendo operaciones correlativas del mismo registro. El corte espectral de esta
nota no los convierte en cinco sistemas generadores independientes.

## 2. La identidad de publicación específica

Las columnas completas \(J_{+,R},J_{-,R}\) del manuscrito reúnen los relojes
primo–potencia, el canal gamma íntegro, el modo escalar y los términos polares.
Su diferencia se calcula, término a término, como

\[
\mathscr W_R(f,g)=\langle J_{+,R}f,J_{+,R}g\rangle
                 -\langle J_{-,R}f,J_{-,R}g\rangle.
\]

El propietario requiere las publicaciones

\[
\Xi_R^*\Xi_R=J_{+,R}^*J_{+,R},\qquad
\Xi_R^*P_R\Xi_R=J_{-,R}^*J_{-,R}.
\tag{M}
\]

Aquí los productos con asterisco abrevian identidades de formas sesquilineales
sobre \(\mathcal D_R\times\mathcal D_R\); no se presupone que el espacio de
pruebas sea un Hilbert ni que esos mapas no acotados tengan un adjunto definido
en todo el ambiente.

Con ellas, la forma positiva generada es exactamente \(\mathscr W_R\). El
contenido por comprobar en la aplicación es (M), sobre todo el dominio cuantificado;
no la positividad de \(I-P_R\), ni la existencia del continuo genealógico.

### Lema: fuerza exacta de la doble publicación

Para dos aplicaciones lineales \(J_+:\mathcal D\to H_+\) y
\(J_-:\mathcal D\to H_-\), son equivalentes:

1. \(\|J_-f\|\leq\|J_+f\|\) para todo \(f\in\mathcal D\).
2. Existe una contracción \(C:\overline{J_+\mathcal D}\to H_-\) tal que
   \(CJ_+=J_-\).
3. Existen un Hilbert \(K\), una proyección ortogonal \(P\) y un mapa
   \(\Xi:\mathcal D\to K\) que satisfacen (M).

**Demostración.** De 1, la regla \(C(J_+f)=J_-f\) está bien definida:
si \(J_+f=0\), la desigualdad implica \(J_-f=0\). Es contractiva y se
prolonga al cierre. De 2, se toma
\(K=H_-\oplus\overline{J_+\mathcal D}\) y se define, sobre ese cierre,
\(D_C=(I-C^*C)^{1/2}\) y
\(\Xi f=(CJ_+f,D_CJ_+f)\). La proyección al primer sumando verifica
ambos momentos, porque \(C^*C+D_C^2=I\). De 3, la contracción de una
proyección da \(\|J_-f\|^2=\|P\Xi f\|^2\leq\|\Xi f\|^2
=\|J_+f\|^2\). La polarización conserva las identidades sesquilineales. ∎

El lema no propone la construcción retrospectiva de 2 a 3 como generador HMT.
Precisa por qué producir (M) independientemente sería el resultado decisivo, y
por qué su mera inclusión en una definición no constituye todavía esa producción.
No refuta la posibilidad de obtener (M) desde los operadores del corpus.

## 3. Dos direcciones temporales que deben conservarse

El capítulo RH declara una historia residual con

\[
\Omega_n=qV_n\Omega_{n+1},\qquad V_n^*V_n=I,\qquad
\sup_n\|\Omega_nf\|<\infty,\qquad q=5/9,
\tag{R}
\]

cuyo primer término es \(\Omega_0=K^{\rm src}J_+-J_-\).

**Lema.** Para cada \(f\) y una historia que satisface la recurrencia,

\[
\|\Omega_nf\|=q^{-n}\|\Omega_0f\|.
\]

Por tanto, dentro de esa historia, la acotación uniforme equivale a la anulación
de todos sus términos.

**Demostración.** Tomar normas en la recurrencia y utilizar la isometría da
\(\|\Omega_nf\|=q\|\Omega_{n+1}f\|\). La iteración da la fórmula.
Si el término inicial es no nulo, las normas crecen geométricamente; si es nulo,
todas son cero. ∎

Esto distingue (R) de \(A^nE=q^nE\). Esta última es una evolución prospectiva
contractiva de un estado ya obtenido. (R) impone compatibilidad inversa y acotación
sobre la diferencia de dos publicaciones. La telescopía prospectiva, por sí sola,
no prueba esa compatibilidad para \(K^{\rm src}J_+-J_-\).

### Criterio sobre generadores para construir el transporte inverso

El contraste coordinado con la tarea «Ley 9 puertas» permite fijar una prueba
operativa concreta. Sean \(X_n\) espacios vectoriales,
\(R_n:X_n\to X_{n+1}\) el refinamiento lineal y
\(D_n:X_n\to H_n\) el defecto lineal de publicación, con \(H_n\) Hilbert.
Existe una contracción \(V_n:H_{n+1}\to H_n\) que verifica

\[
D_n=qV_nD_{n+1}R_n
\]

si y sólo si

\[
\|D_nx\|^2\le q^2\|D_{n+1}R_nx\|^2\qquad(x\in X_n).
\tag{G}
\]

**Demostración.** La necesidad se obtiene tomando normas. Para la suficiencia,
defínase \(V_n(D_{n+1}R_nx)=q^{-1}D_nx\). La desigualdad (G) hace esta regla
bien definida y contractiva. Se extiende continuamente al cierre de ese rango
y por cero sobre su complemento ortogonal. Si (G) es una igualdad, el mapa
es isométrico sobre el rango residual, no necesariamente sobre todo el ambiente.
Esto basta para la identidad de normas de las historias compatibles
\(x_{n+1}=R_nx_n\), \(\Omega_n=D_nx_n\). ∎

Para una familia \(g_{n,j}\) que genere algebraicamente \(X_n\),
(G) equivale a comparar los Grams
de todas las combinaciones finitas:

\[
G_n^{\rm def}\preceq\frac{25}{81}G_n^{\rm ref}.
\]

La comparación incluye los términos cruzados; no basta verificar únicamente
las normas de cada generador. Si sólo se ha comprobado sobre un subespacio denso,
la extensión al dominio restante requiere su justificación de continuidad.
Aplicado a las rutas TPK, este criterio pide
evaluar el defecto y el refinamiento ya construidos sobre esas rutas. No los
sustituye por una matriz elegida posteriormente ni acredita por sí mismo (G).

La distinción de direcciones tiene incluso un control escalar: \(A=q\),
\(E=1\), \(\Omega_n=q^n\) satisfacen \(AE=qE\) y la acotación de
\(\Omega_n\). La relación inversa exigiría \(V_n=q^{-2}=81/25\),
que no es contractiva. Este ejemplo sólo refuta la implicación formal entre
ambas direcciones; no es un contraejemplo a la positividad de Weil.

## 4. Residencias verificadas y composición de sus referencias

Raíz del integral consultado:

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/`

- `reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b2_operaciones_intrinsecas_correlativas.tex`:
  `eq:pdfv2-cor-u-comun`, `eq:pdfv2-cor-u-gram`, `eq:pdfv2-cor-balance-hojas`.
  El transporte de hojas conserva su condición isométrica declarada; no se infiere
  del conteo solamente.
- El propietario contiguo `04b3_terminal_naturalidad_limite.tex`:
  `eq:pdfv2-terminal-evaluacion-ponderada`, `eq:pdfv2-terminal-isometria`.
  La realización ponderada conserva todas las historias y sus multiplicidades.
- `sections/sucesora/04_cinco_realizaciones_fundamentales_20260817.tex`:
  `eq:realizaciones-rh-momento-mas`, `eq:realizaciones-rh-momento-menos`,
  `eq:realizaciones-rh-publicaciones-comunes`, `eq:realizaciones-rh-identificacion-gw`.
- `sections/ampliacion_20260817/04a_refuerzo_riemann_weil.tex`:
  `eq:amp-rh-owner-binding`, `eq:amp-rh-owner-telescopia`,
  `eq:amp-rh-owner-terminal`. Su teorema cofinal remite para la identificación
  a `eq:realizaciones-rh-identificacion-gw` del propietario precedente.
- `incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/02_riemann_weil.tex`:
  `eq:pdf2-rh-momentos-lector-estructural`, `eq:pdf2-rh-recurrencia-residual`,
  `eq:pdf2-rh-energia-source-first`, `eq:pdf2-rh-xi-comun-explicita`.

El propietario de las cinco resoluciones independiente es
`/Users/ruben/Documents/HMT2/PDF_2_RESOLUCIONES_EXTENSAS_RH_NS_YM_HODGE_BSD_2026-08-19/manuscrito/secciones/02_riemann_weil.tex`.
En su PDF, capítulo 3, (3.8) presenta los momentos, (3.11) la recurrencia residual,
(3.15) la energía y (3.28) el codificador posterior. Su antecedente
`01_antecedente_comun.tex`, líneas 103–128, distingue explícitamente la construcción
interna de la coligación específica de Weil.

La fórmula explícita posterior

\[
\mathfrak C f=u\otimes(J_-f,0)+\eta\otimes(0,Ef),\qquad u\perp\eta,
\]

verifica \(\|\mathfrak C f\|^2=\|J_-f\|^2+\|Ef\|^2\). Para obtener
el primer momento de (M), su prueba utiliza la identidad anterior
\(\|J_+f\|^2=\|J_-f\|^2+\|Ef\|^2\). Es una representación legítima
una vez establecida esa energía; no constituye su prueba antecedente.

## 5. Resultado de la recuperación

Se recuperan positivamente la construcción ponderada de historias, su proyección,
el complemento positivo, el transporte con memoria, la telescopía, la extinción
prospectiva y la implicación exacta de la doble publicación. Estos resultados no
se vuelven a presentar como inexistentes.

En los propietarios examinados, la acción anterior que verifique (M), o que produzca
(R) con su acotación para las columnas completas, no queda desplegada: las
referencias vuelven a esas mismas publicaciones. Es una conclusión delimitada a
esta composición de fuentes, no una afirmación de ausencia en todo el corpus.
No se ha acreditado con esta lectura la positividad global de Weil. La presentación
corregida del PDF conserva ese alcance, sin convertir una corrección tipográfica en
una certificación matemática.

Procedencia: arquitectura autoral preexistente y resultados recuperados. Los dos
lemas y el criterio de Grams de esta nota son una formalización explicativa de sus condiciones lógicas;
no se atribuyen como descubrimientos nuevos. Los certificados documentales y hashes
acreditan conservación, no sustituyen las pruebas matemáticas.
