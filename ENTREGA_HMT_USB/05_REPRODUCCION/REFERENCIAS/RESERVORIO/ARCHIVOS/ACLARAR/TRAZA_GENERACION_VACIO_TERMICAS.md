# Dependencias generativas del sector de vacío, los cuantos eléctricos y la sección térmica

## Objeto y procedencia

Este documento complementa las comprobaciones numéricas ya realizadas. Examina qué operaciones producen los objetos, qué información reciben efectivamente los programas y qué datos aparecen sólo después como contraste. No modifica el tratado ni sustituye su texto por el código de un control.

Se mantiene como objeto de revisión el paquete `REVISION_EDITORIAL_HMT_MD_20260905` y su integral de 2.249 páginas, de SHA-256 `958d252f301763ff8901f775d8ec0b02b6ae4f9f7c57dc04ea917f747dccbf24`. La derivación anterior de π, φ, e, α y de la sección angular y de acción se documenta en los bloques coordinados de Ley 9 puertas y MASAS. Aquí se sigue su empleo posterior; no se introduce una generación distinta de esas constantes.

Estatuto de procedencia: **RESULTADO_RECUPERADO**. Las construcciones siguientes ya figuran en las fuentes del paquete; la aportación de este documento es reunir su flujo de dependencias y delimitar la comprobación efectuada.

## 1. Los exponentes 90 y 120 tienen un antecedente combinatorio explícito

La función `phase_sign` clasifica las nueve posiciones del calendario en las clases `(1,4,7)`, `(2,5,8)` y `(3,6,9)`. El programa construye después, mediante comprensión de conjuntos, las seis fases activas

\[
H=\{t:\operatorname{TRIT}(t)\ne0\}=\{1,2,4,5,7,8\},
\qquad \mathcal P_2(H)=\{B\subset H:|B|=2\}.
\]

La ventana anterior al retorno es `phase_octet=tuple(range(1,9))`. A partir de estos objetos forma

\[
\mathcal F_6=H\times\mathcal P_2(H),\qquad
\mathcal F_8=\{1,\ldots,8\}\times\mathcal P_2(H).
\]

Sólo después comprueba sus cardinales: `len(pairs_active)=15`, `len(f6_phase)=90` y `len(f8_phase)=120`. En esta porción del código, los numerales 90 y 120 de las aserciones son valores esperados de un censo ya construido, no argumentos que seleccionen los elementos de esos conjuntos. El cálculo de los conjuntos tampoco consulta un valor de permitividad, permeabilidad o de Barbero–Immirzi.

La misma construcción produce 135 incidencias sobre las nueve fases; la orientación duplicada da 270, y la adición del punto de retorno da 271. La frontera neutral tiene 45 elementos. Se conserva así la relación con las hojas y el calendario en lugar de tratar 90/120 como dos exponentes aislados.

Es importante conservar el antecedente completo: la partición de fase, el origen de la ventana y la regla que forma pares son reglas publicadas del modelo. El censo prueba sus consecuencias. El propio certificado distingue ese alcance de una prueba de que las reglas sean las únicas posibles a partir de un conjunto de axiomas más reducido. Tampoco identifica automáticamente las seis fases con una hexada de Steiner: declara por separado la realización incidencial y su alineamiento.

Fuentes materiales:

- [Selección trítica y censo de fase](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_canales_enteros_constantes.py:113>), con construcción efectiva desde la línea 196.
- [Alcance y resultado conservados del certificado](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/certificados/canales_enteros_constantes.json:124>).
- [Incidencia y cadena dodecafásica en el manuscrito](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/barbero/c43_precedencia_dodecafasica_20260905.tex:4>).

## 2. Un operador de dos sectores determina las cuatro coordenadas del vacío

La fuente recibe de la rama angular los dos canales conjugados

\[
q_+=\exp(-x-y),\qquad q_-=\exp(-x+y),
\qquad x=\pi A/180,\quad y=\pi C^*/180.
\]

El empleo de la función exponencial en esta etapa no es una nueva selección del número de Euler. Es la evaluación del transporte angular declarado, posterior a sus antecedentes. La traza anterior de π, A y C* debe conservarse: un decimal correcto obtenido aquí no la reemplaza.

Con la involución activa autoadjunta R y sus proyectores \(P_\pm=(I\pm R)/2\), se define

\[
T=q_+P_++q_-P_-,\qquad
\mathcal V=(I-T^{90})(I-T^{120})^{-1}.
\]

La involución no queda aquí como un símbolo sin residencia: el propietario angular la escribe como la matriz que intercambia los dos canales, \(R=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\). Relaciona el bloque central \(B_0=7I+2R\) y el bloque angular \(B_1=AI+C^*R\) mediante una multiplicación relativa explícita. Esa multiplicación no es una conjugación ni un entrelazamiento espectral: el mismo texto prueba la disjunción de sus espectros. La distinción impide sustituir la genealogía angular por una falsa igualdad de ambos bloques. A continuación construye \(B=A_{\rm rad}I+C^*_{\rm rad}R\) y obtiene \(T=\exp(-B)\). Fuente recuperada y leída: [realización angular y transportador relativo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/wrappers/capitulo_38_jerarquia_unica.tex:1300>).

