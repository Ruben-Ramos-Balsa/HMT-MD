# Residencias demostrativas del núcleo incorporado

## Resultado material de esta intervención

Se ha añadido `manuscrito/sections/11_nucleo_finito.tex`. El apéndice no es un índice de referencias: contiene el dominio de 104976 parejas de condiciones iniciales, el selector, la regla de desplazamiento y lectura, las inversiones de orientación, el lector discreto, la emisión decimal, las 18+26 firmas, las multiplicidades y el censo ternario. Demuestra la inyectividad de la emisión y la exhaustividad finita. En un apartado distinto reproduce las cuatro matrices de transiciones y prueba la reconstrucción única de L0/L1, la selección entre los 16 calendarios y la incompatibilidad de las 144 modificaciones unitarias.

El certificado `verificar_nucleo_finito.py` produce el censo desde esas reglas antes de compararlo con el catálogo. La segunda parte extrae las matrices del propietario literal 06e, calcula las inversas y enumera los calendarios y perturbaciones. No recibe cifras reales ni metrología. Esta intervención constituye un **CERTIFICADO_NUEVO** y una **FORMALIZACION_REUNIDA** de resultados finitos preexistentes; no una nueva generación histórica de las constantes.

## Propietarios concretos y dependencias que no se sustituyen

### Emisión finita y proyección ternaria

La regla está en el artículo I, `sections/extension.tex:8–76`, y coincide con la función `channel_signature` del propietario `verificar_dinamica_cociente_468.py:73–94` y su selector/lectores anteriores. El apéndice hace pública esa regla completa y sus clases. La tabla `TPK_U_catalog_468.json` y el catálogo de rutas se preservan para comparación posterior. La uniformización de continuaciones y las evaluaciones reales que aparecen más adelante en aquel programa no son parte del productor finito ejecutado aquí.

### Levantamientos L0/L1

El propietario `06e_certificado_generacion_monodromica_rev7.tex:45–154` contiene las matrices X0,Y0,X1,Y1, la reconstrucción y las sucesiones. El artículo I `sections/generacion.tex:46–82` había remitido el examen de los calendarios al suplemento. El nuevo apéndice incorpora ese examen y su prueba.

Permanece una distinción imprescindible: la operación `L=X^{-1}Y` recibe las transiciones. La composición nominal de Sel/Tra/Upd está escrita en 06e:58–64; ese pasaje no despliega su acción coordenada anterior que produzca las cuatro matrices sin recibirlas. El programa histórico `certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py:6–7,68–86,544–567` declara las matrices como primitivas y las aplica. No debe presentarse el nuevo censo de calendarios como si hubiese reconstruido una operación anterior no ejecutada en él.

El propietario U008, `manuscrito/ampliaciones_sucesoras_20260824/parte_i_ii/owners/U008_orbitas_elevacion_r36.tex:381–407`, sí proporciona la elevación exacta con residuos y cocientes:

\[
y_k=x_kA,\quad u_k=y_k\bmod3,\quad x_{k+1}=(y_k-u_k)/3,
\quad x_k=(u_k+3x_{k+1})A^{-1}.
\]

Es una operación de transporte con un levantamiento A ya fijado. Puede incorporarse con su prueba cuando se desarrolla la memoria; no debe usarse para sustituir la procedencia de A. La fuente íntegra se preserva en este paquete.

### Selección terminal y extracción de K

U016 está preservado íntegro. Sus líneas 167–243 fijan los catálogos terminales 196/197/196, anuncian la reducción 7567952→331→2 y exponen las dos matrices finales y la selección axial. Un apéndice de esa enumeración debe incluir los tres catálogos o su productor, los predicados de Gram/norma/peso/distancia y la procedencia del margen q∂. Copiar solamente los cardinales y las dos matrices no reproduce la enumeración anterior.

U016:256–298 sitúa el extractor E108^{90,120} sobre el registro de incidencias y presenta sus 25 coordenadas; U016:298–326 desarrolla explícitamente la operación posterior Pi_H que produce el registro firmado. El artículo I preserva esa separación en `registro_k.tex:211–237`. Para una clausura pública del tramo anterior se requiere una especificación evaluable de la acción del extractor sobre los generadores efectivos del registro. Las identidades D3K y D4K permiten verificar las coordenadas desde K, pero no deben convertirse en su productor inverso. La nota del artículo I `technical/APENDICE_REGLAS_PROCEDENCIA.md` documenta la búsqueda focal previa y su alcance exacto.

Esta intervención no repite una investigación de todo el corpus ni declara inexistente el resultado: conserva los propietarios completos y delimita lo que contiene la reproducción suministrada.

### Prolongación de alfa

El capítulo de alfa incorporado conserva su distinción entre truncamiento de orden nueve y compatibilidad a toda profundidad. La sección `memoria_resolvente.tex` añade los teoremas sobre memoria, series y compresiones que efectivamente demuestra. El presente certificado finito no construye desde ellos una equivalencia global adicional entre las dos vías. Las dependencias que el propio artículo I localiza en `technical/AUTONOMIA_DEPENDENCIAS_LOCALIZADAS.md:68–91` mantienen su alcance en la copia, salvo una incorporación ulterior explícita por parte del responsable del artículo.

## Consecuencia editorial

El apéndice añadido permite leer y reproducir dentro del artículo las pruebas del censo finito, la inversión matricial, los calendarios y las perturbaciones. No elimina por afirmación las dependencias anteriores de los registros ni sustituye una demostración infinitaria por un control finito. Los originales I y II permanecen íntegros; la entrega técnica no modifica los capítulos importados ni sus advertencias de alcance.
