# Incorporación focal del Artículo III y cantera radional conservada

Estado: fragmento de integración redactado y comprobado localmente; no se han modificado ni compilado PDFs. Fecha: 10 de septiembre de 2026.

## Decisión editorial más reciente

El editor comunicó que **II no incorpora un capítulo ni el concepto de radión**: recibe únicamente aportaciones quirúrgicas pertinentes. Para III rige la misma selección por dependencia.

Por ello sólo se propone incorporar **insercion_focal_constitutiva_LC.tex**. El archivo **radion_iii.tex** conserva fuera del PDF la redacción extensa de S_E/S_T, 20/81, ε_R, 50° y cuatro lecturas. No debe incluirse automáticamente, ni presentarse como contenido ya incorporado.

## Contenido de la inserción

La respuesta normalizada (Zhat, chat) recupera los dos autovalores r±. La inversión cúbica ya demostrada recupera s±=q±^30. La composición proporciona:

- y/x=(log s+−log s−)/(log s++log s−);
- η_el=(1/2)log(log s+/log s−);
- Z_LC/Z*=sqrt(log s−/log s+).

La prueba es contigua. Se conserva el dominio de los r±, la orientación de hojas y el cambio de carta dimensional. La razón constitutiva Zhat=f(s−)/f(s+) **no se identifica** con Z_LC/Z*. El reloj ω y la referencia Z* son datos de la realización LC ya presente, no parámetros que este fragmento pretenda generar.

## Ubicación y referencias internas

Incluir la inserción **dentro de la sección del operador constitutivo**, después de la declaración de los tipos dimensionales (final de 04_respuesta_constitutiva.tex), antes de comenzar el ciclo Catalán. Es una subsección, no un capítulo nuevo.

Debe incluirse fuera del grupo que transforma etiquetas heredadas de II. Sus etiquetas comienzan por iii: y son distintas de las de la cantera extensa.

Referencias utilizadas y presentes en III REV02:

- iii:eq:cubic — inversión cúbica;
- iii:eq:dimensions — cartas dimensionales;
- hmtII:eq:ii-elipse-lc — Lη y Cη;
- hmtII:eq:ii-elipse-impedancia — Zη/Z*=exp(−η).

El texto recibe los desarrollos de elipse, Hilbert–Klein y LC ya incluidos en III, pp.111–114 impresas (visor112–115). No los elimina, no cambia sus pruebas ni los duplica. Las mismas piezas se conservan en II REV08, pp.103–106. Su fuente 07b_geometria_elipse.tex es idéntica entre II REV07 y REV08; la residencia vigente de II es REV08.

El editor debe comprobar los enlaces internos al compilar la sucesora y revisar visualmente las páginas modificadas. Esta carpeta no contiene un PDF de entrega ni sustituye esa revisión.

Se comprobaron las cuatro referencias externas del fragmento contra el AUX de III REV02 y las14 copias por identidad SHA-256 con sus originales. El resultado figura en MANIFIESTO_FUENTES.json. El recibo causal RECIBO_CAUSAL_INSERCION.json obtuvo PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY al auditar conjuntamente recibo y fragmento. Estos resultados son focales; no se presentan como un nuevo certificado genealógico integral de la sucesora.

## Procedencia

Las piezas de la composición son RESULTADO_RECUPERADO. La reunión explícita en una proposición que expresa la forma mediante las raíces de las coordenadas constitutivas es FORMALIZACION_NUEVA de una relación ya constituida por esos mapas; no se atribuye una nueva constante o descubrimiento físico. El código focal es CERTIFICADO_NUEVO.

### Fuentes portables conservadas

Las copias de fuentes de esta carpeta son testimonios de procedencia. Sus demostraciones relevantes ya aparecen en III o en la inserción; la copia privada no sustituye la residencia pública.

