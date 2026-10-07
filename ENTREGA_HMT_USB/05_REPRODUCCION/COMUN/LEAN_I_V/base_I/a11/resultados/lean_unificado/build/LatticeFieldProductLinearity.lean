import LatticeChargedVertexField

/-!
The two actual coefficient products as linear maps into bivariate series.
A linear operation on those series (in particular polynomial multiplication)
preserves extension from the existing carrier basis to every carrier state.
No locality hypothesis is inserted: the basis identity is the explicit
input to this linear extension lemma.
-/

noncomputable section
namespace HMT.IV.LatticeFieldProductLinearity

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeChargedVertexField

def forwardProduct (o : Fin 12) (x y : Lattice o) :
    LatticeCarrier o →ₗ[ℂ] (ℤ → ℤ → LatticeCarrier o) where
  toFun v := fun k l => fieldCoefficient o x k (fieldCoefficient o y l v)
  map_add' v w := by funext k l; simp
  map_smul' c v := by funext k l; simp

def reverseProduct (o : Fin 12) (x y : Lattice o) :
    LatticeCarrier o →ₗ[ℂ] (ℤ → ℤ → LatticeCarrier o) where
  toFun v := fun k l => fieldCoefficient o y l (fieldCoefficient o x k v)
  map_add' v w := by funext k l; simp
  map_smul' c v := by funext k l; simp

/-- A single linear series operation is fixed before quantifying over states. -/
theorem field_product_identity_of_basis (o : Fin 12) (x y : Lattice o)
    (P : Module.End ℂ (ℤ → ℤ → LatticeCarrier o))
    (hP : ∀ (a : Occupation o) (z : Lattice o),
      P (forwardProduct o x y (carrierBasis o (a,z))) =
        P (reverseProduct o x y (carrierBasis o (a,z)))) :
    ∀ v : LatticeCarrier o,
      P (forwardProduct o x y v) = P (reverseProduct o x y v) := by
  have he : P.comp (forwardProduct o x y) = P.comp (reverseProduct o x y) := by
    apply (carrierBasis o).ext
    rintro ⟨a,z⟩
    exact hP a z
  exact fun v => LinearMap.congr_fun he v

theorem field_product_coefficients_of_basis (o : Fin 12) (x y : Lattice o)
    (P : Module.End ℂ (ℤ → ℤ → LatticeCarrier o))
    (hP : ∀ (a : Occupation o) (z : Lattice o),
      P (forwardProduct o x y (carrierBasis o (a,z))) =
        P (reverseProduct o x y (carrierBasis o (a,z))))
    (v : LatticeCarrier o) (k l : ℤ) :
    P (fun k l => fieldCoefficient o x k (fieldCoefficient o y l v)) k l =
      P (fun k l => fieldCoefficient o y l (fieldCoefficient o x k v)) k l :=
  congrFun (congrFun (field_product_identity_of_basis o x y P hP v) k) l

end HMT.IV.LatticeFieldProductLinearity
end

#print axioms HMT.IV.LatticeFieldProductLinearity.field_product_identity_of_basis
#print axioms HMT.IV.LatticeFieldProductLinearity.field_product_coefficients_of_basis
