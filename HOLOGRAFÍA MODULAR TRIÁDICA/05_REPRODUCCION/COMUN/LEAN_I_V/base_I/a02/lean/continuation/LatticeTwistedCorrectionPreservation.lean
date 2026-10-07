import LatticeTwistedCorrection
import LatticeEvenVertexFields

/-! The correction uses the actual lattice modes. It fixes pure charge states
and preserves the existing parity decomposition at every coefficient, hence
restricts to the even lattice space. These assertions also hold for its full
formal exponential, with the pointwise finite bound proved in its owner. -/

noncomputable section
namespace HMT.IV.LatticeTwistedCorrectionPreservation
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeHeisenbergModes LatticeEnergyModes LatticeTwistedCorrection
open LatticeParityCarrier LatticeStateFieldParity LatticeEvenVertexFields
open PowerSeries
open scoped BigOperators

theorem nonnegative_modes_commute (o : Fin 12) (i j : Fin (BasisSize o))
    (m n : ℕ) (v : LatticeCarrier o) :
    hmode o i (m:ℤ) (hmode o j (n:ℤ) v) =
      hmode o j (n:ℤ) (hmode o i (m:ℤ) v) := by
  have h := heisenberg_relation_apply o i j (m:ℤ) (n:ℤ) v
  have hz : (if (m:ℤ)+(n:ℤ)=0 then ((m:ℤ):ℂ)*gram o i j else 0) = 0 := by
    split_ifs with hm
    · have : m=0 := by omega
      simp [this]
    · rfl
  rw [hz, zero_smul, sub_eq_zero] at h
  exact h

theorem positive_mode_pure_charge (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (x : Lattice o) :
    hmode o i ((n+1:ℕ):ℤ) (carrierBasis o (0,x)) = 0 := by
  rw [hmode_castSucc, carrierAnnihilate_basis]
  simp

theorem mode_pair_pure_charge (o : Fin 12) (i j : Fin (BasisSize o))
    (m n : ℕ) (h : 0 < m+n) (x : Lattice o) :
    (hmode o i (m:ℤ) * hmode o j (n:ℤ)) (carrierBasis o (0,x)) = 0 := by
  change hmode o i (m:ℤ) (hmode o j (n:ℤ) (carrierBasis o (0,x))) = 0
  cases n with
  | succ n => rw [positive_mode_pure_charge, map_zero]
  | zero =>
    rw [nonnegative_modes_commute]
    cases m with
    | zero => omega
    | succ m => rw [positive_mode_pure_charge, map_zero]

theorem correctionCoefficient_pure_charge (o : Fin 12) (d : ℕ) (x : Lattice o) :
    correctionCoefficient o d (carrierBasis o (0,x)) = 0 := by
  by_cases hd : d=0
  · rw [hd, correctionCoefficient_zero, LinearMap.zero_apply]
  · simp only [correctionCoefficient, LinearMap.sum_apply, LinearMap.smul_apply]
    apply Finset.sum_eq_zero
    intro p hp
    have hpos : 0 < p.1+p.2 := by
      rw [Finset.mem_antidiagonal.mp hp]
      omega
    simp only [mode_pair_pure_charge o _ _ p.1 p.2 hpos x, smul_zero,
      Finset.sum_const_zero]

theorem correctionPositivePower_pure_charge (o : Fin 12) (k d : ℕ) (x : Lattice o) :
    coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o ^ (k+1))
      (carrierBasis o (0,x)) = 0 := by
  rw [pow_succ, coeff_mul, LinearMap.sum_apply]
  apply Finset.sum_eq_zero
  intro p _
  change (coeff (Module.End ℂ (LatticeCarrier o)) p.1 (correctionSeries o ^ k))
    ((coeff (Module.End ℂ (LatticeCarrier o)) p.2 (correctionSeries o))
      (carrierBasis o (0,x))) = 0
  rw [correctionSeries_coefficient, correctionCoefficient_pure_charge, map_zero]

