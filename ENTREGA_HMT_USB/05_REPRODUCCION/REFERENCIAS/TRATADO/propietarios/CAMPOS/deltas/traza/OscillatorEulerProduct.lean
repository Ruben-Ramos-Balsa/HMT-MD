import Mathlib.RingTheory.PowerSeries.Inverse
import Mathlib.RingTheory.PowerSeries.Trunc
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

/-!
Formal oscillator Euler products at arbitrary degree. Every positive mode
contributes `(1 + X^n)⁻¹` per colour. Finite products stabilize coefficientwise,
giving an actual formal power series, without an analytic convergence premise.
This is not an identification of an FLM module or of a Moonshine character.
-/

noncomputable section
namespace HMT.IV.OscillatorEulerProduct

open PowerSeries

abbrev Series := PowerSeries ℂ

/-- Equality of all coefficients through degree d, including degree zero. -/
def AgreeThrough (d : ℕ) (f g : Series) : Prop :=
  ∀ k ≤ d, coeff ℂ k f = coeff ℂ k g

theorem agreeThrough_refl (d : ℕ) (f : Series) : AgreeThrough d f f :=
  fun _ _ => rfl

theorem agreeThrough_mul {d : ℕ} {f f' g g' : Series}
    (hf : AgreeThrough d f f') (hg : AgreeThrough d g g') :
    AgreeThrough d (f * g) (f' * g') := by
  intro k hk
  simp only [coeff_mul]
  apply Finset.sum_congr rfl
  intro p hp
  have hp' := Finset.mem_antidiagonal.mp hp
  rw [hf p.1 (by omega), hg p.2 (by omega)]

theorem agreeThrough_pow {d : ℕ} {f g : Series}
    (h : AgreeThrough d f g) (r : ℕ) : AgreeThrough d (f ^ r) (g ^ r) := by
  induction r with
  | zero => exact agreeThrough_refl d 1
  | succ r ih => simpa only [pow_succ] using agreeThrough_mul ih h

theorem agreeThrough_trunc {d : ℕ} {f g : Series} (h : AgreeThrough d f g) :
    PowerSeries.trunc (d+1) f = PowerSeries.trunc (d+1) g := by
  apply Polynomial.ext
  intro k
  simp only [coeff_trunc]
  split_ifs with hk
  · exact h k (by omega)
  · rfl

/-- The index n denotes the positive oscillator mode n+1. -/
def modeFactor (n : ℕ) : Series := (1 + X ^ (n+1))⁻¹

theorem modeFactor_inverse (n : ℕ) :
    modeFactor n * (1 + X ^ (n+1)) = 1 := by
  apply PowerSeries.inv_mul_cancel
  simp

