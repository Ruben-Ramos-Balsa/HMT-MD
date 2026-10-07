import ClosureAnalytic
import PropagationLimit
import Mathlib.Data.Rat.Floor
import Mathlib.Data.Real.Pi.Irrational
import Mathlib.Data.Real.GoldenRatio
import Mathlib.Tactic

/-!
# Posterior selection of positional cells from rational enclosures

The enclosure and its limit are already produced by a scalar reader.
The result below is a positional publication criterion, not the upstream
TPK selector or its regional prolongation.  The non-boundary condition is
essential: width < one cell is not by itself sufficient.
-/

noncomputable section
open Filter Topology

namespace RadixCellSelection

def first (lower : ℚ) (scale : Nat) : Int := ⌊lower * scale⌋
def last (upper : ℚ) (scale : Nat) : Int := ⌈upper * scale⌉ - 1
def cell (x : ℝ) (scale : Nat) : Int := ⌊x * scale⌋

def AvoidsBoundary (x : ℝ) (scale : Nat) : Prop :=
  ∀ z : Int, x * scale ≠ z

theorem first_real (q : ℚ) (scale : Nat) : first q scale = ⌊(q : ℝ) * scale⌋ := by
  rw [first, ← Rat.floor_cast (α := ℝ)]
  simp

theorem last_real (q : ℚ) (scale : Nat) : last q scale = ⌈(q : ℝ) * scale⌉ - 1 := by
  rw [last, ← Rat.ceil_cast (α := ℝ)]
  simp

theorem cell_strict_lower (x : ℝ) (scale : Nat) (hx : AvoidsBoundary x scale) :
    (cell x scale : ℝ) < x * scale := by
  exact lt_of_le_of_ne (Int.floor_le _) (Ne.symm (hx _))

theorem cell_strict_upper (x : ℝ) (scale : Nat) :
    x * scale < (cell x scale : ℝ) + 1 := Int.lt_floor_add_one _

theorem irrational_avoids_boundary {x : ℝ} (hx : Irrational x)
    (scale : Nat) (hs : 0 < scale) : AvoidsBoundary x scale := by
  intro z
  exact (hx.mul_natCast (Nat.ne_of_gt hs)).ne_int z

/-- A vanishing enclosure width gives both endpoint limits; no limit is assumed twice. -/
theorem bracket_limits_of_width (lower upper : Nat → ℚ) (x : ℝ)
    (hb : ∀ n, (lower n : ℝ) ≤ x ∧ x ≤ (upper n : ℝ))
    (hw : Tendsto (fun n => ((upper n - lower n : ℚ) : ℝ)) atTop (𝓝 0)) :
    Tendsto (fun n => (lower n : ℝ)) atTop (𝓝 x) ∧
      Tendsto (fun n => (upper n : ℝ)) atTop (𝓝 x) := by
  have hw' : Tendsto (fun n => (upper n : ℝ) - (lower n : ℝ)) atTop (𝓝 0) := by
    simpa only [Rat.cast_sub] using hw
  constructor
  · rw [tendsto_iff_norm_sub_tendsto_zero]
    apply squeeze_zero (fun _ => norm_nonneg _) (fun n => ?_) hw'
    rw [Real.norm_eq_abs, abs_of_nonpos (sub_nonpos.mpr (hb n).1)]
    linarith [(hb n).2]
  · rw [tendsto_iff_norm_sub_tendsto_zero]
    apply squeeze_zero (fun _ => norm_nonneg _) (fun n => ?_) hw'
    rw [Real.norm_eq_abs, abs_of_nonneg (sub_nonneg.mpr (hb n).2)]
    linarith [(hb n).1]

