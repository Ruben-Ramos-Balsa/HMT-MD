import LatticeTwistedCorrectedStateField
import LatticeTwistedRawStateParity
import LatticeTwistedPositiveSector

/-! Concrete corrected fields from the existing PBW field assignment.
Equivariance is transported through the actual correction exponential, giving
Laurent fields on the positive twisted sector for every even lattice state.
The coordinate remains t (z=t^2); descent and mixed locality are separate. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedStateField

open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeTwistedCarrier LatticeTwistedParity LatticeTwistedPositiveSector
open LatticeParityCarrier LatticeEvenVertexFields
open LatticeTwistedCorrection LatticeTwistedCorrectionPreservation
open LatticeTwistedCorrectedStateField LatticeTwistedRawStateField
open LatticeTwistedRawChargeField LatticeTwistedRawStateParity
open scoped BigOperators

def twistedStateField (o : Fin 12) : FieldAssignment o :=
  correctedAssignment o (rawStateField o)

theorem twistedStateField_coefficient (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    HVertexOperator.coeff (twistedStateField o u) k = ∑ᶠ d,
      HVertexOperator.coeff (rawStateField o (correctionExponentialCoefficient o d u))
        (k+2*(d:ℤ)) := rfl

theorem twistedStateField_pure_charge (o : Fin 12) (x : Lattice o) :
    twistedStateField o (carrierBasis o (0,x)) = rawChargeField o x := by
  rw [twistedStateField, correctedAssignment_pure_charge, rawStateField_pure_charge]

theorem twistedStateField_vacuum (o : Fin 12) :
    twistedStateField o (vacuum o) = rawChargeField o 0 := by
  rw [twistedStateField, correctedAssignment_vacuum, rawStateField_vacuum]

theorem twistedStateField_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (twistedStateField o (vacuum o)) k =
      if k=0 then (1 : Module.End ℂ (Carrier o)) else 0 := by
  rw [twistedStateField_vacuum, rawChargeField_zero_charge]

theorem twistedStateField_laurent_bound (o : Fin 12)
    (u : LatticeCarrier o) (v : Carrier o) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff (twistedStateField o u) k v = 0 :=
  correctedCoefficient_bounded o (rawStateField o) u v

theorem corrected_terms_apply_finite (o : Fin 12) (u : LatticeCarrier o)
    (k : ℤ) (v : Carrier o) :
    (Function.support (fun d =>
      HVertexOperator.coeff (rawStateField o (correctionExponentialCoefficient o d u))
        (k+2*(d:ℤ)) v)).Finite := by
  apply (stateTerm_finite o (rawStateField o) k u).subset
  intro d hd
  intro hz
  change stateTerm o (rawStateField o) k d u = 0 at hz
  apply hd
  change stateTerm o (rawStateField o) k d u v = 0
  rw [hz, LinearMap.zero_apply]

theorem twistedStateField_coefficient_apply (o : Fin 12) (u : LatticeCarrier o)
    (k : ℤ) (v : Carrier o) :
    HVertexOperator.coeff (twistedStateField o u) k v = ∑ᶠ d,
      HVertexOperator.coeff (rawStateField o (correctionExponentialCoefficient o d u))
        (k+2*(d:ℤ)) v := by
  let ev : Module.End ℂ (Carrier o) →+ Carrier o :=
    { toFun := fun f => f v, map_zero' := rfl, map_add' := fun _ _ => rfl }
  change ev (∑ᶠ d, stateTerm o (rawStateField o) k d u) = _
  exact ev.map_finsum (stateTerm_finite o (rawStateField o) k u)

theorem theta_twistedStateField_apply (o : Fin 12) (u : LatticeCarrier o)
    (k : ℤ) (v : Carrier o) :
    liftedTheta o (HVertexOperator.coeff (twistedStateField o u) k v) =
      HVertexOperator.coeff (twistedStateField o (carrierTheta o u)) k (liftedTheta o v) := by
  rw [twistedStateField_coefficient_apply]
  have hm := (liftedTheta o).toAddMonoidHom.map_finsum
    (corrected_terms_apply_finite o u k v)
  change liftedTheta o (∑ᶠ d,
      HVertexOperator.coeff (rawStateField o (correctionExponentialCoefficient o d u))
        (k+2*(d:ℤ)) v) = ∑ᶠ d,
      liftedTheta o (HVertexOperator.coeff
        (rawStateField o (correctionExponentialCoefficient o d u))
          (k+2*(d:ℤ)) v) at hm
  rw [hm, twistedStateField_coefficient_apply]
  apply finsum_congr
  intro d
  rw [theta_rawStateField_apply, correctionExponential_parity]

theorem theta_twistedStateField_intertwines (o : Fin 12)
    (u : LatticeCarrier o) (k : ℤ) :
    (liftedTheta o).comp (HVertexOperator.coeff (twistedStateField o u) k) =
      (HVertexOperator.coeff (twistedStateField o (carrierTheta o u)) k).comp
        (liftedTheta o) := by
  apply LinearMap.ext
  intro v
  exact theta_twistedStateField_apply o u k v

theorem twistedCoefficient_mem_positive (o : Fin 12) (u : LatticeCarrier o)
    (hu : u ∈ evenSpace o) (k : ℤ) (v : Carrier o) (hv : v ∈ positiveSector o) :
    HVertexOperator.coeff (twistedStateField o u) k v ∈ positiveSector o := by
  change liftedTheta o (HVertexOperator.coeff (twistedStateField o u) k v) = _
  rw [theta_twistedStateField_apply, (mem_evenSpace o u).1 hu,
    (mem_positiveSector o v).1 hv]

def positiveStateCoefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    Module.End ℂ (positiveSector o) :=
  (HVertexOperator.coeff (twistedStateField o u.val) k).restrict
    (fun v hv => twistedCoefficient_mem_positive o u.val u.property k v hv)

theorem positiveStateCoefficient_coe (o : Fin 12) (u : evenSpace o) (k : ℤ)
    (v : positiveSector o) :
    (positiveStateCoefficient o u k v).val =
      HVertexOperator.coeff (twistedStateField o u.val) k v.val := rfl

theorem positiveStateCoefficient_bounded (o : Fin 12) (u : evenSpace o)
    (v : positiveSector o) :
    ∃ b : ℤ, ∀ k < b, positiveStateCoefficient o u k v = 0 := by
  obtain ⟨b,hb⟩ := twistedStateField_laurent_bound o u.val v.val
  refine ⟨b, fun k hk => ?_⟩
  apply Subtype.ext
  exact hb k hk

def positiveStateField (o : Fin 12) (u : evenSpace o) :
    VertexOperator ℂ (positiveSector o) :=
  VertexOperator.of_coeff (positiveStateCoefficient o u)
    (positiveStateCoefficient_bounded o u)

theorem positiveStateField_coefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (positiveStateField o u) k = positiveStateCoefficient o u k := rfl

def positiveStateAssignment (o : Fin 12) :
    evenSpace o →ₗ[ℂ] VertexOperator ℂ (positiveSector o) where
  toFun := positiveStateField o
  map_add' u w := by
    apply HVertexOperator.coeff_inj
    funext k
    apply LinearMap.ext
    intro v
    apply Subtype.ext
    change HVertexOperator.coeff (twistedStateField o (u.val+w.val)) k v.val = _
    simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
    rfl
  map_smul' c u := by
    apply HVertexOperator.coeff_inj
    funext k
    apply LinearMap.ext
    intro v
    apply Subtype.ext
    change HVertexOperator.coeff (twistedStateField o (c • u.val)) k v.val = _
    simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply, LinearMap.smul_apply]
    rfl

theorem positiveStateField_intertwines_inclusion (o : Fin 12) (u : evenSpace o)
    (k : ℤ) :
    (positiveSector o).subtype.comp (HVertexOperator.coeff (positiveStateAssignment o u) k) =
      (HVertexOperator.coeff (twistedStateField o u.val) k).comp (positiveSector o).subtype := by
  ext v
  rfl

theorem positiveStateField_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (positiveStateAssignment o (evenVacuum o)) k =
      if k=0 then (1 : Module.End ℂ (positiveSector o)) else 0 := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  change HVertexOperator.coeff (twistedStateField o (vacuum o)) k v.val = _
  rw [twistedStateField_vacuum_coefficient]
  split_ifs <;> rfl

end HMT.IV.LatticeTwistedStateField
end
