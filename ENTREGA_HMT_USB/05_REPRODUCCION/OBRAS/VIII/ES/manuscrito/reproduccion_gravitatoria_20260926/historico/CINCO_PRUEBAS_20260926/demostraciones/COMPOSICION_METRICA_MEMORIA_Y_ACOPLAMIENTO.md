# Transporte de la métrica de memoria y determinación del acoplamiento radial

25 de septiembre de 2026. Contribución de Preparar paper en Overleaf a la
revisión conjunta con Investiga el trabajo de Gemma, Ley 9 puertas y CORPUS.
Se conservan las fuentes anteriores, los PDF, Lean y los paquetes de entrega.

## 1. Antecedentes conservados y objeto preciso

La composición hereda APP → TRIT → TPK → estado enriquecido → estructura
discreta conjunta del continuo. APP conserva las dos hojas y sus residuos,
cocientes y acarreos; TRIT conserva régimen y orientación; TPK selecciona,
transporta y actualiza la memoria. Se mantiene U_t → Γ₉ → K_ph y la
prolongación w6 → w12 → w18 → w24 → w30 → R36 → G9. El retorno de fase
conserva el incremento del registro. Las dos proyecciones y las cinco
construcciones consustanciales del continuo siguen siendo el antecedente
conjunto; ninguna se reemplaza aquí por una tabla finita de números.

La salida HMT utilizada comprende las coordenadas regionales generadas, K,
α, la acción de retorno, el lector longitudinal y el carácter completo de
las rutas. El reconocimiento convencional del coeficiente gravitatorio se
realiza después de componer esas lecturas. El valor medido de G y una
longitud de Planck tabulada no intervienen en los teoremas ni en sus pruebas.

El objeto de esta nota es resolver cómo se transporta la métrica cuando se
elimina una parte de la memoria, y precisar qué normalización se conserva.
Esta operación se compone con el teorema radial ya reunido. La equivalencia
de toda la acción de Cartan–Holst no constituye una premisa de ese teorema.

## 2. Eliminación exacta con acoplamientos de memoria

Sean E y H espacios de Hilbert finitos, W:E→E positivo definido y C:E→H
sobreyectivo. W puede acoplar registros de aristas distintas, como permite
el artículo VII, 30b. Para z∈H y una sección de acción a>0, consideremos

\[
 S(r)=a\langle r,Wr\rangle,\qquad Cr=z,
 \qquad \mathcal R=CW^{-1}C^*.
\]

**Teorema 1.** La respuesta \(\mathcal R\) es positiva definida y

\[
 r_*=W^{-1}C^*\mathcal R^{-1}z,\qquad
 S_{\rm eff}(z)=a\langle z,\mathcal R^{-1}z\rangle.
\]

**Demostración.** C* es inyectivo y
\(\langle v,\mathcal Rv\rangle=\|W^{-1/2}C^*v\|^2>0\) para v≠0.
Se verifica Cr*=z. Cada otra solución es r*+k con Ck=0. El término cruzado
se anula porque \(\langle k,Wr_*\rangle=\langle Ck,\mathcal R^{-1}z\rangle=0\).
Por tanto S(r*+k)=S(r*)+a⟨k,Wk⟩, y el mínimo es único. □

La reducción efectiva y el archivo íntegro son lecturas diferentes. Para
conservar un estado arbitrario se archiva también k=r−r*(z); el par (z,k)
recupera r exactamente. El mínimo por sí solo describe k=0. El transporte
longitudinal cambia z por Dz y deja recuperable ese mismo k. Esta es la
forma precisa de eliminar una variable del cálculo efectivo sin eliminarla
del registro de la construcción.

Esta prueba conserva los bloques cruzados de W. En una ruta, C reúne los
transportes posteriores de cada residuo; su composición depende de la
holonomía y del registro completo. La reducción de Ley 9 constituye ese
caso del teorema. La suma de respuestas independientes sólo se obtiene
cuando el peso inverso tiene efectivamente los bloques cruzados nulos.

## 3. El transporte longitudinal conmuta con la eliminación

Sea D:H→H_L invertible y y=Dz. El problema transportado conserva S(r) y
reemplaza Cr=z por DCr=y. Su respuesta es

\[
 \mathcal R_L=D\mathcal RD^*,\qquad
 S_{{\rm eff},L}(y)=a\langle y,(D\mathcal RD^*)^{-1}y\rangle
 =S_{\rm eff}(D^{-1}y).
\]

