import LatticeTwistedRawStateField
import LatticeTwistedNormalParity
import LatticeStateFieldParity

/-! Equivariance of the constructed W-map on the actual whole lattice carrier.
The sign is the number of oscillator letters; charge reversal uses the proved
finite lattice action. This is an operator equality, not equality of dimensions.
-/

noncomputable section
namespace HMT.IV.LatticeTwistedRawStateParity
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeOscillatorWords LatticeParityCarrier LatticeStateFieldMap
open LatticeStateFieldParity LatticeDescendantFields
open LatticeTwistedCarrier LatticeTwistedParity
open LatticeTwistedRawChargeField LatticeTwistedRawStateField
open LatticeTwistedNormalParity

theorem theta_rawDescendantField (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) (k : ℤ) (v : Carrier o) :
    liftedTheta o (HVertexOperator.coeff (rawDescendantField o x w) k v) =
      (-1:ℂ)^w.length •
        HVertexOperator.coeff (rawDescendantField o (-x) w) k (liftedTheta o v) := by
  induction w generalizing k v with
  | nil =>
    have h := LinearMap.congr_fun (theta_rawChargeCoefficient o x k) v
    simpa only [rawDescendantField, rawChargeField_coefficient, List.length_nil,
      pow_zero, one_smul, LinearMap.comp_apply] using h
  | cons m w ih =>
    simp only [rawDescendantField, List.length_cons]
    rw [theta_derivativeNormalField o m.2 m.1 _ _ _ ih, pow_succ, mul_neg_one]

theorem theta_carrierBasis_word (o : Fin 12) (a : Occupation o) (x : Lattice o) :
    carrierTheta o (carrierBasis o (a,x)) =
      (-1:ℂ)^(wordForOccupation o a).length • carrierBasis o (a,-x) := by
  rw [← carrierBasis_wordForOccupation o a x, ← descendantState_eq_word,
    theta_descendantState, descendantState_eq_word, carrierBasis_wordForOccupation]

theorem theta_rawStateField_apply (o : Fin 12) (u : LatticeCarrier o)
    (k : ℤ) (v : Carrier o) :
    liftedTheta o (HVertexOperator.coeff (rawStateField o u) k v) =
      HVertexOperator.coeff (rawStateField o (carrierTheta o u)) k (liftedTheta o v) := by
  let L : LatticeCarrier o →ₗ[ℂ] Carrier o :=
    { toFun := fun z => liftedTheta o (HVertexOperator.coeff (rawStateField o z) k v)
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          LinearMap.smul_apply, RingHom.id_apply] }
  let R : LatticeCarrier o →ₗ[ℂ] Carrier o :=
    { toFun := fun z => HVertexOperator.coeff (rawStateField o (carrierTheta o z))
          k (liftedTheta o v)
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          LinearMap.smul_apply, RingHom.id_apply] }
  have hLR : L=R := by
    apply (carrierBasis o).ext
    rintro ⟨a,x⟩
    change liftedTheta o (HVertexOperator.coeff (rawStateField o (carrierBasis o (a,x))) k v) =
      HVertexOperator.coeff (rawStateField o (carrierTheta o (carrierBasis o (a,x))))
        k (liftedTheta o v)
    rw [theta_carrierBasis_word, map_smul, rawStateField_basis, rawStateField_basis]
    simp only [HVertexOperator.coeff_smul, Pi.smul_apply, LinearMap.smul_apply]
    exact theta_rawDescendantField o x (wordForOccupation o a) k v
  exact LinearMap.congr_fun hLR u

theorem theta_rawStateField_intertwines (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    (liftedTheta o).comp (HVertexOperator.coeff (rawStateField o u) k) =
      (HVertexOperator.coeff (rawStateField o (carrierTheta o u)) k).comp (liftedTheta o) := by
  apply LinearMap.ext
  intro v
  exact theta_rawStateField_apply o u k v

end HMT.IV.LatticeTwistedRawStateParity
end

#print axioms HMT.IV.LatticeTwistedRawStateParity.theta_rawDescendantField
#print axioms HMT.IV.LatticeTwistedRawStateParity.theta_carrierBasis_word
#print axioms HMT.IV.LatticeTwistedRawStateParity.theta_rawStateField_apply
#print axioms HMT.IV.LatticeTwistedRawStateParity.theta_rawStateField_intertwines
