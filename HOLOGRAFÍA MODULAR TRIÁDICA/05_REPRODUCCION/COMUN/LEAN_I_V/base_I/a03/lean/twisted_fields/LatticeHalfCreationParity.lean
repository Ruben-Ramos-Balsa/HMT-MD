import LatticeHalfCreationExponential
import LatticeChargedFieldParity

/-! Parity of the ramified creation exponential. Odd oscillator frequencies
force coefficient d to transform by (-1)^d. This is proved coefficientwise
for the actual Fock algebra, rather than imposed on a new formal field. -/

noncomputable section
namespace HMT.IV.LatticeHalfCreationParity
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeParityCarrier LatticeHalfCreationExponential
open LatticeCreationExponential LatticeChargedFieldParity PowerSeries
open scoped BigOperators

theorem theta_halfPotentialCoefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    fockTheta o (coeff (HalfFock o) d (halfCreationPotential o x)) =
      (-1:ℂ)^d • coeff (HalfFock o) d (halfCreationPotential o x) := by
  by_cases he : d % 2 = 0
  · have hd : d = 2 * (d/2) := by omega
    rw [hd, halfCreationPotential_coefficient_even]
    simp
  · have hd : d = 2 * (d/2) + 1 := by omega
    rw [hd, halfCreationPotential_coefficient_odd, map_smul]
    simp [chargeCreationState, fockTheta_generator, pow_add, pow_mul]

theorem halfPotentialCoefficient_neg_charge (o : Fin 12) (x : Lattice o) (d : ℕ) :
    coeff (HalfFock o) d (halfCreationPotential o (-x)) =
      (-1:ℂ)^d • coeff (HalfFock o) d (halfCreationPotential o x) := by
  by_cases he : d % 2 = 0
  · have hd : d = 2 * (d/2) := by omega
    rw [hd, halfCreationPotential_coefficient_even, halfCreationPotential_coefficient_even]
    simp
  · have hd : d = 2 * (d/2) + 1 := by omega
    rw [hd, halfCreationPotential_coefficient_odd, halfCreationPotential_coefficient_odd,
      chargeCreationState_neg]
    simp [pow_add, pow_mul]

theorem theta_halfPotentialPowerCoefficient (o : Fin 12) (x : Lattice o) (k d : ℕ) :
    fockTheta o (coeff (HalfFock o) d (halfCreationPotential o x ^ k)) =
      (-1:ℂ)^d • coeff (HalfFock o) d (halfCreationPotential o x ^ k) := by
  induction k generalizing d with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs with hd
    · subst d
      simp
    · simp
  | succ k ih =>
    simp only [pow_succ, coeff_mul, map_sum, Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro p hp
    have hd := Finset.mem_antidiagonal.mp hp
    rw [map_mul, ih, theta_halfPotentialCoefficient, smul_mul_assoc,
      mul_smul_comm, smul_smul, ← pow_add, hd]

theorem halfPotentialPowerCoefficient_neg_charge (o : Fin 12) (x : Lattice o)
    (k d : ℕ) :
    coeff (HalfFock o) d (halfCreationPotential o (-x) ^ k) =
      (-1:ℂ)^d • coeff (HalfFock o) d (halfCreationPotential o x ^ k) := by
  induction k generalizing d with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs with hd
    · subst d
      simp
    · simp
  | succ k ih =>
    rw [pow_succ, pow_succ, coeff_mul, coeff_mul, Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro p hp
    have hd := Finset.mem_antidiagonal.mp hp
    rw [ih, halfPotentialCoefficient_neg_charge, smul_mul_assoc,
      mul_smul_comm, smul_smul, ← pow_add, hd]

theorem theta_halfCreationExponential_coefficient (o : Fin 12) (x : Lattice o)
    (d : ℕ) :
    fockTheta o (coeff (HalfFock o) d (halfCreationExponential o x)) =
      (-1:ℂ)^d • coeff (HalfFock o) d (halfCreationExponential o x) := by
  simp only [halfCreationExponential_coefficient, map_sum, map_smul,
    theta_halfPotentialPowerCoefficient, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [smul_comm]

theorem halfCreationExponential_coefficient_neg_charge (o : Fin 12) (x : Lattice o)
    (d : ℕ) :
    coeff (HalfFock o) d (halfCreationExponential o (-x)) =
      (-1:ℂ)^d • coeff (HalfFock o) d (halfCreationExponential o x) := by
  simp only [halfCreationExponential_coefficient, halfPotentialPowerCoefficient_neg_charge,
    Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [smul_comm]

theorem theta_halfCreationExponentialMode (o : Fin 12) (x : Lattice o) (d : ℕ)
    (v : HalfFock o) :
    fockTheta o (halfCreationExponentialMode o x d v) =
      (-1:ℂ)^d • halfCreationExponentialMode o x d (fockTheta o v) := by
  change fockTheta o (coeff (HalfFock o) d (halfCreationExponential o x) * v) = _
  rw [map_mul, theta_halfCreationExponential_coefficient, smul_mul_assoc]
  rfl

theorem halfCreationExponentialMode_neg_charge (o : Fin 12) (x : Lattice o) (d : ℕ) :
    halfCreationExponentialMode o (-x) d = (-1:ℂ)^d • halfCreationExponentialMode o x d := by
  ext v
  change coeff (HalfFock o) d (halfCreationExponential o (-x)) * v = _
  rw [halfCreationExponential_coefficient_neg_charge, smul_mul_assoc]
  rfl

end HMT.IV.LatticeHalfCreationParity
end

#print axioms HMT.IV.LatticeHalfCreationParity.theta_halfCreationExponentialMode
#print axioms HMT.IV.LatticeHalfCreationParity.halfCreationExponentialMode_neg_charge