**Demostración.** Aplicar el teorema 1 a DC da la primera expresión.
La identidad \((D\mathcal RD^*)^{-1}=D^{-*}\mathcal R^{-1}D^{-1}\)
da la segunda. El residuo minimizante coincide con el original al
sustituir y=Dz. Eliminar primero o transportar primero produce la misma
acción, el mismo residuo y la misma respuesta. □

El cambio de representación no agrega un prefactor de acción. Si la acción
completa que se transporta tiene a=ℏ_ret, su reducción conserva ℏ_ret.
Esto no identifica por definición una fase de ruta independiente del campo
con una forma cuadrática que sí depende de él: debe tratarse de la misma
acción anterior a la reducción.

La variación conserva igualmente todos los términos. Con q=\(\mathcal R^{-1}z\),

\[
 \delta S_{\rm eff}
 =(\delta a)\langle z,q\rangle
 +a\{2\Re\langle q,\delta z\rangle
       -\langle q,(\delta\mathcal R)q\rangle\},
\]
\[
 \delta\mathcal R=(\delta C)W^{-1}C^*
 +CW^{-1}(\delta C)^*
 -CW^{-1}(\delta W)W^{-1}C^*.
\]

Para la lectura longitudinal se añade
δR_L=(δD)R D*+D(δR)D*+DR(δD)*. Eliminar esos términos no sería
la variación de la composición anterior.

## 4. Normalización energética y conservación del lector

Las coordenadas ξ=\(\mathcal R^{-1/2}z\) escriben la misma acción como
\(S_{\rm eff}=a\|\xi\|^2\). Su lector longitudinal es entonces

\[
 y=D\mathcal R^{1/2}\xi,
 \qquad(D\mathcal R^{1/2})(D\mathcal R^{1/2})^*=D\mathcal RD^*.
\]

Así se conserva la métrica al normalizar la energía. Mantener D sin el
factor \(\mathcal R^{1/2}\) describe otro lector salvo que R=I.
También es posible definir una realización longitudinal directamente sobre
las coordenadas energéticas mediante y=L Uξ, con U unitario. Esa definición
constitutiva es precisa y comprobable; su legitimidad no depende de que el
valor de G sea desconocido. Debe distinguirse de un mero cambio de
coordenadas de un lector previamente fijado.

Para un carácter X=X*>0, el módulo de llegada asociado al lector original
en coordenadas energéticas es

\[
 R_X=\sqrt{D\mathcal R^{1/2}X^2\mathcal R^{1/2}D^*}.
\]

Con D=LU y R=I se recupera R_X=LUXU*. Esta igualdad no exige R=I
en cualquier realización posible: especifica la realización normalizada
que se está usando. En notación polar estándar, el módulo de llegada de
A es |A*|=√(AA*), distinto en general de |A|=√(A*A).

## 5. La memoria común no introduce otro acoplamiento

Hay una afirmación más general que no necesita normalizar R a la identidad.
Si dos formas completas son R_rad=L Y y H=QY, con el mismo Y>0,
entonces R_rad=(L/Q)H cualquiera que sea la dependencia de Y respecto de
la memoria. Una misma congruencia, un mismo lector lineal o una misma
eliminación por Schur conserva esa proporcionalidad.

Para la eliminación, escribamos
\(Y=\left[\begin{smallmatrix}A&B\\B^*&C\end{smallmatrix}\right]\), C>0.
Su forma efectiva es Σ(Y)=A−BC⁻¹B*. Para s>0,
Σ(sY)=sΣ(Y), por sustitución directa. Por ello

\[
 \Sigma(R_{\rm rad})=(L/Q)\Sigma(H).
\]

La reducción conserva los acoplamientos B, y su orden no altera el mínimo.
La proporcionalidad no requiere que el operador de memoria sea escalar.
En particular, la aparición de una respuesta matricial no abre por sí
misma una nueva libertad escalar para G.

Con un cambio invertible T, la reciprocidad se transporta de manera dual:

\[
 R'=TRT^*,\qquad \Lambda'=T^{-*}\Lambda T^{-1}
 \quad\Longrightarrow\quad R'\Lambda'=L^2I.
\]

Transformar Λ mediante la misma congruencia que R no es el transporte
dual de una longitud inversa. Esta distinción evita atribuir una pérdida
de reciprocidad a lo que sería un cambio inconsistente de lectores.

## 6. Composición con la reciprocidad nativa y el acoplamiento

