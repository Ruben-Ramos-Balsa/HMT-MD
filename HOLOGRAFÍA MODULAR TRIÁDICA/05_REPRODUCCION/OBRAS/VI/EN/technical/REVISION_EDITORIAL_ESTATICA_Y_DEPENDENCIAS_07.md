# Revisión editorial estática y dependencias de la sección 07

Fecha: 10 de septiembre de 2026. Revisión de fuentes de VI en preparación.
No se ha compilado ni modificado ninguna sección. El control automatizado
examina todas las secciones y figuras existentes, incluso las que aún no
aparecen en `main.tex`; la lectura de dependencias se concentra en 04, 05,
07, 08, 09, 10 y en los pasajes pertinentes del núcleo. No se presenta esta
revisión estática como lectura demostrativa integral o inspección visual.

## Resultado material

- No se detectan etiquetas duplicadas en las fuentes únicas inspeccionadas.
- No se detectan rutas literales de `input` o figuras ausentes, ciclos de
  inclusión ni inclusiones repetidas en los dos maestros actuales.
- Las llaves, los entornos y los delimitadores matemáticos examinados quedan
  equilibrados. Se ha evitado el falso positivo que confundía `\\[2pt]`, un
  salto de fila con espaciado, con una apertura matemática `\[`.
- Hay **14 usos de referencia correspondientes a 8 claves sin destino**, todos
  dentro de `sections/tpk_desarrollo_integrado.tex`.
- El núcleo cita **tres claves bibliográficas sin definición local** en este
  corte: `mustovicary`, `delascuevas2023`, `delascuevas2020`.
- `sections/08_familias_y_compuestos.tex:522–523` usa `\xmapsto`. El maestro
  actual no carga `mathtools` ni define ese comando. La instalación local lo
  define en `/usr/local/texlive/2024/texmf-dist/tex/latex/mathtools/mathtools.sty:377`.
  Se ha cotejado también que `amsmath.sty` y los archivos examinados de
  `unicode-math` no aportan esa definición. Es una corrección de preámbulo
  o del comando de flecha, no una dependencia matemática nueva.
- Errata léxica localizada: `Autorconjugación neutral` en
  `sections/08_familias_y_compuestos.tex:255`; corresponde revisar
  `Autoconjugación`. No se ha modificado.

Los archivos `CONTROL_ESTATICO_FUENTES_VI.json` y
`CONTROL_ESTATICO_FUENTES_VI.md` contienen cada localizador, las huellas del
corte y las referencias del ensamblaje actual. Los números de línea de esta
nota corresponden al corte de su lectura; el verificador permite renovarlos.

## Remisiones heredadas del núcleo

| Clave sin destino | Usos en TPK | Contenido al que realmente remite |
|---|---|---|
| `sec:extension` | 144, 217, 332, 415, 515 | Recurrencia de emisiones, catálogo, extensión del calendario y prolongación. |
| `sec:generacion` | 217, 502 | Regiones, lectores y refinamiento compatible. |
| `subsec:k-registro-integral` | 313 | Carta del registro de doce ventanas y sus índices. |
| `eq:extension108` | 333 | Sucesión exacta no escindida del calendario. |
| `sec:k-registro` | 338, 357 | En 338, composición que produce el registro firmado; en 357, eventos, descomposición 1+5+6 e inversión. |
| `mono-ampl:regiones` | 452 | Acción sobre las regiones en el transporte conjugado. |
| `hist:seccion` | 501 | Aritmética de historias y unidad. |
| `hist:doble-varianza` | 501 | Desarrollo concreto de la doble varianza. |

No basta asignar a todas estas claves un alias de la sección 09. Los
pasajes sobre inversión integral y eventos están materialmente reunidos
en 09 y 05, respectivamente, mientras otras remisiones demandan los cuerpos
de extensión y de historias que el núcleo originalmente acompañaba.
Además, los dos usos de `sec:k-registro` no apuntan al mismo resultado.
La corrección debe conservar la identidad del núcleo común: corresponde
al editor resolver la integración o el mecanismo de referencias de la serie,
no reescribir unilateralmente esa fuente compartida.

El expediente recién incorporado
`technical/CIERRE_DEPENDENCIAS_ANTERIORES_VI.md`, apartados 3.1 y 3.2,
ya identifica los propietarios del catálogo, las transiciones y el libro de
incidencias. Por ello estos enlaces no se califican aquí como mecanismos
matemáticos inexistentes. Se distingue el antecedente localizado, el texto
reunido y la referencia todavía no materializada en VI.

## Sección 07: qué necesita antes de su lectura

