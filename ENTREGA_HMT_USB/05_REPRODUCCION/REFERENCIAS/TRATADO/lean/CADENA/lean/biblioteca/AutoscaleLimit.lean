import ModalIncidence
import Mathlib.Data.Real.GoldenRatio
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic

/-!
# Limit of the emitted modal incidence ratios

The input sequence is `ModalIncidence.sequence`, emitted by the generated
incidence matrix F = [[0,1],[1,1]].  Neither a real root nor a target ratio
is an input to that sequence.  Identification with `Nat.fib` and the use
of Binet's identity below are posterior proofs about that emitted sequence.

Source: article I, generacion.tex, "Incidencia modal y generación de la
autoescala", and retorno_areal_volumetrico.tex, "Operador de clausura y
límite de los retornos marcados".
-/

noncomputable section
open Filter Topology

namespace AutoscaleLimit

/-- The real publication of the integer sequence, with no real input. -/
def emitted (n : Nat) : ℝ := (ModalIncidence.sequence n : ℝ)

/-- Consecutive positive coordinates; the first denominator is sequence 1. -/
def ratio (n : Nat) : ℝ := emitted (n + 2) / emitted (n + 1)

theorem sequence_pair_eq_fib (n : Nat) :
    ModalIncidence.sequence n = (Nat.fib n : Int) ∧
    ModalIncidence.sequence (n + 1) = (Nat.fib (n + 1) : Int) := by
  induction n with
  | zero => simp [ModalIncidence.sequence_zero, ModalIncidence.sequence_one]
  | succ n ih =>
    refine ⟨ih.2, ?_⟩
    rw [show n + 1 + 1 = n + 2 by omega,
      ModalIncidence.sequence_recurrence, ih.1, ih.2, Nat.fib_add_two]
    simp

theorem sequence_eq_fib (n : Nat) :
    ModalIncidence.sequence n = (Nat.fib n : Int) :=
  (sequence_pair_eq_fib n).1

theorem emitted_eq_fib (n : Nat) : emitted n = (Nat.fib n : ℝ) := by
  simp [emitted, sequence_eq_fib]

theorem emitted_recurrence (n : Nat) :
    emitted (n + 2) = emitted n + emitted (n + 1) := by
  simp only [emitted, ModalIncidence.sequence_recurrence, Int.cast_add]

theorem emitted_positive (n : Nat) : 0 < emitted (n + 1) := by
  unfold emitted
  exact_mod_cast ModalIncidence.sequence_positive n

theorem emitted_ge_one (n : Nat) : 1 ≤ emitted (n + 1) := by
  have h := ModalIncidence.sequence_positive n
  have h' : (1 : Int) ≤ ModalIncidence.sequence (n + 1) := by omega
  unfold emitted
  exact_mod_cast h'

theorem ratio_eq_fib (n : Nat) :
    ratio n = (Nat.fib (n + 2) : ℝ) / (Nat.fib (n + 1) : ℝ) := by
  simp only [ratio, emitted_eq_fib]

theorem ratio_positive (n : Nat) : 0 < ratio n :=
  div_pos (emitted_positive (n + 1)) (emitted_positive n)

/-- Binet's error identity is proved only after the sequence has been emitted. -/
theorem ratio_error (n : Nat) :
    ratio n - goldenRatio = goldenConj ^ (n + 1) / emitted (n + 1) := by
  have h := fib_golden_conj_exp (n + 1)
  rw [← emitted_eq_fib, ← emitted_eq_fib] at h
  calc
    ratio n - goldenRatio =
        (emitted (n + 2) - goldenRatio * emitted (n + 1)) / emitted (n + 1) := by
      rw [sub_div, mul_div_cancel_right₀ _ (ne_of_gt (emitted_positive n))]
      rfl
    _ = goldenConj ^ (n + 1) / emitted (n + 1) := by
      rw [show emitted (n + 2) - goldenRatio * emitted (n + 1) =
        goldenConj ^ (n + 1) by simpa only [Nat.add_assoc] using h]

theorem ratio_error_bound (n : Nat) :
    |ratio n - goldenRatio| ≤ |goldenConj| ^ (n + 1) := by
  rw [ratio_error, abs_div, abs_pow, abs_of_pos (emitted_positive n)]
  exact div_le_self (pow_nonneg (abs_nonneg _) _) (emitted_ge_one n)

theorem conjugate_abs_lt_one : |goldenConj| < 1 := by
  rw [abs_lt]
  exact ⟨neg_one_lt_goldConj, lt_trans goldConj_neg zero_lt_one⟩

/-- Convergence is proved by an explicit geometric bound, not assumed. -/
theorem ratio_tendsto : Tendsto ratio atTop (𝓝 goldenRatio) := by
  rw [tendsto_iff_norm_sub_tendsto_zero]
  apply squeeze_zero (fun _ => norm_nonneg _)
    (fun n => by simpa only [Real.norm_eq_abs] using ratio_error_bound n)
  have h : Tendsto (fun n : Nat => |goldenConj| ^ n) atTop (𝓝 (0 : ℝ)) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one (abs_nonneg _) conjugate_abs_lt_one
  simpa only [pow_succ, zero_mul] using h.mul_const |goldenConj|

theorem positive_root_polynomial :
    0 < goldenRatio ∧ goldenRatio ^ 2 - goldenRatio - 1 = 0 := by
  constructor
  · exact gold_pos
  · nlinarith [gold_sq]

