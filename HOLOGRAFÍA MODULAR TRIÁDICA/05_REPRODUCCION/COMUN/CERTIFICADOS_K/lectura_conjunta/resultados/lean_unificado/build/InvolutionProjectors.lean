import TwoSheetOperator
import Mathlib.Tactic.Module

/-! The two constitutive projectors are constructed from the declared sheet
involution. Their algebraic laws are conclusions, not fields supplied again.
This is a downstream real-algebra realization, not a claim that a scalar
response reconstructs the full enriched TPK history. -/
noncomputable section
namespace HMT.III.Constitutive
variable {A : Type*} [Ring A] [Algebra ℝ A]

def sheetPlus (R : A) : A := (1 / 2 : ℝ) • (1 + R)
def sheetMinus (R : A) : A := (1 / 2 : ℝ) • (1 - R)

theorem sheetPlus_idempotent (R : A) (hR : R * R = 1) :
    sheetPlus R * sheetPlus R = sheetPlus R := by
  simp only [sheetPlus, Algebra.smul_mul_assoc, Algebra.mul_smul_comm,
    smul_smul, add_mul, mul_add, one_mul, mul_one, hR]
  module

theorem sheetMinus_idempotent (R : A) (hR : R * R = 1) :
    sheetMinus R * sheetMinus R = sheetMinus R := by
  simp only [sheetMinus, Algebra.smul_mul_assoc, Algebra.mul_smul_comm,
    smul_smul, sub_mul, mul_sub, one_mul, mul_one, hR]
  module

theorem sheetPlus_sheetMinus (R : A) (hR : R * R = 1) :
    sheetPlus R * sheetMinus R = 0 := by
  simp only [sheetPlus, sheetMinus, Algebra.smul_mul_assoc, Algebra.mul_smul_comm,
    smul_smul, add_mul, mul_sub, one_mul, mul_one, hR]
  module

theorem sheetMinus_sheetPlus (R : A) (hR : R * R = 1) :
    sheetMinus R * sheetPlus R = 0 := by
  simp only [sheetPlus, sheetMinus, Algebra.smul_mul_assoc, Algebra.mul_smul_comm,
    smul_smul, sub_mul, mul_add, one_mul, mul_one, hR]
  module

theorem sheet_complete (R : A) : sheetPlus R + sheetMinus R = 1 := by
  unfold sheetPlus sheetMinus
  module

def projectorsOfInvolution (R : A) (hR : R * R = 1) : TwoSheetProjectors A where
  plus := sheetPlus R
  minus := sheetMinus R
  plus_idempotent := sheetPlus_idempotent R hR
  minus_idempotent := sheetMinus_idempotent R hR
  plus_minus := sheetPlus_sheetMinus R hR
  minus_plus := sheetMinus_sheetPlus R hR
  complete := sheet_complete R

theorem sheet_difference (R : A) : sheetPlus R - sheetMinus R = R := by
  unfold sheetPlus sheetMinus
  module

theorem sheet_conjugate_plus (R : A) : sheetPlus (-R) = sheetMinus R := by
  simp only [sheetPlus, sheetMinus, sub_eq_add_neg]

theorem sheet_conjugate_minus (R : A) : sheetMinus (-R) = sheetPlus R := by
  simp only [sheetPlus, sheetMinus, sub_neg_eq_add]

theorem involution_transport (R : A) (hR : R * R = 1) (u v : ℝ) :
    (projectorsOfInvolution R hR).transport u v =
      ((u + v) / 2) • (1 : A) + ((u - v) / 2) • R := by
  unfold TwoSheetProjectors.transport TwoSheetProjectors.diagonal
    projectorsOfInvolution sheetPlus sheetMinus
  module

theorem involution_response_unique (R : A) (hR : R * R = 1)
    (Q : OrientedChannels) :
    ∃! W : A, W * TwoSheetProjectors.sigma4
      ((projectorsOfInvolution R hR).transport Q.qPlus Q.qMinus ^ 30) =
      TwoSheetProjectors.sigma3
        ((projectorsOfInvolution R hR).transport Q.qPlus Q.qMinus ^ 30) :=
  (projectorsOfInvolution R hR).completion_exists_unique Q.plus_mem Q.minus_mem

#print axioms sheetPlus_idempotent
#print axioms sheetMinus_idempotent
#print axioms sheetPlus_sheetMinus
#print axioms sheetMinus_sheetPlus
#print axioms sheet_complete
#print axioms sheet_difference
#print axioms sheet_conjugate_plus
#print axioms sheet_conjugate_minus
#print axioms involution_transport
#print axioms involution_response_unique
end HMT.III.Constitutive
