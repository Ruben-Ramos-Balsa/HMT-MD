import AlphaCarry
import RadixRecovery
import ClosureAnalytic
import PropagationLimit
import AutoscaleLimit
import RadixCellSelection
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic

/-!
# Real publication of the normalized signed closure

The finite inputs are the signed APP–TRIT–TPK downstream blocks already
handled by `AlphaCarry`, a right boundary, and a supplied twelve-block
register. No target value is used to select those inputs. The limit theorem
states explicitly the source-reader and boundary hypotheses at this cut.
Source: alpha.tex, alpha-recurrencia, alpha-telescopia, alpha-identidad-completa;
registro_k.tex, k-kappas; k_reversibilidad.tex.
-/

noncomputable section
open Filter Topology

namespace AlphaCarryLimit

namespace Periodic

open RadixRecovery

def blockBase : ℕ := 1000 ^ 12

def blockPrefix (register : K12) : ℕ → ℕ
  | 0 => 0
  | n + 1 => blockPrefix register n * blockBase + register.publish

def repeatedDigits (register : K12) : ℕ → List ℕ
  | 0 => []
  | n + 1 => repeatedDigits register n ++ register.digits

def reader (register : K12) (n : ℕ) : ℝ :=
  (blockPrefix register n : ℝ) / (blockBase : ℝ)^n

def finiteValue (register : K12) : ℝ :=
  (register.publish : ℝ) / (blockBase : ℝ)

def periodicValue (register : K12) : ℝ :=
  (register.publish : ℝ) / ((blockBase : ℝ) - 1)

theorem blockBase_gt_one : (1 : ℝ) < blockBase := by norm_num [blockBase]

theorem encode_append (base : ℕ) (left right : List ℕ) :
    encode base (left ++ right) = encode base left * base^right.length + encode base right := by
  simp only [encode, List.reverse_append, encodeLE_append, List.length_reverse]
  ring

