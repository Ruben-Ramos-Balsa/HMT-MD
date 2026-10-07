import LatticeFullGradedTrace
import Mathlib.LinearAlgebra.Eigenspace.Basic

/-!
The algebraic total-energy operator on the same generated lattice carrier.
It counts positive oscillator frequency and the proved integral half norm
of the charge. Its eigenspaces are exactly the finite total-weight spaces
already used for the reflected character. This is an energy grading, not
an assertion of a conformal vector or the Virasoro relations.
-/

noncomputable section
namespace HMT.IV.LatticeEnergyGrading

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeCocycle HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeWeightShells HMT.IV.LatticeFullGradedTrace

def totalWeight (o : Fin 12) (p : Occupation o × Lattice o) : ℕ :=
  occupationWeight o p.1 + halfnormNat o p.2

def energy (o : Fin 12) : Module.End ℂ (LatticeCarrier o) :=
  (carrierBasis o).constr ℂ fun p =>
    (totalWeight o p : ℂ) • carrierBasis o p

@[simp] theorem energy_basis (o : Fin 12) (p : Occupation o × Lattice o) :
    energy o (carrierBasis o p) = (totalWeight o p : ℂ) • carrierBasis o p :=
  Basis.constr_basis _ _ _ _

@[simp] theorem totalWeight_reflect (o : Fin 12) (a : Occupation o) (x : Lattice o) :
    totalWeight o (a, -x) = totalWeight o (a, x) := by
  simp only [totalWeight, halfnormNat_neg]

@[simp] theorem totalWeight_empty (o : Fin 12) : totalWeight o (0, 0) = 0 := by
  simp [totalWeight, occupationWeight]

theorem energy_vacuum (o : Fin 12) : energy o (vacuum o) = 0 := by
  rw [← vacuum_is_empty_monomial, energy_basis, totalWeight_empty]
  simp

theorem energy_commutes_carrierTheta (o : Fin 12) :
    (energy o).comp (carrierTheta o) = (carrierTheta o).comp (energy o) := by
  apply (carrierBasis o).ext
  rintro ⟨a, x⟩
  simp only [LinearMap.comp_apply, carrierTheta_basis, energy_basis,
    map_smul, totalWeight_reflect, smul_smul]
  rw [mul_comm]

theorem energy_coefficient (o : Fin 12) (v : LatticeCarrier o)
    (p : Occupation o × Lattice o) :
    (carrierBasis o).repr (energy o v) p =
      (totalWeight o p : ℂ) * (carrierBasis o).repr v p := by
  classical
  have h : ((carrierBasis o).coord p).comp (energy o) =
      (totalWeight o p : ℂ) • (carrierBasis o).coord p := by
    apply (carrierBasis o).ext
    intro q
    simp only [LinearMap.comp_apply, energy_basis, map_smul,
      LinearMap.smul_apply, Basis.coord_apply, Basis.repr_self,
      Finsupp.single_apply, smul_eq_mul]
    split_ifs with hq
    · subst q
      rfl
    · simp
  exact LinearMap.congr_fun h v

theorem fullWeightSpace_le_eigenspace (o : Fin 12) (d : ℕ) :
    fullWeightSpace o d ≤ Module.End.eigenspace (energy o) (d : ℂ) := by
  apply Submodule.span_le.mpr
  rintro _ ⟨a, rfl⟩
  apply Module.End.mem_eigenspace_iff.mpr
  rw [energy_basis]
  have h : totalWeight o a.val = d := a.property
  rw [h]

theorem eigenspace_le_fullWeightSpace (o : Fin 12) (d : ℕ) :
    Module.End.eigenspace (energy o) (d : ℂ) ≤ fullWeightSpace o d := by
  classical
  intro v hv
  have hv' := Module.End.mem_eigenspace_iff.mp hv
  rw [← (carrierBasis o).linearCombination_repr v,
    Finsupp.linearCombination_apply, Finsupp.sum]
  apply Submodule.sum_mem
  intro p hp
  apply Submodule.smul_mem
  apply Submodule.subset_span
  have hn : (carrierBasis o).repr v p ≠ 0 := Finsupp.mem_support_iff.mp hp
  have h := congrArg (fun w => (carrierBasis o).repr w p) hv'
  dsimp only at h
  rw [energy_coefficient] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have hw : (totalWeight o p : ℂ) = (d : ℂ) := mul_right_cancel₀ hn h
  have hw' : totalWeight o p = d := by exact_mod_cast hw
  exact ⟨⟨p, hw'⟩, rfl⟩

theorem fullWeightSpace_eq_eigenspace (o : Fin 12) (d : ℕ) :
    fullWeightSpace o d = Module.End.eigenspace (energy o) (d : ℂ) :=
  le_antisymm (fullWeightSpace_le_eigenspace o d) (eigenspace_le_fullWeightSpace o d)

theorem energy_on_weight (o : Fin 12) (d : ℕ) (v : fullWeightSpace o d) :
    energy o (v : LatticeCarrier o) = (d : ℂ) • (v : LatticeCarrier o) := by
  apply Module.End.mem_eigenspace_iff.mp
  rw [← fullWeightSpace_eq_eigenspace]
  exact v.property

end HMT.IV.LatticeEnergyGrading
end

#print axioms HMT.IV.LatticeEnergyGrading.energy_basis
#print axioms HMT.IV.LatticeEnergyGrading.energy_vacuum
#print axioms HMT.IV.LatticeEnergyGrading.energy_commutes_carrierTheta
#print axioms HMT.IV.LatticeEnergyGrading.energy_coefficient
#print axioms HMT.IV.LatticeEnergyGrading.fullWeightSpace_eq_eigenspace
#print axioms HMT.IV.LatticeEnergyGrading.energy_on_weight
