# Formalización Lean finita — Artículo VI

Proyecto reproducible con Lean `4.21.0`. Integra, como dependencias explícitas,
los microcertificados compartidos `HMT/Atlas.lean`, `HMT/Dodecaphase.lean` y
`HMTMD/HMTMD.lean`, y añade en `ArticleVI.lean` comprobaciones finitas que
corresponden a enunciados concretos del Artículo VI.

Las tres dependencias compartidas se integran sin modificación desde
`PUBLICACION_HMT/PAQUETE_PROBATORIO_COMUN_AUTONOMO_HMT_MD_20260903/evidencia/lean/`;
su identidad byte a byte se comprueba por SHA-256 antes de esta entrega.

## Matriz exacta de cobertura

| Teorema Lean | Enunciado comprobado | Fuente del Artículo VI |
|---|---|---|
| `ArticleVI.route_family_class_count` | `41+10+2+1+2=56` | `sections/04_atlas_familias.tex:115-124` |
| `ArticleVI.route_family_cell_coverage` | `41+20+6+4+10=81` | `sections/04_atlas_familias.tex:120-128` |
| `ArticleVI.oriented_atlas_count` | `81·4=324` orientaciones | `sections/04_atlas_familias.tex:168-175` |
| `ArticleVI.seed_pair_count` | `324²=104976` pares ordenados de cursores | `sections/14_generacion_regional.tex:14-23` |
| `ArticleVI.additive_signature_multiplicity` | `18·18=324` | `sections/14_generacion_regional.tex:110-116` |
| `ArticleVI.multiplicative_signature_multiplicity` | `24·8+24+108=324` | `sections/14_generacion_regional.tex:113-117` |
| `ArticleVI.emission_weight_total` | `432·144+18·432+18·1944=104976` | `sections/14_generacion_regional.tex:117-122` |
| `ArticleVI.electron_displacement_reader` | evaluación electrónica de `K_D=(80,54,6)` | `sections/05_registro_operador_masa.tex:193-210` |
| `ArticleVI.electron_reader_coincidence` | coincidencia finita `K_D=K_Ω=(80,54,6)` para la ruta electrónica | `sections/05_registro_operador_masa.tex:195-220` |
| `ArticleVI.shared_incidence_pair` | composición de incidencias `90+120=210` | `HMTMD/HMTMD.lean`, teorema compartido importado |

`HMT/Atlas.lean` certifica el atlas cuadrático nonádico compartido; no se lo
identifica con el censo de partículas `81/56/13/324`. `HMT/Dodecaphase.lean`
certifica identidades finitas dodecafásicas. `HMTMD/HMTMD.lean` certifica las
incidencias `90/120` y otros microresultados compartidos. La matriz anterior
delimita qué afirmaciones adicionales pertenecen realmente a este proyecto.

## Dependencias y orden de construcción

No hay dependencias de terceros: Lean core y `Std` incluidos en la distribución.
Lake resuelve los módulos en este orden:

1. `HMT/Atlas.lean`, `HMT/Dodecaphase.lean`, `HMTMD/HMTMD.lean`;
2. `ArticleVI.lean`;
3. `lake build` desde este directorio.

El `#print axioms` del módulo raíz deja visible la base axiomática de una muestra.
Este proyecto es una formalización parcial y finita; no declara formalizado el
Artículo VI completo ni la Ley General de Masas completa.
