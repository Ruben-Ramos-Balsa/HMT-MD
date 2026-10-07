import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Data.Complex.Exponential
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-!
# Bose--Einstein and Fermi--Dirac occupation laws from normalized state sums

Article V, `50_estadisticas_ocupacion.tex`, theorem
`v:rec:thm:factorizacion-gran-canonica-rev3`.
The modal state domains are `Bool` and `Nat`; weights, partition functions,
normalized probabilities, and expectations are defined before evaluating them.
The geometric series and its first moment are proved library theorems, not
hypotheses. The explicit Fock/TPK realization is a separate bridge.
-/

noncomputable section

open scoped BigOperators

namespace QuantumOccupations

/-- The two states of one fermionic mode have weights `1` and `u`. -/
def fermionWeight (u : ℝ) (b : Bool) : ℝ := if b then u else 1

def fermionOccupation (b : Bool) : ℝ := if b then 1 else 0

def fermionPartition (u : ℝ) : ℝ := ∑ b : Bool, fermionWeight u b

def fermionProbability (u : ℝ) (b : Bool) : ℝ :=
  fermionWeight u b / fermionPartition u

def fermionMean (u : ℝ) : ℝ :=
  ∑ b : Bool, fermionOccupation b * fermionProbability u b

theorem fermion_partition_eq (u : ℝ) : fermionPartition u = 1 + u := by
  simp [fermionPartition, fermionWeight, add_comm]

theorem fermion_partition_pos {u : ℝ} (hu : 0 ≤ u) : 0 < fermionPartition u := by
  rw [fermion_partition_eq]
  linarith

theorem fermion_probability_nonneg {u : ℝ} (hu : 0 ≤ u) (b : Bool) :
    0 ≤ fermionProbability u b := by
  apply div_nonneg _ (le_of_lt (fermion_partition_pos hu))
  cases b <;> simp [fermionWeight, hu]

theorem fermion_probability_sum {u : ℝ} (hu : 0 ≤ u) :
    (∑ b : Bool, fermionProbability u b) = 1 := by
  unfold fermionProbability
  have hd : 1 + u ≠ 0 := ne_of_gt (by linarith)
  simp [fermionWeight, fermion_partition_eq]
  field_simp
  ring

/-- The FD law is evaluated from the finite expectation, not postulated. -/
theorem fermion_mean_eq (u : ℝ) : fermionMean u = u / (1 + u) := by
  simp [fermionMean, fermionOccupation, fermionProbability,
    fermionWeight, fermion_partition_eq]

/-- Every nonnegative integer is an allowed occupation of one bosonic mode. -/
def bosonWeight (u : ℝ) (n : ℕ) : ℝ := u ^ n

def bosonPartition (u : ℝ) : ℝ := ∑' n : ℕ, bosonWeight u n

def bosonProbability (u : ℝ) (n : ℕ) : ℝ := bosonWeight u n / bosonPartition u

def bosonMean (u : ℝ) : ℝ := ∑' n : ℕ, (n : ℝ) * bosonProbability u n

