import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic

/-!
# Normalized propagation reader

The rational coefficients are produced by a₀ = 1 and
(n + 1) aₙ₊₁ = aₙ.  Factorials and Real.exp appear afterwards in proofs,
not as inputs selecting a regional state, coefficient, or finite prefix.

Source: generacion.tex, "Lector de propagación y normalización de la unidad";
generar_desde_estructura.py, propagation_e_bounds (lines 484–499).
This file formalizes the normalized scalar reader at that explicit cut;
it does not assert a complete Lean implementation of the upstream TPK.
-/

noncomputable section
open Filter Topology Finset

namespace PropagationLimit

/-- Exact rational coefficients, generated without a target real value. -/
def coefficient : Nat → ℚ
  | 0 => 1
  | n + 1 => coefficient n / (n + 1 : ℚ)

def Normalized {K : Type*} [Field K] [CharZero K] (a : Nat → K) : Prop :=
  a 0 = 1 ∧ ∀ n : Nat, (n + 1 : K) * a (n + 1) = a n

theorem coefficient_zero : coefficient 0 = 1 := rfl

theorem coefficient_recurrence (n : Nat) :
    (n + 1 : ℚ) * coefficient (n + 1) = coefficient n := by
  rw [coefficient]
  have hn : (n + 1 : ℚ) ≠ 0 := by positivity
  field_simp

theorem coefficient_normalized : Normalized coefficient :=
  ⟨coefficient_zero, coefficient_recurrence⟩

theorem normalized_unique {K : Type*} [Field K] [CharZero K]
    (a b : Nat → K) (ha : Normalized a) (hb : Normalized b) : a = b := by
  funext n
  induction n with
  | zero => exact ha.1.trans hb.1.symm
  | succ n ih =>
    have hn : (n + 1 : K) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
    apply mul_left_cancel₀ hn
    rw [ha.2, hb.2, ih]

theorem coefficient_unique (a : Nat → ℚ) (ha : Normalized a) :
    a = coefficient := normalized_unique a coefficient ha coefficient_normalized

/-- Factorial identification is a theorem downstream of the recurrence. -/
theorem coefficient_eq_factorial (n : Nat) :
    coefficient n = 1 / (n.factorial : ℚ) := by
  induction n with
  | zero => simp [coefficient]
  | succ n ih =>
    rw [coefficient, ih, Nat.factorial_succ, div_div]
    congr 1
    push_cast
    ring

theorem coefficient_positive (n : Nat) : 0 < coefficient n := by
  rw [coefficient_eq_factorial]
  positivity

def partialQ (n : Nat) : ℚ := ∑ j ∈ range (n + 1), coefficient j

/-- Real publication of the already generated rational partial sum. -/
def partialSum (n : Nat) : ℝ := (partialQ n : ℝ)

/-- The scalar publication is defined from the generated coefficients. -/
def value : ℝ := ∑' n : Nat, (coefficient n : ℝ)

theorem coefficient_real_factorial (n : Nat) :
    (coefficient n : ℝ) = 1 / (n.factorial : ℝ) := by
  rw [coefficient_eq_factorial]
  push_cast
  rfl

theorem real_coefficients_normalized : Normalized (fun n => (coefficient n : ℝ)) := by
  constructor
  · norm_num [coefficient_zero]
  · intro n
    have h := congrArg (fun q : ℚ => (q : ℝ)) (coefficient_recurrence n)
    simpa only [Rat.cast_mul, Rat.cast_add, Rat.cast_natCast, Rat.cast_one] using h

theorem partial_factorial (n : Nat) :
    partialSum n = ∑ j ∈ range (n + 1), 1 / (j.factorial : ℝ) := by
  simp [partialSum, partialQ, coefficient_real_factorial]

theorem partial_succ (n : Nat) :
    partialSum (n + 1) = partialSum n + (coefficient (n + 1) : ℝ) := by
  simp [partialSum, partialQ, Finset.sum_range_succ]

theorem partial_strictMono : StrictMono partialSum := by
  apply strictMono_nat_of_lt_succ
  intro n
  rw [partial_succ]
  have h : (0 : ℝ) < coefficient (n + 1) := by exact_mod_cast coefficient_positive (n + 1)
  linarith

theorem generated_summable : Summable (fun n => (coefficient n : ℝ)) := by
  simpa only [one_pow, coefficient_real_factorial] using
    Real.summable_pow_div_factorial (1 : ℝ)

