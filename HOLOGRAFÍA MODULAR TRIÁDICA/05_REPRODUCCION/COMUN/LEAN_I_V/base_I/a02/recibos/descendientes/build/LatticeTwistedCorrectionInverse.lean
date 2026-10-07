import LatticeTwistedCorrectionPreservation
import FiniteExponentialProduct

/-! Two-sided formal inverse of the actual descendant-correction exponential.
The coefficient algebra is the endomorphism algebra of the inherited lattice
carrier. The factorial series used here is the one in the correction owner;
neither commutation nor an exponential inverse is assumed as additional data. -/

noncomputable section
namespace HMT.IV.LatticeTwistedCorrectionInverse
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeTwistedCorrection LatticeTwistedCorrectionPreservation
open LatticeEnergyGrading LatticeEnergyModes
open LatticeParityCarrier LatticeEvenVertexFields
open HMT.Formal.FiniteExponentialProduct
open PowerSeries
open scoped BigOperators

theorem expCoeff_fin_zero {A : Type*} [Ring A] [Algebra ℂ A] (n : ℕ) :
    expCoeff_fin (0 : PowerSeries A) n = coeff A n 1 := by
  rw [expCoeff_fin, Finset.sum_eq_single 0]
  · simp
  · intro k _ hk
    simp [zero_pow hk]
  · simp

theorem correctionSeries_constant (o : Fin 12) :
    constantCoeff (Module.End ℂ (LatticeCarrier o)) (correctionSeries o) = 0 := by
  exact correctionCoefficient_zero o

def correctionExponential (o : Fin 12) :
    PowerSeries (Module.End ℂ (LatticeCarrier o)) :=
  mk (correctionExponentialCoefficient o)

def inverseCorrectionCoefficient (o : Fin 12) (d : ℕ) :
    Module.End ℂ (LatticeCarrier o) :=
  expCoeff_fin (-correctionSeries o) d

def inverseCorrectionExponential (o : Fin 12) :
    PowerSeries (Module.End ℂ (LatticeCarrier o)) :=
  mk (inverseCorrectionCoefficient o)

theorem correctionExponential_coefficient (o : Fin 12) (d : ℕ) :
    coeff (Module.End ℂ (LatticeCarrier o)) d (correctionExponential o) =
      correctionExponentialCoefficient o d := coeff_mk _ _

theorem inverseCorrectionExponential_coefficient (o : Fin 12) (d : ℕ) :
    coeff (Module.End ℂ (LatticeCarrier o)) d (inverseCorrectionExponential o) =
      inverseCorrectionCoefficient o d := coeff_mk _ _

theorem correctionExponential_mul_inverse (o : Fin 12) :
    correctionExponential o * inverseCorrectionExponential o = 1 := by
  apply PowerSeries.ext
  intro d
  have h := expCoeff_fin_add_eq_coeff_mul (correctionSeries o) (-correctionSeries o)
    (correctionSeries_constant o) (by simp [correctionSeries_constant])
    (Commute.refl (correctionSeries o)).neg_right d
  rw [add_neg_cancel, expCoeff_fin_zero] at h
  exact h.symm

theorem inverseCorrectionExponential_mul (o : Fin 12) :
    inverseCorrectionExponential o * correctionExponential o = 1 := by
  apply PowerSeries.ext
  intro d
  have h := expCoeff_fin_add_eq_coeff_mul (-correctionSeries o) (correctionSeries o)
    (by simp [correctionSeries_constant]) (correctionSeries_constant o)
    (Commute.refl (correctionSeries o)).neg_left d
  rw [neg_add_cancel, expCoeff_fin_zero] at h
  exact h.symm

theorem correction_inverse_convolution (o : Fin 12) (d : ℕ) :
    ∑ p ∈ Finset.antidiagonal d,
      correctionExponentialCoefficient o p.1 * inverseCorrectionCoefficient o p.2 =
        if d = 0 then 1 else 0 := by
  have h := congrArg (coeff (Module.End ℂ (LatticeCarrier o)) d)
    (correctionExponential_mul_inverse o)
  simpa only [coeff_mul, correctionExponential_coefficient,
    inverseCorrectionExponential_coefficient, coeff_one] using h

theorem inverse_correction_convolution (o : Fin 12) (d : ℕ) :
    ∑ p ∈ Finset.antidiagonal d,
      inverseCorrectionCoefficient o p.1 * correctionExponentialCoefficient o p.2 =
        if d = 0 then 1 else 0 := by
  have h := congrArg (coeff (Module.End ℂ (LatticeCarrier o)) d)
    (inverseCorrectionExponential_mul o)
  simpa only [coeff_mul, correctionExponential_coefficient,
    inverseCorrectionExponential_coefficient, coeff_one] using h

def correctionUnit (o : Fin 12) :
    (PowerSeries (Module.End ℂ (LatticeCarrier o)))ˣ where
  val := correctionExponential o
  inv := inverseCorrectionExponential o
  val_inv := correctionExponential_mul_inverse o
  inv_val := inverseCorrectionExponential_mul o

theorem inverseCorrectionCoefficient_zero (o : Fin 12) :
    inverseCorrectionCoefficient o 0 = 1 := by
  simp [inverseCorrectionCoefficient, expCoeff_fin]

