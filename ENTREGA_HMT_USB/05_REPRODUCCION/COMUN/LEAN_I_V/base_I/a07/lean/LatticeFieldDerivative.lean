import LatticeTranslationLinear
import LatticeResidueProducts

/-! The ordinary derivative of a genuine Laurent field and its covariance.
The lower Laurent bound is transported explicitly; no completed-space
summation or truncation uniform in the input vector is introduced. -/

noncomputable section
namespace HMT.IV.LatticeFieldDerivative

open HMT.IV.LatticeTranslationLinear HMT.IV.LatticeResidueProducts
variable {V : Type*} [AddCommGroup V] [Module ℂ V]

def derivativeCoefficient (B : VertexOperator ℂ V) (k : ℤ) : Module.End ℂ V :=
  ((k : ℂ)+1) • HVertexOperator.coeff B (k+1)

theorem derivative_bounded (B : VertexOperator ℂ V) (v : V) :
    ∃ b : ℤ, ∀ k < b, derivativeCoefficient B k v = 0 := by
  obtain ⟨b,hb⟩ := field_lower_bound B v
  refine ⟨b-1, ?_⟩
  intro k hk
  simp only [derivativeCoefficient, LinearMap.smul_apply, hb (k+1) (by omega),
    smul_zero]

def derivativeField (B : VertexOperator ℂ V) : VertexOperator ℂ V :=
  VertexOperator.of_coeff (derivativeCoefficient B) (derivative_bounded B)

theorem derivativeField_coefficient (B : VertexOperator ℂ V) (k : ℤ) :
    HVertexOperator.coeff (derivativeField B) k =
      ((k : ℂ)+1) • HVertexOperator.coeff B (k+1) := by
  apply LinearMap.ext
  intro v
  rfl

theorem derivative_covariant {T : Module.End ℂ V} {B : VertexOperator ℂ V}
    (hB : TranslationCovariant T B) : TranslationCovariant T (derivativeField B) := by
  intro k
  rw [derivativeField_coefficient, derivativeField_coefficient,
    mul_smul_comm, smul_mul_assoc, ← smul_sub, hB (k+1)]

theorem derivative_regular (B : VertexOperator ℂ V) (v : V)
    (h : ∀ k : ℤ, k < 0 → HVertexOperator.coeff B k v = 0)
    (k : ℤ) (hk : k < 0) : HVertexOperator.coeff (derivativeField B) k v = 0 := by
  rw [derivativeField_coefficient, LinearMap.smul_apply]
  by_cases h1 : k+1 < 0
  · rw [h (k+1) h1, smul_zero]
  · have he : k = -1 := by omega
    subst k
    norm_num

theorem derivative_constant (B : VertexOperator ℂ V) (v : V) :
    HVertexOperator.coeff (derivativeField B) 0 v = HVertexOperator.coeff B 1 v := by
  rw [derivativeField_coefficient, LinearMap.smul_apply]
  norm_num

end HMT.IV.LatticeFieldDerivative
end

#print axioms HMT.IV.LatticeFieldDerivative.derivative_bounded
#print axioms HMT.IV.LatticeFieldDerivative.derivativeField_coefficient
#print axioms HMT.IV.LatticeFieldDerivative.derivative_covariant
#print axioms HMT.IV.LatticeFieldDerivative.derivative_regular
#print axioms HMT.IV.LatticeFieldDerivative.derivative_constant
