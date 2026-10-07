# Parámetros cosmológicos y relaciones de horizonte

Apéndice de **Preparar paper en Overleaf** para la integración de **Aclarar la tarea**, 6 de septiembre de 2026.

## Resultados recuperados

El bloque cosmológico está presente en el tratado y contiene más magnitudes que las cuatro entradas nominales del inventario inicial. Se han cotejado los propietarios de CT108–de Sitter, Perron–Einstein–Cartan, energía de horizonte y selector cosmológico. Las identidades que siguen se conservan con sus dominios y normalizaciones; los valores numéricos de las tres primeras tasas/curvaturas se reutilizan del cálculo compartido.

La edición examinada es la misma de **2.249 páginas**, SHA-256 `958d252f301763ff8901f775d8ec0b02b6ae4f9f7c57dc04ea917f747dccbf24`. Gravedad, Barbero y las escalas de Planck permanecen asignadas a **MASAS**; aquí se utilizan sus resultados como antecedentes, sin repetir esas ejecuciones ni modificar sus archivos.

### Magnitudes y relaciones

| Magnitud | Estructura o lector | Resultado y significado |
|---|---|---|
| \(H_{108}\) | Reloj \(T_{108}=108t_0\); radio \(R_{108}=c_{\rm int}/\omega_{108}\) | \(H_{108}=\omega_{108}=\pi/(54t_0)\). La coordenada adimensional ya calculada es \(H_{108}t_0=0.0581776417331443192307896922829537571\ldots\). Es la escala temporal del radio de Sitter seleccionado. |
| \(\Lambda_{108}\) | Realización cuadridimensional de Sitter del radio CT108 | \(\Lambda_{108}=3/R_{108}^2=\pi^2/(972\ell_0^2)\); \(\Lambda_{108}\ell_0^2=0.0101539139928902866448914516459631185\ldots\). Es curvatura inversa al cuadrado de una longitud, con \(\ell_0=c_{\rm int}t_0\). |
| \(H_\varphi\) | Cociclo \(V_n=\varphi^n\), dimensión espacial \(D=3\) y tiempo aditivo \(t_n=nt_0\) | \(H_\varphi=\log\varphi/(3t_0)\); \(H_\varphi t_0=0.1604039416865344824992529711414561410\ldots\). Es la tasa logarítmica de esa escala discreta. |
| Temperatura del horizonte | Temperatura de Gibbons–Hawking en el radio seleccionado | \(k_BT_{\rm dS}=\hbar_a/(108t_0)\); \(T_{\rm dS}/\Theta_{\rm clk}=\log3/(2\pi)\). El índice \(a\) conserva la sección de acción utilizada. |
| Entropía del horizonte | Área \(4\pi R_{108}^2\), normalización \(4\ell_P^2\) y selector \(R_{108}=\ell_P\) | \(S_{\rm dS}/k_B=\pi\). El resultado es una razón de entropías; la constante \(k_B\) conserva su propia derivación y carta. |
| Energía del horizonte | Densidad cosmológica integrada y energía de Misner–Sharp en la esfera marginal | \(E_\Lambda=c^4R/(2G)=T_HS_H\). Para \(R=R_{108}=\ell_P\), \(E_\Lambda=E_P/2\). |
| Media acción del horizonte | El mismo cuanto y los tiempos angular y circular | \(E_\Lambda t_P=\hbar/2\) y \(E_\Lambda T_{108}=h/2\). El factor \(1/2\) se demuestra; no se ajusta mediante un valor observado. |
| Densidad y presión del sector de traza | Carta de Sitter, tensor bariónico nulo y \(\Lambda_{\rm ref}=0\) | En la convención \(c=1\), \(\rho_*=3H_*^2/(8\pi G_{\rm int})\), \(p_*=-\rho_*\), \(w_*=-1\) y \(\ddot a/a=H_*^2>0\). Es un resultado de esa carta, no una densidad numérica universal sin escala. |
| Curvatura escalar | Tres foliaciones del mismo espacio de Sitter | \(R^{(4)}=12H_*^2\) en \(c=1\); equivalentemente \(R^{(4)}=4\Lambda_{108}\) con la convención de longitud. La curvatura espacial es \(R^{(3)}=6k/a_k^2\). |
| Exponente de memoria | Modo estable \(M_n=\varphi^{-2n}\) y \(a_n/a_0=\varphi^{n/3}\) | \(M_n=(a_n/a_0)^{-6}\), por tanto \(M_na_n^6=a_0^6\). El exponente procede del cociente \(-2/(1/3)\). |
| Escala de rebote del dominio material seleccionado | \(H^2=C(Aa^{-n}-Ba^{-6})\), con \(A,B,C>0\), \(0<n<6\) | \(a_b=(B/A)^{1/(6-n)}\) y \(\dot H(a_b)=C(6-n)Aa_b^{-n}/2>0\). La fuente demuestra unicidad del umbral positivo y rebote local regular en ese dominio. Los coeficientes son lecturas del estado, no nuevas constantes universales con un único decimal. |

