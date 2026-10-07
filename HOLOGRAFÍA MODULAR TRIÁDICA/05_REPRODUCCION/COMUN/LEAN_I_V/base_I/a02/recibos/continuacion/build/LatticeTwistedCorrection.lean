import LatticeEnergyModes
import LatticeGramDual
import Mathlib.RingTheory.PowerSeries.Binomial
import Mathlib.RingTheory.PowerSeries.WellKnown

/-! The descendant-correction operator acts on the existing untwisted lattice
carrier. Its coefficients use nonnegative Heisenberg modes and the inverse of
the inherited Gram matrix. Every positive coefficient lowers the actual energy;
therefore its formal exponential is polynomial on each algebraic input state.
The closed rational coefficients below are the Euler-degree coefficients for
the FLM correction kernel. Identification with its bivariate logarithm and the
twisted Jacobi identity are not asserted by this module. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedCorrection
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeEnergyGrading LatticeEnergyModes LatticeHeisenbergModes LatticeGramDual
open PowerSeries
open scoped BigOperators

def correctionScalar (m n : ℕ) : ℂ :=
  ((Ring.choose (-1/2 : ℚ) m * Ring.choose (-1/2 : ℚ) n /
    (2 * (m+n : ℚ)) : ℚ) : ℂ)

theorem correctionScalar_symm (m n : ℕ) :
    correctionScalar m n = correctionScalar n m := by
  simp only [correctionScalar, mul_comm, add_comm]

theorem correctionScalar_zero_zero : correctionScalar 0 0 = 0 := by
  simp [correctionScalar]

def correctionCoefficient (o : Fin 12) (d : ℕ) :
    Module.End ℂ (LatticeCarrier o) :=
  ∑ p ∈ Finset.antidiagonal d, correctionScalar p.1 p.2 •
    ∑ i, ∑ j, gramInv o i j • (hmode o i (p.1 : ℤ) * hmode o j (p.2 : ℤ))

def correctionSeries (o : Fin 12) : PowerSeries (Module.End ℂ (LatticeCarrier o)) :=
  PowerSeries.mk (correctionCoefficient o)

theorem correctionSeries_coefficient (o : Fin 12) (d : ℕ) :
    coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o) =
      correctionCoefficient o d := coeff_mk _ _

theorem correctionCoefficient_zero (o : Fin 12) : correctionCoefficient o 0 = 0 := by
  simp [correctionCoefficient, correctionScalar_zero_zero]

def LowersEnergy (o : Fin 12) (d : ℕ) (T : Module.End ℂ (LatticeCarrier o)) : Prop :=
  ∀ v, energy o (T v) = T (energy o v) - (d:ℂ) • T v

theorem lowersEnergy_zero (o : Fin 12) (d : ℕ) : LowersEnergy o d 0 := by
  intro v
  simp

theorem lowersEnergy_one (o : Fin 12) : LowersEnergy o 0 1 := by
  intro v
  simp

theorem lowersEnergy_smul (o : Fin 12) (d : ℕ) (c : ℂ)
    (T : Module.End ℂ (LatticeCarrier o)) (hT : LowersEnergy o d T) :
    LowersEnergy o d (c • T) := by
  intro v
  simp only [LinearMap.smul_apply, map_smul]
  rw [hT v]
  simp only [smul_sub, smul_smul]
  congr 1
  rw [mul_comm]

theorem lowersEnergy_sum (o : Fin 12) (d : ℕ) {ι : Type*}
    (s : Finset ι) (T : ι → Module.End ℂ (LatticeCarrier o))
    (hT : ∀ i ∈ s, LowersEnergy o d (T i)) : LowersEnergy o d (∑ i ∈ s, T i) := by
  intro v
  simp only [LinearMap.sum_apply, map_sum, Finset.smul_sum]
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun i hi => hT i hi v

theorem lowersEnergy_mul (o : Fin 12) (d e : ℕ)
    (T S : Module.End ℂ (LatticeCarrier o))
    (hT : LowersEnergy o d T) (hS : LowersEnergy o e S) :
    LowersEnergy o (d+e) (T*S) := by
  intro v
  change energy o (T (S v)) = T (S (energy o v)) -
    ((d+e : ℕ) : ℂ) • T (S v)
  rw [hT, hS, map_sub, map_smul, Nat.cast_add, add_smul]
  abel

theorem nonnegativeMode_lowersEnergy (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    LowersEnergy o n (hmode o i (n:ℤ)) := by
  intro v
  have h := LinearMap.congr_fun (energy_hmode o i (n:ℤ)) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    Int.cast_natCast, neg_smul] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h]
  abel

theorem correctionCoefficient_lowersEnergy (o : Fin 12) (d : ℕ) :
    LowersEnergy o d (correctionCoefficient o d) := by
  apply lowersEnergy_sum
  intro p hp
  rw [← Finset.mem_antidiagonal.mp hp]
  apply lowersEnergy_smul
  apply lowersEnergy_sum
  intro i _
  apply lowersEnergy_sum
  intro j _
  apply lowersEnergy_smul
  exact lowersEnergy_mul o p.1 p.2 _ _
    (nonnegativeMode_lowersEnergy o i p.1) (nonnegativeMode_lowersEnergy o j p.2)

theorem correctionPower_lowersEnergy (o : Fin 12) (k d : ℕ) :
    LowersEnergy o d (coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o ^ k)) := by
  induction k generalizing d with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs with h
    · subst d
      exact lowersEnergy_one o
    · exact lowersEnergy_zero o d
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply lowersEnergy_sum
    intro p hp
    rw [← Finset.mem_antidiagonal.mp hp]
    rw [correctionSeries_coefficient]
    exact lowersEnergy_mul o p.1 p.2 _ _ (ih p.1)
      (correctionCoefficient_lowersEnergy o p.2)

