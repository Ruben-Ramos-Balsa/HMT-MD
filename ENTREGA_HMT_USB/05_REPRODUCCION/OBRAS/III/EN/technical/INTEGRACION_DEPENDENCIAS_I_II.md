# Integración literal de las dependencias de los artículos I y II

## Alcance y estado

Se ha construido una copia documental de trabajo dentro del artículo III, sin
modificar los artículos I y II y sin compilar. Los controles realizados acreditan
identidad binaria de las copias, clausura de los `input` literales seleccionados y
resolución estática de sus referencias. No constituyen un certificado de autonomía
matemática global ni una aprobación de publicación.

Fuentes:

- I: `ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909`, 117 páginas.
- II: `ARTICULO_II_AUTONOMIA_20260909_REVISION_05_TRABAJO`, 182 páginas, identificado
  por `gestion/ESTADO_REVISION.json` y no por la fecha de modificación. Su estado
  preservado es `BORRADOR_COMPILADO_REVISION_FOCAL` y declara
  `mathematical_closure_certified: false`.

La revisión 06 existente no se ha promovido sobre la revisión 05 seleccionada para
esta tarea. El manifiesto anterior del núcleo I permanece intacto.

## Artículo I: adición excepcional

Los 28 TeX del núcleo común previamente copiados se completan con nueve archivos:

```text
sections/excepcional.tex
sections/revision_incidencia_argumento.tex
sections/incidencia_registro.tex
sections/incidencia_normalizacion.tex
sections/incidencia_bandera.tex
sections/estrella_pentadica_recuperada.tex
figures/estrella_cinco_regiones.tex
sections/incidencia_reticulo.tex
sections/incidencia_automorfismos.tex
```

El conjunto tiene 37 TeX activos y una bibliografía copiada íntegramente. Resuelve
`exc:doble-lectura` e `inc-ampl-cuaterna` conservando sus definiciones, mapas y
pruebas. No se incorpora el archivo histórico `incidencia_articulacion.tex`, que
duplicaría la segunda etiqueta.

Manifiestos separados:

- `base_articulo_I/MANIFIESTO_COPIA_NUCLEO.json`: permanece inalterado.
- `base_articulo_I/MANIFIESTO_ADICION_EXCEPCIONAL.json`: nueve copias adicionales.

## Artículo II: selección demostrativa

La clausura literal de los puntos de entrada seleccionados tiene 13 TeX:

```text
sections/03_actualizacion.tex
  sections/03b_memoria_resolvente.tex
  sections/ii_sello_y_lectura.tex
sections/04_determinantes.tex
sections/05_accion.tex
  sections/revision_planck.tex
sections/05b_coordenadas_angulares.tex
sections/06_barbero.tex
sections/06b_significado_incidencia.tex
sections/07_elipse.tex
sections/07b_geometria_elipse.tex
  figures/elipse_accion_II.tex
sections/revision_planck_contraste.tex
```

La comparación de Planck se conserva porque `revision_planck.tex` la reclama
expresamente. No se sustituyen sus diferencias cuantitativas por una declaración
de igualdad exacta.

Se añade como residencia pública el propietario
`propietarios/c43_precedencia_dodecafasica_20260905.tex`, copiado íntegramente del
propietario B01 conservado por II. Define la incidencia activa, la cadena de doce
sectores y una frontera orientada, el lector lineal y la prueba del coeficiente de
polo. La ponderación `12:-1` no queda apoyada únicamente en una autorreferencia.

Son por tanto **14 TeX activos**, más seis archivos de procedencia. No se copian
los capítulos de CKM/PMNS, gravedad, Boltzmann, área, dualidad T, introducción,
resumen ni conclusiones de II. No se afirma que éstos sean innecesarios para
cualquier artículo: quedan fuera de esta selección concreta de acción, par
angular, canales, Barbero y elipse.

## Uso de las envolturas

Desde un `main.tex` compilado con directorio de trabajo en la raíz del artículo III:

```tex
\input{base_articulo_I/INCLUIR_NUCLEO_Y_EXCEPCIONAL_I.tex}
\input{base_articulo_II/INCLUIR_DEPENDENCIAS_II.tex}
```

Las envolturas ajustan `\input@path` dentro de grupos. Los `input` anidados de las
copias siguen siendo literalmente `sections/...` y `figures/...`; no se modifican
los archivos para relocalizarlos. Si el editor cambia el directorio de compilación,
debe ajustar el punto de entrada, no las fuentes copiadas.

La envoltura I presupone el preámbulo del artículo I (paquetes, STIX Two, macros
matemáticas y entornos de teoremas). La de II añade localmente las macros `HMT`,
`Tr`, `dd`, `R`, `Z`, los colores de sus figuras y el entorno `apunte` cuando no
existe. No modifica el título ni los autores del artículo III.

