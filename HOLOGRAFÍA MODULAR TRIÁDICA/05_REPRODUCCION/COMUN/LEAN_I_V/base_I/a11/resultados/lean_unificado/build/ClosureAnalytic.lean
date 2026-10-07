import TRITCore
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan
import Mathlib.Analysis.SpecialFunctions.Complex.Arctan
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Tactic

/-!
# Analytic realization of the structural closure reader

The explicit finite input at this cut is five reader positions and four
companions. The primitive slope and compensator are computed rationally.
Only after those definitions do angle identities recognize the resulting
character as Real.pi. No scalar target selects an upstream TPK region.
-/

noncomputable section
open Finset

namespace ClosureAnalytic

def regionCount : Nat := 5
def companionCount : Nat := 4
def quarterCount : Nat := 4

def primitiveSlope : ℚ := 1 / (regionCount : ℚ)

def tanAdd (a b : ℚ) : ℚ := (a + b) / (1 - a * b)

def accumulated : Nat → ℚ
  | 0 => 0
  | n + 1 => tanAdd (accumulated n) primitiveSlope

def companionSlope : ℚ := accumulated companionCount

def compensator : ℚ := (1 + companionSlope) / (companionSlope - 1)

def compensatorSlope : ℚ := 1 / compensator

def unitSlope : ℚ :=
  (companionSlope - compensatorSlope) / (1 + companionSlope * compensatorSlope)

theorem companion_count : companionCount + 1 = regionCount := rfl

theorem primitive_slope_value : primitiveSlope = 1 / 5 := rfl

/-- Equal reader coordinates with total mass one force the primitive slope. -/
theorem normalized_positions_force_slope (w : Fin 5 → ℚ)
    (hsym : ∀ i j, w i = w j) (hunit : ∑ i, w i = 1) (j : Fin 5) :
    w j = primitiveSlope := by
  have hsum : ∑ i, w i = 5 * w j := by
    simp_rw [hsym _ j]
    simp
  rw [hsum] at hunit
  rw [primitive_slope_value]
  linarith

/-- The rational extension of the elliptic TRIT chart. -/
def ellipticJ (v : ℚ × ℚ) : ℚ × ℚ := (-v.2, v.1)

def embedPlane (v : TRITCore.Plane) : ℚ × ℚ := ((v.1 : ℚ), (v.2 : ℚ))

theorem ellipticJ_extends_TRIT (v : TRITCore.Plane) :
    ellipticJ (embedPlane v) = embedPlane (TRITCore.J 1 v) := by
  ext <;> simp [ellipticJ, embedPlane, TRITCore.J]

theorem ellipticJ_square (v : ℚ × ℚ) : ellipticJ (ellipticJ v) = -v := by
  ext <;> simp [ellipticJ]

def elementary (a : ℚ) (v : ℚ × ℚ) : ℚ × ℚ :=
  (v.1 - a * v.2, v.2 + a * v.1)

theorem elementary_product (a b : ℚ) (v : ℚ × ℚ) :
    elementary a (elementary b v) =
      ((1 - a * b) * v.1 - (a + b) * v.2,
       (1 - a * b) * v.2 + (a + b) * v.1) := by
  ext <;> dsimp [elementary] <;> ring

theorem elementary_normalized (a b : ℚ) (v : ℚ × ℚ)
    (h : 1 - a * b ≠ 0) :
    elementary a (elementary b v) = (1 - a * b) • elementary (tanAdd a b) v := by
  rw [elementary_product]
  ext <;> dsimp [elementary, tanAdd] <;> field_simp <;> ring

theorem accumulated_values :
    [accumulated 0, accumulated 1, accumulated 2, accumulated 3, accumulated 4] =
      [0, 1 / 5, 5 / 12, 37 / 55, 120 / 119] := by
  norm_num [accumulated, tanAdd, primitiveSlope, regionCount]

theorem composition_branch (n : Nat) (hn : n < companionCount) :
    accumulated n * primitiveSlope < 1 := by
  change n < 4 at hn
  interval_cases n <;> norm_num [accumulated, tanAdd, primitiveSlope, regionCount]