Los símbolos repetidos se identifican por su tipo y fórmula: \(H_*\) y \(\omega_{108}\) coinciden con \(H_{108}\) en el selector citado; no son tres constantes independientes. La curvatura \(\Lambda_{108}\) y la energía \(E_\Lambda\) son objetos diferentes.

El archivo compartido utiliza los nombres `Lambda108_por_l02`, `H108_por_t0` y `Hphi_por_t0`. Sus números corresponden respectivamente a **los productos adimensionales** \(\Lambda_{108}\ell_0^2\), \(H_{108}t_0\) y \(H_\varphi t_0\), no a divisiones por esas escalas. Las fórmulas guardadas y la fuente permiten fijar inequívocamente esta lectura.

## Construcción y composición de los resultados

### Procedencia de las coordenadas utilizadas

π y φ son aquí antecedentes de los lectores cosmológicos. Su orden documental y ejecutable APP–TRIT–TPK → caracteres → evaluación → representación de los valores queda identificado en la [sección 2.1 del informe matemático](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/RESULTADOS_CONSTANTES_MATEMATICAS.md>). Allí se distinguen la ejecución de integración nonádica ya conservada, los controles de interfaz y nuestra reevaluación parcial. Esta última escribe los caracteres de e/φ y aplica sus evaluadores: no reejecuta todo el transporte TPK, ni su alcance particular sustituye la construcción documentada.

Las tres operaciones cosmológicas de [`comprobar_valores_corpus.py`](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_valores_corpus.py:241>) usan esas coordenadas ya evaluadas para calcular las razones indicadas. Son comprobaciones posteriores de las fórmulas de CT108 y del cociclo de volumen; no constituyen otro generador de π o φ ni una ejecución independiente del selector gravitatorio. La documentación del paquete y los recibos de integración se enlazan en la misma sección, sin depender de habilidades de esta sesión.

### 1. Radio CT108 y cuádruple de horizonte

El desarrollo parte del estado enriquecido APP–TRIT–TPK. La lectura cronológica produce \(108t_0\) y la coordenada angular π ya construida determina
\[
\omega_{108}=\frac{2\pi}{108t_0},\qquad
R_{108}=\frac{54}{\pi}\ell_0,\qquad
2\pi R_{108}=108\ell_0.
\]
La comprobación del selector gravitatorio pertenece al informe MASAS. Su resultado \(R_{108}=\ell_P\) se utiliza después en la realización geométrica, no como longitud exterior que elija retroactivamente las fases.

Una vez fijada la realización de Sitter de ese radio, sustitución directa produce el cuádruple exacto
\[
\left(H_{108}t_0,\Lambda_{108}\ell_0^2,
\frac{T_{\rm dS}}{\Theta_{\rm clk}},\frac{S_{\rm dS}}{k_B}\right)
=
\left(\frac{\pi}{54},\frac{\pi^2}{972},
\frac{\log3}{2\pi},\pi\right).
\]
También se conserva la identidad de compatibilidad
\[
\Lambda_{108}c_{\rm int}^2=3H_{108}^2.
\]
Los factores de tiempo, longitud y acción deben pertenecer a la misma carta. La derivación de las razones no requiere insertar un Hubble observado.

