import LatticeHalfExponentialCommutator

/-! Normal ordering in every pair of ramified degrees. The contraction is
read from the inherited lattice pairing and the actual half-integer frequency.
An independent finite recursion moves creation operators left and annihilation
operators right. Equality with the original product is proved by induction.
No BCH identity, locality, or mixed orbifold product is assumed. -/

noncomputable section
namespace HMT.IV.LatticeHalfExponentialExchange
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeHalfExponentialCommutator PowerSeries
open scoped BigOperators

abbrev HalfEnd (o : Fin 12) := Module.End ℂ (HalfFock o)

def contraction (o : Fin 12) (x y : Lattice o) (r : ℕ) : ℂ :=
  (-1 / (((r/2 : ℕ):ℂ)+1/2)) * (integerPair o x y : ℂ)

theorem contraction_odd (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    contraction o x y (2*n+1) = -2*(integerPair o x y : ℂ)/(2*(n:ℂ)+1) := by
  rw [contraction, show (2*n+1)/2 = n by omega]
  rw [show (n:ℂ)+1/2 = (2*(n:ℂ)+1)/2 by ring, div_div_eq_mul_div]
  ring

theorem potentialCoefficient_exchange (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) :
    coeff (HalfEnd o) r (annihilationPotential o x) * halfCreationExponentialMode o y d =
      halfCreationExponentialMode o y d * coeff (HalfEnd o) r (annihilationPotential o x) +
        if r%2=1 ∧ r≤d then
          contraction o x y r • halfCreationExponentialMode o y (d-r) else 0 := by
  rw [annihilationPotential_coefficient]
  by_cases hr : r%2=1
  · rw [if_pos hr]
    have he : 2*(r/2)+1 = r := by omega
    apply LinearMap.ext
    intro v
    have h := mixed_half_exponential_commutator o x y (r/2) d v
    rw [he, sub_eq_iff_eq_add] at h
    simp only [LinearMap.smul_apply, LinearMap.add_apply, Module.End.mul_apply, map_smul]
    rw [h]
    by_cases hd : r≤d
    · simp only [if_pos hd, hr, true_and, if_pos hd, smul_add,
        smul_smul, contraction, LinearMap.smul_apply]
      exact add_comm _ _
    · simp only [if_neg hd, hr, true_and, if_neg hd,
        zero_add, smul_zero, add_zero, LinearMap.zero_apply]
  · rw [if_neg hr, if_neg (by simp [hr])]
    simp

def normalPower (o : Fin 12) (x y : Lattice o) : ℕ → ℕ → ℕ → HalfEnd o
  | 0, r, d => if r=0 then halfCreationExponentialMode o y d else 0
  | k+1, r, d => ∑ p ∈ Finset.antidiagonal r,
      (normalPower o x y k p.1 d * coeff (HalfEnd o) p.2 (annihilationPotential o x) +
        if p.2%2=1 ∧ p.2≤d then
          contraction o x y p.2 • normalPower o x y k p.1 (d-p.2)
        else 0)

theorem powerCoefficient_exchange (o : Fin 12) (x y : Lattice o) (k r d : ℕ) :
    coeff (HalfEnd o) r (annihilationPotential o x ^ k) * halfCreationExponentialMode o y d =
      normalPower o x y k r d := by
  induction k generalizing r d with
  | zero =>
    simp only [pow_zero, coeff_one, normalPower]
    split_ifs <;> simp
  | succ k ih =>
    rw [pow_succ, coeff_mul, Finset.sum_mul, normalPower]
    apply Finset.sum_congr rfl
    intro p _
    rw [mul_assoc, potentialCoefficient_exchange, mul_add, ← mul_assoc, ih]
    congr 1
    split_ifs
    · rw [mul_smul_comm, ih]
    · rw [mul_zero]

def normalExponential (o : Fin 12) (x y : Lattice o) (r d : ℕ) : HalfEnd o :=
  ∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) • normalPower o x y k r d

theorem exponentialCoefficient_exchange (o : Fin 12) (x y : Lattice o) (r d : ℕ) :
    exponentialCoefficient o x r * halfCreationExponentialMode o y d =
      normalExponential o x y r d := by
  rw [exponentialCoefficient, Finset.sum_mul, normalExponential]
  apply Finset.sum_congr rfl
  intro k _
  rw [smul_mul_assoc, powerCoefficient_exchange]

theorem exponentialCoefficient_exchange_apply (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) (v : HalfFock o) :
    exponentialCoefficient o x r (halfCreationExponentialMode o y d v) =
      normalExponential o x y r d v :=
  LinearMap.congr_fun (exponentialCoefficient_exchange o x y r d) v

theorem normalExponential_zero_annihilation (o : Fin 12) (x y : Lattice o) (d : ℕ) :
    normalExponential o x y 0 d = halfCreationExponentialMode o y d := by
  rw [← exponentialCoefficient_exchange, annihilationExponential_constant]
  exact one_mul _

theorem normalExponential_zero_creation (o : Fin 12) (x y : Lattice o) (r : ℕ) :
    normalExponential o x y r 0 = exponentialCoefficient o x r := by
  rw [← exponentialCoefficient_exchange, halfCreationExponentialMode_zero]
  exact mul_one _

theorem orthogonal_potential_commute (o : Fin 12) (x y : Lattice o)
    (hxy : integerPair o x y = 0) (r d : ℕ) :
    Commute (coeff (HalfEnd o) r (annihilationPotential o x))
      (halfCreationExponentialMode o y d) := by
  change _ * _ = _ * _
  rw [potentialCoefficient_exchange]
  simp [contraction, hxy]

theorem orthogonal_power_commute (o : Fin 12) (x y : Lattice o)
    (hxy : integerPair o x y = 0) (k r d : ℕ) :
    Commute (coeff (HalfEnd o) r (annihilationPotential o x ^ k))
      (halfCreationExponentialMode o y d) := by
  induction k generalizing r with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs
    · exact Commute.one_left _
    · exact Commute.zero_left _
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply Commute.sum_left
    intro p _
    exact (ih p.1).mul_left (orthogonal_potential_commute o x y hxy p.2 d)

theorem orthogonal_exponentials_commute (o : Fin 12) (x y : Lattice o)
    (hxy : integerPair o x y = 0) (r d : ℕ) :
    Commute (exponentialCoefficient o x r) (halfCreationExponentialMode o y d) := by
  unfold exponentialCoefficient
  apply Commute.sum_left
  intro k _
  exact (orthogonal_power_commute o x y hxy k r d).smul_left _

end HMT.IV.LatticeHalfExponentialExchange
end

#print axioms HMT.IV.LatticeHalfExponentialExchange.exponentialCoefficient_exchange
#print axioms HMT.IV.LatticeHalfExponentialExchange.contraction_odd
