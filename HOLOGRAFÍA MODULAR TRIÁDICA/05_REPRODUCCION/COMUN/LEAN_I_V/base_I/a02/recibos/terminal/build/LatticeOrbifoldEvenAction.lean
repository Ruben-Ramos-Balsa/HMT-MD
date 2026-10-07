import LatticeOrbifoldBlocks
import LatticeTwistedPositiveStateDescent

/-! The actual even lattice states act on both already constructed sectors.
Both fields use the unramified coordinate z.  No undetermined mixed product
is replaced by zero: the source of this action is only the even subspace.
The remaining two products are exposed separately for the later assembly.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeOrbifoldEvenAction

open LatticeEvenVertexFields LatticeEvenTranslation LatticeEvenLocality
open LatticeTwistedPositiveSector LatticeTwistedPositiveStateDescent
open LatticeOrbifoldCarrier

def coefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    Module.End ℂ (Space o) :=
  (evenCoefficient o u k).prodMap
    (HVertexOperator.coeff (positiveDescendedAssignment o u) k)

theorem coefficient_apply (o : Fin 12) (u : evenSpace o) (v : Space o) (k : ℤ) :
    coefficient o u k v =
      (evenCoefficient o u k v.1,
       HVertexOperator.coeff (positiveDescendedAssignment o u) k v.2) := rfl

theorem coefficient_bounded (o : Fin 12) (u : evenSpace o) (v : Space o) :
    ∃ b : ℤ, ∀ k < b, coefficient o u k v = 0 := by
  obtain ⟨a, ha⟩ := evenCoefficient_laurent_bound o u v.1
  obtain ⟨b, hb⟩ := positiveDescendedCoefficient_bounded o u v.2
  refine ⟨min a b, fun k hk => ?_⟩
  apply Prod.ext
  · exact ha k (lt_of_lt_of_le hk (min_le_left _ _))
  · exact hb k (lt_of_lt_of_le hk (min_le_right _ _))

def field (o : Fin 12) (u : evenSpace o) : VertexOperator ℂ (Space o) :=
  VertexOperator.of_coeff (coefficient o u) (coefficient_bounded o u)

theorem field_coefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (field o u) k = coefficient o u k := rfl

def assignment (o : Fin 12) :
    evenSpace o →ₗ[ℂ] VertexOperator ℂ (Space o) where
  toFun := field o
  map_add' u v := by
    apply HVertexOperator.coeff_inj
    funext k
    apply LinearMap.ext
    intro w
    change coefficient o (u+v) k w = coefficient o u k w + coefficient o v k w
    apply Prod.ext
    · change HVertexOperator.coeff (evenStateField o (u+v)) k w.1 =
        HVertexOperator.coeff (evenStateField o u) k w.1 +
        HVertexOperator.coeff (evenStateField o v) k w.1
      simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
    · change HVertexOperator.coeff (positiveDescendedAssignment o (u+v)) k w.2 =
        HVertexOperator.coeff (positiveDescendedAssignment o u) k w.2 +
        HVertexOperator.coeff (positiveDescendedAssignment o v) k w.2
      simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
  map_smul' c u := by
    apply HVertexOperator.coeff_inj
    funext k
    apply LinearMap.ext
    intro w
    change coefficient o (c • u) k w = c • coefficient o u k w
    apply Prod.ext
    · change HVertexOperator.coeff (evenStateField o (c • u)) k w.1 =
        c • HVertexOperator.coeff (evenStateField o u) k w.1
      simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply, LinearMap.smul_apply]
    · change HVertexOperator.coeff (positiveDescendedAssignment o (c • u)) k w.2 =
        c • HVertexOperator.coeff (positiveDescendedAssignment o u) k w.2
      simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply, LinearMap.smul_apply]