theorem prefix_eq_encode (register : K12) (n : ℕ) :
    blockPrefix register n = encode 1000 (repeatedDigits register n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [blockPrefix, repeatedDigits, encode_append, register.length_eq, ← ih,
      blockBase, Register.publish]

theorem repeatedDigits_length (register : K12) (n : ℕ) :
    (repeatedDigits register n).length = 12 * n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [repeatedDigits, List.length_append, ih, register.length_eq]
    omega

theorem repeatedDigits_valid (register : K12) (n : ℕ) :
    Valid 1000 (repeatedDigits register n) := by
  induction n with
  | zero => simp [repeatedDigits, Valid]
  | succ n ih =>
    intro d hd
    simp only [repeatedDigits, List.mem_append] at hd
    exact hd.elim (ih d) (register.valid d)

theorem prefix_recovers_repeatedDigits (register : K12) (n : ℕ) :
    decode 1000 (12 * n) (blockPrefix register n) = repeatedDigits register n := by
  rw [prefix_eq_encode, ← repeatedDigits_length]
  exact decode_encode 1000 (by norm_num) _ (repeatedDigits_valid register n)

theorem prefix_geometric_identity (register : K12) (n : ℕ) :
    (blockPrefix register n : ℝ) * ((blockBase : ℝ) - 1) =
      (register.publish : ℝ) * ((blockBase : ℝ)^n - 1) := by
  induction n with
  | zero => simp [blockPrefix]
  | succ n ih =>
    simp only [blockPrefix, Nat.cast_add, Nat.cast_mul, pow_succ]
    calc
      ((blockPrefix register n : ℝ) * blockBase + register.publish) * ((blockBase : ℝ) - 1) =
          ((blockPrefix register n : ℝ) * ((blockBase : ℝ) - 1)) * blockBase +
            register.publish * ((blockBase : ℝ) - 1) := by ring
      _ = (register.publish : ℝ) * ((blockBase : ℝ)^n * blockBase - 1) := by
        rw [ih]
        ring

theorem reader_closed (register : K12) (n : ℕ) :
    reader register n = periodicValue register * (1 - ((blockBase : ℝ)⁻¹)^n) := by
  have hb : (blockBase : ℝ) ≠ 0 := ne_of_gt (lt_trans zero_lt_one blockBase_gt_one)
  have hd : (blockBase : ℝ) - 1 ≠ 0 := ne_of_gt (sub_pos.mpr blockBase_gt_one)
  have hi : (blockPrefix register n : ℝ) =
      ((register.publish : ℝ) * ((blockBase : ℝ)^n - 1)) / ((blockBase : ℝ) - 1) :=
    (eq_div_iff hd).2 (prefix_geometric_identity register n)
  unfold reader periodicValue
  rw [hi]
  simp only [inv_pow]
  field_simp

theorem reader_tendsto (register : K12) :
    Tendsto (reader register) atTop (𝓝 (periodicValue register)) := by
  have hp : Tendsto (fun n : ℕ => ((blockBase : ℝ)⁻¹)^n) atTop (𝓝 (0 : ℝ)) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one (by positivity)
      (inv_lt_one_of_one_lt₀ blockBase_gt_one)
  have hc : Tendsto (fun _ : ℕ => (1 : ℝ)) atTop (𝓝 (1 : ℝ)) := tendsto_const_nhds
  have h := (hc.sub hp).const_mul (periodicValue register)
  simpa only [← reader_closed, sub_zero, mul_one] using h

theorem reader_error_exact (register : K12) (n : ℕ) :
    periodicValue register - reader register n =
      periodicValue register * ((blockBase : ℝ)⁻¹)^n := by
  rw [reader_closed]
  ring

theorem reader_one (register : K12) : reader register 1 = finiteValue register := by
  simp [reader, blockPrefix, finiteValue]

theorem periodic_sub_finite (register : K12) :
    periodicValue register - finiteValue register =
      (register.publish : ℝ) / ((blockBase : ℝ) * ((blockBase : ℝ) - 1)) := by
  have hb : (blockBase : ℝ) ≠ 0 := ne_of_gt (lt_trans zero_lt_one blockBase_gt_one)
  have hd : (blockBase : ℝ) - 1 ≠ 0 := ne_of_gt (sub_pos.mpr blockBase_gt_one)
  unfold periodicValue finiteValue
  field_simp
  ring

theorem periodic_sub_finite_eq_scaled (register : K12) :
    periodicValue register - finiteValue register =
      (blockBase : ℝ)⁻¹ * periodicValue register := by
  rw [← reader_one, reader_error_exact, pow_one]
  ring

theorem periodic_integer_recovery (register : K12) :
    ((blockBase : ℝ) - 1) * periodicValue register = (register.publish : ℝ) := by
  have hd : (blockBase : ℝ) - 1 ≠ 0 := ne_of_gt (sub_pos.mpr blockBase_gt_one)
  exact mul_div_cancel₀ _ hd

theorem periodic_digits_recovery (register : K12) :
    decode 1000 12 ⌊((blockBase : ℝ) - 1) * periodicValue register⌋₊ = register.digits := by
  rw [periodic_integer_recovery, Nat.floor_natCast]
  exact k12_recover register

end Periodic

/-- Big-endian fractional publication of a finite integer word. -/
def readWord (zs : List Int) : ℝ :=
  (AlphaCarry.evaluate zs : ℝ) / (1000 : ℝ) ^ zs.length

def closedRead (zs : List Int) (boundary : Int) : ℝ :=
  readWord (AlphaCarry.close zs boundary).digits

theorem evaluate_nat_digits (digits : List Nat) :
    AlphaCarry.evaluate (digits.map Int.ofNat) =
      (RadixRecovery.encode 1000 digits : Int) := by
  induction digits with
  | nil => rfl
  | cons d ds ih =>
    simp only [List.map_cons, AlphaCarry.evaluate, List.length_map,
      RadixRecovery.encode_cons, Nat.cast_add, Nat.cast_mul, Nat.cast_pow, ih]
    rfl

theorem repeated_register_read (register : RadixRecovery.K12) (n : Nat) :
    readWord ((Periodic.repeatedDigits register n).map Int.ofNat) =
      Periodic.reader register n := by
  simp only [readWord, evaluate_nat_digits, List.length_map,
    Periodic.repeatedDigits_length, Periodic.reader, Periodic.prefix_eq_encode,
    Periodic.blockBase, Int.cast_natCast, Nat.cast_pow, Nat.cast_ofNat, pow_mul]

theorem normalized_telescoping (zs : List Int) (boundary : Int) :
    readWord zs - closedRead zs boundary =
      ((AlphaCarry.close zs boundary).outgoing : ℝ) -
        (boundary : ℝ) / (1000 : ℝ) ^ zs.length := by
  have h := congrArg (fun z : Int => (z : ℝ))
    (AlphaCarry.closure_telescoping zs boundary)
  push_cast at h
  unfold readWord closedRead readWord
  rw [AlphaCarry.close_length]
  have hd : (1000 : ℝ) ^ zs.length ≠ 0 := by positivity
  field_simp
  nlinarith [h]

theorem closed_read_formula (zs : List Int) (boundary : Int) :
    closedRead zs boundary = readWord zs -
      ((AlphaCarry.close zs boundary).outgoing : ℝ) +
      (boundary : ℝ) / (1000 : ℝ) ^ zs.length := by
  linarith [normalized_telescoping zs boundary]

theorem balance_read (zs : List AlphaCarry.InputBlock) :
    readWord (zs.map AlphaCarry.InputBlock.balance) =
      readWord (zs.map AlphaCarry.InputBlock.p) +
      readWord (zs.map AlphaCarry.InputBlock.e) -
      readWord (zs.map AlphaCarry.InputBlock.phi) -
      readWord (zs.map AlphaCarry.InputBlock.k) := by
  simp only [readWord, AlphaCarry.balance_evaluation, List.length_map,
    Int.cast_add, Int.cast_sub, add_div, sub_div]

theorem inverse_scale_tendsto_zero :
    Tendsto (fun n : Nat => 1 / (1000 : ℝ) ^ n) atTop (𝓝 0) := by
  simpa only [one_div, inv_pow] using
    (tendsto_pow_atTop_nhds_zero_of_lt_one
      (by norm_num : 0 ≤ (1000 : ℝ)⁻¹) (by norm_num : (1000 : ℝ)⁻¹ < 1))

/-- Bounded remote carries suffice; no convergence of the carries is required. -/
theorem bounded_boundary_vanishes (boundary : Nat → Int) (C : ℝ)
    (hC : ∀ n, |(boundary n : ℝ)| ≤ C) :
    Tendsto (fun n => (boundary n : ℝ) / (1000 : ℝ) ^ n) atTop (𝓝 0) := by
  have hb : ∀ n, ‖(boundary n : ℝ) / (1000 : ℝ) ^ n‖ ≤
      C * (1 / (1000 : ℝ) ^ n) := by
    intro n
    rw [Real.norm_eq_abs, abs_div, abs_of_pos (by positivity : 0 < (1000 : ℝ) ^ n)]
    simpa only [div_eq_mul_inv, one_mul] using
      (div_le_div_of_nonneg_right (hC n) (by positivity : 0 ≤ (1000 : ℝ) ^ n))
  exact squeeze_zero_norm hb (by simpa using inverse_scale_tendsto_zero.const_mul C)

theorem bounded_boundary_vanishes_at_lengths (boundary : Nat → Int) (lengths : Nat → Nat)
    (C : ℝ) (hC : ∀ n, |(boundary n : ℝ)| ≤ C)
    (hlen : Tendsto lengths atTop atTop) :
    Tendsto (fun n => (boundary n : ℝ) / (1000 : ℝ) ^ lengths n) atTop (𝓝 0) := by
  have hb : ∀ n, ‖(boundary n : ℝ) / (1000 : ℝ) ^ lengths n‖ ≤
      C * (1 / (1000 : ℝ) ^ lengths n) := by
    intro n
    rw [Real.norm_eq_abs, abs_div, abs_of_pos (by positivity : 0 < (1000 : ℝ) ^ lengths n)]
    simpa only [div_eq_mul_inv, one_mul] using
      (div_le_div_of_nonneg_right (hC n) (by positivity : 0 ≤ (1000 : ℝ) ^ lengths n))
  exact squeeze_zero_norm hb
    (by simpa using (inverse_scale_tendsto_zero.comp hlen).const_mul C)

/-- The exact residual condition is enough even for unbounded carries. -/
theorem closure_limit (words : Nat → List Int) (boundary : Nat → Int)
    (y c : ℝ)
    (hsource : Tendsto (fun n => readWord (words n)) atTop (𝓝 y))
    (hfront : Tendsto (fun n => ((AlphaCarry.close (words n) (boundary n)).outgoing : ℝ))
      atTop (𝓝 c))
    (hremote : Tendsto (fun n => (boundary n : ℝ) / (1000 : ℝ) ^ (words n).length)
      atTop (𝓝 0)) :
    Tendsto (fun n => closedRead (words n) (boundary n)) atTop (𝓝 (y - c)) := by
  simpa only [closed_read_formula, add_zero] using (hsource.sub hfront).add hremote

theorem closure_limit_bounded (words : Nat → List Int) (boundary : Nat → Int)
    (y : ℝ) (c : Int) (C : ℝ) (hlen : ∀ n, (words n).length = n)
    (hsource : Tendsto (fun n => readWord (words n)) atTop (𝓝 y))
    (hfront : ∀ n, (AlphaCarry.close (words n) (boundary n)).outgoing = c)
    (hbound : ∀ n, |(boundary n : ℝ)| ≤ C) :
    Tendsto (fun n => closedRead (words n) (boundary n)) atTop (𝓝 (y - (c : ℝ))) := by
  apply closure_limit words boundary y (c : ℝ) hsource
  · simpa only [hfront] using (tendsto_const_nhds : Tendsto (fun _ : Nat => (c : ℝ)) atTop (𝓝 (c : ℝ)))
  · simpa only [hlen] using bounded_boundary_vanishes boundary C hbound

theorem alpha_reader_limit (blocks : Nat → List AlphaCarry.InputBlock)
    (boundary : Nat → Int) (p e phi k c : ℝ)
    (hp : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.p)) atTop (𝓝 p))
    (he : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.e)) atTop (𝓝 e))
    (hphi : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.phi)) atTop (𝓝 phi))
    (hk : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.k)) atTop (𝓝 k))
    (hfront : Tendsto (fun n => ((AlphaCarry.close
      ((blocks n).map AlphaCarry.InputBlock.balance) (boundary n)).outgoing : ℝ)) atTop (𝓝 c))
    (hremote : Tendsto (fun n => (boundary n : ℝ) / (1000 : ℝ) ^ (blocks n).length)
      atTop (𝓝 0)) :
    Tendsto (fun n => closedRead ((blocks n).map AlphaCarry.InputBlock.balance) (boundary n))
      atTop (𝓝 (p + e - phi - k - c)) := by
  apply closure_limit _ boundary (p + e - phi - k) c
  · simpa only [balance_read] using ((hp.add he).sub hphi).sub hk
  · exact hfront
  · simpa only [List.length_map] using hremote

