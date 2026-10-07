import LatticeHalfAnnihilationExponential
import LatticeTwistedParity

/-! The parity of the half-integer annihilation exponential is derived from
the existing oscillator involution and the odd support of its potential.
Both conjugation and lattice-charge negation act on coefficient d by (-1)^d.
All statements concern the actual Fock operators; no parity hypothesis or
twisted vertex-algebra identity is supplied. -/

noncomputable section
namespace HMT.IV.LatticeHalfAnnihilationParity
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeParityCarrier LatticeHalfAnnihilationExponential
open PowerSeries
open scoped BigOperators

theorem chargeHalfAnnihilation_neg (o : Fin 12) (x : Lattice o) (n : ℕ) :
    chargeHalfAnnihilation o (-x) n = -chargeHalfAnnihilation o x n := by
  simp [chargeHalfAnnihilation, Finset.sum_neg_distrib]

theorem theta_chargeHalfAnnihilation (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : HalfFock o) :
    fockTheta o (chargeHalfAnnihilation o x n v) =
      -chargeHalfAnnihilation o x n (fockTheta o v) := by
  simp only [chargeHalfAnnihilation_apply, map_sum, map_smul,
    LatticeTwistedParity.theta_halfAnnihilate, smul_neg, Finset.sum_neg_distrib]

theorem theta_potentialCoefficient (o : Fin 12) (x : Lattice o) (d : ℕ)
    (v : HalfFock o) :
    fockTheta o (coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x) v) =
      (-1:ℂ)^d • coeff (Module.End ℂ (HalfFock o)) d
        (annihilationPotential o x) (fockTheta o v) := by
  rw [annihilationPotential_coefficient]
  split_ifs with hd
  · rw [LinearMap.smul_apply, map_smul, theta_chargeHalfAnnihilation,
      neg_one_pow_eq_pow_mod_two, hd]
    simp
  · simp

theorem potentialCoefficient_neg_charge (o : Fin 12) (x : Lattice o) (d : ℕ) :
    coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o (-x)) =
      (-1:ℂ)^d • coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x) := by
  rw [annihilationPotential_coefficient, annihilationPotential_coefficient]
  split_ifs with hd
  · rw [chargeHalfAnnihilation_neg, neg_one_pow_eq_pow_mod_two, hd]
    simp
  · simp

theorem theta_powerCoefficient (o : Fin 12) (x : Lattice o) (k d : ℕ)
    (v : HalfFock o) :
    fockTheta o (coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x ^ k) v) =
      (-1:ℂ)^d • coeff (Module.End ℂ (HalfFock o)) d
        (annihilationPotential o x ^ k) (fockTheta o v) := by
  induction k generalizing d v with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs with hd
    · subst d
      simp
    · simp
  | succ k ih =>
    simp only [pow_succ, coeff_mul, LinearMap.sum_apply, map_sum, Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro p hp
    have hd := Finset.mem_antidiagonal.mp hp
    simp only [Module.End.mul_apply, ih, theta_potentialCoefficient, map_smul, smul_smul]
    rw [← pow_add, hd]

theorem powerCoefficient_neg_charge (o : Fin 12) (x : Lattice o) (k d : ℕ) :
    coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o (-x) ^ k) =
      (-1:ℂ)^d • coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x ^ k) := by
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
    rw [ih, potentialCoefficient_neg_charge, smul_mul_assoc, mul_smul_comm,
      smul_smul, ← pow_add, hd]

theorem theta_exponentialCoefficient (o : Fin 12) (x : Lattice o) (d : ℕ)
    (v : HalfFock o) :
    fockTheta o (exponentialCoefficient o x d v) =
      (-1:ℂ)^d • exponentialCoefficient o x d (fockTheta o v) := by
  simp only [exponentialCoefficient, LinearMap.sum_apply, map_sum,
    LinearMap.smul_apply, map_smul, theta_powerCoefficient, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [smul_comm]

theorem exponentialCoefficient_neg_charge (o : Fin 12) (x : Lattice o) (d : ℕ) :
    exponentialCoefficient o (-x) d = (-1:ℂ)^d • exponentialCoefficient o x d := by
  simp only [exponentialCoefficient, powerCoefficient_neg_charge, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [smul_comm]

theorem theta_exponentialCoefficient_charge (o : Fin 12) (x : Lattice o) (d : ℕ)
    (v : HalfFock o) :
    fockTheta o (exponentialCoefficient o x d v) =
      exponentialCoefficient o (-x) d (fockTheta o v) := by
  rw [theta_exponentialCoefficient, exponentialCoefficient_neg_charge,
    LinearMap.smul_apply]

theorem conjugate_exponentialCoefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    (fockTheta o).toLinearMap * exponentialCoefficient o x d *
      (fockTheta o).toLinearMap = (-1:ℂ)^d • exponentialCoefficient o x d := by
  apply LinearMap.ext
  intro v
  change fockTheta o (exponentialCoefficient o x d (fockTheta o v)) = _
  rw [theta_exponentialCoefficient, fockTheta_square, LinearMap.smul_apply]

end HMT.IV.LatticeHalfAnnihilationParity
end

#print axioms HMT.IV.LatticeHalfAnnihilationParity.chargeHalfAnnihilation_neg
#print axioms HMT.IV.LatticeHalfAnnihilationParity.theta_chargeHalfAnnihilation
#print axioms HMT.IV.LatticeHalfAnnihilationParity.theta_potentialCoefficient
#print axioms HMT.IV.LatticeHalfAnnihilationParity.potentialCoefficient_neg_charge
#print axioms HMT.IV.LatticeHalfAnnihilationParity.theta_powerCoefficient
#print axioms HMT.IV.LatticeHalfAnnihilationParity.powerCoefficient_neg_charge
#print axioms HMT.IV.LatticeHalfAnnihilationParity.theta_exponentialCoefficient
#print axioms HMT.IV.LatticeHalfAnnihilationParity.exponentialCoefficient_neg_charge
#print axioms HMT.IV.LatticeHalfAnnihilationParity.theta_exponentialCoefficient_charge
#print axioms HMT.IV.LatticeHalfAnnihilationParity.conjugate_exponentialCoefficient
