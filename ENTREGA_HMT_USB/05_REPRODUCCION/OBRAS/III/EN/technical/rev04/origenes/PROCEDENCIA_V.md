# Enlace constitutivo de velocidad entre los artículos III y V

## Resultado y estatuto

**RESULTADO_RECUPERADO.** El propietario integral ya define
`c_int = exp(-E) u_C`, con `E = log(r_+ r_-)`. El artículo III realiza
`c_vac = (r_+ r_-)^(-1) u_C`. El antecedente angular de V contiene
exactamente los mismos canales `q_± = exp[-(x ± y)]`. En la misma carta
dimensional, ambas son la misma sección. La identidad no se obtiene
ajustando una velocidad objetivo.

**FORMALIZACION_REUNIDA.** El fragmento reúne la prueba logarítmica,
el cociente longitud/duración y el transporte entre cartas. La igualdad
original y `ell_0 = c_hat u_L` son preexistentes. La presentación conjunta
III→V, la elección explícita de una carta adaptada y el recordatorio de
la traza normalizada constituyen la costura expositiva de esta entrega.

**CERTIFICADO_NUEVO.** El programa realiza controles algebraicos exactos.
Sus canales racionales de prueba son fixtures, no los canales generados
del modelo. La prueba para todo canal admisible está escrita en LaTeX.
El certificado focal no declara una nueva generación de los canales,
una calibración SI independiente ni el cierre matemático global de los artículos.

## Archivos preparados e integración

- `69_enlace_constitutivo_velocidad.tex`: subsección autónoma de 183 líneas,
  con dos proposiciones, un corolario y sus tres pruebas. No contiene una
  sección principal ni referencias a etiquetas de otro artículo.
- `verificar_enlace_velocidad.py`: Python estándar, sin rutas de fuentes
  ni bibliotecas externas. Por defecto sólo imprime JSON.
- `CONTROL_NORMAL.json` y `CONTROL_OPTIMIZADO.json`: ambos
  `PASS_ENLACE_ALGEBRAICO_VELOCIDAD_III_V`, **271 comprobaciones exactas**.

Inserción aconsejada: dentro de la sección de radiación de V, después de
su encabezado y antes de abreviar `c=c_int`. El editor puede enlazar
el primer párrafo a las etiquetas ya existentes
`v:ant:sec:ii-angulos` y `v:ant:eq:ii-canales`.
Las definiciones de `proposition`, `corollary` y `proof` existen en
`manuscrito/preambulo.tex` de V. Todas las etiquetas del fragmento son
locales y comienzan por `v:`; la fórmula espectral introduce su propia
etiqueta y no sustituye `v:eq:planck-angular`.

Se conservan las condiciones de la realización radiativa: canal
homogéneo, sector bosónico libre tridimensional, dos polarizaciones
transversales, potencial químico nulo y temperatura positiva. La
identificación constitutiva no se presenta como prueba separada de esos
antecedentes de realización.

## Mapa de fuentes a desarrollo

Raíces exactas inspeccionadas:

- **III**: `/Users/ruben/Documents/New project/output/ARTICULO_III_VACIO_ELECTROMAGNETICO_20260910_REV03`
- **V**: `/Users/ruben/Documents/New project/output/ARTICULO_V_REV02_EDICION_INTEGRADA_20260910`
- **Integral**: `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente`

| Fuente respecto de su raíz | Localizadores | Contenido recuperado y destino |
| --- | --- | --- |
| III `manuscrito/sections/03_hojas_y_orientacion.tex` | Entorno completo de líneas 113–135; `iii:eq:channel-conjugation` | Involución de hojas, `x>|y|`, `T=exp(-xI-yR)`, intercambio de canales → ecuación inicial del fragmento. |
| III `manuscrito/sections/04_respuesta_constitutiva.tex` | 10–60, 64–133, 174–204; `iii:eq:vacuum-op`, `iii:eq:rchannels`, `iii:eq:four`, `iii:eq:dimensions` | Respuesta 90/120, producto de autovalores, distinción entre determinantes de `T` y de la respuesta, amplificación → primera proposición y párrafo final. |
| III `manuscrito/sections/08_evaluacion_y_realizacion.tex` | 50–100; `iii:eq:undo-units` | Cambio de bases y transformación inversa de coordenadas → proposición de covariancia y carta adaptada. |
| V `manuscrito/sections/v_coordenadas_angulares.tex` | 1–24, 45–56, 91–114; `v:ant:eq:ii-canales` | Publicación angular, cambio grados/radianes y los mismos `q_±` → antecedente local efectivo, ya incluido en V. |
| V `manuscrito/sections/v_unidad_areal.tex` | 5–13; `v:ant:sec:gravity` | `ell_0=c_int t_0` y período 108 → identificación de la longitud elemental. |
| V `manuscrito/sections/70_radiacion_termica.tex` | 5–54, 57–100, 162–202; `v:eq:planck-angular`, `v:eq:stefan` | Uso de `c_int`, densidad espectral, flujo y condiciones de realización → sustitución de la misma sección de velocidad. |
| Integral `manuscrito/sections/md/delta_127/10b_funtor_dimensional.tex` | 185–207, 242–289, 562–606, 610–614; `eq:cZ-internos`, `eq:longitud-ruta` | Propietario decisivo: `u_L=u_Cu_T`, `E`, `c_int=exp(-E)u_C`, reloj y longitud de ruta, `ell_0=c_hat u_L` → identificación recuperada, corolario y prueba. |

