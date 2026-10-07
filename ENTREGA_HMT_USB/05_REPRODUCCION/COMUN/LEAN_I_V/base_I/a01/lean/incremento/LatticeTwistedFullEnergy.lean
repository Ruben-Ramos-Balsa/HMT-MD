import LatticeTwistedRawEnergy
import LatticeTwistedCorrectedEnergy
import LatticeTwistedPositiveStateDescent
import LatticeEvenConformal
import LatticeTwistedEvenProduct
import SkewFieldEnergy

/-! Energy covariance of the actual full corrected, descended and skew fields.
All coefficients are inherited constructions; no energy equation is an input. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedFullEnergy
open LatticeOscillatorFock LatticeEnergyGrading LatticeTwistedCarrier
open LatticeTwistedRawStateField LatticeTwistedRawEnergy LatticeTwistedCorrectedEnergy
open LatticeTwistedStateField LatticeTwistedPositiveStateDescent
open LatticeEvenVertexFields LatticeEvenConformal LatticeTwistedPositiveSector
open LatticeTwistedEvenProduct SkewFieldEnergy

theorem twistedStateField_energy (o : Fin 12) : EnergyCovariant o (twistedStateField o) := by
  apply correctedAssignment_energy
  intro u k
  exact rawStateField_energy o u k

theorem positiveDescended_energy (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    positiveConformalMode o 0 * HVertexOperator.coeff (positiveDescendedAssignment o u) k -
      HVertexOperator.coeff (positiveDescendedAssignment o u) k * positiveConformalMode o 0 =
    HVertexOperator.coeff (positiveDescendedAssignment o (evenConformalMode o 0 u)) k +
      (k:ℂ) • HVertexOperator.coeff (positiveDescendedAssignment o u) k := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  have h := LinearMap.congr_fun (twistedStateField_energy o u.val (2*k)) v.val
  change conformalMode o 0 (HVertexOperator.coeff (twistedStateField o u.val) (2*k) v.val) -
    HVertexOperator.coeff (twistedStateField o u.val) (2*k) (conformalMode o 0 v.val) =
      HVertexOperator.coeff (twistedStateField o (energy o u.val)) (2*k) v.val +
        (((2*k:ℤ):ℂ)/2) • HVertexOperator.coeff (twistedStateField o u.val) (2*k) v.val at h
  change conformalMode o 0 (HVertexOperator.coeff (twistedStateField o u.val) (2*k) v.val) -
    HVertexOperator.coeff (twistedStateField o u.val) (2*k) (conformalMode o 0 v.val) =
      HVertexOperator.coeff (twistedStateField o (evenConformalMode o 0 u).val) (2*k) v.val +
        (k:ℂ) • HVertexOperator.coeff (twistedStateField o u.val) (2*k) v.val
  rw [evenConformalMode_zero_energy]
  have hs : (((2*k:ℤ):ℂ)/2) = (k:ℂ) := by push_cast; ring
  simpa only [hs] using h

theorem positiveDescended_weight (o : Fin 12) (u : evenSpace o) (v : positiveSector o)
    (a b : ℂ) (hu : evenConformalMode o 0 u = a • u)
    (hv : positiveConformalMode o 0 v = b • v) (k : ℤ) :
    positiveConformalMode o 0 (HVertexOperator.coeff (positiveDescendedAssignment o u) k v) =
      (a+b+(k:ℂ)) • HVertexOperator.coeff (positiveDescendedAssignment o u) k v := by
  have h := LinearMap.congr_fun (positiveDescended_energy o u k) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.add_apply,
    LinearMap.smul_apply, hu, hv, map_smul, HVertexOperator.coeff_smul,
    Pi.smul_apply] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h]
  module

theorem translation_raises (o : Fin 12) (v : positiveSector o) :
    positiveConformalMode o 0 (translation o v) =
      translation o (positiveConformalMode o 0 v) + translation o v := by
  have hc : positiveConformalMode o 0 * positiveConformalMode o (-1) -
      positiveConformalMode o (-1) * positiveConformalMode o 0 =
        positiveConformalMode o (-1) := by
    have h := positive_virasoro_central_charge_twentyFour o 0 (-1)
    norm_num at h
    exact h
  have h := LinearMap.congr_fun hc v
  change positiveConformalMode o 0 (translation o v) -
    translation o (positiveConformalMode o 0 v) = translation o v at h
  exact (sub_eq_iff_eq_add.mp h).trans (add_comm _ _)

theorem twistedEvenField_weight (o : Fin 12) (v : positiveSector o) (u : evenSpace o)
    (a b : ℂ) (hu : evenConformalMode o 0 u = a • u)
    (hv : positiveConformalMode o 0 v = b • v) (k : ℤ) :
    positiveConformalMode o 0 (HVertexOperator.coeff (twistedEvenField o v) k u) =
      (a+b+(k:ℂ)) • HVertexOperator.coeff (twistedEvenField o v) k u := by
  exact skewAssignment_weight (positiveDescendedAssignment o) (positiveConformalMode o 0)
    (translation o) (translation_raises o) v u (a+b)
      (positiveDescended_weight o u v a b hu hv) k

end HMT.IV.LatticeTwistedFullEnergy
end
