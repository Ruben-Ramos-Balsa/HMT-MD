import HilbertTDuality
import Mathlib.Analysis.InnerProductSpace.LinearPMap

/-!
Self-adjointness of the full diagonal Hamiltonian on ell-two. Symmetry is
proved on its weighted domain. Testing the adjoint against coordinate vectors
then reconstructs all its coordinates and proves equality of domains.
Finite support is used only as a family of tests, not as an operator domain.
-/
noncomputable section
namespace HMT.IV.HilbertTAdjoint

open HMT.IV.HilbertTDuality FiniteWeyl.Duality
open scoped LinearPMap

def hamiltonianPMap (r : ℝ) : State →ₗ.[ℂ] State where
  domain := operatorDomain r
  toFun := hamiltonian r

theorem hamiltonianPMap_apply (r : ℝ) (f : (hamiltonianPMap r).domain)
    (v : ℤ × ℤ) :
    hamiltonianPMap r f v = (energyAt r v : ℂ) * f.val v := rfl

theorem hamiltonianPMap_dense (r : ℝ) :
    Dense ((hamiltonianPMap r).domain : Set State) := operator_domain_dense r

theorem hamiltonianPMap_formalAdjoint (r : ℝ) :
    (hamiltonianPMap r).IsFormalAdjoint (hamiltonianPMap r) := by
  intro f g
  rw [lp.inner_eq_tsum, lp.inner_eq_tsum]
  apply tsum_congr
  intro v
  change inner ℂ ((energyAt r v : ℂ) * f.val v) (g.val v) =
    inner ℂ (f.val v) ((energyAt r v : ℂ) * g.val v)
  simp [RCLike.inner_apply, map_mul, Complex.conj_ofReal]
  ring

theorem hamiltonianPMap_single (r : ℝ) (v : ℤ × ℤ) (a : ℂ) :
    hamiltonianPMap r ⟨lp.single 2 v a, single_in_domain r v a⟩ =
      lp.single 2 v ((energyAt r v : ℂ) * a) := by
  apply lp.ext
  funext u
  by_cases hu : u = v
  · subst u
    simp [hamiltonianPMap_apply, lp.single_apply_self]
  · simp [hamiltonianPMap_apply, lp.single_apply, Pi.single_eq_of_ne hu]

theorem adjoint_coordinate (r : ℝ) (y : (hamiltonianPMap r)†.domain)
    (v : ℤ × ℤ) :
    (hamiltonianPMap r)† y v = (energyAt r v : ℂ) * y.val v := by
  have h := (LinearPMap.adjoint_isFormalAdjoint (hamiltonianPMap_dense r)).symm
    ⟨lp.single 2 v 1, single_in_domain r v 1⟩ y
  rw [hamiltonianPMap_single, lp.inner_single_left, lp.inner_single_left] at h
  simpa [RCLike.inner_apply, Complex.conj_ofReal, mul_comm] using h.symm

theorem adjoint_domain_subset (r : ℝ) :
    (hamiltonianPMap r)†.domain ≤ (hamiltonianPMap r).domain := by
  intro y hy
  change InDomain r y
  unfold InDomain
  have he : multiplyEnergy r y = ((hamiltonianPMap r)† ⟨y, hy⟩ : State) := by
    funext v
    exact (adjoint_coordinate r ⟨y, hy⟩ v).symm
  rw [he]
  exact ((hamiltonianPMap r)† ⟨y, hy⟩).property

theorem adjoint_domain_eq (r : ℝ) :
    (hamiltonianPMap r)†.domain = (hamiltonianPMap r).domain := by
  apply le_antisymm (adjoint_domain_subset r)
  exact ((hamiltonianPMap_formalAdjoint r).le_adjoint (hamiltonianPMap_dense r)).1

theorem hamiltonianPMap_adjoint_eq (r : ℝ) :
    (hamiltonianPMap r)† = hamiltonianPMap r := by
  apply LinearPMap.ext (adjoint_domain_eq r)
  intro y hy hyD
  apply lp.ext
  funext v
  exact adjoint_coordinate r ⟨y, hy⟩ v

theorem hamiltonianPMap_selfAdjoint (r : ℝ) : IsSelfAdjoint (hamiltonianPMap r) :=
  (LinearPMap.isSelfAdjoint_def).mpr (hamiltonianPMap_adjoint_eq r)

#print axioms hamiltonianPMap_apply
#print axioms hamiltonianPMap_dense
#print axioms hamiltonianPMap_formalAdjoint
#print axioms hamiltonianPMap_single
#print axioms adjoint_coordinate
#print axioms adjoint_domain_subset
#print axioms adjoint_domain_eq
#print axioms hamiltonianPMap_adjoint_eq
#print axioms hamiltonianPMap_selfAdjoint

end HMT.IV.HilbertTAdjoint
end
