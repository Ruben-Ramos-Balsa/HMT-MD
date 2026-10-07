import LatticeExponentialExchange
import Mathlib.RingTheory.PowerSeries.Derivative

/-!
Scalar contraction and operator regrouping on the already constructed
Fock carrier. The scalar coefficients are fixed by an initial value and an
all-degree recurrence from the inherited integral pairing.
-/

noncomputable section
set_option maxHeartbeats 1500000
namespace HMT.IV.LatticeExponentialContraction

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialCommutator HMT.IV.LatticeExponentialExchange
open PowerSeries
open scoped BigOperators

section SeriesDerivative
variable {R : Type*} [Ring R]

def diffSeries (f : PowerSeries R) : PowerSeries R :=
  PowerSeries.mk fun n => (n+1) • coeff R (n+1) f

@[simp] theorem diffSeries_coeff (f : PowerSeries R) (n : ℕ) :
    coeff R n (diffSeries f) = (n+1) • coeff R (n+1) f := coeff_mk _ _

theorem diffSeries_add (f g : PowerSeries R) :
    diffSeries (f+g) = diffSeries f + diffSeries g := by
  ext n
  simp [diffSeries_coeff, nsmul_add]

theorem diffSeries_C (r : R) : diffSeries (C R r) = 0 := by
  ext n
  simp