theorem composition_denominator_positive (n : Nat) (hn : n < companionCount) :
    0 < 1 - accumulated n * primitiveSlope := sub_pos.mpr (composition_branch n hn)

theorem companion_slope_value : companionSlope = 120 / 119 := by
  norm_num [companionSlope, companionCount, accumulated, tanAdd, primitiveSlope, regionCount]

theorem companion_crosses_unit : 1 < companionSlope := by
  rw [companion_slope_value]
  norm_num

theorem compensator_value : compensator = 239 := by
  norm_num [compensator, companion_slope_value]

theorem compensator_positive_integer : 1 < compensator ∧ ∃ q : Nat, compensator = q := by
  rw [compensator_value]
  exact ⟨by norm_num, ⟨239, by norm_num⟩⟩

theorem compensator_slope_value : compensatorSlope = 1 / 239 := by
  rw [compensatorSlope, compensator_value]

theorem compensation_denominator_positive : 0 < 1 + companionSlope * compensatorSlope := by
  rw [companion_slope_value, compensator_slope_value]
  norm_num

theorem returns_unit : unitSlope = 1 := by
  norm_num [unitSlope, companion_slope_value, compensator_slope_value]

theorem compensator_unique (q : ℚ) (hq : 1 < q)
    (hreturn : (companionSlope - 1 / q) / (1 + companionSlope * (1 / q)) = 1) :
    q = compensator := by
  have hq0 : q ≠ 0 := ne_of_gt (lt_trans zero_lt_one hq)
  have hden : 1 + companionSlope * (1 / q) ≠ 0 := by
    rw [companion_slope_value]
    have : 0 < 1 + (120 / 119 : ℚ) * (1 / q) := by positivity
    exact ne_of_gt this
  have h := (div_eq_one_iff_eq hden).mp hreturn
  rw [companion_slope_value] at h
  field_simp at h
  rw [compensator_value]
  linarith

def companionAngle : ℝ := (companionCount : ℝ) * Real.arctan (primitiveSlope : ℝ)

def closureAngle : ℝ := companionAngle - Real.arctan (compensatorSlope : ℝ)

def value : ℝ := (quarterCount : ℝ) * closureAngle

theorem accumulated_angle (n : Nat) (hn : n ≤ companionCount) :
    (n : ℝ) * Real.arctan (primitiveSlope : ℝ) = Real.arctan (accumulated n : ℝ) := by
  induction n with
  | zero => simp [accumulated]
  | succ n ih =>
    have hn' : n < companionCount := by omega
    have hbranch : (accumulated n : ℝ) * primitiveSlope < 1 := by
      exact_mod_cast composition_branch n hn'
    calc
      ((n + 1 : Nat) : ℝ) * Real.arctan (primitiveSlope : ℝ) =
          (n : ℝ) * Real.arctan (primitiveSlope : ℝ) +
            Real.arctan (primitiveSlope : ℝ) := by push_cast; ring
      _ = Real.arctan (accumulated n : ℝ) + Real.arctan (primitiveSlope : ℝ) := by
        rw [ih (by omega)]
      _ = Real.arctan (((accumulated n : ℝ) + primitiveSlope) /
          (1 - (accumulated n : ℝ) * primitiveSlope)) := Real.arctan_add hbranch
      _ = Real.arctan (accumulated (n + 1) : ℝ) := by
        simp [accumulated, tanAdd]

theorem companion_angle_realization : companionAngle = Real.arctan (companionSlope : ℝ) :=
  accumulated_angle companionCount (Nat.le_refl _)

theorem companion_angle_branch :
    -(Real.pi / 2) < companionAngle ∧ companionAngle < Real.pi / 2 := by
  rw [companion_angle_realization]
  exact Real.arctan_mem_Ioo _

theorem compensation_branch : (companionSlope : ℝ) * (-(compensatorSlope : ℝ)) < 1 := by
  rw [companion_slope_value, compensator_slope_value]
  norm_num

theorem closure_angle_realization : closureAngle = Real.arctan (unitSlope : ℝ) := by
  unfold closureAngle
  rw [companion_angle_realization, sub_eq_add_neg, ← Real.arctan_neg]
  rw [Real.arctan_add compensation_branch]
  simp [unitSlope, sub_eq_add_neg]