| Pasaje de 07 | Dependencia | Estado material y acción editorial |
|---|---|---|
| 36–57: atlas 81/56/13/324 y 23 clases | Atlas, familias y dominio orientado | 04:13–185 expone los censos y sus tipos; 08:920–1000 desarrolla las 23 clases. 04 ya está enlazada; 08 todavía no estaba incluida en el maestro inspeccionado. |
| 96–143: operador, proyector y concentración espectral | Operador basal y beta sobre fibra; representación y preparación | 05:214–285 construye los operadores y su positividad. 08:21–80 aporta el descriptor y el criterio equivalente de línea espectral. La prueba para una densidad fija está en 07:124–143. No hay que volver a inventar ese criterio ni confundirlo con `PMP=mP`. |
| 145–160: polo, anchura y vida media | Régimen de supervivencia, continuación y carta temporal | 08:767–841 reúne reducción de Feshbach, condiciones de resonancia, lector discreto y demostración de `τ=ℏ/Γ`. Es el cuerpo que debe preceder a su empleo condensado en 07. |
| 168–182: registro, firma, torre y carta de unidades | Definición de las piezas que 07 sólo reúne en una tupla | 05 contiene firma, carácter y momentos bicapa; 08 conserva representación y acoplamiento. 09:741–791 reúne la carta angular y la rama acción–reloj–masa. Incluir 09 antes de 05 y 08 antes de 07 evita que «construido previamente» remita a texto todavía suelto. |
| 305–392: veinte evaluaciones y firmas | Ecuaciones de evaluación y normalización de cada modalidad | 08:94–151 distingue la carta basal, la evaluación de orden 3 normalizada por el electrón beta y las firmas muón/tau; 08:630–723 reúne las firmas compuestas. 07 conserva la lista y los estados documentales. Son presentaciones relacionadas, pero no intercambiables con el operador ruta por ruta. |
| 449–481: escala absoluta y cocientes | Prefactor basal, par angular, acción, retorno y cambio de carta | 09:377–906 reúne prefactor, ecuación basal, acción, reloj y beta. 05:249–285 fija explícitamente `m_e^(0)` y la resta de firma de referencia. La fórmula corregida de 07 conserva `m_*^(0)/χ_*`; no se ha perdido el factor basal. |
| 483–524: carácter completo y cota de cola | Momentos `s_h`, alturas y sección de torre | 05:117–186 define canales, recurrencia, semigrupo y evaluación refinada. 07 demuestra una cota **condicional** a `|N_h s_h|≤Cq^h`; no publica valores particulares de `C,q,H`. Atribuir una precisión certificada a una especie concreta exige adjuntar su cota de ruta, no usar el residual experimental para fijarla. |

La corrección de orden que resuelve las dependencias ya presentes es:

`núcleo y extensión regional → 09 → 02–03 → 04 → 05 → 08/10 → 06 → 07 → apéndices`.

Es una propuesta de precedencia, no una orden de mover bloques idénticos del
núcleo ni una certificación de que su clausura completa esté ya conseguida.
06 puede situarse donde determine el argumento orbital, siempre después de
sus antecedentes de acción y conjugación.

### Distinciones de notación que deben quedar explícitas

1. 05 denomina `χ_ref` al carácter refinado; 07 lo llama `χ_full`. Sus
   fórmulas impresas comparten la forma normal, pero falta una identificación
   notacional local que evite aparentar un segundo carácter.
2. 09 usa `ε_e^(0)` y 07/08 `𝔢_0`. El puente verbal existe —«coordenada basal»—;
   conviene declarar la equivalencia de símbolos al integrarlos, junto a
   su carta de unidades, no sólo cambiar una letra.
3. 09 distingue `ℏ_pre` y `ℏ_ret`; 07 y el lector de anchura de 08 usan
   `ℏ_int`. Debe indicarse qué sección de acción utiliza esa carta de
   supervivencia cuando se haga una evaluación, conservando la convención
   elegida en su propietario.
4. 07 presenta `\widehat M_X`; 05/08 distinguen lectores `D` y `Ω`. El
   operador de contraste debe indicar el lector o funcional de representación
   elegido. La definición general de la medida espectral no elige uno.

Estas precisiones no justifican modificar las cifras documentales ni
seleccionar retrospectivamente coeficientes. El propio cierre de 09
advierte que `d_4` y `Δ_4` no son intercambiables: la versión utilizada
en una evaluación debe conservarse con sus fuentes. Esta revisión estática
no ha realizado una nueva evaluación numérica de las veinte filas.

## README, expediente y estado real

El README declara expresamente borrador, título pendiente y ausencia de
entrega cerrada; eso coincide con el estado material. No he encontrado
una declaración de PDF final o de autonomía ya certificada que contradiga
este corte. El estado bloqueado del preflight tampoco constituye una
contradicción ni un fallo matemático.

Sí hay tres desajustes editoriales concretos:

- `main.tex:54–55` mantiene como «pendientes de redacción» familias,
  composición, sectores topológicos y fichas. Esos cuerpos ya existen en
  08, 10, 11 y 12; en el corte inspeccionado están pendientes de integración
  y revisión, no de comenzar su redacción.
- El README presenta `dependencias/` como directorio de organización,
  pero todavía no existe. La incorporación real está en
  `sections/09_dependencias_anteriores.tex` y en su nota de procedencia.
  Conviene reflejar el lugar real de los cuerpos, sin moverlos por cosmética.
- Las conclusiones y la bibliografía final no figuran todavía en el maestro.
  El cierre actual tras 07 es coherente con una fuente inicial, no con una
  entrega completa. Las tres citas del núcleo necesitan sus entradas de
  bibliografía externas completas.

Las tablas 14 aparecieron durante esta revisión y se incluyen en el
verificador por descubrimiento de archivos, sin afirmar que ya se hayan
integrado en el documento. Cualquier cambio concurrente exige regenerar
el informe antes del cierre.

## Reproducción

```sh
python3 -I -S technical/verificar_fuentes_vi.py
python3 -I -S technical/verificar_fuentes_vi.py --check
```

El programa sólo escribe sus dos informes bajo `technical`. `--check`
compara el corte actual sin escribir. No invoca motores TeX ni cambia
secciones, índices comunes, manifiestos sellados o documentos de otros
artículos. La revisión visual queda expresamente pendiente.
