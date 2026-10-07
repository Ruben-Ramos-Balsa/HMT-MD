# Compatibilidad quiral de la realización conjunta

Fecha: 29 de septiembre de 2026. Nota focal añadida; no modifica fuentes selladas.

## Procedencia y dominio

Esta comprobación actúa sobre la representación de materia recibida después de la cadena común APP–TRIT–TPK, estado enriquecido y estructura discreta del continuo. No selecciona retrospectivamente semillas, rutas, valores de constantes ni el registro K. La cuestión es si las lecturas de color, carga y sabor ya publicadas admiten el ensamblaje gauge quiral propuesto sobre el mismo soporte material.

Propietarios consultados:

1. `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/03_conjugacion_mobius.tex`, líneas 114–119: el carácter de carga declarado actúa sobre la parte impar del registro y cambia de signo al conjugar; la carga elemental dimensional es una salida interna anterior.
2. `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/11_apendices_catalogo.tex`, líneas 297–319: cargas de leptones, neutrinos y quarks y sus residencias/multisecciones. Este pasaje publica las cargas en el catálogo; no es por sí solo una nueva demostración de cada asignación de hipercarga.
3. `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/08_familias_y_compuestos.tex`, líneas 181–315 y 317–402: lector neutral orientado, compresión de rango tres, condiciones de los marcos PMNS, distinción Dirac–Majorana, sector estéril y separación entre generación, color y sabor quark.
4. `/Users/ruben/Documents/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/06e_color_qutrit_gauge_finito.tex`: residuo cromático, qutrit, operadores de Weyl y realización de color SU(3).

Las cargas eléctricas utilizadas son las etiquetas recibidas `Q(u)=2/3`, `Q(d)=−1/3`, `Q(ν)=0`, `Q(e)=−1`. La elección de dobletes izquierdos, singletes derechos y la convención `Q=T3+Y` explicitan la realización gauge que se comprueba; no se presenta esta elección como una generación nueva de hipercargas desde las semillas. El cálculo conserva así la genealogía anterior y señala exactamente su punto de aplicación.

## Representación y resultado exacto

Por generación, en la convención de **todos los fermiones Weyl izquierdos**, la representación es

\[
 (3,2)_{1/6}\oplus(\bar3,1)_{-2/3}\oplus
 (\bar3,1)_{1/3}\oplus(1,2)_{-1/2}\oplus(1,1)_1.
\]

Los campos derechos físicos se han sustituido por sus conjugados izquierdos. Puede añadirse un singlete neutrínico `(1,1)_0` sin alterar ningún coeficiente. Para integrar las hipercargas al grupo circular con periodo `2π`, se utiliza la normalización entera `y=6Y` y la correspondiente normalización de la conexión; no se confunden caracteres fraccionarios con caracteres de ese U(1) global.

Con índice cuadrático fundamental `T(3)=T(2)=1/2`, los coeficientes se anulan:

\[
\begin{aligned}
\mathcal A_{33Y}&=2\frac16\frac12-\frac23\frac12+\frac13\frac12=0,\\
\mathcal A_{22Y}&=3\frac16\frac12-\frac12\frac12=0,\\
\mathcal A_{YYY}&=6(\tfrac16)^3+3(-\tfrac23)^3+3(\tfrac13)^3+2(-\tfrac12)^3+1=0,\\
\mathcal A_{\mathrm{grav}\,Y}&=6\tfrac16+3(-\tfrac23)+3\tfrac13+2(-\tfrac12)+1=0,\\
\mathcal A_{333}&=2-1-1=0.
\end{aligned}
\]

Las anomalías mixtas con un único generador de SU(2) o SU(3) se anulan por su traza cero. La representación doblete de SU(2) es pseudorreal y no tiene anomalía cúbica local. La anomalía global de Witten exige además paridad: hay `3+1=4` dobletes por generación y `12` para tres generaciones. Este resultado se refiere a la obstrucción de Witten para la representación indicada; no sustituye un análisis de todas las posibles formas globales cociente del grupo gauge.

