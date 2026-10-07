import Mathlib

namespace HMT.IV.LatticeCocycle

theorem integral_basis_parity_expansion {n : ℕ} {M : Type*}
    [AddCommGroup M] [Module ℤ M]
    (b : Basis (Fin n) ℤ M) (B : M →ₗ[ℤ] M →ₗ[ℤ] ZMod 2)
    (x y : M) :
    B x y = ∑ i, ∑ j,
      (b.repr x i : ZMod 2) * B (b i) (b j) * (b.repr y j : ZMod 2) := by
  have h := LinearMap.sum_repr_mul_repr_mul b b (B := B) x y
  simpa [Finsupp.sum_fintype, zsmul_eq_mul, mul_assoc, mul_comm, mul_left_comm] using h.symm

#print axioms integral_basis_parity_expansion

end HMT.IV.LatticeCocycle
