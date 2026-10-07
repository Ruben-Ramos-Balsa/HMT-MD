import LatticeTwistedStateField
import LatticeTwistedStateDescent
import LatticeTwistedEvenChargeStates

/-! Restriction and descent commute for the corrected field on every even
lattice state. This gives the explicit even-to-twisted-positive block in z.
On exponential generators it is exactly the previously normalized charge
field. The construction does not assert the module Jacobi identities. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedPositiveStateDescent
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeEvenVertexFields LatticeTwistedPositiveSector
open LatticeTwistedStateField LatticeTwistedStateDescent
open LatticeTwistedRawChargeField LatticeTwistedChargeNormalization
open LatticeTwistedEvenChargeStates LatticeTwistedKernelParity

def positiveDescendedCoefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    Module.End ℂ (positiveSector o) := positiveStateCoefficient o u (2*k)

theorem positiveDescendedCoefficient_bounded (o : Fin 12) (u : evenSpace o)
    (v : positiveSector o) :
    ∃ b : ℤ, ∀ k < b, positiveDescendedCoefficient o u k v = 0 := by
  obtain ⟨b,hb⟩ := positiveStateCoefficient_bounded o u v
  exact ⟨b/2, fun k hk => hb (2*k) (by omega)⟩

def positiveDescendedField (o : Fin 12) (u : evenSpace o) :
    VertexOperator ℂ (positiveSector o) :=
  VertexOperator.of_coeff (positiveDescendedCoefficient o u)
    (positiveDescendedCoefficient_bounded o u)

theorem positiveDescendedField_coefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (positiveDescendedField o u) k = positiveStateCoefficient o u (2*k) := rfl

def positiveDescendedAssignment (o : Fin 12) :
    evenSpace o →ₗ[ℂ] VertexOperator ℂ (positiveSector o) where
  toFun := positiveDescendedField o
  map_add' u w := by
    apply HVertexOperator.coeff_inj
    funext k
    change HVertexOperator.coeff (positiveStateAssignment o (u+w)) (2*k) =
      HVertexOperator.coeff (positiveDescendedField o u + positiveDescendedField o w) k
    simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply,
      positiveDescendedField_coefficient, positiveStateField_coefficient]
    rfl
  map_smul' c u := by
    apply HVertexOperator.coeff_inj
    funext k
    change HVertexOperator.coeff (positiveStateAssignment o (c • u)) (2*k) =
      HVertexOperator.coeff (c • positiveDescendedField o u) k
    simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
      positiveDescendedField_coefficient, positiveStateField_coefficient]
    rfl

theorem positiveDescent_intertwines_inclusion (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    (positiveSector o).subtype.comp (HVertexOperator.coeff (positiveDescendedAssignment o u) k) =
      (HVertexOperator.coeff (descendedAssignment o u) k).comp (positiveSector o).subtype := by
  apply LinearMap.ext
  intro v
  rfl

theorem positiveState_odd_coefficients_zero (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (positiveStateAssignment o u) (2*k+1) = 0 := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  change HVertexOperator.coeff (twistedStateField o u.val) (2*k+1) v.val = 0
  rw [twistedStateField, descendedField_odd_discarded_zero, LinearMap.zero_apply]

theorem positiveDescent_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (positiveDescendedAssignment o (evenVacuum o)) k =
      if k=0 then (1 : Module.End ℂ (positiveSector o)) else 0 := by
  change HVertexOperator.coeff (positiveStateAssignment o (evenVacuum o)) (2*k) = _
  rw [positiveStateField_vacuum_coefficient]
  simp only [show (2*k=0) ↔ k=0 by omega]

theorem positiveDescent_evenExponentialState (o : Fin 12) (x : Lattice o) :
    positiveDescendedAssignment o (evenExponentialState o x) = chargeField o x := by
  apply HVertexOperator.coeff_inj
  funext k
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  change HVertexOperator.coeff (twistedStateField o (evenExponentialState o x).val)
    (2*k) v.val = (HVertexOperator.coeff (chargeField o x) k v).val
  have h := LinearMap.congr_fun (chargeField_inclusion_even_raw o x k) v
  change (HVertexOperator.coeff (chargeField o x) k v).val =
    rawChargeCoefficient o x (2*k) v.val at h
  rw [h, evenExponentialState_coe, map_smul, map_add,
    exponentialState_eq_carrierBasis, exponentialState_eq_carrierBasis,
    twistedStateField_pure_charge, twistedStateField_pure_charge]
  simp only [HVertexOperator.coeff_smul, HVertexOperator.coeff_add, Pi.smul_apply,
    Pi.add_apply, LinearMap.smul_apply, LinearMap.add_apply, rawChargeField_coefficient,
    rawChargeCoefficient_neg_charge, paritySign_even, one_smul]
  module

end HMT.IV.LatticeTwistedPositiveStateDescent
end

#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescendedCoefficient
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescendedCoefficient_bounded
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescendedField
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescendedField_coefficient
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescendedAssignment
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescent_intertwines_inclusion
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveState_odd_coefficients_zero
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescent_vacuum_coefficient
#print axioms HMT.IV.LatticeTwistedPositiveStateDescent.positiveDescent_evenExponentialState
