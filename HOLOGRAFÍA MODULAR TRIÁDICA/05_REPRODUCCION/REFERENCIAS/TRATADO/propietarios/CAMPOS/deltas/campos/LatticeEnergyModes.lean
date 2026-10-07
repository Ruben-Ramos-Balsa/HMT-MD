import LatticeEnergyShift
import LatticeModeWeights

/-!
Energy commutators for the actual integer-indexed Heisenberg operators.
The proof uses the creation/annihilation action on the already constructed
monomial basis; no commutator with energy is an extra assumption.
-/

noncomputable section
namespace HMT.IV.LatticeEnergyModes

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeEnergyGrading HMT.IV.LatticeEnergyShift
open HMT.IV.LatticeModeWeights HMT.IV.LatticeHeisenbergModes
open HMT.IV.LatticeWeightShells
open scoped TensorProduct BigOperators

theorem carrierCreate_basis (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (a : Occupation o) (x : Lattice o) :
    onCarrier o (create o n i) (carrierBasis o (a,x)) =
      carrierBasis o (Finsupp.single (n,i) 1+a,x) := by
  simp only [carrierBasis, Basis.tensorProduct_apply, onCarrier_pure,
    create_monomial]

theorem carrierAnnihilate_basis (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (a : Occupation o) (x : Lattice o) :
    onCarrier o (annihilate o n i) (carrierBasis o (a,x)) =
      ∑ p ∈ a.support,
        ((a p : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0)) •
          carrierBasis o (a-Finsupp.single p 1,x) := by
  simp only [carrierBasis, Basis.tensorProduct_apply, onCarrier_pure,
    annihilate_monomial, Finsupp.sum, TensorProduct.sum_tmul,
    TensorProduct.smul_tmul']

theorem energy_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    (energy o).comp (onCarrier o (create o n i)) -
      (onCarrier o (create o n i)).comp (energy o) =
      (n+1 : ℂ) • onCarrier o (create o n i) := by
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    carrierCreate_basis, energy_basis, map_smul, smul_smul]
  rw [← sub_smul]
  congr 1
  simp only [totalWeight, create_monomial_weight, Nat.cast_add, Nat.cast_one]
  ring

theorem energy_annihilate (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    (energy o).comp (onCarrier o (annihilate o n i)) -
      (onCarrier o (annihilate o n i)).comp (energy o) =
      (-(n+1 : ℂ)) • onCarrier o (annihilate o n i) := by
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    carrierAnnihilate_basis, energy_basis, map_sum, map_smul, Finset.smul_sum,
    smul_smul]
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro p hp
  rw [← sub_smul]
  by_cases hz : (a p : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0) = 0
  · rw [hz]
    simp
  · have hw := annihilate_nonzero_term_weight o n i a p hz
    have hwC : (occupationWeight o (a-Finsupp.single p 1) : ℂ) + (n+1 : ℂ) =
        (occupationWeight o a : ℂ) := by exact_mod_cast hw
    congr 1
    simp only [totalWeight, Nat.cast_add]
    linear_combination
      ((a p : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0)) * hwC

theorem energy_hmode (o : Fin 12) (i : Fin (BasisSize o)) (n : ℤ) :
    (energy o).comp (hmode o i n) - (hmode o i n).comp (energy o) =
      (-(n : ℂ)) • hmode o i n := by
  cases n with
  | ofNat n =>
    cases n with
    | zero =>
      simp only [Int.ofNat_eq_coe, Nat.cast_zero, Int.cast_zero, neg_zero,
        zero_smul, hmode_zero]
      rw [energy_commutes_zeroMode, sub_self]
    | succ n =>
      rw [hmode_natSucc]
      simpa only [Int.ofNat_eq_coe, Int.cast_natCast, Nat.cast_add, Nat.cast_one,
        Int.cast_add, Int.cast_one]
        using energy_annihilate o n i
  | negSucc n =>
    rw [hmode_negSucc]
    simpa using energy_create o n i

theorem hmode_changes_energy (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℤ) (v : LatticeCarrier o) (d : ℂ)
    (hv : energy o v = d • v) :
    energy o (hmode o i n v) = (d-(n : ℂ)) • hmode o i n v := by
  have h := LinearMap.congr_fun (energy_hmode o i n) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    hv, map_smul] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h, sub_smul, neg_smul]
  abel

end HMT.IV.LatticeEnergyModes
end

#print axioms HMT.IV.LatticeEnergyModes.carrierCreate_basis
#print axioms HMT.IV.LatticeEnergyModes.carrierAnnihilate_basis
#print axioms HMT.IV.LatticeEnergyModes.energy_create
#print axioms HMT.IV.LatticeEnergyModes.energy_annihilate
#print axioms HMT.IV.LatticeEnergyModes.energy_hmode
#print axioms HMT.IV.LatticeEnergyModes.hmode_changes_energy
