/-
  APP arithmetic at the explicit causal cut before TRIT and TPK.
  Source: active package I, manuscript_es/sections/nucleo.tex,
  eq:residuo-cociente, eq:app-levantada, carry-cocycle lemma,
  and eq:defecto-integrado. The source file was read in full.

  One support: Digit x Digit, with Digit = Fin 9 indexing positive marks 1..9.
  Both evaluations retain residue AND quotient. Totals are outputs of folds
  over that support; no expected total is an input to any evaluation.
  General reconstruction is proved for all positive naturals, not by a finite
  census. Finite census and finite cocycle proofs use kernel-checked decide.
  This file does not claim to formalize the whole APP-TRIT-TPK construction.
-/
import Std

namespace APPArithmetic

abbrev Digit := Fin 9

def value (i : Digit) : Nat := i.val + 1

-- Theorems about reconstruction have an explicit positive-input hypothesis.
-- Nat's totalization at zero is not asserted to represent the source domain.
def rho9 (n : Nat) : Nat := 1 + (n - 1) % 9
def q9 (n : Nat) : Nat := (n - 1) / 9

theorem value_positive (i : Digit) : 0 < value i := Nat.zero_lt_succ i.val

theorem value_upper (i : Digit) : value i ≤ 9 := i.isLt

theorem rho9_range (n : Nat) : 1 ≤ rho9 n ∧ rho9 n ≤ 9 := by
  have h := Nat.mod_lt (n - 1) (by decide : 0 < 9)
  constructor
  · exact Nat.le_add_right 1 ((n - 1) % 9)
  · change 1 + (n - 1) % 9 ≤ 9
    calc
      1 + (n - 1) % 9 = (n - 1) % 9 + 1 := Nat.add_comm _ _
      _ ≤ 9 := h

theorem reconstruct (n : Nat) (hn : 0 < n) : n = rho9 n + 9 * q9 n := by
  calc
    n = n - 1 + 1 := (Nat.sub_add_cancel hn).symm
    _ = ((n - 1) % 9 + 9 * ((n - 1) / 9)) + 1 :=
      congrArg (fun x => x + 1) (Nat.mod_add_div (n - 1) 9).symm
    _ = 1 + ((n - 1) % 9 + 9 * ((n - 1) / 9)) := Nat.add_comm _ _
    _ = (1 + (n - 1) % 9) + 9 * ((n - 1) / 9) :=
      (Nat.add_assoc _ _ _).symm
    _ = rho9 n + 9 * q9 n := rfl

-- Reconciles the executable quotient with the manuscript's (n-rho9(n))/9.
theorem quotient_source_formula (n : Nat) (hn : 0 < n) :
    q9 n = (n - rho9 n) / 9 := by
  calc
    q9 n = (9 * q9 n) / 9 := (Nat.mul_div_cancel_left _ (by decide : 0 < 9)).symm
    _ = ((rho9 n + 9 * q9 n) - rho9 n) / 9 :=
      congrArg (fun x => x / 9) (Nat.add_sub_cancel_left _ _).symm
    _ = (n - rho9 n) / 9 :=
      congrArg (fun x => (x - rho9 n) / 9) (reconstruct n hn).symm

theorem rho9_mod (n : Nat) (hn : 0 < n) : rho9 n % 9 = n % 9 := by
  calc
    rho9 n % 9 = (rho9 n + 9 * q9 n) % 9 :=
      (Nat.add_mul_mod_self_left (rho9 n) 9 (q9 n)).symm
    _ = n % 9 := congrArg (fun x => x % 9) (reconstruct n hn).symm

theorem rho9_value (i : Digit) : rho9 (value i) = value i := by
  change 1 + ((i.val + 1 - 1) % 9) = i.val + 1
  calc
    1 + ((i.val + 1 - 1) % 9) = 1 + (i.val % 9) := rfl
    _ = 1 + i.val := congrArg (fun x => 1 + x) (Nat.mod_eq_of_lt i.isLt)
    _ = i.val + 1 := Nat.add_comm _ _

theorem q9_value (i : Digit) : q9 (value i) = 0 :=
  Nat.div_eq_of_lt i.isLt

structure Lifted where
  residue : Nat
  quotient : Nat
  deriving Repr, DecidableEq

def lift (n : Nat) : Lifted := ⟨rho9 n, q9 n⟩
def decode (x : Lifted) : Nat := x.residue + 9 * x.quotient

