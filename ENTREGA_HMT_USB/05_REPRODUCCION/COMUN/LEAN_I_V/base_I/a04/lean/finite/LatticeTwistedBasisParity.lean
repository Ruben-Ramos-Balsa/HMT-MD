import LatticeTwistedLowWeights
import LatticeTwistedParity

/-! The lifted involution is diagonal on the actual monomial tensor basis.
Its positive part has odd half-oscillator occupation and hence integral
conformal weights at least two. These properties follow from the existing
operators; no truncation or twisted vertex multiplication is postulated. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedBasisParity
open TensorProduct
open LatticeFockMonomialParity LatticeHalfWeightBasis
open LatticeTwistedCarrier LatticeTwistedParity LatticeTwistedLowWeights

theorem liftedTheta_basis (o : Fin 12) (p : BasisIndex o) :
    liftedTheta o (twistedBasis o p) =
      (-((-1 : ℂ) ^ occupationLength o p.1)) • twistedBasis o p := by
  simp only [twistedBasis, Basis.tensorProduct_apply', liftedTheta_tmul,
    fockTheta_monomial, TensorProduct.smul_tmul', neg_smul]

theorem twiceWeight_mod_two (o : Fin 12) (a : Occupation o) :
    twiceWeight o a % 2 = occupationLength o a % 2 := by
  simp [twiceWeight, occupationLength, Finsupp.sum, Finset.sum_nat_mod,
    Nat.add_mod, Nat.mul_mod]

theorem liftedTheta_coefficient (o : Fin 12) (v : Carrier o) (p : BasisIndex o) :
    (twistedBasis o).repr (liftedTheta o v) p =
      (-((-1 : ℂ) ^ occupationLength o p.1)) * (twistedBasis o).repr v p := by
  classical
  have h : ((twistedBasis o).coord p).comp (liftedTheta o) =
      (-((-1 : ℂ) ^ occupationLength o p.1)) • (twistedBasis o).coord p := by
    apply (twistedBasis o).ext
    intro q
    simp only [LinearMap.comp_apply, liftedTheta_basis, map_smul,
      LinearMap.smul_apply, Basis.coord_apply, Basis.repr_self,
      Finsupp.single_apply, smul_eq_mul]
    split_ifs with hq
    · subst q
      rfl
    · simp
  exact LinearMap.congr_fun h v

theorem positive_basis_iff_odd (o : Fin 12) (p : BasisIndex o) :
    liftedTheta o (twistedBasis o p) = twistedBasis o p ↔
      occupationLength o p.1 % 2 = 1 := by
  rw [liftedTheta_basis]
  constructor
  · intro h
    have hs : -((-1 : ℂ) ^ occupationLength o p.1) = 1 :=
      smul_left_injective ℂ ((twistedBasis o).ne_zero p) (h.trans (one_smul ℂ _).symm)
    have hp : (-1 : ℂ) ^ occupationLength o p.1 = -1 := neg_eq_iff_eq_neg.mp hs
    exact Nat.odd_iff.mp ((neg_one_pow_eq_neg_one_iff_odd (by norm_num)).mp hp)
  · intro h
    rw [neg_one_pow_eq_pow_mod_two, h]
    simp

theorem evenProjector_basis (o : Fin 12) (p : BasisIndex o) :
    evenProjector o (twistedBasis o p) =
      if occupationLength o p.1 % 2 = 1 then twistedBasis o p else 0 := by
  change (2 : ℂ)⁻¹ • (twistedBasis o p + liftedTheta o (twistedBasis o p)) = _
  rw [liftedTheta_basis, neg_one_pow_eq_pow_mod_two]
  by_cases hp : occupationLength o p.1 % 2 = 1
  · rw [if_pos hp, hp]
    simp only [pow_one, neg_neg, one_smul]
    module
  · have hz : occupationLength o p.1 % 2 = 0 := by omega
    rw [if_neg hp, hz]
    simp

theorem positive_support_odd (o : Fin 12) (v : Carrier o)
    (hv : liftedTheta o v = v) (p : BasisIndex o)
    (hp : (twistedBasis o).repr v p ≠ 0) :
    occupationLength o p.1 % 2 = 1 := by
  have h := congrArg (fun w : Carrier o => (twistedBasis o).repr w p) hv
  dsimp only at h
  rw [liftedTheta_coefficient] at h
  have hs : -((-1 : ℂ) ^ occupationLength o p.1) = 1 :=
    mul_right_cancel₀ hp (h.trans (one_mul _).symm)
  have hn : (-1 : ℂ) ^ occupationLength o p.1 = -1 := neg_eq_iff_eq_neg.mp hs
  exact Nat.odd_iff.mp ((neg_one_pow_eq_neg_one_iff_odd (by norm_num)).mp hn)

theorem odd_basis_integer_weight (o : Fin 12) (p : BasisIndex o)
    (hp : occupationLength o p.1 % 2 = 1) :
    ∃ d : ℕ, 2 ≤ d ∧ (((twiceWeight o p.1 : ℂ)+3)/2) = (d : ℂ) := by
  have hw : twiceWeight o p.1 % 2 = 1 := (twiceWeight_mod_two o p.1).trans hp
  refine ⟨(twiceWeight o p.1 + 3)/2, by omega, ?_⟩
  have hn : twiceWeight o p.1 + 3 = 2*((twiceWeight o p.1+3)/2) := by omega
  have hc : (twiceWeight o p.1 : ℂ)+3 = 2*(((twiceWeight o p.1+3)/2 : ℕ) : ℂ) := by
    exact_mod_cast hn
  linear_combination hc / 2

theorem positive_basis_integer_weight (o : Fin 12) (p : BasisIndex o)
    (hp : liftedTheta o (twistedBasis o p) = twistedBasis o p) :
    ∃ d : ℕ, 2 ≤ d ∧ conformalMode o 0 (twistedBasis o p) =
      (d : ℂ) • twistedBasis o p := by
  obtain ⟨d, hd, hw⟩ := odd_basis_integer_weight o p ((positive_basis_iff_odd o p).mp hp)
  exact ⟨d, hd, (conformal_basis_weight o p).trans (congrArg (fun c : ℂ =>
    c • twistedBasis o p) hw)⟩

theorem positive_eigenvalue_integer_ge_two (o : Fin 12) (v : Carrier o)
    (hv0 : v ≠ 0) (hv : liftedTheta o v = v) (w : ℂ)
    (hw : conformalMode o 0 v = w • v) :
    ∃ d : ℕ, 2 ≤ d ∧ w = (d : ℂ) := by
  classical
  have hr : (twistedBasis o).repr v ≠ 0 := by
    intro h
    apply hv0
    exact (twistedBasis o).repr.injective (h.trans (map_zero _).symm)
  obtain ⟨p, hp⟩ := Finsupp.support_nonempty_iff.mpr hr
  have hp0 : (twistedBasis o).repr v p ≠ 0 := Finsupp.mem_support_iff.mp hp
  obtain ⟨d, hd, hweight⟩ := odd_basis_integer_weight o p (positive_support_odd o v hv p hp0)
  have h := congrArg (fun x : Carrier o => (twistedBasis o).repr x p) hw
  dsimp only at h
  rw [conformal_coefficient] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have hsame := mul_right_cancel₀ hp0 h
  exact ⟨d, hd, hsame.symm.trans hweight⟩

end HMT.IV.LatticeTwistedBasisParity
end

#print axioms HMT.IV.LatticeTwistedBasisParity.liftedTheta_basis
#print axioms HMT.IV.LatticeTwistedBasisParity.twiceWeight_mod_two
#print axioms HMT.IV.LatticeTwistedBasisParity.liftedTheta_coefficient
#print axioms HMT.IV.LatticeTwistedBasisParity.positive_basis_iff_odd
#print axioms HMT.IV.LatticeTwistedBasisParity.evenProjector_basis
#print axioms HMT.IV.LatticeTwistedBasisParity.positive_support_odd
#print axioms HMT.IV.LatticeTwistedBasisParity.odd_basis_integer_weight
#print axioms HMT.IV.LatticeTwistedBasisParity.positive_basis_integer_weight
#print axioms HMT.IV.LatticeTwistedBasisParity.positive_eigenvalue_integer_ge_two
