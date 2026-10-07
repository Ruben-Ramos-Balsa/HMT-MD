import LatticeTwistedTensorField
import LatticeTwistedChargeNormalization

/-! Normalized ramified charge fields on the whole constructed twisted
carrier. The coefficient shift and scalar are read from the same lattice norm.
The finite charge action is already present in the inherited exponential
kernel; it is not multiplied in a second time. Charge symmetrization and the
even ramified exponents recover the existing positive-sector field exactly.
No twisted Jacobi identity or full state-field map is postulated here. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedRawChargeField
open LatticeCocycle LatticeWeightShells LatticeTwistedCarrier
open LatticeTwistedParity LatticeTwistedPositiveSector
open LatticeTwistedExponentialKernel LatticeTwistedKernelParity
open LatticeTwistedPositiveKernel LatticeTwistedPositiveEnergy
open LatticeTwistedChargeNormalization LatticeTwistedLowWeights
open LatticeFiniteIrreducible LatticeFiniteGroundState
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeHalfIntegerHeisenberg LatticeFockMonomialParity

theorem normScalar_eq_pair_zpow (o : Fin 12) (x : Lattice o) :
    normScalar o x = (2:ℂ)^(-integerPair o x x) := by
  rw [integerPair_eq_two_halfnorm,
    show (2:ℤ)*(halfnormNat o x:ℤ)=((2*halfnormNat o x:ℕ):ℤ) by push_cast; rfl,
    zpow_neg, zpow_natCast]
  rfl

/-- Coefficients of `2^(-<x,x>) t^(-<x,x>) E⁻_x(t) E⁺_x(t) e_x`. -/
def rawChargeCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    Module.End ℂ (Carrier o) :=
  normScalar o x • kernelCoefficient o x 0 (k+integerPair o x x)

theorem rawChargeCoefficient_bounded_pole (o : Fin 12) (x : Lattice o)
    (v : Carrier o) : ∃ b : ℤ, ∀ k<b, rawChargeCoefficient o x k v=0 := by
  obtain ⟨b,hb⟩ := kernelCoefficient_bounded_pole o x 0 v
  refine ⟨b-integerPair o x x, fun k hk => ?_⟩
  simp only [rawChargeCoefficient, LinearMap.smul_apply,
    hb (k+integerPair o x x) (by omega), smul_zero]

def rawChargeField (o : Fin 12) (x : Lattice o) : VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (rawChargeCoefficient o x)
    (rawChargeCoefficient_bounded_pole o x)

theorem rawChargeField_coefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    HVertexOperator.coeff (rawChargeField o x) k = rawChargeCoefficient o x k := rfl

theorem rawChargeCoefficient_basis (o : Fin 12) (x : Lattice o) (k : ℤ)
    (p : BasisIndex o) :
    rawChargeCoefficient o x k (twistedBasis o p) =
      normScalar o x • basisKernelCoefficient o x 0 (k+integerPair o x x) p.1 p.2 := by
  rw [rawChargeCoefficient, LinearMap.smul_apply, kernelCoefficient_basis]

theorem rawChargeCoefficient_zero_charge (o : Fin 12) (k : ℤ) :
    rawChargeCoefficient o 0 k = if k=0 then 1 else 0 := by
  simp only [rawChargeCoefficient, normScalar_zero, integerPair_zero_left,
    add_zero, one_smul, kernel_zero_charge]

