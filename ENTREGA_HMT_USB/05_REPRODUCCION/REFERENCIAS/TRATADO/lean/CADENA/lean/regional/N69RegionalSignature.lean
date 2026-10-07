import Mathlib

/-!
# N69 regional signatures

This module implements the finite signature reader of three ordered HMT
regional bands (clausura, propagación, autoescala), each containing six trits.
The caller supplies the bands, not their signatures. It does not select K,
assume a terminal register, or reconstruct a regional producer backwards.

Source: hmt_puerta_ley01_taxonomia_ciclos.py, `sig`, lines 67–83.
The publication clock is calculated by exact integer logarithm, separately
from the transition index. No floating-point logarithm occurs here.
-/

namespace HMT.N69RegionalSignature

abbrev Band := Fin 6 → Fin 3
abbrev Bands := Fin 3 → Band

def columnTotal (B : Bands) (j : Fin 6) : ℕ :=
  (B 0 j).val + (B 1 j).val + (B 2 j).val

def q (B : Bands) (j : Fin 6) : ℕ := columnTotal B j % 3

/-- The extra 3 keeps subtraction in ℕ exact before taking its residue. -/
def a (B : Bands) (j : Fin 6) : ℕ :=
  ((B 0 j).val + (B 1 j).val + 3 - (B 2 j).val) % 3

def carry (B : Bands) (j : Fin 6) : ℕ := columnTotal B j / 3

def nonzeroIndicator (x : Fin 3) : ℕ := if x.val = 0 then 0 else 1

def columnWeight (B : Bands) (j : Fin 6) : ℕ :=
  nonzeroIndicator (B 0 j) + nonzeroIndicator (B 1 j) +
    nonzeroIndicator (B 2 j)

def columnWeightMod (B : Bands) (j : Fin 6) : ℕ := columnWeight B j % 3

def rowTotal (B : Bands) (i : Fin 3) : ℕ := ∑ j : Fin 6, (B i j).val

def visibleCharge (B : Bands) (i : Fin 3) : ℕ := rowTotal B i % 3

/-- The declared six-coordinate Witt chart, with entries represented in ℕ. -/
def wittMatrix : Fin 6 → Fin 6 → ℕ :=
  ![![0, 1, 1, 1, 1, 1],
    ![1, 0, 1, 1, 2, 2],
    ![1, 1, 0, 2, 1, 2],
    ![1, 1, 2, 0, 2, 1],
    ![1, 2, 1, 2, 0, 1],
    ![1, 2, 2, 1, 1, 0]]

def wittImage (B : Bands) (i : Fin 3) (j : Fin 6) : ℕ :=
  ∑ k : Fin 6, (B i k).val * wittMatrix k j

def wittResidue (B : Bands) (i : Fin 3) (j : Fin 6) : ℕ :=
  wittImage B i j % 3

/-- Sum of the Witt-transformed row, reduced modulo 3 as in the source. -/
def wittDualCharge (B : Bands) (i : Fin 3) : ℕ :=
  (∑ j : Fin 6, wittImage B i j) % 3

structure Signature where
  q : Fin 6 → ℕ
  a : Fin 6 → ℕ
  c : Fin 6 → ℕ
  colw : Fin 6 → ℕ
  colwMod : Fin 6 → ℕ
  visible : Fin 3 → ℕ
  wittDual : Fin 3 → ℕ

def readSignature (B : Bands) : Signature :=
  ⟨q B, a B, carry B, columnWeight B, columnWeightMod B,
    visibleCharge B, wittDualCharge B⟩

theorem columnTotal_le_six (B : Bands) (j : Fin 6) : columnTotal B j ≤ 6 := by
  have h0 := (B 0 j).isLt
  have h1 := (B 1 j).isLt
  have h2 := (B 2 j).isLt
  unfold columnTotal
  omega

theorem residue_carry_reconstruct (B : Bands) (j : Fin 6) :
    q B j + 3 * carry B j = columnTotal B j := by
  exact Nat.mod_add_div (columnTotal B j) 3

theorem q_lt_three (B : Bands) (j : Fin 6) : q B j < 3 :=
  Nat.mod_lt _ (by decide)

theorem a_lt_three (B : Bands) (j : Fin 6) : a B j < 3 :=
  Nat.mod_lt _ (by decide)

theorem carry_le_two (B : Bands) (j : Fin 6) : carry B j ≤ 2 := by
  have ht := columnTotal_le_six B j
  unfold carry
  omega

/-- This is Python's signed `(p + e - f) % 3`, not truncated subtraction. -/
theorem a_is_signed_residue (B : Bands) (j : Fin 6) :
    (a B j : ℤ) =
      ((B 0 j).val + (B 1 j).val - (B 2 j).val : ℤ) % 3 := by
  have h0 := (B 0 j).isLt
  have h1 := (B 1 j).isLt
  have h2 := (B 2 j).isLt
  unfold a
  omega

theorem nonzeroIndicator_le_one (x : Fin 3) : nonzeroIndicator x ≤ 1 := by
  unfold nonzeroIndicator
  split <;> omega

theorem columnWeight_le_three (B : Bands) (j : Fin 6) : columnWeight B j ≤ 3 := by
  have h0 := nonzeroIndicator_le_one (B 0 j)
  have h1 := nonzeroIndicator_le_one (B 1 j)
  have h2 := nonzeroIndicator_le_one (B 2 j)
  unfold columnWeight
  omega

