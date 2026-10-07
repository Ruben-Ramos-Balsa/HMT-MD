# Continuidad de la construcción de K entre los artículos I y VI

Fecha editorial: 10 de septiembre de 2026. Cotejo focal de fuentes TeX.
Esta nota distingue la construcción del registro K, sus representaciones
reversibles y la selección del libro incidencial que las precede. No constituye
una auditoría integral del corpus ni cambia el estatuto probatorio de las fuentes.

## 1. Resultado del cotejo

**Las pruebas esenciales de I que VI utiliza para reconstruir K desde sus
coordenadas transversales están presentes en VI.** Se conservan la lectura
armónica, la inversión integral de Hadamard por órbitas, el registro firmado,
las diferencias cíclicas, la carga total, el testigo ordenado, la evaluación
racional y la recuperación del registro desde esa evaluación.

Por tanto, no debe sustituirse este resultado concreto por expresiones genéricas
como «falta K», «hay que volver a construir K» o «no se sabe cómo se obtiene K».
Tampoco debe usarse su reversibilidad para afirmar que se ha ejecutado en este
artículo la selección anterior de todas las incidencias del libro. Son dos
operaciones diferentes y sus dominios permanecen explícitos.

## 2. Fuentes cotejadas

Artículo I actual solicitado por el editor:

`/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910/`

Leídos completos: `sections/registro_k.tex`, `sections/k_reversibilidad.tex`,
`sections/revision_k.tex`, `technical/procedencia_alpha.md` y
`technical/AUTONOMIA_DEPENDENCIAS_LOCALIZADAS.md`. Se contrastaron además las
referencias del recibo causal y las inclusiones del manuscrito.

Artículo V, edición integrada REV02, para la ampliación incidencial heredada:

`/Users/ruben/Documents/New project/output/ARTICULO_V_REV02_EDICION_INTEGRADA_20260910/`

Leídos completos: `manuscrito/sections/registro_incidencias.tex` y
`manuscrito/sections/registro_imagen_integral.tex`. Estos dos nombres no designan
archivos presentes dentro de la carpeta del I actual anterior. Su presencia
material se localizó en V, con antecedentes de II; no se atribuye a I una
inclusión que su `main.tex` no realiza.

Destino:

`/Users/ruben/Documents/New project/output/ARTICULO_VI_PARTICULAS_Y_MASAS_20260910_REV02/`

Las etiquetas indicadas a continuación son los localizadores estables. Las
líneas corresponden al corte posterior a las dos adiciones de esta nota.

## 3. Mapa de pruebas preservadas

| Operación o resultado | Fuente de I | Residencia en VI_REV02 |
|---|---|---|
| Calendario C108, cociente C9, extensión no escindida y avance de memoria | `registro_k.tex:34–90`, `prop:k-extension` | `sections/14_generacion_regional.tex:220–255`, `eq:extension108`, con prueba por núcleo y exponentes |
| Eventos firmados y carta 12=1+5+6 | `registro_k.tex:92–170`, `lem:k-carta-integral` | `sections/05_registro_operador_masa.tex:12–57`, `vi:prop:eventos`, con congruencias e inversa |
| Lectura armónica de los dos canales y la carga | `registro_k.tex:239–294`, `eq:k-sumas-armonicas`, `eq:k-bloques-firmados` | `sections/09_dependencias_anteriores.tex:384–411`, `vi:dep:PiH`, con demostración por órbitas |
| Hadamard en las órbitas (1,4,7,10), (2,5,8,11), (3,6,9,12) | `registro_k.tex:296–355`, `lem:k-hadamard` | `09_dependencias_anteriores.tex:364–381`, `vi:dep:hadamard`, `vi:dep:K-reversible` |
| Integralidad y unicidad de K=H12 U/4 | `registro_k.tex:357–387`, `prop:k-sello` | `09_dependencias_anteriores.tex:372–439`, mismas etiquetas y `vi:dep:K-testigo` |
| Determinación por D3, D4 y Q | `registro_k.tex:406–456`, `prop:k-transversal` | `09_dependencias_anteriores.tex:322–361`, `vi:dep:imagen-integral`: criterio necesario y suficiente e inversa explícita |
| Comprobación del testigo y de sus tres bloques firmados | `registro_k.tex:272–283,357–387,448–456` | `09_dependencias_anteriores.tex:413–439`, `vi:dep:K-testigo` |
| Evaluación periódica y recuperación de los doce bloques | `registro_k.tex:458–503`; `k_reversibilidad.tex:8–33` | `09_dependencias_anteriores.tex:441–454`, `vi:dep:alpha` |
| Rotación de la fase: κ(ρK)=1000κ(K)−K1 | `k_reversibilidad.tex:16–30`, `eq:k-rotacion-racional` | `09_dependencias_anteriores.tex:450–454` |
| Separación de la lectura finita y de la periódica | `registro_k.tex:486–520`, `eq:k-diferencia-kappas` | Apartado `vi:dep:alpha`: diferencia exacta B^-12 κ y frontera c13 conservada |