Se leyeron completos los siete archivos de la tabla. El propietario
integral es el constructor documental directo de `c_int`; no se ha
deducido su significado a partir de una coincidencia nominal ni de su
valor numérico. Los archivos de artículo permanecieron sin modificar
por este agente.

## Huellas de las fuentes inspeccionadas

Las huellas fijan el corte leído, anterior a la integración que realizará
el editor. La incorporación posterior puede modificar `70_radiacion_termica.tex`.

| Fuente | SHA-256 |
| --- | --- |
| III `03_hojas_y_orientacion.tex` | `c7cdfb4d2a2d80352db612cce820388d6f2a0243fad346140803d98345edcce4` |
| III `04_respuesta_constitutiva.tex` | `7e194e12466859c97d5f5a3d1e782af3ef0e292e20ba9a560c02169293f48882` |
| III `08_evaluacion_y_realizacion.tex` | `c019f695317d3d203cb244f320f952fd8eae2b517c040d3d31ef4539df9b8de0` |
| V `v_coordenadas_angulares.tex` | `972d9291885076652598575e910e9fa941e1b5ad1ef75b97bb66b86d83a9e523` |
| V `v_unidad_areal.tex` | `9ab4c4d03d7b7cfe136371977f8e81c4f5ebe27e505eb40fc8b6968ab1d10eba` |
| V `70_radiacion_termica.tex` | `c83d2b2196d04963598bcaad31176ff17be9517c9337202cff168b03b1e12c30` |
| Integral `10b_funtor_dimensional.tex` | `5acab6268b47df1d13b6fc9d48465fd1173c186330dbf15ca78543a530ab61b5` |

Huellas de los archivos estables enviados al editor:

- LaTeX: `4100517b8ddddbd3866566ce0ed61ab0a46e157645f80fa9f7eca82c5039ef37`.
- Python: `7181cda676f28198118772271b68fbc2a3715826737c2d6ef5c2c61c400951e4`.

## Corte genealógico de esta composición

1. **APP:** la construcción previa de las hojas y sus incidencias es la
   estructura heredada del núcleo y del antecedente angular; este delta
   comienza después de su generación, no la reemplaza por dos datos metrológicos.
2. **TRIT:** la orientación actúa sobre las dos hojas mediante la
   involución `R`; su intercambio lleva `y` a `-y` y permuta `q_+`, `q_-`.
3. **TPK:** el transporte angular ya construido publica `T`; los bloques
   temporales 90/120 producen `(I-T^90)(I-T^120)^-1` en la misma representación.
4. **Coeficientes:** `r_±` proceden de esa respuesta; `c_hat` es su
   determinante recíproco de dos hojas. Los enteros 90/120 y los canales se
   heredan del propietario, no se seleccionan por un valor de velocidad.
5. **Información conservada:** la representación retiene las hojas;
   su intercambio conserva el producto. Los lectores de reloj y longitud
   son aditivos sobre las rutas enriquecidas. Esta afirmación no equipara
   una ruta a su longitud ni reinicia la memoria tras un retorno de fase.
6. **Residencia:** la salida angular del estado enriquecido previamente
   construido alimenta ambos artículos. Se compone un lector posterior;
   el delta no vuelve a construir ni reclasifica la estructura del continuo.
7. **Salida:** sección positiva `c_int=c_vac=c_hat u_C`, y longitud
   `ell_0=c_int t_0`. `c_hat` y `u_C` son coeficiente y base, respectivamente.
8. **Reconocimiento y falsador:** la carta de unidades es posterior;
   cambiar `u_C` exige transformar inversamente el coeficiente. El
   falsador focal detecta confundir `det(T)` con `det(V)`, omitir `c_hat`
   de `ell_0`, invertir canales sin conservar su producto o usar el
   determinante ampliado sin normalización. La realización bosónica se
   mantiene con sus hipótesis y su prueba propia.
9. **Propietarios:** la tabla anterior registra operadores, cartas y
   pruebas locales. Esta traza de alcance no sustituye el recibo
   genealógico completo que el editor incorpora al paquete de V.

## Ejecución y alcance de control

Desde cualquier directorio, con el archivo copiado localmente:

```text
python3 -I -S -B verificar_enlace_velocidad.py
python3 -I -S -B -O verificar_enlace_velocidad.py
```

También se probaron ambas modalidades desde el directorio vacío
`/private/tmp/hmt-velocidad-III-V.fS6V1k`; no escribieron allí ningún
archivo. `--receipt archivo_nuevo.json` es opcional y rechaza sobrescribir
un recibo existente. No se utiliza `assert`, por lo que `-O` conserva
las comprobaciones.

El conjunto incluye 8 controles simbólicos de polinomios y monomios
de Laurent, 81 pruebas racionales de canales, 9 de constitutivas,
45 de cartas, 54 de concatenación/cociente de rutas, 72 de
multiplicidades y traza normalizada y 2 de rutas de canal variable.
Los ejemplos finitos respaldan el programa; la igualdad universal de
las expresiones y la covariancia se demuestran en el fragmento.

El arranque histórico global notificó una divergencia de huella del
índice `DOCUMENTOS_DE_REFERENCIA_HMT_MD.md`. No se modificó dicho
índice ni se reselló su control. El núcleo formal y la autocomprobación
de causalidad de constantes dieron PASS. Esta contribución es focal,
separada y pendiente de los controles de integración del editor;
ningún resultado local se anuncia como aprobación global del paquete.
