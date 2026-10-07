import LatticeFiniteGroundState
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.CategoryTheory.Abelian.Basic

/-! An invariant bilinear duality on the actual finite ground-state factor.
The dual is selected by the character of the inherited finite central extension;
no target matrix or pairing is supplied. This is a precursor for the TT product,
not a claim of the complete orbifold Jacobi identity. -/

noncomputable section
namespace HMT.IV.LatticeFiniteInvariantPairing

open LatticeTwistedFiniteQuotient LatticeFiniteRepresentation LatticeCocycle
open LatticeFiniteIrreducible LatticeFiniteGroundState LatticeFiniteCharacter
open CategoryTheory

def dualFDRep (o : Fin 12) : FDRep ℂ (FiniteExtension o) :=
  FDRep.of (constituentRepresentation o).dual

theorem dual_central_negative (o : Fin 12) : (dualFDRep o).ρ (1,0) = -1 := by
  change (constituentRepresentation o).dual (1,0) = -1
  apply LinearMap.ext
  intro f
  apply LinearMap.ext
  intro v
  change f (constituentRepresentation o ((1,0) : FiniteExtension o)⁻¹ v) = -f v
  have hz := central_inverse o 1
  dsimp only [centralElement] at hz
  rw [hz, constituent_central_involution_negative]
  simp

theorem dual_dimension (o : Fin 12) :
    Module.finrank ℂ (dualFDRep o) = 4096 := by
  change Module.finrank ℂ (Module.Dual ℂ (FiniteSpace o)) = 4096
  rw [Subspace.dual_finrank_eq, finiteSpace_dimension]

theorem equivariant_duality_dimension (o : Fin 12) :
    Module.finrank ℂ (finiteFDRep o ⟶ dualFDRep o) = 1 := by
  letI : Invertible (Fintype.card (FiniteExtension o) : ℂ) :=
    invertibleOfNonzero (by exact_mod_cast Fintype.card_ne_zero)
  have h := FDRep.scalar_product_char_eq_finrank_equivariant (finiteFDRep o) (dualFDRep o)
  rw [character_pair_sum o (dualFDRep o) (finiteFDRep o)
    (dual_central_negative o) (constituent_central_involution_negative o),
    dual_dimension] at h
  change _ = (Module.finrank ℂ (finiteFDRep o ⟶ dualFDRep o) : ℂ) at h
  have hf : Module.finrank ℂ (finiteFDRep o) = 4096 := finiteSpace_dimension o
  rw [hf, smul_eq_mul, invOf_eq_inv, finiteExtension_card_rank24] at h
  norm_num at h
  exact_mod_cast h.symm

theorem equivariant_duality_exists (o : Fin 12) :
    ∃ f : finiteFDRep o ⟶ dualFDRep o, f ≠ 0 := by
  haveI : Nontrivial (finiteFDRep o ⟶ dualFDRep o) :=
    Module.finrank_pos_iff.mp (by rw [equivariant_duality_dimension]; decide)
  exact exists_ne 0

/-- A choice of nonzero equivariant duality. Its scale is not normalized. -/
def dualityMorphism (o : Fin 12) : finiteFDRep o ⟶ dualFDRep o :=
  Classical.choose (equivariant_duality_exists o)

theorem dualityMorphism_ne_zero (o : Fin 12) : dualityMorphism o ≠ 0 :=
  Classical.choose_spec (equivariant_duality_exists o)

def invariantPairing (o : Fin 12) : LinearMap.BilinForm ℂ (FiniteSpace o) :=
  (dualityMorphism o).hom.hom

theorem invariantPairing_injective (o : Fin 12) :
    Function.Injective (invariantPairing o) := by
  letI : Mono (dualityMorphism o) := mono_of_nonzero_from_simple (dualityMorphism_ne_zero o)
  haveI : Mono ((Action.forget (FGModuleCat ℂ) (FiniteExtension o)).map
      (dualityMorphism o)) := inferInstance
  haveI : Mono (dualityMorphism o).hom := inferInstanceAs
    (Mono ((Action.forget (FGModuleCat ℂ) (FiniteExtension o)).map (dualityMorphism o)))
  exact (ModuleCat.mono_iff_injective
    ((forget₂ (FGModuleCat ℂ) (ModuleCat ℂ)).map (dualityMorphism o).hom)).mp inferInstance

