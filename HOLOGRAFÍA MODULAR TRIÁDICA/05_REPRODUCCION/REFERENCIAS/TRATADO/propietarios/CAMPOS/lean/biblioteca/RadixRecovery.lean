/-
  Reversible radix publication, Lean 4.21.0 + Std.
  Provenance: registro_k.tex, eq:k-numerador, and k_reversibilidad.tex,
  proposition "Recuperación integral y transformación cíclica".
  This file starts with a supplied finite digit register. It proves the
  information-preserving publication/reader, not TPK event production of K.
-/
import Std

namespace RadixRecovery

def appendDigit (base initial digit : Nat) : Nat := base * initial + digit

theorem appendDigit_div (base initial digit : Nat) (hb : 0 < base)
    (hd : digit < base) : appendDigit base initial digit / base = initial := by
  unfold appendDigit
  rw [Nat.mul_add_div hb, Nat.div_eq_of_lt hd, Nat.add_zero]

theorem appendDigit_mod (base initial digit : Nat) (hd : digit < base) :
    appendDigit base initial digit % base = digit := by
  unfold appendDigit
  rw [Nat.mul_add_mod, Nat.mod_eq_of_lt hd]

def Valid (base : Nat) (digits : List Nat) : Prop :=
  ∀ digit ∈ digits, digit < base

-- The auxiliary reader is little-endian; the public interface is big-endian.
def encodeLE (base : Nat) : List Nat → Nat
  | [] => 0
  | digit :: tail => appendDigit base (encodeLE base tail) digit

def decodeLE (base : Nat) : Nat → Nat → List Nat
  | 0, _ => []
  | n + 1, value => value % base :: decodeLE base n (value / base)

def encode (base : Nat) (digits : List Nat) : Nat :=
  encodeLE base digits.reverse

def decode (base width value : Nat) : List Nat :=
  (decodeLE base width value).reverse

theorem decodeLE_length (base width value : Nat) :
    (decodeLE base width value).length = width := by
  induction width generalizing value with
  | zero => rfl
  | succ n ih => simp only [decodeLE, List.length_cons, ih]

theorem decode_length (base width value : Nat) :
    (decode base width value).length = width := by
  simp only [decode, List.length_reverse, decodeLE_length]

theorem decodeLE_encodeLE (base : Nat) (hb : 0 < base) (digits : List Nat)
    (hv : Valid base digits) :
    decodeLE base digits.length (encodeLE base digits) = digits := by
  induction digits with
  | nil => rfl
  | cons digit tail ih =>
    have hd : digit < base := hv digit (by simp)
    have ht : Valid base tail := by
      intro d hm
      exact hv d (by simp [hm])
    simp only [List.length_cons, encodeLE, decodeLE,
      appendDigit_div base _ digit hb hd, appendDigit_mod base _ digit hd]
    rw [ih ht]

-- No bound on the supplied list length; zero-valued leading blocks are retained.
theorem decode_encode (base : Nat) (hb : 0 < base) (digits : List Nat)
    (hv : Valid base digits) :
    decode base digits.length (encode base digits) = digits := by
  have hr : Valid base digits.reverse := by
    intro d hm
    exact hv d (List.mem_reverse.mp hm)
  unfold decode encode
  rw [← List.length_reverse (as := digits), decodeLE_encodeLE base hb _ hr,
    List.reverse_reverse]

theorem encode_injective_fixed_length (base width : Nat) (hb : 0 < base)
    (left right : List Nat) (hl : Valid base left) (hr : Valid base right)
    (hll : left.length = width) (hrl : right.length = width)
    (he : encode base left = encode base right) : left = right := by
  have dl := decode_encode base hb left hl
  have dr := decode_encode base hb right hr
  rw [hll] at dl
  rw [hrl] at dr
  rw [← dl, ← dr, he]

theorem encode_append_digit (base : Nat) (digits : List Nat) (digit : Nat) :
    encode base (digits ++ [digit]) = appendDigit base (encode base digits) digit := by
  simp [encode, List.reverse_append, encodeLE]

