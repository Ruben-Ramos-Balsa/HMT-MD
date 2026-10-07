import LatticeChargedVertexField
import LatticeExponentialEnergy
import LatticeAnnihilationEnergy

/-!
Energy covariance of the actual charged lattice field. Its Laurent index k
denotes the coefficient of z^k, so its energy shift is k plus the charge
half-norm. The proof combines the previously constructed Euler derivation,
the homogeneous creation coefficients, the weight-lowering annihilation
coefficients and the quadratic identity for the same lattice charge.
No Virasoro identification, Jacobi identity or FLM premise is introduced.
-/

noncomputable section
namespace HMT.IV.LatticeChargedFieldEnergy

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeWeightShells HMT.IV.LatticeChargeEnergy
open HMT.IV.LatticeEnergyGrading HMT.IV.LatticeEulerEnergy
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialEnergy HMT.IV.LatticeAnnihilationEnergy
open HMT.IV.LatticeChargedVertexField
open scoped TensorProduct BigOperators

theorem energy_pure (o : Fin 12) (v : Fock o) (y : Lattice o) :
    energy o (v ⊗ₜ[ℂ] basisElement o y) =
      euler o v ⊗ₜ[ℂ] basisElement o y +
        (halfnormNat o y : ℂ) • (v ⊗ₜ[ℂ] basisElement o y) := by
  rw [energy_eq_euler_plus_charge, LinearMap.add_apply,
    onCarrier_pure, onLattice_pure, chargeEnergy_basis, TensorProduct.tmul_smul]
  rfl

theorem creationMode_euler (o : Fin 12) (x : Lattice o) (p : ℕ)
    (v : Fock o) :
    euler o (creationExponentialMode o x p v) =
      creationExponentialMode o x p (euler o v) +
        (p : ℂ) • creationExponentialMode o x p v := by
  change euler o (PowerSeries.coeff (Fock o) p (creationExponential o x) * v) = _
  rw [(euler o).leibniz, creationExponential_coefficient_energy]
  change _ = PowerSeries.coeff (Fock o) p (creationExponential o x) * euler o v +
    (p : ℂ) • (PowerSeries.coeff (Fock o) p (creationExponential o x) * v)
  simp only [smul_eq_mul, Algebra.smul_def, map_mul]
  ring

theorem creation_annihilation_euler (o : Fin 12) (x : Lattice o)
    (p j : ℕ) (a : Occupation o) :
    euler o (creationExponentialMode o x p
      (exponentialCoefficient o x j (monomialBasis o a))) =
      ((occupationWeight o a : ℂ) + (p : ℂ) - (j : ℂ)) •
        creationExponentialMode o x p
          (exponentialCoefficient o x j (monomialBasis o a)) := by
  rw [creationMode_euler, exponentialCoefficient_lowersWeight,
    euler_monomial, map_smul, map_sub, map_smul, map_smul,
    ← sub_smul, ← add_smul]
  congr 1
  ring

theorem charged_term_energy (o : Fin 12) (x y : Lattice o)
    (a : Occupation o) (k : ℤ) (j : ℕ)
    (h : 0 ≤ k-integerPair o x y+(j : ℤ)) :
    energy o (creationExponentialMode o x ((k-integerPair o x y+(j : ℤ)).toNat)
      (exponentialCoefficient o x j (monomialBasis o a)) ⊗ₜ[ℂ]
        basisElement o (x+y)) =
      ((totalWeight o (a,y) : ℂ) + (k : ℂ) + (halfnormNat o x : ℂ)) •
        (creationExponentialMode o x ((k-integerPair o x y+(j : ℤ)).toNat)
          (exponentialCoefficient o x j (monomialBasis o a)) ⊗ₜ[ℂ]
            basisElement o (x+y)) := by
  rw [energy_pure, creation_annihilation_euler]
  simp only [← TensorProduct.smul_tmul']
  rw [← add_smul]
  congr 1
  have hc : (((k-integerPair o x y+(j : ℤ)).toNat : ℕ) : ℂ) =
      (k : ℂ)-(integerPair o x y : ℂ)+(j : ℂ) := by
    have hz := Int.toNat_of_nonneg h
    exact_mod_cast hz
  rw [hc, halfnorm_add_complex]
  simp only [totalWeight, Nat.cast_add]
  ring

theorem basisCoefficient_energy (o : Fin 12) (x y : Lattice o)
    (a : Occupation o) (k : ℤ) :
    energy o (basisCoefficient o x k a y) =
      ((totalWeight o (a,y) : ℂ) + (k : ℂ) + (halfnormNat o x : ℂ)) •
        basisCoefficient o x k a y := by
  unfold basisCoefficient basisCoefficientCutoff
  rw [map_smul, map_sum]
  conv_rhs => rw [smul_comm]
  congr 1
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  split_ifs with h
  · exact charged_term_energy o x y a k j h
  · simp

theorem energy_fieldCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (energy o).comp (fieldCoefficient o x k) -
      (fieldCoefficient o x k).comp (energy o) =
      ((k : ℂ) + (halfnormNat o x : ℂ)) • fieldCoefficient o x k := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  change energy o (fieldCoefficient o x k (carrierBasis o (a,y))) -
    fieldCoefficient o x k (energy o (carrierBasis o (a,y))) =
      ((k : ℂ) + (halfnormNat o x : ℂ)) •
        fieldCoefficient o x k (carrierBasis o (a,y))
  rw [fieldCoefficient_basis, basisCoefficient_energy, energy_basis,
    map_smul, fieldCoefficient_basis, ← sub_smul]
  congr 1
  ring

theorem fieldCoefficient_changes_energy (o : Fin 12) (x : Lattice o)
    (k : ℤ) (d : ℂ) (v : LatticeCarrier o) (hv : energy o v = d • v) :
    energy o (fieldCoefficient o x k v) =
      (d + (k : ℂ) + (halfnormNat o x : ℂ)) • fieldCoefficient o x k v := by
  have h := LinearMap.congr_fun (energy_fieldCoefficient o x k) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply] at h
  rw [hv, map_smul, sub_eq_iff_eq_add] at h
  rw [h, ← add_smul]
  congr 1
  ring

end HMT.IV.LatticeChargedFieldEnergy
end

#print axioms HMT.IV.LatticeChargedFieldEnergy.energy_pure
#print axioms HMT.IV.LatticeChargedFieldEnergy.creationMode_euler
#print axioms HMT.IV.LatticeChargedFieldEnergy.creation_annihilation_euler
#print axioms HMT.IV.LatticeChargedFieldEnergy.charged_term_energy
#print axioms HMT.IV.LatticeChargedFieldEnergy.basisCoefficient_energy
#print axioms HMT.IV.LatticeChargedFieldEnergy.energy_fieldCoefficient
#print axioms HMT.IV.LatticeChargedFieldEnergy.fieldCoefficient_changes_energy
