import AutoscaleLimit
import RadixCellSelection
import Mathlib.Tactic

/-!
# Rational brackets of the generated modal auto-scale

Both quotient endpoints are read from ModalIncidence.sequence.  No square
root bisection, target real number, or independently defined Fibonacci
sequence generates them.  The previously proved analytic recognition is
used to certify the enclosure and the posterior positional publication.
-/

noncomputable section
open Filter Topology

namespace AutoscaleBrackets

open AutoscaleLimit

/-- Loop state before its k-th update; the source starts with (1,1). -/
def cursorPair (k : Nat) : Int × Int :=
  (ModalIncidence.sequence (k + 1), ModalIncidence.sequence (k + 2))

def ratioQ (k : Nat) : ℚ := ((cursorPair k).2 : ℚ) / ((cursorPair k).1 : ℚ)

def lowerQ (k : Nat) : ℚ := min (ratioQ k) (ratioQ (k + 1))
def upperQ (k : Nat) : ℚ := max (ratioQ k) (ratioQ (k + 1))

theorem cursorPair_zero : cursorPair 0 = (1, 1) := by
  simp [cursorPair, ModalIncidence.sequence_recurrence,
    ModalIncidence.sequence_zero, ModalIncidence.sequence_one]

theorem cursorPair_next (k : Nat) :
    cursorPair (k + 1) = ((cursorPair k).2, (cursorPair k).1 + (cursorPair k).2) := by
  apply Prod.ext
  · rfl
  · exact ModalIncidence.sequence_recurrence (k + 1)

theorem initial_bracket : lowerQ 0 = 1 ∧ upperQ 0 = 2 := by
  norm_num [lowerQ, upperQ, ratioQ, cursorPair, ModalIncidence.sequence_recurrence,
    ModalIncidence.sequence_zero, ModalIncidence.sequence_one]

theorem ratio_cast (k : Nat) : (ratioQ k : ℝ) = AutoscaleLimit.ratio k := by
  simp [ratioQ, cursorPair, AutoscaleLimit.ratio, AutoscaleLimit.emitted]

theorem lower_cast (k : Nat) : (lowerQ k : ℝ) =
    min (AutoscaleLimit.ratio k) (AutoscaleLimit.ratio (k + 1)) := by
  simp [lowerQ, ratio_cast]

theorem upper_cast (k : Nat) : (upperQ k : ℝ) =
    max (AutoscaleLimit.ratio k) (AutoscaleLimit.ratio (k + 1)) := by
  simp [upperQ, ratio_cast]

theorem ratioQ_positive (k : Nat) : 0 < ratioQ k := by
  have h : (0 : ℝ) < ratioQ k := by rw [ratio_cast]; exact AutoscaleLimit.ratio_positive k
  exact_mod_cast h

theorem lowerQ_positive (k : Nat) : 0 < lowerQ k :=
  lt_min (ratioQ_positive k) (ratioQ_positive (k + 1))

theorem upperQ_positive (k : Nat) : 0 < upperQ k :=
  (ratioQ_positive k).trans_le (le_max_left _ _)

theorem consecutive_error_product (k : Nat) :
    (AutoscaleLimit.ratio k - goldenRatio) * (AutoscaleLimit.ratio (k + 1) - goldenRatio) =
      (goldenConj ^ (k + 1))^2 * goldenConj /
        (AutoscaleLimit.emitted (k + 1) * AutoscaleLimit.emitted (k + 2)) := by
  rw [AutoscaleLimit.ratio_error, AutoscaleLimit.ratio_error,
    pow_succ goldenConj (k + 1), div_mul_div_comm]
  ring

theorem consecutive_straddle (k : Nat) :
    (AutoscaleLimit.ratio k - goldenRatio) * (AutoscaleLimit.ratio (k + 1) - goldenRatio) < 0 := by
  rw [consecutive_error_product]
  apply div_neg_of_neg_of_pos
  · exact mul_neg_of_pos_of_neg
      (sq_pos_of_ne_zero (pow_ne_zero _ goldConj_ne_zero)) goldConj_neg
  · exact mul_pos (AutoscaleLimit.emitted_positive k)
      (AutoscaleLimit.emitted_positive (k + 1))

