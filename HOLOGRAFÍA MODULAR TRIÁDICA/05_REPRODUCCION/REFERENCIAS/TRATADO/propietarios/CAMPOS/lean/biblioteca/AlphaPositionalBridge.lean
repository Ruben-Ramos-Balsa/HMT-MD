import AlphaCarryLimit
import AutoscaleBrackets
import Mathlib.Tactic

/-!
# Positional publication of the already constructed real readers

This is a downstream realization bridge. The floor operation does not
select a TPK state or define its regional characters. Those real readers
have already been generated in the imported modules.
-/

noncomputable section
open Filter Topology

namespace AlphaPositionalBridge

open RadixRecovery

theorem decodeLE_valid (base width value : ℕ) (hb : 0 < base) :
    Valid base (decodeLE base width value) := by
  induction width generalizing value with
  | zero => simp [decodeLE, Valid]
  | succ n ih =>
    intro digit hd
    simp only [decodeLE, List.mem_cons] at hd
    rcases hd with rfl | hd
    · exact Nat.mod_lt value hb
    · exact ih (value / base) digit hd

theorem decode_valid (base width value : ℕ) (hb : 0 < base) :
    Valid base (decode base width value) := by
  intro digit hd
  exact decodeLE_valid base width value hb digit (List.mem_reverse.mp hd)

theorem encodeLE_decodeLE (base width value : ℕ) (hb : 0 < base)
    (hv : value < base ^ width) :
    encodeLE base (decodeLE base width value) = value := by
  induction width generalizing value with
  | zero =>
    have hzero : value = 0 := by simpa using hv
    simp [decodeLE, encodeLE, hzero]
  | succ n ih =>
    have hdiv : value / base < base ^ n := by
      apply (Nat.div_lt_iff_lt_mul hb).2
      simpa [Nat.pow_succ] using hv
    simp only [decodeLE, encodeLE, appendDigit, ih (value / base) hdiv]
    exact Nat.div_add_mod value base

theorem encode_decode (base width value : ℕ) (hb : 0 < base)
    (hv : value < base ^ width) : encode base (decode base width value) = value := by
  simp only [encode, decode, List.reverse_reverse]
  exact encodeLE_decodeLE base width value hb hv

def integerPublication (x : ℝ) (n : Nat) : Int := ⌊x * (1000 : ℝ) ^ n⌋

def realPublication (x : ℝ) (n : Nat) : ℝ :=
  (integerPublication x n : ℝ) / (1000 : ℝ) ^ n

theorem publication_error (x : ℝ) (n : Nat) :
    0 ≤ x - realPublication x n ∧
      x - realPublication x n < 1 / (1000 : ℝ) ^ n := by
  have hs : (0 : ℝ) < 1000 ^ n := by positivity
  have hlo := Int.floor_le (x * (1000 : ℝ) ^ n)
  have hhi := Int.lt_floor_add_one (x * (1000 : ℝ) ^ n)
  unfold realPublication integerPublication
  constructor
  · rw [sub_nonneg, div_le_iff₀ hs]
    exact hlo
  · rw [sub_lt_iff_lt_add, ← add_div, lt_div_iff₀ hs]
    linarith

/-- Universal convergence, including negative real inputs. -/
theorem publication_tendsto (x : ℝ) :
    Tendsto (realPublication x) atTop (𝓝 x) := by
  rw [tendsto_iff_norm_sub_tendsto_zero]
  apply squeeze_zero (fun _ => norm_nonneg _) (fun n => ?_)
    AlphaCarryLimit.inverse_scale_tendsto_zero
  rw [Real.norm_eq_abs, abs_sub_comm, abs_of_nonneg (publication_error x n).1]
  exact (publication_error x n).2.le

def naturalPublication (x : ℝ) (n : Nat) : Nat := ⌊x * (1000 : ℝ) ^ n⌋₊

theorem natural_publication_eq (x : ℝ) (hx : 0 ≤ x) (n : Nat) :
    (naturalPublication x n : Int) = integerPublication x n := by
  unfold naturalPublication integerPublication
  rw [← Int.floor_toNat]
  exact Int.toNat_of_nonneg (Int.floor_nonneg.mpr (mul_nonneg hx (by positivity)))

theorem natural_publication_bound (x : ℝ) (hx : 0 ≤ x) (hx1 : x < 1) (n : Nat) :
    naturalPublication x n < 1000 ^ n := by
  have hh : (integerPublication x n : ℝ) < (1000 : ℝ) ^ n :=
    (Int.floor_le _).trans_lt (by nlinarith [show (0 : ℝ) < 1000 ^ n by positivity])
  rw [← natural_publication_eq x hx] at hh
  exact_mod_cast hh

