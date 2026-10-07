import MarkedNeighborFinite

/-!
The integer rank of the marked neighbour is deduced from two explicit
injective integer-linear maps. The lower map is the same triple-glue
inclusion that generates the previously proved rational full span.
No rank, determinant, lattice classification or real topology is assumed.
-/
namespace HMT.IV.NeighborRank

open HMT.IV.CoxeterNeighbor HMT.IV.NeighborSpan HMT.IV.NeighborLattice

def integerPoint {n : ℕ} (x : Fin n → ℤ × ℤ) : Space n :=
  fun i => ((x i).1, (x i).2)

theorem integerPoint_mem_glue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (x : Fin n → ℤ × ℤ) :
    integerPoint x ∈ glue C :=
  integer_coordinates_mem_glue C (fun i => (x i).1) (fun i => (x i).2)

noncomputable def tripleIntegerMap {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (hC : IntegralGlue C) (t : Fin n → ℤ) :
    (Fin n → ℤ × ℤ) →ₗ[ℤ] NeighborModule C t where
  toFun x := ⟨(3 : ℚ) • integerPoint x,
    kernel_mem_neighbor C (radial t)
      (triple_glue_mem_kernel C (radial t) hC
        (HMT.IV.NeighborSpan.radial_mem_glue C t) (integerPoint_mem_glue C x))⟩
  map_add' := by
    intro x y
    apply Subtype.ext
    funext i
    ext <;> simp [integerPoint] <;> ring
  map_smul' := by
    intro k x
    apply Subtype.ext
    funext i
    ext <;> simp [integerPoint] <;> ring

theorem tripleIntegerMap_injective {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (hC : IntegralGlue C) (t : Fin n → ℤ) :
    Function.Injective (tripleIntegerMap C hC t) := by
  intro x y h
  funext i
  apply Prod.ext
  · have hi := congrArg (fun z : NeighborModule C t => ((z : Space n) i).1) h
    change (3 : ℚ) * ((x i).1 : ℚ) = 3 * ((y i).1 : ℚ) at hi
    apply Int.cast_injective (α := ℚ)
    linarith
  · have hi := congrArg (fun z : NeighborModule C t => ((z : Space n) i).2) h
    change (3 : ℚ) * ((x i).2 : ℚ) = 3 * ((y i).2 : ℚ) at hi
    apply Int.cast_injective (α := ℚ)
    linarith

theorem neighbor_integer_rank_upper {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) :
    Module.finrank ℤ (NeighborModule C t) ≤ 2 * n := by
  have h := (integralCoordinateMap C t).finrank_le_finrank_of_injective
    (integralCoordinateMap_injective C t)
  simpa [Module.finrank_pi_fintype, Module.finrank_prod, mul_comm] using h

theorem neighbor_integer_rank_lower {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (hC : IntegralGlue C) (t : Fin n → ℤ) :
    2 * n ≤ Module.finrank ℤ (NeighborModule C t) := by
  letI := neighbor_module_finite C t
  have h := (tripleIntegerMap C hC t).finrank_le_finrank_of_injective
    (tripleIntegerMap_injective C hC t)
  simpa [Module.finrank_pi_fintype, Module.finrank_prod, mul_comm] using h

theorem neighbor_integer_rank {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (hC : IntegralGlue C) (t : Fin n → ℤ) :
    Module.finrank ℤ (NeighborModule C t) = 2 * n :=
  Nat.le_antisymm (neighbor_integer_rank_upper C t) (neighbor_integer_rank_lower C hC t)

theorem witt_marked_integer_rank (o : Fin 12) :
    Module.finrank ℤ (neighborSubgroup wittCode (radial (marked o))) = 24 :=
  neighbor_integer_rank wittCode witt_glue_integral (marked o)

theorem witt_marked_integer_and_rational_ranks (o : Fin 12) :
    Module.finrank ℤ (neighborSubgroup wittCode (radial (marked o))) =
      Module.finrank ℚ (Submodule.span ℚ (neighbor wittCode (radial (marked o)))) := by
  rw [witt_marked_integer_rank, witt_marked_rational_dimension]

#print axioms integerPoint_mem_glue
#print axioms tripleIntegerMap
#print axioms tripleIntegerMap_injective
#print axioms neighbor_integer_rank_upper
#print axioms neighbor_integer_rank_lower
#print axioms neighbor_integer_rank
#print axioms witt_marked_integer_rank
#print axioms witt_marked_integer_and_rational_ranks

end HMT.IV.NeighborRank
