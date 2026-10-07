import AlphaPositionalBridge
import AlphaCarry
import Mathlib.Tactic

/-!
# Canonical compatible boundary of the posterior alpha closure

The four unit-interval coordinates are already produced readers. Their
positional publication determines every finite prefix and remote carry.
The register, when specialized below, is supplied upstream of alpha.
Source: source_passages/alpha.tex, lines 195–310.
-/

noncomputable section
open Filter Topology

namespace AlphaCanonicalSection

def InUnit (x : ℝ) : Prop := 0 ≤ x ∧ x < 1

abbrev intPrefix := AlphaPositionalBridge.integerPublication
abbrev digits := AlphaPositionalBridge.positionalDigits

def total (p e f k : ℝ) : ℝ := p + e - f - k
def sourcePrefix (p e f k : ℝ) (n : Nat) : Int :=
  intPrefix p n + intPrefix e n - intPrefix f n - intPrefix k n

/-- This is source c_(N+1); index n counts the number of preceding blocks. -/
def carry (p e f k : ℝ) (n : Nat) : Int :=
  intPrefix (total p e f k) n - sourcePrefix p e f k n

def tail (x : ℝ) (n : Nat) : ℝ := x * (1000 : ℝ)^n - (intPrefix x n : ℝ)

theorem tail_bounds (x : ℝ) (n : Nat) : 0 ≤ tail x n ∧ tail x n < 1 := by
  have hl := Int.floor_le (x * (1000 : ℝ)^n)
  have hu := Int.lt_floor_add_one (x * (1000 : ℝ)^n)
  unfold tail intPrefix AlphaPositionalBridge.integerPublication
  constructor <;> linarith

theorem tail_balance (p e f k : ℝ) (n : Nat) :
    total p e f k * (1000 : ℝ)^n = (sourcePrefix p e f k n : ℝ) +
      (tail p n + tail e n - tail f n - tail k n) := by
  simp only [total, sourcePrefix, tail, Int.cast_add, Int.cast_sub]
  ring

theorem carry_is_floor_of_tails (p e f k : ℝ) (n : Nat) :
    carry p e f k n = ⌊tail p n + tail e n - tail f n - tail k n⌋ := by
  unfold carry intPrefix AlphaPositionalBridge.integerPublication
  rw [tail_balance, Int.floor_intCast_add]
  omega

theorem carry_tail_difference (p e f k : ℝ) (n : Nat) :
    (carry p e f k n : ℝ) =
      tail p n + tail e n - tail f n - tail k n - tail (total p e f k) n := by
  simp only [carry, sourcePrefix, tail, total, Int.cast_add, Int.cast_sub]
  ring

theorem carry_bounds (p e f k : ℝ) (n : Nat) :
    (-2 : Int) ≤ carry p e f k n ∧ carry p e f k n ≤ 1 := by
  have hp := tail_bounds p n
  have he := tail_bounds e n
  have hf := tail_bounds f n
  have hk := tail_bounds k n
  rw [carry_is_floor_of_tails]
  constructor
  · apply Int.le_floor.mpr
    norm_num
    linarith
  · have ht : ⌊tail p n + tail e n - tail f n - tail k n⌋ < (2 : Int) :=
      Int.floor_lt.mpr (by norm_num; linarith)
    omega

theorem prefix_zero (x : ℝ) (hx : InUnit x) : intPrefix x 0 = 0 := by
  simp only [intPrefix, AlphaPositionalBridge.integerPublication, pow_zero, mul_one]
  exact Int.floor_eq_zero_iff.mpr hx

theorem carry_zero (p e f k : ℝ) (hp : InUnit p) (he : InUnit e)
    (hf : InUnit f) (hk : InUnit k) (ha : InUnit (total p e f k)) :
    carry p e f k 0 = 0 := by
  simp only [carry, sourcePrefix, prefix_zero _ hp, prefix_zero _ he,
    prefix_zero _ hf, prefix_zero _ hk, prefix_zero _ ha]
  norm_num