theorem rational_bracket (k : Nat) :
    (lowerQ k : ℝ) < goldenRatio ∧ goldenRatio < (upperQ k : ℝ) := by
  rw [lower_cast, upper_cast]
  rcases mul_neg_iff.mp (consecutive_straddle k) with h | h
  · exact ⟨(min_le_right _ _).trans_lt (by linarith [h.2]),
      (show goldenRatio < AutoscaleLimit.ratio k by linarith [h.1]).trans_le
        (le_max_left _ _)⟩
  · exact ⟨(min_le_left _ _).trans_lt (by linarith [h.1]),
      (show goldenRatio < AutoscaleLimit.ratio (k + 1) by linarith [h.2]).trans_le
        (le_max_right _ _)⟩

theorem polynomial_signs (k : Nat) :
    lowerQ k * lowerQ k - lowerQ k - 1 < 0 ∧
      0 < upperQ k * upperQ k - upperQ k - 1 := by
  have hb := rational_bracket k
  have hl : (0 : ℝ) < lowerQ k := by exact_mod_cast lowerQ_positive k
  have hu : (0 : ℝ) < upperQ k := by exact_mod_cast upperQ_positive k
  have hlprod : ((lowerQ k : ℝ) - goldenRatio) * ((lowerQ k : ℝ) + goldenRatio - 1) < 0 :=
    mul_neg_of_neg_of_pos (sub_neg.mpr hb.1) (by linarith [one_lt_gold])
  have huprod : 0 < ((upperQ k : ℝ) - goldenRatio) * ((upperQ k : ℝ) + goldenRatio - 1) :=
    mul_pos (sub_pos.mpr hb.2) (by linarith [one_lt_gold])
  have hL : (lowerQ k : ℝ) * lowerQ k - lowerQ k - 1 < 0 := by
    nlinarith [gold_sq]
  have hU : (0 : ℝ) < (upperQ k : ℝ) * upperQ k - upperQ k - 1 := by
    nlinarith [gold_sq]
  exact ⟨by exact_mod_cast hL, by exact_mod_cast hU⟩

theorem lower_tendsto : Tendsto (fun k => (lowerQ k : ℝ)) atTop (𝓝 goldenRatio) := by
  have hnext := AutoscaleLimit.ratio_tendsto.comp (tendsto_add_atTop_nat 1)
  simpa only [lower_cast, Function.comp_def, min_self] using
    AutoscaleLimit.ratio_tendsto.min hnext

theorem upper_tendsto : Tendsto (fun k => (upperQ k : ℝ)) atTop (𝓝 goldenRatio) := by
  have hnext := AutoscaleLimit.ratio_tendsto.comp (tendsto_add_atTop_nat 1)
  simpa only [upper_cast, Function.comp_def, max_self] using
    AutoscaleLimit.ratio_tendsto.max hnext

theorem width_positive (k : Nat) : 0 < upperQ k - lowerQ k := by
  have h : (lowerQ k : ℝ) < upperQ k := (rational_bracket k).1.trans (rational_bracket k).2
  exact sub_pos.mpr (by exact_mod_cast h)

theorem emitted_cassini (n : Nat) :
    emitted (n + 1) * emitted (n + 1) - emitted n * emitted (n + 2) =
      (-1 : ℝ) ^ n := by
  unfold emitted
  exact_mod_cast ModalIncidence.cassini n

theorem ratio_succ_sub (n : Nat) :
    ratio (n + 1) - ratio n =
      -((-1 : ℝ) ^ (n + 1)) / (emitted (n + 1) * emitted (n + 2)) := by
  have hc := emitted_cassini (n + 1)
  simp only [Nat.add_assoc, Nat.reduceAdd] at hc
  unfold ratio
  simp only [Nat.add_assoc, Nat.reduceAdd]
  have h1 : emitted (n + 1) ≠ 0 := ne_of_gt (emitted_positive n)
  have h2 : emitted (n + 2) ≠ 0 := ne_of_gt (emitted_positive (n + 1))
  calc
    emitted (n + 3) / emitted (n + 2) - emitted (n + 2) / emitted (n + 1) =
        (emitted (n + 1) * emitted (n + 3) - emitted (n + 2) * emitted (n + 2)) /
          (emitted (n + 1) * emitted (n + 2)) := by field_simp; ring
    _ = _ := by congr 1; linarith