theorem evaluate_digit_bounds (zs : List Int)
    (hz : ∀ d ∈ zs, 0 ≤ d ∧ d < 1000) :
    0 ≤ AlphaCarry.evaluate zs ∧ AlphaCarry.evaluate zs < (1000 : Int) ^ zs.length := by
  induction zs with
  | nil => norm_num [AlphaCarry.evaluate]
  | cons z zs ih =>
    have hh := hz z (by simp)
    have ht := ih (by intro d hd; exact hz d (by simp [hd]))
    simp only [AlphaCarry.evaluate, List.length_cons, pow_succ]
    have hp : (0 : Int) < 1000 ^ zs.length := by positivity
    constructor <;> nlinarith

theorem closed_read_bounds (zs : List Int) (boundary : Int) :
    0 ≤ closedRead zs boundary ∧ closedRead zs boundary < 1 := by
  have h := evaluate_digit_bounds (AlphaCarry.close zs boundary).digits
    (AlphaCarry.close_digit_bounds zs boundary)
  have hreal : (0 : ℝ) ≤ AlphaCarry.evaluate (AlphaCarry.close zs boundary).digits ∧
      (AlphaCarry.evaluate (AlphaCarry.close zs boundary).digits : ℝ) <
        (1000 : ℝ) ^ (AlphaCarry.close zs boundary).digits.length := by
    exact_mod_cast h
  unfold closedRead readWord
  constructor
  · exact div_nonneg hreal.1 (by positivity)
  · exact (div_lt_one (by positivity)).mpr hreal.2

