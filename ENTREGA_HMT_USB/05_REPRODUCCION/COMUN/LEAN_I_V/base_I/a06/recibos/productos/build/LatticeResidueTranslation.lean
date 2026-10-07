import LatticeResidueProducts
import LatticeNormalTranslation
import LatticeTranslationLinear

/-! Translation covariance of all integral residue products. The two
expansion regions are treated separately by finite telescoping on each
input vector; the scalar recurrence is that of the existing kernels. -/

noncomputable section
set_option maxHeartbeats 1200000
namespace HMT.IV.LatticeResidueTranslation

open LatticeResidueProducts LatticeNormalOrderedField LatticeNormalTranslation
open LatticeTranslationLinear LatticeTwoRegionFactor LatticeExponentialContraction
open LatticeFiniteDoubleSums

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem left_kernel_value (p : ℤ) (a : ℕ) :
    leftExpansion p (p-a) a = scalarContraction p a := by
  simp [leftExpansion]

theorem right_kernel_value (p : ℤ) (a : ℕ) :
    rightExpansion p a (p-a) = (-1 : ℂ)^p * scalarContraction p a := by
  rw [rightExpansion, left_kernel_value]

theorem left_kernel_step (p : ℤ) (a : ℕ) :
    ((a : ℂ)-(p : ℂ)) * leftExpansion p (p-a) a =
      (a+1 : ℂ) * leftExpansion p (p-(a+1 : ℕ)) (a+1 : ℕ) := by
  simp only [left_kernel_value]
  exact (scalarContraction_step p a).symm

theorem right_kernel_step (p : ℤ) (a : ℕ) :
    ((a : ℂ)-(p : ℂ)) * rightExpansion p a (p-a) =
      (a+1 : ℂ) * rightExpansion p (a+1 : ℕ) (p-(a+1 : ℕ)) := by
  simp only [right_kernel_value]
  linear_combination (-1 : ℂ)^p * (scalarContraction_step p a).symm

theorem leftTerm_translation (T : Module.End ℂ V) (p : ℤ)
    (A B : VertexOperator ℂ V) (hA : TranslationCovariant T A)
    (hB : TranslationCovariant T B) (k : ℤ) (a : ℕ) :
    T * leftTerm p A B k a - leftTerm p A B k a * T =
      ((k : ℂ)+1) • leftTerm p A B (k+1) a +
        ((a+1 : ℂ) • leftTerm p A B (k+1) (a+1) -
          (a : ℂ) • leftTerm p A B (k+1) a) := by
  change T * (leftExpansion p (p-a) a •
      (HVertexOperator.coeff A (a-p-1) * HVertexOperator.coeff B (k-a))) -
    (leftExpansion p (p-a) a •
      (HVertexOperator.coeff A (a-p-1) * HVertexOperator.coeff B (k-a))) * T = _
  rw [commutator_smul, commutator_mul, hA, hB]
  simp only [leftTerm, smul_add, smul_mul_assoc, mul_smul_comm, smul_smul]
  rw [show (a : ℤ)-p-1+1 = a-p by omega,
    show k-(a : ℤ)+1 = k+1-a by omega,
    show ((a+1 : ℕ) : ℤ)-p-1 = a-p by omega,
    show k+1-((a+1 : ℕ) : ℤ) = k-a by omega]
  have hs := left_kernel_step p a
  push_cast at hs ⊢
  match_scalars
  all_goals first | (solve | ring) | linear_combination hs

theorem rightTerm_translation_zero (T : Module.End ℂ V) (p : ℤ)
    (A B : VertexOperator ℂ V) (hA : TranslationCovariant T A)
    (hB : TranslationCovariant T B) (k : ℤ) :
    T * rightTerm p A B k 0 - rightTerm p A B k 0 * T =
      ((k : ℂ)+1) • rightTerm p A B (k+1) 0 +
        (-(p : ℂ)) • rightTerm p A B (k+1) 0 := by
  change T * (rightExpansion p 0 (p-0) •
      (HVertexOperator.coeff B (k-p+0) * HVertexOperator.coeff A (-0-1))) -
    (rightExpansion p 0 (p-0) •
      (HVertexOperator.coeff B (k-p+0) * HVertexOperator.coeff A (-0-1))) * T = _
  rw [commutator_smul, commutator_mul, hB, hA]
  simp only [rightTerm, Nat.cast_zero, sub_zero, neg_zero, zero_sub, add_zero,
    Int.cast_neg, Int.cast_one, neg_add_cancel, zero_smul, mul_zero,
    smul_mul_assoc, smul_smul]
  rw [show k-p+1 = k+1-p by omega]
  push_cast
  module