theorem rawChargeField_zero_charge (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (rawChargeField o 0) k = if k=0 then 1 else 0 := by
  rw [rawChargeField_coefficient, rawChargeCoefficient_zero_charge]

theorem rawChargeCoefficient_ground (o : Fin 12) (x : Lattice o) (k : ℤ)
    (v : FiniteSpace o) :
    rawChargeCoefficient o x k (groundEmbedding o v) =
      normScalar o x • (if 0≤k+integerPair o x x then
        halfCreationExponentialMode o x (k+integerPair o x x).toNat 1
          ⊗ₜ[ℂ] latticeOperator o x v else 0) := by
  rw [rawChargeCoefficient, LinearMap.smul_apply, kernelCoefficient_ground]
  simp only [sub_zero]

theorem rawChargeCoefficient_ground_leading (o : Fin 12) (x : Lattice o)
    (v : FiniteSpace o) :
    rawChargeCoefficient o x (-integerPair o x x) (groundEmbedding o v) =
      normScalar o x • groundEmbedding o (latticeOperator o x v) := by
  rw [rawChargeCoefficient, LinearMap.smul_apply, neg_add_cancel,
    kernelCoefficient_ground_at_shift]

theorem rawChargeCoefficient_ground_below (o : Fin 12) (x : Lattice o)
    (k : ℤ) (v : FiniteSpace o) (hk : k < -integerPair o x x) :
    rawChargeCoefficient o x k (groundEmbedding o v) = 0 := by
  rw [rawChargeCoefficient_ground, if_neg (by omega), smul_zero]

theorem norm_shift_parity (o : Fin 12) (x : Lattice o) (k : ℤ) :
    paritySign (k+integerPair o x x) = paritySign k := by
  rw [integerPair_eq_two_halfnorm]
  unfold paritySign
  rw [show (k+2*(halfnormNat o x:ℤ))%2=k%2 by omega]

theorem rawChargeCoefficient_neg_charge (o : Fin 12) (x : Lattice o) (k : ℤ) :
    rawChargeCoefficient o (-x) k = paritySign k • rawChargeCoefficient o x k := by
  simp only [rawChargeCoefficient, normScalar_neg, integerPair_neg_neg,
    kernelCoefficient_neg_charge, sub_zero, norm_shift_parity]
  exact smul_comm _ _ _

theorem theta_rawChargeCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (liftedTheta o).comp (rawChargeCoefficient o x k) =
      (rawChargeCoefficient o (-x) k).comp (liftedTheta o) := by
  simp only [rawChargeCoefficient, normScalar_neg, integerPair_neg_neg,
    LinearMap.comp_smul, LinearMap.smul_comp, theta_kernelCoefficient]

def symmetrizedCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    Module.End ℂ (Carrier o) :=
  (2:ℂ)⁻¹ • (rawChargeCoefficient o x k+rawChargeCoefficient o (-x) k)

theorem symmetrizedCoefficient_even (o : Fin 12) (x : Lattice o) (k : ℤ) :
    symmetrizedCoefficient o x (2*k)=rawChargeCoefficient o x (2*k) := by
  unfold symmetrizedCoefficient
  rw [rawChargeCoefficient_neg_charge, paritySign_even, one_smul]
  module

theorem symmetrizedCoefficient_odd (o : Fin 12) (x : Lattice o) (k : ℤ) :
    symmetrizedCoefficient o x (2*k+1)=0 := by
  unfold symmetrizedCoefficient
  rw [rawChargeCoefficient_neg_charge, paritySign_odd]
  module

theorem chargeField_inclusion_even_raw (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (positiveSector o).subtype.comp (HVertexOperator.coeff (chargeField o x) k) =
      (rawChargeCoefficient o x (2*k)).comp (positiveSector o).subtype := by
  apply LinearMap.ext
  intro v
  simp only [LinearMap.comp_apply, chargeField_coefficient, chargeCoefficient,
    LinearMap.smul_apply, Submodule.coe_smul, positiveCoefficient_coe,
    rawChargeCoefficient]
  change normScalar o x • descendedCoefficient o x 0 (k+(halfnormNat o x:ℤ)) v.val =
    normScalar o x • kernelCoefficient o x 0 (2*k+integerPair o x x) v.val
  rw [descendedCoefficient_eq_kernel, integerPair_eq_two_halfnorm]
  rw [show 2*(k+(halfnormNat o x:ℤ))+0=2*k+2*(halfnormNat o x:ℤ) by omega]

theorem chargeField_inclusion_symmetrized (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (positiveSector o).subtype.comp (HVertexOperator.coeff (chargeField o x) k) =
      (symmetrizedCoefficient o x (2*k)).comp (positiveSector o).subtype := by
  rw [symmetrizedCoefficient_even]
  exact chargeField_inclusion_even_raw o x k

theorem rawChargeField_even_intertwines (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (positiveSector o).subtype.comp (HVertexOperator.coeff (chargeField o x) k) =
      (HVertexOperator.coeff (rawChargeField o x) (2*k)).comp
        (positiveSector o).subtype := by
  rw [rawChargeField_coefficient]
  exact chargeField_inclusion_even_raw o x k

end HMT.IV.LatticeTwistedRawChargeField
end
