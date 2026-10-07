import PropagationLimit
import Mathlib.Data.Nat.Choose.Cast
import Mathlib.RingTheory.PowerSeries.Derivative

/-!
Coefficient comparison for the normalized formal propagation law.
The (m,n) coefficients of P(s+t) and P(s)P(t) are defined before
recognition by an analytic exponential. Their equality is equivalent to
the normalized recurrence, with its unit and positively oriented generator.
Source: generacion.tex, normalized propagation reader.
-/
noncomputable section
namespace PropagationSemigroup

open PropagationLimit

variable {K : Type*} [Field K] [CharZero K]

/-- Coefficient of s^m t^n after the binomial substitution in P(s+t). -/
def translatedCoefficient (a : Nat → K) (m n : Nat) : K :=
  ((m + n).choose m : K) * a (m + n)

/-- Coefficient of s^m t^n in the separated product P(s)P(t). -/
def productCoefficient (a : Nat → K) (m n : Nat) : K := a m * a n

def SemigroupLaw (a : Nat → K) : Prop :=
  ∀ m n, translatedCoefficient a m n = productCoefficient a m n

def UnitGenerator (a : Nat → K) : Prop := a 0 = 1 ∧ a 1 = 1

theorem recurrence_from_semigroup (a : Nat → K)
    (h : SemigroupLaw a) (hunit : UnitGenerator a) : Normalized a := by
  refine ⟨hunit.1, ?_⟩
  intro n
  have hn := h 1 n
  simpa [translatedCoefficient, productCoefficient, Nat.choose_one_right,
    hunit.2, Nat.add_comm] using hn

theorem normalized_first (a : Nat → K) (h : Normalized a) : a 1 = 1 := by
  have hn := h.2 0
  simpa [h.1] using hn

theorem normalized_factorial (a : Nat → K) (h : Normalized a) (n : Nat) :
    a n = 1 / (n.factorial : K) := by
  induction n with
  | zero => simpa using h.1
  | succ n ih =>
    have hne : (n + 1 : K) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
    have hn := h.2 n
    rw [ih] at hn
    apply mul_left_cancel₀ hne
    rw [hn, Nat.factorial_succ]
    push_cast
    have hf : (n.factorial : K) ≠ 0 := by exact_mod_cast n.factorial_ne_zero
    field_simp [hne, hf]

theorem inverse_factorial_binomial (m n : Nat) :
    (((m + n).choose m : Nat) : K) * (1 / ((m + n).factorial : K)) =
      (1 / (m.factorial : K)) * (1 / (n.factorial : K)) := by
  have hfactor : (((m + n).choose m : Nat) : K) * (m.factorial : K) *
      (n.factorial : K) = ((m + n).factorial : K) := by
    have h := Nat.add_choose_mul_factorial_mul_factorial m n
    rw [← Nat.choose_symm_add] at h
    exact_mod_cast h
  have hm : (m.factorial : K) ≠ 0 := by exact_mod_cast m.factorial_ne_zero
  have hn : (n.factorial : K) ≠ 0 := by exact_mod_cast n.factorial_ne_zero
  have hmn : ((m + n).factorial : K) ≠ 0 := by
    exact_mod_cast (m + n).factorial_ne_zero
  field_simp
  simpa only [mul_assoc] using hfactor

theorem semigroup_from_recurrence (a : Nat → K) (h : Normalized a) :
    SemigroupLaw a := by
  intro m n
  simp only [translatedCoefficient, productCoefficient, normalized_factorial a h]
  exact inverse_factorial_binomial m n

theorem normalized_iff_unit_semigroup (a : Nat → K) :
    Normalized a ↔ UnitGenerator a ∧ SemigroupLaw a := by
  constructor
  · intro h
    exact ⟨⟨h.1, normalized_first a h⟩, semigroup_from_recurrence a h⟩
  · rintro ⟨hu, hs⟩
    exact recurrence_from_semigroup a hs hu

theorem coefficient_semigroup : SemigroupLaw coefficient :=
  semigroup_from_recurrence coefficient coefficient_normalized

theorem coefficient_unit_generator : UnitGenerator coefficient :=
  ⟨coefficient_zero, normalized_first coefficient coefficient_normalized⟩

theorem unique_normalized_formal_propagation (a : Nat → ℚ)
    (hu : UnitGenerator a) (hs : SemigroupLaw a) : a = coefficient :=
  coefficient_unique a (recurrence_from_semigroup a hs hu)

theorem semigroup_real_hasSum (a : Nat → ℝ)
    (hu : UnitGenerator a) (hs : SemigroupLaw a) : HasSum a value :=
  normalized_real_hasSum a (recurrence_from_semigroup a hs hu)

/-- The actual one-variable formal series is built from the produced coefficients. -/
def series : PowerSeries ℚ := PowerSeries.mk coefficient

theorem series_coefficient (n : Nat) :
    PowerSeries.coeff ℚ n series = coefficient n := by
  simp [series]

theorem series_derivative : PowerSeries.derivative ℚ series = series := by
  ext n
  rw [PowerSeries.coeff_derivative, series_coefficient, series_coefficient, mul_comm]
  exact coefficient_recurrence n

theorem recurrence_from_formal_derivative (f : PowerSeries K)
    (h0 : PowerSeries.coeff K 0 f = 1)
    (hd : PowerSeries.derivative K f = f) :
    Normalized (fun n => PowerSeries.coeff K n f) := by
  refine ⟨h0, ?_⟩
  intro n
  have h := congrArg (PowerSeries.coeff K n) hd
  simpa only [PowerSeries.coeff_derivative, mul_comm] using h

theorem formal_series_unique (f : PowerSeries ℚ)
    (h0 : PowerSeries.coeff ℚ 0 f = 1)
    (hd : PowerSeries.derivative ℚ f = f) : f = series := by
  have h := coefficient_unique (fun n => PowerSeries.coeff ℚ n f)
    (recurrence_from_formal_derivative f h0 hd)
  ext n
  rw [series_coefficient]
  exact congrFun h n

theorem series_translation_coefficients (m n : Nat) :
    translatedCoefficient (fun k => PowerSeries.coeff ℚ k series) m n =
      productCoefficient (fun k => PowerSeries.coeff ℚ k series) m n := by
  simpa only [series_coefficient] using coefficient_semigroup m n

end PropagationSemigroup
end

#print axioms PropagationSemigroup.recurrence_from_semigroup
#print axioms PropagationSemigroup.normalized_first
#print axioms PropagationSemigroup.normalized_factorial
#print axioms PropagationSemigroup.inverse_factorial_binomial
#print axioms PropagationSemigroup.semigroup_from_recurrence
#print axioms PropagationSemigroup.normalized_iff_unit_semigroup
#print axioms PropagationSemigroup.coefficient_semigroup
#print axioms PropagationSemigroup.coefficient_unit_generator
#print axioms PropagationSemigroup.unique_normalized_formal_propagation
#print axioms PropagationSemigroup.semigroup_real_hasSum
#print axioms PropagationSemigroup.series_coefficient
#print axioms PropagationSemigroup.series_derivative
#print axioms PropagationSemigroup.recurrence_from_formal_derivative
#print axioms PropagationSemigroup.formal_series_unique
#print axioms PropagationSemigroup.series_translation_coefficients
