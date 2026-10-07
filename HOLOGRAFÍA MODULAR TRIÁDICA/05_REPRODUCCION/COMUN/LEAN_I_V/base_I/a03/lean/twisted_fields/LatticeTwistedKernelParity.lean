import LatticeTwistedExponentialKernel
import LatticeHalfCreationParity
import LatticeHalfAnnihilationParity
import LatticeTwistedBasisParity

/-! Charge reversal, the lifted involution and the ramified exponential kernel.
The charge-even combination has support k congruent to its explicit shift s
modulo two. After removal of that shift, a genuine Laurent field in z=t² is
constructed from its even coefficients. No physical prefactor, twisted Jacobi
identity or orbifold multiplication is assumed. -/

noncomputable section
namespace HMT.IV.LatticeTwistedKernelParity
open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeFiniteIrreducible LatticeFiniteGroundState LatticeHalfIntegerHeisenberg
open LatticeTwistedCarrier LatticeTwistedParity LatticeTwistedLowWeights
open LatticeTwistedBasisParity LatticeParityCarrier
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeHalfCreationParity LatticeHalfAnnihilationParity
open LatticeTwistedExponentialKernel

def paritySign (r : ℤ) : ℂ := (-1:ℂ) ^ (r%2).toNat

theorem paritySign_even (r : ℤ) : paritySign (2*r) = 1 := by
  simp [paritySign]

theorem paritySign_odd (r : ℤ) : paritySign (2*r+1) = -1 := by
  have h : (2*r+1)%2=1 := by omega
  simp [paritySign, h]

theorem combined_parity (r : ℤ) (j : ℕ) (h : 0 ≤ r+(j:ℤ)) :
    (-1:ℂ) ^ (r+(j:ℤ)).toNat * (-1:ℂ)^j = paritySign r := by
  rw [← pow_add, neg_one_pow_eq_pow_mod_two]
  have he : ((r+(j:ℤ)).toNat+j)%2 = (r%2).toNat := by omega
  rw [he]
  rfl