/-- Recognition by the exponential series comes after coefficient generation. -/
theorem generated_hasSum_exp_one :
    HasSum (fun n => (coefficient n : ℝ)) (Real.exp 1) := by
  have h := NormedSpace.expSeries_div_hasSum_exp ℝ (1 : ℝ)
  simpa only [← Real.exp_eq_exp_ℝ, one_pow, coefficient_real_factorial] using h

theorem value_eq_exp_one : value = Real.exp 1 := generated_hasSum_exp_one.tsum_eq

theorem partial_tendsto : Tendsto partialSum atTop (𝓝 value) := by
  have h := generated_summable.hasSum.tendsto_sum_nat
  have hs := h.comp (tendsto_add_atTop_nat 1)
  change Tendsto (fun n => (partialQ n : ℝ)) atTop (𝓝 value)
  simpa [partialQ, value, Function.comp_def] using hs

theorem partial_tendsto_exp_one : Tendsto partialSum atTop (𝓝 (Real.exp 1)) := by
  rw [← value_eq_exp_one]
  exact partial_tendsto

theorem normalized_real_hasSum (a : Nat → ℝ) (ha : Normalized a) :
    HasSum a value := by
  have heq := normalized_unique a (fun n => (coefficient n : ℝ)) ha real_coefficients_normalized
  rw [heq]
  exact generated_summable.hasSum

theorem partial_lt_value (n : Nat) : partialSum n < value := by
  have hle : partialSum (n + 1) ≤ value := by
    have h := generated_summable.sum_le_tsum (range (n + 1 + 1))
      (fun k _ => (show (0 : ℝ) ≤ coefficient k from
        le_of_lt (by exact_mod_cast coefficient_positive k)))
    simpa [partialSum, partialQ, value] using h
  exact lt_of_lt_of_le (partial_strictMono (Nat.lt_succ_self n)) hle

/-- The exact rational tail width in the executable certificate. -/
def tailQ (n : Nat) : ℚ := (n + 2) / ((n + 1)^2 * (n.factorial : ℚ))

def upperQ (n : Nat) : ℚ := partialQ n + tailQ n

theorem tailQ_positive (n : Nat) : 0 < tailQ n := by
  unfold tailQ
  positivity

theorem tail_real_formula (n : Nat) :
    (tailQ n : ℝ) = (n + 2 : ℝ) / ((n + 1) * (n + 1).factorial) := by
  simp only [tailQ, Rat.cast_div, Rat.cast_add, Rat.cast_natCast, Rat.cast_ofNat,
    Rat.cast_mul, Rat.cast_pow]
  rw [Nat.factorial_succ]
  push_cast
  congr 1
  ring

/-- Strict bound obtained from the series after its posterior recognition. -/
theorem factorial_remainder_lt (n : Nat) :
    Real.exp 1 - ∑ k ∈ range (n + 1), (1 : ℝ) / k.factorial <
      (n + 2 : ℝ) / ((n + 1) * (n + 1).factorial) := by
  have h : Real.exp 1 ≤
      (∑ k ∈ range (n + 2), (1 : ℝ) / k.factorial) +
        (n + 3 : ℝ) / ((n + 2).factorial * (n + 2)) := by
    convert Real.exp_bound' (x := 1) (by norm_num) (by norm_num)
      (n := n + 2) (by omega) using 1
    simp
    ring
  rw [Finset.sum_range_succ] at h
  have hn : (0 : ℝ) < n + 1 := by positivity
  have hn2 : (0 : ℝ) < n + 2 := by positivity
  have hf : (0 : ℝ) < (n + 1).factorial := by positivity
  have hfac : ((n + 2).factorial : ℝ) =
      (n + 2 : ℝ) * (n + 1).factorial := by
    rw [show n + 2 = Nat.succ (n + 1) by omega, Nat.factorial_succ]
    push_cast
    ring
  have hg : (n + 2 : ℝ) / ((n + 1) * (n + 1).factorial) -
      ((1 : ℝ) / (n + 1).factorial +
        (n + 3 : ℝ) / ((n + 2).factorial * (n + 2))) =
      1 / ((n + 1) * (n + 2)^2 * (n + 1).factorial) := by
    rw [hfac]
    field_simp
    ring
  have hpos : (0 : ℝ) <
      1 / ((n + 1) * (n + 2)^2 * (n + 1).factorial) := by positivity
  linarith

