import LatticeConformalEnergy
import LatticeStateFieldEnergy
import LatticeConformalLowModes

/-! The previously constructed finite weight spaces are the eigenspaces
of the actual conformal zero mode. Field products preserve their predicted
integral weights; negative output weights vanish. -/

noncomputable section
namespace HMT.IV.LatticeConformalGrading

open LatticeOscillatorFock LatticeStateFieldMap LatticeEnergyGrading
open LatticeFullGradedTrace LatticeStateFieldEnergy LatticeConformalLowModes
open LatticeConformalState LatticeConformalEnergy LatticeLowWeightParity

theorem conformal_weight_space (o : Fin 12) (d : ℕ) :
    Module.End.eigenspace (conformalMode o 0) (d : ℂ) = fullWeightSpace o d := by
  rw [conformalMode_zero_eq_energy, fullWeightSpace_eq_eigenspace]

theorem conformal_weight_finite (o : Fin 12) (d : ℕ) :
    FiniteDimensional ℂ (Module.End.eigenspace (conformalMode o 0) (d : ℂ)) := by
  rw [conformal_weight_space]
  infer_instance

theorem conformal_weights_span (o : Fin 12) :
    (⨆ d : ℕ, Module.End.eigenspace (conformalMode o 0) (d : ℂ)) = ⊤ := by
  simp only [conformal_weight_space]
  exact total_weights_span_carrier o

theorem conformal_weight_zero (o : Fin 12) :
    Module.End.eigenspace (conformalMode o 0) 0 =
      Submodule.span ℂ {vacuum o} := by
  rw [conformalMode_zero_eq_energy]
  exact energy_zero_is_vacuum_line o

theorem coefficient_energy (o : Fin 12) (u v : LatticeCarrier o) (d e : ℂ)
    (hu : energy o u = d • u) (hv : energy o v = e • v) (k : ℤ) :
    energy o (HVertexOperator.coeff (stateField o u) k v) =
      (d+e+(k : ℂ)) • HVertexOperator.coeff (stateField o u) k v := by
  have h := LinearMap.congr_fun (stateField_homogeneous_energy o u d hu k) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    hv, map_smul] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h]
  module

theorem coefficient_mem_weight (o : Fin 12) (u v : LatticeCarrier o)
    (d e r : ℕ) (hu : u ∈ fullWeightSpace o d) (hv : v ∈ fullWeightSpace o e)
    (k : ℤ) (hr : (r : ℤ) = d+e+k) :
    HVertexOperator.coeff (stateField o u) k v ∈ fullWeightSpace o r := by
  rw [fullWeightSpace_eq_eigenspace]
  apply Module.End.mem_eigenspace_iff.mpr
  have he := coefficient_energy o u v (d : ℂ) (e : ℂ)
    (energy_on_weight o d ⟨u,hu⟩) (energy_on_weight o e ⟨v,hv⟩) k
  have hc := congrArg (fun z : ℤ => (z : ℂ)) hr
  push_cast at hc
  rw [he, ← hc]

theorem coefficient_negative_weight_zero (o : Fin 12) (u v : LatticeCarrier o)
    (d e : ℕ) (hu : u ∈ fullWeightSpace o d) (hv : v ∈ fullWeightSpace o e)
    (k : ℤ) (hk : (d : ℤ)+e+k < 0) :
    HVertexOperator.coeff (stateField o u) k v = 0 := by
  apply negative_energy_vector_zero o _ ((d : ℤ)+e+k) hk
  have h := coefficient_energy o u v (d : ℂ) (e : ℂ)
    (energy_on_weight o d ⟨u,hu⟩) (energy_on_weight o e ⟨v,hv⟩) k
  simpa only [Int.cast_add, Int.cast_natCast] using h

end HMT.IV.LatticeConformalGrading
end

#print axioms HMT.IV.LatticeConformalGrading.conformal_weight_space
#print axioms HMT.IV.LatticeConformalGrading.conformal_weight_finite
#print axioms HMT.IV.LatticeConformalGrading.conformal_weights_span
#print axioms HMT.IV.LatticeConformalGrading.conformal_weight_zero
#print axioms HMT.IV.LatticeConformalGrading.coefficient_energy
#print axioms HMT.IV.LatticeConformalGrading.coefficient_mem_weight
#print axioms HMT.IV.LatticeConformalGrading.coefficient_negative_weight_zero
