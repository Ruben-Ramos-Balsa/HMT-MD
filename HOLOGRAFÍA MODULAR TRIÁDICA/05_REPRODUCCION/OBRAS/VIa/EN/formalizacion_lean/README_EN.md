# Finite Lean formalization — Article VI

Reproducible project using Lean `4.21.0`. It integrates the shared
microcertificates `HMT/Atlas.lean`, `HMT/Dodecaphase.lean` and
`HMTMD/HMTMD.lean` as explicit dependencies, and adds finite checks in
`ArticleVI.lean` corresponding to specific statements of Article VI.

The three shared dependencies are incorporated without modification from
`PUBLICACION_HMT/PAQUETE_PROBATORIO_COMUN_AUTONOMO_HMT_MD_20260903/evidencia/lean/`;
their byte-for-byte identity is checked by SHA-256 before this delivery.

## Exact coverage matrix

| Lean theorem | Checked statement | Article VI source |
|---|---|---|
| `ArticleVI.route_family_class_count` | `41+10+2+1+2=56` | `sections/04_atlas_familias.tex:115-124` |
| `ArticleVI.route_family_cell_coverage` | `41+20+6+4+10=81` | `sections/04_atlas_familias.tex:120-128` |
| `ArticleVI.oriented_atlas_count` | `81·4=324` orientations | `sections/04_atlas_familias.tex:168-175` |
| `ArticleVI.seed_pair_count` | `324²=104976` ordered cursor pairs | `sections/14_generacion_regional.tex:14-23` |
| `ArticleVI.additive_signature_multiplicity` | `18·18=324` | `sections/14_generacion_regional.tex:110-116` |
| `ArticleVI.multiplicative_signature_multiplicity` | `24·8+24+108=324` | `sections/14_generacion_regional.tex:113-117` |
| `ArticleVI.emission_weight_total` | `432·144+18·432+18·1944=104976` | `sections/14_generacion_regional.tex:117-122` |
| `ArticleVI.electron_displacement_reader` | electronic evaluation of `K_D=(80,54,6)` | `sections/05_registro_operador_masa.tex:193-210` |
| `ArticleVI.electron_reader_coincidence` | finite equality `K_D=K_Ω=(80,54,6)` for the electronic route | `sections/05_registro_operador_masa.tex:195-220` |
| `ArticleVI.shared_incidence_pair` | incidence composition `90+120=210` | `HMTMD/HMTMD.lean`, imported shared theorem |

`HMT/Atlas.lean` certifies the shared nonadic quadratic atlas; it is not
identified with the particle census `81/56/13/324`. `HMT/Dodecaphase.lean`
certifies finite dodecaphasic identities. `HMTMD/HMTMD.lean` certifies the
`90/120` incidences and other shared microresults. The matrix above specifies
which additional assertions actually belong to this project.

## Dependencies and build order

There are no third-party dependencies: Lean core and `Std` are included in
the distribution. Lake resolves the modules in this order:

1. `HMT/Atlas.lean`, `HMT/Dodecaphase.lean`, `HMTMD/HMTMD.lean`;
2. `ArticleVI.lean`;
3. `lake build` from this directory.

The `#print axioms` commands in the root module display the axiomatic basis
of a sample. This project is a partial, finite formalization; it does not
claim to formalize the whole of Article VI or the entire General Mass Law.

The source locations above retain the line numbers of the frozen Spanish
edition. Translation does not change any `.lean` file. The original Spanish
README is preserved alongside this complete English translation.
