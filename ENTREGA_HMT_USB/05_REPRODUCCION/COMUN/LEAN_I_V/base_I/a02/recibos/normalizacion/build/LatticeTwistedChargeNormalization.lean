import LatticeTwistedPositiveEnergy
import LatticeWeightShells

/-! Reinsert the lattice-dependent power of z and the nonzero scalar in the
charge-even exponential field. Both are read from the norm of the same lattice
vector, not supplied as target values. The resulting grading identity has the
weight halfnormNat of that charge. This is a family of actual Laurent fields;
compatibility with the full descendant correction and mixed products is not
asserted by these definitions. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedChargeNormalization
open LatticeCocycle LatticeWeightShells LatticeTwistedPositiveSector
open LatticeTwistedPositiveKernel LatticeTwistedPositiveEnergy
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeTwistedExponentialKernel LatticeTwistedKernelParity
open LatticeTwistedLowWeights LatticeTwistedCarrier
open LatticeFiniteGroundState LatticeHalfIntegerHeisenberg
open LatticeFockMonomialParity LatticeFiniteIrreducible

def normScalar (o : Fin 12) (x : Lattice o) : ℂ :=
  ((2:ℂ) ^ (2 * halfnormNat o x))⁻¹

theorem normScalar_ne_zero (o : Fin 12) (x : Lattice o) :
    normScalar o x ≠ 0 := inv_ne_zero (pow_ne_zero _ (by norm_num))

theorem normScalar_neg (o : Fin 12) (x : Lattice o) :
    normScalar o (-x) = normScalar o x := by
  simp only [normScalar, halfnormNat_neg]

theorem normScalar_zero (o : Fin 12) : normScalar o 0 = 1 := by
  simp [normScalar]

def chargeCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    Module.End ℂ (positiveSector o) :=
  normScalar o x • positiveCoefficient o x 0 (k + (halfnormNat o x : ℤ))

theorem chargeCoefficient_bounded_pole (o : Fin 12) (x : Lattice o)
    (v : positiveSector o) : ∃ b : ℤ, ∀ k < b, chargeCoefficient o x k v = 0 := by
  obtain ⟨b,hb⟩ := positiveCoefficient_bounded_pole o x 0 v
  refine ⟨b - (halfnormNat o x : ℤ), fun k hk => ?_⟩
  simp only [chargeCoefficient, LinearMap.smul_apply,
    hb (k + (halfnormNat o x : ℤ)) (by omega), smul_zero]

def chargeField (o : Fin 12) (x : Lattice o) :
    VertexOperator ℂ (positiveSector o) :=
  VertexOperator.of_coeff (chargeCoefficient o x)
    (chargeCoefficient_bounded_pole o x)

theorem chargeField_coefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    HVertexOperator.coeff (chargeField o x) k = chargeCoefficient o x k := rfl

theorem chargeCoefficient_conformal_commutator (o : Fin 12)
    (x : Lattice o) (k : ℤ) :
    positiveConformalMode o 0 * chargeCoefficient o x k -
      chargeCoefficient o x k * positiveConformalMode o 0 =
        ((k:ℂ) + (halfnormNat o x : ℂ)) • chargeCoefficient o x k := by
  unfold chargeCoefficient
  rw [mul_smul_comm, smul_mul_assoc]
  rw [← smul_sub (normScalar o x)
    (positiveConformalMode o 0 * positiveCoefficient o x 0 (k + (halfnormNat o x : ℤ)))
    (positiveCoefficient o x 0 (k + (halfnormNat o x : ℤ)) * positiveConformalMode o 0)]
  rw [positiveCoefficient_conformal_commutator]
  push_cast
  exact smul_comm _ _ _

theorem chargeCoefficient_weight_shift (o : Fin 12) (x : Lattice o)
    (k : ℤ) (d : ℂ) (v : positiveSector o)
    (hv : positiveConformalMode o 0 v = d • v) :
    positiveConformalMode o 0 (chargeCoefficient o x k v) =
      (d + (k:ℂ) + (halfnormNat o x : ℂ)) • chargeCoefficient o x k v := by
  have h := LinearMap.congr_fun (chargeCoefficient_conformal_commutator o x k) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply] at h
  rw [hv, map_smul, sub_eq_iff_eq_add] at h
  rw [h]
  module

theorem chargeField_weight_shift (o : Fin 12) (x : Lattice o)
    (k : ℤ) (d : ℂ) (v : positiveSector o)
    (hv : positiveConformalMode o 0 v = d • v) :
    positiveConformalMode o 0 (HVertexOperator.coeff (chargeField o x) k v) =
      (d + (k:ℂ) + (halfnormNat o x : ℂ)) •
        HVertexOperator.coeff (chargeField o x) k v :=
  chargeCoefficient_weight_shift o x k d v hv

