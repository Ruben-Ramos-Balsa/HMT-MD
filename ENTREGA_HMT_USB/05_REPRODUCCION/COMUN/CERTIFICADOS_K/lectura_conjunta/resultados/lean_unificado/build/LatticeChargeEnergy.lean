import LatticeWeightShells
import LatticeFockMonomialParity
import WittLatticeZeroModes

/-!
The charge contribution to energy on the generated lattice carrier.
The half-norm and the zero-mode pairing are read from the same integral
marked lattice. Translation of charge is the existing twisted-algebra
left multiplication, not a replacement operator chosen to fit a spectrum.
-/

noncomputable section
namespace HMT.IV.LatticeChargeEnergy

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeZeroModes HMT.IV.LatticeWeightShells
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open scoped TensorProduct

theorem halfnorm_add (o : Fin 12) (x y : Lattice o) :
    (halfnormNat o (x+y) : ℤ) =
      halfnormNat o x + halfnormNat o y + integerPair o x y := by
  have h := integerPair_eq_two_halfnorm o (x+y)
  rw [integerPair_add_left, integerPair_add_right,
    integerPair_add_right, integerPair_comm o y x,
    integerPair_eq_two_halfnorm o x, integerPair_eq_two_halfnorm o y] at h
  omega

theorem halfnorm_add_complex (o : Fin 12) (x y : Lattice o) :
    (halfnormNat o (x+y) : ℂ) =
      halfnormNat o x + halfnormNat o y + (integerPair o x y : ℂ) := by
  exact_mod_cast halfnorm_add o x y

def chargeEnergy (o : Fin 12) : Module.End ℂ (TwistedAlgebra o) :=
  (latticeBasisComplex o).constr ℂ fun x =>
    (halfnormNat o x : ℂ) • basisElement o x

@[simp] theorem chargeEnergy_basis (o : Fin 12) (x : Lattice o) :
    chargeEnergy o (basisElement o x) =
      (halfnormNat o x : ℂ) • basisElement o x := by
  exact Basis.constr_basis (latticeBasisComplex o) ℂ _ x

theorem chargeEnergy_shift (o : Fin 12) (x : Lattice o) :
    (chargeEnergy o).comp (latticeShift o x) -
      (latticeShift o x).comp (chargeEnergy o) =
      (latticeShift o x).comp (zeroMode o x) +
        (halfnormNat o x : ℂ) • latticeShift o x := by
  apply (latticeBasisComplex o).ext
  intro y
  change chargeEnergy o (latticeShift o x (basisElement o y)) -
      latticeShift o x (chargeEnergy o (basisElement o y)) =
    latticeShift o x (zeroMode o x (basisElement o y)) +
      (halfnormNat o x : ℂ) • latticeShift o x (basisElement o y)
  simp only [latticeShift_basis, map_smul, chargeEnergy_basis,
    zeroMode_basis, smul_smul, halfnorm_add_complex]
  rw [← sub_smul, ← add_smul]
  congr 1
  ring

theorem chargeEnergy_zeroMode (o : Fin 12) (x : Lattice o) :
    (chargeEnergy o).comp (zeroMode o x) =
      (zeroMode o x).comp (chargeEnergy o) := by
  apply (latticeBasisComplex o).ext
  intro y
  change chargeEnergy o (zeroMode o x (basisElement o y)) =
    zeroMode o x (chargeEnergy o (basisElement o y))
  simp only [zeroMode_basis, chargeEnergy_basis, map_smul, smul_smul]
  rw [mul_comm]

theorem carrierShift_basis (o : Fin 12) (x y : Lattice o)
    (a : Occupation o) :
    onLattice o (latticeShift o x) (carrierBasis o (a,y)) =
      epsilon o x y • carrierBasis o (a,x+y) := by
  simp only [carrierBasis, Basis.tensorProduct_apply, onLattice_pure]
  change monomialBasis o a ⊗ₜ[ℂ] latticeShift o x (basisElement o y) = _
  rw [latticeShift_basis, TensorProduct.tmul_smul]
  rfl

theorem carrierZeroMode_basis (o : Fin 12) (x y : Lattice o)
    (a : Occupation o) :
    onLattice o (zeroMode o x) (carrierBasis o (a,y)) =
      (integerPair o x y : ℂ) • carrierBasis o (a,y) := by
  simp only [carrierBasis, Basis.tensorProduct_apply, onLattice_pure]
  change monomialBasis o a ⊗ₜ[ℂ] zeroMode o x (basisElement o y) = _
  rw [zeroMode_basis, TensorProduct.tmul_smul]
  rfl

theorem carrierChargeEnergy_basis (o : Fin 12) (y : Lattice o)
    (a : Occupation o) :
    onLattice o (chargeEnergy o) (carrierBasis o (a,y)) =
      (halfnormNat o y : ℂ) • carrierBasis o (a,y) := by
  simp only [carrierBasis, Basis.tensorProduct_apply, onLattice_pure]
  change monomialBasis o a ⊗ₜ[ℂ] chargeEnergy o (basisElement o y) = _
  rw [chargeEnergy_basis, TensorProduct.tmul_smul]
  rfl

theorem carrierChargeEnergy_shift (o : Fin 12) (x : Lattice o) :
    (onLattice o (chargeEnergy o)).comp (onLattice o (latticeShift o x)) -
      (onLattice o (latticeShift o x)).comp (onLattice o (chargeEnergy o)) =
      (onLattice o (latticeShift o x)).comp (onLattice o (zeroMode o x)) +
        (halfnormNat o x : ℂ) • onLattice o (latticeShift o x) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.add_apply,
    LinearMap.smul_apply, carrierShift_basis, carrierChargeEnergy_basis,
    carrierZeroMode_basis, map_smul, smul_smul, halfnorm_add_complex]
  rw [← sub_smul, ← add_smul]
  congr 1
  ring

end HMT.IV.LatticeChargeEnergy
end

#print axioms HMT.IV.LatticeChargeEnergy.halfnorm_add
#print axioms HMT.IV.LatticeChargeEnergy.chargeEnergy_shift
#print axioms HMT.IV.LatticeChargeEnergy.chargeEnergy_zeroMode
#print axioms HMT.IV.LatticeChargeEnergy.carrierShift_basis
#print axioms HMT.IV.LatticeChargeEnergy.carrierZeroMode_basis
#print axioms HMT.IV.LatticeChargeEnergy.carrierChargeEnergy_basis
#print axioms HMT.IV.LatticeChargeEnergy.carrierChargeEnergy_shift
