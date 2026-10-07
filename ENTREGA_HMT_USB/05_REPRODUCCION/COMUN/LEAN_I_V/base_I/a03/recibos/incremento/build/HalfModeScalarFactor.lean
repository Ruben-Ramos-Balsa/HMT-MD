import Mathlib.Data.Complex.Basic
import Mathlib.RingTheory.PowerSeries.Derivative
import Mathlib.RingTheory.PowerSeries.WellKnown
import Mathlib.Tactic

/-!
Formal scalar-factor library. The exponential is constructed by its universal
coefficient recurrence, independently of the rational identity proved below.
No analytic convergence or application to fields is asserted here.
-/

namespace HMT.Formal.HalfModeScalarFactor

open PowerSeries
open scoped BigOperators

noncomputable section

abbrev Series := PowerSeries ℂ

/-- Coefficient construction of the normalized formal exponential.
The constant coefficient of the argument is discarded; the intended domain
is the ideal of power series with zero constant coefficient. -/
def expCoeff (s : Series) : ℕ → ℂ
  | 0 => 1
  | n + 1 =>
    (∑ k ∈ Finset.range (n + 1),
      (coeff ℂ (k + 1) s * (k + 1)) * expCoeff s (n - k)) / (n + 1)
termination_by n => n
decreasing_by omega

def formalExp (s : Series) : Series := mk (expCoeff s)

@[simp] theorem coeff_formalExp (s : Series) (n : ℕ) :
    coeff ℂ n (formalExp s) = expCoeff s n := coeff_mk _ _

@[simp] theorem constantCoeff_formalExp (s : Series) :
    constantCoeff ℂ (formalExp s) = 1 := by
  rw [← coeff_zero_eq_constantCoeff_apply, coeff_formalExp, expCoeff]

