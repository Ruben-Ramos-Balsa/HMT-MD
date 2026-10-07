import LatticeTwistedRawArgument
import LatticeTwistedCorrectedStateField

/-! The corrected full field has the source involution as ramified argument
parity. Hence every even source state has only even powers of t and descends
to an actual Laurent field in z=t². This holds for all algebraic states, not
only pure lattice charges or finitely selected conformal weights. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedStateDescent
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeParityCarrier LatticeEvenVertexFields LatticeTwistedKernelParity
open LatticeTwistedRawStateField LatticeTwistedRawArgument
open LatticeTwistedCorrection LatticeTwistedCorrectionPreservation
open LatticeTwistedCorrectedStateField

theorem paritySign_even_translate (k : ℤ) (d : ℕ) :
    paritySign (k+2*(d:ℤ)) = paritySign k := by
  unfold paritySign
  rw [show (k+2*(d:ℤ))%2=k%2 by omega]

theorem theta_source_correctedAssignment (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    HVertexOperator.coeff (correctedAssignment o (rawStateField o) (carrierTheta o u)) k =
      paritySign k • HVertexOperator.coeff (correctedAssignment o (rawStateField o) u) k := by
  rw [correctedAssignment_coefficient, correctedAssignment_coefficient]
  simp_rw [← correctionExponential_parity, theta_source_rawStateField,
    paritySign_even_translate]
  have hf : (Function.support (fun d : ℕ =>
      HVertexOperator.coeff (rawStateField o (correctionExponentialCoefficient o d u))
        (k+2*(d:ℤ)))).Finite := stateTerm_finite o (rawStateField o) k u
  exact (smul_finsum' (paritySign k) hf).symm

theorem correctedAssignment_even_source_odd_zero (o : Fin 12) (u : LatticeCarrier o)
    (hu : carrierTheta o u=u) (k : ℤ) :
    HVertexOperator.coeff (correctedAssignment o (rawStateField o) u) (2*k+1) = 0 := by
  have h := theta_source_correctedAssignment o u (2*k+1)
  rw [hu, paritySign_odd] at h
  let T := HVertexOperator.coeff (correctedAssignment o (rawStateField o) u) (2*k+1)
  have hz : (2:ℂ) • T = 0 := by
    calc
      _ = (1:ℂ) • T - (-1:ℂ) • T := by module
      _ = 0 := by rw [one_smul]; exact sub_eq_zero.mpr h
  have h2 := congrArg (fun f : Module.End ℂ (Carrier o) => (2:ℂ)⁻¹ • f) hz
  simpa only [smul_smul, inv_mul_cancel₀ (by norm_num : (2:ℂ)≠0),
    one_smul, smul_zero] using h2

def descendedCoefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    Module.End ℂ (Carrier o) :=
  HVertexOperator.coeff (correctedAssignment o (rawStateField o) u.val) (2*k)

theorem descendedCoefficient_bounded (o : Fin 12) (u : evenSpace o) (v : Carrier o) :
    ∃ b : ℤ, ∀ k < b, descendedCoefficient o u k v = 0 := by
  obtain ⟨b,hb⟩ := field_has_bound o (correctedAssignment o (rawStateField o) u.val) v
  refine ⟨b/2, fun k hk => hb (2*k) (by omega)⟩

def descendedField (o : Fin 12) (u : evenSpace o) : VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (descendedCoefficient o u) (descendedCoefficient_bounded o u)

theorem descendedField_coefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (descendedField o u) k =
      HVertexOperator.coeff (correctedAssignment o (rawStateField o) u.val) (2*k) := rfl

theorem descendedField_odd_discarded_zero (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (correctedAssignment o (rawStateField o) u.val) (2*k+1) = 0 :=
  correctedAssignment_even_source_odd_zero o u.val ((mem_evenSpace o u.val).1 u.property) k

def descendedAssignment (o : Fin 12) :
    evenSpace o →ₗ[ℂ] VertexOperator ℂ (Carrier o) where
  toFun := descendedField o
  map_add' u v := by
    apply HVertexOperator.coeff_inj
    funext k
    simp only [descendedField_coefficient, Submodule.coe_add, map_add,
      HVertexOperator.coeff_add, Pi.add_apply]
  map_smul' c u := by
    apply HVertexOperator.coeff_inj
    funext k
    simp only [descendedField_coefficient, Submodule.coe_smul, map_smul,
      HVertexOperator.coeff_smul, Pi.smul_apply, RingHom.id_apply]

theorem descendedAssignment_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (descendedAssignment o (evenVacuum o)) k =
      if k=0 then (1 : Module.End ℂ (Carrier o)) else 0 := by
  change HVertexOperator.coeff (correctedAssignment o (rawStateField o) (vacuum o)) (2*k) = _
  rw [correctedAssignment_vacuum, rawStateField_vacuum_coefficient]
  simp only [show (2*k=0) ↔ k=0 by omega]

end HMT.IV.LatticeTwistedStateDescent
end

#print axioms HMT.IV.LatticeTwistedStateDescent.paritySign_even_translate
#print axioms HMT.IV.LatticeTwistedStateDescent.theta_source_correctedAssignment
#print axioms HMT.IV.LatticeTwistedStateDescent.correctedAssignment_even_source_odd_zero
#print axioms HMT.IV.LatticeTwistedStateDescent.descendedCoefficient
#print axioms HMT.IV.LatticeTwistedStateDescent.descendedCoefficient_bounded
#print axioms HMT.IV.LatticeTwistedStateDescent.descendedField
#print axioms HMT.IV.LatticeTwistedStateDescent.descendedField_coefficient
#print axioms HMT.IV.LatticeTwistedStateDescent.descendedField_odd_discarded_zero
#print axioms HMT.IV.LatticeTwistedStateDescent.descendedAssignment
#print axioms HMT.IV.LatticeTwistedStateDescent.descendedAssignment_vacuum_coefficient
