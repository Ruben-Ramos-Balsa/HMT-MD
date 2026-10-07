import WittNegationLift
import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Mathlib.Tactic

/-!
Charge reflection on the actual integral lattice and its twisted group algebra.
Each finite negation-stable charge set gives a faithful finite-dimensional
model of the restriction of theta. Its trace counts only the zero charge.
No FLM construction or Monster identification is assumed.
-/

noncomputable section
namespace HMT.IV.LatticeChargeParityTrace

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.WittNegationLift
open scoped BigOperators

theorem negation_fixed_iff_zero (o : Fin 12) (x : Lattice o) : -x = x ↔ x = 0 := by
  constructor
  · intro h
    apply (latticeBasis o).repr.injective
    ext i
    have hi := congrArg (fun y : Lattice o => (latticeBasis o).repr y i) h
    simp only [map_neg, Finsupp.neg_apply] at hi
    simp only [map_zero, Finsupp.zero_apply]
    omega
  · rintro rfl
    exact neg_zero

abbrev Charge (o : Fin 12) (S : Finset (Lattice o)) := {x : Lattice o // x ∈ S}
abbrev ChargeSpace (o : Fin 12) (S : Finset (Lattice o)) := Charge o S → ℂ

def chargeNegation (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) : Charge o S ≃ Charge o S where
  toFun x := ⟨-x.val, hS x.val x.property⟩
  invFun x := ⟨-x.val, hS x.val x.property⟩
  left_inv x := Subtype.ext (neg_neg x.val)
  right_inv x := Subtype.ext (neg_neg x.val)

def chargeParity (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) : Module.End ℂ (ChargeSpace o S) where
  toFun v x := v (chargeNegation o S hS x)
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

theorem chargeParity_apply (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) (v : ChargeSpace o S) (x : Charge o S) :
    chargeParity o S hS v x = v (chargeNegation o S hS x) := rfl

def chargeEmbedding (o : Fin 12) (S : Finset (Lattice o)) :
    ChargeSpace o S →ₗ[ℂ] TwistedAlgebra o :=
  Fintype.linearCombination ℂ (fun x : Charge o S => basisElement o x.val)

def chargeCoefficient (o : Fin 12) (f : TwistedAlgebra o) (x : Lattice o) : ℂ :=
  (show Lattice o →₀ ℂ from f) x

theorem chargeEmbedding_apply (o : Fin 12) (S : Finset (Lattice o))
    (v : ChargeSpace o S) :
    chargeEmbedding o S v = ∑ x : Charge o S, v x • basisElement o x.val := rfl

theorem chargeEmbedding_coefficient (o : Fin 12) (S : Finset (Lattice o))
    (v : ChargeSpace o S) (x : Charge o S) :
    chargeCoefficient o (chargeEmbedding o S v) x.val = v x := by
  classical
  rw [chargeEmbedding_apply]
  change (∑ y : Charge o S, v y • Finsupp.single y.val (1 : ℂ)) x.val = v x
  simp only [Finsupp.finset_sum_apply, Finsupp.smul_apply, smul_eq_mul,
    Finsupp.single_apply]
  rw [Finset.sum_eq_single x]
  · simp
  · intro y _ hy
    have hxy : y.val ≠ x.val := fun h => hy (Subtype.ext h)
    simp [hxy]
  · simp

theorem chargeEmbedding_injective (o : Fin 12) (S : Finset (Lattice o)) :
    Function.Injective (chargeEmbedding o S) := by
  intro v w h
  funext x
  have := congrArg (fun f : TwistedAlgebra o => chargeCoefficient o f x.val) h
  simpa only [chargeEmbedding_coefficient] using this

/-- The finite coordinate model is the restriction of the actual theta,
not an unrelated permutation matrix. -/
theorem chargeEmbedding_intertwines (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) (v : ChargeSpace o S) :
    theta o (chargeEmbedding o S v) =
      chargeEmbedding o S (chargeParity o S hS v) := by
  classical
  simp only [chargeEmbedding_apply, map_sum, map_smul, theta_basis,
    chargeParity_apply]
  have h := Equiv.sum_comp (chargeNegation o S hS)
    (fun x : Charge o S => v x • basisElement o (-x.val))
  simpa only [chargeNegation, Equiv.coe_fn_mk, neg_neg] using h.symm

theorem chargeParity_matrix (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) (x y : Charge o S) :
    LinearMap.toMatrix (Pi.basisFun ℂ (Charge o S))
      (Pi.basisFun ℂ (Charge o S)) (chargeParity o S hS) x y =
        if y = chargeNegation o S hS x then 1 else 0 := by
  classical
  simp [LinearMap.toMatrix_apply, chargeParity_apply, Pi.basisFun_apply,
    Pi.single_apply, eq_comm]

theorem chargeParity_diagonal (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) (x : Charge o S) :
    LinearMap.toMatrix (Pi.basisFun ℂ (Charge o S))
      (Pi.basisFun ℂ (Charge o S)) (chargeParity o S hS) x x =
        if x.val = 0 then 1 else 0 := by
  classical
  rw [chargeParity_matrix]
  have hx : x = chargeNegation o S hS x ↔ x.val = 0 := by
    constructor
    · intro h
      have hv := congrArg Subtype.val h
      exact (negation_fixed_iff_zero o x.val).mp hv.symm
    · intro h
      apply Subtype.ext
      change x.val = -x.val
      simp [h]
  simp only [hx]

/-- Only the zero charge contributes to the reflected charge trace. -/
theorem chargeParity_trace (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) :
    LinearMap.trace ℂ (ChargeSpace o S) (chargeParity o S hS) =
      if (0 : Lattice o) ∈ S then 1 else 0 := by
  classical
  rw [LinearMap.trace_eq_matrix_trace ℂ (Pi.basisFun ℂ (Charge o S))]
  change (∑ x : Charge o S,
    LinearMap.toMatrix (Pi.basisFun ℂ (Charge o S))
      (Pi.basisFun ℂ (Charge o S)) (chargeParity o S hS) x x) = _
  simp_rw [chargeParity_diagonal]
  by_cases hz : (0 : Lattice o) ∈ S
  · rw [if_pos hz]
    let z : Charge o S := ⟨0, hz⟩
    rw [Finset.sum_eq_single z]
    · simp [z]
    · intro x _ hx
      have hne : x.val ≠ 0 := fun h => hx (Subtype.ext h)
      simp [hne]
    · simp
  · rw [if_neg hz]
    apply Finset.sum_eq_zero
    intro x _
    have hne : x.val ≠ 0 := by
      intro h
      exact hz (h ▸ x.property)
    simp [hne]

theorem nonzero_charge_trace_vanishes (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) (hzero : (0 : Lattice o) ∉ S) :
    LinearMap.trace ℂ (ChargeSpace o S) (chargeParity o S hS) = 0 := by
  rw [chargeParity_trace, if_neg hzero]

theorem vacuum_charge_trace (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) (hzero : (0 : Lattice o) ∈ S) :
    LinearMap.trace ℂ (ChargeSpace o S) (chargeParity o S hS) = 1 := by
  rw [chargeParity_trace, if_pos hzero]

/-- The actual subspace of the twisted group algebra spanned by S. -/
def chargeSubspace (o : Fin 12) (S : Finset (Lattice o)) :
    Submodule ℂ (TwistedAlgebra o) := LinearMap.range (chargeEmbedding o S)

def chargeEquiv (o : Fin 12) (S : Finset (Lattice o)) :
    ChargeSpace o S ≃ₗ[ℂ] chargeSubspace o S :=
  LinearEquiv.ofInjective (chargeEmbedding o S) (chargeEmbedding_injective o S)

def chargeBasis (o : Fin 12) (S : Finset (Lattice o)) :
    Basis (Charge o S) ℂ (chargeSubspace o S) :=
  (Pi.basisFun ℂ (Charge o S)).map (chargeEquiv o S)

theorem chargeBasis_coe (o : Fin 12) (S : Finset (Lattice o)) (x : Charge o S) :
    ((chargeBasis o S x : chargeSubspace o S) : TwistedAlgebra o) =
      basisElement o x.val := by
  classical
  change (chargeEmbedding o S) ((Pi.basisFun ℂ (Charge o S)) x) = _
  rw [Pi.basisFun_apply]
  change Fintype.linearCombination ℂ (fun x : Charge o S => basisElement o x.val)
    (Pi.single x 1) = _
  rw [Fintype.linearCombination_apply_single, one_smul]

def chargeRestriction (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) : Module.End ℂ (chargeSubspace o S) :=
  (chargeEquiv o S).conj (chargeParity o S hS)

/-- The conjugated finite model really acts by theta on each vector of the
actual charge subspace. -/
theorem chargeRestriction_coe (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) (f : chargeSubspace o S) :
    ((chargeRestriction o S hS f : chargeSubspace o S) : TwistedAlgebra o) =
      theta o (f : TwistedAlgebra o) := by
  change (chargeEmbedding o S) (chargeParity o S hS ((chargeEquiv o S).symm f)) = _
  rw [← chargeEmbedding_intertwines]
  congr 1
  exact congrArg Subtype.val ((chargeEquiv o S).apply_symm_apply f)

theorem chargeRestriction_trace (o : Fin 12) (S : Finset (Lattice o))
    (hS : ∀ x ∈ S, -x ∈ S) :
    LinearMap.trace ℂ (chargeSubspace o S) (chargeRestriction o S hS) =
      if (0 : Lattice o) ∈ S then 1 else 0 := by
  rw [chargeRestriction, LinearMap.trace_conj', chargeParity_trace]

end HMT.IV.LatticeChargeParityTrace
end

#print axioms HMT.IV.LatticeChargeParityTrace.negation_fixed_iff_zero
#print axioms HMT.IV.LatticeChargeParityTrace.chargeEmbedding_injective
#print axioms HMT.IV.LatticeChargeParityTrace.chargeEmbedding_intertwines
#print axioms HMT.IV.LatticeChargeParityTrace.chargeParity_diagonal
#print axioms HMT.IV.LatticeChargeParityTrace.chargeParity_trace
#print axioms HMT.IV.LatticeChargeParityTrace.nonzero_charge_trace_vanishes
#print axioms HMT.IV.LatticeChargeParityTrace.vacuum_charge_trace
#print axioms HMT.IV.LatticeChargeParityTrace.chargeBasis_coe
#print axioms HMT.IV.LatticeChargeParityTrace.chargeRestriction_coe
#print axioms HMT.IV.LatticeChargeParityTrace.chargeRestriction_trace
