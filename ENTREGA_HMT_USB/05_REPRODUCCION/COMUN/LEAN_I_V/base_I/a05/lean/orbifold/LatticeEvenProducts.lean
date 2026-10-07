import LatticeEvenLocality
import LatticeStateFieldProducts

/-! Residue products on the actual fixed carrier. Restriction commutes with
both expansion regions, their composition orders, and the pointwise finite
sums. The identity is not supplied as a new axiom of an even algebra. -/

noncomputable section
namespace HMT.IV.LatticeEvenProducts

open LatticeOscillatorFock LatticeStateFieldMap LatticeEvenVertexFields
open LatticeEvenTranslation LatticeEvenLocality LatticeResidueProducts
open LatticeStateFieldProducts

section Naturality
variable {V W : Type*} [AddCommGroup V] [Module ℂ V]
  [AddCommGroup W] [Module ℂ W]

/-- Any coefficient-intertwining linear map transports both genuine residue
sums. No surjectivity or injectivity is required for this identity. -/
theorem residueCoefficient_intertwines (L : V →ₗ[ℂ] W)
    (A B : VertexOperator ℂ V) (A' B' : VertexOperator ℂ W)
    (hA : ∀ k v, L (HVertexOperator.coeff A k v) = HVertexOperator.coeff A' k (L v))
    (hB : ∀ k v, L (HVertexOperator.coeff B k v) = HVertexOperator.coeff B' k (L v))
    (p k : ℤ) (v : V) :
    L (residueCoefficient p A B k v) = residueCoefficient p A' B' k (L v) := by
  have hl (a : ℕ) : L (leftTerm p A B k a v) = leftTerm p A' B' k a (L v) := by
    simp only [leftTerm, LinearMap.smul_apply, LinearMap.comp_apply, map_smul, hA, hB]
  have hr (a : ℕ) : L (rightTerm p A B k a v) = rightTerm p A' B' k a (L v) := by
    simp only [rightTerm, LinearMap.smul_apply, LinearMap.comp_apply, map_smul, hA, hB]
  have hls : L (∑ᶠ a, leftTerm p A B k a v) = ∑ᶠ a, L (leftTerm p A B k a v) :=
    L.toAddMonoidHom.map_finsum (leftTerm_finite p A B k v)
  have hrs : L (∑ᶠ a, rightTerm p A B k a v) = ∑ᶠ a, L (rightTerm p A B k a v) :=
    L.toAddMonoidHom.map_finsum (rightTerm_finite p A B k v)
  rw [residueCoefficient_apply, residueCoefficient_apply, map_sub, hls, hrs]
  simp only [hl, hr]

end Naturality

theorem even_residue_coe (o : Fin 12) (p k : ℤ) (u v w : evenSpace o) :
    (residueCoefficient p (evenField o u) (evenField o v) k w).val =
      residueCoefficient p (stateField o u.val) (stateField o v.val) k w.val := by
  apply residueCoefficient_intertwines (evenSpace o).subtype
  · intro a x
    simp only [Submodule.subtype_apply, evenField_coefficient, evenCoefficient_coe]
  · intro a x
    simp only [Submodule.subtype_apply, evenField_coefficient, evenCoefficient_coe]

/-- Every integer product of the even fields is the even field of its
produced state. These are restrictions of the same fields on the same lattice. -/
theorem evenField_residue_product (o : Fin 12) (p : ℤ) (u v : evenSpace o) :
    evenField o (HVertexOperator.coeff (evenField o u) (-p-1) v) =
      residueField p (evenField o u) (evenField o v) := by
  apply HVertexOperator.coeff_inj
  funext k
  apply LinearMap.ext
  intro w
  apply Subtype.ext
  rw [evenField_coefficient, evenCoefficient_coe, residueField_coefficient,
    even_residue_coe, evenField_coefficient, evenCoefficient_coe]
  exact LinearMap.congr_fun (stateField_product_coefficient o p k u.val v.val) w.val

theorem evenField_iterate (o : Fin 12) (p k : ℤ) (u v w : evenSpace o) :
    HVertexOperator.coeff
      (evenField o (HVertexOperator.coeff (evenField o u) (-p-1) v)) k w =
      (∑ᶠ a, leftTerm p (evenField o u) (evenField o v) k a w) -
        ∑ᶠ a, rightTerm p (evenField o u) (evenField o v) k a w := by
  rw [evenField_residue_product, residueField_coefficient, residueCoefficient_apply]

end HMT.IV.LatticeEvenProducts
end

#print axioms HMT.IV.LatticeEvenProducts.residueCoefficient_intertwines
#print axioms HMT.IV.LatticeEvenProducts.even_residue_coe
#print axioms HMT.IV.LatticeEvenProducts.evenField_residue_product
#print axioms HMT.IV.LatticeEvenProducts.evenField_iterate
