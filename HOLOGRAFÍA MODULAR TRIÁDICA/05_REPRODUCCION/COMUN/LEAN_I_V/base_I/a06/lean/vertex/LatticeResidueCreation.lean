import LatticeResidueProducts
import LatticeStateFieldMap

/-! Every integral residue product of two creative fields creates the
actual coefficient state. The opposite expansion contributes zero on the
vacuum; the first region has only its zero-index term at the constant
coefficient. No state-field product identity is imposed. -/

noncomputable section
namespace HMT.IV.LatticeResidueCreation

open LatticeOscillatorFock LatticeDescendantFields LatticeResidueProducts
open LatticeStateFieldMap LatticeTwoRegionFactor LatticeExponentialContraction

theorem residue_right_vacuum (o : Fin 12) (p : ℤ)
    (A B : VertexOperator ℂ (LatticeCarrier o)) (u : LatticeCarrier o)
    (hA : Creates o A u) (k : ℤ) (a : ℕ) :
    rightTerm p A B k a (vacuum o) = 0 := by
  simp only [rightTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    hA.1 (-a-1) (by omega), map_zero, smul_zero]

theorem residue_negative_vacuum (o : Fin 12) (p : ℤ)
    (A B : VertexOperator ℂ (LatticeCarrier o)) (u v : LatticeCarrier o)
    (hA : Creates o A u) (hB : Creates o B v) (k : ℤ) (hk : k < 0) :
    HVertexOperator.coeff (residueField p A B) k (vacuum o) = 0 := by
  rw [residueField_coefficient, residueCoefficient_apply]
  have hl (a : ℕ) : leftTerm p A B k a (vacuum o) = 0 := by
    simp only [leftTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hB.1 (k-a) (by omega), map_zero, smul_zero]
  simp only [hl, residue_right_vacuum o p A B u hA, finsum_zero, sub_self]

theorem residue_constant_vacuum (o : Fin 12) (p : ℤ)
    (A B : VertexOperator ℂ (LatticeCarrier o)) (u v : LatticeCarrier o)
    (hA : Creates o A u) (hB : Creates o B v) :
    HVertexOperator.coeff (residueField p A B) 0 (vacuum o) =
      HVertexOperator.coeff A (-p-1) v := by
  rw [residueField_coefficient, residueCoefficient_apply]
  simp only [residue_right_vacuum o p A B u hA, finsum_zero, sub_zero]
  rw [finsum_eq_single _ 0]
  · simp only [leftTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      Nat.cast_zero, sub_zero, zero_sub, hB.2]
    have he : leftExpansion p p 0 = (1 : ℂ) := by
      simp [leftExpansion]
    rw [he, one_smul]
  · intro a ha
    simp only [leftTerm, LinearMap.smul_apply, LinearMap.comp_apply,
      hB.1 (0-a) (by omega), map_zero, smul_zero]

theorem residue_creates (o : Fin 12) (p : ℤ)
    (A B : VertexOperator ℂ (LatticeCarrier o)) (u v : LatticeCarrier o)
    (hA : Creates o A u) (hB : Creates o B v) :
    Creates o (residueField p A B) (HVertexOperator.coeff A (-p-1) v) :=
  ⟨residue_negative_vacuum o p A B u v hA hB,
    residue_constant_vacuum o p A B u v hA hB⟩

theorem stateField_residue_creates (o : Fin 12) (p : ℤ) (u v : LatticeCarrier o) :
    Creates o (residueField p (stateField o u) (stateField o v))
      (HVertexOperator.coeff (stateField o u) (-p-1) v) :=
  residue_creates o p _ _ u v (stateField_creates o u) (stateField_creates o v)

end HMT.IV.LatticeResidueCreation
end

#print axioms HMT.IV.LatticeResidueCreation.residue_right_vacuum
#print axioms HMT.IV.LatticeResidueCreation.residue_negative_vacuum
#print axioms HMT.IV.LatticeResidueCreation.residue_constant_vacuum
#print axioms HMT.IV.LatticeResidueCreation.residue_creates
#print axioms HMT.IV.LatticeResidueCreation.stateField_residue_creates
