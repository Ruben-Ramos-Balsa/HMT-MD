import VertexBlockAssembly
import LatticeOrbifoldCarrier
import LatticeEvenLocality

/-!
Assembly on the two existing lattice sectors, with no replacement of their
origin, cocycle or carriers. The even-even block is the already constructed
lattice state-field map. The three mixed blocks are explicit linear inputs.

This module proves how those inputs assemble and how to recover each one.
It does not assert that the mixed products exist, satisfy locality, or define
the FLM orbifold. Those are separate properties of the concrete inputs.
All exponents here are exponents of z, not of the ramified coordinate t.
-/

noncomputable section
namespace HMT.IV.LatticeOrbifoldBlocks

open LatticeEvenVertexFields LatticeEvenTranslation LatticeEvenLocality
open LatticeTwistedPositiveSector LatticeOrbifoldCarrier

/-- Exactly the three sector products not already supplied by `evenStateField`.
No equations identifying an output with the desired orbifold are assumed. -/
structure MixedFields (o : Fin 12) where
  et : evenSpace o →ₗ[ℂ] HVertexOperator ℤ ℂ (positiveSector o) (positiveSector o)
  te : positiveSector o →ₗ[ℂ] HVertexOperator ℤ ℂ (evenSpace o) (positiveSector o)
  tt : positiveSector o →ₗ[ℂ] HVertexOperator ℤ ℂ (positiveSector o) (evenSpace o)

def blocks (o : Fin 12) (M : MixedFields o) :
    VertexBlockAssembly.Blocks ℂ (evenSpace o) (positiveSector o) where
  ee := evenStateField o
  et := M.et
  te := M.te
  tt := M.tt

/-- A linear family of lower-truncated fields on the existing direct sum. -/
def stateField (o : Fin 12) (M : MixedFields o) :
    Space o →ₗ[ℂ] VertexOperator ℂ (Space o) :=
  VertexBlockAssembly.fieldMap (blocks o M)

theorem coefficient_formula (o : Fin 12) (M : MixedFields o)
    (u v : Space o) (k : ℤ) :
    HVertexOperator.coeff (stateField o M u) k v =
      (evenCoefficient o u.1 k v.1 + HVertexOperator.coeff (M.tt u.2) k v.2,
       HVertexOperator.coeff (M.et u.1) k v.2 +
         HVertexOperator.coeff (M.te u.2) k v.1) := by
  change HVertexOperator.coeff (VertexBlockAssembly.field (blocks o M) u) k v = _
  rw [VertexBlockAssembly.field_coefficient]
  simp only [VertexBlockAssembly.coefficient, blocks, evenStateField_apply,
    evenField_coefficient, LinearMap.coe_mk, AddHom.coe_mk]

/-- The old even product is preserved exactly, not merely up to isomorphism. -/
theorem even_even (o : Fin 12) (M : MixedFields o)
    (u v : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (stateField o M (u, 0)) k (v, 0) =
      (evenCoefficient o u k v, 0) := by
  change HVertexOperator.coeff (VertexBlockAssembly.field (blocks o M) (u, 0)) k
    (v, 0) = _
  rw [VertexBlockAssembly.field_even_even]
  simp only [blocks, evenStateField_apply, evenField_coefficient]

theorem even_twisted (o : Fin 12) (M : MixedFields o)
    (u : evenSpace o) (v : positiveSector o) (k : ℤ) :
    HVertexOperator.coeff (stateField o M (u, 0)) k (0, v) =
      (0, HVertexOperator.coeff (M.et u) k v) := by
  change HVertexOperator.coeff (VertexBlockAssembly.field (blocks o M) (u, 0)) k
    (0, v) = _
  exact VertexBlockAssembly.field_even_twisted (blocks o M) u v k

theorem twisted_even (o : Fin 12) (M : MixedFields o)
    (u : positiveSector o) (v : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (stateField o M (0, u)) k (v, 0) =
      (0, HVertexOperator.coeff (M.te u) k v) := by
  change HVertexOperator.coeff (VertexBlockAssembly.field (blocks o M) (0, u)) k
    (v, 0) = _
  exact VertexBlockAssembly.field_twisted_even (blocks o M) u v k

theorem twisted_twisted (o : Fin 12) (M : MixedFields o)
    (u v : positiveSector o) (k : ℤ) :
    HVertexOperator.coeff (stateField o M (0, u)) k (0, v) =
      (HVertexOperator.coeff (M.tt u) k v, 0) := by
  change HVertexOperator.coeff (VertexBlockAssembly.field (blocks o M) (0, u)) k
    (0, v) = _
  exact VertexBlockAssembly.field_twisted_twisted (blocks o M) u v k

theorem lower_truncation (o : Fin 12) (M : MixedFields o) (u v : Space o) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff (stateField o M u) k v = 0 := by
  obtain ⟨b, hb⟩ := VertexBlockAssembly.coefficient_bounded_pole (blocks o M) u v
  refine ⟨b, fun k hk => ?_⟩
  change HVertexOperator.coeff (VertexBlockAssembly.field (blocks o M) u) k v = 0
  rw [VertexBlockAssembly.field_coefficient]
  exact hb k hk

/-- Assembly cannot discard or silently replace any of the mixed blocks. -/
theorem stateField_injective (o : Fin 12) : Function.Injective (stateField o) := by
  intro A B h
  have het : A.et = B.et := by
    apply LinearMap.ext
    intro u
    apply HVertexOperator.coeff_inj
    funext k
    apply LinearMap.ext
    intro v
    have hh := congrArg
      (fun F => (HVertexOperator.coeff (F (u, 0)) k (0, v)).2) h
    simpa only [even_twisted] using hh
  have hte : A.te = B.te := by
    apply LinearMap.ext
    intro u
    apply HVertexOperator.coeff_inj
    funext k
    apply LinearMap.ext
    intro v
    have hh := congrArg
      (fun F => (HVertexOperator.coeff (F (0, u)) k (v, 0)).2) h
    simpa only [twisted_even] using hh
  have htt : A.tt = B.tt := by
    apply LinearMap.ext
    intro u
    apply HVertexOperator.coeff_inj
    funext k
    apply LinearMap.ext
    intro v
    have hh := congrArg
      (fun F => (HVertexOperator.coeff (F (0, u)) k (0, v)).1) h
    simpa only [twisted_twisted] using hh
  cases A
  cases B
  cases het
  cases hte
  cases htt
  rfl

end HMT.IV.LatticeOrbifoldBlocks
end

