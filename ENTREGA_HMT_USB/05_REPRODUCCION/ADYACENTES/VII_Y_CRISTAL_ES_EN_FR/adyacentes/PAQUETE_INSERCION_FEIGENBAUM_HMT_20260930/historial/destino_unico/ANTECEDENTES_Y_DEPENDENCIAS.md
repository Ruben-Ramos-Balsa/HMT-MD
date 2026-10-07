# Antecedentes operatorios para la inserción de Feigenbaum

## Material entregado y alcance

Se han creado exclusivamente estos dos fragmentos nuevos:

- `latex/00_antecedentes_operatorios.tex`: antecedentes APP–TRIT–TPK, transporte levantado y calendario, cobertura efectiva por cilindros, carta ordenada interna, descenso por fibras, selección de las doce fases y del lector uniforme, transporte de iteradas/raíces/mínimos y representación espectral finita.
- `latex/00a_transiciones_nonadicas.tex`: recuperación íntegra del propietario `ch_tres_vueltas_ext.tex` de XI REV11. Conserva las 855 líneas del cuerpo de origen, incluida la tabla de veintisiete incidencias, las actualizaciones campo por campo y sus dos pruebas. Sólo se antepone `hmtfg:` a las etiquetas y sus referencias; tres líneas iniciales nuevas documentan la procedencia.

Este material es un bloque de inserción en la monografía que ya contiene el núcleo común HMT y la construcción conjunta del continuo. No sustituye ese cuerpo anterior ni presenta el recorte como una reedición autónoma de todo XI. Las definiciones y las pruebas específicas utilizadas para el lector de Feigenbaum quedan contiguas. No se han editado publicaciones, recalculado certificados ni compilado documentos.

## Inclusión y preámbulo

Desde un archivo maestro situado en la raíz del paquete:

```tex
\providecommand{\HMTFGRoot}{.}
\input{\HMTFGRoot/latex/00_antecedentes_operatorios.tex}
```

Ese fragmento contiene una única inclusión adicional:

```tex
\input{\HMTFGRoot/latex/00a_transiciones_nonadicas.tex}
```

No hay inclusiones hacia archivos propietarios externos ni dependencias de notas privadas. El fragmento maestro INSERCION_FEIGENBAUM.tex recibe la raíz mediante HMTFGRoot y encapsula localmente los alias de símbolos para conservar el significado de las operaciones sin cambiar el preámbulo exterior.

Requisitos del preámbulo:

- `amsmath`: ecuaciones, alineaciones, casos, `\operatorname`, `\eqref`, `\text`.
- `amsthm`, con entornos `proposition`, `lemma` y `proof`. Se respetará la numeración ya utilizada por el archivo maestro.
- Alfabetos y símbolos `\mathbb`, `\mathfrak`, `\mathscr`, `\varnothing`, `\twoheadrightarrow`, `\bigsqcup` y `\frown`. Son suficientes `amssymb,mathrsfs` en una configuración clásica; el preámbulo de XI emplea `unicode-math` con STIX Two Math.
- `booktabs`: `\toprule`, `\midrule` y `\bottomrule` en la tabla de veintisiete incidencias.
- Idioma español y codificación UTF-8. El fragmento no prescribe motor ni tipografía.

El propio fragmento proporciona con `\providecommand` los alias `\ZZ`, `\RR`, `\FF`, `\APP`, `\TPK` y `\TRIT`. Este último debe tener el significado del propietario: `\{-1,0,+1\}`. Si el maestro ya define alguno con otro significado, corresponde reconciliarlo en la inclusión; `\providecommand` conserva la definición previa.

Todas las etiquetas y referencias internas de los dos fragmentos tienen el prefijo `hmtfg:`. No se requieren macros privadas de XI. El archivo complementario se incluye una sola vez.

## Propietarios materiales exactos

### A. Núcleo y prolongaciones TPK de XI REV11

Directorio propietario completo:

`/Users/ruben/Documents/New project/output/PREPARACION_ENTREGA_USB_20260928/ENTREGA_HMT_USB/03_FUENTES_Y_REPRODUCCION/ACTUALIZACIONES_20260928/FINAL01/PAQUETES/ARTICULO_XI_REV11_ES_EN_FINAL_BN_20260928/ARTICULO_XI_REV11_ES_EN_FINAL_BN/ES/source/`

