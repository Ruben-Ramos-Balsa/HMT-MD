import LatticeHalfContractionFactor
import ScalarFactorBinomial
import FormalExpCoefficientBridge
import FiniteExponentialProduct

/-! Bivariate normal ordering from the inherited half-mode commutator.
The outer degree records annihilation and the inner degree creation.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 100000
namespace HMT.IV.LatticeHalfNormalOrderClosed

open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeHalfExponentialExchange LatticeHalfContractionFactor PowerSeries
open scoped BigOperators

abbrev BiSeries (o : Fin 12) := PowerSeries (PowerSeries (HalfEnd o))

def creationSeries (o : Fin 12) (y : Lattice o) : PowerSeries (HalfEnd o) :=
  mk (halfCreationExponentialMode o y)

def creationConstant (o : Fin 12) (y : Lattice o) : BiSeries o :=
  C _ (creationSeries o y)

def liftedPotential (o : Fin 12) (x : Lattice o) : BiSeries o :=
  map (C _) (annihilationPotential o x)

def scalarDiagonal : PowerSeries ℂ →+* PowerSeries (PowerSeries ℂ) :=
  (rescale (X : PowerSeries ℂ)).comp (map (C ℂ))

def diagonal (o : Fin 12) : PowerSeries ℂ →+* BiSeries o :=
  (map (map (algebraMap ℂ (HalfEnd o)))).comp scalarDiagonal

theorem coeff_diagonal (o : Fin 12) (s : PowerSeries ℂ) (r : ℕ) :
    coeff (PowerSeries (HalfEnd o)) r (diagonal o s) =
      coeff ℂ r s • (X ^ r : PowerSeries (HalfEnd o)) := by
  ext d
  simp only [diagonal, scalarDiagonal, RingHom.comp_apply, coeff_map, coeff_rescale,
    map_mul, map_pow, PowerSeries.map_X, PowerSeries.map_C, coeff_C_mul,
    coeff_mul_C, coeff_X_pow, coeff_smul]
  split_ifs <;> simp [Algebra.algebraMap_eq_smul_one]

theorem commute_of_coeff_commute {A : Type*} [Semiring A]
    (f g : PowerSeries A)
    (h : ∀ m n, Commute (coeff A m f) (coeff A n g)) : Commute f g := by
  change f * g = g * f
  ext n
  rw [coeff_mul, coeff_mul, ← Finset.Nat.sum_antidiagonal_swap]
  apply Finset.sum_congr rfl
  intro p _
  exact h _ _

theorem commute_diagonal (o : Fin 12) (f : BiSeries o) (s : PowerSeries ℂ) :
    Commute f (diagonal o s) := by
  apply commute_of_coeff_commute
  intro m n
  rw [coeff_diagonal]
  exact (PowerSeries.commute_X_pow _ n).smul_right _

theorem liftedPotential_constant (o : Fin 12) (x : Lattice o) :
    coeff (PowerSeries (HalfEnd o)) 0 (liftedPotential o x) = 0 := by
  simp only [liftedPotential, coeff_map, annihilationPotential_constant, map_zero]

theorem diagonal_contraction_constant (o : Fin 12) (x y : Lattice o) :
    coeff (PowerSeries (HalfEnd o)) 0 (diagonal o (contractionSeries o x y)) = 0 := by
  rw [coeff_diagonal, coeff_zero_eq_constantCoeff, contractionSeries_constant, zero_smul]

