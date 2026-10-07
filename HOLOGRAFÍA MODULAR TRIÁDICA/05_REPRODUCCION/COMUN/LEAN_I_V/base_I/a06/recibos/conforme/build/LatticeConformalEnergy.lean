import LatticeConformalEnergyParts
import LatticeConformalCoefficient

/-! The conformal zero mode equals the energy already constructed on the
same lattice carrier. All sums are finite on each vector, with the cutoff
obtained from its oscillator support. -/
noncomputable section
namespace HMT.IV.LatticeConformalEnergy
open LatticeCocycle LatticeOscillatorFock LatticeGramDual LatticeGramSymmetry
open LatticeConformalState LatticeConformalCoefficient LatticeNormalZeroMode
open LatticeConformalEnergyParts LatticeHeisenbergModes LatticeHeisenbergField
open LatticeFockMonomialParity LatticeChargeEnergy LatticeWeightShells
open LatticeEnergyGrading
open scoped BigOperators TensorProduct

theorem zero_mode_cutoff (o : Fin 12) (v : LatticeCarrier o) (N : ℕ)
    (hN : ∀ a ≥ N, ∀ i : Fin (BasisSize o), onCarrier o (annihilate o a i) v=0) :
    conformalMode o 0 v =
      (2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j • hmode o j 0 (hmode o i 0 v)) +
      ∑ a ∈ Finset.range N, ∑ i, ∑ j, gramInv o i j •
        onCarrier o (create o a i) (onCarrier o (annihilate o a j) v) := by
  classical
  rw [conformalMode_normal_sum_apply]
  simp only [neg_zero, zero_sub]
  simp only [normal_zero_mode_cutoff o _ _ v N hN, smul_add,
    Finset.smul_sum, Finset.sum_add_distrib]
  have rearrange (F : Fin (BasisSize o) → Fin (BasisSize o) → ℕ → LatticeCarrier o) :
      (∑ i, ∑ j, ∑ a ∈ Finset.range N, F i j a) =
        ∑ a ∈ Finset.range N, ∑ i, ∑ j, F i j a := by
    calc
      _ = ∑ i, ∑ a ∈ Finset.range N, ∑ j, F i j a := by
        apply Finset.sum_congr rfl
        intros
        rw [Finset.sum_comm]
      _ = _ := by rw [Finset.sum_comm]
  rw [rearrange, rearrange]
  have swap (a : ℕ) :
      (∑ i, ∑ j, gramInv o i j •
        onCarrier o (create o a j) (onCarrier o (annihilate o a i) v)) =
      ∑ i, ∑ j, gramInv o i j •
        onCarrier o (create o a i) (onCarrier o (annihilate o a j) v) := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    rw [gramInv_symmetric o j i]
  simp only [← Finset.smul_sum, swap]
  module

theorem carrier_oscillators_energy_cutoff (o : Fin 12) (a : Occupation o)
    (x : Lattice o) (N : ℕ) (hN : ∀ p ∈ a.support, p.1<N) :
    (∑ n ∈ Finset.range N, ∑ i, ∑ j, gramInv o i j •
      onCarrier o (create o n i) (onCarrier o (annihilate o n j)
        (carrierBasis o (a,x)))) =
      (occupationWeight o a : ℂ) • carrierBasis o (a,x) := by
  have h := congrArg (fun w : Fock o => w ⊗ₜ[ℂ] latticeBasisComplex o x)
    (oscillators_energy_cutoff o a N hN)
  simpa only [carrierBasis, Basis.tensorProduct_apply, onCarrier_pure,
    TensorProduct.smul_tmul', TensorProduct.sum_tmul] using h

theorem carrier_charge_quadratic (o : Fin 12) (a : Occupation o) (x : Lattice o) :
    (2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j •
      hmode o j 0 (hmode o i 0 (carrierBasis o (a,x)))) =
      (halfnormNat o x : ℂ) • carrierBasis o (a,x) := by
  simp only [hmode_zero, carrierZeroMode_basis, map_smul, smul_smul]
  simp_rw [← Finset.sum_smul]
  rw [smul_smul]
  have hsum : (∑ i, ∑ j, gramInv o i j *
      ((integerPair o (latticeBasis o i) x : ℂ) *
       (integerPair o (latticeBasis o j) x : ℂ))) =
      ∑ i, ∑ j, gramInv o i j * (integerPair o (latticeBasis o j) x : ℂ) *
        (integerPair o (latticeBasis o i) x : ℂ) := by
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intros
    ring
  rw [hsum, half_quadratic_pair_contraction]

theorem conformalMode_zero_eq_energy (o : Fin 12) : conformalMode o 0 = energy o := by
  classical
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  let N := a.support.sup (fun p => p.1) + 1
  have hN : ∀ p ∈ a.support, p.1<N := by
    intro p hp
    have h : p.1 ≤ a.support.sup (fun p => p.1) := Finset.le_sup hp
    dsimp [N]
    omega
  have hann : ∀ n ≥ N, ∀ i : Fin (BasisSize o),
      onCarrier o (annihilate o n i) (carrierBasis o (a,x))=0 := by
    intro n hn i
    simp only [carrierBasis, Basis.tensorProduct_apply, onCarrier_pure]
    rw [annihilate_monomial_cutoff o a N hN n hn i, TensorProduct.zero_tmul]
  rw [zero_mode_cutoff o _ N hann, carrier_oscillators_energy_cutoff o a x N hN,
    carrier_charge_quadratic, energy_basis]
  simp only [totalWeight, Nat.cast_add, add_smul]
  abel

end HMT.IV.LatticeConformalEnergy
end
#print axioms HMT.IV.LatticeConformalEnergy.zero_mode_cutoff
#print axioms HMT.IV.LatticeConformalEnergy.carrier_oscillators_energy_cutoff
#print axioms HMT.IV.LatticeConformalEnergy.carrier_charge_quadratic
#print axioms HMT.IV.LatticeConformalEnergy.conformalMode_zero_eq_energy
