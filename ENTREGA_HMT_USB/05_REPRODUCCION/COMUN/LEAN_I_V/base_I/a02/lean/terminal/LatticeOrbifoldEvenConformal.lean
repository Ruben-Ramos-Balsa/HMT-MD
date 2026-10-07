import LatticeOrbifoldEvenAction
import LatticePositiveDescendedConformal

/-! The diagonal action is compatible with the conformal modes already
constructed on the same direct sum.  The field coefficient identity is proved
from the two sector identities; the Virasoro relation is then consumed, not
rederived or assumed for a newly chosen family of operators. -/

noncomputable section
namespace HMT.IV.LatticeOrbifoldEvenConformal
open LatticeEvenVertexFields LatticeEvenTranslation LatticeEvenConformal
open LatticeTwistedPositiveSector LatticeOrbifoldCarrier
open LatticeOrbifoldEvenAction LatticePositiveDescendedConformal

theorem conformal_coefficient (o : Fin 12) (m : ℤ) :
    HVertexOperator.coeff (assignment o (evenConformalState o)) (-m-2) =
      modes o m := by
  apply LinearMap.ext
  intro v
  rw [assignment_coefficient, coefficient_apply, modes_apply,
    positiveDescended_conformalState_mode]
  rfl

def fieldMode (o : Fin 12) (m : ℤ) : Module.End ℂ (Space o) :=
  HVertexOperator.coeff (assignment o (evenConformalState o)) (-m-2)

theorem fieldMode_eq_modes (o : Fin 12) (m : ℤ) : fieldMode o m = modes o m :=
  conformal_coefficient o m

theorem fieldMode_virasoro (o : Fin 12) (m n : ℤ) :
    fieldMode o m * fieldMode o n - fieldMode o n * fieldMode o m =
      ((m-n:ℤ):ℂ) • fieldMode o (m+n) +
        (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
          (1 : Module.End ℂ (Space o)) else 0) := by
  simp only [fieldMode_eq_modes]
  exact virasoro_central_charge_twentyFour o m n

theorem fieldMode_vacuum (o : Fin 12) (m : ℤ) (hm : -1 ≤ m) :
    fieldMode o m (vacuum o) = 0 := by
  rw [fieldMode_eq_modes]
  exact modes_vacuum o m hm

theorem fieldMode_creates_conformalState (o : Fin 12) :
    fieldMode o (-2) (vacuum o) = conformalState o := by
  rw [fieldMode_eq_modes]
  exact modes_create_conformalState o

theorem fieldMode_weight_one_zero (o : Fin 12) :
    Module.End.eigenspace (fieldMode o 0) (1:ℂ) = ⊥ := by
  rw [fieldMode_eq_modes]
  exact weight_one_zero o

theorem completeWith_conformal_coefficient (o : Fin 12) (M : RemainingFields o)
    (m : ℤ) :
    HVertexOperator.coeff
      (LatticeOrbifoldBlocks.stateField o (completeWith o M) (conformalState o))
      (-m-2) = modes o m := by
  change HVertexOperator.coeff
    (LatticeOrbifoldBlocks.stateField o (completeWith o M) (evenConformalState o,0))
    (-m-2) = modes o m
  rw [completeWith_even_source, conformal_coefficient]

end HMT.IV.LatticeOrbifoldEvenConformal
end