theorem potential_intertwining (o : Fin 12) (x y : Lattice o) :
    liftedPotential o x * creationConstant o y =
      creationConstant o y * (liftedPotential o x + diagonal o (contractionSeries o x y)) := by
  apply PowerSeries.ext
  intro r
  apply PowerSeries.ext
  intro d
  simp only [creationConstant, liftedPotential, coeff_mul_C, coeff_C_mul, map_add,
    coeff_map, coeff_diagonal, mul_add, coeff_mul_C, coeff_C_mul, creationSeries,
    coeff_mk, mul_smul_comm, coeff_smul, coeff_mul_X_pow']
  by_cases hr : r ≤ d <;>
    simpa only [hr, if_true, if_false, smul_zero] using
      potential_exchange_via_contractionSeries o x y r d

theorem power_intertwining (o : Fin 12) (x y : Lattice o) (k : ℕ) :
    liftedPotential o x ^ k * creationConstant o y =
      creationConstant o y *
        (liftedPotential o x + diagonal o (contractionSeries o x y)) ^ k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ', mul_assoc, ih, ← mul_assoc, potential_intertwining]
    simp only [mul_assoc, pow_succ']

theorem C_smul {A : Type*} [Ring A] [Algebra ℂ A] (c : ℂ) (a : A) :
    C A (c • a) = c • C A a := by
  apply PowerSeries.ext
  intro n
  simp only [coeff_C, coeff_smul]
  split_ifs <;> simp

theorem coeff_liftedPotential_pow (o : Fin 12) (x : Lattice o) (k r : ℕ) :
    coeff (PowerSeries (HalfEnd o)) r (liftedPotential o x ^ k) =
      C _ (coeff (HalfEnd o) r (annihilationPotential o x ^ k)) := by
  rw [liftedPotential, ← map_pow, coeff_map]

theorem sum_exp_liftedPotential (o : Fin 12) (x : Lattice o) (r : ℕ) :
    (∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) •
      coeff (PowerSeries (HalfEnd o)) r (liftedPotential o x ^ k)) =
        C _ (exponentialCoefficient o x r) := by
  rw [exponentialCoefficient, map_sum (C (HalfEnd o))]
  apply Finset.sum_congr rfl
  intro k _
  rw [coeff_liftedPotential_pow, C_smul]

theorem sum_exp_diagonal (o : Fin 12) (s : PowerSeries ℂ) (r : ℕ) :
    (∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) •
      coeff (PowerSeries (HalfEnd o)) r (diagonal o s ^ k)) =
        (∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) *
          coeff ℂ r (s ^ k)) • (X ^ r : PowerSeries (HalfEnd o)) := by
  rw [Finset.sum_smul]
  apply Finset.sum_congr rfl
  intro k _
  rw [← map_pow, coeff_diagonal, smul_smul]

theorem factorial_intertwining (o : Fin 12) (x y : Lattice o) (r : ℕ) :
    C _ (exponentialCoefficient o x r) * creationSeries o y =
      creationSeries o y *
        (∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) •
          coeff (PowerSeries (HalfEnd o)) r
            ((liftedPotential o x + diagonal o (contractionSeries o x y)) ^ k)) := by
  rw [← sum_exp_liftedPotential, Finset.sum_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [smul_mul_assoc, mul_smul_comm]
  congr 1
  have h := congrArg (coeff (PowerSeries (HalfEnd o)) r) (power_intertwining o x y k)
  simpa only [creationConstant, coeff_mul_C, coeff_C_mul] using h

theorem sum_exp_diagonal_factor (o : Fin 12) (x y : Lattice o) (r : ℕ) :
    (∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) •
      coeff (PowerSeries (HalfEnd o)) r (diagonal o (contractionSeries o x y) ^ k)) =
        coeff ℂ r (contractionFactor o x y) • (X ^ r : PowerSeries (HalfEnd o)) := by
  rw [sum_exp_diagonal, contractionFactor,
    HMT.Formal.FormalExpCoefficientBridge.coeff_formalExp_eq_sum _
      (contractionSeries_constant o x y)]