/-- A source value strictly inside the unit interval forces the front carry
to vanish eventually, independently of the finite right-boundary choice. -/
theorem front_eventually_zero (words : Nat → List Int) (boundary : Nat → Int)
    (y : ℝ) (hy0 : 0 < y) (hy1 : y < 1)
    (hsource : Tendsto (fun n => readWord (words n)) atTop (𝓝 y))
    (hremote : Tendsto (fun n => (boundary n : ℝ) / (1000 : ℝ) ^ (words n).length)
      atTop (𝓝 0)) :
    ∀ᶠ n in atTop, (AlphaCarry.close (words n) (boundary n)).outgoing = 0 := by
  have ht : Tendsto (fun n => readWord (words n) +
      (boundary n : ℝ) / (1000 : ℝ) ^ (words n).length) atTop (𝓝 y) := by
    simpa using hsource.add hremote
  have hpos := (tendsto_order.mp ht).1 0 hy0
  have hlt := (tendsto_order.mp ht).2 1 hy1
  filter_upwards [hpos, hlt] with n hn0 hn1
  have hb := closed_read_bounds (words n) (boundary n)
  have hf := closed_read_formula (words n) (boundary n)
  have hfrontlow : (-1 : ℝ) < (AlphaCarry.close (words n) (boundary n)).outgoing := by
    linarith
  have hfronthigh : ((AlphaCarry.close (words n) (boundary n)).outgoing : ℝ) < 1 := by
    linarith
  have hlo : (-1 : Int) < (AlphaCarry.close (words n) (boundary n)).outgoing := by
    exact_mod_cast hfrontlow
  have hhi : (AlphaCarry.close (words n) (boundary n)).outgoing < (1 : Int) := by
    exact_mod_cast hfronthigh
  omega