theorem natural_publication_truncate (x : ℝ) (n m : Nat) :
    naturalPublication x (n + m) / 1000 ^ m = naturalPublication x n :=
  RadixCellSelection.prefix_truncate x 1000 n m (by norm_num)

def positionalDigits (x : ℝ) (n : Nat) : List Nat :=
  decode 1000 n (naturalPublication x n)

theorem positional_digits_length (x : ℝ) (n : Nat) :
    (positionalDigits x n).length = n := decode_length _ _ _

theorem positional_digits_valid (x : ℝ) (n : Nat) :
    Valid 1000 (positionalDigits x n) := decode_valid _ _ _ (by norm_num)

theorem positional_digits_encode (x : ℝ) (hx : 0 ≤ x) (hx1 : x < 1) (n : Nat) :
    encode 1000 (positionalDigits x n) = naturalPublication x n :=
  encode_decode _ _ _ (by norm_num) (natural_publication_bound x hx hx1 n)

theorem positional_digits_read (x : ℝ) (hx : 0 ≤ x) (hx1 : x < 1) (n : Nat) :
    AlphaCarryLimit.readWord ((positionalDigits x n).map Int.ofNat) =
      realPublication x n := by
  unfold AlphaCarryLimit.readWord realPublication
  rw [AlphaCarryLimit.evaluate_nat_digits, positional_digits_encode x hx hx1,
    natural_publication_eq x hx]
  simp only [List.length_map, positional_digits_length]

theorem positional_digits_tendsto (x : ℝ) (hx : 0 ≤ x) (hx1 : x < 1) :
    Tendsto (fun n => AlphaCarryLimit.readWord ((positionalDigits x n).map Int.ofNat))
      atTop (𝓝 x) := by
  simpa only [positional_digits_read x hx hx1] using publication_tendsto x

theorem closure_integer_part : 3 < ClosureAnalytic.value ∧ ClosureAnalytic.value < 4 := by
  have h := ClosureAnalytic.rational_brackets 1
  have hl : (3 : ℝ) < ClosureAnalytic.lowerQ 1 := by
    norm_num [ClosureAnalytic.lowerQ, ClosureAnalytic.quarterCount,
      ClosureAnalytic.companionCount, ClosureAnalytic.primitive_slope_value,
      ClosureAnalytic.compensator_slope_value, ClosureAnalytic.arctanPartialQ, ClosureAnalytic.magnitudeQ,
      Finset.sum_range_succ]
  have hu : (ClosureAnalytic.upperQ 1 : ℝ) < 4 := by
    norm_num [ClosureAnalytic.upperQ, ClosureAnalytic.quarterCount,
      ClosureAnalytic.companionCount, ClosureAnalytic.primitive_slope_value,
      ClosureAnalytic.compensator_slope_value, ClosureAnalytic.arctanPartialQ, ClosureAnalytic.magnitudeQ,
      Finset.sum_range_succ]
  exact ⟨hl.trans_le h.1, h.2.trans_lt hu⟩

theorem propagation_integer_part :
    2 < PropagationLimit.value ∧ PropagationLimit.value < 3 := by
  have h := PropagationLimit.rational_bracket 1
  norm_num [PropagationLimit.partialQ, PropagationLimit.upperQ,
    PropagationLimit.tailQ, PropagationLimit.coefficient, Finset.sum_range_succ] at h
  constructor <;> linarith

theorem autoscale_integer_part :
    1 < AlphaCarryLimit.autoscaleValue ∧ AlphaCarryLimit.autoscaleValue < 2 := by
  have h := AutoscaleBrackets.rational_bracket 0
  rw [AutoscaleBrackets.initial_bracket.1, AutoscaleBrackets.initial_bracket.2] at h
  simpa only [Rat.cast_one, Rat.cast_ofNat, AlphaCarryLimit.autoscale_recognition] using h

theorem fractional_ranges :
    (0 < ClosureAnalytic.value - 3 ∧ ClosureAnalytic.value - 3 < 1) ∧
    (0 < PropagationLimit.value - 2 ∧ PropagationLimit.value - 2 < 1) ∧
    (0 < AlphaCarryLimit.autoscaleValue - 1 ∧ AlphaCarryLimit.autoscaleValue - 1 < 1) := by
  have hp := closure_integer_part
  have he := propagation_integer_part
  have hf := autoscale_integer_part
  constructor
  · constructor <;> linarith
  · constructor <;> constructor <;> linarith