/-- Actual convergence of the infinite modal partition series. -/
theorem boson_weight_hasSum {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    HasSum (bosonWeight u) (1 - u)⁻¹ :=
  hasSum_geometric_of_lt_one hu0 hu1

theorem boson_partition_eq {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    bosonPartition u = (1 - u)⁻¹ := (boson_weight_hasSum hu0 hu1).tsum_eq

theorem boson_partition_pos {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    0 < bosonPartition u := by
  rw [boson_partition_eq hu0 hu1]
  exact inv_pos.mpr (sub_pos.mpr hu1)

theorem boson_probability_nonneg {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) (n : ℕ) :
    0 ≤ bosonProbability u n :=
  div_nonneg (pow_nonneg hu0 n) (le_of_lt (boson_partition_pos hu0 hu1))

/-- Normalization is a convergent infinite sum equal to one. -/
theorem boson_probability_hasSum {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    HasSum (bosonProbability u) 1 := by
  have h := (boson_weight_hasSum hu0 hu1).div_const (bosonPartition u)
  have hz : (1 - u)⁻¹ = bosonPartition u := (boson_partition_eq hu0 hu1).symm
  rw [hz, div_self (ne_of_gt (boson_partition_pos hu0 hu1))] at h
  exact h

theorem boson_probability_sum {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    (∑' n : ℕ, bosonProbability u n) = 1 :=
  (boson_probability_hasSum hu0 hu1).tsum_eq

/-- The first unnormalized moment is also a convergent infinite series. -/
theorem boson_firstMoment_hasSum {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    HasSum (fun n : ℕ => (n : ℝ) * bosonWeight u n) (u / (1 - u) ^ 2) := by
  apply hasSum_coe_mul_geometric_of_norm_lt_one
  simpa only [Real.norm_eq_abs, abs_of_nonneg hu0] using hu1

/-- Normalize the proved first moment to obtain the Bose--Einstein occupation. -/
theorem boson_mean_hasSum {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    HasSum (fun n : ℕ => (n : ℝ) * bosonProbability u n) (u / (1 - u)) := by
  have h := (boson_firstMoment_hasSum hu0 hu1).div_const (bosonPartition u)
  have hd : 1 - u ≠ 0 := ne_of_gt (sub_pos.mpr hu1)
  have hvalue : (u / (1 - u) ^ 2) / bosonPartition u = u / (1 - u) := by
    rw [boson_partition_eq hu0 hu1]
    field_simp
    ring
  rw [hvalue] at h
  simpa only [bosonProbability, div_eq_mul_inv, mul_assoc] using h

/-- The BE law is evaluated from the normalized infinite expectation. -/
theorem boson_mean_eq {u : ℝ} (hu0 : 0 ≤ u) (hu1 : u < 1) :
    bosonMean u = u / (1 - u) := (boson_mean_hasSum hu0 hu1).tsum_eq

/-- Outside the upper convergence boundary the nonnegative weights are not summable. -/
theorem boson_not_summable_of_one_le {u : ℝ} (hu : 1 ≤ u) :
    ¬ Summable (bosonWeight u) := by
  intro h
  have hnorm : ‖u‖ < 1 := summable_geometric_iff_norm_lt_one.mp h
  have hu0 : 0 ≤ u := le_trans zero_le_one hu
  rw [Real.norm_eq_abs, abs_of_nonneg hu0] at hnorm
  exact (not_lt_of_ge hu) hnorm

/-- Thermal modal weight, with the full energy-minus-chemical-potential exponent. -/
def fugacity (β E μ : ℝ) : ℝ := Real.exp (-(β * (E - μ)))

theorem fugacity_pos (β E μ : ℝ) : 0 < fugacity β E μ := Real.exp_pos _

theorem fugacity_lt_one {β E μ : ℝ} (hβ : 0 < β) (hμ : μ < E) :
    fugacity β E μ < 1 := by
  apply Real.exp_lt_one_iff.mpr
  exact neg_lt_zero.mpr (mul_pos hβ (sub_pos.mpr hμ))

/-- FD exponential form follows from the finite probability expectation. -/
theorem fermion_mean_exponential (β E μ : ℝ) :
    fermionMean (fugacity β E μ) = 1 / (Real.exp (β * (E - μ)) + 1) := by
  rw [fermion_mean_eq, fugacity, Real.exp_neg]
  have he : 0 < Real.exp (β * (E - μ)) := Real.exp_pos _
  have hd : Real.exp (β * (E - μ)) + 1 ≠ 0 := by positivity
  field_simp

/-- BE exponential form includes the condition ensuring convergence and normalization. -/
theorem boson_mean_exponential {β E μ : ℝ} (hβ : 0 < β) (hμ : μ < E) :
    bosonMean (fugacity β E μ) = 1 / (Real.exp (β * (E - μ)) - 1) := by
  rw [boson_mean_eq (le_of_lt (fugacity_pos β E μ)) (fugacity_lt_one hβ hμ),
    fugacity, Real.exp_neg]
  have he : 0 < Real.exp (β * (E - μ)) := Real.exp_pos _
  have he1 : 1 < Real.exp (β * (E - μ)) :=
    Real.one_lt_exp_iff.mpr (mul_pos hβ (sub_pos.mpr hμ))
  have hd : Real.exp (β * (E - μ)) - 1 ≠ 0 := ne_of_gt (sub_pos.mpr he1)
  field_simp

/-- A level with `g` equally weighted modes has the sum of their expectations. -/
def fermionLevelMean (g : ℕ) (u : ℝ) : ℝ := ∑ _ : Fin g, fermionMean u

def bosonLevelMean (g : ℕ) (u : ℝ) : ℝ := ∑ _ : Fin g, bosonMean u

theorem fermion_level_mean_exponential (g : ℕ) (β E μ : ℝ) :
    fermionLevelMean g (fugacity β E μ) = (g : ℝ) / (Real.exp (β * (E - μ)) + 1) := by
  simp [fermionLevelMean, fermion_mean_exponential, nsmul_eq_mul, div_eq_mul_inv]

theorem boson_level_mean_exponential (g : ℕ) {β E μ : ℝ} (hβ : 0 < β) (hμ : μ < E) :
    bosonLevelMean g (fugacity β E μ) = (g : ℝ) / (Real.exp (β * (E - μ)) - 1) := by
  simp [bosonLevelMean, boson_mean_exponential hβ hμ, nsmul_eq_mul, div_eq_mul_inv]

#print axioms fermion_probability_sum
#print axioms fermion_mean_eq
#print axioms boson_weight_hasSum
#print axioms boson_probability_hasSum
#print axioms boson_firstMoment_hasSum
#print axioms boson_mean_eq
#print axioms boson_not_summable_of_one_le
#print axioms fermion_mean_exponential
#print axioms boson_mean_exponential
#print axioms fermion_level_mean_exponential
#print axioms boson_level_mean_exponential

end QuantumOccupations
