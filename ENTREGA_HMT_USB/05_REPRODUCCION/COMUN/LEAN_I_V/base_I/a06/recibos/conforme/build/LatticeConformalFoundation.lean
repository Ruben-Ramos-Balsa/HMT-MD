import LatticeConformalCentralCoefficient
import LatticeConformalEnergy
import LatticeConformalTranslation

/-! The conformal-state identities assembled on the original lattice carrier.
Both distinguished modes, the self-field low coefficients and the three
Möbius commutators are deduced from the concrete normal-product construction.
The full Virasoro commutator and twisted extension are not assumed. -/

noncomputable section
namespace HMT.IV.LatticeConformalFoundation

open LatticeOscillatorFock LatticeCocycle LatticeConformalState
open LatticeConformalCovariance LatticeConformalLowModes
open LatticeConformalCentralCoefficient LatticeConformalEnergy
open LatticeConformalTranslation LatticeEnergyGrading

theorem conformalMode_zero_state (o : Fin 12) :
    conformalMode o 0 (conformalState o) = (2 : ℂ) • conformalState o := by
  rw [conformalMode_zero_eq_energy]
  exact conformalState_weight_two o

theorem conformalMode_minus_one_state (o : Fin 12) :
    conformalMode o (-1) (conformalState o) =
      LatticeTranslationOperator.translation o (conformalState o) := by
  rw [conformalMode_neg_one_eq_translation]

theorem conformalMode_zero_commutator (o : Fin 12) (m : ℤ) :
    conformalMode o 0 * conformalMode o m - conformalMode o m * conformalMode o 0 =
      (-(m : ℂ)) • conformalMode o m := by
  rw [conformalMode_zero_eq_energy]
  exact conformalMode_energy o m

theorem conformalMode_minus_one_commutator (o : Fin 12) (m : ℤ) :
    conformalMode o (-1) * conformalMode o m -
      conformalMode o m * conformalMode o (-1) =
      (-((m : ℂ)+1)) • conformalMode o (m-1) := by
  rw [conformalMode_neg_one_eq_translation]
  exact conformalMode_translation o m

theorem mobius_zero_minus_one (o : Fin 12) :
    conformalMode o 0 * conformalMode o (-1) -
      conformalMode o (-1) * conformalMode o 0 = conformalMode o (-1) := by
  simpa using conformalMode_zero_commutator o (-1)

theorem mobius_zero_one (o : Fin 12) :
    conformalMode o 0 * conformalMode o 1 -
      conformalMode o 1 * conformalMode o 0 = -conformalMode o 1 := by
  rw [conformalMode_zero_commutator]
  apply LinearMap.ext
  intro v
  simp only [LinearMap.smul_apply, LinearMap.neg_apply, Int.cast_one]
  module

theorem mobius_one_minus_one (o : Fin 12) :
    conformalMode o 1 * conformalMode o (-1) -
      conformalMode o (-1) * conformalMode o 1 = (2 : ℂ) • conformalMode o 0 := by
  have h := conformalMode_minus_one_commutator o 1
  simp only [Int.cast_one, show (1 : ℤ)-1=0 by rfl] at h
  have h' := congrArg Neg.neg h
  rw [neg_sub] at h'
  have he : -((-((1 : ℂ)+1)) • conformalMode o 0) = (2 : ℂ) • conformalMode o 0 := by
    apply LinearMap.ext
    intro v
    change -((-((1 : ℂ)+1)) • conformalMode o 0 v) = (2 : ℂ) • conformalMode o 0 v
    module
  exact h'.trans he

/-- These are the actual singular self-field coefficients, including the
rank-dependent central coefficient, not postulated OPE relations. -/
theorem conformal_self_coefficients (o : Fin 12) :
    conformalMode o (-1) (conformalState o) =
        LatticeTranslationOperator.translation o (conformalState o) ∧
    conformalMode o 0 (conformalState o) = (2 : ℂ) • conformalState o ∧
    conformalMode o 1 (conformalState o) = 0 ∧
    conformalMode o 2 (conformalState o) = ((BasisSize o : ℂ)/2) • vacuum o ∧
    ∀ m : ℤ, 2 < m → conformalMode o m (conformalState o) = 0 :=
  ⟨conformalMode_minus_one_state o, conformalMode_zero_state o,
    conformalMode_one_state o, conformalMode_two_state o, conformalMode_above_two_state o⟩

end HMT.IV.LatticeConformalFoundation
end

#print axioms HMT.IV.LatticeConformalFoundation.conformalMode_zero_state
#print axioms HMT.IV.LatticeConformalFoundation.conformalMode_minus_one_state
#print axioms HMT.IV.LatticeConformalFoundation.conformalMode_zero_commutator
#print axioms HMT.IV.LatticeConformalFoundation.conformalMode_minus_one_commutator
#print axioms HMT.IV.LatticeConformalFoundation.mobius_zero_minus_one
#print axioms HMT.IV.LatticeConformalFoundation.mobius_zero_one
#print axioms HMT.IV.LatticeConformalFoundation.mobius_one_minus_one
#print axioms HMT.IV.LatticeConformalFoundation.conformal_self_coefficients