theorem basisKernelCutoff_neg_charge (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (N : ℕ) (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) :
    basisKernelCutoff o (-x) s k N a q =
      paritySign (k-s) • basisKernelCutoff o x s k N a q := by
  unfold basisKernelCutoff
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  by_cases hj : 0 ≤ k-s+(j:ℤ)
  · rw [if_pos hj, if_pos hj, halfCreationExponentialMode_neg_charge,
      exponentialCoefficient_neg_charge, LinearMap.smul_apply, LinearMap.smul_apply,
      map_smul, smul_smul, combined_parity (k-s) j hj,
      TensorProduct.smul_tmul', latticeOperator_neg]
  · simp only [if_neg hj, smul_zero]

theorem kernelCoefficient_neg_charge (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    kernelCoefficient o (-x) s k = paritySign (k-s) • kernelCoefficient o x s k := by
  apply (twistedBasis o).ext
  rintro ⟨a,q⟩
  rw [kernelCoefficient_basis, LinearMap.smul_apply, kernelCoefficient_basis]
  exact basisKernelCutoff_neg_charge o x s k _ a q

theorem theta_creationMode_charge (o : Fin 12) (x : Lattice o) (d : ℕ)
    (v : HalfFock o) :
    fockTheta o (halfCreationExponentialMode o x d v) =
      halfCreationExponentialMode o (-x) d (fockTheta o v) := by
  rw [theta_halfCreationExponentialMode, halfCreationExponentialMode_neg_charge,
    LinearMap.smul_apply]

theorem theta_basisKernelCutoff (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (N : ℕ) (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) :
    liftedTheta o (basisKernelCutoff o x s k N a q) =
      (-((-1:ℂ)^occupationLength o a)) • basisKernelCutoff o (-x) s k N a q := by
  unfold basisKernelCutoff
  rw [map_sum, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  by_cases hj : 0 ≤ k-s+(j:ℤ)
  · rw [if_pos hj, if_pos hj, liftedTheta_tmul, theta_creationMode_charge,
      theta_exponentialCoefficient_charge, fockTheta_monomial,
      map_smul, map_smul, TensorProduct.smul_tmul', latticeOperator_neg]
    simp only [neg_smul, TensorProduct.neg_tmul]
  · simp only [if_neg hj, map_zero, smul_zero]

theorem theta_kernelCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    (liftedTheta o).comp (kernelCoefficient o x s k) =
      (kernelCoefficient o (-x) s k).comp (liftedTheta o) := by
  apply (twistedBasis o).ext
  rintro ⟨a,q⟩
  simp only [LinearMap.comp_apply, kernelCoefficient_basis, liftedTheta_basis,
    map_smul]
  exact theta_basisKernelCutoff o x s k _ a q

def evenKernelCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    Module.End ℂ (Carrier o) :=
  (2:ℂ)⁻¹ • (kernelCoefficient o x s k + kernelCoefficient o (-x) s k)

theorem evenKernelCoefficient_even_shift (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    evenKernelCoefficient o x s (2*k+s) = kernelCoefficient o x s (2*k+s) := by
  unfold evenKernelCoefficient
  rw [kernelCoefficient_neg_charge, show 2*k+s-s=2*k by omega, paritySign_even]
  simp only [one_smul]
  module

theorem evenKernelCoefficient_odd_shift (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    evenKernelCoefficient o x s (2*k+1+s) = 0 := by
  unfold evenKernelCoefficient
  rw [kernelCoefficient_neg_charge, show 2*k+1+s-s=2*k+1 by omega, paritySign_odd]
  module

theorem theta_evenKernelCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    (liftedTheta o).comp (evenKernelCoefficient o x s k) =
      (evenKernelCoefficient o x s k).comp (liftedTheta o) := by
  unfold evenKernelCoefficient
  simp only [LinearMap.comp_smul, LinearMap.comp_add, LinearMap.smul_comp,
    LinearMap.add_comp, theta_kernelCoefficient, neg_neg]
  rw [add_comm]

theorem evenKernelCoefficient_bounded_pole (o : Fin 12) (x : Lattice o) (s : ℤ)
    (v : Carrier o) : ∃ b : ℤ, ∀ k < b, evenKernelCoefficient o x s k v = 0 := by
  obtain ⟨b,hb⟩ := kernelCoefficient_bounded_pole o x s v
  obtain ⟨c,hc⟩ := kernelCoefficient_bounded_pole o (-x) s v
  refine ⟨min b c, ?_⟩
  intro k hk
  simp only [evenKernelCoefficient, LinearMap.smul_apply, LinearMap.add_apply,
    hb k (lt_of_lt_of_le hk (min_le_left _ _)),
    hc k (lt_of_lt_of_le hk (min_le_right _ _)), add_zero, smul_zero]

def evenKernel (o : Fin 12) (x : Lattice o) (s : ℤ) :
    VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (evenKernelCoefficient o x s)
    (evenKernelCoefficient_bounded_pole o x s)

theorem evenKernel_coefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    HVertexOperator.coeff (evenKernel o x s) k = evenKernelCoefficient o x s k := by
  apply LinearMap.ext
  intro v
  rfl

def descendedCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    Module.End ℂ (Carrier o) := evenKernelCoefficient o x s (2*k+s)

theorem descendedCoefficient_bounded_pole (o : Fin 12) (x : Lattice o) (s : ℤ)
    (v : Carrier o) : ∃ b : ℤ, ∀ k < b, descendedCoefficient o x s k v = 0 := by
  obtain ⟨b,hb⟩ := evenKernelCoefficient_bounded_pole o x s v
  refine ⟨(b-s)/2, ?_⟩
  intro k hk
  exact hb _ (by omega)

def descendedEvenKernel (o : Fin 12) (x : Lattice o) (s : ℤ) :
    VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (descendedCoefficient o x s)
    (descendedCoefficient_bounded_pole o x s)

theorem descendedEvenKernel_coefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    HVertexOperator.coeff (descendedEvenKernel o x s) k =
      HVertexOperator.coeff (evenKernel o x s) (2*k+s) := by
  rw [evenKernel_coefficient]
  apply LinearMap.ext
  intro v
  rfl

theorem evenKernel_odd_shift_zero (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    HVertexOperator.coeff (evenKernel o x s) (2*k+1+s) = 0 := by
  rw [evenKernel_coefficient, evenKernelCoefficient_odd_shift]

theorem theta_descendedEvenKernel (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    (liftedTheta o).comp (HVertexOperator.coeff (descendedEvenKernel o x s) k) =
      (HVertexOperator.coeff (descendedEvenKernel o x s) k).comp (liftedTheta o) := by
  rw [descendedEvenKernel_coefficient, evenKernel_coefficient]
  exact theta_evenKernelCoefficient o x s (2*k+s)

end HMT.IV.LatticeTwistedKernelParity
end