/-- No limit of the output digits or of the front carry is assumed here. -/
theorem closure_limit_of_unit_interval (words : Nat → List Int) (boundary : Nat → Int)
    (y : ℝ) (hy0 : 0 < y) (hy1 : y < 1)
    (hsource : Tendsto (fun n => readWord (words n)) atTop (𝓝 y))
    (hremote : Tendsto (fun n => (boundary n : ℝ) / (1000 : ℝ) ^ (words n).length)
      atTop (𝓝 0)) :
    Tendsto (fun n => closedRead (words n) (boundary n)) atTop (𝓝 y) := by
  have hz := front_eventually_zero words boundary y hy0 hy1 hsource hremote
  have hf : Tendsto (fun n => ((AlphaCarry.close (words n) (boundary n)).outgoing : ℝ))
      atTop (𝓝 0) := by
    apply tendsto_const_nhds.congr'
    filter_upwards [hz] with n hn
    simp [hn]
  simpa using closure_limit words boundary y 0 hsource hf hremote

/-- Choose the proved limit of the emitted modal recurrence, not a target root. -/
def autoscaleValue : ℝ :=
  Classical.choose AutoscaleLimit.generated_autoscale_limit.exists

theorem autoscale_limit :
    Tendsto AutoscaleLimit.ratio atTop (𝓝 autoscaleValue) :=
  (Classical.choose_spec AutoscaleLimit.generated_autoscale_limit.exists).2.2