/-- The first and last candidate coincide eventually at every non-boundary scale. -/
theorem eventual_single_cell (lower upper : Nat → ℚ) (x : ℝ)
    (scale : Nat) (hs : 0 < scale)
    (hb : ∀ n, (lower n : ℝ) ≤ x ∧ x ≤ (upper n : ℝ))
    (hl : Tendsto (fun n => (lower n : ℝ)) atTop (𝓝 x))
    (hu : Tendsto (fun n => (upper n : ℝ)) atTop (𝓝 x))
    (hx : AvoidsBoundary x scale) :
    ∃ N : Nat, ∀ n, N ≤ n →
      first (lower n) scale = cell x scale ∧ last (upper n) scale = cell x scale := by
  have hsR : (0 : ℝ) < scale := by exact_mod_cast hs
  have hcl := cell_strict_lower x scale hx
  have hcu := cell_strict_upper x scale
  have hL : ∀ᶠ n in atTop, (cell x scale : ℝ) < (lower n : ℝ) * scale :=
    (tendsto_order.mp (hl.mul_const (scale : ℝ))).1 _ hcl
  have hU : ∀ᶠ n in atTop, (upper n : ℝ) * scale < (cell x scale : ℝ) + 1 :=
    (tendsto_order.mp (hu.mul_const (scale : ℝ))).2 _ hcu
  apply eventually_atTop.mp
  filter_upwards [hL, hU] with n hln hun
  have hlo := mul_le_mul_of_nonneg_right (hb n).1 hsR.le
  have hup := mul_le_mul_of_nonneg_right (hb n).2 hsR.le
  constructor
  · rw [first_real]
    exact Int.floor_eq_iff.mpr ⟨hln.le, hlo.trans_lt hcu⟩
  · rw [last_real]
    have hc : ⌈(upper n : ℝ) * scale⌉ = cell x scale + 1 := by
      apply Int.ceil_eq_iff.mpr
      push_cast
      constructor <;> linarith
    rw [hc]
    omega

theorem unique_candidate (lower upper : ℚ) (scale : Nat) (c : Int)
    (hf : first lower scale = c) (hl : last upper scale = c) :
    ∀ z : Int, first lower scale ≤ z ∧ z ≤ last upper scale ↔ z = c := by
  intro z
  rw [hf, hl]
  omega

theorem eventual_unique_candidate (lower upper : Nat → ℚ) (x : ℝ)
    (scale : Nat) (hs : 0 < scale)
    (hb : ∀ n, (lower n : ℝ) ≤ x ∧ x ≤ (upper n : ℝ))
    (hw : Tendsto (fun n => ((upper n - lower n : ℚ) : ℝ)) atTop (𝓝 0))
    (hx : AvoidsBoundary x scale) :
    ∃ N : Nat, ∀ n, N ≤ n → ∀ z : Int,
      first (lower n) scale ≤ z ∧ z ≤ last (upper n) scale ↔ z = cell x scale := by
  obtain ⟨hl, hu⟩ := bracket_limits_of_width lower upper x hb hw
  obtain ⟨N, hN⟩ := eventual_single_cell lower upper x scale hs hb hl hu hx
  exact ⟨N, fun n hn => unique_candidate _ _ _ _ (hN n hn).1 (hN n hn).2⟩

theorem width_alone_not_enough :
    ∃ lower upper : ℚ, lower ≤ 1 ∧ 1 ≤ upper ∧ upper - lower < 1 ∧
      first lower 1 ≠ last upper 1 := by
  refine ⟨3 / 4, 5 / 4, ?_⟩
  norm_num [first, last]

/-- Prefixes are published only from the already determined scalar value. -/
def positionalPrefix (x : ℝ) (base n : Nat) : Nat := ⌊x * (base : ℝ)^n⌋₊

