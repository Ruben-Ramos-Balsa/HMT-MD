# Partial Lean formalization — Article VII

Reproducible project using Lean `4.21.0`. `ArticleVII.lean` contains an actual,
compilable algebraic core for explicit identities in the article.

## Exact coverage matrix

| Lean theorem | Checked statement | Article VII source |
|---|---|---|
| `ArticleVII.reverse_channel_involution` | exchanging retarded/advanced channels twice is the identity | `manuscrito/81_propagacion_bidireccional.tex:240-253` |
| `ArticleVII.reverse_channel_exchanges` | typed exchange of the two channels | `manuscrito/81_propagacion_bidireccional.tex:248-253` |
| `ArticleVII.symmetric_numerator_even_under_exchange` | even parity of the symmetric numerator | `manuscrito/81_propagacion_bidireccional.tex:280-298` |
| `ArticleVII.radiative_numerator_odd_under_exchange` | odd parity of the radiative numerator | `manuscrito/81_propagacion_bidireccional.tex:280-299` |
| `ArticleVII.reconstruct_retarded_doubled` | `(ret+adv)+(ret-adv)=2 ret` | `manuscrito/81_propagacion_bidireccional.tex:286-299` |
| `ArticleVII.reconstruct_advanced_doubled` | `(ret+adv)-(ret-adv)=2 adv` | `manuscrito/81_propagacion_bidireccional.tex:286-299` |
| `ArticleVII.hexad_incidence` | `6·C(6,2)=90` | `manuscrito/sections/v_funcional_barbero.tex:3-13` |
| `ArticleVII.octad_incidence` | `8·C(6,2)=120` | `manuscrito/sections/v_funcional_barbero.tex:3-13` |
| `ArticleVII.recover_sector_90_scaled` | `120N-D=30N₉₀` | `manuscrito/sections/v_area_informacion.tex:178-196` |
| `ArticleVII.recover_sector_120_scaled` | `D-90N=30N₁₂₀` | `manuscrito/sections/v_area_informacion.tex:178-196` |
| `ArticleVII.bounce_polynomial_even` | parity of the quadratic kernel `base+curvature·u²` | `manuscrito/51_solucion_homogenea.tex:35-42` |
| `ArticleVII.bounce_polynomial_at_origin` | value of the quadratic kernel at `u=0` | `manuscrito/51_solucion_homogenea.tex:35-42` |
| `ArticleVII.bounce_polynomial_increment` | factorization of the increment relative to the bounce | `manuscrito/51_solucion_homogenea.tex:35-42` |

The symmetric/radiative identities are formalized in doubled form, without
introducing division by two: this preserves exactly their algebraic content
over the integers. The bounce polynomial formalizes only the quadratic
identity underlying `y=s₀/ρ₀+6πGρ₀u²`; it does not assert positivity,
uniqueness, regularity, or formalization of the complete differential system.

## Dependencies and build order

There are no third-party dependencies: only Lean core and `Std` from the distribution.

1. Select the version declared in `lean-toolchain`.
2. Build `ArticleVII.lean` with `lake build` from this directory.
3. Inspect the `#print axioms` outputs from the root module.

This project does not claim a complete formalization of Article VII,
HMT–MD gravitation, or its analytic realizations.

The source locations above retain the line numbers of the frozen Spanish
edition. Translation does not change any `.lean` file. The original Spanish
README is preserved alongside this complete English translation.
