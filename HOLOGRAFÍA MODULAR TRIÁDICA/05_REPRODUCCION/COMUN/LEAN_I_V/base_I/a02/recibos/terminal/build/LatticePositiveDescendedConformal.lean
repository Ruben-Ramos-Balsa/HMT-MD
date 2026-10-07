import LatticeTwistedPositiveStateDescent
import LatticeTwistedStateConformal
import LatticeEvenConformal

/-! The descended corrected field of the inherited even conformal state has
exactly the existing Virasoro modes on the positive twisted carrier. This is
the transport of the proved ramified coefficient identity through restriction
and descent, with z = t^2; no normalization or field identity is assumed. -/

noncomputable section
namespace HMT.IV.LatticePositiveDescendedConformal

open LatticeCocycle LatticeEvenConformal
open LatticeTwistedPositiveSector LatticeTwistedPositiveStateDescent
open LatticeTwistedStateField LatticeTwistedStateConformal

theorem positiveDescended_conformalState_mode (o : Fin 12) (m : ℤ) :
    HVertexOperator.coeff
      (positiveDescendedAssignment o (evenConformalState o)) (-m-2) =
      positiveConformalMode o m := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  change HVertexOperator.coeff
    (twistedStateField o (evenConformalState o).val) (2*(-m-2)) v.val =
      LatticeTwistedCarrier.conformalMode o m v.val
  rw [evenConformalState_coe, show 2*(-m-2) = -2*m-4 by ring,
    twistedStateField_conformalState_coefficient]

theorem positiveDescended_conformalState_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff
      (positiveDescendedAssignment o (evenConformalState o)) k =
      positiveConformalMode o (-k-2) := by
  have h := positiveDescended_conformalState_mode o (-k-2)
  convert h using 1
  ring

theorem positiveDescended_conformalState_mode_apply (o : Fin 12) (m : ℤ)
    (v : positiveSector o) :
    HVertexOperator.coeff
      (positiveDescendedAssignment o (evenConformalState o)) (-m-2) v =
      positiveConformalMode o m v := by
  rw [positiveDescended_conformalState_mode]

end HMT.IV.LatticePositiveDescendedConformal
end

#print axioms HMT.IV.LatticePositiveDescendedConformal.positiveDescended_conformalState_mode
#print axioms HMT.IV.LatticePositiveDescendedConformal.positiveDescended_conformalState_coefficient
#print axioms HMT.IV.LatticePositiveDescendedConformal.positiveDescended_conformalState_mode_apply