theorem integer_parts_floor :
    ⌊ClosureAnalytic.value⌋ = (3 : Int) ∧
    ⌊PropagationLimit.value⌋ = (2 : Int) ∧
    ⌊AlphaCarryLimit.autoscaleValue⌋ = (1 : Int) := by
  have hp := closure_integer_part
  have he := propagation_integer_part
  have hf := autoscale_integer_part
  refine ⟨Int.floor_eq_iff.mpr ?_, Int.floor_eq_iff.mpr ?_, Int.floor_eq_iff.mpr ?_⟩ <;>
    constructor <;> norm_num <;> linarith

theorem closure_fractional_publication :
    Tendsto (fun n => AlphaCarryLimit.readWord
      ((positionalDigits (ClosureAnalytic.value - 3) n).map Int.ofNat))
      atTop (𝓝 (ClosureAnalytic.value - 3)) :=
  positional_digits_tendsto _ fractional_ranges.1.1.le fractional_ranges.1.2

theorem propagation_fractional_publication :
    Tendsto (fun n => AlphaCarryLimit.readWord
      ((positionalDigits (PropagationLimit.value - 2) n).map Int.ofNat))
      atTop (𝓝 (PropagationLimit.value - 2)) :=
  positional_digits_tendsto _ fractional_ranges.2.1.1.le fractional_ranges.2.1.2

theorem autoscale_fractional_publication :
    Tendsto (fun n => AlphaCarryLimit.readWord
      ((positionalDigits (AlphaCarryLimit.autoscaleValue - 1) n).map Int.ofNat))
      atTop (𝓝 (AlphaCarryLimit.autoscaleValue - 1)) :=
  positional_digits_tendsto _ fractional_ranges.2.2.1.le fractional_ranges.2.2.2

def wordAt (digits : List Nat) {width : Nat} (hlen : digits.length = width)
    (i : Fin width) : Nat := digits.get ⟨i.val, by simpa only [hlen] using i.isLt⟩

theorem ofFn_wordAt (digits : List Nat) (width : Nat) (hlen : digits.length = width) :
    List.ofFn (wordAt digits hlen) = digits := by
  subst width
  exact List.ofFn_get digits

/-- Four columns are assembled at a common width, after their readers exist. -/
def publishedBlocks (register : K12) (n : Nat) : List AlphaCarry.InputBlock :=
  List.ofFn (fun i : Fin (12 * n) =>
    ⟨(wordAt (positionalDigits (ClosureAnalytic.value - 3) (12 * n))
       (positional_digits_length _ _) i : Int),
     (wordAt (positionalDigits (PropagationLimit.value - 2) (12 * n))
       (positional_digits_length _ _) i : Int),
     (wordAt (positionalDigits (AlphaCarryLimit.autoscaleValue - 1) (12 * n))
       (positional_digits_length _ _) i : Int),
     (wordAt (AlphaCarryLimit.Periodic.repeatedDigits register n)
       (AlphaCarryLimit.Periodic.repeatedDigits_length _ _) i : Int)⟩)