theorem prefix_bounds (x : ℝ) (hx : InUnit x) (n : Nat) :
    (0 : Int) ≤ intPrefix x n ∧ intPrefix x n < (1000 : Int)^n := by
  change (0 : Int) ≤ AlphaPositionalBridge.integerPublication x n ∧
    AlphaPositionalBridge.integerPublication x n < (1000 : Int)^n
  rw [← AlphaPositionalBridge.natural_publication_eq x hx.1]
  constructor
  · exact Int.natCast_nonneg _
  · exact_mod_cast AlphaPositionalBridge.natural_publication_bound x hx.1 hx.2 n

theorem digits_evaluate (x : ℝ) (hx : InUnit x) (n : Nat) :
    AlphaCarry.evaluate ((digits x n).map Int.ofNat) = intPrefix x n := by
  rw [AlphaCarryLimit.evaluate_nat_digits,
    AlphaPositionalBridge.positional_digits_encode x hx.1 hx.2,
    AlphaPositionalBridge.natural_publication_eq x hx.1]

theorem int_digits_valid (x : ℝ) (n : Nat) :
    ∀ d ∈ (digits x n).map Int.ofNat, 0 ≤ d ∧ d < 1000 := by
  intro d hd
  obtain ⟨j, hj, rfl⟩ := List.mem_map.mp hd
  constructor
  · exact Int.natCast_nonneg _
  · change (j : Int) < 1000
    exact_mod_cast AlphaPositionalBridge.positional_digits_valid x n j hj

theorem evaluate_injective (xs ys : List Int)
    (hx : ∀ d ∈ xs, 0 ≤ d ∧ d < 1000)
    (hy : ∀ d ∈ ys, 0 ≤ d ∧ d < 1000)
    (hlen : xs.length = ys.length)
    (heq : AlphaCarry.evaluate xs = AlphaCarry.evaluate ys) : xs = ys := by
  induction xs generalizing ys with
  | nil =>
    have : ys = [] := List.length_eq_zero_iff.mp hlen.symm
    exact this.symm
  | cons x xs ih =>
    cases ys with
    | nil => simp at hlen
    | cons y ys =>
      have hl : xs.length = ys.length := Nat.add_right_cancel hlen
      have hxt : ∀ d ∈ xs, 0 ≤ d ∧ d < 1000 := by
        intro d hd; exact hx d (by simp [hd])
      have hyt : ∀ d ∈ ys, 0 ≤ d ∧ d < 1000 := by
        intro d hd; exact hy d (by simp [hd])
      have bx := AlphaCarryLimit.evaluate_digit_bounds xs hxt
      have bys := AlphaCarryLimit.evaluate_digit_bounds ys hyt
      rw [← hl] at bys
      simp only [AlphaCarry.evaluate, ← hl] at heq
      have hpow : (0 : Int) < 1000 ^ xs.length := by positivity
      have hxy : x = y := by
        by_contra hn
        rcases lt_or_gt_of_ne hn with hlt | hgt
        · have hm := mul_le_mul_of_nonneg_right (show x + 1 ≤ y by omega) hpow.le
          nlinarith
        · have hm := mul_le_mul_of_nonneg_right (show y + 1 ≤ x by omega) hpow.le
          nlinarith
      subst y
      have ht : AlphaCarry.evaluate xs = AlphaCarry.evaluate ys := by linarith
      rw [ih ys hxt hyt hl ht]