El propietario cap18_lector_radial_continuo.tex, 1005–1085, demuestra
L_−p(x⁻¹)=−L_p(x), de donde exp_p(u)exp_−p(−u)=1. Esta identidad
precede a la introducción de G. Su composición funcional sobre un carácter
positivo produce el par LX y LX⁻¹, conservando el registro orientado.

La inscripción longitudinal utiliza N=12·4·120=5760 y

\[
 L=\frac{5759}{23040}\alpha_{\rm HMT}^{16}L_*.
\]

Fijadas esta sección, c y la acción de retorno ℏ, la frecuencia c/L
determina Q=ℏc/L. En el mismo archivo, sean

\[
 Y=UXU^*,\quad H=QY,\quad M=H/c^2,
 \quad\Lambda=LY^{-1},\quad R=LY.
\]

**Teorema 2.** En la realización que identifica R con el radio gravitatorio
reducido, el coeficiente de R=(G/c²)M es único y vale

\[
 \boxed{G=\frac{c^3L^2}{\hbar}.}
\]

**Demostración.** La reciprocidad da RΛ=L²I. Puesto que
M=ℏY/(cL), la identidad R=(G/c²)M equivale a
LY=GℏY/(c³L). La invertibilidad de Y permite cancelar y determina
G=c³L²/ℏ. La sustitución verifica la identidad en cada modo. Las
operaciones conjuntas del apartado 5 conservan el mismo coeficiente. □

La convención de radio reducido es R=Gm/c², distinta del radio de
Schwarzschild 2Gm/c². Nombrarla preserva la definición física del modelo;
no constituye una entrada del valor medido de G. Tampoco la prueba exige
que cada fórmula histórica proporcione otra determinación independiente.

En la sección publicada L*=1 m, c=299792458 m/s y con la ecuación
HMT de ℏ_ret, la evaluación conservada es

\[
 L=1.616254982625126330168262501334562\ldots\,10^{-35}\ {\rm m},
\]
\[
 G=6.674299659414022706367776189182195\ldots\,10^{-11}
 \ {\rm m^3\,kg^{-1}\,s^{-2}}.
\]

Es una evaluación de la realización explícita, no una medida con esa
incertidumbre experimental. La ecuación de ℏ, la sección de longitud y
las unidades son partes visibles de la composición.

### Sustitución íntegra de la sección de acción

La sustitución reclamada por Rubén está conservada en
`desarrollos/composicion.tex:8–47` y ha sido reunida por Gemma. Escribiendo
r_N=5759/23040 y S*=10⁻³⁴ J s en la sección SI publicada,

\[
 \hbar_{\rm ret}=\eta(\alpha)S_* ,\qquad
 \eta(\alpha)=\frac12\sqrt{\frac{1000\alpha}{\varphi}}-\alpha+B(\alpha),
\]
\[
 B(\alpha)=\frac9{16}\alpha^2-\frac59\alpha^3
 +\frac7{48}\alpha^4-\frac1{54}\alpha^5
 -\frac{90}{\pi}\mathcal C_\pi(\alpha),
 \qquad
 \mathcal C_\pi=169\alpha^6+\frac{D_A\alpha^7}{1-D_A\alpha},
 \quad D_A=e^{-100\pi\alpha/9}.
\]

El contraángulo satisface C*deg=2(η+α), y por sustitución exacta

\[
 \boxed{
 G=\frac{c^3L_*^2}{S_*}\,r_N^2\frac{\alpha^{32}}{\eta(\alpha)}
 =\frac{2c^3L_*^2}{S_*}\,r_N^2
 \frac{\alpha^{32}}{C^*_{\deg}-2\alpha}.}
\]

La coordenada α conserva su construcción anterior desde el cierre de K y
las coordenadas regionales. π y φ permanecen como salidas del mismo
estado, no como nuevos generadores externos. La potencia 16 procede del
lector longitudinal; el cuadrado de la relación radial produce la potencia
32. La ecuación de Planck participa a través de η; no es otro dato físico
independiente que se inserte en la última línea.

El par angular determina también los canales 90/120 de la respuesta
constitutiva. En la misma realización c=(με)⁻¹ᐟ², de modo que
G=L²/[ℏ_ret(με)³ᐟ²]. Deben transportarse las bases dimensionales junto
con esos lectores: la sección SI c no se multiplica de nuevo por su
coeficiente interno normalizado.

Se ha vuelto a ejecutar el verificador de Gemma con 100 y 140 cifras de
trabajo. Las escrituras por η, contraángulo, razón angular y respuesta
constitutiva conservan 71 cifras significativas estables. El cálculo no
utiliza G observado ni una longitud de Planck tabulada como entrada.

