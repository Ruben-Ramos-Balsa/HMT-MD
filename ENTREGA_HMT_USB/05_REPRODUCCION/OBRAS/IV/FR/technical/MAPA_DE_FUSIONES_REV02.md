# Integración editorial de IV, revisión 02

Autorización: Rubén pidió aplicar la crítica completa, coordinar I–V y terminar
las sucesoras. Se conserva el alcance de los resultados; no se atribuye al autor
una revisión de las huellas nuevas ni una aprobación científica sobrevenida.

## Incorporación II → IV

Procedencia: artículo II REV10, 206 páginas. Las pruebas de acción, renovación,
publicación angular, elipse y radio se reúnen en tres cuerpos autónomos:

- `sections/iv_accion_antecedente.tex`: `05_accion.tex` y los antecedentes
  pertinentes de `revision_planck.tex`, con asignación de coeficientes y
  normalización de renovación conservadas.
- `sections/iv_angulos_antecedente.tex`: publicación del par angular, cartas,
  memoria e inversión de canales de `05b_coordenadas_angulares.tex`.
- `sections/iv_elipse_radio.tex`: elipse orientada, transportes, ley areal,
  radio y matriz; propietarios `07_elipse.tex`, `07b_geometria_elipse.tex` y
  `12_dualidad_t.tex`.

La clausura utilizada excluye los desarrollos posteriores de Barbero, CKM,
masas y contraste metrológico: ninguno selecciona el radio adimensional.
Se conserva la distinción entre forma y escala, así como la escala de cuerda
α′ declarada en la realización. Estatuto: resultado recuperado y composición
editorial explícita. Las cotas y especializaciones se prueban dentro del texto.

`02_dualidad_t.tex` mantiene los teoremas generales y añade su especialización
a las dos fibras {R*,1/R*}, con dominios operatorios y de formas. El morfismo
de `03_pantallas_coordinadas.tex` se restringe a esa familia estable.

## Pruebas duplicadas reunidas

La versión anterior de `pantallas_dualidad.tex` queda conservada en
`technical/antecedente_revision_01/sections/`. Su residencia pública se transforma
en un enlace expositivo. Cada contenido matemático tiene estas residencias:

| Contenido anterior | Residencia de prueba conservada | Etiqueta anterior y destino |
|---|---|---|
| Involución y forma cuadrática | `02_dualidad_t.tex`, `iv:thm:dualidad-escalar` | `eq:dualidad-normalizada-k` en la definición de energía |
| Conjugación unitaria | `02_dualidad_t.tex`, `iv:thm:t-unitaria`; incluye dominios completos | `prop:dualidad-radios-k` |
| Cambio de sección, memoria, ejemplo n=9 | `02_dualidad_t.tex`, subsección de cambio de representante | `eq:dualidad-cociente-k` |
| Mínimo coercivo y transporte L9 → SL9 | `02_dualidad_t.tex`, `iv:thm:dualidad-cociente`, con los dos candidatos enteros | misma sección |
| Plano hiperbólico y cociente reticular | `03_pantallas_coordinadas.tex`, `iv:eq:26-24`, prueba explícita por coordenadas | sin pérdida de coordenadas |
| Mapa conjunto, inversa, grafo y entrelazamiento | `03_pantallas_coordinadas.tex`, `iv:thm:pantallas-isomorfas` | `eq:k-mapa-pantallas`, `thm:k-pantallas-coordinadas` |
| Reducción ortogonal repetida en III bloque de IV | prueba `prop:k-reduccion-diez` en `k_direccion_dimensional.tex`; consecuencia y descomposiciones en `iv:prop:12-11-10` | ambas etiquetas conservadas |

Se usa una sola denominación, R_M^alg, para el mismo mapa. Se conserva el grafo
que retiene V11; no se introduce una equivalencia V11 ≅ V10. La covariancia
ortogonal permanece explícita. Las condiciones de campos y supercarga no cambian.

Precisión técnica tras la primera pasada: amsmath admite una sola etiqueta por
ecuación. Se retiraron exclusivamente los aliases `eq:dualidad-normalizada-k`,
`eq:dualidad-cociente-k` y `eq:k-mapa-pantallas`, que no tienen remisiones
activas. Sus destinos conservados son, respectivamente, `iv:eq:energia-t`,
`iv:eq:energia-cociente` y `iv:eq:rm-alg`. Los aliases de teorema se mantienen.
No se cambió ninguna ecuación, hipótesis ni prueba. Las menciones de esas tres
etiquetas en la tabla identifican su procedencia, no tres etiquetas TeX activas.

## Bibliografía y presentación

- Las claves duplicadas `hmtedicionintegral` y `hmtedicionsintesis` se reúnen,
  respectivamente, con `hmtintegral` y `hmtsintesis`; las citas se actualizan.
  Los nucleares de 97 y 144 páginas permanecen distintos.
- Chen–Lam–Shimakura, arXiv:1606.05961v2, teorema 1.1; Abe–Lam–Yamada,
  arXiv:1705.09022v4, teorema 4.4 y §§2–4: localizadores trasladados al texto
  y contrastados con las fuentes primarias el 10 de septiembre de 2026.
- Resumen, introducción y conclusiones incluyen el enlace elíptico. Título,
  autoría, procedencia editorial y alcance de supercarga se conservan.

Los controles de conservación, de álgebra finita, de referencias, de compilación
y de maquetación tienen alcances distintos; ninguno se presenta como verificación
global de todas las afirmaciones de HMT o de una equivalencia física universal.