theorem autoscale_recognition : autoscaleValue = goldenRatio :=
  tendsto_nhds_unique autoscale_limit AutoscaleLimit.ratio_tendsto

/-- The fractional shifts are the source's integer parts 3, 2, and 1. -/
def value (register : RadixRecovery.K12) : ℝ :=
  (ClosureAnalytic.value - 3) + (PropagationLimit.value - 2) -
    (autoscaleValue - 1) - Periodic.periodicValue register

theorem integer_shift_origin : (3 : Int) + 2 - 1 = 4 := by norm_num

theorem value_composition (register : RadixRecovery.K12) :
    value register = ClosureAnalytic.value + PropagationLimit.value -
      autoscaleValue - 4 - Periodic.periodicValue register := by
  unfold value
  ring

/-- Conventional names recognize the already composed readers afterwards. -/
theorem value_recognition (register : RadixRecovery.K12) :
    value register = Real.pi + Real.exp 1 - goldenRatio - 4 -
      (register.publish : ℝ) / ((1000 : ℝ) ^ 12 - 1) := by
  rw [value_composition, ClosureAnalytic.value_eq_pi,
    PropagationLimit.value_eq_exp_one, autoscale_recognition]
  simp only [Periodic.periodicValue, Periodic.blockBase, Nat.cast_pow, Nat.cast_ofNat]

/-- These are evaluations of previously generated readers, not a TPK selector. -/
def composedApprox (register : RadixRecovery.K12) (n : Nat) : ℝ :=
  ((ClosureAnalytic.lowerQ n : ℝ) - 3) + (PropagationLimit.partialSum n - 2) -
    (AutoscaleLimit.ratio n - 1) - Periodic.reader register n

theorem composed_approx_tendsto (register : RadixRecovery.K12) :
    Tendsto (composedApprox register) atTop (𝓝 (value register)) := by
  have hp := (RadixCellSelection.bracket_limits_of_width
    ClosureAnalytic.lowerQ ClosureAnalytic.upperQ ClosureAnalytic.value
    ClosureAnalytic.rational_brackets ClosureAnalytic.width_tendsto_zero).1
  exact (((hp.sub_const 3).add (PropagationLimit.partial_tendsto.sub_const 2)).sub
    (autoscale_limit.sub_const 1)).sub (Periodic.reader_tendsto register)

