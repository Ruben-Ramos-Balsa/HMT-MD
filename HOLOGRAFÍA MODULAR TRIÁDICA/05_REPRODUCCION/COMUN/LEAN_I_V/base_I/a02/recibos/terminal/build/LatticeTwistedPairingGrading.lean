import LatticeTwistedTensorPairing
import LatticeHalfGramWeight
import LatticeTwistedPositiveGrading

/-! The constructed tensor form respects the existing weight decomposition.
Its restriction to the actual positive fixed sector is nondegenerate; no
symmetry of the finite-ground pairing is used. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedPairingGrading
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeHalfWeightBasis LatticeTwistedCarrier LatticeTwistedLowWeights
open LatticeHalfFockPairing LatticeHalfGramTransport LatticeHalfGramWeight
open LatticeFactorialPairing LatticeTwistedTensorPairing LatticeTwistedGrading
open LatticeTwistedParity LatticeTwistedBasisParity LatticeTwistedPositiveSector
open LatticeTwistedPositiveGrading
open HMT.FockTransport.Symmetric

theorem tensorPairing_basis_off_weight (o : Fin 12) (p q : BasisIndex o)
    (h : twiceWeight o p.1 ≠ twiceWeight o q.1) :
    tensorPairing o (twistedBasis o p) (twistedBasis o q) = 0 := by
  simp only [twistedBasis, Basis.tensorProduct_apply', tensorPairing_pure,
    contravariantPairing_apply, factorialPairing_right]
  have hc := block_gamma_coefficient_off_weight o (gram o) halfScale p.1 q.1 h
  change _ * (_ * (monomialBasis o).repr
    (gamma (blockMap o (gram o) halfScale) (monomialBasis o p.1)) q.1) = 0
  rw [hc, mul_zero, mul_zero]

theorem evenProjector_pairing (o : Fin 12) (u v : Carrier o) :
    tensorPairing o (evenProjector o u) v =
      tensorPairing o u (evenProjector o v) := by
  classical
  have he : LinearMap.comp (tensorPairing o) (evenProjector o) =
      (tensorPairing o).compl₂ (evenProjector o) := by
    apply (twistedBasis o).ext
    intro p
    apply (twistedBasis o).ext
    intro q
    change tensorPairing o (evenProjector o (twistedBasis o p)) (twistedBasis o q) =
      tensorPairing o (twistedBasis o p) (evenProjector o (twistedBasis o q))
    rw [evenProjector_basis, evenProjector_basis]
    by_cases hp : occupationLength o p.1 % 2 = 1 <;>
      by_cases hq : occupationLength o q.1 % 2 = 1
    · rw [if_pos hp, if_pos hq]
    · rw [if_pos hp, if_neg hq, map_zero]
      apply tensorPairing_basis_off_weight
      intro hw
      have ha := twiceWeight_mod_two o p.1
      have hb := twiceWeight_mod_two o q.1
      omega
    · rw [if_neg hp, if_pos hq, map_zero, LinearMap.zero_apply]
      symm
      apply tensorPairing_basis_off_weight
      intro hw
      have ha := twiceWeight_mod_two o p.1
      have hb := twiceWeight_mod_two o q.1
      omega
    · simp only [if_neg hp, if_neg hq, map_zero, LinearMap.zero_apply]
  exact LinearMap.congr_fun (LinearMap.congr_fun he u) v

def positivePairing (o : Fin 12) : LinearMap.BilinForm ℂ (positiveSector o) :=
  (tensorPairing o).restrict (positiveSector o)

theorem positivePairing_nondegenerate (o : Fin 12) :
    (positivePairing o).Nondegenerate := by
  intro v hv
  apply Subtype.ext
  change v.val = 0
  apply tensorPairing_nondegenerate o
  intro w
  have h := hv (positiveProjection o w)
  change tensorPairing o v.val (evenProjector o w) = 0 at h
  rw [← evenProjector_pairing, evenProjector_fixed_identity o v.val v.property] at h
  exact h

theorem positivePairing_right_separating (o : Fin 12) (v : positiveSector o)
    (h : ∀ w, positivePairing o w v = 0) : v = 0 := by
  apply Subtype.ext
  change v.val = 0
  apply tensorPairing_right_separating o
  intro w
  have hw := h (positiveProjection o w)
  change tensorPairing o (evenProjector o w) v.val = 0 at hw
  rw [evenProjector_pairing, evenProjector_fixed_identity o v.val v.property] at hw
  exact hw

theorem tensorPairing_weight_basis_off (o : Fin 12) (d : ℕ)
    (v : weightSpace o d) (q : BasisIndex o) (hq : d ≠ twiceWeight o q.1) :
    tensorPairing o v.val (twistedBasis o q) = 0 := by
  have he : ((tensorPairing o).flip (twistedBasis o q)).comp (weightSpace o d).subtype = 0 := by
    apply (weightBasis o d).ext
    intro p
    change tensorPairing o ((weightBasis o d p : weightSpace o d) : Carrier o)
      (twistedBasis o q) = 0
    rw [weightBasis_coe]
    apply tensorPairing_basis_off_weight
    rw [p.property]
    exact hq
  exact LinearMap.congr_fun he v