theorem closure_angle_branch :
    -(Real.pi / 2) < closureAngle ∧ closureAngle < Real.pi / 2 := by
  rw [closure_angle_realization]
  exact Real.arctan_mem_Ioo _

theorem closure_angle_recognition : closureAngle = Real.pi / 4 := by
  rw [closure_angle_realization, returns_unit]
  simp

theorem value_eq_pi : value = Real.pi := by
  rw [value, closure_angle_recognition]
  norm_num [quarterCount]
  ring

theorem reader_formula : value =
    4 * (4 * Real.arctan (1 / 5) - Real.arctan (1 / 239)) := by
  simp [value, closureAngle, companionAngle, quarterCount, companionCount,
    primitive_slope_value, compensator_slope_value]

def magnitude (x : ℝ) (n : Nat) : ℝ := x ^ (2 * n + 1) / (2 * n + 1 : ℝ)

def arctanPartial (x : ℝ) (n : Nat) : ℝ :=
  ∑ k ∈ range n, (-1 : ℝ) ^ k * magnitude x k

def magnitudeQ (x : ℚ) (n : Nat) : ℚ := x ^ (2 * n + 1) / (2 * n + 1 : ℚ)

def arctanPartialQ (x : ℚ) (n : Nat) : ℚ :=
  ∑ k ∈ range n, (-1 : ℚ) ^ k * magnitudeQ x k

theorem magnitude_cast (x : ℚ) (n : Nat) :
    (magnitudeQ x n : ℝ) = magnitude x n := by
  simp [magnitudeQ, magnitude]

theorem arctanPartial_cast (x : ℚ) (n : Nat) :
    (arctanPartialQ x n : ℝ) = arctanPartial x n := by
  simp [arctanPartialQ, arctanPartial, magnitude_cast]

theorem magnitude_antitone {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ 1) :
    Antitone (magnitude x) := by
  apply antitone_nat_of_succ_le
  intro n
  dsimp [magnitude]
  have hp : x ^ (2 * (n + 1) + 1) ≤ x ^ (2 * n + 1) :=
    pow_le_pow_of_le_one hx0 hx1 (by omega)
  exact div_le_div₀ (by positivity) hp (by positivity) (by push_cast; linarith)

theorem arctanPartial_tendsto {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x < 1) :
    Filter.Tendsto (arctanPartial x) Filter.atTop (nhds (Real.arctan x)) := by
  have hx : ‖x‖ < 1 := by simpa [Real.norm_eq_abs, abs_of_nonneg hx0] using hx1
  simpa [arctanPartial, magnitude, mul_div_assoc] using
    (Real.hasSum_arctan hx).tendsto_sum_nat

theorem arctanPartial_brackets {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x < 1) (k : Nat) :
    arctanPartial x (2 * k) ≤ Real.arctan x ∧
      Real.arctan x ≤ arctanPartial x (2 * k + 1) := by
  have ht := arctanPartial_tendsto hx0 hx1
  have hm := magnitude_antitone hx0 hx1.le
  exact ⟨Antitone.alternating_series_le_tendsto ht hm k,
    Antitone.tendsto_le_alternating_series ht hm k⟩

theorem arctan_remainder_le {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x < 1) (n : Nat) :
    |Real.arctan x - arctanPartial x n| ≤ magnitude x n := by
  by_cases he : n % 2 = 0
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k := ⟨n / 2, by omega⟩
    obtain ⟨hl, hu⟩ := arctanPartial_brackets hx0 hx1 k
    have hs : arctanPartial x (2 * k + 1) =
        arctanPartial x (2 * k) + magnitude x (2 * k) := by
      simp [arctanPartial, Finset.sum_range_succ, pow_mul]
    rw [hs] at hu
    rw [abs_of_nonneg (sub_nonneg.mpr hl)]
    linarith
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k + 1 := ⟨n / 2, by omega⟩
    have hu := (arctanPartial_brackets hx0 hx1 k).2
    have hl := (arctanPartial_brackets hx0 hx1 (k + 1)).1
    have hs : arctanPartial x (2 * (k + 1)) =
        arctanPartial x (2 * k + 1) - magnitude x (2 * k + 1) := by
      rw [show 2 * (k + 1) = (2 * k + 1) + 1 by omega]
      simp [arctanPartial, Finset.sum_range_succ, pow_add, pow_mul, sub_eq_add_neg]
    rw [hs] at hl
    rw [abs_of_nonpos (sub_nonpos.mpr hu)]
    linarith

