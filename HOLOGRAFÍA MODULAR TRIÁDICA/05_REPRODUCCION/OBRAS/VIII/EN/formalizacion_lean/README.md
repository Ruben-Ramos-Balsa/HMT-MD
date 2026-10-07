# Formalización Lean parcial — Artículo VII

Proyecto reproducible con Lean `4.21.0`. El archivo `ArticleVII.lean` contiene
un núcleo algebraico real y compilable para identidades explícitas del artículo.

## Matriz exacta de cobertura

| Teorema Lean | Enunciado comprobado | Fuente del Artículo VII |
|---|---|---|
| `ArticleVII.reverse_channel_involution` | el intercambio retardado/avanzado aplicado dos veces es la identidad | `manuscrito/81_propagacion_bidireccional.tex:240-253` |
| `ArticleVII.reverse_channel_exchanges` | intercambio tipado de los dos canales | `manuscrito/81_propagacion_bidireccional.tex:248-253` |
| `ArticleVII.symmetric_numerator_even_under_exchange` | paridad par del numerador simétrico | `manuscrito/81_propagacion_bidireccional.tex:280-298` |
| `ArticleVII.radiative_numerator_odd_under_exchange` | paridad impar del numerador radiativo | `manuscrito/81_propagacion_bidireccional.tex:280-299` |
| `ArticleVII.reconstruct_retarded_doubled` | `(ret+adv)+(ret-adv)=2 ret` | `manuscrito/81_propagacion_bidireccional.tex:286-299` |
| `ArticleVII.reconstruct_advanced_doubled` | `(ret+adv)-(ret-adv)=2 adv` | `manuscrito/81_propagacion_bidireccional.tex:286-299` |
| `ArticleVII.hexad_incidence` | `6·C(6,2)=90` | `manuscrito/sections/v_funcional_barbero.tex:3-13` |
| `ArticleVII.octad_incidence` | `8·C(6,2)=120` | `manuscrito/sections/v_funcional_barbero.tex:3-13` |
| `ArticleVII.recover_sector_90_scaled` | `120N-D=30N₉₀` | `manuscrito/sections/v_area_informacion.tex:178-196` |
| `ArticleVII.recover_sector_120_scaled` | `D-90N=30N₁₂₀` | `manuscrito/sections/v_area_informacion.tex:178-196` |
| `ArticleVII.bounce_polynomial_even` | paridad del núcleo cuadrático `base+curvature·u²` | `manuscrito/51_solucion_homogenea.tex:35-42` |
| `ArticleVII.bounce_polynomial_at_origin` | valor del núcleo cuadrático en `u=0` | `manuscrito/51_solucion_homogenea.tex:35-42` |
| `ArticleVII.bounce_polynomial_increment` | factorización del incremento respecto del rebote | `manuscrito/51_solucion_homogenea.tex:35-42` |

Las identidades simétrica/radiativa se formalizan en forma duplicada, sin
introducir división por dos: esto conserva exactamente su contenido algebraico
sobre enteros. El polinomio del rebote formaliza sólo la identidad cuadrática
subyacente a `y=s₀/ρ₀+6πGρ₀u²`; no afirma positividad, unicidad, regularidad ni
que el sistema diferencial completo haya sido formalizado.

## Dependencias y orden de construcción

No hay dependencias de terceros: sólo Lean core y `Std` de la distribución.

1. Seleccionar la versión declarada en `lean-toolchain`.
2. Construir `ArticleVII.lean` mediante `lake build` desde este directorio.
3. Revisar las salidas `#print axioms` del módulo raíz.

Este proyecto no declara una formalización completa del Artículo VII, de la
gravitación HMT–MD ni de sus realizaciones analíticas.