### 2. Escala de Perron y memoria

La fuente distingue el cociclo de volumen de la escala lineal:
\[
V_n=\varphi^n,\qquad a_n/a_0=V_n^{1/3},\qquad M_n=V_n^{-2}.
\]
La eliminación del nivel \(n\) prueba la ley de sexto orden. En las profundidades \(9,27,108\), la escala toma \(\varphi^3,\varphi^9,\varphi^{36}\), respectivamente.

La diferencia \(\log a_{n+1}-\log a_n=(\log\varphi)/3\) prueba la tasa \(H_\varphi\) bajo el tiempo aditivo declarado. El cociclo y la memoria anteceden a su interpretación como expansión o dilución de espín. El mapa escrito en el tratado es \(M_n\mapsto s_n^2=s_*^2M_n\), con amplitud positiva explícita.

\(H_\varphi\) y \(H_{108}\) poseen genealogía común y lectores distintos. Las fórmulas y valores existentes muestran esa distinción, que no debe borrarse al reunir el inventario.

### 3. Energía, temperatura y acción de horizonte

Con la convención de densidad energética
\[
\varepsilon_\Lambda=\frac{\Lambda_Rc^4}{8\pi G},\qquad
\Lambda_R=\frac3{R^2},\qquad V_R=\frac{4\pi R^3}{3},
\]
la integración da \(E_\Lambda=\varepsilon_\Lambda V_R=c^4R/(2G)\).
La condición de esfera marginal produce la misma energía de Misner–Sharp. La multiplicación de temperatura y entropía usa \(\ell_P^2=G\hbar/c^3\) y prueba \(T_HS_H=E_\Lambda\).

En \(R=\ell_P\), las igualdades \(E_Pt_P=\hbar\), \(T_{108}=2\pi t_P\) y \(h=2\pi\hbar\) dan las dos identidades de media acción. El resultado se recupera del propietario completo; no se infiere de una coincidencia decimal.

### 4. El selector cosmológico ya escrito

El propietario de cierre define \(s(x)=\tau(x)\) y
\[
H_*(x)=\frac{2\pi}{108t_0(x)}
\]
para \(t_0(x)>0\), y selecciona las foliaciones cerrada, plana y abierta de de Sitter. Las funciones hiperbólicas y exponencial satisfacen por sustitución las ecuaciones impresas. Por ello, el informe no se limita a una exposición anterior que pedía construir el selector: incluye el selector posterior efectivamente escrito.

Conviene conservar una precisión del propio cálculo: en las cartas cerrada y abierta,
\[
\frac{\dot a_+}{a_+}=H_*\tanh(H_*t),\qquad
\frac{\dot a_-}{a_-}=H_*\coth(H_*t),
\]
mientras que en la plana \(\dot a_0/a_0=H_*\).
El parámetro constante de curvatura y la tasa instantánea de una foliación no se identifican indiscriminadamente.

## Información cosmológica adicional en los pasajes contiguos

El tensor \(T_{\rm osc}\) y su descomposición en traza y parte sin traza están construidos en el propietario de cierre. La conservación se prueba mediante Bianchi y la conservación del tensor bariónico. En la carta de Sitter citada, el sector de traza da la presión negativa y la aceleración de la tabla.

También está la plantilla dodecafásica
\[
w_k=\frac1{12}[1+2\epsilon\cos(3\phi_k-\delta)],
\qquad |\epsilon|\le\frac12,
\]
con pesos positivos o nulos, suma uno y soporte discreto \(m=0,\pm3\pmod{12}\). Se registra su estructura, pero **\(\epsilon,\delta\), el eje celeste y la máscara no se cuentan como constantes universales ya evaluadas**: el texto los conserva como parámetros de la realización y del contraste. Análogamente, los coeficientes \(A,B,C,n\) del rebote y \(\Lambda_{\rm ref}\) son datos del selector particular hasta precisar sus lectores.