theorem invariantPairing_surjective (o : Fin 12) :
    Function.Surjective (invariantPairing o) := by
  apply (LinearMap.injective_iff_surjective_of_finrank_eq_finrank ?_).mp
    (invariantPairing_injective o)
  exact (Subspace.dual_finrank_eq).symm

theorem invariantPairing_nondegenerate (o : Fin 12) :
    (invariantPairing o).Nondegenerate := by
  exact LinearMap.BilinForm.nondegenerate_iff_ker_eq_bot.mpr
    (LinearMap.ker_eq_bot.mpr (invariantPairing_injective o))

def invariantDuality (o : Fin 12) : FiniteSpace o ≃ₗ[ℂ] Module.Dual ℂ (FiniteSpace o) :=
  LinearEquiv.ofBijective (invariantPairing o)
    ⟨invariantPairing_injective o, invariantPairing_surjective o⟩

theorem invariantPairing_contravariant (o : Fin 12) (g : FiniteExtension o)
    (v w : FiniteSpace o) :
    invariantPairing o (constituentRepresentation o g v) w =
      invariantPairing o v (constituentRepresentation o g⁻¹ w) := by
  have h := (dualityMorphism o).comm g
  have hh := congrArg (fun F => F.hom v) h
  change invariantPairing o (constituentRepresentation o g v) =
    (constituentRepresentation o).dual g (invariantPairing o v) at hh
  exact LinearMap.congr_fun hh w

theorem invariantPairing_invariant (o : Fin 12) (g : FiniteExtension o)
    (v w : FiniteSpace o) :
    invariantPairing o (constituentRepresentation o g v)
      (constituentRepresentation o g w) = invariantPairing o v w := by
  rw [invariantPairing_contravariant]
  have h : constituentRepresentation o g⁻¹ (constituentRepresentation o g w) = w := by
    rw [← Module.End.mul_apply, ← map_mul, inv_mul_cancel, map_one, Module.End.one_apply]
  rw [h]

theorem invariantPairing_right_separating (o : Fin 12) (w : FiniteSpace o)
    (h : ∀ v, invariantPairing o v w = 0) : w = 0 := by
  apply (Module.forall_dual_apply_eq_zero_iff ℂ w).mp
  intro f
  obtain ⟨v, rfl⟩ := invariantPairing_surjective o f
  exact h v

theorem latticeOperator_preserves_pairing (o : Fin 12) (x : LatticeCocycle.Lattice o)
    (v w : FiniteSpace o) :
    invariantPairing o (latticeOperator o x v) (latticeOperator o x w) =
      invariantPairing o v w :=
  invariantPairing_invariant o (parityLift o (parityCoordinates o x)) v w

theorem invariantDuality_represents (o : Fin 12) (f : Module.Dual ℂ (FiniteSpace o))
    (w : FiniteSpace o) : invariantPairing o ((invariantDuality o).symm f) w = f w := by
  exact LinearMap.congr_fun ((invariantDuality o).apply_symm_apply f) w

theorem invariantDuality_representation_unique (o : Fin 12)
    (f : Module.Dual ℂ (FiniteSpace o)) (v : FiniteSpace o)
    (h : ∀ w, invariantPairing o v w = f w) : v = (invariantDuality o).symm f := by
  apply (invariantDuality o).injective
  apply LinearMap.ext
  intro w
  change invariantPairing o v w = invariantPairing o ((invariantDuality o).symm f) w
  rw [invariantDuality_represents]
  exact h w

#print axioms HMT.IV.LatticeFiniteInvariantPairing.equivariant_duality_dimension
#print axioms HMT.IV.LatticeFiniteInvariantPairing.invariantPairing_nondegenerate
#print axioms HMT.IV.LatticeFiniteInvariantPairing.invariantPairing_invariant

end HMT.IV.LatticeFiniteInvariantPairing
end