La cancelación es el resultado estándar para esa representación, aquí verificado sobre el ensamblaje recibido. Véanse [Bilal, *Lectures on Anomalies*, §7.3](https://arxiv.org/abs/0802.0634) y [Witten, *An SU(2) anomaly*](https://doi.org/10.1016/0370-2693(82)90728-6). No se atribuye novedad a estas identidades convencionales.

## Leptones, neutrinos y transporte de sabor

El bloque leptónico se realiza mediante `L_L=(ν_L,e_L)`, `Y(L_L)=−1/2`, `Y(e_R)=−1`. Con `Y(H)=1/2`, el operador `H⊗Y_e` es covariante porque `1/2−1=−1/2`. Si se declara un singlete `ν_R` de hipercarga cero, `\widetilde H⊗Y_ν` también lo es: `−1/2+0=−1/2`. Estos bloques producen masas de Dirac al evaluar el campo escalar en su sección de vacío, con `Y_f=√2M_f/v` en el marco fijado.

Un singlete neutral admite además un término de Majorana gauge invariante. En cambio, la neutralidad eléctrica de un neutrino activo no autoriza una masa de Majorana desnuda para el doblete antes de la ruptura: debe declararse su realización covariante (por ejemplo, un operador de dos Higgs o una extensión con singletes). La nota no selecciona entre estas realizaciones y no convierte una profundidad del atlas en una especie estéril.

CKM y PMNS, cuando actúan unitariamente sobre marcos completos del mismo espacio físico, cambian la base de generaciones pero no las multiplicidades gauge. Por invariancia cíclica de la traza, `tr(T_a{T_b,T_c})` y `tr(Y)` no cambian bajo conjugación unitaria. Las fases de mezcla, incluidas fases de Majorana cuando estén definidas, tampoco alteran las sumas anteriores. Si los marcos neutrínicos tienen imágenes distintas, el propietario sólo garantiza una contracción: esa operación no se sustituye aquí por una matriz unitaria sin su condición de subespacio.

## Controles reproducibles

Ejecutar `python3 -I -S anomalias_quirales.py` desde esta carpeta. El programa usa únicamente racionales exactos y publica JSON por la salida estándar.

Los 36 controles son: cinco coeficientes locales y el número par de dobletes para `N=1,2,3,4,17` generaciones (30); invariancia al añadir un singlete neutral (1); detección de inconsistencia al retirar cualquiera de los cinco multipletes (5).

Control negativo relevante: el sector quark aislado conserva las cancelaciones de color, pero da `A_22Y=1/4`, `A_YYY=−3/4` y tres dobletes. La incorporación leptónica no es ornamental: es necesaria para la compatibilidad quiral del conjunto. Retirar sólo el singlete cargado da `A_YYY=A_gravY=−1`.

## Medida, BRST y alcance preciso

La anulación anterior elimina estas obstrucciones de representación; no construye por sí misma una medida fermiónica quiral, ni prueba su positividad por reflexión, ni demuestra que una integral gravitatoria esté definida.

Se buscó de forma focal `BRST`, `Slavnov`, determinante/medida quiral, reflexión fermiónica y anomalías gauge en los `.tex`/`.md` del árbol vigente `CUMPLIMIENTO_EDITORIAL_20260928/fuentes` y en los `.tex` de `ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections`. La búsqueda no recuperó un propietario nominal de esos certificados dentro de ese alcance. Esto no declara inexistencia en todo el proyecto ni reabre los resultados gauge ya recuperados.

El propietario actual de Yang–Mills `X_ES/sections/ym_complete.tex` contiene su propia construcción de medida, transporte, identidades de Ward/Schwinger–Dyson y realización espectral. Añadir los determinantes quirales de materia cambia el integrando: la transferencia de sus propiedades al sistema conjunto exige la operación y la prueba correspondientes, no una mera identificación de nombres. La presente nota aporta la prueba exacta de compatibilidad de la representación que debe entrar en esa composición, preservando el origen HMT de sus objetos anteriores.
