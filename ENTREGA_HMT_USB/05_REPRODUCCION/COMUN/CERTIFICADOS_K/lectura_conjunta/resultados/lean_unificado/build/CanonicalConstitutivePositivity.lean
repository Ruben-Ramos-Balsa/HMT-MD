import AngularConstitutiveClosure
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Data.Real.StarOrdered

/-!
Positive definiteness of the canonical two-sheet constitutive realization.
The projectors are evaluated from the fixed sheet involution; the diagonal
entries are the responses of the channels produced by the angular chamber.
Positive definiteness is a conclusion, not an extra structure field or premise.
This scoped downstream result is not a formalization of all of Article III.
-/
noncomputable section
namespace HMT.III.Constitutive

theorem canonical_sheetPlus_diagonal :
    sheetPlus canonicalSheetInvolution =
      Matrix.diagonal ![(1 : ℝ), 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [sheetPlus, canonicalSheetInvolution, Matrix.one_apply]

theorem canonical_sheetMinus_diagonal :
    sheetMinus canonicalSheetInvolution =
      Matrix.diagonal ![(0 : ℝ), 1] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [sheetMinus, canonicalSheetInvolution, Matrix.one_apply]

namespace AngularChamber

def canonicalConstitutiveOperator (a : AngularChamber) :
    Matrix (Fin 2) (Fin 2) ℝ :=
  a.constitutiveOperator canonicalSheetInvolution canonicalSheetInvolution_square

theorem canonical_operator_diagonal (a : AngularChamber) :
    a.canonicalConstitutiveOperator =
      Matrix.diagonal ![a.channels.vacuum.rPlus, a.channels.vacuum.rMinus] := by
  rw [canonicalConstitutiveOperator, a.operator_from_angles,
    canonical_sheetPlus_diagonal, canonical_sheetMinus_diagonal]
  change a.channels.vacuum.rPlus • Matrix.diagonal ![(1 : ℝ), 0] +
      a.channels.vacuum.rMinus • Matrix.diagonal ![(0 : ℝ), 1] = _
  ext i j
  fin_cases i <;> fin_cases j <;> simp

theorem canonical_operator_posDef (a : AngularChamber) :
    a.canonicalConstitutiveOperator.PosDef := by
  rw [a.canonical_operator_diagonal]
  apply Matrix.PosDef.diagonal
  intro i
  fin_cases i
  · exact a.channels.vacuum.plus_pos
  · exact a.channels.vacuum.minus_pos

theorem canonical_operator_completion (a : AngularChamber) :
    a.canonicalConstitutiveOperator * TwoSheetProjectors.sigma4
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30) =
      TwoSheetProjectors.sigma3
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30) :=
  (projectorsOfInvolution canonicalSheetInvolution canonicalSheetInvolution_square).completion_equation
    a.channels.plus_mem a.channels.minus_mem

/-- The ambient completion equation determines one matrix, and that matrix is
positive definite. The uniqueness premise does not restrict candidate matrices
to diagonal, positive or sheet-preserving matrices. -/
theorem canonical_unique_completion_is_posDef (a : AngularChamber) :
    (∃! W : Matrix (Fin 2) (Fin 2) ℝ,
      W * TwoSheetProjectors.sigma4
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30) =
      TwoSheetProjectors.sigma3
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30)) ∧
    a.canonicalConstitutiveOperator.PosDef :=
  ⟨a.completion_from_angles canonicalSheetInvolution canonicalSheetInvolution_square,
   a.canonical_operator_posDef⟩

/-- Existence and uniqueness may also be stated with positive definiteness in
the resulting predicate; it is proved for the explicit canonical operator. -/
theorem canonical_positive_completion_exists_unique (a : AngularChamber) :
    ∃! W : Matrix (Fin 2) (Fin 2) ℝ,
      (W * TwoSheetProjectors.sigma4
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30) =
      TwoSheetProjectors.sigma3
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30)) ∧
      W.PosDef := by
  refine ⟨a.canonicalConstitutiveOperator,
    ⟨a.canonical_operator_completion, a.canonical_operator_posDef⟩, ?_⟩
  intro W hW
  exact (projectorsOfInvolution canonicalSheetInvolution canonicalSheetInvolution_square).completion_unique
    a.channels.plus_mem a.channels.minus_mem hW.1

end AngularChamber

#print axioms canonical_sheetPlus_diagonal
#print axioms canonical_sheetMinus_diagonal
#print axioms AngularChamber.canonical_operator_diagonal
#print axioms AngularChamber.canonical_operator_posDef
#print axioms AngularChamber.canonical_operator_completion
#print axioms AngularChamber.canonical_unique_completion_is_posDef
#print axioms AngularChamber.canonical_positive_completion_exists_unique

end HMT.III.Constitutive