theorem chargeField_mode_weight_shift (o : Fin 12) (x : Lattice o)
    (j : ℤ) (d : ℂ) (v : positiveSector o)
    (hv : positiveConformalMode o 0 v = d • v) :
    positiveConformalMode o 0 (HVertexOperator.coeff (chargeField o x) (-j-1) v) =
      (d + (halfnormNat o x : ℂ) - (j:ℂ) - 1) •
        HVertexOperator.coeff (chargeField o x) (-j-1) v := by
  rw [chargeField_weight_shift o x (-j-1) d v hv]
  congr 1
  push_cast
  ring

theorem annihilationPotential_zero_charge (o : Fin 12) :
    annihilationPotential o 0 = 0 := by
  ext r
  simp [annihilationPotential_coefficient, chargeHalfAnnihilation]

theorem annihilationCoefficient_zero_charge (o : Fin 12) (r : ℕ) :
    exponentialCoefficient o 0 r = if r=0 then 1 else 0 := by
  classical
  unfold exponentialCoefficient
  rw [Finset.sum_eq_single 0]
  · simp
  · intro k _ hk
    rw [annihilationPotential_zero_charge, zero_pow hk]
    simp
  · simp

theorem creationMode_zero_charge (o : Fin 12) (r : ℕ) :
    halfCreationExponentialMode o 0 r = if r=0 then 1 else 0 := by
  ext v
  change PowerSeries.coeff (HalfFock o) r (halfCreationExponential o 0) * v = _
  rw [halfCreationExponential_zero_charge, PowerSeries.coeff_one]
  split_ifs <;> simp

theorem basisKernel_zero_charge (o : Fin 12) (s k : ℤ) (p : BasisIndex o) :
    basisKernelCoefficient o 0 s k p.1 p.2 = if k=s then twistedBasis o p else 0 := by
  classical
  unfold basisKernelCoefficient basisKernelCutoff
  rw [Finset.sum_eq_single 0]
  · simp only [Nat.cast_zero, add_zero, annihilationCoefficient_zero_charge,
      if_pos rfl, Module.End.one_apply, latticeOperator_zero]
    by_cases hks : k=s
    · simp [hks, creationMode_zero_charge, twistedBasis, Basis.tensorProduct_apply']
    · rw [if_neg hks]
      by_cases hk : 0 ≤ k-s
      · rw [if_pos hk, creationMode_zero_charge, if_neg (by omega)]
        simp
      · rw [if_neg hk]
  · intro j _ hj
    rw [annihilationCoefficient_zero_charge, if_neg hj]
    simp
  · simp

theorem kernel_zero_charge (o : Fin 12) (s k : ℤ) :
    kernelCoefficient o 0 s k = if k=s then 1 else 0 := by
  apply (twistedBasis o).ext
  intro p
  rw [kernelCoefficient_basis, basisKernel_zero_charge]
  split_ifs <;> rfl

theorem positiveCoefficient_zero_charge (o : Fin 12) (k : ℤ) :
    positiveCoefficient o 0 0 k = if k=0 then 1 else 0 := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  change descendedCoefficient o 0 0 k v.val = _
  rw [descendedCoefficient_eq_kernel, kernel_zero_charge]
  by_cases hk : k=0
  · simp [hk]
  · simp [hk, show 2*k+0 ≠ 0 by omega]

theorem chargeField_zero_charge (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (chargeField o 0) k = if k=0 then 1 else 0 := by
  rw [chargeField_coefficient]
  simp only [chargeCoefficient, normScalar_zero, halfnormNat_zero,
    Nat.cast_zero, add_zero, one_smul]
  exact positiveCoefficient_zero_charge o k

end HMT.IV.LatticeTwistedChargeNormalization
end

#print axioms HMT.IV.LatticeTwistedChargeNormalization.normScalar
#print axioms HMT.IV.LatticeTwistedChargeNormalization.normScalar_ne_zero
#print axioms HMT.IV.LatticeTwistedChargeNormalization.normScalar_neg
#print axioms HMT.IV.LatticeTwistedChargeNormalization.normScalar_zero
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeCoefficient
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeCoefficient_bounded_pole
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeField
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeField_coefficient
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeCoefficient_conformal_commutator
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeCoefficient_weight_shift
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeField_weight_shift
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeField_mode_weight_shift
#print axioms HMT.IV.LatticeTwistedChargeNormalization.annihilationPotential_zero_charge
#print axioms HMT.IV.LatticeTwistedChargeNormalization.annihilationCoefficient_zero_charge
#print axioms HMT.IV.LatticeTwistedChargeNormalization.creationMode_zero_charge
#print axioms HMT.IV.LatticeTwistedChargeNormalization.basisKernel_zero_charge
#print axioms HMT.IV.LatticeTwistedChargeNormalization.kernel_zero_charge
#print axioms HMT.IV.LatticeTwistedChargeNormalization.positiveCoefficient_zero_charge
#print axioms HMT.IV.LatticeTwistedChargeNormalization.chargeField_zero_charge
