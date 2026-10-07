import LatticeOscillatorTranslation
import LatticeChargedFieldEnergy

/-!
The charged translation operator on the existing carrier is the oscillator
derivation plus multiplication by the frequency-one vector of the incoming
lattice charge. Its energy shift and vacuum action are proved below. These
facts alone do not claim differential covariance of every charged field or
the axioms of a vertex algebra.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeTranslationOperator

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeEulerEnergy HMT.IV.LatticeEnergyGrading
open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeChargeEnergy HMT.IV.LatticeWeightShells
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeExponentialEnergy
open HMT.IV.LatticeChargedFieldEnergy HMT.IV.LatticeOscillatorTranslation
open scoped TensorProduct

def chargeTranslation (o : Fin 12) : Module.End ℂ (LatticeCarrier o) :=
  (carrierBasis o).constr ℂ fun p =>
    (chargeCreationState o p.2 0 * monomialBasis o p.1) ⊗ₜ[ℂ]
      basisElement o p.2

@[simp] theorem chargeTranslation_basis (o : Fin 12)
    (a : Occupation o) (y : Lattice o) :
    chargeTranslation o (carrierBasis o (a,y)) =
      (chargeCreationState o y 0 * monomialBasis o a) ⊗ₜ[ℂ] basisElement o y :=
  Basis.constr_basis _ _ _ _

theorem chargeTranslation_pure (o : Fin 12) (v : Fock o) (y : Lattice o) :
    chargeTranslation o (v ⊗ₜ[ℂ] basisElement o y) =
      (chargeCreationState o y 0 * v) ⊗ₜ[ℂ] basisElement o y := by
  let emb : Fock o →ₗ[ℂ] LatticeCarrier o :=
    (TensorProduct.mk ℂ (Fock o) (TwistedAlgebra o)).flip (basisElement o y)
  have h : (chargeTranslation o).comp emb =
      emb.comp (LinearMap.mulLeft ℂ (chargeCreationState o y 0)) := by
    apply (monomialBasis o).ext
    intro a
    change chargeTranslation o (monomialBasis o a ⊗ₜ[ℂ] basisElement o y) = _
    have hb : carrierBasis o (a,y) =
        monomialBasis o a ⊗ₜ[ℂ] basisElement o y := by
      simp only [carrierBasis, Basis.tensorProduct_apply]
      rfl
    rw [← hb]
    rw [chargeTranslation_basis]
    rfl
  exact LinearMap.congr_fun h v

theorem chargeTranslation_energy (o : Fin 12) :
    (energy o).comp (chargeTranslation o) -
      (chargeTranslation o).comp (energy o) = chargeTranslation o := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  change energy o (chargeTranslation o (carrierBasis o (a,y))) -
    chargeTranslation o (energy o (carrierBasis o (a,y))) =
      chargeTranslation o (carrierBasis o (a,y))
  rw [chargeTranslation_basis, energy_pure, (euler o).leibniz,
    euler_chargeCreationState, euler_monomial, energy_basis, map_smul,
    chargeTranslation_basis]
  simp only [Nat.cast_zero, zero_add, one_smul]
  have hs : chargeCreationState o y 0 •
        ((occupationWeight o a : ℂ) • monomialBasis o a) +
      monomialBasis o a • chargeCreationState o y 0 =
      ((occupationWeight o a : ℂ)+1) •
        (chargeCreationState o y 0 * monomialBasis o a) := by
    simp only [smul_eq_mul, Algebra.smul_def, map_add, map_one]
    ring
  rw [hs]
  simp only [← TensorProduct.smul_tmul', totalWeight, Nat.cast_add]
  module

theorem chargeTranslation_vacuum (o : Fin 12) :
    chargeTranslation o (vacuum o) = 0 := by
  rw [← vacuum_is_empty_monomial, chargeTranslation_basis]
  simp [chargeCreationState, chargeModeVector]

def translation (o : Fin 12) : Module.End ℂ (LatticeCarrier o) :=
  carrierTranslation o + chargeTranslation o

theorem translation_pure (o : Fin 12) (v : Fock o) (y : Lattice o) :
    translation o (v ⊗ₜ[ℂ] basisElement o y) =
      (LatticeOscillatorTranslation.translation o v + chargeCreationState o y 0 * v)
        ⊗ₜ[ℂ] basisElement o y := by
  rw [translation, LinearMap.add_apply, carrierTranslation, onCarrier_pure,
    chargeTranslation_pure, TensorProduct.add_tmul]
  rfl

theorem translation_vacuum (o : Fin 12) : translation o (vacuum o) = 0 := by
  rw [translation, LinearMap.add_apply, carrierTranslation_vacuum,
    chargeTranslation_vacuum, add_zero]

theorem translation_energy (o : Fin 12) :
    (energy o).comp (translation o) - (translation o).comp (energy o) =
      translation o := by
  apply LinearMap.ext
  intro v
  have hc := LinearMap.congr_fun (chargeTranslation_energy o) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply] at hc
  have ht := carrierTranslation_energy o v
  change energy o (carrierTranslation o v + chargeTranslation o v) -
    (carrierTranslation o (energy o v) + chargeTranslation o (energy o v)) =
      carrierTranslation o v + chargeTranslation o v
  rw [map_add]
  calc
    _ = (energy o (carrierTranslation o v) - carrierTranslation o (energy o v)) +
      (energy o (chargeTranslation o v) - chargeTranslation o (energy o v)) := by abel
    _ = _ := by rw [ht, hc]

theorem translation_changes_energy (o : Fin 12) (d : ℂ)
    (v : LatticeCarrier o) (hv : energy o v = d • v) :
    energy o (translation o v) = (d+1) • translation o v := by
  have h := LinearMap.congr_fun (translation_energy o) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply] at h
  rw [hv, map_smul, sub_eq_iff_eq_add] at h
  rw [h, add_smul, one_smul]
  abel

end HMT.IV.LatticeTranslationOperator
end

#print axioms HMT.IV.LatticeTranslationOperator.chargeTranslation_basis
#print axioms HMT.IV.LatticeTranslationOperator.chargeTranslation_pure
#print axioms HMT.IV.LatticeTranslationOperator.chargeTranslation_energy
#print axioms HMT.IV.LatticeTranslationOperator.chargeTranslation_vacuum
#print axioms HMT.IV.LatticeTranslationOperator.translation_pure
#print axioms HMT.IV.LatticeTranslationOperator.translation_vacuum
#print axioms HMT.IV.LatticeTranslationOperator.translation_energy
#print axioms HMT.IV.LatticeTranslationOperator.translation_changes_energy