| Archivo relativo a ese directorio | Material utilizado | Tratamiento en el paquete |
|---|---|---|
| `sections/nucleo.tex` | Célula APP completa, residuos y cocientes; reducción trítica balanceada; selector `M_ph`; factorización de la actualización | Definiciones y prueba de conservación reexpresadas en §«Células aritméticas, orientación y transporte», sin cambiar operaciones |
| `sections/tpk_desarrollo_integrado.tex:22–165` | Configuración `Q_obs`, fase nonádica, sector dodecafásico, cursores, levantamiento de frontera, `F_obs`, retorno 108 | Fórmulas y prueba completas pertinentes reunidas en la primera subsección |
| `sections/ch_tres_vueltas_ext.tex:1–855` | Modelo autónomo arista por arista; célula completa; tres parejas; acarreo balanceado; memoria graduada; 27 incidencias; Sel–Tra–Upd; portador generado; truncamientos; prueba de realización; tres prolongaciones efectivas | Cuerpo íntegro incluido en `00a_transiciones_nonadicas.tex`; transformación mecánica de etiquetas exclusivamente |
| `sections/ch_elevacion_catalogal.tex` | Composición de seis vueltas en 54 aristas; `Y_N`; biyección `beta_blk,N`; compatibilidad con truncamientos; 729 subcilindros no vacíos | Definiciones y pruebas pertinentes reunidas en §«Refinamiento de cilindros y lectura ordenada» |
| `sections/ch_cierre_cardinal.tex:375–497` | Lector radix 729; partición; contracción; `P_ar`; cociente; realización dentro de `G_HMT`; isomorfismo ordenado interno y cobertura de todos los elementos internos | Definiciones y prueba contigua de cobertura; expansión expositiva de la unicidad del cuerpo ordenado completo utilizada por el propietario |
| `sections/ch_descenso_por_fibras.tex:10–39` | Criterio necesario y suficiente para descender una operación y prueba de buena definición | Enunciado y prueba completos pertinentes en §«Descenso por fibras y conservación del selector» |

El universo `\mathfrak G_HMT(h,m_\infty)` se mantiene como universo **interno**. La carta `\iota` es el isomorfismo llamado `\eta` en XI. Se cambia la letra únicamente para distinguirlo del lector de pesos `\eta_0` del perfil de criticidad. El dominio y el codominio siguen siendo `\mathbb R_HMT^G` y `\mathbb R^G`, respectivamente.

El fragmento no traslada la parte de XI dedicada a clasificación cardinal general, condensación, inyecciones hacia potencias, ni las demostraciones Hensel que sirven a la biyección adicional con `\mathbb Z_3^6`. Para esta aplicación se utiliza la biyección explícita entre palabras de seis trits y prolongaciones TPK; esa biyección y su prueba sí se incluyen. La construcción general del universo y del continuo conjunto permanece en el núcleo ya publicado de la monografía de destino.

### B. Perfil de criticidad de la monografía integral

Propietario exacto:

`/Users/ruben/Documents/New project/output/TRATADO_GENERATIVO_HMT_MD_20260919/REV03/source/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/feigenbaum/c37_feigenbaum.tex`

El comienzo del capítulo ya contiene:

1. La sección angular `\mathcal P_crit(m)=(30m-10)pi/180`, con representantes, orientación y orden fijados.
2. El funcional uniforme `\eta_0=12^{-1}\sum_m`.
3. `D_0=899/648`, la normalización `s_0=36/(pi sqrt899)` y las frecuencias `k_m=2(3m-1)/sqrt899`.
4. La suma de doce cosenos, su forma trigonométrica cerrada, la expansión cuadrática y cuártica y la familia `f_lambda=1-lambda u_0`.
5. Las propiedades analíticas y de criticidad de esa familia.

El fragmento 00 incluye íntegramente las definiciones de los puntos 1–4 y la prueba pertinente de normalización y forma cerrada. Las propiedades dinámicas posteriores residen en los restantes fragmentos del paquete. No se introduce el valor de Feigenbaum para elegir fases, pesos o normalización.