La [traza estructural ampliada, sección 4](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/PROCEDENCIA_ESTRUCTURAL_MATEMATICAS_Y_COSMOLOGIA.md>) reúne las dependencias del reloj, modo estable y realizadores cosmológicos, con sus entradas efectivas y su correspondencia con los programas ya ejecutados.

## Cuestiones concretas para la integración

1. **Entrada nominal \(\Lambda_0\).** El resultado cero localizado positivamente en estos propietarios es \(\Lambda_{\rm ref}=0\), en la carta con \(T_b=0\). Ese cero es la elección de referencia del ejemplo; el tensor construido sigue produciendo curvatura y densidad efectivas positivas. Para identificarlo con la entrada «constante cosmológica nula \(\Lambda_0\)» del inventario anterior hace falta su localizador específico y su definición. Se ha solicitado a la coordinación. No se convierte la elección de referencia en una derivación autónoma de \(\Lambda_0\), ni se deduce de esta falta de conciliación que el corpus carezca de otras construcciones de vacío.
2. **Escalas físicas.** Las tres cifras principales son adimensionales. La conversión de \(H\) a unidades temporales o de \(\Lambda\) a longitud inversa cuadrada utiliza \(t_0,\ell_0,c_{\rm int}\) de la carta. Este bloque no presenta esas cifras como valores de \(H_0\) o \(\Lambda\) observados.
3. **Alcance de las soluciones.** Están demostradas las identidades y soluciones descritas dentro de sus dominios. La correspondencia con la historia cosmológica observada y la determinación de una amplitud de materia o espín para nuestro universo no se obtienen únicamente de repetir esas identidades.
4. **Corte documental.** Se mantiene el PDF fijo acordado de 2.249 páginas. Los verificadores de continuidad que todavía rotulan una edición histórica no sustituyen este corte ni constituyen evidencia de haber comprobado íntegramente su contenido.

## Fuentes y evidencia reutilizada

- [CT108–de Sitter: propietario completo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_iv/body/B031_ch71_cosmologia_torsional_ct108_608e66fccb17_10_cosmologia.tex:34>): reloj y radio; desde la línea 124, realización y cuádruple.
- [Perron, escala y memoria: propietario completo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_iv/body/B027_ch67_perron_memoria_einstein_cartan_608e66fccb17_10_cosmologia.tex:1>).
- [Atlas de parámetros cosmológicos](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c44_atlas_genealogico_purificado.tex:1055>).
- [Selector de Sitter y rebote](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_iv_v/tex/residencias/86_cosmologia_cerrada.tex:5>); [tensor de traza y referencia nula](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_iv_v/tex/residencias/86_cosmologia_cerrada.tex:174>).
- [Foliaciones y sus curvaturas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_iv_v/tex/residencias/86_perspectivas_cosmologicas_cerradas.tex:83>).
- [Horizonte y media acción: propietario completo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_iv/body/B029_ch69_confluencia_horizonte_area_4d1f0ca1d353_25_horizonte_media_accion.tex:1>).
- [Energía libre y especialización al horizonte](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_iv_v/tex/residencias/71_energia_libre_holografica_cerrada.tex:355>).
- [Plantilla angular del fondo cosmológico](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_iv_v/tex/residencias/86_cosmologia_hojas_sector_oscuro.tex:217>).
- [Valores existentes](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/VALORES_RECALCULADOS_CORPUS.json:1053>) y [operaciones que los calcularon](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_valores_corpus.py:241>).
- [Antecedentes ya comprobados por MASAS](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/RESULTADO_MASAS.md:101>).

Procedencia: **resultados recuperados del corpus**. Se ha efectuado lectura y comprobación algebraica de los pasajes, reutilizando las evaluaciones numéricas existentes. No se han generado nuevas cifras de π o φ, ni recompilado un PDF, ni modificado fuentes o resultados de otra tarea.
