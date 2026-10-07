import LatticeChargePairing
import LatticeIntegerPairingWeights
import LatticeEnergyGrading
import Mathlib.LinearAlgebra.BilinearForm.TensorProduct

/-! The bilinear form on the existing untwisted lattice carrier, assembled
from the contravariant oscillator form and the norm/cocycle charge form. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeUntwistedPairing
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeParityCarrier LatticeIntegerFockPairing LatticeIntegerPairingWeights
open LatticeChargePairing LatticeEnergyGrading LatticeWeightShells
open TwistedGroupAlgebra
open scoped TensorProduct

def untwistedPairing (o : Fin 12) : LinearMap.BilinForm ℂ (LatticeCarrier o) :=
  (contravariantPairing o).tmul (chargePairing o)

theorem untwistedPairing_pure (o : Fin 12) (u v : Fock o) (s t : TwistedAlgebra o) :
    untwistedPairing o (u ⊗ₜ[ℂ] s) (v ⊗ₜ[ℂ] t) =
      chargePairing o s t * contravariantPairing o u v := rfl

def chargeCoordinates (o : Fin 12) : LatticeCarrier o ≃ₗ[ℂ] (Lattice o →₀ Fock o) :=
  TensorProduct.equivFinsuppOfBasisRight (latticeBasisComplex o)

theorem untwistedPairing_right_test (o : Fin 12) (w : LatticeCarrier o)
    (u : Fock o) (x : Lattice o) :
    untwistedPairing o w (u ⊗ₜ[ℂ] chargeDual o x) =
      contravariantPairing o (chargeCoordinates o w x) u := by
  induction w using TensorProduct.induction_on with
  | zero => simp
  | tmul v t =>
    rw [untwistedPairing_pure, chargeDual_right]
    change _ = contravariantPairing o
      ((TensorProduct.equivFinsuppOfBasisRight (latticeBasisComplex o))
        (v ⊗ₜ[ℂ] t) x) u
    rw [TensorProduct.equivFinsuppOfBasisRight_apply_tmul_apply]
    simp only [map_smul, LinearMap.smul_apply, smul_eq_mul,
      latticeBasisComplex, Finsupp.basisSingleOne_repr]
  | add x y hx hy => simp only [map_add, LinearMap.add_apply, Finsupp.add_apply, hx, hy]

theorem untwistedPairing_left_test (o : Fin 12) (w : LatticeCarrier o)
    (u : Fock o) (x : Lattice o) :
    untwistedPairing o (u ⊗ₜ[ℂ] chargeDual o x) w =
      contravariantPairing o u (chargeCoordinates o w x) := by
  induction w using TensorProduct.induction_on with
  | zero => simp
  | tmul v t =>
    rw [untwistedPairing_pure, chargeDual_left]
    change _ = contravariantPairing o u
      ((TensorProduct.equivFinsuppOfBasisRight (latticeBasisComplex o))
        (v ⊗ₜ[ℂ] t) x)
    rw [TensorProduct.equivFinsuppOfBasisRight_apply_tmul_apply]
    simp only [map_smul, smul_eq_mul, latticeBasisComplex, Finsupp.basisSingleOne_repr]
  | add x y hx hy => simp only [map_add, Finsupp.add_apply, hx, hy]

theorem untwistedPairing_nondegenerate (o : Fin 12) :
    (untwistedPairing o).Nondegenerate := by
  intro v hv
  apply (chargeCoordinates o).injective
  apply Finsupp.ext
  intro x
  simp only [map_zero, Finsupp.zero_apply]
  apply contravariantPairing_nondegenerate o
  intro u
  rw [← untwistedPairing_right_test]
  exact hv _

theorem untwistedPairing_right_separating (o : Fin 12) (v : LatticeCarrier o)
    (h : ∀ w, untwistedPairing o w v = 0) : v = 0 := by
  apply (chargeCoordinates o).injective
  apply Finsupp.ext
  intro x
  simp only [map_zero, Finsupp.zero_apply]
  apply contravariantPairing_right_separating o
  intro u
  rw [← untwistedPairing_left_test]
  exact h _