theorem formalExp_derivative (s : Series) :
    derivative ℂ (formalExp s) = derivative ℂ s * formalExp s := by
  ext n
  rw [coeff_derivative, coeff_formalExp, expCoeff]
  rw [div_mul_cancel₀ _ (by exact_mod_cast Nat.succ_ne_zero n)]
  rw [coeff_mul, Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
  apply Finset.sum_congr rfl
  intro k _
  simp only [coeff_derivative, coeff_formalExp]

/-- Uniqueness of the formal exponential's normalized initial-value problem. -/
theorem formalExp_unique (s f : Series)
    (hc : constantCoeff ℂ f = 1)
    (hd : derivative ℂ f = derivative ℂ s * f) : f = formalExp s := by
  ext n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    cases n with
    | zero => simpa only [coeff_zero_eq_constantCoeff, constantCoeff_formalExp] using hc
    | succ n =>
      apply mul_right_cancel₀ (show (n + 1 : ℂ) ≠ 0 by exact_mod_cast Nat.succ_ne_zero n)
      rw [← coeff_derivative, ← coeff_derivative, hd, formalExp_derivative]
      simp only [coeff_mul, Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
      apply Finset.sum_congr rfl
      intro k _
      rw [ih (n - k) (by omega)]

@[simp] theorem formalExp_zero : formalExp (0 : Series) = 1 := by
  symm
  apply formalExp_unique
  · simp
  · simp

theorem formalExp_add (s t : Series) :
    formalExp (s + t) = formalExp s * formalExp t := by
  symm
  apply formalExp_unique
  · simp
  · rw [Derivation.leibniz, map_add, formalExp_derivative, formalExp_derivative]
    simp only [smul_eq_mul]
    ring

theorem formalExp_nsmul (s : Series) (n : ℕ) :
    formalExp (n • s) = formalExp s ^ n := by
  induction n with
  | zero => simp
  | succ n ih => rw [succ_nsmul, formalExp_add, ih, pow_succ]

/-- The constructed exponential is always a unit, with opposite argument
giving its inverse. -/
def formalExpUnit (s : Series) : Seriesˣ where
  val := formalExp s
  inv := formalExp (-s)
  val_inv := by rw [← formalExp_add, add_neg_cancel, formalExp_zero]
  inv_val := by rw [← formalExp_add, neg_add_cancel, formalExp_zero]

@[simp] theorem coe_formalExpUnit (s : Series) :
    (formalExpUnit s : Series) = formalExp s := rfl

theorem formalExpUnit_add (s t : Series) :
    formalExpUnit (s + t) = formalExpUnit s * formalExpUnit t := by
  apply Units.ext
  exact formalExp_add s t

/-- An additive-to-multiplicative morphism packages all integer powers. -/
def formalExpHom : Multiplicative Series →* Seriesˣ where
  toFun s := formalExpUnit s.toAdd
  map_one' := by apply Units.ext; exact formalExp_zero
  map_mul' s t := formalExpUnit_add s.toAdd t.toAdd

theorem formalExp_zsmul (s : Series) (z : ℤ) :
    formalExp (z • s) = ((formalExpUnit s) ^ z : Seriesˣ) := by
  have h := congrArg (fun u : Seriesˣ => (u : Series))
    (map_zpow formalExpHom (Multiplicative.ofAdd s) z)
  exact h

theorem derivative_mathlib_exp :
    derivative ℂ (PowerSeries.exp ℂ) = PowerSeries.exp ℂ := by
  ext n
  simp only [coeff_derivative, coeff_exp, Nat.factorial_succ]
  push_cast
  have hn : (n + 1 : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
  have hf : (n.factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero n
  field_simp [hn, hf]

/-- The recurrence construction agrees with Mathlib's factorial series at `X`. -/
theorem formalExp_X : formalExp (X : Series) = PowerSeries.exp ℂ := by
  symm
  apply formalExp_unique
  · exact PowerSeries.constantCoeff_exp
  · rw [derivative_X, one_mul]
    exact derivative_mathlib_exp

/-- The odd half-mode scalar series, with coefficient `-2/n` in odd degree. -/
def S : Series := mk fun n => ((-1 : ℂ) ^ n - 1) / n

@[simp] theorem coeff_S (n : ℕ) :
    coeff ℂ n S = ((-1 : ℂ) ^ n - 1) / n := coeff_mk _ _

@[simp] theorem constantCoeff_S : constantCoeff ℂ S = 0 := by
  simp [← coeff_zero_eq_constantCoeff_apply]

theorem coeff_S_even (n : ℕ) : coeff ℂ (2 * n) S = 0 := by
  simp [pow_mul]

theorem coeff_S_odd (n : ℕ) :
    coeff ℂ (2 * n + 1) S = -2 / (2 * n + 1 : ℂ) := by
  norm_num [pow_add, pow_mul]

theorem coeff_derivative_S (n : ℕ) :
    coeff ℂ n (derivative ℂ S) = (-1 : ℂ) ^ (n + 1) - 1 := by
  rw [coeff_derivative, coeff_S, Nat.cast_add, Nat.cast_one]
  exact div_mul_cancel₀ _ (by exact_mod_cast Nat.succ_ne_zero n)

theorem derivative_S_cleared :
    derivative ℂ S * (1 - X ^ 2) = C ℂ (-2) := by
  ext n
  rw [mul_sub, mul_one, map_sub]
  cases n with
  | zero => norm_num [coeff_derivative_S, coeff_mul_X_pow']
  | succ n =>
    cases n with
    | zero => simp [coeff_derivative_S, coeff_mul_X_pow']
    | succ n =>
      rw [show n + 1 + 1 = n + 2 by omega, coeff_mul_X_pow]
      simp [coeff_derivative_S, pow_add]

theorem derivative_S :
    derivative ℂ S = C ℂ (-2) * (1 - X ^ 2 : Series)⁻¹ := by
  have h : constantCoeff ℂ (1 - X ^ 2 : Series) ≠ 0 := by simp
  calc
    derivative ℂ S = derivative ℂ S * ((1 - X ^ 2) * (1 - X ^ 2 : Series)⁻¹) := by
      rw [PowerSeries.mul_inv_cancel _ h, mul_one]
    _ = C ℂ (-2) * (1 - X ^ 2 : Series)⁻¹ := by rw [← mul_assoc, derivative_S_cleared]

/-- The rational expression uses the inverse of the unit `1 + X`. -/
def rationalFactor : Series := (1 - X) * (1 + X : Series)⁻¹

@[simp] theorem constantCoeff_rationalFactor : constantCoeff ℂ rationalFactor = 1 := by
  simp [rationalFactor]

theorem rationalFactor_derivative_cleared :
    derivative ℂ rationalFactor * (1 - X ^ 2) = C ℂ (-2) * rationalFactor := by
  have hq : (1 + X : Series) * (1 + X : Series)⁻¹ = 1 :=
    PowerSeries.mul_inv_cancel _ (by simp)
  simp only [rationalFactor, Derivation.leibniz, derivative_inv', map_add, map_sub,
    Derivation.map_one_eq_zero, derivative_X, zero_add, zero_sub, smul_eq_mul]
  have hc : C ℂ (-2) = (-2 : Series) := by simp only [map_neg, map_ofNat]
  rw [hc]
  linear_combination
    (-((1 - X : Series) * (1 + X : Series)⁻¹ * (1 - X))) * hq

theorem rationalFactor_derivative :
    derivative ℂ rationalFactor = derivative ℂ S * rationalFactor := by
  have hd : (1 - X ^ 2 : Series) ≠ 0 := by
    intro h
    have := congrArg (constantCoeff ℂ) h
    simp at this
  apply mul_right_cancel₀ hd
  rw [rationalFactor_derivative_cleared]
  calc
    C ℂ (-2) * rationalFactor = (derivative ℂ S * (1 - X ^ 2)) * rationalFactor := by
      rw [derivative_S_cleared]
    _ = (derivative ℂ S * rationalFactor) * (1 - X ^ 2) := by ring

/-- Formal exponential identity; no analytic interpretation is needed. -/
theorem formalExp_S :
    formalExp S = (1 - X) * (1 + X : Series)⁻¹ := by
  exact (formalExp_unique S rationalFactor constantCoeff_rationalFactor
    rationalFactor_derivative).symm

theorem formalExp_nsmul_S (n : ℕ) :
    formalExp (n • S) = ((1 - X) * (1 + X : Series)⁻¹) ^ n := by
  rw [formalExp_nsmul, formalExp_S]

def oneMinusXUnit : Seriesˣ := Units.mkOfMulEqOne (1 - X) (1 - X : Series)⁻¹
  (PowerSeries.mul_inv_cancel _ (by simp))

def onePlusXUnit : Seriesˣ := Units.mkOfMulEqOne (1 + X) (1 + X : Series)⁻¹
  (PowerSeries.mul_inv_cancel _ (by simp))

/-- The rational unit is constructed independently from its two factors. -/
def rationalFactorUnit : Seriesˣ := oneMinusXUnit * onePlusXUnit⁻¹

theorem coe_rationalFactorUnit :
    (rationalFactorUnit : Series) = (1 - X) * (1 + X : Series)⁻¹ := rfl

theorem formalExpUnit_S : formalExpUnit S = rationalFactorUnit := by
  apply Units.ext
  exact formalExp_S

theorem formalExp_zsmul_S (z : ℤ) :
    formalExp (z • S) = (rationalFactorUnit ^ z : Seriesˣ) := by
  rw [formalExp_zsmul, formalExpUnit_S]

end

end HMT.Formal.HalfModeScalarFactor