theorem assignment_coefficient (o : Fin 12) (u : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (assignment o u) k = coefficient o u k := rfl

theorem even_inclusion (o : Fin 12) (u v : evenSpace o) (k : ℤ) :
    HVertexOperator.coeff (assignment o u) k (v, 0) =
      (HVertexOperator.coeff (evenStateField o u) k v, 0) := by
  change (evenCoefficient o u k v,
    HVertexOperator.coeff (positiveDescendedAssignment o u) k 0) = _
  rw [map_zero]
  rfl

theorem positive_inclusion (o : Fin 12) (u : evenSpace o) (v : positiveSector o)
    (k : ℤ) :
    HVertexOperator.coeff (assignment o u) k (0, v) =
      (0, HVertexOperator.coeff (positiveDescendedAssignment o u) k v) := by
  change (evenCoefficient o u k 0, _) = _
  rw [map_zero]
  rfl

theorem vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (assignment o (evenVacuum o)) k =
      if k=0 then (1 : Module.End ℂ (Space o)) else 0 := by
  apply LinearMap.ext
  intro v
  rw [assignment_coefficient, coefficient_apply, evenCoefficient_vacuum,
    positiveDescent_vacuum_coefficient]
  by_cases hk : k=0
  · simp only [if_pos hk, LinearMap.id_apply, Module.End.one_apply]
  · simp only [if_neg hk, LinearMap.zero_apply]
    rfl

theorem creation (o : Fin 12) (u : evenSpace o) :
    HVertexOperator.coeff (assignment o u) 0 (vacuum o) = (u, 0) := by
  rw [vacuum, even_inclusion]
  congr 1
  exact (evenField_creates o u).2

theorem negative_vacuum (o : Fin 12) (u : evenSpace o) (k : ℤ) (hk : k<0) :
    HVertexOperator.coeff (assignment o u) k (vacuum o) = 0 := by
  rw [vacuum, even_inclusion, evenStateField_apply, (evenField_creates o u).1 k hk]
  rfl

theorem assignment_injective (o : Fin 12) : Function.Injective (assignment o) := by
  intro u v h
  have hc := congrArg (fun F => (HVertexOperator.coeff F 0 (vacuum o)).1) h
  simpa only [creation] using hc

/-- Only the two products with twisted source remain arguments. -/
structure RemainingFields (o : Fin 12) where
  te : positiveSector o →ₗ[ℂ] HVertexOperator ℤ ℂ (evenSpace o) (positiveSector o)
  tt : positiveSector o →ₗ[ℂ] HVertexOperator ℤ ℂ (positiveSector o) (evenSpace o)

def completeWith (o : Fin 12) (M : RemainingFields o) :
    LatticeOrbifoldBlocks.MixedFields o where
  et := positiveDescendedAssignment o
  te := M.te
  tt := M.tt

set_option maxHeartbeats 1200000 in
theorem completeWith_even_source (o : Fin 12) (M : RemainingFields o)
    (u : evenSpace o) :
    LatticeOrbifoldBlocks.stateField o (completeWith o M) (u,0) = assignment o u := by
  apply HVertexOperator.coeff_inj
  funext k
  apply LinearMap.ext
  intro v
  rw [LatticeOrbifoldBlocks.coefficient_formula, assignment_coefficient, coefficient_apply]
  change (evenCoefficient o u k v.1 + HVertexOperator.coeff (M.tt 0) k v.2,
    HVertexOperator.coeff (positiveDescendedAssignment o u) k v.2 +
      HVertexOperator.coeff (M.te 0) k v.1) = _
  rw [map_zero, map_zero]
  have he : HVertexOperator.coeff
      (0 : HVertexOperator ℤ ℂ (positiveSector o) (evenSpace o)) k v.2 = 0 := rfl
  have ht : HVertexOperator.coeff
      (0 : HVertexOperator ℤ ℂ (evenSpace o) (positiveSector o)) k v.1 = 0 := rfl
  rw [he, ht, add_zero, add_zero]

theorem completeWith_even_twisted (o : Fin 12) (M : RemainingFields o)
    (u : evenSpace o) (v : positiveSector o) (k : ℤ) :
    HVertexOperator.coeff (LatticeOrbifoldBlocks.stateField o (completeWith o M) (u,0)) k
      (0,v) = (0, HVertexOperator.coeff (positiveDescendedAssignment o u) k v) := by
  rw [completeWith_even_source, positive_inclusion]

end HMT.IV.LatticeOrbifoldEvenAction
end