theorem coeff_creation_diagonal_convolution {A : Type*} [Ring A] [Algebra ℂ A]
    (c : PowerSeries A) (a : ℕ → A) (f : PowerSeries ℂ) (r d : ℕ) :
    coeff A d (c * (∑ p ∈ Finset.antidiagonal r,
      ((coeff ℂ p.1 f) • (X ^ p.1 : PowerSeries A)) * C A (a p.2))) =
        ∑ j ∈ Finset.range (min r d + 1),
          coeff ℂ j f • (coeff A (d-j) c * a (r-j)) := by
  rw [Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk, Finset.mul_sum, map_sum]
  simp only [← mul_assoc, mul_smul_comm, smul_mul_assoc, coeff_smul, coeff_mul_C,
    coeff_mul_X_pow']
  calc
    (∑ j ∈ Finset.range (r+1), coeff ℂ j f •
      ((if j ≤ d then coeff A (d-j) c else 0) * a (r-j))) =
      ∑ j ∈ Finset.range (min r d + 1), coeff ℂ j f •
        ((if j ≤ d then coeff A (d-j) c else 0) * a (r-j)) := by
      symm
      apply Finset.sum_subset (Finset.range_mono (by omega))
      intro j hj hjn
      have hjr : j ≤ r := by simp only [Finset.mem_range] at hj; omega
      have hjd : ¬j ≤ d := by simp only [Finset.mem_range] at hjn; omega
      simp only [if_neg hjd, zero_mul, smul_zero]
    _ = _ := by
      apply Finset.sum_congr rfl
      intro j hj
      have hjd : j ≤ d := by simp only [Finset.mem_range] at hj; omega
      rw [if_pos hjd]

theorem exponential_sum_factorization (o : Fin 12) (x y : Lattice o) (r : ℕ) :
    (∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) •
      coeff (PowerSeries (HalfEnd o)) r
        ((liftedPotential o x + diagonal o (contractionSeries o x y)) ^ k)) =
      ∑ p ∈ Finset.antidiagonal r,
        (coeff ℂ p.1 (contractionFactor o x y) •
          (X ^ p.1 : PowerSeries (HalfEnd o))) * C _ (exponentialCoefficient o x p.2) := by
  change HMT.Formal.FiniteExponentialProduct.expCoeff_fin
    (liftedPotential o x + diagonal o (contractionSeries o x y)) r = _
  rw [add_comm (liftedPotential o x),
    HMT.Formal.FiniteExponentialProduct.expCoeff_fin_add]
  · apply Finset.sum_congr rfl
    intro p _
    change (∑ k ∈ Finset.range (p.1+1), coeff ℂ k (PowerSeries.exp ℂ) •
      coeff (PowerSeries (HalfEnd o)) p.1 (diagonal o (contractionSeries o x y) ^ k)) *
      (∑ k ∈ Finset.range (p.2+1), coeff ℂ k (PowerSeries.exp ℂ) •
        coeff (PowerSeries (HalfEnd o)) p.2 (liftedPotential o x ^ k)) = _
    rw [sum_exp_diagonal_factor, sum_exp_liftedPotential]
  · simpa only [coeff_zero_eq_constantCoeff] using diagonal_contraction_constant o x y
  · simpa only [coeff_zero_eq_constantCoeff] using liftedPotential_constant o x
  · exact (commute_diagonal o (liftedPotential o x) (contractionSeries o x y)).symm

/-- Universal coefficientwise normal ordering. The finite summation bound is
determined by the two arbitrary degrees; there is no global mode cutoff. -/
theorem exponentialCoefficient_normal_order (o : Fin 12) (x y : Lattice o) (r d : ℕ) :
    exponentialCoefficient o x r * halfCreationExponentialMode o y d =
      ∑ j ∈ Finset.range (min r d + 1),
        coeff ℂ j (contractionFactor o x y) •
          (halfCreationExponentialMode o y (d-j) * exponentialCoefficient o x (r-j)) := by
  have h := factorial_intertwining o x y r
  rw [exponential_sum_factorization] at h
  have hc := congrArg (coeff (HalfEnd o) d) h
  rw [coeff_C_mul, coeff_creation_diagonal_convolution] at hc
  simpa only [creationSeries, coeff_mk] using hc

theorem normalExponential_closed (o : Fin 12) (x y : Lattice o) (r d : ℕ) :
    normalExponential o x y r d =
      ∑ j ∈ Finset.range (min r d + 1),
        coeff ℂ j (contractionFactor o x y) •
          (halfCreationExponentialMode o y (d-j) * exponentialCoefficient o x (r-j)) := by
  rw [← exponentialCoefficient_exchange, exponentialCoefficient_normal_order]

theorem exponentialCoefficient_normal_order_apply (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) (v : HalfFock o) :
    exponentialCoefficient o x r (halfCreationExponentialMode o y d v) =
      (∑ j ∈ Finset.range (min r d + 1),
        coeff ℂ j (contractionFactor o x y) •
          (halfCreationExponentialMode o y (d-j) * exponentialCoefficient o x (r-j))) v :=
  LinearMap.congr_fun (exponentialCoefficient_normal_order o x y r d) v

theorem exponentialCoefficient_rational_normal_order (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) :
    exponentialCoefficient o x r * halfCreationExponentialMode o y d =
      ∑ j ∈ Finset.range (min r d + 1),
        coeff ℂ j
          (HMT.Formal.HalfModeScalarFactor.rationalFactorUnit ^ integerPair o x y :
            (PowerSeries ℂ)ˣ) •
          (halfCreationExponentialMode o y (d-j) * exponentialCoefficient o x (r-j)) := by
  rw [exponentialCoefficient_normal_order, contractionFactor_eq_rational_integer_power]

end HMT.IV.LatticeHalfNormalOrderClosed
end
