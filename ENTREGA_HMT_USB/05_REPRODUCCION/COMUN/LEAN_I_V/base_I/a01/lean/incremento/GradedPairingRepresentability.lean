import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.BilinearForm.Properties
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.Tactic.NormNum

/-!
# Representability on homogeneous pieces of a nondegenerate pairing

The ambient complex module need not be finite-dimensional.  Self-adjointness of
the weight operator gives orthogonality of distinct eigenspaces; the spanning
hypothesis then transfers left nondegeneracy to each weight.  Only the final
identification with the full algebraic dual requires finite-dimensionality of
the individual weight space.  The pairing need not be symmetric.
-/

noncomputable section

namespace HMT.IV.GradedPairingRepresentability

open LinearMap (BilinForm)

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- The actual eigenspace inside the original module. -/
def weightSpace (E : Module.End ℂ V) (d : ℕ) : Submodule ℂ V :=
  Module.End.eigenspace E (d : ℂ)

@[simp]
theorem mem_weightSpace (E : Module.End ℂ V) (d : ℕ) (v : V) :
    v ∈ weightSpace E d ↔ E v = (d : ℂ) • v :=
  Module.End.mem_eigenspace_iff

/-- Distinct natural weights are orthogonal in the specified argument order. -/
theorem orthogonal_weights (B : BilinForm ℂ V) (E : Module.End ℂ V)
    (hself : ∀ u v, B (E u) v = B u (E v))
    {d e : ℕ} {u v : V} (hu : E u = (d : ℂ) • u)
    (hv : E v = (e : ℂ) • v) (hne : d ≠ e) : B u v = 0 := by
  have h : (d : ℂ) * B u v = (e : ℂ) * B u v := by
    simpa only [hu, hv, BilinForm.smul_left, BilinForm.smul_right] using hself u v
  exact (mul_eq_mul_right_iff.mp h).resolve_left
    (fun heq => hne (Nat.cast_injective heq))

/-- Global nondegeneracy and the spanning eigenspaces imply nondegeneracy on
each weight; this is not an additional assumption about the restriction. -/
theorem weight_restrict_nondegenerate (B : BilinForm ℂ V) (E : Module.End ℂ V)
    (hB : B.Nondegenerate)
    (hself : ∀ u v, B (E u) v = B u (E v))
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) (d : ℕ) :
    (B.restrict (weightSpace E d)).Nondegenerate := by
  intro u hu
  apply Subtype.ext
  change (u : V) = 0
  apply hB
  intro v
  have hv : v ∈ ⨆ e : ℕ, weightSpace E e := by rw [hspan]; trivial
  apply Submodule.iSup_induction (weightSpace E)
    (motive := fun v => B (u : V) v = 0) hv
  · intro e v hv
    by_cases hde : d = e
    · subst e
      exact hu ⟨v, hv⟩
    · exact orthogonal_weights B E hself
        ((mem_weightSpace E d u).mp u.property)
        ((mem_weightSpace E e v).mp hv) hde
  · exact map_zero (B (u : V))
  · intro x y hx hy
    simp only [map_add, hx, hy, add_zero]

/-- Mathlib's `BilinForm.toDual`, applied only after proving nondegeneracy of
the restriction and requiring finite-dimensionality of this weight space. -/
def weightToDual (B : BilinForm ℂ V) (E : Module.End ℂ V)
    (hB : B.Nondegenerate)
    (hself : ∀ u v, B (E u) v = B u (E v))
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) (d : ℕ)
    [FiniteDimensional ℂ (weightSpace E d)] :
    weightSpace E d ≃ₗ[ℂ] Module.Dual ℂ (weightSpace E d) :=
  (B.restrict (weightSpace E d)).toDual
    (weight_restrict_nondegenerate B E hB hself hspan d)

/-- The unique representing vector of a functional on a finite-dimensional weight. -/
def weightRepresentative (B : BilinForm ℂ V) (E : Module.End ℂ V)
    (hB : B.Nondegenerate)
    (hself : ∀ u v, B (E u) v = B u (E v))
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) (d : ℕ)
    [FiniteDimensional ℂ (weightSpace E d)]
    (f : Module.Dual ℂ (weightSpace E d)) : weightSpace E d :=
  (weightToDual B E hB hself hspan d).symm f

