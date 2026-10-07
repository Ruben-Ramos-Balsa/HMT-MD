import LatticeConformalCovariance
import LatticeEvenTranslation
import LatticeLowWeightParity

/-! Low conformal modes from the already proved energy spectrum and parity.
The central coefficient is confined to the actual vacuum line here; its
numerical evaluation and the Virasoro relation are not assumptions. -/

noncomputable section
namespace HMT.IV.LatticeConformalLowModes

open LatticeOscillatorFock LatticeEnergyGrading LatticeFockMonomialParity
open LatticeConformalState LatticeConformalCovariance LatticeEvenTranslation
open LatticeEvenVertexFields LatticeLowWeightParity

theorem negative_energy_vector_zero (o : Fin 12) (u : LatticeCarrier o)
    (d : ℤ) (hd : d < 0) (hu : energy o u = (d : ℂ) • u) : u = 0 := by
  apply (carrierBasis o).repr.injective
  ext p
  change (carrierBasis o).repr u p = 0
  by_contra hn
  have h := congrArg (fun v => (carrierBasis o).repr v p) hu
  simp only [energy_coefficient, map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have he : (totalWeight o p : ℂ) = (d : ℂ) := mul_right_cancel₀ hn h
  have he' : (totalWeight o p : ℤ) = d := by exact_mod_cast he
  have hp : (0 : ℤ) ≤ totalWeight o p := Int.natCast_nonneg _
  omega

theorem conformalMode_above_weight_zero (o : Fin 12) (u : LatticeCarrier o)
    (d : ℕ) (hu : energy o u = (d : ℂ) • u) (m : ℤ) (hm : (d : ℤ) < m) :
    conformalMode o m u = 0 := by
  apply negative_energy_vector_zero o _ ((d : ℤ)-m) (by omega)
  simpa only [Int.cast_sub, Int.cast_natCast] using
    conformalMode_changes_energy o m u (d : ℂ) hu

theorem conformalMode_above_two_state (o : Fin 12) (m : ℤ) (hm : 2 < m) :
    conformalMode o m (conformalState o) = 0 :=
  conformalMode_above_weight_zero o _ 2 (conformalState_weight_two o) m hm

theorem conformalMode_one_state (o : Fin 12) :
    conformalMode o 1 (conformalState o) = 0 := by
  apply fixed_weight_one_eq_zero
  · rw [fullWeightSpace_eq_eigenspace]
    apply Module.End.mem_eigenspace_iff.mpr
    simpa only [Int.cast_one, show (2 : ℂ)-1=1 by norm_num, one_smul, Nat.cast_one] using
      conformalMode_changes_energy o 1 (conformalState o) 2 (conformalState_weight_two o)
  · exact (mem_evenSpace o _).1
      (conformalMode_mem_even o 1 _ (conformalState_mem_even o))

theorem conformalMode_two_state_vacuum_line (o : Fin 12) :
    conformalMode o 2 (conformalState o) ∈ Submodule.span ℂ {vacuum o} := by
  rw [← energy_zero_is_vacuum_line]
  apply Module.End.mem_eigenspace_iff.mpr
  simpa only [Int.cast_ofNat, sub_self, zero_smul] using
    conformalMode_changes_energy o 2 (conformalState o) 2 (conformalState_weight_two o)

end HMT.IV.LatticeConformalLowModes
end

#print axioms HMT.IV.LatticeConformalLowModes.negative_energy_vector_zero
#print axioms HMT.IV.LatticeConformalLowModes.conformalMode_above_weight_zero
#print axioms HMT.IV.LatticeConformalLowModes.conformalMode_above_two_state
#print axioms HMT.IV.LatticeConformalLowModes.conformalMode_one_state
#print axioms HMT.IV.LatticeConformalLowModes.conformalMode_two_state_vacuum_line
