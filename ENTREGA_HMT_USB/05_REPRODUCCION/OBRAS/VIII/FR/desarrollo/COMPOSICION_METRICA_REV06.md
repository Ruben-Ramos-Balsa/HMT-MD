# Composición de extensión mínima, contorsión y respuesta métrica

Fecha: 10 de septiembre de 2026. Revisión focal de los propietarios reunidos en VII, seguida de desarrollo autorizado. No se modificaron `30e`, `31`, `50`, el ensamblado ni los artículos anteriores. No se compiló ningún PDF.

## Resultado implementado

Archivo: `manuscrito/32_eliminacion_torsional_no_lineal.tex`.

Estatuto: **FORMALIZACION_NUEVA / CERTIFICADO_NUEVO** de la composición entre operaciones ya reunidas, no una nueva selección de datos de frontera, rutas, acoplamientos ni amplitudes cosmológicas. Contiene siete enunciados con prueba. Inserción aconsejada: inmediatamente después de `31_corriente_y_respuesta_cartan.tex`, antes de `50_dilucion_y_rebote.tex`.

La composición obtenida es:

\[
(\mathsf C_U,b,\chi,\mathfrak a)
\longmapsto (\mathsf L,y,f_{\min},F)
\longmapsto s=-2\partial_kF
\longmapsto \sigma=\mathsf M_{\rm cel}^{-1}s
\longmapsto k_*(p)
\longmapsto\Delta S(p)
\longmapsto d_p\Delta S.
\]

La incidencia y los transportes conservan su procedencia APP–TRIT–TPK, tal como los realiza `30e`. Las operaciones nuevas componen esa acción con la forma gravitatoria de `31`; ningún valor gravitatorio, cosmológico o metrológico se usa para elegir el resultado del ejemplo o la corriente de la construcción.

## Propietarios efectivamente leídos

Raíz de todos los localizadores relativos de esta nota:

`/Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/propuestas/ARTICULO_VII_GRAVITACION_20260910`.

| Propietario y localizadores | Operación conservada |
| --- | --- |
| `manuscrito/30e_corriente_extension_minima.tex:30–81` | Gramiano positivo, extensión mínima única, energía \(E=\chi b^*(\mathsf C\mathsf C^*)^{-1}b\). |
| Mismo, `83–97` | Incidencia cúbica y normalización \(\chi=112/(81\ell^2)\), \(\Lambda=28(P_u+3P_-)/(243\ell^2)\). Se conserva la unidad de los datos; \(E\) es adimensional cuando \(b\) tiene longitud. |
| Mismo, `102–176` | Diferencial completo de incidencia, frontera y normalización; trivialización de cocientes y distinción entre producto positivo y métrica lorentziana. |
| Mismo, `209–306` | Incidencia transportada por rutas; regla de derivación del producto ordenado; corriente variacional de \(S_{\min}=\mathfrak a E\) y emparejamiento celular invertible. |
| `manuscrito/30c_composicion_corriente_conexion.tex:194–292` | Tipos de covector/corriente; normalización y composición con Cartan; aviso explícito de dependencia no afín por holonomías. Lectura auxiliar directamente pertinente. |
| `manuscrito/31_corriente_y_respuesta_cartan.tex:74–176` | Acción, factores \(\kappa c\), signo \(\delta_\omega S_m=-\frac12\int\delta\omega\wedge\sigma\), inversa de Holst. |
| Mismo, `182–270` | Inversión \(Y\mapsto T\mapsto K\); linealidad en la corriente cuando ésta es independiente de \(K\). |
| Mismo, `275–347` | Hipótesis material afín expresa; forma gravitatoria homogénea de grado dos, borde conservado y eliminación \(-K\sigma/4=-\mathcal Q\). |
| Mismo, `357–412` | Variación métrica de la acción eliminada, conversión \(U^{\rm phys}=c\mathcal U^S\), conservación de la fuente total. |
| `manuscrito/50_dilucion_y_rebote.tex:21–51` | Eliminación del índice: \(M_n=(a_n/a_{\rm ref})^{-6}\); realización de la densidad cuadrática y amplitud de referencia. |
| Mismo, `56–111`, `122–183` | Realización homogénea con signo torsional negativo, \(w<1\), positividad de amplitudes; umbral único y persistencia transversal con dos controles \(C^1\). |

Las fuentes históricas citadas en las cabeceras se conservaron como procedencia; no se inició otra búsqueda ni se sustituyeron estos propietarios por un resultado convencional externo.

## Composición no afín exacta

Se trabaja en un nivel celular finito y una trivialización fija. El punto de corte está después de la publicación de rutas, frontera, peso y sección de acción. Para \(p\) geométrico/material y \(k\) coordenadas de contorsión:

