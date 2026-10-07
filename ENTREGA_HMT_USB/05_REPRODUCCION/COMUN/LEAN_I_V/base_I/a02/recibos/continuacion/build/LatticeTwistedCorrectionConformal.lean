import LatticeTwistedCorrectionPreservation
import LatticeConformalCentralCoefficient

/-! The correction on the actual conformal state is evaluated, not calibrated:
the inverse Gram contraction gives rank/16. This is the same scalar previously
forced by the half-mode Virasoro relations. No mixed-product identity is assumed. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedCorrectionConformal
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeHeisenbergModes LatticeGramDual LatticeConformalState
open LatticeConformalCentralCoefficient LatticeTwistedCorrection
open LatticeTwistedCorrectionPreservation
open PowerSeries
open scoped BigOperators

theorem correctionScalar_one_one : correctionScalar 1 1 = (1/16 : ℂ) := by
  norm_num [correctionScalar, Ring.choose_one_right]

theorem mode_pair_conformalState (o : Fin 12) (i j : Fin (BasisSize o)) (m n : ℕ) :
    (hmode o i (m:ℤ) * hmode o j (n:ℤ)) (conformalState o) =
      if m=1 ∧ n=1 then gram o i j • vacuum o else 0 := by
  simp only [Module.End.mul_apply, nonnegative_mode_conformalState]
  by_cases hn : n=1
  · rw [if_pos hn, nonnegative_mode_one_creator]
    by_cases hm : m=1 <;> simp [hm, hn]
  · simp [hn]

theorem gram_trace_vacuum (o : Fin 12) :
    (∑ i, ∑ j, gramInv o i j • (gram o i j • vacuum o)) =
      (BasisSize o : ℂ) • vacuum o := by
  classical
  simp only [smul_smul]
  have inner (i : Fin (BasisSize o)) :
      (∑ j, (gramInv o i j * gram o i j) • vacuum o) = vacuum o := by
    rw [← Finset.sum_smul]
    simp_rw [gram_symmetric o i]
    rw [gramInv_pairing, if_pos rfl, one_smul]
  simp_rw [inner]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    Nat.cast_smul_eq_nsmul]

theorem correctionCoefficient_conformalState (o : Fin 12) (d : ℕ) :
    correctionCoefficient o d (conformalState o) =
      if d=2 then ((BasisSize o : ℂ)/16) • vacuum o else 0 := by
  classical
  simp only [correctionCoefficient, LinearMap.sum_apply, LinearMap.smul_apply,
    mode_pair_conformalState]
  by_cases hd : d=2
  · subst d
    rw [if_pos rfl, Finset.sum_eq_single (1,1)]
    · simp only [and_self, if_pos rfl, if_true, correctionScalar_one_one]
      rw [gram_trace_vacuum, smul_smul]
      congr 1
      ring
    · intro p _ hp
      have h : ¬(p.1=1 ∧ p.2=1) := by
        rintro ⟨h1,h2⟩
        exact hp (Prod.ext h1 h2)
      simp only [if_neg h, smul_zero, Finset.sum_const_zero]
    · simp
  · rw [if_neg hd]
    apply Finset.sum_eq_zero
    intro p hp
    have h : ¬(p.1=1 ∧ p.2=1) := by
      have hs := Finset.mem_antidiagonal.mp hp
      omega
    simp only [if_neg h, smul_zero, Finset.sum_const_zero]

theorem correctionCoefficient_vacuum (o : Fin 12) (d : ℕ) :
    correctionCoefficient o d (vacuum o) = 0 := by
  rw [← vacuum_is_empty_monomial]
  exact correctionCoefficient_pure_charge o d 0

theorem correctionPower_ge_two_conformalState (o : Fin 12) (k d : ℕ) :
    coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o ^ (k+2))
      (conformalState o) = 0 := by
  induction k generalizing d with
  | zero =>
    rw [show 0+2=1+1 by rfl, pow_succ, pow_one, coeff_mul, LinearMap.sum_apply]
    apply Finset.sum_eq_zero
    intro p _
    simp only [Module.End.mul_apply, correctionSeries_coefficient,
      correctionCoefficient_conformalState]
    split_ifs <;> simp only [map_smul, correctionCoefficient_vacuum, smul_zero, map_zero]
  | succ k ih =>
    rw [show (k+1)+2=(k+2)+1 by omega, pow_succ', coeff_mul, LinearMap.sum_apply]
    apply Finset.sum_eq_zero
    intro p _
    change (coeff (Module.End ℂ (LatticeCarrier o)) p.1 (correctionSeries o))
      ((coeff (Module.End ℂ (LatticeCarrier o)) p.2 (correctionSeries o ^ (k+2)))
        (conformalState o)) = 0
    rw [ih, map_zero]

theorem correctionExponential_conformalState (o : Fin 12) (d : ℕ) :
    correctionExponentialCoefficient o d (conformalState o) =
      (if d=0 then conformalState o else 0) +
      (if d=2 then ((BasisSize o : ℂ)/16) • vacuum o else 0) := by
  classical
  cases d with
  | zero => simp [correctionExponential_zero]
  | succ d =>
    rw [correctionExponentialCoefficient, LinearMap.sum_apply,
      Finset.sum_range_succ']
    have hz : (coeff ℂ 0 (PowerSeries.exp ℂ) •
        coeff (Module.End ℂ (LatticeCarrier o)) (d+1) (correctionSeries o ^ 0))
        (conformalState o) = 0 := by simp
    rw [hz, add_zero, Finset.sum_eq_single 0]
    · simp only [zero_add, pow_one, coeff_exp, Nat.factorial_one, Nat.cast_one,
        inv_one, one_smul, correctionSeries_coefficient, correctionCoefficient_conformalState]
      simp [correctionCoefficient_conformalState]
    · intro k _ hk
      obtain ⟨j,rfl⟩ := Nat.exists_eq_succ_of_ne_zero hk
      rw [LinearMap.smul_apply, show (j+1)+1=j+2 by omega,
        correctionPower_ge_two_conformalState, smul_zero]
    · simp

end HMT.IV.LatticeTwistedCorrectionConformal
end

#print axioms HMT.IV.LatticeTwistedCorrectionConformal.correctionScalar_one_one
#print axioms HMT.IV.LatticeTwistedCorrectionConformal.mode_pair_conformalState
#print axioms HMT.IV.LatticeTwistedCorrectionConformal.gram_trace_vacuum
#print axioms HMT.IV.LatticeTwistedCorrectionConformal.correctionCoefficient_conformalState
#print axioms HMT.IV.LatticeTwistedCorrectionConformal.correctionCoefficient_vacuum
#print axioms HMT.IV.LatticeTwistedCorrectionConformal.correctionPower_ge_two_conformalState
#print axioms HMT.IV.LatticeTwistedCorrectionConformal.correctionExponential_conformalState
