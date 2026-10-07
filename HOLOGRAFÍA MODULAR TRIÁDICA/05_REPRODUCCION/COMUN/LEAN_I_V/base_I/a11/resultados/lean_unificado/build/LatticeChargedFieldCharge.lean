import LatticeChargedVertexField
import LatticeChargeEnergy

/-!
Charge covariance of the constructed lattice fields. The zero modes, lattice
pairing and charged fields are the already constructed operators on the same
carrier. No charge-selection equation is postulated here: it is proved by
the common lattice component of every term of the field coefficient.
-/

noncomputable section
namespace HMT.IV.LatticeChargedFieldCharge

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeZeroModes
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeChargeEnergy
open HMT.IV.LatticeChargedVertexField
open scoped TensorProduct BigOperators

theorem zeroMode_pure (o : Fin 12) (u y : Lattice o) (v : Fock o) :
    onLattice o (zeroMode o u) (v ⊗ₜ[ℂ] basisElement o y) =
      (integerPair o u y : ℂ) • (v ⊗ₜ[ℂ] basisElement o y) := by
  rw [onLattice_pure, zeroMode_basis, TensorProduct.tmul_smul]

theorem basisCoefficient_charge (o : Fin 12) (u x y : Lattice o)
    (a : Occupation o) (k : ℤ) :
    onLattice o (zeroMode o u) (basisCoefficient o x k a y) =
      (integerPair o u (x+y) : ℂ) • basisCoefficient o x k a y := by
  unfold basisCoefficient basisCoefficientCutoff
  rw [map_smul, map_sum]
  conv_rhs => rw [smul_comm]
  congr 1
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  split_ifs
  · exact zeroMode_pure o u (x+y) _
  · simp

theorem zeroMode_fieldCoefficient (o : Fin 12) (u x : Lattice o) (k : ℤ) :
    (onLattice o (zeroMode o u)).comp (fieldCoefficient o x k) -
      (fieldCoefficient o x k).comp (onLattice o (zeroMode o u)) =
      (integerPair o u x : ℂ) • fieldCoefficient o x k := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  change onLattice o (zeroMode o u) (fieldCoefficient o x k (carrierBasis o (a,y))) -
    fieldCoefficient o x k (onLattice o (zeroMode o u) (carrierBasis o (a,y))) =
      (integerPair o u x : ℂ) • fieldCoefficient o x k (carrierBasis o (a,y))
  rw [fieldCoefficient_basis, basisCoefficient_charge, carrierZeroMode_basis,
    map_smul, fieldCoefficient_basis, ← sub_smul]
  rw [integerPair_add_right, Int.cast_add]
  congr 1
  ring

theorem fieldCoefficient_changes_charge (o : Fin 12) (u x : Lattice o)
    (k : ℤ) (c : ℂ) (v : LatticeCarrier o)
    (hv : onLattice o (zeroMode o u) v = c • v) :
    onLattice o (zeroMode o u) (fieldCoefficient o x k v) =
      (c + (integerPair o u x : ℂ)) • fieldCoefficient o x k v := by
  have h := LinearMap.congr_fun (zeroMode_fieldCoefficient o u x k) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply] at h
  rw [hv, map_smul, sub_eq_iff_eq_add] at h
  rw [h, ← add_smul, add_comm]

end HMT.IV.LatticeChargedFieldCharge
end

#print axioms HMT.IV.LatticeChargedFieldCharge.zeroMode_pure
#print axioms HMT.IV.LatticeChargedFieldCharge.basisCoefficient_charge
#print axioms HMT.IV.LatticeChargedFieldCharge.zeroMode_fieldCoefficient
#print axioms HMT.IV.LatticeChargedFieldCharge.fieldCoefficient_changes_charge
