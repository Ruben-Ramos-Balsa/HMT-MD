/-
  Joint APP sum/product fibres on the third realization {1,...,9}^3.
  The incidence matrix is defined by counting actual triples. Its printed
  table and marginals are consequences, not inputs to the operations.
  This is the APP arithmetic cut used by the electronic-prefactor argument;
  it does not by itself assert the operator-norm or full electronic result.
-/
import APPArithmetic
import Mathlib.Data.Matrix.Notation
import Mathlib.Data.Fintype.Prod
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace HMT.I.APPFiberCensus

abbrev Digit := APPArithmetic.Digit
abbrev Triple := Digit × Digit × Digit

def sumValue (x : Triple) : ℕ :=
  APPArithmetic.value x.1 + APPArithmetic.value x.2.1 + APPArithmetic.value x.2.2

def productValue (x : Triple) : ℕ :=
  APPArithmetic.value x.1 * APPArithmetic.value x.2.1 * APPArithmetic.value x.2.2

def sumDigit (x : Triple) : ℕ := APPArithmetic.rho9 (sumValue x)
def productDigit (x : Triple) : ℕ := APPArithmetic.rho9 (productValue x)

def jointFiber (a b : Digit) : Finset Triple :=
  Finset.univ.filter (fun x => sumDigit x = APPArithmetic.value a ∧
    productDigit x = APPArithmetic.value b)

def sumFiber (a : Digit) : Finset Triple :=
  Finset.univ.filter (fun x => sumDigit x = APPArithmetic.value a)

def productFiber (b : Digit) : Finset Triple :=
  Finset.univ.filter (fun x => productDigit x = APPArithmetic.value b)

def N : Matrix Digit Digit ℕ := fun a b => (jointFiber a b).card

def rowTotal (a : Digit) : ℕ := ∑ b, N a b
def columnTotal (b : Digit) : ℕ := ∑ a, N a b

def baseTable : Matrix Digit Digit ℕ := !![
  0,1,1,0,1,1,0,1,4;
  1,0,1,1,0,1,1,0,4;
  1,0,2,0,1,2,0,0,3;
  0,1,1,0,1,1,0,1,4;
  1,0,1,1,0,1,1,0,4;
  0,0,2,1,0,2,0,1,3;
  0,1,1,0,1,1,0,1,4;
  1,0,1,1,0,1,1,0,4;
  0,1,2,0,0,2,1,0,3]

theorem triple_cardinality : Fintype.card Triple = 729 := by decide

theorem jointFiber_membership (a b : Digit) (x : Triple) :
    x ∈ jointFiber a b ↔ sumDigit x = APPArithmetic.value a ∧
      productDigit x = APPArithmetic.value b := by
  simp [jointFiber]

theorem jointFiber_eq_inter (a b : Digit) :
    jointFiber a b = sumFiber a ∩ productFiber b := by
  ext x
  simp [jointFiber, sumFiber, productFiber]

theorem sumValue_positive (x : Triple) : 0 < sumValue x := by
  have := APPArithmetic.value_positive x.1
  simp only [sumValue]
  omega

theorem productValue_positive (x : Triple) : 0 < productValue x :=
  Nat.mul_pos (Nat.mul_pos (APPArithmetic.value_positive x.1)
    (APPArithmetic.value_positive x.2.1)) (APPArithmetic.value_positive x.2.2)

theorem sum_reconstruction (x : Triple) :
    sumValue x = sumDigit x + 9 * APPArithmetic.q9 (sumValue x) :=
  APPArithmetic.reconstruct _ (sumValue_positive x)

theorem product_reconstruction (x : Triple) :
    productValue x = productDigit x + 9 * APPArithmetic.q9 (productValue x) :=
  APPArithmetic.reconstruct _ (productValue_positive x)

theorem census_entry : ∀ a b : Digit, N a b = 9 * baseTable a b := by
  decide

theorem census_matrix : N = 9 • baseTable := by
  ext a b
  simpa only [Pi.smul_apply, smul_eq_mul] using census_entry a b

theorem row_total : ∀ a : Digit, rowTotal a = 81 := by
  intro a
  simp only [rowTotal, census_entry]
  revert a
  decide

theorem column_totals :
    columnTotal = ![36,36,108,36,36,108,36,36,297] := by
  funext b
  simp only [columnTotal, census_entry]
  revert b
  decide

theorem column_total_positive (b : Digit) : 0 < columnTotal b := by
  rw [column_totals]
  fin_cases b <;> decide

theorem sum_fiber_card : ∀ a : Digit, (sumFiber a).card = 81 := by decide

theorem product_fiber_cards :
    (fun b : Digit => (productFiber b).card) =
      ![36,36,108,36,36,108,36,36,297] := by
  funext b
  revert b
  decide

theorem rowTotal_eq_fiber_card (a : Digit) : rowTotal a = (sumFiber a).card := by
  rw [row_total, sum_fiber_card]

theorem columnTotal_eq_fiber_card (b : Digit) :
    columnTotal b = (productFiber b).card := by
  exact congrFun (column_totals.trans product_fiber_cards.symm) b

theorem census_total : (∑ a, ∑ b, N a b) = 729 := by
  change (∑ a, rowTotal a) = 729
  simp [row_total]

end HMT.I.APPFiberCensus

#print axioms HMT.I.APPFiberCensus.triple_cardinality
#print axioms HMT.I.APPFiberCensus.jointFiber_membership
#print axioms HMT.I.APPFiberCensus.jointFiber_eq_inter
#print axioms HMT.I.APPFiberCensus.sumValue_positive
#print axioms HMT.I.APPFiberCensus.productValue_positive
#print axioms HMT.I.APPFiberCensus.sum_reconstruction
#print axioms HMT.I.APPFiberCensus.product_reconstruction
#print axioms HMT.I.APPFiberCensus.census_entry
#print axioms HMT.I.APPFiberCensus.census_matrix
#print axioms HMT.I.APPFiberCensus.row_total
#print axioms HMT.I.APPFiberCensus.column_totals
#print axioms HMT.I.APPFiberCensus.column_total_positive
#print axioms HMT.I.APPFiberCensus.sum_fiber_card
#print axioms HMT.I.APPFiberCensus.product_fiber_cards
#print axioms HMT.I.APPFiberCensus.rowTotal_eq_fiber_card
#print axioms HMT.I.APPFiberCensus.columnTotal_eq_fiber_card
#print axioms HMT.I.APPFiberCensus.census_total