theorem encodeLE_append (base : Nat) (left right : List Nat) :
    encodeLE base (left ++ right) =
      encodeLE base left + base ^ left.length * encodeLE base right := by
  induction left with
  | nil => simp [encodeLE]
  | cons digit tail ih =>
    simp only [List.cons_append, encodeLE, appendDigit, List.length_cons, ih,
      Nat.pow_succ, Nat.mul_add, Nat.add_mul]
    simp [Nat.mul_assoc, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm,
      Nat.mul_comm, Nat.mul_left_comm]

theorem encode_cons (base digit : Nat) (tail : List Nat) :
    encode base (digit :: tail) = digit * base ^ tail.length + encode base tail := by
  simp [encode, List.reverse_cons, encodeLE_append, encodeLE, appendDigit,
    Nat.mul_comm, Nat.add_comm]

-- Width is part of the type; it is not inferred from a numeral that drops zeros.
structure Register (base width : Nat) where
  digits : List Nat
  valid : Valid base digits
  length_eq : digits.length = width

def Register.publish {base width : Nat} (register : Register base width) : Nat :=
  encode base register.digits

theorem Register.recover {base width : Nat} (hb : 0 < base)
    (register : Register base width) :
    decode base width register.publish = register.digits := by
  have h := decode_encode base hb register.digits register.valid
  simpa only [register.length_eq] using h

abbrev K12 := Register 1000 12

theorem k12_recover (register : K12) :
    decode 1000 12 register.publish = register.digits :=
  Register.recover (by decide) register

theorem leading_zero_preserved (base : Nat) (hb : 0 < base)
    (digits : List Nat) (hv : Valid base digits) :
    decode base (digits.length + 1) (encode base (0 :: digits)) = 0 :: digits := by
  exact decode_encode base hb (0 :: digits) (by
    intro d hm
    cases hm with
    | head => exact hb
    | tail _ ht => exact hv d ht)

-- Integer rather than truncated-natural subtraction records the exact identity.
-- The supplied list is nonempty and rotation moves its first block to the end.
theorem rotation_integer (base first : Nat) (tail : List Nat) :
    (encode base (tail ++ [first]) : Int) =
      (base : Int) * (encode base (first :: tail) : Int) -
        (first : Int) * ((base : Int) ^ (tail.length + 1) - 1) := by
  rw [encode_append_digit, encode_cons]
  simp only [appendDigit, Int.natCast_add, Int.natCast_mul, Int.natCast_pow,
    Int.pow_succ, Int.mul_add, Int.mul_sub, Int.mul_one]
  have hc : (base : Int) * ((first : Int) * (base : Int) ^ tail.length) =
      (first : Int) * ((base : Int) ^ tail.length * (base : Int)) := by
    simp [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  rw [hc]
  omega

theorem rotation_twelve (base first : Nat) (tail : List Nat)
    (hl : tail.length = 11) :
    (encode base (tail ++ [first]) : Int) =
      (base : Int) * (encode base (first :: tail) : Int) -
        (first : Int) * ((base : Int) ^ 12 - 1) := by
  simpa only [hl] using rotation_integer base first tail

theorem k12_rotation (register : K12) (first : Nat) (tail : List Nat)
    (hshape : register.digits = first :: tail) :
    (encode 1000 (tail ++ [first]) : Int) =
      1000 * (register.publish : Int) - (first : Int) * ((1000 : Int) ^ 12 - 1) := by
  have hl : tail.length = 11 := by
    have h := register.length_eq
    rw [hshape, List.length_cons] at h
    omega
  unfold Register.publish
  rw [hshape]
  exact rotation_twelve 1000 first tail hl

#print axioms appendDigit_div
#print axioms appendDigit_mod
#print axioms decodeLE_length
#print axioms decode_length
#print axioms decodeLE_encodeLE
#print axioms decode_encode
#print axioms encode_injective_fixed_length
#print axioms encode_append_digit
#print axioms encodeLE_append
#print axioms encode_cons
#print axioms Register.recover
#print axioms k12_recover
#print axioms leading_zero_preserved
#print axioms rotation_integer
#print axioms rotation_twelve
#print axioms k12_rotation

end RadixRecovery