theorem ratio_gap_exact (n : Nat) :
    |ratio (n + 1) - ratio n| =
      1 / (emitted (n + 1) * emitted (n + 2)) := by
  rw [ratio_succ_sub, abs_div, abs_neg, abs_pow]
  norm_num [abs_of_pos (mul_pos (emitted_positive n) (emitted_positive (n + 1)))]

theorem width_exact (n : Nat) : ((upperQ n - lowerQ n : ℚ) : ℝ) =
    1 / (emitted (n + 1) * emitted (n + 2)) := by
  rw [Rat.cast_sub, upper_cast, lower_cast, max_sub_min_eq_abs, ratio_gap_exact]

theorem width_tendsto_zero :
    Tendsto (fun k => ((upperQ k - lowerQ k : ℚ) : ℝ)) atTop (𝓝 0) := by
  simpa only [Rat.cast_sub, sub_self] using upper_tendsto.sub lower_tendsto

theorem exists_precision_index (scale : Nat) :
    ∃ k : Nat, (upperQ k - lowerQ k) * scale < 1 := by
  have hlim : Tendsto
      (fun k => ((upperQ k - lowerQ k : ℚ) : ℝ) * scale) atTop (𝓝 0) := by
    simpa only [zero_mul] using width_tendsto_zero.mul_const (scale : ℝ)
  have hevent : ∀ᶠ k in atTop, ((upperQ k - lowerQ k : ℚ) : ℝ) * scale < 1 :=
    (tendsto_order.mp hlim).2 1 (by norm_num)
  obtain ⟨k, hk⟩ := hevent.exists
  exact ⟨k, by exact_mod_cast hk⟩

theorem eventual_single_cell (scale : Nat) (hs : 0 < scale) :
    ∃ N : Nat, ∀ k, N ≤ k →
      RadixCellSelection.first (lowerQ k) scale = RadixCellSelection.cell goldenRatio scale ∧
      RadixCellSelection.last (upperQ k) scale = RadixCellSelection.cell goldenRatio scale := by
  apply RadixCellSelection.eventual_single_cell _ _ _ scale hs
    (fun k => ⟨(rational_bracket k).1.le, (rational_bracket k).2.le⟩)
    lower_tendsto upper_tendsto
  exact RadixCellSelection.golden_avoids_boundary scale hs

end AutoscaleBrackets
end

#print axioms AutoscaleBrackets.cursorPair_zero
#print axioms AutoscaleBrackets.cursorPair_next
#print axioms AutoscaleBrackets.initial_bracket
#print axioms AutoscaleBrackets.ratio_cast
#print axioms AutoscaleBrackets.lower_cast
#print axioms AutoscaleBrackets.upper_cast
#print axioms AutoscaleBrackets.ratioQ_positive
#print axioms AutoscaleBrackets.lowerQ_positive
#print axioms AutoscaleBrackets.upperQ_positive
#print axioms AutoscaleBrackets.consecutive_error_product
#print axioms AutoscaleBrackets.consecutive_straddle
#print axioms AutoscaleBrackets.rational_bracket
#print axioms AutoscaleBrackets.polynomial_signs
#print axioms AutoscaleBrackets.lower_tendsto
#print axioms AutoscaleBrackets.upper_tendsto
#print axioms AutoscaleBrackets.width_positive
#print axioms AutoscaleBrackets.emitted_cassini
#print axioms AutoscaleBrackets.ratio_succ_sub
#print axioms AutoscaleBrackets.ratio_gap_exact
#print axioms AutoscaleBrackets.width_exact
#print axioms AutoscaleBrackets.width_tendsto_zero
#print axioms AutoscaleBrackets.exists_precision_index
#print axioms AutoscaleBrackets.eventual_single_cell
