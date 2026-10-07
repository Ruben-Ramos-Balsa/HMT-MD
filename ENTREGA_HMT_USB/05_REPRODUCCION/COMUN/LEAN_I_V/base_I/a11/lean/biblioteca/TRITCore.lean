/-
  TRIT balanced coordinates and integer quadratic realization.
  Lean 4.21.0 + Std; no real exponential or analytic assertion is made here.
  Source: article I, manuscript_es/sections/trit_desarrollo.tex and nucleo.tex.
  The input is an integer APP evaluation. The cutoff is the local TRIT chart:
  its carry is retained; this chart does not replace the enriched TPK history.
-/
import Std

namespace TRITCore

/-- The signed residue type, not an untyped integer label. -/
def Digit := { r : Int // -1 ≤ r ∧ r ≤ 1 }

def quotient (n : Int) : Int := (n + 1) / 3

def residue (n : Int) : Int := n - 3 * quotient n

theorem residue_bounds (n : Int) : -1 ≤ residue n ∧ residue n ≤ 1 := by
  unfold residue quotient
  omega

theorem residue_cases (n : Int) :
    residue n = -1 ∨ residue n = 0 ∨ residue n = 1 := by
  have h := residue_bounds n
  omega

def balanced (n : Int) : Digit × Int := (⟨residue n, residue_bounds n⟩, quotient n)

def reconstruct (p : Digit × Int) : Int := p.1.val + 3 * p.2

theorem reconstruction (n : Int) : n = residue n + 3 * quotient n := by
  unfold residue
  omega

theorem reconstruct_balanced (n : Int) : reconstruct (balanced n) = n := by
  exact (reconstruction n).symm

theorem balanced_unique (r s : Digit) (c d : Int)
    (h : r.val + 3 * c = s.val + 3 * d) : r = s ∧ c = d := by
  have hr := r.property
  have hs := s.property
  have hrs : r.val = s.val := by omega
  constructor
  · exact Subtype.ext hrs
  · omega

theorem balanced_reconstruct (p : Digit × Int) : balanced (reconstruct p) = p := by
  have h := balanced_unique (balanced (reconstruct p)).1 p.1
    (balanced (reconstruct p)).2 p.2 (reconstruct_balanced (reconstruct p))
  exact Prod.ext h.1 h.2

theorem reconstruct_injective (p q : Digit × Int)
    (h : reconstruct p = reconstruct q) : p = q := by
  rw [← balanced_reconstruct p, ← balanced_reconstruct q, h]

theorem residue_mod (n : Int) : residue n % 3 = n % 3 := by
  unfold residue quotient
  omega

/-- The phase reader extends the three canonical classes to all integers.
    It is a selector, not a cardinal transport. -/
def phase (n : Int) : Int := if n % 3 = 0 then 0 else if n % 3 = 1 then 1 else -1

theorem residue_eq_phase (n : Int) : residue n = phase n := by
  have hb := residue_bounds n
  have hm := residue_mod n
  unfold phase
  split <;> (try split) <;> omega

theorem phase_periodic (n k : Int) : phase (n + 3 * k) = phase n := by
  have h : (n + 3 * k) % 3 = n % 3 := by omega
  simp only [phase, h]

theorem phase_nonadic_values :
    [phase 1, phase 2, phase 3, phase 4, phase 5, phase 6,
     phase 7, phase 8, phase 9] = [1, -1, 0, 1, -1, 0, 1, -1, 0] := by
  decide

theorem quotient_shift (n k : Int) : quotient (n + 3 * k) = quotient n + k := by
  unfold quotient
  omega

theorem residue_shift (n k : Int) : residue (n + 3 * k) = residue n := by
  unfold residue
  rw [quotient_shift]
  omega

theorem residue_neg (n : Int) : residue (-n) = -residue n := by
  have hp := residue_bounds n
  have hn := residue_bounds (-n)
  have rp := reconstruction n
  have rn := reconstruction (-n)
  omega

theorem quotient_neg (n : Int) : quotient (-n) = -quotient n := by
  have hp := reconstruction n
  have hn := reconstruction (-n)
  rw [residue_neg] at hn
  omega

theorem zero_residue_retains_carry (c : Int) :
    residue (3 * c) = 0 ∧ quotient (3 * c) = c := by
  unfold residue quotient
  omega

theorem visible_residue_not_injective : residue 0 = residue 3 ∧ (0 : Int) ≠ 3 := by
  decide

theorem digit_cases (r : Digit) : r.val = -1 ∨ r.val = 0 ∨ r.val = 1 := by
  have h := r.property
  omega

/-- The carry of a sum of signed representatives. -/
def carry (r s : Int) : Int := quotient (r + s)

theorem carry_formula (r s : Int) :
    carry r s = (r + s - residue (r + s)) / 3 := by
  unfold carry residue
  omega

/-- Explicit transported addition; the residual carry updates the second level. -/
def pairAdd (p q : Digit × Int) : Digit × Int :=
  (⟨residue (p.1.val + q.1.val), residue_bounds _⟩,
   p.2 + q.2 + carry p.1.val q.1.val)

theorem reconstruct_pairAdd (p q : Digit × Int) :
    reconstruct (pairAdd p q) = reconstruct p + reconstruct q := by
  have h := reconstruction (p.1.val + q.1.val)
  unfold reconstruct pairAdd carry
  dsimp
  omega

theorem digit_product_bounds (r s : Digit) :
    -1 ≤ r.val * s.val ∧ r.val * s.val ≤ 1 := by
  have hs := s.property
  rcases digit_cases r with h | h | h <;> simp [h] <;> omega

/-- Multiplication retains the two cross terms and the product of carries. -/
def pairMul (p q : Digit × Int) : Digit × Int :=
  (⟨p.1.val * q.1.val, digit_product_bounds p.1 q.1⟩,
   p.1.val * q.2 + q.1.val * p.2 + 3 * p.2 * q.2)

theorem reconstruct_pairMul (p q : Digit × Int) :
    reconstruct (pairMul p q) = reconstruct p * reconstruct q := by
  simp only [reconstruct, pairMul, Int.mul_add, Int.add_mul]
  simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm,
    Int.add_assoc, Int.add_comm, Int.add_left_comm]

