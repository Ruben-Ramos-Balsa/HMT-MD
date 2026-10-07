import Mathlib.Algebra.DirectSum.Module
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Eigenspace.Basic

/-!
# The sign of an integral weight

If the natural-number eigenspaces of an endomorphism span its original complex
module, they form an internal direct sum.  Multiplication by `(-1)^d` on the
weight-`d` summand therefore defines a linear involution of that same module.
No finite-dimensionality, choice of eigenbasis, or new carrier is assumed.
-/

noncomputable section

namespace HMT.IV.CoordinateWeightSign

open scoped DirectSum

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- The natural-number weight space of the given endomorphism. -/
def weightSpace (E : Module.End ℂ V) (d : ℕ) : Submodule ℂ V :=
  Module.End.eigenspace E (d : ℂ)

@[simp]
theorem mem_weightSpace (E : Module.End ℂ V) (d : ℕ) (v : V) :
    v ∈ weightSpace E d ↔ E v = (d : ℂ) • v :=
  Module.End.mem_eigenspace_iff

/-- Independence is supplied by distinct eigenvalues, not an extra hypothesis. -/
theorem weightSpaces_independent (E : Module.End ℂ V) :
    iSupIndep (weightSpace E) :=
  E.eigenspaces_iSupIndep.comp (Nat.cast_injective : Function.Injective (Nat.cast : ℕ → ℂ))

/-- Spanning makes the eigenspace decomposition internal to `V`. -/
theorem weightSpaces_internal (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) :
    DirectSum.IsInternal (weightSpace E) :=
  DirectSum.isInternal_submodule_of_iSupIndep_of_iSup_eq_top
    (weightSpaces_independent E) hspan

/-- Recombination is an isomorphism onto the original carrier. -/
def weightDecomposition (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) :
    (⨁ d : ℕ, weightSpace E d) ≃ₗ[ℂ] V :=
  LinearEquiv.ofBijective (DirectSum.coeLinearMap (weightSpace E))
    (weightSpaces_internal E hspan)

/-- The coordinate sign, transported back to the original module. -/
def weightSign (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) : Module.End ℂ V :=
  (DirectSum.toModule ℂ ℕ V
    (fun d => ((-1 : ℂ) ^ d) • (weightSpace E d).subtype)).comp
      (weightDecomposition E hspan).symm.toLinearMap

/-- On a homogeneous vector, the operator has its defining sign. -/
theorem weightSign_apply_of_weight (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) (d : ℕ)
    {v : V} (hv : E v = (d : ℂ) • v) :
    weightSign E hspan v = ((-1 : ℂ) ^ d) • v := by
  have hmem : v ∈ weightSpace E d := (mem_weightSpace E d v).mpr hv
  have hdecomp : (weightDecomposition E hspan).symm v =
      DirectSum.lof ℂ ℕ (fun d => weightSpace E d) d ⟨v, hmem⟩ := by
    apply (weightDecomposition E hspan).injective
    simp only [LinearEquiv.apply_symm_apply]
    change v = DirectSum.coeLinearMap (weightSpace E)
      (DirectSum.of (fun d => weightSpace E d) d ⟨v, hmem⟩)
    rw [DirectSum.coeLinearMap_of]
  unfold weightSign
  rw [LinearMap.comp_apply, LinearEquiv.coe_coe, hdecomp, DirectSum.toModule_lof]
  rfl

/-- Endomorphisms are equal if they agree on all weight vectors. -/
theorem ext_on_weights (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤)
    {f g : Module.End ℂ V}
    (h : ∀ (d : ℕ) (v : V), E v = (d : ℂ) • v → f v = g v) : f = g := by
  apply LinearMap.ext
  intro v
  have hv : v ∈ ⨆ d : ℕ, weightSpace E d := by rw [hspan]; trivial
  apply Submodule.iSup_induction (weightSpace E) (motive := fun v => f v = g v) hv
  · intro d v hv
    exact h d v ((mem_weightSpace E d v).mp hv)
  · simp only [map_zero]
  · intro x y hx hy
    simp only [map_add, hx, hy]

/-- The square is the identity endomorphism. -/
theorem weightSign_sq (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) :
    weightSign E hspan * weightSign E hspan = 1 := by
  apply ext_on_weights E hspan
  intro d v hv
  change weightSign E hspan (weightSign E hspan v) = v
  rw [weightSign_apply_of_weight E hspan d hv, map_smul,
    weightSign_apply_of_weight E hspan d hv, smul_smul, ← mul_pow]
  simp

/-- Pointwise involutivity, independent of multiplication notation on endomorphisms. -/
theorem weightSign_involutive (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) :
    Function.Involutive (weightSign E hspan) := by
  intro v
  exact DFunLike.congr_fun (weightSign_sq E hspan) v

/-- The coordinate sign commutes with the original weight operator. -/
theorem weightSign_commutes_energy (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) :
    weightSign E hspan * E = E * weightSign E hspan := by
  apply ext_on_weights E hspan
  intro d v hv
  change weightSign E hspan (E v) = E (weightSign E hspan v)
  rw [hv, map_smul, weightSign_apply_of_weight E hspan d hv, map_smul, hv]
  exact smul_comm _ _ _

/-- The action on the spanning eigenspaces determines this operator uniquely. -/
theorem weightSign_unique (E : Module.End ℂ V)
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) (S : Module.End ℂ V)
    (hS : ∀ (d : ℕ) (v : V), E v = (d : ℂ) • v → S v = ((-1 : ℂ) ^ d) • v) :
    S = weightSign E hspan := by
  apply ext_on_weights E hspan
  intro d v hv
  rw [hS d v hv, weightSign_apply_of_weight E hspan d hv]

end HMT.IV.CoordinateWeightSign