theorem weightRepresentative_spec (B : BilinForm ℂ V) (E : Module.End ℂ V)
    (hB : B.Nondegenerate)
    (hself : ∀ u v, B (E u) v = B u (E v))
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) (d : ℕ)
    [FiniteDimensional ℂ (weightSpace E d)]
    (f : Module.Dual ℂ (weightSpace E d)) (v : weightSpace E d) :
    B (weightRepresentative B E hB hself hspan d f) v = f v :=
  BilinForm.apply_toDual_symm_apply (B := B.restrict (weightSpace E d))
    (hB := weight_restrict_nondegenerate B E hB hself hspan d) f v

theorem existsUnique_weight_representative (B : BilinForm ℂ V) (E : Module.End ℂ V)
    (hB : B.Nondegenerate)
    (hself : ∀ u v, B (E u) v = B u (E v))
    (hspan : (⨆ d : ℕ, weightSpace E d) = ⊤) (d : ℕ)
    [FiniteDimensional ℂ (weightSpace E d)]
    (f : Module.Dual ℂ (weightSpace E d)) :
    ∃! u : weightSpace E d, ∀ v : weightSpace E d, B u v = f v := by
  refine ⟨weightRepresentative B E hB hself hspan d f,
    weightRepresentative_spec B E hB hself hspan d f, ?_⟩
  intro u hu
  apply (weightToDual B E hB hself hspan d).injective
  apply LinearMap.ext
  intro v
  exact (hu v).trans (weightRepresentative_spec B E hB hself hspan d f v).symm

/-- Fixed vectors of an endomorphism, as its eigenvalue-one subspace. -/
def fixedSpace (S : Module.End ℂ V) : Submodule ℂ V :=
  Module.End.eigenspace S 1

@[simp]
theorem mem_fixedSpace (S : Module.End ℂ V) (v : V) :
    v ∈ fixedSpace S ↔ S v = v := by
  simp only [fixedSpace, Module.End.mem_eigenspace_iff, one_smul]

/-- The averaging projector associated to an involution. -/
def fixedProjection (S : Module.End ℂ V) : Module.End ℂ V :=
  (1 / 2 : ℂ) • (1 + S)

@[simp]
theorem fixedProjection_apply (S : Module.End ℂ V) (v : V) :
    fixedProjection S v = (1 / 2 : ℂ) • (v + S v) := rfl

theorem fixedProjection_mem (S : Module.End ℂ V) (hS : Function.Involutive S) (v : V) :
    fixedProjection S v ∈ fixedSpace S := by
  rw [mem_fixedSpace, fixedProjection_apply, map_smul, map_add, hS v, add_comm]

/-- For a fixed vector in the first argument, averaging the second argument
does not change the pairing.  Self-adjointness, not symmetry of `B`, is used. -/
theorem pairing_fixedProjection (B : BilinForm ℂ V) (S : Module.End ℂ V)
    (hself : ∀ u v, B (S u) v = B u (S v)) {u : V} (hu : S u = u) (v : V) :
    B u (fixedProjection S v) = B u v := by
  have hpair : B u (S v) = B u v := by rw [← hself u v, hu]
  rw [fixedProjection_apply, BilinForm.smul_right, map_add, hpair, ← two_mul]
  rw [← mul_assoc]
  norm_num

/-- A self-adjoint involution has a nondegenerate fixed-space restriction even
when the ambient module is infinite-dimensional. -/
theorem fixed_restrict_nondegenerate (B : BilinForm ℂ V) (S : Module.End ℂ V)
    (hB : B.Nondegenerate) (hS : Function.Involutive S)
    (hself : ∀ u v, B (S u) v = B u (S v)) :
    (B.restrict (fixedSpace S)).Nondegenerate := by
  intro u hu
  apply Subtype.ext
  change (u : V) = 0
  apply hB
  intro v
  have hz := hu ⟨fixedProjection S v, fixedProjection_mem S hS v⟩
  change B (u : V) (fixedProjection S v) = 0 at hz
  rw [pairing_fixedProjection B S hself ((mem_fixedSpace S u).mp u.property)] at hz
  exact hz

end HMT.IV.GradedPairingRepresentability