/-- At full-register depths, the K-reader limit is proved from repeated
digits. Only the three regional block-reader identifications remain inputs. -/
theorem registered_alpha_limit (register : RadixRecovery.K12)
    (blocks : Nat → List AlphaCarry.InputBlock) (boundary : Nat → Int) (C : ℝ)
    (hp : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.p))
      atTop (𝓝 (ClosureAnalytic.value - 3)))
    (he : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.e))
      atTop (𝓝 (PropagationLimit.value - 2)))
    (hphi : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.phi))
      atTop (𝓝 (autoscaleValue - 1)))
    (hk : ∀ n, (blocks n).map AlphaCarry.InputBlock.k =
      (Periodic.repeatedDigits register n).map Int.ofNat)
    (hbound : ∀ n, |(boundary n : ℝ)| ≤ C)
    (hy0 : 0 < value register) (hy1 : value register < 1) :
    Tendsto (fun n => closedRead ((blocks n).map AlphaCarry.InputBlock.balance) (boundary n))
      atTop (𝓝 (value register)) := by
  have hklim : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.k))
      atTop (𝓝 (Periodic.periodicValue register)) := by
    simpa only [hk, repeated_register_read] using Periodic.reader_tendsto register
  have hsource : Tendsto (fun n => readWord ((blocks n).map AlphaCarry.InputBlock.balance))
      atTop (𝓝 (value register)) := by
    simpa only [balance_read, value] using ((hp.add he).sub hphi).sub hklim
  have hlength : ∀ n, (blocks n).length = 12 * n := by
    intro n
    have h := congrArg List.length (hk n)
    simpa only [List.length_map, Periodic.repeatedDigits_length] using h
  have ht : Tendsto (fun n => ((blocks n).map AlphaCarry.InputBlock.balance).length)
      atTop atTop := by
    simp only [List.length_map, hlength]
    exact tendsto_atTop.2 (fun b => eventually_atTop.2 ⟨b, fun a ha => by omega⟩)
  exact closure_limit_of_unit_interval _ boundary (value register) hy0 hy1 hsource
    (bounded_boundary_vanishes_at_lengths boundary _ C hbound ht)

end AlphaCarryLimit
end

#print axioms AlphaCarryLimit.normalized_telescoping
#print axioms AlphaCarryLimit.closed_read_formula
#print axioms AlphaCarryLimit.balance_read
#print axioms AlphaCarryLimit.inverse_scale_tendsto_zero
#print axioms AlphaCarryLimit.bounded_boundary_vanishes
#print axioms AlphaCarryLimit.closure_limit
#print axioms AlphaCarryLimit.closure_limit_bounded
#print axioms AlphaCarryLimit.alpha_reader_limit
#print axioms AlphaCarryLimit.Periodic.blockBase_gt_one
#print axioms AlphaCarryLimit.Periodic.encode_append
#print axioms AlphaCarryLimit.Periodic.prefix_eq_encode
#print axioms AlphaCarryLimit.Periodic.repeatedDigits_length
#print axioms AlphaCarryLimit.Periodic.repeatedDigits_valid
#print axioms AlphaCarryLimit.Periodic.prefix_recovers_repeatedDigits
#print axioms AlphaCarryLimit.Periodic.prefix_geometric_identity
#print axioms AlphaCarryLimit.Periodic.reader_closed
#print axioms AlphaCarryLimit.Periodic.reader_tendsto
#print axioms AlphaCarryLimit.Periodic.reader_error_exact
#print axioms AlphaCarryLimit.Periodic.reader_one
#print axioms AlphaCarryLimit.Periodic.periodic_sub_finite
#print axioms AlphaCarryLimit.Periodic.periodic_sub_finite_eq_scaled
#print axioms AlphaCarryLimit.Periodic.periodic_integer_recovery
#print axioms AlphaCarryLimit.Periodic.periodic_digits_recovery
#print axioms AlphaCarryLimit.evaluate_nat_digits
#print axioms AlphaCarryLimit.repeated_register_read
#print axioms AlphaCarryLimit.bounded_boundary_vanishes_at_lengths
#print axioms AlphaCarryLimit.evaluate_digit_bounds
#print axioms AlphaCarryLimit.closed_read_bounds
#print axioms AlphaCarryLimit.front_eventually_zero
#print axioms AlphaCarryLimit.closure_limit_of_unit_interval
#print axioms AlphaCarryLimit.autoscale_limit
#print axioms AlphaCarryLimit.autoscale_recognition
#print axioms AlphaCarryLimit.integer_shift_origin
#print axioms AlphaCarryLimit.value_composition
#print axioms AlphaCarryLimit.value_recognition
#print axioms AlphaCarryLimit.composed_approx_tendsto
#print axioms AlphaCarryLimit.registered_alpha_limit