theorem untwistedPairing_theta (o : Fin 12) (u v : LatticeCarrier o) :
    untwistedPairing o (carrierTheta o u) v =
      untwistedPairing o u (carrierTheta o v) := by
  induction u using TensorProduct.induction_on with
  | zero => simp
  | tmul u s =>
    induction v using TensorProduct.induction_on with
    | zero => simp
    | tmul v t =>
      simp only [carrierTheta_pure, untwistedPairing_pure,
        contravariantPairing_theta]
      change chargePairing o (WittNegationLift.thetaLinear o s) t * _ =
        chargePairing o s (WittNegationLift.thetaLinear o t) * _
      rw [chargePairing_theta]
    | add x y hx hy => simp only [map_add, hx, hy]
  | add x y hx hy => simp only [map_add, LinearMap.add_apply, hx, hy]

theorem untwistedPairing_basis (o : Fin 12)
    (a b : Occupation o) (x y : Lattice o) :
    untwistedPairing o (carrierBasis o (a,x)) (carrierBasis o (b,y)) =
      (if y = -x then chargeWeight o x else 0) *
        contravariantPairing o (monomialBasis o a) (monomialBasis o b) := by
  rw [carrierBasis, Basis.tensorProduct_apply, Basis.tensorProduct_apply,
    untwistedPairing_pure]
  change chargePairing o (basisElement o x) (basisElement o y) * _ = _
  rw [chargePairing_basis]

theorem untwistedPairing_basis_off_weight (o : Fin 12)
    (p q : Occupation o × Lattice o) (hpq : totalWeight o p ≠ totalWeight o q) :
    untwistedPairing o (carrierBasis o p) (carrierBasis o q) = 0 := by
  rcases p with ⟨a,x⟩
  rcases q with ⟨b,y⟩
  rw [untwistedPairing_basis]
  by_cases hy : y = -x
  · subst y
    rw [if_pos rfl]
    have hab : occupationWeight o a ≠ occupationWeight o b := by
      intro h
      apply hpq
      simp only [totalWeight, halfnormNat_neg, h]
    rw [contravariantPairing_weight_orthogonal o a b hab, mul_zero]
  · rw [if_neg hy, zero_mul]

theorem untwistedPairing_energy (o : Fin 12) (u v : LatticeCarrier o) :
    untwistedPairing o (energy o u) v = untwistedPairing o u (energy o v) := by
  have he : LinearMap.comp (untwistedPairing o) (energy o) =
      (untwistedPairing o).compl₂ (energy o) := by
    apply (carrierBasis o).ext
    intro p
    apply (carrierBasis o).ext
    intro q
    change untwistedPairing o (energy o (carrierBasis o p)) (carrierBasis o q) =
      untwistedPairing o (carrierBasis o p) (energy o (carrierBasis o q))
    rw [energy_basis, energy_basis]
    simp only [map_smul, LinearMap.smul_apply, smul_eq_mul]
    by_cases h : totalWeight o p = totalWeight o q
    · rw [h]
    · rw [untwistedPairing_basis_off_weight o p q h]
      simp
  exact LinearMap.congr_fun (LinearMap.congr_fun he u) v

theorem untwistedPairing_vacuum (o : Fin 12) :
    untwistedPairing o (vacuum o) (vacuum o) = 1 := by
  change untwistedPairing o ((1 : Fock o) ⊗ₜ[ℂ] basisElement o 0)
    ((1 : Fock o) ⊗ₜ[ℂ] basisElement o 0) = 1
  rw [untwistedPairing_pure, chargePairing_vacuum, one_mul,
    contravariantPairing_apply, map_one (integerGramTransport o)]
  have h1 : (1 : Fock o) = monomialBasis o 0 := by
    rw [monomialBasis_product, Finsupp.prod_zero_index]
  rw [h1, LatticeFactorialPairing.factorialPairing_left]
  simp only [LatticeFactorialPairing.occupationFactorial_zero,
    Basis.repr_self, Finsupp.single_eq_same, mul_one]

end HMT.IV.LatticeUntwistedPairing
end