theorem rational_bracket (n : Nat) :
    (partialQ n : ℝ) < value ∧ value < (upperQ n : ℝ) := by
  refine ⟨partial_lt_value n, ?_⟩
  have h := factorial_remainder_lt n
  rw [← value_eq_exp_one, ← partial_factorial, ← tail_real_formula] at h
  simpa only [upperQ, Rat.cast_add, partialSum, add_comm] using (sub_lt_iff_lt_add.mp h)

theorem tail_real_le_two_coefficients (n : Nat) :
    (tailQ n : ℝ) ≤ 2 * (coefficient (n + 1) : ℝ) := by
  rw [tail_real_formula, coefficient_real_factorial]
  have hn : (0 : ℝ) < n + 1 := by positivity
  have hf : (0 : ℝ) < (n + 1).factorial := by positivity
  rw [div_mul_eq_div_div, mul_one_div]
  apply (div_le_div_iff_of_pos_right hf).2
  apply (div_le_iff₀ hn).2
  nlinarith [show (0 : ℝ) ≤ n by positivity]

theorem tail_tendsto_zero : Tendsto (fun n => (tailQ n : ℝ)) atTop (𝓝 0) := by
  apply squeeze_zero (fun n => le_of_lt (by exact_mod_cast tailQ_positive n))
    tail_real_le_two_coefficients
  have h := generated_summable.tendsto_atTop_zero
  have hs := h.comp (tendsto_add_atTop_nat 1)
  simpa only [Function.comp_def, mul_zero] using hs.const_mul 2

theorem upper_tendsto : Tendsto (fun n => (upperQ n : ℝ)) atTop (𝓝 value) := by
  have h := partial_tendsto.add tail_tendsto_zero
  simpa only [upperQ, Rat.cast_add, add_zero, partialSum] using h

theorem rational_width (n : Nat) : upperQ n - partialQ n = tailQ n := by
  simp [upperQ]

/-- Every finite requested scale satisfies the certificate's stopping test. -/
theorem exists_precision_index (scale : Nat) :
    ∃ n : Nat, 1 ≤ n ∧ (upperQ n - partialQ n) * scale < 1 := by
  have hlim : Tendsto (fun n => (tailQ n : ℝ) * scale) atTop (𝓝 0) := by
    simpa only [zero_mul] using tail_tendsto_zero.mul_const (scale : ℝ)
  have hevent : ∀ᶠ n in atTop, (tailQ n : ℝ) * scale < 1 :=
    (tendsto_order.mp hlim).2 1 (by norm_num)
  rcases eventually_atTop.mp hevent with ⟨N, hN⟩
  refine ⟨max N 1, le_max_right _ _, ?_⟩
  rw [rational_width]
  have h := hN (max N 1) (le_max_left _ _)
  exact_mod_cast h

end PropagationLimit
end

#print axioms PropagationLimit.coefficient_zero
#print axioms PropagationLimit.coefficient_recurrence
#print axioms PropagationLimit.coefficient_normalized
#print axioms PropagationLimit.normalized_unique
#print axioms PropagationLimit.coefficient_unique
#print axioms PropagationLimit.coefficient_eq_factorial
#print axioms PropagationLimit.coefficient_positive
#print axioms PropagationLimit.coefficient_real_factorial
#print axioms PropagationLimit.real_coefficients_normalized
#print axioms PropagationLimit.partial_factorial
#print axioms PropagationLimit.partial_succ
#print axioms PropagationLimit.partial_strictMono
#print axioms PropagationLimit.generated_hasSum_exp_one
#print axioms PropagationLimit.generated_summable
#print axioms PropagationLimit.value_eq_exp_one
#print axioms PropagationLimit.partial_tendsto
#print axioms PropagationLimit.partial_tendsto_exp_one
#print axioms PropagationLimit.normalized_real_hasSum
#print axioms PropagationLimit.partial_lt_value
#print axioms PropagationLimit.tailQ_positive
#print axioms PropagationLimit.tail_real_formula
#print axioms PropagationLimit.factorial_remainder_lt
#print axioms PropagationLimit.rational_bracket
#print axioms PropagationLimit.tail_real_le_two_coefficients
#print axioms PropagationLimit.tail_tendsto_zero
#print axioms PropagationLimit.upper_tendsto
#print axioms PropagationLimit.rational_width
#print axioms PropagationLimit.exists_precision_index
