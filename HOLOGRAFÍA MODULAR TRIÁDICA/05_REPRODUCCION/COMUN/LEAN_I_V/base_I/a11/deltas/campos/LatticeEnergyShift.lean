import LatticeEnergyGrading
import LatticeChargeEnergy

/-!
Compatibility of the generated energy grading with the existing charged
operators. The scalar term is the integral half-norm, and the other term
is the original lattice zero mode; neither is an independently supplied
parameter. These identities hold on the full algebraic carrier.
-/

noncomputable section
namespace HMT.IV.LatticeEnergyShift

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeZeroModes HMT.IV.LatticeWeightShells
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeEnergyGrading HMT.IV.LatticeChargeEnergy

theorem totalWeight_charge_add (o : Fin 12) (a : Occupation o)
    (x y : Lattice o) :
    (totalWeight o (a,x+y) : ℂ) = (totalWeight o (a,y) : ℂ) +
      (halfnormNat o x : ℂ) + (integerPair o x y : ℂ) := by
  simp only [totalWeight, Nat.cast_add, halfnorm_add_complex]
  ring

theorem energy_shift (o : Fin 12) (x : Lattice o) :
    (energy o).comp (onLattice o (latticeShift o x)) -
      (onLattice o (latticeShift o x)).comp (energy o) =
      (onLattice o (latticeShift o x)).comp (onLattice o (zeroMode o x)) +
        (halfnormNat o x : ℂ) • onLattice o (latticeShift o x) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.add_apply,
    LinearMap.smul_apply, carrierShift_basis, energy_basis,
    carrierZeroMode_basis, map_smul, smul_smul, totalWeight_charge_add]
  rw [← sub_smul, ← add_smul]
  congr 1
  ring

theorem energy_commutes_zeroMode (o : Fin 12) (x : Lattice o) :
    (energy o).comp (onLattice o (zeroMode o x)) =
      (onLattice o (zeroMode o x)).comp (energy o) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [LinearMap.comp_apply, carrierZeroMode_basis, energy_basis,
    map_smul, smul_smul]
  rw [mul_comm]

theorem energy_commutes_chargeEnergy (o : Fin 12) :
    (energy o).comp (onLattice o (chargeEnergy o)) =
      (onLattice o (chargeEnergy o)).comp (energy o) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [LinearMap.comp_apply, carrierChargeEnergy_basis, energy_basis,
    map_smul, smul_smul]
  rw [mul_comm]

theorem shifted_joint_eigenvector (o : Fin 12) (x : Lattice o)
    (v : LatticeCarrier o) (d q : ℂ)
    (hd : energy o v = d • v)
    (hq : onLattice o (zeroMode o x) v = q • v) :
    energy o (onLattice o (latticeShift o x) v) =
      (d+q+(halfnormNat o x : ℂ)) • onLattice o (latticeShift o x) v := by
  have h := LinearMap.congr_fun (energy_shift o x) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.add_apply,
    LinearMap.smul_apply, hd, hq, map_smul] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h]
  simp only [add_smul]
  abel

end HMT.IV.LatticeEnergyShift
end

#print axioms HMT.IV.LatticeEnergyShift.totalWeight_charge_add
#print axioms HMT.IV.LatticeEnergyShift.energy_shift
#print axioms HMT.IV.LatticeEnergyShift.energy_commutes_zeroMode
#print axioms HMT.IV.LatticeEnergyShift.energy_commutes_chargeEnergy
#print axioms HMT.IV.LatticeEnergyShift.shifted_joint_eigenvector
