import LatticeTwistedNormalProduct
import LatticeHalfConformalModes

/-!
The half-Heisenberg normal product on the actual twisted carrier is the
tensor transport of the already constructed half-normal quadratic modes.
The equality is proved term by term and then across the pointwise finite
sums. Gram contraction gives the unshifted quadratic mode; no vacuum shift,
Jacobi identity or complete twisted state-field map is assumed here.
-/

noncomputable section
namespace HMT.IV.LatticeTwistedNormalConformalBridge

open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeFiniteIrreducible
open LatticeHalfIntegerHeisenberg hiding halfMode
open LatticeHalfIntegerField LatticeHalfConformalModes LatticeGramDual
open LatticeTwistedCarrier LatticeTwistedTensorField LatticeTwistedNormalProduct
open LatticeTwistedOscillatorTensor
open scoped BigOperators

theorem creationTerm_eq_tensor (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) :
    creationTerm o i (twistedHalfHeisenbergField o j) (-2*m-4) a =
      (creationHalfTerm o i j m a).rTensor (FiniteSpace o) := by
  unfold creationTerm
  rw [show -2*m-4-2*(a:ℤ)+1 = ramifiedExponent (m+a) by
    unfold ramifiedExponent; omega]
  rw [twistedHalfHeisenbergField_mode]
  unfold creationHalfTerm LatticeTwistedCarrier.halfMode halfModeTensor
  rw [LinearMap.rTensor_comp, halfMode_negSucc]

theorem annihilationTerm_eq_tensor (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) :
    annihilationTerm o i (twistedHalfHeisenbergField o j) (-2*m-4) a =
      (annihilationHalfTerm o i j m a).rTensor (FiniteSpace o) := by
  unfold annihilationTerm
  rw [show -2*m-4+2*(a:ℤ)+3 = ramifiedExponent (m-a-1) by
    unfold ramifiedExponent; omega]
  rw [twistedHalfHeisenbergField_mode]
  unfold annihilationHalfTerm LatticeTwistedCarrier.halfMode halfModeTensor
  rw [LinearMap.rTensor_comp, halfMode_ofNat]

theorem normalCoefficient_eq_halfNormalMode_tensor (o : Fin 12)
    (i j : Fin (BasisSize o)) (m : ℤ) :
    normalCoefficient o i (twistedHalfHeisenbergField o j) (-2*m-4) =
      (halfNormalMode o i j m).rTensor (FiniteSpace o) := by
  apply LinearMap.ext
  intro w
  induction w using TensorProduct.induction_on with
  | zero => simp only [map_zero]
  | add v w hv hw => simp only [map_add, hv, hw]
  | tmul v t =>
    let L : HalfFock o →ₗ[ℂ] Carrier o :=
      (TensorProduct.mk ℂ (HalfFock o) (FiniteSpace o)).flip t
    have hc : (∑ᶠ a, creationHalfTerm o i j m a v) ⊗ₜ[ℂ] t =
        ∑ᶠ a, creationHalfTerm o i j m a v ⊗ₜ[ℂ] t :=
      L.toAddMonoidHom.map_finsum (creationHalfTerm_finite o i j m v)
    have ha : (∑ᶠ a, annihilationHalfTerm o i j m a v) ⊗ₜ[ℂ] t =
        ∑ᶠ a, annihilationHalfTerm o i j m a v ⊗ₜ[ℂ] t :=
      L.toAddMonoidHom.map_finsum (annihilationHalfTerm_finite o i j m v)
    rw [normalCoefficient_apply, LinearMap.rTensor_tmul, halfNormalMode_apply,
      TensorProduct.add_tmul, hc, ha]
    simp only [creationTerm_eq_tensor, annihilationTerm_eq_tensor,
      LinearMap.rTensor_tmul]

theorem normalField_coefficient_eq_halfNormalMode_tensor (o : Fin 12)
    (i j : Fin (BasisSize o)) (m : ℤ) :
    HVertexOperator.coeff (normalField o i (twistedHalfHeisenbergField o j))
        (-2*m-4) = (halfNormalMode o i j m).rTensor (FiniteSpace o) := by
  rw [normalField_coefficient, normalCoefficient_eq_halfNormalMode_tensor]

theorem gram_contracted_normalCoefficient_eq_quadraticMode_tensor (o : Fin 12)
    (m : ℤ) :
    (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j •
      normalCoefficient o i (twistedHalfHeisenbergField o j) (-2*m-4) =
      (quadraticMode o m).rTensor (FiniteSpace o) := by
  simp only [normalCoefficient_eq_halfNormalMode_tensor]
  change _ = (LinearMap.rTensorHom (FiniteSpace o))
    ((2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j • halfNormalMode o i j m)
  simp only [map_smul, map_sum]
  rfl

end HMT.IV.LatticeTwistedNormalConformalBridge
end

#print axioms HMT.IV.LatticeTwistedNormalConformalBridge.creationTerm_eq_tensor
#print axioms HMT.IV.LatticeTwistedNormalConformalBridge.annihilationTerm_eq_tensor
#print axioms HMT.IV.LatticeTwistedNormalConformalBridge.normalCoefficient_eq_halfNormalMode_tensor
#print axioms HMT.IV.LatticeTwistedNormalConformalBridge.normalField_coefficient_eq_halfNormalMode_tensor
#print axioms HMT.IV.LatticeTwistedNormalConformalBridge.gram_contracted_normalCoefficient_eq_quadraticMode_tensor
