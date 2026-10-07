import LatticeTwistedRawStateParity
import LatticeTwistedNormalArgumentScalar

/-! The actual source involution is the change of ramified argument t to -t.
Every oscillator derivative has odd ramified exponents, and the inherited
lattice charge field has the exact charge-negation rule. No branch parity is
assumed on the complete state-field map.
-/

noncomputable section
namespace HMT.IV.LatticeTwistedRawArgument
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeOscillatorWords LatticeParityCarrier
open LatticeTwistedCarrier LatticeTwistedKernelParity
open LatticeTwistedRawChargeField LatticeTwistedRawStateField
open LatticeTwistedRawStateParity LatticeTwistedNormalArgumentScalar

theorem negArgument_rawDescendantField (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) (k : ℤ) :
    HVertexOperator.coeff (rawDescendantField o (-x) w) k =
      ((-1:ℂ)^w.length * paritySign k) •
        HVertexOperator.coeff (rawDescendantField o x w) k := by
  induction w generalizing k with
  | nil =>
    simpa only [rawDescendantField, rawChargeField_coefficient, List.length_nil,
      pow_zero, one_mul] using rawChargeCoefficient_neg_charge o x k
  | cons m w ih =>
    apply LinearMap.ext
    intro v
    simp only [rawDescendantField, List.length_cons, LinearMap.smul_apply]
    rw [negArgument_derivativeNormalField_scalar o m.2 m.1 _ _ _ ih,
      pow_succ, mul_neg_one]

theorem theta_source_rawStateField (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    HVertexOperator.coeff (rawStateField o (carrierTheta o u)) k =
      paritySign k • HVertexOperator.coeff (rawStateField o u) k := by
  let L : LatticeCarrier o →ₗ[ℂ] Module.End ℂ (Carrier o) :=
    { toFun := fun z => HVertexOperator.coeff (rawStateField o (carrierTheta o z)) k
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply]
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply, RingHom.id_apply] }
  let R : LatticeCarrier o →ₗ[ℂ] Module.End ℂ (Carrier o) :=
    { toFun := fun z => paritySign k • HVertexOperator.coeff (rawStateField o z) k
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, smul_add]
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          RingHom.id_apply, smul_comm (paritySign k) c] }
  have hLR : L=R := by
    apply (carrierBasis o).ext
    rintro ⟨a,x⟩
    change HVertexOperator.coeff (rawStateField o (carrierTheta o (carrierBasis o (a,x)))) k =
      paritySign k • HVertexOperator.coeff (rawStateField o (carrierBasis o (a,x))) k
    rw [theta_carrierBasis_word, map_smul, HVertexOperator.coeff_smul,
      rawStateField_basis, rawStateField_basis]
    simp only [Pi.smul_apply, negArgument_rawDescendantField, smul_smul]
    have hs : ((-1:ℂ)^(wordForOccupation o a).length) *
        ((-1:ℂ)^(wordForOccupation o a).length) = 1 := by
      rw [← mul_pow]
      simp
    rw [← mul_assoc, hs, one_mul]
  exact LinearMap.congr_fun hLR u

theorem rawStateField_even_source_odd_zero (o : Fin 12) (u : LatticeCarrier o)
    (hu : carrierTheta o u = u) (k : ℤ) :
    HVertexOperator.coeff (rawStateField o u) (2*k+1) = 0 := by
  have h := theta_source_rawStateField o u (2*k+1)
  rw [hu, paritySign_odd] at h
  have hz : (2:ℂ) • HVertexOperator.coeff (rawStateField o u) (2*k+1) = 0 := by
    calc
      _ = (1:ℂ) • HVertexOperator.coeff (rawStateField o u) (2*k+1) -
          (-1:ℂ) • HVertexOperator.coeff (rawStateField o u) (2*k+1) := by module
      _ = 0 := by rw [one_smul]; exact sub_eq_zero.mpr h
  have h2 := congrArg (fun f : Module.End ℂ (Carrier o) => (2:ℂ)⁻¹ • f) hz
  simpa only [smul_smul, inv_mul_cancel₀ (by norm_num : (2:ℂ)≠0),
    one_smul, smul_zero] using h2

end HMT.IV.LatticeTwistedRawArgument
end

#print axioms HMT.IV.LatticeTwistedRawArgument.negArgument_rawDescendantField
#print axioms HMT.IV.LatticeTwistedRawArgument.theta_source_rawStateField
#print axioms HMT.IV.LatticeTwistedRawArgument.rawStateField_even_source_odd_zero
