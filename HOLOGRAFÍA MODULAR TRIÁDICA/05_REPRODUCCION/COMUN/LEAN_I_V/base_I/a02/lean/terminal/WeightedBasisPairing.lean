import Mathlib.LinearAlgebra.BilinearForm.Basic
import Mathlib.LinearAlgebra.Basis.Basic
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

noncomputable section
namespace HMT.IV.WeightedBasisPairing

variable {ι V : Type*} [AddCommGroup V] [Module ℂ V]

def form (b : Basis ι ℂ V) (w : ι → ℂ) : LinearMap.BilinForm ℂ V :=
  b.constr ℂ (fun i => w i • b.coord i)

theorem basis_left (b : Basis ι ℂ V) (w : ι → ℂ) (i : ι) (v : V) :
    form b w (b i) v = w i * b.repr v i := by
  simp [form, Basis.constr_basis]

theorem basis_right (b : Basis ι ℂ V) (w : ι → ℂ) (v : V) (j : ι) :
    form b w v (b j) = w j * b.repr v j := by
  classical
  have he : (form b w).flip (b j) = w j • b.coord j := by
    apply b.ext
    intro i
    change form b w (b i) (b j) = (w j • b.coord j) (b i)
    simp only [basis_left, Basis.repr_self, Finsupp.single_apply,
      LinearMap.smul_apply, Basis.coord_apply, smul_eq_mul]
    by_cases h : i = j
    · subst j; simp
    · simp [h, Ne.symm h]
  exact LinearMap.congr_fun he v

theorem symmetric (b : Basis ι ℂ V) (w : ι → ℂ) (u v : V) :
    form b w u v = form b w v u := by
  have he : form b w = (form b w).flip := by
    apply b.ext
    intro i
    apply LinearMap.ext
    intro v
    change form b w (b i) v = form b w v (b i)
    rw [basis_left, basis_right]
  exact LinearMap.congr_fun (LinearMap.congr_fun he u) v

theorem nondegenerate (b : Basis ι ℂ V) (w : ι → ℂ) (hw : ∀ i, w i ≠ 0) :
    (form b w).Nondegenerate := by
  intro v hv
  apply b.repr.injective
  apply Finsupp.ext
  intro i
  have h := hv (b i)
  rw [basis_right] at h
  simpa only [map_zero, Finsupp.zero_apply] using (mul_eq_zero.mp h).resolve_left (hw i)

theorem right_separating (b : Basis ι ℂ V) (w : ι → ℂ) (hw : ∀ i, w i ≠ 0)
    (v : V) (h : ∀ u, form b w u v = 0) : v = 0 := by
  apply nondegenerate b w hw v
  intro u
  rw [symmetric]
  exact h u

end HMT.IV.WeightedBasisPairing
end