La inversión transversal de VI explicita además, para `(b,c,q)`,

`w_i=c_i−b_(i+1)`, `P_i=Σ_(j<i) w_j`, `T_w=Σ_i P_i`,

`k_i=(q+T_w)/12−P_i`.

Su prueba establece las condiciones integrales necesarias y suficientes. La
prueba de la lectura armónica muestra a continuación que
`Π_H D=H12`, de modo que ambas reconstrucciones producen el mismo registro
en el dominio declarado. No se está usando una coincidencia numérica como
sustituto de una identidad de operadores.

## 4. Ampliaciones incorporadas en este corte

### Período mínimo

Se añade `vi:dep:periodo-minimo-k`, después de la evaluación racional.
Procede de `I/sections/registro_k.tex:486–514`. Los doce componentes
distintos prueban el período mínimo de doce bloques; la agrupación de
cifras prueba el período mínimo decimal de treinta y seis. El alcance es
la prolongación racional de K, no la expansión completa de alfa.

### Conjugación incidencial y frontera

Se añaden `vi:dep:conjugacion-incidencial`, `vi:dep:conjugacion-recuentos`,
`vi:dep:conjugacion-bloque` y `vi:dep:conjugacion-frontera`, después de
la definición del bloque incidencial. Proceden de
`V/manuscrito/sections/registro_incidencias.tex:99–133`.

Las biyecciones de incidencias conservan multiplicidades, clase aritmética y
etiqueta de frontera, e intercambian los canales. Por ello transportan los
recuentos como `(A,C,V)→(A,−C,V)` en las ventanas invertidas. El cambio de
su publicación decimal se demuestra, incluidos sus cocientes. La inversión
de una ruta leída antes del avance conserva el término `f(x_n)−f(x_0)`.
Se mantiene explícita la acción concreta de la conjugación sobre el libro;
no se atribuye esta fórmula a cualquier involución sólo por su nombre.

No se añadieron el Smith global de H12, el conúcleo periódico del acarreo ni
el desarrollo excepcional de la órbita racional. Son resultados de I
identificados en el cotejo, pero no necesarios para estas dos incorporaciones.
El Smith local de H4 que VI utiliza para la escala de acción ya está en su
apartado correspondiente y no se ha eliminado.

## 5. Corte exacto entre selección del libro y reconstrucción del registro

La cadena conservada parte de APP–TRIT–TPK y del estado con memoria. Dentro
del tramo incidencial se distinguen estas operaciones:

1. **Selección del libro de una historia.** Se fija la familia concreta de
   rutas, visitas y trazas, con sus multiplicidades, etiquetas, extremos,
   longitudes y transportes. No basta conocer el formato del libro para
   individualizar esa familia.
2. **Evaluación del libro seleccionado.** VI define el dominio, calcula los
   recuentos `(A_m,C_m,V_m)`, conserva sus divisiones euclídeas, publica los
   bloques `z_m` y obtiene `(D3z,D4z,Q(z))`. Incluye las reglas de actualización
   y la partición de las trazas que cruzan una concatenación.
3. **Reconstrucción integral.** Desde los canales compatibles y la carga,
   VI demuestra la inversa, la lectura armónica y `K=H12 U/4`.
4. **Publicaciones posteriores.** Se evalúa κ, se recupera K desde ella y se
   compone el registro con las coordenadas regionales para la normalización
   posicional de alfa.

Los puntos 2–4 tienen sus fórmulas y pruebas reunidas en VI. El cotejo no ha
localizado dentro de I una regla adicional que, trasladada sin más a VI,
individualice la familia completa del punto 1 y produzca de principio a fin
las veinticinco coordenadas del testigo. El propio
`I/technical/procedencia_alpha.md`, apartado 3, delimita la transcripción de
la acción de E108 sobre las incidencias efectivas antes de la reconstrucción.
El párrafo `I/sections/registro_k.tex:232–237` mantiene ese mismo corte.

Esta constatación está acotada a los propietarios examinados; no declara
ausencia universal en HMT. Tampoco reclasifica las coordenadas del corpus
como entradas metrológicas. La inversión exacta no se niega ni se presenta
como un productor de los argumentos que recibe. La condición editorial que
debe conservarse es precisa: **construcción reversible de K reunida;
individualización prospectiva del libro terminal no reproducida por esta
reunión de pruebas**.

## 6. Controles y continuidad

La sección 09 sólo recibe los dos bloques aditivos descritos. Los recibos
`CONTROL_PERIODO_CONJUGACION_K_VI_REV02.json` y
`CONTROL_PERIODO_CONJUGACION_K_VI_REV02_OPT.json` documentan controles exactos
ejecutados sobre el testigo y las identidades focales; no declaran una
ejecución del selector del libro.

La procedencia detallada de los añadidos reside en
`technical/PROCEDENCIA_PERIODO_CONJUGACION_K_VI_REV02.md`. Se utilizan las
skills de continuidad HMT, núcleo formal y constantes generadas para conservar
el orden causal, el contenido probado y la distinción entre los dominios.
