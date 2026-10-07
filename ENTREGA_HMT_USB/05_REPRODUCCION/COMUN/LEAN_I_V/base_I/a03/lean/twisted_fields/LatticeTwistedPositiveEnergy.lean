import LatticeTwistedKernelEnergy
import LatticeTwistedPositiveKernel

/-! Conformal covariance of the existing charge-even kernel on the actual
positive sector. Descent uses ramified degree 2k+s, so the proved shift
(2k+s-s)/2 is exactly k. Stability under L0 and restriction of the kernel were
already proved; no field normalization or state-field correspondence is added. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedPositiveEnergy
open LatticeCocycle LatticeTwistedCarrier LatticeTwistedPositiveSector
open LatticeTwistedExponentialKernel LatticeTwistedKernelParity
open LatticeTwistedKernelEnergy LatticeTwistedPositiveKernel

theorem descendedCoefficient_eq_kernel (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    descendedCoefficient o x s k = kernelCoefficient o x s (2*k+s) :=
  evenKernelCoefficient_even_shift o x s k

theorem descendedCoefficient_conformal_commutator (o : Fin 12) (x : Lattice o)
    (s k : ℤ) :
    conformalMode o 0 * descendedCoefficient o x s k -
      descendedCoefficient o x s k * conformalMode o 0 =
        (k:ℂ) • descendedCoefficient o x s k := by
  rw [descendedCoefficient_eq_kernel, kernelCoefficient_conformal_commutator]
  congr 1
  push_cast
  ring

theorem positiveCoefficient_conformal_commutator (o : Fin 12) (x : Lattice o)
    (s k : ℤ) :
    positiveConformalMode o 0 * positiveCoefficient o x s k -
      positiveCoefficient o x s k * positiveConformalMode o 0 =
        (k:ℂ) • positiveCoefficient o x s k := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  exact LinearMap.congr_fun (descendedCoefficient_conformal_commutator o x s k) v.val

theorem positiveKernel_conformal_commutator (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    positiveConformalMode o 0 * HVertexOperator.coeff (positiveKernel o x s) k -
      HVertexOperator.coeff (positiveKernel o x s) k * positiveConformalMode o 0 =
        (k:ℂ) • HVertexOperator.coeff (positiveKernel o x s) k := by
  rw [positiveKernel_coefficient]
  exact positiveCoefficient_conformal_commutator o x s k

theorem positiveCoefficient_weight_shift (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (v : positiveSector o) (d : ℂ) (hv : positiveConformalMode o 0 v = d • v) :
    positiveConformalMode o 0 (positiveCoefficient o x s k v) =
      (d+(k:ℂ)) • positiveCoefficient o x s k v := by
  have h := LinearMap.congr_fun (positiveCoefficient_conformal_commutator o x s k) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply] at h
  rw [hv, map_smul, sub_eq_iff_eq_add] at h
  rw [h]
  module

theorem positiveKernel_weight_shift (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (v : positiveSector o) (d : ℂ) (hv : positiveConformalMode o 0 v = d • v) :
    positiveConformalMode o 0 (HVertexOperator.coeff (positiveKernel o x s) k v) =
      (d+(k:ℂ)) • HVertexOperator.coeff (positiveKernel o x s) k v := by
  rw [positiveKernel_coefficient]
  exact positiveCoefficient_weight_shift o x s k v d hv

theorem positiveKernel_maps_eigenspace (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (d : ℂ) (v : positiveSector o)
    (hv : v ∈ Module.End.eigenspace (positiveConformalMode o 0) d) :
    HVertexOperator.coeff (positiveKernel o x s) k v ∈
      Module.End.eigenspace (positiveConformalMode o 0) (d+(k:ℂ)) := by
  apply Module.End.mem_eigenspace_iff.mpr
  exact positiveKernel_weight_shift o x s k v d (Module.End.mem_eigenspace_iff.mp hv)

end HMT.IV.LatticeTwistedPositiveEnergy
end

#print axioms HMT.IV.LatticeTwistedPositiveEnergy.descendedCoefficient_eq_kernel
#print axioms HMT.IV.LatticeTwistedPositiveEnergy.descendedCoefficient_conformal_commutator
#print axioms HMT.IV.LatticeTwistedPositiveEnergy.positiveCoefficient_conformal_commutator
#print axioms HMT.IV.LatticeTwistedPositiveEnergy.positiveKernel_conformal_commutator
#print axioms HMT.IV.LatticeTwistedPositiveEnergy.positiveCoefficient_weight_shift
#print axioms HMT.IV.LatticeTwistedPositiveEnergy.positiveKernel_weight_shift
#print axioms HMT.IV.LatticeTwistedPositiveEnergy.positiveKernel_maps_eigenspace
