import LatticeTwistedExponentialKernel
import LatticeHalfCreationEnergy

/-! The actual normally ordered kernel coefficients have the conformal
shift dictated by their ramified Laurent exponent. Creation raises degree,
annihilation lowers it, and the finite lattice action occupies only the second
tensor factor. The existing ground shift cancels in the commutator. The
integer Laurent shift s remains explicit; no field normalization is assumed. -/

noncomputable section
namespace HMT.IV.LatticeTwistedKernelEnergy
open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeHalfIntegerHeisenberg LatticeHalfConformalModes
open LatticeHalfConformalVacuum LatticeHalfConformalCentralizer LatticeHalfWeightBasis
open LatticeFiniteIrreducible LatticeFiniteGroundState
open LatticeTwistedCarrier LatticeTwistedOscillatorTensor LatticeTwistedLowWeights
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeHalfAnnihilationEnergy LatticeHalfCreationEnergy
open LatticeTwistedExponentialKernel

theorem two_shifted_zero (o : Fin 12) (v : HalfFock o) :
    (2:ℂ) • shiftedModes o 0 v = halfDegree o v + (3:ℂ) • v := by
  have hr : BasisSize o=24 := NeighborRank.witt_marked_integer_rank o
  change (2:ℂ) • (quadraticMode o 0 v + ((BasisSize o:ℂ)/16) • v) =
    (2:ℂ) • quadraticMode o 0 v + (3:ℂ) • v
  rw [hr]
  norm_num
  module

