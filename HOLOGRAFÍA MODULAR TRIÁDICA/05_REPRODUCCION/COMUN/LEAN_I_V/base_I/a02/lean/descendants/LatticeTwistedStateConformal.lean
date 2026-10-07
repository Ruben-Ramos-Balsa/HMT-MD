import LatticeTwistedStateField
import LatticeTwistedRawConformal
import LatticeTwistedCorrectionConformal

/-! The corrected field of the inherited conformal state has exactly the
already proved half-integer Virasoro modes on the actual twisted carrier.
The rank/16 shift comes from evaluating the correction exponential on that
state, not from an assumed conformal-field identity or a target value. -/
noncomputable section
namespace HMT.IV.LatticeTwistedStateConformal
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeConformalState (conformalState)
open LatticeTwistedStateField LatticeTwistedRawStateField LatticeTwistedRawConformal
open LatticeTwistedCorrection LatticeTwistedCorrectionConformal
open LatticeHalfConformalModes LatticeHalfConformalCentralizer LatticeHalfConformalVacuum
open LatticeTwistedOscillatorTensor LatticeFiniteIrreducible

theorem twistedStateField_conformalState_correction (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (twistedStateField o (conformalState o)) k =
      HVertexOperator.coeff (rawStateField o (conformalState o)) k +
      if k = -4 then ((BasisSize o : ℂ)/16) • (1 : Module.End ℂ (Carrier o)) else 0 := by
  classical
  rw [twistedStateField_coefficient]
  let f (d : ℕ) : Module.End ℂ (Carrier o) :=
    HVertexOperator.coeff (rawStateField o (correctionExponentialCoefficient o d
      (conformalState o))) (k+2*(d:ℤ))
  change (∑ᶠ d, f d) = _
  have hz (d : ℕ) (h0 : d ≠ 0) (h2 : d ≠ 2) : f d = 0 := by
    dsimp [f]
    rw [correctionExponential_conformalState, if_neg h0, if_neg h2, zero_add]
    ext v
    simp [HVertexOperator.coeff]
  have hs : Function.support f ⊆ ({0,2} : Finset ℕ) := by
    intro d hd
    simp only [Finset.mem_coe, Finset.mem_insert, Finset.mem_singleton]
    by_contra h
    push_neg at h
    exact hd (hz d h.1 h.2)
  rw [finsum_eq_sum_of_support_subset f hs, Finset.sum_insert (by decide), Finset.sum_singleton]
  have h0 : f 0 = HVertexOperator.coeff (rawStateField o (conformalState o)) k := by
    have hc : correctionExponentialCoefficient o 0 (conformalState o) = conformalState o := by
      rw [correctionExponential_conformalState, if_pos rfl, if_neg (by decide), add_zero]
    dsimp [f]
    rw [hc]
    simp only [Nat.cast_zero, mul_zero, add_zero]
  have h2 : f 2 = if k = -4 then
      ((BasisSize o : ℂ)/16) • (1 : Module.End ℂ (Carrier o)) else 0 := by
    have hc : correctionExponentialCoefficient o 2 (conformalState o) =
        ((BasisSize o : ℂ)/16) • vacuum o := by
      simp [correctionExponential_conformalState]
    dsimp [f]
    rw [hc, map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
      rawStateField_vacuum_coefficient]
    by_cases hk : k = -4
    · subst k
      norm_num
    · rw [if_neg hk, if_neg (by omega), smul_zero]
  rw [h0, h2]

theorem twistedStateField_conformalState_coefficient (o : Fin 12) (m : ℤ) :
    HVertexOperator.coeff (twistedStateField o (conformalState o)) (-2*m-4) =
      conformalMode o m := by
  rw [twistedStateField_conformalState_correction,
    rawStateField_conformalState_coefficient]
  unfold conformalMode conformalModeTensor shiftedModes shiftedQuadraticMode
  rw [LinearMap.rTensor_add]
  by_cases hm : m = 0
  · subst m
    simp only [mul_zero, zero_sub, if_pos rfl, LinearMap.rTensor_smul,
      LinearMap.rTensor_id]
    rfl
  · rw [if_neg hm, if_neg (by omega), LinearMap.rTensor_zero]

end HMT.IV.LatticeTwistedStateConformal
end

#print axioms HMT.IV.LatticeTwistedStateConformal.twistedStateField_conformalState_correction
#print axioms HMT.IV.LatticeTwistedStateConformal.twistedStateField_conformalState_coefficient
