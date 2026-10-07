import LatticeConformalState

/-! The coefficient reader is linear on the already constructed fields. -/

noncomputable section
namespace HMT.IV.LatticeConformalCoefficient

open LatticeCocycle LatticeOscillatorFock LatticeNormalOrderedField
open LatticeHeisenbergField LatticeConformalState LatticeGramDual
open scoped BigOperators

def coefficientReader (o : Fin 12) (k : ℤ) :
    VertexOperator ℂ (LatticeCarrier o) →ₗ[ℂ] Module.End ℂ (LatticeCarrier o) where
  toFun A := HVertexOperator.coeff A k
  map_add' A B := by simp only [HVertexOperator.coeff_add, Pi.add_apply]
  map_smul' c A := by simp only [HVertexOperator.coeff_smul, Pi.smul_apply, RingHom.id_apply]

theorem conformalMode_normal_sum (o : Fin 12) (m : ℤ) :
    conformalMode o m = (2 : ℂ)⁻¹ • ∑ i, ∑ j,
      gramInv o i j • normalCoefficient o i 0 (heisenbergField o j) (-m-2) := by
  change coefficientReader o (-m-2) (conformalField o) = _
  rw [conformalField_eq_normal_sum]
  simp only [map_smul, map_sum]
  rfl

theorem conformalMode_normal_sum_apply (o : Fin 12) (m : ℤ) (v : LatticeCarrier o) :
    conformalMode o m v = (2 : ℂ)⁻¹ • ∑ i, ∑ j,
      gramInv o i j • normalCoefficient o i 0 (heisenbergField o j) (-m-2) v := by
  rw [conformalMode_normal_sum]
  simp only [LinearMap.smul_apply, LinearMap.sum_apply]

end HMT.IV.LatticeConformalCoefficient
end

#print axioms HMT.IV.LatticeConformalCoefficient.coefficientReader
#print axioms HMT.IV.LatticeConformalCoefficient.conformalMode_normal_sum
#print axioms HMT.IV.LatticeConformalCoefficient.conformalMode_normal_sum_apply
