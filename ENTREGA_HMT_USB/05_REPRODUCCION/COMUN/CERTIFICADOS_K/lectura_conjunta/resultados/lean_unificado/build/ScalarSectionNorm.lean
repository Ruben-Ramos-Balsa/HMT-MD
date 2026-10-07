import H4Quotient
import Mathlib.Data.Real.Basic

/-! Article II, eq:el-lector-determinantal. The multiplicative norm is taken
over the actual local quotient; the single autoscale application is explicit.
The reader is declared here, not selected by the cardinality theorem alone. -/
namespace HMT.II.DeterminantalAction
noncomputable section

open scoped BigOperators

def sectionNorm (s : LocalQuotient → ℝ) : ℝ := ∏ g, s g

def constantSection (alpha : ℝ) : LocalQuotient → ℝ := fun _ => alpha

theorem sectionNorm_mul (s t : LocalQuotient → ℝ) :
    sectionNorm (fun g => s g * t g) = sectionNorm s * sectionNorm t := by
  simp only [sectionNorm, Finset.prod_mul_distrib]

theorem constantSection_norm (alpha : ℝ) :
    sectionNorm (constantSection alpha) = alpha ^ 16 := by
  simp [sectionNorm, constantSection, localQuotient_cardinal]

theorem constantSection_norm_pos {alpha : ℝ} (ha : 0 < alpha) :
    0 < sectionNorm (constantSection alpha) := by
  rw [constantSection_norm]
  exact pow_pos ha _

/-- Phi is applied once to the base of the action line, after the quotient norm. -/
def actionScale (phi alpha : ℝ) : ℝ := phi * sectionNorm (constantSection alpha)

theorem actionScale_eq (phi alpha : ℝ) : actionScale phi alpha = phi * alpha ^ 16 := by
  rw [actionScale, constantSection_norm]

theorem actionScale_pos {phi alpha : ℝ} (hp : 0 < phi) (ha : 0 < alpha) :
    0 < actionScale phi alpha := mul_pos hp (constantSection_norm_pos ha)

#print axioms sectionNorm_mul
#print axioms constantSection_norm
#print axioms actionScale_eq
#print axioms actionScale_pos

end
end HMT.II.DeterminantalAction
