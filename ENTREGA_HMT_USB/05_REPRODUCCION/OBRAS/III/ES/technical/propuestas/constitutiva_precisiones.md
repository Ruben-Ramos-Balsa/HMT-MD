# Precisiones constitutivas para la revisión II del artículo III

Material de trabajo para el editor único. No se ha modificado ningún TeX ni PDF. La propuesta conserva el antecedente APP–TRIT–TPK, las coordenadas angulares ya producidas y las hojas marcadas; no introduce valores externos, una nueva selección de canales ni una identificación SI. No es un certificado de autonomía global.

## 1. Procedencia y diferencia expositiva

Raíz de los propietarios consultados íntegramente:

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/`

- `constantes/c31_vacio.tex`: respuesta definida en líneas24–29; caracteres cuadráticos y prueba en líneas58–76; completación3→4 en líneas122–186; rectas dimensionales en líneas259–301; proposición **Minimalidad espectral**, con prueba, en líneas303–322. Esta última explica precisamente bajo qué reglas se fuerzan los cuadrados. Estatuto: **RESULTADO_RECUPERADO**.
- `constantes/c41_determinante_vacio.tex`: distingue el lector constitutivo `F(T)^2` del lector electrodébil `det T`. No deriva una de esas reglas a partir de la otra.
- `narrativa/01_vacio.tex`: presenta el cociente como completación de tres a cuatro términos del modo30 y distingue producto común y cociente orientado. Es interpretación del operador definido, no un segundo teorema de selección universal.

Artículo III de140 páginas cotejado: `manuscrito/sections/04_respuesta_constitutiva.tex`, `06_pell_barbero.tex`, `08_evaluacion_y_realizacion.tex`, `09_conclusiones.tex` y `00_resumen.tex`. El artículo ya prueba la monotonía, las identidades y la inversión, pero la sección04 pasa directamente de la definición de la respuesta a la definición de los cuatro caracteres. Conviene recuperar entre ambos pasos la condición de completación, y después la caracterización positiva del propietario. El resumen y las conclusiones necesitan sólo ajustar una frase, no otra exposición de las mismas pruebas.

La genealogía efectiva del corte es: estado enriquecido → registros regionales y dodecafásico → par angular orientado → `T` y sus dos hojas → respuesta de completación → caracteres normalizados → rectas dimensionales. Las coordenadas generadas se reutilizan después de su construcción. La selección de `90/120` conserva su incidencia anterior y no procede de las cifras evaluadas.

## 2. Fragmento propuesto: regla de completación y su solución única

Ubicación: sección04, junto a `iii:eq:vacuum-op`, antes de «Descomposición y positividad». Esta formulación desarrolla algebraicamente la regla ya presente; no asegura que positividad o dualidad de hojas, por sí solas, escojan esa regla entre todas las respuestas posibles.

```latex
El lector constitutivo compara, sobre cada hoja, la suma de los tres
primeros términos del modo elemental treinta con su completación de
cuatro términos. Escribamos
\[
 A_3(T)=I+T^{30}+T^{60},\qquad
 A_4(T)=I+T^{30}+T^{60}+T^{90}.
\]
La normalización de respuesta se expresa por
\begin{equation}
 \mathcal V A_4(T)=A_3(T).
 \label{iii:eq:completion-rule}
\end{equation}
Esta ecuación fija qué comparación de las dos incidencias se realiza;
la contracción y la orientación especifican su dominio de evaluación.