theorem published_blocks_p (register : K12) (n : Nat) :
    (publishedBlocks register n).map AlphaCarry.InputBlock.p =
      (positionalDigits (ClosureAnalytic.value - 3) (12 * n)).map Int.ofNat := by
  simpa only [publishedBlocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (ofFn_wordAt
      (positionalDigits (ClosureAnalytic.value - 3) (12 * n)) _ (positional_digits_length _ _))

theorem published_blocks_e (register : K12) (n : Nat) :
    (publishedBlocks register n).map AlphaCarry.InputBlock.e =
      (positionalDigits (PropagationLimit.value - 2) (12 * n)).map Int.ofNat := by
  simpa only [publishedBlocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (ofFn_wordAt
      (positionalDigits (PropagationLimit.value - 2) (12 * n)) _ (positional_digits_length _ _))

theorem published_blocks_phi (register : K12) (n : Nat) :
    (publishedBlocks register n).map AlphaCarry.InputBlock.phi =
      (positionalDigits (AlphaCarryLimit.autoscaleValue - 1) (12 * n)).map Int.ofNat := by
  simpa only [publishedBlocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (ofFn_wordAt
      (positionalDigits (AlphaCarryLimit.autoscaleValue - 1) (12 * n)) _ (positional_digits_length _ _))

theorem published_blocks_k (register : K12) (n : Nat) :
    (publishedBlocks register n).map AlphaCarry.InputBlock.k =
      (AlphaCarryLimit.Periodic.repeatedDigits register n).map Int.ofNat := by
  simpa only [publishedBlocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (ofFn_wordAt
      (AlphaCarryLimit.Periodic.repeatedDigits register n) _
      (AlphaCarryLimit.Periodic.repeatedDigits_length _ _))

theorem published_blocks_length (register : K12) (n : Nat) :
    (publishedBlocks register n).length = 12 * n := by
  simp only [publishedBlocks, List.length_ofFn]

theorem full_turn_depths_tendsto : Tendsto (fun n : Nat => 12 * n) atTop atTop := by
  exact tendsto_atTop.2 (fun b => eventually_atTop.2 ⟨b, fun a ha => by omega⟩)

/-- No regional convergence hypotheses remain: they follow from the
positional publication and the already established real readers. -/
theorem published_alpha_limit (register : K12) (boundary : Nat → Int) (C : ℝ)
    (hbound : ∀ n, |(boundary n : ℝ)| ≤ C)
    (hy0 : 0 < AlphaCarryLimit.value register) (hy1 : AlphaCarryLimit.value register < 1) :
    Tendsto (fun n => AlphaCarryLimit.closedRead
      ((publishedBlocks register n).map AlphaCarry.InputBlock.balance) (boundary n))
      atTop (𝓝 (AlphaCarryLimit.value register)) := by
  apply AlphaCarryLimit.registered_alpha_limit register (publishedBlocks register) boundary C
  · simpa only [published_blocks_p, Function.comp_apply] using
      closure_fractional_publication.comp full_turn_depths_tendsto
  · simpa only [published_blocks_e, Function.comp_apply] using
      propagation_fractional_publication.comp full_turn_depths_tendsto
  · simpa only [published_blocks_phi, Function.comp_apply] using
      autoscale_fractional_publication.comp full_turn_depths_tendsto
  · exact published_blocks_k register
  · exact hbound
  · exact hy0
  · exact hy1

theorem published_alpha_zero_boundary (register : K12)
    (hy0 : 0 < AlphaCarryLimit.value register) (hy1 : AlphaCarryLimit.value register < 1) :
    Tendsto (fun n => AlphaCarryLimit.closedRead
      ((publishedBlocks register n).map AlphaCarry.InputBlock.balance) 0)
      atTop (𝓝 (AlphaCarryLimit.value register)) :=
  published_alpha_limit register (fun _ => 0) 0 (by intro n; norm_num) hy0 hy1

end AlphaPositionalBridge
end

#print axioms AlphaPositionalBridge.publication_error
#print axioms AlphaPositionalBridge.publication_tendsto
#print axioms AlphaPositionalBridge.natural_publication_eq
#print axioms AlphaPositionalBridge.natural_publication_bound
#print axioms AlphaPositionalBridge.decodeLE_valid
#print axioms AlphaPositionalBridge.decode_valid
#print axioms AlphaPositionalBridge.encodeLE_decodeLE
#print axioms AlphaPositionalBridge.encode_decode
#print axioms AlphaPositionalBridge.natural_publication_truncate
#print axioms AlphaPositionalBridge.positional_digits_length
#print axioms AlphaPositionalBridge.positional_digits_valid
#print axioms AlphaPositionalBridge.positional_digits_encode
#print axioms AlphaPositionalBridge.positional_digits_read
#print axioms AlphaPositionalBridge.positional_digits_tendsto
#print axioms AlphaPositionalBridge.closure_integer_part
#print axioms AlphaPositionalBridge.propagation_integer_part
#print axioms AlphaPositionalBridge.autoscale_integer_part
#print axioms AlphaPositionalBridge.fractional_ranges
#print axioms AlphaPositionalBridge.integer_parts_floor
#print axioms AlphaPositionalBridge.closure_fractional_publication
#print axioms AlphaPositionalBridge.propagation_fractional_publication
#print axioms AlphaPositionalBridge.autoscale_fractional_publication
#print axioms AlphaPositionalBridge.ofFn_wordAt
#print axioms AlphaPositionalBridge.published_blocks_p
#print axioms AlphaPositionalBridge.published_blocks_e
#print axioms AlphaPositionalBridge.published_blocks_phi
#print axioms AlphaPositionalBridge.published_blocks_k
#print axioms AlphaPositionalBridge.published_blocks_length
#print axioms AlphaPositionalBridge.full_turn_depths_tendsto
#print axioms AlphaPositionalBridge.published_alpha_limit
#print axioms AlphaPositionalBridge.published_alpha_zero_boundary