\[
F(p,k)=S_{\min}[e(p),\mathring\omega(e(p))+K(k),\Psi(p)],\qquad
Q(p,k)=\tfrac12k^{\mathsf T}\mathsf A(p)k.
\]

El covector es \(s=-2\partial_kF\), con la fórmula explícita de `30e`. Por consiguiente:

\[
\mathcal R(p,k)=\mathsf A(p)k-\tfrac12s(p,k)=0.
\]

Esto equivale, cuando los emparejamientos realizan la misma ecuación de conexión, a la composición
\(\mathsf C_e^{\rm tor}\mathsf L_e^{-1}(\kappa c\mathsf P_\gamma^{-1}\sigma)\)
de las tres inversas ya demostradas en `31`. La corriente permanece evaluada en \(\omega=\mathring\omega+K\). No se la congela para aplicar indebidamente la fórmula afín.

Una rama local se obtiene si las familias son \(C^2\), existe un punto estacionario \((p_0,k_0)\) y el Hessiano total

\[
\mathsf H_0=\mathsf A(p_0)+\partial_k^2F(p_0,k_0)
\]

es invertible. El texto demuestra la continuación local, con su derivada, mediante función implícita y muestra la aplicación contractiva local correspondiente. La positividad del Gramiano de pantalla no sustituye esa condición: corresponde a otro operador. El resultado es finito y local; no se promueve a unicidad global ni a límite continuo.

Para una rama estacionaria y un segmento radial contenido en el abierto de rango completo:

\[
\Delta S=Q(p,k_*)+F(p,k_*)-F(p,0)
=\tfrac14k_*^{\mathsf T}s(p,k_*)
-\tfrac12\int_0^1k_*^{\mathsf T}s(p,tk_*)\,dt.
\]

La integral proviene del teorema fundamental aplicado al funcional existente. Sólo cuando \(s\) es constante en \(k\) se reduce a \(-k_*^{\mathsf T}s/4\), exactamente como en `31`. La identidad es para la acción integrada/celular; una lectura como densidad puntual requiere la realización local correspondiente. Los posibles acoplamientos entre celdas por productos de ruta se conservan.

## Variación métrica evaluable

La estacionariedad cancela el término que multiplica \(d_pk_*\), y queda:

\[
\partial_{p_i}\Delta S
=\tfrac12k_*^{\mathsf T}(\partial_{p_i}\mathsf A)k_*
+\partial_{p_i}F(p,k_*)-\partial_{p_i}F(p,0).
\]

Cada derivada material se obtiene de las matrices y datos del mismo mínimo:

\[
\partial_{p_i}F
=(\partial_{p_i}\mathfrak a)E+
\mathfrak a(\partial_{p_i}\chi)b^*y
+2\mathfrak a\chi\Re\langle y,\partial_{p_i}b-(\partial_{p_i}\mathsf C)f_{\min}\rangle.
\]

Al variar la cotetrada con \(k\) fijo se varía también \(\mathring\omega(e)\). Esta dependencia está escrita expresamente. Si el producto positivo de extensión tiene matriz variable \(\mathsf h\), se añade el término demostrado \(\chi f_{\min}^*(\delta\mathsf h)f_{\min}\), después de sustituir el Gramiano por \(\mathsf C\mathsf h^{-1}\mathsf C^*\). Se preserva así la advertencia tipada de `30e:166–176`.

La fuente física se obtiene mediante el emparejamiento métrico de `31`, en una realización que lo admita. El desarrollo proporciona la acción y su diferencial, sin identificar automáticamente el signo del mínimo positivo con el signo de su tensor gravitatorio. Para aplicar literalmente `50`, el tensor de la realización debe publicar, además de isotropía, la contracción negativa \(\rho_{\rm corr}=-s_0a^{-6}\) y el comportamiento de presión utilizado allí. La conservación de la fuente total de `31` no equivale por sí sola a conservación separada de esa contribución. Cuando la ley constitutiva se evalúa en el estado material, \(s_0=-a_{\rm ref}^6\rho_{\rm corr}(a_{\rm ref})\) es una lectura de ese estado, no un parámetro elegido para colocar el rebote.

## Control exacto y alcance

`pruebas/verificar_eliminacion_torsional_no_lineal.py` es autónomo y usa exclusivamente biblioteca estándar y racionales `Fraction`. La diferenciación por jets de orden dos controla fórmulas cerradas independientes, sin diferencias finitas decimales ni `assert`.

Ejemplo no afín impreso y comprobado:

\[
\mathsf C(k)=(1\ \ k),\quad b=\chi=1,\quad
F=\frac{\lambda}{1+k^2},\quad Q=\frac{k^2}{2}.
\]

En \(\lambda=25/2\), las soluciones son \(0,\pm2\). Para \(k_*=2\), el Hessiano total es \(16/5\), la corrección exacta es \(-8\), la integral radial es \(20\) y la expresión afín no aplicable da \(-2\). El ejemplo demuestra por cálculo la relevancia de conservar la dependencia no lineal; no selecciona una ruta ni una corriente física. Se comprueban también la especialización afín, las derivadas de rama/envolvente y la variación del producto positivo, incluido el control negativo que detecta su omisión.

