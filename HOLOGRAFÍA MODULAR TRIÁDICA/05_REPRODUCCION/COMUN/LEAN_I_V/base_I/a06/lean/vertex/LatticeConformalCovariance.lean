import LatticeConformalState
import LatticeStateFieldEnergy
import LatticeStateFieldTranslation

/-! Energy and translation covariance of the modes of the actual quadratic
state. These identities are proved before identifying its zero and minus-one
modes with the corresponding inherited operators. -/

noncomputable section
namespace HMT.IV.LatticeConformalCovariance

open LatticeOscillatorFock LatticeConformalState LatticeEnergyGrading
open LatticeStateFieldEnergy LatticeStateFieldTranslation LatticeStateFieldMap

local notation "T" => LatticeTranslationOperator.translation

theorem conformalMode_energy (o : Fin 12) (m : ℤ) :
    energy o * conformalMode o m - conformalMode o m * energy o =
      (-(m : ℂ)) • conformalMode o m := by
  have h := stateField_homogeneous_energy o (conformalState o) 2
    (conformalState_weight_two o) (-m-2)
  change energy o * conformalMode o m - conformalMode o m * energy o =
    (2 + ((-m-2 : ℤ) : ℂ)) • conformalMode o m at h
  have hs : (2 + ((-m-2 : ℤ) : ℂ)) = -(m : ℂ) := by push_cast; ring
  simpa only [hs] using h

theorem conformalMode_changes_energy (o : Fin 12) (m : ℤ)
    (u : LatticeCarrier o) (d : ℂ) (hu : energy o u = d • u) :
    energy o (conformalMode o m u) = (d - (m : ℂ)) • conformalMode o m u := by
  have h := LinearMap.congr_fun (conformalMode_energy o m) u
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    hu, map_smul] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h, sub_smul, neg_smul]
  abel

theorem conformalMode_translation (o : Fin 12) (m : ℤ) :
    T o * conformalMode o m - conformalMode o m * T o =
      (-((m : ℂ)+1)) • conformalMode o (m-1) := by
  have h := stateField_translation o (conformalState o) (-m-2)
  change T o * conformalMode o m - conformalMode o m * T o =
    (((-m-2 : ℤ) : ℂ)+1) •
      HVertexOperator.coeff (conformalField o) (-m-2+1) at h
  rw [show -m-2+1 = -(m-1)-2 by omega] at h
  have hs : (((-m-2 : ℤ) : ℂ)+1) = -((m : ℂ)+1) := by push_cast; ring
  simpa only [hs, conformalMode] using h

theorem conformalMode_vacuum (o : Fin 12) (m : ℤ) (hm : -1 ≤ m) :
    conformalMode o m (vacuum o) = 0 :=
  (conformalField_creates o).1 (-m-2) (by omega)

theorem conformalMode_minus_two_vacuum (o : Fin 12) :
    conformalMode o (-2) (vacuum o) = conformalState o := by
  change HVertexOperator.coeff (conformalField o) 0 (vacuum o) = _
  exact (conformalField_creates o).2

theorem conformalMode_minus_three_vacuum (o : Fin 12) :
    conformalMode o (-3) (vacuum o) = T o (conformalState o) := by
  change HVertexOperator.coeff (stateField o (conformalState o)) 1 (vacuum o) = _
  exact stateField_translation_vacuum_coefficient o (conformalState o)

end HMT.IV.LatticeConformalCovariance
end

#print axioms HMT.IV.LatticeConformalCovariance.conformalMode_energy
#print axioms HMT.IV.LatticeConformalCovariance.conformalMode_changes_energy
#print axioms HMT.IV.LatticeConformalCovariance.conformalMode_translation
#print axioms HMT.IV.LatticeConformalCovariance.conformalMode_vacuum
#print axioms HMT.IV.LatticeConformalCovariance.conformalMode_minus_two_vacuum
#print axioms HMT.IV.LatticeConformalCovariance.conformalMode_minus_three_vacuum