theorem modeFactor_agrees_one (n d : ℕ) (hd : d ≤ n) :
    AgreeThrough d (modeFactor n) 1 := by
  intro k hk
  have h := congrArg (coeff ℂ k) (modeFactor_inverse n)
  rw [mul_add, mul_one, map_add, coeff_mul_X_pow'] at h
  simpa only [if_neg (by omega : ¬ n+1 ≤ k), add_zero] using h

theorem modeFactor_coefficient_zero (n : ℕ) : coeff ℂ 0 (modeFactor n) = 1 := by
  simpa using modeFactor_agrees_one n 0 (Nat.zero_le n) 0 le_rfl

/-- Adding one occupation of mode n+1 reverses its sign. -/
theorem modeFactor_coefficient_step (n d : ℕ) :
    coeff ℂ (d+(n+1)) (modeFactor n) = -coeff ℂ d (modeFactor n) := by
  have h := congrArg (coeff ℂ (d+(n+1))) (modeFactor_inverse n)
  rw [mul_add, mul_one, map_add, coeff_mul_X_pow'] at h
  have hn : n+1 ≤ d+(n+1) := by omega
  have hz : d+(n+1) ≠ 0 := by omega
  simp only [if_pos hn, Nat.add_sub_cancel, coeff_one, if_neg hz] at h
  exact eq_neg_of_add_eq_zero_left h

/-- The coefficient records the occupation number when the total degree is
a multiple of the positive mode, and vanishes otherwise. -/
theorem modeFactor_coefficient (n d : ℕ) :
    coeff ℂ d (modeFactor n) =
      if (n+1) ∣ d then (-1 : ℂ) ^ (d / (n+1)) else 0 := by
  induction d using Nat.strong_induction_on with
  | h d ih =>
    by_cases hd : d < n+1
    · have heq := modeFactor_agrees_one n d (by omega) d le_rfl
      by_cases hz : d = 0
      · subst d
        simp [modeFactor_coefficient_zero]
      · rw [heq, coeff_one, if_neg hz, if_neg]
        intro hdiv
        have := Nat.le_of_dvd (Nat.pos_of_ne_zero hz) hdiv
        omega
    · have hle : n+1 ≤ d := by omega
      have hsmall : d-(n+1) < d := by omega
      have heq : d = (d-(n+1))+(n+1) := by omega
      rw [heq, modeFactor_coefficient_step]
      rw [ih _ hsmall]
      have hdiv : (n+1) ∣ d-(n+1)+(n+1) ↔ (n+1) ∣ d-(n+1) := by
        simp
      rw [if_congr hdiv rfl rfl]
      have hquot : (d-(n+1)+(n+1))/(n+1) = (d-(n+1))/(n+1)+1 := by
        exact Nat.add_div_right _ (by omega)
      rw [hquot]
      split_ifs
      · rw [pow_succ]
        ring
      · simp

/-- r independent colours contribute the r-th power at each positive mode. -/
def colouredFactor (r n : ℕ) : Series := modeFactor n ^ r

theorem colouredFactor_inverse (r n : ℕ) :
    colouredFactor r n * (1 + X ^ (n+1)) ^ r = 1 := by
  simpa only [colouredFactor, mul_pow, one_pow] using
    congrArg (fun f : Series => f ^ r) (modeFactor_inverse n)

theorem colouredFactor_agrees_one (r n d : ℕ) (hd : d ≤ n) :
    AgreeThrough d (colouredFactor r n) 1 := by
  simpa only [one_pow, colouredFactor] using agreeThrough_pow (modeFactor_agrees_one n d hd) r

/-- All positive modes 1,...,N with r colours. -/
def finiteProduct (r N : ℕ) : Series :=
  ∏ n ∈ Finset.range N, colouredFactor r n

theorem finiteProduct_zero (r : ℕ) : finiteProduct r 0 = 1 := by
  simp [finiteProduct]

theorem finiteProduct_succ (r N : ℕ) :
    finiteProduct r (N+1) = finiteProduct r N * colouredFactor r N := by
  exact Finset.prod_range_succ _ _

theorem finiteProduct_step (r d N : ℕ) (hd : d ≤ N) :
    AgreeThrough d (finiteProduct r (N+1)) (finiteProduct r N) := by
  rw [finiteProduct_succ]
  simpa only [mul_one] using
    agreeThrough_mul (agreeThrough_refl d (finiteProduct r N))
      (colouredFactor_agrees_one r N d hd)

/-- Exact coefficient compatibility for arbitrary finite cuts. -/
theorem finiteProduct_compatible (r d N M : ℕ) (hd : d ≤ N) (hNM : N ≤ M) :
    AgreeThrough d (finiteProduct r M) (finiteProduct r N) := by
  induction M, hNM using Nat.le_induction with
  | base => exact agreeThrough_refl d (finiteProduct r N)
  | succ M hNM ih =>
    intro k hk
    exact (finiteProduct_step r d M (hd.trans hNM) k hk).trans (ih k hk)

/-- Coefficientwise limit of the oscillator product. Its d-th coefficient
is computed from exactly the first d positive modes. -/
def oscillatorProduct (r : ℕ) : Series :=
  PowerSeries.mk fun d => coeff ℂ d (finiteProduct r d)

theorem oscillatorProduct_coefficient (r d N : ℕ) (hd : d ≤ N) :
    coeff ℂ d (oscillatorProduct r) = coeff ℂ d (finiteProduct r N) := by
  rw [oscillatorProduct, coeff_mk]
  exact (finiteProduct_compatible r d d N le_rfl hd d le_rfl).symm

theorem oscillatorProduct_agrees_cut (r d N : ℕ) (hd : d ≤ N) :
    AgreeThrough d (oscillatorProduct r) (finiteProduct r N) := by
  intro k hk
  exact oscillatorProduct_coefficient r k N (hk.trans hd)

theorem oscillatorProduct_trunc (r d N : ℕ) (hd : d ≤ N) :
    PowerSeries.trunc (d+1) (oscillatorProduct r) =
      PowerSeries.trunc (d+1) (finiteProduct r N) :=
  agreeThrough_trunc (oscillatorProduct_agrees_cut r d N hd)

theorem oscillatorProduct_unique (r : ℕ) (f : Series)
    (h : ∀ d, AgreeThrough d f (finiteProduct r d)) : f = oscillatorProduct r := by
  apply PowerSeries.ext
  intro d
  exact (h d d le_rfl).trans (oscillatorProduct_coefficient r d d le_rfl).symm

theorem oscillatorProduct_constant (r : ℕ) :
    coeff ℂ 0 (oscillatorProduct r) = 1 := by
  rw [oscillatorProduct_coefficient r 0 0 le_rfl, finiteProduct_zero]
  simp

end HMT.IV.OscillatorEulerProduct
end

#print axioms HMT.IV.OscillatorEulerProduct.modeFactor_inverse
#print axioms HMT.IV.OscillatorEulerProduct.modeFactor_agrees_one
#print axioms HMT.IV.OscillatorEulerProduct.modeFactor_coefficient
#print axioms HMT.IV.OscillatorEulerProduct.colouredFactor_inverse
#print axioms HMT.IV.OscillatorEulerProduct.finiteProduct_compatible
#print axioms HMT.IV.OscillatorEulerProduct.oscillatorProduct_coefficient
#print axioms HMT.IV.OscillatorEulerProduct.oscillatorProduct_trunc
#print axioms HMT.IV.OscillatorEulerProduct.oscillatorProduct_unique