theorem rightTerm_translation_succ (T : Module.End ℂ V) (p : ℤ)
    (A B : VertexOperator ℂ V) (hA : TranslationCovariant T A)
    (hB : TranslationCovariant T B) (k : ℤ) (a : ℕ) :
    T * rightTerm p A B k (a+1) - rightTerm p A B k (a+1) * T =
      ((k : ℂ)+1) • rightTerm p A B (k+1) (a+1) +
        ((a+1-(p : ℂ)) • rightTerm p A B (k+1) (a+1) -
          ((a : ℂ)-p) • rightTerm p A B (k+1) a) := by
  change T * (rightExpansion p (a+1 : ℕ) (p-(a+1 : ℕ)) •
      (HVertexOperator.coeff B (k-p+(a+1 : ℕ)) *
        HVertexOperator.coeff A (-(a+1 : ℕ)-1))) -
    (rightExpansion p (a+1 : ℕ) (p-(a+1 : ℕ)) •
      (HVertexOperator.coeff B (k-p+(a+1 : ℕ)) *
        HVertexOperator.coeff A (-(a+1 : ℕ)-1))) * T = _
  rw [commutator_smul, commutator_mul, hB, hA]
  simp only [rightTerm, smul_add, smul_mul_assoc, mul_smul_comm, smul_smul]
  rw [show k-p+((a+1 : ℕ) : ℤ)+1 = k+1-p+(a+1 : ℕ) by omega,
    show -((a+1 : ℕ) : ℤ)-1+1 = -(a : ℤ)-1 by omega,
    show k-p+((a+1 : ℕ) : ℤ) = k+1-p+a by omega]
  have hs := right_kernel_step p a
  push_cast at hs ⊢
  match_scalars
  all_goals first | (solve | ring) | linear_combination hs

theorem left_sum_translation (T : Module.End ℂ V) (p : ℤ)
    (A B : VertexOperator ℂ V) (hA : TranslationCovariant T A)
    (hB : TranslationCovariant T B) (k : ℤ) (v : V) :
    T (∑ᶠ a, leftTerm p A B k a v) - (∑ᶠ a, leftTerm p A B k a (T v)) =
      ((k : ℂ)+1) • (∑ᶠ a, leftTerm p A B (k+1) a v) := by
  let F : ℕ → V := fun a => (a : ℂ) • leftTerm p A B (k+1) a v
  have hf : (Function.support F).Finite := by
    apply (leftTerm_finite p A B (k+1) v).subset
    intro a ha hz
    exact ha (by simp [F, hz])
  apply locallyFiniteSum_commutator_of_telescoping T
    (leftTerm p A B k) (leftTerm p A B (k+1))
    (leftTerm_finite p A B k) (leftTerm_finite p A B (k+1))
    ((k : ℂ)+1) v F hf (by simp [F])
  intro a
  have h := LinearMap.congr_fun (leftTerm_translation T p A B hA hB k a) v
  simpa [F, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    LinearMap.add_apply] using h

theorem right_sum_translation (T : Module.End ℂ V) (p : ℤ)
    (A B : VertexOperator ℂ V) (hA : TranslationCovariant T A)
    (hB : TranslationCovariant T B) (k : ℤ) (v : V) :
    T (∑ᶠ a, rightTerm p A B k a v) - (∑ᶠ a, rightTerm p A B k a (T v)) =
      ((k : ℂ)+1) • (∑ᶠ a, rightTerm p A B (k+1) a v) := by
  classical
  let F : ℕ → V
    | 0 => 0
    | a+1 => ((a : ℂ)-p) • rightTerm p A B (k+1) a v
  have hf : (Function.support F).Finite := by
    let hs := rightTerm_finite p A B (k+1) v
    apply (hs.image Nat.succ).subset
    intro a ha
    cases a with
    | zero => exact False.elim (ha rfl)
    | succ a =>
      refine ⟨a, ?_, rfl⟩
      intro hz
      exact ha (by simp [F, hz])
  apply locallyFiniteSum_commutator_of_telescoping T
    (rightTerm p A B k) (rightTerm p A B (k+1))
    (rightTerm_finite p A B k) (rightTerm_finite p A B (k+1))
    ((k : ℂ)+1) v F hf rfl
  intro a
  cases a with
  | zero =>
    have h := LinearMap.congr_fun (rightTerm_translation_zero T p A B hA hB k) v
    simpa [F, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
      LinearMap.add_apply] using h
  | succ a =>
    have h := LinearMap.congr_fun (rightTerm_translation_succ T p A B hA hB k a) v
    simpa [F, LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
      LinearMap.add_apply, Nat.cast_add, Nat.cast_one] using h

theorem residueField_translation (T : Module.End ℂ V) (p : ℤ)
    (A B : VertexOperator ℂ V) (hA : TranslationCovariant T A)
    (hB : TranslationCovariant T B) : TranslationCovariant T (residueField p A B) := by
  intro k
  apply LinearMap.ext
  intro v
  simp only [residueField_coefficient, Module.End.mul_apply, LinearMap.sub_apply,
    LinearMap.smul_apply, residueCoefficient_apply, map_sub]
  have hl := left_sum_translation T p A B hA hB k v
  have hr := right_sum_translation T p A B hA hB k v
  rw [smul_sub, ← hl, ← hr]
  abel

end HMT.IV.LatticeResidueTranslation
end

#print axioms HMT.IV.LatticeResidueTranslation.left_kernel_value
#print axioms HMT.IV.LatticeResidueTranslation.right_kernel_value
#print axioms HMT.IV.LatticeResidueTranslation.left_kernel_step
#print axioms HMT.IV.LatticeResidueTranslation.right_kernel_step
#print axioms HMT.IV.LatticeResidueTranslation.leftTerm_translation
#print axioms HMT.IV.LatticeResidueTranslation.rightTerm_translation_zero
#print axioms HMT.IV.LatticeResidueTranslation.rightTerm_translation_succ
#print axioms HMT.IV.LatticeResidueTranslation.left_sum_translation
#print axioms HMT.IV.LatticeResidueTranslation.right_sum_translation
#print axioms HMT.IV.LatticeResidueTranslation.residueField_translation