/-- An integer conservation equation in the canonical digit range determines
both the front carry and the complete normalized word. -/
theorem closure_exact_from_evaluation (zs : List Int) (boundary : Int)
    (x : ℝ) (hx : InUnit x)
    (heq : AlphaCarry.evaluate zs + boundary = intPrefix x zs.length) :
    (AlphaCarry.close zs boundary).outgoing = 0 ∧
      (AlphaCarry.close zs boundary).digits = (digits x zs.length).map Int.ofNat := by
  have hcons := AlphaCarry.closure_conservation zs boundary
  rw [heq] at hcons
  have hd := AlphaCarryLimit.evaluate_digit_bounds (AlphaCarry.close zs boundary).digits
    (AlphaCarry.close_digit_bounds zs boundary)
  rw [AlphaCarry.close_length] at hd
  have hp := prefix_bounds x hx zs.length
  have hpow : (0 : Int) < 1000 ^ zs.length := by positivity
  have hc : (AlphaCarry.close zs boundary).outgoing = 0 := by
    by_contra hn
    rcases lt_or_gt_of_ne hn with hlt | hgt
    · have hm := mul_le_mul_of_nonneg_left
        (show (AlphaCarry.close zs boundary).outgoing ≤ -1 by omega) hpow.le
      nlinarith
    · have hm := mul_le_mul_of_nonneg_left
        (show 1 ≤ (AlphaCarry.close zs boundary).outgoing by omega) hpow.le
      nlinarith
  refine ⟨hc, ?_⟩
  apply evaluate_injective _ _ (AlphaCarry.close_digit_bounds zs boundary) (int_digits_valid _ _)
  · simp only [AlphaCarry.close_length, List.length_map,
      AlphaPositionalBridge.positional_digits_length]
  · rw [digits_evaluate x hx]
    simpa only [hc, mul_zero, add_zero] using hcons

theorem drop_decodeLE (base n m value : Nat) :
    (RadixRecovery.decodeLE base (n + m) value).drop m =
      RadixRecovery.decodeLE base n (value / base ^ m) := by
  induction m generalizing value with
  | zero => simp
  | succ m ih =>
    rw [show n + (m + 1) = (n + m) + 1 by omega]
    simp only [RadixRecovery.decodeLE, List.drop_succ_cons]
    rw [ih]
    simp only [Nat.div_div_eq_div_mul, pow_succ, Nat.mul_comm]

theorem take_decode (base n m value : Nat) :
    (RadixRecovery.decode base (n + m) value).take n =
      RadixRecovery.decode base n (value / base ^ m) := by
  unfold RadixRecovery.decode
  rw [List.take_reverse, RadixRecovery.decodeLE_length]
  rw [show n + m - n = m by omega, drop_decodeLE]

theorem digits_compatible (x : ℝ) (n m : Nat) :
    (digits x (n + m)).take n = digits x n := by
  unfold digits AlphaPositionalBridge.positionalDigits
  rw [take_decode, AlphaPositionalBridge.natural_publication_truncate]

/-- Four posterior positional columns at one common depth. -/
def blocks (p e f k : ℝ) (n : Nat) : List AlphaCarry.InputBlock :=
  List.ofFn (fun i : Fin n =>
    ⟨(AlphaPositionalBridge.wordAt (digits p n)
        (AlphaPositionalBridge.positional_digits_length _ _) i : Int),
     (AlphaPositionalBridge.wordAt (digits e n)
        (AlphaPositionalBridge.positional_digits_length _ _) i : Int),
     (AlphaPositionalBridge.wordAt (digits f n)
        (AlphaPositionalBridge.positional_digits_length _ _) i : Int),
     (AlphaPositionalBridge.wordAt (digits k n)
        (AlphaPositionalBridge.positional_digits_length _ _) i : Int)⟩)