theorem decode_lift (n : Nat) (hn : 0 < n) : decode (lift n) = n :=
  (reconstruct n hn).symm

theorem lift_injective_positive (m n : Nat) (hm : 0 < m) (hn : 0 < n)
    (h : lift m = lift n) : m = n := by
  calc
    m = decode (lift m) := (decode_lift m hm).symm
    _ = decode (lift n) := congrArg decode h
    _ = n := decode_lift n hn

def sumEval (i j : Digit) : Nat := value i + value j
def productEval (i j : Digit) : Nat := value i * value j
def sumResidue (i j : Digit) : Nat := rho9 (sumEval i j)
def productResidue (i j : Digit) : Nat := rho9 (productEval i j)
def sumQuotient (i j : Digit) : Nat := q9 (sumEval i j)
def productQuotient (i j : Digit) : Nat := q9 (productEval i j)

structure PairedEvaluation where
  additive : Lifted
  multiplicative : Lifted
  deriving Repr, DecidableEq

def evaluate (i j : Digit) : PairedEvaluation :=
  ⟨lift (sumEval i j), lift (productEval i j)⟩

theorem sum_positive (i j : Digit) : 0 < sumEval i j :=
  Nat.lt_of_lt_of_le (value_positive i) (Nat.le_add_right _ _)

theorem product_positive (i j : Digit) : 0 < productEval i j :=
  Nat.mul_pos (value_positive i) (value_positive j)

theorem reconstruct_sum (i j : Digit) :
    sumEval i j = sumResidue i j + 9 * sumQuotient i j :=
  reconstruct (sumEval i j) (sum_positive i j)

theorem reconstruct_product (i j : Digit) :
    productEval i j = productResidue i j + 9 * productQuotient i j :=
  reconstruct (productEval i j) (product_positive i j)

theorem paired_reconstruction (i j : Digit) :
    decode (evaluate i j).additive = sumEval i j ∧
    decode (evaluate i j).multiplicative = productEval i j :=
  ⟨decode_lift (sumEval i j) (sum_positive i j),
    decode_lift (productEval i j) (product_positive i j)⟩

theorem sum_symmetry (i j : Digit) : sumEval i j = sumEval j i :=
  Nat.add_comm _ _

theorem product_symmetry (i j : Digit) : productEval i j = productEval j i :=
  Nat.mul_comm _ _

theorem paired_symmetry (i j : Digit) : evaluate i j = evaluate j i := by
  calc
    evaluate i j = ⟨lift (sumEval j i), lift (productEval i j)⟩ :=
      congrArg (fun x => PairedEvaluation.mk x (lift (productEval i j)))
        (congrArg lift (sum_symmetry i j))
    _ = evaluate j i :=
      congrArg (fun x => PairedEvaluation.mk (lift (sumEval j i)) x)
        (congrArg lift (product_symmetry i j))

-- Positive section of the cyclic class: value 9 represents its identity.
-- This shifted addition is deliberately distinct from Fin's default addition.
def addPositive (a b : Digit) : Digit :=
  ⟨(value a + value b - 1) % 9, Nat.mod_lt _ (by decide)⟩

def zeroClass : Digit := ⟨8, by decide⟩

def carry (a b : Digit) : Nat := q9 (value a + value b)

theorem section_add (a b : Digit) :
    value (addPositive a b) = rho9 (value a + value b) := Nat.add_comm _ _

theorem carry_reconstruction (a b : Digit) :
    value a + value b = value (addPositive a b) + 9 * carry a b := by
  exact (reconstruct (value a + value b) (sum_positive a b)).trans
    (congrArg (fun x => x + 9 * carry a b) (section_add a b).symm)

theorem carry_source_formula (a b : Digit) :
    carry a b = (value a + value b - value (addPositive a b)) / 9 := by
  exact (quotient_source_formula (value a + value b) (sum_positive a b)).trans
    (congrArg (fun x => (value a + value b - x) / 9) (section_add a b).symm)

theorem section_add_mod (a b : Digit) :
    value (addPositive a b) % 9 = (value a + value b) % 9 :=
  (congrArg (fun x => x % 9) (section_add a b)).trans
    (rho9_mod (value a + value b) (sum_positive a b))

set_option maxRecDepth 20000 in
theorem addPositive_associative :
    ∀ a b c : Digit, addPositive (addPositive a b) c = addPositive a (addPositive b c) := by
  decide