I y II reproducen once etiquetas `mem:*`. Para conservar ambos textos sin
redefiniciones ambiguas, la envoltura II antepone `hmtII:` exclusivamente a sus
etiquetas técnicas. Las referencias que apuntan a una etiqueta definida en II se
transportan a ese espacio; las dirigidas al núcleo I mantienen el rótulo original.
Las formas ordinaria y estrellada de `\ref` se conservan. Desde fuera de la
envoltura, una referencia al bloque II se escribe, por ejemplo,
`\eqref{hmtII:eq:ii-canales}`. La numeración impresa de secciones y ecuaciones
sigue la del documento ensamblado: no se alteran fórmulas, títulos ni enunciados.

## Bibliografía

Las siete claves del núcleo I están en su bibliografía íntegra. Excepcional añade
`conwaysloane`, `flm` y `borcherds`, también presentes allí.

II requiere `bipm2018`, `codata2022` y `hmtedicionintegral`, que ya existen en I, y
las tres claves `registro`, `precedencia`, `elipse`. Estas últimas se recuperan
literalmente de la bibliografía predecesora preservada por II en:

```text
base_articulo_II/BIBITEMS_ADICIONALES_II.tex
```

Ese archivo se inserta **dentro del único entorno `thebibliography` final**. No se
deben cargar dos bibliografías completas con claves duplicadas. La biblioteca
predecesora completa se conserva sólo como procedencia; el ensamblador puede
extraer mecánicamente las entradas pertinentes manteniendo una traza explícita.

`procedencia/referencias_internas_NO_ACTIVAR.tex` documenta el remapeo original de
II, pero no se carga: transforma, entre otras, la cita `precedencia` en una
remisión al propio capítulo y ecuación de Barbero. Esa remisión resuelve un rótulo,
pero no sustituye al propietario B01 que ahora sí se incorpora.

## Dependencias semánticas que el editor debe conservar

1. **Bohr utiliza la masa electrónica.** `07b_geometria_elipse.tex:173–205`
   presenta una composición con `hbar,m_e,c,alpha` positivos en una misma carta.
   La construcción de `m_e` no pertenece a los cinco capítulos comunes y al
   excepcional aquí copiados. Si III afirma también su generación autónoma, debe
   recuperar la sección electrónica de I con su cierre. El lector del vacío que
   produce `c` corresponde al desarrollo propio de III. No se declara suplida
   ninguna de esas construcciones por esta copia.
   **Decisión de alcance del editor:** la generación de la escala de Bohr no se
   anuncia como objetivo propio de III. Se conserva literalmente la proposición
   de II como composición con sus magnitudes declaradas; no se incorpora la
   sección electrónica completa para ampliar ese objetivo. La fuente preservada
   no debe presentarse como una nueva derivación independiente de Bohr en III.
2. **Carácter H5 y renovación.** `05_accion.tex:101–118` y
   `revision_planck.tex:13–86` conservan los coeficientes, su procedencia, la
   asignación a grados y la normalización inicial de la continuación. El
   propietario A03, conservado en `procedencia/c35_componente_adimensional_retorno.tex`,
   contiene esta misma regla. No debe deducirse la asignación a los grados sólo
   a partir de la lista de cardinales.
3. **Selector regional 169.** Aparece como cuarta componente de las regiones de
   pi en I, `sections/generacion.tex:33–36`. A03:30–35 y la regla de renovación
   explicitan su empleo como impulso de grado seis. Se conserva ese mapa declarado;
   la mera coincidencia del número no constituye una selección distinta.
4. **Ángulos y canales.** `05b_coordenadas_angulares.tex` define el mapa de
   publicación, sus unidades y el paso a `q_+` y `q_-`, con prueba de recuperación.
   Recibe las coordenadas HMT ya construidas; no recibe `h` en unidades SI para
   seleccionar un ángulo.
5. **Representación de la elipse y vacío.** `07b_geometria_elipse.tex:207–263`
   demuestra la realización LC con reloj y transductor declarados. Su identificación
   con el lector constitutivo del vacío exige el mapa que III está desarrollando;
   no se identifica con él porque ambos usen el antecedente angular.
6. **Alcance de alfa y del productor firmado.** Los límites y obligaciones
   expresados en I `alpha_dependencias.tex` y en el estado preservado de II no han
   sido cambiados por la copia. No se declara igualdad exacta de dos vías o autonomía
   global a partir del cierre de referencias.

Estos puntos no son declaraciones de ausencia en el corpus. Delimitan lo que
transmiten los propietarios consultados y la integración que debe acompañar a
los resultados concretos anunciados por III.

## Reproducción y verificaciones efectuadas

```text
python3 -I -S technical/copiar_dependencias_I_II.py
```

El script rechaza destinos divergentes, conserva el manifiesto anterior, copia
bytes originales, registra SHA256 fuente/destino, identifica referencias y produce
envolturas documentadas. La ejecución no altera los textos de procedencia ni
añade valores numéricos generadores. El recibo es:

`technical/RECIBO_COPIAS_DEPENDENCIAS_I_II.json`.

No se ejecutó LuaLaTeX. El control visual, la cobertura de los desarrollos propios
de III y la autonomía del artículo completo corresponden al ensamblado posterior.
