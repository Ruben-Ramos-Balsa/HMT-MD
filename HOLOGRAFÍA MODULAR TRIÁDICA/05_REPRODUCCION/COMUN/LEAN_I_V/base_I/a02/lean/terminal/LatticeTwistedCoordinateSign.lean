import CoordinateWeightSign
import LatticeTwistedWeightSignLaws

/-! Coordinate reflection on the actual positive twisted carrier.
Its value on conformal weight d is (-1)^d. The decomposition is supplied
by the proved grading of the existing carrier, not by a replacement space. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedCoordinateSign
open LatticeTwistedPositiveSector LatticeTwistedPositiveGrading
open LatticeTwistedContragredientTruncation LatticeTwistedWeightSignLaws
open CoordinateWeightSign

def coordinateSign (o : Fin 12) : Module.End ℂ (positiveSector o) :=
  weightSign (positiveConformalMode o 0) (positive_weights_span o)

theorem coordinateSign_weight (o : Fin 12) (d : ℕ) (v : positiveSector o)
    (hv : v ∈ positiveWeightSpace o d) :
    coordinateSign o v = (-1 : ℂ)^d • v := by
  exact weightSign_apply_of_weight (positiveConformalMode o 0)
    (positive_weights_span o) d (Module.End.mem_eigenspace_iff.mp hv)

theorem coordinateSign_square (o : Fin 12) :
    coordinateSign o * coordinateSign o = 1 :=
  sign_square o (coordinateSign o) (coordinateSign_weight o)

theorem coordinateSign_involutive (o : Fin 12) :
    Function.Involutive (coordinateSign o) := by
  intro v
  exact LinearMap.congr_fun (coordinateSign_square o) v

def coordinateSignEquiv (o : Fin 12) : positiveSector o ≃ₗ[ℂ] positiveSector o :=
  LinearEquiv.ofInvolutive (coordinateSign o) (coordinateSign_involutive o)

theorem coordinateSign_anticommutes_lowering (o : Fin 12) :
    coordinateSign o * lowering o = -(lowering o * coordinateSign o) :=
  sign_anticommutes_lowering o (coordinateSign o) (coordinateSign_weight o)

theorem coordinateSign_commutes_energy (o : Fin 12) :
    coordinateSign o * positiveConformalMode o 0 =
      positiveConformalMode o 0 * coordinateSign o :=
  sign_commutes_energy o (coordinateSign o) (coordinateSign_weight o)

theorem coordinateSign_conjugates_lowering (o : Fin 12) :
    coordinateSign o * lowering o * coordinateSign o = -lowering o := by
  apply LinearMap.ext
  intro v
  have h := LinearMap.congr_fun (coordinateSign_anticommutes_lowering o)
    (coordinateSign o v)
  simpa only [Module.End.mul_apply, LinearMap.neg_apply,
    coordinateSign_involutive o v] using h

theorem coordinateSign_conjugates_energy (o : Fin 12) :
    coordinateSign o * positiveConformalMode o 0 * coordinateSign o =
      positiveConformalMode o 0 := by
  rw [coordinateSign_commutes_energy, mul_assoc, coordinateSign_square, mul_one]

theorem coordinateSign_lowering_power (o : Fin 12) (n : ℕ) :
    coordinateSign o * (lowering o)^n =
      (-1 : ℂ)^n • ((lowering o)^n * coordinateSign o) :=
  sign_lowering_power o (coordinateSign o) (coordinateSign_weight o) n

theorem coordinateSign_inversionCoefficient (o : Fin 12) (n : ℕ) :
    coordinateSign o * inversionCoefficient o n * coordinateSign o =
      (-1 : ℂ)^n • inversionCoefficient o n := by
  simp only [inversionCoefficient, mul_smul_comm,
    coordinateSign_lowering_power, smul_mul_assoc,
    mul_assoc, coordinateSign_square, mul_one]
  module

end HMT.IV.LatticeTwistedCoordinateSign
end