theorem pairAdd_associative (p q t : Digit × Int) :
    pairAdd (pairAdd p q) t = pairAdd p (pairAdd q t) := by
  apply reconstruct_injective
  simp only [reconstruct_pairAdd, Int.add_assoc]

theorem carry_cocycle (r s t : Int) :
    carry r s + carry (residue (r + s)) t =
    carry s t + carry r (residue (s + t)) := by
  unfold carry residue quotient
  omega

/-- Coordinatewise addition and scalar multiplication on the integer plane. -/
abbrev Plane := Int × Int

def add (v w : Plane) : Plane := (v.1 + w.1, v.2 + w.2)

def scale (a : Int) (v : Plane) : Plane := (a * v.1, a * v.2)

/-- Integral realization of the already selected quadratic type. -/
def J (τ : Int) (v : Plane) : Plane := (-τ * v.2, v.1)

theorem J_add (τ : Int) (v w : Plane) : J τ (add v w) = add (J τ v) (J τ w) := by
  apply Prod.ext
  · simp only [J, add, Int.mul_add]
  · rfl

theorem J_scale (τ a : Int) (v : Plane) : J τ (scale a v) = scale a (J τ v) := by
  apply Prod.ext
  · simp only [J, scale]
    rw [← Int.mul_assoc, ← Int.mul_assoc, Int.mul_comm (-τ) a]
  · rfl

theorem J_square (τ : Int) (v : Plane) : J τ (J τ v) = scale (-τ) v := by
  rfl

def iterateJ (τ : Int) : Nat → Plane → Plane
  | 0, v => v
  | n + 1, v => J τ (iterateJ τ n v)

theorem iterateJ_two_step (τ : Int) (n : Nat) (v : Plane) :
    iterateJ τ (n + 2) v = scale (-τ) (iterateJ τ n v) := by
  exact J_square τ (iterateJ τ n v)

theorem scale_scale (a b : Int) (v : Plane) :
    scale a (scale b v) = scale (a * b) v := by
  apply Prod.ext <;> simp only [scale, Int.mul_assoc]

theorem scale_one (v : Plane) : scale 1 v = v := by
  apply Prod.ext <;> simp [scale]

theorem iterateJ_even (τ : Int) (n : Nat) (v : Plane) :
    iterateJ τ (2 * n) v = scale ((-τ) ^ n) v := by
  induction n with
  | zero => simp only [Nat.mul_zero, iterateJ, Int.pow_zero, scale_one]
  | succ n ih =>
    have hi : 2 * (n + 1) = 2 * n + 2 := by omega
    rw [hi, iterateJ_two_step, ih, scale_scale, Int.pow_succ]
    rw [Int.mul_comm (-τ) ((-τ) ^ n)]

theorem iterateJ_odd (τ : Int) (n : Nat) (v : Plane) :
    iterateJ τ (2 * n + 1) v = scale ((-τ) ^ n) (J τ v) := by
  change J τ (iterateJ τ (2 * n) v) = _
  rw [iterateJ_even, J_scale]

theorem elliptic_square (v : Plane) : J 1 (J 1 v) = scale (-1) v := by
  exact J_square 1 v

theorem parabolic_square (v : Plane) : J 0 (J 0 v) = (0, 0) := by
  simp [J]

theorem hyperbolic_square (v : Plane) : J (-1) (J (-1) v) = v := by
  simp [J]

theorem parabolic_nonzero : J 0 (1, 0) ≠ (0, 0) := by decide

theorem elliptic_fourth (v : Plane) : iterateJ 1 4 v = v := by
  simp [iterateJ, J]

#print axioms residue_bounds
#print axioms residue_cases
#print axioms reconstruction
#print axioms reconstruct_balanced
#print axioms balanced_unique
#print axioms balanced_reconstruct
#print axioms reconstruct_injective
#print axioms residue_mod
#print axioms residue_eq_phase
#print axioms phase_periodic
#print axioms phase_nonadic_values
#print axioms quotient_shift
#print axioms residue_shift
#print axioms residue_neg
#print axioms quotient_neg
#print axioms zero_residue_retains_carry
#print axioms visible_residue_not_injective
#print axioms digit_cases
#print axioms carry_formula
#print axioms reconstruct_pairAdd
#print axioms digit_product_bounds
#print axioms reconstruct_pairMul
#print axioms pairAdd_associative
#print axioms carry_cocycle
#print axioms J_add
#print axioms J_scale
#print axioms J_square
#print axioms iterateJ_two_step
#print axioms scale_scale
#print axioms scale_one
#print axioms iterateJ_even
#print axioms iterateJ_odd
#print axioms elliptic_square
#print axioms parabolic_square
#print axioms hyperbolic_square
#print axioms parabolic_nonzero
#print axioms elliptic_fourth

end TRITCore