theorem two_conformalMode_tmul (o : Fin 12) (v : HalfFock o) (t : FiniteSpace o) :
    (2:ℂ) • conformalMode o 0 (v ⊗ₜ[ℂ] t) =
      halfDegree o v ⊗ₜ[ℂ] t + (3:ℂ) • (v ⊗ₜ[ℂ] t) := by
  change (2:ℂ) • conformalModeTensor (FiniteSpace o) o 0 (v ⊗ₜ[ℂ] t) = _
  rw [conformalModeTensor_tmul]
  calc
    (2:ℂ) • (shiftedModes o 0 v ⊗ₜ[ℂ] t) =
        ((2:ℂ) • shiftedModes o 0 v) ⊗ₜ[ℂ] t := (TensorProduct.smul_tmul' _ _ _).symm
    _ = (halfDegree o v + (3:ℂ) • v) ⊗ₜ[ℂ] t := by rw [two_shifted_zero]
    _ = _ := by rw [TensorProduct.add_tmul, TensorProduct.smul_tmul']

theorem halfDegree_creation_annihilation (o : Fin 12) (x : Lattice o)
    (n j : ℕ) (a : Occupation o) :
    halfDegree o (halfCreationExponentialMode o x n
      (exponentialCoefficient o x j (monomialBasis o a))) =
      ((twiceWeight o a:ℂ)+(n:ℂ)-(j:ℂ)) •
        halfCreationExponentialMode o x n
          (exponentialCoefficient o x j (monomialBasis o a)) := by
  have hc := LinearMap.congr_fun (halfCreationExponentialMode_commutator o x n)
    (exponentialCoefficient o x j (monomialBasis o a))
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply] at hc
  rw [sub_eq_iff_eq_add] at hc
  rw [hc, exponentialCoefficient_lowersWeight o x j, halfDegree_monomial]
  simp only [map_sub, map_smul]
  module

theorem two_conformal_basisKernelCutoff (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (N : ℕ) (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) :
    (2:ℂ) • conformalMode o 0 (basisKernelCutoff o x s k N a q) =
      ((twiceWeight o a:ℂ)+3+((k-s:ℤ):ℂ)) • basisKernelCutoff o x s k N a q := by
  simp only [basisKernelCutoff, map_sum, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  by_cases hj : 0 ≤ k-s+(j:ℤ)
  · rw [if_pos hj, two_conformalMode_tmul, halfDegree_creation_annihilation]
    simp only [← TensorProduct.smul_tmul']
    have hc : (((k-s+(j:ℤ)).toNat : ℕ):ℂ) = (k:ℂ)-(s:ℂ)+(j:ℂ) := by
      exact_mod_cast (Int.toNat_of_nonneg hj)
    rw [hc]
    simp only [Int.cast_sub]
    module
  · rw [if_neg hj, map_zero, smul_zero, smul_zero]

theorem two_conformal_basisKernelCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) :
    (2:ℂ) • conformalMode o 0 (basisKernelCoefficient o x s k a q) =
      ((twiceWeight o a:ℂ)+3+((k-s:ℤ):ℂ)) • basisKernelCoefficient o x s k a q :=
  two_conformal_basisKernelCutoff o x s k (twiceWeight o a) a q

theorem kernelCoefficient_two_conformal_commutator (o : Fin 12) (x : Lattice o)
    (s k : ℤ) :
    ((2:ℂ) • conformalMode o 0) * kernelCoefficient o x s k -
      kernelCoefficient o x s k * ((2:ℂ) • conformalMode o 0) =
        ((k-s:ℤ):ℂ) • kernelCoefficient o x s k := by
  apply (twistedBasis o).ext
  rintro ⟨a,q⟩
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    conformal_basis_weight, map_smul, kernelCoefficient_basis]
  rw [two_conformal_basisKernelCoefficient]
  module

theorem kernelCoefficient_conformal_commutator (o : Fin 12) (x : Lattice o)
    (s k : ℤ) :
    conformalMode o 0 * kernelCoefficient o x s k -
      kernelCoefficient o x s k * conformalMode o 0 =
        (((k-s:ℤ):ℂ)/2) • kernelCoefficient o x s k := by
  apply LinearMap.ext
  intro v
  have h := LinearMap.congr_fun (kernelCoefficient_two_conformal_commutator o x s k) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    map_smul] at h ⊢
  calc
    _ = (1/2:ℂ) • ((2:ℂ) • conformalMode o 0 (kernelCoefficient o x s k v) -
        (2:ℂ) • kernelCoefficient o x s k (conformalMode o 0 v)) := by module
    _ = (1/2:ℂ) • (((k-s:ℤ):ℂ) • kernelCoefficient o x s k v) := by rw [h]
    _ = _ := by module

theorem kernelCoefficient_weight_shift (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (v : Carrier o) (d : ℂ) (hv : conformalMode o 0 v = d • v) :
    conformalMode o 0 (kernelCoefficient o x s k v) =
      (d+((k-s:ℤ):ℂ)/2) • kernelCoefficient o x s k v := by
  have h := LinearMap.congr_fun (kernelCoefficient_conformal_commutator o x s k) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply] at h
  rw [hv, map_smul, sub_eq_iff_eq_add] at h
  rw [h]
  module

theorem kernelCoefficient_ground_weight (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (t : FiniteSpace o) :
    conformalMode o 0 (kernelCoefficient o x s k (groundEmbedding o t)) =
      ((3/2:ℂ)+((k-s:ℤ):ℂ)/2) • kernelCoefficient o x s k (groundEmbedding o t) :=
  kernelCoefficient_weight_shift o x s k (groundEmbedding o t) (3/2) (ground_weight o t)

end HMT.IV.LatticeTwistedKernelEnergy
end

#print axioms HMT.IV.LatticeTwistedKernelEnergy.two_shifted_zero
#print axioms HMT.IV.LatticeTwistedKernelEnergy.two_conformalMode_tmul
#print axioms HMT.IV.LatticeTwistedKernelEnergy.halfDegree_creation_annihilation
#print axioms HMT.IV.LatticeTwistedKernelEnergy.two_conformal_basisKernelCutoff
#print axioms HMT.IV.LatticeTwistedKernelEnergy.two_conformal_basisKernelCoefficient
#print axioms HMT.IV.LatticeTwistedKernelEnergy.kernelCoefficient_two_conformal_commutator
#print axioms HMT.IV.LatticeTwistedKernelEnergy.kernelCoefficient_conformal_commutator
#print axioms HMT.IV.LatticeTwistedKernelEnergy.kernelCoefficient_weight_shift
#print axioms HMT.IV.LatticeTwistedKernelEnergy.kernelCoefficient_ground_weight
