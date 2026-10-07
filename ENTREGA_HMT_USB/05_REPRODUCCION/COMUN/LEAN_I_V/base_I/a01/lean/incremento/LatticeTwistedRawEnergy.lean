import LatticeTwistedNormalEnergy
import LatticeTwistedRawStateField
import LatticeEnergyModes

/-! Energy covariance of the actual raw state field. The charge norm and
oscillator occupation are the existing source grading; all normal sums are
locally finite. No covariance hypothesis is supplied for this assignment. -/
noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedRawEnergy
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeWeightShells LatticeEnergyGrading LatticeModeWeights
open LatticeOscillatorWords LatticeTwistedCarrier LatticeTwistedRawStateField
open LatticeTwistedRawChargeField LatticeTwistedNormalEnergy
open LatticeTwistedKernelEnergy LatticeTwistedExponentialKernel

theorem rawChargeField_energy (o : Fin 12) (x : Lattice o)
    (k : ℤ) (v : Carrier o) :
    conformalMode o 0 (HVertexOperator.coeff (rawChargeField o x) k v) =
      HVertexOperator.coeff (rawChargeField o x) k (conformalMode o 0 v) +
        ((halfnormNat o x:ℂ)+(k:ℂ)/2) •
          HVertexOperator.coeff (rawChargeField o x) k v := by
  have h := LinearMap.congr_fun
    (kernelCoefficient_conformal_commutator o x 0 (k+integerPair o x x)) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    sub_zero] at h
  rw [integerPair_eq_two_halfnorm] at h
  push_cast at h
  rw [sub_eq_iff_eq_add] at h
  simp only [rawChargeField_coefficient, rawChargeCoefficient,
    LinearMap.smul_apply, map_smul, integerPair_eq_two_halfnorm, h]
  module

theorem rawDescendantField_energy (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) (k : ℤ) (v : Carrier o) :
    conformalMode o 0 (HVertexOperator.coeff (rawDescendantField o x w) k v) =
      HVertexOperator.coeff (rawDescendantField o x w) k (conformalMode o 0 v) +
        ((totalWeight o (wordOccupation o w,x):ℂ)+(k:ℂ)/2) •
          HVertexOperator.coeff (rawDescendantField o x w) k v := by
  induction w generalizing k v with
  | nil =>
    simpa only [rawDescendantField_nil, wordOccupation, totalWeight,
      occupationWeight, Finsupp.sum_zero_index, zero_add]
      using rawChargeField_energy o x k v
  | cons m w ih =>
    have hw : totalWeight o (wordOccupation o (m::w),x) =
        totalWeight o (wordOccupation o w,x) + (m.1+1) := by
      simp only [totalWeight, wordOccupation, occupationWeight_add,
        occupationWeight_single, mul_one]
      omega
    rw [rawDescendantField_cons, hw]
    simpa only [Nat.cast_add, Nat.cast_one, add_assoc] using
      derivativeNormalField_energy o m.2 m.1 (rawDescendantField o x w)
        (totalWeight o (wordOccupation o w,x):ℂ) ih k v

theorem rawStateField_energy_apply (o : Fin 12) (u : LatticeCarrier o)
    (k : ℤ) (v : Carrier o) :
    conformalMode o 0 (HVertexOperator.coeff (rawStateField o u) k v) =
      HVertexOperator.coeff (rawStateField o u) k (conformalMode o 0 v) +
      HVertexOperator.coeff (rawStateField o (energy o u)) k v +
      ((k:ℂ)/2) • HVertexOperator.coeff (rawStateField o u) k v := by
  let L : LatticeCarrier o →ₗ[ℂ] Carrier o :=
    { toFun := fun z => conformalMode o 0 (HVertexOperator.coeff (rawStateField o z) k v)
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          LinearMap.smul_apply, RingHom.id_apply] }
  let R : LatticeCarrier o →ₗ[ℂ] Carrier o :=
    { toFun := fun z =>
        HVertexOperator.coeff (rawStateField o z) k (conformalMode o 0 v) +
        HVertexOperator.coeff (rawStateField o (energy o z)) k v +
        ((k:ℂ)/2) • HVertexOperator.coeff (rawStateField o z) k v
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply,
          smul_add]
        abel
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          LinearMap.smul_apply, RingHom.id_apply]
        module }
  have hLR : L = R := by
    apply (carrierBasis o).ext
    rintro ⟨a,x⟩
    change conformalMode o 0
      (HVertexOperator.coeff (rawStateField o (carrierBasis o (a,x))) k v) = _
    dsimp only [R, LinearMap.coe_mk, AddHom.coe_mk]
    rw [energy_basis, map_smul, rawStateField_basis]
    simp only [HVertexOperator.coeff_smul, Pi.smul_apply, LinearMap.smul_apply]
    have h := rawDescendantField_energy o x (wordForOccupation o a) k v
    rw [wordForOccupation_counts] at h
    rw [h]
    module
  exact LinearMap.congr_fun hLR u

theorem rawStateField_energy (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    conformalMode o 0 * HVertexOperator.coeff (rawStateField o u) k -
      HVertexOperator.coeff (rawStateField o u) k * conformalMode o 0 =
      HVertexOperator.coeff (rawStateField o (energy o u)) k +
        ((k:ℂ)/2) • HVertexOperator.coeff (rawStateField o u) k := by
  apply LinearMap.ext
  intro v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.add_apply,
    LinearMap.smul_apply, rawStateField_energy_apply]
  abel

end HMT.IV.LatticeTwistedRawEnergy
end