theorem negativeCorrectionPower_lowersEnergy (o : Fin 12) (k d : ℕ) :
    LowersEnergy o d
      (coeff (Module.End ℂ (LatticeCarrier o)) d ((-correctionSeries o) ^ k)) := by
  induction k generalizing d with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs with h
    · subst d
      exact lowersEnergy_one o
    · exact lowersEnergy_zero o d
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply lowersEnergy_sum
    intro p hp
    rw [← Finset.mem_antidiagonal.mp hp]
    rw [map_neg, correctionSeries_coefficient]
    apply lowersEnergy_mul o p.1 p.2 _ _ (ih p.1)
    intro v
    simp only [LinearMap.neg_apply, map_neg]
    rw [correctionCoefficient_lowersEnergy o p.2 v]
    simp only [smul_neg]
    abel

theorem inverseCorrection_lowersEnergy (o : Fin 12) (d : ℕ) :
    LowersEnergy o d (inverseCorrectionCoefficient o d) := by
  apply lowersEnergy_sum
  intro k _
  exact lowersEnergy_smul o d _ _ (negativeCorrectionPower_lowersEnergy o k d)

theorem inverseCorrection_basis_cutoff (o : Fin 12)
    (p : Occupation o × Lattice o) (d : ℕ) (hd : totalWeight o p < d) :
    inverseCorrectionCoefficient o d (carrierBasis o p) = 0 := by
  apply negative_energy_eigenvector_zero o _ (totalWeight o p) d hd
  rw [inverseCorrection_lowersEnergy, energy_basis, map_smul, sub_smul]

theorem inverseCorrection_polynomial_on_state (o : Fin 12) (v : LatticeCarrier o) :
    ∃ N : ℕ, ∀ d ≥ N, inverseCorrectionCoefficient o d v = 0 := by
  classical
  let S := ((carrierBasis o).repr v).support
  refine ⟨S.sup (totalWeight o) + 1, ?_⟩
  intro d hd
  conv_lhs => rw [← (carrierBasis o).linearCombination_repr v]
  rw [Finsupp.linearCombination_apply, Finsupp.sum, map_sum]
  apply Finset.sum_eq_zero
  intro p hp
  rw [map_smul]
  have hw : totalWeight o p ≤ S.sup (totalWeight o) := Finset.le_sup hp
  rw [inverseCorrection_basis_cutoff o p d (by omega), smul_zero]

theorem negativeCorrectionPower_parity (o : Fin 12) (k d : ℕ)
    (v : LatticeCarrier o) :
    carrierTheta o
        ((coeff (Module.End ℂ (LatticeCarrier o)) d ((-correctionSeries o) ^ k)) v) =
      (coeff (Module.End ℂ (LatticeCarrier o)) d ((-correctionSeries o) ^ k))
        (carrierTheta o v) := by
  induction k generalizing d v with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs <;> simp
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    simp only [LinearMap.sum_apply, Module.End.mul_apply, map_sum,
      map_neg, correctionSeries_coefficient, LinearMap.neg_apply,
      ih, map_neg, correctionCoefficient_parity]

theorem inverseCorrection_parity (o : Fin 12) (d : ℕ) (v : LatticeCarrier o) :
    carrierTheta o (inverseCorrectionCoefficient o d v) =
      inverseCorrectionCoefficient o d (carrierTheta o v) := by
  simp only [inverseCorrectionCoefficient, expCoeff_fin, LinearMap.sum_apply,
    LinearMap.smul_apply, map_sum, map_smul, negativeCorrectionPower_parity]

theorem inverseCorrection_mem_parity (o : Fin 12) (d : ℕ) (s : ℂ)
    (v : LatticeCarrier o) (hv : v ∈ paritySpace o s) :
    inverseCorrectionCoefficient o d v ∈ paritySpace o s := by
  apply (mem_paritySpace o s _).2
  rw [inverseCorrection_parity, (mem_paritySpace o s v).1 hv, map_smul]

def evenInverseCorrectionCoefficient (o : Fin 12) (d : ℕ) :
    Module.End ℂ (evenSpace o) :=
  (inverseCorrectionCoefficient o d).restrict
    (fun v hv => inverseCorrection_mem_parity o d 1 v hv)

theorem evenInverseCorrection_coefficient (o : Fin 12) (d : ℕ) (v : evenSpace o) :
    (evenInverseCorrectionCoefficient o d v).val =
      inverseCorrectionCoefficient o d v.val := rfl

theorem evenInverseCorrection_polynomial_on_state (o : Fin 12) (v : evenSpace o) :
    ∃ N : ℕ, ∀ d ≥ N, evenInverseCorrectionCoefficient o d v = 0 := by
  obtain ⟨N,hN⟩ := inverseCorrection_polynomial_on_state o v.val
  refine ⟨N, fun d hd => ?_⟩
  apply Subtype.ext
  exact hN d hd

end HMT.IV.LatticeTwistedCorrectionInverse
end

#print axioms HMT.IV.LatticeTwistedCorrectionInverse.correctionExponential_mul_inverse
#print axioms HMT.IV.LatticeTwistedCorrectionInverse.inverseCorrectionExponential_mul
#print axioms HMT.IV.LatticeTwistedCorrectionInverse.correction_inverse_convolution
#print axioms HMT.IV.LatticeTwistedCorrectionInverse.inverse_correction_convolution