def homogeneousPairing (o : Fin 12) (d : ℕ) : LinearMap.BilinForm ℂ (weightSpace o d) :=
  (tensorPairing o).restrict (weightSpace o d)

theorem homogeneousPairing_nondegenerate (o : Fin 12) (d : ℕ) :
    (homogeneousPairing o d).Nondegenerate := by
  classical
  intro v hv
  apply Subtype.ext
  change v.val = 0
  apply tensorPairing_nondegenerate o
  have he : tensorPairing o v.val = 0 := by
    apply (twistedBasis o).ext
    intro q
    change tensorPairing o v.val (twistedBasis o q) = 0
    by_cases hq : d = twiceWeight o q.1
    · exact hv ⟨twistedBasis o q, hq.symm ▸ basis_mem_weight o q⟩
    · exact tensorPairing_weight_basis_off o d v q hq
  intro w
  exact LinearMap.congr_fun he w

def homogeneousDuality (o : Fin 12) (d : ℕ) :
    weightSpace o d ≃ₗ[ℂ] Module.Dual ℂ (weightSpace o d) :=
  (homogeneousPairing o d).toDual (homogeneousPairing_nondegenerate o d)

theorem positiveProjection_eigen (o : Fin 12) (d : ℕ) (v : Carrier o)
    (hv : conformalMode o 0 v = (d:ℂ) • v) :
    positiveProjection o v ∈ positiveWeightSpace o d := by
  apply Module.End.mem_eigenspace_iff.mpr
  apply Subtype.ext
  change conformalMode o 0 (evenProjector o v) = (d:ℂ) • evenProjector o v
  simp only [evenProjector, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.id_apply, map_smul, map_add]
  rw [← liftedTheta_comm_conformal_apply, hv, map_smul]
  module

def positiveHomogeneousPairing (o : Fin 12) (d : ℕ) :
    LinearMap.BilinForm ℂ (positiveWeightSpace o d) :=
  (positivePairing o).restrict (positiveWeightSpace o d)

theorem positiveHomogeneousPairing_nondegenerate (o : Fin 12) (d : ℕ) :
    (positiveHomogeneousPairing o d).Nondegenerate := by
  intro v hv
  by_cases hd : d ≤ 1
  · have hz : positiveWeightSpace o d = ⊥ := by
      interval_cases d
      · exact positive_weight_zero o
      · exact positive_weight_one o
    apply Subtype.ext
    have hmem : v.val ∈ (⊥ : Submodule ℂ (positiveSector o)) := hz ▸ v.property
    simpa only [Submodule.mem_bot] using hmem
  · have hi : ((2*d-3:ℕ):ℂ)+3 = 2*(d:ℂ) := by
      have h : (2*d-3:ℕ)+3=2*d := by omega
      exact_mod_cast h
    have hc : (((2*d-3:ℕ):ℂ)+3)/2 = (d:ℂ) := by linear_combination hi/2
    have hvw : v.val.val ∈ weightSpace o (2*d-3) := by
      rw [weightSpace_eq_eigenspace, hc]
      exact (positiveWeightInclusion o d v).property
    let wv : weightSpace o (2*d-3) := ⟨v.val.val, hvw⟩
    have hzero : wv = 0 := homogeneousPairing_nondegenerate o (2*d-3) wv (by
      intro w
      have hw : conformalMode o 0 w.val = (d:ℂ) • w.val := by
        have he := (weightSpace_le_eigenspace o (2*d-3)) w.property
        rw [hc] at he
        exact Module.End.mem_eigenspace_iff.mp he
      have h := hv ⟨positiveProjection o w.val, positiveProjection_eigen o d w.val hw⟩
      change tensorPairing o v.val.val (evenProjector o w.val) = 0 at h
      rw [← evenProjector_pairing,
        evenProjector_fixed_identity o v.val.val v.val.property] at h
      exact h)
    apply Subtype.ext
    apply Subtype.ext
    change v.val.val = 0
    exact congrArg (fun w : weightSpace o (2*d-3) => w.val) hzero

def positiveHomogeneousDuality (o : Fin 12) (d : ℕ) :
    positiveWeightSpace o d ≃ₗ[ℂ] Module.Dual ℂ (positiveWeightSpace o d) := by
  exact LinearMap.BilinForm.toDual (K := ℂ) (V := positiveWeightSpace o d)
    (B := positiveHomogeneousPairing o d)
    (positiveHomogeneousPairing_nondegenerate o d)

end HMT.IV.LatticeTwistedPairingGrading
end