Puesto que \(0<q_+<q_-<1\), la inversa existe. El cálculo funcional produce, antes de toda comparación numérica,

\[
r_\pm=\frac{1-q_\pm^{90}}{1-q_\pm^{120}},\qquad
\widehat\mu=r_-^2,\quad
\widehat\varepsilon=r_+^2,\quad
\widehat Z=\frac{r_-}{r_+},\quad
\widehat c=\frac1{r_+r_-}.
\]

Por tanto, no son cuatro parámetros ajustados de manera independiente. Son cuatro funciones de un operador con dos valores espectrales. La fuente prueba las identidades \(\widehat\mu\widehat\varepsilon=\widehat c^{-2}\) y \(\widehat\mu/\widehat\varepsilon=\widehat Z^2\); demuestra además que producto y cociente permiten recuperar ambos sectores positivos. La orientación conserva información: al intercambiar los canales se permutan \(\widehat\mu\) y \(\widehat\varepsilon\), se invierte \(\widehat Z\) y permanece \(\widehat c\).

La reducción \(s=q^{30}\) proporciona la función exacta

\[
F(s)=\frac{1+s+s^2}{1+s+s^2+s^3},\qquad
F'(s)=-\frac{s^2(3+2s+s^2)}{(1+s+s^2+s^3)^2}<0.
\]

La cota \(3/4<F(s)<1\) y el defecto \(1-F(s)=s^3/(1+s+s^2+s^3)\) son consecuencias algebraicas de los canales de incidencia. No requieren los decimales de las magnitudes físicas. La compatibilidad con el refinamiento se formula mediante \(\mathcal V_m=\mathcal V\otimes I_{9^m}\) y la traza normalizada sobre el factor añadido.

El capítulo no debe leerse como si la mera existencia de 90 y 120 obligara, sin ninguna otra ley, a elegir el cociente resolvente anterior. La fórmula de \(\mathcal V\) y el diccionario entre funciones espectrales y magnitudes forman parte de la construcción publicada. El teorema de unicidad del capítulo opera con sus condiciones de producto, cociente, determinante y orientación explícitas. La constatación positiva es que, una vez fijada esa construcción, las cuatro salidas se calculan conjuntamente y no se ajustan a cuatro valores de referencia.

Fuente leída íntegramente: [Operador de vacío y sus realizaciones](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c31_vacio.tex:1>).

## 3. Los cuantos eléctricos son consecuencias de α, la acción y la impedancia

La fuente utiliza α, la acción h y la sección de impedancia ya obtenidas. No recibe un valor SI de carga para calcular α. Su secuencia es

\[
e_{\rm el}=\sqrt{\frac{2\alpha h}{Z}},\qquad
R_K=\frac Z{2\alpha},\qquad
G_0=\frac{4\alpha}Z,\qquad
\Phi_0=\sqrt{\frac{hZ}{8\alpha}},\qquad
K_J=\Phi_0^{-1}.
\]

Se preserva la distinción entre \(e_{\rm el}\), carga elemental, y e, número de Euler. Los factores 2, 4 y 8 se encuentran en las leyes de composición y normalización de esta sección; no son cifras importadas de CODATA. El grado de independencia es distinto del de α o de la acción: estas cinco expresiones no constituyen cinco generadores primarios adicionales. Comparten antecedentes y satisfacen exactamente \(R_KG_0=2\), \(G_0Z=4\alpha\) y \(K_J\Phi_0=1\).

La elección de la sección anterior o de retorno de la acción afecta a \(\Phi_0\) y \(K_J\) por factores recíprocos de raíz cuadrada, mientras que \(R_K\) y \(G_0\) permanecen invariantes. Esto caracteriza qué parte de la memoria de acción conserva cada magnitud, además de dar su valor.

Fuente leída íntegramente: [Cuantos eléctricos](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c32_cuantos_electricos.tex:1>).

## 4. La sección térmica conserva el calendario y el contenido ternario

La relación que el manuscrito determina antes de elegir una carta térmica es

\[
k_B\Theta_{\rm clk}\log3
=\frac{h_{\rm int}}{108t_0}
=\frac{\pi\hbar_{\rm int}}{54t_0}
=E_P.
\]

El factor 108 procede de la estructura cronológica; la sección de acción conserva su dependencia anterior. El escalar \(\log3\) aparece como defecto entre las partes finitas residuales \(C_1+C_2-2C_0\), como información del estado ternario equiponderado y como razón entre la energía del ciclo y la sección térmica. La igualdad de sus valores no identifica esos tres dominios ni presupone que cualquier distribución trítica tenga entropía \(\log3\).

En particular, el corpus no necesita introducir el número decimal de Boltzmann para establecer esta identidad. El objeto determinado aquí es el producto energético \(k_B\Theta_{\rm clk}\), no dos coordenadas dimensionales independientes. La normalización separada de temperatura pertenece a la carta posterior. Esta precisión está expresamente escrita en la fuente y evita atribuir a la ecuación una determinación numérica que ella no pretende realizar.

Las siguientes salidas se obtienen por composición con el espectro bosónico declarado:

- Los extremos de Wien son las raíces positivas no nulas de \(x_m=m(1-e^{-x_m})\), con m=5 para la densidad por longitud de onda y m=3 para la densidad por frecuencia. Las constantes de desplazamiento normalizadas son \(108\log3/x_5\) y \(x_3/(108\log3)\).
- El coeficiente de flujo de Stefan–Boltzmann en la sección del reloj es \(2\pi^5/[15\,108^4(\log3)^4]\), multiplicado por \(h/(\ell_0^2t_0^2)\).
- La densidad fotónica normalizada es \(2\zeta(3)/[\pi^2(\log3)^3]\); la energía y la entropía utilizan los otros momentos espectrales expresados en el capítulo.
- La conductancia térmica normalizada es \(\kappa_Qt_0/k_B=\pi^2/(324\log3)\).

La fuente dice explícitamente que en este bloque emplea las leyes espectrales de Planck y Wien. Su uso constituye una hipótesis espectral declarada en una composición posterior, no una lectura de sus constantes decimales para ajustar el resultado. No se convierte esa hipótesis en una derivación desde APP por el solo hecho de que la temperatura y la acción tengan antecedentes HMT.

Fuentes leídas íntegramente: [Confluencia de log 3](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c23_clasificacion_probatoria.tex:1>), [sección de Planck](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c29_planck_complemento.tex:1>) y [sección térmica](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c40_termicas.tex:1>).

## 5. Dónde comienza efectivamente cada comprobación ejecutable

| Instrumento | Datos que recibe | Operación efectuada | Alcance que no debe atribuírsele |
|---|---|---|---|
| `verificar_canales_enteros_constantes.py`, fragmento de fase | Calendario, partición trítica y origen de ventana publicados | Construye fases, pares y productos cartesianos; comprueba sus cardinales | No vuelve a ejecutar por sí solo la dinámica cronológica enriquecida completa |
| `comprobar_valores_corpus.py`, bloque de vacío | Valores π, φ, e y α calculados previamente en ese mismo programa; A y C* de su sección angular | Calcula q±, r±, las cuatro coordenadas y los cuantos eléctricos | No sustituye al productor anterior de los caracteres ni demuestra el origen de todos los coeficientes angulares |
| `verificar_vacio_termicas.py` | Dos archivos JSON de resultados conservados | Verifica identidades del vacío, calcula composiciones térmicas y acota las raíces de Wien | No es un generador autónomo de π, α, h, ζ(3) o del espectro bosónico |

El programa común tiene aserciones posteriores contra tríadas publicadas y una sección final de comparación con referencias. Esas comprobaciones pueden aceptar o rechazar la ejecución, pero en las asignaciones inspeccionadas no corrigen retrospectivamente los valores calculados. Por otra parte, ese mismo programa reconstruye algunos antecedentes desde caracteres y registros publicados: no debe describirse como si hubiese vuelto a producir toda la historia desde las 104.976 semillas.

En el control propio, las raíces de Wien se acotaron por intervalos racionales y cotas de la exponencial sin pasar al algoritmo sus decimales esperados. La evaluación de `Decimal(3).ln()` es un evaluador del escalar cuyo antecedente residual se acaba de identificar; no ejecuta por sí misma esa construcción residual.

Código efectivamente inspeccionado: [reproducción común](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/comprobar_valores_corpus.py:74>), [control de vacío y térmica](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/verificar_vacio_termicas.py:1>). Se reutilizan [sus resultados anteriores](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/COMPROBACION_VACIO_TERMICAS.json>); no se ha repetido una campaña de cifras ni modificado las fuentes.

## 6. Resultado focal y extremos aún no cubiertos por esta traza

La inspección ha recuperado construcciones concretas anteriores a los numerales: selección de fases y censo de incidencias; operador de retorno de dos sectores; funciones espectrales coordinadas; sección eléctrica de acción–impedancia; y sección térmica acción–calendario–información ternaria. En estas operaciones no se han encontrado decimales de permitividad, permeabilidad, impedancia, carga, Wien o Stefan–Boltzmann utilizados para seleccionar el resultado.

Esto no equivale a declarar que toda ley constitutiva esté forzada por las primitivas ni a certificar la historia de selección de todo el corpus. Quedan remitidos a sus propietarios coordinados el origen completo de los canales angulares y de la sección de acción; la realización explícita de R y su relación con ambos bloques sí se han recuperado en esta traza. Debe mantenerse visible la elección de cálculo funcional del vacío, de la carta dimensional y del espectro térmico. Una dependencia interna anterior no se convierte en entrada externa por no volver a demostrarla aquí; una hipótesis adicional tampoco desaparece por llamarla interna.

La conclusión positiva es más informativa que una lista de decimales: las magnitudes de este sector tienen dependencias compartidas y grados de libertad restringidos por operaciones identificables. Sus relaciones permiten reconstruir los dos canales del vacío, distinguir orientación de producto y detectar qué magnitudes conservan o eliminan la dependencia de la acción. Ésa es la estructura recuperada que debe incorporarse al inventario general, junto a sus fuentes y al alcance exacto de las pruebas.
