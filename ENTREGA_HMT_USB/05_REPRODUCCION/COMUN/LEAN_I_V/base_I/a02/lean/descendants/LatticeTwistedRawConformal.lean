import LatticeTwistedWordCoherence
import LatticeTwistedNormalVacuum
import LatticeTwistedNormalConformalBridge
import LatticeConformalState

/-! The uncorrected W-map of the actual inherited conformal state is the
Gram-contracted half-normal field. Its coefficients are the transported
unshifted quadratic modes. The Delta correction and scalar vacuum shift
remain separate; neither is inserted into this raw field by definition. -/
noncomputable section
namespace HMT.IV.LatticeTwistedRawConformal
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeGramDual LatticeHalfConformalModes LatticeFiniteIrreducible
open LatticeTwistedNormalDerivative LatticeTwistedRawStateField
open LatticeTwistedWordCoherence LatticeTwistedNormalVacuum
open LatticeTwistedTensorField LatticeTwistedNormalConformalBridge
open LatticeConformalState (conformalState)
open scoped BigOperators

theorem derivativeField_zero (o : Fin 12) (i : Fin (BasisSize o)) :
    derivativeField o i 0 = twistedHalfHeisenbergField o i := by
  apply HVertexOperator.coeff_inj
  funext k
  simp only [derivativeField_coefficient, derivativeCoefficient,
    Nat.cast_zero, mul_zero, add_zero, dividedFactor_zero, one_smul,
    twistedHalfHeisenbergField_coefficient]

theorem derivativeNormalField_zero_order (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) :
    derivativeNormalField o i 0 B = LatticeTwistedNormalProduct.normalField o i B := by
  apply HVertexOperator.coeff_inj
  funext k
  rw [derivativeNormalField_coefficient, normalCoefficient_zero,
    LatticeTwistedNormalProduct.normalField_coefficient]

theorem rawStateField_conformalState (o : Fin 12) :
    rawStateField o (conformalState o) = (2:ℂ)⁻¹ • ∑ i, ∑ j,
      gramInv o i j • LatticeTwistedNormalProduct.normalField o i
        (twistedHalfHeisenbergField o j) := by
  have h (i j : Fin (BasisSize o)) :
      rawStateField o (onCarrier o (create o 0 i)
        (onCarrier o (create o 0 j) (vacuum o))) =
      LatticeTwistedNormalProduct.normalField o i (twistedHalfHeisenbergField o j) := by
    rw [rawStateField_create, rawStateField_create, rawStateField_vacuum,
      derivativeNormalField_zero_charge, derivativeField_zero,
      derivativeNormalField_zero_order]
  simp only [conformalState, map_smul, map_sum, h]

theorem rawStateField_conformalState_coefficient (o : Fin 12) (m : ℤ) :
    HVertexOperator.coeff (rawStateField o (conformalState o)) (-2*m-4) =
      (quadraticMode o m).rTensor (FiniteSpace o) := by
  let R : VertexOperator ℂ (Carrier o) →ₗ[ℂ] Module.End ℂ (Carrier o) :=
    { toFun := fun B => HVertexOperator.coeff B (-2*m-4)
      map_add' := fun B C => by simp only [HVertexOperator.coeff_add, Pi.add_apply]
      map_smul' := fun c B => by
        simp only [HVertexOperator.coeff_smul, Pi.smul_apply, RingHom.id_apply] }
  change R (rawStateField o (conformalState o)) = _
  rw [rawStateField_conformalState]
  simp only [map_smul, map_sum]
  change (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j •
    LatticeTwistedNormalProduct.normalCoefficient o i (twistedHalfHeisenbergField o j)
      (-2*m-4) = _
  exact gram_contracted_normalCoefficient_eq_quadraticMode_tensor o m

end HMT.IV.LatticeTwistedRawConformal
end

#print axioms HMT.IV.LatticeTwistedRawConformal.derivativeField_zero
#print axioms HMT.IV.LatticeTwistedRawConformal.derivativeNormalField_zero_order
#print axioms HMT.IV.LatticeTwistedRawConformal.rawStateField_conformalState
#print axioms HMT.IV.LatticeTwistedRawConformal.rawStateField_conformalState_coefficient