def lowerQ (k : Nat) : ℚ := quarterCount *
  (companionCount * arctanPartialQ primitiveSlope (2 * k) -
    arctanPartialQ compensatorSlope (2 * k + 1))

def upperQ (k : Nat) : ℚ := quarterCount *
  (companionCount * arctanPartialQ primitiveSlope (2 * k + 1) -
    arctanPartialQ compensatorSlope (2 * k))

theorem rational_brackets (k : Nat) : (lowerQ k : ℝ) ≤ value ∧ value ≤ (upperQ k : ℝ) := by
  have hp0 : (0 : ℝ) ≤ primitiveSlope := by rw [primitive_slope_value]; norm_num
  have hp1 : (primitiveSlope : ℝ) < 1 := by rw [primitive_slope_value]; norm_num
  have hm0 : (0 : ℝ) ≤ compensatorSlope := by rw [compensator_slope_value]; norm_num
  have hm1 : (compensatorSlope : ℝ) < 1 := by rw [compensator_slope_value]; norm_num
  obtain ⟨hpL, hpU⟩ := arctanPartial_brackets hp0 hp1 k
  obtain ⟨hmL, hmU⟩ := arctanPartial_brackets hm0 hm1 k
  simp only [lowerQ, upperQ, Rat.cast_mul, Rat.cast_sub, Rat.cast_natCast, arctanPartial_cast,
    value, closureAngle, companionAngle]
  norm_num [quarterCount, companionCount] at *
  constructor <;> linarith

theorem arctanPartialQ_even_succ (x : ℚ) (k : Nat) :
    arctanPartialQ x (2 * k + 1) = arctanPartialQ x (2 * k) + magnitudeQ x (2 * k) := by
  simp [arctanPartialQ, Finset.sum_range_succ, pow_mul]

theorem rational_width (k : Nat) : upperQ k - lowerQ k =
    quarterCount * (companionCount * magnitudeQ primitiveSlope (2 * k) +
      magnitudeQ compensatorSlope (2 * k)) := by
  rw [upperQ, lowerQ, arctanPartialQ_even_succ, arctanPartialQ_even_succ]
  ring

theorem rational_width_positive (k : Nat) : 0 < upperQ k - lowerQ k := by
  rw [rational_width]
  have hp : 0 < primitiveSlope := by rw [primitive_slope_value]; norm_num
  have hm : 0 < compensatorSlope := by rw [compensator_slope_value]; norm_num
  unfold magnitudeQ quarterCount companionCount
  positivity

theorem magnitude_tendsto_zero {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x < 1) :
    Filter.Tendsto (magnitude x) Filter.atTop (nhds 0) := by
  apply squeeze_zero (fun n => by dsimp [magnitude]; positivity)
    (fun n => ?_) (tendsto_pow_atTop_nhds_zero_of_lt_one hx0 hx1)
  dsimp [magnitude]
  have hden : (1 : ℝ) ≤ 2 * n + 1 := by
    have hn : (0 : ℝ) ≤ n := by positivity
    linarith
  exact (div_le_self (pow_nonneg hx0 _) hden).trans
    (pow_le_pow_of_le_one hx0 hx1.le (by omega))