\begin{proposition}[Caracterización de la respuesta de completación]
Para el transporte positivo contractivo $T$ ya construido,
\eqref{iii:eq:completion-rule} tiene una única solución operatoria.
Esta solución es positiva, conserva los subespacios de hoja y coincide
con \eqref{iii:eq:vacuum-op}.
\end{proposition}
\begin{proof}
Los dos valores propios de $A_4(T)$ son
$1+q_\pm^{30}+q_\pm^{60}+q_\pm^{90}>0$. Por tanto, su inversa
existe y la ecuación equivale a
$\mathcal V=A_3(T)A_4(T)^{-1}$. Los factores son funciones del
mismo transporte, así que conmutan y conservan sus hojas. Sus valores
propios son cocientes positivos. Finalmente,
\[
 (I-T^{30})A_3(T)=I-T^{90},\qquad
 (I-T^{30})A_4(T)=I-T^{120}.
\]
Como $I-T^{30}$ también es invertible, la cancelación prueba
\eqref{iii:eq:vacuum-op}. Recíprocamente, esa expresión satisface
\eqref{iii:eq:completion-rule}.
\end{proof}
```

Alcance exacto: unicidad **para el transporte y la regla de completación especificados**. La incidencia fija los sectores; la ecuación anterior explicita la comparación que se utiliza. No convertir «única solución de esta ecuación» en «única ley electromagnética posible».

## 3. Fragmento propuesto: por qué aparecen los cuadrados

Ubicación: sección04, después de `iii:eq:four-identities`. Recupera la proposición del propietario, escribiendo también el recíproco. Las hipótesis tienen que permanecer visibles.

```latex
\begin{proposition}[Caracterización positiva de las cuatro lecturas]
Fijados los dos valores positivos etiquetados $r_+,r_-$ de la
respuesta, una cuaterna positiva
$(\widehat\mu,\widehat\varepsilon,\widehat Z,\widehat c)$
satisface simultáneamente
\[
 \widehat c^{-1}=\det\mathcal V=r_+r_-,\qquad
 \widehat Z=r_-/r_+,\qquad
 \widehat\mu\widehat\varepsilon=\widehat c^{-2},\qquad
 \widehat\mu/\widehat\varepsilon=\widehat Z^2
\]
si y sólo si es la cuaterna de \eqref{iii:eq:four}.
\end{proposition}
\begin{proof}
Producto y cociente positivos dan
\[
 \widehat\mu^2=(r_+r_-)^2(r_-/r_+)^2=r_-^4,\qquad
 \widehat\varepsilon^2=(r_+r_-)^2(r_+/r_-)^2=r_+^4.
\]
La positividad selecciona $\widehat\mu=r_-^2$ y
$\widehat\varepsilon=r_+^2$. Los otros dos caracteres están
fijados por las primeras igualdades. La sustitución demuestra el
recíproco.
\end{proof}

Los cuadrados son, por tanto, necesarios y suficientes para estas
reglas de lectura: propagación común mediante el determinante,
impedancia mediante el cociente orientado y compatibilidad constitutiva
positiva. La necesidad pertenece a esta realización especificada.
```

El determinante se refiere a la representación bidimensional; en una amplificación se conserva la normalización ya declarada, no se sustituye por el determinante ordinario de dimensión `2·9^m`.

La elección del nombre físico de cada carácter conserva la asignación de hoja y las rectas de la sección08. La proposición no prueba una identificación SI ni necesita afirmarla para justificar los exponentes cuadrados dentro de la realización.

## 4. Inversión en normalización interna: complemento breve

La sección06 ya da el dominio conjunto mediante `iii:eq:barbero-zc-domain`. Conviene que la sección04 remita a él o adelante su enunciado, para evitar que se lea la inversión como aplicación a cualquier pareja positiva de magnitudes SI.

```latex
La inversión anterior utiliza las coordenadas de la normalización interna.
En esa normalización, una pareja positiva $(\widehat Z,\widehat c)$
admite una representación única mediante dos canales del dominio
$x>|y|$ si y sólo si
\[
 1<\widehat Z\widehat c<16/9,\qquad
 9/16<\widehat Z/\widehat c<1.
\]
En efecto, estas condiciones equivalen a que las dos raíces positivas
de \eqref{iii:eq:four-identities} pertenezcan a $(3/4,1)$.
La biyección $f$ recupera entonces $s_\pm\in(0,1)$ y
$q_\pm=s_\pm^{1/30}$. Si $a=-\log q_+>0$ y
$b=-\log q_->0$, la pareja
$x=(a+b)/2$, $y=(a-b)/2$ satisface $x>|y|$ y es única.
La cámara $y>0$ equivale, además, a $\widehat Z<1$;
el caso $\widehat Z=1$ corresponde a $y=0$.