**fuentes/articulo_III/**

- 04_respuesta_constitutiva.tex: dominio, monotonía, cubicidad e inversión, ecuaciones de dimensiones y conservación de etiquetas. Original: output/ARTICULO_III_VACIO_ELECTROMAGNETICO_20260909_REV02/manuscrito/sections/04_respuesta_constitutiva.tex.
- 07_elipse.tex: η_el=artanh(C*/A), semiejes y forma. Original: output/ARTICULO_III_VACIO_ELECTROMAGNETICO_20260909_REV02/base_articulo_II/sections/07_elipse.tex.
- 07b_geometria_elipse.tex: ley areal, Hilbert–Klein, LC y distinción respecto de la respuesta constitutiva. Original: misma raíz base_articulo_II/sections.

**fuentes/radion_52/** conserva once fragmentos del capítulo52 del integral de2249páginas. Se conservan para la cantera, no se insertan en bloque:

| Resultado | Residencia impresa | Fragmento |
|---|---|---|
| APP, TRIT, TPK y resta por bloques | §52.1.1, desde p.916 | c52_01_01_app_trit_tpk.tex |
| Secciones directa/torsional | §52.2.1, p.923 | c52_02_01_secciones_independientes.tex |
| 2·90/729=20/81 | §52.2.2, pp.923–924 | c52_02_02_densidad_20_81.tex |
| ε_R y cierre | §52.2.3, pp.924–925 | c52_02_03_cociclo_acarreo.tex |
| Segunda fase50° y carta crítica | §52.3.1, pp.926–927 | c52_03_01_registro_critico.tex |
| Memoria helicoidal | §52.5.2, pp.933–934 | c52_05_02_helice_memoria.tex |
| Forma e intercambio energético | §52.6.2, p.936 | c52_06_02_intercambio_constitutivo.tex |
| Cuatro lectores y significado de ε_R | §52.13, desde p.959 | c52_13_00_cuatro_lectores.tex |
| Definición del radión | §52.13.1, desde p.960 | c52_13_01_definicion.tex |
| Teoremas y pruebas reunidas | §52.13.2, pp.961–963 | c52_13_02_teoremas_componentes.tex |
| Controles y perfiles publicados | §52.13.3, desde p.964 | c52_13_03_controles_fuentes_conclusion.tex |

Raíz original de estos once fragmentos:
output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/radion_52/snippets/

Los números de página se usan como localizadores del integral, no como comprobación visual nueva. Las fuentes se cotejaron directamente.

## Ejecución y alcance

Desde esta carpeta:

    python3 -I -S verificar_radion_iii.py

Resultado: PASS_RADION_III_FOCAL, 30 controles. Incluye:

- recuentos y densidades exactos con aritmética racional;
- fase50° y pertenencia de S_E a la celda(1,2) usando los intervalos explícitos del texto;
- 120 restas por bloques, con efecto del coeficiente remoto;
- 325 retornos nonádicos;
- tres testigos racionales de canales y ambas orientaciones, con inversión cúbica;
- recuperación de y/x, η y Z_LC/Z*;
- control negativo de la identificación Zhat=Z_LC/Z*;
- cierre unitario y angular con operandos de prueba;
- unicidad de las etiquetas locales.

La precisión Decimal es200 para amortiguar el condicionamiento de la inversión cuando r está próximo a1. Los testigos x,y son pruebas matemáticas deliberadamente ajenas a los valores físicos; no intervienen en el generador HMT. Estos controles no vuelven a certificar la generación de π,e,φ,α ni una identificación SI, y no sustituyen la prueba simbólica del fragmento.

No se ha creado un archivo Lean nominal. No se afirma haber formalizado esta proposición en Lean.

## Puertas heredadas y alcance de la incidencia documental

En este encargo el núcleo formal permanente y la autocomprobación causal de constantes respondieron PASS. El envoltorio general de masas se detuvo antes de su cálculo por la divergencia de hash de DOCUMENTOS_DE_REFERENCIA_HMT_MD.md, índice que estaba actualizándose en la tarea editora. No se modificó ese índice ni sus manifiestos. El fallo se comunicó al editor; no se atribuyó a una ecuación del radión ni se presentó como una ejecución satisfactoria del envoltorio.

El control focal que acompaña esta carpeta tiene un ámbito distinto y consta expresamente arriba. El editor conserva la responsabilidad de la integración, el recibo de la sucesora y la revisión visual.