theorem columnWeightMod_lt_three (B : Bands) (j : Fin 6) :
    columnWeightMod B j < 3 := Nat.mod_lt _ (by decide)

theorem visibleCharge_lt_three (B : Bands) (i : Fin 3) :
    visibleCharge B i < 3 := Nat.mod_lt _ (by decide)

theorem wittResidue_lt_three (B : Bands) (i : Fin 3) (j : Fin 6) :
    wittResidue B i j < 3 := Nat.mod_lt _ (by decide)

theorem wittDualCharge_lt_three (B : Bands) (i : Fin 3) :
    wittDualCharge B i < 3 := Nat.mod_lt _ (by decide)

theorem wittDualCharge_residue_sum (B : Bands) (i : Fin 3) :
    wittDualCharge B i = (∑ j : Fin 6, wittResidue B i j) % 3 := by
  exact Finset.sum_nat_mod Finset.univ 3 (wittImage B i)

theorem signature_reconstructs_columns (B : Bands) (j : Fin 6) :
    (readSignature B).q j + 3 * (readSignature B).c j = columnTotal B j :=
  residue_carry_reconstruct B j

/-- One transition emits one additional six-trit band, with t starting at 0. -/
def ternaryDepth (t : ℕ) : ℕ := 6 * (t + 1)

/-- Exact floor(log_1000(3^(6(t+1)))); this is not the transition index. -/
def publicationClock (t : ℕ) : ℕ := Nat.log 1000 (3 ^ ternaryDepth t)

theorem publicationClock_lower (t : ℕ) :
    1000 ^ publicationClock t ≤ 3 ^ ternaryDepth t := by
  exact Nat.pow_log_le_self 1000 (pow_ne_zero _ (by decide))

theorem publicationClock_upper (t : ℕ) :
    3 ^ ternaryDepth t < 1000 ^ (publicationClock t + 1) := by
  exact Nat.lt_pow_succ_log_self (by decide) _

theorem publicationClock_unique (t k : ℕ)
    (lo : 1000 ^ k ≤ 3 ^ ternaryDepth t)
    (hi : 3 ^ ternaryDepth t < 1000 ^ (k + 1)) :
    publicationClock t = k := Nat.log_eq_of_pow_le_of_lt_pow lo hi

theorem publicationClock_monotone : Monotone publicationClock := by
  intro s t hst
  apply Nat.log_mono_right
  apply Nat.pow_le_pow_right (by decide : 0 < 3)
  unfold ternaryDepth
  omega

theorem publicationClock_twenty : publicationClock 20 = 20 := by
  apply publicationClock_unique <;> norm_num [ternaryDepth]

theorem publicationClock_twenty_one : publicationClock 21 = 20 := by
  apply publicationClock_unique <;> norm_num [ternaryDepth]

/-- Consecutive transition indices can publish the same decimal depth. -/
theorem distinct_times_same_clock :
    (20 : ℕ) ≠ 21 ∧ publicationClock 20 = publicationClock 21 := by
  constructor
  · decide
  · rw [publicationClock_twenty, publicationClock_twenty_one]

def signatureHistory (B : ℕ → Bands) (t : ℕ) : Signature := readSignature (B t)

theorem history_column_reconstruction (B : ℕ → Bands) (t : ℕ) (j : Fin 6) :
    (signatureHistory B t).q j + 3 * (signatureHistory B t).c j =
      columnTotal (B t) j := residue_carry_reconstruct (B t) j

end HMT.N69RegionalSignature

#print axioms HMT.N69RegionalSignature.columnTotal_le_six
#print axioms HMT.N69RegionalSignature.residue_carry_reconstruct
#print axioms HMT.N69RegionalSignature.q_lt_three
#print axioms HMT.N69RegionalSignature.a_lt_three
#print axioms HMT.N69RegionalSignature.carry_le_two
#print axioms HMT.N69RegionalSignature.a_is_signed_residue
#print axioms HMT.N69RegionalSignature.nonzeroIndicator_le_one
#print axioms HMT.N69RegionalSignature.columnWeight_le_three
#print axioms HMT.N69RegionalSignature.columnWeightMod_lt_three
#print axioms HMT.N69RegionalSignature.visibleCharge_lt_three
#print axioms HMT.N69RegionalSignature.wittResidue_lt_three
#print axioms HMT.N69RegionalSignature.wittDualCharge_lt_three
#print axioms HMT.N69RegionalSignature.wittDualCharge_residue_sum
#print axioms HMT.N69RegionalSignature.signature_reconstructs_columns
#print axioms HMT.N69RegionalSignature.publicationClock_lower
#print axioms HMT.N69RegionalSignature.publicationClock_upper
#print axioms HMT.N69RegionalSignature.publicationClock_unique
#print axioms HMT.N69RegionalSignature.publicationClock_monotone
#print axioms HMT.N69RegionalSignature.publicationClock_twenty
#print axioms HMT.N69RegionalSignature.publicationClock_twenty_one
#print axioms HMT.N69RegionalSignature.distinct_times_same_clock
#print axioms HMT.N69RegionalSignature.history_column_reconstruction