**Tipo de la selección:** la sección angular y el lector uniforme son los datos operatorios declarados de este perfil HMT. La reconstrucción ordenada no convierte por sí sola a ese perfil en la única publicación posible del calendario. El texto conserva exactamente la sección ya fijada por el propietario.

### C. Representación espectral y entrelazamiento

Propietario del mecanismo de momentos/Jacobi:

`/Users/ruben/Documents/New project/output/GRASSMANNIANOS_CUBO_HISTORICO_REV07_20260928/ES/source/sections/jacobi_spectral.tex:35–136`

Propietario de la especialización a Feigenbaum y del transporte de selectores:

`/Users/ruben/Documents/New project/output/FEIGENBAUM_HMT_DESARROLLO_20260929/TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md:581–729`, §14.

El fragmento recupera:

- §14.1: `u_HMT`, la familia `F_a`, las iteradas `S_n^HMT`, el entrelazamiento por la carta ordenada y la conservación de conjuntos de raíces, periodo exacto y mínimos.
- §14.2: nodos `s_m=4(3m-1)^2/899`, medida atómica uniforme `\nu_0`, matrices de Hankel, polinomios ortogonales, `Q`, `D`, `J_12` y la identidad exacta del perfil con `e_0^T[I-cos(x sqrt(J_12))]e_0`.
- La prueba de recurrencia de tres términos y el entrelazamiento espectral, escrita contiguamente para esta medida atómica.

**Distinción de medidas:** el propietario de Grassmannianos desarrolla inicialmente una medida continua positiva por intervalos. Feigenbaum utiliza una medida atómica de doce nodos. Se recupera el mecanismo de Gram–Schmidt y Jacobi, no los coeficientes numéricos de la medida continua. Para `\nu_0` hay normas positivas en grados 0–11 y norma nula en grado 12; la matriz tiene dimensión 12. Los coeficientes incluidos son los ya calculados para este perfil: `a_0=2`, `beta_1=2493348/808201`.

## Clausura local de las dependencias

| Afirmación utilizada después | Dependencia efectiva contigua en estos fragmentos | Alcance conservado |
|---|---|---|
| Tres continuaciones de cada vuelta | 27 incidencias, Sel–Tra–Upd y truncamientos completos de `00a` | Rutas construidas, no prolongaciones supuestas |
| 729 sucesores de un bloque | Composición de seis vueltas y decodificador de registros | Refinamiento que conserva prefijo y memoria |
| Cobertura total del lector | Partición de cilindros, diámetros tendentes a cero y completación | Todos los elementos de la realización interna declarada |
| Operaciones visibles bien definidas | Criterio de descenso por fibras | Se comprueba la operación concreta; una mera biyección no basta |
| Familia y normalización | Sección de doce fases, lector uniforme, segundo momento y perfil | Publicación HMT fijada antes de comparar una constante |
| Transporte del mínimo de raíces | Isomorfismo de orden, serie de coseno e iteración conjugada | Conservación del mínimo cuando existe; no sustituye su prueba dinámica |
| Representación espectral | Medida positiva de doce nodos, Hankel, Gram–Schmidt y matriz ortogonal | Igualdad exacta de funcional y perfil, con dimensión y medida explícitas |

## Conservación editorial y estado

Se mantiene entero el propietario de las tres prolongaciones, incluida su narrativa y sus pruebas. Los otros cortes reúnen las definiciones y demostraciones utilizadas por este resultado; no sustituyen ni reducen los capítulos propietarios. El texto integral previo, sus figuras, las cinco construcciones conjuntas del continuo y las otras aplicaciones de XI quedan fuera del ámbito de edición de este frente y deben conservarse en la monografía.

La inclusión del archivo 00 no certifica por sí sola que el manuscrito de destino haya incorporado ya las dependencias anteriores. El integrador debe situarlo después del núcleo común y antes del perfil/dinámica de Feigenbaum, conservar los capítulos de origen y resolver la eventual repetición expositiva sin ablaciones.

No se ejecutó compilación. No se iniciaron pruebas nuevas, búsquedas matemáticas adicionales ni verificadores de resultados. Los certificados y su correspondencia con la tesis final pertenecen al control global del paquete.