theorem addPositive_identity :
    ∀ a : Digit, addPositive zeroClass a = a ∧ addPositive a zeroClass = a := by
  decide

set_option maxRecDepth 20000 in
theorem carry_cocycle : ∀ a b c : Digit,
    carry a b + carry (addPositive a b) c =
      carry b c + carry a (addPositive b c) := by
  decide

-- The positive section is intentionally not normalized at the identity.
theorem carry_identity : ∀ a : Digit, carry zeroClass a = 1 := by decide

def sumOverDigits (f : Digit → Nat) : Nat :=
  ((List.finRange 9).map f).foldl Nat.add 0

def totalOverSupport (f : Digit → Digit → Nat) : Nat :=
  sumOverDigits (fun i => sumOverDigits (fun j => f i j))

theorem census_sum : totalOverSupport sumEval = 810 := by decide
theorem census_product : totalOverSupport productEval = 2025 := by decide
theorem census_sum_residue : totalOverSupport sumResidue = 405 := by decide
theorem census_product_residue : totalOverSupport productResidue = 459 := by decide
theorem census_sum_quotient : totalOverSupport sumQuotient = 45 := by decide
theorem census_product_quotient : totalOverSupport productQuotient = 174 := by decide

theorem integrated_defect :
    totalOverSupport productEval - totalOverSupport sumEval =
      (totalOverSupport productResidue - totalOverSupport sumResidue) +
        9 * (totalOverSupport productQuotient - totalOverSupport sumQuotient) := by
  decide

theorem integrated_defect_value :
    totalOverSupport productEval - totalOverSupport sumEval = 54 + 9 * 129 := by
  decide

theorem residue_does_not_determine_quotient :
    rho9 10 = rho9 19 ∧ q9 10 ≠ q9 19 := by decide

-- Source witnesses (5,5) and (8,2), encoded by zero-based indices (4,4),(7,1).
theorem paired_residual_collision :
    sumEval ⟨4, by decide⟩ ⟨4, by decide⟩ = sumEval ⟨7, by decide⟩ ⟨1, by decide⟩ ∧
    productResidue ⟨4, by decide⟩ ⟨4, by decide⟩ =
      productResidue ⟨7, by decide⟩ ⟨1, by decide⟩ ∧
    evaluate ⟨4, by decide⟩ ⟨4, by decide⟩ ≠ evaluate ⟨7, by decide⟩ ⟨1, by decide⟩ := by
  decide

end APPArithmetic

#print axioms APPArithmetic.value_positive
#print axioms APPArithmetic.value_upper
#print axioms APPArithmetic.rho9_range
#print axioms APPArithmetic.reconstruct
#print axioms APPArithmetic.quotient_source_formula
#print axioms APPArithmetic.rho9_mod
#print axioms APPArithmetic.rho9_value
#print axioms APPArithmetic.q9_value
#print axioms APPArithmetic.decode_lift
#print axioms APPArithmetic.lift_injective_positive
#print axioms APPArithmetic.sum_positive
#print axioms APPArithmetic.product_positive
#print axioms APPArithmetic.reconstruct_sum
#print axioms APPArithmetic.reconstruct_product
#print axioms APPArithmetic.paired_reconstruction
#print axioms APPArithmetic.sum_symmetry
#print axioms APPArithmetic.product_symmetry
#print axioms APPArithmetic.paired_symmetry
#print axioms APPArithmetic.section_add
#print axioms APPArithmetic.carry_reconstruction
#print axioms APPArithmetic.carry_source_formula
#print axioms APPArithmetic.section_add_mod
#print axioms APPArithmetic.addPositive_associative
#print axioms APPArithmetic.addPositive_identity
#print axioms APPArithmetic.carry_cocycle
#print axioms APPArithmetic.carry_identity
#print axioms APPArithmetic.census_sum
#print axioms APPArithmetic.census_product
#print axioms APPArithmetic.census_sum_residue
#print axioms APPArithmetic.census_product_residue
#print axioms APPArithmetic.census_sum_quotient
#print axioms APPArithmetic.census_product_quotient
#print axioms APPArithmetic.integrated_defect
#print axioms APPArithmetic.integrated_defect_value
#print axioms APPArithmetic.residue_does_not_determine_quotient
#print axioms APPArithmetic.paired_residual_collision
