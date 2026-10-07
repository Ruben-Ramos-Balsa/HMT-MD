import LatticeResidueCreation
import LatticeResidueTranslation
import LatticeDongAllIndices
import LatticeStateFieldTranslation

/-! The state-field map preserves every integral residue product.
Both fields are the already constructed Laurent operators. The equality
follows from proved locality, creativity and differential covariance,
not from a product-compatibility axiom. -/

noncomputable section
namespace HMT.IV.LatticeStateFieldProducts

open LatticeOscillatorFock LatticeStateFieldMap LatticeResidueProducts
open LatticeResidueCreation LatticeResidueTranslation LatticeDongAllIndices
open LatticeStateFieldTranslation LatticeDescendantLocality
open LatticeCovariantFieldUniqueness

theorem stateField_residue_product (o : Fin 12) (p : ℤ) (u v : LatticeCarrier o) :
    stateField o (HVertexOperator.coeff (stateField o u) (-p-1) v) =
      residueField p (stateField o u) (stateField o v) := by
  apply creative_covariant_fields_unique o _ _
    (HVertexOperator.coeff (stateField o u) (-p-1) v)
  · exact stateField_local o _
  · intro w
    exact residueField_local_all_indices (stateField_local o u w)
      (stateField_local o v w) (stateField_local o u v) p
  · exact stateField_translation_covariant o _
  · exact residueField_translation _ p _ _
      (stateField_translation_covariant o u) (stateField_translation_covariant o v)
  · exact stateField_creates o _
  · exact stateField_residue_creates o p u v

theorem stateField_product_coefficient (o : Fin 12) (p k : ℤ)
    (u v : LatticeCarrier o) :
    HVertexOperator.coeff
      (stateField o (HVertexOperator.coeff (stateField o u) (-p-1) v)) k =
        residueCoefficient p (stateField o u) (stateField o v) k := by
  rw [stateField_residue_product, residueField_coefficient]

/-- The full two-region iterate formula, on every vector and at every
integral product index. The two locally finite sums keep their order. -/
theorem stateField_iterate (o : Fin 12) (p k : ℤ) (u v w : LatticeCarrier o) :
    HVertexOperator.coeff
      (stateField o (HVertexOperator.coeff (stateField o u) (-p-1) v)) k w =
      (∑ᶠ a, leftTerm p (stateField o u) (stateField o v) k a w) -
        ∑ᶠ a, rightTerm p (stateField o u) (stateField o v) k a w := by
  rw [stateField_product_coefficient, residueCoefficient_apply]

end HMT.IV.LatticeStateFieldProducts
end

#print axioms HMT.IV.LatticeStateFieldProducts.stateField_residue_product
#print axioms HMT.IV.LatticeStateFieldProducts.stateField_product_coefficient
#print axioms HMT.IV.LatticeStateFieldProducts.stateField_iterate
