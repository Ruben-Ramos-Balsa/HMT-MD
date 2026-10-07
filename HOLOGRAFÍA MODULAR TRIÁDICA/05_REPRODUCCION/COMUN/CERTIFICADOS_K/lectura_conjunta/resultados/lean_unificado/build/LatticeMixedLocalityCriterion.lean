import LatticeFactorConvolution

/-! Coefficientwise conversion of an integer-mode commutator to first-order
mixed locality. This is an algebraic lemma; its premise must be discharged
by the already constructed modes, not assumed as a field axiom. -/
noncomputable section
namespace HMT.IV.LatticeMixedLocalityCriterion
open HMT.IV.LatticeFactorConvolution
variable {V : Type*} [AddCommGroup V] [Module ℂ V]

def mixedForward (H Y : ℤ → Module.End ℂ V) : BiStates (Module.End ℂ V) :=
  fun a b => H (-a-1) * Y b

def mixedBackward (H Y : ℤ → Module.End ℂ V) : BiStates (Module.End ℂ V) :=
  fun a b => Y b * H (-a-1)

theorem mixed_locality_of_mode_relation (H Y : ℤ → Module.End ℂ V) (c : ℂ)
    (hc : ∀ m k, H m * Y k - Y k * H m = c • Y (k-m)) :
    crossing (mixedForward H Y) = crossing (mixedBackward H Y) := by
  funext a b
  change H (-(a-1)-1) * Y b - H (-a-1) * Y (b-1) =
    Y b * H (-(a-1)-1) - Y (b-1) * H (-a-1)
  have h₁ := hc (-(a-1)-1) b
  have h₂ := hc (-a-1) (b-1)
  have he : b-(-(a-1)-1)=(b-1)-(-a-1) := by omega
  rw [he] at h₁
  have hz : (H (-(a-1)-1) * Y b - Y b * H (-(a-1)-1)) -
      (H (-a-1) * Y (b-1) - Y (b-1) * H (-a-1)) = 0 := by
    rw [h₁,h₂,sub_self]
  apply sub_eq_zero.mp
  convert hz using 1
  abel

end HMT.IV.LatticeMixedLocalityCriterion
end
#print axioms HMT.IV.LatticeMixedLocalityCriterion.mixed_locality_of_mode_relation