theorem correctionPower_vanishes_below_order (o : Fin 12) (k d : ℕ) (h : d < k) :
    coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o ^ k) = 0 := by
  induction k generalizing d with
  | zero => omega
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply Finset.sum_eq_zero
    intro p hp
    have hd := Finset.mem_antidiagonal.mp hp
    by_cases hz : p.2=0
    · rw [hz, correctionSeries_coefficient, correctionCoefficient_zero, mul_zero]
    · rw [ih p.1 (by omega), zero_mul]

def correctionExponentialCoefficient (o : Fin 12) (d : ℕ) :
    Module.End ℂ (LatticeCarrier o) :=
  ∑ k ∈ Finset.range (d+1), coeff ℂ k (PowerSeries.exp ℂ) •
    coeff (Module.End ℂ (LatticeCarrier o)) d (correctionSeries o ^ k)

theorem correctionExponential_lowersEnergy (o : Fin 12) (d : ℕ) :
    LowersEnergy o d (correctionExponentialCoefficient o d) := by
  apply lowersEnergy_sum
  intro k _
  exact lowersEnergy_smul o d _ _ (correctionPower_lowersEnergy o k d)

theorem correctionExponential_zero (o : Fin 12) : correctionExponentialCoefficient o 0 = 1 := by
  simp [correctionExponentialCoefficient]

theorem negative_energy_eigenvector_zero (o : Fin 12) (v : LatticeCarrier o) (m d : ℕ)
    (hmd : m < d) (hv : energy o v = ((m:ℂ)-(d:ℂ)) • v) : v=0 := by
  apply (carrierBasis o).repr.injective
  ext a
  simp only [map_zero, Finsupp.zero_apply]
  by_contra hn
  have h := congrArg (fun w => (carrierBasis o).repr w a) hv
  dsimp only at h
  rw [energy_coefficient] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have hw : (totalWeight o a : ℂ) = (m:ℂ)-(d:ℂ) := mul_right_cancel₀ hn h
  have hc : ((totalWeight o a + d : ℕ) : ℂ) = (m:ℂ) := by
    rw [Nat.cast_add, hw]
    ring
  have hnat : totalWeight o a + d = m := by exact_mod_cast hc
  omega

theorem correctionExponential_basis_cutoff (o : Fin 12) (p : Occupation o × Lattice o)
    (d : ℕ) (hd : totalWeight o p < d) :
    correctionExponentialCoefficient o d (carrierBasis o p) = 0 := by
  apply negative_energy_eigenvector_zero o _ (totalWeight o p) d hd
  rw [correctionExponential_lowersEnergy, energy_basis, map_smul, sub_smul]

theorem correctionExponential_polynomial_on_state (o : Fin 12) (v : LatticeCarrier o) :
    ∃ N : ℕ, ∀ d ≥ N, correctionExponentialCoefficient o d v = 0 := by
  classical
  let S := ((carrierBasis o).repr v).support
  refine ⟨S.sup (totalWeight o) + 1, ?_⟩
  intro d hd
  conv_lhs => rw [← (carrierBasis o).linearCombination_repr v]
  rw [Finsupp.linearCombination_apply, Finsupp.sum, map_sum]
  apply Finset.sum_eq_zero
  intro p hp
  rw [map_smul]
  have hw : totalWeight o p ≤ S.sup (totalWeight o) := Finset.le_sup hp
  rw [correctionExponential_basis_cutoff o p d (by omega), smul_zero]

end HMT.IV.LatticeTwistedCorrection
end

#print axioms HMT.IV.LatticeTwistedCorrection.correctionScalar
#print axioms HMT.IV.LatticeTwistedCorrection.correctionScalar_symm
#print axioms HMT.IV.LatticeTwistedCorrection.correctionScalar_zero_zero
#print axioms HMT.IV.LatticeTwistedCorrection.correctionCoefficient
#print axioms HMT.IV.LatticeTwistedCorrection.correctionSeries
#print axioms HMT.IV.LatticeTwistedCorrection.correctionSeries_coefficient
#print axioms HMT.IV.LatticeTwistedCorrection.correctionCoefficient_zero
#print axioms HMT.IV.LatticeTwistedCorrection.LowersEnergy
#print axioms HMT.IV.LatticeTwistedCorrection.lowersEnergy_zero
#print axioms HMT.IV.LatticeTwistedCorrection.lowersEnergy_one
#print axioms HMT.IV.LatticeTwistedCorrection.lowersEnergy_smul
#print axioms HMT.IV.LatticeTwistedCorrection.lowersEnergy_sum
#print axioms HMT.IV.LatticeTwistedCorrection.lowersEnergy_mul
#print axioms HMT.IV.LatticeTwistedCorrection.nonnegativeMode_lowersEnergy
#print axioms HMT.IV.LatticeTwistedCorrection.correctionCoefficient_lowersEnergy
#print axioms HMT.IV.LatticeTwistedCorrection.correctionPower_lowersEnergy
#print axioms HMT.IV.LatticeTwistedCorrection.correctionPower_vanishes_below_order
#print axioms HMT.IV.LatticeTwistedCorrection.correctionExponentialCoefficient
#print axioms HMT.IV.LatticeTwistedCorrection.correctionExponential_lowersEnergy
#print axioms HMT.IV.LatticeTwistedCorrection.correctionExponential_zero
#print axioms HMT.IV.LatticeTwistedCorrection.negative_energy_eigenvector_zero
#print axioms HMT.IV.LatticeTwistedCorrection.correctionExponential_basis_cutoff
#print axioms HMT.IV.LatticeTwistedCorrection.correctionExponential_polynomial_on_state