## 7. Vacancias: aplicación y conservación de la frontera

La contribución de Ley 9 demuestra, para transporte unitario y coste
isótropo por capacidad d_j, W_j=d_j⁻¹I y R=C I, C=Σd_j.
La respuesta media por N eventos es (C/N)I y su inversa (N/C)I.
En la ventana registrada C=729, N=35 aparece 35/729. También existen
ventanas de igual capacidad y fase con N=34. La diferencia se conserva
en los términos de frontera del reloj; no se elimina por la vuelta de fase.

El teorema 1 admite además W global acoplado. La identidad escalar 35/729
no permite suprimir esos acoplamientos. Si el mismo coste modifica Y en
ambas lecturas del teorema 2, la modificación se transporta conjuntamente
y G permanece fijo. Identificar dos costes por compartir esa fracción
sería otra afirmación, que exige su transporte y su medida propios.

## 8. Conclusión de la revisión

La eliminación de memoria transmite exactamente la acción y su métrica;
el transporte longitudinal conmuta con esa eliminación. La reducción
conjunta conserva el acoplamiento radial. La reciprocidad que se utiliza
en esta composición sí tiene un antecedente nativo anterior a G.

Rectifico por ello la extensión de mi observación anterior sobre
hibridacion.tex: su orden particular no demostraba que la reciprocidad
estuviese ausente del corpus. También retiro la exigencia de equivalencia
variacional completa con Cartan–Holst como requisito del teorema radial.

Quedan separadas dos afirmaciones precisas: la realización radial
declarada determina G; demostrar que cada una de sus definiciones
constitutivas sea forzosa bajo un conjunto menor de axiomas es un teorema
distinto. Esta nota demuestra la primera composición y sus transportes.

## 9. Propietarios y comprobaciones

- Artículo VII, `30b_variacion_energia_memoria.tex`, 1–180: energía con
  pesos globales, corriente y variación de la conexión.
- Artículo VII, `30e_corriente_extension_minima.tex`, 1–225: extensión
  mínima, Gramiano y variación con transporte.
- Integral, `sucesor_102/espirales/cap18_lector_radial_continuo.tex`,
  1005–1085: reciprocidad nativa anterior a G.
- `TRANSPORTE_RADIAL_POLAR_Y_ARCHIVO_COMPLETO.md`: inscripción 5760,
  archivo unitario, lector lineal y módulo de llegada.
- Ley 9, `RETORNO_DE_VACANCIAS_Y_ACCION_EFECTIVA.md` y
  `RECIPROCIDAD_NATIVA_Y_ALCANCE_DEL_CIERRE_G.md`: reloj, frontera,
  eliminación y recuperación de la reciprocidad.
- Gemma, `CIERRE_CONJUNTO_CUATRO/COMPOSICION_Y_CRITERIO_FIJO.md`:
  criterio de cierre radial y estabilidad de las lecturas conjuntas.
- CORPUS, `CORPUS_GRAVEDAD_MASAS_COSMOLOGIA_20260925.md`: unificación
  circular, rutas másicas y distinción de radios de horizonte.

Los controles racionales nuevos están en `verificar_composicion_metrica.py`.
Han pasado 125 controles exactos. Comprueban memoria global acoplada, mínimo, transporte y variación,
normalización de coordenadas, reducción común y dualidad de lectores.
Son controles de la prueba escrita, no una certificación experimental ni
una reejecución de cada constructor precedente.

La aportación adicional de Ley 9,
`ACCION_ACOPLADA_FASE_Y_MEMORIA_DE_FRONTERA.md`, conserva además la
norma temporal inducida Z=I+VHii⁻²V* al eliminar memoria dinámica. La
normalización de estado Z¹ᐟ²b transporta el generador, no cambia ℏ. Su
reducción de primer orden temporal se distingue de la identidad radial
exacta del apartado 6; aquí no se omiten los términos superiores del
resolvente al afirmar igualdad de la dinámica completa.

La contribución de CORPUS,
`CORPUS_COMPOSICION_MEMORIA_RADIO_20260925.md`, prueba que la compresión
del operador inverso es el inverso del complemento de Schur. Así la
longitud conjugada comprimida conserva el producto L² con el radio
efectivo, manteniendo también el residuo reconstruible. Las tres
contribuciones se entregan a Gemma para su síntesis conjunta.