theorem prefix_truncate (x : ℝ) (base n m : Nat) (hb : 0 < base) :
    positionalPrefix x base (n + m) / base^m = positionalPrefix x base n := by
  unfold positionalPrefix
  rw [← Nat.floor_div_natCast]
  congr 1
  push_cast
  rw [pow_add]
  have hbR : (base : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hb
  field_simp
  ring

theorem prefix_step (x : ℝ) (base n : Nat) (hb : 0 < base) :
    positionalPrefix x base (n + 1) / base = positionalPrefix x base n := by
  simpa using prefix_truncate x base n 1 hb

def digit (x : ℝ) (base n : Nat) : Nat := positionalPrefix x base (n + 1) % base

theorem digit_bound (x : ℝ) (base n : Nat) (hb : 0 < base) : digit x base n < base :=
  Nat.mod_lt _ hb

theorem prefix_extend (x : ℝ) (base n : Nat) (hb : 0 < base) :
    positionalPrefix x base (n + 1) = base * positionalPrefix x base n + digit x base n := by
  rw [← prefix_step x base n hb]
  exact (Nat.div_add_mod (positionalPrefix x base (n + 1)) base).symm

theorem prefix_as_cell (x : ℝ) (hx : 0 ≤ x) (base n : Nat) :
    (positionalPrefix x base n : Int) = cell x (base^n) := by
  unfold positionalPrefix cell
  rw [Nat.cast_pow]
  exact Int.natCast_floor_eq_floor (mul_nonneg hx (pow_nonneg (Nat.cast_nonneg _) _))

theorem prefix_child_interval (x : ℝ) (base n : Nat) (hb : 0 < base) :
    base * positionalPrefix x base n ≤ positionalPrefix x base (n + 1) ∧
      positionalPrefix x base (n + 1) < base * positionalPrefix x base n + base := by
  have he := prefix_extend x base n hb
  have hd := digit_bound x base n hb
  omega

/-- The max/min clipping in the executable gate preserves a selected child. -/
theorem clipped_single_cell (lower upper : ℚ) (scale : Nat)
    (parentBase radix c : Int) (hc : parentBase ≤ c ∧ c < parentBase + radix)
    (hf : first lower scale = c) (hl : last upper scale = c) :
    max parentBase (first lower scale) = c ∧
      min (parentBase + radix - 1) (last upper scale) = c := by
  rw [hf, hl]
  constructor <;> omega

theorem closure_irrational : Irrational ClosureAnalytic.value := by
  rw [ClosureAnalytic.value_eq_pi]
  exact irrational_pi

theorem golden_irrational : Irrational goldenRatio := gold_irrational

/-- The factorial-scaled rational partial sum is an integer. -/
theorem scaled_partial_integer (n : Nat) :
    ∃ z : Int, (n.factorial : ℝ) * PropagationLimit.partialSum n = z := by
  refine ⟨∑ k ∈ Finset.range (n + 1), ((n.factorial / k.factorial : Nat) : Int), ?_⟩
  rw [PropagationLimit.partial_factorial, Finset.mul_sum]
  simp only [Int.cast_sum, Int.cast_natCast]
  apply Finset.sum_congr rfl
  intro k hk
  rw [Nat.cast_div (Nat.factorial_dvd_factorial
    (Nat.le_of_lt_succ (Finset.mem_range.mp hk))) (by positivity)]
  ring

theorem scaled_rational_integer (q : ℚ) :
    ∃ n : Nat, 1 ≤ n ∧ ∃ z : Int, (n.factorial : ℝ) * (q : ℝ) = z := by
  let n := q.den + 1
  have hd : q.den ∣ n.factorial := Nat.dvd_factorial q.pos (by dsimp [n]; omega)
  refine ⟨n, by dsimp [n]; omega, ((n.factorial / q.den : Nat) : Int) * q.num, ?_⟩
  rw [Rat.cast_def]
  simp only [Int.cast_mul, Int.cast_natCast]
  rw [Nat.cast_div hd (by exact_mod_cast Nat.ne_of_gt q.pos)]
  ring

theorem scaled_tail_lt_one (n : Nat) (hn : 1 ≤ n) :
    (n.factorial : ℝ) * (PropagationLimit.value - PropagationLimit.partialSum n) < 1 := by
  have hb := (PropagationLimit.rational_bracket n).2
  have hr : PropagationLimit.value - PropagationLimit.partialSum n <
      (n + 2 : ℝ) / ((n + 1)^2 * (n.factorial : ℝ)) := by
    simp only [PropagationLimit.upperQ, PropagationLimit.partialSum,
      PropagationLimit.tailQ, Rat.cast_add, Rat.cast_div, Rat.cast_mul,
      Rat.cast_pow, Rat.cast_natCast, Rat.cast_ofNat] at hb ⊢
    linarith
  have hf : (0 : ℝ) < n.factorial := by positivity
  have hm := mul_lt_mul_of_pos_left hr hf
  have he : (n.factorial : ℝ) *
      ((n + 2 : ℝ) / ((n + 1)^2 * (n.factorial : ℝ))) =
      (n + 2 : ℝ) / (n + 1)^2 := by field_simp; ring
  rw [he] at hm
  have hn' : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hlt : (n + 2 : ℝ) / (n + 1)^2 < 1 := by
    apply (div_lt_one (by positivity)).2
    nlinarith
  exact hm.trans hlt

/-- Irrationality follows from the already proved rational enclosure. -/
theorem propagation_irrational : Irrational PropagationLimit.value := by
  intro ⟨q, hq⟩
  obtain ⟨n, hn, z, hz⟩ := scaled_rational_integer q
  obtain ⟨w, hw⟩ := scaled_partial_integer n
  have he : (n.factorial : ℝ) *
      (PropagationLimit.value - PropagationLimit.partialSum n) = ((z - w : Int) : ℝ) := by
    rw [mul_sub, ← hq, hz, hw]
    push_cast
    rfl
  have hl : (0 : ℝ) < (n.factorial : ℝ) *
      (PropagationLimit.value - PropagationLimit.partialSum n) :=
    mul_pos (by positivity) (sub_pos.mpr (PropagationLimit.partial_lt_value n))
  have hu := scaled_tail_lt_one n hn
  rw [he] at hl hu
  have hlz : (0 : Int) < z - w := by exact_mod_cast hl
  have huz : z - w < (1 : Int) := by exact_mod_cast hu
  omega

theorem exp_one_irrational : Irrational (Real.exp 1) := by
  rw [← PropagationLimit.value_eq_exp_one]
  exact propagation_irrational

theorem closure_eventual_cell (scale : Nat) (hs : 0 < scale) :
    ∃ N : Nat, ∀ n, N ≤ n →
      first (ClosureAnalytic.lowerQ n) scale = cell ClosureAnalytic.value scale ∧
      last (ClosureAnalytic.upperQ n) scale = cell ClosureAnalytic.value scale := by
  have hb := ClosureAnalytic.rational_brackets
  obtain ⟨hl, hu⟩ := bracket_limits_of_width _ _ _ hb ClosureAnalytic.width_tendsto_zero
  apply eventual_single_cell _ _ _ scale hs hb hl hu
  exact irrational_avoids_boundary closure_irrational scale hs

theorem propagation_eventual_cell (scale : Nat) (hs : 0 < scale) :
    ∃ N : Nat, ∀ n, N ≤ n →
      first (PropagationLimit.partialQ n) scale = cell PropagationLimit.value scale ∧
      last (PropagationLimit.upperQ n) scale = cell PropagationLimit.value scale := by
  apply eventual_single_cell _ _ _ scale hs
    (fun n => ⟨(PropagationLimit.rational_bracket n).1.le,
      (PropagationLimit.rational_bracket n).2.le⟩)
    PropagationLimit.partial_tendsto PropagationLimit.upper_tendsto
  exact irrational_avoids_boundary propagation_irrational scale hs

theorem golden_avoids_boundary (scale : Nat) (hs : 0 < scale) :
    AvoidsBoundary goldenRatio scale := irrational_avoids_boundary golden_irrational scale hs

end RadixCellSelection
end

#print axioms RadixCellSelection.first_real
#print axioms RadixCellSelection.last_real
#print axioms RadixCellSelection.cell_strict_lower
#print axioms RadixCellSelection.cell_strict_upper
#print axioms RadixCellSelection.irrational_avoids_boundary
#print axioms RadixCellSelection.bracket_limits_of_width
#print axioms RadixCellSelection.eventual_single_cell
#print axioms RadixCellSelection.unique_candidate
#print axioms RadixCellSelection.eventual_unique_candidate
#print axioms RadixCellSelection.width_alone_not_enough
#print axioms RadixCellSelection.prefix_truncate
#print axioms RadixCellSelection.prefix_step
#print axioms RadixCellSelection.digit_bound
#print axioms RadixCellSelection.prefix_extend
#print axioms RadixCellSelection.prefix_as_cell
#print axioms RadixCellSelection.prefix_child_interval
#print axioms RadixCellSelection.clipped_single_cell
#print axioms RadixCellSelection.closure_irrational
#print axioms RadixCellSelection.golden_irrational
#print axioms RadixCellSelection.scaled_partial_integer
#print axioms RadixCellSelection.scaled_rational_integer
#print axioms RadixCellSelection.scaled_tail_lt_one
#print axioms RadixCellSelection.propagation_irrational
#print axioms RadixCellSelection.exp_one_irrational
#print axioms RadixCellSelection.closure_eventual_cell
#print axioms RadixCellSelection.propagation_eventual_cell
#print axioms RadixCellSelection.golden_avoids_boundary
