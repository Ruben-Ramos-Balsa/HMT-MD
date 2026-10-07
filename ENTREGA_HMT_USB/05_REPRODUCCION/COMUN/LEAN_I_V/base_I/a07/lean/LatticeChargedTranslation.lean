import LatticeTranslationDefect
import LatticeTranslationChargedGround

/-!
Translation covariance of the constructed charged fields on the whole
constructed carrier. The ground calculation is discharged before applying
the proved creation-history spanning theorem. No covariance hypothesis is
retained and no VOA or orbifold axiom is introduced.
-/

noncomputable section
namespace HMT.IV.LatticeChargedTranslation

open LatticeCocycle LatticeOscillatorFock LatticeChargedVertexField
open LatticeTranslationDefect LatticeTranslationChargedGround

local notation "T" => LatticeTranslationOperator.translation

theorem charged_translation_defect_zero (o : Fin 12) (x : Lattice o) (k : ℤ) :
    defect o x k = 0 := by
  apply defect_zero_of_ground o x
  intro y j
  change T o (fieldCoefficient o x j _) - fieldCoefficient o x j (T o _) -
    ((j : ℂ)+1) • fieldCoefficient o x (j+1) _ = 0
  exact sub_eq_zero.mpr (translation_charged_ground o x y j)

theorem translation_charged_coefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    T o * fieldCoefficient o x k - fieldCoefficient o x k * T o =
      ((k : ℂ)+1) • fieldCoefficient o x (k+1) := by
  exact sub_eq_zero.mp (charged_translation_defect_zero o x k)

theorem translation_charged_coefficient_apply (o : Fin 12) (x : Lattice o)
    (k : ℤ) (v : LatticeCarrier o) :
    T o (fieldCoefficient o x k v) - fieldCoefficient o x k (T o v) =
      ((k : ℂ)+1) • fieldCoefficient o x (k+1) v :=
  LinearMap.congr_fun (translation_charged_coefficient o x k) v

end HMT.IV.LatticeChargedTranslation
end

#print axioms HMT.IV.LatticeChargedTranslation.charged_translation_defect_zero
#print axioms HMT.IV.LatticeChargedTranslation.translation_charged_coefficient
#print axioms HMT.IV.LatticeChargedTranslation.translation_charged_coefficient_apply