theorem positive_root_unique (x : ℝ) (hx : 0 < x)
    (hpoly : x ^ 2 - x - 1 = 0) : x = goldenRatio := by
  have hprod : (x - goldenRatio) * (x + goldenRatio - 1) = 0 := by
    nlinarith [gold_sq]
  have hp : 0 < x + goldenRatio - 1 := by linarith [one_lt_gold]
  have hz := (mul_eq_zero.mp hprod).resolve_right (ne_of_gt hp)
  linarith

/-- Main theorem: the generated incidence ratios converge to the unique
positive real root.  The theorem has no convergence or spectral hypotheses. -/
theorem generated_autoscale_limit :
    ∃! x : ℝ, 0 < x ∧ x ^ 2 - x - 1 = 0 ∧
      Tendsto ratio atTop (𝓝 x) := by
  refine ⟨goldenRatio, ⟨gold_pos, positive_root_polynomial.2, ratio_tendsto⟩, ?_⟩
  intro x hx
  exact positive_root_unique x hx.1 hx.2.1

/-- The radical is a posterior recognition of the produced limit. -/
theorem limit_radical_recognition :
    Tendsto ratio atTop (𝓝 ((1 + Real.sqrt 5) / 2)) := ratio_tendsto

/-- Real realization of the already generated integer incidence matrix. -/
def realAction (v : ℝ × ℝ) : ℝ × ℝ :=
  ((ModalIncidence.F.aa : ℝ) * v.1 + (ModalIncidence.F.av : ℝ) * v.2,
   (ModalIncidence.F.va : ℝ) * v.1 + (ModalIncidence.F.vv : ℝ) * v.2)

theorem real_action_formula (x y : ℝ) : realAction (x, y) = (y, x + y) := by
  simp [realAction, ModalIncidence.incidence_generated]

theorem positive_eigenray_exists :
    realAction (1, goldenRatio) = (goldenRatio, goldenRatio * goldenRatio) := by
  rw [real_action_formula]
  congr 1
  nlinarith [gold_sq]

theorem positive_eigenray_unique (x lam : ℝ) (hx : 0 < x)
    (h : realAction (1, x) = (lam, lam * x)) :
    x = goldenRatio ∧ lam = goldenRatio := by
  rw [real_action_formula] at h
  have h₁ := congrArg Prod.fst h
  have h₂ := congrArg Prod.snd h
  dsimp at h₁ h₂
  have hr : x = goldenRatio := positive_root_unique x hx (by nlinarith)
  exact ⟨hr, h₁.symm.trans hr⟩

/-- The two-step return ratio is read from the same emitted coordinates. -/
def returnRatio (n : Nat) : ℝ := emitted (n + 1) / emitted (n + 3)

theorem return_ratio_power_entries (n : Nat) :
    returnRatio n = ((ModalIncidence.power (n + 2)).aa : ℝ) /
      ((ModalIncidence.power (n + 2)).vv : ℝ) := by
  have h := ModalIncidence.power_entries (n + 1)
  simp only [Nat.add_assoc] at h
  rw [h]
  rfl

theorem return_ratio_factor (n : Nat) :
    returnRatio n = (ratio n)⁻¹ * (ratio (n + 1))⁻¹ := by
  simp only [returnRatio, ratio, inv_div, Nat.add_assoc]
  field_simp [ne_of_gt (emitted_positive (n + 1))]

theorem return_ratio_tendsto :
    Tendsto returnRatio atTop (𝓝 (goldenRatio ^ 2)⁻¹) := by
  have h₁ := ratio_tendsto.inv₀ gold_ne_zero
  have h₂ := h₁.comp (tendsto_add_atTop_nat 1)
  simpa only [Function.comp_apply, ← return_ratio_factor, ← pow_two, inv_pow]
    using h₁.mul h₂

/-- A boundary mark is applied downstream, once; it does not change F or its sequence. -/
theorem marked_return_tendsto (boundaryMark : ℝ) :
    Tendsto (fun n => boundaryMark * returnRatio n) atTop
      (𝓝 (boundaryMark / goldenRatio ^ 2)) := by
  simpa only [div_eq_mul_inv] using return_ratio_tendsto.const_mul boundaryMark

end AutoscaleLimit
end

#print axioms AutoscaleLimit.sequence_pair_eq_fib
#print axioms AutoscaleLimit.sequence_eq_fib
#print axioms AutoscaleLimit.emitted_eq_fib
#print axioms AutoscaleLimit.emitted_recurrence
#print axioms AutoscaleLimit.emitted_positive
#print axioms AutoscaleLimit.emitted_ge_one
#print axioms AutoscaleLimit.ratio_eq_fib
#print axioms AutoscaleLimit.ratio_positive
#print axioms AutoscaleLimit.ratio_error
#print axioms AutoscaleLimit.ratio_error_bound
#print axioms AutoscaleLimit.conjugate_abs_lt_one
#print axioms AutoscaleLimit.ratio_tendsto
#print axioms AutoscaleLimit.positive_root_polynomial
#print axioms AutoscaleLimit.positive_root_unique
#print axioms AutoscaleLimit.generated_autoscale_limit
#print axioms AutoscaleLimit.limit_radical_recognition
#print axioms AutoscaleLimit.real_action_formula
#print axioms AutoscaleLimit.positive_eigenray_exists
#print axioms AutoscaleLimit.positive_eigenray_unique
#print axioms AutoscaleLimit.return_ratio_power_entries
#print axioms AutoscaleLimit.return_ratio_factor
#print axioms AutoscaleLimit.return_ratio_tendsto
#print axioms AutoscaleLimit.marked_return_tendsto