theorem correctionExponential_pure_charge (o : Fin 12) (d : ℕ) (x : Lattice o) :
    correctionExponentialCoefficient o d (carrierBasis o (0,x)) =
      if d=0 then carrierBasis o (0,x) else 0 := by
  rw [correctionExponentialCoefficient, LinearMap.sum_apply,
    Finset.sum_eq_single 0]
  · by_cases hd : d=0 <;> simp [coeff_one, hd]
  · intro k _ hk
    rw [LinearMap.smul_apply]
    obtain ⟨j,rfl⟩ := Nat.exists_eq_succ_of_ne_zero hk
    rw [correctionPositivePower_pure_charge, smul_zero]
  · simp

theorem correctionCoefficient_parity (o : Fin 12) (d : ℕ) (v : LatticeCarrier o) :
    carrierTheta o (correctionCoefficient o d v) =
      correctionCoefficient o d (carrierTheta o v) := by
  simp only [correctionCoefficient, LinearMap.sum_apply, LinearMap.smul_apply,
    Module.End.mul_apply, map_sum, map_smul, theta_hmode, map_neg, neg_neg]

theorem correctionPower_parity (o : Fin 12) (k d : ℕ) (v : LatticeCarrier o) :
    carrierTheta o ((coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o ^ k)) v) =
      (coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o ^ k)) (carrierTheta o v) := by
  induction k generalizing d v with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs <;> simp
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    simp only [LinearMap.sum_apply, Module.End.mul_apply, map_sum,
      correctionSeries_coefficient, ih, correctionCoefficient_parity]

theorem correctionExponential_parity (o : Fin 12) (d : ℕ) (v : LatticeCarrier o) :
    carrierTheta o (correctionExponentialCoefficient o d v) =
      correctionExponentialCoefficient o d (carrierTheta o v) := by
  simp only [correctionExponentialCoefficient, LinearMap.sum_apply,
    LinearMap.smul_apply, map_sum, map_smul, correctionPower_parity]

theorem correctionExponential_mem_parity (o : Fin 12) (d : ℕ) (s : ℂ)
    (v : LatticeCarrier o) (hv : v ∈ paritySpace o s) :
    correctionExponentialCoefficient o d v ∈ paritySpace o s := by
  apply (mem_paritySpace o s _).2
  rw [correctionExponential_parity, (mem_paritySpace o s v).1 hv, map_smul]

def evenCorrectionCoefficient (o : Fin 12) (d : ℕ) : Module.End ℂ (evenSpace o) :=
  (correctionExponentialCoefficient o d).restrict
    (fun v hv => correctionExponential_mem_parity o d 1 v hv)

theorem evenCorrection_coefficient (o : Fin 12) (d : ℕ) (v : evenSpace o) :
    (evenCorrectionCoefficient o d v).val = correctionExponentialCoefficient o d v.val := rfl

theorem evenCorrection_polynomial_on_state (o : Fin 12) (v : evenSpace o) :
    ∃ N : ℕ, ∀ d ≥ N, evenCorrectionCoefficient o d v = 0 := by
  obtain ⟨N,hN⟩ := correctionExponential_polynomial_on_state o v.val
  refine ⟨N, fun d hd => ?_⟩
  apply Subtype.ext
  exact hN d hd

end HMT.IV.LatticeTwistedCorrectionPreservation
end

#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.nonnegative_modes_commute
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.positive_mode_pure_charge
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.mode_pair_pure_charge
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.correctionCoefficient_pure_charge
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.correctionPositivePower_pure_charge
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.correctionExponential_pure_charge
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.correctionCoefficient_parity
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.correctionPower_parity
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.correctionExponential_parity
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.correctionExponential_mem_parity
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.evenCorrectionCoefficient
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.evenCorrection_coefficient
#print axioms HMT.IV.LatticeTwistedCorrectionPreservation.evenCorrection_polynomial_on_state