Ejecuciones desde `/private/tmp`:

```text
python3 -I -S -B .../pruebas/verificar_eliminacion_torsional_no_lineal.py
python3 -I -S -B -O .../pruebas/verificar_eliminacion_torsional_no_lineal.py
```

Ambas: `PASS_ELIMINACION_TORSIONAL_NO_LINEAL_RACIONAL`, **191 comprobaciones**; los dos recibos son idénticos por SHA-256. Distribución: 96 diferenciales, 45 integrales radiales, 22 controles de soluciones no afines, 5 negativos, 10 de dominio, 4 de envolvente, 6 afines, 3 de producto variable. Esto acredita únicamente el alcance focal publicado, no una evaluación cosmológica completa ni una prueba universal HMT.

Control estático del fragmento: 31 etiquetas propias, siete pruebas, cero colisiones de sus etiquetas con el árbol actual, cero referencias suyas sin definición y entornos balanceados. No equivale a compilación ni a revisión visual.

## Recomendaciones editoriales para el ensamblado

Instantánea leída: `00_apertura.tex:6–23,37–53,71–94,114–121` y `cuerpo_en_desarrollo.tex:7–30`. El ensamblado ya incluye núcleo común y antecedentes, `29`, los cuatro desarrollos de pantalla/conexión, `30e`, `31`, `50`, `60`, `70` y `80`.

1. Dar a la composición **mínimo → corriente → conexión estacionaria → acción efectiva → respuesta métrica** un lugar central en el resumen. En la apertura actual domina la lista dilución/rebote/persistencia, aunque el nuevo desarrollo causal anterior es la aportación que permite enlazarlos.
2. Mantener «respuesta algebraica lineal» para el dominio afín de `31`. Para la incidencia transportada de `30e`, describir «ecuación variacional compuesta y eliminación local de la conexión». Las holonomías pueden acoplar celdas; esa especificidad no debe quedar aplanada como un mapa puntual independiente de la corriente.
3. En las conclusiones reunir las operaciones que sí están demostradas: mínimo y normalización, diferencial completo, inversión de Cartan, eliminación afín y no afín, respuesta métrica, dilución y persistencia con sus hipótesis, horizonte y observador. La expresión «amplitud determinada» debe remitir a la evaluación material concreta que efectivamente se incorpore, no únicamente al nombre del funcional o al exponente de escala.
4. La introducción contiene, dentro de una ecuación numerada, toda la identidad de dilución; conviene reservar la prueba en `50` y usar la apertura para explicar el papel de ese exponente respecto del nuevo mapa de respuesta. No se solicita borrar la identidad ni resumir las pruebas.
5. El archivo parcial leído no incluye una residencia de conclusiones ni un cierre bibliográfico autónomo. Es una observación del ensamblado de esta instantánea, mientras root prepara su sucesor, no una conclusión sobre el corpus. Las conclusiones deberían conservar las condiciones enunciadas sin convertir los ejemplos racionales en observaciones físicas.

No se tocaron título, apertura, conclusiones, `31`, `50` ni el ensamblado. El radión sigue fuera de este encargo.

## Huellas de la instantánea revisada

| Archivo | SHA-256 |
| --- | --- |
| `manuscrito/30e_corriente_extension_minima.tex` | `2de0de1eb74bfa41e889d7d208886fa833a47be19494b9e8561ce24ae3f2d843` |
| `manuscrito/31_corriente_y_respuesta_cartan.tex` | `1873a165372014a51f16c6ea90be9c35351da5a924843b6de6ac636853d0adad` |
| `manuscrito/50_dilucion_y_rebote.tex` | `050cae9d6f5596c6813c08b726cef44c8205d65dd5bc6b5c0773dddbd2d0593a` |
| `manuscrito/32_eliminacion_torsional_no_lineal.tex` | `d0005a4e97eebd9c7280271af8ed82e61b0157d824baf300f794a29ac5a364eb` |
| `pruebas/verificar_eliminacion_torsional_no_lineal.py` | `6483bfd56a3dc6d1e5e3f7f17d1ceb666b3dd11b6500ddd79c701cfdbaa2388e` |
| `desarrollo/ELIMINACION_TORSIONAL_NO_LINEAL_NORMAL.json` | `b3238c9e24a55bba2abd7e3b2383f49eed38cb98ac1b429b3627571046e4b71f` |
| `desarrollo/ELIMINACION_TORSIONAL_NO_LINEAL_OPTIMIZADO.json` | `b3238c9e24a55bba2abd7e3b2383f49eed38cb98ac1b429b3627571046e4b71f` |