theorem width_tendsto_zero :
    Filter.Tendsto (fun k => ((upperQ k - lowerQ k : ℚ) : ℝ)) Filter.atTop (nhds 0) := by
  have hp0 : (0 : ℝ) ≤ primitiveSlope := by rw [primitive_slope_value]; norm_num
  have hp1 : (primitiveSlope : ℝ) < 1 := by rw [primitive_slope_value]; norm_num
  have hm0 : (0 : ℝ) ≤ compensatorSlope := by rw [compensator_slope_value]; norm_num
  have hm1 : (compensatorSlope : ℝ) < 1 := by rw [compensator_slope_value]; norm_num
  have hi : Filter.Tendsto (fun k : Nat => 2 * k) Filter.atTop Filter.atTop := by
    apply Filter.tendsto_atTop.mpr
    intro b
    exact Filter.eventually_atTop.mpr ⟨b, fun a ha => by omega⟩
  have hp := (magnitude_tendsto_zero hp0 hp1).comp hi
  have hm := (magnitude_tendsto_zero hm0 hm1).comp hi
  have h := ((hp.const_mul (companionCount : ℝ)).add hm).const_mul (quarterCount : ℝ)
  simpa only [rational_width, Rat.cast_mul, Rat.cast_natCast, Rat.cast_add, magnitude_cast,
    Function.comp_def, mul_zero, add_zero] using h

theorem exists_precision_index (scale : Nat) :
    ∃ k : Nat, 1 ≤ k ∧ (upperQ k - lowerQ k) * scale < 1 := by
  have hlim : Filter.Tendsto
      (fun k => ((upperQ k - lowerQ k : ℚ) : ℝ) * scale) Filter.atTop (nhds 0) := by
    simpa only [zero_mul] using width_tendsto_zero.mul_const (scale : ℝ)
  have hevent : ∀ᶠ k in Filter.atTop, ((upperQ k - lowerQ k : ℚ) : ℝ) * scale < 1 :=
    (tendsto_order.mp hlim).2 1 (by norm_num)
  rcases Filter.eventually_atTop.mp hevent with ⟨N, hN⟩
  refine ⟨max N 1, le_max_right _ _, ?_⟩
  have h := hN (max N 1) (le_max_left _ _)
  exact_mod_cast h

end ClosureAnalytic
end

#print axioms ClosureAnalytic.companion_count
#print axioms ClosureAnalytic.primitive_slope_value
#print axioms ClosureAnalytic.normalized_positions_force_slope
#print axioms ClosureAnalytic.ellipticJ_extends_TRIT
#print axioms ClosureAnalytic.ellipticJ_square
#print axioms ClosureAnalytic.elementary_product
#print axioms ClosureAnalytic.elementary_normalized
#print axioms ClosureAnalytic.accumulated_values
#print axioms ClosureAnalytic.composition_branch
#print axioms ClosureAnalytic.composition_denominator_positive
#print axioms ClosureAnalytic.companion_slope_value
#print axioms ClosureAnalytic.companion_crosses_unit
#print axioms ClosureAnalytic.compensator_value
#print axioms ClosureAnalytic.compensator_positive_integer
#print axioms ClosureAnalytic.compensator_slope_value
#print axioms ClosureAnalytic.compensation_denominator_positive
#print axioms ClosureAnalytic.returns_unit
#print axioms ClosureAnalytic.compensator_unique
#print axioms ClosureAnalytic.accumulated_angle
#print axioms ClosureAnalytic.companion_angle_realization
#print axioms ClosureAnalytic.companion_angle_branch
#print axioms ClosureAnalytic.compensation_branch
#print axioms ClosureAnalytic.closure_angle_realization
#print axioms ClosureAnalytic.closure_angle_branch
#print axioms ClosureAnalytic.closure_angle_recognition
#print axioms ClosureAnalytic.value_eq_pi
#print axioms ClosureAnalytic.reader_formula
#print axioms ClosureAnalytic.magnitude_cast
#print axioms ClosureAnalytic.arctanPartial_cast
#print axioms ClosureAnalytic.magnitude_antitone
#print axioms ClosureAnalytic.arctanPartial_tendsto
#print axioms ClosureAnalytic.arctanPartial_brackets
#print axioms ClosureAnalytic.arctan_remainder_le
#print axioms ClosureAnalytic.rational_brackets
#print axioms ClosureAnalytic.arctanPartialQ_even_succ
#print axioms ClosureAnalytic.rational_width
#print axioms ClosureAnalytic.rational_width_positive
#print axioms ClosureAnalytic.magnitude_tendsto_zero
#print axioms ClosureAnalytic.width_tendsto_zero
#print axioms ClosureAnalytic.exists_precision_index