theorem diffSeries_mul (f g : PowerSeries R) :
    diffSeries (f*g) = diffSeries f * g + f * diffSeries g := by
  ext n
  simp only [diffSeries_coeff, coeff_mul, map_add, Finset.smul_sum]
  have hs : (∑ p ∈ Finset.antidiagonal (n+1),
      (n+1) • (coeff R p.1 f * coeff R p.2 g)) =
      (∑ p ∈ Finset.antidiagonal (n+1), p.1 • (coeff R p.1 f * coeff R p.2 g)) +
      (∑ p ∈ Finset.antidiagonal (n+1), p.2 • (coeff R p.1 f * coeff R p.2 g)) := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro p hp
    rw [← add_nsmul, Finset.mem_antidiagonal.mp hp]
  rw [hs, Finset.Nat.sum_antidiagonal_succ, Finset.Nat.sum_antidiagonal_succ']
  simp only [zero_nsmul, zero_add, smul_mul_assoc, mul_smul_comm]

theorem series_commute_of_coefficients (f g : PowerSeries R)
    (h : ∀ i j, Commute (coeff R i f) (coeff R j g)) : Commute f g := by
  change f*g=g*f
  ext n
  rw [coeff_mul, coeff_mul, ← Finset.Nat.sum_antidiagonal_swap]
  apply Finset.sum_congr rfl
  intro p _
  exact (h p.2 p.1).eq

end SeriesDerivative

def scalarContraction (p : ℤ) : ℕ → ℂ
  | 0 => 1
  | n+1 => ((n : ℂ)-(p : ℂ)) / (n+1 : ℂ) * scalarContraction p n

@[simp] theorem scalarContraction_zero (p : ℤ) : scalarContraction p 0 = 1 := rfl

theorem scalarContraction_step (p : ℤ) (n : ℕ) :
    (n+1 : ℂ) * scalarContraction p (n+1) =
      ((n : ℂ)-(p : ℂ)) * scalarContraction p n := by
  rw [scalarContraction]
  have hn : (n+1 : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
  field_simp

theorem scalarContraction_unique (p : ℤ) (b : ℕ → ℂ) (h0 : b 0 = 1)
    (h : ∀ n : ℕ, (n+1 : ℂ)*b (n+1)=((n : ℂ)-(p : ℂ))*b n) :
    b = scalarContraction p := by
  funext n
  induction n with
  | zero => exact h0
  | succ n ih =>
    apply mul_left_cancel₀ (show (n+1 : ℂ) ≠ 0 by exact_mod_cast Nat.succ_ne_zero n)
    rw [h, ih, scalarContraction_step]

theorem scalarContraction_sum_recurrence (p : ℤ) (n : ℕ) :
    (n+1 : ℂ) * scalarContraction p (n+1) =
      -(p : ℂ) * ∑ i ∈ Finset.range (n+1), scalarContraction p i := by
  induction n with
  | zero => simp [scalarContraction]
  | succ n ih =>
    rw [scalarContraction_step, Finset.sum_range_succ, mul_add, ← ih]
    push_cast
    ring

abbrev Inner (o : Fin 12) := PowerSeries (FockEnd o)

def creationSeries (o : Fin 12) (y : Lattice o) : Inner o :=
  PowerSeries.mk (creationExponentialMode o y)

def contractionSeries (o : Fin 12) (p : ℤ) : PowerSeries (Inner o) :=
  PowerSeries.mk fun r => scalarContraction p r • (X^r : Inner o)

def poleSeries (o : Fin 12) (p : ℤ) : PowerSeries (Inner o) :=
  PowerSeries.mk fun n => (p : ℂ) • (X^(n+1) : Inner o)

@[simp] theorem contractionSeries_coeff (o : Fin 12) (p : ℤ) (r : ℕ) :
    coeff (Inner o) r (contractionSeries o p) =
      scalarContraction p r • (X^r : Inner o) := coeff_mk _ _

@[simp] theorem poleSeries_coeff (o : Fin 12) (p : ℤ) (r : ℕ) :
    coeff (Inner o) r (poleSeries o p) = (p : ℂ) • (X^(r+1) : Inner o) :=
  coeff_mk _ _

theorem contractionSeries_commute (o : Fin 12) (p : ℤ)
    (f : PowerSeries (Inner o)) : Commute (contractionSeries o p) f := by
  apply series_commute_of_coefficients
  intro i j
  rw [contractionSeries_coeff]
  exact ((PowerSeries.commute_X_pow (coeff (Inner o) j f) i).symm).smul_left _

theorem contractionSeries_diff (o : Fin 12) (p : ℤ) :
    diffSeries (contractionSeries o p) = -(poleSeries o p * contractionSeries o p) := by
  apply PowerSeries.ext
  intro n
  rw [diffSeries_coeff, contractionSeries_coeff, map_neg, coeff_mul]
  simp only [poleSeries_coeff, contractionSeries_coeff, smul_mul_assoc,
    mul_smul_comm, smul_smul, mul_comm (scalarContraction p _) (p : ℂ)]
  have hs : (∑ q ∈ Finset.antidiagonal n,
      ((p : ℂ) * scalarContraction p q.2) •
        ((X^(q.1+1) : Inner o) * X^q.2)) =
      ((p : ℂ) * ∑ i ∈ Finset.range (n+1), scalarContraction p i) •
        (X^(n+1) : Inner o) := by
    simp_rw [← pow_add]
    have he : (∑ q ∈ Finset.antidiagonal n,
        ((p : ℂ) * scalarContraction p q.2) • (X^(q.1+1+q.2) : Inner o)) =
        ∑ q ∈ Finset.antidiagonal n,
          ((p : ℂ) * scalarContraction p q.2) • (X^(n+1) : Inner o) := by
      apply Finset.sum_congr rfl
      intro q hq
      have hq' := Finset.mem_antidiagonal.mp hq
      rw [show q.1+1+q.2=n+1 by omega]
    rw [he, ← Finset.sum_smul, ← Finset.mul_sum,
      ← Finset.Nat.sum_antidiagonal_swap]
    change ((p : ℂ) * ∑ q ∈ Finset.antidiagonal n, scalarContraction p q.1) • _ = _
    rw [Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
  rw [hs, ← neg_smul, ← neg_mul]
  rw [← Nat.cast_smul_eq_nsmul ℂ, smul_smul,
    Nat.cast_add, Nat.cast_one, scalarContraction_sum_recurrence]

def annihilatorSeries (o : Fin 12) (x : Lattice o) : PowerSeries (Inner o) :=
  PowerSeries.mk fun n => C (FockEnd o) (chargeAnnihilation o x n)

def annihilationSeries (o : Fin 12) (x : Lattice o) : PowerSeries (Inner o) :=
  PowerSeries.mk fun r => C (FockEnd o) (exponentialCoefficient o x r)

theorem annihilator_creationSeries (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    C (FockEnd o) (chargeAnnihilation o x n) * creationSeries o y =
      creationSeries o y * C (FockEnd o) (chargeAnnihilation o x n) +
        ((integerPair o x y : ℂ) • (X^(n+1) : Inner o)) * creationSeries o y := by
  apply PowerSeries.ext
  intro d
  simp only [coeff_C_mul, coeff_mul_C, map_add, creationSeries, coeff_mk,
    smul_mul_assoc, coeff_smul, coeff_X_pow_mul']
  apply LinearMap.ext
  intro v
  have h := mixed_exponential_commutator_pairing o x y n d v
  rw [sub_eq_iff_eq_add] at h
  by_cases hd : n+1 ≤ d
  · simpa only [if_pos hd, LinearMap.add_apply, LinearMap.smul_apply,
      Module.End.mul_apply, add_comm] using h
  · simpa only [if_neg hd, LinearMap.add_apply, LinearMap.smul_apply,
      Module.End.mul_apply, smul_zero, LinearMap.zero_apply, add_zero, zero_add] using h

theorem annihilatorSeries_creation (o : Fin 12) (x y : Lattice o) :
    annihilatorSeries o x * C (Inner o) (creationSeries o y) =
      C (Inner o) (creationSeries o y) * annihilatorSeries o x +
        poleSeries o (integerPair o x y) * C (Inner o) (creationSeries o y) := by
  apply PowerSeries.ext
  intro n
  simp only [coeff_mul_C, coeff_C_mul, map_add, annihilatorSeries, coeff_mk,
    poleSeries_coeff]
  exact annihilator_creationSeries o x y n

theorem first_order_unique {R : Type*} [Ring R] [Algebra ℂ R]
    (K f g : PowerSeries R) (hf : diffSeries f = K*f)
    (hg : diffSeries g = K*g) (h0 : coeff R 0 f = coeff R 0 g) : f=g := by
  apply PowerSeries.ext
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    cases n with
    | zero => exact h0
    | succ n =>
      have he : (n+1) • coeff R (n+1) f = (n+1) • coeff R (n+1) g := by
        rw [← diffSeries_coeff, hf, ← diffSeries_coeff, hg, coeff_mul, coeff_mul]
        apply Finset.sum_congr rfl
        intro p hp
        rw [ih p.2 (by have hh := Finset.mem_antidiagonal.mp hp; omega)]
      rw [← Nat.cast_smul_eq_nsmul ℂ, ← Nat.cast_smul_eq_nsmul ℂ] at he
      exact smul_right_injective R (show ((n+1 : ℕ) : ℂ) ≠ 0 by
        exact_mod_cast Nat.succ_ne_zero n) he

end HMT.IV.LatticeExponentialContraction
end

#print axioms HMT.IV.LatticeExponentialContraction.diffSeries_mul
#print axioms HMT.IV.LatticeExponentialContraction.scalarContraction_unique
#print axioms HMT.IV.LatticeExponentialContraction.scalarContraction_sum_recurrence
#print axioms HMT.IV.LatticeExponentialContraction.contractionSeries_commute
#print axioms HMT.IV.LatticeExponentialContraction.contractionSeries_diff
#print axioms HMT.IV.LatticeExponentialContraction.annihilatorSeries_creation
#print axioms HMT.IV.LatticeExponentialContraction.first_order_unique
