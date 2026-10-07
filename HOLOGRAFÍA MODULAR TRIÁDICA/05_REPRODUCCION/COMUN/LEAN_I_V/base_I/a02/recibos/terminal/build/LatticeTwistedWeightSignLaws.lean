import LatticeTwistedContragredientTruncation

/-! Weightwise consequences on the existing positive twisted sector.
The sign action used in the hypotheses is constructed separately from the
actual eigenspace decomposition; it is not a new axiom about the sector. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedWeightSignLaws
open LatticeTwistedPositiveSector LatticeTwistedPositiveGrading
open LatticeTwistedContragredientTruncation

theorem positive_weight_ext (o : Fin 12)
    (f g : Module.End ℂ (positiveSector o))
    (h : ∀ d v, v ∈ positiveWeightSpace o d → f v = g v) : f = g := by
  apply LinearMap.ext
  intro v
  have hv : v ∈ ⨆ d : ℕ, positiveWeightSpace o d := by
    rw [positive_weights_span o]
    trivial
  refine Submodule.iSup_induction (positiveWeightSpace o)
    (motive := fun x => f x = g x) hv h ?_ ?_
  · simp
  · intro x y hx hy
    simp only [map_add, hx, hy]

theorem sign_anticommutes_lowering (o : Fin 12)
    (S : Module.End ℂ (positiveSector o))
    (hS : ∀ d v, v ∈ positiveWeightSpace o d → S v = (-1 : ℂ)^d • v) :
    S * lowering o = -(lowering o * S) := by
  apply positive_weight_ext o
  intro d v hv
  cases d with
  | zero =>
    have hz : v = 0 := by
      simpa only [positive_weight_zero, Submodule.mem_bot] using hv
    subst v
    simp
  | succ d =>
    have hl : lowering o v ∈ positiveWeightSpace o d := by
      apply Module.End.mem_eigenspace_iff.mpr
      have hw := lowering_weight o v ((d+1 : ℕ) : ℂ)
        (Module.End.mem_eigenspace_iff.mp hv)
      simpa only [Nat.cast_add, Nat.cast_one, add_sub_cancel_right] using hw
    simp only [Module.End.mul_apply, LinearMap.neg_apply, hS d _ hl,
      hS (d+1) v hv, map_smul]
    simp only [pow_succ, mul_neg_one]
    module

theorem sign_commutes_energy (o : Fin 12)
    (S : Module.End ℂ (positiveSector o))
    (hS : ∀ d v, v ∈ positiveWeightSpace o d → S v = (-1 : ℂ)^d • v) :
    S * positiveConformalMode o 0 = positiveConformalMode o 0 * S := by
  apply positive_weight_ext o
  intro d v hv
  have he := Module.End.mem_eigenspace_iff.mp hv
  simp only [Module.End.mul_apply, he, map_smul, hS d v hv]
  module

theorem sign_square (o : Fin 12)
    (S : Module.End ℂ (positiveSector o))
    (hS : ∀ d v, v ∈ positiveWeightSpace o d → S v = (-1 : ℂ)^d • v) :
    S * S = 1 := by
  apply positive_weight_ext o
  intro d v hv
  simp only [Module.End.mul_apply, hS d v hv, map_smul, smul_smul,
    Module.End.one_apply]
  rw [← mul_pow]
  simp

theorem sign_lowering_power (o : Fin 12)
    (S : Module.End ℂ (positiveSector o))
    (hS : ∀ d v, v ∈ positiveWeightSpace o d → S v = (-1 : ℂ)^d • v)
    (n : ℕ) : S * (lowering o)^n = (-1 : ℂ)^n • ((lowering o)^n * S) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ, ← mul_assoc, ih, smul_mul_assoc, mul_assoc,
      sign_anticommutes_lowering o S hS]
    apply LinearMap.ext
    intro v
    simp only [Module.End.mul_apply, LinearMap.smul_apply, LinearMap.neg_apply,
      map_neg, map_smul, pow_succ, mul_neg_one]
    module

end HMT.IV.LatticeTwistedWeightSignLaws
end
