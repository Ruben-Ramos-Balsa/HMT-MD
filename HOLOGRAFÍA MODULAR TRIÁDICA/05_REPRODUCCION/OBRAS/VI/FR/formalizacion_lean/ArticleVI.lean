import HMT.Atlas
import HMT.Dodecaphase
import HMTMD.HMTMD

/-!
Certificados finitos propios del Artículo VI. No formalizan la totalidad del
artículo ni sustituyen sus hipótesis, construcciones o pruebas analíticas.
-/

namespace ArticleVI

theorem route_family_class_count : 41 + 10 + 2 + 1 + 2 = 56 := by decide

theorem route_family_cell_coverage : 41 + 20 + 6 + 4 + 10 = 81 := by decide

theorem oriented_atlas_count : 81 * 4 = 324 := by decide

theorem seed_pair_count : 324 * 324 = 104976 := by decide

theorem additive_signature_multiplicity : 18 * 18 = 324 := by decide

theorem multiplicative_signature_multiplicity : 24 * 8 + 24 + 108 = 324 := by decide

theorem emission_weight_total :
    432 * 144 + 18 * 432 + 18 * 1944 = 104976 := by decide

def displacementReader (d1 d3 d4 d27 d36 : Int) : Int × Int × Int :=
  (d27 + d36, d1, (d4 - d3) / 2)

def autocorrelationReader (omega d1 p6 : Int) : Int × Int × Int :=
  (omega, d1, p6)

theorem electron_displacement_reader :
    displacementReader 54 56 68 48 32 = (80, 54, 6) := by native_decide

theorem electron_reader_coincidence :
    displacementReader 54 56 68 48 32 = autocorrelationReader 80 54 6 := by
  native_decide

theorem shared_incidence_pair : 90 + 120 = 210 := HMTMD.tower_210

end ArticleVI

#print axioms ArticleVI.electron_reader_coincidence
#print axioms HMT.aw_square_minus_identity
#print axioms HMT.v_alpha_norm_is_54
#print axioms HMTMD.hexad_incidence
