import LatticeHalfGramTransport

/-! A bilinear contragredient pairing on the actual unbounded half-integer
oscillator algebra. Its Gram matrix, frequency factors and inverse all come
from the inherited marked lattice. The convention is creator adjoint = minus
annihilator, rather than the positive Hermitian convention. -/

noncomputable section
namespace HMT.IV.LatticeHalfFockPairing
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeFockMonomialParity LatticeFactorialPairing LatticeHalfGramTransport
open LatticeGramDual
open scoped BigOperators

def contravariantPairing (o : Fin 12) : LinearMap.BilinForm ℂ (HalfFock o) :=
  LinearMap.comp (factorialPairing o) (gramTransport o).toLinearMap

theorem contravariantPairing_apply (o : Fin 12) (u v : HalfFock o) :
    contravariantPairing o u v = factorialPairing o (gramTransport o u) v := rfl

theorem contravariantPairing_nondegenerate (o : Fin 12) :
    (contravariantPairing o).Nondegenerate := by
  intro v hv
  have hg : gramTransport o v = 0 := factorialPairing_nondegenerate o _ hv
  apply (gramTransport_left_inverse o).injective
  simpa only [map_zero] using hg

theorem contravariantPairing_right_separating (o : Fin 12) (v : HalfFock o)
    (h : ∀ u, contravariantPairing o u v = 0) : v = 0 := by
  apply WeightedBasisPairing.right_separating (monomialBasis o)
    (occupationFactorial o) (occupationFactorial_ne_zero o) v
  intro w
  obtain ⟨u, hu⟩ := (gramTransport_right_inverse o).surjective w
  rw [← hu]
  exact h u

theorem halfAnnihilate_coordinate_expansion (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) :
    (∑ j, (halfScale n*gram o i j) • coordinateDerivative o (n,j)) =
      -halfAnnihilate o n i := by
  classical
  apply LinearMap.ext
  intro v
  simp only [LinearMap.sum_apply, LinearMap.smul_apply, coordinateDerivative,
    Finset.smul_sum, smul_smul]
  rw [Finset.sum_comm]
  have inner (k : Fin (BasisSize o)) :
      (∑ j, (halfScale n*gram o i j*((n+1:ℂ)⁻¹*gramInv o j k)) • annihilate o n k v) =
        (halfScale n*(n+1:ℂ)⁻¹*(if i=k then 1 else 0)) • annihilate o n k v := by
    rw [← Finset.sum_smul]
    congr 1
    calc
      _ = (halfScale n*(n+1:ℂ)⁻¹) * ∑ j, gram o i j*gramInv o j k := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = _ := by rw [pairing_gramInv]
  simp_rw [inner]
  simp only [mul_ite, mul_one, mul_zero, ite_smul, zero_smul]
  rw [Finset.sum_ite_eq]
  simp only [Finset.mem_univ, if_true, halfAnnihilate, LinearMap.neg_apply,
    LinearMap.smul_apply, halfScale, annihilationScale, neg_mul, div_eq_mul_inv,
    neg_smul]

theorem contravariantPairing_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (u v : HalfFock o) :
    contravariantPairing o (create o n i u) v =
      -contravariantPairing o u (halfAnnihilate o n i v) := by
  rw [contravariantPairing_apply, gramTransport_create]
  simp only [map_sum, LinearMap.sum_apply, map_smul, LinearMap.smul_apply,
    factorialPairing_create]
  have h := LinearMap.congr_fun (halfAnnihilate_coordinate_expansion o n i) v
  simp only [LinearMap.sum_apply, LinearMap.smul_apply, LinearMap.neg_apply] at h
  calc
    _ = ∑ j, (halfScale n*gram o i j) • factorialPairing o (gramTransport o u)
        (coordinateDerivative o (n,j) v) := by
      apply Finset.sum_congr rfl
      intro j _
      rw [factorialPairing_create o (n,j)]
    _ = factorialPairing o (gramTransport o u)
        (∑ j, (halfScale n*gram o i j) • coordinateDerivative o (n,j) v) := by
      simp only [map_sum, map_smul]
    _ = _ := by rw [h, map_neg]; rfl

end HMT.IV.LatticeHalfFockPairing
end