theorem blocks_p (p e f k : ℝ) (n : Nat) :
    (blocks p e f k n).map AlphaCarry.InputBlock.p = (digits p n).map Int.ofNat := by
  simpa only [blocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (AlphaPositionalBridge.ofFn_wordAt (digits p n) n
      (AlphaPositionalBridge.positional_digits_length _ _))

theorem blocks_e (p e f k : ℝ) (n : Nat) :
    (blocks p e f k n).map AlphaCarry.InputBlock.e = (digits e n).map Int.ofNat := by
  simpa only [blocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (AlphaPositionalBridge.ofFn_wordAt (digits e n) n
      (AlphaPositionalBridge.positional_digits_length _ _))

theorem blocks_phi (p e f k : ℝ) (n : Nat) :
    (blocks p e f k n).map AlphaCarry.InputBlock.phi = (digits f n).map Int.ofNat := by
  simpa only [blocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (AlphaPositionalBridge.ofFn_wordAt (digits f n) n
      (AlphaPositionalBridge.positional_digits_length _ _))

theorem blocks_k (p e f k : ℝ) (n : Nat) :
    (blocks p e f k n).map AlphaCarry.InputBlock.k = (digits k n).map Int.ofNat := by
  simpa only [blocks, List.map_ofFn, Function.comp_apply] using
    congrArg (List.map Int.ofNat) (AlphaPositionalBridge.ofFn_wordAt (digits k n) n
      (AlphaPositionalBridge.positional_digits_length _ _))

theorem blocks_length (p e f k : ℝ) (n : Nat) : (blocks p e f k n).length = n := by
  simp [blocks]

theorem balance_evaluate (p e f k : ℝ) (hp : InUnit p) (he : InUnit e)
    (hf : InUnit f) (hk : InUnit k) (n : Nat) :
    AlphaCarry.evaluate ((blocks p e f k n).map AlphaCarry.InputBlock.balance) =
      sourcePrefix p e f k n := by
  rw [AlphaCarry.balance_evaluation, blocks_p, blocks_e, blocks_phi, blocks_k,
    digits_evaluate p hp, digits_evaluate e he, digits_evaluate f hf, digits_evaluate k hk]
  rfl

theorem canonical_closure (p e f k : ℝ) (hp : InUnit p) (he : InUnit e)
    (hf : InUnit f) (hk : InUnit k) (ha : InUnit (total p e f k)) (n : Nat) :
    (AlphaCarry.close ((blocks p e f k n).map AlphaCarry.InputBlock.balance)
      (carry p e f k n)).outgoing = 0 ∧
    (AlphaCarry.close ((blocks p e f k n).map AlphaCarry.InputBlock.balance)
      (carry p e f k n)).digits = (digits (total p e f k) n).map Int.ofNat := by
  have h := closure_exact_from_evaluation
    ((blocks p e f k n).map AlphaCarry.InputBlock.balance)
    (carry p e f k n) (total p e f k) ha (by
      rw [balance_evaluate p e f k hp he hf hk]
      simp only [List.length_map, blocks_length, carry]
      omega)
  simpa only [List.length_map, blocks_length] using h

theorem canonical_closure_compatible (p e f k : ℝ) (hp : InUnit p) (he : InUnit e)
    (hf : InUnit f) (hk : InUnit k) (ha : InUnit (total p e f k)) (n m : Nat) :
    ((AlphaCarry.close ((blocks p e f k (n + m)).map AlphaCarry.InputBlock.balance)
      (carry p e f k (n + m))).digits).take n =
    (AlphaCarry.close ((blocks p e f k n).map AlphaCarry.InputBlock.balance)
      (carry p e f k n)).digits := by
  rw [(canonical_closure p e f k hp he hf hk ha (n + m)).2,
    (canonical_closure p e f k hp he hf hk ha n).2, ← List.map_take, digits_compatible]

theorem canonical_boundary_unique (p e f k : ℝ) (hp : InUnit p) (he : InUnit e)
    (hf : InUnit f) (hk : InUnit k) (ha : InUnit (total p e f k)) (n : Nat)
    (boundary : Int)
    (hout : (AlphaCarry.close ((blocks p e f k n).map AlphaCarry.InputBlock.balance)
      boundary).outgoing = 0)
    (hdigits : (AlphaCarry.close ((blocks p e f k n).map AlphaCarry.InputBlock.balance)
      boundary).digits = (digits (total p e f k) n).map Int.ofNat) :
    boundary = carry p e f k n := by
  have hc := AlphaCarry.closure_conservation
    ((blocks p e f k n).map AlphaCarry.InputBlock.balance) boundary
  rw [hout, hdigits, mul_zero, add_zero, digits_evaluate _ ha,
    balance_evaluate p e f k hp he hf hk] at hc
  unfold carry
  omega

def digit (x : ℝ) (n : Nat) : Int := intPrefix x (n + 1) - 1000 * intPrefix x n

theorem local_carry_equation (p e f k : ℝ) (n : Nat) :
    digit (total p e f k) n + 1000 * carry p e f k n =
      digit p n + digit e n - digit f n - digit k n + carry p e f k (n + 1) := by
  simp only [digit, carry, sourcePrefix]
  ring

open AlphaCarryLimit.Periodic

theorem periodic_scaled (register : RadixRecovery.K12) (n : Nat) :
    periodicValue register * (1000 : ℝ) ^ (12 * n) =
      (blockPrefix register n : ℝ) + periodicValue register := by
  have hg := prefix_geometric_identity register n
  have hr := periodic_integer_recovery register
  have hd : (blockBase : ℝ) - 1 ≠ 0 := ne_of_gt (sub_pos.mpr blockBase_gt_one)
  have hpow : (1000 : ℝ) ^ (12 * n) = (blockBase : ℝ)^n := by
    simp only [blockBase, Nat.cast_pow, Nat.cast_ofNat, pow_mul]
  rw [hpow]
  apply (mul_right_cancel₀ hd)
  calc
    (periodicValue register * (blockBase : ℝ)^n) * ((blockBase : ℝ) - 1) =
        ((blockBase : ℝ) - 1) * periodicValue register * (blockBase : ℝ)^n := by ring
    _ = (register.publish : ℝ) * (blockBase : ℝ)^n := by rw [hr]
    _ = ((blockPrefix register n : ℝ) + periodicValue register) *
        ((blockBase : ℝ) - 1) := by nlinarith [hg, hr]

theorem periodic_prefix (register : RadixRecovery.K12)
    (hk : InUnit (periodicValue register)) (n : Nat) :
    intPrefix (periodicValue register) (12 * n) = (blockPrefix register n : Int) := by
  unfold intPrefix AlphaPositionalBridge.integerPublication
  rw [periodic_scaled]
  have hz : ⌊periodicValue register⌋ = (0 : Int) := Int.floor_eq_zero_iff.mpr hk
  rw [Int.floor_natCast_add, hz, add_zero]

theorem periodic_natural_prefix (register : RadixRecovery.K12)
    (hk : InUnit (periodicValue register)) (n : Nat) :
    AlphaPositionalBridge.naturalPublication (periodicValue register) (12 * n) =
      blockPrefix register n := by
  have h := periodic_prefix register hk n
  change AlphaPositionalBridge.integerPublication (periodicValue register) (12 * n) =
    (blockPrefix register n : Int) at h
  rw [← AlphaPositionalBridge.natural_publication_eq _ hk.1] at h
  exact_mod_cast h

theorem periodic_digits (register : RadixRecovery.K12)
    (hk : InUnit (periodicValue register)) (n : Nat) :
    digits (periodicValue register) (12 * n) = repeatedDigits register n := by
  unfold digits AlphaPositionalBridge.positionalDigits
  rw [periodic_natural_prefix register hk, prefix_recovers_repeatedDigits]

theorem published_blocks_eq (register : RadixRecovery.K12)
    (hk : InUnit (periodicValue register)) (n : Nat) :
    blocks (ClosureAnalytic.value - 3) (PropagationLimit.value - 2)
      (AlphaCarryLimit.autoscaleValue - 1) (periodicValue register) (12 * n) =
        AlphaPositionalBridge.publishedBlocks register n := by
  simp only [blocks, AlphaPositionalBridge.publishedBlocks, periodic_digits register hk]

/-- The compatible remote boundary is computed from the four already published
coordinates; it is not the zero-boundary truncation of a finite computation. -/
def registeredBoundary (register : RadixRecovery.K12) (n : Nat) : Int :=
  carry (ClosureAnalytic.value - 3) (PropagationLimit.value - 2)
    (AlphaCarryLimit.autoscaleValue - 1) (periodicValue register) (12 * n)

theorem registered_boundary_bounds (register : RadixRecovery.K12) (n : Nat) :
    (-2 : Int) ≤ registeredBoundary register n ∧ registeredBoundary register n ≤ 1 :=
  carry_bounds _ _ _ _ _

theorem registered_canonical_closure (register : RadixRecovery.K12)
    (hk : InUnit (periodicValue register)) (ha : InUnit (AlphaCarryLimit.value register))
    (n : Nat) :
    (AlphaCarry.close ((AlphaPositionalBridge.publishedBlocks register n).map
      AlphaCarry.InputBlock.balance) (registeredBoundary register n)).outgoing = 0 ∧
    (AlphaCarry.close ((AlphaPositionalBridge.publishedBlocks register n).map
      AlphaCarry.InputBlock.balance) (registeredBoundary register n)).digits =
        (digits (AlphaCarryLimit.value register) (12 * n)).map Int.ofNat := by
  obtain ⟨hp, he, hf⟩ := AlphaPositionalBridge.fractional_ranges
  have h := canonical_closure (ClosureAnalytic.value - 3) (PropagationLimit.value - 2)
    (AlphaCarryLimit.autoscaleValue - 1) (periodicValue register)
    ⟨hp.1.le, hp.2⟩ ⟨he.1.le, he.2⟩ ⟨hf.1.le, hf.2⟩ hk ha (12 * n)
  rw [published_blocks_eq register hk] at h
  exact h

theorem registered_closure_compatible (register : RadixRecovery.K12)
    (hk : InUnit (periodicValue register)) (ha : InUnit (AlphaCarryLimit.value register))
    (n m : Nat) :
    ((AlphaCarry.close ((AlphaPositionalBridge.publishedBlocks register (n + m)).map
      AlphaCarry.InputBlock.balance) (registeredBoundary register (n + m))).digits).take
        (12 * n) =
    (AlphaCarry.close ((AlphaPositionalBridge.publishedBlocks register n).map
      AlphaCarry.InputBlock.balance) (registeredBoundary register n)).digits := by
  rw [(registered_canonical_closure register hk ha (n + m)).2,
    (registered_canonical_closure register hk ha n).2, ← List.map_take, Nat.mul_add,
    digits_compatible]

theorem registered_boundary_zero (register : RadixRecovery.K12)
    (hk : InUnit (periodicValue register)) (ha : InUnit (AlphaCarryLimit.value register)) :
    registeredBoundary register 0 = 0 := by
  obtain ⟨hp, he, hf⟩ := AlphaPositionalBridge.fractional_ranges
  exact carry_zero _ _ _ _ ⟨hp.1.le, hp.2⟩ ⟨he.1.le, he.2⟩ ⟨hf.1.le, hf.2⟩ hk ha

end AlphaCanonicalSection
end

#print axioms AlphaCanonicalSection.tail_bounds
#print axioms AlphaCanonicalSection.tail_balance
#print axioms AlphaCanonicalSection.carry_is_floor_of_tails
#print axioms AlphaCanonicalSection.carry_tail_difference
#print axioms AlphaCanonicalSection.carry_bounds
#print axioms AlphaCanonicalSection.prefix_zero
#print axioms AlphaCanonicalSection.carry_zero
#print axioms AlphaCanonicalSection.prefix_bounds
#print axioms AlphaCanonicalSection.digits_evaluate
#print axioms AlphaCanonicalSection.int_digits_valid
#print axioms AlphaCanonicalSection.evaluate_injective
#print axioms AlphaCanonicalSection.closure_exact_from_evaluation
#print axioms AlphaCanonicalSection.drop_decodeLE
#print axioms AlphaCanonicalSection.take_decode
#print axioms AlphaCanonicalSection.digits_compatible
#print axioms AlphaCanonicalSection.blocks_p
#print axioms AlphaCanonicalSection.blocks_e
#print axioms AlphaCanonicalSection.blocks_phi
#print axioms AlphaCanonicalSection.blocks_k
#print axioms AlphaCanonicalSection.blocks_length
#print axioms AlphaCanonicalSection.balance_evaluate
#print axioms AlphaCanonicalSection.canonical_closure
#print axioms AlphaCanonicalSection.canonical_closure_compatible
#print axioms AlphaCanonicalSection.canonical_boundary_unique
#print axioms AlphaCanonicalSection.local_carry_equation
#print axioms AlphaCanonicalSection.periodic_scaled
#print axioms AlphaCanonicalSection.periodic_prefix
#print axioms AlphaCanonicalSection.periodic_natural_prefix
#print axioms AlphaCanonicalSection.periodic_digits
#print axioms AlphaCanonicalSection.published_blocks_eq
#print axioms AlphaCanonicalSection.registered_boundary_bounds
#print axioms AlphaCanonicalSection.registered_canonical_closure
#print axioms AlphaCanonicalSection.registered_closure_compatible
#print axioms AlphaCanonicalSection.registered_boundary_zero