La recuperación de las hojas se entiende con su marca conservada.
Cuando $r_+\ne r_-$, los proyectores se recuperan del operador y de
las etiquetas mediante
$P_+=(\mathcal V-r_-I)/(r_+-r_-)$ y $P_-=I-P_+$.
En el caso balanceado, $\mathcal V=rI$ conserva el canal común y
la condición $y=0$, pero no determina por sí sola una descomposición
de ese autoespacio en dos hojas. En ese caso, la marca $\mathcal R$
continúa siendo parte de los datos de representación.
```

La representación única de ese párrafo se refiere a la imagen de la **representación analítica de dos canales**. No dice que todo punto de ese dominio haya sido seleccionado por una trayectoria HMT: esa procedencia sigue residiendo en el par angular construido antes.

Adición sugerida al final de «Cartas de unidades y covariancia», sección08:

```latex
Un cambio de carta mantiene la magnitud, pero transforma sus coordenadas.
Las coordenadas transformadas de la proposición anterior no son, en
general, los mismos caracteres espectrales normalizados
$r_\pm^2$, $r_-/r_+$ y $(r_+r_-)^{-1}$. Para aplicar la inversión
cúbica a datos expresados en otra carta hay que recuperar primero la
normalización interna mediante las secciones de referencia. La inversión
no determina por sí sola dichas secciones ni la historia completa del TPK.
```

Esta precisión evita usar la transformación de unidades como una nueva selección de canales o aplicar indebidamente las cotas `(3/4,1)` a coordenadas arbitrariamente reescaladas.

## 5. Signo de Barbero: marca fija y conjugación total

La sección06 dice «bajo la conjugación de hojas ... cambia el signo» inmediatamente después de `iii:eq:barbero-trace`. Le falta allí la precisión «con la marca fija», aunque sección04 sí la conserva. Sustituir únicamente ese párrafo por:

```latex
Sea $h=\mathcal H\circ\psi$ y escribamos
$\Gamma(\mathcal R,\mathcal V)=-\operatorname{Tr}
(\mathcal R h(\mathcal V))$. El cambio activo de hojas, observado
con la marca $\mathcal R$ fija, satisface
\[
 \Gamma(\mathcal R,\mathcal S\mathcal V\mathcal S^{-1})
 =-\Gamma(\mathcal R,\mathcal V).
\]
En efecto, el cálculo funcional conmuta con la conjugación, la traza
es cíclica y $\mathcal S^{-1}\mathcal R\mathcal S=-\mathcal R$.
En cambio, el transporte conjunto del operador y de su marca conserva
la evaluación:
\[
 \Gamma(\mathcal S\mathcal R\mathcal S^{-1},
        \mathcal S\mathcal V\mathcal S^{-1})
 =\Gamma(\mathcal R,\mathcal V).
\]
La segunda igualdad es la invariancia de la traza bajo conjugación.
Así se distinguen inversión respecto de una orientación fija y cambio
conjunto de representación. El par espectral sin etiquetas conserva
menos información que cualquiera de estas evaluaciones marcadas.
```

Mantener después las fórmulas de traza normalizada y amplificación tal como están. En `iii:eq:barbero-zc` y el párrafo final de la reconstrucción, añadir sólo «con la marca fija» a `gamma→−gamma`. No combinar el cambio activo de canal y una inversión adicional del funcional para contar dos veces el mismo cambio de orientación.

En la sección08, el control de intercambio también debe decir «con marca fija». En resumen y conclusiones basta utilizar «inversión constitutiva normalizada» y «reglas de completación y lectura especificadas». No repetir los nuevos enunciados completos.

## 6. Condensación de la memoria dentro de III, sin pérdida

Se leyeron completos los dos cuerpos de la copia REV02:

- `base_articulo_I/sections/memoria_resolvente.tex`,298 líneas. En el PDF140, las proposiciones de serie/cola y Schur están en p25; ejemplo, cociclo y transitividad en p26. Este cuerpo debe conservarse íntegro como núcleo común.
- `base_articulo_II/sections/03b_memoria_resolvente.tex`,235 líneas. Las líneas1–46 adaptan el origen de ventanas y añaden la identidad de truncación. Desde la línea47, «Serie generadora...», repiten el cuerpo de I desde la línea110, salvo remisiones a `eq:eta` en lugar de `mem:actualizacion`. En el PDF140 ocupan pp94–96. Son páginas de bloques I/II **dentro de III**, no páginas94–96 del PDF autónomo II05.

La aportación no redundante que se conserva íntegra es:

```latex
\[
Y_N(u)=\sum_{m=0}^Ny_mu^m,\qquad
H_{\eta,N}(u)=\sum_{m=0}^{N-1}\eta_mu^m,\qquad N\geq1,
\]
\[
(I-uR)Y_N(u)=y_0+uH_{\eta,N}(u)-u^{N+1}Ry_N.
\]
```

Al integrar, conservar el entorno numerado y la prueba ya existentes. Conservar la comparación de coeficientes en grados0,1,…,N,N+1 y la interpretación del estado terminal. Su etiqueta pública actual es `hmtII:mem:identidad-finita`, ecuación(8.5), p94.

Disposición exacta recomendada:

| Origen repetido II | Destino íntegro en núcleo I de III | Acción expositiva |
|---|---|---|
| Líneas47–97, serie y cota | Líneas110–160; `mem:prop-serie`, `mem:serie`, `mem:cota` | Remisión interna explícita, conservando el cambio de numeración de ventanas y la identificación de la actualización. |
| Líneas98–173, Schur y ejemplo | Líneas161–236; `mem:prop-schur`, `mem:schur-fuente`, `mem:schur-lector`, `mem:ejemplo-ciclo` | Remisión al operador, fuente y lector, no sólo al nombre «Schur». |
| Líneas174–235, cociclo y transitividad | Líneas237–298; `mem:cociclo-tres`, `mem:schur-intermedio`, `mem:schur-transitivo` | Remisión a las identidades y pruebas contiguas conservadas. |

No alterar las copias archivadas de I117 ni de II05. Conservar los cuerpos fuente íntegros en el paquete de procedencia y registrar como delta editorial de III la sustitución de la segunda comparecencia por una residencia de aplicación/truncación. La identidad finita no se elimina ni se reemplaza por la identidad de series infinitas.

### Precaución concreta con las referencias

`base_articulo_II/INCLUIR_DEPENDENCIAS_II.tex` prefija con `hmtII:` los rótulos de la segunda comparecencia, e incluye en su tabla de referencias las etiquetas `mem:*`. Una remisión nueva escrita allí como `\ref{mem:prop-serie}` buscaría todavía la segunda etiqueta, que se acaba de condensar. Por eso hay que cambiar también la resolución de esas referencias, no sólo el párrafo.

- Conservar `hmtII:mem:identidad-finita`, `hmtII:eq:eta` y `hmtII:mem:balance`, que pertenecen a contenido propio del bloqueII.
- Las remisiones de la residencia abreviada a la primera comparecencia pueden usar, dentro del grupo actual, `\HMTIIRefOriginal{mem:prop-serie}` y las demás etiquetas originales equivalentes. Ese comando ya existe y evita el prefijado automático.
- Si se conservan referencias externas a rótulos repetidos `hmtII:mem:*`, registrar su correspondencia explícita con las etiquetas originales; no dejar anclas huérfanas ni fabricar una segunda numeración matemática.
- Verificar el AUX final y los enlaces en el PDF: las remisiones deben llegar al contenido de pp25–26, mientras la identidad finita permanece en su nueva residencia.

## 7. Alcance de esta propuesta

La procedencia de la regla de completación, de los cuatro caracteres y de su caracterización positiva está recuperada en `c31_vacio.tex`. La forma de «si y sólo si», la prueba por las sumas `A3/A4` y la distinción de conjugación total son explicitaciones algebraicas de esos operadores y de sus reglas; no añaden un selector físico. La condensación de memoria preserva la prueba común y su única adición finita.

El editor debe integrar primero los fragmentos elegidos y después actualizar los recibos causales del artefacto real, las huellas y la verificación de referencias. Los controles de continuidad y orden causal no constituyen por sí solos una prueba matemática ni una identificación experimental. No se ha declarado que la propuesta esté incorporada al PDF ni que toda la serie esté cerrada.

Control focal ejecutado: igualdad literal de los sufijos de memoria desde `\Needspace{20\baselineskip}`, tras sustituir únicamente la referencia `eq:eta` por `mem:actualizacion`; resultado verdadero. Se comprobaron también con fracciones exactas ejemplos de la ecuación de completación, las identidades de los caracteres, su dominio y los dos signos de la traza marcada. Son controles de transcripción de las identidades demostradas en la propuesta, no una selección física ni una auditoría del corpus.
